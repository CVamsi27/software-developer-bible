---
section: Performance Monitoring
category: Quality
tags: [concept, reference, guide]
---

# Performance Budgets

## Definition

A **performance budget** is a quantitative limit on metrics that affect user experience — bundle size, image weight, request count, time-to-interactive, Core Web Vitals. Budgets are enforced in CI to prevent regressions, owned by the team (not just SRE), and tied to business outcomes (conversion, bounce rate, SEO). Without a budget, every feature is "free" and bundle size grows until users notice.

The most important performance work happens *before* a regression ships. A 200 KB budget enforced in CI is cheaper than 6 months of optimization later.

## Why Do We Need It?

1. **Prevent regression creep**: every new feature adds weight; without a budget, bundle grows unbounded
2. **Align team on priorities**: when bundle is at 199/200 KB, the team knows to optimize
3. **Make trade-offs visible**: "should I add this 50 KB carousel?" is a budget question
4. **Tie engineering to business**: budgets surface as conversion / SEO impact
5. **Catch issues before they ship** — when they are 10x cheaper to fix
6. **Enable long-term architectural discipline** — micro-frontends, lazy loading, code splitting

## Types of Performance Budgets

| Type | Metric | Example |
|------|--------|---------|
| **Bundle size** | Total JS / CSS shipped | Main bundle < 200 KB gzipped |
| **Per-chunk** | Size of each route chunk | Any route < 100 KB gzipped |
| **Image weight** | Total image bytes on initial load | Hero images < 500 KB |
| **Request count** | HTTP requests on first load | < 60 requests |
| **Web Vitals** | p75 in production | LCP < 2.5s, INP < 200ms, CLS < 0.1 |
| **Time to Interactive** | TTI in lab | TTI < 3.5s on Slow 4G |
| **CPU time** | Main-thread blocking | < 200ms TBT |
| **Third-party** | Sum of all third-party scripts | < 100 KB |

## How It Works

### Budget Enforcement Lifecycle

```text
┌──────────────────────────────────────────────────────────────────┐
│                  Budget Enforcement Lifecycle                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Define budgets (team consensus, tied to UX/business)         │
│       │                                                          │
│       ▼                                                          │
│  2. Encode in CI (size-limit, Lighthouse CI, custom scripts)     │
│       │                                                          │
│       ▼                                                          │
│  3. PRs are checked against budget                               │
│       ├── Pass: continue pipeline                                │
│       └── Fail: block merge + show diff vs baseline              │
│                                                                  │
│  4. Track in dashboard (size over time, per-team)                │
│                                                                  │
│  5. Quarterly review (are budgets still right?)                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Code Examples

### size-limit (Bundle Size Budget)

```javascript
// .size-limit.json
[
  {
    "name": "Initial JS (gzipped)",
    "path": "dist/main.[contenthash].js",
    "limit": "200 KB",
    "gzip": true
  },
  {
    "name": "Vendor bundle (gzipped)",
    "path": "dist/vendor.[contenthash].js",
    "limit": "150 KB",
    "gzip": true
  },
  {
    "name": "Largest single chunk",
    "path": "dist/*.js",
    "limit": "100 KB"
  },
  {
    "name": "Total CSS (gzipped)",
    "path": "dist/*.css",
    "limit": "30 KB",
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
  }
}
```

```bash
# Run locally
npm run size

# Output:
#  Initial JS (gzipped)               185 KB →  200 KB  ✓
#  Vendor bundle (gzipped)           142 KB →  150 KB  ✓
#  Largest single chunk               98 KB →  100 KB  ✓
#  Total CSS (gzipped)                18 KB →   30 KB  ✓
```

### bundlesize (Alternative)

```json
{
  "bundlesize": [
    { "path": "./dist/main.js", "maxSize": "200 KB" },
    { "path": "./dist/vendor.js", "maxSize": "150 KB" }
  ]
}
```

### Lighthouse CI Budget (Web Vitals)

```json
// .lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 200 }],
        "categories:performance": ["error", { "minScore": 0.9 }]
      }
    }
  }
}
```

### Webpack Custom Budget Plugin

```javascript
// webpack.config.js
const { BundleBudgetPlugin } = require('webpack-bundle-budget');

