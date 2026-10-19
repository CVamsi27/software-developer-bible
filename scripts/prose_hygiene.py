#!/usr/bin/env python3
"""Prose hygiene — reader-visible defects no other gate owns.

Six classes. Rules 1–4 were measured before this tool's first line was written
(2026-09-22 audit over 867 markdown files); rules 5–6 record two construction
defects a 2026-10-19 spacing pass found across the same corpus and repaired.

  Rule 1 — spelling consistency. The corpus is American-English by an
overwhelming margin: `behavior` 845 occurrences against `behaviour` 26,
`optimize` 197 against 0 `optimise`, `while` 403 against 0 `whilst`. Thirteen
pairs still carried *both* forms, so a reader met `behaviour` in one chapter
and `behavior` in the next — 62 instances of the minority form. Pairs where the
corpus is internally consistent (`cancelled` 25 / `canceled` 0) or genuinely
split (`grey` 3 / `gray` 4, both settled jargon in their own literature) are
deliberately NOT covered: a rule may only enforce a convention the corpus
already follows, or it fires on the corpus as it is and buries its signal.

  Rule 2 — an ATX heading with no space after the hashes. CommonMark requires
the space, so `##管道和重定向` is not a heading at all: it renders as literal
text and the section it was meant to introduce loses its structure. Exactly one
instance existed, and it is a *rendering break* rather than a style preference,
which is why it is gated despite being a singleton class — the rule cannot
false-positive on a real heading.

  Rule 3 — a GFM table row whose cell count differs from its header's. GFM
splits on `|` *before* inline parsing, so an unescaped pipe inside a code span
(`| `==` vs `===`, `??` vs `||` |`) silently breaks the cell grid: the row
renders with extra columns and the table stops lining up. Two rows, both from
that exact cause; the fix escapes the pipes inside the span, which GFM renders
as the literal character.

  Rule 4 — empty discourse filler. A separate pass measured whether the corpus
dilutes its own points, and the answer was no on every axis: adjacent-sentence
restatement was **0** at Jaccard >= 0.34 over the 776 chapter files, the partial
band (0.20-0.34) was **0**, intra-chapter near-duplicate paragraphs were **0**,
and TL;DR-to-Summary overlap had a **median of 0.00** (no chapter above 0.25) —
the template's "repeated" sections genuinely carry different content. The one
residue worth keeping is why that holds: none of the eighteen empty openers
below appears anywhere in the corpus. They are gated so the property cannot
regress by accident. Two phrases a naive list would include are deliberately
NOT listed, because this corpus uses them for real work: `essentially` (10 uses,
every one a precise comparison — "this is essentially Strategy + a coordinator")
and `the fact that` (6 uses, every one a causal derivation — "the amortized O(n)
bound comes from the fact that each element is pushed exactly once"). A rule
that fired on those would be a rule against technical prose.

Rule 4 is the one finding `--write` cannot repair: deleting a phrase from a
sentence produces worse prose than the phrase did, so the run reports it and
exits non-zero for the author to rewrite.

  Rule 5 — a heading or `---` thematic break with no blank line above it,
directly under list content. Kramdown reads the line as part of the list item:
`---` becomes a setext underline, so the reference above it turns into an `<h2>`
inside the `<li>` and the separator disappears (286 files, every references
footer built this way), and `## References & Learn More` is absorbed into the
last See Also item together with the entire references list (66 files).
Measured 2026-10-19 as 352 instances in 304 files.

  Rule 6 — an otherwise-tight list whose item boundaries are blank-separated in
isolated places. Kramdown wraps exactly the items above those blanks in `<p>`,
so their gap is 18px against 5.4px neighbours: one list, two rhythms. All 104
separators in 96 files (measured 2026-10-19) were artifacts of the kind of edit
that adds an item and a trailing blank.

Every rule is prose-only: fenced code, inline code spans, link targets, bare
URLs, HTML tags and the file-metadata comment are masked before matching, so a
CSS `color:` or a `colour` inside a URL is never touched. Masking preserves
character offsets, so a match can be repaired in place. Rules 5–6 are
structural instead: they read fence-aware raw lines and repair by inserting or
deleting a whole blank line, which is idempotent because a repaired file no
longer matches.

This tool is both the fixer and the gate, matching fix_nav_labels.py:

--check  exit 1 listing every finding (the gate; a clean corpus prints one OK)
--write  repair in place (idempotent; prose spans + blank-line structure)

Scope excludes `personal/` at any depth by recorded decision: that tree is
canonical personal data and campaign copy, not a chapter a reader studies.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'api', '_site', '.archive', '__pycache__',
             '.jekyll-cache', 'scripts', 'node_modules'}
EXCLUDE_PATH = re.compile(r'(^|/)personal/')

# ---------------------------------------------------------------------------
# Rule 1: the spelling convention the corpus already follows.
#
# Every pair is (minority form, canonical form, the measured evidence). The
# list is closed: a new pair is a new defect and fails until someone records
# why the direction is what it is. The canonical side is never the one the
# corpus uses less — `cancelled`, used 25 times with zero `canceled`, is
# consistent and therefore absent, not wrong.
# ---------------------------------------------------------------------------
VOCAB = [
    ('behaviour', 'behavior', 'behavior 845 / behaviour 26'),
    ('defence', 'defense', 'defense 138 / defence 7'),
    ('colour', 'color', 'color 117 / colour 5'),
    ('modelling', 'modeling', 'modeling 126 / modelling 8'),
    ('serialise', 'serialize', 'serialize 79 / serialise 4'),
    ('recognise', 'recognize', 'recognize 35 / recognise 5'),
    ('acknowledgement', 'acknowledgment', 'acknowledgment 18 / acknowledgement 4'),
    ('labelled', 'labeled', 'labeled 15 / labelled 2'),
    ('catalogue', 'catalog', 'catalog 86 / catalogue 1'),
    ('judgement', 'judgment', 'judgment 95 / judgement 1'),
]

# Terms that contain a minority spelling but must not be "corrected", each with
# the reason. A blanket word rule cannot know these; naming them is the point.
EXEMPT_TERMS = [
    (re.compile(r'Colour Contrast Analyser'),
     'the TPGi tool\'s registered name (tpgi.com/color-contrast-checker)'),
    (re.compile(r'aria-labelledby'),
     'an HTML attribute identifier — "labeledby" would name nothing'),
    (re.compile(r'IT Consultant Defence'),
     'a company\'s own role title (Materna Berlin)'),
    (re.compile(r'Sopra Steria Defence'),
     'that division\'s own name (Sopra Steria Defence & Security)'),
]

META_LINE = re.compile(r'^\s*<!--\s*section:')
HTML_COMMENT = re.compile(r'<!--.*?-->', re.S)
CODE_SPAN = re.compile(r'(`+)(.+?)\1', re.S)
LINK_TARGET = re.compile(r'\]\(\s*[^)]*\)')
BARE_URL = re.compile(r'<?https?://[^\s)>]+')
HTML_TAG = re.compile(r'</?[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?>')

HEADING_NO_SPACE = re.compile(r'^(#{1,6})([^#\s])')

# Rules 5–6 read list and block structure instead of prose spans.
LIST_ITEM = re.compile(r'^(?:[-*+] |\d+\. )')
STARTER_UNDER_LIST = re.compile(r'^(?:#{1,6} |---\s*$)')
BLOCK_BOUNDARY = re.compile(r'^(?:#{1,6} |```|> |\||<[A-Za-z/!])')

# Empty register: phrases that assert nothing and carry no technical claim,
# none of which the corpus uses today (measured 2026-09-22). Cheaper to keep
# out than to hunt later — and the list stays short and unambiguous on purpose.
FILLER_OPENERS = [
    'it is important to note', 'it is important to remember',
    'it should be noted', 'it is worth noting', 'it is worth mentioning',
    'needless to say', 'it goes without saying', 'at the end of the day',
    'as we can see', 'as you can see', "let's dive into", 'let us dive into',
    'dive deep into', "in today's fast-paced", 'in this day and age',
    'for all intents and purposes', 'last but not least', 'first and foremost',
]


def mask(line):
    """The same line with every non-prose span blanked, offsets preserved.

    Replacing spans with equal-length runs of spaces (never deleting them) is
    what lets a rule match on the masked text and repair on the real one.
    """
    if META_LINE.match(line):
        return ' ' * len(line)
    out = line
    for pattern in (HTML_COMMENT, CODE_SPAN, LINK_TARGET, BARE_URL, HTML_TAG):
        out = pattern.sub(lambda m: ' ' * (m.end() - m.start()), out)
    return out


def match_case(source, replacement):
    """`Behaviour` -> `Behavior`, `BEHAVIOUR` -> `BEHAVIOR`."""
    if source.isupper() and len(source) > 1:
        return replacement.upper()
    if source[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def find_spelling(masked, line):
    """(start, end, replacement, note) for every minority-form occurrence."""
    found = []
    for variant, canonical, evidence in VOCAB:
        pattern = re.compile(rf'\b{variant}\w*', re.I)
        for m in pattern.finditer(masked):
            if any(x.search(line, max(0, m.start() - 40), m.end() + 40)
                   for x, _ in EXEMPT_TERMS):
                continue
            # Swap the stem only, so inflections follow: behaviours ->
            # behaviors, recognised -> recognized, serialises -> serializes.
            word = m.group(0)
            stem = canonical + word[len(variant):] if word.lower().startswith(variant) \
                else canonical
            found.append((m.start(), m.end(), match_case(word, stem), evidence))
    return found


def find_filler(masked):
    """Empty discourse phrases in a line of prose. Check-only (see rule 4)."""
    low = masked.lower()
    return [phrase for phrase in FILLER_OPENERS if phrase in low]


def find_heading(line):
    """Insert the missing space *between* the hashes and the text.

    Anchoring on the matched text instead (m.end()) put the space after its
    first character — `##管道` became `##管 道` — and left the line still
    matching, so every `--write` run added another space. Insertion at the
    boundary is what makes the repair idempotent, which gate 22 requires.
    """
    m = HEADING_NO_SPACE.match(line)
    if not m:
        return None
    return (m.start(2), m.start(2), ' ', 'an ATX heading needs a space before its text')


def table_rows(lines):
    """(index, header_cells, [(line_index, cells, unescaped_pipes)]) per table."""
    tables, block = [], []
    for i, line, in_fence, is_fence in md_fences.walk(lines):
        if in_fence or is_fence:
            if block:
                tables.append(block)
                block = []
            continue
        stripped = re.sub(r'^\s*>?\s*', '', line)
        if stripped.startswith('|') and stripped.rstrip().endswith('|'):
            block.append((i, line))
        elif block:
            tables.append(block)
            block = []
    if block:
        tables.append(block)
    for table in tables:
        if len(table) < 2:
            continue
        _, header = table[0]
        yield header, table


def cells(line):
    """Cell count the way GFM counts them: split on every unescaped pipe."""
    stripped = re.sub(r'^\s*>?\s*', '', line)
    body = stripped.strip()
    if not body.startswith('|'):
        return 0, []
    pipes = [m.start() for m in re.finditer(r'(?<!\\)\|', body)]
    return len(pipes) - 1, pipes


def after_list_content(lines, i, in_fence_state):
    """True when line i sits directly under list content (no blank line).

    The walk back over a paragraph's continuation lines stops at any block
    starter, so a heading that merely follows a paragraph is not mistaken for
    content hanging off a list.
    """
    j = i - 1
    if j < 0 or not lines[j].strip() or in_fence_state[j]:
        return False
    if LIST_ITEM.match(lines[j]):
        return True
    while j >= 0 and lines[j].strip() and not in_fence_state[j] \
            and not LIST_ITEM.match(lines[j]) and not BLOCK_BOUNDARY.match(lines[j]):
        j -= 1
    return j >= 0 and bool(LIST_ITEM.match(lines[j]))


def mixed_list_separators(lines, in_fence_state):
    """Indices of stray blank separators inside an otherwise-tight list.

    Only a boundary made entirely of blank lines is a "blank separator"; a
    blank followed by an indented continuation paragraph is item content and
    is ignored. A fully blank-separated list is a deliberate style and is left
    alone — the defect is the mixed list, where kramdown renders only some
    items loose and the reader sees one gap at three times the rhythm.
    """
    found = []
    i, n = 0, len(lines)
    while i < n:
        if in_fence_state[i] or not LIST_ITEM.match(lines[i]):
            i += 1
            continue
        items = [i]
        j = i + 1
        while j < n:
            if in_fence_state[j]:
                break
            if LIST_ITEM.match(lines[j]):
                items.append(j)
                j += 1
            elif not lines[j].strip():
                k = j
                while k < n and not in_fence_state[k] and not lines[k].strip():
                    k += 1
                if k < n and not in_fence_state[k] and LIST_ITEM.match(lines[k]):
                    items.append(k)
                    j = k + 1
                else:
                    break
            elif BLOCK_BOUNDARY.match(lines[j]):
                break
            else:
                j += 1        # continuation line of the current item
        if len(items) >= 3:
            boundaries = list(zip(items, items[1:]))
            blank = [(a, b) for a, b in boundaries
                     if lines[a + 1:b] and all(not l.strip() for l in lines[a + 1:b])]
            if blank and len(blank) < len(boundaries):
                for a, b in blank:
                    found.extend(range(a + 1, b))
        i = items[-1] + 1
    return found


def main():
    write = '--write' in sys.argv
    files = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in names:
            if name.endswith('.md'):
                rel = os.path.relpath(os.path.join(base, name), ROOT)
                if not EXCLUDE_PATH.search(rel):
                    files.append(rel)
    files.sort()
    guard(len(files), 'markdown files')

    findings, unfixable, repaired = [], [], 0
    for rel in files:
        path = os.path.join(ROOT, rel)
        with open(path, encoding='utf-8') as handle:
            lines = handle.read().split('\n')
        edits = {}          # line index -> list of (start, end, replacement)
        inserts = {}        # line index -> note (a blank line goes above it)
        deletes = {}        # line index -> note (a stray blank separator)
        notes = {}          # line index -> list of notes
        in_fence_state = [False] * len(lines)
        for i, line, in_fence, is_fence in md_fences.walk(lines):
            in_fence_state[i] = in_fence or is_fence

        for i, line in enumerate(lines):
            if in_fence_state[i]:
                continue
            if line.lstrip().startswith('|') or re.match(r'^\s*>\s*\|', line):
                continue                      # tables: rule 3 owns them
            masked = mask(line)
            for start, end, replacement, note in find_spelling(masked, line):
                edits.setdefault(i, []).append((start, end, replacement))
                notes.setdefault(i, []).append(f'spelling: {line[start:end]} -> '
                                               f'{replacement}  ({note})')
            head = find_heading(line)
            if head:
                start, end, replacement, note = head
                edits.setdefault(i, []).append((start, end, replacement))
                notes.setdefault(i, []).append(f'heading: {note}')
            for phrase in find_filler(masked):
                note = (f'filler: {phrase!r} asserts nothing — state the claim '
                        f'directly (rule 4 cannot be auto-repaired)')
                notes.setdefault(i, []).append(note)
                unfixable.append(f'{rel}:{i + 1}: {note}')

        # Rule 3 — table cell counts, measured against each table's own header.
        for header, table in table_rows(lines):
            want, _ = cells(header)
            if want < 2:
                continue
            for i, line in table[1:]:
                if re.match(r'^\s*>?\s*\|[\s:|-]+\|\s*$', line):
                    continue                  # the |---|---| separator row
                got, _ = cells(line)
                if got != want:
                    notes.setdefault(i, []).append(
                        f'table: {got} cells against a {want}-cell header '
                        f'(an unescaped `|` inside a cell splits it in GFM)')
                    # Repair: escape the pipes that sit inside inline code spans.
                    for m in CODE_SPAN.finditer(line):
                        for pipe in re.finditer(r'(?<!\\)\|', m.group(2)):
                            index = m.start(2) + pipe.start()
                            edits.setdefault(i, []).append((index, index, '\\'))

        # Rule 5 — a heading or thematic break directly under list content.
        for i, line in enumerate(lines):
            if in_fence_state[i] or not STARTER_UNDER_LIST.match(line):
                continue
            if after_list_content(lines, i, in_fence_state):
                note = ('block: this heading/thematic break sits directly under list '
                        'content — kramdown reads it as part of the item (a `---` '
                        'becomes a setext heading over the item); a blank line '
                        'restores the block')
                inserts[i] = note
                notes.setdefault(i, []).append(note)

        # Rule 6 — isolated blank separators inside an otherwise-tight list.
        for i in mixed_list_separators(lines, in_fence_state):
            note = ('list: a blank line separates items here while the rest of the '
                    'list is tight — kramdown renders exactly these items loose, so '
                    'one gap is 3x its neighbours')
            deletes[i] = note
            notes.setdefault(i, []).append(note)

        if notes:
            for i in sorted(notes):
                for note in notes[i]:
                    findings.append(f'{rel}:{i + 1}: {note}')
        if write and (edits or inserts or deletes):
            for i, spans in edits.items():
                line = lines[i]
                for start, end, replacement in sorted(spans, reverse=True):
                    line = line[:start] + replacement + line[end:]
                lines[i] = line
            # Rebuild once on the original line indices, so an insert and a
            # delete never have to account for each other's index shifts.
            rebuilt = []
            for idx, line in enumerate(lines):
                if idx in inserts:
                    rebuilt.append('')
                if idx not in deletes:
                    rebuilt.append(line)
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write('\n'.join(rebuilt))
            repaired += 1

    if findings:
        for finding in findings:
            print(f'  {finding}')
    if write:
        print(f'{repaired} file(s) repaired across {len(files)} markdown file(s)')
        # A writer that cannot repair a finding must still fail the run: an
        # operator reading "N repaired" would otherwise never learn that a
        # filler phrase was reported and left in place.
        if unfixable:
            print(f'{len(unfixable)} finding(s) need a rewrite by hand — '
                  f'rule 4 is check-only')
            return 1
    elif findings:
        print(f'\n{len(findings)} finding(s) in {len(files)} markdown file(s) — '
              f'run: python3 scripts/prose_hygiene.py --write')
        return 1
    else:
        print(f'prose hygiene OK — {len(files)} markdown file(s), '
              f'{len(VOCAB)} spelling pairs, {len(FILLER_OPENERS)} empty openers, '
              f'no findings')
    return 0


if __name__ == '__main__':
    sys.exit(main())
