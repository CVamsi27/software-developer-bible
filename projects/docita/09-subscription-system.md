# 09 — Subscription System

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

A subscription connects a clinic's paid plan and billing period to the features and usage allowances it can access. Payment state, feature entitlement and recorded consumption are related, but each answers a different question.

A failed renewal makes the distinction concrete: should staff lose access immediately, can an administrator still resolve billing, and what happens to work already accepted?

## First Principles

A payment provider and the application cannot change state in one database transaction. Notifications can arrive late or more than once. The application therefore needs its own subscription state, a policy for access while payment is unresolved, and a way to reconcile provider evidence.

Usage has a separate timing problem. Recording an action after it completes can support billing, but cannot prevent two concurrent requests from consuming the last available unit. A hard limit needs an atomic reservation before the expensive action.

## Why Entitlements Need Their Own Check

Authentication identifies the caller. Authorization decides whether that caller may operate on this clinic's resources. Entitlement decides whether the clinic's plan includes the feature. Paying for a feature never grants permission to read another clinic's data.

Keep prices and included quantities in the configured product catalog. A hard-coded price table in a case study quickly becomes misleading and does not explain enforcement.

## How a Route Declares Its Required Feature

The actual decorators are `@RequireFeature(...)` and `@RequireTier(...)`. They attach Nest metadata; the decorator itself does not query the subscription or reject the request.

```text
Route metadata → TierGuard → clinic auth snapshot
                              ↓
                 subscription/access policy
                              ↓
                    feature or tier check
                              ↓
                      route execution
```

`TierGuard` reads handler and class metadata. Routes with neither requirement return early. Session-guard bypass routes and internal users have explicit exceptions. A gated request without a clinic is rejected, and failure to load its clinic snapshot is rejected.

The guard checks billing hard-lock policy and subscription status before checking the feature. Its allowed-status set includes ACTIVE, TRIALING, PAST_DUE, GRACE and PAUSED; hard-lock rules can still restrict access. Billing administrators receive special treatment at the hard-lock step, which is not a blanket exemption from all entitlement checks.

A feature requirement takes precedence when both metadata values are present. Review route coverage and cache invalidation after plan changes; this source does not establish that every relevant route is gated or that stale entitlements are impossible.

## Subscription States Are a Graph

The source uses `GRACE`, not `GRACE_PERIOD`, and includes trial, pause and cancellation paths. It is not the single chain PENDING → ACTIVE → PAST_DUE → GRACE → EXPIRED.

| Starting state | Allowed transitions in the value object |
| -------------------- | ------------------------------------------- |
| TRIALING | ACTIVE, PAST_DUE, GRACE, CANCELLED, EXPIRED |
| ACTIVE | PAST_DUE, GRACE, PAUSED, CANCELLED, EXPIRED |
| PAST_DUE | ACTIVE, GRACE, CANCELLED, EXPIRED |
| GRACE | ACTIVE, CANCELLED, EXPIRED |
| PAUSED | ACTIVE, CANCELLED |
| CANCELLED or EXPIRED | ACTIVE |

The shared lockout helper adds ten calendar days with `Date.setDate`. This does not mean every caller traverses seven days of past due followed by three days of grace. Pending and halted webhook handlers use the shared deadline through their respective paths. A calendar-day calculation can differ from a fixed number of elapsed hours around daylight-saving changes.

Activation clears the grace deadline. However, `activatePaidPlan` directly assigns ACTIVE rather than calling the value object's transition method. Evaluate invariants across actual write paths, not only the transition table.

## Examples: Renewal Date and Usage Units

The entity supports monthly, quarterly, semiannual and yearly cycles. It can store a scheduled plan change with an effective date, so annual billing and deferred changes are existing mechanisms rather than absent future ideas.

A same-cycle mid-period upgrade can preserve the current period end through an explicit option. A lapsed renewal of the same plan and cycle uses a helper to retain a period anchor instead of necessarily starting the new period on the payment date. These are business policies: explain what time the payment buys and test late-payment boundaries.

Period-end calculations use JavaScript month/year setters. Month-end overflow and process timezone need explicit tests; adding one month to January 31 does not automatically implement an end-of-February billing policy.

Usage tracking records clinic, type, quantity and optional entity identity. When an entity ID exists, the command builds an event key from clinic, type, entity type and entity ID. The repository treats a uniqueness conflict as a duplicate. Calls without such identity do not get this deduplication mechanism.

For WhatsApp, weights are rounded upward: template 1 → 1 unit, session 0.5 → 1 unit, media 1.5 → 2 units. These are application usage units, not necessarily provider prices. AI credit costs come from shared configuration. Patient activity, appointments, prescriptions, invoices, consultations, OCR pages and API calls have tracking entry points; their existence does not prove every business path invokes them.

## Daily Aggregation and Monthly Billing Are Separate

| Process | Source schedule | Purpose |
| ----------------------------- | --------------- | ------------------------------ |
| Billing usage aggregation | `30 0 * * *` | Roll up yesterday's usage |
| Usage threshold notifications | `30 * * * *` | Evaluate warnings hourly |
| Monthly overage billing | `0 2 1 * *` | Process the previous UTC month |

