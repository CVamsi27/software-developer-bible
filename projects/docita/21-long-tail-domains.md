# 22 — The Long Tail: Reminders, Custom Fields, Webhooks, Lab Portal, Leave, Feedback, Users

> The domains that don't headline an interview but show engineering range: an automation scheduler that must never double-text a patient, a small dynamic-schema facility, the webhook trust boundary, a staff leave system that publishes doctor time-off, and the smallest domains that are easy to get subtly wrong.

---

## Context

Docita's headline domains (billing, prescriptions, clinic workflows, RLS) carry the architecture story. These seven don't — but each encodes at least one decision worth being able to defend, and several share a recurring theme: **side effects that must be deduplicated, scoped, or reversed correctly even in small features.**

- **reminders (~2.8k LOC)** — the largest of the tail: per-clinic automation settings, a scheduler that scans for due appointments, per-channel send + dedupe, and a manual "send now" path.
- **custom-fields (~670 LOC)** — per-clinic dynamic fields (text/number/select/date/checkbox/textarea) on top of the fixed Patient model.
- **webhooks** — inbound webhook *verification* (shared module) + error/audit persistence (domain) + an outbound delivery system with retries.
- **lab-portal (~125 LOC)** — a scaffold: role-scoped login for lab technicians.
- **leave (~1.6k LOC)** — staff leave plans (quota/carry-forward), requests with approve/reject/cancel, and the interesting bit: approving a *doctor's* leave writes time-off into the availability system so slots vanish.
- **feedback (~1.6k LOC)** — in-app product feedback with category/status workflow and stats.
- **users (~925 LOC)** — profile, guided-tour state, account deletion.

The unifying lesson: even the "small" domains in this codebase are built with the same discipline (ports over direct imports, clocks injected for time, transactions where two writes must commit together, feature/role gates on every controller) — which is itself an interview story about consistent engineering culture.

---

## Domain 1: Reminders

### Context

Clinics want patients reminded about appointments over email, SMS, and WhatsApp — configured per clinic (which channels, how many hours before, whether a 30-minute WhatsApp nudge is on). Patients forget; clinics lose revenue to no-shows; but **over-reminding is as bad as under-reminding** (patients get annoyed, and WhatsApp messages cost money per template).

### Decisions

**D1 — Push scheduler, not per-appointment jobs.** Two `@Cron`s run on schedules: an hourly scan that finds appointments in the window (`startTime BETWEEN now AND now + hoursBeforeAppt`) for enabled clinics, and a 30-minute-dispatch scan. No per-appointment scheduled jobs, no job table, no missed-job recovery problem — if a cron tick is skipped, the next tick still finds the appointment (within its window).

**D2 — The cron is RLS-bypassed by design, per clinic batch.** The scheduler scans *across* clinics (it has no request context), so it wraps in `runUnrestricted`, loads enabled settings, then processes each clinic as its own `Promise.allSettled` batch:

```typescript
// reminders/application/services/reminder-scheduler.service.ts
return await this.persistence.runUnrestricted(async () => {
  const allSettings = await this.persistence.reminderSettings.findMany({
    where: { enabled: true, clinicId: { not: null } },
  });
  ... // per-clinic Promise.allSettled batches
});
```

**D3 — Send dedupe is per-channel and type-scoped.** Before sending, the scheduler loads existing `appointmentReminder` rows for the appointments in play and skips a channel that already has a `sent` row of that type. Crucially, the dedupe lookups are *narrowed*: the 30-minute WhatsApp pass only suppresses on prior `whatsapp_30min` rows ("only a previously SENT whatsapp_30min reminder suppresses this pass — email/SMS/hourly rows must never mask the 30-minute nudge"), and the hourly pass dedupes per channel so an already-sent email never suppresses the WhatsApp nudge.

**D4 — Settings are per-clinic with sensible fallbacks, and the WhatsApp send is policy-gated.** `ReminderSettingsService` provides a complete fallback settings object (24h, email+WhatsApp, template text) so the feature works before a clinic configures anything. Each WhatsApp send first checks `isClinicWhatsAppAutomationSendingAllowed(clinicId)` — a tier/feature gate (requires WHATSAPP_MESSAGING) plus the clinic's own automation opt-out — so a Free-tier clinic or an opted-out clinic is never texted.

