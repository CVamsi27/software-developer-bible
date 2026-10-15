# 24 — Explain the Product Work Behind Each Docita Resume Bullet

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



## Definition

A resume walkthrough connects a concise application claim to a product problem, implementation path, personal contribution and observed boundary. It is preparation for a technical discussion, not a script that supplies missing experience.

> **Textbook Definition:** A claim-evidence crosswalk maps each professional claim to its implementation, personal contribution, verification artifacts and scope limitations, making the wording independently assessable.

Start with one clinic visit: a receptionist books an appointment, a clinician opens the record and writes a prescription, billing records the charge, and background work creates or delivers documents. Explain the user-visible behavior before naming infrastructure.

The cases below cover the Docita resume's product, frontend, persistence, reliability and delivery themes. Source inspection establishes that code exists; the candidate must identify which changes they personally designed, implemented, reviewed or operated. Deployment, adoption and business outcomes require separate evidence.

A scoped **15 October 2026** refresh inspected clean Docita HEAD `4e3032c2d0fd9d2ee74e7c74536fefef454d5a65` and ran 104 focused local tests across the frontend, tenant boundaries, appointment writes, invoice settlement, queue and outbox. It updates the claim-fencing discussion below; the linked cases retain their own inspection dates and limits. These tests establish neither personal ownership nor production readiness. Record an own-contribution map before strengthening any application claim: change or work artifact, your action, shared responsibility, check, observed result and remaining limit.

## First Principles

A system crosses different trust and failure boundaries at the UI, API, database, worker and provider. One successful demonstration does not prove every boundary. A convincing explanation follows an operation through those boundaries, describes why a decision was necessary and identifies where the implementation remains limited.

## Bullet 1: Connect Five Workflows to One Clinic Visit

**Resume scope:** end-to-end ownership across five named healthcare workflows in a TypeScript monorepo. Five is a grouping of product responsibilities, not a customer count, release count or adoption metric.

Use this map to explain what the product does before drawing its architecture:

| Workflow | User action | State that must be correct | Case to study |
| --------------- | --------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------ |
| Scheduling | Receptionist books or changes a visit | Clinic, clinician, time and appointment status | [Clinic workflows](05-clinic-workflows.md) |
| Patient records | Clinician opens the relevant patient's record | Patient identity, clinic access and sensitive fields | [Tenant isolation](02-multi-tenancy-rls.md) |
| Prescriptions | Clinician records and reviews treatment | Patient/visit association, medication data and document revision | [Prescription safety](07-prescription-safety.md) |
| Billing | Staff records charges and settlement | Amounts, invoice lifecycle and duplicate payment effects | [Billing](08-billing-invoicing.md) |
| Inventory | Staff records stock movement | Item, unit, quantity and authoritative stock movement | [Inventory](13-inventory.md) |

Start with scheduling → record → prescription → billing. Inventory is a related stock workflow; it is not automatically a step in every visit. Explain the actual integration before claiming a prescription always decrements stock.

Read [architecture](01-architecture-decisions.md), [clinic workflows](05-clinic-workflows.md), [prescriptions](07-prescription-safety.md), [billing](08-billing-invoicing.md) and [inventory](13-inventory.md). Draw the current API, worker, clinician app, internal app and landing site. Separate deployable applications from shared packages and from independently operated microservices.

Trace appointment input, trusted clinic identity, availability rules, persistence, UI update and any downstream work. Explain why a shared contract helps coordinated changes, then why old and new application versions may still overlap. A pre-save overlap query alone does not prevent concurrent bookings; identify the actual persistence invariant before describing it as guaranteed.

Bring one actual change: initial problem, files touched, acceptance behavior, review or deployment artifact and your contribution. Do not adopt the hypothetical 25-clinic scenario as a production account.

## Bullet 2: Trace a Form and Its Server State

**Resume scope:** React/Vite, TanStack Query, React Hook Form and Zod contracts.

Explain local form state separately from cached server state. Follow input parsing, field errors, mutation submission, server authorization, success/error handling and cache updates. A shared inferred TypeScript type helps development but does not replace runtime parsing or permissions.

Demonstrate one real form with an invalid value, server rejection, slow response and a repeated submit. Discuss stale cached results, query-key tenant scope, cancellation, optimistic updates and rollback. Identify what the current form actually does rather than claiming every listed improvement exists.

Rehearsal: implement a small appointment editor with explicit pending/error states, keyboard navigation and safe cache invalidation in a synthetic exercise. Label the exercise separately from current application behavior. Read the [React learning stages](../../10-frontend/10.3-react/INDEX.md) for hooks and rendering, then inspect the actual app source.

## Bullet 3: Connect Identity to the Database Operation

