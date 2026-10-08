# Explanation Depth Implementation Plan

> **For agentic workers:** Use the approved design and execute the following tasks with checkpoints. The executing-plans workflow recommends parallel review where available. Review work uses disjoint chapter paths and separate ledger fragments; the coordinating agent owns consolidation and generated files.

**Goal:** Make every authored Markdown document understandable in its genre, repairing missing mechanisms, terminology, traces and correctness boundaries.

**Architecture:** Preserve topic homes and chapter IDs. Review entire documents, not only scan hits, using a per-file evidence ledger. Teach the basic mechanism before taxonomy and formal internals, then connect examples, failures and decisions.

**Tech Stack:** Markdown, existing Python corpus utilities, JavaScript/browser example checks, Jekyll, and primary-source documentation.

## Global Constraints

- Keep chapter IDs and canonical topic homes stable.
- Preserve the practical/formal definition pair where correct, one final Summary, separate revision, source-linked authored questions, existing role-priority semantics and private-data boundaries.
- Do not duplicate personal data, alter job-history claims, or commit/push in `career-ops`.
- A scanner pass does not set a file to reviewed.
- Optional/deferred role priority affects sequence, not review coverage.
- There is no target word count, fixed number of examples or requirement to fill every template heading.
- Teach terms before using them; explain the arrows in diagrams and the conditions behind expected code results.
- Do not run generated-file writers or change shared scripts from concurrent editorial workers.

## Task 1: Establish evidence and ownership

**Files:** Create `docs/2026-10-08-explanation-depth-review.json`; use per-worker fragments under `/tmp/bible-depth-review/`. Modify the approved design's status and this plan's checkboxes.

**Interfaces:** Inventory entries contain `path`, `genre`, `baseline_sha256`, `state`, `findings`, `disposition`, `questions` and `validation`. A review fragment is a JSON list of those entries; `state` is `reviewed` or `revised` only after reading the document. Pending entries retain `state: pending`.

- [x] Enumerate tracked and authored untracked Markdown, excluding dependencies/build output. Preserve personal/historical genres.
- [x] Capture baseline hashes and candidate section signals using `md_fences.walk` and `prose_scan.prose_words`; save signals as investigation leads.
- [x] Partition ownership: coordinator owns JavaScript execution/scope category, quality, realtime, interview toolkit, strategy, lanes, projects and meta; workers own remaining frontend, backend, architecture/platform respectively.
- [x] Verify the inventory's unique paths cover the source tree. Each worker must return a disposition per assigned file, never a blanket review status.

## Task 2: Repair the JavaScript scope reference treatment

**Files:** `10-frontend/10.1-javascript/01-execution-and-scope/*.md`; related `this` links and the JavaScript interview bank are coordinated with the frontend worker.

**Interfaces:** Consumes the design's eight comprehension criteria. Produces revised learning chapters, retained/expanded revision questions and the coordinator ledger fragment.

- [x] Read lexical environment, execution context, scope, hoisting, closures, call stack, INDEX and REVISION together; locate unsupported assumptions and cross-chapter omissions.
- [x] Verify record hierarchy, global/module boundaries and execution-context environment references against ECMAScript; distinguish model from implementation.
- [x] Develop the five record kinds in the LE chapter with a focused observable case for each meaningful difference. Keep name lookup and binding initialization connected to the existing examples.
- [x] Explain LE/VE jobs and block transitions in execution context; cover strictness and default-parameter qualifications without universal memory-bucket claims.
- [x] Execute the authored examples in an isolated JavaScript/browser environment: defining-scope lookup, independent closures, TDZ, block `var`/`let`, ordinary/arrow ownership, classic-script globals, module live imports and parameter closures.
- [x] Review each revised chapter without its code: prose must still explain what occurs. Review code with its prose: outputs must match stated setup.
- [x] Update source-linked revision questions and any contradictory interview answers. Run template, alignment and internal-link checks.

## Task 3: Review remaining frontend

**Files:** All authored Markdown under `10-frontend/`, excluding the coordinator's execution/scope category.

**Interfaces:** Produces `/tmp/bible-depth-review/frontend.json`, edited chapters/companions and a citation list; shared metadata is consolidated later.

- [ ] Read each file in learning order, including navigation/revision/drills. For every consequential named variant, check meaning, relation, trace and boundary.
- [ ] Replace catalog-only instruction with concrete explanations in the relevant canonical section. Preserve useful compact comparisons.
- [ ] Check lifecycle/identity/ownership examples across language, TypeScript, browser, React, forms, Next.js, animation and mobile material.
- [ ] Verify unstable/niche claims through primary sources. Run representative changed examples and record unexecuted integrations accurately.
- [ ] For each learning document, record one trace question and one changed-condition question. Return per-file findings, rationale and validation; do not infer completion from file length.

