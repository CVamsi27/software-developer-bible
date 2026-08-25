# Shipping & Evolution

> **2 files.** Change without breakage: deploying new versions with zero downtime, and paying down technical debt deliberately instead of drowning in it.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Shipping-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Shipping is not `git push` to prod. Users are mid-request while you deploy; schemas change under running code; yesterday's shortcut becomes next quarter's outage. Zero-downtime deployment patterns (blue-green, canary, expand/contract migrations) decouple deploys from risk, and a working technical-debt strategy keeps the codebase shippable years in.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Zero-Downtime Deployments](30.3.5.01-zero-downtime-deployments.md) | Rolling vs blue-green vs canary, expand/contract migrations, health-gated rollouts, rollback paths | 30 min |
| 02 | [Technical Debt](30.3.5.02-technical-debt.md) | Debt quadrants, intentional vs accidental debt, remediation strategy, communicating debt to stakeholders | 20 min |

---

## Cross-References

- [CI/CD Stack](../../../40-platform/40.3-ci-cd/INDEX.md) — pipelines that execute these deploy patterns
- [Blue-Green & Canary](../../../40-platform/40.3-ci-cd/03-releases-and-metrics/INDEX.md) — the platform-level implementation
- [Liveness & Lifecycle](../01-liveness-lifecycle/INDEX.md) — graceful shutdown makes zero-downtime possible

---

## Navigation

[← Data at Scale](../04-data-at-scale/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md)
