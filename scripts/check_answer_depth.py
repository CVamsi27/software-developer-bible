#!/usr/bin/env python3
"""Interview answer-depth gate (gate 22).

The interview banks were completed to a *quantity* standard (a >=25-question
floor, gate 6b) long before anything measured whether the **answers** were
real. The 2026-09-21 answer-quality arc deepened 247 answers across 11 banks,
and the follow-up probe found the residue its own scanner had masked:
**table-only answers** — a comparison table with zero reasoning prose (the
arc's scanner counted table words, so a `| Aspect | ... |` block plus one
`**Answer:**` line read as "healthy"). Tables enumerate; they don't explain
the why. 27 such answers existed across 6 banks the day this gate was written.

This gate makes the property permanent: every answer must carry at least
ANSWER_FLOOR words of *prose* — lines outside code fences, minus tables,
headings, blockquotes, separators, badges, and HTML comments. Code, tables,
and lists may accompany an answer but cannot substitute for the reasoning
around them.

Scanner contract (learned the hard way, twice, in the arc):
  - Fence-awareness comes from `md_fences.walk` — never a naive toggle.
  - Question headings in the wild: `### Q3:`, `### Q12.`, `### Question 3:`,
    `### Question 12:` — one regex covers all; the digit is required so an
    overview box like `### Question Categories` never matches (that exact
    false positive burned the manual scans).
  - An answer spans from its question heading to the next question heading
    or the next `##` section — so trailing See Also content can't inflate
    the last answer's count.
  - `**30-sec:**` rapid-fire answers and `**Senior answer**:` variants count
    their prose like any other — format labels are not special-cased, only
    measured.

Banks whose questions aren't `### Q...` headings (e.g. bold-line formats)
are out of contract; none exist in the corpus today (checked at gate birth).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal'}
ANSWER_FLOOR = 25  # prose words; tables/code don't count (see module docstring)

QUESTION_RX = re.compile(r"^###\s+Q(?:uestion)?\.?\s*\d+", re.I)
SECTION_RX = re.compile(r"^##\s+")

# Lines that never count as answer prose. Tables are the point (the
# table-only defect class); badges/comments/quotes are navigation or
# decoration; `---` is a separator.
SKIP_PREFIXES = ('|', '#', '>', '---', '<!--', '[!', '![')


def prose_words(segment):
    """Count prose words in a question segment, fence- and table-aware."""
    words = 0
    for _i, line, in_fence, is_fence_line in md_fences.walk(segment):
        if in_fence or is_fence_line:
            continue
        s = line.strip()
        if not s or s.startswith(SKIP_PREFIXES):
            continue
        words += len(s.split())
    return words


def check_file(path):
    """Return [(line_no, heading, words)] for sub-floor answers in one file."""
    with open(path, encoding='utf-8') as fh:
        lines = fh.read().splitlines()
    heads = [i for i, l in enumerate(lines) if QUESTION_RX.match(l)]
    if not heads:
        return []
    fails = []
    for n, start in enumerate(heads):
        # Answer extends to the next question heading or the next `##` section.
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if SECTION_RX.match(lines[j]) or (j in heads):
                end = j
                break
        words = prose_words(lines[start + 1:end])
        if words < ANSWER_FLOOR:
            fails.append((start + 1, lines[start].lstrip('# ').strip(), words))
    return fails


def main():
    floor = ANSWER_FLOOR
    if '--floor' in sys.argv:
        floor = int(sys.argv[sys.argv.index('--floor') + 1])

    problems = []
    checked = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith('.md') or 'interview-questions' not in name:
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            checked += 1
            for line_no, heading, words in check_file(path):
                problems.append(
                    f"{rel}:{line_no}: answer has {words} prose words "
                    f"(floor {floor}) — \"{heading[:70]}\"\n"
                    f"    Add the why: mechanism, trade-off, or the failure "
                    f"the table can't show. Tables and code don't count."
                )

    if problems:
        print(f"ANSWER DEPTH FAIL — {len(problems)} answer(s) below "
              f"{floor} prose words across {checked} interview banks:\n")
        for p in problems:
            print(p)
        return 1
    print(f"answer depth OK — {checked} interview banks, every answer "
          f"carries >= {floor} prose words")
    return 0


if __name__ == '__main__':
    sys.exit(main())
