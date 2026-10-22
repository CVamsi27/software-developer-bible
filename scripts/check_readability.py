#!/usr/bin/env python3
"""Readable outline — the section headings must carry the argument, not a label.

Born 2026-10-21 from a side-by-side read: a generated answer about `let` versus
`var` against this corpus's own chapter on the same topic. The generated answer
read better, and the difference was measurable rather than mystical:

  * its opening states the claim first ("comes down to a mix of historical
    backward compatibility and modern architectural safety"), then develops it —
    this corpus already does that: 504 of 521 chapter openings contain a
    declarative answer sentence;
  * every one of its headings names a step of the argument — "The Historical
    Accident of `var` and `globalThis`" — while 500 of 738 chapter files filed
    the entire mechanism under the identical generic pair
    `## How It Works` + `### 1. ...`, `### 2. ...`;
  * its paragraphs lead with the load-bearing term in bold and annotate the
    code with the *why*, which the house style already prescribes
    (docs/readability-standard.md).

So the gap was one thing, and it was structural: a chapter's outline is its
table of contents, its summary of the argument and its in-page navigation (the
reading rail in assets/reading-ui.js is built from `h2[id]`). Under one label,
five chapters outline as "How It Works, How It Works, How It Works"; the reader
cannot see what each chapter argues before reading it. AGENTS.md already says
so in its own words: use short, topic-specific headings that carry the
explanation forward, and do not make every chapter follow the same sequence of
generic headings.

The repair is mechanical because the specific headings already exist — they are
the `### N. Title` children. This tool removes the generic umbrella and promotes
its children to `##`, so a chapter outlines as its own argument:

    ## How It Works            ->   ## 1. The Four Scope Levels
    ### 1. The Four Scope Levels      ## 2. Lexical Resolution and Shadowing
    ### 2. Lexical Resolution ...     ## 3. Comparing Declaration Boundaries

Measured before the first line was written (2026-10-21): 488 in-scope chapters
carry the umbrella (504 files corpus-wide, the rest interview banks, guides and
meta docs outside this gate's scope); 21 carry a lead-in paragraph under the
umbrella, which is relocated under the first promoted heading so no sentence
changes owner silently; 0 have `####` grandchildren (so no heading jumps a
level); 0 in-scope files use `### Q` steps (interview banks keep their own
template and are out of scope). Zero incoming `#how-it-works` anchors exist in
the repository, so removing the label breaks no link; heading slugs are
generated from the title text, so promoting a heading preserves its anchor.

Rules (learning chapters only — numbered stacks, personal/api/docs/meta, INDEX,
REVISION, interview banks, cheat sheets, trackers, case studies and multi-`#`
guide files excluded):

  1. no retired generic heading (`How It Works`, `Explanation`, `Overview`,
     `Details`, `Key Points`, `Deep Dive`, `In Depth`, `Mechanism`);
  2. no numbered mechanism step left under a retired umbrella — the same
     defect seen from the child's side.

Usage:
  python3 scripts/check_readability.py            # gate: exit 1 with violations
  python3 scripts/check_readability.py --write     # repair in place (idempotent)
  python3 scripts/check_readability.py --report    # corpus shape, per-rule counts
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_fences
from scan_scope import guard

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '_site', 'node_modules', '.archive', 'vendor', '__pycache__',
             '.jekyll-cache', 'personal', 'api', 'scripts', 'docs', '.github'}
EXCLUDE_PATH = re.compile(r'(^|/)personal/')
GENERIC = {'how it works', 'explanation', 'overview', 'details', 'key points',
           'deep dive', 'in depth', 'mechanism'}
UMBRELLA = 'how it works'

H2_RX = re.compile(r'^(#{2})\s+(.+?)\s*$')
H1_RX = re.compile(r'^#\s+(?!#)(.+?)\s*$')
NUM_STEP_RX = re.compile(r'^###\s+\d+[.)]\s+\S')


def is_guide_file(text):
    """Multi-`# Phase` role guides use their own outline (contributing.md)."""
    phase = 0
    for _, line, in_fence, _ in md_fences.walk(text.splitlines()):
        if in_fence:
            continue
        if line.startswith('# ') and (line[2:].lstrip().startswith('Phase')
                                      or line[2:].lstrip().startswith('Part')):
            phase += 1
    return phase >= 2


def iter_chapters():
    """[(rel, abs_path)] — learning chapters this gate owns."""
    files = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if not name.endswith('.md'):
                continue
            rel = os.path.relpath(os.path.join(base, name), ROOT)
            if not re.match(r'\d\d-', rel) or EXCLUDE_PATH.search(rel):
                continue
            low = name.lower()
            if low in ('index.md', 'readme.md', 'revision.md'):
                continue
            if any(key in low for key in ('interview', 'cheat', 'tracker', 'bank')):
                continue
            if 'case-studies' in rel:
                continue
            files.append(rel)
    return sorted(files)


def code_mask(lines):
    """True for fence delimiters and everything inside a fence: those lines
    are shell comments or literal examples, never headings of the document."""
    mask = [False] * len(lines)
    for i, _line, in_fence, is_fence in md_fences.walk(lines):
        if in_fence or is_fence:
            mask[i] = True
    return mask


def umbrella_span(lines, code):
    """(start, end) of the first `## How It Works` section, fence-aware;
    end is the line index of the next real `##` heading (or the file end)."""
    start = None
    for i, line in enumerate(lines):
        if code[i] or not re.match(r'^##\s+How It Works\s*$', line, re.I):
            continue
        start = i
        break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if not code[j] and re.match(r'^##\s+\S', lines[j]):
            end = j
            break
    return start, end


def repair_text(text):
    """Return (new_text, changed). Promote the umbrella's children in place."""
    lines = text.split('\n')
    code = code_mask(lines)
    span = umbrella_span(lines, code)
    if span is None:
        return text, False
    start, end = span
    body = lines[start + 1:end]
    # child offsets are relative to `body`
    kids = [k for k, line in enumerate(body)
            if not code[start + 1 + k] and line.strip().startswith('### ')]
    if not kids:
        return text, False  # a prose-only umbrella needs an authored title

    def trim(chunk):
        """One blank line is ours to insert; the original's are not needed."""
        chunk = list(chunk)
        while chunk and not chunk[0].strip():
            chunk.pop(0)
        while chunk and not chunk[-1].strip():
            chunk.pop()
        return chunk

    intro = trim(body[:kids[0]])

    def block(lo, hi):
        return trim(body[lo:hi])

    pieces = []
    for n, k in enumerate(kids):
        title = body[k].strip()[4:].strip()  # drop leading `### `
        piece = ['## ' + title, '']
        if n == 0 and intro:
            piece += intro + ['']
        stop = kids[n + 1] if n + 1 < len(kids) else len(body)
        piece += block(k + 1, stop)
        while piece and not piece[-1].strip():
            piece.pop()
        pieces.append(piece)

    new = []
    for piece in pieces:
        new += [''] + piece if new else piece
    out = lines[:start] + new
    if out and out[-1].strip():
        out.append('')
    out += lines[end:]
    return '\n'.join(out), True


