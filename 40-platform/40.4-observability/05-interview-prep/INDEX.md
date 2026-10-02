# Interview Prep — Observability

> **Study time:** ≈ 18 min of reading (1 files, ~18 min average).
> **1 file, 50+ curated questions with answers.** The senior-differentiator drill: logs vs metrics vs traces is the opening question; SLO math and sampling strategy are the follow-ups.

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

50+ curated questions with answers, organized by difficulty. Work them after the content categories.

---

## Navigation

[← Advanced Telemetry](../04-advanced-telemetry/INDEX.md) · [↑ Observability Home](../INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — gives me true stories for these answers.

| Topic | Docita evidence |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| "Logs vs metrics vs traces?" | Pino JSON logs + Prom-style metric factories + Sentry tracing — and the honest tradeoff of skipping OTel |
| "Scrubbing PII from telemetry?" (healthcare!) | `phi-redactor.ts` + parity-enforced Sentry scrubbing gates in CI |
| "How do you set an SLO?" | API-latency and web-vitals budgets enforced as merge gates, not dashboards |
| "Alert fatigue?" | Symptom-driven ops alerts on domain events + runbook per failure class |
| OTel collector / eBPF stories | _No direct docita implementation yet._ |
