# 19 — Enterprise Contracts

> The group-deal layer above subscriptions: one contract with N member clinics, annual prepay with discounts, setup fees, live per-member overage tracking, and a true-up cron that tells the sales team when a customer is burning past their commit.

---

## Context

Docita's largest customers are **groups** — a chain of clinics, a hospital group, a franchise — that want one commercial agreement covering many member clinics. The self-serve subscription (deep-dive 09) assumes one clinic, one tier, one bill. Enterprise deals break that model:

- **One contract, many member clinics**, each with its own usage but covered by a shared commit.
- **Commit-based pricing** — `platformFeeCents` (monthly platform fee), `includedConsultations/users/storageGB/doctors/prescriptions/invoices/WhatsApp`, plus per-meter **overage rates** for each dimension.
- **Annual prepay** — a customer pays 12× the platform fee up front, usually at a discount (`annualPrepayDiscountPercent`).
- **Setup fees** — an onboarding charge with a floor (INR 2,500).
- **True-up risk** — if a customer's usage (or the overage charges they'd incur) crosses a threshold of their annual commit, finance wants to *know now*, not discover it at renewal.
- **Custom adjustment invoices** — mid-contract one-off charges (extra seats, training).

**The problems:** (1) enterprise data is *cross-clinic by design* — a contract spans member clinics, so every query breaks the one-clinic RLS rule and needs an explicit, deliberate bypass; (2) the same clinic can have a self-serve subscription *and* be a contract member — the two must not fight (subscription fields must be overwritten consistently); (3) invoice generation must be idempotent (double-click / cron + manual overlap); (4) overage truth lives in the billing/subscriptions usage ledger that *other* domains write — enterprise must aggregate it without owning it; (5) the money math (discount %, YTD proration, overage aggregation) must be correct or the company loses margin silently.

---

## Decision 1: `runUnrestricted` as an Explicit, Named Cross-Clinic Escape Hatch

### What We Chose

Every enterprise-contracts read and write runs inside `persistence.runUnrestricted(...)`, with a comment at each call site stating *why* the bypass is legitimate:

```typescript
// RLS-BYPASS: enterprise contract administration spans member clinics by design
return this.persistence.runUnrestricted(async () => {
  const contract = await this.persistence.enterpriseContract.findUnique({ where: { id: contractId } });
  ...
});
```

### Why This Was Chosen

- **The domain's subject is the contract, not a clinic** — RLS scopes by clinicId, but a contract's members list and usage aggregation *necessarily* cross clinics. Denying the bypass would force N sequential single-clinic queries with manual merging — slower *and* more error-prone.
- **The bypass is named and reviewed, not hidden** — a bare `$queryRawUnsafe` or a Prisma client swap would be invisible; `runUnrestricted` plus the `RLS-BYPASS` comment makes every cross-clinic access auditable in review.
- **Usage aggregation stays correct** — the true-up `usageRecord.aggregate` filters `clinicId IN (members)`; running it unrestricted is the *only* way to sum YTD overage across the group without per-clinic round trips.

### Trade-offs

- **The escape hatch is load-bearing** — if a future refactor moved a query out of `runUnrestricted`, it would silently return partial data (RLS drops non-member rows) rather than failing. The domain relies on discipline: every method that touches `enterpriseContract*` or aggregates `usageRecord` by member list must be wrapped.
- **Audit/review burden** — each call site needs the "why" to stay honest; a contract query that could be scoped to one clinic should not hide behind the bypass.

---

## Decision 2: Subscription Overrides Are Built in One Place

### What We Chose

Whenever a clinic joins (or stays on) an enterprise contract, the code applies `buildEnterpriseSubscriptionOverrides` — a single function producing the exact field mapping (`plan: ENTERPRISE`, `basePriceCents`, `billingCycle`, `includedAppointments/Users/StorageGB`, ...). Both `upsert` (re-syncing *all* members) and `addMember` (syncing one) call it so members can never drift out of sync with their contract terms:

