---
section: Performance Monitoring
category: Quality
tags: [concept]
---

# Lighthouse CI

## Definition

**Lighthouse CI** automates Lighthouse performance, accessibility, SEO, and best-practice audits in CI/CD pipelines. It tracks scores over time, sets budgets to prevent regressions, and integrates with GitHub Actions for PR-level performance checks.

## Why Do We Need It?

1. **Performance regression prevention**: Block PRs that degrade LCP/CLS/TBT
2. **Score tracking**: Historical view of performance metrics
3. **Budgets**: Assert score thresholds (e.g., performance ≥ 90, accessibility ≥ 95)
4. **Assertions**: Fail builds when metrics regress beyond thresholds

## Code Examples

### Configuration

```json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000"],
      "numberOfRuns": 3,
      "settings": { "preset": "desktop" }
    },
    "assert": {
      "assertions": {
        "performance": ["warn", {"minScore": 0.9}],
        "accessibility": ["error", {"minScore": 0.95}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

---

### See Also

- [Bundle Analysis](06-Bundle-Analysis.md)
- [Core Web Vitals](01-Core-Web-Vitals.md)
- [Interview Questions](04-Interview-Questions.md)
- [Performance APIs](02-Performance-APIs.md)
- [Profiling Tools](03-Profiling-Tools.md)

### References

- [Lighthouse CI Documentation](https://github.com/GoogleChrome/lighthouse-ci)
- [Lighthouse GitHub Action](https://github.com/treosh/lighthouse-ci-action)
