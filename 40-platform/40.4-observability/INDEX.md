# Observability — Index

> **Study time:** ≈ 1 h 30 m of reading (15 files, ~6 min average).
> **15 files** — Observability fundamentals from logging and monitoring to distributed tracing, OpenTelemetry, continuous profiling, eBPF, error tracking, health checks, SLI/SLO/SLA, alerting, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Observability-%230ea5e9)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

When a user journey degrades, define the affected population and symptom first. Metrics show how broadly it happens; traces locate time across dependencies; logs and error reports add event context. Health checks answer bounded routing or restart questions. The chapters connect those observations to objectives, alerts and recovery decisions, then add profiling and kernel-level evidence where the runtime and platform support them.

---

## Category Map

Start with the classic logs, metrics and traces signals, then connect their evidence to error tracking, health policy and service objectives. OpenTelemetry standardizes instrumentation and transport, while profiling and eBPF add runtime or kernel evidence with their own support and privacy limits.

| Category | Folder | Files | What it covers |
| ------------------ | -------------------------------------------------------- | ----: | ---------------------------------------------------------------- |
| The 3 Pillars | [01-pillars/](01-pillars/INDEX.md) | 3 | Logs, metrics, traces — the foundation |
| Errors & Health | [02-errors-and-health/](02-errors-and-health/INDEX.md) | 2 | Error tracking, health checks — runtime quality |
| SRE Targets | [03-sre-targets/](03-sre-targets/INDEX.md) | 2 | SLI/SLO/SLA, alerting — the SRE framework |
| Advanced Telemetry | [04-advanced-telemetry/](04-advanced-telemetry/INDEX.md) | 3 | OpenTelemetry, continuous profiling, eBPF — the advanced signals |
| Interview Prep | [05-interview-prep/](05-interview-prep/INDEX.md) | 1 | 50 Qs |

---

## The 3 Pillars

These three signals answer different investigation questions. Profiles add sampled evidence about code-level resource use in the advanced section.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Logging](01-pillars/40.4.1.01-logging.md) | Structured logging, log levels, centralized logging, ELK stack, log retention | "What happened at time T?" | Important | Important | 6 min |
| 02 | [Monitoring](01-pillars/40.4.1.02-monitoring.md) | Metrics, dashboards, Prometheus, Grafana, SLIs | "How is the system performing?" | Important | Important | 6 min |
| 03 | [Tracing](01-pillars/40.4.1.03-tracing.md) | Distributed tracing, spans, OpenTelemetry, Jaeger | "Where did the request spend time?" | Important | Important | 6 min |

---

## Errors & Health

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Error Tracking](02-errors-and-health/40.4.2.01-error-tracking.md) | Error aggregation (Sentry), source maps, alerting, release tracking | Important | Important | 6 min |
| 05 | [Health Checks](02-errors-and-health/40.4.2.02-health-checks.md) | Liveness/readiness probes, health endpoints, dependency checks | Important | Important | 7 min |

---

## SRE Targets

Define the eligible event, good outcome, target and window before writing alert rules. The revision questions check the budget arithmetic and how independent short/long alert policies behave.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [SLI / SLO / SLA](03-sre-targets/40.4.3.01-sli-slo-sla.md) | Reliability targets, error budgets, multi-window burn rate, SLO-driven alerting | Important | Important | 8 min |
| 07 | [Alerting](03-sre-targets/40.4.3.02-alerting.md) | Alerting principles, PagerDuty, Alertmanager, runbooks, what to alert on | Important | Important | 7 min |

---

## Advanced Telemetry

Follow the instrumentation-to-collection path, then select runtime or kernel profiling only for a question those signals can answer. Check supported versions, data loss, privileges and retention before treating the evidence as complete.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [OpenTelemetry](04-advanced-telemetry/40.4.4.01-opentelemetry.md) | Vendor-neutral traces + metrics + logs, OTLP, W3C Trace Context, head/tail sampling, baggage, collector pipeline | Important | Important | 9 min |
| 09 | [Continuous Profiling](04-advanced-telemetry/40.4.4.02-continuous-profiling.md) | Always-on CPU/heap/allocation sampling, Pyroscope/Parca, flamegraph diffing, span profiles | Important | Important | 8 min |
| 10 | [eBPF Observability](04-advanced-telemetry/40.4.4.03-ebpf-observability.md) | Kernel programs + verifier + maps, Hubble/Cilium flows, Pixie auto-telemetry, Falco/Tetragon overlap | Important | Specialized | 9 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 11 | [Interview Questions](05-interview-prep/40.4.5.01-interview-questions.md) | 50 curated questions with answers | Important | Important | 10 min |

---

## Suggested Study Order

1. **Logging + Monitoring** — the basics
2. **Tracing** — connect request work and dependencies
3. **Error Tracking + Health Checks** — production hygiene
4. **SLI/SLO/SLA + Alerting** — for SRE/staff roles
5. **OpenTelemetry** — modern standard
6. **Continuous Profiling + eBPF** — add when code-level or kernel evidence answers a remaining question
7. **Revision companions** — [Pillars](01-pillars/REVISION.md), [Errors and health](02-errors-and-health/REVISION.md), [SRE targets](03-sre-targets/REVISION.md), [Advanced telemetry](04-advanced-telemetry/REVISION.md)
8. **Interview Questions** — explain a trace, then change its conditions

---

## Cross-References

- [Kubernetes (Health Checks)](../40.2-kubernetes/INDEX.md) — K8s probe configuration
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — web performance measurement and service latency
- [Production Engineering](../../50-quality/50.4-production-engineering/INDEX.md) — incident response, SLOs
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — observability in serverless

---

## Navigation

[← Previous: CI/CD](../40.3-ci-cd/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Build Tools →](../40.5-build-tools/INDEX.md)
