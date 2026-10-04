# 11 — Insurance Claim State, Concurrency and History

[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

An insurance claim is the application's record of a reimbursement or cashless request, its referenced patient/invoice, amounts, status and supporting documents. Local submission state does not by itself mean an insurer has received or accepted it.

The concrete engineering problem is two staff tabs editing the same claim: one approves it while another submits an older draft. The application must reject the stale write and preserve the history of the accepted transition.

## First Principles

A status enum—a fixed set of named values—lists possible states but does not constrain which state changes are allowed. A transition rule can reject a move in memory but still lose a race before the database write. A stored history row can also diverge from the status if they commit separately.

The design therefore needs three cooperating mechanisms: transition validation, a conditional write against the version read by the caller, and a transaction containing both the accepted state change and its event.

## Why Transition Rules and Version Checks Are Separate

`ClaimStatusVO` defines the current transition graph. SETTLED and CANCELLED are terminal through this value object. INFO_REQUESTED and APPEALED can return to SUBMITTED; submission is not exclusively a DRAFT edge.

| State | Allowed next states |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| DRAFT | SUBMITTED, CANCELLED |
| SUBMITTED or INFO_REQUESTED | Approval variants, DENIED, CANCELLED; INFO_REQUESTED can also return to SUBMITTED, and SUBMITTED can request information |
| APPROVED or PARTIALLY_APPROVED | SETTLED, APPEALED, CANCELLED |
| DENIED | APPEALED, CANCELLED |
| APPEALED | SUBMITTED, approval variants, DENIED, CANCELLED |
| SETTLED or CANCELLED | None through this transition method |

The entity and value object are testable without a database, but import generated database enum/types. That is narrower than a framework-independent domain package with no database dependency.

## How a Transition Computes Financial Fields

The entity validates the requested move and returns the fields to persist. SUBMITTED stamps submittedAt only when it was previously absent. Approval stamps respondedAt and computes amounts; denial requires a nonblank reason, sets approved amount to zero and assigns the claimed amount as patient responsibility. Settlement stamps settledAt.

For full approval, approved amount must equal claimed amount. Partial approval requires an amount strictly between zero and the claim, and approved amount plus patient responsibility must equal claimed amount. These are implemented application invariants, not proof of insurer settlement or all coverage rules.

The entity advances its internal status before validating some amount-specific conditions. Current commands rebuild the entity per request, which limits reuse of an invalid mutated instance. A stronger pure transition function would return a validated result without changing state before every invariant passes.

## Examples: Two Writers Against One Version

The repository performs a conditional update with claim ID, expected version and ownership scope, then increments the version. For transitions, the event insert and final read are in the same database transaction.

```text
Tab A reads version 4          Tab B reads version 4
        ↓                              ↓
Update where version=4          Update where version=4
        ↓                              ↓
One accepted write → version 5; the other matches zero rows
```

A zero count becomes a conflict response. The accepted transition creates an event with from/to status, actor, note and approved amount. If event insertion fails, the transaction rolls the state change back.

This is a concrete strength. It does not make history immutable: the schema has a normal event table and claim deletion cascades to its events. Permissions, retention and tamper-evidence policy are separate concerns. Events cover transitions, not necessarily every draft edit, document attachment or external insurer action.

The ordinary update method writes through the primary client and then reads via the repository's read client outside that transaction. When that client is a replica, lag can affect the returned representation. Return the accepted write result from a consistent primary boundary when clients rely on its new version.

## Submission Readiness Belongs to Billing

The command depends on a claim-validation port. Nest composition imports BillingModule and wires billing's ClaimValidationService to that port. This reduces command-layer coupling, but does not mean the entire claims module never imports billing internals.

Before any requested transition to SUBMITTED with a linked invoice, the command calls the readiness gate—including resubmission from INFO_REQUESTED or APPEALED. The previous claim that resubmission was not checked was incorrect.

The gate verifies clinic context through the invoice's patient. If the invoice has no appointment, it returns ready without requiring clinical coding. If there is an appointment, it requires at least one diagnosis and procedure and rejects entries missing their ICD or CPT/HCPCS identifier. An absent linked appointment is not ready.

Coding presence does not establish coding correctness, insurer compatibility, finalized invoice status, coverage or financial amount agreement. Readiness is checked before the transition transaction and does not lock the invoice's coding version; concurrent changes need a defined snapshot or revalidation policy.

## Reference Ownership, Documents and Retry Identity

Create verifies patient membership and appointment, invoice and parent-claim references against patient and clinic. Reimbursement requires an invoice ID, but the inspected shape check does not independently validate that invoice's finalized state. Draft updates reject direct self-parenting; this is not complete multi-record cycle detection.

Claim ownership permits an explicit clinicId or a legacy null clinicId with a patient belonging to the clinic. Document attachment uses a patient match, unclaimed document condition, and clinic-or-patient-clinic scope. These are deliberate compatibility paths whose consistency should be tested and eventually normalized where practical.

Create first looks up an optional idempotency key within ownership scope. The schema's key is globally unique, not a clinic/key composite. Two concurrent creates can both miss the preliminary lookup; the unique constraint prevents duplicate rows, but this create service does not catch the conflict and return the existing response. Shared middleware may add behavior and must be traced separately.

Define key scope and request fingerprint: reusing a key for different content should not silently return an unrelated claim. A unique row is a storage guarantee, while a stable retried API response is a separate contract.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Version-conditioned writes reject stale edits; accepted transitions and events commit together; reference checks and a readiness port make important rules visible. |
| Limitations | History is not structurally immutable; create retries can surface uniqueness errors; readiness can race with invoice edits; replica reads and legacy nullable ownership need care. |
| Recommended design | Normalize tenant ownership, enforce key plus request-fingerprint semantics, validate transition and referenced financial/coding snapshot consistently, and retain versioned audit evidence for all material changes. |
| External submission | Model insurer dispatch, acknowledgement and reconciliation separately from local SUBMITTED, using durable operation identity if electronic integration is added. |
| Acceptance evidence | Two stale writers produce one accepted transition/event pair; cross-patient references fail; repeated identical creates return one result; conflicting key content fails; later invoice edits cannot silently change submitted evidence. |

The recommended design is a proposal, not a shipped insurer integration or compliance claim. Add a scoped history endpoint with access controls when staff or patients need that evidence; the inspected claims controller does not expose a dedicated events route.

## Mistakes and Best Practices

- Calling a local state transition insurer approval: retain provider/insurer evidence separately.
- Calling append-only application usage immutable history: verify database permissions, deletion and retention policy.
- Calling a preliminary key lookup retry safety: inspect the unique constraint and conflict response.
- Calling any linked invoice final: verify its allowed financial state and currency/amount relationships.
- Automatically retrying a conflict with a new version: reload and let the user reconsider the changed claim instead of overwriting another decision.

Test every transition edge, amount invariant, stale version, failed event insert, tenant reference, concurrent create, document attachment and readiness change. Avoid invented staff incidents or performance comparisons with row locks; measure contention before changing concurrency strategy.

## Code Evidence

Paths are in the inspected Docita checkout, not production outcome evidence.

| Mechanism | Source path |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Transition graph | `apps/api/src/domains/insurance-claims/core/value-objects/claim-status.value-object.ts` |
| Amount and timestamp rules | `apps/api/src/domains/insurance-claims/core/entities/insurance-claim.entity.ts` |
| Create, update and submit orchestration | `apps/api/src/domains/insurance-claims/application/services/insurance-claims-command.service.ts` |
| Conditional write, event transaction and references | `apps/api/src/domains/insurance-claims/infrastructure/repositories/prisma.insurance-claim.repository.ts` |
| Readiness implementation | `apps/api/src/domains/billing/core/services/claim-validation.service.ts` |
| Composition | `apps/api/src/domains/insurance-claims/insurance-claims.module.ts` |
| Key uniqueness and event deletion | `packages/db/prisma/schema.prisma` — InsuranceClaim and InsuranceClaimEvent |

## Summary

Combine checks of allowed state changes, version checks that reject stale writes (optimistic concurrency), and events saved in the same transaction as the change. Keep local workflow state separate from insurer evidence, and check the exact ownership, retry and history guarantees instead of inferring them from class names.

## See Also

- [Category revision](REVISION.md) — claims questions and recall.
- [Billing and invoicing](08-billing-invoicing.md) — amounts and historical context.
- [Multi-tenancy and RLS](02-multi-tenancy-rls.md) — legacy ownership and database scope.
- [Async processing](03-async-processing.md) — durable external effects.
- [Case-study index](INDEX.md) — reading order.
