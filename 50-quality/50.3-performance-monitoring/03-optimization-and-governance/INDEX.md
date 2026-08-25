# Optimization & Governance

> **2 files.** Turning measurement into action: bundle analysis to find what to cut, and performance budgets so the wins survive contact with feature development.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality-green)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why governance, not just optimization

One-off optimization decays: every sprint adds bytes. Budgets convert "the site feels fast" into a CI-enforced contract — which is why interviewers love the question "how do you keep a fast site fast?"

---

## The 2 files

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Bundle Analysis](50.3.3.01-bundle-analysis.md) | Bundle size, tree shaking, code splitting, bundlephobia, source-map-explorer | 25 min |
| 02 | [Performance Budgets](50.3.3.02-performance-budgets.md) | `size-limit`, per-chunk budgets, CI enforcement, budgeting tiers | 20 min |

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
