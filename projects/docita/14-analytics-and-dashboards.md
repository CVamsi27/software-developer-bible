# 14 — Analytics: Define the Metric, Calendar and Snapshot Before Aggregating

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



“Revenue this month” is incomplete until you define clinic identity, paid versus invoiced value, currency, timezone, corrections and the reporting cutoff. A fast query can consistently return the wrong metric if those definitions are missing.

## Definition

Analytics turns business records into metrics for a specified scope and period. A dashboard is a frequently read presentation of selected metrics; a persisted snapshot stores a computed result for later comparison.

> **Textbook Definition:** A metric is a defined aggregation over a population, time window and measurement rule; a dashboard presents selected metrics, while a snapshot persists results for a particular cutoff.

The analytics-factory assessment below retains its **2 October 2026** source inspection and controlled probes. The operational-dashboard section has a scoped **28 October 2026** implementation and definition update in a tested working tree based on canonical revision `f3fddffc0`. It has not been deployed by this work. That update does not refresh the other factory findings into a new audit or establish production activity.

## First Principles

Source records change over time, calendars depend on timezone, caches can retain earlier results and independent queries can observe different states. Aggregating current prices can also differ from aggregating historical charged amounts.

A correct metric therefore needs a definition, the full set of records it covers, explicit start and end times, numerical units, and rules for how fresh and mutually consistent its inputs must be. Storing a result preserves what was calculated, including any mistakes or stale inputs.

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

The overview cache uses **one hour**; dashboard home stats use **60 seconds**. Other methods use configured or method-specific time-to-live (TTL) values, which determine how long an entry remains valid. Cache keys must include every input that changes the result: tenant, period/range, timezone, permission-sensitive scope and metric version where applicable.

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

## A Dashboard Built From Actual Records and Retained Telemetry

A receptionist can book one visit, a clinician can revise its prescription, and a payment callback can arrive twice. Counting every row or request as another patient would inflate the result. The internal operational dashboard therefore needs a definition for each displayed quantity before a capacity claim can use it.

The dashboard reads existing appointment, prescription, invoice, queue and request records through one aggregate statement. It adds no invented metric rows. The route is restricted to INTERNAL operators and the frontend parses a shared Zod contract. Contract version 2 identifies customer-request scope and adds prescription creation, distinct clinic-patients seen, P99 and valid/invalid latency sample counts. Those fields are optional for compatibility with an older API; a missing field means unknown or unavailable, rather than a silently assumed version-2 value.

### Follow the Business Record to Its Counter

Every read uses a rolling **30 × 24-hour UTC window**, including the start and excluding the end. The same instant at the right edge belongs to the following window. A single PostgreSQL statement gives these aggregates one statement snapshot. This differs from the separate analytics facade's clinic-local calendar-month counters.

```text
Reporting cutoff from injected clock
             |
             +--> start = cutoff - 30 days; end = cutoff
             |
             +--> Appointment.startTime in [start, end)
             |      +--> all statuses --> appointments scheduled
             |      +--> current COMPLETED --> completed appointments
             |      +--> completed + distinct clinic/patient pairs --> patients seen
             |
             +--> Prescription.createdAt in [start, end) --> prescriptions created
             +--> Invoice.createdAt in [start, end) --> invoices created
             +--> QueueJob.createdAt in [start, end) --> retained job cohorts
             |
             +--> one SQL statement --> one response with exact window bounds
```

