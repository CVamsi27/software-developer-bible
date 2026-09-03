# Core Metrics

> **1 file.** The three Core Web Vitals — LCP, INP, CLS — their thresholds, measurement, and optimization levers. Every senior frontend interview starts here.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Core Web Vitals](50.3.1.01-core-web-vitals.md) | LCP, INP, CLS — measurement, thresholds, optimization strategies. INP replaced FID in 2024. | 30 min |

---

## Memorize the thresholds

| Metric | What it measures | Good |
| ----------------------------------- | --------------------------------------------------- | ------- |
| **LCP** (Largest Contentful Paint) | Loading — when the main content paints | ≤ 2.5s |
| **INP** (Interaction to Next Paint) | Responsiveness — worst-case interaction delay (p75) | ≤ 200ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — unexpected layout movement | ≤ 0.1 |

---

## Why this is its own category

Everything downstream (Performance APIs, profiling, RUM, budgets) exists to move these three numbers. If you can state the metrics, thresholds, and one concrete fix for each, you pass the screening question; the rest of this stack is how you go deeper.

---

## Cross-References

- [Measurement](../02-measurement/INDEX.md) — the APIs and tools that capture these numbers.
- [Optimization & Governance](../03-optimization-and-governance/INDEX.md) — keeping them in budget over time.

---

## Navigation

[↑ Performance Home](../INDEX.md) · [Next: Measurement →](../02-measurement/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| Web Vitals ingestion service | `apps/api/src/shared/modules/monitoring/monitoring/services/web-vitals-metrics.service.ts` |
| Metrics aggregation | `apps/api/src/shared/modules/monitoring/monitoring/services/metrics-aggregation.service.ts` |
| Field-data reporting endpoint | `apps/api/src/shared/modules/performance/performance.controller.ts` |
| Vitals budget check | `scripts/perf/check-web-vitals-budget.mjs` |
