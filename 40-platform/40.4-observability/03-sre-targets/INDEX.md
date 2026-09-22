# SRE Targets

> **Study time:** ≈ 25 min of reading (2 files, ~12 min average).
> **2 files.** The SRE framework for reliability: define SLIs/SLOs with real error budgets, then alert in a way that pages humans only when it matters.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-SRE%20Targets-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

"99.9% availability" is meaningless until you pick an SLI (which requests count?), a window (over 30 days?), and consequences (what stops when the budget burns?). This category covers the measurement layer — SLI/SLO/SLA distinctions, multi-window burn-rate math — and the response layer: alerting principles, runbooks, and why paging on CPU is how on-call dies inside.

Quick distinction:
- **SLI** = Service Level Indicator (the metric, e.g., "99.5% of requests succeed")
- **SLO** = Service Level Objective (the target, e.g., "99.9% availability")
- **SLA** = Service Level Agreement (the contract, with consequences)

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [SLI / SLO / SLA](40.4.3.01-sli-slo-sla.md) | Reliability targets, error budgets, multi-window burn rates, SLO-driven alerting | 11 min |
| 02 | [Alerting](40.4.3.02-alerting.md) | Alert principles, PagerDuty, Alertmanager, runbooks, symptom vs cause alerts | 14 min |

---

## Cross-References

- [The 3 Pillars](../01-pillars/INDEX.md) — where SLI measurements come from
- [Production Engineering](../../../50-quality/50.4-production-engineering/INDEX.md) — incident response when budgets burn

---

## Navigation

[← Errors & Health](../02-errors-and-health/INDEX.md) · [↑ Observability Home](../INDEX.md) · [Next: Advanced Telemetry →](../04-advanced-telemetry/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — sets targets and alerts for real.

| Topic | Docita evidence |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Latency SLOs as CI gates | `scripts/checks/api-latency-slos.mjs` + `check-api-latency-budget.mjs` — budgets enforced, not just graphed |
| Web-vitals SLOs | `check:web-vitals:enforce` baseline gate (see release evidence doc P5.8) |
| Alerting | `ops-alert.service.ts` wired to domain events via listener; admin alert channel under `messaging/admin-alerts` |
| Runbooks for breaches | `docs/operations/playbooks/*` (DB exhaustion, upstream timeouts, queue backlog) |
| Synthetic probes | `.github/workflows/synthetic-monitoring.yml` |
| Burn-rate dashboards / PagerDuty | _No direct docita implementation yet._ |
