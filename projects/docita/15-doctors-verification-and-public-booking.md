# 15 — Doctor Verification, Availability and Public Requests

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

Doctor verification records the outcome of a credential check. Availability generation turns weekly schedules into candidate slots. Public booking accepts a patient request in a clinic context. These capabilities cooperate, but none proves the others are complete.

A patient may see a candidate time while verification is pending or while another request is being confirmed. The product must state what is actually promised.

## First Principles

External credential checks can fail, return an uncertain result or become stale. A stored VERIFIED status therefore needs source, checked-at time and a policy for freshness; it is not a timeless guarantee.

Weekly hours represent clinic-local calendar time, while appointments use instants. Generation must translate between them and exclude conflicting appointments and time off. A displayed slot is still a read result, not a reservation.

Anonymous requests need tenant resolution and bounded identity proof before they can read or change patient data. An obscure referral code identifies a clinic; it is not patient authentication.

## Why Three Domains Share the Workflow

| Domain | Responsibility |
| -------------- | ---------------------------------------------------------------------- |
| Doctors | Profile, verification, schedules and availability generation |
| Doctor-clinics | Association and practice scope across clinics |
| Public booking | Clinic resolution, patient verification and appointment-request intake |

Verification is associated with a doctor identity, while practice permissions and schedules need clinic scope. A join avoids copying the doctor's identity for each clinic, but every relevant query must support that association consistently.

## How Credential Verification Works Today

The service skips missing/non-doctor users. Without a registration number it records UNVERIFIED. Otherwise it writes PENDING, checks recorded license expiry, then tries configured HPR lookup, a configured HTTP provider, or manual administration.

A past recorded expiry produces REJECTED with LICENSE_CHECK source. HPR configuration is optional; lookup failure or no match falls through. If no general provider URL exists, the service remains PENDING with MANUAL_ADMIN source. It does not always call a live NMC registry.

A successful provider payload can set VERIFIED and retain reference/data. Non-success responses produce FAILED or REJECTED according to the mapped result. These are implemented source mappings; they do not independently establish the authority, completeness or current legal sufficiency of a configured provider.

The HTTP dependency is behind a client seam. Retained payloads support later explanation but also need access, minimization and retention policies. The PENDING write precedes the external call, and no attempt/version predicate protects a later result from overwriting a newer verification request or edited registration fields.

## Reverification Is a Bounded Scan, Not Complete Freshness

The sweep uses a bypassed tenant context and settled promises so one rejected call does not stop others. The repository selects doctor roles with non-null registration numbers and takes up to 500, with no due-time filter, cursor or explicit ordering.

Above that bound, it can repeatedly cover an incomplete cohort; even below it, unbounded provider fan-out can overload the dependency. A configured cron/heartbeat does not establish that all credentials are fresh or that PENDING records will heal.

A stronger queue selects due records with pagination, bounded concurrency, backoff and persisted attempt identity. Measure oldest unchecked age and coverage, not just whether a scheduled method ran. Keep provider unavailability distinct from a negative credential verdict.

## How Weekly Hours Become Candidate Slots

The slot service resolves clinic timezone, normalizes the requested calendar date, derives weekday in that zone, and loads active doctor schedules. It creates the clinic-day interval from local midnight to next local midnight, then loads overlapping time off and appointments through a lookup port.

The fallback chain is doctor schedule → clinic weekly schedule → implicit clinic hours when no weekly schedule exists. The fallback's doctor lookup uses direct user.clinicId membership, so a joined-only doctor may not receive the same fallback behavior. Do not claim all multi-clinic paths behave identically.

Full-day time off can suppress a schedule. Otherwise the helper generates slots and filters conflicts; results carry empty reasons such as NO_WEEKLY_HOURS, DATE_PARSE_ERROR, FULL_DAY_BLOCKED and NO_SLOTS_IN_RANGE.

Implicit opening hours are a product assumption. They can show availability on a day the clinic never intended to open. Prefer explicit approved defaults or an unavailable explanation rather than interpreting missing configuration as confirmed capacity.

## Examples: Anonymous Intake Is a Request

```text
Referral code → active clinic → tenant context
                                     ↓
                    existing phone or new phone
                                     ↓
          verify booking token or collect registration/notice
                                     ↓
                    validate selected candidate slot
                                     ↓
                     create AppointmentRequest
                                     ↓
                        staff approval/booking
```

