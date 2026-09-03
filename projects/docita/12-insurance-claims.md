# 12 — Insurance Claims

> The claims lifecycle — a state machine with an audit event per move, optimistic concurrency, and a cross-domain readiness gate that reuses billing's ICD/CPT coding instead of duplicating it.

---

## Context

Indian clinics submit **health insurance claims** to insurers and TPAs (third-party administrators) on behalf of patients. A claim in Docita:

- **Attaches to an invoice** — reimbursement claims must reference a *final* invoice (`REIMBURSEMENT` type requires `invoiceId`); cashless claims attach at consultation time.
- **Goes through a regulated lifecycle** — DRAFT → SUBMITTED → APPROVED / PARTIALLY_APPROVED / DENIED / INFO_REQUESTED / APPEALED → SETTLED / CANCELLED. Each move has financial side effects (approved amount, patient responsibility, timestamps).
- **Must be auditable** — an insurer dispute or a patient complaint requires a perfect history: who moved the claim, from what status to what, with what amount.
- **Spans two domains** — a claim cannot be submitted until the invoice's *clinical coding* (ICD-10 diagnoses, CPT procedures) is complete, but that knowledge lives in billing, not insurance-claims.

**The problems:** (1) an unbounded `PATCH` on a claim would let any status overwrite any other; (2) two staff tabs editing the same claim would silently clobber each other; (3) submission needs a gate the claims domain has no business implementing itself; (4) claims reference patients, appointments, invoices, documents, and parent claims that must all belong to the *same clinic* (RLS boundary).

---

## Decision 1: A Pure State Machine in the Domain Layer

### What We Chose

A `ClaimStatusVO` value object holds the legal transition table; a domain entity (`InsuranceClaim`) applies transitions and computes side effects (timestamps, defaulted amounts). Both are pure TypeScript — no Prisma — so the entire lifecycle is unit-testable without a database (`insurance-claim.entity.spec.ts`, `claim-status` tests).

```typescript
// apps/api/src/domains/insurance-claims/core/value-objects/claim-status.value-object.ts
private static readonly VALID_TRANSITIONS: Record<ClaimStatusEnum, ClaimStatusEnum[]> = {
  [ClaimStatusEnum.DRAFT]: [ClaimStatusEnum.SUBMITTED, ClaimStatusEnum.CANCELLED],
  [ClaimStatusEnum.SUBMITTED]: [
    ClaimStatusEnum.INFO_REQUESTED, ClaimStatusEnum.APPROVED,
    ClaimStatusEnum.PARTIALLY_APPROVED, ClaimStatusEnum.DENIED, ClaimStatusEnum.CANCELLED,
  ],
  [ClaimStatusEnum.APPROVED]: [ClaimStatusEnum.SETTLED, ClaimStatusEnum.APPEALED, ClaimStatusEnum.CANCELLED],
  ...
  [ClaimStatusEnum.SETTLED]: [],   // terminal
  [ClaimStatusEnum.CANCELLED]: [], // terminal
};

transitionTo(next: ClaimStatus): ClaimStatusVO {
  if (!this.canTransitionTo(next)) {
    throw new InvariantViolationError(`Cannot transition claim from ${this.value} to ${next}`);
  }
  return new ClaimStatusVO(next);
}
```

The entity's `transitionTo(target, { now, approvedAmountCents, ... })` returns a `ClaimTransitionResult` that **only carries the fields a given move is allowed to change** — going SUBMITTED sets `submittedAt` once; APPROVED defaults `approvedAmountCents` to the claimed amount when the insurer approves in full; DENIED records `denialReason`. The command layer then writes exactly those fields.

### Alternatives Considered

- **Prisma enum + `update` with no guard** — simplest, but nothing stops `DENIED → SETTLED` or a delete-then-recreate. For regulated money flows, correctness had to be structural, not convention.
- **A workflow library (e.g., `xstate`-style statecharts)** — heavier machinery than a single status column warrants; the transition table is small and readable as data.
- **Status stored as a string checked in services** — the same logic would scatter across every command method and drift.

### Why This Was Chosen

- **Same pattern as invoices** — file comment: "Mirrors the invoice status value object"; consistency across money domains lowers review cost.
- **Side effects computed in one place** — the "what does APPROVED mean for amounts and timestamps" logic exists once, not in four command methods.
- **Terminal states are explicit** — `isTerminal()` and empty transition arrays make "can this claim still change?" a lookup, not a chain of `if`s.