| Quantity | Version-2 definition | What would change its interpretation |
| -------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Clinics with appointments | Distinct clinic IDs with appointment start times in the window | Includes cancelled appointments and demo/test clinic records; not active paying customers |
| Appointments scheduled | Appointment start time in the window, all current statuses | Not appointment creation time or only completed visits |
| Completed appointments | Scheduled in the window and currently COMPLETED | Does not establish when completion occurred; a later status correction can change a rerun |
| Clinic-patients seen | Distinct `(clinicId, patientId)` pairs among those completed appointments | Not new registrations or globally deduplicated people; one person at two clinics can contribute twice |
| Prescriptions created | Prescription record creation time in the window | Not medication-item count, subsequent edits, reviewed clinical correctness or generated PDF count |
| Invoices created | Invoice creation time in the window, without a paid-only filter | Not collected revenue, captured payments or settlement; corrections and states require separate analysis |
| Retained jobs / currently failed | Jobs created in the window, with their current status | Cleanup removes history; a failure followed by recovery is no longer currently failed |

The general analytics facade's `patientsThisMonth` counts new patient records from its month start. Its usage endpoint groups doctor IDs on recently created appointments for an activity measure. Neither can replace distinct patients treated or all staff logins. Staff accounts, daily activity, concurrent sessions and in-flight requests need their own definitions.

The schema allows one prescription record per appointment, while PDF metadata is nullable and PDF work has a separate lifecycle. One invoice per completed visit and one PDF per prescription remain assumptions in the [25-clinic model](23-hypothetical-clinic-metrics.md). Counting unique prescription rows cannot verify successful document delivery.

### Preserve the Observation Time Through a Delayed Flush

A request observation has two relevant clocks. `observedAt` records when the instrumented request was observed; `createdAt` records when its row reached persistence. A delayed buffer flush must not move old traffic into the current hour or month. The version-2 operational query selects `observedAt` in the same half-open reporting window and selects `routeCategory = CUSTOMER` before calculating request counts and latency.

```text
Customer request --> timed observation --> buffered request record --> database flush
                           |                         |                       |
                      observedAt                may be delayed           createdAt
                           |                                                 |
                           +--> chooses the reporting window                 +--> ingest time
                           |
                           +--> CUSTOMER population
                                  +--> all retained outcomes --> request/error counts
                                  +--> valid durations --> P50 / P95 / P99
                                  +--> invalid durations --> excluded-latency count

Missing observations or failed flushes --> separate coverage evidence
```

Health probes and internal operator routes have separate categories. Their small or frequent responses must not dominate the customer distribution. A mixed legacy query and a customer-only query cannot be compared as though they measured the same population.

Within the customer-request population, valid durations must have `latencyValid = true` and lie between zero and the canonical **120,000 ms** validity ceiling. Zero can be a valid millisecond-resolution observation. Rows outside the latency rule remain visible through the invalid count; their HTTP outcomes remain in the request/error denominator. Filtering out an invalid duration must not erase a failed request from the outcome rate.

| Request metric | Definition | Required reading condition |
| -------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| Request samples | Retained CUSTOMER observations whose `observedAt` falls in the window | This is observed traffic, not traffic reconstructed during a capture outage |
| Server errors | HTTP 5xx observations in that same customer population | Intentional 4xx responses and business-level failures need separate classifications |
| Server-error percentage | Server errors divided by request samples, multiplied by 100 | No samples produces unavailable, not a measured zero-percent error rate |
| Valid latency samples | Customer observations satisfying the flag and duration bounds | Keep their count alongside the total request count |
| Invalid latency samples | Customer observations excluded by that latency rule | Investigate instrumentation and preserve the missing distribution's uncertainty |
| P50 / P95 / P99 | PostgreSQL continuous percentiles of valid customer durations, in milliseconds | State the population, sample count, algorithm, window and capture coverage |
| First / last sample | Earliest/latest eligible `observedAt` retained for the window | Bounds of observed data, not proof of continuous capture or service availability |

An HTTP 200 can still contain the wrong business result, and a completed database transaction can leave an external effect pending. Add domain correctness checks and job/provider outcomes to the request-level measurements. The [async case](03-async-processing.md) explains those distinct acknowledgment boundaries.

### Match the Percentile Method Before Comparing Two Runs

The operational SQL uses `percentile_cont`, which interpolates between sorted observations. The reproducible API-soak producer uses the nearest-rank method, which selects an observed value. Both need an explicit definition; their values can differ on the same small sample.

