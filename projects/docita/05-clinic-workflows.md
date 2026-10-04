# 05 — Clinic Workflows: Keep Appointment, Queue and Follow-Up State Consistent

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

A clinic workflow coordinates a booked time, a patient's arrival, a consultation and any follow-up or payment work. These are related records with different lifecycles; one status field cannot represent all of them.

A typical operation is arrival → queue → consultation → prescription → payment. The difficult cases are competing check-ins, cancellation while consultation starts, concurrent bookings and local-calendar boundaries. This case follows those mechanisms rather than assuming every patient takes one uninterrupted path.

Source was inspected on **2 October 2026**. Earlier wait-time and attendance improvements and incident stories were not verified in this review.

## First Principles

Checking a record and later changing it leaves a window for another operation. A local-time label identifies a calendar position, while a timestamp identifies an instant. A follow-up recommendation can exist before any future appointment is booked.

The workflow therefore needs separate states for each kind of record, explicit time conversion, and database rules that remain enforced when requests write at the same time. UI checks and business-rule validation provide feedback, but the database must keep the required rules true when callers overlap.

## Why Appointment and Queue States Are Different

An appointment reserves clinical time; a queue token represents arrival and service progress. An appointment can exist before arrival, and a waiting patient has not necessarily begun consultation. Keep those meanings explicit when updating both records.

The current consultation-start use case permits DOCTOR or ADMIN_DOCTOR, requires that the appointment's doctor matches the caller and rejects the Front Desk plan. It accepts specified starting statuses including an already-in-progress appointment. The write repository updates the appointment and its queue token inside a transaction.

That transaction avoids committing only half of those local updates. It does not independently prevent a competing status change if the update predicate does not verify the state that was read.

## How Check-In Allocates a Queue Number

The inspected check-in command finds the clinic's appointment, returns an existing appointment token if present, resolves a clinic-day boundary, reads the latest token number and creates **`lastNumber + 1`**.

It does **not** derive the token from an appointment hash. Shortening a hash would not guarantee uniqueness either; truncation introduces collisions.

```text
staff A: reads last number 4 → intends number 5
staff B: reads last number 4 → intends number 5
```

The schema makes `appointmentId` unique, preventing separate queue rows for the same non-null appointment ID. That is a different invariant from unique display numbering. The inspected schema does not declare a clinic/day/token-number uniqueness constraint.

A safe sequential allocator needs coordination—for example, an atomic per-clinic/day counter, or a constrained insert with a defined retry protocol. A number is a display aid, not a safe identifier for authorization or mutation.

Calling and completing a queue token first verify a token under clinic scope, then update it. Define permitted state transitions and carry their relevant expected state into persistence if a competing operator could change the token.

## How Appointment Rules Constrain Status Changes

The appointment entity rejects cancellation of a completed appointment and rescheduling of a completed or cancelled appointment. Cancelling an already-cancelled entity returns without another mutation.

The scheduling service also has a transition table covering scheduled, confirmed, rescheduling, in-progress, completed, cancelled and no-show states. The consultation use case has its own accepted-status set. The old single linear diagram containing ARRIVED as a universal persisted step did not accurately represent all these paths.

An in-memory state check is useful for one operation. To retain it under concurrency, a write can condition on the expected version or allowed persisted status. The inspected repository increments `version`, but several updates match only ID and clinic; **incrementing a version is not optimistic concurrency control** unless the expected version is compared.

For example, a consultation starter can read a permitted status while another request cancels it. A later unconditional update can overwrite that intervening change. A transaction grouping appointment and token writes does not itself validate an earlier read performed outside it.

## How Scheduling Detects Overlapping Instants

The overlap helper treats appointments as half-open intervals `[start, end)`:

```typescript
function overlaps(
  startA: number, endA: number,
  startB: number, endB: number,
): boolean {
  return startA < endB && endA > startB;
}

console.log(overlaps(9 * 60, 9 * 60 + 30, 9 * 60 + 30, 10 * 60)); // false
console.log(overlaps(9 * 60, 9 * 60 + 30, 9 * 60 + 29, 10 * 60)); // true
```

The example uses minutes on one day to show the comparison. Production comparisons need complete instants. A source-extracted check of the actual helper confirmed adjacent intervals are permitted and a one-minute overlap conflicts.

The current overlap query uses the same start-before-end/end-after-start predicate with clinic, doctor and active-status filters. A declared five-minute buffer constant is not applied in this query/helper path. Do not advertise that buffer as enforced behavior. SQL can express buffered intervals and timezone-aware bounds; those needs do not require rejecting database-level checks.

### The Database Constraint Protects Concurrent Bookings

The latest inspected overlap migration defines a GiST exclusion constraint:

```sql
EXCLUDE USING gist (
  "clinicId" WITH =,
  "doctorId" WITH =,
  tstzrange("startTime", "endTime") WITH &&
)
WHERE (status IN ('SCHEDULED', 'CONFIRMED', 'IN_PROGRESS', 'RESCHEDULING'));
```

When applied, it prevents overlapping ranges for equal clinic and doctor keys within its predicate. The repository translates the named constraint violation into an appointment-overlap error. The preflight query can improve feedback; the constraint provides the concurrent write boundary.

