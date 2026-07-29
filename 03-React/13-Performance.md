# React Performance Optimization

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

## Definition

React performance optimization is the practice of improving the speed, responsiveness, and efficiency of React applications. It involves reducing unnecessary re-renders, minimizing bundle size, optimizing rendering cycles, and improving user experience metrics like First Contentful Paint (FCP) and Time to Interactive (TTI).

## Why Do We Need It?

React applications can become slow due to unnecessary re-renders, large bundle sizes, expensive computations, poor state management, and missing memoization.

## How It Works

### Performance Optimization Hierarchy

```text
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

## Summary

React performance optimization involves memoization, virtualization, code splitting, and concurrent features. Profile before optimizing, focus on actual bottlenecks, and balance performance with code maintainability.

## Cheat Sheet
```text
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

---

## See Also
- [Animation](../30-Animation/)
- [Compound Components](18-Compound-Components.md)
- [Custom Hooks](16-Custom-Hooks.md)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Portals](17-Portals.md)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: Optimizing Performance](https://react.dev/learn/rendering-lists)
- [React Dev Tools Profiler](https://react.dev/learn/profiling-react-performance)
- [Optimizing React Performance](https://www.freecodecamp.org/news/optimize-react-app-performance/)
- [React Performance Optimization](https://www.joshwcomeau.com/react/performance/)
