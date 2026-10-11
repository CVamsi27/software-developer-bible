#!/usr/bin/env python3
"""Rewrite every relative .md link whose basename equals OLD so it points to NEW.

Usage: python3 scripts/relink.py <old-basename.md> <new/path/file.md>
Safe to run after the file has already moved: links are rewritten even if stale.
"""
import os
import re
import sys
from pathlib import Path

old_name, new_rel = sys.argv[1], Path(sys.argv[2])
ROOT = Path(".").resolve()
target_abs = ROOT / new_rel
LINK = re.compile(r"(\]\()([^)\s]+\.md)(\))")
SKIP = ("/.git/", "/node_modules/", "/vendor/", "/_site/", "/.archive/",
        "/.freebuff/", "/.sass-cache/")
changed = 0

for p in ROOT.rglob("*.md"):
    if any(s in str(p) for s in SKIP):
        continue
    txt = p.read_text(encoding="utf-8", errors="replace")
    orig = txt

    def repl(m):
        ref = m.group(2)
        base = os.path.basename(ref.split("#")[0])
        if base != old_name:
            return m.group(0)
        newref = os.path.relpath(target_abs, p.parent)
        return m.group(1) + newref + m.group(3)

    txt = LINK.sub(repl, txt)
    if txt != orig:
        p.write_text(txt, encoding="utf-8")
        changed += 1

print(f"relink {old_name} -> {new_rel}: rewrote links in {changed} files")
