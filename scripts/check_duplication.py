#!/usr/bin/env python3
"""Near-duplicate section detector: find chapters that teach the same thing.

The "every topic lives in exactly ONE place" rule is only as good as the
tooling behind it — the chaos-engineering duplication grew to ~250
overlapping lines because nothing measured overlap.

Method:
  1. Split each content file into `##` sections (fence-aware).
  2. Drop the template/cross-reference sections (TL;DR, First Principles,
     Definition, Summary, Cheat Sheet, See Also, References, Interview
     Questions) — those are *supposed* to resemble each other.
  3. Shingle the surviving prose (5-word shingles, code fences excluded),
     into a set per section.
  4. Report cross-file section pairs over a Jaccard threshold, plus
     intra-file near-duplicates.

Exit 0 with a report (advisory by default); `--strict` exits 1 when a pair
exceeds --threshold. Sections under --min-words are ignored so a short
paragraph cannot trip it on its own.

Usage:
  python3 scripts/check_duplication.py                    # report
  python3 scripts/check_duplication.py --strict --threshold 0.35
"""
import argparse
import os
import re
import sys
from collections import defaultdict
import md_fences

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal', 'docs', '.freebuff'}
SKIP_FILES = {'INDEX.md', 'README.md', 'AGENTS.md', 'contributing.md', 'ROADMAP.md', 'search.md'}
EXEMPT_PREFIXES = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang', 'projects')

# Sections that are template scaffolding or navigation: expected to be similar
# across files, so they are not duplication.
TEMPLATE_SECTIONS = {
    'TL;DR', 'First Principles', 'Definition', 'Summary', 'Cheat Sheet',
    'See Also', 'References & Learn More', 'Interview Questions',
    'Interview Tips', 'Common Mistakes', 'Best Practices',
    'Performance Considerations', 'Real-World Use Cases', 'Why It Matters',
    'Why Do We Need It?', '30-Second Interview Version', 'Table of Contents',
}
VARIANTS = {
    'why it matters (tldr)': 'Why It Matters',
    'why it matters (tl;dr)': 'Why It Matters',
    'why this matters': 'Why It Matters',
    'references': 'References & Learn More',
}

FENCE = re.compile(r'^\s*(```|~~~)')
HEAD = re.compile(r'^## (.+?)\s*$')
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'\-]+")
SHINGLE = 5


def normalize(name):
    return VARIANTS.get(name.strip().lower(), name.strip())


def sections(path):
    """Yield (name, prose) for non-template `##` sections."""
    lines = open(path, encoding='utf-8').read().split('\n')
    cur, buf, in_fence, out = None, [], False, []
    for _, line, in_fence, is_fence in md_fences.walk(lines):
        if is_fence:
            if cur is not None:
                buf.append('')          # fence content is not prose
            continue
        m = HEAD.match(line) if not in_fence else None
        if m:
            if cur is not None:
                out.append((cur, ' '.join(buf)))
            cur, buf = normalize(m.group(1)), []
            continue
        if cur is not None and not in_fence:
            buf.append(line)
    if cur is not None:
        out.append((cur, ' '.join(buf)))
    return [(n, p) for n, p in out if n not in TEMPLATE_SECTIONS]


def shingles(text):
    w = [t.lower() for t in WORD.findall(text)]
    if len(w) < SHINGLE:
        return set(), len(w)
    return {tuple(w[i:i + SHINGLE]) for i in range(len(w) - SHINGLE + 1)}, len(w)


def iter_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        rel = os.path.relpath(root, ROOT)
        if rel.startswith(EXEMPT_PREFIXES):
            continue
        for f in sorted(files):
            if f.endswith('.md') and f not in SKIP_FILES and 'interview' not in f.lower():
                yield os.path.join(root, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--threshold', type=float, default=0.35)
    ap.add_argument('--min-words', type=int, default=80)
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()

    index = defaultdict(list)      # shingle -> [(file, section)]
    section_sets = {}              # (file, section) -> set
    for path in iter_files():
        rel = os.path.relpath(path, ROOT)
        for name, prose in sections(path):
            sh, nwords = shingles(prose)
            if nwords < args.min_words or not sh:
                continue
            key = (rel, name)
            section_sets[key] = sh
            for s in sh:
                index[s].append(key)

    # Count shared shingles per section pair, then Jaccard.
    pair_hits = defaultdict(int)
    for keys in index.values():
        if len(keys) < 2 or len(keys) > 60:
            continue
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                if keys[i][0] == keys[j][0]:
                    continue
                pair_hits[(keys[i], keys[j])] += 1

    findings = []
    for (a, b), hits in pair_hits.items():
        union = len(section_sets[a]) + len(section_sets[b]) - hits
        if union <= 0:
            continue
        jac = hits / union
        if jac >= args.threshold:
            findings.append((jac, a, b))
    findings.sort(reverse=True)

    print(f"scanned {len(section_sets)} non-template sections across "
          f"{len({k[0] for k in section_sets})} files")
    if not findings:
        print(f"no cross-file section pairs at or above Jaccard {args.threshold}")
        return 0

    print(f"\nDUPLICATE-RISK PAIRS ({len(findings)}) at Jaccard >= {args.threshold}:")
    for jac, a, b in findings:
        print(f"  {jac:.2f}  {a[0]} :: '{a[1]}'")
        print(f"        {b[0]} :: '{b[1]}'")
    return 1 if args.strict else 0


if __name__ == '__main__':
    sys.exit(main())
