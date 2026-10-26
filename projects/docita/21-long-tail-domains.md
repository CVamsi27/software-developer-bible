# 21 — Smaller Domains: Automation, Trust and Reversible State

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



These features are smaller than billing or appointments, but an incorrect tenant selection can disclose clinical data and an incomplete reversal can leave a doctor unavailable. Source inspection establishes implemented behavior; it does not establish production outcomes.

## Definition

The long tail covers reminders, custom fields, inbound/outbound webhooks, lab login, staff leave, product feedback and user lifecycle. Read each through its boundary: what is authorized, what changes, what can race, and what proves completion.

> **Textbook Definition:** Cross-cutting workflow analysis evaluates authorization, state transitions, concurrency and recovery across smaller capabilities that share infrastructure but retain distinct business rules.

## First Principles

Reading “not sent” before sending does not reserve the right to send. A transaction can couple writes without preventing two callers from passing the same earlier check. An enum defines available labels without defining permitted transitions. Authentication establishes identity, while resource authorization establishes what that identity may access.

Those constraints explain the recurring design needs: tenant-qualified operations, stable operation identities, conditional state changes and recoverable side effects.

## Reminders: A Scan Window Is Not a Durable Job

The hourly scheduler reads enabled settings with a clinic ID under explicit unrestricted database access, then scans each clinic for SCHEDULED/CONFIRMED appointments between now and its configured horizon. The shorter WhatsApp pass searches appointments 25–35 minutes ahead. Both use allSettled to isolate failures; this fan-out is not a concurrency limit.

Previously sent reminder rows suppress the corresponding channel/type. An hourly email does not suppress whatsapp_30min. WhatsApp sends also consult the clinic automation policy. A manual send-now route supports staff-triggered reminders, while settings provide defaults for callers requesting them. The scheduler itself scans persisted enabled settings; a default returned by a settings service does not enroll every clinic automatically.

```text
Read eligible appointments → read sent history → send → record outcome
                             ↑
                  Another runner can read the same absence
```

History improves sequential deduplication, but does not atomically claim a send. Provider acceptance followed by a failed history write can permit another send. A skipped tick only recovers while the appointment remains in its window; the ten-minute short window is not an indefinite retry queue. Database-auth errors set a process latch that suppresses subsequent runs, so recovery/reset and meaningful heartbeat interpretation need an explicit operational policy.

**Recommended design:** persist one tenant-qualified intent per appointment version, channel and reminder type; atomically claim due work, track attempts and provider receipts, and expire obsolete work after rescheduling/cancellation. Bound concurrency and alert on overdue work and disabled scans.

## Custom Fields: Definitions and Values Need a Shared Contract

Definitions store name, field type, select options, required/order settings and nullable clinic ownership. Patient values live in customData JSON. This keeps intake extensible without adding a Patient column for every clinic request.

CustomFieldsService accepts an optional clinic ID. findOne checks ownership when that argument is supplied; update/remove pre-read and then write by ID. This is not structurally mandatory tenant qualification. Callers, database policy and platform-default permissions must enforce the missing boundary.

Definition CRUD does not itself prove that every patient write validates value types, required keys or definition ownership. Renaming/deleting a definition also needs a historical-value policy; the effects depend on the actual JSON key convention, not merely the displayed name.

**Recommended design:** identify definitions by stable IDs and versions, validate values against the authorized clinic schema at the server boundary, and define retirement/migration rules. Require explicit tenant scope or an explicit platform operation in repository methods.

## Inbound Webhooks: Authentication, Freshness and Completion Differ

The shared verifier supports a hash-based message authentication code (HMAC) over the raw body, or authentication through a shared-secret header. It rejects requests when no secret is configured and compares secrets/signatures safely. Before returning success, it records a replay hash in the database for ten minutes so another request with the same hash can be rejected during that window.

A five-minute freshness check applies only when a finite timestamp is provided. Generic HMAC covers the raw body; a separately supplied timestamp is not automatically covered by that MAC. Provider adapters must establish the authentic timestamp contract. Absence of a timestamp does not imply rejection by this generic helper.

The replay claim means “accepted within this window,” not “business processing completed.” A crash after claiming can suppress a retry until expiry; a later replay can be accepted again. Durable business idempotency must outlive transport replay protection. Error/audit persistence assists diagnosis, but hashing a payload alone is not proof that every log field is free of sensitive data.

**Recommended design:** verify the provider-specific signed representation, persist an authenticated inbox with event identity and processing state, acknowledge according to the delivery contract, and retry failed processing under durable business idempotency. Apply deliberate data minimization to logs and retained evidence.

