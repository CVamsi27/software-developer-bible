# Dead-Link Remediation — Outcome Report (September 2026)

Closing report for the dead-link remediation executed from
`docs/superpowers/plans/2026-09-10-dead-link-remediation.md`. It records
what was replaced, what was deliberately left alone, what the audit
discovered about *how* the links died, and the tooling that now keeps
the citation set healthy. The execution log is the `docs:` commit series
from `2d02534` to `f53f345`; this document is the summary a future
maintainer reads first.

|  |  |
| ------------------ | ------------------------------------------------------------------------------------ |
| **Status** | Complete — all 10 plan tasks executed and committed |
| **Executed** | 2026-09-10 → 2026-09-11 |
| **Starting point** | ~200+ dead external citations across the docs |
| **Final state** | 0 dead · 1,707 live · 522 bot-wall warns · 1 by-design exclusion (2,230 URLs probed) |
| **Gates** | `bash scripts/verify.sh` 5/5 PASS at every commit |

## 1. Results in numbers

- **13 remediation commits**, touching **~200 citation sites in ~180 files**
  (per-commit file counts in `git log --shortstat 1c193d93..HEAD`).
- **~180 distinct dead URLs replaced**, every single one with a replacement
  GET-verified live at citation time — no guessed URLs were written.
- **5 exact-timestamp Wayback snapshots** cited (verified 200 at citation time).
- **2 citations removed** rather than replaced (deleted repos / posts with no
  snapshot and no successor; noted in the respective commit messages).
- **1,707 of 2,230 baseline URLs** probe live; the 522 warnings are
  bot-walls (403/429/202 mitigation), not rot — see §4.

## 2. How the links died — the four failure classes

The audit's most useful output was the taxonomy. Every dead citation fit
one of these classes, and two of them were invisible to a naive link
checker:

1. **Genuine restructures** — the majority. Sites move content without
   redirects (martinfowler.com, brendangregg.com, patterns.dev, OWASP's
   site-wide `cheat-sheets/` → `cheatsheets/` rename, basarat gitbook,
   High Scalability, GitHub `master`→`main` renames and blob-path rot).
2. **Retired content** — pages deleted upstream with no successor
   (substack/stream-handbook, DefinitelyTyped's `Contributors.md`,
   changesets' intro doc, the Princeton COS 226 lecture PDF, EDB's vacuum
   series). Fix: canonical doc page, maintained successor repo, or Wayback.
3. **Fabricated citations** — the alarming class. URLs that *look*
   plausible but never existed: a High Scalability "1-billion-views
   YouTube" slug (real post is the 2008 `youtube-architecture` article),
   a never-archived "2011 Dropbox tech-talk" slug, a never-existed Google
   monorepo paper title. AI-era citation rot: plausible-shaped, zero
   ground truth. Detection: CDX prefix searches showing the slug was
   **never archived, ever**.
4. **Bot-wall false positives** — O'Reilly (403), JFrog (202 + empty body,
   with sweep runs intermittently returning 404), W3C APG (403),
   LinkedIn (404 even with browser headers → treated as dead and replaced
   with levels.fyi). WARN ≠ DEAD; only repeated browser-header GET 404s
   justify replacement.

## 3. Deliberate exclusions

| Target | Reason |
| ---------------------------- | ------------------------------------------------------------------------------- |
| `github.com/CVamsi27/docita` | Private repo; 404s only for unauthenticated probes. Documented in changelog §5. |
| O'Reilly library links | 403 bot-wall; page serves fine in browsers. |
| JFrog help center | 202 + empty body on every path; the sweep 404 was transient. |
| W3C APG pages | 403 bot-wall during audit; left per WARN≠DEAD. |
| `personal/` lanes | Historical records (applications, targets); expired links there are expected. |

## 4. Tooling added (the durable outcome)

1. **`scripts/check_freshness.py` rule `RETIRED-OWASP-CHEATSHEET`** — now
   8 rules. Catches both retired OWASP URL forms; the short-host branch
   needs a `(?<![\w.])` guard so it does not match inside the *good*
   `cheatsheetseries.owasp.org/cheatsheets/` URLs (unit-tested 6/6).
2. **`scripts/link_baseline.py` + `scripts/external-links-baseline.json`** —
   committed snapshot of all 2,230 cited URLs. Bare run diffs the tree
   against it and fails on unverified ADDED URLs; `--probe` GET-probes
   everything. Its first run immediately caught one dead citation the
   cluster sweeps had missed (the Princeton PDF misattributing Bloom's
   1970 paper).
3. **`.github/workflows/link-rot-audit.yml`** — monthly (3rd, 06:00 UTC)
   plus manual-run audit: full probe, tracking issue opened/updated only
   when dead links exist, stale issue auto-closed on a clean run. Warns
   never fail the job. First live run needs a manual **Run workflow**
   click in the Actions tab (scheduled runs take over from the next month).

Workflow after adding citations (contributing.md, maintenance contract):
probe-verify → edit docs → `link_baseline.py` (must show no unverified
ADDED) → `--update` → commit baseline JSON with the doc change.

## 5. Lessons for the next audit

- **The committed baseline changes the audit's shape**: start from a diff,
  not a cold sweep. The ~200-link backlog existed because nothing recorded
  what *should* be live.
- **Probe exactly like the checker probes** (urllib GET, browser UA,
  2-retry). curl and urllib can disagree (JFrog); the gate's verdict is
  the one that counts.
- **Ground truth beats memory for famous URLs** — the "everyone knows"
  High Scalability slugs were the fabricated ones. CDX + GET verification
  all the way down.
- **Wayback last, exact always**: live replacement preferred; when
  archiving, cite the machine-found timestamp and GET-verify it — never a
  hand-typed `web.archive.org/web/2024...` guess.
- **Site-wide renames are rule-worthy**: one rename broke N citations.
  The OWASP rule now fails verify.sh on any regression. When the next
  rename class appears, add its rule the same day (see also AGENTS.md).

## 6. See also

- `docs/superpowers/plans/2026-09-10-dead-link-remediation.md` — the plan
- `docs/2026-09-10-modernization-changelog.md` — §5 open items, §6 maintenance contract
- `contributing.md` — gate table incl. the link-baseline row
- Commit series: `git log --oneline 1c193d93..HEAD`
