---
section: Performance Monitoring
category: Quality
tags: [concept, tool, guide]
---

# Lighthouse CI

## Definition

**Lighthouse CI** automates Lighthouse audits in CI/CD pipelines. It runs Lighthouse against a deployed or locally-served build, asserts against performance budgets, fails builds when regressions occur, and uploads results for historical tracking. It is the most common way to prevent performance regressions before they reach production.

Lighthouse CI is **not** the same as running `lighthouse` in a script. The `@lhci/cli` tool orchestrates multiple runs, applies statistical assertions, and uploads results to a server (or temporary public storage) for trend tracking across builds.

## Why Do We Need It?

1. **Regression prevention**: A "harmless" dependency upgrade can increase LCP by 800ms. Lighthouse CI blocks the PR.
2. **Performance budgets as code**: Encode "performance ≥ 90, LCP < 2.5s" in version control, not in tribal knowledge.
3. **Historical trend tracking**: See the line go up or down across commits.
4. **PR-level feedback**: Comment on the PR with the diff and which metric regressed.
5. **Standardized measurement**: Replace "Lighthouse is 85 on my machine" with reproducible CI runs.

## How It Works

### Architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│                      Lighthouse CI Flow                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. CI Build (GitHub Actions, GitLab CI, etc.)                   │
│       │                                                          │
│       ▼                                                          │
│  2. Build & serve app (next build && next start)                 │
│       │                                                          │
│       ▼                                                          │
│  3. @lhci/cli autorun                                            │
│       │   - collects N runs (default 1, recommended 3-5)         │
│       │   - applies assertions (fail/warn)                       │
│       │   - uploads to server                                    │
│       ▼                                                          │
│  4. Result                                                        │
│       ├── Pass: continue pipeline                                │
│       ├── Warn: PR comment, no block                              │
│       └── Fail: block merge                                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Assertable Metrics

| Metric | Type | Unit |
|--------|------|------|
| `performance` | score (0-1) | — |
| `accessibility` | score (0-1) | — |
| `best-practices` | score (0-1) | — |
| `seo` | score (0-1) | — |
| `first-contentful-paint` | numeric | ms |
| `largest-contentful-paint` | numeric | ms |
| `cumulative-layout-shift` | numeric | score |
| `total-blocking-time` | numeric | ms |
| `speed-index` | numeric | ms |
| `interactive` | numeric | ms |

## Code Examples

### lighthouserc.json (Standard Config)

```json
{
  "ci": {
    "collect": {
      "url": [
        "http://localhost:3000/",
        "http://localhost:3000/dashboard",
        "http://localhost:3000/checkout"
      ],
      "numberOfRuns": 3,
      "settings": {
        "preset": "desktop",
        "chromeFlags": "--no-sandbox"
      }
    },
    "assert": {
      "assertions": {
        "performance": ["error", { "minScore": 0.9 }],
        "accessibility": ["error", { "minScore": 0.95 }],
        "best-practices": ["error", { "minScore": 0.95 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 200 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### GitHub Actions Integration

```yaml
# .github/workflows/lhci.yml
name: Lighthouse CI
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - run: npm start &  # serve the production build
      - run: npx wait-on http://localhost:3000
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v11
        with:
          configPath: ./.lighthouserc.json
          uploadArtifacts: true
```

### Programmatic API (Node)

```typescript
import { start, upload } from '@lhci/cli';

async function runLighthouseCI() {
  // Custom assertions based on environment
  const result = await start({
    url: process.env.PREVIEW_URL,
    numberOfRuns: 5,
    settings: { preset: 'mobile' },
    assert: {
      assertions: {
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],
      },
    },
  });

  if (result.overallAssertionFailure) {
    throw new Error('Lighthouse CI failed - performance regression detected');
  }
}
```

## Real-World Use Cases

### 1. PR-Level Performance Gates

Block merges when performance drops below threshold:

```yaml
# In CI config - exit code 1 fails the build
- run: npx lhci autorun
  env:
    LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

### 2. Multi-Environment Tracking

Track scores across staging, preview, and production:

```json
{
  "ci": {
    "collect": {
      "url": [
        "https://staging.example.com/",
        "https://preview-123.example.com/"
      ]
    }
  }
}
```

### 3. Mobile + Desktop Split

Different budgets for each form factor:

