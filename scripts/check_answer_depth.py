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

Rule 2 (2026-09-21, the chapter sweep): the same table-only failure mode
exists in study chapters — a `## Definition` that is a bare comparison
table (four found: hash-tables, auth-fundamentals, and two 20.9 chapters
written the same week) or a diagram with no definitional prose. Chapters
(non-bank, non-INDEX files) must carry at least CHAPTER_DEFINITION_FLOOR
prose words in their Definition section. The title-plus-code genres
(Best Practices; the numbered mechanism sections that before 2026-10-21 sat
under `## How It Works`) are deliberately NOT gated: their explanations live
in the headings and annotated code — measured and decided at rule birth, not
silently skipped.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prose_scan
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', 'vendor', '_site', '.archive', 'personal'}
ANSWER_FLOOR = 25  # prose words; tables/code don't count (see module docstring)
CHAPTER_DEFINITION_FLOOR = 25  # prose words in a chapter's `## Definition`
# Chapter sweep scope mirrors check_template's exempt prefixes; contributing
# and readme are meta docs whose Definitions define terms, not topics.
CHAPTER_EXEMPT_PREFIXES = ('80-lanes-abroad-full-stack', '81-lanes-indian-sde-faang',
                           'projects', 'docs')
META_FILENAMES = {'contributing.md', 'readme.md'}

QUESTION_RX = re.compile(r"^###\s+Q(?:uestion)?\.?\s*\d+", re.I)
SECTION_RX = re.compile(r"^##\s+")

# Classification lives in prose_scan.py — the single owner of
# "what counts as reasoning prose" (tables/headings/quotes/badges excluded,
# fence-aware via md_fences). The gate owns only the floors and the
# question/section topology. Pinned semantics in test_prose_scan.py.


def prose_words(segment):
    """Count prose words in a question segment (classification: prose_scan)."""
    return prose_scan.prose_words(segment)


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


def check_definition(path, rel):
    """Return (line_no, words) if a chapter's `## Definition` is sub-floor."""
    name = os.path.basename(path).lower()
    if name in META_FILENAMES or name == 'index.md' or 'interview' in name:
        return None
    top = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if top.startswith(CHAPTER_EXEMPT_PREFIXES):
        return None
    with open(path, encoding='utf-8') as fh:
        lines = fh.read().splitlines()
    for i, l in enumerate(lines):
        if re.match(r'^##\s+Definition\b', l, re.I):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if re.match(r'^##\s+', lines[j]):
                    end = j
                    break
            words = prose_words(lines[i + 1:end])
            if words < CHAPTER_DEFINITION_FLOOR:
                return (i + 1, words)
            return None
    return None


def main():
    floor = ANSWER_FLOOR
    if '--floor' in sys.argv:
        floor = int(sys.argv[sys.argv.index('--floor') + 1])

    problems = []
    checked = 0
    def_checks = 0
    n_files = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith('.md'):
                continue
            n_files += 1
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            if 'interview-questions' in name:
                checked += 1
                for line_no, heading, words in check_file(path):
                    problems.append(
                        f"{rel}:{line_no}: answer has {words} prose words "
                        f"(floor {floor}) — \"{heading[:70]}\"\n"
                        f"    Add the why: mechanism, trade-off, or the failure "
                        f"the table can't show. Tables and code don't count."
                    )
            else:
                hit = check_definition(path, rel)
                if hit is not None:
                    def_checks += 1
                    line_no, words = hit
                    problems.append(
                        f"{rel}:{line_no}: `## Definition` carries only {words} "
                        f"prose words (floor {CHAPTER_DEFINITION_FLOOR})\n"
                        f"    A definition must say what the thing IS before the "
                        f"table enumerates it — add the mechanism prose."
                    )

    # Zero banks means the walk found nothing (see scan_scope): "every answer
    # >= 25 prose words" over an empty set is a vacuous pass, and a walk that
    # missed the banks would report exactly that.
    guard(n_files, 'markdown files', ROOT)
    guard(checked, 'interview banks', ROOT)

    if problems:
        print(f"ANSWER DEPTH FAIL — {len(problems)} problem(s): answers below "
              f"{floor} prose words across {checked} interview banks, plus "
              f"sub-floor chapter Definitions:\n")
        for p in problems:
            print(p)
        return 1
    print(f"answer depth OK — {checked} interview banks (every answer "
          f">= {floor} prose words) and all chapter Definitions "
          f">= {CHAPTER_DEFINITION_FLOOR} prose words")
    return 0


if __name__ == '__main__':
    sys.exit(main())