This is source evidence, not verification of a live migration. Confirm the installed constraint, relevant statuses, null-key behavior and the desired policy for doctors working across clinics. The constraint groups by clinic as well as doctor; it does not automatically enforce a global cross-clinic rule or the unused five-minute buffer.

## How Clinic-Local Days Become UTC Bounds

Store and compare complete instants; derive clinic-local dates and business-hour boundaries with the explicit clinic timezone. A calendar day in one timezone is not necessarily the UTC day and is not always 24 hours across daylight-saving transitions.

The queue helper uses clinic-local day bounds when conversion succeeds and falls back to process-local day calculations otherwise. The slot-availability method resolves the clinic timezone and converts local period boundaries to instants. In contrast, `validateAppointmentTime` checks hours using `Date.getHours()`, which uses the process timezone. The chapter must not claim all scheduling checks are already clinic-timezone correct.

Resolve invalid configuration deliberately and test local midnight, UTC-date changes and daylight-saving gaps/repeated times for supported regions. Removing the date and comparing only times of day causes false comparisons; converting both full instants consistently is the mechanism.

## Why Follow-Up Intent Has Its Own Record

A doctor can recommend a future visit before the patient books one. A follow-up record retains the originating appointment, patient, doctor, clinic, proposed date and reason, then can link to a booked appointment.

The current service delegates create, book, complete and cancel to command/query services. Those command methods verify clinic-scoped existence before updates, but do not show a strict transition table in the inspected implementation. Treat a stronger pending → booked → completed protocol as a rule to verify or add, not an already-proven guarantee.

Reminders connect this intent to [asynchronous delivery](03-async-processing.md) and [WhatsApp integration](06-whatsapp-integration.md). Provider acceptance or a scheduled reminder is not proof of attendance improvement.

## Real-World Decisions

| Situation | Boundary to enforce | Useful verification |
| ------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------- |
| Two desks check in simultaneously | Appointment uniqueness and display-number allocation | Concurrent same/different appointment tests |
| Cancellation races with consultation start | Allowed persisted transition or expected version | Controlled interleaving of the competing writes |
| Two callers book overlapping time | Database overlap constraint and correct scope | Concurrent inserts and active-status changes |
| Doctor works in multiple clinics | Clinic-local or global scheduling policy | Cross-clinic overlap tests |
| Clinic day crosses UTC midnight or DST | Explicit local-to-instant conversion | Boundary dates in supported zones |
| Follow-up is cancelled while booking occurs | Follow-up transition and linked appointment consistency | Concurrent command tests |

## Mistakes

- Claiming hash-derived queue tokens when the source uses sequential allocation.
- Treating a version increment as a compare-and-swap check.
- Assuming a preflight overlap query replaces a database invariant.
- Advertising a declared buffer constant as an enforced rule.
- Using process-local hours for a clinic-local policy.
- Claiming measured workflow improvements without dated evidence.

## Best Practices

Start with the business invariant and identify the write that enforces it. Keep appointment, queue and follow-up meanings distinct, reconcile real-time UI state after server outcomes and make conflict errors actionable. Exercise competing operators and calendar boundaries rather than only the happy path. Present source mechanisms and actual measured outcomes separately in interviews.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Current strengths | Conditional reply transitions and the appointment exclusion constraint protect important paths. |
| Current limitations | Other preflight checks and token allocation can race; local-time assumptions and unused buffer constants can mislead readers. |
| Recommended design | Enforce overlapping-slot and token uniqueness in the database, couple related state changes transactionally, and calculate clinic calendar boundaries from explicit timezone policy. |
| Evidence needed | Concurrent bookings yield one winner, terminal visits reject stale actions, queue tokens remain unique, and timezone/DST fixtures preserve the intended clinic day. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Clinic workflows combine related state models, explicit calendar conversion and concurrent persistence rules. Current source contains a database overlap constraint and transactional consultation writes, alongside limits in token allocation, expected-state checks and timezone handling that must remain visible.

## See Also

- [Category revision](REVISION.md) — recall and concurrency scenarios.
- [Architecture](01-architecture-decisions.md) — rule and persistence responsibilities.
- [Async processing](03-async-processing.md) — durable follow-up intent and delivery.
- [Payment flows](04-payment-flows.md) — financial transitions.
- [Case-study index](INDEX.md) — learning stages.

## References

Docita source inspected on 2 October 2026:

- `apps/api/src/domains/appointments/application/services/queue-command.service.ts` and `queue-token.helpers.ts`
- `apps/api/src/domains/appointments/core/entities/appointment.entity.ts`
- `apps/api/src/domains/appointments/core/domain-services/appointment-scheduling-rules.service.ts` and `appointment-interval-overlap.ts`
- `apps/api/src/domains/appointments/application/use-cases/start-consultation.use-case.ts`
- `apps/api/src/domains/appointments/infrastructure/persistence/prisma-appointment-write.repository.ts`
- `apps/api/src/domains/appointments/application/services/follow-up-command.service.ts`
- `packages/db/prisma/schema.prisma` — `QueueToken` model.
- `packages/db/prisma/migrations/20260603000000_fix_appointment_overlap_exclusion_include_rescheduling/migration.sql`
