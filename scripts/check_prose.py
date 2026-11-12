#!/usr/bin/env python3
"""Mechanical prose gate — grammar defects a reader sees and a regex can prove.

`prose_hygiene.py` already owns spelling convention, heading spacing, table
cells, filler phrases and blank-line structure. It deliberately does NOT own
word-level grammar, and nothing else did either: a duplicated word, a doubled
space between words, a sentence run together with the next one, a space before
a comma, or `a hour` all render exactly as typed. Those classes are
*determinable* — the correct form is never a matter of voice — which is what
separates this gate from the judgment calls an editor makes.

Seven classes, each measured against the corpus before being gated (see
`docs/2026-11-quality-rubric.md` for the rubric this serves):

  P1  a word repeated twice in a row ................ "the the request"
  P2  two or more spaces between words .............. "the  request"
  P3  no space after a sentence-final period ........ "retry.Next"
  P4  space before a comma, semicolon or colon ...... "timeout , retry"
  P5  a doubled comma or semicolon .................. "retry,, then"
  P6  the wrong indefinite article .................. "a hour", "an user"
  P7  an odd number of bold markers on one line ..... "**retry policy"

Every rule is prose-only. Lines are passed through `prose_hygiene.mask()`
before matching, so fenced code is skipped entirely and inline code, link
targets, bare URLs, HTML tags and the metadata comment are blanked while
character offsets are preserved. That is what lets P1-P5 be repaired in place.

P6 and P7 are report-only. `a`/`an` depends on the *sound* of the next word
(`a URL` is right, `an URL` is wrong; `an hour` is right, `a hour` is wrong),
so the rule only fires on a closed list of words whose pronunciation is not in
dispute, and even then a wrong repair is worse than a report. An odd `**`
count can legitimately open a bold run that closes on the next line, so it is
reported for a human to look at rather than rewritten.

Usage:
  python3 scripts/check_prose.py            # the gate: exit 1 on any finding
  python3 scripts/check_prose.py --write    # repair P1-P5 in place (idempotent)
  python3 scripts/check_prose.py --json     # machine-readable findings

Scope excludes `personal/` at any depth, matching `prose_hygiene.py`.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import prose_hygiene
from scan_scope import guard  # noqa: E402  (masking contract + skip list, one owner)

ROOT = os.path.dirname(HERE)
SKIP_DIRS = prose_hygiene.SKIP_DIRS
EXCLUDE_PATH = prose_hygiene.EXCLUDE_PATH

# ---------------------------------------------------------------------------
# Rules. Each entry is (code, title, pattern, repair) where `repair` is either
# a callable taking the match and returning the replacement text, or None for
# report-only rules.
# ---------------------------------------------------------------------------

# P1 — a word repeated twice. The lookbehind rejects a hyphenated or pathed
# first word, because `server-side side effects`, `Retry-After after` and
# `per-order order` are correct English, not stutters — three of the four
# original hits were exactly that shape. The floor of three letters keeps
# `a a` and `I I` out of scope: both are more likely to be a table cell or a
# quoted fragment than prose.
REPEATED_WORD = re.compile(r'(?<![\w/.-])\b([A-Za-z]{3,})\s+\1\b', re.I)

# P2 — two spaces between words. The lookbehind requires the run to start after
# a non-space character and the lookahead requires a word character after it, so
# leading indentation, list nesting, and alignment padding at line start are all
# out of scope. Trailing double spaces are `check_code_whitespace.py`'s subject
# only inside fences; prose trailing space is invisible to a reader and not
# gated here.
DOUBLE_SPACE = re.compile(r'(?<=[A-Za-z0-9,.;:)\]"\'])([ \t]{2,})(?=[A-Za-z0-9(\["\'])')

# P3 — a sentence run together. Requires at least two lowercase letters, a
# period, then a capitalised word of three or more letters: `e.g. This` has no
# lowercase-dot-capital sequence, `Node.js` fails the capital requirement, and
# `v1.2` fails the lowercase requirement. Version strings and file extensions
# are therefore out of scope by construction rather than by allowlist.
MISSING_SPACE = re.compile(r'(?<=[a-z]{2})\.(?=[A-Z][a-z]{2,})')

# P4 — a space before punctuation that never takes one in running prose. The
# captured group is the *whitespace*, so the repair deletes it; capturing the
# punctuation instead left the space in place (caught by the test suite).
SPACE_BEFORE_PUNCT = re.compile(r'(?<=[A-Za-z0-9)\]"\'])([ \t]+)(?=[,;:])')

# P5 — a doubled comma or semicolon. Only the mark itself: a bare `..` was in
# this rule until calibration found **14** legitimately double-dotted spans
# (`1..n`, `-128..127`, a router's `..` path step), every one of them correct.
# Range notation is common enough in this corpus that the dot rule could only
# ever have produced noise.
DOUBLE_PUNCT = re.compile(r'([,;])\1')

# P6 — indefinite article against a closed pronunciation list. Words are
# grouped by the *first sound*, not the first letter: `hour`/`honest`/`heir`
# begin with a vowel sound and take `an`, while `user`/`union`/`one`/`euro`
# begin with a consonant sound and take `a`. Acronyms are excluded entirely
# (`an API`, `a URL`, `an HTML` all depend on how the author reads them).
VOWEL_SOUND = r'(hour|honest|honor|heir|honour)'
CONSONANT_SOUND = (r'(user|users|usable|usage|union|unique|uniform|unit|unary|'
                   r'universal|university|utility|utilities|euro|european|'
                   r'one|once|ubiquitous|usual|useful)')
WRONG_A = re.compile(rf'\ba\s+({VOWEL_SOUND})\b', re.I)
WRONG_AN = re.compile(rf'\ban\s+({CONSONANT_SOUND})\b', re.I)

# P7 — an odd number of bold markers in one paragraph. Counting per line was
# wrong: `**text` may close on the next line (a valid emphasis run over a soft
# break), and `apps/web/**` is a glob, not emphasis. Both shapes produced all
# 32 original hits, so the rule reads a whole paragraph and strips glob forms
# first.
BOLD = re.compile(r'\*\*')
# A paragraph that uses glob syntax is exempt: `**projects/**` is a bold run
# whose closing marker is also a glob's `**`, so no marker count can separate
# the two uses. Every one of the 32 original P7 hits was this shape.
GLOB = re.compile(r'\*\*/|(?<=[A-Za-z0-9._-])/\*\*')

# code -> (title, pattern, repair mode)
#
# The repair mode is explicit rather than a callable per rule: `repair_line`
# needs to know which character a rule wants kept, and making that a string
# keeps the decision readable and testable.
RULES = {
    'P1': ('word repeated twice', REPEATED_WORD, 'keep-group-1'),
    'P2': ('two or more spaces between words', DOUBLE_SPACE, 'single-space'),
    'P3': ('no space after a sentence-final period', MISSING_SPACE, 'insert-after-dot'),
    'P4': ('space before punctuation', SPACE_BEFORE_PUNCT, 'delete-span'),
    'P5': ('duplicated punctuation', DOUBLE_PUNCT, 'drop-duplicate'),
    'P6': ('wrong indefinite article', None, 'report-only'),
    'P7': ('odd number of bold markers', None, 'report-only'),
}

REPAIRABLE = {'P1', 'P2', 'P3', 'P4', 'P5'}

SENTINEL = '\x00'


def mask_prose(line):
    """`prose_hygiene.mask()`, then make every masked span opaque.

    The shared masker blanks non-prose spans with spaces, which is right for
    rules that only need to know *whether* text is prose. A grammar rule needs
    more: `use `code`, then` must not read as the double space in
    `use  , then`, and a code span between two words must not look like a
    repeated word. Replacing each blanked character that masked real text with
    a sentinel keeps the offsets (so repairs still apply to the raw line) while
    making every rule stop at the span boundary.
    """
    masked = prose_hygiene.mask(line)
    if len(masked) != len(line):
        return masked
    return ''.join(SENTINEL if (m == ' ' and l != ' ') else m
                   for l, m in zip(line, masked))


def iter_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if not name.endswith('.md'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            if EXCLUDE_PATH.search(rel.replace(os.sep, '/')):
                continue
            yield path, rel


def scan_line(masked, raw):
    """Findings for one line as (code, start, end, text)."""
    out = []
    for code in ('P1', 'P2', 'P3', 'P4', 'P5'):
        _title, pattern, _repair = RULES[code]
        for m in pattern.finditer(masked):
            out.append((code, m.start(), m.end(), raw[m.start():m.end()]))
    for m in WRONG_A.finditer(masked):
        out.append(('P6', m.start(), m.end(), 'a ' + m.group(1)))
    for m in WRONG_AN.finditer(masked):
        out.append(('P6', m.start(), m.end(), 'an ' + m.group(1)))
    return out


def paragraph_has_unbalanced_bold(paragraph):
    """True when a paragraph's emphasis markers never pair up."""
    text = SENTINEL.join(paragraph)
    if GLOB.search(text):
        return False
    return len(BOLD.findall(text)) % 2 == 1


