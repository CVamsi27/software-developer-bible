#!/usr/bin/env python3
"""Insert the missing See Also links between topic twins.

`check_topic_twins.py` reports twin chapters that do not reference each
other. This tool writes those links, using the *target* chapter's own title
and opening line as the description — so the pointer says what the other
chapter actually covers instead of a generic "related reading".

Usage:
  python3 scripts/link_topic_twins.py --dry-run [--limit N]
  python3 scripts/link_topic_twins.py
"""
import argparse
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location(
    'twins', os.path.join(ROOT, 'scripts', 'check_topic_twins.py'))
twins = importlib.util.module_from_spec(spec)
spec.loader.exec_module(twins)

FENCE = re.compile(r'^\s*(```|~~~)')
H1 = re.compile(r'^#\s+(.+?)\s*$')
SECTION = re.compile(r'^##\s+(.+?)\s*$')


def read(path):
    return open(path, encoding='utf-8').read()


def title(text, rel):
    for line in text.splitlines():
        m = H1.match(line)
        if m:
            t = re.sub(r'\s*—.*$', '', m.group(1)).strip()
            if t:
                return t
    base = os.path.basename(rel)[:-3]
    base = re.sub(r'^(?:\d+\.)*\d+[a-z]?-', '', base)
    return base.replace('-', ' ').title()


def clamp(s, limit=96):
    """Cut at a word boundary so a description never ends mid-word."""
    s = s.strip()
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(' ', 1)[0].rstrip(',;:')
    return cut + '…'


def first_sentence(rel):
    """The target's own opening line: TL;DR first bullet, else Definition."""
    text = read(os.path.join(ROOT, rel))
    lines = text.split('\n')
    in_fence = False
    for want in ('TL;DR', 'Definition', 'Why It Matters', 'Why Do We Need It?'):
        grab = False
        for line in lines:
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = SECTION.match(line)
            if m:
                grab = m.group(1).strip().lower() == want.lower()
                continue
            if grab and line.strip():
                s = line.strip()
                s = re.sub(r'^[-*\d.]+\s*', '', s)          # bullets / numbers
                s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)       # bold
                s = re.sub(r'`(.+?)`', r'\1', s)             # inline code
                s = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', s)    # links
                s = re.sub(r'^>\s*', '', s)
                s = s.split('. ')[0].rstrip('.').strip()
                if len(s) > 12:
                    return clamp(s)
        in_fence = False
    return ''


def see_also_bounds(text):
    lines = text.split('\n')
    start = end = None
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = SECTION.match(line)
        if m and m.group(1).strip().lower() == 'see also':
            start = i
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('## '):
                    end = j
                    break
            else:
                end = len(lines)
            break
    return start, end


def add_link(rel_from, rel_to, dry_run=False):
    path = os.path.join(ROOT, rel_from)
    text = read(path)
    if os.path.basename(rel_to) in twins.links(path):
        return False
    tgt = os.path.join(ROOT, rel_to)
    dist = os.path.relpath(tgt, os.path.dirname(path)).replace(os.sep, '/')
    label = title(read(tgt), rel_to)
    desc = first_sentence(rel_to)
    bullet = f"- [{label}]({dist})" + (f" — {desc}" if desc else "")

    start, end = see_also_bounds(text)
    lines = text.split('\n')
    if start is None:
        # No See Also: create one before References, else at the end.
        ref = next((i for i, l in enumerate(lines)
                    if SECTION.match(l) and SECTION.match(l).group(1).strip()
                    .lower().startswith('references')), None)
        at = ref if ref is not None else len(lines)
        lines[at:at] = ['## See Also', '', bullet, '']
    else:
        at = end
        while at > start and not lines[at - 1].strip():
            at -= 1
        lines[at:at] = [bullet]
    new = '\n'.join(lines)
    new = re.sub(r'\n{4,}', '\n\n\n', new)
    if not new.endswith('\n'):
        new += '\n'
    if dry_run:
        print(f"  {rel_from}\n    + {bullet}")
        return False
    open(path, 'w', encoding='utf-8').write(new)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    _groups, _topics, pairs = twins.analyse()
    if args.limit:
        pairs = pairs[:args.limit]
    print(f"{len(pairs)} missing twin link(s)")
    n = 0
    for a, b in pairs:
        if add_link(a, b, dry_run=args.dry_run):
            n += 1
            print(f"linked {a} -> {os.path.basename(b)}")
    if not args.dry_run:
        print(f"\n{n} link(s) added")


if __name__ == '__main__':
    sys.exit(main())
