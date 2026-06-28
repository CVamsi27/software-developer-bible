# Memory Leaks

## Definition

A **Memory Leak** occurs when a program allocates memory but fails to release it when no longer needed. In JavaScript, this happens when objects are no longer used but still have references, preventing garbage collection.

## Why Do We Need It?

- **Performance**: Leaks cause slowdowns over time
- **Stability**: Can crash applications
- **User Experience**: Memory usage grows indefinitely
- **Resource Management**: Servers run out of memory

## How It Works

### Common Causes

```text
┌─────────────────────────────────────────────────────────────┐
│                 COMMON MEMORY LEAK CAUSES                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DETACHED DOM ELEMENTS                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  const element = document.getElementById('app');    │    │
│  │  document.body.removeChild(element);                │    │
│  │  // element still has references!                   │    │
│  │  // If event listeners not removed, memory leaks   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  2. UNATTACHED EVENT LISTENERS                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function setup() {                                │    │
│  │    const button = document.getElementById('btn');  │    │
│  │    button.addEventListener('click', handler);     │    │
│  │    // If button removed, listener still attached  │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  3. CLOSURES                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function createHandler() {                        │    │
│  │    const hugeData = new Array(1000000);            │    │
│  │    return function handler() {                     │    │
│  │      // hugeData kept alive by closure            │    │
│  │      console.log('clicked');                       │    │
│  │    };                                               │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  4. TIMERS AND INTERVALS                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function start() {                                │    │
│  │    setInterval(() => {                             │    │
│  │      // Keeps running, references kept            │    │
│  │      updateUI();                                   │    │
│  │    }, 1000);                                       │    │
│  │    // If not cleared, leaks                       │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  5. GLOBAL VARIABLES                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function leak() {                                │    │
│  │    leakedVar = new Array(1000000);  // Global!    │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Detection Methods

```text
┌─────────────────────────────────────────────────────────────┐
│                  DETECTION METHODS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. CHROME DEVTOOLS                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Memory tab → Heap snapshots                     │    │
│  │  • Take snapshot before/after action               │    │
│  │  • Compare snapshots to find growing objects       │    │
│  │  • Allocation timeline for real-time monitoring    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  2. performance.memory                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  console.log(performance.memory);                  │    │
│  │  // {                                              │    │
│  │  //   usedJSHeapSize: 1000000,                     │    │
│  │  //   jsHeapSizeLimit: 2000000                     │    │
│  │  // }                                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  3. MANUAL MONITORING                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  setInterval(() => {                               │    │
│  │    console.log(performance.memory.usedJSHeapSize); │    │
│  │  }, 5000);                                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Global Variable Leak

```typescript
// Bad: Global variable
function leak() {
  leakedArray = [];  // Implicit global!
  for (let i = 0; i < 1000000; i++) {
    leakedArray.push(i);
  }
}

// Good: Use const/let
function noLeak() {
  const localArray = [];
  for (let i = 0; i < 1000000; i++) {
    localArray.push(i);
  }
}

```

### Forgotten Timer

```typescript
// Bad: Timer not cleared
function startTimer() {
  const data = new Array(1000000).fill(0);

  setInterval(() => {
    console.log(data.length);  // data kept alive
  }, 1000);
}

// Good: Clear timer
function startTimerFixed() {
  const data = new Array(1000000).fill(0);

  const intervalId = setInterval(() => {
    console.log(data.length);
  }, 1000);

  // Clear when done
  clearInterval(intervalId);
}

```

### Detached DOM

```typescript
// Bad: Detached element with listener
function createAndRemove() {
  const button = document.createElement('button');
  button.addEventListener('click', () => {
    console.log('clicked');
  });
  document.body.appendChild(button);

  // Later remove
  document.body.removeChild(button);
  // button and listener still in memory!
}

// Good: Remove listener before removing element
function createAndRemoveFixed() {
  const button = document.createElement('button');
  const handler = () => console.log('clicked');

  button.addEventListener('click', handler);
  document.body.appendChild(button);

  // Remove listener first
  button.removeEventListener('click', handler);
  document.body.removeChild(button);
}

```

### Closure Memory Leak

