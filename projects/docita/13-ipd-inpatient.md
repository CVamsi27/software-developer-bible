# 13 — IPD (Inpatient)

> Ward, room, and bed management plus the admit / transfer / discharge lifecycle — a small domain where every mutation flips bed state, so all of it happens in transactions with audit events.

---

## Context

Docita started as an OPD (outpatient) clinic tool, but several clinics run **IPD** — inpatient wards. IPD introduces a resource Docita had never tracked before: **beds**. A bed is either AVAILABLE or OCCUPIED, and that state must never drift from reality:

- A patient can have **only one active admission** at a clinic at a time.
- A **transfer** frees one bed and occupies another, in a single atomic step.
- A **discharge** frees the bed and timestamps the end of the admission.
- Every step is clinically sensitive (who admitted, who discharged, which bed) — the audit trail matters more than the CRUD.

**The problems:** (1) bed transitions are multi-row operations — occupying a bed must be atomic with creating the admission; (2) stale reads (two staff admitting to the same bed) must be impossible; (3) each action needs an audit log entry tying the actor, the bed, and the patient together.

---

## Decision 1: Thin Service Facade + Transactional Repository

### What We Chose

`IpdService` is deliberately thin — it delegates straight to `IpdRepository` and then writes an audit entry. All real logic lives in the Prisma repository, and every state-changing operation is a `$transaction`.

```typescript
// apps/api/src/domains/ipd/application/services/ipd.service.ts
async admitPatient(clinicId, input, actorUserId, ipAddress?) {
  const admission = await this.repository.admitPatient(clinicId, input);
  await this.auditService.logAction({
    clinicId, userId: actorUserId,
    actionType: 'IPD_ADMISSION_CREATED',
    resourceType: 'Admission', resourceId: admission.id,
    metadata: { patientId: input.patientId, bedId: input.bedId, admittingDoctorId: input.admittingDoctorId },
  });
  return admission;
}
```

### Why This Was Chosen

- **One owner of bed-state invariants.** `admitPatient` validates in order: patient exists in this clinic → admitting clinician is clinical staff (DOCTOR / ADMIN_DOCTOR / NURSE of this clinic or a linked doctor-clinic) → bed exists in this clinic → bed is AVAILABLE → patient has no active admission. Only then does the transaction create the admission and flip the bed to OCCUPIED.
- **Audit as a post-condition, not embedded state.** The service writes a structured audit event (`IPD_ADMISSION_CREATED` / `TRANSFERRED` / `DISCHARGED`) after the domain operation succeeds, reusing the shared AuditModule (same pattern as prescriptions).
- **Clinic scoping is enforced per query** — every lookup walks `bed → room → ward → clinicId`, so a bed from another clinic can never be addressed (`findAdmissionForClinic` filters through the same chain).

### Alternatives Considered

- Business logic in the service + separate repository calls — rejected: each operation is 2–3 row writes; without a transaction a crash between "create admission" and "occupy bed" would strand a patient with an unavailable bed.
- Stored-procedure style raw SQL — rejected: Prisma transactions + entity checks are readable and testable (`ipd.service.spec.ts`, `prisma-ipd.repository.spec.ts`).

### Trade-offs

- **Service layer is a pass-through** — the facade adds little beyond audit wiring; an alternative would merge audit into the repository, but keeping it in the service makes the audit *dependency* visible at the call site.
- **Validation reads happen outside the transaction** — `admitPatient` checks bed AVAILABLE before opening the transaction (see `What Could Be Better`).

---

## Decision 2: One Active Admission Per Patient — Enforced in the Transaction

### What We Chose

Inside the admit transaction, the repository re-checks for an existing active admission (`status: ADMITTED`) for this patient in this clinic and throws `ConflictException` if one exists:

```typescript
// apps/api/src/domains/ipd/infrastructure/repositories/prisma-ipd.repository.ts
const activeAdmission = await tx.admission.findFirst({
  where: { patientId: input.patientId, status: AdmissionStatus.ADMITTED,
           bed: { room: { ward: { clinicId } } } },
});
if (activeAdmission) throw new ConflictException('Patient already has an active admission');
const admission = await tx.admission.create({ ... });
await tx.bed.update({ where: { id: input.bedId }, data: { status: BedStatus.OCCUPIED } });
```

### Why This Was Chosen

- **The check must be race-free.** Two front-desk staff admitting the same patient concurrently would both pass a pre-transaction check; the in-transaction check serializes them.
- **Unique constraint on patient would be too broad** — the same patient legitimately has past (DISCHARGED) admissions; only *active* ones conflict.

### Trade-offs

- Admission is patient-centric but bed transitions are row-level; there's no DB unique constraint enforcing one-active-admission, so the invariant depends on this query inside every write path (there's only one write path today, which is why it holds).

---

## Decision 3: Transfers and Discharges as Paired Bed Flips

### What We Chose

