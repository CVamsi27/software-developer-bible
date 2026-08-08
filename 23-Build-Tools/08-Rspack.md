---
section: Build Tools
category: DevOps
tags: [concept, reference, tool]
---

# Rspack

## Definition

**Rspack** is a Rust-based JavaScript bundler from ByteDance, designed as a drop-in replacement for Webpack with significantly faster build times. It provides Webpack-compatible APIs (loaders, plugins, configuration) so existing Webpack projects can migrate with minimal changes. Rspack powers the build system of TikTok, ByteDance, and many enterprise apps with millions of lines of code.

Rspack is part of the **Modern.js** family, alongside Rsbuild (the wrapper) and Rspress (the docs tool). It is often described as "Webpack compatible, but 5-10x faster."

## Why Do We Need It?

1. **Webpack performance ceiling**: Large apps (1000+ modules) hit 30-60s cold builds. Rspack brings this under 5s.
2. **Webpack ecosystem compatibility**: Most existing loaders, plugins, and configs work unchanged.
3. **Incremental migration**: Teams can adopt Rspack without rewriting build config or ejecting from CRA.
4. **Production-ready**: Not experimental — used in production at ByteDance for TikTok web.
5. **Native module federation**: First-class support via `@rspack/core` federation plugin.

## Rspack vs Webpack vs Vite vs Turbopack

| Feature | Webpack | Rspack | Vite | Turbopack |
|---------|---------|--------|------|-----------|
| Language | JS | Rust | JS (esbuild + Rollup) | Rust |
| Cold build (10K modules) | 30-60s | 2-5s | < 1s (dev) / 10s (prod) | < 1s (dev) |
| Webpack API compat | Native | Native | None | None |
| Production build | Yes | Yes | Yes (Rollup) | Beta |
| Module Federation | Yes | Yes | Vite Federation | Limited |
| Plugin ecosystem | Massive | Growing | Vite-only | Limited |
| Used in production | Everywhere | TikTok, ByteDance | Vue, React, many | Next.js dev |

## How It Works

### Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                       Rspack Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────────────┐  │
│  │  Rust Core   │   │  SWC         │   │  Webpack Compat    │  │
│  │  (parallel)  │──▶│  Transform   │──▶│  Loader/Plugin     │  │
│  │              │   │  (TS, JSX)   │   │  Interface         │  │
│  └──────────────┘   └──────────────┘   └────────────────────┘  │
│         │                                        │              │
│         ▼                                        ▼              │
│  ┌──────────────┐                       ┌────────────────────┐  │
│  │  Module      │                       │  Output            │  │
│  │  Graph       │                       │  (same as Webpack) │  │
│  └──────────────┘                       └────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Webpack Compatibility Layer

Rspack implements the Webpack loader and plugin interfaces in Rust. Most Webpack loaders (which are JS-based) can run via a JS shim. Plugins are partially supported.

## Code Examples

### Basic Configuration (Webpack-Compatible)

```javascript
// rspack.config.js — almost identical to webpack.config.js
const path = require('path');
const HtmlRspackPlugin = require('@rspack/core').HtmlRspackPlugin;

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        use: 'builtin:swc-loader',  // Rust-based, no Babel needed
        options: {
          jsc: {
            parser: { syntax: 'ecmascript', jsx: true },
            transform: {
              react: { runtime: 'automatic' },
            },
          },
        },
      },
      {
        test: /\.css$/,
        type: 'css',  // native CSS support, no loader needed
      },
    ],
  },
  plugins: [
    new HtmlRspackPlugin({ template: './index.html' }),
  ],
};
```

### Built-in SWC Loader (No Babel)

```javascript
// TypeScript + JSX via SWC
{
  test: /\.(j|t)sx?$/,
  exclude: /node_modules/,
  use: {
    loader: 'builtin:swc-loader',
    options: {
      jsc: {
        parser: {
          syntax: 'typescript',
          tsx: true,
          decorators: true,
        },
        target: 'es2020',
      },
    },
  },
}
```

### Module Federation

```javascript
// Host (consumer)
const { ModuleFederationPlugin } = require('@rspack/core');

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'host',
      remotes: {
        mfe1: 'mfe1@http://localhost:3001/remoteEntry.js',
      },
      shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
    }),
  ],
};

// Remote (provider)
// mfe1/rspack.config.js
new ModuleFederationPlugin({
  name: 'mfe1',
  filename: 'remoteEntry.js',
  exposes: {
    './Button': './src/Button',
    './Header': './src/Header',
  },
  shared: { react: { singleton: true } },
});
```

### Migration from Webpack

```bash
# Step 1: install rspack
npm install -D @rspack/core @rspack/cli

# Step 2: rename config
mv webpack.config.js rspack.config.js

# Step 3: replace webpack with @rspack/core
# Most loaders and plugins work as-is
# Some Babel/PostCSS configs need adjustment

# Step 4: run
npx rspack serve   # dev
npx rspack build   # production
```

## Real-World Use Cases

### 1. TikTok Web Build

