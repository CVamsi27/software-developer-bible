# 17 — Patient Portal

> Patients get their own read-mostly window into the clinic: OTP login by WhatsApp, scoped PHI read endpoints (records, prescriptions, invoices, clinical timeline, medication adherence), and a UI that can never touch another patient's data because the session itself is patient-bound.

---

## Context

Docita's data belongs to clinics, but the *patient* is the subject of it — and Indian law (DPDP Act, 2023) plus product sense both say patients should see their own health data. The patient portal is that surface:

- **Login without passwords** — patients are not staff; they don't have credentials and won't remember a password. WhatsApp OTP is the natural channel (Docita already talks to patients over WhatsApp).
- **Read-mostly, but not read-only** — patients view prescriptions, invoices, and a clinical timeline, and *record medication doses / adherence* (the one interactive write).
- **PHI at stake** — a portal bug that leaks one patient's prescriptions to another is a DPDP breach and a destroyed trust story.

**The problems:** (1) OTP login is a race against brute force — 6 digits is only 10⁶ space, and the verify path must consume attempts atomically or concurrent requests all pass the "attempts left" check; (2) "the patient" must be derived from the *session*, not from request parameters, or nothing stops a patient from querying another's records by swapping an ID; (3) OTP delivery must not reveal whether a phone number is registered (account enumeration); (4) there is no patient "password" — so session lifecycle and token expiry are the whole auth story.

---

## Decision 1: Passwordless WhatsApp OTP with Brute-Force-Hardened Verification

### What We Chose

Request flow (`requestOtp`): normalize phone to E164 → if a patient exists for that phone, generate a 6-digit OTP with `crypto.randomInt(100000, 1_000_000)` (inclusive of 999999 — the code comments call out that an earlier `999_999` upper bound silently biased the space), bcrypt-hash it (cost 10), **invalidate prior OTPs for that phone**, store the new one with a 10-minute expiry, and send via the WhatsApp login-OTP template.

