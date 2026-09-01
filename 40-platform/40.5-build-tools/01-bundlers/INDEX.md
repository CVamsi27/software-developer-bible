# Bundlers

> **4 files.** The four bundlers that matter: Webpack (the incumbent), Vite (the default for new projects), and the Rust challengers Turbopack and Rspack.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Bundlers-%2364748b)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

The bundler decides dev-server latency, build time, and output shape. Interviews ask "Webpack vs Vite — when do you use which?" and expect you to know what changed (unbundled dev, native bindings) rather than recite config. These four chapters cover each tool's model and its sweet spot.

**Decision tree:**

```text
New project?
├── Yes → Vite (or Next.js = Turbopack)
├── Legacy Webpack → stay on Webpack (or migrate to Rspack)
├── Very large monorepo → Rspack or Turbopack
└── Next.js → Turbopack (default since v15)
```

---

## File Index

| Order  | File                                | Topics                                                        | Read time   |
| --   : | ------                              | --------                                                      | ----------: |
| 01     | [Webpack](40.5.1.01-webpack.md)     | Configuration, loaders, plugins, code splitting, HMR          | 30 min      |
| 02     | [Vite](40.5.1.02-vite.md)           | Dev server, native ESM in dev, ESBuild + Rollup, plugins, SSR | 30 min      |
| 03     | [Turbopack](40.5.1.03-turbopack.md) | Incremental computation, caching, Rust-based bundling         | 25 min      |
| 04     | [Rspack](40.5.1.04-rspack.md)       | Rust-based Webpack-compatible bundler, module federation      | 20 min      |

---

## Cross-References

- [Compilers](../02-compilers/INDEX.md) — how TS/JSX reach the bundler
- [Optimization & Comparison](../03-optimization-and-comparison/INDEX.md) — making any of them fast

---

## Navigation

[↑ Build Tools Home](../INDEX.md) · [Next: Compilers →](../02-compilers/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — bundles for real.

| Topic               | Docita evidence                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Vite                | The SPA apps (`apps/app`, `apps/internal`) run on Vite — ADR 0012 records replacing Next.js with a Vite SPA              |
| Astro (SSG)         | `apps/landing` builds with Astro, deployable to Cloudflare Workers (`build:cloudflare`, wrangler)                        |
| Turbopack / Rspack  | _No direct docita implementation yet._                                                                                   |
| Build orchestration | Turbo task graph wraps every bundle: `build` depends on `^build` + `check-types` + `lint`, outputs `dist/**` for caching |
