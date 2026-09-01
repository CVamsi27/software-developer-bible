# Optimization & Comparison

> **3 files.** Making builds fast and bundles small, shipping assets (CSS/images/fonts) through a real pipeline — then choosing tools with evidence instead of hype.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Optimization-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Tool choice gets debated endlessly; bundle size regressions ship silently. This category covers the mechanics that apply to every bundler (tree shaking, route-level code splitting, source maps, build caches), the asset pipeline that dominates real page weight (CSS transforms, image variants, fonts, fingerprinting), and a side-by-side tool comparison so you can justify the pick — the form senior interviews reward.

---

## File Index

| Order  | File                                                                                   | Topics                                                                                                                                                          | Read time   |
| --   : | ------                                                                                 | --------                                                                                                                                                        | ----------: |
| 01     | [Build Optimization](40.5.3.01-build-optimization.md)                                  | Tree shaking, code splitting (route/lazy), bundle analysis, caching, source maps                                                                                | 30 min      |
| 02     | [Asset Pipelines — CSS, Images & Fonts](40.5.3.02-asset-pipelines-css-images-fonts.md) | PostCSS/Lightning CSS chain, Tailwind compile path, sharp responsive sets, font subsetting + preload, content hashing, hidden source maps, Vite/webpack configs | 30 min      |
| 03     | [Build Tool Comparison](40.5.3.03-build-tool-comparison.md)                            | Webpack vs Vite vs Turbopack vs Rspack trade-offs, migration paths, when to use each                                                                            | 20 min      |

---

## Cross-References

- [Bundlers](../01-bundlers/INDEX.md) — the tools being optimized and compared
- [Performance Monitoring](../../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring real-user impact

---

## Navigation

[← Compilers](../02-compilers/INDEX.md) · [↑ Build Tools Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — keeps builds fast for real.

| Topic                           | Docita evidence                                                                                    |
| ------------------------------- | -------------------------------------------------------------------------------------------------- |
| Build caching                   | Turbo caches `build`/`test` outputs (`dist/**`, empty test outputs) keyed by scoped env allowlists |
| Dead-code elimination as a gate | `knip.json` + knip-clean requirement recorded in release evidence                                  |
| Duplication budget              | `check:duplication` (jscpd, zero clones) in pre-push and release evidence                          |
| Size budgets                    | `scripts/checks/check-file-size-budget.mjs` and `check-worker-size.mjs`                            |
| Tree-shaking / bundle analysis  | Not separately configured beyond toolchain defaults                                                |