**D5 — Manual "send now" exists for the front desk.** `POST /reminders/send/:appointmentId` lets staff nudge a specific patient immediately (e.g., a no-show-risk patient sitting in the waiting room), reusing the same send path.

### Trade-offs

- **Time-window scans mean reminder time is approximate** — an appointment at 10:00 with `hoursBeforeAppt: 24` is caught by whichever hourly tick sees it first within the window, not at exactly 24:00 before. Precision is unnecessary; simplicity (no job scheduler) is worth it.
- **`Promise.allSettled` swallows per-appointment failures into a count** — a failed send logs a warning but isn't retried by the scheduler (no per-appointment retry state); the manual send-now path is the recovery.
- **Database auth failure disables the cron via a latch** (`databaseAccessDisabled`) — deliberate: stop hammering a dead DB and surface via heartbeat instead of erroring every tick.

### What Worked / What Failed

Worked: per-channel dedupe prevents double-texts in production (no double-text complaints); the DB-auth latch turns a noisy cron into a quiet one. Failed/guarded: the dedupe lookups are deliberately *type-scoped* — the code comments call out that an email/SMS/hourly row must never suppress the 30-minute WhatsApp nudge the clinic explicitly enabled — which is exactly the bug a naive "any reminder already sent?" check would cause; the narrowing is documented at each lookup.

### Code Evidence

| Claim | File |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Hourly + 30-min schedulers | `apps/api/src/domains/reminders/application/services/reminder-scheduler.service.ts` |
| Channel sends + templates | `apps/api/src/domains/reminders/application/services/reminder-notification.service.ts` |
| Per-clinic settings + fallbacks | `apps/api/src/domains/reminders/application/services/reminder-settings.service.ts` |
| History query | `apps/api/src/domains/reminders/application/services/reminder-history.service.ts` |
| HTTP surface + access decorator | `apps/api/src/domains/reminders/presentation/controllers/reminders.controller.ts`, `reminders.controller.access.ts` |
| WhatsApp policy gate | `apps/api/src/shared/whatsapp/whatsapp-patient-send-policy.util.ts` |

### Interview Script (30 seconds)

> "Appointment reminders are a push scheduler, not per-appointment jobs: cron ticks scan for appointments entering each clinic's configured window, so a skipped tick self-heals. The scheduler runs RLS-bypassed across clinics and processes them as isolated batches. The correctness core is dedupe: sends are recorded per channel and per type, and each pass only suppresses on its own type — so an hourly email can never mask the 30-minute WhatsApp nudge the clinic explicitly enabled. WhatsApp sends are policy-gated per clinic by tier and automation opt-out, and per-clinic fallback settings make the feature work before configuration. Manual send-now reuses the same path for the front desk."

---

## Domain 2: Custom Fields

### Context

Clinics have intake needs Docita's fixed Patient columns don't cover — a dental clinic wants "last cleaning date", a physio wants "injury side". The obvious answer is per-clinic dynamic fields, but **the trap is scope**: a custom field must belong to one clinic (never leak across tenants) and values must live somewhere queryable, not in an untyped blob the rest of the product ignores.

### Decisions

**D1 — A definition table with clinic scoping.** `CustomField` rows hold `name`, `fieldType` (text/number/select/date/checkbox/textarea — a fixed enum of options from `CUSTOM_FIELD_TYPE_OPTIONS`), `options` (for select), `required`, `order`, and `clinicId` (nullable → platform-level defaults). The repository interface (`ICustomFieldsRepository`) exposes find/create/update/delete, all clinic-scoped (`findAll(clinicId)`, and `findOne` cross-checks `field.clinicId === clinicId`).

**D2 — Values ride the patient's `customData` JSON, definitions drive the UI.** The schema shows `Patient.customData Json @default("{}")`; the patient mapper reads/writes it (`Object.fromEntries(...)`), while the frontend fetches the clinic's field definitions to render the form. This keeps the *definition* typed and validated while the *values* stay flexible.

### Trade-offs

- **`customData` is schema-less** — a field renamed in definitions orphans old values under the old key; there's no migration tool for JSON keys.
- **Validation is frontend-driven** — nothing server-side enforces that submitted `customData` keys match the clinic's current field definitions or that `required` fields are present; a clinic changing definitions can break past submissions' rendering.

### What Worked / What Failed

