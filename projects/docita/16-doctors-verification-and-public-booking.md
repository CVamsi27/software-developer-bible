# 16 — Doctors, Verification & Public Booking

> The outward-facing acquisition loop: doctor credential verification against the NMC registry with a reverification cron, timezone-correct slot generation from weekly schedules, and an anonymous referral-code public booking funnel that re-uses the tenant/RLS machinery instead of inventing its own.

---

## Context

Docita sells to clinics, but its **doctors** are the regulated users — Indian law requires verified medical registration before a doctor can practice through the platform. And clinics acquire patients through a **public booking page**: a clinic shares a short referral link, a patient books without an account, and staff confirm.

Three domains share one story:

- **doctors** — profiles, verification against a provider, availability schedules, slot generation.
- **doctor-clinics** — doctors who work at multiple clinics (a multi-clinic doctor must be valid at *each* clinic they practice at).
- **public-booking** — the anonymous, referral-coded funnel that consumes doctors' schedules.

**The problems:** (1) a doctor's registration must be checked against an *external* authority and re-checked periodically — one-time checks rot; (2) slots are weekly schedules reinterpreted per calendar date in the *clinic's* timezone; (3) public booking runs in a **different trust context** — no logged-in user, so RLS's clinic-claiming middleware can't run as it does for staff; (4) abuse: bots, OTP spam, and booking on behalf of someone else's phone number.

---

## Decision 1: Doctor Verification as an External Provider + State Machine

### What We Chose

Verification runs against a configurable HTTP provider (NMC-backed), recording a **state** on the doctor: `UNVERIFIED → PENDING → VERIFIED / REJECTED / FAILED`. The flow (`verifyAndPersistDoctorVerification`) is:

1. Load the doctor; skip non-doctors.
2. No `registrationNumber`? → set `UNVERIFIED` with reason "Registration number is required" and stop.
3. Otherwise set `PENDING`, call the provider with name + registrationNumber + council + state code + license, then persist the outcome (`VERIFIED`/`REJECTED`/`FAILED`) with `verificationSource`, `verificationRef`, `verificationReason`, and the raw provider payload (`verificationData`) for audit.

```typescript
// apps/api/src/domains/doctors/application/services/doctor-verification.service.ts
if (!doctor.registrationNumber) {
  await this.repository.updateVerificationStatus(doctorId, {
    verificationStatus: DoctorVerificationStatus.UNVERIFIED,
    verificationSource: 'NMC',
    verificationReason: 'Registration number is required', ...
  });
}
```

The provider call is behind `DoctorVerificationHttpClient` (`doctors/infrastructure/external/doctor-verification-http.client.ts`) so the NMC adapter can be swapped for jurisdiction-specific council APIs.

### Why This Was Chosen

- **Verification is a workflow, not a boolean** — REJECTED (registry says invalid) and FAILED (provider unreachable) are different: FAILED should be retried; REJECTED needs a human.
- **Raw provider data is stored** — when a dispute arises, Docita can show exactly what the registry returned, not just a verdict.
- **Http-client seam** — the NMC integration is a configurable external dependency; tests stub it (`doctor-verification.service.spec.ts`).

### Trade-offs

- **The registry provider is the weak link** — if it's down, verification degrades to FAILED; the domain can't verify offline.
- **PENDING is stored optimistically before the call** — a crash between the PENDING write and the outcome write leaves a PENDING doctor; the reverification cron heals it (below).

---

## Decision 2: The Reverification Sweep (Cron, Batch, Tenant-Bypassed)

### What We Chose

A `@Cron` (`DOCTOR_REVERIFICATION` schedule, heartbeat-tracked, disabled in non-cron processes) sweeps *all* doctors with a registration number — `role IN (DOCTOR, ADMIN_DOCTOR)`, `registrationNumber NOT NULL`, batched `take: 500` — and re-verifies each. The sweep runs under `runWithTenant({ bypassed: true })` and uses `Promise.allSettled` so one provider failure doesn't kill the batch:

