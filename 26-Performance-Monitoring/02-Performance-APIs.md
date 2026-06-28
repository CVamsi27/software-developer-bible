# Performance APIs

## Definition
Performance APIs are browser APIs that provide detailed timing and performance data about web pages, resources, and user interactions. They enable developers to measure and optimize application performance with precise, low-level timing information.

## Why Do We Need It?
- **Precise Timing**: Millisecond-accurate measurements
- **Resource Monitoring**: Track loading of all page resources
- **Custom Metrics**: Create application-specific performance marks
- **Real User Monitoring**: Collect actual user performance data
- **Debugging**: Identify performance bottlenecks

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PERFORMANCE APIs HIERARCHY                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Performance Interface                     │   │
│  │  • now() - High resolution timestamp                        │   │
│  │  • timing - Navigation timing data                          │   │
│  │  • navigation - Navigation type information                 │   │
│  │  • memory - Memory usage (Chrome only)                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│         ┌────────────────────┼────────────────────┐                │
│         ▼                    ▼                    ▼                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │ Navigation  │    │   Resource  │    │    User     │            │
│  │   Timing    │    │   Timing    │    │    Timing   │            │
│  │             │    │             │    │             │            │
│  │ • domainLookup│  │ • fetchStart│    │ • mark()    │            │
│  │ • connect   │    │ • responseEnd│   │ • measure() │            │
│  │ • domLoading│    │ • duration  │    │ • getEntries│            │
│  │ • domComplete│   │ • transferSize│  │ • clearMarks│            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   PerformanceObserver                        │   │
│  │  • Listen for performance entry additions                   │   │
│  │  • Process entries asynchronously                           │   │
│  │  • Observe specific entry types                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Navigation Timing API

### Complete Navigation Timeline
```
Navigation Timing Model:
├── 0ms: start
├── ────: navigationStart
├── ────: unloadEventStart
├── ────: unloadEventEnd
├── ────: redirectStart
├── ────: redirectEnd
├── ────: fetchStart
├── ────: domainLookupStart
├── ────: domainLookupEnd
├── ────: connectStart
├── ────: secureConnectionStart (TLS)
├── ────: connectEnd
├── ────: requestStart
├── ────: responseStart
├── ────: responseEnd
├── ────: domLoading
├── ────: domInteractive
├── ────: domContentLoadedEventStart
├── ────: domContentLoadedEventEnd
├── ────: domComplete
├── ────: loadEventStart
└── ────: loadEventEnd
```

## Code Examples

### 1. Navigation Timing Data

```typescript
interface NavigationTiming {
  // Time to First Byte
  ttfb: number;
  
  // DNS Lookup
  dnsLookup: number;
  
  // TCP Connection
  tcpConnection: number;
  
  // TLS Negotiation
  tlsNegotiation: number;
  
  // Time to Content
  firstByte: number;
  contentLoaded: number;
  pageLoad: number;
  
  // DOM
  domInteractive: number;
  domComplete: number;
}

function getNavigationTiming(): NavigationTiming {
  const timing = performance.timing;
  
  return {
    ttfb: timing.responseStart - timing.requestStart,
    dnsLookup: timing.domainLookupEnd - timing.domainLookupStart,
    tcpConnection: timing.connectEnd - timing.connectStart,
    tlsNegotiation: timing.connectEnd - timing.secureConnectionStart,
    firstByte: timing.responseStart - timing.navigationStart,
    contentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
    pageLoad: timing.loadEventEnd - timing.navigationStart,
    domInteractive: timing.domInteractive - timing.navigationStart,
    domComplete: timing.domComplete - timing.navigationStart,
  };
}

// Modern Navigation Timing (Level 2)
function getNavigationTimingV2(): PerformanceNavigationTiming | null {
  const entries = performance.getEntriesByType('navigation');
  return entries.length > 0 ? entries[0] as PerformanceNavigationTiming : null;
}
```

### 2. Resource Timing

