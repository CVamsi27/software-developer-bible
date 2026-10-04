# 12 — Inpatient Admissions and Bed Allocation

[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

Inpatient management connects a patient's admission to a bed and tracks admission, transfer and discharge. Two rules must remain true: one bed must not be assigned to two active admissions, and one patient must not acquire conflicting active admissions within the defined clinic policy.

The difficult case is concurrent staff activity: two requests can both read AVAILABLE before either occupies the bed.

## First Principles

A multi-row transaction makes its writes commit or roll back together. It does not automatically make earlier reads behave as though transactions ran one at a time, or reserve the fact that no row exists yet. Two transactions can both find no active admission and then create one unless a database constraint, locking rule, or suitable transaction-isolation policy with retries prevents it.

Bed status and admission assignment encode related facts. Maintaining both makes reads convenient, but requires all writers to preserve their agreement.

## Why the Repository Owns Paired Writes

The service delegates to a repository and then writes a shared audit action. The repository keeps related admission and bed writes in one Prisma transaction.

| Operation | Writes grouped in the transaction |
| --------- | ------------------------------------------------------------------------------ |
| Admit | Create admission; mark selected bed OCCUPIED |
| Transfer | Mark old bed AVAILABLE; target OCCUPIED; replace admission bed and append note |
| Discharge | Mark admission DISCHARGED with time/notes; mark its bed AVAILABLE |

Atomic grouping prevents a crash halfway through these writes from committing just one side. It is a useful existing safeguard, with concurrency and audit completion still requiring separate reasoning.

## How Admission Validation Works Today

Before opening the admission transaction, the repository loads the bed through bed → room → ward → clinic, loads a non-deleted patient in the clinic, and checks clinical staff membership. DOCTOR, ADMIN_DOCTOR or NURSE can qualify through direct clinic membership or an active doctor-clinic link.

It rejects a missing reference or a bed whose earlier status is not AVAILABLE. Inside the transaction, it looks for an ADMITTED record for the patient through the clinic's ward chain, then creates an admission and unconditionally updates the bed to OCCUPIED.

This read-inside-transaction is not a concurrency lock on the absence of an admission. The inspected schema has ordinary indexes for patient, bed, clinic/status and status, rather than active-admission uniqueness. The repository does not request serializable isolation or lock a stable patient row for this check.

The create data also omits the schema's optional clinicId; queries derive clinic through the bed's ward. That compatibility path should be explicit, especially if RLS or future constraints rely on the direct field.

## Examples: Two Requests for One Bed

```text
Request A reads bed AVAILABLE     Request B reads bed AVAILABLE
A checks its patient has no admission
                                 B checks its patient has no admission
A creates admission and sets bed OCCUPIED
                                 B creates admission and sets bed OCCUPIED
```

Both sets of writes can be individually atomic while the final allocation is invalid. Updating the same bed to OCCUPIED does not reject the second writer because its write predicate does not require AVAILABLE.

A conditional bed claim can close that boundary:

```text
Within the admission transaction:
UPDATE bed WHERE id = target AND status = AVAILABLE
Require one affected row; otherwise roll back and return conflict.
Create the admission only with the successfully claimed bed.
```

This is recommended pseudocode, not the current implementation. It protects bed capacity; a separate patient/clinic active-admission constraint or serialization policy is needed when the same patient targets two different beds.

## Transfers and Discharges Also Need Current Ownership

Transfer and discharge load the admission before their transactions. They check that the earlier status is ADMITTED. Transfer also checks the target bed's earlier availability and rejects transfer to the same bed.

The subsequent writes use IDs without an expected admission version/status/bed predicate. Concurrent transfer, discharge or another bed claim can therefore invalidate the earlier decision. A stale discharge can free a bed that no longer represents that admission's current allocation; simply adding a transaction around the writes does not establish current ownership.

Transfers append a human-readable note using the earlier notes snapshot. Concurrent appends can overwrite each other. Discharge summary and instructions are optional and append in the same way. A stronger history model stores individual allocation and clinical-document events rather than treating a mutable note string as a complete timeline.

A later admission creates another row; patient continuity across admissions is a separate episode/history policy. Room occupancy must be computed from bed/allocation state, because room grouping and charges are not an independent bed-availability authority.

## Audit and Time Boundaries

The service awaits audit logging after the repository operation commits. That keeps audit dependencies visible, but does not make audit and allocation one transaction. An audit failure may occur after successful allocation; trace the audit service's own handling before promising a successful response or eventual history completion.

Admission and discharge dates can come from caller input. Define backfill permission, valid date parsing, admission ≤ discharge, timezone display and immutable event time separately. Legitimate historical entry does not require unrestricted date acceptance.

The inspected ward listing returns nested rooms and beds without pagination, and admission listing is also unpaginated. This can become a response-size and query-cost issue; it is not evidence of a measured production slowdown.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Tenant-qualified reference queries and transactional paired writes protect clear ownership and partial-commit boundaries. |
| Limitations | Availability prechecks, absent-row admission checks and stale transfer/discharge snapshots can race; mutable notes and post-commit audit leave history gaps. |
| Recommended design | Store canonical tenant ownership; enforce one active bed allocation and patient admission with database constraints; claim availability conditionally and serialize allocation changes against current admission ownership. |
| History | Record allocation transitions and required audit work transactionally; retain original notes/documents with correction semantics rather than overwriting a single string. |
| Acceptance evidence | Concurrent claims for one bed produce one winner; one patient cannot acquire two active admissions; transfer/discharge races preserve allocation consistency; audit failure remains recoverable. |

The recommended design is a proposal. Define uniqueness over active records, not every historical admission: patients and beds legitimately recur after discharge. Lock resources in a consistent order and use bounded retry for actual serialization/deadlock failures.

## Mistakes and Best Practices

- Calling an in-transaction absence check race-free: identify the constraint or stable row being locked.
- Calling bed state derived: it is stored separately from admission state and can drift.
- Calling a post-commit audit event atomic with allocation: record required work in the same commit boundary.
- Claiming no stuck beds or perfect dispute history from source: prove invariants with concurrency tests and operational reconciliation.

Add reconciliation that compares active allocations to bed states, reports conflicts and requires a deliberate repair policy. Do not silently free a bed merely because one read model temporarily lacks an admission.

## Code Evidence

Paths are from the inspected Docita checkout, not live database or production outcomes.

| Mechanism | Source path |
| ------------------------------------- | ------------------------------------------------------------------------------- |
| Facade and post-operation audit | `apps/api/src/domains/ipd/application/services/ipd.service.ts` |
| Validation and transaction boundaries | `apps/api/src/domains/ipd/infrastructure/repositories/prisma-ipd.repository.ts` |
| Admission fields and indexes | `packages/db/prisma/schema.prisma` — Admission |

## Summary

Transactional paired writes prevent partial commits, while conditional claims and database invariants prevent concurrent over-allocation. Protect transfer and discharge against stale ownership, and keep required history recoverable alongside the allocation change.

## See Also

- [Category revision](REVISION.md) — bed-allocation and transaction questions.
- [Inventory](13-inventory.md) — guarded resource decrement.
- [Clinic workflows](05-clinic-workflows.md) — database-backed scheduling invariants.
- [Async processing](03-async-processing.md) — required post-commit work.
- [Case-study index](INDEX.md) — reading order.
