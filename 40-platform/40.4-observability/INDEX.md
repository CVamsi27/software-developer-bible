# Observability — Index

> **Study time:** ≈ 3 h 11 m of reading (15 files, ~13 min average).
> **15 files** — Observability fundamentals from logging and monitoring to distributed tracing, OpenTelemetry, continuous profiling, eBPF, error tracking, health checks, SLI/SLO/SLA, alerting, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Observability-%230ea5e9)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why observability:** "If you can't measure it, you can't improve it." Senior interviews at scale-focused companies test observability: logging, metrics, tracing, alerting, SLI/SLO, error budgets. OpenTelemetry is the vendor-neutral standard. This is the senior-differentiator stack.

---

## Category Map

The 3 pillars of observability + the SLO/error-budget framework.

| Category | Folder | Files | What it covers |
| ------------------ | -------------------------------------------------------- | ----: | ---------------------------------------------------------------- |
| The 3 Pillars | [01-pillars/](01-pillars/INDEX.md) | 3 | Logs, metrics, traces — the foundation |
| Errors & Health | [02-errors-and-health/](02-errors-and-health/INDEX.md) | 2 | Error tracking, health checks — runtime quality |
| SRE Targets | [03-sre-targets/](03-sre-targets/INDEX.md) | 2 | SLI/SLO/SLA, alerting — the SRE framework |
| Advanced Telemetry | [04-advanced-telemetry/](04-advanced-telemetry/INDEX.md) | 3 | OpenTelemetry, continuous profiling, eBPF — the advanced signals |
| Interview Prep | [05-interview-prep/](05-interview-prep/INDEX.md) | 1 | 50+ Qs |

---

## The 3 Pillars

Logs, metrics, traces — the foundation of observability.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Logging](01-pillars/40.4.1.01-logging.md) | Structured logging, log levels, centralized logging, ELK stack, log retention | "What happened at time T?" | Important | 17 min | 16 min |
| 02 | [Monitoring](01-pillars/40.4.1.02-monitoring.md) | Metrics, dashboards, Prometheus, Grafana, SLIs | "How is the system performing?" | Important | 18 min | 18 min |
| 03 | [Tracing](01-pillars/40.4.1.03-tracing.md) | Distributed tracing, spans, OpenTelemetry, Jaeger | "Where did the request spend time?" | Important | 18 min | 18 min |

**When to use what:**
- **Logs** = discrete events ("user X signed up at time T")
- **Metrics** = numerical time series ("CPU is at 80%")
- **Traces** = request flow across services ("this request took 200ms, with 150ms in service B")

---

## Errors & Health

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Error Tracking](02-errors-and-health/40.4.2.01-error-tracking.md) | Error aggregation (Sentry), source maps, alerting, release tracking | Important | 20 min | 20 min |
| 05 | [Health Checks](02-errors-and-health/40.4.2.02-health-checks.md) | Liveness/readiness probes, health endpoints, dependency checks | Important | 19 min | 19 min |

---

## SRE Targets

The SRE framework.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [SLI / SLO / SLA](03-sre-targets/40.4.3.01-sli-slo-sla.md) | Reliability targets, error budgets, multi-window burn rate, SLO-driven alerting | Important | 9 min | 9 min |
| 07 | [Alerting](03-sre-targets/40.4.3.02-alerting.md) | Alerting principles, PagerDuty, Alertmanager, runbooks, what to alert on | Important | 13 min | 13 min |

**Quick distinction:**
- **SLI** = Service Level Indicator (the metric, e.g., "99.5% of requests succeed")
- **SLO** = Service Level Objective (the target, e.g., "99.9% availability")
- **SLA** = Service Level Agreement (the contract, with consequences)

---

## Advanced Telemetry

The vendor-neutral standard plus the advanced signals.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [OpenTelemetry](04-advanced-telemetry/40.4.4.01-opentelemetry.md) | Vendor-neutral traces + metrics + logs, OTLP, W3C Trace Context, head/tail sampling, baggage, collector pipeline | Important | 24 min | 23 min |
| 09 | [Continuous Profiling](04-advanced-telemetry/40.4.4.02-continuous-profiling.md) | Always-on CPU/heap/allocation sampling, Pyroscope/Parca, flamegraph diffing, span profiles | Important | 13 min | 13 min |
| 10 | [eBPF Observability](04-advanced-telemetry/40.4.4.03-ebpf-observability.md) | Kernel programs + verifier + maps, Hubble/Cilium flows, Pixie auto-telemetry, Falco/Tetragon overlap | Important | 14 min | 13 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 11 | [Interview Questions](05-interview-prep/40.4.5.01-interview-questions.md) | 50+ curated questions with answers | Important | 18 min | 18 min |

---

## Suggested Study Order

1. **Logging + Monitoring** — the basics
2. **Tracing** — the senior differentiator
3. **Error Tracking + Health Checks** — production hygiene
4. **SLI/SLO/SLA + Alerting** — for SRE/staff roles
5. **OpenTelemetry** — modern standard
6. **Continuous Profiling + eBPF** — advanced signals, staff-level
7. **Interview Questions** — final review

---

## Cross-References

- [Kubernetes (Health Checks)](../40.2-kubernetes/INDEX.md) — K8s probe configuration
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — frontend observability
- [Production Engineering](../../50-quality/50.4-production-engineering/INDEX.md) — incident response, SLOs
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — observability in serverless

---

## Navigation

[← Previous: CI/CD](../40.3-ci-cd/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Build Tools →](../40.5-build-tools/INDEX.md)