`transferPatient` and `dischargePatient` both run inside transactions that flip beds in pairs:

```typescript
// transfer: old bed → AVAILABLE, new bed → OCCUPIED, admission.bedId updated, note appended
await tx.bed.update({ where: { id: admission.bedId }, data: { status: BedStatus.AVAILABLE } });
await tx.bed.update({ where: { id: input.toBedId }, data: { status: BedStatus.OCCUPIED } });
// discharge: admission → DISCHARGED (+dischargedAt), bed → AVAILABLE
```

Transfer also appends a human-readable line to `admission.notes` (`Transferred to bed {n}: {reason}`) so the ward's running clinical note isn't lost when the bed changes. Discharge appends discharge summary + instructions the same way.

### Why This Was Chosen

- **Atomicity over convenience** — a transfer that frees the old bed but crashes before occupying the new one would leave the patient "in" a bed that shows AVAILABLE. Wrapping both flips in one transaction makes the pair the unit of success.
- **Appending notes preserves the timeline** — discharge summaries and transfer reasons become part of the admission's note history instead of separate disconnected rows.
- **State is derived, not duplicated** — the bed's `status` is the single source of truth; the admission row stores *which* bed, and queries filter through the ward chain to stay clinic-scoped.

### Trade-offs

- **Admission history is linear, not branched** — a patient re-admitted after discharge gets a new Admission row; the old row keeps its own bed/timestamps. Cross-admission continuity (same episode?) must be reconstructed by patientId.
- **No bed-status enum on the *room* level** — rooms are informational groupings (with `charges`); occupancy is tracked only per bed, so a "room fully occupied" query must aggregate beds.

---

## What Worked

- **Bed state never drifted in practice.** The paired-flip transactions and the admission-create + occupy in one tx meant no stuck "occupied" beds in production incidents.
- **Audit trail made IPD disputes trivial to answer** — every admit/transfer/discharge has actor, bed, and metadata, so "who moved this patient at 3am" is one query.
- **Clinical-staff check reused the doctor-clinic link** — an admitting doctor who works at two clinics is validated through `doctorClinics`, not a fragile single-clinic `clinicId` equality.

## What Failed

- **Ward list performance** — the initial `listWards` fetch nested rooms → beds via Prisma relations without pagination; a large multi-floor ward tree produced a heavy response. It was acceptable at single-clinic scale but had to be revisited as clinics added wards.
- **Admission date was client-supplied freely** — `admissionDate` could be backdated arbitrarily, which confused discharge-summary reporting. It is still permitted (clinics legitimately backfill), but it taught the team that temporal fields in clinical domains deserve explicit validation policy, not trust.

## What Could Be Better

- **Bed availability is checked outside the transaction** — `admitPatient` reads `bed.status !== AVAILABLE` *before* `$transaction` opens. Two concurrent admits to the same bed could both pass the pre-check; the in-transaction query only guards the patient, not the bed. A conditional `updateMany({ where: { id, status: AVAILABLE } })` (like inventory's stock decrement) would close the race.
- **No discharge-required fields** — a discharge doesn't require a summary; adding "mandatory summary or explicit override" would harden clinical documentation.
- **No ward/room-level capacity reporting endpoint** — the domain has the data (beds + statuses) but no aggregate "occupancy by ward" query; dashboards end up counting admissions instead.
- **Bed history** — `Bed` rows have no status-history table, so "when was bed 7 last free" is unknowable without admission events. Cheap to add, valuable for utilization analysis.

---

## Code Evidence

| Claim | File |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Thin facade + audit wiring | `apps/api/src/domains/ipd/application/services/ipd.service.ts` |
| Admit/transfer/discharge transactions | `apps/api/src/domains/ipd/infrastructure/repositories/prisma-ipd.repository.ts` |
| Repository interface | `apps/api/src/domains/ipd/core/repositories/ipd.repository.interface.ts` |
| HTTP surface (`/ipd/wards`, `/admissions`, `/transfers`, `/discharges`) | `apps/api/src/domains/ipd/presentation/controllers/ipd.controller.ts` |
| Shared audit service used by IPD | `apps/api/src/shared/modules/audit/audit/audit.service.ts` |

---

## Interview Script (60 seconds)

> "IPD adds a resource we'd never tracked — beds — with a hard invariant: a bed is either available or occupied, and that state must never drift from reality. Every mutation is multi-row — admitting creates the admission *and* occupies the bed; transferring frees one bed and occupies another; discharging closes the admission and frees the bed — so all three are Prisma transactions where the pair of writes is the unit of success. The service layer stays thin and writes a structured audit event after each action — who admitted, which bed, which patient — reusing the shared audit module. Clinic scoping is enforced by walking the bed→room→ward chain in every query. The honest gap I'd fix next: bed availability is read before the transaction opens, so two concurrent admits to the same bed could race — a conditional `updateMany` on status would close it."

---