Clinic resolution normalizes the code and returns clinic information, including its ID. The code therefore does not eliminate enumeration or make clinic IDs secret. `withBookingTenant` scopes the callback; downstream tenant propagation and actual database roles/policies still need verification.

Submit parses a shared schema and verifies Turnstile. A configuration flag determines whether an unsuccessful check blocks submission. Configuration and incident fallback policy are part of the effective abuse protection.

For an existing phone, the service requires a bearer or booking-verification token, then checks clinic ID, patient ID and normalized phone against the resolved record. The token service verifies signature, audience, purpose and a 15-minute expiry.

For a new phone, the service requires date of birth and current-version accepted notice, creates a patient, and records consent. This branch does not require the same existing-patient token. Consent records are implementation evidence, not proof of all legal requirements or ownership of a newly supplied phone.

When a slot is supplied, both endpoints, valid order and doctor ID are required, and the public slot service revalidates it before intake. That check is still not an atomic hold or final appointment creation.

Existing-patient intake updates submitted name/email/phone fields after token validation. New patient creation, consent recording and request creation are separate service calls in this orchestration. Partial failure and duplicate submission need stable operation identity and recovery; a successful earlier step does not mean a complete request exists.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Provider seam and explicit verification states, clinic-zone slot generation, tenant callback and purpose-bound existing-patient tokens make important boundaries visible. |
| Limitations | Credential results can become stale or overwrite newer facts; sweep coverage is capped; implicit hours can mislead; new-phone identity and intake partial failures need explicit policy. |
| Recommended design | Version verified credential inputs and attempts, schedule bounded due-time rechecks, and separate trustworthy verdicts from provider/manual-review availability. |
| Availability | Require approved hours and consistent multi-clinic associations; define DST/nonexistent local-time policy; retain candidate-slot versus reservation wording. |
| Intake | Enforce deployment-backed abuse limits, scoped identity proof where required, request fingerprints and durable recovery across patient/consent/request creation. |
| Acceptance evidence | Stale provider results cannot replace a newer credential version; all due doctors receive fair coverage; cross-clinic tokens fail; duplicate intake returns one request; confirmation atomically claims a currently available slot. |

These are recommended improvements, not implemented production guarantees. If the product stays request-based, expose status and a response-time policy. A request avoids promising immediate booking; it does not eliminate concurrency problems when staff later confirm it.

## Mistakes and Best Practices

Do not infer zero phone squatting, lapsed-registration detection, support incidents or complete RLS enforcement from this source. Trace OTP challenge issuance/finalization and rate-limit guard/storage separately, using the patient-portal boundaries as a comparison rather than assuming identical implementation.

Test clinic membership, stale verification results, due-time pagination, provider failures, timezone boundaries, missing hours, time off, expired/wrong-scope tokens, duplicate intake and confirmation races. Cache candidate availability only with clear freshness and invalidation rules; materialize windows when measured load justifies it.

## Code Evidence

Paths are in the inspected Docita checkout.

| Mechanism | Source path |
| -------------------------------- | --------------------------------------------------------------------------------------------------- |
| Provider and manual verification | `apps/api/src/domains/doctors/application/services/doctor-verification.service.ts` |
| Sweep selection and writes | `apps/api/src/domains/doctors/infrastructure/repositories/prisma-doctor-verification.repository.ts` |
| Availability and fallbacks | `apps/api/src/domains/doctors/application/services/slot-generation.service.ts` |
| Clinic resolution/context | `apps/api/src/domains/public-booking/application/services/public-booking-utils.ts` |
| Token purpose and audience | `apps/api/src/domains/public-booking/application/services/public-booking-token.service.ts` |
| Intake and partial boundaries | `apps/api/src/domains/public-booking/application/services/public-booking-submit.service.ts` |

## Summary

Describe verification as dated evidence, slots as candidate capacity and anonymous intake as a scoped request. Protect each transition with its own identity, concurrency and recovery policy instead of treating a shared tenant wrapper or token as a universal guarantee.

## See Also

- [Category revision](REVISION.md) — verification and request questions.
- [Patient portal](16-patient-portal.md) — OTP and session boundaries.
- [Clinic workflows](05-clinic-workflows.md) — final scheduling constraints.
- [Prescription validation](07-prescription-safety.md) — use of verification state.
- [Case-study index](INDEX.md) — reading order.
