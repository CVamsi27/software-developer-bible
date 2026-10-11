# Corpus readability review — 3 October 2026

> **Dated review record:** counts, test results and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-10-senior-precision-progress.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

## What was checked

The [per-page inventory](2026-10-03-readability-inventory.csv) records 754 pages: 583 teaching/case pages and 171 revision or interview-drill pages. Every listed file was read by the structural scanner, including its fence boundaries, headings and prose. This is **automated screening**, not a claim that every paragraph received a full reader review.

Scope includes the technical corpus, project cases and career learning lanes. Personal data, operational repository docs, generated site files, INDEX/README navigation and archived material are not teaching topics in this inventory. Java and the Indian SDE lane were included in screening but remain deferred for rewrite priority.

Fresh-reader review examined headings/openings across the main frontend/backend and remaining role-relevant areas, then fully read 18 selected chapters; the Docita architecture case was additionally fully read. This pass also rewrote useState and checked its related examples and incoming links. Other full bodies remain unreviewed editorially. No all-readable certification follows from this review.

## What the scan means

333 pages have one or more screening signals. A blank flags cell means no configured signal was detected, **not** that the page is clear or correct. A long worked example can be useful; a brief page can still introduce unexplained terms.

The screening measures length over 550 lines, more than 50 box-diagram lines, more than 650 prose words before the first fenced example, paragraphs over 105 words, five or more generic template headings, vague “in detail” headings, and inline revision labels. The first-example measure misses prose examples and is particularly weak for career chapters. These thresholds select candidates rather than judge teaching quality.

| Signal | Pages |
| ----------------- | ----- |
| `dense-paragraph` | 32 |
| `diagram-heavy` | 95 |
| `late-example` | 18 |
| `long-page` | 121 |
| `template-heavy` | 244 |
| `vague-heading` | 8 |

## Confirmed corrections in this pass

- **useState:** replaced repeated introductions and oversized mechanics diagrams with one click trace, snapshot/queue reasoning, state-shape decisions and distinct practical examples. Preserved initialization, object replacement, batching, identity, purity and reducer boundaries.
- **Currying/composition:** restored the missing placeholder binding and separated promise-returning I/O from the synchronous pipeline.
- **Variance:** distinguished the soundness requirement for mutable containers from TypeScript’s permitted unsound assignments.
- **Reconciliation:** the key-reset example now changes only the key while retaining component type and position.
- **React Hook Form:** the multi-step example now validates the visible step, advances, retains earlier values and submits on the final step.
- **Zod:** removed the misleading universal first-error short-circuit claim.
- **Next caching:** introduced model/configuration selection and essential terms before the taxonomy; Summary now distinguishes the traditional and Cache Components paths.
- **Capacity planning:** corrected five-versus-four headings, carried seconds through video bandwidth arithmetic, removed the second rapid-fire recap and replaced automatic-sharding rhetoric with measured workload reasoning.
- **Docker:** install build dependencies before compilation, then prune them for the copied runtime tree; assumptions are explicit.
- **Platform SLOs:** separated percentile latency from good-event targets and connected actual recording-rule names to a consistent one-hour/five-minute burn alert.
- **Quality error budgets:** the request-based calculator reports request counts rather than invented equivalent downtime; empty populations are unavailable and input bounds are explicit. The elapsed-time table is labeled as a different measurement contract.
- **Production readiness:** corrected the mapping-versus-array consumer and undefined item type; the example is explicitly illustrative and still requires parsed-input validation.
- **Docita authorization:** expanded RBAC/ABAC and explained the application-specific INTERNAL classification.

These are documentation corrections. They do not modify Docita production code or establish measured business results. Targeted Node execution checked the placeholder binding, async pipeline with mocked fetch, and request-budget empty/boundary/below/over/invalid cases. Browser behavior and full application integration of illustrative snippets were not tested by the corpus verification gates.

## Confirmed queue completed — 4 October follow-up

The ten remaining chapters were read and consolidated in the follow-up pass:

