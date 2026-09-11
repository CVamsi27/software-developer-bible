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


def probe_all() -> None:
    urls = sorted(load())
    print(f'probing all {len(urls)} baseline urls...')
    dead, warned, skipped = [], [], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        for u, (status, detail) in zip(urls, ex.map(probe, urls)):
            if any(s in u for s in KNOWN_404_OK):
                skipped += 1
                print(f'  skip  {"(by-design 404)":20}  {u}')
            elif status == 'DEAD':
                dead.append((u, detail))
                print(f'  DEAD  {detail:20}  {u}')
            elif status == 'WARN':
                warned.append((u, detail))
                print(f'  warn  {detail:20}  {u}')
    print(f'\n{len(dead)} dead, {len(warned)} warn '
          f'(warns are usually bot-walls, not rot), {skipped} by-design, '
          f'{len(urls) - len(dead) - len(warned) - skipped} live')
    sys.exit(1 if dead else 0)


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