```json
{
  "ci": {
    "collect": [
      {
        "url": "http://localhost:3000",
        "numberOfRuns": 3,
        "settings": { "preset": "mobile" }
      },
      {
        "url": "http://localhost:3000",
        "numberOfRuns": 3,
        "settings": { "preset": "desktop" }
      }
    ]
  }
}
```

## Common Mistakes

### 1. Single-Run Asserts (Noisy Failures)

```text
❌ Bad:  numberOfRuns: 1 — Lighthouse scores vary ±5 between runs
✅ Good: numberOfRuns: 3 or 5 — median reduces noise
```

Lighthouse scores are inherently noisy. A single run can swing 5-10 points. Use 3-5 runs and either median assertion or compare against baseline.

### 2. Asserting on `lighthouse-score` Without Knowing What It Measures

`performance` is a weighted score: FCP 10%, SI 10%, LCP 25%, TBT 30%, CLS 25%. A score of 90 might still have a poor LCP. Assert on raw metrics (LCP, INP, CLS) for harder guarantees.

### 3. Running Against the Dev Server

Dev mode includes source maps, hot-reload, and unminified code. LCP will be 3-5x worse. Always assert against the **production build**.

### 4. Ignoring Lab vs Field

Lighthouse CI runs in a synthetic environment. Real users may have slower devices, slower networks, and worse LCP. Complement with RUM (Real User Monitoring) for production signals.

## Best Practices

1. **Run on production build**, not dev server
2. **Use 3-5 runs** to dampen variance
3. **Assert on raw metrics** (LCP, INP, CLS), not just the overall score
4. **Separate mobile and desktop** presets
5. **Upload to a persistent server** (lhci-server, Treo) for historical trends
6. **Pair with size-limit** for bundle size assertions
7. **Skip on draft PRs** to save CI minutes
8. **Pin Chrome version** in CI to avoid engine drift

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| CI time | 3 runs × 5 URLs = 15 audits (~2-5 min) |
| Flake | Use median, more runs, stable hosting |
| Dev vs prod | Always serve production build |
| Lab vs field | Use Lighthouse for budgets, RUM for truth |

## Summary

- Lighthouse CI runs Lighthouse audits on every PR and blocks regressions
- `@lhci/cli` orchestrates multi-run audits with assertions and uploads
- `lighthouserc.json` defines URLs, runs, settings, and assertion budgets
- Assert on raw metrics (LCP < 2500ms) not just the overall score
- Always run on the **production build**, never dev mode
- Pair with RUM (Sentry, Datadog) to catch what synthetic tests miss

---

## Cheat Sheet
```text
LIGHTHOUSE CI CHEAT SHEET
============================================================

SETUP:
  npm install -D @lhci/cli
  npx lhci autorun    # uses .lighthouserc.json

CONFIG (.lighthouserc.json):
  • ci.collect.url         - URLs to audit
  • ci.collect.numberOfRuns - 3-5 for stability
  • ci.collect.settings.preset - "desktop" or "mobile"
  • ci.assert.assertions   - { metric: [level, { ... }] }
  • ci.upload.target       - "temporary-public-storage" or lhci-server

ASSERTION LEVELS:
  • "off"   - skip
  • "warn"  - comment but don't fail
  • "error" - fail the build (exit 1)

KEY METRICS:
  • performance:    score 0-1
  • lcp:            ms (2500 = good)
  • cls:            score (0.1 = good)
  • tbt:            ms (200 = good)
  • fcp, tti, si:   legacy but still tracked

GITHUB ACTION:
  uses: treosh/lighthouse-ci-action@v11
  with: { configPath: ./.lighthouserc.json }

INTERVIEW TIPS:
  • Mention multi-run noise reduction (3-5 runs)
  • Distinguish lab (Lighthouse) from field (CrUX/RUM)
  • Discuss why dev-server runs are misleading
  • Show how to gate PRs with assertion failures
```
---

## See Also
- [Accessibility](../25-Accessibility/)
- [Bundle Analysis](06-Bundle-Analysis.md)
- [Core Web Vitals](01-Core-Web-Vitals.md)
- [Profiling Tools](03-Profiling-Tools.md)

## References & Learn More

- [Lighthouse CI Documentation](https://github.com/GoogleChrome/lighthouse-ci)
- [Lighthouse GitHub Action](https://github.com/treosh/lighthouse-ci-action)
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)
- [Web Vitals Reference](https://web.dev/articles/vitals)
- [Lighthouse CI Server (self-hosted)](https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md#the-lighthouse-ci-server)
