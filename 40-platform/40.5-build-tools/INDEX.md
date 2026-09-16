# Build Tools — Index

> **Study time:** ≈ 1 h 56 m of reading (10 files, ~12 min average).
> **10 files** — Frontend build tooling from Webpack, Vite, Turbopack, Rspack to Babel, ESBuild, SWC, build optimization, asset pipelines (CSS/images/fonts), tool comparison, and interview questions.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Tooling-%2364748b)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why build tools:** Senior frontend interviews ask about bundlers, transpilers, and build optimization. Pick the right tool (Vite for new projects, Webpack for legacy), understand tree shaking and code splitting, and know what Babel/SWC do under the hood.

---

## Category Map

| Category | Folder | Files | What it covers |
| ------------------------- | -------------------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------------------------- |
| Bundlers | [01-bundlers/](01-bundlers/INDEX.md) | 4 | Webpack, Vite, Turbopack, Rspack — the main options |
| Compilers | [02-compilers/](02-compilers/INDEX.md) | 2 | Babel, ESBuild/SWC — how JSX + TS get to JS |
| Optimization & Comparison | [03-optimization-and-comparison/](03-optimization-and-comparison/INDEX.md) | 3 | Build optimization, asset pipelines (CSS/images/fonts), tool comparison — fast builds, small bundles |
| Interview Prep | [04-interview-prep/](04-interview-prep/INDEX.md) | 1 | 50+ Qs |

---

## Bundlers

The main bundlers — pick based on project needs.

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 01 | [Webpack](01-bundlers/40.5.1.01-webpack.md) | Configuration, loaders, plugins, code splitting, HMR | Legacy / complex configs | 11 min |
| 02 | [Vite](01-bundlers/40.5.1.02-vite.md) | Dev server, ESBuild, Rollup, plugins, SSR | New projects, fastest dev experience | 11 min |
| 03 | [Turbopack](01-bundlers/40.5.1.03-turbopack.md) | Incremental computation, caching, Rust-based bundling | Next.js 13+, very large apps | 10 min |
| 04 | [Rspack](01-bundlers/40.5.1.04-rspack.md) | Rust-based Webpack-compatible bundler, federation | Webpack replacement for large apps | 11 min |

**Decision tree:**

```text
New project?
├── Yes → Vite (or Next.js = Turbopack)
├── Legacy Webpack → stay on Webpack (or migrate to Rspack)
├── Very large monorepo → Rspack or Turbopack
└── Next.js → Turbopack (default since v15)
```

---

## Compilers

How TS/JSX become browser-compatible JS.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 05 | [Babel](02-compilers/40.5.2.01-babel.md) | Compilation, presets, plugins, polyfills, browserslist | 5 min |
| 06 | [ESBuild & SWC](02-compilers/40.5.2.02-esbuild-swc.md) | Go/Rust bundlers, performance, config, use cases | 6 min |

---

## Optimization & Comparison

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 07 | [Build Optimization](03-optimization-and-comparison/40.5.3.01-build-optimization.md) | Tree shaking, code splitting (route/lazy), bundle analysis, caching, source maps | 15 min |
| 08 | [Asset Pipelines — CSS, Images & Fonts](03-optimization-and-comparison/40.5.3.02-asset-pipelines-css-images-fonts.md) | PostCSS/Lightning CSS, Tailwind compile path, sharp responsive image sets, font subsetting + preload, hashing/fingerprinting, hidden source maps | 18 min |
| 09 | [Build Tool Comparison](03-optimization-and-comparison/40.5.3.03-build-tool-comparison.md) | Webpack vs Vite vs Turbopack vs Rspack trade-offs, when to use each | 12 min |

---

## Interview Prep

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 10 | [Interview Questions](04-interview-prep/40.5.4.01-interview-questions.md) | 50+ curated questions with answers | 17 min |

---

## Suggested Study Order

1. **Webpack + Vite** — the two main ones
2. **Build Optimization** — tree shaking, code splitting
3. **Asset Pipelines** — CSS/images/fonts, where page weight actually lives
4. **Babel + ESBuild/SWC** — the transpilers
5. **Turbopack + Rspack** — the new Rust-based options
6. **Tool Comparison** — when to use what
7. **Interview Questions** — final review

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