**Resume scope:** NestJS/Prisma/PostgreSQL, scoped authorization, ABAC, RLS policies, migrations, transactions, encryption and audit logging.

Read [tenant isolation](02-multi-tenancy-rls.md). Explain authentication, clinic membership, action/resource authorization and database scope as separate steps. Show why the relevant query must run with the intended settings and privileges on the correct transaction.

The inspected RLS enable condition is staged; policies existing in migrations do not prove universal production enforcement. Transaction routing, role privileges and fallback paths matter. Likewise, audit logging is not automatically immutable storage, and field encryption does not protect every metadata or logging path.

For one query, show its filters and join scope, pagination ordering, index rationale and execution plan when available. For one migration, explain compatibility, backfill, constraints and rollback limits. Use two synthetic tenants and real database roles for isolation evidence; unit mocks alone are insufficient.

## Bullet 4: Separate Durable Intent From External Completion

**Resume scope:** PostgreSQL jobs, outbox, retries, dead letters, payment webhooks and document work.

Read [async processing](03-async-processing.md), [payments](04-payment-flows.md), [WhatsApp](06-whatsapp-integration.md) and [uploads](19-documents-and-uploads.md). Trace a business write, durable intent, claim, effect and acknowledgment.

The queue's completed-job lookup does not enforce effect-level idempotency, and not every producer demonstrably shares a transaction with business state. The **15 October** source does implement claim fencing: each claimed job receives a fresh `claimToken`; completion, retry, dead-letter and duplicate-skip acknowledgments require the matching token and `ACTIVE` status. Stale recovery clears the old token, so a late worker cannot overwrite its replacement's local job state. The focused mock-based regressions passed for these acknowledgment paths. This does not cancel an old handler or prevent repeated provider effects; verify the actual SQL with competing database connections before treating that exercise as completed evidence.

The outbox relay awaits `emitAsync` under a 30-second timeout and now refuses to acknowledge an event with no registered listener. That guards an empty consumer set, but does not establish that every required consumer is present or propagates failure. A keyed outbox append uses conflict-safe `createMany` with `skipDuplicates`, rather than catching `P2002` inside the transaction. Returned listener promises, real Nest error propagation, producer transaction boundaries and effect-level idempotency still require path-specific checks. Timed-out listeners keep running, delivery remains at least once, some appointment events retain allowed direct emits, and automatic dead-letter replay is not wired; manual replay remains the recovery path. Explain those current limits before proposing renewable leases or stronger durable handoff.

Verify a payment signature against the exact raw payload and appropriate merchant secret. Then separately establish event ownership, duplicate business effects, ordering and reconciliation. A valid signature is not proof that an event is authorized for every clinic or that a payment settled.

Demonstrate a crash after an external effect but before acknowledgment. Explain what authoritative record determines whether replay is safe. Do not call delivery exactly once without an effect-level protocol and evidence.

## Bullet 5: Explain a Dashboard With Defined Metrics

**Resume scope:** an internal operational dashboard built from PostgreSQL business records and measured API telemetry, with latency percentiles, server-error rates, sample coverage and validated contracts.

