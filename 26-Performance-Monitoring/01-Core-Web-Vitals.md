# Core Web Vitals

[![Category: Quality](https://img.shields.io/badge/category-Quality-brightgreen)](.)

sure real-world user experience for loading performance, interactivity, and visual stability of web pages. They are part of Google's Page Experience signals and directly impact SEO rankings.

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

## Summary

Core Web Vitals are essential metrics for measuring and improving user experience. Focus on LCP (loading), INP (interactivity), and CLS (visual stability) to ensure your website provides a good user experience and ranks well in search results.

---

## See Also
- [Accessibility](../25-Accessibility/)
- [Build Tools](../23-Build-Tools/)
- [Observability](../22-Observability/)
- [React](../03-React/)

## References & Learn More

- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Google Search Central - CWV](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [web-vitals Library](https://github.com/GoogleChrome/web-vitals)
- [Chrome DevTools - Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/)