## Outbound Webhooks: The Current Retry Path Is Incomplete

Dispatch creates delivery rows for active subscriptions and persists a payload with an event UUID. The repository selects subscriptions by eventName and active status, without a clinic predicate. The caller supplies an event clinic ID, but that does not filter recipients. This is a concrete cross-tenant fan-out risk in the inspected path; the review does not prove an actual disclosure occurred.

The key subscriptionId:aggregateId:timestamp suppresses a repeated key, but omits eventName and does not survive changed timestamps as the same operation. A fresh UUID is generated on dispatch. Stable logical identity and payload fingerprints should distinguish a retry from a different event.

The repository claims PENDING/FAILED rows using one UPDATE with FOR UPDATE SKIP LOCKED and increments attemptCount. That is a useful atomic claim. The rest of the inspected tick does not complete the reliability contract:

| Current behavior | Consequence |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| tick passes the literal resolved-from-subscription as signingSecret | Retry signatures do not use the stored subscriber secret |
| Failed send calls markFailed, which only changes error/status-code fields | The row remains IN_FLIGHT and is excluded from later pending claims |
| Computed backoff appears only in the error text | No scheduledAt update establishes that retry delay |
| No ownership lease/recovery appears in this claim/finalize path | A crashed worker can leave an unreclaimed in-flight delivery |
| Success is recorded as HTTP 200 | The actual successful response code is lost |

sendDelivery applies a timeout and signs the serialized payload, but does not itself enforce a destination allowlist or safe egress policy. Subscription validation and deployment egress controls need separate verification. allSettled and logged creation failures also do not guarantee every required subscriber received durable work.

**Recommended design:** filter subscriptions by authoritative event clinic, commit delivery intent with the event, freeze its payload and logical ID, load/version the real secret securely, and validate destinations. Claim with a lease/ownership token; conditionally finalize DELIVERED, retryable FAILED with scheduledAt, or DEAD_LETTERED. Preserve actual response evidence, recover expired leases and support deliberate replay.

## Lab Login: Role Checking Is the Entry Boundary

The lab login service validates credentials, requires Role.LAB, and delegates successful login to the shared session service. This avoids a second session implementation and prevents non-LAB users from entering this particular login surface.

It does not prove that a LAB session cannot call staff endpoints. Every worklist, upload and result endpoint still needs clinic/lab/order authorization. The inspected lab-portal domain is an authentication scaffold, not evidence of a complete isolated partner workflow.

**Recommended design:** provision approved lab identities, scope assigned work and uploads explicitly, and test both allowed access and attempts to access another clinic, patient or order. Reuse authentication while defining the lab resource policy separately.

## Leave: Coupled Writes Still Need Conditional Transitions

Plans are unique by clinic/type and record quotas and carry-forward settings. The balance query selects current-year starts, sums inclusive calendar duration for APPROVED and PENDING requests, and computes remaining from annual quota minus approved days. It does not apply stored carry-forward settings, working-day calendars or year-boundary splitting.

Approval checks clinic ownership, blocks self-approval and requires PENDING. Doctor approval writes availability time-off and APPROVED state using the transaction handle. This usefully couples the two writes on success/rollback.

However, the status re-read calls findLeaveById without the transaction handle, and the final update is by ID rather than a conditional PENDING/version predicate. Re-reading does not establish exclusive transition ownership. Approval, rejection and cancellation can race; a transaction alone is not proof that stale actions are impossible.

Cancellation first changes leave state, then separately finds/deletes time-off rows and logs failures. A crash can leave cancelled leave with blocked slots. Explicit leave-to-time-off linkage is safer than reconstructing ownership from a date range. Rejection also stamps approvedAt, which conflates decision timestamps.

**Recommended design:** conditionally own each transition, link time-off to leave identity, and atomically apply/reverse both states or persist recoverable reversal work. Define calendar, timezone, cross-year and carry-forward rules with examples; name decision timestamps by their actual meaning.

## Feedback: Labels Are Not a Transition Workflow

Feedback stores ratings/comments and normalized GOOD/BAD/IMPROVEMENT feature rows for aggregation. Pure filter and enum helpers keep parsing and query construction inspectable. These are useful foundations for product triage.

updateStatus parses an enum and writes the requested status. It does not enforce a NEW → REVIEWED → IN_PROGRESS → RESOLVED → ARCHIVED transition graph. Optional clinic arguments also mean callers must establish scope explicitly. The thirty-day recent-feedback query is a read predicate; it is not itself an atomic submission throttle.