Verify flow (`verifyOtp`): look up the active OTP → **atomically consume an attempt** via `tryConsumeOtpAttempt` (a single conditional UPDATE that checks-and-increments so concurrent requests can't all observe `attempts < MAX`) → if attempts remain, `bcrypt.compare` the submitted OTP.

```typescript
// apps/api/src/domains/patient-portal/application/services/patient-portal-auth-command.service.ts
private static readonly MAX_OTP_ATTEMPTS = 3;
// Max attempts per OTP. Bound chosen so a real user mistyping twice has room to
// recover, but brute-force against a 6-digit OTP cannot succeed
// (10^6 / 3 ≈ 333k OTPs needed, each costing an SMS).
```

### Why This Was Chosen

- **Enumeration-safe request** — `requestOtp` returns the *same* message whether or not the phone exists ("If a patient account exists for this phone, an OTP has been sent"). The OTP is only sent when a patient exists, but an attacker can't distinguish by response shape.
- **bcrypt at cost 10** — even if an OTP row leaks (DB read), the stored value isn't reversible quickly; hashing OTPs (not storing plaintext) is the same discipline as passwords.
- **Per-OTP attempt cap of 3, consumed atomically** — the comment is the threat model: an attacker needs ~333k OTPs and each costs an SMS + a bcrypt compare. Atomic consumption closes the concurrent-request bypass.
- **Invalidate-on-request** — requesting a new OTP kills old ones, so a leaked earlier OTP can't be replayed after re-request.

### Alternatives Considered

- Password + email reset — patients don't manage passwords; support load would drown the clinics.
- TOTP/authenticator — inappropriate for the demographic (patients range from 20 to 80+; most interact via WhatsApp links).
- Phone-call OTP — more expensive and slower than WhatsApp.

### Trade-offs

- **WhatsApp delivery is the single point of availability** — if Meta's API is degraded, login is down. The portal can't fall back to SMS without a second provider integration.
- **10-minute expiry vs convenience** — short enough to be safe, long enough that most patients complete within it; expired OTPs force a re-request.
- **Attempt cap of 3** can frustrate a patient who mistypes 3 times — they re-request, which invalidates and re-issues; the friction is deliberate.

---

## Decision 2: The Session IS the Patient — Context From the Token, Not Parameters

### What We Chose

After OTP success, the patient receives an app session (via shared `AuthService`). Every portal controller resolves the patient from the **authenticated user**, never from a client-supplied patientId. `PatientPortalContextService.getPatientContext(userId)` looks up the patient by userId and throws `UnauthorizedException` if none exists, returning `{ patient, patientId, clinicId }` for downstream scoping.

Controllers then scope *every* query by that patientId: `patient-portal-records.controller.ts` (`GET prescriptions`, `GET prescriptions/:id`, `GET invoices`), `patient-portal-clinical.controller.ts` (timeline, snapshot, active medications, **doses + adherence**).

### Why This Was Chosen

- **IDOR is structurally impossible** — a patient asking for `prescriptions/:id` only ever queries with their own derived patientId; there is no endpoint that takes "another patient's id" and returns data.
- **One resolution point** — the context service is the single place that maps a session to a patient; a new portal endpoint can't forget to scope because it starts from the same resolved context.
- **ClinicId comes along for free** — portal reads are clinic-scoped like everything else, so RLS still applies beneath the patient scoping.

### Trade-offs

- **Patient ↔ user identity is a 1:1 assumption** — the portal repository (`findPatientByUserId`) treats a user as *the* patient; if Docita ever needs a guardian/representative portal (a parent managing a child's records), this mapping needs a relation table, not a single patientId.

---

## Decision 3: The Interactive Write Is Bounded to Medication Adherence

### What We Chose

Of everything a patient could do, the portal allows exactly one class of write: **recording medication doses and adherence** (`POST medications/doses`, `GET medications/adherence`). Everything else — prescriptions, invoices, timeline, active medications — is read-only for the patient.

### Why This Was Chosen

- **Adherence is the one thing only the patient knows** — "did you take tonight's dose?" has no other source of truth; capturing it in the portal turns a read-only app into a clinical-data contributor without letting patients edit clinical records.
- **Read-mostly is a PHI risk decision, not a laziness decision** — every write surface is another place a patient (or a bug) can corrupt the record a doctor relies on. Restricting writes to adherence keeps the clinical write path staff-only and audited.
- **Dose confirmation is a natural OTP-session interaction** — it fits the "patient taps a link, confirms the dose" pattern the product already uses for confirmations.

### Trade-offs

- **Adherence data quality depends on patient honesty and memory** — the feature records *reported* adherence; nothing reconciles it against refill data (pharmacy claims could, later).
- **No patient-initiated corrections** — a patient who spots a wrong phone number or address on their profile can't fix it in the portal; it's read-only, and corrections route to the clinic. Deliberate (avoid PHI edit conflicts), but adds clinic workload.

---

## What Worked

- **Zero IDOR incidents** — because the session is the patient and every query derives from context, the classic "change the id in the URL" attack class never surfaced.
- **OTP login converted effortlessly** — patients who already got WhatsApp messages from the clinic accepted a login link + OTP without training; support load for "I forgot my password" is zero by construction.
- **Atomic attempt consumption held under load** — a test that fired concurrent verify requests against one OTP confirmed only `MAX` compares could ever run.

## What Failed

- **The first OTP generator biased the space** — `randomInt(100000, 999999)` (exclusive max) silently excluded `999999`; the fix to `1_000_000` is documented in a code comment precisely because the bug was invisible. Lesson: read the `randomInt` upper-bound semantics.
- **Session expiry confusion** — an early iteration let portal tokens live as long as staff tokens; a shared token TTL meant sessions outlived their usefulness and patients got confusing "please log in again" states mid-flow. Portal sessions now use their own, shorter lifecycle.
- **WhatsApp template lock** — the login OTP had to ride an approved Meta template (`patient_login_otp`); template rejections blocked rollout until the copy was re-approved.

## What Could Be Better

- **Per-phone request rate limit** — invalidate-on-request prevents replay but not *spam*; a patient who taps "resend" 20 times burns 20 WhatsApp sends. A request-side cooldown (e.g., 30–60s, or N/hour per phone) is missing.
- **Device/session revocation** — there's no "log out all devices" or per-device session list for patients; a lost phone leaves a live session until natural expiry.
- **Representative/guardian model** — as noted, parent-manages-child and caretaker access need a proper relation instead of the 1:1 assumption.
- **Portal read model caching** — timeline + adherence reads hit live tables per request; fine now, but a patient-specific read snapshot would cut primary load as portal usage grows.

---

## Code Evidence

| Claim | File |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| OTP request/verify + attempt cap | `apps/api/src/domains/patient-portal/application/services/patient-portal-auth-command.service.ts` |
| Atomic attempt consumption | `apps/api/src/domains/patient-portal/core/repositories/portal-auth.repository.interface.ts` (+ Prisma impl) |
| Session → patient context | `apps/api/src/domains/patient-portal/application/services/patient-portal-context.service.ts` |
| Portal auth endpoints | `apps/api/src/domains/patient-portal/presentation/controllers/patient-portal-auth.controller.ts` |
| Records endpoints (prescriptions/invoices) | `apps/api/src/domains/patient-portal/presentation/controllers/patient-portal-records.controller.ts` |
| Clinical timeline + adherence | `apps/api/src/domains/patient-portal/presentation/controllers/patient-portal-clinical.controller.ts` |
| Shared WhatsApp login-OTP helper | `apps/api/src/shared/whatsapp/whatsapp-login-otp.helper.ts` |
| Shared auth (session issue) | `apps/api/src/shared/modules/auth/auth/auth.service.ts` |

---

## Interview Script (60 seconds)

> "The patient portal is passwordless: login is a 6-digit OTP over WhatsApp, bcrypt-hashed at rest, with a 10-minute expiry and a three-attempt cap that's consumed atomically — one conditional update, so concurrent guesses can't all pass the attempts check. The request endpoint is enumeration-safe: it returns the same message whether or not the phone is registered, and requesting a new OTP invalidates old ones. The security property I'm proudest of is that the session *is* the patient: every controller resolves the patient from the authenticated user via one context service, then scopes all queries by that derived patientId — there's no endpoint that accepts another patient's id, so IDOR is structurally impossible rather than merely discouraged. Patients are read-only except for medication adherence, which is the one thing only they know. The gap I'd fix next is request-side OTP rate limiting and per-device session revocation."
---

[← Previous: Doctors Verification And Public Booking](15-doctors-verification-and-public-booking.md) · [ Back to Index](INDEX.md) · [Next: ABDM Integration →](17-abdm-integration.md)
