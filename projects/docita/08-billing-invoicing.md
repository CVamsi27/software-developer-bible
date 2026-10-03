# 08 — Invoices: Preserve the Calculation and Reconcile Actual Collections

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



## Definition

An invoice records a charge and the facts used to calculate it. A payment records collected money. Tax snapshots retain calculation context; a daybook groups collection records for reconciliation. These are connected responsibilities with different state and time boundaries.

If a clinic changes its registration or a catalog price after an invoice was created, a historical document should not silently substitute today's facts. If a payment arrives late, a collection report must also say which date determines its period.

This case describes source inspected on **2 October 2026**. Tax component names below explain the implementation; they do not establish the legally applicable treatment of a particular healthcare service. The old universal 12%/18% assertions and unverified tax-accuracy outcomes have been removed.

## First Principles

Settings and prices change, financial calculations involve rounding, and invoice and payment state can diverge when delivery or processing fails. Historical facts must be retained independently of mutable configuration, and collected amounts need a reconcilable identity and period.

A snapshot preserves inputs; it does not prove those inputs were correct. A status transition records a local state change; it does not prove the provider collected money.

## Why Preserve Seller, Buyer and Line Calculations?

The invoice command reads the clinic's configured tax settings and builds seller/buyer snapshots. Seller values include registration, legal name, address and state information. The buyer captures identity/address from the patient context. The calculator receives line items, currency and place-of-supply context.

```text
configured context + supplied items
  → validate and calculate lines/components
  → persist totals, line items and seller/buyer/tax snapshots
  → render the historical invoice from those retained facts
```

The creation path persists calculated values; allowed edits can recalculate items using existing seller/buyer snapshots. If snapshots are missing, the update path falls back to current context. The implementation therefore does not make every invoice immutable from its first creation onward.

Define when a document becomes final, which corrections create a new document and how missing legacy snapshots are handled. Historical settings changes should not automatically rewrite an already-final document, but preserving an incorrect calculation forever is not a correction policy either.

## How the Inspected Tax Calculator Works

The calculator determines line treatment from explicit fields and configured defaults, derives subtotal/discount/tax/grand total and aggregates components by type and rate. Taxable lines require a place-of-supply state in the current implementation. The supplied buyer address is not itself an automatically validated supply-state classification.

For configured Indian taxable treatment, the implementation compares normalized seller and supply state codes. Matching codes split the computed tax into CGST and SGST; differing codes produce IGST. The split rounds one component and derives the other from the total, preserving the component sum.

This explains code behavior, not a universal tax rule. Applicable exemption, classification, rate, place of supply and document requirements need an independently maintained and reviewed policy. The calculator's defaults, including exempt-healthcare treatment and `eInvoice.required = false`, are implementation choices rather than proof of compliance.

### Money Needs Explicit Units and Rounding

The command persists calculated totals alongside canonical minor-unit fields for supported writes. A trustworthy calculation also defines line versus invoice rounding, discounts, precision, numeric range and currency scale.

```text
subtotal − discount + tax = grand total
sum(component amounts) = tax total
```

Use these identities as consistency checks with representative rounding cases. A field named cents does not establish that all supported currencies use two decimal places. Do not sum incompatible currencies or assume floating-point rounding and integer persistence are interchangeable.

## How Current Invoice States Differ From the Old Diagram

The current transition helper uses **PENDING, PARTIALLY_PAID, PAID, OVERDUE and CANCELLED**, rather than a universal DRAFT → ISSUED sequence.

| Current state | Helper permits |
| -------------- | ------------------------------------------ |
| PENDING | Paid, partially paid, overdue or cancelled |
| PARTIALLY_PAID | Paid, overdue or cancelled |
| OVERDUE | Paid, partially paid or cancelled |
| PAID/CANCELLED | No transition to a different state |

The helper permits a repeated same-status request. The entity value object's table differs in some cancellation paths, so do not claim every write follows one perfectly unified state machine. The payment capture path also writes invoice status through its own transaction, as described in the [payments case](04-payment-flows.md).

The command rejects line-item or total edits on paid/cancelled invoices and invokes claim-readiness checks for selected transitions. These are inspected local protections. A preflight read must still be connected to an expected-state or version-aware write if a competing update can intervene. An allowed PAID transition is not evidence of a verified payment amount.

