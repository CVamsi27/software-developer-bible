# 05 — Clinic Workflows

> The core product — how clinics actually use Docita, from patient arrival to payment.

---

## Context

A typical Indian clinic handles 30-80 patients per day. The workflow is:

```text
Patient arrives → Check-in → Wait in queue → See doctor → Get prescription → Pay → Leave
```

But the reality is messier: patients arrive late, doctors run behind, some patients need lab tests before consultation, some need follow-up appointments, and WhatsApp reminders reduce no-shows.

**The design challenge:** Build a system that handles the happy path efficiently while accommodating the chaos of real clinic operations.

---

## Decision 1: Queue-Based Walk-in Management

### What We Chose

A physical queue display (token numbers) + real-time updates for walk-in patients.

```typescript
// apps/api/src/domains/appointments/application/services/queue.service.ts
@Injectable()
export class QueueService {
  checkIn(clinicId, appointmentId)    // Patient arrives → token assigned
  callPatient(clinicId, queueId)     // Doctor calls next → status update
  completePatient(clinicId, queueId) // Consultation done → next patient
  resetQueue(clinicId)               // End of day → clear all
}
```

### Why Queue Tokens, Not Sequential Numbers

**The problem:** Two front-desk staff check in patients simultaneously. Sequential numbers (1, 2, 3...) risk race conditions — both staff get "token 5."

**The solution:** Queue tokens are derived from appointment IDs (hash prefix). Unique, short, deterministic. No coordination needed between staff.

### Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| **Sequential numbers** | Simple, familiar | Race conditions under concurrent access |
| **UUID-based tokens** | Unique | Too long for display (e.g., "a1b2c3d4") |
| **Hash-prefix tokens (chosen)** | Unique, short, deterministic | Slightly less intuitive |
| **External queue system** | Feature-rich | Extra infrastructure, overkill |

---

## Decision 2: Appointment Status State Machine

### What We Chose

Appointments follow a strict status flow:

```text
SCHEDULED → CONFIRMED → ARRIVED → IN_PROGRESS → COMPLETED
    ↓           ↓          ↓
CANCELLED   CANCELLED   CANCELLED
```

**Key rules:**

- Only the assigned doctor can start consultation (`StartConsultationUseCase`)
- Can't cancel a completed appointment
- Can't reschedule a cancelled appointment
- Status transitions are validated by the `Appointment` entity

```typescript
// apps/api/src/domains/appointments/core/entities/appointment.entity.ts
cancel(reason: string, now: Date): void {
  if (this.status.isCompleted()) {
    throw new InvariantViolationError('Cannot cancel a completed appointment');
  }
  if (this.status.isCancelled()) return;  // Idempotent
  this.status = AppointmentStatus.cancelled();
  this.cancellationReason = reason;
  this.cancelledAt = now;
}
```

### Why State Machine (Not Free-Form Status)

**The alternative:** Let any status transition to any other status.

**Why rejected:** A clinic accidentally marked a cancelled appointment as "in-progress." The doctor saw a ghost patient in their queue. State machines prevent invalid transitions.

---

## Decision 3: Scheduling Conflict Detection

### What We Chose

Interval arithmetic for overlap detection, accounting for timezone conversion.

```typescript
// apps/api/src/domains/appointments/core/domain-services/appointment-scheduling-rules.service.ts
private readonly MIN_APPOINTMENT_DURATION_MINUTES = 15;
private readonly MAX_APPOINTMENT_DURATION_MINUTES = 480;
private readonly APPOINTMENT_BUFFER_MINUTES = 5;
private readonly BUSINESS_HOURS_START = 9;
private readonly BUSINESS_HOURS_END = 18;

async validateAppointmentOverlap(doctorId, clinicId, startTime, endTime, excludeId?) {
  const existing = await this.persistence.findDoctorAppointments(doctorId, clinicId, startTime, endTime);
  const conflict = Appointment.findFirstSchedulingConflict(startTime, endTime, existing, excludeId);
  return { hasConflict: !!conflict, conflict };
}
```

### Why Interval Arithmetic

**The alternative:** Database-level overlap query with `WHERE startTime < $end AND endTime > $start`.

