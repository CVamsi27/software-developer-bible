#!/usr/bin/env python3
"""Gate 7 — the public repo must never reference the private workspace.

Born from the 2026-10-17 migration. Campaign material — CV, application
tracker, outreach playbook, reports, resume sources — used to live inside
this repository under the lane-80 `personal/` subtree. When the repo went
public, that subtree moved to a separate private repository, and two
reference shapes became defects in a public artifact:

  1. the retired in-repo path (the lane-80 folder plus `/personal`), and
  2. a github.com URL to the private workspace repository, and
  3. a local home-directory path into the private workspace.

Both are tight signatures of the moved subtree: a reader following either
gets a 404, and the reference itself keeps a public doc pointing at private
material — exactly the leak class the migration closed.

Scope: the public reading surface — Markdown, YAML and HTML anywhere except
`scripts/` (tooling keeps historical scoping logic; it is not publication
content) and dependency/build skips. Dated records are exempt by name
pattern: changelogs and reports (`docs/20XX-XX-XX-*`) and plans/specs
(`docs/superpowers/**`) legitimately quote the paths of their time — the
same tolerance `check_links.py` documents for reconstructed history.
Anything else — chapters, lane guides, INDEXes, READMEs, workflows,
configuration — must stay free of private-workspace references. AGENTS.md is
operator guidance, not a published reading page; it names canonical locations
so assistants can obey the repository boundary.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_scope import guard

REPO = Path(__file__).resolve().parent.parent

PATTERNS = [
    (
        "retired in-repo private path",
        re.compile(r"80-lanes-abroad-full-stack/personal\b"),
    ),
    (
        "link to the private workspace repository",
        re.compile(r"github\.com/CVamsi27/personal(?![\w-])"),
    ),
    (
        "local private-workspace path",
        re.compile(r"(?:~|\$\{?HOME\}?|/(?:Users|home)/[^\s/`]+)[/\\]repos[/\\]personal(?![\w-])"),
    ),
]

EXTS = {".md", ".yml", ".yaml", ".html"}
SKIP_DIRS = {".git", "node_modules", "vendor", "_site", ".archive",
             ".freebuff", "__pycache__", "scripts", "functions", "api"}


def is_dated(rel: Path) -> bool:
    """Changelogs, reports, plans and specs keep the paths of their time."""
    if rel.parts[:1] != ("docs",):
        return False
    if "superpowers" in rel.parts:
        return True
    return bool(re.match(r"\d{4}-\d{2}-\d{2}-", rel.name))


def discovered_files():
    files = []
    for path in REPO.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTS:
            continue
        rel = path.relative_to(REPO)
        if path.name == "AGENTS.md":
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if is_dated(rel):
            continue
        files.append((path, rel))
    return files


def main() -> int:
    files = discovered_files()
    guard(len(files), "markdown/YAML/HTML files")

    hits = []
    for path, rel in files:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            for label, pattern in PATTERNS:
                if pattern.search(line):
                    hits.append(f"{rel}:{n}: {label}\n    {line.strip()[:160]}")
    if hits:
        print("PRIVATE-WORKSPACE REFERENCES IN THIS PUBLIC REPO:\n")
        for h in hits:
            print(h)
        print(
            f"\n{len(hits)} reference(s) — remove them. Private material "
            f"lives in the private workspace repository."
        )
        return 1
    print(f"OK — {len(files)} public files scanned, 0 private-workspace references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