| Chapter | Reading flow and correction |
| ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Reconciliation](../10-frontend/10.3-react/01-react-internals/10.3.1.03-reconciliation.md) | One editable-row reorder trace; identity preservation/reset, fragments, render/commit and memo boundaries follow from it. |
| [HTTP methods](../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.01-http-methods.md) | Appointment retry trace; idempotency means repeated intended effect, not identical responses. Conditional writes and durable POST retry contracts are separate. |
| [Joins](../20-backend/20.4-database/02-querying-and-optimization/20.4.2.02-joins.md) | Patient fixture carries matching, preservation, counting, EXISTS and LATERAL reasoning; distinct self/product/aggregate mechanisms remain. |
| [Nest modules](../20-backend/20.2-nestjs/01-core-architecture/20.2.1.01-modules.md) | Provider ownership/import/export trace before dynamic configuration, lifetime/global visibility and lazy loading. Removed fabricated LazyModule import and false initialization/tree-shaking advice. |
| [Broker selection](../20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.05-message-brokers.md) | Retained history versus unfinished work, followed by acknowledgment/crash boundaries. RabbitMQ Streams replay and publisher confirms are explicit; unmeasured latency tables removed. |
| [Event-driven architecture](../20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.06-event-driven-architecture.md) | Invoice commit/outbox/consumer/UI trace; event identity, local transaction boundaries, ordering and replay explained before separate CQRS/event-sourcing decisions. |
| [Quality SLOs](../50-quality/50.4-production-engineering/50.4.02-sli-slo-error-budgets.md) | User measurement contract → request budget → burn alert → separately agreed release policy. Removed repeated request-to-downtime claims and corrected six-hour burn arithmetic. |
| [Next caching](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.03-caching.md) | Request-first explanation with explicit traditional/Cache Components model selection and writer freshness/invalidation boundaries. |
| [React Hook Form](../10-frontend/10.5-form-handling/10.5.01-react-hook-form.md) | Validation/awaited submission/server error trace; controlled adaptation, row identity, subscriptions and retained multistep mechanism remain distinct. |
| [Zod](../10-frontend/10.5-form-handling/10.5.02-zod.md) | Parsed-input trace before composition/refinement/conversion and trust boundaries; resolver wiring has one home in RHF. |

CAP's partitioned-booking rewrite and Node streams' NDJSON clarification were already closed in the preceding main-branch pass. Each revised category keeps its separate revision companion and existing questions, with additional source-linked practical questions. Importance metadata and chapter IDs remain stable; incoming anchors were repaired.

### Verification scope

Executed fixtures checked Nest exported-provider resolution, missing-export rejection, shared default-scope identity and dynamic token configuration; Zod parsing/conversion, extra-key policy and environment bounds; request-budget empty/boundary/overspend cases; and SQL LEFT preservation, matched counts and EXISTS in SQLite. PostgreSQL LATERAL was not executed. The new freshness regression fixture rejects a fabricated framework LazyModule import, including multiline imports, while accepting LazyModuleLoader and a user-defined local LazyModule.

Fresh-reader review of the frontend group identified a missing concrete Controller adapter; the example was restored. The independent backend reader could not run because its service usage limit was reached. Backend correctness checks above are primary-agent checks, not an independent reader certification. Illustrative UI snippets were not exercised as a browser application; production Next cache behavior depends on the installed model and host.

New official citations were HTTP-probed successfully before updating the baseline. The historical inventory remains a screening snapshot; these rewrites do not certify the unreviewed corpus. There is no remaining item in this **confirmed rewrite queue**. The broader automated candidates still require selective reader review.

## How to close a page

Read its introduction without assumed jargon knowledge. Identify the concrete problem and explain the first mechanism before showing variants. Trace one example and its failure boundary, then keep each distinct mechanism in one place. Check technical claims and examples independently of layout. Preserve authored revision questions in the separate category companion, repair incoming anchors, regenerate navigation/search metadata and run the verification gates.

This review exposes the remaining editorial work; successful gates alone do not close this queue.

## Fresh-reader follow-up — 5 October

Independent full-prose reads now cover the REST API category and the PostgreSQL/database category; a selected set of system-design theory chapters was also read fully. The exact path coverage, the one database drill that was sampled only, and the open system-design scope are recorded in [the 5 October review ledger](2026-10-05-fresh-reader-review.md). These batches corrected specific protocol, PostgreSQL, queue, CDC and capacity claims; they do not close the corpus-wide review.

A targeted follow-up also corrected the hospital case study's booking-concurrency, tenant-isolation, audit, caching, and failure-recovery examples. See the review ledger for its scope and remaining limits; this does not count as an independent full read of the case study.
