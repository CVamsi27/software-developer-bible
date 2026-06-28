# Core Web Vitals

## Definition
Core Web Vitals are a set of standardized metrics from Google that measure real-world user experience for loading performance, interactivity, and visual stability of web pages. They are part of Google's Page Experience signals and directly impact SEO rankings.

## Why Do We Need It?
- **SEO Impact**: Google uses Core Web Vitals as a ranking factor
- **User Experience**: Slow, janky pages cause user abandonment
- **Business Metrics**: Performance directly correlates with conversion rates
- **Standardization**: Provides consistent, measurable benchmarks across all websites
- **Actionable Data**: Focuses on metrics that matter to real users

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                      CORE WEB VITALS                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │     LCP     │  │     INP     │  │     CLS     │  │   FID     │ │
│  │   (Loading) │  │(Interaction)│  │  (Stability) │  │ (Legacy) │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘ │
│         │                │                │               │        │
│         ▼                ▼                ▼               ▼        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    USER EXPERIENCE                          │   │
│  │  • How fast content loads                                   │   │
│  │  • How responsive the page feels                            │   │
│  │  • How stable the layout remains                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Thresholds:                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Good:          Needs Improvement:       Poor:              │   │
│  │  LCP ≤ 2.5s     LCP 2.5-4.0s           LCP > 4.0s          │   │
│  │  INP ≤ 200ms    INP 200-500ms          INP > 500ms          │   │
│  │  CLS ≤ 0.1      CLS 0.1-0.25           CLS > 0.25          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Metrics Deep Dive

### LCP (Largest Contentful Paint)
**Measures**: Loading performance - when the largest contentful element becomes visible

**Eligible Elements**:
- `<img>` elements
- `<video>` poster images
- Background images via `background-image`
- Block-level elements with text content

```text
Timeline: LCP Measurement
├── 0ms: Navigation starts
├── TTFB: First byte received
├── Resource Load: Images, fonts, CSS loaded
└── LCP Element Rendered ✓ (Target: ≤ 2.5s)
```

### INP (Interaction to Next Paint)
**Measures**: Responsiveness - time from user interaction to visual response

**Replaces**: First Input Delay (FID) in March 2024

**Interactions Measured**:
- Clicks
- Taps
- Keyboard input

```text
User Interaction Flow:
┌──────────┐     ┌──────────────┐     ┌─────────────┐     ┌────────────┐
│  Input   │ ──▶ │   Processing │ ──▶ │   Main      │ ──▶ │  Paint     │
│  Event   │     │   Delay      │     │   Thread    │     │  Response  │
└──────────┘     └──────────────┘     └─────────────┘     └────────────┘
                  (INP = Total Latency)
```

### CLS (Cumulative Layout Shift)
**Measures**: Visual stability - unexpected layout shifts during page lifecycle

**Formula**: CLS = Impact Fraction × Distance Fraction

```text
Layout Shift Example:
┌─────────────────────────────────────────────────┐
│ BEFORE:                    AFTER:               │
│ ┌───────────────────┐     ┌───────────────────┐ │
│ │                   │     │ [Ad Banner]       │ │ ← New element
│ │     Content       │     │                   │ │    inserted
│ │                   │     │     Content       │ │    above
│ │                   │     │                   │ │
│ └───────────────────┘     └───────────────────┘ │
│                           ↑ Layout shifted!      │
└─────────────────────────────────────────────────┘
```

## Code Examples

### 1. Web Vitals Library

```typescript
import { onLCP, onINP, onCLS, Metric } from 'web-vitals';

function sendToAnalytics(metric: Metric): void {
  const { name, delta, id, navigationType } = metric;

  // Send to your analytics endpoint
  const body = JSON.stringify({
    name,
    value: delta,
    id,
    navigationType,
    page: window.location.pathname,
    timestamp: Date.now(),
  });

  // Use sendBeacon for non-blocking analytics
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/analytics', body);
  } else {
    fetch('/api/analytics', { body, method: 'POST', keepalive: true });
  }
}

// Initialize Core Web Vitals reporting
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### 2. Custom Performance Observer

```typescript
// Advanced LCP tracking with element details
function observeLCP(): void {
  const observer = new PerformanceObserver((entryList) => {
    const entries = entryList.getEntries();
    const lastEntry = entries[entries.length - 1] as LargestContentfulPaint;

    console.log('LCP:', lastEntry.startTime);
    console.log('LCP Element:', lastEntry.element);
    console.log('LCP URL:', lastEntry.url);
    console.log('LCP Size:', lastEntry.size);
  });

  observer.observe({ type: 'largest-contentful-paint', buffered: true });
}

// CLS tracking with session window
function observeCLS(): void {
  let clsValue = 0;
  let clsEntries: LayoutShift[] = [];

  const observer = new PerformanceObserver((entryList) => {
    for (const entry of entryList.getEntries()) {
      if (!(entry as LayoutShift).hadRecentInput) {
        clsValue += (entry as LayoutShift).value;
        clsEntries.push(entry as LayoutShift);
      }
    }
  });

  observer.observe({ type: 'layout-shift', buffered: true });

  // Report on page visibility change
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      console.log('CLS:', clsValue);
      console.log('CLS Entries:', clsEntries);
    }
  });
}
```

### 3. Performance Budget Setup

```typescript
// Define performance budgets
interface PerformanceBudget {
  lcp: number;
  inp: number;
  cls: number;
  fcp: number;
  ttfb: number;
}