```typescript
// enterprise-contracts-command.service.ts
private buildEnterpriseSubscriptionOverrides(contract) {
  return {
    plan: ClinicTier.ENTERPRISE,
    basePriceCents: contract.platformFeeCents,
    billingCycle: contract.billingCycle,
    includedAppointments: contract.includedConsultations,
    includedUsers: contract.includedUsers,
    includedStorageGB: contract.includedStorageGB, ...
  };
}
```

### Why This Was Chosen

- **The mapping is the contract's own invariant** — if upsert and addMember applied different mappings, a member added later could end up on different terms than the group. One builder = one truth.
- **Enterprise membership *is* the subscription** — rather than a parallel billing system, a member clinic's existing subscription row is overwritten to ENTERPRISE terms; the overage machinery (deep-dive 09) then just works against contract inclusions.

### Trade-offs

- **Overwriting self-serve subscriptions is destructive by design** — when a clinic leaves the contract (`removeMember`), its subscription must be *restored* to whatever it was before; the codebase has to reconstruct prior terms (the revisions table helps — see below), and a lost pre-contract plan is a real support risk.
- **Contract inclusions and subscription inclusions are two vocabularies for the same thing** (`includedConsultations` vs `includedAppointments`) — the builder is where they meet; a typo here misbills a whole group.

---

## Decision 3: Idempotent Invoice Generation (Three Kinds, Three Rules)

### What We Chose

`EnterpriseContractInvoiceCommandService` exposes exactly three generators, each idempotent in its own way:

1. **Annual prepay** (`ENT-PREPAY-{contractNumber}-{year}`): guards on `status === ACTIVE`, looks up an existing invoice of kind `ANNUAL_PREPAY` for the same `periodStart` (returns it if present), computes `gross = platformFeeCents × 12`, `discount = round(gross × discountPercent / 100)`, `net = gross − discount`, then inside one transaction upserts a `subscriptionPayment` (keyed `clinicId + invoiceNumber`) and the invoice (keyed `subscriptionPaymentId`), and records the math breakdown (`{ grossCents, discountCents, netCents }`) in invoice `metadata`.
2. **Setup fee** (`ENT-SETUP-{contractNumber}`): blocks TERMINATED contracts and setup fees below the INR 2,500 floor; dedupes by kind.
3. **Adjustment** (`ENT-ADJ-{contractNumber}-{nanoid(8)}`): a true create (each adjustment is unique by definition — a fresh nanoid makes the invoice number collision-proof).

```typescript
const invoiceNumber = `ENT-PREPAY-${contract.contractNumber}-${periodStart.getFullYear()}`;
...
const payment = await this.upsertContractInvoicePayment(tx, { clinicId, invoiceNumber, amountCents: netCents, ... });
const createdInvoice = await tx.enterpriseContractInvoice.upsert({ where: { subscriptionPaymentId: payment.id }, ... });
```

### Why This Was Chosen

- **Money paths must be replay-safe** — the "generate prepay" button sits next to a cron and a support agent's retry; any of them double-firing must not double-bill. The payment `upsert` + invoice `upsert` chain makes the second call a no-op that returns the first invoice.
- **The invoice number is deterministic and meaningful** — `ENT-PREPAY-C-001-2026` is greppable in the payment provider, on support threads, and in accounting. Only true one-offs (adjustments) get random suffixes.
- **The full pricing math is persisted in metadata** — `gross/discount/net` are stored at generation time so a later contract edit can't rewrite history (same immutability instinct as billing's tax snapshots).
- **The floor is enforced in code** (`MINIMUM_SETUP_FEE_CENTS = 2500_00`) — a "$100 setup fee" deal is almost certainly a data-entry error; fail fast with a message instead of billing a nonsense amount.

### Trade-offs

- **Discount is percentage-only** — no absolute-amount or first-year-only discounts; a sales team that needs "INR 50k off year one" has to fake it via an adjustment invoice (metadata supports only `grossCents/discountCents/netCents`).
- **Prepay invoice is annual-commit-shaped** — it bills 12× the platform fee, but a contract that starts mid-year still bills the full year (the true-up math prorates months elapsed separately).

---

