# Optimization & Governance

> **Study time:** ≈ 18 min of reading (3 files, ~6 min average).
> **3 files.** Turning measurement into action: bundle analysis to find what to cut, and performance budgets so the wins survive contact with feature development.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why governance, not just optimization

A page can become slower as each sprint adds more code and assets. A performance budget sets a measurable limit, and continuous integration (CI) checks enforce it before changes ship. This answers the interview question “how do you keep a fast site fast?”

---

## The 2 files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Bundle Analysis](50.3.3.01-bundle-analysis.md) | Bundle size, tree shaking, code splitting, bundlephobia, source-map-explorer | Important | Important | 8 min |
| 02 | [Performance Budgets](50.3.3.02-performance-budgets.md) | artifact and route budgets, CI enforcement, explicit units, valid inputs and exception ownership | Important | Important | 8 min |

---

## The loop

```text
Measure shipped assets and field outcomes
   → Attribute a surprising asset to its source modules
      → Change a dependency or loading boundary
         → Enforce the declared artifact budget
            → Recheck the affected journey in lab and field
```

Choose independent boundaries: initial JavaScript, route-loaded chunks, CSS, third-party scripts and user metrics such as field LCP. Use an appropriate gate for each measurement.

---

## Learning passes

1. Read bundle analysis and run the eager/lazy fixture. Explain both requested assets and export retention.
2. Read performance budgets and test a legitimate pass, an aggregate breach and missing inputs.
3. Close the chapters and complete [revision](REVISION.md) before the [interview bank](../04-interview-prep/50.3.4.01-interview-questions.md). State the measured boundary and its limits in each answer.

## Cross-References

- [Measurement](../02-measurement/INDEX.md) — Lighthouse CI executes metric-level budgets.
- [Build Tools](../../../40-platform/40.5-build-tools/INDEX.md) — bundler-side knobs for bundle size.

---

## Navigation

[← Measurement](../02-measurement/INDEX.md) · [↑ Performance Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to. The paths below are inspection pointers; verify their current code and results before claiming tested behavior.

| Topic | Docita evidence |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Route budgets as config, not folklore | `scripts/perf/route-budgets.config.mjs` + `check-route-budgets.mjs` |
| Budget enforcement scripts (perf / vitals / a11y) | `check-perf-budget.mjs`, `check-web-vitals-budget.mjs`, `check-a11y-budget.mjs` under `scripts/perf/` |
| Breach alerting | `apps/api/src/shared/modules/monitoring/monitoring/listeners/ops-alert.listener.ts` + `ops-alert.service.ts` |
| SLOs written down | `docs/operations/SLOS.md` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