def repair_line(line, masked):
    """Apply the P1-P5 repairs to one line, left to right, idempotently."""
    # Collect repair spans from the masked line, then rewrite the raw line.
    spans = []
    for code in ('P1', 'P2', 'P3', 'P4', 'P5'):
        _title, pattern, mode = RULES[code]
        for m in pattern.finditer(masked):
            if mode == 'keep-group-1':
                spans.append((m.start(), m.end(), m.group(1)))
            elif mode == 'single-space':
                spans.append((m.start(), m.end(), ' '))
            elif mode == 'insert-after-dot':
                # the match starts at the period; insert the space after it
                spans.append((m.start() + 1, m.start() + 1, ' '))
            elif mode == 'delete-span':
                spans.append((m.start(1), m.end(1), ''))
            elif mode == 'drop-duplicate':
                spans.append((m.start(), m.end(), m.group(1)))
    if not spans:
        return line
    spans.sort()
    out, cursor = [], 0
    for start, end, text in spans:
        if start < cursor:          # overlapping earlier repair — skip
            continue
        out.append(line[cursor:start])
        out.append(text)
        cursor = end
    out.append(line[cursor:])
    return ''.join(out)


def scan_file(path):
    findings = []
    with open(path, encoding='utf-8', errors='replace') as fh:
        lines = fh.read().split('\n')
    in_fence = False
    paragraph = []
    paragraph_line = 0
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            if paragraph:
                if paragraph_has_unbalanced_bold(paragraph):
                    findings.append((paragraph_line, 'P7', 'unbalanced ** in paragraph'))
                paragraph = []
            continue
        masked = mask_prose(line)
        # A table row is not running prose: pipes are syntax, and cell padding
        # legitimately uses repeated spaces.
        if masked.lstrip().startswith('|'):
            continue
        if masked.lstrip().startswith('#'):
            continue
        if not paragraph:
            paragraph_line = number
        paragraph.append(masked)
        for code, start, end, text in scan_line(masked, line):
            findings.append((number, code, text.replace(SENTINEL, '')))
    if paragraph and paragraph_has_unbalanced_bold(paragraph):
        findings.append((paragraph_line, 'P7', 'unbalanced ** in paragraph'))
    return findings, lines