For synthetic durations of **10, 20, 30, 40 and 50 ms**, continuous P95 is **48 ms**, while nearest-rank P95 is **50 ms**. These are arithmetic examples, not Docita latency results. A change from one algorithm to the other can create an apparent change without any request becoming faster.

```text
Retained CUSTOMER observations                 Controlled API-soak requests
          |                                              |
valid flag + duration bounds                    expected-status and run checks
          |                                              |
PostgreSQL percentile_cont                     nearest-rank summarizer
          |                                              |
production-observation card                    controlled-run evidence card
          +----------------------+-----------------------+
                                 |
                compare only equivalent measurement boundaries
```

P99 describes the upper tail of the selected population; it does not identify its cause. With 100 samples the highest few observations control the result. Even 1,000 observations give only about ten observations in the upper one percent, before considering correlated requests or route imbalance. Retain raw observations or a compatible mergeable distribution and repeat representative windows. Do not average per-route, per-machine or per-clinic percentile values into a platform percentile.

A pooled customer percentile can still hide an expensive route or a noisy clinic. Break the measurement down by endpoint class, payload size and relevant workload, while avoiding patient identifiers and uncontrolled high-cardinality labels. Keep cold-start and warm steady-state results separately when their user experience differs.

### Distinguish a Latency Budget From an Executed Result

The source defines CRUD targets of P95 at most **200 ms** and P99 at most **500 ms**, alongside separate authentication, search, report and webhook-ingress budgets. A target states the objective; it does not populate a measurement. The API-soak capture records route class, offered rate, outcome counts, cache headers and source provenance. Its required-baseline gate rejects absent or incomplete evidence.

The bounded-rate soak is a latency experiment rather than a maximum-capacity test. Its current webhook probe exercises invalid-signature rejection, so that probe's response time does not measure successful payment processing or settlement. Long document completion has its own enqueue-to-artifact timestamps rather than borrowing the report-ingress budget.

Before claiming a comparison, keep the same route, dataset, authorization, request mix, resource profile, cache protocol and measurement method. Retain timeouts, rejected work and incomplete jobs alongside completed latency samples. An improvement made by returning fewer authorized fields or silently dropping expensive requests changes the experiment.

### Reconcile a Small Fixture Before Generating a Large One

Use known small records to establish the query's meaning before running a workload benchmark. Put one appointment exactly at each time boundary; vary cancelled and completed statuses; repeat a patient within one clinic and across two clinics; create a prescription without a PDF; and create an unpaid invoice. Compare the expected counts with the aggregate output.

For telemetry, include an observation made before the window but flushed inside it, a health probe, a customer 5xx with an invalid duration, a zero-duration valid sample and an entirely empty window. These cases test the clock, population and denominator independently. Reconcile the response with an independently computed result on an isolated PostgreSQL fixture, rather than relying only on mocked repository values.

After correctness, test the modeled daily mix, busy window and stress case. Record database plans and resource pressure at the same times as route latency; a percentile alone cannot distinguish pool wait, lock wait, input/output (I/O), garbage collection, a provider timeout or a cold start. Infrastructure measurement and resource budgeting are developed in [deployment](10-deployment-infrastructure.md) and the [capacity model](23-hypothetical-clinic-metrics.md).

### A Controlled Query Result Establishes the Definition

On **28 October 2026**, the isolated PostgreSQL 16.15 fixture exercised the repository's actual parameterized SQL against synthetic tables. The initial four query tests and nine database-target guard tests passed; the modeled-volume case brought that initial suite to 14. A later same-day continuation adds the nonempty all-invalid case below, bringing the current suite to 15. The fixture creates a uniquely named schema on a designated loopback test database and removes that schema afterward; it does not start the API or contact a clinical production database.