## Task 4: Review backend

**Files:** All authored Markdown under `20-backend/`.

**Interfaces:** Produces `/tmp/bible-depth-review/backend.json`, edited chapters/companions and new source URLs.

- [ ] Review Node, HTTP/API, PostgreSQL, security, NestJS, caching, brokers, microservices, GraphQL, AI and Java in dependency order.
- [ ] Reconcile diagrams and code against prose, prioritizing the confirmed MVCC isolation mismatch. Explain snapshots, visible row versions, concurrent writes and cleanup before low-level tuple fields.
- [ ] Make setups/runtime assumptions explicit; trace request/job/transaction ownership and failure recovery before comparing variants.
- [ ] Use actual PostgreSQL for isolation assertions if available; explicitly record a source-verified but unexecuted database test when it is unavailable. Do not substitute SQLite as MVCC proof.
- [ ] Preserve authored questions and carry changed contracts through category revision/interview material. Produce per-file dispositions and comprehension questions.

## Task 5: Review architecture and platform

**Files:** All authored Markdown under `30-architecture/` and `40-platform/`.

**Interfaces:** Produces `/tmp/bible-depth-review/architecture-platform.json`, revised source documents and citation/verification notes.

- [ ] Explain component responsibilities and interactions before taxonomy, protocols or deployment recipes.
- [ ] Trace design decisions from requirements, invariants, workload and failures; remove unsupported guarantees and contradictory diagrams.
- [ ] Teach platform behavior through inputs, controller/runtime action and observable results. Review HPA resource metrics and scheduling/readiness boundaries in particular.
- [ ] Distinguish measured integration evidence from algorithm/configuration reasoning. Verify volatile/niche behavior against primary docs.
- [ ] Update affected revision/navigation/drill passages and record per-file trace/changed-condition questions and dispositions.

## Task 6: Review quality, realtime, interview and supporting genres

**Files:** `00-strategy/`, `50-quality/`, `60-realtime/`, `70-interview-toolkit/`, `80-lanes-abroad-full-stack/`, `81-lanes-indian-sde-faang/`, `projects/`, `lanes/`, root Markdown and `docs/`.

**Interfaces:** Produces `/tmp/bible-depth-review/coordinator.json`; personal data remains in its canonical private paths.

- [ ] Review every document according to its genre: concepts teach mechanisms, cases justify decisions, drills explain answers, indexes establish prerequisites, and operational documents explain actions and evidence.
- [ ] Clarify measurement boundaries, causal reasoning, ownership, retries, races and recovery where consequential to the topic.
- [ ] Preserve historical dates/facts and personal experience; distinguish existing behavior, proposed designs and hypothetical evidence.
- [ ] Record a reason for unchanged documents, as well as specific edited passages and their checks. Do not insert textbook structure into trackers or historical notes.

## Task 7: Consolidate and validate

**Files:** Final review JSON/report, modified chapters and companions, `scripts/external-links-baseline.json`, read-time/count/search/API generated output.

**Interfaces:** Merge fragments by unique source path; pending and unresolved entries remain explicit. Verify current hashes after metadata writers without treating regeneration as a new semantic review.

- [ ] Inspect worker edits and evidence; resolve cross-owner contract changes and missing dispositions. Confirm no uncovered inventory entries remain before claiming completion.
- [x] Probe newly introduced primary URLs, then refresh the external-link baseline with the existing workflow.
- [x] Run existing writers sequentially: alignment repair, read time, master index, counts. Inspect output and run `bash scripts/verify.sh`.
- [x] Build Jekyll, confirm private exclusions, and inspect expanded chapters at mobile/desktop widths in both themes.
- [x] Run the reader, navigation and read-aloud browser suites on the final rendered output; check new diagrams/tables and code captions.
- [x] Publish an accurate report of semantic review, runtime checks and remaining limitations. Commit/push only when separately requested or already authorized for the resulting work.

## Test discipline

This work primarily edits prose. Existing meaningful checks protect structural and rendering behavior; no tests assert that particular paragraphs contain preferred phrases. If a shared utility or gate needs a behavior change, add a failing real-case test first, observe its failure, make the minimal change and rerun its tests. Do not add a universal prose-word floor as a comprehension gate.
