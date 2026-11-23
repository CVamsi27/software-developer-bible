#!/usr/bin/env python3
"""Live job-board discovery and weekly ATS watch.

Supports two modes against public ATS feeds (Greenhouse, Ashby, Lever, Personio):

1. Watch mode (default): monitors previously-targeted postings for two signals:
   - REOPEN: a previously-closed posting title reappears on the board.
   - GONE:   an applied posting disappeared from the board (follow up or close).
   Exit codes: 0 = nothing actionable, 1 = at least one REOPEN/GONE signal.

2. Discover mode (--discover): queries a list of public ATS boards and filters
   live open roles by --query (comma-separated title keywords) and --location
   (comma-separated location substrings), printing matching titles, locations,
   and direct employer ATS URLs (or --json).

Targets are personal application data, so they never live in this public
repository. Supply them with --config (or JOB_WATCH_CONFIG) pointing at a JSON
file kept in your private workspace:
  - Watch format:    [{"board": "greenhouse:acme", "reopen": ["..."], "gone": ["..."]}]
  - Discover format: ["greenhouse:acme", "ashby:acme", "lever:acme", "personio:acme"]
                     or {"boards": [...]} or watch-format entries (board keys reused).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

TIMEOUT = 25
UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
}

# Deliberately empty: watch/discovery targets are personal data kept in the
# private canonical workspace. Load them via --config or JOB_WATCH_CONFIG.
WATCHES = []


class BoardFetchError(Exception):
    """Board returned a non-200 status (rate-limit, WAF, wrong slug, down)."""


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        # Never treat a non-200 as an empty board: Personio 307-redirects bad
        # slugs to personio.com (429 there), WAFs 403, rate limits 429. An
        # empty list from such a response would fire false GONE signals.
        raise BoardFetchError(f"HTTP {exc.code}") from exc


def jobs_greenhouse(board: str) -> list[dict]:
    data = json.loads(fetch(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=false"))
    out = []
    for j in data.get("jobs", []):
        loc = j.get("location") or {}
        out.append({
            "board": f"greenhouse:{board}",
            "title": j.get("title", ""),
            "location": loc.get("name", "") if isinstance(loc, dict) else str(loc),
            "url": j.get("absolute_url", f"https://boards.greenhouse.io/{board}"),
        })
    return out


def jobs_ashby(board: str) -> list[dict]:
    data = json.loads(fetch(f"https://api.ashbyhq.com/posting-api/job-board/{board}"))
    out = []
    for j in data.get("jobs", []):
        if str(j.get("isListed", "True")).lower() != "true":
            continue
        loc = j.get("location", "")
        if j.get("isRemote"):
            loc = f"{loc} (Remote)".strip() if loc else "Remote"
        out.append({
            "board": f"ashby:{board}",
            "title": j.get("title", ""),
            "location": loc,
            "url": j.get("jobUrl") or j.get("applyUrl") or f"https://jobs.ashbyhq.com/{board}",
        })
    return out


def jobs_lever(board: str) -> list[dict]:
    data = json.loads(fetch(f"https://api.lever.co/v0/postings/{board}?mode=json"))
    if not isinstance(data, list):
        raise BoardFetchError("unexpected non-list Lever payload")
    out = []
    for j in data:
        cats = j.get("categories") or {}
        loc = cats.get("location", "") if isinstance(cats, dict) else ""
        workplace = j.get("workplaceType", "")
        if workplace and workplace.lower() == "remote" and "remote" not in loc.lower():
            loc = f"{loc} (Remote)".strip() if loc else "Remote"
        out.append({
            "board": f"lever:{board}",
            "title": j.get("text", ""),
            "location": loc,
            "url": j.get("hostedUrl", f"https://jobs.lever.co/{board}"),
        })
    return out


def jobs_personio(board: str) -> list[dict]:
    xml_text = fetch(f"https://{board}.jobs.personio.com/xml")
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        # A redirect-to-HTML page parses as garbage: treat as fetch failure
        # (warn) rather than "0 positions" (false GONE).
        raise BoardFetchError("non-XML response (wrong slug or redirected)") from exc
    out = []
    for pos in root.iter("position"):
        pid = (pos.findtext("id") or "").strip()
        title = (pos.findtext("name") or "").strip()
        office = (pos.findtext("office") or "").strip()
        url = f"https://{board}.jobs.personio.com/job/{pid}" if pid else f"https://{board}.jobs.personio.com/"
        out.append({
            "board": f"personio:{board}",
            "title": title,
            "location": office,
            "url": url,
        })
    return out


def titles_greenhouse(board: str) -> list[str]:
    return [j["title"] for j in jobs_greenhouse(board)]


def titles_ashby(board: str) -> list[str]:
    return [j["title"] for j in jobs_ashby(board)]


def titles_lever(board: str) -> list[str]:
    return [j["title"] for j in jobs_lever(board)]


def titles_personio(board: str) -> list[str]:
    return [j["title"] for j in jobs_personio(board)]


JOB_FETCHERS = {
    "greenhouse": jobs_greenhouse,
    "ashby": jobs_ashby,
    "lever": jobs_lever,
    "personio": jobs_personio,
}
FETCHERS = {
    "greenhouse": titles_greenhouse,
    "ashby": titles_ashby,
    "lever": titles_lever,
    "personio": titles_personio,
}


def evaluate(watches):
    signals, oks = [], []
    for w in watches:
        kind, _, board = w["board"].partition(":")
        if kind not in FETCHERS:
            signals.append(f"CONFIG  {w['board']:<24} unknown board kind (use greenhouse|ashby|lever|personio)")
            continue
        try:
            titles = FETCHERS[kind](board)
        except Exception as exc:  # noqa: BLE001 - a dead board is a warn, not a crash
            detail = str(exc) or exc.__class__.__name__
            oks.append(f"warn    {w['board']:<24} fetch failed ({detail}) - treated as unknown, NOT a GONE signal")
            continue
        lowered = [t.lower() for t in titles]
        for term in w.get("reopen", []):
            if any(term.lower() in t for t in lowered):
                signals.append(f"REOPEN  {board:<12} '{term}' is listed again -> apply fast with the existing draft answers")
            else:
                oks.append(f"ok      {board:<12} '{term}' still closed (as expected)")
        for term in w.get("gone", []):
            if any(term.lower() in t for t in lowered):
                oks.append(f"ok      {board:<12} '{term}' still listed")
            else:
                signals.append(f"GONE    {board:<12} '{term}' no longer listed -> check spam, then bump the named contact or mark Dead")
    return signals, oks


def parse_board_specs(raw) -> list[str]:
    """Accept a list of 'kind:slug' strings, {'boards': [...]}, or watch-shaped dicts."""
    items = raw.get("boards", []) if isinstance(raw, dict) else raw
    specs = []
    for item in items:
        if isinstance(item, str) and item.strip():
            specs.append(item.strip())
        elif isinstance(item, dict) and item.get("board"):
            specs.append(str(item["board"]).strip())
    return list(dict.fromkeys(specs))


def split_terms(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


def discover(board_specs: list[str], query_terms: list[str], location_terms: list[str]):
    matches, warnings = [], []
    for spec in board_specs:
        kind, _, board = spec.partition(":")
        if kind not in JOB_FETCHERS:
            warnings.append(f"CONFIG  {spec:<24} unknown board kind (use greenhouse|ashby|lever|personio)")
            continue
        try:
            postings = JOB_FETCHERS[kind](board)
        except Exception as exc:  # noqa: BLE001 - one failed board never aborts discovery
            detail = str(exc) or exc.__class__.__name__
            warnings.append(f"warn    {spec:<24} fetch failed ({detail})")
            continue
        for job in postings:
            title_l = job["title"].lower()
            loc_l = job["location"].lower()
            if query_terms and not any(q in title_l for q in query_terms):
                continue
            if location_terms and not any(loc in loc_l or loc in title_l for loc in location_terms):
                continue
            matches.append(job)
    return matches, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", help="JSON file with watch entries or board specs; overrides built-ins")
    parser.add_argument("--discover", action="store_true", help="Query live openings across configured ATS boards")
    parser.add_argument("--query", help="Comma-separated title keywords to match in --discover mode")
    parser.add_argument("--location", help="Comma-separated location keywords to match in --discover mode")
    parser.add_argument("--json", action="store_true", help="Emit JSON output in --discover mode")
    args = parser.parse_args()

    raw_config = None
    config_path = args.config or os.environ.get("JOB_WATCH_CONFIG")
    if config_path:
        with open(config_path, encoding="utf-8") as fh:
            raw_config = json.load(fh)

    if args.discover:
        boards = parse_board_specs(raw_config) if raw_config else []
        if not boards:
            print(
                "No boards configured for discovery. Pass --config <json> or set "
                "JOB_WATCH_CONFIG with 'greenhouse:<slug>', 'ashby:<slug>', "
                "'lever:<slug>', or 'personio:<slug>' entries kept in your private workspace."
            )
            return 0
        matches, warnings = discover(boards, split_terms(args.query), split_terms(args.location))
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        if args.json:
            print(json.dumps({"checked_at": stamp, "matches": matches, "warnings": warnings}, indent=2))
            return 0
        lines = [f"Live ATS discovery — {stamp}", ""]
        for m in matches:
            loc = m["location"] or "Location unspecified"
            lines.append(f"  [{m['board']}] {m['title']}  —  {loc}")
            lines.append(f"    {m['url']}")
        if warnings:
            lines.append("")
            lines += [f"  {w}" for w in warnings]
        lines += ["", f"{len(matches)} matching role(s), {len(warnings)} warning(s) across {len(boards)} board(s)."]
        print("\n".join(lines))
        return 0

    watches = raw_config if isinstance(raw_config, list) else []
    if not watches:
        print(
            "No watch targets configured. Pass --config <json> or set "
            "JOB_WATCH_CONFIG; targets are personal data kept in the private "
            "workspace, never this repository."
        )
        return 0

    signals, oks = evaluate(watches)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"Job-board watch — {stamp}", ""]
    lines += [f"  {s}" for s in signals]
    lines += [f"  {o}" for o in oks]
    lines += ["", f"{len(signals)} signal(s), {len(oks)} ok/warn across {len(watches)} board(s)."]
    print("\n".join(lines))
    return 1 if signals else 0


if __name__ == "__main__":
    sys.exit(main())
