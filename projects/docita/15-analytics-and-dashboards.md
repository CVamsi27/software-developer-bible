# 15 — Analytics & Dashboards

> The read-model layer — per-metric factories, timezone-aware bucketing, 1-hour cache TTLs on the overview, daily persisted snapshots for history, and raw-SQL group-bys for the compliance/revenue breakdowns.

---

## Context

Clinics want to *see* their business: revenue trends, patient growth, appointment fill rates, top diagnoses, uncoded-visits compliance, demographics. The questions look simple but hide real problems:

- **Money must sum correctly across tax classes, CPT codes, and categories** — a `SUM` in float ruins revenue reports.
- **"Today", "this month", "last month" are timezone-relative** — a clinic's day starts in *its* timezone (IST for Indian clinics), not UTC; bucketing by UTC date mislabels every report.
- **Queries touch huge fact tables** (invoices, appointments, patients, prescriptions) and must not hammer the primary database — or the same query twice.
- **History must survive** — "what was our dashboard on 1 March?" is unanswerable from live tables alone; growth % comparisons need a frozen point-in-time record.
- **Per-clinic RLS applies to analytics too** — a clinic must never read another clinic's revenue through a shared aggregate.

**The problems:** (1) naive group-bys of clinical data produce SQL that's slow or wrong across tax/tier boundaries; (2) raw Prisma `groupBy` can't express every breakdown (e.g., revenue by CPT from a joined table); (3) live-only analytics make month-over-month growth drift as data changes.

---

## Decision 1: Per-Family Factories over One Fat Service

### What We Chose

Analytics is split into **four factory classes by metric family** behind a thin facade (`AnalyticsService`):

- `OperationalAnalyticsFactory` — overview, patient growth, appointment stats/metrics, demographics, uncoded visits.
- `FinancialAnalyticsFactory` — revenue trends, revenue by CPT code, by category, time series, revenue metrics.
- `ClinicalAnalyticsFactory` — top conditions / diagnoses trends.
- `SnapshotAnalyticsFactory` — daily persisted snapshots.

All factories share `BaseAnalyticsFactory`, which injects the read client (via an `ANALYTICS_PERSISTENCE_PORT`), the config service, and a cache manager.

### Why This Was Chosen

- **Each family has a different data shape and cadence** — financial metrics cross invoices/tax/CPT; operational metrics cross appointments/patients; clinical crosses prescriptions/diagnoses. Splitting by family keeps each file focused (single-responsibility), and the facade gives controllers one import.
- **Cache policy is per-factory** — the overview caches 1 hour; expensive time-series can differ.
- **Consistent base concerns** — read-replica access and date-range filtering live once in the base class (`addDateRangeFilter`), so every factory obeys the same "reads never touch the primary" rule.

### Alternatives Considered

- One `AnalyticsService` with 40 methods and raw queries inline — would have been a ~2k-line file where cache/read-replica/date conventions could drift per method.
- A dedicated analytics warehouse (ClickHouse/Materialize) — wildly over-provisioned for ~25 clinics; Postgres on a read replica with 1-hour cache TTLs is correct at this scale.

### Trade-offs

- **Five files instead of one** — more imports, but each is independently testable (`clinical-analytics.factory.spec.ts`, `financial-analytics.factory.spec.ts`, `operational-analytics.factory.spec.ts` all exist).
- **Cache invalidation is TTL-based** — a dashboard can be up to an hour stale after a data change; no write-through invalidation on invoice/appointment creation.

---

## Decision 2: Timezone-Aware Ranges + Client-Side Bucketing

### What We Chose

Every analytics call takes a `timezone` (defaulting to India) and computes ranges like `getMonthRange(now, { timezone })` — boundaries in the clinic's zone — before querying. Row bucketing for time series is done **in application code** using a shared `toISODateString(date, { timezone })` util rather than SQL `date_trunc`, because Prisma can't express per-row timezone conversion portably:

```typescript
// analytics/core/factories/operational-analytics.factory.ts (overview)
const cacheKey = `dashboard-overview-${clinicId}-${timezone}`;
...
const thisMonthRange = getMonthRange(now, { timezone });
const aggregates = await this.repository.getOverviewAggregates(clinicId, thisMonthRange, lastMonthRange);
```