These are configured cron expressions, subject to process enablement and timezone configuration. They are not a promise that every deployment runs the job successfully.

The daily aggregation service currently rolls up WhatsApp and AI usage. It sums yesterday's events, selects add-on allowances for the plan, and writes a record keyed by clinic, type and calendar month. Its day and month boundaries use local `Date` operations, whereas the monthly billing scheduler obtains the previous UTC month.

The repository increments quantity when the monthly record exists. Rerunning the same day can therefore add it again; an upsert alone does not make aggregation idempotent. On update it does not refresh included quota or overage units. Those stored fields must not be assumed to reflect the current cumulative quantity automatically.

A safer design gives each daily contribution a unique period identity or recomputes an authoritative total with a defined watermark. Include late events, plan changes, reruns and timezone alignment in that policy.

Monthly billing scans ACTIVE and TRIALING subscriptions, then invokes a separate overage meter. It uses a capped read and per-subscription settled promises; logged failures and a fulfilled outer cron call are not proof that every subscription was billed. Pagination, retry evidence and period-specific invoice identity matter.

## Real-world Decisions: Grace, Quotas and Referrals

Grace can preserve continuity while billing is resolved, but define exactly which actions remain available. Administrator access, patient-data access and new costly operations need distinct rules. Access restriction and data-retention policy are separate; a status transition does not prove records will be retained indefinitely.

Use post-action usage events for accounting when temporary overshoot is acceptable. For a hard limit, reserve units atomically in the tenant's period, perform the operation, then settle or release the reservation. Stable operation identity must cover retries without double charging or losing legitimately repeated work.

Referrals have two source paths: partner codes and legacy clinic-to-clinic codes. Signup capture links the clinic; first successful payment invokes a separate conversion-credit service. A discount lookup clamps the percentage and caps the result at the amount. Referral capture and realization catch failures so completed onboarding or activation can continue. That continuity requires reconciliation: logging a failure does not eventually award the missing reward.

Do not infer acquisition performance, retention improvement or zero feature leakage from these classes. Such claims require measurements and tests beyond source inspection.

## Mistakes and Best Practices

- Treating a decorator as enforcement: verify the guard is installed and the relevant routes carry metadata.
- Treating a usage event as a quota lock: reserve atomically when concurrent overshoot is unacceptable.
- Treating an upsert as retry safety: inspect whether it replaces an authoritative total or increments a contribution again.
- Treating a state table as universal enforcement: trace direct writes and provider handlers too.
- Treating a successful cron invocation as complete billing: record individual failures, pagination coverage and rerun identity.

Test tenant scope, stale caches, duplicate provider events, out-of-order state changes, month-end periods, partial aggregation failures and repeated billing for the same period.

## Code Evidence

Paths below are in the Docita checkout and describe inspected source, not verified production outcomes.

| Mechanism | Source path |
| ---------------------------- | ------------------------------------------------------------------------------------------- |
| Route requirements and guard | `apps/api/src/shared/modules/auth/auth/tier.decorator.ts` and `tier.guard.ts` |
| Lifecycle and period policy | `apps/api/src/domains/subscriptions/core/entities/subscription.entity.ts` |
| Transition graph | `apps/api/src/domains/subscriptions/core/value-objects/subscription-status.value-object.ts` |
| Grace calculation | `apps/api/src/domains/subscriptions/core/constants/subscription-lockout.constants.ts` |
| Usage identity and units | `apps/api/src/domains/billing/core/services/usage-tracking-command.service.ts` |
| Daily aggregation | `apps/api/src/domains/billing/core/services/usage-aggregation.service.ts` |
| Aggregate update semantics | `apps/api/src/domains/billing/infrastructure/repositories/prisma-usage.repository.ts` |
| Schedule definitions | `apps/api/src/shared/schedule/cron-schedules.ts` |
| Monthly billing | `apps/api/src/domains/subscriptions/infrastructure/schedulers/overage-billing.scheduler.ts` |
| Referral orchestration | `apps/api/src/domains/subscriptions/core/services/referral.service.ts` |

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Route metadata, lifecycle policy and usage identity separate key SaaS responsibilities. |
| Current limitations | Daily increments are not rerun-safe, entitlement caches can lag, and accounting is not hard quota enforcement. |
| Recommended design | Maintain versioned entitlement snapshots, reserve hard quotas atomically, aggregate with unique period contributions or authoritative totals, and bill once per clinic/period with recoverable provider reconciliation. |
| Evidence needed | Parallel last-unit consumption has one winner; reruns preserve totals; duplicate renewal events preserve one period effect; plan changes invalidate relevant access snapshots. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Separate caller permission, clinic entitlement, usage accounting and provider payment state. Explain the actual guard and lifecycle paths, then verify retry-safe aggregation and billing independently. Preserve access deliberately during grace; do not infer correctness or retention from the existence of a state machine.

## See Also

- [Category revision](REVISION.md) — subscription questions and recall.
- [Payment flows](04-payment-flows.md) — provider evidence and acknowledgments.
- [Async processing](03-async-processing.md) — delivery and retry boundaries.
- [Billing and invoicing](08-billing-invoicing.md) — financial state and historical context.
- [Case-study index](INDEX.md) — reading order.
