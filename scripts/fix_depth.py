#!/usr/bin/env python3
"""Fix depth-broken relative md links after files moved deeper/shallower.

For every relative .md link that does NOT resolve, try adding 1..4 '../'
prefixes; rewrite only if EXACTLY ONE candidate depth resolves (ambiguous
cases are reported, never guessed).
"""
import re
import sys
from pathlib import Path

ROOT = Path(".").resolve()
SKIP = ("/.git/", "/.archive/", "/.freebuff/", "/.sass-cache/")
LINK = re.compile(r"(\]\()((?:\.\./|[^)/])[^)\s]*\.md)(\))")
ambiguous = []
fixed = 0

for p in sorted(ROOT.rglob("*.md")):
    if any(s in str(p) for s in SKIP):
        continue
    txt = p.read_text(encoding="utf-8", errors="replace")
    orig = txt

    def repl(m):
        global fixed
        ref = m.group(2)
        cur = p.parent / ref
        if cur.exists():
            return m.group(0)
        hits = []
        probe = ref
        for extra in range(1, 5):
            probe = "../" + probe
            cand = (p.parent / probe.split("#")[0]).resolve()
            if cand.exists():
                hits.append(probe)
        if len(hits) == 1:
            fixed += 1
            return m.group(1) + hits[0] + m.group(3)
        if len(hits) > 1:
            ambiguous.append(f"{p.relative_to(ROOT)} -> {ref} matches {hits}")
        return m.group(0)

    txt = LINK.sub(repl, txt)
    if txt != orig:
        p.write_text(txt, encoding="utf-8")

print(f"depth-fixed {fixed} links")
for a in ambiguous:
    print(f"AMBIGUOUS {a}")
sys.exit(0)
