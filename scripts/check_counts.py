#!/usr/bin/env python3
"""Check that repo-scale count claims match live disk.

The root INDEX footer and the 80-lane INDEX scale notes advertise the
whole-repo totals ("NNN files, NNNK lines"). Those numbers drifted
repeatedly because nothing enforced them. This script recomputes the
live totals (md files and summed line counts, excluding .git /
node_modules / .archive) and fails if any documented claim disagrees.

Usage:
  python3 scripts/check_counts.py            # report + exit 1 on drift
"""
import os
import re
import sys

SKIP_DIRS = {'.git', 'node_modules', '.archive'}
# Files that carry the repo-total scale claim. Root footer is the canonical
# site; the 80-lane rows quote the same totals (scale notes).
CLAIM_FILES = [
    'INDEX.md',
    '80-lanes-abroad-full-stack/INDEX.md',
]


def live_totals():
    files = 0
    lines = 0
    for root, dirs, fs in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in fs:
            if not f.endswith('.md'):
                continue
            files += 1
            with open(os.path.join(root, f), encoding='utf-8') as fh:
                lines += fh.read().count('\n')
    return files, lines


def main():
    files, lines = live_totals()
    k = lines // 1000
    expected = f'{files} files, {k}K lines'
    bad = []
    for path in CLAIM_FILES:
        if not os.path.exists(path):
            bad.append(f'{path}: MISSING')
            continue
        text = open(path, encoding='utf-8').read()
        if expected not in text:
            bad.append(
                f'{path}: does not claim "{expected}" (live: {files} files, '
                f'{lines} lines)'
            )
    if bad:
        print('count drift detected:')
        for line in bad:
            print(f'  {line}')
        print(f'\nrecommended scale string: "{expected}"')
        sys.exit(1)
    print(f'OK — {expected} matches root INDEX footer and 80-lane scale notes.')


if __name__ == '__main__':
    main()