def main():
    write = '--write' in sys.argv
    as_json = '--json' in sys.argv
    total = 0
    per_rule = {code: 0 for code in RULES}
    payload = {}
    files = list(iter_files())
    # Gate 23's discipline: a prose gate that found no files has not certified
    # the prose, and its verdict would read the same if the walk broke.
    guard(len(files), 'markdown files')
    for path, rel in files:
        findings, lines = scan_file(path)
        if not findings:
            continue
        total += len(findings)
        for _number, code, _text in findings:
            per_rule[code] += 1
        payload[rel] = [{'line': n, 'rule': c, 'text': t} for n, c, t in findings]
        if write:
            changed = False
            in_fence = False
            for index, line in enumerate(lines):
                if line.lstrip().startswith('```'):
                    in_fence = not in_fence
                    continue
                if in_fence or not line.strip() or line.lstrip().startswith('|'):
                    continue
                new = repair_line(line, mask_prose(line))
                if new != line:
                    lines[index] = new
                    changed = True
            if changed:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write('\n'.join(lines))

    if as_json:
        print(json.dumps({'total': total, 'per_rule': per_rule, 'files': payload}, indent=1))
        return 1 if total and not write else 0

    if write:
        print(f"check_prose: repaired {total} finding(s) across "
              f"{len(payload)} file(s); P6/P7 are report-only")
        return 0
    if not total:
        print("check_prose: no mechanical prose defects")
        return 0
    for rel in sorted(payload):
        for item in payload[rel][:6]:
            print(f"  {rel}:{item['line']}: {item['rule']} {item['text']!r}")
        extra = len(payload[rel]) - 6
        if extra > 0:
            print(f"  {rel}: … and {extra} more")
    summary = ', '.join(f"{c}={n}" for c, n in per_rule.items() if n)
    print(f"check_prose: {total} finding(s) in {len(payload)} file(s) — {summary}")
    return 1


if __name__ == '__main__':
    sys.exit(main())