Worked: clinic-scoping checks in `findOne`/update prevented cross-tenant field edits. Failed: the domain is small and under-integrated — nothing in the API *validates* customData against the definitions at write time, so a bold claim about "dynamic schema" in an interview must be scoped honestly to "definitions CRUD + JSON values".

### Code Evidence

| Claim | File |
| ------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Definition CRUD | `apps/api/src/domains/custom-fields/application/services/custom-fields.service.ts` |
| Repository + types | `apps/api/src/domains/custom-fields/application/ports/custom-fields.repository.port.ts` |
| Prisma implementation | `apps/api/src/domains/custom-fields/infrastructure/repositories/prisma-custom-fields.repository.ts` |
| Field-type options | `packages/utils/src/config/config-options.ts` (`CUSTOM_FIELD_TYPE_OPTIONS`) |
| Patient customData | `apps/api/src/domains/patients/infrastructure/mappers/patient.mapper.ts`, `packages/db/prisma/schema.prisma` |

### Interview Script (30 seconds)

> "Custom fields are a small facility: a per-clinic definition table with a fixed field-type vocabulary — text, number, select with options, date, checkbox, textarea — plus `clinicId` scoping so definitions never leak across tenants, and a nullable clinicId for platform-level defaults. Values live in the patient's `customData` JSON while definitions drive the UI. The honest limitation I'd flag: values aren't validated server-side against current definitions, so renaming a field can orphan old data — the next step is a write-time validation pass."

---

## Domain 3: Webhooks (Inbound Verification, Outbound Delivery)

### Context

Docita is a webhook *consumer* (Razorpay payment events, Meta status callbacks) and a webhook *producer* (clinics/labs subscribe to Docita events). Both directions face the same two questions: **is this caller who they claim to be?** and **did we already process this event?**

### Decisions

**D1 — Inbound verification is provider-aware, replay-deduped, timestamp-tolerant.** The shared `webhook-verifier.ts` verifies HMAC signatures over the raw body (`createHmac('sha256', secret)` compared with `timingSafeEqual`), rejects signatures outside a 5-minute timestamp tolerance, and **claims a replay key** through a dedupe store (`WebhookReplayDedupeRepository.tryClaim`) so the same event delivered twice is processed once. Razorpay's specific scheme gets its own helper (`razorpay-webhook-verification.helper.ts`).

**D2 — Inbound failures are persisted, not just logged.** The `webhooks` domain's `WebhookErrorHandlingService` writes structured `errorLog` rows (with `payloadHash`, not the payload — PHI discipline) and `auditLog` rows for PENDING/SUCCESS/FAILED tracks, marking critical failures `CRITICAL` severity. Billing's payment webhook controller uses it (`trackWebhookEvent`, `logWebhookError`), so every Razorpay event outcome is audit-trailed.

**D3 — Outbound deliveries are queued rows with HMAC signatures and retry state.** `OutgoingWebhookService.dispatch` fans an event out to matching `WebhookSubscription` rows, creating an `OutgoingWebhookDelivery` per subscriber with an **idempotency key** (`{sub.id}:{aggregateId}:{timestamp}`, unique-constrained — a unique violation means "already enqueued, skip"). `sendDelivery` signs each POST with `X-Webhook-Signature` (HMAC-SHA256 over the payload) and a delivery row carries `attemptCount`/`maxAttempts` (5), `lastStatusCode`, `lastError`, and exponential backoff constants (`BACKOFF_BASE_MS 5s`, `cap 300s`) for the retry loop.

### Trade-offs

- **Two verification schemes to maintain** (generic + Razorpay-specific) — the Razorpay helper exists because its signing format differs; each new provider adds a small adapter.
- **Replay dedupe uses a TTL cache** (10 min) — an attacker replaying an *old but validly signed* event outside the TTL window could theoretically reprocess; the 5-minute timestamp tolerance bounds the real risk.
- **Error-logging stores a payload hash, not the payload** — great for PHI, but debugging a malformed payload requires correlating via the hash + providerId.

### What Worked / What Failed