const budgets: PerformanceBudget = {
  lcp: 2500,    // 2.5s
  inp: 200,     // 200ms
  cls: 0.1,     // 0.1
  fcp: 1800,    // 1.8s
  ttfb: 800,    // 800ms
};

function checkBudget(metric: string, value: number): {
  passed: boolean;
  budget: number;
  status: 'good' | 'needs-improvement' | 'poor';
} {
  const budget = budgets[metric as keyof PerformanceBudget];
  const ratio = value / budget;

  let status: 'good' | 'needs-improvement' | 'poor';
  if (ratio <= 1) status = 'good';
  else if (ratio <= 1.6) status = 'needs-improvement';
  else status = 'poor';

  return {
    passed: ratio <= 1,
    budget,
    status,
  };
}
```

### 4. React Hook for Web Vitals

```typescript
import { useEffect, useRef } from 'react';
import { onLCP, onINP, onCLS, Metric } from 'web-vitals';

interface WebVitalsState {
  lcp: Metric | null;
  inp: Metric | null;
  cls: Metric | null;
}

export function useWebVitals(callback?: (metric: Metric) => void): WebVitalsState {
  const metrics = useRef<WebVitalsState>({
    lcp: null,
    inp: null,
    cls: null,
  });

  useEffect(() => {
    const handleMetric = (metric: Metric) => {
      metrics.current[metric.name.toLowerCase() as keyof WebVitalsState] = metric;
      callback?.(metric);
    };

    onLCP(handleMetric);
    onINP(handleMetric);
    onCLS(handleMetric);
  }, [callback]);

  return metrics.current;
}
```

### 5. Lighthouse CI Integration

```yaml
# lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      numberOfRuns: 3,
      settings: {
        preset: 'desktop',
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['warn', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'interactive': ['error', { maxNumericValue: 3800 }],
      },
    },
    upload: {
      target: 'lhci',
    },
  },
};
```

## Real-World Use Cases

### E-Commerce Optimization
```typescript
// Track product page performance
function trackProductPageMetrics(productId: string): void {
  onLCP((metric) => {
    // LCP for product images
    sendToAnalytics({
      event: 'product_lcp',
      productId,
      value: metric.value,
      element: metric.element?.tagName,
    });
  });

  onINP((metric) => {
    // Track add-to-cart button responsiveness
    sendToAnalytics({
      event: 'product_inp',
      productId,
      value: metric.value,
    });
  });
}
```

### Content Website
```typescript
// Monitor article reading experience
function trackArticleMetrics(articleId: string): void {
  onCLS((metric) => {
    // CLS affects reading experience
    if (metric.value > 0.1) {
      console.warn(`High CLS on article ${articleId}: ${metric.value}`);
      reportLayoutIssue({
        articleId,
        cls: metric.value,
        entries: metric.entries,
      });
    }
  });
}
```

## Common Mistakes

1. **Measuring only lab data**: Real user metrics (RUM) differ from Lighthouse
2. **Ignoring INP**: FID only measured first interaction; INP measures all
3. **Not accounting for dynamic content**: CLS from lazy-loaded images
4. **Over-optimizing**: Chasing perfect scores at the cost of features
5. **Not monitoring in production**: Dev environment metrics aren't representative

## Best Practices

1. **Use RUM**: Real User Monitoring reflects actual user experience
2. **Set performance budgets**: Define acceptable thresholds per metric
3. **Monitor continuously**: Track metrics over time, not just point-in-time
4. **Segment data**: Break down by device, connection, geography
5. **Optimize critical path**: Focus on above-the-fold content first
6. **Preload critical resources**: Use `<link rel="preload">` strategically
7. **Optimize images**: Use modern formats (WebP, AVIF), lazy load

## Performance Considerations

```text
Optimization Priority Matrix:
┌─────────────────────────────────────────────────────────────┐
│  High Impact, Low Effort:                                   │
│  • Compress images                                          │
│  • Enable text compression (Brotli)                         │
│  • Cache static assets                                      │
│  • Preload critical resources                               │
├─────────────────────────────────────────────────────────────┤
│  High Impact, High Effort:                                  │
│  • Code splitting                                           │
│  • Server-side rendering                                    │
│  • Edge caching                                             │
│  • Database optimization                                    │
├─────────────────────────────────────────────────────────────┤
│  Low Impact, Low Effort:                                    │
│  • Minify CSS/JS                                            │
│  • Optimize web fonts                                       │
│  • Reduce third-party scripts                               │
├─────────────────────────────────────────────────────────────┤
│  Low Impact, High Effort:                                   │
│  • Rewrite in different framework                           │
│  • Custom build pipeline                                    │
└─────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)
1. **What are Core Web Vitals?**
   - Answer: Standardized metrics measuring real user experience for loading (LCP), interactivity (INP), and visual stability (CLS).

