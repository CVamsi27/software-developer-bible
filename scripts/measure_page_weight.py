#!/usr/bin/env python3
"""Measure the built page for every tracked Markdown file.

The review ledger's "fast" verdict is not a vibe: it records the bytes the
reader actually downloads for that page. Jekyll writes one HTML file per
Markdown source at the same path with an .html suffix, so the mapping is
deterministic and needs no server.

Usage:
  python3 scripts/measure_page_weight.py                 # summary only
  python3 scripts/measure_page_weight.py --write         # write the JSON ledger
  python3 scripts/measure_page_weight.py --json          # print the JSON
  python3 scripts/measure_page_weight.py --check         # fail above the budget

The JSON is review input, not a quality gate by itself. A page can be small
and still be bad, and a large interview bank can be legitimately large. The
budget is a reading-order signal: the reviewer must explain every exception.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

try:
    import brotli  # type: ignore
except ImportError:  # brotli is optional; gzip is the portable floor.
    brotli = None

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
OUT = ROOT / "docs" / "corpus-review" / "page-weight.json"
BUDGET_BYTES = 120_000
# _config.yml deliberately excludes this section from the published site:
# it contains personal lane material, and site-build.yml asserts that nothing
# personal reaches _site/. The files are still reviewed; they simply have no
# public page to weigh.
EXCLUDED_PREFIXES = ("81-lanes-indian-sde-faang/",)

ASSET_PATTERNS = {
    "scripts": re.compile(rb"<script\b[^>]*\bsrc=", re.I),
    "stylesheets": re.compile(rb"<link\b[^>]*rel=[\"']?stylesheet", re.I),
    "images": re.compile(rb"<img\b", re.I),
    "iframes": re.compile(rb"<iframe\b", re.I),
    "videos": re.compile(rb"<video\b", re.I),
}


def tracked_markdown() -> list[str]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "-z", "*.md"]
    )
    return sorted(p.decode() for p in raw.split(b"\0") if p)


def genre(path: str) -> str:
    name = Path(path).name
    if name == "INDEX.md":
        return "index"
    if name == "REVISION.md":
        return "revision"
    if "interview-questions" in name:
        return "interview"
    if path.startswith("docs/"):
        return "docs"
    if path.startswith("projects/"):
        return "project"
    if path.startswith(("80-", "81-")):
        return "lane"
    if path in {
        "README.md",
        "AGENTS.md",
        "contributing.md",
        "ROADMAP.md",
        "search.md",
        "design-qa.md",
        "lanes",
    }:
        return "root"
    return "chapter"


def html_for(md_path: str) -> Path | None:
    candidate = SITE / Path(md_path).with_suffix(".html")
    if candidate.is_file():
        return candidate
    # INDEX.md can also be emitted as a directory index.html. Never fall back
    # for other names: doing so silently maps a page that was not built (for
    # example the optional-front-matter CONTRIBUTING blacklist) onto the
    # folder's index and reports the wrong weight.
    if Path(md_path).name in {"INDEX.md", "index.md"}:
        fallback = SITE / Path(md_path).parent / "index.html"
        if fallback.is_file():
            return fallback
    return None


def measure(md_path: str) -> dict:
    html = html_for(md_path)
    row = {
        "path": md_path,
        "genre": genre(md_path),
        "html": None,
        "status": "not-built",
        "sourceBytes": (ROOT / md_path).stat().st_size,
        "rawBytes": None,
        "gzipBytes": None,
        "brotliBytes": None,
        "assets": {k: 0 for k in ASSET_PATTERNS},
    }
    if md_path.startswith(EXCLUDED_PREFIXES):
        row["status"] = "excluded"
        row["reason"] = "excluded by _config.yml; personal lane material is never published"
        return row
    if html is None:
        if Path(md_path).name.upper() in {"README.MD", "CONTRIBUTING.MD"}:
            row["reason"] = (
                "Jekyll optional-front-matter blacklists README/CONTRIBUTING names; "
                "the file is copied as a raw Markdown asset"
            )
        else:
            row["reason"] = "no HTML page in _site; rebuild the site before measuring"
        return row
    data = html.read_bytes()
    row.update(
        {
            "html": str(html.relative_to(ROOT)),
            "status": "built",
            "rawBytes": len(data),
            "gzipBytes": len(gzip.compress(data, 9)),
            "brotliBytes": len(brotli.compress(data, quality=11)) if brotli else None,
        }
    )
    row["assets"] = {name: len(pattern.findall(data)) for name, pattern in ASSET_PATTERNS.items()}
    return row


def percentile(values: list[int], fraction: float) -> int:
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * fraction))
    return ordered[index]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write docs/corpus-review/page-weight.json")
    parser.add_argument("--json", action="store_true", help="print the full JSON")
    parser.add_argument("--check", action="store_true", help="exit 1 when a page exceeds the budget")
    parser.add_argument("--budget", type=int, default=BUDGET_BYTES)
    args = parser.parse_args()

    if not SITE.is_dir():
        print(f"FAIL no built site at {SITE}; run the site build first", file=sys.stderr)
        return 2

    rows = [measure(path) for path in tracked_markdown()]
    built = [r for r in rows if r["status"] == "built"]
    excluded = [r for r in rows if r["status"] == "excluded"]
    raw = [r["rawBytes"] for r in built]
    over = [r for r in built if r["rawBytes"] > args.budget]

    print(f"tracked Markdown: {len(rows)}")
    print(f"built pages:      {len(built)}")
    print(f"excluded:         {len(excluded)}")
    print(f"not built:        {len(rows) - len(built) - len(excluded)}")
    if raw:
        print(f"median raw:       {statistics.median(raw) / 1024:.1f} KB")
        print(f"p90 raw:          {percentile(raw, 0.90) / 1024:.1f} KB")
        print(f"max raw:          {max(raw) / 1024:.1f} KB")
        print(f"over {args.budget // 1024} KB:      {len(over)}")
        for row in sorted(over, key=lambda r: r["rawBytes"], reverse=True)[:15]:
            print(f"  {row['rawBytes'] / 1024:7.1f} KB  {row['path']}")
    if brotli is None:
        print("brotli:           unavailable (gzip only)")

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "generated": "2026-11-15",
            "budgetBytes": args.budget,
            "trackedMarkdown": len(rows),
            "builtPages": len(built),
            "rows": rows,
        }
        OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {OUT.relative_to(ROOT)}")
    if args.check and over:
        print(f"FAIL {len(over)} page(s) exceed {args.budget} bytes", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
