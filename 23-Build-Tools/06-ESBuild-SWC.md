---
section: Build Tools
category: DevOps
tags: [concept, reference, tool]
---

# ESBuild & SWC

## Definition

**ESBuild** and **SWC** are next-generation JavaScript/TypeScript bundlers and compilers written in Go and Rust respectively. They offer 10-100x faster performance than traditional tools like Babel and Webpack by leveraging native code and parallel processing.

| Feature | ESBuild | SWC |
|---------|:-------:|:---:|
| Language | Go | Rust |
| Speeds | 10-100x Babel | 20x Babel |
| Bundling | ✅ Built-in | ⚠️ Via `spack` |
| Minification | ✅ Built-in | ✅ Built-in |
| TypeScript | ✅ (no type-check) | ✅ (no type-check) |
| JSX | ✅ | ✅ |
| Plugins | ✅ (JS API) | ✅ (WASM/Rust) |
| Linting | ❌ | ✅ (via plugin) |

## Why Do We Need It?

1. **Build speed**: Sub-second rebuilds in development
2. **Development experience**: Near-instant HMR with Vite (uses ESBuild)
3. **Production builds**: SWC replaces Babel in Next.js 13+ for faster builds
4. **Smaller bundles**: Efficient tree-shaking and minification

## Code Examples

### ESBuild

```javascript
// build.js
const esbuild = require('esbuild');

// Build
esbuild.buildSync({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/bundle.js',
  platform: 'browser',
  target: ['es2020'],
  minify: true,
  sourcemap: true,
  loader: { '.ts': 'ts', '.tsx': 'tsx' },
});

// Serve with HMR
async function serve() {
  const ctx = await esbuild.context({
    entryPoints: ['src/index.tsx'],
    bundle: true,
    outdir: 'dist',
    define: { 'process.env.NODE_ENV': '"development"' },
  });
  await ctx.watch();
  await ctx.serve({ port: 3000, servedir: 'dist' });
}

// CSS bundling
esbuild.buildSync({
  entryPoints: ['src/styles.css'],
  bundle: true,
  outfile: 'dist/styles.css',
  loader: { '.css': 'css' },
});
```

### SWC

```javascript
// .swcrc
{
  "jsc": {
    "parser": {
      "syntax": "typescript",
      "tsx": true,
      "decorators": true,
      "dynamicImport": true
    },
    "transform": {
      "react": {
        "runtime": "automatic",
        "importSource": "react"
      },
      "optimizer": {
        "globals": {
          "typeofs": { "window": "object" }
        }
      }
    },
    "target": "es2020",
    "minify": {
      "compress": { "unused": true, "dead_code": true },
      "format": { "comments": false }
    }
  },
  "module": { "type": "es6" }
}
```

## Best Practices

1. **Use ESBuild for development bundling** (Vite uses it internally)
2. **Use SWC for production TypeScript compilation** (faster than tsc)
3. **Keep Babel for advanced transforms** if plugins lack ESBuild/SWC equivalents
4. **Combine with Webpack** for complex code-splitting needs
5. **Use ESBuild for one-off builds** (CLI tools, server bundles)

## Summary

- ESBuild is an extremely fast JavaScript bundler and minifier written in Go (10-100x faster than Webpack)
- SWC is a Rust-based platform for compilation, bundling, and minification with Babel-compatible plugins
- Both tools are designed as drop-in replacements for Babel and Webpack in modern build pipelines
- ESBuild excels at single-file bundling and is used internally by Vite for dependency pre-bundling
- SWC powers Next.js and Parcel, offering TypeScript compilation and minification in a single binary

---

## Cheat Sheet
```text
ESBUILD & SWC CHEAT SHEET
============================================================

ESBUILD (Go):
  • Bundler + minifier + dev server in one
  • 10-100x faster than Babel+webpack
  • Used internally by Vite (pre-bundling)
  • Plugin API in JavaScript
  • Limitation: no type-checking (use tsc separately)

SWC (Rust):
  • Standalone compiler (transforms TS/JSX)
  • 20x faster than Babel
  • Used by Next.js 13+ (replaces Babel for app router)
  • Plugin API in Rust or WASM
  • spack (experimental bundler, in development)

CHOOSING BETWEEN:
  • Use SWC when:  Next.js, large monorepo, transform-only
  • Use ESBuild when: small/medium apps, Vite, CLI bundling
  • Use Babel when:  complex plugin ecosystem needed, stage-3+

INTERVIEW TIPS:
  • Explain why Go/Rust is faster than JS (parallelism, no GC pauses)
  • Discuss how Vite uses esbuild (dev pre-bundle, prod Rollup)
  • Show swc config in Next.js 13+
  • Mention esbuild's --metafile for bundle analysis
```
---
## See Also
- [Babel](05-Babel.md)
- [Next.js](../04-NextJS/)

## References & Learn More

- [ESBuild Documentation](https://esbuild.github.io/)
- [SWC Documentation](https://swc.rs/docs/)
- [ESBuild vs SWC Comparison](https://blog.logrocket.com/esbuild-vs-swc-bundler-comparison/)