Week/day bucket keys come from `period-bucket.util.ts` (`toAnalyticsPeriodKey`, `toTimeSeriesBucketKey`) — the same bucketing code tested in `period-bucket.util.spec.ts` and reused across factories so "monthly" means the same thing everywhere.

### Why This Was Chosen

- **Correctness first** — a UTC-midnight bucket would split a clinic's Saturday across two report days. Computing range bounds and date keys in the clinic's timezone is the only correct approach for a product whose customers live in one country (IST) but whose servers run UTC.
- **Reuse over duplication** — the timezone utils (`toISODateString`, month ranges) live in `@workspace/utils` and are shared with appointments/clinic-calendar code (e.g., `getClinicLocalDayUtcBounds`), so clinic-local "day" logic is consistent product-wide.

### Trade-offs

- **Bucketing in JS means fetching rows to bucket** — for a 30-day patient-growth chart the fetch is bounded by a date range, so it's fine; a multi-year daily time series would be slow and should move to SQL `date_trunc` with an explicit `timezone` argument.
- **The `timezone` param is trust-based** — a caller passing `Asia/Kolkata` vs `IST`-style junk is handled by shared utils, but the API doesn't validate clinic-vs-passed timezone match; a mismatch silently shifts "today".

---

## Decision 3: Raw SQL Group-Bys for Cross-Table Breakdowns

### What We Chose

Breakdowns that cross tables — revenue by CPT code, revenue by category, disease trends — use **targeted raw SQL** (`$queryRaw`) behind repository methods, with defensive row mappers that validate shapes instead of trusting column order:

```typescript
// analytics/infrastructure/repositories/analytics-groupby.helpers.ts
export function mapAppointmentStatusGroupRows(rows: unknown[]): Array<{ status: string; count: number }> {
  return rows.flatMap((row) => {
    if (!isRecord(row) || typeof row.status !== 'string') return [];
    return [{ status: row.status, count: readGroupCount(row, 'id') }];
  });
}
```

Where Prisma's typed `groupBy` suffices (status counts, gender), it is used (`analytics-groupby-count.ts`, `analytics-gender-groupby.ts`).

### Why This Was Chosen

- **Prisma `groupBy` can't do joined aggregations** (revenue requires invoice → line items → CPT). Raw SQL is the honest tool; the *results* are re-typed defensively so a schema drift fails loudly in the mapper, not silently in the UI.
- **Read-only discipline holds** — these run on the read client, never the primary.

### Trade-offs

- **Raw SQL escapes Prisma's type safety** — mitigated by small mappers + specs, but a schema change in a joined table needs a matching mapper update.
- **Each raw query is hand-tuned per Postgres** — portability to another dialect is not a goal.

---

## Decision 4: Daily Persisted Snapshots for History

### What We Chose

`SnapshotAnalyticsFactory.createAnalyticsSnapshot(clinicId)` computes one day's key numbers (total revenue, invoice count, avg invoice amount, appointment totals/fill rate, new vs active patients, top conditions) by *reusing the same factories* the live endpoints use, then persists a frozen `AnalyticsSnapshot` row and caches it under `snapshot-{clinicId}-{date}`.

### Why This Was Chosen

- **Same math, frozen in time** — because the snapshot calls the live factories, "yesterday's dashboard" and "the dashboard when it was yesterday" are computed identically; later data corrections don't rewrite history.
- **Growth reporting becomes trivial** — month-over-month patient growth compares snapshot rows, not live-vs-live queries that both changed.
- **An event announces each snapshot** (`ANALYTICS_SNAPSHOT_CREATED`) so other systems can react without polling.

### Alternatives Considered

- Live-only metrics — cheaper, but every "trend" recomputes from full history and month-over-month deltas drift as old data is edited.
- A full OLAP cube — overkill (see Decision 1).

### Trade-offs

- **Snapshots can go stale if the cron is missed** — a failed daily job leaves a gap that live queries can't backfill automatically (the pipeline reuses factories, so a manual re-run heals it).
- **`appointmentFillRate` is duplicated into `appointmentRate`** in the snapshot row — the same value under two names is a smell that says the metric taxonomy wasn't settled when the table was designed.

---

## Decision 5: Dashboard = Cached Stats, Analytics = Factories

### What We Chose

