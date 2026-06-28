# Performance Monitoring Interview Questions

## Definition
This comprehensive guide covers 25+ interview questions on performance monitoring, ranging from Core Web Vitals fundamentals to advanced real-user monitoring system design.

## Why Do We Need It?
- **Technical Interviews**: Performance monitoring is a critical skill for senior engineers
- **System Design**: Understanding performance is essential for scalable architecture
- **User Experience**: Directly impacts business metrics and user satisfaction
- **Debugging Skills**: Essential for identifying and fixing production issues

## How It Works

```
Interview Question Categories:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Fundamentals│  │   Practical │  │      System Design      │ │
│  │             │  │             │  │                         │ │
│  │ • CWV       │  │ • Debugging │  │ • RUM Systems           │ │
│  │ • APIs      │  │ • Profiling │  │ • Monitoring Dashboards │ │
│  │ • Metrics   │  │ • Tools     │  │ • Alerting Systems      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Common Interview Answer Patterns

```typescript
// Pattern 1: Define → Explain → Code Example → Real-world
function answerPattern(question: string): string {
  return `
    1. Definition: What ${question} is
    2. Explanation: How it works and why it matters
    3. Code Example: Practical implementation
    4. Real-world: Production use case
  `;
}

// Pattern 2: Problem → Solution → Trade-offs
function problemSolutionPattern(problem: string): string {
  return `
    1. Problem: ${problem}
    2. Solution: Approach taken
    3. Trade-offs: What we gained and what we lost
  `;
}
```

## Interview Questions

### Beginner (5)

**Q1: What are Core Web Vitals?**
- **Answer**: Core Web Vitals are three metrics from Google measuring real user experience: LCP (Largest Contentful Paint) for loading, INP (Interaction to Next Paint) for interactivity, and CLS (Cumulative Layout Shift) for visual stability.

**Q2: What does LCP measure and what is a good score?**
- **Answer**: LCP measures when the largest contentful element (image, video poster, text block) becomes visible. Good: ≤ 2.5s, Needs Improvement: 2.5-4.0s, Poor: > 4.0s.

**Q3: What is the difference between FID and INP?**
- **Answer**: FID only measured the delay of the first user interaction. INP measures the latency of ALL interactions throughout the page lifecycle, providing a more complete picture of responsiveness. INP replaced FID in March 2024.

**Q4: How do you measure Core Web Vitals?**
- **Answer**: Use the `web-vitals` library, Chrome DevTools (Performance tab), Lighthouse, or Chrome UX Report for field data.

**Q5: What is CLS and how is it calculated?**
- **Answer**: CLS (Cumulative Layout Shift) measures visual stability. It's calculated as: CLS = Impact Fraction × Distance Fraction, where Impact Fraction is how much viewport was affected and Distance Fraction is how far elements moved.

### Intermediate (5)

**Q6: How do you track Core Web Vitals in production?**
- **Answer**:
```typescript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({ name: metric.name, value: metric.delta });
  navigator.sendBeacon('/api/analytics', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```
Use `sendBeacon` for non-blocking metric submission.

**Q7: What is the difference between lab and field metrics?**
- **Answer**: Lab metrics (Lighthouse, WebPageTest) are collected in controlled environments with simulated conditions. Field metrics (Real User Monitoring) are collected from actual users in real-world conditions. Field data is more representative but harder to control.

**Q8: How do you set up performance budgets?**
- **Answer**: Define thresholds for each metric (e.g., LCP ≤ 2.5s, CLS ≤ 0.1), integrate with CI/CD (Lighthouse CI), and fail builds when budgets are exceeded. Track budgets in `lighthouserc.js` or similar configuration.

**Q9: What causes layout shifts and how do you prevent them?**
- **Answer**: Causes: Images without dimensions, dynamic content injection, web fonts causing FOIT/FOUT, late-loading ads. Prevention: Set explicit dimensions, use `aspect-ratio`, preload fonts, reserve space for dynamic content.

**Q10: How do you measure performance of a Single Page Application?**
- **Answer**: Track route change duration, component render time, data loading time. Use custom performance marks for app-specific metrics. Measure First Input Delay for initial load, and interaction latency for subsequent navigation.

### Senior (10)

**Q11: Explain the Navigation Timing API and its key metrics.**
- **Answer**: Navigation Timing provides detailed page load timing:
- `navigationStart`: When navigation begins
- `domainLookupStart/End`: DNS resolution
- `connectStart/End`: TCP connection
- `responseStart`: First byte received (TTFB)
- `domContentLoaded`: DOM ready
- `loadEventEnd`: Page fully loaded

**Q12: How do you handle performance monitoring in a micro-frontend architecture?**
- **Answer**: Each micro-frontend reports metrics to a parent container via `postMessage`. Aggregate metrics at the shell level, attribute performance to specific micro-frontends, and track cross-micro-frontend interactions.

**Q13: What is the relationship between TTFB and LCP?**
- **Answer**: TTFB is the foundation - LCP cannot be faster than TTFB. TTFB = DNS + TCP + TLS + Server Processing. Optimize server response time first, then focus on content rendering for LCP.

**Q14: How do you optimize LCP for a content-heavy website?**
- **Answer**:
1. Preload critical resources (`<link rel="preload">`)
2. Optimize images (modern formats, responsive images)
3. Server-side rendering or static generation
4. Remove render-blocking resources
5. Use CDN for edge caching

**Q15: Explain how you would design a Real User Monitoring (RUM) system.**
- **Answer**:
1. Collect: web-vitals library + custom metrics
2. Buffer: localStorage with batched sends
3. Transport: sendBeacon API
4. Process: Streaming pipeline (Kafka/Kinesis)
5. Store: Time-series database (InfluxDB/TimescaleDB)
6. Visualize: Grafana/Datadog dashboards
7. Alert: Anomaly detection on metric distributions

**Q16: How do you handle third-party script impact on performance?**
- **Answer**: Lazy load non-critical scripts, use `async`/`defer`, consider Web Workers for heavy computation, monitor Third-Party impact with Lighthouse, implement loading strategies (consent-based, intersection observer).

**Q17: What is the difference between FCP and LCP?**
- **Answer**: FCP (First Contentful Paint) measures when any content renders. LCP measures when the largest contentful element renders. LCP is often the hero image or main text block. FCP gives early feedback; LCP represents meaningful content load.

**Q18: How do you detect and fix memory leaks?**
- **Answer**: Use Chrome DevTools Memory tab, take heap snapshots and compare, look for growing detached DOM elements, check event listener cleanup. Common causes: forgotten event listeners, closures holding references, detached DOM nodes.

**Q19: Explain the impact of web fonts on performance.**
- **Answer**: Fonts cause FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text). Optimize with `font-display: swap`, preload critical fonts, subset fonts, use system fonts when possible, consider variable fonts.

**Q20: How do you optimize performance for global audiences?**
- **Answer**: Use CDN for edge caching, implement regional deployment, optimize for different network conditions, consider adaptive loading based on connection speed, use service workers for offline support.

### FAANG-style (5)

**Q21: Design a performance monitoring system that handles 1 billion events per day.**
- **Answer**:
1. Collection: Client-side SDK with sampling
2. Ingestion: Kafka/Kinesis for streaming
3. Processing: Flink/Spark for real-time aggregation
4. Storage: Time-series DB (Druid/TimescaleDB) + data lake
5. Query: Pre-aggregated metrics for dashboards
6. Alerting: Anomaly detection with ML models
7. Visualization: Grafana with custom dashboards

**Q22: How would you detect performance regressions automatically?**
- **Answer**:
1. Statistical comparison of metric distributions (p50, p95, p99)
2. Anomaly detection using ML models
3. A/B testing with CWV as guardrail metric
4. Canary deployments with automated rollback
5. CI/CD integration with performance budgets

**Q23: Explain the performance waterfall and how to optimize it.**
- **Answer**: Waterfall: DNS → TCP → TLS → TTFB → First Byte → DOMContentLoaded → Load → LCP. Optimization: DNS prefetch, connection pooling, HTTP/2 multiplexing, critical resource inlining, lazy loading.

**Q24: How do you handle performance measurement in Server-Side Rendering?**
- **Answer**: Combine server-side timing (TTFB, render time) with client-side metrics (hydration time, interactivity). Use `PerformanceObserver` for client metrics, server logs for backend timing, and trace IDs to correlate.

**Q25: Design a system to track performance across micro-frontends.**
- **Answer**:
1. Each micro-frontend reports to parent via postMessage
2. Shell aggregates metrics with micro-frontend identifiers
3. Use distributed tracing (OpenTelemetry) for cross-service metrics
4. Dashboard shows per-team performance
5. Alert on team-specific regressions

### Follow-ups (5)

**Q26: How do you handle performance in a Progressive Web App?**
- **Answer**: Service workers for caching, offline-first architecture, background sync, push notifications. Measure both online and offline performance, track cache hit rates.

**Q27: What is the impact of HTTP/2 on performance?**
- **Answer**: Multiplexing (parallel requests), header compression, server push. Reduces waterfall by allowing parallel resource loading, but requires careful resource prioritization.

**Q28: How do you profile performance in development vs production?**
- **Answer**: Development: React DevTools, Why Did You Render, custom profilers. Production: Lighthouse, RUM, APM tools (Datadog, New Relic). Always test with production builds and realistic data.

**Q29: Explain the relationship between performance and SEO.**
- **Answer**: Google uses Core Web Vitals as a Page Experience signal. Better CWV = better rankings. Focus on LCP for loading, INP for interactivity, CLS for stability.

**Q30: How do you handle performance monitoring during incidents?**
- **Answer**: Have pre-defined dashboards for incident response, alert on metric thresholds, use distributed tracing to identify bottlenecks, communicate performance impact to stakeholders.

## Best Practices for Interview Answers

### Structure Your Answer
```
1. Direct Answer (1-2 sentences)
2. Explanation (2-3 sentences)
3. Code Example (if applicable)
4. Real-world Application (1-2 sentences)
5. Trade-offs/Considerations (1-2 sentences)
```

### Common Follow-up Questions
- "How would you implement this in production?"
- "What are the trade-offs of this approach?"
- "How do you handle edge cases?"
- "What metrics would you track?"
- "How do you ensure reliability at scale?"

### Key Metrics to Remember
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5-4.0s | > 4.0s |
| INP | ≤ 200ms | 200-500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1-0.25 | > 0.25 |
| FCP | ≤ 1.8s | 1.8-3.0s | > 3.0s |
| TTFB | ≤ 800ms | 800-1800ms | > 1800ms |

## Summary

Performance monitoring interviews test your understanding of web performance metrics, tools, and optimization strategies. Focus on Core Web Vitals, practical implementation, and system design for large-scale monitoring.

## References & Learn More

- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Google Search Central - CWV](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/)
- [web-vitals Library](https://github.com/GoogleChrome/web-vitals)
