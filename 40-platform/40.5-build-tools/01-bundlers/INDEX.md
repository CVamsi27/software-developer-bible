# Bundlers

> **Study time:** ≈ 28 min of reading (5 files, ~6 min average).
> **5 files.** Four widely used bundler paths: Webpack, Vite, Next.js-integrated Turbopack, and Webpack-oriented Rspack. Choose against framework support and required integrations.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Bundlers-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Bundler choice affects development feedback, build time, compatibility, and emitted output. Compare the same workload and know which part is the bundler, development server, compiler, or task runner before recommending a migration.

**Decision tree:**

```text
Framework requirement -> supported default -> required extension inventory
                     -> measured migration slice -> production output checks
```

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Webpack](40.5.1.01-webpack.md) | Dependency graph, transforms, Asset Modules, lazy chunks, HMR and deployment | Important | Specialized | 7 min |
| 02 | [Vite](40.5.1.02-vite.md) | HTML-to-module requests, dependency pre-bundling, HMR, Rolldown/Oxc, mode, plugins and deployment | Important | Specialized | 7 min |
| 03 | [Turbopack](40.5.1.03-turbopack.md) | Fine-grained invalidation, cache lifetimes, loader compatibility, tracing | Important | Specialized | 6 min |
| 04 | [Rspack](40.5.1.04-rspack.md) | Webpack-oriented migration, cache versus incremental work, plugin/runtime compatibility | Important | Specialized | 5 min |

---

## Cross-References

- [Compilers](../02-compilers/INDEX.md) — how TS/JSX reach the bundler
- [Optimization & Comparison](../03-optimization-and-comparison/INDEX.md) — making any of them fast

---

## Navigation

[↑ Build Tools Home](../INDEX.md) · [Next: Compilers →](../02-compilers/INDEX.md)

---

## Docita Anchor

The [Docita evidence walkthrough](../../../projects/docita/INDEX.md) distinguishes dated lab results from source configuration and deployed behavior. Vite/Astro, shared TypeScript settings and Turbo tasks provide related source examples. Inspect the actual task inputs, invoked gates and emitted outputs before claiming type safety, cache validity or runtime performance. No direct Rspack/Turbopack implementation or measured migration speedup is claimed here.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