```typescript
// Bad: Closure captures large object
function createHandler() {
  const hugeData = new Array(1000000).fill(0);

  return function handler() {
    console.log('clicked');  // hugeData kept alive
  };
}

// Good: Only capture what's needed
function createHandlerFixed() {
  const hugeData = new Array(1000000).fill(0);
  const length = hugeData.length;  // Capture only needed value

  return function handler() {
    console.log(length);  // Only number kept alive
  };
}

```

### Event Listener Leak

```typescript
// Bad: Not removing listener
class Component {
  componentDidMount() {
    window.addEventListener('resize', this.handleResize);
  }

  // componentWillUnmount() missing!
}

// Good: Proper cleanup
class Component {
  componentDidMount() {
    window.addEventListener('resize', this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize);
  }
}

```

### React useEffect Leak

```typescript
// Bad: Missing cleanup
useEffect(() => {
  const subscription = api.subscribe(data => {
    setData(data);
  });
  // Missing cleanup!
}, []);

// Good: Proper cleanup
useEffect(() => {
  const subscription = api.subscribe(data => {
    setData(data);
  });

  return () => {
    subscription.unsubscribe();
  };
}, []);

```

### Array Growth

```typescript
// Bad: Array keeps growing
const cache: any[] = [];

function addToCache(item: any) {
  cache.push(item);  // Never cleaned!
}

// Good: Limit cache size
const cache: any[] = [];
const MAX_CACHE_SIZE = 1000;

function addToCacheFixed(item: any) {
  cache.push(item);
  if (cache.length > MAX_CACHE_SIZE) {
    cache.shift();  // Remove oldest
  }
}

```

### WeakMap/WeakRef

```typescript
// Good: Use WeakMap for object references
const cache = new WeakMap();

function processObject(obj: object) {
  if (cache.has(obj)) {
    return cache.get(obj);
  }

  const result = expensiveComputation(obj);
  cache.set(obj, result);
  return result;
  // When obj is garbage collected, cache entry is removed
}

```

## Real-World Use Cases

### 1. Component Cleanup (React)

```typescript
function DataComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchData() {
      try {
        const response = await fetch('/api/data', {
          signal: controller.signal
        });
        const result = await response.json();
        setData(result);
      } catch (error) {
        if (error.name !== 'AbortError') {
          throw error;
        }
      }
    }

    fetchData();

    return () => {
      controller.abort();
    };
  }, []);

  return <div>{JSON.stringify(data)}</div>;
}

```

### 2. Event Delegation

```typescript
// Bad: Individual listeners
function setupItems(items: HTMLElement[]) {
  items.forEach(item => {
    item.addEventListener('click', handleClick);
  });
}

// Good: Event delegation
function setupItemsFixed(container: HTMLElement) {
  container.addEventListener('click', (e) => {
    const target = e.target as HTMLElement;
    if (target.matches('.item')) {
      handleClick(e);
    }
  });
}

```

### 3. Object Pooling

```typescript
class ObjectPool<T> {
  private pool: T[] = [];
  private factory: () => T;

  constructor(factory: () => T) {
    this.factory = factory;
  }

  acquire(): T {
    if (this.pool.length > 0) {
      return this.pool.pop()!;
    }
    return this.factory();
  }

  release(obj: T) {
    this.pool.push(obj);
  }
}

```

### 4. Cache with Expiration

```typescript
class Cache<K, V> {
  private cache = new Map<K, { value: V; timestamp: number }>();
  private ttl: number;

  constructor(ttl: number = 60000) {
    this.ttl = ttl;
  }

  set(key: K, value: V) {
    this.cache.set(key, { value, timestamp: Date.now() });
  }

  get(key: K): V | undefined {
    const entry = this.cache.get(key);
    if (!entry) return undefined;

    if (Date.now() - entry.timestamp > this.ttl) {
      this.cache.delete(key);
      return undefined;
    }

    return entry.value;
  }

  cleanup() {
    const now = Date.now();
    for (const [key, entry] of this.cache) {
      if (now - entry.timestamp > this.ttl) {
        this.cache.delete(key);
      }
    }
  }
}

```

## Common Mistakes

### 1. Not Cleaning Up useEffect

```typescript
// Bad
useEffect(() => {
  const handler = () => console.log('resize');
  window.addEventListener('resize', handler);
}, []);

// Good
useEffect(() => {
  const handler = () => console.log('resize');
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, []);

```

