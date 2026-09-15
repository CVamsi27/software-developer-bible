#!/usr/bin/env python3
"""Gate: code-block whitespace hygiene inside fenced blocks.

Fails when either defect class re-enters the repo:

1. TRAILING-WS  — trailing whitespace on any line inside a fenced code
                  block (CommonMark fence detection: fences indented
                  0-3 spaces open/close; deeper indent is code content).

2. PASTE-SHIFT  — a lang-tagged code block whose every non-empty line
                  carries a uniform base indent of >= 4 spaces. That is
                  the signature of a block pasted from an indented
                  source without dedenting; it renders as stray leading
                  whitespace on every line.

Passes by design (do NOT "fix" these):
- go fences using tabs — gofmt style is tabs.
- anki/tsv/csv fences using tabs — the tab IS the data format
  (Anki TSV import files).
- text/(none)/diff/mermaid fences with any indentation — ASCII
  diagrams and column-aligned layouts; the alignment is the content.
- list-nested fences (fence indented 1-3 spaces): the block's base
  indent legitimately equals the list indentation.

Fix mode:  python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift
"""

import os
import re
import sys

SKIP_DIRS = {'.git', 'node_modules', '.archive', 'venv', '__pycache__'}
FENCE_RE = re.compile(r'^( {0,3})(`{3,}|~{3,})([A-Za-z0-9_+-]*)')
LAYOUT_LANGS = {'', 'text', 'tsv', 'anki', 'csv', 'diff', 'mermaid'}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Gate tolerances: known-intentional patterns that would otherwise fire.
# Kept explicit so each one is a decision, not an accident.


def check_file(path):
    """Return list of (lineno, kind, detail) issues."""
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')

    issues = []
    in_fence = False
    fence_ch = None
    open_line_idx = 0
    open_lang = ''
    open_indent = 0
    block = []

    def close_block():
        nonlocal block
        if not block:
            return
        if open_lang in LAYOUT_LANGS:
            block = []  # diagrams / data: any layout is content
            return
        ne = [l for l in block if l.strip()]
        if not ne:
            block = []
            return
        # paste-shift: uniform base indent >= 4 on every non-empty line
        base = min(len(l) - len(l.lstrip(' ')) for l in ne)
        base -= open_indent  # list-nested fences carry their own base
        if base >= 4 and not any('\t' in l for l in ne):
            issues.append((open_line_idx + 1, 'PASTE-SHIFT',
                           f'[{open_lang}] block base-indent {base} spaces'))
        # trailing whitespace inside the block
        for k, l in enumerate(block):
            if l != l.rstrip():
                tail = l[len(l.rstrip()):]
                issues.append((open_line_idx + 2 + k, 'TRAILING-WS',
                               f'{len(tail)} trailing space(s)'))
        block = []

    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            mk = m.group(2)
            if not in_fence:
                in_fence = True
                fence_ch = mk[0]
                open_line_idx = i
                open_lang = m.group(3).lower()
                open_indent = len(m.group(1))
                block = []
            elif mk[0] == fence_ch:
                close_block()
                in_fence = False
            continue
        if in_fence:
            block.append(line)
    close_block()  # tolerate unclosed final fence (structure gate owns that)
    return issues


def main():
    all_issues = {}
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(root, fn)
            found = check_file(path)
            if found:
                all_issues[path] = found

    if not all_issues:
        print("Code-block whitespace: OK (0 trailing-ws, 0 paste-shifted blocks)")
        sys.exit(0)

    total = sum(len(v) for v in all_issues.values())
    print(f"Code-block whitespace: {total} issue(s) in {len(all_issues)} file(s)\n")
    for path, found in sorted(all_issues.items()):
        rel = os.path.relpath(path, repo_root)
        for lineno, kind, detail in found[:6]:
            print(f"  {rel}:{lineno}  {kind}  {detail}")
        if len(found) > 6:
            print(f"  {rel}: ... and {len(found) - 6} more")
    print("\nFix with: python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift")
    sys.exit(1)


if __name__ == '__main__':
    main()
