#!/usr/bin/env python3
"""Cross-file duplicate code examples — ceiling baseline, like gate 25.

The 2026-09-23 audit asked the last unmeasured dilution question: do chapters
re-teach each other's *code* (not prose)? Two detectors over fenced code
blocks, cross-file only (same-file repetition is usually deliberate contrast):

  - identical: raw-text identical bodies (>= 10 lines) in different files
  - near: word/identifier profiles with Jaccard >= 0.80 across files
    (identifiers and string content kept — the first prototype that dropped
    strings scored prose-disguised-as-code blocks as duplicates; strings ARE
    the content of config-literal examples)

The audit found 11 real re-teaches (the FilteredList anti-pattern in three
React chapters, the revalidate endpoint in three Next.js chapters, memoize(),
ObjectPool, Apollo loading states, generic const/let BPs duplicated between
the scope and hoisting chapters) — all trimmed to one-line pointers at their
canonical home. The remaining pairs are recorded keeps in the health report:
deliberate contrasts (debounce vs throttle, ISR vs static export), interview
recaps, and project-doc compilations.

Ceiling baseline (`code-dup-baseline.json`): the gate fails when a class
exceeds its committed maximum, so a *new* copy of an existing example fails
the build even while old keeps stay stable. `--baseline` re-commits
deliberately. Check-only: removing a duplicate is an editorial decision.

Relationship to neighbours: gate 11 owns cross-chapter prose copying over
`##` bodies; check_dilution.py owns within-chapter prose at sentence
granularity; this owns cross-file *code* blocks.
"""
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'code-dup-baseline.json')
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'api', '_site', '.archive', '__pycache__',
             '.jekyll-cache', 'scripts'}
EXCLUDE_PATH = re.compile(r'(^|/)personal/')

FENCE_OPEN = re.compile(r'^```(\w[\w+-]*)\s*$')
FENCE_CLOSE = re.compile(r'^```\s*$')
# Languages where a config/prose literal is plausible content (not exhaustive —
# the near-detector is profile-based anyway; identical needs >= 10 lines).
CODE_LANGS = {'js', 'javascript', 'ts', 'typescript', 'python', 'py', 'go',
              'java', 'tsx', 'jsx', 'sql', 'bash', 'sh'}

MIN_LINES_IDENTICAL = 10
MIN_LINES_NEAR = 10
NEAR_J = 0.80
MIN_TOKENS = 30

STR = re.compile(r'"([^"\n]{4,})"|\'([^\'\n]{4,})\'')
IDENT = re.compile(r'\b[A-Za-z_]\w{3,}\b')
COMMENT = re.compile(r'//[^\n]*|#[^\n]*|/\*.*?\*/', re.S)


def corpus_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, ROOT)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for n in filenames:
            if not n.endswith('.md'):
                continue
            p = os.path.join(rel, n) if rel != '.' else n
            if EXCLUDE_PATH.search(p):
                continue
            out.append(os.path.normpath(p))
    return sorted(out)


def fenced_blocks(path):
    """(open_line_1indexed, lang, raw_body) for every closed fence."""
    try:
        lines = open(os.path.join(ROOT, path), encoding='utf-8').read().split('\n')
    except OSError:
        return []
    blocks, i = [], 0
    while i < len(lines):
        m = FENCE_OPEN.match(lines[i])
        if m:
            j = i + 1
            while j < len(lines) and not FENCE_CLOSE.match(lines[j]):
                j += 1
            body = lines[i + 1:j]
            if body and j < len(lines):
                blocks.append((i + 1, m.group(1).lower(),
                               '\n'.join(body).strip()))
            i = j + 1
        else:
            i += 1
    return blocks


def profile(src):
    words = []
    for a, b in STR.findall(src):
        words += (a or b).lower().split()
    words += [t.lower() for t in IDENT.findall(src)]
    return Counter(words)


def jaccard(a, b):
    keys = set(a) | set(b)
    inter = sum(min(a.get(k, 0), b.get(k, 0)) for k in keys)
    union = sum(max(a.get(k, 0), b.get(k, 0)) for k in keys)
    return inter / union if union else 0.0


def find_hits():
    """Returns ({'identical': [desc...], 'near': [desc...]}, blocks_scanned).

    'identical' counts PAIRS, not groups: two files sharing a body are one
    defect; five files sharing it are ten — a copy-paste that spreads should
    raise the count and trip the ceiling even though the text never changed.
    """
    hits = {'identical': [], 'near': []}
    scanned = 0  # every fenced code-language block — the scope floor's unit
    raw = {}
    prof = []
    for path in corpus_files():
        for ln, lang, body in fenced_blocks(path):
            nlines = body.count('\n') + 1
            if lang not in CODE_LANGS:
                continue
            scanned += 1
            if nlines >= MIN_LINES_IDENTICAL:
                raw.setdefault(body, []).append((path, ln, nlines))
            if nlines >= MIN_LINES_NEAR:
                p = profile(COMMENT.sub(' ', body))
                if sum(p.values()) >= MIN_TOKENS:
                    prof.append((path, ln, nlines, p))

    for body, locs in sorted(raw.items()):
        locs.sort(key=lambda l: (l[0], l[1]))
        for i in range(len(locs)):
            for j in range(i + 1, len(locs)):
                a, b = locs[i], locs[j]
                hits['identical'].append(
                    f"{a[0]}:{a[1]} ({a[2]}L) == {b[0]}:{b[1]} ({b[2]}L); "
                    f"first line: {body.splitlines()[0][:70]!r}")

    for i in range(len(prof)):
        fa, la, na, pa = prof[i]
        for j in range(i + 1, len(prof)):
            fb, lb, nb, pb = prof[j]
            if fb == fa:
                continue
            if jaccard(pa, pb) >= NEAR_J:
                hits['near'].append(
                    f"{fa}:{la} ({na}L) ~ {fb}:{lb} ({nb}L)")
    return hits, scanned


def main():
    args = sys.argv[1:]
    write_baseline = '--baseline' in args

    hits, scanned = find_hits()
    guard(scanned, 'code blocks scanned', str(ROOT))
    counts = {k: len(v) for k, v in hits.items()}

    if write_baseline:
        with open(BASELINE, 'w', encoding='utf-8') as f:
            json.dump(counts, f, indent=2, sort_keys=True)
            f.write('\n')
        print(f"baseline written: {counts}")
        return 0

    baseline = json.load(open(BASELINE, encoding='utf-8'))
    problems = []
    for cls in ('identical', 'near'):
        if counts[cls] > baseline.get(cls, 0):
            problems.append(
                f"{cls}: {counts[cls]} > ceiling {baseline.get(cls, 0)}")
            problems.extend(f"  [{cls}] {d}" for d in hits[cls])

    if problems:
        print("PROBLEMS (duplicate code examples above ceiling):")
        for p in problems:
            print(f"  {p}")
        print("Fix by trimming the copy to a pointer at its canonical home,")
        print("or re-baseline deliberately with --baseline (say why in the commit).")
        return 1

    print(f"OK: duplicate-code classes within ceiling "
          f"(identical {counts['identical']}/{baseline.get('identical', 0)}, "
          f"near {counts['near']}/{baseline.get('near', 0)})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
