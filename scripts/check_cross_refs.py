#!/usr/bin/env python3
"""Verify inline cross-references of the form `→ N.N[.N[.N]]` resolve to real targets.

Resolution hierarchy (mirrors the repo's numbering convention):
  4 components  → category file (`→ 10.1.1.03` names `10.1.1.03-call-stack.md`)
  3 components  → flat-stack file (`→ 40.9.01`) or category folder (`→ 30.2.2`)
  2 components  → stack folder (`→ 10.1`) or flat-stack file (`→ 81.16`)
  1 component   → prose (HTTP codes, quantities) — ignored

Both sides are normalized identically: every component after the first is
zero-padded to 2 digits, so `10.4.3.03` == filename `10.4.3.03-…` groups
`('10','4','3','03')`. Refs whose first component is not a real stack
prefix (e.g. `→ 1.0`, `→ 99.99`) are treated as prose arrows, not refs.
Skips fences, personal/, .archive.
"""
import os
import re
import sys
import md_fences
from scan_scope import guard

REF = re.compile(r'→\s*((?:\d+\.)*\d+)')
FENCE = re.compile(r'^\s*(```|~~~)')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {'.git', 'node_modules', '.archive', 'personal'}


def normalize(ref: str):
    """Zero-pad components after the first; return the component tuple."""
    parts = ref.split('.')
    return tuple([parts[0]] + [p.zfill(2) for p in parts[1:]])


def iter_md_files():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel = os.path.relpath(root, ROOT)
        if 'personal' in rel.split(os.sep):
            continue
        for f in files:
            if f.endswith('.md'):
                yield os.path.join(root, f)


def build_index():
    """Collect stack dirs, category dirs, file-ID prefixes — all normalized."""
    stacks, cats, fids = set(), set(), set()
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for d in dirs:
            m = re.match(r'^(\d{2})\.(\d{1,2})-(.*)$', d)          # stack: 10.1-javascript / 40.9-twelve-factor
            if m:
                stacks.add(normalize(m.group(1) + '.' + m.group(2)))
            m3 = re.match(r'^(\d{2})\.(\d{1,2})\.(\d{1,2})-(.*)$', d)
            if m3:
                stacks.add(normalize(m3.group(1) + '.' + m3.group(2)))
        for d in dirs:
            full = os.path.join(root, d)
            mp = re.match(r'^(\d{2})\.(\d{1,2})-(.*)$', d)
            if mp and os.path.isdir(full):
                for sub in os.listdir(full):
                    mc = re.match(r'^(\d{2})-', sub)               # category: 01-execution-and-scope
                    if os.path.isdir(os.path.join(full, sub)) and mc:
                        cats.add(normalize(mp.group(1) + '.' + mp.group(2) + '.' + mc.group(1)))
        for f in files:
            m = re.match(r'^(\d{2})\.(\d{1,2})\.(\d{1,2})\.(\d{1,2})-', f)  # category file: 10.1.1.02-
            if m:
                fids.add(normalize('.'.join(m.groups())))
                continue
            m = re.match(r'^(\d{2})\.(\d{1,2})\.(\d{1,2})-', f)             # flat file: 40.9.01- / 10.7.04-
            if m:
                fids.add(normalize('.'.join(m.groups())))
    return stacks, cats, fids


def resolves(parts, stacks, cats, fids):
    n = len(parts)
    if n == 1:
        return True  # prose number
    if parts[0] not in {s[0] for s in stacks}:
        return True  # first component isn't a stack prefix → prose arrow (→ 1.0, → 99.99)
    if n >= 4:
        return parts[:4] in fids
    if n == 3:
        return parts in fids or parts in cats or any(p[:3] == parts for p in fids)
    if n == 2:
        return parts in stacks or any(p[:2] == parts for p in fids)
    return True


def strip_fences(text: str):
    in_fence = False
    for _, line, in_fence, is_fence in md_fences.walk(text.splitlines()):
        if is_fence:
            continue
        if not in_fence:
            yield line


def main() -> int:
    stacks, cats, fids = build_index()

    # No indexed stacks means the inventory scan itself failed, not that the
    # corpus is clean — every → N.N.N ref would "resolve" vacuously (scan_scope).
    guard(len(stacks), 'study stacks', str(ROOT))

    broken = []
    for path in iter_md_files():
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding='utf-8').read()
        for line in strip_fences(text):
            for m in REF.finditer(line):
                parts = normalize(m.group(1))
                if not resolves(parts, stacks, cats, fids):
                    broken.append((rel, m.group(1)))
    if broken:
        seen = set()
        uniq = [x for x in broken if not (x in seen or seen.add(x))]
        print(f"BROKEN cross-references: {len(uniq)}")
        for rel, ref in uniq:
            print(f"  {rel}: → {ref}")
        return 1
    print(f"cross-references OK ({len(stacks)} stacks, {len(cats)} categories, {len(fids)} file IDs indexed)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
