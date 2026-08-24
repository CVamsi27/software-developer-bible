# Observability — Index

> **9 files** — Observability fundamentals from logging and monitoring to distributed tracing, OpenTelemetry, error tracking, health checks, SLI/SLO/SLA, alerting, and interview questions.

[![Files](https://img.shields.io/badge/files-9-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Observability-%230ea5e9)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why observability:** "If you can't measure it, you can't improve it." Senior interviews at scale-focused companies test observability: logging, metrics, tracing, alerting, SLI/SLO, error budgets. OpenTelemetry is the vendor-neutral standard. This is the senior-differentiator stack.

---

## 🗂️ Topic Categories

The 3 pillars of observability + the SLO/error-budget framework.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [The 3 Pillars](#-the-3-pillars) | 3 | Logs, metrics, traces — the foundation |
| [Errors & Health](#-errors--health) | 2 | Error tracking, health checks — runtime quality |
| [Reliability Targets](#-reliability-targets) | 2 | SLI/SLO/SLA, alerting — SRE framework |
| [OpenTelemetry](#-opentelemetry) | 1 | The vendor-neutral standard |
| [Interview Prep](#-interview-prep) | 1 | 50+ Qs |

---

## 📊 The 3 Pillars

Logs, metrics, traces — the foundation of observability.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 01 | [Logging](40.4.01-logging.md) | Structured logging, log levels, centralized logging, ELK stack, log retention | "What happened at time T?" | 30 min |
| 02 | [Monitoring](40.4.02-monitoring.md) | Metrics, dashboards, Prometheus, Grafana, SLIs | "How is the system performing?" | 30 min |
| 03 | [Tracing](40.4.03-tracing.md) | Distributed tracing, spans, OpenTelemetry, Jaeger | "Where did the request spend time?" | 30 min |

**When to use what:**
- **Logs** = discrete events ("user X signed up at time T")
- **Metrics** = numerical time series ("CPU is at 80%")
- **Traces** = request flow across services ("this request took 200ms, with 150ms in service B")

---

## 🐛 Errors & Health

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Error Tracking](40.4.04-error-tracking.md) | Error aggregation (Sentry), source maps, alerting, release tracking | 25 min |
| 05 | [Health Checks](40.4.05-health-checks.md) | Liveness/readiness probes, health endpoints, dependency checks | 20 min |

---

## 🎯 Reliability Targets

The SRE framework.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [SLI / SLO / SLA](40.4.07-sli-slo-sla.md) | Reliability targets, error budgets, multi-window burn rate, SLO-driven alerting | 30 min |
| 08 | [Alerting](40.4.08-alerting.md) | Alerting principles, PagerDuty, Alertmanager, runbooks, what to alert on | 25 min |

**Quick distinction:**
- **SLI** = Service Level Indicator (the metric, e.g., "99.5% of requests succeed")
- **SLO** = Service Level Objective (the target, e.g., "99.9% availability")
- **SLA** = Service Level Agreement (the contract, with consequences)

---

## 🌐 OpenTelemetry

The vendor-neutral standard.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 09 | [OpenTelemetry](40.4.09-opentelemetry.md) | Vendor-neutral traces + metrics + logs, OTLP, W3C Trace Context, head/tail sampling, baggage, collector pipeline | 30 min |

---

## 🎤 Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Interview Questions](40.4.06-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## 🛣️ Suggested Study Order

1. **Logging + Monitoring** — the basics
2. **Tracing** — the senior differentiator
3. **Error Tracking + Health Checks** — production hygiene
4. **SLI/SLO/SLA + Alerting** — for SRE/staff roles
5. **OpenTelemetry** — modern standard
6. **Interview Questions** — final review

---

## 🔗 Cross-References

- [Kubernetes (Health Checks)](../40.2-kubernetes/INDEX.md) — K8s probe configuration
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — frontend observability
- [Production Engineering](../../50-quality/50.4-production-engineering/INDEX.md) — incident response, SLOs
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — observability in serverless

---

## Navigation

[← Previous: CI/CD](../40.3-ci-cd/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Build Tools →](../40.5-build-tools/INDEX.md)