ByteDance reports Rspack reduces their build pipeline from minutes to seconds across the TikTok web app, enabling faster CI and developer iteration.

### 2. Migrating a Legacy Webpack Monorepo

Drop-in Rspack with webpack-compatible config means you can replace `webpack` with `rspack` in `package.json` and ship a 5x faster dev experience with minimal risk.

### 3. Module Federation at Scale

Rspack's first-class federation support (faster than Webpack's, simpler than Vite's) makes it attractive for micro-frontend architectures.

## Common Mistakes

### 1. Assuming 100% Webpack Compatibility

Some Webpack plugins use internal APIs that Rspack doesn't expose. Always test critical plugins (especially custom in-house ones) in a small project first.

### 2. Using Babel Instead of Built-in SWC

```text
❌ Slower: babel-loader (Node.js)
✅ Faster: builtin:swc-loader (Rust, built into Rspack)
```

Use `builtin:swc-loader` for transforms. Babel is for special cases (e.g., experimental proposals).

### 3. Not Enabling Persistent Caching

```javascript
// rspack.config.js
module.exports = {
  experiments: {
    cache: {
      type: 'persistent',  // cache between builds
    },
  },
};
```

Without persistent cache, repeated builds are still slow.

### 4. Mixing Rspack and Webpack Plugins Incorrectly

Some plugins assume the Webpack plugin lifecycle. Check Rspack's compatibility list before adopting.

## Best Practices

1. **Use `builtin:swc-loader`** instead of Babel where possible
2. **Enable persistent caching** (`experiments.cache.type: 'persistent'`)
3. **Migrate incrementally** — start with one app in a monorepo
4. **Use Rsbuild** for new projects (wraps Rspack with sensible defaults)
5. **Keep Webpack config in sync** for fallback during migration
6. **Test Module Federation** thoroughly — runtime remotes add complexity
7. **Benchmark before/after** — measure real gains, not just marketing claims

## Performance Considerations

| App Size | Webpack Cold | Rspack Cold | Speedup |
|----------|--------------|-------------|---------|
| 100 modules | 3s | 0.5s | 6x |
| 1,000 modules | 15s | 2s | 7.5x |
| 10,000 modules | 90s | 8s | 11x |
| 100,000 modules | 600s | 50s | 12x |

Gains scale with app size. Rspack's parallelism shines on large dependency graphs.

## When to Choose Rspack

```text
✅ Choose Rspack when:
  • Migrating from a large Webpack project
  • Need production builds with federation
  • Want Rust speed without rewriting config

❌ Stick with Vite when:
  • Greenfield project with no Webpack history
  • Plugin ecosystem matters most (Vite is broader)

❌ Stick with Turbopack when:
  • Next.js app and OK with dev-only
  • Don't need federation

❌ Stick with Webpack when:
  • Heavy custom in-house plugins
  • Migration risk too high
```

## Summary

- Rspack is a Rust-based Webpack-compatible bundler from ByteDance
- 5-10x faster than Webpack, with Webpack-compatible config
- `builtin:swc-loader` replaces Babel for transforms
- First-class Module Federation support
- Drop-in migration path from Webpack
- Use Rsbuild for greenfield, Rspack directly for migration

---

## Cheat Sheet
```text
RSPACK CHEAT SHEET
============================================================

WHY:
  • Webpack-compatible API, Rust performance
  • 5-10x faster cold builds on large apps
  • Used in production at TikTok, ByteDance
  • First-class Module Federation

CONFIG BASICS:
  • Same as Webpack (rspack.config.js)
  • entry, output, module.rules, plugins
  • HtmlRspackPlugin (not HtmlWebpackPlugin)
  • builtin:swc-loader (not babel-loader)

COMMON GOTCHAS:
  • Most Webpack loaders work as-is
  • Some plugins use Webpack internals (test first)
  • Use builtin:swc-loader over babel-loader
  • Enable experiments.cache.type: 'persistent'

VS COMPETITORS:
  • vs Webpack: 5-10x faster, same API
  • vs Vite: less ecosystem, but Webpack compat
  • vs Turbopack: production-ready, federation support

INTERVIEW TIPS:
  • Explain the Webpack compatibility strategy
  • Discuss Module Federation benefits
  • Show how to migrate from Webpack
  • Mention real-world usage (TikTok, ByteDance)
```
---

## See Also
- [Babel](05-Babel.md)
- [Build Optimization](04-Build-Optimization.md)
- [ESBuild & SWC](06-ESBuild-SWC.md)
- [Next.js](../04-NextJS/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Turbopack](03-Turbopack.md)
- [Vite](02-Vite.md)
- [Webpack](01-Webpack.md)

## References & Learn More

- [Rspack Official Site](https://www.rspack.dev/)
- [Rspack Migration from Webpack](https://www.rspack.dev/guide/migrate-from-webpack)
- [Rsbuild (recommended wrapper)](https://rsbuild.dev/)
- [Module Federation in Rspack](https://www.rspack.dev/guide/features/module-federation)
- [ByteDance Engineering Blog](https://blog.rsbuild.dev/)
