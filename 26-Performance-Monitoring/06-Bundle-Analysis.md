---
section: Performance Monitoring
category: Quality
tags: [concept, tool, guide]
---

# Bundle Analysis

## Definition

**Bundle analysis** is the practice of inspecting the contents, size, and composition of JavaScript bundles shipped to the browser. Tools like `webpack-bundle-analyzer`, `vite-bundle-visualizer`, and `source-map-explorer` produce interactive visualizations of what is in your bundle — modules, dependencies, duplicates, and unused code. Combined with size budgets in CI, bundle analysis prevents regressions before they ship.

The most expensive mistake a frontend team can make is shipping a 2 MB bundle because someone imported `lodash` instead of `lodash-es`. Bundle analysis is how you catch this.

## Why Do We Need It?

1. **Find bloat**: Identify oversized libraries, accidental duplicates, framework bloat
2. **Code splitting decisions**: Identify split points for route/component-level lazy loading
3. **Tree shaking verification**: Confirm unused exports are actually eliminated
4. **Budget compliance**: Enforce size limits per chunk in CI
5. **Dependency audits**: Visualize the cost of adding a new npm package
6. **Migration planning**: Compare bundle impact when swapping libraries (e.g., moment → date-fns)

## Tools Comparison

| Tool | Purpose | Integration |
|------|---------|-------------|
| **webpack-bundle-analyzer** | Interactive treemap | Webpack plugin / CLI |
| **vite-bundle-visualizer** | Rollup output analysis | Vite plugin |
| **source-map-explorer** | Source-level analysis | CLI |
| **Bundlephobia** | Package cost before install | Web service |
| **size-limit** | Size budgets in CI | CLI / Jest plugin |
| **rollup-plugin-visualizer** | Rollup-based bundlers | Rollup plugin |
| **esbuild metafile** | esbuild's built-in | `--metafile=out.json` |

## Code Examples

### webpack-bundle-analyzer

```javascript
// webpack.config.js (production)
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',      // generates report.html
      openAnalyzer: false,          // don't open browser in CI
      reportFilename: 'bundle-report.html',
      generateStatsFile: true,
      statsFilename: 'bundle-stats.json',
    }),
  ],
};
```

```bash
# Run with analysis
ANALYZE=true npm run build

# Or add to package.json scripts
"analyze": "webpack --mode production --env analyze"
```

### vite-bundle-visualizer

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      filename: 'dist/stats.html',
      open: false,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
});
```

### size-limit Configuration

```javascript
// .size-limit.json
[
  {
    "name": "Main bundle (gzipped)",
    "path": "dist/main.js",
    "limit": "150 KB",
    "gzip": true
  },
  {
    "name": "Vendor bundle (gzipped)",
    "path": "dist/vendor.js",
    "limit": "200 KB",
    "gzip": true
  },
  {
    "name": "All chunks combined",
    "path": "dist/*.js",
    "limit": "500 KB"
  },
  {
    "name": "Initial load (above the fold)",
    "path": ["dist/main.js", "dist/vendor.js"],
    "limit": "300 KB",
    "gzip": true
  }
]
```

```json
// package.json
{
  "scripts": {
    "size": "size-limit",
    "test:size": "size-limit --json"
  },
  "size-limit": {
    "current": 285000
  }
}
```

### source-map-explorer

```bash
# Generate source maps during build, then analyze
npx webpack --mode production --devtool source-map
npx source-map-explorer 'dist/*.js' --html dist/source-map-report.html
```

### esbuild Metafile

```typescript
// build.ts
import esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  outfile: 'dist/bundle.js',
  minify: true,
  metafile: true,  // outputs to disk
});

// Analyze the metafile
// https://esbuild.github.io/analyze/  - paste the JSON
// or: npx esbuild-visualizer --metadata out.meta.json --output report.html
```

## Real-World Use Cases

### 1. Finding Duplicate Dependencies

The treemap reveals when `react@17` and `react@18` are both bundled (peer dep conflict), or when two packages each bundle their own copy of `lodash`:

```text
dist/
├── main.js (450 KB)
│   ├── react@17.0.2     (45 KB)  ← duplicate
│   ├── react@18.2.0     (45 KB)
│   ├── lodash@4.17.20   (75 KB)  ← via old dep
│   └── lodash@4.17.21   (75 KB)  ← via new dep
```

Fix: deduplicate with `npm dedupe` or use a single source.

### 2. Identifying Lazy-Load Candidates

A treemap showing 200 KB in `chart-library` revealed it was only used on the analytics page. Splitting reduced initial bundle by 180 KB.

```typescript
// Before: imported eagerly
import { Chart } from 'chart-library';

// After: dynamic import
const Chart = lazy(() => import('chart-library').then(m => ({ default: m.Chart })));
```

### 3. Pre-install Cost Analysis

Before adding `moment` (300 KB), check Bundlephobia — discover `date-fns` (tree-shakeable, 20 KB for the parts you use). Use [bundlephobia.com](https://bundlephobia.com/) before installing.

## Common Mistakes

### 1. Importing Whole Libraries

```typescript
// ❌ Bad: imports entire lodash
import _ from 'lodash';
_.debounce(fn, 300);  // 70 KB shipped

