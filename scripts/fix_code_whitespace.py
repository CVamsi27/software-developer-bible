#!/usr/bin/env python3
"""Fix code-block whitespace defects in markdown files.

Three fixes, each verified against a repo-wide scan before enabling:

1. --trailing-ws  Strip trailing whitespace on lines INSIDE fenced code
                  blocks. Prose lines are left alone (the aligner owns
                  prose; some prose lines are table alignment artifacts
                  that check_alignment.py already tolerates).

2. --paste-shift  Dedent lang-tagged code blocks whose EVERY non-empty
                  line carries a uniform base indent of >= 4 spaces —
                  the signature of a whole block pasted from an
                  indented source. Internal relative indentation is
                  preserved exactly (only the base is removed).
                  text/(none)/data fences are skipped: their base
                  indent is usually a centered diagram title and the
                  alignment IS the content.

3. --relabel-anki Relabel ```text fences that contain tab characters
                  to ```anki. Tabs in the flashcard deck are the Anki
                  TSV import format — load-bearing data, not sloppy
                  indentation. The fence label should say so.

Checks that PASS BY DESIGN (documented so nobody "fixes" them):
- Go code fenced as ```go uses tabs (gofmt style) — correct.
- ASCII diagrams with odd/centered leading spaces — alignment is the
  content; never dedent or reflow them.

Usage:
  python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift --relabel-anki [--dry-run]
"""

import os
import re
import sys

SKIP_DIRS = {'.git', 'node_modules', '.archive', 'venv', '__pycache__'}
# CommonMark: fences may be indented 0-3 spaces and still open/close a
# block (deeper than 3 spaces = indented code, not a fence).
FENCE_RE = re.compile(r'^( {0,3})(`{3,}|~{3,})([A-Za-z0-9_+-]*)')
# Fences whose leading whitespace is layout/content, not paste damage.
LAYOUT_LANGS = {'', 'text', 'tsv', 'anki', 'csv', 'diff', 'mermaid'}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def md_files():
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.endswith('.md'):
                yield os.path.join(root, fn)


def _iter_fenced_blocks(lines):
    """Yield (open_idx, close_idx, body_lines) for top-level fences."""
    in_fence = False
    fence_ch = None
    start = 0
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            mk = m.group(2)
            if not in_fence:
                in_fence, fence_ch, start = True, mk[0], i
            elif mk[0] == fence_ch:
                yield start, i, lines[start + 1:i]
                in_fence = False
    # unclosed fence: ignored (check_structure catches real fence bugs)


def strip_trailing_ws(lines):
    """Strip trailing whitespace inside fenced blocks only."""
    changed = 0
    fenced = set()
    for open_i, close_i, _body in _iter_fenced_blocks(lines):
        fenced.update(range(open_i, close_i + 1))
    for i in sorted(fenced):
        new = lines[i].rstrip()
        if new != lines[i]:
            lines[i] = new
            changed += 1
    return changed


def dedent_base_indented_blocks(lines):
    """Dedent code blocks pasted with a uniform >=4-space base indent."""
    rewritten = 0
    for open_i, close_i, body in list(_iter_fenced_blocks(lines)):
        if not body:
            continue
        m = FENCE_RE.match(lines[open_i])
        lang = m.group(3).lower() if m else ''
        if lang in LAYOUT_LANGS:
            continue
        ne = [l for l in body if l.strip()]
        if not ne:
            continue
        base = min(len(l) - len(l.lstrip(' ')) for l in ne)
        if base < 4:
            continue
        if any('\t' in l for l in body):
            continue  # tab-indented code: style choice, not paste damage
        new_body = [l[base:] if l.strip() else l for l in body]
        for k, idx in enumerate(range(open_i + 1, close_i)):
            lines[idx] = new_body[k]
        rewritten += 1
    return rewritten


def relabel_tab_text_fences(lines):
    """Relabel ```text fences containing tabs to ```anki (TSV data)."""
    rewritten = 0
    for open_i, close_i, body in list(_iter_fenced_blocks(lines)):
        m = FENCE_RE.match(lines[open_i])
        if not m or m.group(3).lower() != 'text':
            continue
        if not any('\t' in l for l in body):
            continue
        lines[open_i] = FENCE_RE.sub(
            lambda mm: mm.group(1) + mm.group(2) + 'anki',
            lines[open_i], count=1)
        rewritten += 1
    return rewritten


def process_file(path, trailing_ws, paste_shift, relabel_anki, dry_run):
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    orig = list(lines)

    changed_ws = changed_shift = changed_label = 0
    if trailing_ws:
        changed_ws = strip_trailing_ws(lines)
    if paste_shift:
        changed_shift = dedent_base_indented_blocks(lines)
    if relabel_anki:
        changed_label = relabel_tab_text_fences(lines)

    if not dry_run and lines != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    return changed_ws, changed_shift, changed_label


def main():
    args = sys.argv[1:]
    dry = '--dry-run' in args
    trailing_ws = '--trailing-ws' in args
    paste_shift = '--paste-shift' in args
    relabel_anki = '--relabel-anki' in args
    if not (trailing_ws or paste_shift or relabel_anki):
        print(__doc__)
        sys.exit(2)

    tot_ws = tot_shift = tot_rel = tot_files = 0
    for path in md_files():
        ws, sh, rel = process_file(path, trailing_ws, paste_shift,
                                   relabel_anki, dry)
        if ws or sh or rel:
            tot_files += 1
            tot_ws += ws
            tot_shift += sh
            tot_rel += rel
            print(f"  {path}: ws={ws} shifted_blocks={sh} relabeled={rel}")

    label = "WOULD FIX" if dry else "FIXED"
    print(f"\n{label}: {tot_ws} trailing-ws lines, "
          f"{tot_shift} paste-shifted blocks, {tot_rel} relabeled fences "
          f"in {tot_files} file(s)")


if __name__ == '__main__':
    main()
