# Releases & Metrics

> **Study time:** ≈ 38 min of reading (2 files, ~19 min average).
> **2 files.** Shipping safely and measuring delivery: blue-green and canary deployments for zero-downtime releases with instant rollback, plus the four DORA metrics that tell you whether shipping actually got faster AND safer.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Releases-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Rolling updates are the default but not always enough: big-bang rollouts carry all-or-nothing risk, and "deploy = release" couples shipping code to exposing it to users. Blue-green gives instant rollback; canary gives graduated risk reduction backed by metrics. Senior interviews treat these as the minimum bar for "how do you deploy?" answers.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Blue-Green & Canary](40.3.3.01-blue-green-canary.md) | Blue-green swaps, canary traffic shifting, automated rollback on metrics, feature flags as decoupling | 20 min |
| 02 | [DORA Metrics & Delivery Performance](40.3.3.02-dora-metrics-delivery-performance.md) | Four keys (deployment frequency, lead time, MTTR, change-fail rate), honest instrumentation from CI + incident tools, benchmark bands, gaming pitfalls, error-budget link | 18 min |

---

## Cross-References

- [Build & Deploy](../02-build-and-deploy/INDEX.md) — pipelines that execute these releases
- [Observability Stack](../../../40-platform/40.4-observability/INDEX.md) — the metrics canary decisions depend on

---

## Navigation

[← Build & Deploy](../02-build-and-deploy/INDEX.md) · [↑ CI/CD Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — releases and measures for real.

| Topic | Docita evidence |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Canary | `scripts/deploy/worker-canary-deploy.sh` rolls the worker app gradually |
| Health-gated rollouts | Fly checks gate deploys: `/api/health/live`, 240s `grace_period` |
| Release evidence | `docs/operations/releases/2026-08-06-p5-closure.md` fills a release-evidence checklist with measured facts (test counts, SLO baselines) |
| Latency SLOs in CI | `scripts/checks/api-latency-slos.mjs` + `check-api-latency-budget.mjs` enforce budgets as gates |
| Synthetic monitoring | `.github/workflows/synthetic-monitoring.yml` probes the live deployment |
| DORA dashboards | _No direct docita implementation yet._ |
