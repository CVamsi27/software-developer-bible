# Docs Modernization Changelog 2 — September 2026

> **Dated review record:** counts, test results and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-10-senior-precision-progress.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

> The second modernization pass: repetition removal, ordering fixes, missing
> topics, the closing-section gap driven to zero (and gate-enforced), merge
> artifacts purged, and every one of the 2,313 cited URLs probe-verified.
> Follows `2026-09-10-modernization-changelog.md` (pass 1) and
> `2026-09-11-dead-link-remediation-report.md`.

|  |  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status** | Final |
| **Date** | 2026-09-14 |
| **Trigger** | User request: fix stale code repo-wide, remove repetition and dilution, restore missing main points, close topic gaps, verify every citation |
| **Scale** | 3 content commits + 1 integrity commit; 195 files touched; net −4,000 lines of duplication/junk |

---


Pass 1 caught stale APIs; this pass caught the *structure* rot that makes the
bible feel diluted: chapters carrying two competing why-sections, interview
banks wearing the concept template, chapters ending with no Summary or onward
links, a curriculum gap where a tested topic was never taught, and old merge
grafts (repeated page tails, stray Phase headers) polluting chapter files.
Every fix class is now mechanically enforced: the required-sections gate
(`check_required_sections.py --strict`) is blocking gate 6 in `verify.sh`, and
the freshness gate grew to 11 rules. The citation layer is fully verified: the
committed baseline (2,313 URLs) was probed end to end — **0 dead, 0 suspect**.

## 1. Repetition — the main dilution source, quantified

- **92 files carried BOTH "Why It Matters" and "Why Do We Need It?"**
  back-to-back (template drift; contributing.md sanctions one why-section).
  79 with generic bullets were merged into a single senior-voice section with
  a compact **Concretely:** list; 13 with genuine Problem/Solution narratives
  were renamed "The Problem It Solves" and repositioned after Definition.
- **6 interview banks** had Q&A deep-dives mislabeled "Code Examples" —
  renamed (with cross-pointers where deep-dive and rapid-fire overlap).
- **40 files** opened with Definition before TL;DR, violating the repo's own
  template — all reordered; verified zero remaining.

## 2. Ordering — one real contradiction, one convention bug

- The 10.1 JavaScript stack INDEX claimed a read order that contradicted both
  the category INDEX rationale and the actual file numbering — aligned
  everywhere.
- **40 files** violated TL;DR-first (above).

## 3. Missing topics — the gap that mattered

- **Equality & type coercion was tested but never taught.** New chapter
  `10.1.4.09-equality-and-coercion.md`: the three conflicting coercion engines
  (ToNumber/ToPrimitive/truthiness), `==` decision flow, `??` vs `||` as a
  correctness decision, `Object.is`, classics derived rather than memorized.
- **ES2020 foundations** (`?.`, `??`) added to the ES2024+ chapter.
- Browser-context env config (`import.meta.env` / `NEXT_PUBLIC_*`) added to
  the modules chapter's `process.env.NODE_ENV` example.

## 4. The closing-section gap: 114 files → 0, then enforced

Scanning all content files against contributing.md's mandatory closing
sections (Summary / See Also / References) found **114 files missing at least
one** — mostly older flat chapters ending abruptly. All were closed with
content-specific sections (no boilerplate): mobile release trio, case studies
21–31, Docker production, CDN, IaC/CI-CD, testing frameworks,
production-engineering, and more. With the backlog at zero,
`check_required_sections.py --strict` became **blocking gate 6** — a new file
without the sections fails the build. Records (lanes, projects, docs,
repo-meta) are exempt as non-curriculum.

## 5. Merge-artifact purge (the "unwanted things" sweep)

- **19 files carried five duplicate `[ Back to Index]` footers** — an old
  automated merge grafted page tails repeatedly (203 junk lines removed;
  health-checks chapter also had 4 orphan footers mid-file). Exactly one
  canonical footer at EOF now, everywhere.
- **Two Java chapters** had a stray `# Phase N` header + one-line blurb
  grafted between References and Summary (grafts of the 81-lanes mega-guide's
  section titles) — removed.
- **3 See Also lines** a prior pass had collapsed into single lines were
  un-merged.
- **Number-theory chapter (70.2.5.01)** tail held a stray Phase header and 5
  duplicate footers — removed.
- Freshness gate grew **DUPLICATE-FOOTER** and **STRAY-GRAFT-HEADER** rules
  (81-lanes guides allowlisted for legitimate `# Phase` structure) — these
  classes cannot ship again.

## 6. Citation integrity: every URL verified

- All new external citations were probe-verified before entering the baseline;
  9 dead or unverifiable citations from batches 1–2 were replaced with live,
  semantically-correct URLs (correct SRE Book/Workbook chapters, AWS RDS docs,
  Cloudflare/Fastly purge docs, canonical JUnit docs home, Fowler *evodb*,
  Richardson's own Maturity Model article, Informit for *Effective Java*).
  O'Reilly library URLs resist all verification (WAF) and were replaced with
  verifiable equivalents; Baeldung stayed — verified live server-side.
- 8 broken relative links in newly-added See Also sections were fixed (wrong
  `../` depth, wrong category names, wrong file number).
- **Full baseline probe (2,313 URLs): 0 dead, 0 suspect** — 1,813 live, 364
  by-design skips, 136 warns decomposing into known bot-walls (LeetCode,
  npm, Stack Overflow, Cloudflare learning, Medium blogs) and slow hosts
  (arxiv PDFs, securityheaders.com) — none rot.

## 7. Verification at close

```
1/6 counts      OK — 830 files, 349K lines
2/6 alignment   PASS
3/6 structure   PASS (830 files)
4/6 links       OK — 7,154 links checked (204 anchors), 0 broken
5/6 freshness   OK — 11 rules
6/6 sections    OK — 542 content files, 0 gaps (STRICT)
   + baseline   OK — 2,313 URLs, 0 added / 0 removed, 0 dead on probe
```

## 8. Durable rules for future passes

1. The gates are the spec: if a defect class needed a manual sweep twice, it
   needs a rule (this pass added three: required-sections strict, duplicate
   footers, stray grafts).
2. Never bulk-overwrite a chapter from its tail — read the whole file first
   (one overwrite was caught and restored from git within the same session).
3. 403 is not 404: verify bot-walled hosts server-side (or via a server-side
   fetcher) before declaring them dead; replace only the truly unverifiable.
4. Citation changes ship as a pair: doc commit + probe-verified baseline
   update, together, or the baseline diff gate fails the build.

Commits: `247812c9` (dedup/order/gap) → `9cb477f6` (worst gaps + gate) →
`5754d1f9` (full gap closure, gate strict) → `d0f18621` (artifact purge +
probe).
