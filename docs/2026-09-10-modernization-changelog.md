# Docs Modernization Changelog — September 2026

> **Dated review record:** counts, test results and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-08-explanation-depth-progress.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

> What changed in the software-developer-bible docs during the September 2026
> modernization pass, why, and how the new verification gates prevent the same
> classes of rot from shipping again.

|  |  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Status** | Final — co-authored via the doc-coauthoring workflow |
| **Date** | 2026-09-10 |
| **Trigger** | Stale `setTimeout`-chunking code flagged in `10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.02-call-stack.md` |
| **Scale** | 56 files changed, +337/−2,638 lines |

---


One user-flagged stale code sample turned into a repo-wide audit that found and
fixed three classes of rot: **outdated APIs** (`setTimeout` chunking instead of
`scheduler.yield()`, Pages Router examples, sync `params`, `url.parse()`,
`new Buffer()`), **fabricated or rotted reference citations** (fake archive
timestamps, never-existed URLs, dead site restructures), and **security
anti-patterns taught uncritically** (JWT in `localStorage`, unsanitized
`dangerouslySetInnerHTML`, interpolated SQL). The durable outcome is
`scripts/check_freshness.py` — 8 staleness rules plus an opt-in link-liveness
mode — wired into `scripts/verify.sh` as gate 5/6, so every class of rot this
pass fixed now fails verification mechanically. The dead-link remediation
(`docs/superpowers/plans/2026-09-10-dead-link-remediation.md`) added the
RETIRED-OWASP-CHEATSHEET rule and `scripts/link_baseline.py`, which snapshots
every cited external URL (`scripts/external-links-baseline.json`, ~2,230) so
the next audit diffs against known-good state instead of starting cold.

## 1. Why This Pass Happened

A single stale code sample (synchronous 1-billion-iteration loop chunked with
`setTimeout(..., 0)`) was flagged in the call-stack chapter. One instance
implied others: nothing in the repo distinguished "current" from "stale"
content, and no gate would catch the next one. The audit therefore scaled
repo-wide, and grew three further mandates along the way: remove redundant or
off-topic material that diluted the chapters, reorder sequences so basics
precede dependent topics, and add missing modern topics.

## 2. Content Changes

### Modernized APIs

| Was | Now | Where it mattered most |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------ |
| `setTimeout` chunking (with its ~4ms nested-timer clamping) | `scheduler.yield()` time-slicing, with RAF / Web Workers compared | execution-and-scope chapters |
| Pages Router-only examples (`getStaticProps` era) | App Router | Next.js stack, CDN architecture chapter |
| Sync `params: { id: string }` | `Promise<{ id: string }>` awaited (Next.js 15+) | data fetching, ISR, static exports, cheat sheets |
| `url.parse()` | WHATWG `new URL()` + `searchParams` | Node chapters |
| ES2024-era content | ES2025 (iterator helpers, `Object.groupBy` vs `Map.groupBy`, `Promise.withResolvers()`) | modern-and-interview chapters |
| No `use cache` / PPR coverage | dedicated treatment | caching chapters |

### Structure

- **Reordered** the execution-and-scope sequence to teach basics first.
- **Removed** duplication: a repeated function definition, and an off-topic
  heap deep-dive that now points to the memory chapters instead of inlining.
- **Added** `10-frontend/10.1-javascript/03-async-concurrency/10.1.3.05-abort-and-cancellation.md` —
  `AbortController`, `AbortSignal.timeout()` / `AbortSignal.any()`,
  `throwIfAborted()` cooperative cancellation, the classic stale-request React
  race, and `AbortError` handling — a core senior topic the JS stack lacked.
- **Extended** the interview bank with Q51–Q55 covering exactly the APIs above,
  so the bank tests what the docs now teach.

### Security anti-patterns taught uncritically

- `context-api.md`'s flagship auth demo persisted a JWT in `localStorage` —
  the docs' own auth chapters call this out as a mistake. Rewritten as an
  httpOnly-cookie session flow; the Context-teaching value is unchanged.
- `incremental-static-regeneration.md` piped raw CMS HTML into
  `dangerouslySetInnerHTML` (the textbook stored-XSS vector). Now sanitized
  (`DOMPurify`), with a note that ingestion-time sanitization is better.
- A DI example in `decorators.md` interpolated an id into SQL; now
  parameterized with the rule stated.

## 3. Reference-Link Findings (the citation problem)

This was the most serious finding class, in three tiers:

1. **Fabricated citations.** Five references cited the same fabricated
   `web.archive.org` timestamp — midnight on 1 July 2024, to the second, on
   five different "archived" pages, at least one of which never existed.
   Separately, Google's index contains no trace of three "official" URLs the
   docs cited (`wiki.postgresql.org/wiki/VACUUM`, `v8.dev/features/temporal`,
   an OWASP `Configuration_Cheat_Sheet`): they were generated, not observed.
   The durable fix for never-existed citations is citing official docs that
   certainly exist (e.g. postgresql.org's `routine-vacuuming` and
   `explicit-locking` chapters).
