#!/usr/bin/env python3
"""Fence-aware broken-link checker for software-developer-bible.

Scans every .md file (skipping .git / node_modules / .archive) and verifies
that each *prose* markdown link resolves to a real file or directory inside
the repo. This scripts the footer claims ("0 broken links") that previously
were asserted by hand.

Fence-aware means links inside code fences (``` / ~~~), {% raw %} blocks,
and HTML comments are ignored — they are examples, not navigation. External
links (http/https/mailto/tel), anchor-only links (`#heading`), and relative
targets that escape the repo root are reported as skipped, never as broken.

Usage:
  python3 scripts/check_links.py          # report + exit 1 on any broken link
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.archive'}

# Protocols / target forms that cannot or should not be resolved to a file.
EXTERNAL_PREFIXES = (
    'http://', 'https://', 'mailto:', 'tel:', 'ftp://', 'data:',
    '//', 'javascript:', '<',
)

LINK_RE = re.compile(r'\[[^\]\n]*\]\(([^)\n]+)\)')
# A fence opener may carry an info string (```js); a closer must be an
# otherwise-empty line of at least as many of the same marker chars.
FENCE_OPEN_RE = re.compile(r'^(\s*)(`{3,}|~{3,})')
FENCE_CLOSE_RE = re.compile(r'^\s*(`{3,}|~{3,})\s*$')
RAW_START_RE = re.compile(r'^\s*\{\%\s*raw')
RAW_END_RE = re.compile(r'\{\%\s*endraw')
HTML_COMMENT_START = re.compile(r'<!--')
HTML_COMMENT_END = re.compile(r'-->')


def is_external(target):
    return target.startswith(EXTERNAL_PREFIXES) or os.path.isabs(target)


def main():
    broken = []
    total = 0
    skipped = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if not name.endswith('.md'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT)
            try:
                with open(path, encoding='utf-8') as fh:
                    lines = fh.read().splitlines()
            except (OSError, UnicodeDecodeError) as exc:
                broken.append(f'{rel}: unreadable ({exc})')
                continue

            # Fence/comment state is per-file: nothing can span files.
            fence_char = None
            fence_len = 0
            in_raw = False
            in_comment = False

            for lineno, line in enumerate(lines, start=1):
                stripped = line.strip()

                # Fence tracking (code blocks, raw blocks, HTML comments).
                if in_comment:
                    if HTML_COMMENT_END.search(stripped):
                        in_comment = False
                    continue
                if not in_comment and HTML_COMMENT_START.search(stripped) \
                        and not HTML_COMMENT_END.search(stripped):
                    in_comment = True
                    continue
                if HTML_COMMENT_START.search(stripped) \
                        and HTML_COMMENT_END.search(stripped):
                    continue  # single-line comment

                if in_raw:
                    if RAW_END_RE.search(stripped):
                        in_raw = False
                    continue
                if RAW_START_RE.search(stripped):
                    in_raw = True
                    continue

                if fence_char:
                    close = FENCE_CLOSE_RE.match(line)
                    if close and close.group(1)[0] == fence_char \
                            and len(close.group(1)) >= fence_len:
                        fence_char = None
                        fence_len = 0
                    continue
                opener = FENCE_OPEN_RE.match(line)
                if opener and len(opener.group(1).rstrip()) < 4:
                    # Fence only counts when the indent is under 4 spaces
                    # (4+ spaces is an indented code block instead).
                    fence_char = opener.group(2)[0]
                    fence_len = len(opener.group(2))
                    continue

                # Strip inline code spans so `[x](y)` examples don't count.
                line = re.sub(r'`[^`\n]*`', '', line)

                for m in LINK_RE.finditer(line):
                    raw_target = m.group(1).strip()
                    # Optional markdown title after whitespace, angle brackets.
                    target = raw_target.split()[0].strip('\'"') \
                        if raw_target.split() else ''
                    if target.startswith('<'):
                        target = target[1:]
                        target = target.split('>')[0]
                    target = target.strip()

                    if not target or target.startswith('#') \
                            or is_external(target):
                        skipped += 1
                        continue

                    # A fragment/anchor doesn't change the file to resolve.
                    base = target.split('#', 1)[0].split('?', 1)[0]
                    if not base:
                        skipped += 1
                        continue

                    resolved = os.path.normpath(
                        os.path.join(os.path.dirname(path), base))
                    if not (resolved == ROOT
                            or resolved.startswith(ROOT + os.sep)):
                        # Escapes the repo root -> external, can't verify.
                        skipped += 1
                        continue

                    total += 1
                    if not os.path.exists(resolved):
                        broken.append(f'{rel}:{lineno}: {target} -> '
                                      f'{os.path.relpath(resolved, ROOT)}')

    if broken:
        print(f'BROKEN LINKS ({len(broken)}):')
        for b in broken:
            print(f'  {b}')
        print(f'\n{total} prose links checked, {len(broken)} broken '
              f'({skipped} external/anchor links skipped).')
        sys.exit(1)
    print(f'OK — {total} prose links checked, 0 broken '
          f'({skipped} external/anchor links skipped).')


if __name__ == '__main__':
    main()
