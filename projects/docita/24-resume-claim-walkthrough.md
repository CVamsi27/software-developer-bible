# 24 — Explain the Product Work Behind Each Docita Resume Bullet

## Definition

A resume walkthrough connects a concise application claim to a product problem, implementation path, personal contribution and observed boundary. It is preparation for a technical discussion, not a script that supplies missing experience.

Start with one clinic visit: a receptionist books an appointment, a clinician opens the record and writes a prescription, billing records the charge, and background work creates or delivers documents. Explain the user-visible behavior before naming infrastructure.

The current resume contains seven Docita bullets. The cases below map to their order. Source inspection establishes that code exists; the candidate must identify which changes they personally designed, implemented, reviewed or operated. Deployment, adoption and business outcomes require separate evidence.

## First Principles

A system crosses different trust and failure boundaries at the UI, API, database, worker and provider. One successful demonstration does not prove every boundary. A convincing explanation follows an operation through those boundaries, describes why a decision was necessary and identifies where the implementation remains limited.

## Bullet 1: Follow the Product Across the Monorepo

**Resume scope:** end-to-end healthcare workflows in a TypeScript monorepo.

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

The inspected queue's completed-job lookup does not enforce effect-level idempotency. Not every producer demonstrably shares a transaction with business state. The outbox relay's process-local emit is not awaited asynchronous-consumer completion. Recovery without claim fencing can permit repeated work. Explain these current gaps before recommending leases, conditional completion and durable handoff.

Verify a payment signature against the exact raw payload and appropriate merchant secret. Then separately establish event ownership, duplicate business effects, ordering and reconciliation. A valid signature is not proof that an event is authorized for every clinic or that a payment settled.

Demonstrate a crash after an external effect but before acknowledgment. Explain what authoritative record determines whether replay is safe. Do not call delivery exactly once without an effect-level protocol and evidence.

## Bullet 5: Explain a Dashboard With Defined Metrics

**Resume scope:** an internal operational dashboard built from PostgreSQL business records and measured API telemetry, with latency percentiles, server-error rates, sample coverage and validated contracts.

Read the [actual-record dashboard case](14-analytics-and-dashboards.md#a-dashboard-built-from-actual-records-and-retained-telemetry). Trace the INTERNAL authorization gate, shared Zod contract, repository query, exact UTC window and frontend loading/error states. Explain why appointment start time, invoice creation time, current job status and retained request observations answer different questions.

Demonstrate that no samples produces unavailable latency/error rate, a database failure produces an error state, and a valid empty activity count remains zero. Define the percentile population and its coverage before quoting a number. Health checks and persistence gaps prevent the current aggregate from establishing customer-facing API performance or availability.

The recorded production query contained 158 retained requests with partial coverage, and no appointment/invoice/job activity in its selected window. This supports explaining the measurement implementation; it does not support 25 active clinics or a performance-improvement percentage. Verify the deployed revision before describing the dashboard as live.

The [local appointment-index benchmark](../../80-lanes-abroad-full-stack/personal/resume/benchmarks/README.md) remains a separate reproducible SQL exercise. It is no longer a bullet in the current application resume.

## Bullet 6: Keep AI Assistance Inside Explicit Boundaries

**Resume scope:** intake and clinical support with output validation, quotas, timeouts, kill switches and human decisions.

Read [prescription safety](07-prescription-safety.md) and [clinical integrations](20-clinical-lab-and-medical-coding.md). Select one actual AI call path and inspect request data, authorization, provider invocation, output parsing, cancellation and fallback. Identify the particular controls implemented on that path; a helper existing elsewhere does not prove every call uses it.

Schema validation constrains shape, not clinical truth. Show how the interface keeps a person responsible for the clinical decision. Discuss prompt injection, sensitive data disclosure, hallucinations, quota enforcement, ambiguous timeouts and degraded behavior. Describe proposed evaluation and missing evidence as future work, not a completed safety certification.

## Bullet 7: Explain What a Release Check Actually Establishes

**Resume scope:** Jest, Vitest, Playwright, GitHub Actions and delivery infrastructure.

Read [deployment](10-deployment-infrastructure.md). Select one unit assertion, integration scenario and browser flow. Explain why each belongs at that layer and which dependencies are mocked or real. The previously executed focused unit run is a limited regression result, not a business-impact metric or full release certification.

Trace a compatible API/worker/frontend release and migration. Explain secret boundaries, health/readiness, smoke checks, rollback and database restore. Configuration for Fly.io, RDS or Cloudflare establishes a configured integration; actual uptime, backup recovery and performance need dated operational results.

## Rehearse One Complete Explanation

Prepare a 90-second product overview, a five-minute operation walkthrough and a deeper discussion of one failure. Use this order: user problem → your responsibility → actual implementation → trade-off → verification → current limitation → next improvement.

Build three sanitized evidence cards: tenant scope, booking/resource correctness, and external-effect recovery. Add a frontend card when the role prioritizes UI work. Record actual contributions from Git history or work artifacts, including shared ownership. Keep sensitive patient data and secrets out of interview material.

Practice changed constraints: ten times the modeled burst, two concurrent clinics, a stale browser tab, duplicate callbacks, provider success with a lost response, a worker restart and mixed-version deployment. These are exercises, not invented incidents you experienced.

## Summary

Explain Docita as a product operation crossing real boundaries. Each resume bullet should lead to an actual path, personal contribution, meaningful check and honest limitation. Technical depth comes from tracing and testing those boundaries rather than memorizing a flawless architecture story.

## See Also

- [Category revision](REVISION.md) — resume-bullet follow-ups kept outside this walkthrough.
- [Case-study index](INDEX.md) — all implementation assessments.
- [Hypothetical workload model](23-hypothetical-clinic-metrics.md) — changed-load exercises, not adoption evidence.
- [Private resume source](../../80-lanes-abroad-full-stack/personal/resume/generator/resume_content.py) — current wording.

## References

The linked cases contain source paths and inspection qualifications. Recheck the local Docita working tree before using its behavior as current evidence.

- `apps/app/src/` — current React/Vite client; inspect actual forms and query callers.
- `apps/api/src/` — API domains, security, jobs, outbox and provider adapters.
- `packages/db/prisma/schema.prisma` — persisted states and constraints.
