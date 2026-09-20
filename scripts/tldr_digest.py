#!/usr/bin/env python3
"""Print an authoring digest for chapters the template gate flags.

Usage: python3 scripts/tldr_digest.py [stack-prefix]

For each concept file missing a TL;DR, prints the title and the opening
lines of Definition / Why It Matters / Summary, so a TL;DR can be written
from the chapter's own thesis instead of a generic summary.
"""
import os
import re
import subprocess
import sys
import md_fences

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTION = re.compile(r'^##\s+(.+?)\s*$')
FENCE = re.compile(r'^\s*(```|~~~)')


def flagged(prefix=''):
    out = subprocess.run([sys.executable, 'scripts/check_template.py'],
                         cwd=ROOT, capture_output=True, text=True).stdout
    files, prev = [], ''
    for line in out.split('\n'):
        if 'missing required sections' in line:
            if "'TL;DR'" in line and prev.endswith('.md'):
                files.append(prev)
        elif line.strip():
            prev = line.strip()
    return [f for f in files if f.startswith(prefix)]


def digest(rel, compact=False):
    text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    lines = text.split('\n')
    title = next((l[2:].strip() for l in lines if l.startswith('# ')), rel)
    print(f"\n### {rel}\n  T: {title}")
    in_fence, want, got = False, None, 0
    for _, line, in_fence, is_fence in md_fences.walk(lines):
        if is_fence:
            continue
        if in_fence:
            continue
        m = SECTION.match(line)
        if m:
            h = m.group(1).strip()
            want = h if h.lower() in ('definition', 'why it matters',
                                      'why do we need it?', 'summary',
                                      'how it works') else None
            got = 0
            continue
        if want and line.strip() and got < (1 if compact else 2):
            print(f"  {want[:4]}: {line.strip()[:190]}")
            got += 1
            if got >= (1 if compact else 2):
                want = None


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    pre = args[0] if args else ''
    compact = '--compact' in sys.argv
    files = flagged(pre)
    print(f"{len(files)} file(s) missing TL;DR" + (f" under {pre}" if pre else ''))
    for f in files:
        digest(f, compact)