| Fixture input | Expected version-2 result |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Six eligible customer observations, including three invalid timings | Six requests, two server errors, three valid timings and three invalid timings |
| Manually seeded valid durations of 100, 200 and 500 ms | Continuous P50 200 ms, P95 470 ms and P99 494 ms |
| Health/internal observations, an older-observed late flush and an exact-end observation | Excluded from the customer observation window |
| Six in-window appointments, including cancelled/demo records | Three clinic IDs, six scheduled appointments and four currently completed appointments |
| Repeated completed patient in one clinic and another clinic/patient pairing | Three distinct clinic-patient pairs |
| Two prescription records, one without a PDF | Two prescriptions created; no inference that two PDFs exist |
| Three invoices including unpaid/cancelled and four retained jobs | Three invoices, four jobs and one job currently FAILED |

Before the repair, four query assertions failed for the expected scope/count defects: the old query mixed observation populations and yielded P50 250 ms and P95 92,250.75 ms on these supplied rows. The corrected duration values were deliberately inserted inputs. The test proves that the SQL selects and aggregates them correctly; **470 ms and 494 ms are not measured API response times**. It does not exercise the application's runtime database role, end-to-end tenant enforcement, deployment memory limits or a 25-clinic workload. Those experiments remain separate evidence cards.

### Keep the Error Rate When Every Timing Is Invalid

A later real-PostgreSQL regression inserts three customer observations inside the window: one explicitly invalid timing, one negative duration and one duration above the accepted bound. Two observations have server-error statuses. The aggregate must retain **three requests, two errors, zero valid timings and three invalid timings**, with known first/last observation timestamps and `null` P50/P95/P99.

The same result passes through the actual operational service under a fixed clock. It reports a **66.67% retained-request error rate** while every latency percentile remains unavailable. This closes a distinct boundary from an empty window: outcomes can be known even when timings are unusable. Returning a zero percentile would invent fast service; discarding the requests would hide failures. The fixture does not establish that production telemetry captured every request.

The dedicated suites pass **15 tests: six PostgreSQL aggregate cases and nine database-target guards**. The existing focused service suite passes **four**. Their owned fixture schemas are removed afterward. These are executed regression checks, not a customer error-rate or API latency result.

### Verify the SQL at a Known Monthly Row Volume

A second fixture inserted the modeled month's projected records and checked the aggregate:

| Synthetic input and expected output | Verified count |
| --------------------------------------- | -------------- |
| Clinics represented by appointment keys | 25 |
| Completed appointments | 26,000 |
| Distinct clinic-patient pairs seen | 20,000 |
| Prescription records created | 20,800 |
| Invoice records created | 26,000 |
| Valid customer observation rows | 520,000 |

The modeled-volume fixture remains part of the dedicated SQL/target-guard suite, now at 15 passing tests. The volume fixture uses 800 distinct patient aliases and 1,040 visits per clinic, with returning patients contributing the remaining visits. Prescription PDF fields are left empty and invoices are pending, preserving the distinction between record creation and completed external effects.

This verifies aggregate definitions on that row volume. The projected tables do not include the full application's indexes, constraints, RLS roles or patient workflows, and the tests do not run the API or worker. Therefore they do not establish tenant authorization, end-to-end latency, concurrent capacity, customer adoption or Fly resource sufficiency. The real application capacity experiment remains a separate boundary.

### Retained Samples Do Not Form an Availability Monitor

The request logger buffers observations before persistence and can disable persistence after database authentication or missing-table errors. Monitoring cleanup removes old observations. The UI's first and last sample timestamps therefore cannot establish what happened between them, and a version-2 response does not guarantee a complete reporting window.

Consult telemetry-coverage events and missing-observation indicators before interpreting request totals and percentiles. Record separately whether the observation set is complete enough for the stated claim. A time-based availability objective needs an independent observation contract, outage classification and reporting window. A 5xx fraction computed from retained application rows has a different denominator.

### Preserve the Historical Result With Its Original Population

