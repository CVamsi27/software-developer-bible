# 16 — Patient Portal Identity and Access

## Definition

The patient portal gives an authenticated patient access to selected records and a medication-dose reporting surface. Its security boundary is the mapping from authenticated user to patient and clinic, followed by ownership checks for each requested resource.

The concrete failure to prevent is simple: a patient changes a prescription ID in the URL and receives someone else's record.

## First Principles

A phone OTP proves temporary control of a delivery channel, not an immutable patient identity. Shared phones, recycled numbers and guardian access require an explicit account-linking policy.

A short code also has a small search space. Limiting guesses per challenge helps online attacks; limiting challenge issuance prevents an attacker from continuously obtaining fresh attempts or exhausting messaging capacity. Neither control makes guessing mathematically impossible.

## How OTP Request and Verification Work

The command normalizes the phone, finds a patient, generates a code using `crypto.randomInt(100000, 1_000_000)`, bcrypt-hashes it at cost 10, invalidates previous unused codes, stores a ten-minute expiry, and invokes the WhatsApp login template helper.

The upper bound is exclusive. This range has 900,000 possible codes, not one million: leading-zero codes are excluded. Excluding only 999999 in an earlier range was an off-by-one issue, not evidence of a severe attack or a production incident.

The normal response has the same message whether a patient exists. That reduces response-body enumeration, but the registered path also performs hashing, storage and delivery. Timing, exceptional responses and externally observable side effects must be assessed before claiming enumeration is eliminated.

Verification follows these steps:

```text
Find latest unused, unexpired challenge
                 ↓
Conditional attempt increment below cap of three
                 ↓
Compare supplied code against hash
                 ↓
Mark challenge used
                 ↓
Resolve/create user → link patient → shared login
```

The atomic attempt update prevents concurrent requests from each observing unused attempt capacity and performing unlimited comparisons. However, its predicate checks ID and attempt count only; it does not recheck expiry or usedAt. The successful-use update is a later unconditional write.

Thus attempt-cap enforcement and single-use success are different properties. Concurrent correct submissions can each consume an available attempt, compare successfully and proceed to login. A code invalidated or expired after the initial read can also pass that later attempt predicate. The source does not justify a universal replay-prevention claim.

Invalidation and new challenge creation are separate repository calls. Concurrent resend requests need a defined newest-challenge policy. User creation and patient linking also occur separately, so concurrent first login needs uniqueness and transaction handling rather than reliance on a prior absence check.

## Request Throttling and Session Cookies

Both public auth endpoints carry a Nest throttle configuration of five requests per 60 seconds in the short bucket. This is existing metadata, not proof of active deployment enforcement: guard installation, tracker key, proxy trust and shared rate-limit storage determine its effective scope.

Do not call request-side throttling entirely absent. A phone-specific cooldown, distributed abuse controls and delivery-budget limit still need separate verification; an IP-based endpoint limit is not equivalent to those controls.

The auth controller sets HTTP-only access and refresh cookies, uses Secure in production and SameSite Strict, and restricts the refresh cookie path to `/api/v1/auth`. It uses shared AUTH_CONSTANTS and the command invokes shared AuthService login. This path does not establish a separate shorter portal token lifetime.

Trace token audience, patient role, refresh rotation, logout/revocation and browser-origin behavior through the shared auth system. Cookie flags reduce particular risks; they do not prove every session lifecycle or CSRF boundary is correct.

## How Session-derived Context Prevents ID Swapping

`PatientPortalContextService.getPatientContext(userId)` resolves a patient from the authenticated user and returns patientId plus clinicId. Missing linkage is unauthorized. Controllers declare patient-session metadata, JWT guard and PATIENT role requirements.

Prescription detail still accepts a resource ID. The service and repository must combine that ID with the derived ownership scope. Deriving a patient ID centrally is a useful design choice, but a new endpoint can still omit or misuse it. Tenant isolation and IDOR resistance require checks on every read, write, file URL and nested relation.

The current mapping treats one user as one patient context. A parent or caregiver managing several patients needs an explicit, revocable delegation relation with scope and audit evidence. Do not weaken patient ownership by allowing an arbitrary request patientId.

