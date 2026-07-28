---
section: JavaScript
category: Core
tags: [concept]
---

# Memoization

## Definition

**Memoization** is an optimization technique that caches the results of expensive function calls and returns the cached result when the same inputs occur again. It trades memory for computation time.

## Why Do We Need It?

- **Performance**: Speed up expensive calculations
- **Caching**: Avoid redundant computations
- **React Optimization**: Prevent unnecessary re-renders
- **Algorithm Optimization**: Reduce time complexity

## How It Works

### Memoization Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    MEMOIZATION FLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WITHOUT MEMOIZATION:                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  fibonacci(5) → calculates                         │    │
│  │  fibonacci(5) → calculates again!                  │    │
│  │  fibonacci(5) → calculates again!                  │    │
│  │                                                      │    │
│  │  Same calculation repeated multiple times         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  WITH MEMOIZATION:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  fibonacci(5) → calculates, stores in cache       │    │
│  │  fibonacci(5) → returns cached result              │    │
│  │  fibonacci(5) → returns cached result              │    │
│  │                                                      │    │
│  │  First call: O(n)                                  │    │
│  │  Subsequent: O(1)                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  CACHE STRUCTURE:                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Map or Object:                                    │    │
│  │  {                                                  │    │
│  │    "5": 5,                                          │    │
│  │    "6": 8,                                          │    │
│  │    "7": 13                                          │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Memoization

```typescript
function memoize<T extends (...args: any[]) => any>(
  fn: T
): (...args: Parameters<T>) => ReturnType<T> {
  const cache = new Map<string, ReturnType<T>>();

  return function(...args: Parameters<T>): ReturnType<T> {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// Usage
const expensiveCalculation = memoize((n: number): number => {
  console.log('Computing...');
  return n * n;
});

console.log(expensiveCalculation(4));  // Computing... 16
console.log(expensiveCalculation(4));  // 16 (cached)

```

### Fibonacci with Memoization

```typescript
// Without memoization: O(2^n)
function fibonacci(n: number): number {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// With memoization: O(n)
function fibonacciMemo(n: number, memo: Map<number, number> = new Map()): number {
  if (n <= 1) return n;

  if (memo.has(n)) {
    return memo.get(n)!;
  }

  const result = fibonacciMemo(n - 1, memo) + fibonacciMemo(n - 2, memo);
  memo.set(n, result);
  return result;
}

// Using memoize utility
const fib = memoize((n: number): number => {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
});

```

### Advanced Memoization with LRU Cache

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();
  private maxSize: number;

  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    const value = this.cache.get(key);
    if (value !== undefined) {
      // Move to end (most recently used)
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      // Delete oldest (first) entry
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}

function memoizeWithLRU<T extends (...args: any[]) => any>(
  fn: T,
  maxSize: number = 100
): (...args: Parameters<T>) => ReturnType<T> {
  const cache = new LRUCache<string, ReturnType<T>>(maxSize);

  return function(...args: Parameters<T>): ReturnType<T> {
    const key = JSON.stringify(args);

    const cached = cache.get(key);
    if (cached !== undefined) {
      return cached;
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

```

### React useMemo/useCallback

```typescript
import { useMemo, useCallback } from 'react';

function ExpensiveComponent({ items, filter }: Props) {
  // Memoize expensive computation
  const filteredItems = useMemo(() => {
    return items.filter(item => item.category === filter);
  }, [items, filter]);

  // Memoize callback
  const handleClick = useCallback((id: string) => {
    console.log(`Clicked ${id}`);
  }, []);

  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}

```

### Memoization with TTL

```typescript
function memoizeWithTTL<T extends (...args: any[]) => any>(
  fn: T,
  ttl: number = 60000
): (...args: Parameters<T>) => ReturnType<T> {
  const cache = new Map<string, { value: ReturnType<T>; timestamp: number }>();

  return function(...args: Parameters<T>): ReturnType<T> {
    const key = JSON.stringify(args);
    const now = Date.now();

    const cached = cache.get(key);
    if (cached && now - cached.timestamp < ttl) {
      return cached.value;
    }

    const result = fn(...args);
    cache.set(key, { value: result, timestamp: now });
    return result;
  };
}

// Usage
const apiCall = memoizeWithTTL(fetchData, 30000);  // Cache for 30 seconds

```

## Real-World Use Cases

### 1. Data Processing

```typescript
const expensiveTransform = memoize((data: any[]) => {
  return data
    .filter(item => item.active)
    .map(item => ({
      ...item,
      score: calculateScore(item)
    }))
    .sort((a, b) => b.score - a.score);
});

```

### 2. API Response Caching

```typescript
const apiCache = memoizeWithTTL(async (url: string) => {
  const response = await fetch(url);
  return response.json();
}, 60000);

// Usage
const users = await apiCache('/api/users');

```

### 3. React Component Optimization

```typescript
function ProductList({ products, category }: Props) {
  const filtered = useMemo(
    () => products.filter(p => p.category === category),
    [products, category]
  );

  const total = useMemo(
    () => filtered.reduce((sum, p) => sum + p.price, 0),
    [filtered]
  );

  return (
    <div>
      <p>Total: ${total}</p>
      <ul>
        {filtered.map(p => <li key={p.id}>{p.name}</li>)}
      </ul>
    </div>
  );
}

```

### 4. Recursive Functions

```typescript
function memoize<T extends (...args: any[]) => any>(fn: T) {
  const cache = new Map();

  const memoized = function(...args: Parameters<T>) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };

  return memoized;
}

// Recursive factorial
const factorial = memoize((n: number): number => {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
});

```

## Common Mistakes

### 1. Memoizing Everything

```typescript
// Bad: Memoizing simple functions
const add = memoize((a: number, b: number) => a + b);

// Good: Only memoize expensive operations
const complexCalculation = memoize((data: LargeDataset) => {
  // Expensive computation
});

```

### 2. Ignoring Cache Size

```typescript
// Bad: Unbounded cache
const cache = new Map();
function getData(key: string) {
  if (!cache.has(key)) {
    cache.set(key, fetchData(key));
  }
  return cache.get(key);
}

// Good: Bounded cache
const cache = new LRUCache(1000);

```

### 3. Wrong Cache Key

```typescript
// Bad: Using object reference as key
const cache = new Map();
function process(obj: object) {
  if (cache.has(obj)) return cache.get(obj);
  // ...
}

// Good: Use stringified key
function process(obj: object) {
  const key = JSON.stringify(obj);
  if (cache.has(key)) return cache.get(key);
  // ...
}

```

### 4. Not Handling Cache Invalidation

```typescript
// Bad: Cache never invalidated
const data = memoize(fetchData);

// Good: Implement TTL or manual invalidation
const data = memoizeWithTTL(fetchData, 60000);

```

## Best Practices

### 1. Choose What to Memoize

```typescript
// Memoize:
// - Expensive computations
// - API calls with same parameters
// - Complex filtering/sorting
// - Recursive functions

// Don't memoize:
// - Simple operations
// - Frequently changing data
// - Functions with side effects

```

### 2. Set Cache Limits

```typescript
// Use LRU cache with reasonable size
const cache = new LRUCache(1000);

// Or use TTL
const cache = memoizeWithTTL(fn, 60000);

```

### 3. Use Proper Cache Keys

```typescript
// For objects, use stable stringification
function createKey(args: any[]): string {
  return JSON.stringify(args, Object.keys(args[0] || {}).sort());
}

```

### 4. Profile Before Memoizing

```typescript
// Measure performance impact
console.time('memoized');
memoizedFn(args);
console.timeEnd('memoized');

console.time('original');
originalFn(args);
console.timeEnd('original');

```

## Performance Considerations

### Memory vs Time Trade-off

```typescript
// Each memoized function uses memory for cache
// Only worth it if computation is expensive

// Bad: Memoizing O(1) operation
const add = memoize((a: number, b: number) => a + b);

// Good: Memoizing O(n) or worse operation
const fibonacci = memoize((n: number) => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

```

### Cache Hit Rate

```typescript
// Monitor cache effectiveness
function memoizeWithStats<T extends (...args: any[]) => any>(fn: T) {
  const cache = new Map();
  let hits = 0;
  let misses = 0;

  const memoized = function(...args: Parameters<T>) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      hits++;
      return cache.get(key);
    }
    misses++;
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };

  memoized.getStats = () => ({ hits, misses, ratio: hits / (hits + misses) });

  return memoized;
}

```

## Summary

Memoization is a powerful optimization:

1. **Definition**: Cache results of expensive function calls

2. **Implementation**: Map/object with stringified keys

3. **React**: useMemo, useCallback, React.memo

4. **Cache strategies**: LRU, TTL, bounded size

5. **Performance**: Trade memory for computation time

6. **Best practices**: Profile, set limits, handle invalidation

7. **Common issues**: Unbounded caches, stale data

## Cheat Sheet
```text
MEMOIZATION CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHAT IS MEMOIZATION?
• Cache function results
• Return cached for repeated inputs
• Trade memory for time

IMPLEMENTATION:
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

REACT:
• useMemo: Cache expensive computations
• useCallback: Cache function references
• React.memo: Prevent re-renders

CACHE STRATEGIES:
• LRU: Least Recently Used
• TTL: Time To Live
• Bounded: Limit cache size

WHEN TO USE:
• Expensive computations
• API calls with same params
• Recursive functions
• Complex filtering/sorting

WHEN NOT TO USE:
• Simple operations
• Frequently changing data
• Functions with side effects

PERFORMANCE:
• First call: O(n) same as original
• Subsequent: O(1) cache lookup
• Monitor hit rate
• Set cache limits

COMMON ISSUES:
• Unbounded caches
• Stale data
• Wrong cache keys
• Memory leaks

BEST PRACTICES:
• Profile before memoizing
• Set cache limits (LRU)
• Handle invalidation (TTL)
• Monitor effectiveness

```

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Node.js](../05-NodeJS/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [Wikipedia: Memoization](https://en.wikipedia.org/wiki/Memoization)
- [JavaScript.info: Memoize](https://javascript.info/function-basics)
- [FreeCodeCamp: Memoize Function](https://www.freecodecamp.org/news/memoize-function-javascript/)
- [Lodash: memoize()](https://lodash.com/docs/4.17.15#memoize)
