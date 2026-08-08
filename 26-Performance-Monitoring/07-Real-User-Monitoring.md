---
section: Performance Monitoring
category: Quality
tags: [concept, reference, guide]
---

# Real User Monitoring (RUM)

## Definition

**Real User Monitoring (RUM)** captures performance data from actual users in production, as opposed to synthetic tests (Lighthouse, WebPageTest) which run in controlled lab environments. RUM reveals the **p75 / p95 / p99** of Core Web Vitals across real devices, networks, and geographies — the data Google uses for SEO ranking via the Chrome User Experience Report (CrUX).

RUM is essential because lab tests can't replicate the diversity of real users: 4-year-old Android phones on slow 3G, hotel WiFi in a remote area, or a corporate laptop behind a VPN. If you optimize only for Lighthouse 100, you may miss the actual experience of your slowest 25% of users.

## Why Do We Need It?

1. **SEO ranking signal**: Google uses CrUX (field data) — not Lighthouse — for Page Experience
2. **Catch real-world issues** that synthetic tests miss (slow networks, old devices, geo latency)
3. **Set realistic SLOs** based on actual user data, not aspirational lab scores
4. **Segment by dimension** (device tier, country, browser) to find underserved populations
5. **A/B test performance changes** in production with statistical significance
6. **Detect regressions** before users complain (with alerting on p75 regressions)

## Lab vs Field

| Aspect | Lab (Lighthouse, WPT) | Field (RUM, CrUX) |
|--------|----------------------|--------------------|
| Environment | Controlled (specific device, network) | Real users (millions of variations) |
| Repeatability | Highly reproducible | Varies by user |
| Coverage | One URL, one device | All URLs, all devices |
| Speed | Run on demand | Continuous collection |
| Use case | Pre-release verification, CI gate | Production monitoring, SEO |
| Data volume | Small (per run) | Massive (millions of page views) |
| Cost | Free (run yourself) | $$ (collection + storage) |
| Tail latency | Limited to 1-3 runs | p95/p99 from real users |

## How It Works

### RUM Data Flow

```text
┌──────────────────────────────────────────────────────────────────┐
│                       RUM Data Flow                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User loads page in browser                                    │
│       │                                                          │
│       ▼                                                          │
│  2. web-vitals JS library measures LCP, INP, CLS                   │
│       │                                                          │
│       ▼                                                          │
│  3. On page hide (visibilitychange / pagehide)                    │
│     Send metrics to RUM endpoint via beacon (navigator.sendBeacon)│
│       │                                                          │
│       ▼                                                          │
│  4. Backend aggregates into time-series DB                        │
│       │                                                          │
│       ├──► Real-time dashboard (Datadog, Grafana)                 │
│       ├──► Alerting (PagerDuty on regressions)                    │
│       └──► BigQuery / data warehouse for long-term analysis      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Metrics Captured

| Metric | Source | Why It Matters |
|--------|--------|----------------|
| **LCP** | Largest Contentful Paint | Perceived load speed |
| **INP** | Interaction to Next Paint | Interactivity |
| **CLS** | Layout Shift API | Visual stability |
| **TTFB** | Navigation Timing | Server response time |
| **FCP** | Paint Timing | First content render |
| **Long Tasks** | PerformanceObserver | Main-thread blocking > 50ms |
| **Resource Timing** | Resource Timing API | Slow assets, third-party impact |
| **Custom Marks** | User Timing API | Business-specific events |
| **Device info** | navigator.userAgent | Device tier, OS, browser segmentation |
| **Connection** | navigator.connection | Network type (4g, wifi, slow-2g) |
| **Page URL** | location.href | Per-page performance |

## Code Examples

### web-vitals Library (Google's Official)

```typescript
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

// Send to analytics on each metric
function sendMetric(metric: { name: string; value: number; id: string; rating: string }) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id,
    rating: metric.rating, // 'good' | 'needs-improvement' | 'poor'
    page: window.location.pathname,
    timestamp: Date.now(),
    connection: (navigator as any).connection?.effectiveType,
  });

  // Use sendBeacon for reliability (survives page unload)
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/rum', body);
  } else {
    fetch('/api/rum', { body, method: 'POST', keepalive: true });
  }
}

onLCP(sendMetric);
onINP(sendMetric);
onCLS(sendMetric);
onFCP(sendMetric);
onTTFB(sendMetric);
```

### Custom Marks and Measures

```typescript
// Mark business-critical events
performance.mark('cart-opened');
performance.mark('checkout-clicked');
performance.measure('cart-to-checkout', 'cart-opened', 'checkout-clicked');

