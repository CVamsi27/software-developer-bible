# The 3 Pillars

> **Study time:** ≈ 21 min of reading (4 files, ~5 min average).
> **4 files.** Logs, metrics, traces — the three data types every observability system is built from. Each answers a different question; senior engineers know which pillar to reach for before opening a dashboard.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Pillars-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

- **Logs** answer "what happened at time T?" — selected events with safe context.
- **Metrics** answer "how is the system performing?" — cheap numerical time series for dashboards and alerts.
- **Traces** answer "where did the request spend its time?" — causal flow across services.

Interviewers often ask candidates to compare logs, metrics and traces. A strong answer chooses evidence for the question and explains cost and coverage limits instead of treating the signals as interchangeable. These chapters make each pillar concrete through formats, storage, tooling (ELK, Prometheus/Grafana, Jaeger) and trade-offs.

---

## File Index

Read one event log first, then aggregate request measurements, then connect timed operations into a trace. Complete revision before the separate observability interview bank.

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Logging](40.4.1.01-logging.md) | Structured logging, log levels, centralized logging, ELK stack, retention and cost | Important | Important | 6 min |
| 02 | [Monitoring](40.4.1.02-monitoring.md) | Metrics, dashboards, Prometheus, Grafana, SLIs, cardinality | Important | Important | 7 min |
| 03 | [Tracing](40.4.1.03-tracing.md) | Distributed tracing, spans, trace context propagation, OpenTelemetry, Jaeger | Important | Important | 6 min |

---

## Cross-References

- [Advanced Telemetry](../04-advanced-telemetry/INDEX.md) — OpenTelemetry unifies all three pillars
- [SRE Targets](../03-sre-targets/INDEX.md) — metrics become SLIs, then SLOs, then alerts

---

## Navigation

[↑ Observability Home](../INDEX.md) · [Next: Errors & Health →](../02-errors-and-health/INDEX.md)

---

## Docita Anchor

Current source inspected on 2026-10-10; these are implementation anchors, not a live exporter/backend or complete privacy audit.

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic | Docita evidence |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Metrics | `shared/common/utils/prom-metric-factories.ts` + monitoring services (`metrics-recording`, `metrics-aggregation`, `metrics-query`) alongside persisted application monitoring records; source still imports legacy prom-client, distinct from the maintained client used in this chapter |
| Logs | Pino structured logging via `observability/pino-options.factory.ts`; selected PHI fields/value patterns scrubbed by serializers/redaction (`phi-redactor.ts`); this is a scoped implementation, not proof that every free-text value is safe |
| Traces / errors | Sentry, bootstrapped in `apps/api/src/instrument.ts` — **not** OpenTelemetry (`@opentelemetry/core` is only a transitive pin) |
| Client-side pillar | RUM: `web-vitals-metrics.service.ts` + `monitoring-rum.controller.ts` ingest web vitals |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