Read the [actual-record dashboard case](14-analytics-and-dashboards.md#a-dashboard-built-from-actual-records-and-retained-telemetry). Trace the INTERNAL authorization gate, shared Zod contract, repository query, exact UTC window and frontend loading/error states. Explain why appointment start time, invoice creation time, current job status and retained request observations answer different questions.

Demonstrate that no samples produces unavailable latency/error rate, a database failure produces an error state, and a valid empty activity count remains zero. Define the percentile population and its coverage before quoting a number. Health checks and persistence gaps prevent the current aggregate from establishing customer-facing API performance or availability.

The recorded production query contained 158 retained requests with partial coverage, and no appointment/invoice/job activity in its selected window. This supports explaining the measurement implementation; it does not support 25 active clinics or a performance-improvement percentage. Verify the deployed revision before describing the dashboard as live.

The [local appointment-index benchmark](../../80-lanes-abroad-full-stack/personal/resume/benchmarks/README.md) remains a separate reproducible SQL exercise. It is separate technical practice evidence and is omitted from the application resume.

## Bullet 5 Continued: Explain What a Release Check Actually Establishes

**Resume scope:** Jest, Vitest, Playwright, GitHub Actions and delivery infrastructure.

Read [deployment](10-deployment-infrastructure.md). Select one unit assertion, integration scenario and browser flow. Explain why each belongs at that layer and which dependencies are mocked or real. The previously executed focused unit run is a limited regression result, not a business-impact metric or full release certification.

Trace a compatible API/worker/frontend release and migration. Explain secret boundaries, health/readiness, smoke checks, rollback and database restore. Configuration for Fly.io, RDS or Cloudflare establishes a configured integration; actual uptime, backup recovery and performance need dated operational results.

## Optional AI Interview Story: Keep Assistance Inside Explicit Boundaries

**Optional story scope:** intake and clinical support with output validation, quotas, timeouts, kill switches and human decisions. This is omitted from the general application résumé; use it for relevant roles.

Read [prescription safety](07-prescription-safety.md) and [clinical integrations](20-clinical-lab-and-medical-coding.md). Select one actual AI call path and inspect request data, authorization, provider invocation, output parsing, cancellation and fallback. Identify the particular controls implemented on that path; a helper existing elsewhere does not prove every call uses it.

Schema validation constrains shape, not clinical truth. Show how the interface keeps a person responsible for the clinical decision. Discuss prompt injection, sensitive data disclosure, hallucinations, quota enforcement, ambiguous timeouts and degraded behavior. Describe proposed evaluation and missing evidence as future work, not a completed safety certification.


## Rehearse One Complete Explanation

Prepare a 90-second product overview, a five-minute operation walkthrough and a deeper discussion of one failure. Use this order: user problem → your responsibility → actual implementation → trade-off → verification → current limitation → next improvement.

### A Five-Minute Appointment Walkthrough

**First minute — the operation.** A receptionist selects a patient, clinician and slot. Identify the exact form and the acceptance behavior you worked on. Explain which parts you owned and which came from existing shared infrastructure.

**Second minute — the request.** Trace form parsing, mutation submission and trusted clinic identity. The browser can suggest a clinic ID, but the server must derive or validate authorized scope. A pending button improves interaction; server-side correctness must survive two requests anyway.

**Third minute — the write.** Locate the availability rule and persistence operation. Describe what happens if two requests inspect the same free slot. A transaction provides an atomic group of writes; preventing a scheduling collision also requires the correct lock, constraint or conditional update. Name the mechanism found in this path and any unresolved gap.

**Fourth minute — the response and failure.** Trace the response contract and query invalidation. If the write succeeds but the response is lost, the UI cannot infer failure from a timeout alone. Explain the current reconciliation or duplicate-submission behavior before proposing an idempotency key. Keep a provider notification failure separate from whether the appointment itself was saved.

**Fifth minute — the evidence and decision.** Show one check of a meaningful invariant, then one trade-off: strict conflict prevention versus booking flexibility, immediate notification versus durable background work, or optimistic display versus confirmed state. End with the strongest observed result you can support and one improvement with an acceptance criterion.

For each story, keep a compact evidence card: **operation, your action, inspected revision, decision, check, observed result, limitation**. If a result is only a local test, say so once and then explain what the test establishes. The story should remain understandable without reciting every framework in the resume.

Build three sanitized evidence cards: tenant scope, booking/resource correctness, and external-effect recovery. Add a frontend card when the role prioritizes UI work. Record actual contributions from Git history or work artifacts, including shared ownership. Keep sensitive patient data and secrets out of interview material.

Practice changed constraints: ten times the modeled burst, two concurrent clinics, a stale browser tab, duplicate callbacks, provider success with a lost response, a worker restart and mixed-version deployment. These are exercises, not invented incidents you experienced.

## Summary

Explain Docita as a product operation crossing real boundaries. Each resume bullet should lead to an actual path, personal contribution, meaningful check and honest limitation. Technical depth comes from tracing and testing those boundaries rather than memorizing a flawless architecture story.

## See Also

- [Category revision](REVISION.md) — resume-bullet follow-ups kept outside this walkthrough.
- [Case-study index](INDEX.md) — all implementation assessments.
- [Hypothetical workload model](23-hypothetical-clinic-metrics.md) — changed-load exercises, not adoption evidence.
- [Private resume source](../../80-lanes-abroad-full-stack/personal/resume/generator/resume_content.py) — current wording.
- [Private hiring-evidence report](../../80-lanes-abroad-full-stack/personal/reports/2026-10-15-docita-hiring-evidence.md) — exact source pointers, focused test commands and a bounded proof sprint.

## References

The linked cases contain source paths and inspection qualifications. Recheck the local Docita working tree before using its behavior as current evidence.

- `apps/app/src/` — current React/Vite client; inspect actual forms and query callers.
- `apps/api/src/` — API domains, security, jobs, outbox and provider adapters.
- `apps/api/src/shared/modules/queue/queue-job-lifecycle.ts` and `apps/api/src/shared/modules/queue/infrastructure/prisma-queue-job.repository.ts` — token-fenced acknowledgments rechecked on 15 October.
- `packages/db/prisma/schema.prisma` — persisted states and constraints.