2. **What does LCP measure?**
   - Answer: Largest Contentful Paint measures when the largest contentful element becomes visible, targeting ≤ 2.5 seconds.

3. **What replaced FID?**
   - Answer: INP (Interaction to Next Paint) replaced FID in March 2024, measuring all interactions rather than just the first.

4. **What is a good CLS score?**
   - Answer: CLS ≤ 0.1 is considered good, 0.1-0.25 needs improvement, and > 0.25 is poor.

5. **How do you measure Core Web Vitals?**
   - Answer: Using the web-vitals library, Chrome DevTools, or Lighthouse.

### Intermediate (5)
6. **How do you track Core Web Vitals in production?**
   - Answer: Use web-vitals library with sendBeacon API to send metrics to analytics endpoint.

7. **What is the web-vitals library?**
   - Answer: A Google library that provides functions to measure Core Web Vitals with a consistent API.

8. **How do you measure CLS for dynamic content?**
   - Answer: Use session windows to group layout shifts and avoid penalizing intentional shifts.

9. **What is the relationship between CWV and SEO?**
   - Answer: Google uses Core Web Vitals as a Page Experience signal, directly impacting search rankings.

10. **How do you set up performance budgets?**
    - Answer: Define thresholds for each metric and fail CI/CD if budgets are exceeded.

### Senior (10)
11. **Explain CLS score calculation**
    - Answer: CLS = Impact Fraction × Distance Fraction, where Impact Fraction is how much viewport was affected and Distance Fraction is how far elements moved.

12. **How do you handle third-party impact on CWV?**
    - Answer: Lazy load non-critical scripts, use async/defer, consider web workers for heavy computation.

13. **What is the relationship between TTFB and LCP?**
    - Answer: TTFB is the foundation; LCP cannot be faster than TTFB. Optimize server response first.

14. **How do you measure INP for complex interactions?**
    - Answer: INP measures the latency of all interactions, reporting the worst case (p98 or higher).

15. **Explain the difference between lab and field metrics**
    - Answer: Lab metrics (Lighthouse) are controlled; field metrics (RUM) reflect real users with varying devices and networks.

16. **How do you optimize LCP for SPAs?**
    - Answer: SSR/SSG, preload critical resources, optimize image loading, avoid render-blocking resources.

17. **What causes layout shifts?**
    - Answer: Images without dimensions, dynamic content injection, web fonts causing FOIT/FOUT, late-loading ads.

18. **How do you handle CWV in a micro-frontend architecture?**
    - Answer: Measure each micro-frontend's contribution, aggregate metrics, and optimize load order.

19. **What is the impact of CWV on conversion rates?**
    - Answer: Studies show 1-second delay in LCP can reduce conversions by 7%, and 100ms delay in INP can reduce conversions by 1%.

20. **How do you prioritize CWV optimizations?**
    - Answer: Focus on metrics where you're closest to thresholds, have highest business impact, and lowest implementation effort.

### FAANG-style (5)
21. **Design a CWV monitoring system**
    - Answer: Collect metrics via web-vitals, buffer locally, send via sendBeacon, process with streaming pipeline (Kafka), store in time-series DB, visualize with dashboards.

22. **How would you detect CWV regressions automatically?**
    - Answer: Statistical comparison of metric distributions, anomaly detection, A/B testing with CWV as guardrail metric.

23. **Explain the performance waterfall for a typical page load**
    - Answer: DNS → TCP → TLS → TTFB → First Byte → DOMContentLoaded → Load → LCP → INP (user interaction).

24. **How do you optimize CWV for global audiences?**
    - Answer: Edge caching, CDN, regional deployment, consider network conditions in different geographies.

25. **What is the relationship between CWV and Core Business Metrics?**
    - Answer: CWV improvements correlate with increased engagement, reduced bounce rates, and higher conversion rates.

### Follow-ups (5)
26. **How do you handle CWV measurement in iframes?**
    - Answer: Use PerformanceObserver in the iframe, or use postMessage to communicate metrics to parent.

27. **What is the impact of Service Workers on CWV?**
    - Answer: Service workers can improve TTFB and LCP through caching, but can also cause issues if not implemented correctly.

28. **How do you measure CWV for AMP pages?**
    - Answer: AMP has built-in performance guarantees, but you can still use web-vitals library for measurement.

29. **Explain the difference between FCP and LCP**
    - Answer: FCP measures when any content renders; LCP measures when the largest contentful element renders. LCP is often the hero image or main text.

30. **How do you optimize CWV for news websites with heavy ad loads?**
    - Answer: Lazy load ads, use placeholder dimensions, optimize ad loading order, consider ad-free experiences for better metrics.

## Summary

Core Web Vitals are essential metrics for measuring and improving user experience. Focus on LCP (loading), INP (interactivity), and CLS (visual stability) to ensure your website provides a good user experience and ranks well in search results.

## References & Learn More

- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Google Search Central - CWV](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [web-vitals Library](https://github.com/GoogleChrome/web-vitals)
- [Chrome DevTools - Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/)
