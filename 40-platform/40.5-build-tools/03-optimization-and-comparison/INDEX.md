# Optimization & Comparison

> **Study time:** ≈ 19 min of reading (4 files, ~5 min average).
> **4 files.** Making builds fast and bundles small, shipping assets (CSS/images/fonts) through a real pipeline — then choosing tools with evidence instead of hype.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Optimization-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Tool choice gets debated endlessly; bundle size regressions ship silently. This category covers the mechanics that apply to every bundler (tree shaking, route-level code splitting, source maps, build caches), the asset pipeline that dominates real page weight (CSS transforms, image variants, fonts, fingerprinting), and a side-by-side tool comparison so you can justify the pick — the form senior interviews reward.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Build Optimization](40.5.3.01-build-optimization.md) | Tree shaking, code splitting (route/lazy), bundle analysis, caching, source maps | Important | Specialized | 5 min |
| 02 | [Asset Pipelines — CSS, Images & Fonts](40.5.3.02-asset-pipelines-css-images-fonts.md) | PostCSS/Lightning CSS chain, Tailwind compile path, sharp responsive sets, font subsetting + preload, content hashing, hidden source maps, Vite/webpack configs | Important | Specialized | 8 min |
| 03 | [Build Tool Comparison](40.5.3.03-build-tool-comparison.md) | Webpack vs Vite vs Turbopack vs Rspack trade-offs, migration paths, when to use each | Important | Specialized | 4 min |

---

## Cross-References

- [Bundlers](../01-bundlers/INDEX.md) — the tools being optimized and compared
- [Performance Monitoring](../../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring real-user impact

---

## Navigation

[← Compilers](../02-compilers/INDEX.md) · [↑ Build Tools Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

The [Docita evidence walkthrough](../../../projects/docita/INDEX.md) distinguishes dated lab results from source configuration and deployed behavior. Vite/Astro, shared TypeScript settings and Turbo tasks provide related source examples. Inspect the actual task inputs, invoked gates and emitted outputs before claiming type safety, cache validity or runtime performance. No direct Rspack/Turbopack implementation or measured migration speedup is claimed here.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
