# SRE Targets

> **Study time:** ≈ 16 min of reading (3 files, ~5 min average).
> **3 files.** The SRE framework for reliability: define SLIs/SLOs with real error budgets, then alert in a way that pages humans only when it matters.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-SRE%20Targets-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

"99.9% availability" is meaningless until you pick an SLI (which requests count?), a window (over 30 days?), and consequences (what changes when the budget burns?). This category covers SLI/SLO/SLA distinctions and multi-window burn-rate math. Keep percentile objectives distinct from good-request ratios, then connect actionable user impact to an owner and response.

Quick distinction:
- **SLI** = Service Level Indicator (the metric, e.g., "99.5% of requests succeed")
- **SLO** = Service Level Objective (the target, e.g., "99.9% availability")
- **SLA** = Service Level Agreement (the contract, with consequences)

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [SLI / SLO / SLA](40.4.3.01-sli-slo-sla.md) | Reliability targets, error budgets, multi-window burn rates, SLO-driven alerting | Important | Important | 7 min |
| 02 | [Alerting](40.4.3.02-alerting.md) | Alert principles, PagerDuty, Alertmanager, runbooks, symptom vs cause alerts | Important | Important | 7 min |

---

## Cross-References

- [The 3 Pillars](../01-pillars/INDEX.md) — where SLI measurements come from
- [Production Engineering](../../../50-quality/50.4-production-engineering/INDEX.md) — incident response when budgets burn

---

## Navigation

[← Errors & Health](../02-errors-and-health/INDEX.md) · [↑ Observability Home](../INDEX.md) · [Next: Advanced Telemetry →](../04-advanced-telemetry/INDEX.md)

---

## Docita Anchor

Source-level examples from [Docita](https://github.com/CVamsi27/docita); a CI threshold or domain notification is not evidence of a measured production SLO or a working paging integration.

| Topic | Docita evidence |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Latency SLOs as CI gates | `scripts/checks/api-latency-slos.mjs` + `check-api-latency-budget.mjs` — performance regression thresholds; not a production eligible-request SLI |
| Web-vitals SLOs | `check:web-vitals:enforce` baseline regression gate; distinct from a production user population and window |
| Alerting | `ops-alert.service.ts` wired to domain events via listener; admin alert channel under `messaging/admin-alerts` |
| Runbooks for breaches | `docs/operations/playbooks/*` (DB exhaustion, upstream timeouts, queue backlog) |
| Synthetic probes | `.github/workflows/synthetic-monitoring.yml` — the source records a historical disabled status; current scheduling/delivery needs live verification |
| Burn-rate dashboards / PagerDuty | _No direct docita implementation yet._ |

## Learning Passes

1. Define the eligible user event, target and measurement window in the SLI/SLO chapter. Work the request-budget example before converting a time-based target to minutes.
2. Trace long and short windows into each independent alert policy. Then choose routing, ownership and a runbook.
3. Work the revision questions below before the stack interview bank.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
