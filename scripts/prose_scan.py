#!/usr/bin/env python3
"""Reasoning-prose scanner — the single owner of "what counts as prose".

Born 2026-09-21: the prose-word logic existed as copy-pasted snippets in
survey scripts before being centralized here, the same one-owner rule that
`md_fences` applied to fence parsing. Consumers:

  - `check_answer_depth.py` (gate 19): interview answers and chapter
    `## Definition` sections must carry >= 25 prose words;
  - any future survey measuring reasoning depth.

`read_time.py` deliberately does NOT use this module. Its model answers a
different question — reading *weight* (code lines cost ~1/25 min each,
table rows ~1/40) — while this module answers "is there reasoning here"
(code and tables carry none of the why). The two classifiers look similar
and must not be merged; that boundary is a recorded decision, not an
accident of history.

Classification contract (each rule pinned in test_prose_scan.py):

  - Fence-awareness always comes from `md_fences.walk` — never a naive
    toggle. Fence delimiter lines and everything inside a block are
    excluded, including nested fences (a ``` line inside a ```` block is
    content, and content inside a block is never prose).
  - Tables (`|...`) are enumeration, not explanation — excluded. This is
    the rule that caught the 27 table-only interview answers: counting
    table words let a comparison table pass as depth.
  - Headings, blockquotes, `---` separators, HTML comments and shields
    badges are structure or navigation — excluded. (A blockquote *fence*
    — `> ``` — is a known md_fences limitation; harmless here because
    blockquote lines are skipped anyway.)
  - Inline code inside prose counts as words (naive `str.split`); the
    corpus writes "`npm ci` installs" and the floor measures the sentence,
    backticks included. Pinned as-is so the gate and the corpus never
    disagree about the definition of a word.
"""
import md_fences

# Lines that never count as reasoning prose. Tables are the point (the
# table-only defect class); badges/comments/quotes are navigation or
# decoration; `---` is a separator; headings are structure.
SKIP_PREFIXES = ('|', '#', '>', '---', '<!--', '[!', '![')


def prose_lines(lines):
    """Yield stripped prose lines: outside fences, not table/heading/quote/badge."""
    for _i, line, in_fence, is_fence_line in md_fences.walk(lines):
        if in_fence or is_fence_line:
            continue
        s = line.strip()
        if not s or s.startswith(SKIP_PREFIXES):
            continue
        yield s


def prose_words(lines):
    """Total reasoning-prose word count over an iterable of lines."""
    return sum(len(s.split()) for s in prose_lines(lines))