2. **Genuine site restructures.** AWS retired old guide paths, OWASP renamed
   cheat-sheet files, Node reorganized `/learn`, web.dev renumbered articles,
   Stripe renamed the idempotency endpoint docs, Google retired its
   `developers.google.com` web tree, sre.google and the Fowler EAA catalog
   dropped per-chapter URLs. These were real pages that moved; replacements
   were chosen from the new canonical locations.
3. **A fabricated domain.** A hash-tables citation pointed at a domain that
   does not exist; the real article is on the author's actual blog
   (`probablydance.com`).

**~40 citations were replaced**, each probe-verified live before being written
down. One of the dead links was introduced during this very pass (a PPR blog
post), caught by the gate's first liveness run — which is the argument for the
gate in one anecdote.

## 4. Verification Tooling Added or Hardened

### `scripts/check_freshness.py` (new — verify.sh gate 5/6)

| Rule | Catches |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `FAKE-ARCHIVE-TS` | The fabricated archive timestamp literal |
| `STALE-GOOGLE-WEB-TREE` | The retired Google web-docs tree |
| `LEGACY-PAGES-ROUTER-EXPORT` | `getStaticProps`/`getServerSideProps` outside the Next.js stack (which intentionally teaches both routers) |
| `SYNC-PARAMS` | Sync `params` signatures in Next.js contexts |
| `DEPRECATED-URL-PARSE` | Legacy `url.parse()` |
| `NEW-BUFFER` | Deprecated `new Buffer()` |
| `SETTIMEOUT-CHUNKING` | The original flagged pattern |

Scoping decisions that keep it false-positive-free: fence-aware (only
`ts/tsx/js/jsx` blocks), line comments stripped (so "// url.parse() is
deprecated" doesn't self-trigger), Next.js rules scoped to real Next.js
context, `docs/superpowers/` historical plans skipped. In `--check-urls` mode,
`personal/` job-link records are excluded from probing (expired listings are
historical records, not doc rot).

### `--check-urls N` liveness mode (opt-in, network; not in verify.sh)

Probes a deterministic sample of external links. Hardened through its first
full-sweep run: **GET-first** (PortSwigger-class sites 404 on HEAD but serve
GET — HEAD-first produced ~250 false DEADs), a 404 retry for transient
outages, paren-rebalancing for Wikipedia-style URLs, and a `MALFORMED` report
class for non-ASCII URLs. The first run immediately caught a dead citation —
the one introduced during this pass.

### Maintenance contract

`AGENTS.md` now carries the rule: when a modernization pass fixes a class of
staleness, add a gate rule so it cannot regress. The count guard's
recompute-and-restamp rule (never hand-edit scale claims) continues to apply.

## 5. What Deliberately Remains Open

- ~~Dead links in the blog/tutorial long tail~~ — resolved by the plan in
  `docs/superpowers/plans/2026-09-10-dead-link-remediation.md`: every cluster
  replaced with probe-verified live URLs or exact-timestamp Wayback snapshots
  (see git log, `docs:` commits of 2026-09-10/11); bot-walled WARNs (O'Reilly,
  JFrog) deliberately left as-is.
- ~~Wayback snapshot pass~~ — done: the iconic dead posts now cite exact-
  timestamp snapshots verified live at citation time; three fabricated
  High Scalability slugs were corrected to the real articles in the process.
- **The private `docita` GitHub repo links** (projects/docita docs cite them)
  404 only for unauthenticated probes; left as-is deliberately.
- ~~Commit~~ — done: the pass and the dead-link remediation plan are committed
  as a `docs:` commit series on `main`.

## 6. The Maintenance Contract

For future maintainers (human or agent):

1. Never hand-edit the scale claims (the "NNN files, NNK lines" string in four
   sites: root INDEX, 80-lane INDEX, contributing.md, AGENTS.md); recompute and
   restamp all four together — `check_counts.py` prints the exact expected
   string when they drift.
2. When you fix a staleness class, add a `check_freshness.py` rule for it.
3. Probe every URL before citing it; never cite an unverified URL, including
   "obviously fine" ones. After adding citations, run `python3 scripts/link_baseline.py`
   — every ADDED url must be probe-verified live — then `--update` and commit
   the baseline with the doc change.
4. A HEAD 404 is not evidence of death; check GET before replacing anything.
5. Run `bash scripts/verify.sh` before every commit — the six gates encode
   everything above mechanically.

## 7. Verification At Close

```
1/6 counts      OK — 809 files, 347K lines
2/6 alignment   PASS
3/6 structure   PASS (baseline lane-80.x GAPS only)
4/6 links       OK — 0 broken
5/6 freshness   OK — 9 rules
6/6 baseline    OK — 0 added, 0 removed
```

*(This file is itself scanned by gates 1 and 5 — the changelog about the gates
must pass them.)*
