# Build Tools — Index

> **Study time:** ≈ 1 h 7 m of reading (13 files, ~5 min average).
> **13 files** — Frontend build tooling from Webpack, Vite, Turbopack and Rspack through Babel, esbuild and SWC; then build optimization, asset pipelines, tool comparison and interview practice.

[![Files](https://img.shields.io/badge/files-13-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Tooling-%2364748b)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why build tools:** Senior frontend interviews ask about bundlers, transpilers, and build optimization. Start from the framework’s supported integration, understand side effects and lazy loading, then compare transforms and measured workloads.

---

## Category Map

| Category | Folder | Files | What it covers |
| ------------------------- | -------------------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------------------- |
| Bundlers | [01-bundlers/](01-bundlers/INDEX.md) | 4 | Webpack, Vite, Turbopack, Rspack — the main options |
| Compilers | [02-compilers/](02-compilers/INDEX.md) | 2 | Babel, esbuild and SWC — syntax transforms, bundling and runtime/type-check boundaries |
| Optimization & Comparison | [03-optimization-and-comparison/](03-optimization-and-comparison/INDEX.md) | 3 | Build optimization, asset pipelines (CSS/images/fonts), tool comparison — fast builds, small bundles |
| Interview Prep | [04-interview-prep/](04-interview-prep/INDEX.md) | 1 | 44 Qs |

---

## Bundlers

The main bundlers — pick based on project needs.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [Webpack](01-bundlers/40.5.1.01-webpack.md) | Configuration, loaders, plugins, code splitting, HMR | Legacy / complex configs | Important | Specialized | 8 min |
| 02 | [Vite](01-bundlers/40.5.1.02-vite.md) | Dev server, Rolldown/Oxc, plugins, SSR | Supported framework SPAs and library builds | Important | Specialized | 7 min |
| 03 | [Turbopack](01-bundlers/40.5.1.03-turbopack.md) | Incremental computation, caching, Rust-based bundling | Next.js 16 supported default | Important | Specialized | 6 min |
| 04 | [Rspack](01-bundlers/40.5.1.04-rspack.md) | Rust-based Webpack-compatible bundler, federation | Webpack replacement for large apps | Important | Specialized | 5 min |

**Decision tree:**

```text
Framework requirement -> supported default -> required extension inventory
                     -> measured migration slice -> production output checks
```

---

## Compilers

How TS/JSX become browser-compatible JS.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Babel](02-compilers/40.5.2.01-babel.md) | AST transforms, target output, Babel 7-to-8 changes, explicit polyfill and type-check boundaries | Important | Specialized | 5 min |
| 06 | [ESBuild & SWC](02-compilers/40.5.2.02-esbuild-swc.md) | Bundling versus transforms, type erasure, syntax targets, SWC's opt-in `core-js` injection | Important | Specialized | 4 min |

---

## Optimization & Comparison

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 07 | [Build Optimization](03-optimization-and-comparison/40.5.3.01-build-optimization.md) | Tree shaking, code splitting (route/lazy), bundle analysis, caching, source maps | Important | Specialized | 5 min |
| 08 | [Asset Pipelines — CSS, Images & Fonts](03-optimization-and-comparison/40.5.3.02-asset-pipelines-css-images-fonts.md) | PostCSS/Lightning CSS, Tailwind compile path, sharp responsive image sets, font subsetting + preload, hashing/fingerprinting, hidden source maps | Important | Specialized | 8 min |
| 09 | [Build Tool Comparison](03-optimization-and-comparison/40.5.3.03-build-tool-comparison.md) | Webpack vs Vite vs Turbopack vs Rspack trade-offs, when to use each | Important | Specialized | 4 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 10 | [Interview Questions](04-interview-prep/40.5.4.01-interview-questions.md) | 44 curated questions with answers | Important | Specialized | 8 min |

---

## Suggested Study Order

1. **Webpack + Vite** — the two main ones
2. **Build Optimization** — tree shaking, code splitting
3. **Asset Pipelines** — CSS/images/fonts, where page weight actually lives
4. **Babel + esbuild/SWC** — source transformation, type-erasure boundaries and generated output
5. **Turbopack + Rspack** — the new Rust-based options
6. **Tool Comparison** — when to use what
7. **Revision** — [Bundlers](01-bundlers/REVISION.md), [Compilers](02-compilers/REVISION.md), [Optimization](03-optimization-and-comparison/REVISION.md)
8. **Interview Questions** — defend a mechanism under changed conditions

---

## Common interview topics

- "What's tree shaking? How does it work?"
- "Difference between code splitting at route vs component level?"
- "Webpack vs Vite — when to use which?"
- "What does Babel do? How is it different from TypeScript?"
- "How do you debug a bundle size regression?"

---

## Cross-References

- [Next.js](../../10-frontend/10.4-next.js/INDEX.md) — uses Turbopack
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring bundle perf
- [React](../../10-frontend/10.3-react/INDEX.md) — code splitting with React.lazy
- [Monorepo](../40.8-monorepo/INDEX.md) — build orchestration at scale

---

## Navigation

[← Previous: Observability](../40.4-observability/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Git Advanced →](../40.6-git-advanced/INDEX.md)
