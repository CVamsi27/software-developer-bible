# Releases & Metrics

> **Study time:** ≈ 23 min of reading (3 files, ~8 min average).
> **3 files.** Shipping safely and measuring delivery: blue-green and canary deployments for controlled traffic exposure and compatible recovery, plus five current DORA delivery measures that tell you whether shipping actually got faster AND safer.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Releases-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Rolling updates are the default but not always enough: big-bang rollouts carry all-or-nothing risk, and "deploy = release" couples shipping code to exposing it to users. Blue-green retains a potential routing reversal; canary bounds exposure when routing and analysis are configured. Both require compatible data and observed recovery. Senior interviews treat these as the minimum bar for "how do you deploy?" answers.

---

## File Index

Read exposure/recovery mechanisms first, then learn to measure delivery outcomes with consistent identities. Complete the revision companion before interview practice.

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Blue-Green & Canary](40.3.3.01-blue-green-canary.md) | Blue-green swaps, canary traffic shifting, automated rollback on metrics, feature flags as decoupling | Important | Important | 7 min |
| 02 | [DORA Metrics & Delivery Performance](40.3.3.02-dora-metrics-delivery-performance.md) | Five measures (deployment frequency, change lead time, failed-deployment recovery time, change failure rate, deployment rework rate), honest instrumentation from CI + incident tools, benchmark bands, gaming pitfalls, error-budget link | Important | Important | 14 min |

---

## Cross-References

- [Build & Deploy](../02-build-and-deploy/INDEX.md) — pipelines that execute these releases
- [Observability Stack](../../../40-platform/40.4-observability/INDEX.md) — the metrics canary decisions depend on

---

## Navigation

[← Build & Deploy](../02-build-and-deploy/INDEX.md) · [↑ CI/CD Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

Source inspection on 2026-10-10 found deployment triggers paused. These are source-level implementation anchors; historical release notes and workflow comments do not prove current successful live runs.

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — releases and measures for real.

| Topic | Docita evidence |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Canary | `scripts/deploy/worker-canary-deploy.sh` checks a canary machine stays started before a rolling call; it does not measure HTTP request cohorts and uses two remote deploy calls |
| Health-gated rollouts | Fly checks gate deploys: `/api/health/live`, 240s `grace_period` |
| Release evidence | `docs/operations/releases/2026-08-06-p5-closure.md` fills a release-evidence checklist with measured facts (test counts, SLO baselines) |
| Latency SLOs in CI | `scripts/checks/api-latency-slos.mjs` + `check-api-latency-budget.mjs` enforce budgets as gates |
| Synthetic monitoring | `.github/workflows/synthetic-monitoring.yml` defines probes and records a historical manually-disabled note; current live scheduler state was not checked |
| DORA dashboards | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
