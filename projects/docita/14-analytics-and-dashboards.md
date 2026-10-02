# 14 — Analytics: Define the Metric, Calendar and Snapshot Before Aggregating

## Definition

Analytics turns business records into metrics for a specified scope and period. A dashboard is a frequently read presentation of selected metrics; a persisted snapshot stores a computed result for later comparison.

“Revenue this month” is incomplete until you define clinic identity, paid versus invoiced value, currency, timezone, corrections and the reporting cutoff. A fast query can consistently return the wrong metric if those definitions are missing.

This case describes source inspected on **2 October 2026**. Controlled source probes establish specific calculation behavior, not the accuracy of production reports.

## First Principles

Source records change over time, calendars depend on timezone, caches can retain earlier results and independent queries can observe different states. Aggregating current prices can also differ from aggregating historical charged amounts.

Metric correctness therefore needs a definition, complete scope, explicit temporal boundaries, numerical units and a known consistency model. Persisting a result preserves what was calculated, including any mistakes or stale inputs.

## Why Split Metric Families?

The analytics facade coordinates operational, financial, clinical and snapshot factories. They group different calculations rather than presenting one large service with every query.

| Family | Responsibility | Important boundary |
| ----------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| Operational | Patient growth, appointments, demographics and overview | Period definitions and denominator meaning |
| Financial | Revenue trends, CPT/category breakdowns and totals | Charged versus catalog value, currency and money representation |
| Clinical | Conditions and diagnosis summaries | Sensitive data, coding meaning and completeness |
| Snapshot | Persist selected computed metrics | Reporting date, input freshness and correction policy |

The financial factory uses a base for read-client access, date filtering and common dependencies. The operational factory instead delegates through an analytics repository and its own cache configuration; the snapshot factory has separate dependencies. Not all four simply inherit one universal base or guarantee that every read avoids the primary database.

Choose this separation to keep definitions and tests coherent. A dedicated warehouse may be useful for heavier workloads or independent reporting, but clinic counts alone do not prove it unnecessary: query plans, historical volume, freshness needs and operational capacity govern the choice.

## How a Calendar Range Differs From a Bucket Key

A range chooses which records enter a calculation; a bucket key assigns those records to periods. Both must use the same intended calendar.

```text
clinic-local month start/end → corresponding UTC instants → database range
included record instant → clinic-local calendar period → bucket key
```

For example, an instant just after midnight in Asia/Kolkata can still belong to the previous UTC date. Filtering with clinic-local bounds but grouping by the UTC date produces inconsistent labels. PostgreSQL can perform explicit timezone conversion and aggregation; application bucketing is a choice with memory/network costs, not the only correct option.

### Current Timezone Support Is Uneven

The overview includes clinic and timezone in its cache key and obtains month ranges through shared timezone utilities. Patient-growth bucketing uses a timezone-aware date formatter.

The inspected financial period helper is different: daily keys slice UTC ISO dates, monthly keys use process-local year/month and weekly keys use a hand-rolled formula involving the **day of month**. It accepts no timezone parameter. A timezone-aware financial input range therefore does not prove timezone-aware buckets.

A source-extracted probe found **7 January and 7 February 2026 both mapping to `2026-W1`**. Those distinct weeks collide because day-of-month logic is not a year-wide week identity. Select explicit ISO-week or product-specific week semantics and test year/month boundaries, week start, timezone and daylight-saving behavior.

The overview also moves to the previous month using `Date.setMonth` on the current date. Month-end overflow deserves a boundary test; deriving prior-period boundaries from a stable local month start avoids relying on an invalid day in the target month.

## How the Financial Calculation's Meaning Must Stay Visible

The inspected revenue-metrics method fetches invoice `total` and `createdAt`, groups the records by a period key and records each bucket's revenue, invoice count and average. It does not show a paid-only filter in that path and reads legacy totals rather than exclusively canonical minor-unit columns.

The CPT calculation groups procedures by code, fetches current code prices and multiplies price by procedure count. It limits the grouped result to **50 codes** before building categories. This is not the same operation as summing historical invoice-line charges, including discounts, tax and refunds. It can omit codes from the full category total and can change when current catalog prices change.

These methods need accurate names or corrected semantics. Do not describe all financial analytics as exact cents-based recognized revenue, or all CPT breakdowns as raw-SQL joins: the inspected method uses Prisma groupBy plus a price lookup.

### Raw Results Need a Deliberate Failure Policy

Typed ORM grouping is useful for supported aggregates; explicit SQL may better express joins or timezone-aware grouping. Bind values, scope every participating table appropriately and check numerical ranges when mapping database counts or sums into JavaScript numbers.

The inspected group mappers skip malformed rows and default missing count shapes to zero. That can be a chosen tolerance policy, but it **does not fail loudly**. A renamed or missing field can become an empty result or zero. Decide whether missing data should produce an error, a visible incomplete status or a controlled fallback; silently treating failure as a valid zero can mislead a user.

## How Caching Trades Load for Freshness

