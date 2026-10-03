# Compilers

> **Study time:** ≈ 15 min of reading (3 files, ~5 min average).
> **3 files.** How TS/JSX become browser-compatible JS: Babel (the extensible classic) and the Go/Rust speed tier (ESBuild, SWC).

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Compilers-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

TypeScript does not run in browsers; JSX does not either. Something must strip types, transform syntax, and inject polyfills per browserslist targets. Babel's plugin ecosystem made it ubiquitous; ESBuild and SWC rebuilt the same job 10-100x faster in native code, which is why Vite and Next.js adopted them. Interviews probe whether you know where TypeScript ends and Babel begins.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Babel](40.5.2.01-babel.md) | Compilation pipeline, presets, plugins, polyfills, browserslist, `@babel/preset-env` | Important | Specialized | 6 min |
| 02 | [ESBuild & SWC](40.5.2.02-esbuild-swc.md) | Go/Rust toolchains, performance model, configuration, where each is embedded | Important | Specialized | 7 min |

---

## Cross-References

- [Bundlers](../01-bundlers/INDEX.md) — the consumers of compiler output
- [TypeScript Stack](../../../10-frontend/10.2-typescript/INDEX.md) — the language being compiled

---

## Navigation

[← Bundlers](../01-bundlers/INDEX.md) · [↑ Build Tools Home](../INDEX.md) · [Next: Optimization & Comparison →](../03-optimization-and-comparison/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — compiles TypeScript for real.

| Topic | Docita evidence |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| Shared TS config as a package | `packages/typescript-config` centralizes compiler options; apps/projects extend it |
| Type-check as a build gate | Turbo `check-types` task with dependency ordering; Vite builds depend on it passing |
| Astro check | Landing app type-checks via `astro check` in its own pipeline |
| Babel / SWC specifics | Not hand-configured — they arrive embedded inside Vite/Astro toolchains |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
