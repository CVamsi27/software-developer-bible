#!/usr/bin/env python3
"""Verify bible structure: relative md links resolve; numeric IDs unique; sequences contiguous.

Usage:
  python3 scripts/check_structure.py [--root .] [--links-only]

--links-only skips the contiguity check (useful mid-restructure).
"""
import re
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
links_only = "--links-only" in sys.argv
ROOT = Path(args[0] if args else ".").resolve()
SKIP = ("/.git/", "/node_modules/", "/.archive/", "/.freebuff/", "/.sass-cache/")
MD = [p for p in sorted(ROOT.rglob("*.md")) if not any(s in str(p) for s in SKIP)]
errors = []

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODESPAN = re.compile(r"`[^`]*`")


def strip_code(text: str) -> str:
    out = []
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            out.append("")
            continue
        out.append("" if fence else CODESPAN.sub("", line))
    return "\n".join(out)


for p in MD:
    text = strip_code(p.read_text(encoding="utf-8", errors="replace"))
    for m in LINK.finditer(text):
        t = m.group(1)
        if t.startswith(("http", "mailto:", "#")):
            continue
        target = (p.parent / t.split("#")[0]).resolve()
        if not target.exists():
            errors.append(f"BROKEN LINK {p.relative_to(ROOT)} -> {t}")

idre = re.compile(r"^(?:\d+\.)+\d+-")
seen = {}
for p in MD:
    if idre.match(p.name):
        if p.name in seen:
            errors.append(f"DUPLICATE ID {p.name}: {seen[p.name]} & {p.relative_to(ROOT)}")
        seen[p.name] = str(p.relative_to(ROOT))

if not links_only:
    fam = {}
    for p in MD:
        m2 = re.match(r"^((?:\d+\.)*)(\d+)\.(\d+)-", p.name)
        if not m2 or p.name == "INDEX.md":
            continue
        prefix = (m2.group(1) or "") + m2.group(2)
        key = (str(p.parent), prefix)
        fam.setdefault(key, []).append(int(m2.group(3)))
    for (d, pref), nums in sorted(fam.items()):
        exp = list(range(1, len(nums) + 1))
        if sorted(nums) != exp:
            errors.append(f"GAPS {d} prefix {pref}.x: has {sorted(nums)} expected 1..{len(nums)}")

print("\n".join(errors) if errors else f"OK: {len(MD)} md files checked")
sys.exit(1 if errors else 0)