```typescript
// apps/api/src/domains/doctors/application/services/doctor-verification.service.ts
await runWithTenant({ bypassed: true }, async () => {
  const doctors = await this.repository.findDoctorsForReverification();
  const results = await Promise.allSettled(
    doctors.map((doctor) => this.verifyAndPersistDoctorVerification(doctor.id)),
  );
  // surface failures but don't rethrow — the cron retries the whole batch next tick
});
```

### Why This Was Chosen

- **Credentials expire in reality** — registrations lapse; a doctor verified once stays "VERIFIED" forever unless something re-checks. The sweep converts one-time verification into a periodic guarantee.
- **`Promise.allSettled` + log-don't-rethrow** keeps a single flaky provider call from failing the entire batch and losing the heartbeat.
- **`bypassed: true` tenant context is deliberate** — the sweep spans clinics (a doctor may practice at many), so it can't run inside one clinic's RLS scope.

### Trade-offs

- **Batch of 500 with no cursor** — at 10k+ doctors this becomes a thundering sweep; `take: 500` with no pagination offset means the same 500 get re-checked every run. Scale is fine today; needs a cursor or an `X days since last check` filter later.
- **Provider rate limits** — a sweep hitting an external registry with hundreds of concurrent calls needs a throttle that isn't there yet.

---

## Decision 3: Slots = Weekly Schedules × Calendar, in Clinic Timezone, With Fallbacks

### What We Chose

A doctor (or the clinic on their behalf) defines **weekly schedules**: `dayOfWeek`, `startTime`, `endTime`, `slotDuration`, per clinic. Availability for a concrete date is *generated*, never stored: resolve the date's day-of-week **in the clinic's timezone**, find active schedules, generate slot start-times, subtract already-booked appointments (via the `ISlotAppointmentLookup` port), and sort.

The fallback chain matters for clinics that never configured per-doctor schedules:

1. Per-doctor active schedules for that weekday.
2. Clinic-level weekly rows (`findClinicWeeklyForSlotGeneration`) synthesized into per-doctor slots.
3. If the clinic has *no* weekly schedule at all, `implicitClinicWeeklyRowsForSlotFallback` fabricates a standard 9–5 set so the booking page never shows a dead-empty day with no explanation.

Empty results carry a `slotListEmptyReason` for patient-facing copy ("this doctor isn't seeing patients that day" vs "no slots left").

### Why This Was Chosen

- **Timezone correctness is the crux** — a schedule row says "Tuesday 10:00" in the clinic's zone. `getDayOfWeekInClinicZone(dateStr, timezone)` decides which weekday a UTC-stored date is *for that clinic*; generating in the clinic zone and converting to UTC instants for storage/booking keeps patient-visible times honest (helpers in `slot-generation-helpers.ts`).
- **Fallbacks buy adoption** — requiring every doctor to configure schedules before public booking works would kill activation; clinic-level defaults mean the page works on day one and improves as doctors refine.
- **Appointments are looked up through a port** (`slot-appointment-lookup.port.ts`) so slot generation depends on "what's booked", not on appointments' module internals — the same dependency-direction rule as insurance claims.

### Trade-offs

- **Generation at request time** is fine for one doctor/date, but the "next 7 days for 8 doctors" calendar does 8×7 generations per view; it's cached/lightweight today but will want a materialized availability window when usage grows.
- **Implicit fallback rows are a magic default** — a clinic that genuinely closes Tuesdays but never configured anything shows Tuesday slots; the empty-reason copy mitigates but doesn't fix it.

---

## Decision 4: Public Booking = Referral Code + Tenant Wrapper + Purpose-Bound OTP

### What We Chose

Public booking pages are addressed by a **referral code** (`/public/booking/clinics/:referralCode/...`), never a clinic ID. Every handler wraps its work in `withBookingTenant`, which resolves the code to a clinic and then runs inside the *tenant context* — reusing the exact RLS machinery staff use:

