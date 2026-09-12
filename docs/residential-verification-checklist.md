# Residential-Vantage Verification Checklist

> Companion runbook to the monthly `link-rot-audit` CI workflow. The audit
> probes all cited external URLs from a GitHub datacenter IP; some verdicts
> can only be confirmed by a human on a normal (residential) connection.
> This doc lists exactly which ones, and what to do with the result.

|  |  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Trigger** | Any CI run reporting SUSPECT > 0; a DEAD you doubt; quarterly warn-list sweep |
| **Time** | ~15 minutes per pass |
| **Tools** | A normal browser, `gh`, `python3 scripts/link_baseline.py` |
| **Record findings in** | `docs/2026-09-11-dead-link-remediation-report.md` (append a dated subsection) or the changelog maintenance contract |

## 0. Pull the current verdicts from the last CI run

```bash
gh run list --workflow=link-rot-audit.yml --limit 1          # get run id
gh run view --log --job=$(gh run view <RUN_ID> --json jobs \
  --jq '.jobs[0].databaseId') | grep -E '  (DEAD|SUSPECT|warn) '
```

Why vantage matters (full lesson: remediation report, lesson 6):
IP-reputation WAFs 404 datacenter fetchers on *live* pages, while
soft-404 shells serve HTTP 200 to residential clients. Status codes lie
in both directions — verify content, not status.

## 1. SUSPECT rows (hosts in `SUSPECT_DEAD_HOSTS`)

1. Open each URL in a normal browser tab.
2. If the page renders: the host is vantage-blocked, the citation is fine.
   Note it and move on.
3. If the browser shows "not found": confirm at the content level —
   open `https://r.jina.ai/<the-url>` in the browser and *read the body*.
   A "page not found" body (even with HTTP 200) means real rot.
4. On confirmed rot: search a replacement, probe-verify it, edit the
   citing file, run `python3 scripts/link_baseline.py --update`, commit
   the JSON with the doc change. Gates before commit (6/6).

## 2. Datacenter-blocked hosts (`DATACENTER_BLOCKED_HOSTS`, e.g. leetcode)

Their warns are skipped by design — a runner can never distinguish rot
from the block, so only you can see it:

1. List the citations:
   `grep -rn --include='*.md' leetcode.com . | grep -v .archive`
2. Spot-check a random ~10% in the browser (mix of problem pages and
   explore cards — explore-card paths are the ones that historically rot).
3. Fix dead ones exactly as in section 1 step 4.

## 3. Bot-wall WARNs that may hide rot

The residual warn list (currently ~56) is mostly genuine bot-walls:

- **Skip by design**: O'Reilly (403 always — accepted exclusion).
- **Check in browser**: Medium-family engineering publications
  (netflixtechblog, instagram-engineering, eng.lyft, blog.bitsrc.io),
  glassdoor, npmjs, cisa.gov, teamblind. Medium publications get retired
  behind their paywall/WAF — the browser shows whether the article body
  still exists. A "page not found" behind a wall is rot: re-cite.

## 4. Close the loop

- Append findings (date, URLs checked, verdicts, replacements made) to
  the remediation report.
- If a *new* host joins the false-dead class, add it to
  `SUSPECT_DEAD_HOSTS` (link_baseline.py) with a comment, and to this
  checklist if humans must keep verifying it.
- If a domain is confirmed fully dead, add it to `SHUTTERED_DOMAINS`
  (check_freshness.py) so the freshness gate blocks future citations.
- Re-run `bash scripts/verify.sh` — 6/6 must pass before any commit.
