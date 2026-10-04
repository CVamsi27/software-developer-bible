# 06 — WhatsApp Integration

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

WhatsApp integration connects clinic actions to outbound messages and connects incoming provider events to local delivery records or patient responses. A send request and a delivery receipt are separate events.

Consider a reminder that the provider accepts but the patient never receives. The application needs to retain the provider message ID, process later status events, and show unresolved delivery honestly.

## First Principles

The provider cannot commit atomically with the clinic database. Sending first can leave a delivered message without a local record if persistence fails; recording first can leave an unsent message if dispatch fails. Retries require stable identity and a defined recovery path.

Incoming replies introduce another boundary: a phone number and free text do not necessarily identify one patient appointment. Tenant, sender, conversation and reply context must be resolved before changing clinical workflow state.

## Why Sender Identity Matters

The application supports three sender configurations: SHARED uses the platform sender, BYO means bring your own clinic sender, and MANAGED uses managed clinic sender configuration. These modes do not guarantee provider pricing, number ownership or branding.

| Mode | Source behavior |
| ----------------------------- | ------------------------------------------------------------------- |
| SHARED | Uses the platform's configured Meta phone-number ID and token |
| BYO or MANAGED | Uses verified clinic sender configuration and its encrypted token |
| Non-shared sender unavailable | Falls back to shared when verification, number or secret is missing |

The resolver marks those fallback cases with `fallbackActive`. Decryption failure is not explicitly caught by this resolver. Do not assume every credential failure falls back safely.

Shared text is prefixed with the clinic display name. That helps patients recognize the clinic, but it does not grant authorization or prove that a configured number belongs to the clinic. Product policy must decide whether silently changing sender identity is acceptable and whether staff need a visible warning.

## How Sending and Status Updates Fit Together

```text
Clinic operation → entitlement check → sender/template resolution
                                            ↓
                                     provider send
                                            ↓
                              persist provider ID locally
                                            ↓
                                 emit usage/telemetry

Provider status webhook → locate local record → update delivery state
```

`SendMessageUseCase` loads clinic context and checks WhatsApp entitlement. It then calls the delivery service before ensuring the conversation and saving a message. Finally, it emits a local message-sent event for usage and telemetry.

That order has a failure boundary: provider acceptance followed by database failure can lose local correlation. Retrying the operation can send another message. A provider ID alone does not eliminate the gap; use a durable dispatch operation and an explicit ambiguous-send reconciliation policy.

The delivery service resolves an approved Meta template when production mode and a template ID are present. Other branches can send interactive buttons or text. Their existence does not prove that a fallback is permitted for every recipient at that moment.