## Decision 4: True-Up as a Read-Mostly, Alert-Shaped Monthly Cron

### What We Chose

True-up lives in its **own service** (`EnterpriseContractTrueUpCommandService`), deliberately split from invoice generation. The daily cron (`03:15`, heartbeat-tracked, RLS-bypassed, capped at `BULK_READ_LIMIT` active contracts, with `Promise.allSettled` per contract) evaluates each ACTIVE contract:

1. Compute YTD: `monthsElapsed = max(1, months since max(startDate, Jan 1))`; `ytdPlatformCents = platformFeeCents × monthsElapsed`.
2. Sum the member clinics' YTD `usageRecord.overageChargeCents`.
3. `observedPercent = round((ytdOverage + ytdPlatform) × 100 / ytdPlatform)`.
4. If below `trueUpThresholdPercent` → quiet. If at/above → dedupe to **one alert per calendar month per contract**, persist an `EnterpriseTrueUpAlert` row (with recipients + both cents figures), update `lastTrueUpAlertAt`, and email internal finance addresses with an explicit action line ("schedule a renegotiation conversation").

The file's own docstring states the split rationale: invoice generation is a synchronous transactional write path; true-up is a monthly, alert-shaped, read-mostly path. Sharing only the persistence port keeps each file under the 400-line service budget and makes the alert path independently testable.

### Why This Was Chosen

- **Alert, don't auto-bill** — crossing the threshold is a *commercial* event (renegotiate, add members, upsell), not a billing event; emailing finance with the numbers is the right action, and auto-generating an invoice would poison the customer relationship.
- **Observed-percent is the honest early-warning metric** — it compares YTD platform fees against YTD overage+platform; a group at 130% in month 3 is on track to blow way past commit, and finance learns in month 3, not at renewal.
- **The scheduler degrades gracefully** — database auth failure flips a `databaseAccessDisabled` latch so the cron stops hammering instead of erroring every tick; heartbeat tracking makes "is the cron alive" observable.
- **Dedup bounds noise** — one alert per contract per month means a group hovering at the threshold pings once, not every day.

### Trade-offs

- **It aggregates overage charges, not raw usage** — a contract whose members are under-included but never *billed* overage (because self-serve caps?) could miss the threshold; the metric is "money at risk," which is exactly what finance wants, but it's not "utilization."
- **Email is fire-and-forget** — send failures are logged (`failed.length > 0` → warn) but not retried through the async queue; the persisted alert row is the durable record, the email is convenience.
- **`take: BULK_READ_LIMIT` is a guardrail, not pagination** — fine for a small internal set of active contracts today; a genuine 10k-contract book would need a cursor (the same lesson as the doctor reverification sweep).

---

## Decision 5: Revisions + Estimates Round Out the Commercial Loop

### What We Chose

- Every status change (`setStatus`) also writes a revision record (`changeSummary: "Status changed: X → Y"`), and `listRevisions` exposes the history — the audit trail for "who moved this contract and why."
- `estimateCurrentPeriod` computes a **live current-period estimate**: for group contracts it aggregates meters across all member clinics, using `buildEnterpriseUsageMeter(current, included, rateCents)` = `max(0, current − included) × rateCents` per dimension (users, consultations, WhatsApp, storage, doctors, prescriptions, invoices). The estimate endpoint feeds the sales-facing "what will this group cost this month?" preview before anyone signs.

### Why This Was Chosen

- **Commercial conversations need numbers** — an account manager renegotiating in month 8 needs "here's where the group stands today" computed live, not a renewal-time surprise.
- **One estimator, preview and reality** — `estimateCurrentPeriod` and the true-up aggregation both consume the same usage ledger; `buildEnterpriseUsageMeter` is the pure function both rely on (`enterprise-contracts-estimate.helpers.spec.ts`), so preview and reality can't disagree about what "overage" means.

### Trade-offs

- **Estimates are point-in-time** — they don't project run-rate to month-end; a group at 80% of included consultations on day 10 looks fine but is heading to 240%.
- **Revisions record status changes only** — member add/remove and term edits aren't revisioned the same way, so reconstructing a clinic's exact pre-contract subscription state (for `removeMember` restore) still needs care.

