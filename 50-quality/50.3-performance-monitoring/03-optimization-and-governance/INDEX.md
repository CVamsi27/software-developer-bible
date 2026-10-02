# Optimization & Governance

> **Study time:** ≈ 24 min of reading (3 files, ~8 min average).
> **3 files.** Turning measurement into action: bundle analysis to find what to cut, and performance budgets so the wins survive contact with feature development.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why governance, not just optimization

One-off optimization decays: every sprint adds bytes. Budgets convert "the site feels fast" into a CI-enforced contract — which is why interviewers love the question "how do you keep a fast site fast?"

---

## The 2 files

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Bundle Analysis](50.3.3.01-bundle-analysis.md) | Bundle size, tree shaking, code splitting, bundlephobia, source-map-explorer | 10 min |
| 02 | [Performance Budgets](50.3.3.02-performance-budgets.md) | `size-limit`, per-chunk budgets, CI enforcement, budgeting tiers | 12 min |

---

## The loop

```text
Measure (bundle report / RUM)
   → Find the offender (source-map-explorer)
      → Fix (code split, drop dep, tree-shake)
         → Enforce (size-limit budget fails the PR)
            → back to Measure
```

Budget tiers to remember: initial JS, per-route chunks, total CSS, third-party scripts, and metric-level budgets (LCP ms) via Lighthouse CI.

---

## Cross-References

- [Measurement](../02-measurement/INDEX.md) — Lighthouse CI executes metric-level budgets.
- [Build Tools](../../../40-platform/40.5-build-tools/INDEX.md) — bundler-side knobs for bundle size.

---

## Navigation

[← Measurement](../02-measurement/INDEX.md) · [↑ Performance Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Route budgets as config, not folklore | `scripts/perf/route-budgets.config.mjs` + `check-route-budgets.mjs` |
| Budget enforcement scripts (perf / vitals / a11y) | `check-perf-budget.mjs`, `check-web-vitals-budget.mjs`, `check-a11y-budget.mjs` under `scripts/perf/` |
| Breach alerting | `apps/api/src/shared/modules/monitoring/monitoring/listeners/ops-alert.listener.ts` + `ops-alert.service.ts` |
| SLOs written down | `docs/operations/SLOS.md` |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