A read-only production check on **2 October 2026**, with a ten-second SQL timeout, returned **158 retained requests, zero recorded 5xx responses, median 0 ms and P95 2 ms**. The samples covered **29 September 18:04:37 UTC through 30 September 04:29:51 UTC**. The same aggregate returned **zero appointments, invoices and retained jobs** in its rolling window. No patient records or credentials were exposed and no production rows were inserted.

That historical query used the earlier retained-request population; it is not a version-2 customer-only measurement. The 28 October contract change must not relabel those observations or extrapolate them into a 30-day traffic total, an achieved CRUD target or a 25-clinic adoption result. Recheck deployment and obtain a representative observation set before producing a new operational evidence card.

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

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Read repositories, caches and snapshots separate operational views; versioned customer telemetry makes time, population and invalid samples explicit. |
| Current limitations | Historical factory findings remain scoped and dated; retained observations can have gaps, and no capacity or customer-adoption result follows from the operational query. |
| Recommended design | Define each metric with authoritative facts, currency, timezone and window; use stable period keys and idempotent versioned snapshots; publish freshness and correction semantics. |
| Evidence needed | Known fixtures reproduce correct totals and weighted averages; cross-month weeks remain distinct; historical reruns use the intended date and do not duplicate contributions. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Analytics requires explicit business, calendar and numerical definitions. Versioned operational metrics connect records and customer observations to defined counts and percentiles, while older factory findings retain their own scope. Validate the query with known fixtures, preserve capture gaps and distinguish a workload model, a configured objective and an executed result.

## See Also

- [Category revision](REVISION.md) — metric and consistency questions after learning.
- [Inventory](13-inventory.md) — mixed units and parallel reads.
- [Billing](08-billing-invoicing.md) — historical financial records.
- [Async processing](03-async-processing.md) — scheduler failures and recovery.
- [Capacity model](23-hypothetical-clinic-metrics.md) — workload, resource budgets and acceptance experiments.
- [Deployment](10-deployment-infrastructure.md) — measure compute, database and recovery boundaries.
- [Case-study index](INDEX.md) — reading stages.

## References

Docita source inspected on 2 October 2026:

- `apps/api/src/domains/analytics/core/factories/base-analytics.factory.ts`
- `apps/api/src/domains/analytics/core/factories/financial-analytics.factory.ts` and `operational-analytics.factory.ts`
- `apps/api/src/domains/analytics/core/factories/snapshot-analytics.factory.ts` and `period-bucket.util.ts`
- `apps/api/src/domains/analytics/infrastructure/repositories/analytics-groupby.helpers.ts` and `analytics-groupby-count.ts`
- `apps/api/src/domains/dashboards/dashboard/application/services/dashboard.service.ts`
- `apps/api/src/shared/modules/internal/internal-operational-metrics.controller.ts`, `.service.ts`, and `infrastructure/prisma-internal-operational-metrics.repository.ts`
- `packages/types/src/admin/operational-metrics.ts` and `apps/internal/src/features/performance/pages/performance-page.tsx`
- `apps/api/src/shared/modules/monitoring/monitoring/services/request-log.service.ts` and `metrics.scheduler.ts`

Scoped operational-metric revision, 28 October 2026:

- `apps/api/src/shared/modules/internal/internal-operational-metrics.service.ts` and `infrastructure/prisma-internal-operational-metrics.repository.ts`
- `packages/types/src/admin/operational-metrics.ts` and `apps/internal/src/features/performance/pages/performance-page.tsx`
- `apps/api/src/shared/modules/monitoring/monitoring/rules/telemetry-observation.rules.ts` and `services/request-log.service.ts`
- `scripts/perf/capture-api-latency-soak.mjs`, `scripts/checks/check-api-latency-budget.mjs` and `scripts/checks/api-latency-slos.mjs`
- `apps/api/test/metrics/operational-metrics.integration-spec.ts` and `test-database-target.integration-spec.ts` — isolated SQL and target-guard regression evidence