def violations(text):
    """[(rule, detail)] — the two rules this gate owns."""
    if is_guide_file(text):
        return []
    lines = text.split('\n')
    code = code_mask(lines)
    found = []
    parents = {}  # nearest preceding real heading index, per line
    last = None
    for i, line in enumerate(lines):
        if code[i]:
            parents[i] = last
            continue
        if line.strip():
            parents[i] = last
            if H2_RX.match(line) or H1_RX.match(line):
                last = i
    for i, line in enumerate(lines):
        if code[i]:
            continue
        m = H2_RX.match(line)
        if m and m.group(2).strip().lower().rstrip(':') in GENERIC:
            found.append(('retired-heading',
                          f'line {i + 1}: `## {m.group(2).strip()}` names a '
                          f'label, not the mechanism this chapter explains'))
        # rule 2: a numbered mechanism step still parked under a retired label
        if NUM_STEP_RX.match(line):
            parent = parents.get(i)
            if parent is not None:
                pm = H2_RX.match(lines[parent])
                if pm and pm.group(2).strip().lower().rstrip(':') in GENERIC:
                    found.append(('step-under-label',
                                  f'line {i + 1}: `{line.strip()[:60]}` sits '
                                  f'under a retired generic label'))
    return found


def opening_text(lines, code):
    """The prose block between H1 and the first `##`, skipping badges, quotes
    and separators — the standard's "hook opening" zone."""
    start = None
    for i, line in enumerate(lines):
        if not code[i] and H1_RX.match(line):
            start = i
            break
    if start is None:
        return ''
    block = []
    for i in range(start + 1, len(lines)):
        if code[i] or not lines[i].strip():
            continue
        s = lines[i].strip()
        if H2_RX.match(lines[i]):
            break
        if s == '---' or s.startswith(('[!', '![', '>')):
            continue
        block.append(s)
    return ' '.join(block)


