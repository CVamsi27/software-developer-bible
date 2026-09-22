# The 3 Pillars

> **Study time:** ≈ 58 min of reading (3 files, ~19 min average).
> **3 files.** Logs, metrics, traces — the three data types every observability system is built from. Each answers a different question; senior engineers know which pillar to reach for before opening a dashboard.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Pillars-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

- **Logs** answer "what happened at time T?" — discrete events with full context.
- **Metrics** answer "how is the system performing?" — cheap numerical time series for dashboards and alerts.
- **Traces** answer "where did the request spend its time?" — causal flow across services.

Interviews at scale-focused companies open with "compare logs, metrics, and traces" precisely because teams that only have logs debug production by grep. These three chapters make each pillar concrete: formats, storage, tooling (ELK, Prometheus/Grafana, Jaeger), and cost trade-offs.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Logging](40.4.1.01-logging.md) | Structured logging, log levels, centralized logging, ELK stack, retention and cost | 19 min |
| 02 | [Monitoring](40.4.1.02-monitoring.md) | Metrics, dashboards, Prometheus, Grafana, SLIs, cardinality | 20 min |
| 03 | [Tracing](40.4.1.03-tracing.md) | Distributed tracing, spans, trace context propagation, OpenTelemetry, Jaeger | 19 min |

---

## Cross-References

- [Advanced Telemetry](../04-advanced-telemetry/INDEX.md) — OpenTelemetry unifies all three pillars
- [SRE Targets](../03-sre-targets/INDEX.md) — metrics become SLIs, then SLOs, then alerts

---

## Navigation

[↑ Observability Home](../INDEX.md) · [Next: Errors & Health →](../02-errors-and-health/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — implements the pillars (honestly: no OTel).

| Topic | Docita evidence |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Metrics | `shared/common/utils/prom-metric-factories.ts` + monitoring services (`metrics-recording`, `metrics-aggregation`, `metrics-query`) persisted via a metrics repository |
| Logs | Pino structured logging via `observability/pino-options.factory.ts`; PHI scrubbed before emit (`phi-redactor.ts`) |
| Traces / errors | Sentry, bootstrapped in `apps/api/src/instrument.ts` — **not** OpenTelemetry (`@opentelemetry/core` is only a transitive pin) |
| Client-side pillar | RUM: `web-vitals-metrics.service.ts` + `monitoring-rum.controller.ts` ingest web vitals |
