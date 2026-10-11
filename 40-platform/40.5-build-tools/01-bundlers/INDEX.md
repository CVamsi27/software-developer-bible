# Bundlers

> **Study time:** ≈ 20 min of reading (5 files, ~4 min average).
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
| 01 | [Webpack](40.5.1.01-webpack.md) | Configuration, loaders, plugins, code splitting, HMR | Important | Specialized | 4 min |
| 02 | [Vite](40.5.1.02-vite.md) | Dev server, native ESM in dev, Rolldown/Oxc production, plugins, SSR | Important | Specialized | 5 min |
| 03 | [Turbopack](40.5.1.03-turbopack.md) | Incremental computation, development/build caching, Rust-based bundling | Important | Specialized | 5 min |
| 04 | [Rspack](40.5.1.04-rspack.md) | Rust-based Webpack-compatible bundler, module federation | Important | Specialized | 4 min |

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
