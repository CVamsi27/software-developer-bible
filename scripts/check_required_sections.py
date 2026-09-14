#!/usr/bin/env python3
"""Required-sections gate: flag content files missing mandatory sections.

contributing.md requires every content file to carry `## Summary`,
`## See Also`, and `## References & Learn More` (short `## References`
accepted). Interview banks must not carry a `## Code Examples` section —
that heading there is a mislabeled Q&A block (see the Sept 2026 audit).

Exemptions:
  - INDEX.md files (navigation, not chapters)
  - guide-style files (multiple `# Phase`/`# Part` H1 sections), matching
    the SDE Role Guides convention in contributing.md
  - personal/ (job-search records, not curriculum)
  - docs/superpowers/ (historical plans)

Usage:
  python3 scripts/check_required_sections.py           # report, exit 0
  python3 scripts/check_required_sections.py --strict  # exit 1 on gaps
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = ("/.git/", "/node_modules/", "/.archive/", "/.freebuff/",
        "/.sass-cache/", "/personal/", "/docs/superpowers/",
        # Records and repo meta, not curriculum chapters: interview-lane
        # playbooks, project interview-defense docs, and repo-level docs.
        "/80-lanes-abroad-full-stack/", "/81-lanes-indian-sde-faang/",
        "/projects/", "/docs/")

GUIDE_H1 = re.compile(r"^# (Phase|Part|Section) \d", re.M)


def is_guide(text: str) -> bool:
    return len(GUIDE_H1.findall(text)) >= 2


def check(p: Path) -> list[str]:
    text = p.read_text(encoding="utf-8", errors="replace")
    if is_guide(text):
        return []
    heads = {h.strip().lower() for h in re.findall(r"^## (.+)$", text, re.M)}
    missing = []
    if "summary" not in heads:
        missing.append("Summary")
    if "see also" not in heads:
        missing.append("See Also")
    if not ({"references & learn more", "references"} & heads):
        missing.append("References")
    if "interview-questions" in p.name and "code examples" in heads:
        missing.append("mislabeled Code Examples in interview bank")
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any content file misses required sections")
    args = ap.parse_args()

    rows = []
    n = 0
    for p in sorted(ROOT.rglob("*.md")):
        rel = "/" + p.relative_to(ROOT).as_posix()
        if any(s in rel for s in SKIP) or p.name == "INDEX.md":
            continue
        if p.name in ("README.md", "ROADMAP.md", "AGENTS.md", "contributing.md"):
            continue
        n += 1
        missing = check(p)
        if missing:
            rows.append((p.relative_to(ROOT).as_posix(), missing))

    print(f"Required-sections scan: {n} content files, {len(rows)} with gaps.")
    by_kind: dict[str, int] = {}
    for _, missing in rows:
        for m in missing:
            by_kind[m] = by_kind.get(m, 0) + 1
    for kind, count in sorted(by_kind.items(), key=lambda kv: -kv[1]):
        print(f"  {count:4}  missing {kind}")
    if rows and not args.strict:
        print("Top offenders (fix these first):")
        for rel, missing in rows[:12]:
            print(f"  {','.join(missing)}  ::  {rel}")
    if args.strict and rows:
        for rel, missing in rows:
            print(f"  {','.join(missing)}  ::  {rel}")
        print(f"\n{len(rows)} file(s) missing required sections (strict mode).")
        return 1
    if not args.strict:
        print("Advisory only — run with --strict to fail the build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
