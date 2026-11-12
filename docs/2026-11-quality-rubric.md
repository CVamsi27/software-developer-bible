# Quality rubric — the standard every section pass reports against (2026-11)

This document exists because a ledger is not evidence. `docs/2026-10-25-fullstack-coverage.json`
marks **984 of 984 files reviewed**, and the suite it belongs to is green, yet the reader's
complaints were concrete: stale facts, thin explanations of new topics, grammar, gaps for a
senior engineer, no useful startup-hiring guidance. All of those can be true at once with a
complete ledger, because "reviewed" recorded *that* a file was inspected, not *what standard*
it was held to.

So the 2026-11 pass re-reads the corpus against the seven checks below and reports the same
evidence for every section. A section pass is a commit, and its commit message names the files
touched, the defects by class, the examples actually executed, and anything it could not verify.

## The seven checks

| Check | Question | Evidence a pass must produce |
| ---------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R1 Accuracy** | Is each claim true for the version it names? | The command run and its observed output, or the vendor URL and the sentence it supports. A claim neither executed nor sourced is labelled as recollection, or removed. |
| **R2 Depth** | Does the chapter explain the mechanism, not just name it? | The chapter opens on a concrete problem or result, defines a term before using it, shows how the mechanism produces the result, and states the boundary where it stops working. |
| **R3 Execution** | Does every complete example run? | Command plus output in the pass notes. Fragments are framed as fragments (`// excerpt`) so a reader cannot mistake one for a program. |
| **R4 Prose** | Would an editor accept every sentence? | Gate 30 clean, then a read of the file: one idea per sentence, no sentence that has to be re-read to be parsed. Mechanical detection is a floor. |
| **R5 Structure** | Does the file follow the repo's shape? | AGENTS.md section flow, one canonical home per mechanism (a second treatment points at the owner), no TL;DR, exactly one Summary, headings that name their mechanism. |
| **R6 Companion** | Does `REVISION.md` test what the chapter now says? | At least five `**Q:**`/`**A:**` pairs, answers matching the corrected facts, each pointing at the section that supports it. Authored questions are kept, never regenerated wholesale. |
| **R7 Gates** | Does the repo's own machinery agree? | `python3 scripts/check_counts.py --write` for every count, link baseline updated only after a live probe, `bash scripts/verify.sh` green at the commit. |

R1 and R3 are the pair that separates "current" from "plausible". A version number read from a
changelog is R1 evidence; the same version installed and exercised is R3 evidence. When only
the weaker one was available, the pass says so.

## Phase 0 baseline — measured, not asserted

`python3 scripts/depth_report.py` walks the corpus and reports prose words (fence-aware, using
the same classifier gate 19 uses), fenced code, `##` sections and Definition length. Inventory
only: none of its numbers is a gate, because the cheapest way to satisfy a word floor is
padding, which is the failure being removed.

| Section | Files | Prose words | Chapters with no code fence | Chapters under 700 words |
| -------------------------- | ------- | ------------- | --------------------------- | ------------------------ |
| (root) | 7 | 12,442 | 0 | 0 |
| 00-strategy | 6 | 3,157 | 0 | 4 |
| 10-frontend | 179 | 165,718 | 0 | 38 |
| 20-backend | 225 | 231,223 | 1 | 6 |
| 30-architecture | 139 | 179,102 | 0 | 20 |
| 40-platform | 150 | 145,788 | 4 | 2 |
| 50-quality | 64 | 54,973 | 0 | 2 |
| 60-realtime | 20 | 18,712 | 0 | 0 |
| 70-interview-toolkit | 50 | 40,157 | 0 | 0 |
| 80-lanes-abroad-full-stack | 38 | 24,119 | 18 | 24 |
| 81-lanes-indian-sde-faang | 25 | 16,433 | 9 | 13 |
| projects | 33 | 64,031 | 4 | 0 |
| lanes | 1 | 169 | 0 | 0 |
| docs | 47 | 76,311 | 0 | 0 |
| **Total** | **984** | **1,032,335** | **36** | **109** |

558 of those files are learning chapters; the rest are INDEX files, interview banks, cheat
sheets and `REVISION.md` companions, which answer different questions. The thin list is a
reading order, not a verdict: a 350-word weekly tracker is not a shallow chapter, and a
2,000-word chapter can still name a mechanism without showing it. The lane directories supply
most of both lists, which is expected — they are plans and trackers.

## Gate 30 — what the prose gate is allowed to claim

Before a grammar gate can be trusted it has to be measured against the corpus it judges. The
first run of `scripts/check_prose.py` reported **10,154 findings** across the corpus. Reading
them showed **10,152** were artifacts of the detector, in four shapes:

| Reported as | Actually |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 8,150 doubled spaces | Masked code spans were blanked *to spaces*, so `use \`code\`, then` read as `use  , then`. The masker now writes a sentinel that keeps offsets but stops a rule at the span boundary. |
| 4 stutters | `Server-side side effects`, `Retry-After after`, `per-order order` — hyphenated compounds are correct English. |
| 32 unclosed bold runs | `apps/web/**`, `**projects/**` — glob syntax, and bold whose closing marker is also a glob's. Paragraph-level counting with a glob exemption replaced line-level counting. |
| 14 doubled periods | `1..n`, `-128..127`, a router's `..` path step — range notation. The dot half of the rule was removed rather than narrowed; a rule that fires on correct text buries its own signal. |

What remained was **one** genuine defect: a diagram line reading `proxy:  client → …` with a
doubled space and a lowercase sentence start, repaired in
`20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.04-file-upload-apis.md`.

That is the honest baseline: on the classes gate 30 can determine, this corpus was essentially
clean. It is not evidence that every sentence reads well — the gate cannot see a grammatical
sentence that says the wrong thing, or a paragraph whose order hides its point. Those are what
the read pass in R4 is for. Every rule now carries a pinned near-miss case in
`scripts/test_check_prose.py`, so widening one to catch more prose requires adding the case that
would break it.

## How a section pass is performed

In study order (root → `00-strategy` → `10-frontend` → `20-backend` → `30-architecture` →
`40-platform` → `50-quality` → `60-realtime` → `70-interview-toolkit` → `80-lanes-abroad` →
`81-lanes-indian-sde-faang` → `projects` → `lanes`), for every chapter, index, interview bank
and companion in that section:

1. Read the file. R2 and R4 are decided here; no script answers them.
2. Execute what runs. Record command and output; label what only a paid account could prove.
3. Fix only defects against R1–R7. Sound prose is left alone — a pass is not a restyle.
4. Re-verify any version claim; when a *class* of staleness is fixed, add the
   `scripts/check_freshness.py` rule that stops it returning.
5. Restamp counts, refresh the link baseline only after probing, run `bash scripts/verify.sh`,
   commit that section alone.

## Limits this rubric cannot remove

- Detection is mechanical, judgment is not. Gate 30 catches determinable classes; a reader
  still has to hear the sentence.
- Claims that need a paid vendor account (live Stripe charges, an AWS console flow, a funded
  model key) stay source-only and are labeled as such rather than executed.
- The local environment bounds execution: PostgreSQL 16.15 is the only server available here
  (no 17/18), the Docker daemon is down, and Go, Java, Rust and Kotlin are not installed. A
  claim that needs one of those is cited, not executed, and the pass says which.
- Nothing here proves a reader learns from the result. That needs fresh-reader testing, which
  is a separate proposal.
