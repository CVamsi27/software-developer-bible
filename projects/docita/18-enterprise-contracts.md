# 18 — Enterprise Contracts and Group Billing

[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

An enterprise contract records commercial terms for a group of member clinics. It sits above clinic subscriptions: the contract owns group terms, while each clinic still records which features it may access and how much it has used.

The difficult operation is changing membership without leaving a clinic on the wrong plan or billing the same agreement twice.

## First Principles

Group administration legitimately spans tenants, but cross-tenant access still needs an authorized actor and a bounded member set. A database bypass makes access possible; it does not establish permission.

Contract terms, effective membership and historical billing are different facts. Mutating today's terms must not silently rewrite what a past invoice represented, and leaving a group needs an explicit entitlement policy.

## Why Lifecycle, Invoices and Estimates Are Separate

| Component | Current responsibility |
| ------------------------- | ------------------------------------------------------ |
| Contract command service | Terms, status, membership and subscription overrides |
| Invoice command service | Annual prepay, setup fee and adjustment records |
| Query service | Contract views, revisions and current-period estimates |
| True-up service/scheduler | Threshold evaluation and internal alerts |

The separation makes financial writes and advisory calculations easier to reason about. It does not prove they use the same facts or that their outputs always agree.

## How Cross-clinic Administration Works

The inspected operations use `runUnrestricted` with explicit cross-clinic rationale. Member usage queries filter to the contract's active clinic IDs. This is useful visibility for code review; controller authorization, actual database-role behavior and member consistency remain part of the security boundary.

An authorized cross-clinic query can also be expressed through scoped policies or a privileged capability service. A bypass is not the only possible architecture, and a comment is not an audit trail or runtime authorization check.

Contract upsert validates date parsing and end after start. In one transaction it upserts the contract, activates primary-clinic membership, loads active members, updates their existing subscription rows and records a revision. The shared override builder maps ENTERPRISE plan, platform fee, currency, billing cycle and included appointments/users/storage.

The builder does not map every contract meter. Updating existing subscriptions also does not create missing ones or itself activate subscription status, extend periods or invalidate cached entitlements. Group inclusions and per-clinic allowances require a defined allocation policy; applying a whole-group amount to each clinic is not automatically correct group billing.

## Membership and Revision Boundaries

Adding a member checks clinic existence and rejects a membership row belonging to another contract, then transactionally updates membership, existing subscription fields and a revision. The preliminary check can race; unique membership identity prevents duplicate rows but does not alone prevent concurrent reassignment semantics.

Removing a member rejects removal of the primary clinic, sets removedAt by clinic ID and writes a revision afterward. The inspected method does not restore the clinic's previous subscription. It also does not include contractId in the member update predicate. The original statement that leaving automatically restores prior terms was incorrect.

SetStatus updates the contract and then records a revision in separate calls. There is no transition graph or expected-version predicate in that method. A later revision failure can leave a changed status without its corresponding history.

Revisions cover upsert, status and member changes—not only status changes. Upsert/status snapshots capture prior contract data; member add/remove snapshots are empty. They therefore do not preserve the complete pre-contract subscription state needed for an exact exit policy.

## Examples: Three Invoice Operations, Different Retry Semantics

| Operation | Current identity and calculation |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Annual prepay | ACTIVE contract; gross = monthly platform fee × 12; rounded percentage discount; deterministic contract/start-year invoice number |
| Setup fee | Rejects TERMINATED; fixed numeric minimum of 250000 minor units; deterministic contract invoice number |
| Adjustment | Rejects TERMINATED; new random-suffixed number and new records each call |

Prepay first looks for an existing annual invoice at the contract start date. Setup first looks for an existing setup invoice. Their transactions upsert a subscription payment by clinic/invoice number and an enterprise invoice by payment ID.

These keys reduce duplicate records, but the upsert update branches change amount, currency and metadata. They are not universal immutable no-ops. Concurrent calls with different terms need a contract version and frozen issuance policy. A random adjustment suffix reduces accidental identifier collision; it does not make a retried adjustment the same operation or guarantee collision impossibility.

Prepay always multiplies by twelve even if the supplied term length differs. Its number uses start year rather than a complete billing-period identity. Define term length, renewal, partial periods, first-year/absolute discounts and correction invoices before extending this mechanism.

The setup minimum's error message says INR, while contracts carry currency. A fixed number of minor units cannot be interpreted as the same commercial minimum in every currency. Retain minor-unit arithmetic with explicit currency and supported range/rounding policy.

## Estimates and True-up Measure Different Things

The live estimate combines completed appointment counts filtered by updatedAt, current user/doctor counts, and usageEvent quantities for WhatsApp, storage, prescriptions and invoices. It applies `max(0, used − included) × rate` per meter.

These measurements mix current quantities, such as user counts, with activity accumulated over a period, such as usage events. UpdatedAt is not necessarily consultation completion time. A storage usage-event sum is not automatically current occupied storage. The result called projectedMonthTotalCents adds current platform/support fees and observed overages; it does not estimate the rest of the month from the daily rate so far.

The calendar-month helper uses process-local dates and ends at 23:59:59, leaving fractional-second boundary concerns. Prefer an explicit timezone and half-open `[start, nextStart)` window.

True-up instead sums usageRecord overageChargeCents for currently active members since the later of contract start or local January 1. Its denominator is platform fee multiplied by calendar months counted, including the current month. It compares `(platform + overage) / platform` to the threshold; zero platform fee returns zero percent.

This year-to-date (YTD) metric compares charges against platform fees for the counted months. It does not directly compare them against the full annual commitment or guarantee a forecast. Membership changes, late usage aggregation, different currencies and the period definition affect its interpretation. The estimate and true-up do not simply consume one identical ledger/helper.

## Alerts Are Durable Records, Not Guaranteed Email

The configured scheduler runs daily at 03:15, subject to enablement and timezone. It scans a capped ACTIVE-contract set and logs individual settled-promise failures. A cap is not pagination or complete coverage; a heartbeat is not proof every evaluation succeeded.

Threshold evaluation looks for an alert since local month start before creating one. That check/create sequence alone does not enforce one alert under concurrent invocations. It persists an alert, then updates lastTrueUpAlertAt, then awaits email calls and logs failures. Failed email is not queued for retry by this method, and an existing monthly alert can suppress later attempts.

Alerting does not create an overage invoice. That is a useful commercial boundary: a threshold can prompt account review without automatically changing the customer's financial obligation.

## Current Assessment and Recommended Design

| Assessment | Concrete implication |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strengths | Explicit group scope, shared override mapping, transactional prepay/setup records, revisions and separate advisory alerting make important responsibilities visible. |
| Limitations | Removed members retain overwritten subscriptions; some changes/history are separate writes; retry identity and historical pricing are incomplete; estimate and true-up use different metric semantics. |
| Recommended design | Version contracts and effective membership; snapshot prior entitlements on entry; define exit restoration; enforce membership ownership and term updates conditionally in one transaction. |
| Financial records | Freeze issued pricing/period/currency; use stable operation keys plus request fingerprints; represent corrections explicitly rather than mutating issued invoices. |
| Metering and alerts | Define canonical meter facts and time windows; reconcile rollups; persist unique contract/period alert identity with durable notification jobs and paginated evaluation. |
| Acceptance evidence | Concurrent add/remove cannot alter another contract's membership; exit restores the approved policy; retried invoices preserve one frozen result; email failure retries without duplicate alerts; estimates reconcile to defined facts. |

This is the recommended target design, not existing production behavior. A run-rate forecast can be added as a separately labeled estimate with assumptions; it must not replace observed consumption or an issued invoice.

## Mistakes and Best Practices

Avoid claims of zero double bills, recovered historical plans or genuine over-commit customers without evidence. Test membership races, missing subscriptions, differing invoice payloads, term changes, mixed currencies, zero fees, late usage and concurrent alerts. Treat privileged cross-clinic access as a narrow authorized capability rather than a general bypass convenience.

## Code Evidence

Paths below are in the inspected Docita checkout.

| Mechanism | Source path |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Terms and membership | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contracts-command.service.ts` |
| Invoice keys and calculations | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contract-invoice-command.service.ts` |
| Live estimate | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contracts-query.service.ts` — estimateCurrentPeriod |
| Meter and month helper | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contracts-estimate.helpers.ts` |
| True-up metric and notifications | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contract-true-up-command.service.ts` |
| Scheduled scan | `apps/api/src/domains/enterprise-contracts/infrastructure/schedulers/enterprise-contract-trueup.scheduler.ts` |

## Summary

Group terms need versioned membership and an explicit entitlement exit policy. Distinguish retry-safe row identity from immutable financial issuance, observed estimates from forecasts, and recorded alerts from completed notification delivery.

## See Also

- [Category revision](REVISION.md) — enterprise billing and membership questions.
- [Subscription system](09-subscription-system.md) — entitlements and usage aggregation.
- [Billing and invoicing](08-billing-invoicing.md) — financial context and correction policy.
- [Analytics and dashboards](14-analytics-and-dashboards.md) — period and metric definitions.
- [Async processing](03-async-processing.md) — durable notifications.
- [Case-study index](INDEX.md) — reading order.
