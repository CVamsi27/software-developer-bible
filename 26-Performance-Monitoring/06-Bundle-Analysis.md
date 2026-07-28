# Bundle Analysis

[![Category: Quality](https://img.shields.io/badge/category-Quality-brightgreen)](.)

y optimization opportunities — duplicate dependencies, large modules, unused exports, and code-splitting candidates. Tools like `webpack-bundle-analyzer`, `vite-bundle-visualizer`, and `Bundlephobia` visualize bundle contents.

## Why Do We Need It?

1. **Find bloat**: Identify oversized libraries or accidental duplicates
2. **Code splitting**: Identify split points for lazy loading
3. **Tree shaking**: Verify unused exports are eliminated
4. **Budget compliance**: Enforce size budgets in CI/CD

## Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| **webpack-bundle-analyzer** | Interactive treemap | Webpack plugin |
| **vite-bundle-visualizer** | Rollup output analysis | Vite plugin |
| **Bundlephobia** | Package cost before install | Web service |
| **size-limit** | Size budgets in CI | CI/CLI |
| **source-map-explorer** | Source-level analysis | CLI |

## Budget Configuration

```javascript
// size-limit.config.js
module.exports = [
  { path: 'dist/main.js', limit: '150 KB' },
  { path: 'dist/vendor.js', limit: '200 KB' },
  { path: 'dist/*.js', limit: '50 KB' },
];
```

## Summary

- Bundle analysis tools visualize JavaScript bundle composition to identify optimization opportunities
- webpack-bundle-analyzer produces interactive treemaps of module sizes and dependencies
- Bundlephobia provides npm package size insights including dependency weight and tree-shaking analysis
- Source map analysis enables deep inspection of bundled code origins and duplicate dependencies
- CI integration of bundle analysis prevents size regressions with automated threshold checks

---

## Cheat Sheet
```text
BUNDLE ANALYSIS CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  module.exports = [
    { path: 'dist/main.js', limit: '150 KB' },
    { path: 'dist/vendor.js', limit: '200 KB' },
    { path: 'dist/*.js', limit: '50 KB' },
  ];
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [Accessibility](../25-Accessibility/)
- [Build Optimization](../23-Build-Tools/04-Build-Optimization.md)

## References & Learn More

- [Bundlephobia](https://bundlephobia.com/)
- [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)
