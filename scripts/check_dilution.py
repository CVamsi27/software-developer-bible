#!/usr/bin/env python3
"""Prose dilution — a chapter must not restate itself, locked to a baseline.

The 2026-09-22 audit measured the recurring reader complaint ("the corpus
repeats itself and buries its main point") instead of assuming it, over the 776
chapter files, and the answer was zero on every axis:

  - adjacent-sentence restatement (Jaccard >= 0.34 on 4-word shingles, both
    sides >= 8 content words): 0
  - the partial band a reader would still notice (0.20-0.34): 0
  - intra-chapter near-duplicate paragraphs (Jaccard >= 0.40 on 5-word
    shingles, at least 20 lines apart): 0
  - TL;DR-vs-Summary overlap: median 0.00, no chapter above 0.25

This gate makes that measurement standing rather than historical. It is a
*ceiling* baseline, not a floor like the First-Principles one: the committed
`dilution-baseline.json` holds the maximum allowed hit count per class, the
gate fails when a class exceeds it, and `--baseline` re-baselines deliberately
(say why in the commit). Improvement below the ceiling needs no action.

Relationship to the neighbours: gate 11 (`check_duplication.py --strict`) owns
*cross-chapter* copying over `##` bodies; this owns *within-chapter* repetition
at sentence granularity — the "same point made twice in one chapter" class that
a cross-file shingle scan cannot see because the files differ.

Scope is the corpus proper: numbered stack directories, `personal/` excluded at
any depth (canonical personal data, not a chapter a reader studies), and
`docs/`/root meta excluded because the measured baseline was taken there.
Lists, tables, quotes and fences are excluded — they are enumerations, the same
reasoning-prose doctrine `prose_scan.py` applies for gate 19. `## Revision
Questions` bodies (2026-09-30) are excluded too: retrieval practice *by design*
restates the chapter's own facts one line after the question, so measuring that
section for restatement would penalise the template itself — the exclusion is
for the section, not for the answers elsewhere.

Check-only by design: a hit is an editorial problem (merge the two passages or
cut one), not a mechanical repair, so there is no `--write`.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'dilution-baseline.json')
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'api', '_site', '.archive', '__pycache__',
             '.jekyll-cache', 'scripts'}
EXCLUDE_PATH = re.compile(r'(^|/)personal/')

ADJACENT_J, ADJACENT_MIN_WORDS, ADJACENT_N = 0.34, 8, 4
INTRA_J, INTRA_MIN_GAP, INTRA_N = 0.40, 20, 5

SPAN = re.compile(r'(`+)(.+?)\1', re.S)
LINK = re.compile(r'\[([^\]]*)\]\([^)]*\)')
STOP = set("""a an the and or but if then than that this these those of in on at
to for from with without by as is are was were be been being it its their there
here you your we our they them not no nor so such can could may might must
shall should will would do does did done have has had having also more most
much many few some any each every both all one two three other another only own
same very just about into over under again further once during before after
above below up down out off because while when where why how what which who
whom""".split())


def prose_blocks(path):
    """[(block_index, [(lineno, text)])] — heading-delimited prose runs."""
    with open(path, encoding='utf-8') as handle:
        lines = handle.read().split('\n')
    blocks, current, in_rq = [], [], False
    for i, line, in_fence, is_fence in md_fences.walk(lines):
        if is_fence or in_fence:
            continue
        stripped = line.strip()
        if m := re.match(r'^(#{2,6})\s+(.*)$', stripped):
            if current:
                blocks.append(current)
            current = []
            # Only a level-2 heading enters/leaves the RQ section, so its
            # optional `###` group labels stay inside the exclusion.
            if len(m.group(1)) == 2:
                in_rq = m.group(2).strip() == 'Revision Questions'
            continue
        if in_rq:
            continue
        if not stripped or stripped.startswith(('|', '<', '[![', '!', '>', '-',
                                                '*', '```')):
            continue
        current.append((i + 1, stripped))
    if current:
        blocks.append(current)
    return blocks


def words(text):
    """Content words: link labels kept, code spans and stopwords dropped."""
    return [w.lower() for w in
            re.findall(r"[A-Za-z][A-Za-z'-]+", SPAN.sub(' ', LINK.sub(r'\1', text)))
            if w.lower() not in STOP and len(w) > 2]


def shingles(ws, n):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def adjacent_hits(blocks):
    """[(lineno, jaccard)] — a sentence that restates the one before it."""
    hits = []
    for rows in blocks:
        for (_, prev), (lineno, text) in zip(rows, rows[1:]):
            wp, wc = words(prev), words(text)
            if len(wp) < ADJACENT_MIN_WORDS or len(wc) < ADJACENT_MIN_WORDS:
                continue
            sp, sc = shingles(wp, ADJACENT_N), shingles(wc, ADJACENT_N)
            if not sp or not sc:
                continue
            union = len(sp | sc)
            if union and len(sp & sc) / union >= ADJACENT_J:
                hits.append((lineno, len(sp & sc) / union))
    return hits


def intra_hits(rows):
    """[(lineno_a, lineno_b)] — two passages >= min_gap lines apart that share
    >= INTRA_J of their shingles. Inverted index, so a clean corpus costs one
    pass instead of an all-pairs comparison."""
    postings, sets = {}, {}
    for idx, (lineno, text) in enumerate(rows):
        w = words(text)
        if len(w) < INTRA_N + 3:
            continue
        s = shingles(w, INTRA_N)
        if len(s) < 2:
            continue
        sets[idx] = s
        for t in s:
            postings.setdefault(t, []).append(idx)
    hits, seen = [], set()
    for idx, s in sets.items():
        candidates = set()
        for t in s:
            candidates.update(postings[t])
        for other in candidates:
            if other <= idx:
                continue
            pair = (idx, other)
            if pair in seen:
                continue
            if abs(rows[other][0] - rows[idx][0]) < INTRA_MIN_GAP:
                continue
            seen.add(pair)
            union = len(s | sets[other])
            if union and len(s & sets[other]) / union >= INTRA_J:
                hits.append((rows[idx][0], rows[other][0]))
    return hits


def measure(files):
    adjacent, intra = [], []
    for rel in files:
        blocks = prose_blocks(os.path.join(ROOT, rel))
        for lineno, j in adjacent_hits(blocks):
            adjacent.append(f'{rel}:{lineno}: restates the previous sentence '
                            f'(J={j:.2f} >= {ADJACENT_J})')
        flat = [row for block in blocks for row in block]
        for a, b in intra_hits(flat):
            intra.append(f'{rel}:{a}+{b}: two passages {INTRA_MIN_GAP}+ lines '
                         f'apart share >= {INTRA_J} of their shingles')
    return adjacent, intra


def load_baseline():
    with open(BASELINE, encoding='utf-8') as handle:
        return json.load(handle)


def main():
    rebaseline = '--baseline' in sys.argv
    files = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            if not name.endswith('.md'):
                continue
            rel = os.path.relpath(os.path.join(base, name), ROOT)
            if re.match(r'\d\d-', rel) and not EXCLUDE_PATH.search(rel):
                files.append(rel)
    files.sort()
    guard(len(files), 'chapter files')

    adjacent, intra = measure(files)
    if rebaseline:
        with open(BASELINE, 'w', encoding='utf-8') as handle:
            json.dump({
                'measured': '2026-09-22, re-baseline deliberately',
                'scope': 'numbered stacks, personal/ excluded',
                'adjacent_restatement_max': len(adjacent),
                'intra_chapter_duplicate_max': len(intra),
            }, handle, indent=2)
            handle.write('\n')
        print(f'baseline written: {len(adjacent)} adjacent restatement(s), '
              f'{len(intra)} intra-chapter duplicate(s) over {len(files)} files')
        return 0

    limits = load_baseline()
    problems = []
    if len(adjacent) > limits['adjacent_restatement_max']:
        problems += adjacent
    if len(intra) > limits['intra_chapter_duplicate_max']:
        problems += intra
    if problems:
        for problem in problems[:30]:
            print(f'  {problem}')
        print(f'\nDILUTION — {len(problems)} restatement(s) exceed the baseline '
              f'(adjacent max {limits["adjacent_restatement_max"]}, intra max '
              f'{limits["intra_chapter_duplicate_max"]}). Merge the passages or '
              f'cut one; if the new passage is genuinely a distinct treatment, '
              f're-baseline deliberately: python3 scripts/check_dilution.py --baseline')
        return 1
    print(f'prose dilution OK — {len(files)} chapter files, '
          f'{len(adjacent)} adjacent restatement(s) '
          f'(max {limits["adjacent_restatement_max"]}), '
          f'{len(intra)} intra-chapter duplicate(s) '
          f'(max {limits["intra_chapter_duplicate_max"]})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