Stats are computed from current queries, without evidence here of a consistent snapshot or materialized rollup. Add caching only when measured load justifies it, rather than inventing a scale problem.

**Recommended design:** decide whether arbitrary labels or enforced transitions are intended, qualify tenant operations, retain decision history where needed and make any submission-window enforcement atomic. Define the snapshot/freshness semantics of displayed aggregates.

## Users: Deletion Starts With Immediate State Changes

Profile/onboarding and guided-tour state live on the user. GuidedTourService stamps COMPLETED/SKIPPED and checklist dismissal using an injected clock, but directly accepts requested status changes; terminal-state naming does not itself prevent a later update from reopening the tour.

Account deletion is more than a request: the repository soft-deletes the user and sets appLoginDisabled immediately, preserving an earlier deletedAt. For clinic users it then creates a DataSubjectRequest; platform users have no such clinic-bound queue row. These are separate writes, so failure can disable the account without creating its request, and repeating the call can create additional requests.

The response promises erasure within thirty days, but that message does not prove the executor, retention exceptions, object removal, session revocation or completion. Inspect those mechanisms before claiming an erasure guarantee or regulatory compliance.

**Recommended design:** atomically record an idempotent request and disablement, revoke existing sessions according to policy, and track a recoverable lifecycle through authorized retention/anonymization/erasure tasks and completion evidence. Enforce tour transitions only if reopening is actually forbidden; otherwise document restart behavior.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Type-scoped reminder history, shared authentication, normalized feedback, replay claims, atomic delivery claims and coupled leave writes offer useful foundations. |
| Highest-priority gaps | Outbound recipient tenant selection, placeholder retry signing and stranded IN_FLIGHT failures deserve attention before advertising reliable tenant-safe delivery. |
| Other gaps | Reminder claims, leave reversals/transitions, optional tenant arguments and deletion-request atomicity need explicit invariants and recovery. |
| Recommended order | Fix trust and tenant boundaries first; then own state transitions and durable side effects; then improve policy semantics and measured operations. |
| Acceptance evidence | Cross-tenant fan-out is rejected; real-secret retry signatures verify; failure/crash recovers; concurrent reminder/leave/deletion operations preserve one authorized effect and durable completion state. |

These are source-backed assessments and proposed improvements, not application fixes delivered by this documentation change. Avoid invented outage stories, zero-complaint claims and universal statements about clocks, gating or transactions.

## Code Evidence

Paths refer to the inspected Docita checkout.

| Mechanism | Source path |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reminder windows/history | `apps/api/src/domains/reminders/application/services/reminder-scheduler.service.ts` |
| Reminder send/settings | `apps/api/src/domains/reminders/application/services/reminder-notification.service.ts` and `reminder-settings.service.ts` |
| Definition scope | `apps/api/src/domains/custom-fields/application/services/custom-fields.service.ts` |
| Inbound authentication/replay | `apps/api/src/shared/modules/webhooks/webhook-verifier.ts` and `webhook-replay-dedupe.repository.ts` |
| Outbound tenant selection and retry writes | `apps/api/src/shared/modules/webhooks/outgoing/outgoing-webhook.repository.ts` |
| Outbound signing and tick | `apps/api/src/shared/modules/webhooks/outgoing/outgoing-webhook.service.ts` |
| Lab role check | `apps/api/src/domains/lab-portal/application/services/lab-portal-auth.service.ts` |
| Leave transitions/balance | `apps/api/src/domains/leave/application/services/leave-command.service.ts` and `leave-query.service.ts` |
| Feedback labels and recent query | `apps/api/src/domains/feedback/application/services/feedback.service.ts` |
| Tour/profile/deletion | `apps/api/src/domains/users/application/services/guided-tour.service.ts`, `users.service.ts` and `infrastructure/repositories/prisma-user.repository.ts` |

## Summary

Small features need the same explicit boundaries as headline domains. Explain current guarantees narrowly, trace concurrency and failure paths, and propose tenant-qualified, conditionally owned and recoverable operations with acceptance evidence.

## See Also

- [Category revision](REVISION.md) — source-linked questions for each domain.
- [Async processing](03-async-processing.md) — claims, leases and durable intent.
- [Clinical lab and coding](20-clinical-lab-and-medical-coding.md) — lab release and notification.
- [Doctor availability](15-doctors-verification-and-public-booking.md) — schedule ownership.
- [Case-study index](INDEX.md) — reading stages.

---

[← Previous: Lab Release and Medical Code Catalogs](20-clinical-lab-and-medical-coding.md) · [Back to Index](INDEX.md) · [Next: What I'd Do Differently →](22-what-id-do-differently.md)
