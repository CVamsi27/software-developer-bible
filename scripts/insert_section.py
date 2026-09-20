#!/usr/bin/env python3
"""Insert a `## Definition` (or other) section at its canonical slot.

Used by the final template pass to add missing required sections without
hand-editing 75 files. The insertion point is derived from the file's own
structure:

  after `## Why It Matters` / `## Why Do We Need It?` when present,
  else after `## First Principles`,
  else after `## TL;DR`,
  else before the first `## ` heading.

The horizontal rule is inserted only if the file already separates sections
with `---`, so the file's own style is preserved.

Usage (JSON payload of {path: section text}):
  python3 scripts/insert_section.py --heading "## Definition" payload.json
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_template import normalize  # noqa: E402
import md_fences

HEAD = re.compile(r'^##\s+(.+?)\s*$')
FENCE = re.compile(r'^\s*(```|~~~)')
# Section whose body the new section follows, in preference order.
ANCHORS = ('Why It Matters', 'First Principles', 'TL;DR')
RULE = '---'


def heading_positions(lines):
    out = []
    in_fence = False
    for i, line, in_fence, is_fence in md_fences.walk(lines):
        if is_fence:
            continue
        if in_fence:
            continue
        m = HEAD.match(line)
        if m:
            out.append((i, normalize(m.group(1))))
    return out


def find_insert_index(lines):
    heads = heading_positions(lines)
    anchor = None
    for want in ANCHORS:
        for idx, (ln, name) in enumerate(heads):
            if name == want:
                anchor = idx
                break
        if anchor is not None:
            break
    if anchor is None:
        return heads[0][0] if heads else len(lines), heads, False
    if anchor + 1 < len(heads):
        return heads[anchor + 1][0], heads, True
    # anchor is the last section: append at end
    return len(lines), heads, False


def uses_rules(lines):
    return any(l.strip() == RULE for l in lines)


def insert(path, heading, body):
    lines = open(path, encoding='utf-8').read().split('\n')
    idx, heads, has_next = find_insert_index(lines)
    # Walk back over a blank/rule block that belongs to the *next* section.
    cut = idx
    while cut > 0 and not lines[cut - 1].strip():
        cut -= 1
    rule_before_next = cut > 0 and lines[cut - 1].strip() == RULE
    if rule_before_next:
        cut -= 1
        while cut > 0 and not lines[cut - 1].strip():
            cut -= 1
    block = []
    if uses_rules(lines) and has_next:
        block += ['', RULE]
    block += ['', heading, '', body.rstrip()]
    new_lines = lines[:cut] + block + lines[cut:]
    text = '\n'.join(new_lines)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    if not text.endswith('\n'):
        text += '\n'
    open(path, 'w', encoding='utf-8').write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('payload')
    ap.add_argument('--heading', default='## Definition')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    payload = json.load(open(args.payload, encoding='utf-8'))
    for path, body in payload.items():
        insert(path, args.heading, body)
        print(f"inserted {args.heading} -> {path}")


if __name__ == '__main__':
    main()