WhatsApp policy requires approved templates to initiate conversations and outside the 24-hour customer-service window. Free-form replies are permitted within the window, which resets with each user message. Opt-in and opt-out requirements also apply. Validate eligibility before sending a fallback; template rejection is not permission to send unrestricted text. [WhatsApp Business Messaging Policy](https://whatsappbusiness.com/policy/).

The inspected ingress maps provider status values to local sent, delivered, read and failed states. It updates legacy logs, domain messages and the support inbox through separate calls. These stores can diverge when a call fails. Legacy status assignment is not protected by a monotonic ordering rule, so delayed events can overwrite newer status; retain event time and define reconciliation across representations.

## Examples: A Two-step Delay Reply

The parser supports CONFIRM, ON_THE_WAY, DELAY, RESCHEDULE, CANCEL and UNKNOWN. Exact button IDs and normalized words are checked first, followed by ordered substring patterns. Delay minutes are extracted separately and accepted only from 1 to 240.

A focused supported trace is:

1. Patient replies `delay`; it maps to DELAY with no minutes.
2. The handler stores a pending delay response and requests the missing duration.
3. Patient replies `30`; the duration parser returns 30 and the response parser returns UNKNOWN.
4. A recent pending DELAY response for that appointment lets the handler interpret this as the requested duration.
5. The handler updates that response, evaluates a possible scheduling conflict, then sends confirmation and staff notification.

The pending lookup uses a six-hour window and the latest DELAY response without minutes. It is scoped to appointment ID; it does not itself prove a reply belongs to that conversational turn. A number can also be a menu choice: exact `1` maps to CONFIRM rather than a delay follow-up. Define how interactive context disambiguates such inputs.

Substring parsing can misread negation: `do not cancel` contains `cancel`. The phrase `delay 30 min` is not equivalent to the exact token `delay`, and the current includes list contains `delayed` rather than `delay`. Extracting 30 minutes does not automatically make the response type DELAY.

Prefer explicit button IDs for consequential actions, retain UNKNOWN for uncertain text, and test supported languages and negation. Do not claim a parsing accuracy percentage without a labeled evaluation set. Adding an AI parser would still require confirmation, tenant context and safe fallback for ambiguous output.

## Appointment Updates and Delay Warnings

For mapped actions, the handler uses `updateMany` with the current database status in an allowed-predecessor set. This conditional write protects against canceling a completed or in-progress visit through that path, even when the earlier appointment snapshot is stale.

DELAY does not directly reschedule the appointment in this mapping. Its conflict check computes expected arrival and compares it to the next qualifying appointment's start time for the same clinic and doctor. It is a warning heuristic, not the complete overlap check: duration, staff capacity and other visits can matter. A delay request should not promise a newly reserved slot.

The response record, status update, patient confirmation and staff notification occur in separate operations. Partial completion is possible. In particular, the handler can send a confirmation after a status update affected zero rows. Make the response outcome explicit rather than treating parsing success as workflow success.

## Real-world Decisions: Duplicate Ingress and Missing Receipts

Incoming provider-event handling prefers interactive button IDs over display text. It records a clinic conversation message, then resolves the related appointment and delegates response handling.

The conversation transaction checks for an existing inbound ID and upserts the message. Sequential duplicates can skip downstream processing, but conversation unread count is incremented before the duplicate check. Two concurrent transactions can also both observe absence before upserting. A check followed by an upsert does not prove exactly-once effects.

There is a second gap: if the message is recorded and downstream handling fails, a subsequent delivery can be treated as already processed. Durable ingress needs separate received and processed states, with retryable work and a stable operation key. Provider receipt persistence and business-effect completion are different facts.

When clinic resolution fails, the recording helper logs a quarantine message and returns true; the caller still proceeds to appointment resolution. Trace that resolver and its tenant/identity rules before claiming unresolved messages cannot reach clinical actions.

The actual reconciliation cron runs hourly at minute 45. Its service groups non-final outbound records older than six hours, logs counts and emits an alert event. It does not poll a provider status endpoint, change those records to FAILED, repair missing receipts or resend them.

Expose unresolved delivery separately from confirmed failure. Alerting improves visibility; automatic resend can duplicate a message that was delivered while its receipt was lost.

## Mistakes and Best Practices

- Calling provider acceptance delivery: retain distinct states and the external message ID.
- Claiming a fixed per-clinic limit or exponential retry without tracing dispatch and client behavior: limits can apply to shared sender capacity as well as tenants.
- Treating a recorded inbound ID as completed business processing: persist processing state and make recovery explicit.
- Treating text parsing as patient authorization: resolve tenant, contact and appointment context first.
- Logging raw patient replies unnecessarily: the current response handler logs reply text, so masking phone numbers elsewhere does not establish privacy-safe logging.

Test concurrent duplicate ingress, failures between each effect, stale appointment status, negated commands, ambiguous numeric replies, sender fallback and out-of-order receipts. Preserve staff escalation when automation cannot safely choose an action.

## Code Evidence

Paths are from the inspected Docita checkout, not evidence of production message volume or delivery success.

| Mechanism | Source path |
| ------------------------------------- | ----------------------------------------------------------------------------------------- |
| Entitlement and send order | `apps/api/src/domains/whatsapp/application/use-cases/send-message.use-case.ts` |
| Sender credentials and fallback | `apps/api/src/domains/whatsapp/application/services/whatsapp-sender-resolver.service.ts` |
| Template and text dispatch | `apps/api/src/domains/whatsapp/application/services/whatsapp-message-delivery.service.ts` |
| Inbound recording and statuses | `apps/api/src/domains/whatsapp/application/services/whatsapp-webhook-ingress.service.ts` |
| Reply parsing | `apps/api/src/domains/whatsapp/application/services/patient-response-parser.helper.ts` |
| Response mappings | `apps/api/src/domains/whatsapp/application/policies/patient-response.policy.ts` |
| Delay handling and conditional update | `apps/api/src/domains/whatsapp/application/services/response-handler.service.ts` |
| Stale delivery telemetry | `apps/api/src/domains/whatsapp/application/services/whatsapp-reconciliation.service.ts` |
| Cron expression | `apps/api/src/shared/schedule/cron-schedules.ts` |

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Current strengths | Sender resolution, structured button mappings and stale-delivery telemetry make communication traceable. |
| Current limitations | Send-before-save, incomplete processing identity and ambiguous free text leave duplicate and partial-effect risks. |
| Recommended design | Use a durable outbound operation and inbound inbox with separate receipt/processing state; resolve tenant and conversation context before effects; require confirmation for ambiguous consequential replies. |
| Evidence needed | Concurrent duplicates and crashes between effects are recoverable; unknown tenant messages cannot change appointments; UI distinguishes accepted, delivered, failed and unresolved. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Trace the provider send, local database write, webhook receipt and business processing as separate steps. Stable identity helps retries but does not close every failure gap. Determine which conversation and appointment a reply belongs to before acting. Describe the stale-delivery sweep as status monitoring rather than recovery of delivery status.

## See Also

- [Category revision](REVISION.md) — messaging questions and recall.
- [Async processing](03-async-processing.md) — retries and durable effects.
- [Clinic workflows](05-clinic-workflows.md) — status and scheduling boundaries.
- [Subscription system](09-subscription-system.md) — entitlement and usage units.
- [Case-study index](INDEX.md) — reading order.

## References

- [WhatsApp Business Messaging Policy](https://whatsappbusiness.com/policy/) — templates, service window and consent requirements.