def report(files):
    """Corpus shape for docs/readability-standard.md and the run report."""
    from collections import Counter
    stats = Counter()
    question_only = []
    for rel in files:
        text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        stats['files'] += 1
        lines = text.split('\n')
        code = code_mask(lines)
        if any(not code[i] and re.match(r'^##\s+How It Works\s*$', l, re.I)
               for i, l in enumerate(lines)):
            stats['umbrella'] += 1
        stats['retired'] += len(violations(text))
        opening = opening_text(lines, code)
        if opening:
            stats['opening'] += 1
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', opening)
                         if s.strip()]
            answered = [s for s in sentences
                        if not s.endswith('?') and len(s.split()) >= 6]
            if not answered:
                question_only.append(rel)
    print(f'chapters in scope: {stats["files"]}')
    print(f'  with the retired `## How It Works` umbrella: {stats["umbrella"]}')
    print(f'  retired-heading / step-under-label violations: {stats["retired"]}')
    # Advisory, not gated: "the opening answers, it does not only ask" is an
    # authoring judgment (a 6-word declarative can be the real answer), so the
    # report ranks the candidates and a human decides. Structural rules above
    # are the ones that block.
    print(f'  openings with a hook but no answer sentence (advisory): '
          f'{len(question_only)} of {stats["opening"]}')
    for rel in question_only:
        print(f'      {rel}')
    return 0


def main(argv):
    write = '--write' in argv
    files = iter_chapters()
    guard(len(files), 'chapter files', 'numbered stacks')

    if '--report' in argv:
        return report(files)

    problems = []
    repaired = []
    for rel in files:
        path = os.path.join(ROOT, rel)
        text = open(path, encoding='utf-8').read()
        if write:
            new_text, changed = repair_text(text)
            if changed:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(new_text)
                repaired.append(rel)
                text = new_text
        for rule, detail in violations(text):
            problems.append(f'{rel}: {detail}')

    if write:
        print(f'readability repair: {len(repaired)} chapter(s) rewritten, '
              f'{len(problems)} remaining violation(s)')
        if problems:
            for p in problems[:20]:
                print(f'  {p}')
        return 1 if problems else 0

    if problems:
        for p in problems[:40]:
            print(f'  {p}')
        if len(problems) > 40:
            print(f'  ... {len(problems) - 40} more')
        print(f'\nREADABILITY — {len(problems)} violation(s) over '
              f'{len(files)} chapter files. The outline must name the '
              f'mechanism; repair mechanically with:\n'
              f'  python3 scripts/check_readability.py --write')
        return 1
    print(f'readable outline OK — {len(files)} chapter files, no retired '
          f'generic heading and no mechanism step left under one')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
