---
section: Build Tools
category: DevOps
tags: [concept, guide, reference]
---

# Build Tool Comparison

## Definition

Choosing a frontend build tool in 2024+ is no longer "Webpack or nothing." The landscape includes Webpack (mature, slow), Vite (fast dev, broad ecosystem), Turbopack (Rust, dev-first), Rspack (Webpack-compatible Rust), esbuild (Go, no-bundler-needed), SWC (Rust, transform-only), and Rollup (library bundling). This file compares them across dimensions that matter to senior engineers: speed, ecosystem, migration cost, and fit for the use case.

## Why Do We Need It?

1. **No one tool wins everything**: Webpack ecosystem vs Vite speed vs Rspack compat — each has trade-offs
2. **Migration is expensive**: Wrong choice = rewriting config, retraining team, breaking CI
3. **Performance bottlenecks** can be traced to the wrong tool (e.g., 60s Webpack cold builds hurt developer velocity)
4. **Greenfield choices** are easier than migration: choose right the first time

## The Landscape (2024)

```text
┌────────────────────────────────────────────────────────────────────┐
│                   Build Tool Decision Tree                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Start: Building a new project                                      │
│    │                                                               │
│    ├─► Application (SPA, SSR)?                                     │
│    │     ├─► React / Vue / Svelte?  ──► Vite (recommended)         │
│    │     ├─► Next.js?                ──► Turbopack (dev) + SWC     │
│    │     └─► Migrating from Webpack? ──► Rspack                    │
│    │                                                               │
│    ├─► Library / package?           ──► Rollup (or tsup)           │
│    │                                                               │
│    └─► Need Webpack compat?         ──► Rspack                     │
│                                                                    │
│  Already on Webpack?                                                │
│    ├─► Cold build > 30s?           ──► migrate to Rspack           │
│    └─► Cold build < 10s?           ──► stay on Webpack             │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Comparison Matrix

| Tool | Language | Cold Build (10K modules) | Webpack Compat | Prod Ready | HMR | Federation | Ecosystem | Best For |
|------|----------|--------------------------|----------------|------------|-----|------------|-----------|----------|
| **Webpack 5** | JS | 30-60s | Native | ✅ | ✅ | ✅ | Massive | Existing apps, plugins |
| **Vite 5** | JS + esbuild | < 1s dev / 10s prod | ❌ | ✅ | ✅ | Plugin | Large | New projects, fastest dev |
| **Turbopack** | Rust | < 1s dev | ❌ | Beta | ✅ | Limited | Small | Next.js, dev only |
| **Rspack 1** | Rust | 2-5s | ✅ | ✅ | ✅ | Native | Growing | Webpack migration |
| **esbuild** | Go | 0.3s | ❌ | ✅ | ✅ | N/A | Library | Vite, scripts, libraries |
| **SWC** | Rust | 0.1s (transform) | Via Next.js | ✅ | N/A | N/A | Transform-only | TS/JSX transforms |
| **Rollup** | JS | 5-15s | ❌ | ✅ | ✅ | Plugin | Library | Libraries, ESM-first |

## Detailed Trade-offs

### Webpack

```text
✅ Pros:
  • Mature, battle-tested, ubiquitous
  • Massive plugin/loader ecosystem
  • Production-ready Module Federation
  • Every tutorial and example assumes Webpack

❌ Cons:
  • Slow cold builds (60s+ for large apps)
  • Complex configuration
  • JavaScript-bound (no parallelism for transforms)
  • HMR slower than Vite

Choose when:
  • Existing app with stable Webpack config
  • Heavy custom in-house plugins
  • Module Federation is critical
```

### Vite

```text
✅ Pros:
  • Instant dev start (no bundling in dev)
  • HMR updates in < 50ms
  • Out-of-box support for Vue, React, Svelte
  • Simple config (rollupOptions for prod)
  • Plugin ecosystem growing rapidly

❌ Cons:
  • Different mental model from Webpack (dev != prod)
  • Some Webpack plugins need Vite equivalents
  • Rollup for prod has its own quirks
  • Less Module Federation maturity

