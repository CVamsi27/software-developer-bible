# Phase 0 — Full Corpus Rework Plan

> **Status:** Proposed — awaiting your review before any rework begins.
> **Prepared:** 25 November 2026
> **Input:** 991-file corpus, all 34 verification gates passing, tree clean on `main`.

---

## Goal

Rework every study chapter so a senior developer can read it once, understand the mechanism, trace a worked example, and defend the failure boundary — without rereading or hunting for context. The rework covers readability, explanation depth, code examples, grammar, topic coverage, current-version accuracy, and startup/job-relevant material.

---

## Why a Full Rework Is Needed

The corpus passed all structural, link, template, and count gates — but the user's experience is that pages are still hard to read:

> "I still see some is missing … I am not able to read and understand what's written. If required rewrite everything."
> "I wanted this type of analysis and changes on all files which is the agenda of this whole work done in this thread."

The last analysis pass (`2026-11-25 13:23`) scanned all technical concept chapters (stacks 10–70) and found:

| Signal | Count | Example chapters |
|--------|-------|------------------|
| Thin (<130 lines) | 99 | `20.3.1.04-rest-maturity-model`, `40.1.06-production-patterns`, `50.2.01-wcag-overview`, `10.3.1.03-reconciliation` |
| Hedged (≥3 hedge phrases) | 47 | `10.1.1.07-v8-execution-and-optimization` (10), `40.4.4.03-ebpf-observability` (7), `40.1.08-image-signing-sbom-supply-chain` (7) |
| No real code block | 47 | Same set overlapping thin + hedged |
| Riddle opening (starts with "?") | 10 | `10.1.1.06-closures`, `10.1.1.07-v8-execution-and-optimization`, `30.1.1.01-solid-principles`, etc. |
| Smart-quote files | 98 across stacks | 35 frontend, 35 backend, 13 quality, 8 platform, 5 realtime |

The V8 chapter itself (211 lines, referenced by the user) opens with a question — "A function can run slowly on its first calls, accelerate after dozens of iterations, then suddenly slow down…" — which is a hook, but the user flagged it as still not readable end-to-end. That confirms: **passing gates is not the same as reading clearly.**

---

## Scope: Every Topic Chapter Across All Stacks

| Stack | Dir | Concept files (est.) | Primary audience |
|-------|-----|---------------------|------------------|
| Strategy | `00-strategy/` | 5 | Resume, communication, STAR, startup roles |
| Frontend | `10-frontend/` | 127 | JavaScript, TypeScript, React, Next.js, HTML/CSS/PWA, mobile |
| Backend | `20-backend/` | 149 | Node.js, NestJS, REST, databases, auth, security, AI engineering |
| Architecture | `30-architecture/` | 109 | System design, design patterns, infrastructure decisions |
| Platform | `40-platform/` | 95 | Docker, Kubernetes, CI/CD, observability, Git, serverless, monorepo, CDN |
| Quality | `50-quality/` | 39 | Testing, accessibility, performance, production engineering |
| Real-Time | `60-realtime/` | 11 | WebSockets, SSE, scaling patterns |
| Interview Toolkit | `70-interview-toolkit/` | 34 | Coding patterns, behavioral, revision |
| Abroad Full-Stack | `80-lanes-abroad-full-stack/` | 36 | Company prep sheets, Germany domain primer, target engine |