Worked: the dedupe + timestamp tolerance combo absorbed real Razorpay double-deliveries without double-billing (the payment domain's own idempotency keys are the second net). Failed: outbound retry state exists but the *worker* that drains PENDING deliveries with backoff lives outside these files — the rows are there, the loop's cadence is shared infra, and a delivery stuck at attempt 5 needs manual eyes.

### Code Evidence

| Claim | File |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Inbound verifier (HMAC + replay + tolerance) | `apps/api/src/shared/modules/webhooks/webhook-verifier.ts` |
| Razorpay-specific verification | `apps/api/src/shared/modules/webhooks/razorpay-webhook-verification.helper.ts` |
| Replay dedupe store | `apps/api/src/shared/modules/webhooks/webhook-replay-dedupe.repository.ts` |
| Error/audit persistence domain | `apps/api/src/domains/webhooks/application/services/webhook-error-handling.service.ts` |
| Outbound dispatch + signing | `apps/api/src/shared/modules/webhooks/outgoing/outgoing-webhook.service.ts` |
| Subscriptions + deliveries models | `packages/db/prisma/schema.prisma` (`WebhookSubscription`, `OutgoingWebhookDelivery`) |
| Consumer example (payment webhooks) | `apps/api/src/domains/billing/presentation/controllers/webhooks.controller.ts` |

### Interview Script (30 seconds)

> "Docita is both a webhook consumer and producer. Inbound: we verify HMAC signatures over the raw body with constant-time compare, enforce a 5-minute timestamp tolerance, and dedupe replays through a TTL'd claim store so a double-delivered Razorpay event can't double-process — and every outcome is persisted as an audit event with a payload hash, never the payload. Outbound: clinics subscribe to events, dispatch creates a delivery row per subscriber with a unique idempotency key so re-dispatches are no-ops, and each delivery is signed with an HMAC header and carries retry state — attempt count, max five attempts, exponential backoff — so the delivery worker can resume rather than lose events."

---

## Domain 4: Lab Portal

### Context

External lab partners need a login to upload results — but they are **not clinic staff**. The domain exists to give a `LAB`-role account its own authentication surface without entangling it in the clinic-user flows.

### Decisions

**D1 — Role-restricted login on its own controller.** `POST /lab-portal/auth/login` validates credentials through the shared `AuthService.validateUser`, then *additionally* requires `user.role === Role.LAB` — a generic staff account cannot sign in here, and a lab account can't sign in through the staff portal with elevated rights:

```typescript
// lab-portal/application/services/lab-portal-auth.service.ts
if (!user || user.role !== Role.LAB)
  throw new UnauthorizedException('Invalid credentials or not a lab technician account.');
```

**D2 — Login is Zod-validated and reuses the shared session service.** The DTO is a strict Zod schema (email + password); successful auth flows through `AuthSessionService.login` so lab sessions share the same session mechanics, expiry, and audit as everyone else.

### Trade-offs

- **It's a scaffold, not a portal** — only auth exists; the *rest* of the lab experience (worklist, result upload) still runs through the clinic's lab-workflow controllers (deep-dive 20). The separate login is the trust boundary; the feature surface is the next milestone.
- **A `LAB` role must exist on the user** — provisioning lab users is a separate admin step; nothing self-serves account creation here.

### What Worked / What Failed

Worked: role-gating at the login boundary kept the lab surface from accidentally broadening staff permissions. Failed: nothing yet — it's small enough that the honest answer is "auth only, deliberately scoped; the worklist and result-upload UX are the known next step."

### Code Evidence

| Claim | File |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| Lab auth command | `apps/api/src/domains/lab-portal/application/services/lab-portal-auth.service.ts` |
| Login DTO (Zod) | `apps/api/src/domains/lab-portal/application/dto/lab-portal-auth.dto.ts` |
| Login route | `apps/api/src/domains/lab-portal/presentation/controllers/lab-portal-auth.controller.ts` |

### Interview Script (20 seconds)

> "The lab portal is intentionally tiny: a role-restricted login surface. External lab technicians authenticate through the shared auth service but are additionally gated to the `LAB` role, so a clinic staff account can't sign in there and a lab account can't gain staff privileges. Sessions reuse the shared session service. The domain is auth-only by design — the lab worklist and result upload still live in the clinical domain — and that scoping is the point: a separate trust boundary without a parallel auth system."

---

## Domain 5: Leave (Staff Time Off)

### Context

Clinics have staff (receptionists, nurses, doctors) who take leave. The interesting requirement is cross-domain: **when a doctor goes on leave, their appointment slots must disappear** — otherwise patients book into a vacation. Leave therefore isn't just a HR CRUD; approving a doctor's leave must reach the availability/slot system (deep-dive 15).

### Decisions

**D1 — Leave plans are per-clinic, upserted by type.** `LeavePlan` rows (per clinic + `leaveType`: CASUAL/SICK/EARNED/COMP_OFF/UNPAID/HOLIDAY) carry `annualQuota`, `carryForward`, `maxCarryForward`, upserted on the `@@unique([clinicId, leaveType])` so a plan is created-or-updated, never duplicated.

**D2 — Balance is derived at query time.** `getLeaveBalance` computes for the current year, per leave type: quota (from the plan), `used` (sum of APPROVED days, inclusive date math `ceil(diff)+1`), `remaining = max(0, quota − used)`, and `pending`. No balance columns to drift; PENDING days count separately so staff see "what's in flight".

**D3 — Approval is a transaction that publishes doctor time-off.** `approveLeave` guards (not found → 404, cross-clinic → 403, **self-approval → 403**, non-PENDING → 400), then inside one transaction (a) re-checks status to close the TOCTOU window, (b) if the leaver is a DOCTOR/ADMIN_DOCTOR, calls the availability domain's `createTimeOff` to block the doctor's slots for the leave range, and (c) marks the leave APPROVED:

```typescript
// leave/application/services/leave-command.service.ts
const updated = await this.transactionRunner.runInTransaction(async (tx) => {
  const current = await this.leaveRepository.findLeaveById(leaveId);
  if (!current || current.status !== 'PENDING') throw new BadRequestException(...);
  if (isDoctor) {
    await this.availabilityScheduleService.createTimeOff({ doctorId, clinicId, startDate, endDate, ... }, tx);
  }
  return this.leaveRepository.updateLeave(leaveId, { status: 'APPROVED', approver: {...}, approvedAt: this.clock.now() }, tx);
});
```

**D4 — Enum parsing is centralized.** `parseLeaveType`/`parseLeaveStatus` (over `Object.values`) turn untrusted strings into typed enums with one error message — no scattered `=== 'CASUAL'` string compares.

### Trade-offs

- **Balance ignores carry-forward in `remaining`** — the plan stores `carryForward`/`maxCarryForward`, but the balance query computes `remaining = quota − used` for the current year without adding carried days; a clinic using carry-forward sees understated balances.
- **Cancel of an already-published time-off is best-effort, not atomic** — `cancelLeave` flips the leave to CANCELLED *first*, then deletes the doctor's time-off rows with `Promise.allSettled`, logging warnings on failure. A crash between the two leaves a CANCELLED leave whose slots are still blocked; the warning row is the only recovery signal.
- **Reject sets `approvedAt` too** — both approve and reject stamp `approvedAt` (a copy-paste artifact), so the field name is misleading in the REJECTED case; harmless to queries (status is the discriminator) but a small honesty wart.

### What Worked / What Failed

Worked: the approve transaction kept leave state and doctor availability atomic — no "approved leave but doctor still bookable" state survived a crash; the self-approval guard closed an obvious abuse hole. Failed: carry-forward is stored but not honored in displayed balances — a feature that's half-wired is worse than absent when a clinic relies on it.

### Code Evidence

| Claim | File |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Apply / approve (tx + time-off publish) / reject / cancel | `apps/api/src/domains/leave/application/services/leave-command.service.ts` |
| Balance derivation | `apps/api/src/domains/leave/application/services/leave-query.service.ts` |
| Plan upsert | `apps/api/src/domains/leave/application/services/leave-plan.service.ts` |
| Enum parsing helpers | `apps/api/src/domains/leave/application/services/leave-type.helpers.ts` |
| Plans + leave models | `packages/db/prisma/schema.prisma` (`LeavePlan`, `StaffLeave`, `enum LeaveType`) |
| Time-off writer (consumer) | `apps/api/src/domains/doctors/application/services/availability-schedule.service.ts` |

### Interview Script (30 seconds)

> "Staff leave is small but cross-domain: when a doctor's leave is approved, their appointment slots must disappear, so approval runs in a single transaction that both publishes time-off into the availability system and marks the leave approved — a crash can't leave a doctor on vacation who's still bookable. Leave plans are per-clinic with quotas and carry-forward settings upserted by type; balances are derived at query time from APPROVED days so there are no drift-prone balance columns; and the guards — cross-clinic forbidden, self-approval forbidden, status re-checked inside the transaction — close the obvious abuse and race holes. The honest gap: carry-forward is stored in the plan but not yet added into displayed balances."

---

## Domain 6: Feedback

### Context

Docita asks clinics for product feedback (good/bad features, improvement areas, ratings) and tracks it to resolution. It looks like a CRUD — but the data model has to support *aggregation* (what do clinics complain about most?) and a staff-facing triage workflow.

### Decisions

**D1 — Feedback features are normalized rows, not comma-separated strings.** The `Feedback` row holds `overallRating` + category/status/adminNotes, and each mentioned feature becomes its own `FeedbackFeature` row (`featureType: GOOD|BAD|IMPROVEMENT`, unique per feedback+type+feature). That's what makes `topGoodFeatures`/`topBadFeatures`/`topImprovementAreas` real aggregate queries instead of string matching.

**D2 — A status workflow with stats.** FeedbackStatus (NEW → REVIEWED → IN_PROGRESS → RESOLVED → ARCHIVED) plus `getStats` returning totals, per-status and per-category counts, average rating, recent count, and the top-feature lists — the product team's triage dashboard is a single read.

**D3 — Pure filter builders kept testable.** `feedback-helpers.ts` (no DI, pure functions) builds the Prisma `where` from a filter object (status/category/clinic/date range/rating range/search/limit), and `feedback-enum-parse.ts` centralizes enum parsing — the same "pure helpers beside services" pattern as the leave domain.

### Trade-offs

- **`can-submit` logic implies submission windows/permissions** the reviewed slice only partially shows (`GET /feedback/can-submit`, `GET /feedback/my-feedback`) — worth confirming before claiming a throttle exists.
- **Stats recompute on every call** — no materialized rollup; fine at current volume, will want caching when feedback volume grows (same answer as analytics deep-dive 14).

### What Worked / What Failed

Worked: normalized feedback features made "top complaints" a SQL aggregation, and the pure filter builder kept the query logic spec-testable without a database. Failed: nothing substantial — this is a well-contained CRUD-with-aggregation domain; the honest gap is the absence of a materialized stats rollup at scale.

### Code Evidence

| Claim | File |
| ------------------------------ | ------------------------------------------------------------------------------------------ |
| Create/read/stats/status | `apps/api/src/domains/feedback/application/services/feedback.service.ts` |
| Pure filter builder | `apps/api/src/domains/feedback/application/services/feedback-helpers.ts` |
| Enum parse helpers | `apps/api/src/domains/feedback/application/services/feedback-enum-parse.ts` |
| HTTP surface | `apps/api/src/domains/feedback/presentation/controllers/feedback.controller.ts` |
| Models | `packages/db/prisma/schema.prisma` (`Feedback`, `FeedbackFeature`, enums) |

### Interview Script (20 seconds)

> "Product feedback is normalized for aggregation: each good/bad/improvement mention is its own `FeedbackFeature` row, so 'what do clinics complain about most' is a real group-by rather than string matching, and the stats endpoint returns per-status counts, average rating, and the top feature lists for the product team's triage dashboard. Filters build through pure, testable helpers rather than inline Prisma conditionals, and a status workflow moves items from NEW to RESOLVED with admin notes."

---

## Domain 7: Users (Profile, Guided Tour, Deletion)

### Context

The `users` domain owns the *thin* user-facing edges that don't fit auth or a clinical domain: profile reads/updates, onboarding/guided-tour state, and account-deletion requests.

### Decisions

**D1 — Guided-tour state is user columns with terminal-state stamping.** `guidedTourStatus` (NOT_STARTED → … → COMPLETED/SKIPPED), `guidedTourLastStep`, `guidedTourCompletedAt`, `checklistDismissedAt` live on the user row. `GuidedTourService.updateGuidedTour` records the completion/skip timestamp when the state goes terminal so the client auto-start gate never fires again ("COMPLETED/SKIPPED are terminal — record when the tour ended").

**D2 — Profile updates are small and typed; deletion is a request, not a fire.** `users.service.ts` exposes `update` (onboardingStep), `updateProfile` (DTO-validated), `getProfile`, and `requestAccountDeletion` — deletion is *requested* (likely queued/human-reviewed), not executed inline, matching the audit-first posture of the rest of the product.

**D3 — A factory owns user creation shape.** `UserFactory.create(role, data)` builds the Prisma create input (connecting the clinic only when provided) so role+clinic wiring has one home instead of being repeated at call sites.

### Trade-offs

- **Guided-tour state on the user row couples UX state to identity** — a future "multiple products per user" would need to move tour state to a per-product table; fine for one product today.
- **Account deletion request lives here but the executor isn't visible in the domain** — the request boundary is clean; the actual deletion pipeline (GDPR/DPDP erasure, cascades) is elsewhere.

### What Worked / What Failed

Worked: terminal-state stamping fixed the "tour auto-restarts after completion" bug class; the factory keeps user creation consistent across roles. Failed: nothing notable — the domain's honest gap is that deletion-request is the visible half of a bigger erasure pipeline.

### Code Evidence

| Claim | File |
| --------------------------- | ------------------------------------------------------------------------------------------------------ |
| Profile/onboarding/deletion | `apps/api/src/domains/users/application/services/users.service.ts` |
| Guided-tour state machine | `apps/api/src/domains/users/application/services/guided-tour.service.ts` |
| User creation factory | `apps/api/src/domains/users/core/factories/user.factory.ts` |
| HTTP surface | `apps/api/src/domains/users/presentation/controllers/users.controller.ts`, `guided-tour.controller.ts` |
| User tour columns | `packages/db/prisma/schema.prisma` (`User`, `GuidedTourStatus`) |

### Interview Script (20 seconds)

> "The users domain handles the thin edges: profile updates, guided-tour state stored as user columns with terminal states (completed/skipped) timestamped so the tour never auto-restarts, a creation factory so role-and-clinic wiring has one home, and account deletion expressed as a request rather than an inline delete — consistent with the product's audit-first approach to sensitive operations."

---

## The Cross-Domain Lesson

Read together, these seven prove a cultural point worth making in an interview:

1. **Every cron that touches multiple tenants is RLS-bypassed deliberately and processes tenants as isolated batches** (reminders, and deep-dive 15/18's sweeps).
2. **Every two-write side effect is a transaction** — approve-leave + publish-time-off (leave), and deep-dive 13's ledger, 11's claims.
3. **Every send/event is deduplicated somewhere** — per-channel reminder rows, webhook replay claims, delivery idempotency keys.
4. **Every boundary is role/feature/tier-gated** — lab portal role gate, reminders `AUTO_REMINDERS` feature, template/doc access decorators.
5. **Time is always injected** (clock ports) so even a 670-LOC domain is testable.

---

## Code Evidence (domain-level index)

| Claim | File |
| ------------------------------- | ------------------------------------------------------------------------- |
| Reminders scheduler + settings | `apps/api/src/domains/reminders/application/services/` |
| Custom-field definitions | `apps/api/src/domains/custom-fields/` |
| Webhook verification/delivery | `apps/api/src/shared/modules/webhooks/`, `apps/api/src/domains/webhooks/` |
| Lab portal auth | `apps/api/src/domains/lab-portal/` |
| Leave + time-off publish | `apps/api/src/domains/leave/` |
| Feedback + aggregation | `apps/api/src/domains/feedback/` |
| Users + guided tour | `apps/api/src/domains/users/` |

---

## Interview Script (60 seconds — the long tail as one story)

> "Beyond the headline domains, seven smaller ones show the same engineering discipline. Appointment reminders are a push scheduler that scans per clinic with per-channel, per-type dedupe so a clinic's 30-minute WhatsApp nudge is never masked by an hourly email — and every WhatsApp send is gated on tier and the clinic's automation opt-out. Custom fields are a per-clinic definition table whose values ride patient `customData`. Webhooks get the trust treatment on both directions: HMAC verification with a 5-minute timestamp tolerance and replay dedupe inbound, signed deliveries with idempotency keys and retry state outbound. Leave approval is a transaction that publishes doctor time-off so a doctor on vacation stops being bookable. Feedback normalizes every mention into its own row so 'top complaints' is a real aggregate. And even the smallest domains — the lab portal's role-gated login, guided-tour terminal states — get clock-injected time and feature-gated controllers. If there's one theme, it's that side effects are transactional, sends are deduplicated, and every boundary is gated — at every size."

---