```typescript
// apps/api/src/domains/public-booking/application/services/public-booking-utils.ts
export async function withBookingTenant<T>(persistence, referralCode, fn) {
  const clinic = await resolveClinicByReferralCode(persistence, referralCode);
  return await runWithTenant({ clinicId: clinic.id }, async () => fn(clinic));
}
```

Patient identity on submit uses a **two-tier gate**:

- **New phone** → DPDP notice consent + DOB required, patient created, then an appointment *request* is filed (staff confirm later — the funnel never books directly).
- **Known phone** → the submit must carry either a Bearer token or a `bookingVerificationToken` signed by `PublicBookingTokenService` (15-minute expiry, `audience: public-booking`, purpose-bound payload of clinicId+patientId+phoneNumber). The phone-check/OTP endpoints issue it after WhatsApp OTP verification (reusing the same login-OTP WhatsApp helper as the patient portal).
- **Bots** → Cloudflare Turnstile token verified server-side; enforcement is config-flag-controlled (`isTurnstileEnforced`) so the team can relax it during rollout without a deploy.

### Why This Was Chosen

- **Referral code keeps clinic IDs out of the public URL** — no enumeration surface, no need to guess tenant IDs; codes are case-normalized, uppercase, and must match an `active` clinic.
- **Reusing `runWithTenant` means public reads obey RLS** — the anonymous request still hits every query scoped to one clinic; public-booking defines a persistence port so it can never accidentally query cross-clinic.
- **"Request, not appointment" is a product decision with engineering teeth** — submit creates an `AppointmentRequest` (`appointment-request-command.service.ts`) which staff approve/reject; Docita never promises a slot the clinic didn't confirm, and slot-locking races disappear.
- **The purpose-bound short-lived token prevents phone squatting** — you can't submit a booking for someone else's phone number without first passing their OTP; the 15-min expiry and audience bound the token's blast radius.

### Trade-offs

- **The booking funnel has more moving parts** than a logged-in flow — OTP, consent, Turnstile, token — but each maps to a real abuse vector.
- **Turnstile enforcement behind a config flag** means an insecure default during rollout if the flag is mis-set; the check still runs, it's just non-blocking.
- **No real-time slot hold** — the slot shown at page load can be taken before staff confirm; the request model absorbs this honestly (staff see the request), at the cost of a less "magical" UX than a true booking.

---

## Decision 5: Multi-Clinic Doctors as First-Class (doctor-clinics)

### What We Chose

Doctors belong to a clinic *and* optionally to many clinics via a `doctor-clinics` join. Slot availability and staff validation walk both paths — e.g., `admitPatient`'s clinical-staff check accepts a user whose `doctorClinics` include the clinic; public booking's `doctorBelongsToClinic` checks direct `clinicId` *or* the join (`doctor-clinics.repository`). Verification, however, is **clinic-independent** — the registry check is per doctor, not per doctor-clinic row.

### Why This Was Chosen

- **Reality: doctors float between clinics** in Indian healthcare (morning at one hospital, evening at another). Modeling the join instead of duplicating doctor rows keeps one registration, one verification, one schedule source per doctor.
- **Verification on the doctor, practice-scope on the join** cleanly separates "is this person a verified doctor?" from "may this doctor practice at *this* clinic?".

### Trade-offs

- **Every "doctor in this clinic?" check has two shapes** (direct or joined) — the codebase handles it with `OR` clauses and helpers, but it's a recurring subtlety that must not regress into a single-clinic assumption.

---

## What Worked

- **Public booking reuses the tenant machinery** — the referral-code funnel got RLS, audit, and read-replica behavior for free by wrapping `runWithTenant` instead of building its own authz.
- **Reverification caught real lapsed registrations** — the sweep converted "verified once" into an ongoing guarantee and its heartbeat made cron failures visible.
- **The fallback slot chain meant zero-config clinics still had bookable pages** — adoption of public booking didn't wait for schedule hygiene.
- **Known-phone OTP gating stopped squatting** before it became a support issue.

## What Failed

