#!/usr/bin/env python3
"""Weekly job-board watch.

Watches public job-board APIs for two signal classes:

1. REOPEN  - a previously-dead posting title reappears (e.g. SumUp SuperApp
   FS, which 410'd on 2026-09-13 while the program stayed alive).
2. GONE    - a posting the candidate APPLIED to has disappeared from the
   board while the tracker still says Applied/Evaluated (ghosting signal:
   bump the named contact per the playbook day-7 rule, or mark Dead).

Exit codes: 0 = nothing actionable, 1 = at least one REOPEN/GONE signal
(CI treats 1 as "open/update the watch issue"). Adding a target costs one
entry in WATCHES (or a --config JSON file with the same shape); no script
edits needed. Boards used are public JSON/XML endpoints probed with a
browser fingerprint - the same access a browser has.
"""

import argparse
import json
import sys
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

WATCHES = [
    {"board": "greenhouse:sumup", "reopen": ["Full-Stack Engineer, SuperApp"], "gone": []},
    {"board": "ashby:n8n", "reopen": [], "gone": ["Senior Product Engineer (TS/NodeJS/Vue)"]},
    {"board": "ashby:cosuno", "reopen": [], "gone": ["Senior Full Stack Developer (TypeScript)"]},
    {
        "board": "personio:leaseteq-ag",
        "reopen": [],
        "gone": ["Senior Full Stack Engineer - TypeScript / Next.js"],
    },
    {
        "board": "personio:snke",
        "reopen": [],
        "gone": ["Senior Software Engineer (Full-Stack) - Healthcare Applications"],
    },
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def titles_greenhouse(board: str) -> list:
    data = json.loads(fetch(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=false"))
    return [j.get("title", "") for j in data.get("jobs", [])]


def titles_ashby(board: str) -> list:
    data = json.loads(fetch(f"https://api.ashbyhq.com/posting-api/job-board/{board}"))
    return [
        j.get("title", "")
        for j in data.get("jobs", [])
        if str(j.get("isListed", "True")).lower() == "true"
    ]


def titles_personio(board: str) -> list:
    xml_text = fetch(f"https://{board}.jobs.personio.com/xml")
    root = ET.fromstring(xml_text)
    return [(pos.findtext("name") or "") for pos in root.iter("position")]


FETCHERS = {"greenhouse": titles_greenhouse, "ashby": titles_ashby, "personio": titles_personio}


def evaluate(watches):
    signals, oks = [], []
    for w in watches:
        kind, _, board = w["board"].partition(":")
        if kind not in FETCHERS:
            signals.append(f"CONFIG  {w['board']:<24} unknown board kind (use greenhouse|ashby|personio)")
            continue
        try:
            titles = FETCHERS[kind](board)
        except Exception as exc:  # noqa: BLE001 - a dead board is a warn, not a crash
            oks.append(f"warn    {w['board']:<24} fetch failed ({exc.__class__.__name__}) - board may be down")
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", help="JSON file with a WATCHES-shaped list; overrides the built-ins")
    args = parser.parse_args()

    watches = WATCHES
    if args.config:
        with open(args.config, encoding="utf-8") as fh:
            watches = json.load(fh)

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