### 2. Storing Large Objects in State

```typescript
// Bad: Large object in state
const [data, setData] = useState(largeObject);

// Good: Store only needed data
const [summary, setSummary] = useState(extractSummary(largeObject));

```

### 3. Not Using WeakMap/WeakRef

```typescript
// Bad: Strong references prevent GC
const cache = new Map();
cache.set(obj, result);

// Good: WeakMap allows GC
const cache = new WeakMap();
cache.set(obj, result);

```

### 4. Global State Growth

```typescript
// Bad: Global state keeps growing
const globalState = {
  items: []  // Never cleaned!
};

// Good: Implement cleanup
const globalState = {
  items: [],
  cleanup() {
    this.items = [];
  }
};

```

## Best Practices

### 1. Always Clean Up

```typescript
// React
useEffect(() => {
  const subscription = subscribe();
  return () => subscription.unsubscribe();
}, []);

// Vanilla JS
const handler = () => {};
element.addEventListener('click', handler);
// Later
element.removeEventListener('click', handler);

```

### 2. Use WeakMap/WeakRef

```typescript
// For object caches
const cache = new WeakMap();

// For event listeners on objects
const listeners = new WeakMap<object, Function>();

```

### 3. Limit Cache Size

```typescript
class LimitedCache<T> {
  private cache = new Map<string, T>();
  private maxSize: number;

  constructor(maxSize: number = 1000) {
    this.maxSize = maxSize;
  }

  set(key: string, value: T) {
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}

```

### 4. Use Object Pooling

```typescript
// For frequently created/destroyed objects
const pool = new ObjectPool(() => ({
  x: 0, y: 0, width: 0, height: 0
}));

const obj = pool.acquire();
// Use object
pool.release(obj);

```

## Performance Considerations

### Memory Monitoring

```typescript
function monitorMemory() {
  if (performance.memory) {
    const used = performance.memory.usedJSHeapSize / 1024 / 1024;
    const total = performance.memory.jsHeapSizeLimit / 1024 / 1024;
    console.log(`Memory: ${used.toFixed(2)}MB / ${total.toFixed(2)}MB`);
  }
}

setInterval(monitorMemory, 5000);

```

### Garbage Collection Impact

```typescript
// Frequent GC causes jank
// Reduce allocations in hot paths

// Bad: Creates new objects
function processItems(items: any[]) {
  return items.map(item => ({ ...item, processed: true }));
}

// Good: Reuse objects
function processItems(items: any[]) {
  return items.map(item => {
    item.processed = true;
    return item;
  });
}

```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is a memory leak in JavaScript?**

A: A memory leak occurs when allocated memory is not released after it's no longer needed, causing memory usage to grow over time.

**Q2: What are common causes of memory leaks?**

A: Detached DOM elements, forgotten timers, unclosed event listeners, global variables, and closures capturing large objects.

**Q3: How do you detect memory leaks?**

A: Use Chrome DevTools Memory tab, performance.memory API, or monitor memory usage over time.

**Q4: How do you prevent memory leaks in React?**

A: Clean up useEffect, remove event listeners, cancel async operations, and avoid storing large objects in state.

**Q5: What is a detached DOM element?**

A: A DOM element that has been removed from the document but still has JavaScript references, preventing garbage collection.

### Intermediate (5-10 questions)

**Q6: How do closures cause memory leaks?**

A: Closures capture their lexical environment. If a closure captures a large object and the closure is kept alive, the large object cannot be garbage collected.

**Q7: How do you use WeakMap to prevent memory leaks?**

A: WeakMap allows garbage collection of keys. If a key object has no other references, it and its value can be collected.

**Q8: How do you properly clean up event listeners?**

A: Store handler reference, remove it in cleanup function (useEffect return, beforeunload, etc.).

**Q9: What is the difference between memory leak and memory growth?**

A: Memory leak is unbounded growth due to unreleased references. Memory growth can be normal (caching) but should be bounded.

**Q10: How do you test for memory leaks?**

A: Run repeated operations, monitor memory usage, take heap snapshots, compare before/after.

### Senior (10-15 questions)

**Q11: How do you implement a memory-efficient cache?**