Choose when:
  • Greenfield SPA / SSR
  • Speed of iteration matters most
  • No legacy Webpack baggage
```

### Turbopack

```text
✅ Pros:
  • 10x faster than Webpack, ~700x faster than Vite on large apps
  • Incremental computation
  • Built for Next.js (seamless integration)

❌ Cons:
  • Dev server only (production builds still in beta)
  • Webpack plugins not supported
  • Limited to Next.js (officially)
  • Smaller community

Choose when:
  • Next.js app
  • Willing to use --turbo in dev, Webpack in prod for now
```

### Rspack

```text
✅ Pros:
  • Webpack-compatible config (drop-in replacement)
  • 5-10x faster than Webpack
  • Production-ready
  • First-class Module Federation
  • SWC built-in

❌ Cons:
  • Some Webpack plugins don't work
  • Smaller ecosystem than Webpack
  • Rust-based — fewer contributors can debug internals
  • Relatively new (1.0 released 2024)

Choose when:
  • Migrating from Webpack without rewriting config
  • Need production builds with federation
  • Large monorepos with Webpack history
```

### esbuild / SWC

```text
✅ Pros:
  • 10-100x faster than Babel
  • Used inside Vite, Rspack, Turbopack, Next.js
  • Mature (esbuild 1.0 since 2020)

❌ Cons:
  • esbuild: no TypeScript type-checking, limited plugin API
  • SWC: primarily a transform, not a full bundler
  • Don't replace Webpack/Vite for complex apps

Choose when:
  • Need fast transforms (TS, JSX, minification)
  • Use as part of Vite/Rspack/Next.js pipeline
  • Library bundling (tsup = esbuild + tsc types)
```

## Code Examples

### Migration: Webpack → Rspack

```bash
# Install
npm install -D @rspack/core @rspack/cli

# Rename config
mv webpack.config.js rspack.config.js

# Most config works as-is, but check:
# - HtmlWebpackPlugin → HtmlRspackPlugin
# - babel-loader → builtin:swc-loader (10x faster)
# - mini-css-extract-plugin → rspack's built-in CSS
```

### Migration: Webpack → Vite

```bash
# Install
npm install -D vite @vitejs/plugin-react

