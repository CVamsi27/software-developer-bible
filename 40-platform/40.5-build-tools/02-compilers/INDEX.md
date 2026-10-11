# Compilers

> **Study time:** ≈ 9 min of reading (3 files, ~3 min average).
> **3 files.** How TypeScript and JSX syntax become JavaScript, and which checks and runtime APIs remain separate.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Compilers-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

TypeScript and JSX require supported transforms, while emitted JavaScript still needs its runtime APIs. Read Babel’s parse/transform/generate mechanism, then compare esbuild/SWC semantics and explicit type checks. A compiler does not automatically inject every required polyfill or guarantee a fixed speedup.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Babel](40.5.2.01-babel.md) | Compilation pipeline, presets, plugins, polyfills, browserslist, `@babel/preset-env` | Important | Specialized | 4 min |
| 02 | [ESBuild & SWC](40.5.2.02-esbuild-swc.md) | Go/Rust toolchains, performance model, configuration, where each is embedded | Important | Specialized | 3 min |

---

## Cross-References

- [Bundlers](../01-bundlers/INDEX.md) — the consumers of compiler output
- [TypeScript Stack](../../../10-frontend/10.2-typescript/INDEX.md) — the language being compiled

---

## Navigation

[← Bundlers](../01-bundlers/INDEX.md) · [↑ Build Tools Home](../INDEX.md) · [Next: Optimization & Comparison →](../03-optimization-and-comparison/INDEX.md)

---

## Docita Anchor

The [Docita evidence walkthrough](../../../projects/docita/INDEX.md) distinguishes dated lab results from source configuration and deployed behavior. Vite/Astro, shared TypeScript settings and Turbo tasks provide related source examples. Inspect the actual task inputs, invoked gates and emitted outputs before claiming type safety, cache validity or runtime performance. No direct Rspack/Turbopack implementation or measured migration speedup is claimed here.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
