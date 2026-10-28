# 23 — Model a 25-Clinic Workload and Measure Its Outcomes

[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



The problem to solve is concrete: morning bookings, clinical records, billing and asynchronous documents share the database. Average monthly volume can look small while a synchronized morning burst overwhelms one job lane or exposes a booking race.

## Definition

A workload model describes how people use a system and translates that usage into operations, load and measurable outcomes. It helps choose tests and explain capacity decisions before operational records are available.

> **Textbook Definition:** A workload model translates assumed user activity into operation rates, resource demands and test scenarios. Its estimates remain hypotheses until supported by comparable measurements.

**This entire scenario is hypothetical.** Assume exactly **25 active clinics** as the minimum-size example for “25+ clinics.” Usage, timing samples and proposed targets below are invented for study. They are not Docita customer counts, production results, historical improvements or evidence for a resume. Current-code observations are identified separately and linked to their case studies.

## First Principles

A clinic count cannot determine request throughput. We also need operating days, visits, staff behavior, requests per action and when demand occurs. Response time, correctness and recovery are separate: a fast request can create an incorrect booking, and a successful queue claim can precede a failed external effect.

Use four labels throughout this chapter:

| Label | Meaning | Suitable use |
| ---------------- | -------------------------------------------------- | --------------------------------------------------- |
| Assumption | Invented workload input | Scenario design and sensitivity analysis |
| Calculation | Arithmetic from stated inputs | Explaining expected load, not measured capacity |
| Synthetic sample | Invented before/after observations | Learning metric definitions and interview reasoning |
| Proposed target | Acceptance goal still requiring tests or telemetry | Planning; never describe as already achieved |

## Start With One Consistent Clinic Month

Assume 26 operating days per month, an eight-hour working day and an equal clinic mix. Real clinics may differ substantially; this simplification must be replaced by a distribution when measured data exists.

| Quantity | Scenario input or formula | Hypothetical result | Meaning and boundary |
| ----------------------------------- | --------------------------------------------- | -------------------: | ------------------------------------------------------------------------------------------------------------------------ |
| Active clinics | Assumption | 25 | Active means at least one completed appointment in the reporting month |
| Staff accounts | 8 per clinic | 200 | Accounts, not concurrent users or daily active users |
| Completed appointments | 40 per clinic-day | 26,000/month | 25 × 40 × 26; cancellations are excluded from this denominator |
| Completed appointments per day | 25 × 40 | 1,000 | Across the modeled clinics, not per clinic |
| Appointment-linked API requests | 20 per completed appointment | 520,000/month | Includes modeled reads/writes; excludes public browsing and other background traffic |
| Interactive average | 20,000 requests/day ÷ 28,800 seconds | 0.69 requests/second | Average across working hours; not peak load or benchmark throughput |
| Busy-window request rate | 30% of daily requests in 30 minutes | 3.33 requests/second | 6,000 ÷ 1,800; the remaining 70% occur outside this window |
| Brief stress-test burst | Proposed test at 10× busy-window rate | 33.3 requests/second | Artificial headroom exercise, not an observed peak |
| Prescription records | 80% of completed appointments | 20,800/month | Additional assumption: one prescription record per qualifying visit; separate from successful PDF output |
| Prescription PDFs | One PDF per modeled prescription | 20,800/month | Additional artifact assumption; revisions, retries and failed generation excluded |
| Invoices created | One invoice per completed appointment | 26,000/month | Additional billing assumption; this does not count paid invoices or collected revenue |
| Distinct clinic-patients seen | 26,000 visits ÷ 1.3 visits per clinic-patient | 20,000/month | Additional repeat-visit assumption; distinct clinic/patient pairs, not new registrations or globally deduplicated people |
| PDF arrivals in a synchronized hour | 80% of daily PDF work in one hour | 640/hour | 800 daily PDFs × 80%; independent stress assumption |
| Messages | 2 per completed appointment | 52,000/month | Attempts intended by the product; delivery and consent need separate accounting |
| Online payment attempts | 20% of appointments, one attempt each | 5,200/month | Attempts are not captured or settled payments |
| Stored PDFs | 20,800 × 150 KiB each | 2.98 GiB/month | Payload-only estimate; excludes replicas, backups, revisions and other uploads |
| PDF retention | 12 identical modeled months | 35.7 GiB | Capacity assumption, not a clinical retention policy |

Trace one visit through booking, record updates, prescription, invoice and optional payment. Count the requests and jobs from that trace rather than treating “20 requests” as a fact about the implementation. A cancelled visit, retried webhook or document revision follows a different path.

### Check the Queue Before Claiming Headroom

The queue has a two-second polling interval, claims one job per poll per registered name, and prevents overlapping polls for that name inside one instance. The outbox relay has a five-second schedule and a nominal batch cap of 200. A 28 October source refresh at `f3fddffc0` confirms that RLS limits its effective batch to the configured pool size minus two: a 15-connection pool produces a cap of **13**. These are code/configuration facts, not performance measurements.

For an idle, immediately completing single job-name lane, the poll setting gives an idealized upper bound of 1,800 starts/hour. Actual throughput is lower when handler duration, scheduling, database work or contention delays the next claim. Separate names and worker instances change the model; they do not automatically fix idempotency or recovery.

The invented 640 PDFs/hour average in the busy hour is about 0.178 arrivals/second. A 1,000-job burst would need at least about 33 minutes to start its last job in the idealized single-lane model, before accounting for execution time. Therefore the normal-hour average cannot justify a short burst completion SLA.

Without the RLS pool cap, 200 rows every five seconds is an idealized relay selection rate of 40 rows/second. With the checked-in RLS configuration and a 15-connection pool, 13 rows per five-second tick would instead be 2.6 selections/second before handler time, scheduling and contention. Neither value is downstream delivery throughput. The 9 October source recheck shows the relay now awaits promises returned by process-local listeners under a 30-second timeout. Missing listeners, suppressed errors, detached work and uncancelled timeouts still limit what that acknowledgment proves. Read [async processing](03-async-processing.md) before attaching a completion target to either mechanism.

## Translate Monthly Totals Into an Arrival Pattern

The month establishes business volume. It does not select CPU or prove that a short synchronized burst will complete on time.

```text
25 clinics x 40 completed visits/day x 26 operating days
                         |
                         v
              26,000 completed visits/month
                         |
             assumed 20 API requests/visit
                         v
                 520,000 requests/month
                         |
       +-----------------+--------------------------+
       |                 |                          |
       v                 v                          v
24-hour month       8-hour working day         30-minute busy window
~0.20 req/s         ~0.69 req/s                ~3.33 req/s
                                               |
                                      artificial 10x headroom
                                               v
                                           ~33.3 req/s
```

The 0.20 rate divides by all seconds in an illustrative 30-day month; the working-hour rate divides daily activity by eight hours. These answer different questions and must not be interchanged. The busy window contains 30% of the 20,000 daily requests. The headroom phase adds demand; it does not belong in the ordinary day's activity total.

Two hundred staff accounts do not establish 200 simultaneous users. Record login sessions, active interactions and in-flight requests separately. For a stable system, a useful first estimate is Little's Law: mean in-flight requests approximately equals admitted requests/second multiplied by **mean** time in the system. With an invented 80 ms mean, 3.33 requests/second implies about 0.27 requests in flight on average. Do not substitute P95 into that mean relationship or use it to dismiss bursts, waiting queues or timeouts.

Use distributions rather than one identical clinic: several quiet clinics, a few busy clinics, a disproportionately active tenant and a synchronized opening hour. A noisy tenant can monopolize database connections even when the global average looks small. Observe per-tenant wait, denials and completion, while keeping patient identity out of artifacts.

## Put a Connection Budget Around Autoscaling

The source production Prisma pool permits 15 connections per process. `getReadClient()` currently returns the same client; its name does not establish a separate read replica. RLS can retain a transaction/connection for the whole request, including time spent waiting on work outside a SQL query.

```text
API replicas x 15  ----+
                      |
Worker processes x 15 +--> application connection envelope
                      |
Old/new deploy overlap+
                      |
Migrations/admin/reserve-------------------------------+
                                                      v
                         <= effective database/session budget
```

One API plus one worker starts with a nominal 30-connection envelope. A blue-green overlap of two API processes and one worker makes it 45 before operational reserve. The future balanced example of two APIs plus one worker also makes it 45; overlapping a third API raises it to 60. These are upper-bound pool budgets, not observed simultaneous SQL work. Count any additional instantiated client separately, and inspect provider-reserved connections and the actual pooler mapping.

The API proxy's soft/hard request thresholds of 60/100 per machine are not database connection limits. Some requests use no database session; others wait for one or hold it through an RLS transaction. Measure acquisition wait, active/idle sessions, transaction age and rejected work. Raising `max_connections` consumes database resources and cannot create CPU or I/O capacity.

A future shared cache, shared rate limiter or socket adapter needs its own correctness tests. Replica-local state does not become shared when the machine count increases. Start with the [deployment profile](10-deployment-infrastructure.md#keep-the-cheap-deployment-and-future-balanced-reference-distinct) and change one capacity dimension at a time.

## Separate Data Growth From File and Telemetry Growth

Twenty thousand clinic-patients seen in a month are not necessarily 20,000 new patient rows. A returning patient reuses stored identity. Appointment, prescription, medication-item, invoice-item, audit and job rows have different growth and retention rules.

```text
Completed visit
  +--> PostgreSQL rows: appointment / prescription / invoice / child items
  |          +--> indexes and TOAST within relation storage
  |          +--> WAL, temporary work and maintenance headroom
  |          +--> backup/replica copies under their own retention policy
  |
  +--> R2 objects: prescription PDF / optional invoice PDF / uploads
  |
  +--> Request/audit/job observations under separate retention and privacy rules
```

Measure average row and index cost on a representative populated fixture, including skew and history. `pg_total_relation_size` includes indexes and TOAST; measure its components without double-counting them. Row count multiplied by a guessed JSON size is insufficient for allocated disk.

Here are **illustrative calculations**, not Docita storage measurements:

| Item | Additional assumption | Calculation |
| ----------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Appointment relation growth | Measured fixture would show 3 KiB/appointment including its index share | 26,000 × 3 KiB ≈ 76.2 MiB per modeled month |
| Request observations | 1 KiB per retained request before index overhead | 520,000 × 1 KiB ≈ 0.496 GiB for the modeled customer month |
| Prescription PDF payloads | One 150 KiB PDF per prescription | 20,800 × 150 KiB ≈ 2.98 GiB/month |
| Optional invoice PDF payloads | Every modeled invoice also creates a 150 KiB PDF | 26,000 × 150 KiB ≈ 3.72 GiB/month |
| Both PDF families | Both artifact assumptions above hold | About 6.69 GiB/month, before revisions, backups and other uploads |

Replace the assumed per-record sizes with measured fixture values before sizing infrastructure. The 3 KiB row/index figure is a hypothetical input even though the calculation describes what a measured value would enable. Existing 30-day telemetry cleanup means live retained volume is not an unlimited monthly accumulation, but deletes and vacuum do not necessarily shrink the filesystem immediately. Audit and clinical retention must follow their own rules.

At a configured 15-second interval, one continuously checked machine could receive about 172,800 health-check requests in 30 days. That is a scheduling calculation, not observed traffic; the machine may be stopped, and checks can fail or be absent. Separating probes from customer observations is therefore essential to both volume and latency interpretation.

Before adopting the future 50 GiB database allocation, measure the starting history, data/index growth, vacuum/bloat, WAL and temporary peaks, free-space trend and restore workspace. Keep provider-allocated storage, database-used bytes, object-store bytes and backup bytes in different columns.

## Use Outcome Metrics With Explicit Denominators

The sample observations below are **invented before/after datasets**, not results of running Docita. Their purpose is to teach calculation and measurement design. In the table, p95 means the 95th percentile: the value at or below which about 95% of eligible observations fall. No performance change, user study or availability observation has been executed for this chapter.

| Outcome | Synthetic before → after or proposed target | Calculation or definition | Evidence required for an actual claim |
| -------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Reception booking time | Synthetic median 180 → 90 seconds | 50% lower median task time | Same start/end, task mix and participant context; raw timings and sample size |
| Invoice preparation time | Synthetic median 120 → 45 seconds | 62.5% lower median task time | Equivalent invoices, payment handling and correction scope |
| Illustrative booking labor | Synthetic mean 180 → 90 seconds, one task per visit | 26,000 × 90 ÷ 3,600 = 650 staff-hours/month | Mean saving must be measured separately from median; do not multiply medians into labor totals |
| Illustrative invoice labor | Synthetic mean 120 → 45 seconds, one task per visit | 26,000 × 75 ÷ 3,600 ≈ 542 staff-hours/month | Confirm every visit requires that task; no overlap with booking-time measurement |
| Appointment-list API latency | Synthetic pooled p95 800 → 350 ms | (800 − 350) ÷ 800 = 56.25% lower p95 | Same endpoint, filters, dataset, request mix, environment, cache state and load |
| Appointment-list failures | Proposed <1% eligible requests | Failed eligible requests ÷ all eligible requests | Define timeout/5xx rules and intentional denials; retain numerator and denominator |
| API availability | Proposed 99.9% over a 30-day observation | Time-based budget: 43.2 minutes unavailable | External observation and explicit scope; this time-based budget is not a request-error budget |
| PDF completion delay | Proposed p95 <60 seconds under modeled ordinary load | Durable enqueue to available artifact | Full pipeline timestamps; report terminal failures and outstanding work separately |
| Provider-message delivery | Synthetic 50,960 delivered of 52,000 eligible messages | 98% within 24 hours of each eligible message intent | Provider delivery receipts, unique logical-message IDs, consent and final statuses |
| Automatic payment reconciliation | Synthetic 5,174 of 5,200 eligible captured payments | 99.5% matched within five minutes of capture | Separate captured-payment dataset; do not substitute the payment-attempt estimate above |
| Duplicate financial effects | Proposed 0 in defined replay/concurrency checks | Number of extra business effects, not duplicate HTTP requests | Real database constraints, stable effect keys and provider sandbox reconciliation |
| Queue recovery time | Proposed p95 <15 minutes in restart drills | Failure injection to confirmed effect completion | Scenario, backlog, stale timeout, claim ownership and external-effect evidence |
| Restore capability | Proposed RPO ≤24 h; RTO ≤60 min | Acceptable lost-data interval; incident-to-verified service restoration | Backup schedule alone is insufficient; timed restoration with integrity checks |
| Deployment recovery | Proposed rollback ≤15 minutes in rehearsal | Decision to restored compatible application state | Migration compatibility, old/new version overlap and actual drill timestamps |
| Tenant isolation | Proposed 0 unauthorized reads/writes in the named matrix | Violations across roles, queries, workers and pooled connections | Real database roles/policies and adversarial two-tenant tests; no universal “zero leaks” claim |

Treat p95 as a quantile of the eligible request distribution, not the average of per-clinic p95 values. Compute it from pooled observations or mergeable distribution data with compatible boundaries. Keep median task improvement separate from mean labor saving. A target missed by the current code is useful evidence for a design decision, not a reason to relabel it as achieved.

## Connect Every Case to a Measurement and Its Current Boundary

This table maps all existing cases to the model without duplicating their mechanisms. A listed metric is a **measurement proposal**, not proof that its instrumentation already exists.

| Current case | Practical metric to investigate | Current implementation boundary and acceptance evidence |
| ------------------------------------------------------------------ | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [01 Architecture](01-architecture-decisions.md) | Lead time from approved change to compatible release | A shared commit is not atomic deployment; record version overlap and migration compatibility |
| [02 Tenant isolation](02-multi-tenancy-rls.md) | Unauthorized effects in a two-clinic access matrix | Staged policy settings and transaction routing matter; execute real-role and pooled-connection probes |
| [03 Async work](03-async-processing.md) | Backlog age, completion delay, duplicate effects | Completed-job lookup, claim ownership and conditional listener acknowledgment leave gaps; exercise effect/ack crash windows and non-cancelled timeouts |
| [04 Payments](04-payment-flows.md) | Captured payments reconciled; unresolved amount and age | Merchant ownership and idempotency need end-to-end verification; reconcile authoritative provider records |
| [05 Clinic workflows](05-clinic-workflows.md) | Booking time; accepted conflicting reservations | A pre-save availability check does not own capacity; race distinct requests for the same resource |
| [06 WhatsApp](06-whatsapp-integration.md) | Delivered eligible messages; provider delay and cost | Accepted enqueue/send is not delivery; use callback receipts, consent and retry evidence |
| [07 Prescriptions](07-prescription-safety.md) | Time to reviewed prescription and ready PDF | Generated output does not prove clinical correctness; separate clinician review from document execution |
| [08 Billing](08-billing-invoicing.md) | Invoice task time; discrepancies after corrections | Financial values and lifecycle need authoritative amounts and transition tests |
| [09 Subscriptions](09-subscription-system.md) | Entitlement propagation delay after confirmed payment | Local subscription state is not proof of provider settlement or correct authorization at every path |
| [10 Deployment](10-deployment-infrastructure.md) | Observed availability, restore time and rollback time | Configuration is not an executed recovery drill; prove data integrity and mixed-version behavior |
| [11 Insurance](11-insurance-claims.md) | Time to valid submission; rejected/reworked claims | Current state/version ownership needs verification; race transitions and inspect audit evidence |
| [12 Inpatient](12-ipd-inpatient.md) | Bed allocation time; conflicting active allocations | Guarded capacity and coordinated transitions need competing transaction tests |
| [13 Inventory](13-inventory.md) | Stock discrepancies; replenishment task time | Unit meaning and concurrent movement matter; reconcile a known ledger and compete writes |
| [14 Analytics](14-analytics-and-dashboards.md) | Dashboard freshness and financial reconciliation error | Timezone, bucket and historical-price limitations require fixture checks before benchmarking |
| [15 Public booking](15-doctors-verification-and-public-booking.md) | Funnel completion; unauthorized confirmations | Verification and anonymous entry boundaries need scope/rate checks; define eligible starts and completions |
| [16 Patient portal](16-patient-portal.md) | Patient task completion and cross-patient denials | Identity binding and authorized resource reads need separate fixtures and session tests |
| [17 ABDM](17-abdm-integration.md) | Completed consent-bound transfers; callback completion delay | Source integration is not live ecosystem approval or production success; use approved sandbox evidence |
| [18 Enterprise](18-enterprise-contracts.md) | Group invoice reconciliation and override consistency | Contract overrides need effective-date, membership and entitlement fixtures |
| [19 Uploads](19-documents-and-uploads.md) | Upload-to-authorized-availability delay; orphaned objects | Metadata persistence is not a complete storage lifecycle; test authorization, failed finalization and cleanup |
| [20 Clinical/lab/coding](20-clinical-lab-and-medical-coding.md) | Order-to-reviewed-result time; unmatched results | Ownership, status, mapping and external dependencies need known fixtures and human validation |
| [21 Smaller domains](21-long-tail-domains.md) | Reminder delivery, webhook backlog, leave transition conflicts | Claim recovery, placeholder signing and transition ownership gaps prevent blanket reliability claims |
| [22 Improvements](22-what-id-do-differently.md) | Failure rate before/after one implemented correction | Recommendations are not completed fixes; reproduce the failure, change one boundary and rerun it |

## Collect a Metric Without Losing Its Meaning

For each operational metric, retain: definition/version, UTC observation window, clinic-local timezone where relevant, eligible population, sample size, numerator/denominator or raw distribution, exclusions, source revision/deployment, environment, collection method, result and known missing data.

Prefer existing safe identifiers and aggregated telemetry. Operational measurement must not export patient names, diagnoses, documents or secrets into generic logs or interview artifacts. Tenant identifiers and operation IDs can still be sensitive; use approved sanitized evidence.

A booking-time study needs observed task timings, not just API logs. A backend benchmark needs controlled request distributions and enough observations to show tail behavior. Provider outcomes require provider receipts and reconciliation. Adoption requires dated product records with an explicit active-clinic definition. These are distinct evidence paths.

### A Worked Hypothetical Evidence Card

| Field | Synthetic example |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| Claim under investigation | Appointment-list p95 improved from 800 to 350 ms |
| Status | Invented illustration; not measured or resume-ready |
| Operation | Same clinic-scoped list endpoint, page size, filters and authorization |
| Proposed setup | Identical synthetic 12-month dataset and infrastructure; fixed request mix and cache protocol |
| Proposed comparison | Run both revisions after defined warm-up; record errors, load and raw timings; repeat runs |
| Calculation | 450 ms lower; 56.25% relative reduction from the 800 ms baseline |
| Confounders to control | Dataset, concurrent work, cache state, database settings, connection pools and network location |
| Required conclusion | Report the observed result and variation; do not force the invented values onto the experiment |

### Turn the Model Into a Reproducible Benchmark

Start with synthetic tenant aliases and a fixed seed: 25 clinics, 200 staff accounts and 26,000 completed appointments distributed across the stated 26-day month. Record the distribution of appointment times, statuses and record sizes; identical row counts can produce different query plans. Keep this fixture in an isolated environment, with simulated messages and payments. It must not enter operational adoption totals.

Run the normal busy window separately from the headroom experiment. The modeled busy window contains 6,000 interactive requests over 30 minutes; spread the other 14,000 across the remaining working hours if replaying a whole day. A brief 33.3-request/second stress run adds artificial demand and must not be counted as the same normal day. State whether the generator maintains an arrival rate or waits for each response before starting more work: a slow closed-loop client can reduce offered load and hide overload.

Retain a small evidence bundle rather than one screenshot:

| Artifact | What another engineer must be able to check |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scenario manifest | Seed, fixture counts/distribution, request mix, offered-load schedule, duration, resource limits, cache protocol and exact application/database versions |
| Correctness checks | Tenant/role matrix, expected rows and totals, conflicting-booking result, duplicate logical effects and outstanding work; successful HTTP responses alone are insufficient |
| Request and job observations | Scenario/run ID, sanitized operation identity, start/end timestamps and final outcome; retain failures, timeouts and unfinished work alongside successful latency samples |
| Comparison report | Same measurement boundaries for both revisions, warm-up policy, repeated runs, sample counts, raw-result checksums, observed variation and the actual calculation |

Give each run a fresh output directory and retain the command, tested revision and tool assistance. An assistant's reference run proves only what that run exercised; independent explanation and a changed-case rerun establish the learner's own performance. The benchmark may show a slower result, an unmet target or an invariant failure. Those are results to explain, not values to replace with the illustration above.

### Establish Real Adoption Through a Different Query

To investigate an actual active-clinic count, use a defined half-open reporting month, count distinct authorized clinic identities with at least one eligible completed appointment, and exclude synthetic/demo clinics and any records excluded by that definition. Retain the query/version, cutoff, exclusion rules, source environment and a privacy-safe aggregate. Reconcile a sample against the underlying operational records; a row created solely to reach a target count is not evidence of an operating clinic.

The same count cannot establish saved staff-hours or faster bookings. Those claims require their own task observations and comparable baseline. Keep detailed production extracts private; the public evidence can explain the method, scope and a permitted aggregate without exposing clinic or patient identities. Publishing this chapter is an explanation of the method, not independent confirmation of adoption or historical impact.

## Run a Capacity Experiment With a Declared Boundary

The reproducible runner is `loadtest/capacity.mjs` in the Docita repository. Its model and dry-run prepare an experiment; only observations from the selected real isolated API can measure that API. A local stub verifies the runner and must never be relabeled as Docita throughput.

```bash
# Inside the Docita repository; no request is issued by this command.
node loadtest/capacity.mjs --dry-run

# Validate the runner itself against local fixtures.
node --test loadtest/*.test.mjs
```

Use its README for the exact credential-file and phase options. Keep tokens in a private external file and use synthetic tenant aliases. The runner is intended for an explicitly isolated loopback API. It must reject remote production targets, unexpected redirects and unsafe credential/route input. A prepared target needs its own disposable database, correct application schema, synthetic tenant identities, real runtime RLS role and provider mocks. A token labeled `clinic-7` is not proof that its server-side identity belongs to that clinic; verify the association before load.

Use a small correctness experiment before load: one authorized read for each tenant, cross-tenant denials through the actual API, repeated patient visits, a conflicting booking and a duplicate logical payment. After load, inspect final business state and outstanding jobs rather than treating HTTP 200 as success for every asynchronous effect.

| Phase | Workload | Evidence to retain |
| ------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Fixture inventory | 25 synthetic clinics and an explicit historical dataset | Entity counts, tenant distribution, dates/statuses, seed/version and exclusion labels |
| Ordinary activity | Stated mixed routes at the modeled working-hour rate | Offered/started/completed requests, route/tenant counts, errors and resource trends |
| Busy window | Approximately 3.33 requests/second under the chosen mix | Endpoint-level latency, pool waits, lock/I/O pressure, fairness and unfinished work |
| Artificial headroom | Approximately 33.3 requests/second in a separate phase | Saturation onset, throttles, queue growth and recovery after arrivals stop |
| Cold versus warm | Separate resumed/cold and already-active processes/caches | First-request delay, cache state, CPU quota balance and resource limits |
| Recovery | Controlled worker interruption and replay on synthetic work | Claim ownership, eventual effects, duplicate/missing effects and backlog age |

For an initial tail-latency analysis, predeclare at least 1,000 eligible observations per reported route; ten thousand gives more observations in the last percentile. This is a sampling plan, not a confidence guarantee. Report the actual sample size and variability across repeated runs. A route with 20 samples has approximately one observation defining its P95 and cannot provide a stable characterization of a rare P99 tail. Never average P95 values from separate replicas; merge compatible raw observations or aggregatable distributions first.

Keep server-side customer observations and client timings separate. The current SQL reporting uses continuous interpolation; the soak/runner uses nearest rank. For three durations 100, 200 and 500 ms, the interpolated P95 is 470 ms while nearest rank returns 500 ms. Neither comparison proves a performance improvement unless the same boundary, workload, result definition and method are used on both revisions.

```text
Load plan -> scheduled arrivals -> started requests -> terminal outcomes
                   |                    |                   |
                   | generator lag      | in-flight         +--> latency samples
                   |                    |                   +--> failures/throttles
                   +--------------------+-------------------+--> unfinished work

Parallel observation:
  API RSS/heap/event-loop/CPU quota + DB pool/locks/I/O + queue age/completion
```

A closed-loop client that waits for a slow response before making another request can hide overload. An open-arrival generator must expose lag, scheduled-but-unstarted arrivals and in-flight limits. If the generator becomes the bottleneck, the run measures the generator as well as the application. Wait for or explicitly classify in-flight work when a phase ends.

Every result needs revision, command, environment, machine limits, database configuration, fixture, routes, offered/achieved rates, sample method/count, failures/timeouts, capture coverage and raw-artifact hashes. Record whether application memory/CPU limits matched Fly. A native developer-machine test cannot establish performance on a 512 MiB shared-CPU VM. Publish only a sanitized result and keep credential/patient material out of artifacts.

## Decide What the Repository Supports Today

| Question | Current support and remaining acceptance work |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Can the schema represent these workflows and volumes? | The clinic/patient/appointment/prescription/invoice relationships support the model. Confirm constraints and populated plans with representative data. |
| Are 25 clinics currently observed as customers? | This chapter uses an assumption; live adoption records were not collected. Demo/test exclusion requires an explicit rule. |
| Has this full workload met the published API targets? | No complete retained 25-tenant API capacity result is established here; target values must not fill the absent measurement baseline. |
| Are current VM sizes sufficient? | Their budgets are known; sustained CPU/RSS, burst, database and mixed-job experiments still decide sufficiency. |
| Do stopped resources perform current background work? | A stopped worker does not process jobs. Its lifecycle must match the product's promised schedule before active adoption. |
| Does adding replicas solve every bottleneck? | It multiplies connection demand and exposes local cache/rate/socket boundaries; test those before relying on horizontal growth. |
| What is an implemented improvement versus a measurement gap? | Correcting customer-sample SQL is an application repair. Missing real performance results remain missing until the experiment runs. |

## Choose the Next Experiment From the Risk

1. Seed two synthetic clinics and verify authorization with actual database roles before using the model as a scale demonstration.
2. Race separate bookings and financial transitions; confirm one valid resource allocation or financial effect where required.
3. Measure interactive requests with the modeled average, busy window and brief burst; keep dataset and cache conditions visible.
4. Exercise jobs under ordinary arrivals and a burst; crash after the external effect and before acknowledgment; reconcile duplicate and missing effects.
5. Reconcile provider callbacks, invoices and dashboard totals against a known fixture before interpreting latency or revenue figures.
6. Perform a compatible rollout and backup restoration drill, then report actual results against the proposed targets.
7. Observe product tasks and real adoption separately. Synthetic load cannot establish customer adoption or saved staff time.

This chapter specifies full application capacity and recovery experiments that have not been established here. The separate [known-volume SQL fixture](14-analytics-and-dashboards.md#verify-the-sql-at-a-known-monthly-row-volume) executes the aggregate on synthetic projected rows; it does not run that end-to-end workload. Existing unit, component and SQL checks remain evidence for their own assertions, outside the outcome metric table.

## When a Number Can Move Into a Resume

A number becomes eligible when an actual measurement or a reasonable, documented estimate supports it and the wording preserves its scope. Record your contribution and distinguish production, pilot, sandbox and benchmark results. “Measured in a controlled benchmark” must remain visible if that is the evidence available.

For this hypothetical exercise, say: “Assuming 25 clinics completing 40 appointments each on 26 operating days, I model 26,000 monthly visits. I would verify burst capacity and job completion separately.” This explains a design assumption; it does not claim Docita serves those clinics.

Do not describe the synthetic 50% task reduction, 56.25% p95 reduction, 98% delivery or 99.5% reconciliation as past achievements. If actual observations later differ, update the scenario comparison and the evidence card rather than constructing an answer around invented history.

## Summary

The 25-clinic assumption yields a coherent workload model, not measured business success. Useful metrics connect a specific operation to a defined population, observation window and outcome. Current code settings help select experiments; known transaction, acknowledgment, reporting and recovery boundaries must remain part of the explanation.

## See Also

- [Launch through growth](25-launch-to-growth.md) — clinic onboarding, operations and evidence gates from zero through 25+.
- [Monthly operating costs](26-monthly-operating-costs.md) — regional rates, resource hours, retention, provider fees and a complete budget worksheet.
- [Category revision](REVISION.md) — scenario calculations and measurement follow-ups.
- [Case-study index](INDEX.md) — read implementation mechanisms before this model.
- [Interview evidence pack](../../80-lanes-abroad-full-stack/80.17-docita-interview-evidence-pack.md) — assemble real source, check and outcome evidence.

## References

The original queue settings were checked on 2 October; relay acknowledgment was refreshed on 9 October at `dc5a97dc3`. A scoped 28 October refresh at canonical source `f3fddffc0` adds effective RLS batch/pool budgets, retry distinctions, workload/storage assumptions and the experiment protocol. Actual application improvements and executed checks are identified in their canonical chapters. This remains a workload model, not an adoption or full production-capacity audit.

- `apps/api/src/shared/modules/queue/postgres-queue.service.ts` — polling interval and default attempt budget.
- `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts` — batch size and acknowledgment path.
- `apps/api/src/shared/schedule/cron-schedules.ts` — outbox relay schedule.