### Trade-offs

- **Enum evolution is a migration** — adding `RESUBMITTED` later means touching the table + Prisma enum + Zod schema. Acceptable for a regulated flow that changes slowly.
- **Entities are re-hydrated per call** — `InsuranceClaimsCommandService.transition` rebuilds the entity from the fetched row each request; fine at clinic scale (a handful of claims/day), wasteful at insurer scale.

---

## Decision 2: Versioned Writes + an Audit Event per Transition

### What We Chose

Every claim row carries a `version` integer. Edits and transitions go through `updateMany({ where: { id, version: expectedVersion, ...ownershipFilter }, data: { ..., version: { increment: 1 } } })` and check `result.count`. A `0` count means a concurrent writer won — the API returns `409 ConflictException` ("modified by another request"). Status *transitions* additionally write an immutable `InsuranceClaimEvent` row inside the same `$transaction`.

```typescript
// apps/api/src/domains/insurance-claims/infrastructure/repositories/prisma.insurance-claim.repository.ts
async transition(id, clinicId, expectedVersion, data, event) {
  return this.prisma.$transaction(async (tx) => {
    const result = await tx.insuranceClaim.updateMany({
      where: { id, version: expectedVersion, ...this.ownershipFilter(clinicId) },
      data: { ...data, version: { increment: 1 } },
    });
    if (result.count === 0) return null;
    await tx.insuranceClaimEvent.create({ data: { ...event, claim: { connect: { id } } } });
    ...
  });
}
```

The event carries `fromStatus`, `toStatus`, `actorUserId`, `note`, and `amountCents` — a complete claim history without reading audit middleware.

### Why This Was Chosen

- **Optimistic concurrency fits the workload** — clinics have few concurrent editors per claim; a version column is far cheaper than row locks or SELECT FOR UPDATE, and the 409 path tells the client to reload.
- **The transition + event are atomic** — no state where the status changed but the history didn't (or vice versa), which is exactly what an insurer dispute would probe.
- **Events are append-only** — history cannot be rewritten by a later edit.

### Trade-offs

- **The client owns version plumbing** — DTOs carry `version`, every command must read-modify-write. Slightly more API surface than a bare PATCH.
- **Event rows duplicate the status column** — storage is cheap; audit certainty is not.

---

## Decision 3: Cross-Domain Readiness Gate via an Application Port

### What We Chose

Insurance-claims never imports billing's internals. It defines `IClaimValidation` (`assertClaimReady(invoiceId, clinicId)`) in its own `application/ports/`, and the Nest module wires billing's `ClaimValidationService` to that token:

```typescript
// apps/api/src/domains/insurance-claims/insurance-claims.module.ts
providers: [ ..., { provide: CLAIM_VALIDATION_PORT, useExisting: ClaimValidationService } ]
```

On SUBMITTED with a linked invoice, `transition` first calls `assertClaimReady`. Billing's `ClaimValidationService` then checks the invoice's appointment and its **clinical coding completeness** — uncoded diagnoses/procedures block submission (`ClaimReadinessResult.issues`, `requiresClinicalCoding`).

### Why This Was Chosen

- **Single owner of the coding rule** — billing already gates *its own* invoice flows on ICD/CPT completeness (the same `ClaimValidationService` used by the billing claim path — see `apps/api/src/domains/billing/core/services/claim-validation.service.ts`); claims reuse it rather than re-implementing "what counts as coded."
- **Dependency direction is clean** — claims *depend on* a capability, not on billing's module graph. RLS/PHI reasoning stays in one place.
- **Testable seam** — a fake `IClaimValidation` tests claims without seeding billing data (`insurance-claims-command.service.spec.ts`).

### Trade-offs

- **A port per cross-domain edge** — more files than a direct import, but this is the project's stated discipline (AGENTS.md AJ4).
- **Readiness is checked at submit time only** — if an invoice's coding is edited *after* submission, the claim stays SUBMITTED (a deliberate "don't surprise the staff mid-submission" choice).

---

## Decision 4: Idempotency Keys and Tenancy-Scoped References

### What We Chose