// ✅ Good: tree-shakeable
import debounce from 'lodash/debounce';
debounce(fn, 300);  // 2 KB shipped
```

### 2. Side-Effectful Modules

```json
// ❌ Bad: bundler assumes every export might be used
// package.json
{ "sideEffects": true }

// ✅ Good: tells bundler it's safe to drop unused exports
{ "sideEffects": ["*.css", "*.scss"] }
```

### 3. Barrel Files

```typescript
// ❌ Bad: barrel files defeat tree shaking
export * from './Button';
export * from './Modal';
export * from './Dropdown';
// importing { Button } brings in Modal + Dropdown in some bundlers

// ✅ Good: import directly
import { Button } from './Button';
```

### 4. Not Analyzing Production Builds

Dev builds include source maps, hot-reload, and unminified code. Always analyze the production build:

```bash
npm run build && npx webpack-bundle-analyzer dist/bundle-stats.json
```

## Best Practices

1. **Analyze every production build** in CI; fail the build if size grows > 5%
2. **Set per-chunk budgets** (`size-limit`) — not just total bundle
3. **Use `import` from deep paths** for large libraries (lodash, rxjs, date-fns)
4. **Add `"sideEffects": false`** to your `package.json`
5. **Avoid barrel files** in component libraries
6. **Use dynamic `import()`** for routes, modals, and heavy widgets
7. **Compare stats across PRs** — comment on the diff with a percentage
8. **Set up Bundlephobia bot** on GitHub to comment on new dependencies

## CI Integration

```yaml
# .github/workflows/bundle.yml
name: Bundle Size
on: [pull_request]

jobs:
  size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npx size-limit
      - uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch_name: ${{ github.head_ref }}
```

## Performance Considerations

| Bundle Size (gzipped) | TTI Impact | User Experience |
|----------------------|------------|-----------------|
| < 100 KB | < 1s on 4G | Excellent |
| 100-300 KB | 1-3s on 4G | Good |
| 300-500 KB | 3-5s on 4G | Acceptable |
| > 500 KB | 5s+ on 4G | Poor |

The **170 KB rule**: HTTP/1.1 initial connection window is 14 KB; HTTP/2 streams can parallelize, but the **first 170 KB** still fits in the initial congestion window. Aim for your critical-path JS to be under 170 KB gzipped.

## Summary

- Bundle analysis visualizes what's in your JS bundle — modules, duplicates, bloat
- `webpack-bundle-analyzer` and `vite-bundle-visualizer` produce interactive treemaps
- `size-limit` enforces per-chunk budgets in CI
- Look for duplicate dependencies, full-library imports, side-effectful modules
- Check [bundlephobia.com](https://bundlephobia.com/) before adding new packages
- Aim for **< 170 KB gzipped** initial bundle (first congestion window)

---

## Cheat Sheet
```text
BUNDLE ANALYSIS CHEAT SHEET
============================================================

TOOLS BY BUNDLER:
  • Webpack:  webpack-bundle-analyzer
  • Vite:     vite-bundle-visualizer (rollup-plugin-visualizer)
  • esbuild:  --metafile + esbuild-analyze
  • Rollup:   rollup-plugin-visualizer
  • Source:   source-map-explorer (any source map)

SIZE BUDGETS:
  • .size-limit.json with per-chunk limits
  • Initial bundle < 170 KB gzipped (congestion window)
  • Per-route < 100 KB gzipped (lazy loaded)
  • Vendor split (react, lodash) for long-term caching

COMMON WINS:
  • lodash -> lodash-es or per-method imports (save 60-100 KB)
  • moment -> date-fns or dayjs (save 200+ KB)
  • icon libraries: import only used icons
  • duplicate deps: npm dedupe / resolutions in package.json
  • barrel files: import directly from source files

TREE SHAKING:
  • ESM only (CJS not shaken)
  • "sideEffects": false in package.json
  • Avoid top-level side effects in modules
  • Verify with analysis: unused exports should be gone

INTERVIEW TIPS:
  • Discuss trade-off: more chunks vs more HTTP requests
  • Mention HTTP/2 multiplexing changes the calculus
  • Show how to migrate from moment to date-fns
  • Know the 170 KB congestion window rule
```
---

## See Also
- [Accessibility](../25-Accessibility/)
- [Build Optimization](../23-Build-Tools/04-Build-Optimization.md)
- [Core Web Vitals](01-Core-Web-Vitals.md)
- [Lighthouse CI](05-Lighthouse-CI.md)

## References & Learn More

- [Bundlephobia](https://bundlephobia.com/)
- [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)
- [source-map-explorer](https://github.com/danvk/source-map-explorer)
- [size-limit](https://github.com/ai/size-limit)
- [Why 170 KB?](https://hpbn.co/building-blocks-of-tcp/#optimizing-for-tcp)
- [Tree Shaking](https://webpack.js.org/guides/tree-shaking/)
