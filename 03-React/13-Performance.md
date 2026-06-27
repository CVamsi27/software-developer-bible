# React Performance Optimization

## Definition

React performance optimization is the practice of improving the speed, responsiveness, and efficiency of React applications. It involves reducing unnecessary re-renders, minimizing bundle size, optimizing rendering cycles, and improving user experience metrics like First Contentful Paint (FCP) and Time to Interactive (TTI).

## Why Do We Need It?

React applications can become slow due to unnecessary re-renders, large bundle sizes, expensive computations, poor state management, and missing memoization.

## How It Works

### Performance Optimization Hierarchy

```
Level 1: Component Optimization
├── React.memo: Prevent unnecessary re-renders
├── useMemo: Memoize expensive computations
├── useCallback: Memoize function references
└── State colocation: Keep state close to usage

Level 2: Bundle Optimization
├── Code splitting: Lazy load components
├── Tree shaking: Remove unused code
├── Dynamic imports: Load on demand
└── Compression: gzip, brotli

Level 3: Rendering Optimization
├── Virtualization: Render only visible items
├── Concurrent features: Prioritize updates
├── useTransition: Defer non-urgent updates
└── useDeferredValue: Lag behind source value
```

## Code Examples

### React.memo

```typescript
import React, { memo, useState, useCallback } from 'react';

const MemoizedChild = memo(({ data, onClick }: { data: Data; onClick: () => void }) => {
  console.log('MemoizedChild rendered');
  return <div onClick={onClick}><p>{data.text}</p></div>;
});

const Parent = () => {
  const [count, setCount] = useState(0);
  const [data] = useState({ text: 'Hello' });
  const handleClick = useCallback(() => console.log('clicked'), []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <MemoizedChild data={data} onClick={handleClick} />
    </div>
  );
};
```

### useMemo for Expensive Computations

```typescript
const DataVisualization = ({ rawData }: { rawData: RawDataPoint[] }) => {
  const [timeRange, setTimeRange] = useState('all');

  const processedData = useMemo(() => {
    const filtered = rawData.filter(d =>
      timeRange === 'all' || d.timestamp >= Date.now() - timeRangeToMs(timeRange)
    );
    return filtered.sort((a, b) => a.value - b.value);
  }, [rawData, timeRange]);

  return (
    <div>
      <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
      <Chart data={processedData} />
    </div>
  );
};
```

### Virtualization

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

const VirtualList = ({ items }: { items: Item[] }) => {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 10,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div key={virtualRow.key} style={{
            position: 'absolute', top: 0, left: 0, width: '100%',
            height: virtualRow.size, transform: `translateY(${virtualRow.start}px)`,
          }}>
            <ListItem item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
};
```

### Code Splitting

```typescript
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