## Examples: Dose Reporting Is a Separate Write Boundary

The clinical controller exposes timelines, snapshots, active medications, dose history, adherence summaries and a dose-report POST. It derives patient and clinic before delegating to the medication service.

The POST body declares status values TAKEN, MISSED and SKIPPED, but the inspected controller does not forward that status to `recordAdHocDose`; it forwards medication ID, time, amount and notes with source PATIENT_REPORTED. A declared body field therefore does not prove that the requested status is applied.

Medication ownership, duplicate reports, invalid/future timestamps and dose semantics must be checked by the service and validated input boundary. Treat the report as patient-provided evidence, not independently confirmed medication consumption.

Some clinical and prescription reads call the audit helper. In the inspected controllers, active-medication reads and invoice reads do not use that same helper. Do not describe audit coverage as universal without tracing other middleware and downstream auditing.

## Current Assessment and Recommended Design

| Assessment | Source-backed implication |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Session-derived context, conditional attempt counting, hashed challenges, declared endpoint throttling and scoped role metadata address concrete risks. |
| Limitations | Final OTP use is separate from verification, issuance/user linking can race, response timing differs, and shared-session behavior needs tracing. |
| Recommended design | Validate challenge input, bound issuance by phone/device/network and delivery budget, then atomically finalize a still-valid unused challenge after comparison. Create/link identity transactionally and enforce patient ownership at each repository operation. |
| Session policy | Use explicit patient token scope and lifecycle, rotate refresh credentials, support revocation, and model guardian delegation rather than overloading one patient link. |
| Acceptance evidence | Concurrent correct submissions yield one challenge finalization; expired/invalidated challenges cannot finalize; resend races have one active policy; another patient's IDs never return records or accept writes. |

This is the recommended target design, not a claim that it is implemented. Generic responses should be tested for timing and failure differences, and distributed rate limits should be tested through the actual deployed ingress.

## Mistakes and Best Practices

- Treating three attempts as proof that brute force cannot succeed: state the bounded probability and issuance controls.
- Treating bcrypt as high entropy: an OTP still has a small candidate space; protect hash access and challenge lifetime.
- Treating a lookup followed by mark-used as atomic single use: finalize with a conditional write and check its result.
- Treating role metadata as universal authorization: verify guard wiring and each nested resource lookup.
- Claiming zero IDOR incidents, effortless adoption or a shorter portal TTL without current evidence: separate design intent from measured outcomes.

Test different patients and clinics, shared/recycled phone scenarios, expired challenges, concurrent verification, resend races, distributed throttling, stale sessions, logout and medication-resource ownership.

## Code Evidence

Paths below are from source inspection, not a completed production security assessment.

| Mechanism | Source path |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| OTP orchestration | `apps/api/src/domains/patient-portal/application/services/patient-portal-auth-command.service.ts` |
| Attempt and used-state writes | `apps/api/src/domains/patient-portal/infrastructure/repositories/prisma-portal-auth.repository.ts` |
| User → patient context | `apps/api/src/domains/patient-portal/application/services/patient-portal-context.service.ts` |
| Throttle and cookies | `apps/api/src/domains/patient-portal/presentation/controllers/patient-portal-auth.controller.ts` |
| Records surface | `apps/api/src/domains/patient-portal/presentation/controllers/patient-portal-records.controller.ts` |
| Clinical reads and dose write | `apps/api/src/domains/patient-portal/presentation/controllers/patient-portal-clinical.controller.ts` |

## Summary

Derive patient scope from authenticated identity and enforce it for every resource. Count OTP attempts atomically, but verify final single-use consumption separately. Treat request throttling, channel control, account linking and session revocation as distinct parts of the design.

## See Also

- [Category revision](REVISION.md) — patient identity and OTP questions.
- [Multi-tenancy and RLS](02-multi-tenancy-rls.md) — context and database boundaries.
- [WhatsApp integration](06-whatsapp-integration.md) — delivery and processing gaps.
- [Documents and uploads](19-documents-and-uploads.md) — authorized document access.
- [Case-study index](INDEX.md) — reading order.