**Excluded:** `81-lanes-indian-sde-faang/` (external fork, not part of this repo's build).

Total ~565–580 numbered concept chapters, plus revision companions, interview banks, and indexes.

---

## Rework Criteria (per chapter)

Each chapter must pass all of these before it is marked done:

1. **Readability:** One concrete opening problem → one connected explanation → observable result. No generic "Why / How / Examples / Best practices" boilerplate unless that specific chapter earns it. Headings advance the topic; no riddle-only openings.
2. **Explanation depth:** Practical definition + one textbook definition + distinct First Principles derivation + worked trace + Summary + See Also + References. New topics get fuller treatment; shallow chapters are expanded, not padded.
3. **Code examples:** Every technical chapter that teaches a mechanism must run a worked example with observable output. Chapters with zero real code blocks are flagged for addition or for a non-technical justification.
4. **Grammar:** No doubled spaces, stutters, run-together sentences, smart quotes outside code/paths/protocols, or unclear pronoun references. `check_prose.py` and `prose_hygiene.py` must pass clean.
5. **Senior coverage:** Failure modes, trade-offs, version-specific boundaries, and when not to use the mechanism. `senior_coverage.py --require-complete` must pass.
6. **Current version:** No stale API signatures (caught by `check_freshness.py`). Links verified by `check_links.py`; citations in `link_baseline.json`.
7. **Startup/job relevance:** Where a topic maps to a startup role or interview topic, the chapter names it explicitly (not implied). Strategy stack owns the job-opening mapping; technical chapters reference it where relevant.

---

## Execution Order (by dependency group)

Work in groups so each re-read uses previously fixed chapters as reference:

| Phase | Group | Stacks / focus | Est. chapters |
|-------|-------|---------------|---------------|
| P1 | Foundations | `00-strategy` + `10-frontend/10.1-javascript` (execution, scope, closures, V8, prototypes) | ~40 |
| P2 | Frontend UI | `10-frontend` remaining (React, Next.js, HTML/CSS, Tailwind, mobile) | ~87 |
| P3 | Backend runtime | `20-backend/20.1-node.js`, `20.2-nestjs`, `20.3-rest-apis` | ~60 |
| P4 | Data & security | `20-backend` databases, `20.4-database`, `20.5-security` | ~40 |
| P5 | Architecture & platform | `30-architecture`, `40-platform` | ~100 |
| P6 | Quality & real-time | `50-quality`, `60-realtime` | ~50 |
| P7 | Interview & strategy | `70-interview-toolkit`, `00-strategy` remaining, `80-lanes-abroad-full-stack` | ~75 |

The V8 chapter (`10-frontend/10.1-javascript/01-execution-and-scope/10.1.1.07-v8-execution-and-optimization.md`) is a P1 foundational chapter — it gets re-read first as the model for what "readable end-to-end" looks like.

---

## Per-Chapter Work Order

For each chapter:

1. **Read end-to-end** with headings only, then prose only. Note abrupt jumps, undefined terms, orphaned examples, repetitive recaps.
2. **Rewrite the opening** around one concrete problem; keep or restore the practical + textbook definitions.
3. **Rebuild First Principles** as one derivation from cause → mechanism → result.
4. **Add or fix a worked code example** with observable output; ensure every fence is real code (not `text`/`plaintext` placeholders).
5. **Add failure boundary / trade-off section** where it changes a decision.
6. **Fix grammar:** smart quotes → straight quotes outside code, doubled spaces, stutters, run-on sentences.
7. **Update references:** current versions, live links, `link_baseline.json` for new citations.
8. **Reconcile:** category `INDEX.md`, `REVISION.md`, interview bank, cross-references.
9. **Run gates:** `bash scripts/verify.sh` (34 gates), `check_prose.py`, `prose_hygiene.py`, `senior_coverage.py --require-complete`, `check_freshness.py`, `check_links.py`.
10. **Record disposition:** modified / keep / pending in the rework tracker.

---

## Metadata & Ledger Updates

After each group completes:

- `docs/2026-10-25-fullstack-review-records.json` — review evidence per file
- `docs/review-ledger.json` — hash-pinned review evidence (991/991 target)
- `docs/2026-10-25-fullstack-coverage.json` — coverage summary
- Read times regenerated via `read_time.py`
- Counts restamped via `check_counts.py --write`

---

## Gates That Must Stay Green

All 34 gates in `scripts/verify.sh` must pass before any commit, including:

| Gate | What it checks |
|------|----------------|
| `check_counts.py` | File/line/badge counts match disk |
| `check_links.py` | 0 broken links, anchors verified |
| `check_freshness.py` | No stale API signatures |
| `check_template.py` | Section order and genre compliance |
| `check_prose.py` + `prose_hygiene.py` | Grammar, spacing, stutters |
| `senior_coverage.py --require-complete` | Review evidence for every file |
| `review_ledger.py check` | Hash-pinned read-back, 0 pending |
| `check_private_refs.py` | No references to `~/repos/personal` |

---

## How to Review This Plan

Before any rework code is written, please confirm:

1. **Execution order** — Do you want P1 (foundations + V8) first, or a different stack priority?
2. **Per-chapter criteria** — Are all seven criteria acceptable? Anything to add or remove?
3. **Startup/job content** — Where should startup role mappings live? Strategy stack only, or inline in technical chapters too?
4. **Pacing** — Should I rework one stack at a time and push after each, or batch several groups?

Once you approve the plan, I'll start Phase 1 (P1 foundations) with the V8 chapter as the first rewrite, and push each completed group with a full verify run.