// Observe long tasks (blocks main thread > 50ms)
const ltObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 50) {
      console.warn('Long task detected:', entry.duration, 'ms');
      // Send to RUM
      sendMetric({
        name: 'long-task',
        value: entry.duration,
        id: 'long-task-' + Date.now(),
        rating: entry.duration > 100 ? 'poor' : 'needs-improvement',
      });
    }
  }
});
ltObserver.observe({ entryTypes: ['longtask'] });
```

### Resource Timing Analysis

```typescript
// Find slow resources
const resourceObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 1000) {  // > 1s is a problem
      console.warn('Slow resource:', entry.name, entry.duration);
    }
  }
});
resourceObserver.observe({ entryTypes: ['resource'] });
```

### Backend Aggregation (Example: ClickHouse)

```sql
-- p75 LCP by country (last 7 days)
SELECT
  country,
  quantile(0.75)(lcp_value) AS p75_lcp
FROM rum_events
WHERE event_name = 'LCP' AND ts > now() - INTERVAL 7 DAY
GROUP BY country
ORDER BY p75_lcp DESC
LIMIT 20;
```

```sql
-- % of users with good LCP by device tier
SELECT
  device_tier,
  countIf(lcp_value <= 2500) / count(*) AS pct_good_lcp
FROM rum_events
WHERE event_name = 'LCP' AND ts > now() - INTERVAL 1 DAY
GROUP BY device_tier;
```

### React Hook for RUM

```typescript
import { useEffect } from 'react';
import { onLCP, onINP, onCLS } from 'web-vitals';

export function useRUM(endpoint: string) {
  useEffect(() => {
    const report = (metric: any) => {
      const body = JSON.stringify({
        name: metric.name,
        value: metric.value,
        id: metric.id,
        rating: metric.rating,
        route: window.location.pathname,
      });
      navigator.sendBeacon(endpoint, body);
    };

    onLCP(report);
    onINP(report);
    onCLS(report);
  }, [endpoint]);
}

// In app root
function App() {
  useRUM('/api/rum');
  return <Routes />;
}
```

## Real-World Use Cases

### 1. Alerting on Real User Regressions

```yaml
# Prometheus alert: p75 LCP regression
- alert: RealUserLCPRegression
  expr: |
    (
      histogram_quantile(0.75,
        sum by (le) (rate(rum_lcp_bucket[1h]))
      )
      >
      (
        histogram_quantile(0.75,
          sum by (le) (rate(rum_lcp_bucket[1h] offset 7d))
        ) * 1.2
      )
    )
  for: 30m
  annotations:
    summary: "Real-user p75 LCP regressed 20% vs 7-day baseline"
```

### 2. Segmenting Performance by Device Tier

```typescript
// Tag events with device tier
function getDeviceTier(): 'low' | 'mid' | 'high' {
  const memory = (navigator as any).deviceMemory || 4;  // GB
  const cores = navigator.hardwareConcurrency || 4;
  if (memory <= 2 || cores <= 2) return 'low';
  if (memory <= 4 || cores <= 4) return 'mid';
  return 'high';
}

function sendMetric(metric: any) {
  const body = {
    ...metric,
    device_tier: getDeviceTier(),
    connection: (navigator as any).connection?.effectiveType,
    page: window.location.pathname,
  };
  navigator.sendBeacon('/api/rum', JSON.stringify(body));
}
```

### 3. A/B Test Performance Impact

```typescript
// Compare LCP for users in experiment vs control
const variant = window.__EXPERIMENT__?.variant;  // 'control' | 'treatment'

onLCP((metric) => {
  sendMetric({ ...metric, experiment: variant });
});

// Analysis: p75 LCP treatment vs control
// If treatment p75 > control p75 + delta, the change hurts real users
```

### 4. CrUX Integration (Free RUM Data)

```typescript
// Use the CrUX API to get field data for any URL (public)
const cruxResponse = await fetch(
  `https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=${API_KEY}`,
  {
    method: 'POST',
    body: JSON.stringify({
      url: 'https://example.com',
      formFactor: 'PHONE',
    }),
  }
);

const { record } = await cruxResponse.json();
console.log('p75 LCP:', record.metrics.largest_contentful_paint?.percentiles?.p75);
console.log('p75 INP:', record.metrics.interaction_to_next_paint?.percentiles?.p75);
console.log('p75 CLS:', record.metrics.cumulative_layout_shift?.percentiles?.p75);
```

## Common Mistakes

### 1. Sampling Without Statistical Awareness

```typescript
// ❌ Bad: random 1% sample might miss regressions
if (Math.random() < 0.01) sendMetric(metric);

// ✅ Good: stratified sampling, always capture slow outliers
function shouldSample(): boolean {
  // Always report if metric is poor
  if (metric.rating === 'poor') return true;
  // Sample 10% of good / needs-improvement
  return Math.random() < 0.10;
}
```

### 2. Using fetch() Instead of sendBeacon

```typescript
// ❌ Bad: fetch() may not complete on page unload
window.addEventListener('unload', () => {
  fetch('/api/rum', { body: JSON.stringify(metrics) });
});