# Create vite.config.ts
# vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Most build configs port via rollupOptions
});
```

```json
// package.json scripts
{
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview"
}
```

### Library Bundling with tsup

```json
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,        // generate .d.ts
  splitting: true,
  treeshake: true,
  minify: true,
});
```

```bash
npx tsup    # builds dist/index.js, dist/index.cjs, dist/index.d.ts
```

## Real-World Use Cases

### 1. Greenfield SaaS App (React + TypeScript)

```text
Choose: Vite
Why:  Fast dev iteration, simple config, broad plugin ecosystem
```

### 2. Next.js E-commerce Site

```text
Choose: Turbopack (dev) + Webpack (prod) for now
Why:  --turbo in dev for speed, Webpack stable in prod
Migration: as Turbopack stabilizes production builds
```

### 3. Legacy Webpack Monorepo (5 apps, 2 years old)

```text
Choose: Rspack
Why:  Drop-in Webpack compatibility, 5-10x speedup, no config rewrite
```

### 4. React Component Library

```text
Choose: tsup (esbuild-based) or Rollup
Why:  Tree-shakeable ESM/CJS outputs, type generation, small config
```

### 5. Build Tool Plugin Author

```text
Choose: Target multiple — Rspack for Webpack compat, Vite for new projects
Why:  Build on Rollup plugin API (works in both)
```

## Common Mistakes

### 1. Choosing the Newest Tool Without Testing

```text
❌ Migrate entire monorepo to Turbopack because blog post said it's fast
✅ Spike on one app for 2 weeks, measure actual gains
```

### 2. Ignoring Ecosystem Lock-in

```text
❌ Choose esbuild for app bundling (limited plugin support)
✅ Use esbuild for transforms, Vite/Rspack for full bundling
```

### 3. Sacrificing Federation for Speed

```text
❌ Switch to Vite and lose Module Federation
✅ Use Rspack (faster than Webpack, keeps federation)
```

### 4. Not Considering CI Cache

```text
❌ Cold build is 60s, repeat builds also 60s
✅ Persistent cache (Rspack/Webpack experiments.cache, Vite's) makes repeat builds < 5s
```

## Best Practices

1. **Benchmark with your real codebase** — not synthetic examples
2. **Consider migration cost**, not just raw speed
3. **For libraries, prefer Rollup/tsup** (ESM-first, tree-shakeable)
4. **For apps, prefer Vite** (greenfield) or **Rspack** (Webpack migration)
5. **For Next.js, use Turbopack in dev** (with Webpack fallback)
6. **Always enable persistent caching** for CI/CD
7. **Use SWC or esbuild for transforms** (not Babel)
8. **Plan an exit strategy** — even mature tools get replaced
9. **Test on CI, not just dev machine** — dev environments have different characteristics
10. **Monitor build time** in CI as a metric

## Performance Decision Framework

```text
Q1: Is this a library or an app?
  Library → Rollup / tsup
  App     → Q2

Q2: Is this greenfield or migration from Webpack?
  Greenfield     → Vite (or Next.js + Turbopack)
  Webpack legacy → Rspack

Q3: Do you need Module Federation?
  Yes → Rspack (or Webpack)
  No  → Vite / Turbopack

Q4: What's your cold build time target?
  < 1s dev  → Vite / Turbopack
  < 5s dev  → Rspack
  < 30s dev → Webpack acceptable

Q5: Is your team new to bundlers?
  → Vite (simplest mental model)
  → Rspack (same as Webpack they may know)
```

## Summary

- No single "best" tool — each wins in different dimensions
- **Vite**: greenfield, fastest dev, broad ecosystem
- **Turbopack**: Next.js, dev-only, Rust performance
- **Rspack**: Webpack migration, prod-ready, federation
- **Webpack**: legacy apps, biggest plugin ecosystem
- **esbuild/SWC**: transforms and library bundling
- **Rollup**: library bundling, ESM-first
- Benchmark with your own code, not synthetic tests
- Consider migration cost, not just raw speed

---

## Cheat Sheet
```text
BUILD TOOL COMPARISON CHEAT SHEET
============================================================

CHOOSE BY USE CASE:
  • Greenfield SPA / SSR    → Vite
  • Next.js app             → Turbopack (dev) + Webpack (prod)
  • Webpack migration       → Rspack
  • React component library → tsup (esbuild) or Rollup
  • Plugin author           → Rollup plugin API (works in Rspack)

SPEED RANK (10K modules, cold build):
  1. esbuild       ~0.3s
  2. SWC           ~0.1s (transform only)
  3. Vite (dev)    ~1s (esbuild pre-bundle)
  4. Turbopack     ~1s
  5. Rspack        ~3s
  6. Rollup        ~10s
  7. Webpack       ~45s

DECISION QUESTIONS:
  1. App or library?
  2. Greenfield or migration?
  3. Need Module Federation?
  4. Cold build target?
  5. Team experience?

INTERVIEW TIPS:
  • Explain the trade-offs, not just "X is faster"
  • Discuss when NOT to migrate (Webpack 5 is fine for small apps)
  • Show you understand the ecosystem lock-in
  • Mention tsup for libraries, not full bundlers
```
---

## See Also
- [Babel](05-Babel.md)
- [Build Optimization](04-Build-Optimization.md)
- [ESBuild & SWC](06-ESBuild-SWC.md)
- [Next.js](../04-NextJS/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Rspack](08-Rspack.md)
- [Turbopack](03-Turbopack.md)
- [Vite](02-Vite.md)
- [Webpack](01-Webpack.md)

## References & Learn More

- [Vite vs Webpack comparison](https://vitejs.dev/guide/comparisons.html)
- [Rspack vs Webpack benchmark](https://www.rspack.dev/guide/start/benchmark)
- [Turbopack benchmarks](https://turbo.build/pack/docs/benchmarks)
- [Modern Build Tools (2024)](https://github.com/privatenumber/tsx-bundler-comparison)
- [esbuild official site](https://esbuild.github.io/)
- [Rollup official site](https://rollupjs.org/)