```typescript
interface ResourceTiming {
  name: string;
  type: string;
  duration: number;
  transferSize: number;
  decodedBodySize: number;
  startTime: number;
  responseEnd: number;
}

function getResourceTimings(): ResourceTiming[] {
  const resources = performance.getEntriesByType('resource');
  
  return resources.map((resource) => {
    const entry = resource as PerformanceResourceTiming;
    return {
      name: entry.name,
      type: entry.initiatorType,
      duration: entry.duration,
      transferSize: entry.transferSize,
      decodedBodySize: entry.decodedBodySize,
      startTime: entry.startTime,
      responseEnd: entry.responseEnd,
    };
  });
}

// Filter by resource type
function getImageResources(): ResourceTiming[] {
  return getResourceTimings().filter((r) => 
    r.type === 'img' || r.name.match(/\.(jpg|jpeg|png|gif|webp|avif)$/i)
  );
}

// Calculate total transfer size
function getTotalTransferSize(): number {
  return getResourceTimings().reduce((total, r) => total + r.transferSize, 0);
}
```

### 3. User Timing API

```typescript
// Custom performance marks
function markComponentRender(componentName: string): void {
  performance.mark(`${componentName}:render-start`);
}

function measureComponentRender(componentName: string): void {
  performance.mark(`${componentName}:render-end`);
  
  performance.measure(
    `${componentName}:render-duration`,
    `${componentName}:render-start`,
    `${componentName}:render-end`
  );
  
  // Get the measurement
  const entries = performance.getEntriesByName(`${componentName}:render-duration`);
  if (entries.length > 0) {
    console.log(`${componentName} render time: ${entries[0].duration}ms`);
  }
}

// Usage in React
function usePerformanceMark(componentName: string): void {
  markComponentRender(componentName);
  
  useEffect(() => {
    measureComponentRender(componentName);
  }, [componentName]);
}

// Custom metric for API calls
function measureAPICall<T>(
  endpoint: string,
  apiCall: () => Promise<T>
): Promise<T> {
  const markName = `api:${endpoint}`;
  performance.mark(`${markName}:start`);
  
  return apiCall().finally(() => {
    performance.mark(`${markName}:end`);
    performance.measure(markName, `${markName}:start`, `${markName}:end`);
    
    const entries = performance.getEntriesByName(markName);
    if (entries.length > 0) {
      console.log(`API ${endpoint} duration: ${entries[0].duration}ms`);
    }
  });
}
```

### 4. PerformanceObserver

```typescript
// Observe resource loading
function observeResourceLoading(): void {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log('Resource loaded:', {
        name: entry.name,
        type: entry.entryType,
        duration: entry.duration,
      });
    }
  });
  
  observer.observe({ type: 'resource', buffered: true });
}

// Observe Long Tasks (main thread blocking)
function observeLongTasks(): void {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.warn('Long task detected:', {
        duration: entry.duration,
        startTime: entry.startTime,
      });
    }
  });
  
  observer.observe({ type: 'longtask', buffered: true });
}

// Observe Largest Contentful Paint
function observeLCP(): void {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const lastEntry = entries[entries.length - 1];
    console.log('LCP:', lastEntry.startTime);
  });
  
  observer.observe({ type: 'largest-contentful-paint', buffered: true });
}

// Observe Layout Shifts
function observeCLS(): void {
  let clsValue = 0;
  
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (!(entry as any).hadRecentInput) {
        clsValue += (entry as any).value;
      }
    }
  });
  
  observer.observe({ type: 'layout-shift', buffered: true });
  
  // Report on page hide
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      console.log('CLS:', clsValue);
    }
  });
}
```

### 5. Paint Timing API

```typescript
// First Paint and First Contentful Paint
function observePaintTiming(): void {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.name === 'first-paint') {
        console.log('First Paint:', entry.startTime);
      } else if (entry.name === 'first-contentful-paint') {
        console.log('First Contentful Paint:', entry.startTime);
      }
    }
  });
  
  observer.observe({ type: 'paint', buffered: true });
}

// Get paint timing without observer
function getPaintTiming(): { firstPaint: number; fcp: number } | null {
  const entries = performance.getEntriesByType('paint');
  
  const firstPaint = entries.find((e) => e.name === 'first-paint');
  const fcp = entries.find((e) => e.name === 'first-contentful-paint');
  
  if (firstPaint && fcp) {
    return {
      firstPaint: firstPaint.startTime,
      fcp: fcp.startTime,
    };
  }
  
  return null;
}
```

### 6. Memory Usage (Chrome)