module.exports = {
  performance: {
    hints: 'error',           // 'warning' | 'error' | false
    maxAssetSize: 250000,     // 250 KB per asset
    maxEntrypointSize: 400000, // 400 KB total for entry
    assetFilter: (filename) => !filename.includes('chunk-'),  // ignore async chunks
  },
};
```

### Per-PR Bundle Diff Comment

```yaml
# .github/workflows/bundle.yml
- uses: andresz1/size-limit-action@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    branch_name: ${{ github.head_ref }}
    build_script: "npm run build"
```

```text
## Bundle Size Report

| File | Size | Limit | Status |
|------|------|-------|--------|
| main.js (gz) | 192 KB | 200 KB | ✓ +3 KB |
| vendor.js (gz) | 148 KB | 150 KB | ✓ +1 KB |
| css (gz) | 22 KB | 30 KB | ✓ +2 KB |

Total: +6 KB vs main
```

### Image Budget (Custom Script)

```typescript
import globby from 'globby';
import { readFile } from 'fs/promises';

const BUDGET_KB = 500;
const images = await globby('public/images/**/*.{png,jpg,webp,avif}');

let totalKb = 0;
const violations: string[] = [];

for (const path of images) {
  const stat = await readFile(path);
  const kb = stat.length / 1024;
  totalKb += kb;
  if (kb > BUDGET_KB) {
    violations.push(`${path}: ${kb.toFixed(1)} KB > ${BUDGET_KB} KB`);
  }
}

if (violations.length) {
  console.error('Image budget violations:');
  violations.forEach((v) => console.error(`  ${v}`));
  process.exit(1);
}
```

## Real-World Use Cases

### 1. Setting Initial Budgets (No Baseline)

```text
Start with industry standards:
  • Initial JS:    < 200 KB gzipped (170 KB congestion window + buffer)
  • LCP:           < 2.5s (Core Web Vitals "good")
  • TTI:           < 3.5s on Slow 4G
  • Requests:      < 60 on first load

Iterate based on real-user data:
  • If p75 LCP is 1.5s, you have headroom — relax budget to 1.8s
  • If p75 LCP is 2.4s, tighten budget to 2.0s
```

### 2. Migrating to a New Bundler Without Regression

```text
Before: Webpack 5 produces 240 KB main bundle
After:  Rspack produces 180 KB main bundle

Set budget: 200 KB
Initial run: 180 KB → ✓
Future PRs: must stay < 200 KB
```

### 3. Multi-Team Budgets in a Monorepo

```javascript
// Per-package budgets
const budgets = {
  '@acme/web':         { main: '200 KB', vendor: '150 KB' },
  '@acme/admin':       { main: '150 KB', vendor: '100 KB' },
  '@acme/marketing':   { main: '100 KB', vendor: '50 KB' },
};
```

### 4. Performance Budget Gates in CI

```yaml
# PR fails if budget exceeded
- name: Bundle budget
  run: |
    npm run build
    npm run size
    if [ $? -ne 0 ]; then
      echo "::error::Bundle budget exceeded"
      exit 1
    fi
```

## Common Mistakes

### 1. Budget Without Buy-in

```text
❌ Bad: PM unilaterally sets a 100 KB budget that blocks every feature
✅ Good: team agrees on budgets tied to user data and business outcomes
```

### 2. Aggregate Budgets Only

```text
❌ Bad: "Total JS < 500 KB" — main bundle can be 400 KB + 100 lazy chunks
✅ Good: per-chunk + total budgets (main 200 KB, each chunk 100 KB)
```

### 3. Not Updating Budgets

```text
❌ Bad: budget from 2018 still enforced in 2024 (next.js app would fail)
✅ Good: review quarterly, set by current p75 field data
```

### 4. Forgetting About Third-Party

```text
❌ Bad: only budget first-party code, ignore Segment, Hotjar, Sentry, ads
✅ Good: budget third-party separately; monitor with RUM
```

### 5. No Plan When Budget Is Exceeded

When the budget is hit, what happens? Options:
- Lazy-load the new feature
- Replace a dependency (moment → date-fns)
- Image optimization
- Defer to next quarter

Without a plan, the team either ignores the budget or ships anyway.

## Best Practices

1. **Set budgets tied to user data** — what % of users are affected?
2. **Encode in CI** — humans forget, CI never does
3. **Per-chunk budgets** — not just total
4. **Show diff in PR** — `+5 KB` is actionable; `failed` is not
5. **Include third-party** — Segment and Sentry add up
6. **Review quarterly** — budgets are living targets
7. **Have a plan for "over budget"** — lazy load, replace deps, defer
8. **Track trend** — is the budget stable, growing, or shrinking?
9. **Set alerts before hard fail** — warn at 80% of budget
10. **Combine with RUM SLOs** — bundle size budget is a proxy; field data is truth

## Budget Tiers

```text
Bronze (achievable now):
  • Initial JS < 300 KB
  • LCP < 4.0s