const App = () => {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'settings' && <Settings />}
      </Suspense>
    </div>
  );
};
```

### Concurrent Features

```typescript
const SearchApp = () => {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const deferredQuery = useDeferredValue(query);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    startTransition(() => setFilteredResults(filterData(value)));
  };

  return (
    <div>
      <input value={query} onChange={handleSearch} />
      {isPending && <Spinner />}
      <Results query={deferredQuery} />
    </div>
  );
};
```

## Common Mistakes

1. **Overusing React.memo**: Only memoize expensive components
2. **Not stabilizing references**: Use useCallback for functions passed as props
3. **Not virtualizing long lists**: Only render visible items
4. **Not code splitting**: Lazy load heavy components

## Best Practices

1. Profile before optimizing with React DevTools Profiler
2. Memoize expensive computations with useMemo
3. Stabilize references with useCallback
4. Virtualize long lists
5. Code split routes and heavy components
6. Use concurrent features for non-urgent updates
7. Colocate state near usage
8. Split contexts to reduce consumer re-renders

## Performance Metrics

| Metric | Target | Tool |
|--------|--------|------|
| First Contentful Paint | < 1.8s | Lighthouse |
| Largest Contentful Paint | < 2.5s | Lighthouse |
| Time to Interactive | < 3.8s | Lighthouse |
| Cumulative Layout Shift | < 0.1 | Lighthouse |

## Interview Questions

### Beginner (5-10)

**Q1: What is React.memo?**
A: `React.memo` is a higher-order component that prevents re-rendering when props haven't changed (shallow comparison).

**Q2: What is useMemo?**
A: `useMemo` memoizes a computed value, only re-computing when dependencies change.

**Q3: What is useCallback?**
A: `useCallback` memoizes a function reference, only re-creating when dependencies change.

**Q4: What is code splitting?**
A: Code splitting is splitting your bundle into smaller chunks loaded on demand.

**Q5: What is virtualization?**
A: Virtualization renders only visible items in a list, not all items.

**Q6: When should you use React.memo?**
A: When a component re-renders frequently with the same props.

**Q7: What is the difference between useMemo and useCallback?**
A: useMemo memoizes values; useCallback memoizes functions.

**Q8: How do you lazy load a component?**
A: `const Component = lazy(() => import('./Component'));`

**Q9: What are performance metrics?**
A: FCP, LCP, TTI, CLS, TBT measure loading and interactivity.

**Q10: How do you profile React performance?**
A: Use React DevTools Profiler to record and analyze renders.

### Intermediate (5-10)

**Q11: How does React.memo work internally?**
A: It wraps the component and compares props with Object.is before re-rendering.

**Q12: When should you NOT use useMemo?**
A: For cheap computations or values not passed to memoized children.

**Q13: What is the performance impact of inline objects?**
A: New references on every render cause memoized children to re-render.

**Q14: How do you optimize a large list?**
A: Use virtualization (react-window or react-virtual).

**Q15: What is the relationship between React.memo and useCallback?**
A: useCallback stabilizes function references so React.memo can prevent re-renders.

**Q16: How do you measure rendering performance?**
A: React DevTools Profiler, Chrome DevTools Performance, React.Profiler.

**Q17: What is state colocation?**
A: Keeping state as close as possible to where it's used.

**Q18: How do you optimize context performance?**
A: Memoize context value, split contexts by concern.

**Q19: What is the impact of deep component trees?**
A: More components = more re-renders when parent updates.

**Q20: How do you prevent unnecessary re-renders?**
A: React.memo, useMemo, useCallback, state colocation.

### Senior (10-15)

**Q21: Design a performance optimization strategy for a large app.**
A: Profile first, memoize expensive components, virtualize lists, code split routes, split contexts.

**Q22: How do you debug performance issues?**
A: React DevTools Profiler, Chrome DevTools Performance, custom logging.

**Q23: What is the relationship between performance and bundle size?**
A: Larger bundles = longer load times, slower Time to Interactive.

**Q24: How do you optimize for mobile?**
A: Reduce bundle size, virtualize lists, use concurrent features.

**Q25: What is the impact of React Compiler on performance?**
A: Automatic memoization reduces need for manual useMemo/useCallback.

**Q26: How do you handle performance in server components?**
A: Server Components don't contribute to client bundle size.

**Q27: What is the relationship between performance and testing?**
A: Performance tests ensure optimizations don't break functionality.

**Q28: How do you monitor performance in production?**
A: Real User Monitoring (RUM), Lighthouse CI, custom metrics.

**Q29: What is the impact of third-party libraries?**
A: Bundle size, re-renders, runtime overhead.

**Q30: How do you optimize React Native performance?**
A: FlatList, useCallback, useMemo, Hermes engine.

### FAANG-style (5-10)

**Q31: Design a performance monitoring system.**
A: Client-side metrics, server-side metrics, alerting, dashboards.

**Q32: How would you optimize a real-time dashboard?**
A: Virtualization, debouncing, web workers, concurrent features.

**Q33: Analyze the performance implications of React patterns.**
A: HOCs, render props, compound components, context.

**Q34: How would you implement performance budgets?**
A: Lighthouse CI, bundle size limits, performance tests.

**Q35: Design a performance testing strategy.**
A: Unit tests, integration tests, load tests, E2E tests.

**Q36: How do you handle performance regressions?**
A: CI/CD checks, monitoring, automated alerts.

**Q37: What is the relationship between performance and architecture?**
A: Component structure, state management, data fetching.

**Q38: How do you optimize for SEO?**
A: Server-side rendering, code splitting, performance metrics.

**Q39: What is the impact of TypeScript on performance?**
A: Build-time only, no runtime overhead.

**Q40: How do you handle performance in micro-frontends?**
A: Independent bundles, shared dependencies, lazy loading.

### Follow-ups (5-10)

**Q41: How would you explain performance optimization to a non-technical person?**
A: Making the app faster and more responsive by reducing unnecessary work.

**Q42: What are the edge cases in performance optimization?**
A: Over-optimization, trade-offs, memory vs CPU.

**Q43: How does performance interact with accessibility?**
A: Performance affects user experience, which affects accessibility.

**Q44: What is the relationship between performance and security?**
A: Some security measures (encryption) add performance overhead.

**Q45: How do you handle performance in legacy apps?**
A: Incremental optimization, profiling, gradual migration.

## Summary

React performance optimization involves memoization, virtualization, code splitting, and concurrent features. Profile before optimizing, focus on actual bottlenecks, and balance performance with code maintainability.

## Cheat Sheet

```
Performance Optimization:
├── React.memo: Prevent unnecessary re-renders
├── useMemo: Memoize expensive computations
├── useCallback: Memoize function references
├── Virtualization: Render only visible items
├── Code splitting: Lazy load components
├── Concurrent features: useTransition, useDeferredValue
├── State colocation: Keep state near usage
├── Context splitting: Reduce consumer re-renders
└── Profiling: React DevTools Profiler
```

## References & Learn More

- [React Docs: Optimizing Performance](https://react.dev/learn/rendering-lists)
- [React Dev Tools Profiler](https://react.dev/learn/reference-devtools-profiler)
- [Optimizing React Performance](https://www.freecodecamp.org/news/optimize-react-performance/)
- [React Performance Optimization](https://www.joshwcomeau.com/react/performance/)