```typescript
interface MemoryInfo {
  usedJSHeapSize: number;
  totalJSHeapSize: number;
  jsHeapSizeLimit: number;
}

function getMemoryUsage(): MemoryInfo | null {
  const memory = (performance as any).memory;
  
  if (memory) {
    return {
      usedJSHeapSize: memory.usedJSHeapSize,
      totalJSHeapSize: memory.totalJSHeapSize,
      jsHeapSizeLimit: memory.jsHeapSizeLimit,
    };
  }
  
  return null;
}

// Monitor memory leaks
function monitorMemoryLeaks(): void {
  let lastMemory = getMemoryUsage();
  
  setInterval(() => {
    const currentMemory = getMemoryUsage();
    
    if (lastMemory && currentMemory) {
      const increase = currentMemory.usedJSHeapSize - lastMemory.usedJSHeapSize;
      
      if (increase > 10 * 1024 * 1024) { // 10MB increase
        console.warn('Potential memory leak detected:', {
          increase: `${(increase / 1024 / 1024).toFixed(2)}MB`,
          total: `${(currentMemory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB`,
        });
      }
    }
    
    lastMemory = currentMemory;
  }, 5000);
}
```

## Real-World Use Cases

### Performance Dashboard

```typescript
interface PerformanceMetrics {
  navigation: NavigationTiming;
  resources: ResourceTiming[];
  paint: { firstPaint: number; fcp: number };
  memory: MemoryInfo | null;
  timestamp: number;
}

function collectPerformanceMetrics(): PerformanceMetrics {
  return {
    navigation: getNavigationTiming(),
    resources: getResourceTimings(),
    paint: getPaintTiming() || { firstPaint: 0, fcp: 0 },
    memory: getMemoryUsage(),
    timestamp: Date.now(),
  };
}

// Send metrics periodically
function startPerformanceMonitoring(interval: number = 30000): void {
  setInterval(() => {
    const metrics = collectPerformanceMetrics();
    
    fetch('/api/performance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(metrics),
    });
  }, interval);
}
```

### A/B Test Performance Comparison

```typescript
function trackABTestPerformance(
  testId: string,
  variant: string
): void {
  const metrics = collectPerformanceMetrics();
  
  fetch('/api/ab-test-performance', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      testId,
      variant,
      metrics,
    }),
  });
}
```

## Common Mistakes

1. **Using deprecated APIs**: `performance.timing` is deprecated, use Navigation Timing Level 2
2. **Not buffering observers**: Miss entries that occurred before observer was created
3. **Ignoring buffered entries**: Some entry types have buffered entries
4. **Measuring too much**: Can impact performance itself
5. **Not cleaning up marks**: Old marks can cause memory issues

## Best Practices

1. **Use PerformanceObserver**: More efficient than polling `getEntries()`
2. **Buffer entries**: Set `buffered: true` to capture entries from page load
3. **Clean up marks**: Call `performance.clearMarks()` when done
4. **Sample metrics**: Don't measure every page load in production
5. **Use sendBeacon**: For non-blocking metric submission

## Performance Considerations

```
API Performance Impact:
┌─────────────────────────────────────────────────────────────┐
│  Low Impact:                                               │
│  • performance.now()                                       │
│  • performance.getEntriesByType()                          │
│  • performance.mark()                                      │
├─────────────────────────────────────────────────────────────┤
│  Medium Impact:                                            │
│  • PerformanceObserver (continuous)                         │
│  • performance.measure()                                   │
├─────────────────────────────────────────────────────────────┤
│  High Impact (use sparingly):                              │
│  • performance.getEntries() (large lists)                  │
│  • Memory monitoring (frequent)                            │
└─────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)
1. **What is the Performance API?**
   - Answer: A set of browser APIs for measuring timing and performance data of web pages and resources.

2. **What is `performance.now()`?**
   - Answer: Returns a high-resolution timestamp in milliseconds, more precise than `Date.now()`.

3. **What is Navigation Timing API?**
   - Answer: API that provides detailed timing information about page navigation and loading.

4. **What is Resource Timing API?**
   - Answer: API that measures timing and resource loading data for all page resources.

5. **What is User Timing API?**
   - Answer: API for creating custom performance marks and measures for application-specific metrics.

### Intermediate (5)
6. **How do you measure TTFB?**
   - Answer: `performance.timing.responseStart - performance.timing.navigationStart`

7. **What is PerformanceObserver?**
   - Answer: An API that asynchronously observes performance entries as they are added to the browser's performance timeline.

8. **What are the different entry types?**
   - Answer: navigation, resource, paint, mark, measure, longtask, largest-contentful-paint, layout-shift.

9. **How do you track custom metrics?**
   - Answer: Use `performance.mark()` and `performance.measure()` to create custom timing measurements.

10. **What is the difference between `getEntries()` and `PerformanceObserver`?**
    - Answer: `getEntries()` returns all entries at once; `PerformanceObserver` notifies you when new entries are added.

### Senior (10)
11. **Explain Navigation Timing Level 1 vs Level 2**
    - Answer: Level 1 uses `performance.timing` object; Level 2 uses `PerformanceNavigationTiming` entries with more accurate timestamps.

12. **How do you measure Long Tasks?**
    - Answer: Use `PerformanceObserver` with `type: 'longtask'` to detect tasks blocking the main thread for >50ms.

13. **What is the relationship between TTFB and FCP?**
    - Answer: TTFB must complete before FCP can occur; FCP = TTFB + server processing + resource loading.

14. **How do you handle cross-origin resource timing?**
    - Answer: Resources need `Timing-Allow-Origin` header; otherwise timing data is zeroed out.

15. **What metrics would you track for a SPA?**
    - Answer: TTFB, FCP, LCP, CLS, INP, custom metrics for route changes and component renders.

16. **How do you collect metrics without affecting performance?**
    - Answer: Use `requestIdleCallback`, `sendBeacon`, buffer metrics, sample data, use Web Workers.

17. **Explain the `buffered` option in PerformanceObserver**
    - Answer: When `true`, includes entries that occurred before the observer was created, useful for capturing page load metrics.

18. **How do you measure component render time in React?**
    - Answer: Use `performance.mark()` in render function and `performance.measure()` in useEffect.

19. **What is the difference between `entryType: 'resource'` and `entryType: 'navigation'`?**
    - Answer: Navigation entries track page navigation; resource entries track individual resource loads (images, scripts, etc.).

20. **How do you handle performance data from iframes?**
    - Answer: Use `postMessage` to communicate metrics; iframes have separate performance timelines.

### FAANG-style (5)
21. **Design a performance monitoring system**
    - Answer: Collect via PerformanceObserver → buffer in localStorage → send via sendBeacon → process in streaming pipeline → store in time-series DB → visualize with dashboards.

22. **How would you detect performance regressions in CI/CD?**
    - Answer: Run Lighthouse in CI, compare against baseline, fail build if thresholds exceeded, run in consistent environment.

23. **Explain how you'd measure perceived performance**
    - Answer: Use User Timing for custom milestones, combine with Core Web Vitals, track user-centric metrics like time-to-interactive.

24. **How do you optimize for the Navigation Timing waterfall?**
    - Answer: Minimize DNS lookups, use connection pooling, optimize server response, preload critical resources.

25. **Design a system to track performance across micro-frontends**
    - Answer: Each micro-frontend reports to parent via postMessage, aggregate metrics, attribute performance to specific micro-frontends.

### Follow-ups (5)
26. **How do you handle performance monitoring in Server-Side Rendering?**
    - Answer: Collect server-side timing data, combine with client-side metrics, use hydration timing.

27. **What is the impact of Service Workers on Performance APIs?**
    - Answer: Service workers can intercept resource requests, affecting resource timing; navigation timing still works.

28. **How do you measure performance of Web Workers?**
    - Answer: Use `performance.mark()` and `performance.measure()` within workers; communicate results via postMessage.

29. **Explain the relationship between Performance APIs and Real User Monitoring (RUM)**
    - Answer: Performance APIs provide the data collection mechanism; RUM is the practice of collecting and analyzing that data from real users.

30. **How do you handle performance measurement in SPAs with client-side routing?**
    - Answer: Measure route change duration, component render time, data loading time; track custom metrics per route.

## Summary

Performance APIs provide powerful tools for measuring and optimizing web application performance. Master Navigation Timing, Resource Timing, User Timing, and PerformanceObserver to build comprehensive monitoring solutions.

## References & Learn More

- [MDN - Performance API](https://developer.mozilla.org/en-US/docs/Web/API/Performance)
- [MDN - Navigation Timing API](https://developer.mozilla.org/en-US/docs/Web/API/Navigation_Timing_API)
- [MDN - Resource Timing API](https://developer.mozilla.org/en-US/docs/Web/API/Resource_Timing_API)
- [MDN - User Timing API](https://developer.mozilla.org/en-US/docs/Web/API/User_Timing_API)
- [MDN - PerformanceObserver](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver)
