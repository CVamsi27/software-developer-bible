# Explanation-depth review — progress

Status: implementation remains incomplete. This is the current review snapshot, not a claim that every document is perfect or that reading alone guarantees an interview outcome.

The [per-document ledger](2026-10-08-explanation-depth-review.json) records 279 revised and 31 reviewed dispositions, with 707 pending entries. A pending entry can have partial edits; it has not earned a complete semantic disposition. Repository-wide automated checks and metadata generation do not change that state.

## Recorded semantic coverage

| Area | Completed dispositions | Pending dispositions |
| -------------------------- | ---------------------: | -------------------: |
| 00-strategy | 6 | 0 |
| 10-frontend | 75 | 100 |
| 20-backend | 72 | 151 |
| 30-architecture | 50 | 89 |
| 40-platform | 29 | 121 |
| 50-quality | 63 | 0 |
| 60-realtime | 5 | 15 |
| 70-interview-toolkit | 7 | 43 |
| 80-lanes-abroad-full-stack | 0 | 98 |
| 81-lanes-indian-sde-faang | 0 | 25 |
| docs | 1 | 30 |
| projects | 0 | 30 |

Single root documents are also represented individually in the ledger. The [approved design](superpowers/specs/2026-10-08-explanation-depth-design.md) and [implementation plan](superpowers/plans/2026-10-08-explanation-depth.md) retain their acceptance criteria and incomplete tasks.

## What changed in this continuation

- Accessibility: rebuilt the chapters around named controls, actual state changes, manual tab selection, native dialog dismissal, form recovery, exact contrast, data-derived chart alternatives, reusable component ownership and scoped audit evidence. Preserved original interview questions and source-linked revision prompts.
- Testing and production engineering: replaced invalid or incomplete examples with bounded workload/chaos fixtures, strong test oracles, explicit readiness and error-budget contracts, and truthful interview answers.
- Backend: completed the Node and database review batches, then reconciled Nest core ownership and the request lifecycle: guards, validation, safe errors, Observable cleanup and asynchronous context isolation.
- Frontend and patterns: reviewed language/TypeScript foundation batches and pattern collaboration/lifecycle traces; the advanced TypeScript category now has compiler/runtime evidence, while remaining frontend documents retain explicit pending dispositions.
- Performance: corrected Core Web Vitals classification and reporting, made Lighthouse CI executable, and explained RUM sampling bias, update identity and delivery boundaries. Completed the remaining profiling, HTTP protocol effects, bundle/budget and interview material with actual browser/build/checker fixtures.
- Realtime: replaced WebSocket and SSE catalog code with complete bounded local fixtures, validated message/cursor rules, explicit teardown and recovery boundaries; remaining realtime material is still pending.
- Reader UI: removed header palette fading and the theme button’s layout transitions, which briefly hid its mobile hit target; a normal-motion browser regression catches the reported failure.
- Cross-references: supplied concrete reasons to revisit adjacent mechanisms; fixed spelling, a JSONB table pipe and generated metadata through existing writers.

The [saved validation record](2026-10-08-explanation-depth-validation.json) retains the executed fixture outcomes and new-citation probes.

## Executed evidence and limits

| Check | Observed result | Limit |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Accessibility fixtures | Chromium 153 checks cover disclosure, manual tabs, native dialog, form recovery, two-theme contrast and forced-color focus | No screen-reader speech or mobile assistive-technology claim |
| Component fixtures | Strict TypeScript and Vitest checks cover field identity/descriptions, Radix dismissal/return, cart fixtures/properties and response oracles | Component tests do not certify complete product journeys |
| Automated audit failure paths | Correct disclosure passes; missing page language and mismatched disclosure state fail | Selected axe rules and incomplete findings still require human review |
| Nest core fixtures | Actual loopback HTTP 201/200/400/404, invalid DTO rejection, alias identity, two scoped contexts and missing export failure | In-memory fixtures do not establish durable production behavior |
| Browser timing | Actual navigation entries, concurrent timing, rejection preservation, owned cleanup and resource observer disconnect pass | Not proof of production population performance |
| Lighthouse CI | CLI 0.15.1 / Lighthouse 12.6.1 collects three Chromium reports; normal median budget exits 0 and zero-LCP budget exits 1 | Local static page, not a remote CI deployment or field INP |
| RUM pipeline | Actual HTTP and Chromium JSON beacon/fallback tests cover latest snapshots, duplicate/out-of-order updates, invalid/oversized input and capacity | Manual metric fixtures; no real collector lifecycle, complete coverage or persistence claim |
| New citations | Newly introduced primary URLs were probed live before updating the baseline | Liveness does not validate every inference in a chapter |
| Freshness regressions | Planted defect and valid controls cover k6 metric/RFC errors, AxeBuilder context, Recharts export and Lighthouse API/audit errors | Signature checks do not replace full semantic review |

## Verification status

The repository gate suite passes all 30 checks. Jekyll builds without Liquid warnings and excludes private career paths. Reader, navigation and read-aloud browser suites pass on the rebuilt site, including the new normal-motion hit-target and immediate header-contrast regressions. Sixteen expanded chapters pass 96 phone/laptop/wide-screen checks across both themes, with paragraphs filling the article width. Read-aloud tests use controlled speech mocks and do not establish real voice quality. The user authorized a commit and push of this checkpoint; the Git publication outcome is reported separately in the chat. Whole-corpus review remains incomplete.

## Outstanding work

The review workers resumed after the earlier usage-limit interruption and delivered stable batches for this checkpoint. The remaining entries include substantial frontend, backend, architecture/platform, realtime, interview-toolkit, lanes, project and supporting material. Partial system-design theory edits in CAP, consistency and their revision remain pending until complete semantic reconciliation. Optional role priority does not exempt a document from the review.

The next review must finish the pending per-document dispositions and reconcile changed contracts with still-pending drill banks. The existing resume/personal facts remain canonical; this pass has not invented achievements or treated an example as career evidence. Historical records retain their dates and factual context.

A green build, structural gate or browser fixture supports only its stated boundary. Whole-corpus completion requires all pending semantic dispositions and material evidence gaps to be resolved under the approved plan.
