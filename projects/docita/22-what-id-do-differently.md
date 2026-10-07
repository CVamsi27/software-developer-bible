# 22 — Retrospective: Prioritize Invariants Before New Abstractions

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

A technical retrospective compares intended guarantees with current evidence, then selects improvements that close the most consequential gaps. It should explain the problem, proposed change, cost and verification—not invent a failure story or promise that a tool solves it automatically.

> **Textbook Definition:** A technical retrospective evaluates differences between intended behavior and observed evidence, then proposes prioritized corrective actions with explicit cost, ownership and acceptance criteria.

For Docita, the useful question is which boundary could permit an incorrect tenant operation, money movement, state transition or repeated side effect. Start there before pursuing another architectural layer or developer convenience feature.

This is an improvement framework informed by case-source review on **2 October 2026**, not a claim that the proposed changes have been implemented or that all project tests and production outcomes have been reverified.

## First Principles

Engineering time is limited, and a correct-looking local operation can fail when requests race, versions overlap or a process crashes. Prioritize an improvement when it protects a specific invariant—a rule that must remain true—and a meaningful check can demonstrate that protection.

Prioritize consequence and likelihood, then consider implementation and operational cost. More layers, events, dashboards or caching do not inherently improve correctness.

## Why Begin With Identity and Financial Boundaries?

The reviewed [tenant case](02-multi-tenancy-rls.md) distinguishes policy existence from actual transaction, flag and role enforcement. The [payment case](04-payment-flows.md) distinguishes naming two merchant tokens from resolving different credentials. These boundaries affect what data or money an operation can reach.

Before relying on their guarantees, verify the complete operation with the real database role, flags, query path and merchant identity. A source boundary checker or unit mock cannot substitute for that evidence.

## How to Turn a Gap Into a Verifiable Improvement

| Step | Output |
| ------------------------------ | ----------------------------------------------------- |
| Identify an invariant | One statement of what must remain true |
| Reconstruct a counterexample | A race, crash or rollout trace that threatens it |
| Select an enforcing boundary | Constraint, scoped transaction, claim or protocol |
| Define meaningful verification | Controlled interleaving and real integration checks |
| Plan compatible rollout | Old/new versions and existing data/work remain usable |
| Observe and recover | Signals and actions for unresolved outcomes |

For example, “one upload session has one concurrent owner” is an invariant. Two callers reading unused state before either updates it is the counterexample. An atomic claim and owner-aware completion are proposed mechanisms. Repeat the controlled race, plus failure after claim, to assess the change; a new guard decorator alone does not close it.

## Improvements to Evaluate First

### Tenant Isolation and Cross-Tenant Integration Tests

Combine policy tests with application-routing tests. Use a non-owner role without bypass privileges, enable the intended policy settings on the same transaction, seed two tenants and test both allowed and forbidden reads/writes. Include raw queries, pooled connection reuse, concurrent operations, nested transactions and workers.

pgTAP can help express database assertions, but adopting it is optional; the important part is exercising the actual enforcement boundary. The old test that merely set a clinic ID and queried a table did not establish the enable flag, role or transaction required by the current implementation. The same is true of an application test that creates data but never installs trusted tenant scope.

### Merchant Resolution and Payment Recovery

Resolve a patient payment through the clinic's authorized provider configuration and reject inappropriate fallback credentials. Validate expected merchant, amount, currency and business state. Test concurrent duplicate deliveries and equivalent event shapes.

If ingress returns success before local processing finishes, establish durable replay responsibility. Provider abstractions already exist; making them preserve ownership and semantics is more valuable than introducing another interface with generic method names.

### Claim Ownership and Effect Acknowledgments

For jobs, uploads and status changes, compare the expected persisted state or claim generation at the write boundary. Distinguish a stale timeout from proof that the original worker stopped.

For outbox delivery, define what processed means: local dispatch, durable handoff, consumer completion or final provider effect. Test failures after each boundary. A synchronous emitter result is insufficient evidence of async consumer completion; no queue design can promise success after exhausted retries without recovery.

### Event Contract Evolution

Version events whose payloads must survive changes, and give consumers explicit handling for supported versions and unsupported events. A version number is only a discriminator: producers, validation, retained-event migration, replay and mixed-version consumers still need compatible behavior.

Keep payloads minimal and tenant-aware. Do not place a full appointment or patient record into an event simply to avoid a lookup. Determine whether the consumer needs current state or the historical facts at emission time.

## Improvements That Need Measurement and Trade-Offs

### Cross-Domain Events and Read Models

Ports make a synchronous dependency explicit; events introduce dependencies on event contracts and delivery semantics. Events do not completely decouple domains. A local projection can improve independent reads but adds replication lag, repair and consistency rules.

Use a projection when the reader can tolerate its freshness and replay boundaries. An invoice may require correct current or legally retained identity data; “billing is not real-time” is not sufficient justification. Preserve synchronous queries where their consistency and operational simplicity are useful.

### Build Caching