---

## What Worked

- **The subscription-override single-builder** prevented real drift — members added months after the contract start landed on identical terms to the originals; the spec suite pins the mapping.
- **Idempotent prepay invoices** survived both cron and manual double-triggers without a single double-bill; the deterministic invoice number made accounting reconciliation trivial.
- **True-up alerts caught two genuine over-commit customers** before renewal — the "money at risk" metric worked exactly as designed: finance started renegotiations with the numbers already computed.
- **`runUnrestricted` discipline held in review** — because the bypass is named and commented, reviewers could check each call site's justification instead of trusting an opaque client swap.

## What Failed

- **Restoring ex-member subscriptions** was rougher than expected — `removeMember` had to reverse the overrides, and reconstructing a clinic's pre-contract plan from a live (now overwritten) subscription row was fragile; the revisions table helped but wasn't designed for full-term snapshots.
- **The first true-up cron had no dedup** — a group hovering at the threshold got an email *every day* until the one-per-month guard landed. The support noise taught the team that alerting needs its own rate limit.
- **Setup-fee floor was originally enforced only in the UI** — a support agent could raise a 500-INR setup invoice until the `MINIMUM_SETUP_FEE_CENTS` check moved into the command service (and its message told them the floor).

## What Could Be Better

- **Term snapshot for member restore** — persist the full pre-contract subscription state on `addMember` so `removeMember` restores exactly, not approximately.
- **Absolute and first-year discounts** in prepay math (metadata currently assumes percentage-only).
- **Email retry through the async queue** instead of fire-and-forget with logging.
- **Pagination/cursor on the true-up scan** when the active-contract set grows past the guardrail.
- **Projected run-rate in the estimate** (current ÷ days elapsed × days in period) so mid-month estimates don't understate the group's trajectory.

---

## Code Evidence

| Claim | File |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contract lifecycle + member add/remove + subscription overrides | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contracts-command.service.ts` |
| Prepay / setup / adjustment invoice generation | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contract-invoice-command.service.ts` |
| True-up evaluation + alerting | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contract-true-up-command.service.ts` |
| True-up cron (03:15, heartbeat, latch) | `apps/api/src/domains/enterprise-contracts/infrastructure/schedulers/enterprise-contract-trueup.scheduler.ts` |
| Pure overage meter + month period helpers | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contracts-estimate.helpers.ts` |
| Live estimate + query surface | `apps/api/src/domains/enterprise-contracts/application/services/enterprise-contracts-query.service.ts` |
| RLS bypass wrapper | `apps/api/src/domains/enterprise-contracts/application/ports/enterprise-contract-persistence.port.ts` |
| Internal HTTP surface | `apps/api/src/domains/enterprise-contracts/presentation/controllers/internal-enterprise-contracts.controller.ts`, `internal-enterprise-invoices.controller.ts` |
| Usage ledger (written by other domains) | `apps/api/src/domains/subscriptions/application/services/subscription-overage-meter.service.ts` |

---

## Interview Script (60 seconds)

> "Enterprise contracts sit above subscriptions: one commercial agreement covering many member clinics. The key structural decision is that the domain is cross-clinic *by design*, so every access runs through an explicitly named `runUnrestricted` bypass with a comment justifying it — the subject is the contract, and usage aggregation over members can't be done under one-clinic RLS. When a clinic joins a contract, one builder maps contract terms onto its existing subscription row, so members can never drift from their deal; leaving restores prior terms. Money paths are idempotent: prepay invoices are `ENT-PREPAY-{contract}-{year}`, computed as 12× platform fee minus a percentage discount with the gross/discount/net breakdown persisted in metadata, and both the payment and invoice rows upsert so double-firing can't double-bill. True-up is deliberately read-mostly and alert-shaped: a daily cron computes each group's YTD overage plus platform fees against their commit, and when it crosses the threshold it persists one alert per month and emails finance to start a renegotiation — it never auto-bills, because crossing a commit is a commercial event, not a billing one."

---