The overview cache uses **one hour**; dashboard home stats use **60 seconds**. Other methods use configured or method-specific TTLs. Keys must include every dimension that changes the result: tenant, period/range, timezone, permission-sensitive scope and metric version where applicable.

```text
first request → compute and cache
later request before expiry → reuse cached result
data changes → cached value may remain until invalidation or expiry
```

The freshness cost may be noticeable after booking or payment; it is not universally invisible. Replica lag, cached inputs and computation duration can add staleness beyond one simple TTL. Read-client access does not establish that a replica is configured or that different reads form one consistent snapshot.

For critical confirmation views, use suitable current reads or targeted invalidation. For trends, bounded staleness may be acceptable if the UI conveys it. Measure hit rate, query cost and concurrency; a cache miss storm can still overload the database.

## What the Current Snapshot Actually Preserves

The snapshot method calls financial, appointment, demographics and condition methods, then creates a persisted row. It labels the record daily but supplies neither an explicit historical date range nor a clinic timezone to those calls. In the revenue method, daily selects **bucket granularity**, not a restriction to the current day.

A stored row thus does not establish an internally consistent daily report or a historical “dashboard as it was.” Its inputs can cover different ranges and be independently cached. The method catches and logs errors rather than propagating failure; a scheduler caller cannot assume a resolved call created a row.

### Trace the Invoice-Count Error

Given two revenue buckets:

| Bucket | Revenue | Invoice count |
| -------- | ------- | ------------- |
| A | 30 | 3 |
| B | 70 | 7 |
| Combined | 100 | 10 |

The correct combined average per invoice is `100 / 10 = 10`. The inspected snapshot instead uses the number of buckets for `invoiceCount`, so it stores **2** and an average of **50**. A source-extracted probe with those controlled inputs reproduced both values. That probe does not establish which production reports used them.

The snapshot also stores the appointment fill rate under two fields, then exposes those values with coding-completeness and billing-rate labels in trends. A field alias does not change a metric's meaning. Resolve its numerator/denominator before relying on those labels.

### Backfill Needs a Historical Cutoff

A snapshot repair must accept the intended clinic reporting date, stable input window, version and correction policy. Rerunning the current method today does not reconstruct a missed historical day's state. The current cache key uses a UTC date; that also needs alignment with the intended clinic-day identity.

Choose whether corrections produce replacement snapshots, append a revised version or remain in a separate current-truth report. Neither “frozen forever” nor “recomputed live” is universally correct; consumers need to know which question the report answers.

## Real-World Decisions

| Reporting question | Define explicitly | Verification |
| ----------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------- |
| Revenue earned or cash received | Invoice status, settlement/refunds, currency and cutoff | Known transactions with expected totals |
| Procedure value by category | Historical charge or current catalog estimate; truncation policy | Changed prices and more than 50 codes |
| Clinic-local daily trend | Zone, local bounds and bucket identity | UTC midnight, DST and month/year boundaries |
| Growth relative to a zero baseline | Undefined/new-growth policy rather than an unexplained zero | Empty and nonzero baseline examples |
| Historical snapshot | Reporting date, input snapshot and correction version | Late changes and missed-date backfill |
| Home-screen update after a mutation | Freshness budget and invalidation | Read-after-write behavior under caches/replicas |

## Mistakes

- Treating a daily grouping argument as a daily date filter.
- Averaging grouped revenue by the number of buckets instead of the number of invoices.
- Calling catalog-price estimates collected revenue.
- Assuming every mapper rejects malformed results visibly.
- Claiming a persisted row makes historical calculations correct or backfillable.
- Advertising a read-client/cache design as measured near-zero cost.

## Best Practices

Write metric definitions before query code. Use explicit clinic-local bounds and consistent bucket identities, preserve currency/minor-unit meaning and test denominators. Distinguish valid zero from missing or failed data. Verify cache scope and freshness, and make snapshot date/version/recovery explicit. Use known small datasets to check calculations before performance tuning.

## Summary

Analytics requires explicit business, calendar and numerical definitions. Current source has useful family separation and caching, alongside bucket, snapshot and financial-meaning limitations. Accurate reporting depends on correcting and verifying those semantics rather than merely persisting or caching results.

## See Also

- [Category revision](REVISION.md) — metric and consistency questions after learning.
- [Inventory](13-inventory.md) — mixed units and parallel reads.
- [Billing](08-billing-invoicing.md) — historical financial records.
- [Async processing](03-async-processing.md) — scheduler failures and recovery.
- [Case-study index](INDEX.md) — reading stages.

## References

Docita source inspected on 2 October 2026:

- `apps/api/src/domains/analytics/core/factories/base-analytics.factory.ts`
- `apps/api/src/domains/analytics/core/factories/financial-analytics.factory.ts` and `operational-analytics.factory.ts`
- `apps/api/src/domains/analytics/core/factories/snapshot-analytics.factory.ts` and `period-bucket.util.ts`
- `apps/api/src/domains/analytics/infrastructure/repositories/analytics-groupby.helpers.ts` and `analytics-groupby-count.ts`
- `apps/api/src/domains/dashboards/dashboard/application/services/dashboard.service.ts`
