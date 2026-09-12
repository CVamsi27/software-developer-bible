#!/usr/bin/env python3
"""External-link baseline: snapshot, diff, and probe every cited URL.

Born from the Sept 2026 dead-link remediation (the audit started from
"~200 dead links" with no record of what should be there). This tool
keeps a committed baseline of every external URL cited in the docs so
the next audit diffs against known-good state instead of starting cold.

The baseline is deliberately OUTSIDE verify.sh (like check_freshness
--check-urls): it is an audit tool, not a per-commit gate.

Usage:
  python3 scripts/link_baseline.py --update   # re-capture the baseline
  python3 scripts/link_baseline.py            # diff current tree vs baseline
  python3 scripts/link_baseline.py --probe    # GET-probe ALL baseline URLs

Workflow after adding citations: run bare diff; every ADDED url must be
probe-verified live (WARN bot-walls are acceptable, DEAD is not), then
re-run --update and commit the baseline together with the doc change.
"""
import argparse
import concurrent.futures
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_freshness import (  # noqa: E402
    MD_LINK_URL, URL_SKIP, iter_md_files, probe, repair_url,
)

ROOT = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / 'external-links-baseline.json'

# Documented by-design exclusions: URLs that 404 for unauthenticated probes
# but are correct citations (private repos, bot-walled hosts). Mirrors the
# exclusions accepted in the Sept 2026 remediation (changelog section 5).
KNOWN_404_OK = (
    'github.com/CVamsi27/docita',
)

# Hosts whose WAFs are IP-reputation-based: they 404 datacenter fetchers
# (GitHub runners) on LIVE pages, so a runner-side DEAD verdict cannot be
# trusted for these hosts — probe()'s browser-header retry cannot help
# because the decision is made on the client IP, not the headers. A DEAD
# on these hosts is reported as SUSPECT: still printed and surfaced in CI
# summaries, but excluded from the failing exit code and the issue flow,
# pending manual verification from a residential vantage. Verify at the
# CONTENT level (e.g. fetch through r.jina.ai and read the body): status
# codes lie in both directions — Topcoder served HTTP 200 soft-404 shells
# to a residential client while returning real 404s elsewhere.
SUSPECT_DEAD_HOSTS = (
    'topcoder.com',
)

# Hosts that drop/refuse datacenter-IP probes entirely ('no response')
# while serving human readers normally — leetcode drops connections from
# GitHub runners on every page (360 of 434 CI warns). From a runner, real
# rot there is indistinguishable from the block, so these warns carry no
# signal: reported as by-design skips (like docita) instead of drowning
# the warn budget. Rot on these hosts can only be caught from a
# residential vantage — see the remediation report, lesson 6.
DATACENTER_BLOCKED_HOSTS = (
    'leetcode.com',
)


def collect() -> dict:
    """Return {url: sorted [relative citing files]} over living docs.

    Mirrors check_freshness.collect_external_urls: same skip rules
    (.archive, plans, personal/, badge hosts) so the two tools always
    see the same link set.
    """
    files = {}
    for p, rel in iter_md_files(ROOT):
        if '/personal/' in f'/{rel}':
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        for m in MD_LINK_URL.finditer(text):
            u = repair_url(text, m)
            if any(s in u for s in URL_SKIP):
                continue
            files.setdefault(u, [])
            if rel not in files[u]:
                files[u].append(rel)
    return {u: sorted(fs) for u, fs in sorted(files.items())}


def load() -> dict:
    if not BASELINE.exists():
        sys.exit(f'no baseline at {BASELINE}; run with --update first')
    return json.loads(BASELINE.read_text())['urls']


def update() -> None:
    urls = collect()
    BASELINE.write_text(json.dumps(
        {'generated': __import__('datetime').date.today().isoformat(),
         'url_count': len(urls), 'urls': urls},
        indent=1, sort_keys=True) + '\n')
    print(f'baseline written: {len(urls)} urls -> {BASELINE.name}')


def diff() -> None:
    base, cur = load(), collect()
    added = sorted(set(cur) - set(base))
    removed = sorted(set(base) - set(cur))
    for u in added:
        print(f'ADDED    {u}')
    for u in removed:
        print(f'REMOVED  {u}')
    print(f'\n{len(added)} added, {len(removed)} removed '
          f'(baseline {len(base)}, now {len(cur)})')
    if added:
        print('verify each ADDED url is live (probe it), then re-run --update')
        sys.exit(1)


def row_for(u: str, status: str) -> tuple[str, str]:
    """Classify one probe result as (printed label, bucket).

    Buckets: skipped (by-design exclusions: DEAD on private-repo citations,
    WARN on datacenter-blocked hosts), dead (actionable rot),
    suspect (datacenter-IP false-dead candidate — never fails the run),
    warned (bot-wall noise), live.
    """
    if status == 'DEAD' and any(s in u for s in KNOWN_404_OK):
        return 'skip', 'skipped'
    if status == 'DEAD':
        if any(h in u for h in SUSPECT_DEAD_HOSTS):
            return 'SUSPECT', 'suspect'
        return 'DEAD', 'dead'
    if status == 'WARN':
        if any(h in u for h in DATACENTER_BLOCKED_HOSTS):
            return 'skip', 'skipped'
        return 'warn', 'warned'
    return 'ok', 'live'


def probe_all() -> None:
    urls = sorted(load())
    print(f'probing all {len(urls)} baseline urls...')
    buckets = {'skipped': 0, 'dead': [], 'suspect': [], 'warned': [], 'live': 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        for u, (status, detail) in zip(urls, ex.map(probe, urls)):
            label, bucket = row_for(u, status)
            if bucket == 'skipped':
                buckets['skipped'] += 1
                note = ('(by-design 404)' if status == 'DEAD'
                        else f'(datacenter-blocked: {detail})')
                print(f'  {label:4}  {note:30}  {u}')
            elif bucket == 'dead':
                buckets['dead'].append((u, detail))
                print(f'  {label:4}  {detail:20}  {u}')
            elif bucket == 'suspect':
                buckets['suspect'].append((u, detail))
                print(f'  {label}  {detail:18}  {u}  (host 404s datacenter IPs — verify manually, see report)')
            elif bucket == 'warned':
                buckets['warned'].append((u, detail))
                print(f'  {label:4}  {detail:20}  {u}')
    print(f'\n{len(buckets["dead"])} dead, {len(buckets["suspect"])} suspect, '
          f'{len(buckets["warned"])} warn '
          f'(warns are usually bot-walls, not rot), {buckets["skipped"]} by-design, '
          f'{buckets["live"]} live')
    if buckets['suspect']:
        print('SUSPECT rows: these hosts 404 datacenter IPs on live pages — '
              'verify from a residential vantage before changing anything.')
    sys.exit(1 if buckets['dead'] else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--update', action='store_true', help='re-capture the baseline')
    ap.add_argument('--probe', action='store_true', help='GET-probe every baseline url')
    args = ap.parse_args()
    if args.update:
        update()
    elif args.probe:
        probe_all()
    else:
        diff()


if __name__ == '__main__':
    main()