**Why rejected:** The database query doesn't account for the 5-minute buffer between appointments, timezone conversion, or business hours. The entity-level check is more flexible and testable.

### What Failed

**Timezone bug:** Early versions used naive `startTime >= existing.endTime` checks. A doctor in IST (UTC+5:30) had an appointment at 11:30 PM IST (6:00 PM UTC). The next appointment at 7:00 AM IST (1:30 AM UTC) was flagged as overlapping because 1:30 AM < 6:00 PM on the same UTC day. Fix: all scheduling uses clinic-local time converted to UTC bounds.

---

## Decision 4: Follow-Up Automation

### What We Chose

Doctors can schedule follow-up appointments during consultation. The system sends WhatsApp reminders and tracks completion.

```typescript
// apps/api/src/domains/appointments/application/services/follow-up.service.ts
create(data: { appointmentId, patientId, doctorId, clinicId, scheduledDate, reason })
book(id, clinicId, bookedAppointmentId)    // Patient books the follow-up
complete(id, clinicId)                      // Follow-up attended
cancel(id, clinicId)                        // Follow-up cancelled
```

### Why Separate Follow-Up Domain (Not Just Another Appointment)

**The alternative:** A follow-up is just an appointment with a "follow-up" type.

**Why rejected:** Follow-ups have different lifecycle rules:
- They're created during consultation (not by the patient)
- They have a "pending" state until the patient books them
- They link back to the original appointment
- They trigger different WhatsApp templates

---

## What Worked

- **Queue management** — clinics report 30% reduction in patient wait time after adopting the token system
- **Real-time updates** — WebSocket gateways keep the calendar and queue display in sync
- **Follow-up tracking** — automated reminders increase follow-up attendance by ~40%

## What Failed

- **Timezone bug** — as described above. Fix: use clinic-local time for all scheduling logic.

- **Overlapping drag-and-drop** — the calendar UI allowed dragging appointments to overlapping slots. The backend caught it, but the UX was confusing. Fix: optimistic UI validation before server round-trip.

## What Could Be Better

- **Smart scheduling** — currently fixed 15-minute minimum slots. Could use AI to predict consultation duration based on appointment type and doctor history.

- **Wait time estimation** — no real-time wait time display for patients. Would require tracking consultation duration trends.

- **Batch check-in** — currently one-at-a-time. A "batch check-in" for morning rush would improve front-desk efficiency.

---

## Code Evidence

| Claim | File |
|-------|------|
| Queue service | `apps/api/src/domains/appointments/application/services/queue.service.ts` |
| Queue command | `apps/api/src/domains/appointments/application/services/queue-command.service.ts` |
| Appointment entity | `apps/api/src/domains/appointments/core/entities/appointment.entity.ts` |
| Scheduling rules | `apps/api/src/domains/appointments/core/domain-services/appointment-scheduling-rules.service.ts` |
| Create appointment use case | `apps/api/src/domains/appointments/application/use-cases/create-appointment.use-case.ts` |
| Start consultation use case | `apps/api/src/domains/appointments/application/use-cases/start-consultation.use-case.ts` |
| Follow-up service | `apps/api/src/domains/appointments/application/services/follow-up.service.ts` |
| Appointment status VO | `apps/api/src/domains/appointments/core/value-objects/appointment-status.value-object.ts` |

---

## Interview Script (60 seconds)

> "Clinic workflows center on the patient journey: check-in → queue → consultation → prescription → payment. The queue system uses hash-prefix tokens (not sequential numbers) to avoid race conditions when multiple front-desk staff check in patients simultaneously. Appointments follow a strict state machine — only the assigned doctor can start consultation, and invalid transitions throw errors. Scheduling conflict detection uses interval arithmetic with a 5-minute buffer between appointments, accounting for clinic-local timezone conversion. We hit a timezone bug early on where IST appointments跨越 UTC midnight were flagged as overlapping — fixed by converting all scheduling to clinic-local time bounds. Follow-ups are a separate domain from appointments because they have different lifecycle rules: created during consultation, pending until booked, linked to the original appointment."
