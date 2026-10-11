# Interview Prep — Observability

> **Study time:** ≈ 10 min of reading (1 file, ~10 min average).
> **1 file, 50 curated questions with answers.** The senior-differentiator drill: logs vs metrics vs traces is the opening question; SLO math and sampling strategy are the follow-ups.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview%20Prep-%230ea5e9)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What's here

Questions across all four content categories:

- **Easy** — structured logging, log levels, what belongs on a dashboard
- **Medium** — trace propagation, cardinality mistakes, error tracking workflow, probe design
- **Hard** — SLO burn-rate alerting, head vs tail sampling trade-offs, building an observability strategy for a new service

---

## File Index

### [Observability Interview Questions](40.4.5.01-interview-questions.md)

50 curated questions with answers, organized by difficulty. Work them after the content categories and their source-linked revision companions. State the measurement population, explain one failure trace, then defend a decision.

---

## Navigation

[← Advanced Telemetry](../04-advanced-telemetry/INDEX.md) · [↑ Observability Home](../INDEX.md)

---

## Docita source anchors and claim boundaries

Local Docita source inspected on 10 October 2026 supplies implementation examples. Source presence is not proof of deployment, healthcare compliance or a measured service objective; use the dated [evidence walkthrough](../../../projects/docita/INDEX.md) for resume claims.

| Practice question | Source and boundary |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Logs, metrics and traces | Pino configuration, metric factories and Sentry instrumentation provide concrete paths; verify retained output and propagation before asserting coverage. |
| Sensitive telemetry | Redaction and scrubbing fixtures test named cases. They do not prove every clinical payload is scrubbed. |
| Reliability targets | CI performance budgets can block tested regressions; they are not a production request-based SLO or consumed error budget. |
| Alert operations | Inspect rule ownership, runbooks and actual delivery evidence separately from source configuration. |
| Collector and eBPF | No direct Docita implementation is claimed. |
