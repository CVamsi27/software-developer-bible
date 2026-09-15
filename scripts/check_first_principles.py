#!/usr/bin/env python3
"""First Principles coverage tracker.

Counts concept chapters (numbered content files, excluding INDEX,
interview-questions, cheat-sheet/quick-reference files) that carry a
`## First Principles` section, per stack. The section must sit between
TL;DR/Why and Definition-style body sections and derive the topic from
unavoidable constraints — the template rules live in contributing.md.

Usage:
  python3 scripts/check_first_principles.py              # report
  python3 scripts/check_first_principles.py --baseline   # write baseline JSON
  python3 scripts/check_first_principles.py --diff       # fail on coverage regressions
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".archive", ".freebuff", "scripts", "docs", "personal"}
BASELINE = Path(__file__).resolve().parent / "first-principles-baseline.json"

SECTION = re.compile(r"^## First Principles\s*$", re.M)
NUMFILE = re.compile(r"^(?:\d+\.)+\d+-")
EXCLUDE = re.compile(r"interview|cheat|quick-reference", re.I)


def stacks():
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and re.match(r"^\d", d.name) and d.name not in SKIP_DIRS:
            yield d


def concept_files(stack_dir):
    for p in sorted(stack_dir.rglob("*.md")):
        if not NUMFILE.match(p.name) or EXCLUDE.search(p.name):
            continue
        yield p


def has_section(p):
    return bool(SECTION.search(p.read_text(encoding="utf-8", errors="replace")))


def coverage():
    table = {}
    for stack in stacks():
        files = list(concept_files(stack))
        if not files:
            continue
        have = sum(1 for p in files if has_section(p))
        table[stack.name] = {"covered": have, "total": len(files)}
    return table


def main():
    table = coverage()
    cov = sum(v["covered"] for v in table.values())
    tot = sum(v["total"] for v in table.values())
    width = max((len(k) for k in table), default=0)
    print(f"{'stack'.ljust(width)}  covered/total")
    for k, v in table.items():
        bar = "#" * round(20 * v["covered"] / v["total"]) if v["total"] else ""
        print(f"{k.ljust(width)}  {v['covered']:>4}/{v['total']:<4} {bar}")
    print(f"\nTOTAL: {cov}/{tot} concept chapters ({round(100*cov/tot) if tot else 0}%)")

    if "--baseline" in sys.argv:
        BASELINE.write_text(json.dumps(table, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline written: {BASELINE.relative_to(ROOT)}")
        return 0
    if "--diff" in sys.argv and BASELINE.exists():
        old = json.loads(BASELINE.read_text(encoding="utf-8"))
        regressions = []
        for k, v in table.items():
            if k in old and v["covered"] < old[k]["covered"]:
                regressions.append(f"{k}: {old[k]['covered']} -> {v['covered']}")
        if regressions:
            print("coverage regression (First Principles sections removed):")
            for r in regressions:
                print(f"  {r}")
            return 1
        print("baseline diff: no regressions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
