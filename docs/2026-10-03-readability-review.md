# Corpus readability review — 3 October 2026

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

## Remaining confirmed rewrite queue

- [React reconciliation](../10-frontend/10.3-react/01-react-internals/10.3.1.03-reconciliation.md): Rebuild around one editable-row identity trace; repeated diagrams still remain.
- [HTTP methods](../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.01-http-methods.md): Remove duplicate complete-router implementation; teach retry/idempotency once.
- [Database joins](../20-backend/20.4-database/02-querying-and-optimization/20.4.2.02-joins.md): The main-first progression and diagram are repaired in the main-branch pass; the inventory aggregate now excludes unmatched old orders and no longer subtracts sales from current stock. Advanced SQL examples remain for a later full consolidation.
- [Nest modules](../20-backend/20.2-nestjs/01-core-architecture/20.2.1.01-modules.md): Trace provider export/import before advanced variants and reduce repeated benefits.
- [Broker selection](../20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.05-message-brokers.md): Lead with retained replay versus routed work; remove competing saga/event-sourcing tutorial scope.
- [Event-driven architecture](../20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.06-event-driven-architecture.md): Trace one event and consumer retry before taxonomy; delegate CQRS and event-store implementations.
- [CAP](../30-architecture/30.2-system-design/01-theory/30.2.1.01-cap-theorem.md): Closed in the personal-site sync pass: one partitioned booking trace now derives the conflict, separates operation contracts from database labels, and explains minority refusal, acknowledgment uncertainty and recovery. The damaged diagram and repeated interview slogans were removed.
- [SLO pair](../50-quality/50.4-production-engineering/50.4.02-sli-slo-error-budgets.md): Separate measurement vocabulary from release policy; repeated taxonomy remains after unit corrections.
- [Next caching](../10-frontend/10.4-next.js/03-data-and-caching/10.4.3.03-caching.md): Version/model choice is now explicit; still needs a shorter request-first progression.
- [RHF and Zod](../10-frontend/10.5-form-handling/10.5.01-react-hook-form.md): Concrete examples repaired; repeated introductory schema/form architecture sections still need consolidation.
- [Node streams](../20-backend/20.1-node.js/02-io-and-data/20.1.2.01-streams.md): The NDJSON acronym and split-record example are now added; this targeted clarity item is closed.

## How to close a page

Read its introduction without assumed jargon knowledge. Identify the concrete problem and explain the first mechanism before showing variants. Trace one example and its failure boundary, then keep each distinct mechanism in one place. Check technical claims and examples independently of layout. Preserve authored revision questions in the separate category companion, repair incoming anchors, regenerate navigation/search metadata and run the verification gates.

This review exposes the remaining editorial work; successful gates alone do not close this queue.