- **Sweep batch pagination** — the reverification `take: 500` with no offset silently re-checks only the first 500 once the doctor count passes 500; a correctness bug disguised as a working cron (the whole batch runs every tick, so some doctors are never re-checked).
- **Timezone bugs in early slot generation** — the first implementation derived the weekday from the UTC date, which showed Monday schedules on Sunday evenings for IST clinics; the clinic-zone helper fixed it, and the regression tests (`public-booking-slots.service.spec.ts`, `availability-schedule`) now pin it.
- **Turnstile initially blocked legitimate elderly patients** on flaky mobile networks — the config-flag enforcement switch (relax during incidents) came directly from that support noise.

## What Could Be Better

- **Cursor or last-checked filter on reverification** and a **rate-limit/throttle** around the external provider call.
- **Availability window materialization** (next-7-days slots) for the multi-doctor calendar view when usage grows.
- **Appointment-request SLA visibility** — the funnel creates requests; clinics that confirm slowly strand patients. A "confirm within X hours or auto-nudge" policy on top of the existing WhatsApp staff notifications would close the loop.
- **Public booking page rate limiting** per IP/phone for the OTP endpoints (the patient portal has attempt-caps; public booking's OTP endpoints should inherit the same rules).

---

## Code Evidence

| Claim | File |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Verification workflow | `apps/api/src/domains/doctors/application/services/doctor-verification.service.ts` |
| External verification HTTP client | `apps/api/src/domains/doctors/infrastructure/external/doctor-verification-http.client.ts` |
| Reverification cron | `apps/api/src/domains/doctors/doctor-reverification.cron.ts` |
| Sweep batch query | `apps/api/src/domains/doctors/infrastructure/repositories/prisma-doctor-verification.repository.ts` |
| Slot generation + fallbacks | `apps/api/src/domains/doctors/application/services/slot-generation.service.ts`, `slot-generation-helpers.ts` |
| Availability schedules | `apps/api/src/domains/doctors/application/services/availability-schedule.service.ts` |
| Appointment lookup port | `apps/api/src/domains/doctors/application/ports/slot-appointment-lookup.port.ts` |
| Booking tenant wrapper + referral resolution | `apps/api/src/domains/public-booking/application/services/public-booking-utils.ts` |
| Submit funnel (OTP gate, DPDP, request) | `apps/api/src/domains/public-booking/application/services/public-booking-submit.service.ts` |
| Purpose-bound 15-min booking JWT | `apps/api/src/domains/public-booking/application/services/public-booking-token.service.ts` |
| Slots endpoint | `apps/api/src/domains/public-booking/application/services/public-booking-slots.service.ts` |
| Public routes | `apps/api/src/domains/public-booking/presentation/controllers/public-booking.controller.ts` |
| Doctor-clinics join | `apps/api/src/domains/doctor-clinics/application/services/doctor-clinics.service.ts` |
| Approval request creation | `apps/api/src/domains/appointments/application/services/appointment-request-command.service.ts` |

---

## Interview Script (60 seconds)

> "Three domains form the acquisition loop. First, doctor verification: each doctor's registration is checked against an NMC-backed HTTP provider behind a state machine — UNVERIFIED, PENDING, VERIFIED, REJECTED, FAILED — with the raw registry payload stored for audit, and a heartbeat-tracked cron re-verifies the whole cohort periodically so credentials can't rot. Second, slots: availability is generated from weekly schedules for the requested date in the clinic's timezone — the weekday is resolved in the clinic zone, booked appointments are subtracted through a lookup port, and a fallback chain means clinics with no configured schedule still show bookable days. Third, public booking: the page is addressed by referral code, every handler wraps itself in the same tenant context staff use, so RLS applies to anonymous requests. Submitting for a known phone requires a purpose-bound 15-minute JWT issued only after WhatsApp OTP; new phones need DPDP consent. Submits create an appointment *request* that staff confirm — the funnel never promises a slot it can't hold. The honest gap: my reverification sweep batches 500 doctors with no cursor, so past 500 it re-checks the same ones — it needs a last-checked filter."

---