The `dashboards` domain stays deliberately tiny: `DashboardService.getStats(clinicId)` returns a single home-screen payload (total patients, today's appointments, active prescriptions, recent/upcoming activity) with a **60-second cache**, delegating the heavy numbers to `IDashboardRepository` and never duplicating analytics' per-metric endpoints.

### Why This Was Chosen

- **One round-trip for the landing screen** — the dashboard is the highest-frequency read in the product; a 60s cache keeps it off the database almost entirely.
- **No metric logic in the dashboard domain** — anything trend/revenue shaped lives in analytics; the dashboard only aggregates "right now" counts, so there's a single owner per number.

### Trade-offs

- **A 60s-stale landing screen** is invisible in practice but technically present — an appointment booked 5 seconds ago may not show for up to a minute.

---

## What Worked

- **Read-replica + 1-hour cache kept analytics nearly free** — the overview is one of the most-hit reads in the product and rarely touches the primary DB.
- **Snapshot consistency made growth reports trustworthy** — clinic owners could see "you grew 12% this month" computed from frozen rows, not shifting live data.
- **Defensive mappers caught real schema drift** — a renamed column in a group-by surfaced as an empty array + test failure, not a wrong total on a clinic owner's screen.

## What Failed

- **Compliance and revenue breakdowns live in a second controller** (`analytics-advanced.controller.ts`) alongside the overview controller — both mount on `/analytics`, and the route naming drifted (`/analytics/revenue-metrics` vs `/analytics/revenue/time-series`). Merging the two surfaces under one router with consistent verbs would remove the ambiguity.
- **Timezone bugs slipped through in week bucketing** — the first `toAnalyticsPeriodKey('weekly')` used a hand-rolled week-start that disagreed with the shared calendar util for clinics whose week starts on Monday (the ISO week) vs Sunday; the shared util is now the single source.

## What Could Be Better

- **Snapshot gap healing** — a "detect missing snapshot dates per clinic and re-run" reconciliation cron would remove the cron-miss failure mode.
- **Kill the `appointmentRate`/`appointmentFillRate` duplication** — pick one name in the snapshot type and migrate.
- **Move multi-year time series to SQL `date_trunc` with an explicit timezone argument** once any clinic's history exceeds ~2 years; JS bucketing won't scale there.
- **Add write-through cache invalidation** on the hot paths that change the overview (invoice finalization, appointment completion) instead of waiting out the TTL — a small event-listener on existing domain events.

---

## Code Evidence

| Claim | File |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Facade over four factories | `apps/api/src/domains/analytics/application/services/analytics.service.ts` |
| Base factory (cache/read/date) | `apps/api/src/domains/analytics/core/factories/base-analytics.factory.ts` |
| Operational factory (overview) | `apps/api/src/domains/analytics/core/factories/operational-analytics.factory.ts` |
| Financial factory | `apps/api/src/domains/analytics/core/factories/financial-analytics.factory.ts` |
| Snapshot factory | `apps/api/src/domains/analytics/core/factories/snapshot-analytics.factory.ts` |
| Period bucketing utils | `apps/api/src/domains/analytics/core/factories/period-bucket.util.ts` |
| Raw-SQL row mappers | `apps/api/src/domains/analytics/infrastructure/repositories/analytics-groupby.helpers.ts` |
| Overview + advanced controllers | `apps/api/src/domains/analytics/presentation/controllers/analytics-overview.controller.ts`, `analytics-advanced.controller.ts` |
| Dashboard stats + 60s cache | `apps/api/src/domains/dashboards/dashboard/application/services/dashboard.service.ts` |
| Timezone date utils (shared) | `packages/utils/src/date/iso-date-utils.ts` |

---

## Interview Script (60 seconds)

> "Analytics is a read-model split into per-family factories — operational, financial, clinical, and snapshot — all sharing a base that routes to the read replica and a cache manager. The dashboard overview caches for an hour, so one of the most-hit reads barely touches the database. Timezone correctness is handled the hard way: month/day ranges are computed in the clinic's own timezone and rows are bucketed in application code via shared utils, because Prisma can't do per-row timezone conversion — bucketing by UTC would split a clinic's Saturday across two report days. Cross-table breakdowns like revenue-by-CPT use targeted raw SQL with defensive row mappers. History is solved by daily persisted snapshots computed through the same factories the live endpoints use, so growth math never drifts as live data gets corrected. The known gap: snapshot gaps if the daily job is missed — the fix is a reconciliation cron."

---