// ✅ Good: sendBeacon survives page unload
navigator.sendBeacon('/api/rum', JSON.stringify(metrics));
```

### 3. No Device/Connection Segmentation

Reporting aggregate LCP hides issues. A p75 of 2.0s sounds great — until you see it's 5s on low-end Android in India. Always segment.

### 4. Collecting PII in RUM Data

```typescript
// ❌ Bad: full URL with query params may include tokens
body: JSON.stringify({ url: window.location.href })

// ✅ Good: strip query params and PII
body: JSON.stringify({
  url: window.location.pathname,  // no query string
  // never include: user_id, email, search terms
})
```

## Best Practices

1. **Use `navigator.sendBeacon`** for reliability on page unload
2. **Sample intelligently** — always capture poor ratings, sample the rest
3. **Segment by device tier, country, connection type** — aggregate hides issues
4. **Strip PII** from URLs, headers, and metric bodies
5. **Set SLOs on p75 field data**, not lab scores
6. **Alert on regressions** vs 7-day rolling baseline
7. **Use the web-vitals library** (Google's official, used by Chrome team)
8. **Combine with synthetic** — RUM for truth, Lighthouse for pre-release gate
9. **Use CrUX public API** for free competitive benchmarking
10. **Test RUM impact** — bundle size, network calls, and storage cost

## Performance Considerations

- web-vitals.js bundle: ~5 KB gzipped
- sendBeacon size limit: 64 KB per beacon
- Backend cost: 1M pageviews × 5 metrics = 5M events/day → $$ storage
- Sampling: 10% of users = manageable cost, still statistically significant

## RUM Vendors

| Vendor | Type | Cost | Notes |
|--------|------|------|-------|
| **Datadog RUM** | SaaS | $$$ | Full APM, real-time, EU/US |
| **New Relic Browser** | SaaS | $$$ | Strong SPA support |
| **Sentry Performance** | SaaS | $$ | Integrated with error tracking |
| **Highlight.io** | SaaS | $ | Open source + hosted |
| **Elastic RUM** | Self-host | $ | Open source, you operate |
| **Cloudflare Web Analytics** | Free | Free | Privacy-first, basic metrics |
| **Custom (web-vitals + backend)** | DIY | $ | Most flexible, most work |

## Summary

- RUM captures real-user performance data; lab tests don't reflect reality
- Google uses CrUX field data for SEO — your SLOs should too
- Use `web-vitals` library + `navigator.sendBeacon` for collection
- Always segment by device tier, country, and connection
- Sample intelligently — keep poor ratings, sample the rest
- Alert on p75 regressions vs 7-day rolling baseline
- CrUX public API gives free competitive benchmarking

---

## Cheat Sheet
```text
REAL USER MONITORING CHEAT SHEET
============================================================

WHY:
  • Lab ≠ field (different devices, networks, geography)
  • Google uses field data (CrUX) for SEO ranking
  • SLOs should be on p75 field data, not Lighthouse

METRICS TO CAPTURE:
  • Core Web Vitals: LCP, INP, CLS (web-vitals library)
  • Navigation: TTFB, FCP
  • Long tasks: main-thread blocks > 50ms
  • Custom: business events (cart, checkout)

COLLECTION:
  import { onLCP, onINP, onCLS } from 'web-vitals';
  onLCP(metric => navigator.sendBeacon('/api/rum', JSON.stringify(metric)));

SEGMENTATION:
  • Device tier: navigator.deviceMemory, hardwareConcurrency
  • Connection: navigator.connection.effectiveType
  • Country, page, browser

COMMON MISTAKES:
  • fetch() instead of sendBeacon (data loss on unload)
  • No device segmentation (aggregate hides issues)
  • PII in URLs or metric bodies
  • Random sampling (misses poor ratings)

TOOLS:
  • web-vitals (Google's library)
  • CrUX API (free public field data)
  • Vendors: Datadog, New Relic, Sentry, Elastic

INTERVIEW TIPS:
  • Explain lab vs field difference
  • Discuss why p75 (Google's metric)
  • Walk through beacon + sendBeacon reliability
  • Mention segmentation and statistical sampling
```
---

## See Also
- [Accessibility](../25-Accessibility/)
- [Build Tools](../23-Build-Tools/)
- [Core Web Vitals](01-Core-Web-Vitals.md)
- [Lighthouse CI](05-Lighthouse-CI.md)
- [Observability](../22-Observability/)
- [Performance APIs](02-Performance-APIs.md)
- [Profiling Tools](03-Profiling-Tools.md)
- [React](../03-React/)

## References & Learn More

- [web-vitals Library](https://github.com/GoogleChrome/web-vitals)
- [Chrome User Experience Report](https://developer.chrome.com/docs/crux/)
- [CrUX API](https://developer.chrome.com/docs/crux/api/)
- [web.dev - Real User Monitoring](https://web.dev/articles/user-centric-performance-metrics)
- [MDN: PerformanceObserver](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver)
- [navigator.sendBeacon](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon)
- [RUM vs Synthetic](https://web.dev/articles/synthetic-vs-real-user-monitoring)
