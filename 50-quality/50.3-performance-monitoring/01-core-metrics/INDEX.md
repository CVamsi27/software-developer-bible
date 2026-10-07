# Core Metrics

> **Study time:** ≈ 17 min of reading (2 files, ~8 min average).
> **1 file.** The three Core Web Vitals — LCP, INP, CLS — their thresholds, measurement, and optimization levers. Every senior frontend interview starts here.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Core Web Vitals](50.3.1.01-core-web-vitals.md) | LCP, INP, CLS — measurement, thresholds, optimization strategies. INP replaced FID in 2024. | Important | Important | 15 min |

---

## Memorize the thresholds

| Metric | What it measures | Good |
| ----------------------------------- | --------------------------------------------------- | ------- |
| **LCP** (Largest Contentful Paint) | Loading — when the main content paints | ≤ 2.5s |
| **INP** (Interaction to Next Paint) | Responsiveness — worst-case interaction delay (p75) | ≤ 200ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — unexpected layout movement | ≤ 0.1 |

---

## Why this is its own category

The later chapters explain how browser timing APIs, profiling tools, real-user monitoring (RUM), and performance budgets help diagnose and improve these three metrics. First learn each metric, its threshold, and one concrete way to improve it; then use the rest of this stack to investigate its causes in a real page.

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

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