Silver (good practice):
  • Initial JS < 200 KB
  • LCP < 2.5s
  • CLS < 0.1

Gold (excellent):
  • Initial JS < 100 KB
  • LCP < 1.8s
  • INP < 150ms
  • CLS < 0.05
```

## Performance Considerations

- size-limit runs in < 5s for typical apps
- bundlesize + size-limit output is JSON for CI parsing
- Per-chunk budgets need full build to measure (no partial builds)
- Compressed sizes (gzip / brotli) are what users experience

## Tools

| Tool | Purpose |
|------|---------|
| **size-limit** | Bundle size budgets, CI-friendly |
| **bundlesize** | Similar to size-limit, simpler config |
| **Lighthouse CI** | Web Vitals budgets in CI |
| **bundlewatch** | GitHub-native bundle tracking |
| **import-cost** | VSCode extension for inline size |
| **source-map-explorer** | Source-level bundle analysis |

## Summary

- Performance budgets are quantitative limits on user-facing metrics
- Set them in CI to prevent regressions
- Per-chunk budgets (not just total) catch large lazy routes
- Include third-party scripts in the budget
- Review quarterly — set by current p75 field data
- Have a plan for "over budget" — lazy load, optimize, defer
- Show diff in PR — `+5 KB` is actionable

---

## Cheat Sheet
```text
PERFORMANCE BUDGETS CHEAT SHEET
============================================================

TYPES:
  • Bundle size:    main < 200 KB, vendor < 150 KB
  • Per-chunk:      any route < 100 KB gzipped
  • Web Vitals:     LCP < 2.5s, INP < 200ms, CLS < 0.1
  • Image weight:   hero < 500 KB total
  • Request count:  < 60 on initial load

TOOLS:
  • size-limit (preferred) — per-chunk, gzipped
  • bundlesize — simpler, similar
  • Lighthouse CI — Web Vitals budgets
  • bundlewatch — GitHub native

EXAMPLE (size-limit):
  [
    { path: "dist/main.js", limit: "200 KB", gzip: true },
    { path: "dist/vendor.js", limit: "150 KB", gzip: true }
  ]

COMMON MISTAKES:
  • Aggregate budgets only (no per-chunk)
  • Never updating budgets
  • Ignoring third-party scripts
  • No plan when budget is exceeded

BEST PRACTICES:
  • Encode in CI (humans forget)
  • Show diff in PR (+5 KB is actionable)
  • Per-chunk + total budgets
  • Include third-party
  • Review quarterly
  • Set by p75 field data, not lab

INTERVIEW TIPS:
  • Explain why per-chunk budgets matter
  • Discuss size-limit vs Lighthouse CI roles
  • Show how to set budgets from field data
  • Mention the 170 KB congestion window rule
```
---

## See Also
- [Accessibility](../25-Accessibility/)
- [Build Tools](../23-Build-Tools/)
- [Bundle Analysis](06-Bundle-Analysis.md)
- [Core Web Vitals](01-Core-Web-Vitals.md)
- [Lighthouse CI](05-Lighthouse-CI.md)
- [Observability](../22-Observability/)
- [Performance APIs](02-Performance-APIs.md)
- [Profiling Tools](03-Profiling-Tools.md)
- [React](../03-React/)
- [Real User Monitoring](07-Real-User-Monitoring.md)

## References & Learn More

- [performancebudget.io](https://performancebudget.io/)
- [Size Limit](https://github.com/ai/size-limit)
- [Web Performance Budgets (Google)](https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/optimize-encoding-transfer)
- [Bundlephobia](https://bundlephobia.com/)
- [Tim Kadlec - Implementing a Performance Budget](https://timkadlec.com/remembers/2018-08-09-implementing-a-performance-budget/)
- [Lighthouse CI Budgets](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/budgets.md)
