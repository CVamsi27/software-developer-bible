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

from scan_scope import guard

SKIP_DIRS = {'.git', 'node_modules', 'vendor', '_site', '.archive', 'venv', '__pycache__'}
FENCE_RE = re.compile(r'^( {0,3})(`{3,}|~{3,})([A-Za-z0-9_+-]*)')
LAYOUT_LANGS = {'', 'text', 'tsv', 'anki', 'csv', 'diff', 'mermaid'}

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Gate tolerances: known-intentional patterns that would otherwise fire.
# Kept explicit so each one is a decision, not an accident.


def unbalanced_fence(lines):
    """CommonMark-correct fence balance.

    A closing fence may NOT carry an info string. That detail matters because
    fences *nested* inside a fenced block therefore close it early: a
    ```markdown block containing ```sql ... ``` pairs ends at the first bare
    ```, orphaning everything after it. `50.4.01-incident-response.md` shipped
    exactly that — two runbook headings leaked out as real document headings
    and the final ~30 lines were swallowed into an unclosed code block. No gate
    caught it because this script (like every other fence-aware gate) toggled on
    fence character alone, ignoring length and info string. Nesting legitimately
    requires a LONGER outer fence (```` around ```).
    """
    open_len = 0
    open_ch = None
    open_line = 0
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if not m:
            continue
        ch = m.group(2)[0]
        ln = len(m.group(2))
        info = m.group(3).strip()
        if open_len == 0:
            open_len, open_ch, open_line = ln, ch, i + 1
        elif ch == open_ch and ln >= open_len and info == '':
            open_len = 0
        # else: a fence-like line inside the block is content, not a closer
    if open_len:
        return [(open_line, 'UNCLOSED-FENCE',
                 f'opened with {open_ch * open_len} and never closed '
                 f'(to nest fences, make the outer one longer)')]
    return []


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
    issues.extend(unbalanced_fence(lines))
    return issues


def main():
    all_issues = {}
    n_files = 0
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith('.md'):
                continue
            n_files += 1
            path = os.path.join(root, fn)
            found = check_file(path)
            if found:
                all_issues[path] = found

    # "0 trailing-ws" means nothing if the walk found no files (scan_scope).
    guard(n_files, 'markdown files', repo_root)

    if not all_issues:
        print(f"Code-block whitespace: OK (0 trailing-ws, 0 paste-shifted blocks, "
              f"0 unbalanced fences across {n_files} files)")
        sys.exit(0)

    total = sum(len(v) for v in all_issues.values())
    print(f"Code-block whitespace: {total} issue(s) in {len(all_issues)} file(s)\n")
    for path, found in sorted(all_issues.items()):
        rel = os.path.relpath(path, repo_root)
        for lineno, kind, detail in found[:6]:
            print(f"  {rel}:{lineno}  {kind}  {detail}")
        if len(found) > 6:
            print(f"  {rel}: ... and {len(found) - 6} more")
    kinds = {k for v in all_issues.values() for _, k, _ in v}
    if kinds - {'UNCLOSED-FENCE'}:
        print("\nFix with: python3 scripts/fix_code_whitespace.py --trailing-ws --paste-shift")
    if 'UNCLOSED-FENCE' in kinds:
        print("\nUNCLOSED-FENCE is not auto-fixable: a fenced block containing "
              "same-length fences ends at the first bare fence. Make the outer "
              "fence longer (```` around ```) so the inner ones are content.")
    sys.exit(1)


if __name__ == '__main__':
    main()