Turborepo is already configured in the inspected monorepo. The next question is whether tasks declare complete inputs, outputs and relevant environment settings, and whether cached results remain valid. Do not propose a migration already completed or promise a tenfold speedup without measurements.

Measure cold builds, warm builds and representative shared-package changes. A cache hit proves reuse under the configured key, not that omitted inputs could not invalidate its output.

### Correlation and Privacy-Aware Observability

Trace a request through durable intent, worker attempt and provider outcome. Retain identifiers that connect those operations while distinguishing a new attempt from a new business operation. Verify what the current logger already supplies before claiming correlation is absent.

Do not indiscriminately attach patient data or secrets to every log. Redaction, sampling, retention and access control are part of the tracing decision. Correlation helps diagnose failures but does not prevent them.

### Connection-Pool Capacity

Inspect the installed Prisma version and driver-adapter configuration rather than copying an older client constructor. Calculate demand across API replicas, workers, deploy overlap and administrative clients, and leave database capacity for other work.

Measure acquisition wait, query/transaction duration and saturation before choosing a limit. Increasing pool size can overload the database; decreasing it can delay callers. Connection pooling is capacity management, not a universal performance upgrade.

### Health and Business Signals

Separate process liveness, readiness to accept work and successful business progress. Observe database failures, event-loop pressure, queue age, outbox retries and scheduler heartbeats as appropriate.

Calling every external provider from every health probe can amplify an outage or unnecessarily remove healthy application capacity. Define which dependencies justify readiness failure and which should instead produce alerts or degraded operation. The [deployment case](10-deployment-infrastructure.md) distinguishes worker machine state from successful jobs.

### Form Generation From Schemas

Shared schemas already provide inferred types; adding a field does not necessarily require maintaining an independent TypeScript interface. Automatic form generation can help repetitive forms, but validation shape does not determine accessible labels, grouping, conditional workflow, widgets or clinical meaning.

Prefer selective generation with explicit UI metadata and overrides. Verify accessibility, errors and user flow; do not replace a understandable form with a schema dump to reduce line count.

## Real-World Decisions

| Improvement | Prioritize when | Evidence before declaring success |
| ------------------------------------- | ---------------------------------------------- | ------------------------------------------------------- |
| Tenant-routing and policy enforcement | A query can escape intended scope | Allowed/denied integration matrix with real roles |
| Merchant resolution and payment state | Identity or duplicate handling is ambiguous | Test merchant evidence and concurrent/crash scenarios |
| Claim and expected-state checks | Read-then-write races exist | Controlled interleavings and recovery tests |
| Event evolution and acknowledgement | Existing work must survive version changes | Mixed-version replay and consumer failure checks |
| Health/correlation | Recovery is slow or failures hard to locate | Detectable injected failure and actionable signals |
| Pool/cache tuning | Measurements show contention or redundant work | Representative before/after performance and correctness |
| Read models/form generation | Repeated work warrants added machinery | Consistency, repair or UX evidence |

Effort and priority labels should be derived from the actual dependency and rollout work. A schema column may be easy to add while its safe migration and consumer adoption remain substantial.

## Mistakes

- Repeating zero-coupling, zero-drift, zero-leak or zero-lost-event claims as retrospective evidence.
- Treating events as a complete replacement for synchronous domain dependencies.
- Claiming a new version field prevents all migration failures.
- Proposing tools already present in the repository.
- Publishing predicted build or operational improvements as measured results.
- Equating more health checks with better availability.

## Best Practices

Take one invariant through the counterexample, proposed enforcement, test and rollout. Keep the current implementation separate from the proposed change. Recheck source and operational evidence before using a retrospective in an interview, and explain a limitation precisely instead of memorizing a polished success narrative.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Current strengths | The retrospective connects improvements to concrete source boundaries rather than invented performance claims. |
| Current limitations | A list of desirable changes still lacks proof that a particular sequence will reduce the most important risk. |
| Recommended design | Prioritize tenant and financial invariants, then required-work durability, reproducible deployment and measured user experience; give each change an owner, acceptance evidence and rollback boundary. |
| Evidence needed | Each shipped improvement closes a reproduced failure, passes a targeted regression check, and can be rolled back without violating the invariant it protects. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Prioritize concrete identity, money and concurrent-state gaps, then verify delivery and rollout boundaries. Broader abstractions and tuning are useful when measurements and operational needs justify their cost. The strongest retrospective names both what a change enforces and what it leaves unresolved.

## See Also

- [Category revision](REVISION.md) — reconstruct mechanisms after completing the cases.
- [Case-study index](INDEX.md) — the learning sequence.
- [Tenant isolation](02-multi-tenancy-rls.md), [payments](04-payment-flows.md), [workflows](05-clinic-workflows.md) and [uploads](19-documents-and-uploads.md) — reviewed invariants.
- [Architecture](01-architecture-decisions.md), [async processing](03-async-processing.md) and [deployment](10-deployment-infrastructure.md) — dependencies, acknowledgment and compatibility.

## References

Implementation evidence and source paths are retained in the linked case studies. Proposed improvements here have not been applied to the Docita application as part of this documentation review.