Refunds, credit notes and reissued documents need their own authorized financial protocol. The fact that the transition helper disallows changing a paid invoice does not prove a complete correction or refund workflow exists.

## How the Daybook Groups Collection Records

The collection query converts requested dates into **UTC-midnight** bounds. It fetches clinic-scoped sessions in CAPTURED or PAID state, then groups amounts by the recorded channel, falling back to an online/cash classification when metadata is absent.

The repository range filter uses **session `createdAt`**, not `paidAt`. A session created yesterday and captured today can therefore enter yesterday's report. Whether that is appropriate depends on the report's explicitly chosen definition; it is not automatically a clinic-local cash-received-today view.

The aggregator adds all session amounts and returns a currency overwritten by each session. If mixed currencies are possible, labeling the combined amount with the last currency is incorrect. Enforce one report currency or group by currency, and separately reconcile refunds, failed captures and provider settlements according to the desired report.

A daybook supports reconciliation with counted cash or external statements. It does not complete that comparison automatically. Cash declared in the application and cash physically present can differ.

## Real-World Decisions

| Concern | Define before implementation | Verification |
| ----------------------------- | -------------------------------------------------------- | ------------------------------------------- |
| Historical document integrity | Finalization point and retained calculation context | Change settings/prices after creation |
| Tax calculation | Reviewed classification and supplied context | Known line/component/rounding fixtures |
| Concurrent status updates | Allowed persisted transition and expected state | Interleaved capture, edit and cancellation |
| Partial payment | Amount due, applied amount and remaining balance | Multiple and duplicate payment events |
| Daybook date | Created, captured, settled or clinic-local reporting day | Late capture and midnight boundaries |
| Currency | Currency per amount and permitted grouping | Mixed-currency rejection or separate totals |
| Corrections/refunds | New document or financial reversal protocol | Audit continuity and reconciliation |

Multi-currency support and tax-filing integration cannot be inferred from adding a currency field or rendering a tax summary. Verify their complete behavior before describing them as supported or absent.

## Mistakes

- Publishing one healthcare tax rate as a universal rule.
- Calling every persisted invoice snapshot immutable despite allowed recalculation paths.
- Equating PAID status with verified collection.
- Treating a preflight transition check as concurrent enforcement.
- Calling UTC created-date grouping a clinic-local payment-date report.
- Adding mixed-currency amounts and labeling them with one currency.
- Quoting incident-free tax calculation or faster reconciliation without evidence.

## Best Practices

Keep calculation policy separate from historical evidence. Test totals and component identities, preserve explicit units, and exercise concurrent financial transitions. Give reports precise date/currency definitions and reconcile them with independent collection evidence. Explain exactly which write path enforces a rule and which correction workflows remain to be verified.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Current strengths | Minor-unit helpers, context snapshots and explicit invoice states support financial reasoning. |
| Current limitations | State helpers differ across paths, snapshots can be recalculated, and collection dates/currencies need consistent definitions. |
| Recommended design | Finalize immutable financial context, use explicit correction documents, gate state changes on verified payments, and report currency-separated collections by the defined payment time. |
| Evidence needed | Arithmetic identities hold under the rounding policy; finalized context cannot be silently rewritten; late capture appears in the intended period and mixed currencies never form one unlabeled total. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Invoice snapshots retain calculation context; state checks constrain local changes; collection reports support reconciliation. Correct financial behavior also requires reviewed policy, coherent concurrent writes, explicit time/currency definitions and recoverable payment processing.

## See Also

- [Category revision](REVISION.md) — calculation and collection questions.
- [Payment flows](04-payment-flows.md) — provider identity and capture transactions.
- [Analytics](14-analytics-and-dashboards.md) — financial metric definitions.
- [Insurance claims](11-insurance-claims.md) — separate claim lifecycle.
- [Case-study index](INDEX.md) — learning stages.

## References

Docita source inspected on 2 October 2026:

- `apps/api/src/domains/billing/application/services/invoices-command.service.ts`
- `apps/api/src/domains/billing/core/services/tax-calculator.service.ts`
- `apps/api/src/domains/billing/application/services/invoice-status-transition.ts`
- `apps/api/src/domains/billing/core/value-objects/invoice-status.value-object.ts`
- `apps/api/src/domains/billing/application/services/invoices-query.service.ts`
- `apps/api/src/domains/billing/infrastructure/repositories/prisma.payment-session.repository.ts`