A: Use WeakMap for object keys, implement LRU eviction, set TTL, limit cache size.

**Q12: How do you handle memory leaks in a long-running application?**

A: Regular cleanup intervals, memory monitoring, object pooling, bounded caches.

**Q13: How do you prevent memory leaks in Node.js?**

A: Stream large data, close database connections, clear intervals/timeouts, handle errors.

**Q14: How do you use heap snapshots effectively?**

A: Take baseline snapshot, perform action, take second snapshot, compare to find growth.

**Q15: How do you optimize garbage collection?**

A: Reduce allocations, reuse objects, use typed arrays, minimize closure captures.

### FAANG-style (5-10 questions)

**Q16: Design a memory monitoring system.**

A: Track allocations, detect growth patterns, alert on thresholds, provide diagnostics.

**Q17: How would you implement automatic memory cleanup?**

A: Reference counting, weak references, periodic cleanup, automatic disposal.

**Q18: Analyze memory implications of different data structures.**

A: Arrays vs Maps vs WeakMaps, object pooling, structural sharing.

**Q19: How do you debug memory leaks in production?**

A: Memory profiling, heap dumps, growth detection, error tracking.

**Q20: What are security implications of memory leaks?**

A: Denial of service, information leakage through memory dumps, resource exhaustion.

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a memory leak bug in production?**

A: React component not cleaning up setInterval, causing memory to grow indefinitely.

**Q22: How do you handle memory leaks in a micro-frontend architecture?**

A: Each micro-frontend manages its own memory, shared cleanup protocols.

**Q23: What is the relationship between memory leaks and garbage collection?**

A: Leaks prevent GC from collecting unreachable objects, causing memory growth.

**Q24: How do different frameworks handle memory management?**

A: React: useEffect cleanup. Vue: onUnmounted. Angular: ngOnDestroy.

**Q25: What are best practices for memory management?**

A: Clean up resources, use weak references, limit caches, monitor usage, test for leaks.

## Summary

Memory leaks are critical to prevent:

1. **Causes**: Detached DOM, forgotten timers, closures, global variables

2. **Detection**: Chrome DevTools, performance.memory, heap snapshots

3. **Prevention**: Clean up, use WeakMap, limit caches, object pooling

4. **React**: Always clean up useEffect

5. **Performance**: Monitor memory, reduce allocations

6. **Best practices**: Document cleanup, test for leaks

7. **Tools**: Chrome DevTools, memory profilers

## Cheat Sheet

```text
MEMORY LEAKS CHEAT SHEET
═══════════════════════════════════════════════════════════════

COMMON CAUSES:
• Detached DOM elements
• Forgotten timers/intervals
• Uncleared event listeners
• Global variables
• Closures capturing large objects
• Growing caches without limits

DETECTION:
• Chrome DevTools Memory tab
• performance.memory API
• Heap snapshots comparison
• Memory monitoring

PREVENTION:
• Clean up useEffect
• Remove event listeners
• Clear timers
• Use WeakMap/WeakRef
• Limit cache sizes
• Object pooling

REACT:
useEffect(() => {
  const sub = subscribe();
  return () => sub.unsubscribe();
}, []);

VANILLA JS:
const handler = () => {};
el.addEventListener('click', handler);
el.removeEventListener('click', handler);

WEAKMAP:
const cache = new WeakMap();
// Allows GC of keys

CACHE WITH LIMIT:
class Cache {
  set(key, value) {
    if (this.size >= MAX) this.deleteOldest();
    this.map.set(key, value);
  }
}

DEBUGGING:
• Take heap snapshots
• Compare before/after
• Monitor memory usage
• Check for growing objects

BEST PRACTICES:
• Always clean up
• Use weak references
• Limit caches
• Monitor memory
• Test for leaks

```

## References & Learn More

- [MDN: Memory Management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Memory_Management)
- [Chrome DevTools: Memory Profiling](https://developer.chrome.com/docs/devtools/memory-problems/)
- [Auth0: Understanding and Fixing Memory Leaks](https://auth0.com/blog/four-types-of-leaks-in-web-applications-and-how-to-get-rid-of-them/)
- [V8 Blog: Trash Talk - The Orinoco Garbage Collector](https://v8.dev/blog/trash-talk)
