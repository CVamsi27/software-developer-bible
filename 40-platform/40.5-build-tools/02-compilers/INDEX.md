# Compilers

> **Study time:** ≈ 11 min of reading (3 files, ~4 min average).
> **3 files.** How JavaScript-family syntax becomes output, where Babel 8 polyfill settings differ from Babel 7, and which type/runtime checks remain separate.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Compilers-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

TypeScript and JSX need syntax transforms, but emitted JavaScript still needs runtime APIs and TypeScript still needs a checker. Read Babel's current output and polyfill contract first, then compare what esbuild and SWC own. The key decision is which stage each tool handles and which checks remain explicit.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Babel](40.5.2.01-babel.md) | AST transforms, target output, Babel 7-to-8 changes, explicit polyfill and type-check boundaries | Important | Specialized | 5 min |
| 02 | [ESBuild & SWC](40.5.2.02-esbuild-swc.md) | Bundling versus transforms, type erasure, syntax targets, SWC's opt-in `core-js` injection | Important | Specialized | 4 min |

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