`create()` accepts an optional `idempotencyKey` and first looks up `findByIdempotencyKey(key, clinicId)` — a retried POST returns the original claim instead of duplicating it. Before any create/update, a repository helper verifies every referenced entity — patient, appointment, invoice, parent claim — belongs to this patient *and* clinic; any mismatch is a 404, not a leak. `attachDocument` only attaches documents whose `patientId` matches and which aren't already claimed, again scoped by `clinicId` or the patient's clinic.

### Why This Was Chosen

- **Mobile/network retries are the norm in clinics** — double-tap submit on a slow link must not mint two claims.
- **RLS is the last line, not the first** — ownership checks in the repository give deterministic 4xx errors instead of silent empty results, and protect documents that predate per-clinic RLS scope (`OR: [{ clinicId }, { patient: { clinicId } }]`).

---

## What Worked

- **The state machine caught real bugs in review** — disallowed transitions (e.g., SETTLED → anything) fail with a domain error before touching the DB; the spec suite documents the intended lifecycle as executable truth.
- **One audit event per transition** — answering "what happened to claim X?" is a single indexed query, not log archaeology.
- **The port seam held** — insurance-claims shipped without importing a single billing service; the readiness gate was tested with a stub.

## What Failed

- **Version churn surfaced in UI integration** — staff open a claim, leave the tab open, and submit against a stale version. The first version was a hard 409 with no recovery hint; clinics saw it as "the app lost my work." The fix was reload-and-retry messaging, not weaker concurrency.
- **Parent-claim self-reference was initially possible** — `parentClaimId === id` was caught only at DB level in an early iteration; an explicit `BadRequestException` now precedes the write (`"A claim cannot be its own parent."`).

## What Could Be Better

- **No TPA/insurer sync** — the system tracks the lifecycle but does not submit electronically to any TPA API; a clinic still prints and posts. An outbound claims feed (or at least a PDF bundle per claim) is the natural next step.
- **`update()` rejects edits to non-DRAFT claims but allows changing amounts on a DRAFT** with no re-validation against the invoice — a claim inflated after the invoice's coding gate could submit more than the invoice covers. Validate `claimedAmountCents ≤ invoice total` at submit.
- **Event history has no re-hydration API** — there is no `GET /claims/:id/events` endpoint yet, so the audit trail is queryable only in the DB. Expose it for the patient-facing "claim status" story.
- **Reverify coding on re-submit after INFO_REQUESTED** — currently the gate only runs on the DRAFT→SUBMITTED edge.

---

## Code Evidence

| Claim | File |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Transition table / VO | `apps/api/src/domains/insurance-claims/core/value-objects/claim-status.value-object.ts` |
| Entity lifecycle + side effects | `apps/api/src/domains/insurance-claims/core/entities/insurance-claim.entity.ts` |
| Command service (create/update/transition) | `apps/api/src/domains/insurance-claims/application/services/insurance-claims-command.service.ts` |
| Readiness port | `apps/api/src/domains/insurance-claims/application/ports/claim-validation.port.ts` |
| Billing's implementation of the gate | `apps/api/src/domains/billing/core/services/claim-validation.service.ts` |
| Versioned + evented transition (tx) | `apps/api/src/domains/insurance-claims/infrastructure/repositories/prisma.insurance-claim.repository.ts` |
| DI wiring of the port | `apps/api/src/domains/insurance-claims/insurance-claims.module.ts` |
| HTTP surface | `apps/api/src/domains/insurance-claims/presentation/controllers/insurance-claims.controller.ts` |

---

## Interview Script (60 seconds)

> "Insurance claims are a regulated lifecycle, so I modeled the status flow as a pure state machine — a `ClaimStatusVO` holding an explicit transition table, and a domain entity that computes each move's side effects (submitted/responded/settled timestamps, approved amounts). Transitions are optimistic-concurrency writes: the row carries a version, the update is conditional, and a miss returns 409. Every transition also writes an immutable claim-event row in the same transaction, so the audit history is atomic with the state change. Submission is gated through an application port — billing owns the ICD/CPT coding completeness rule and exposes it as `assertClaimReady`, which claims depends on without importing billing internals. Everything is scoped to patient-and-clinic, and creates are idempotency-keyed so network retries can't mint duplicate claims."

---
