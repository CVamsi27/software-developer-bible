# Garbage Collection

## Definition

**Garbage Collection (GC)** is the automatic memory management process that reclaims memory occupied by objects that are no longer in use. JavaScript engines use various algorithms to identify and free unused memory, eliminating the need for manual memory management.

## Why Do We Need It?

- **Memory Management**: Automatic cleanup of unused objects
- **Developer Productivity**: No manual memory allocation/deallocation
- **Safety**: Prevents memory leaks and dangling pointers
- **Performance**: Optimizes memory usage dynamically

## How It Works

### Mark-and-Sweep Algorithm

```
┌─────────────────────────────────────────────────────────────┐
│                  MARK-AND-SWEEP ALGORITHM                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STEP 1: MARK PHASE                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Start from root objects (global, stack)         │    │
│  │  • Mark all reachable objects                      │    │
│  │  • Traverse references recursively                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  STEP 2: SWEEP PHASE                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Scan through all objects                        │    │
│  │  • Collect unmarked objects                        │    │
│  │  • Free memory                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  VISUALIZATION:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Root Objects:                                      │    │
│  │  ┌──────────┐                                      │    │
│  │  │  Global  │                                      │    │
│  │  └────┬─────┘                                      │    │
│  │       │                                              │    │
│  │       ▼                                              │    │
│  │  ┌──────────┐    ┌──────────┐                      │    │
│  │  │ Object A │───→│ Object B │  (Marked)            │    │
│  │  └──────────┘    └──────────┘                      │    │
│  │                                                      │    │
│  │  Unreachable:                                      │    │
│  │  ┌──────────┐    ┌──────────┐                      │    │
│  │  │ Object C │───→│ Object D │  (Swept)            │    │
│  │  └──────────┘    └──────────┘                      │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Reference Counting

```
┌─────────────────────────────────────────────────────────────┐
│                    REFERENCE COUNTING                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CONCEPT:                                                    │
│  • Each object has a reference count                        │
│  • Increment when new reference is created                  │
│  • Decrement when reference is removed                      │
│  • Collect when count reaches zero                          │
│                                                              │
│  EXAMPLE:                                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let obj = { data: 'hello' };  // count = 1        │    │
│  │  let ref = obj;              // count = 2          │    │
│  │                                                      │    │
│  │  obj = null;                 // count = 1          │    │
│  │  ref = null;                 // count = 0 → GC!    │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  LIMITATION: Circular References                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  let a = {};                                       │    │
│  │  let b = {};                                       │    │
│  │  a.ref = b;  // b count = 2                       │    │
│  │  b.ref = a;  // a count = 2                       │    │
│  │                                                      │    │
│  │  a = null;  // a count = 1                         │    │
│  │  b = null;  // b count = 1                         │    │
│  │                                                      │    │
│  │  // Count never reaches zero!                      │    │
│  │  // Mark-and-sweep handles this                    │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Generational GC

```
┌─────────────────────────────────────────────────────────────┐
│                    GENERATIONAL GC                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GENERATIONS:                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Young Generation (Nursery)                        │    │
│  │  • Newly created objects                           │    │
│  │  • Small size                                      │    │
│  │  • Collected frequently                           │    │
│  │                                                      │    │
│  │  Old Generation (Tenured)                          │    │
│  │  • Objects surviving multiple collections          │    │
│  │  • Larger size                                     │    │
│  │  • Collected less frequently                      │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  PROMOTION:                                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  New Object → Young Gen                           │    │
│  │       │                                              │    │
│  │       ▼ (survives collection)                      │    │
│  │  Young Gen → Old Gen                              │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  V8 OPTIMIZATIONS:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  • Scavenge: Young gen collection (fast)           │    │
│  │  • Mark-Sweep-Compact: Old gen collection         │    │
│  │  • Incremental marking: Breaks work into chunks   │    │
│  │  • Concurrent marking: Marks while JS runs        │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Garbage Collection

```typescript
// Objects are created and garbage collected
function example() {
  let obj = { data: 'hello' };  // Created
  console.log(obj.data);
  obj = null;  // Eligible for GC
}

example();
// obj is now garbage collected

// Circular references are handled
function createCircular() {
  let a: any = { name: 'a' };
  let b: any = { name: 'b' };
  a.ref = b;
  b.ref = a;
  
  a = null;
  b = null;
  // Both objects are eligible for GC
}
```

### Closures and GC

```typescript
// Closure prevents GC of captured variables
function createClosure() {
  const largeData = new Array(1000000).fill(0);
  
  return function() {
    // largeData kept alive by closure
    return largeData.length;
  };
}

const closure = createClosure();
// largeData cannot be garbage collected

// To allow GC, release reference
function createClosureFixed() {
  let largeData: number[] | null = new Array(1000000).fill(0);
  
  return function() {
    const length = largeData?.length ?? 0;
    largeData = null;  // Allow GC
    return length;
  };
}
```

### WeakMap and GC

```typescript
// WeakMap allows GC of keys
const cache = new WeakMap<object, any>();

function processObject(obj: object) {
  if (cache.has(obj)) {
    return cache.get(obj);
  }
  
  const result = expensiveComputation(obj);
  cache.set(obj, result);
  return result;
}

let obj = { data: 'test' };
processObject(obj);

// When obj is garbage collected, cache entry is also removed
obj = null;
```

### Object Pooling

```typescript
// Reuse objects to reduce GC pressure
class ObjectPool<T> {
  private pool: T[] = [];
  private factory: () => T;
  
  constructor(factory: () => T) {
    this.factory = factory;
  }
  
  acquire(): T {
    return this.pool.length > 0 
      ? this.pool.pop()! 
      : this.factory();
  }
  
  release(obj: T) {
    this.pool.push(obj);
  }
}

// Usage
const pool = new ObjectPool(() => ({ x: 0, y: 0 }));
const obj = pool.acquire();
// Use obj
pool.release(obj);  // Return to pool instead of GC
```

### Typed Arrays

```typescript
// Typed arrays have predictable memory layout
const buffer = new ArrayBuffer(1024);
const view = new Uint8Array(buffer);

// More efficient than regular arrays
// Memory is allocated in contiguous blocks
// GC can handle them more efficiently
```

## Real-World Use Cases

### 1. React Component Optimization

```typescript
// Bad: Creating new objects on each render
function Component({ items }: { items: Item[] }) {
  const processed = items.map(item => ({
    ...item,
    processed: true
  }));
  
  return <List items={processed} />;
}

// Good: Memoize expensive computations
function Component({ items }: { items: Item[] }) {
  const processed = useMemo(
    () => items.map(item => ({ ...item, processed: true })),
    [items]
  );
  
  return <List items={processed} />;
}
```

### 2. Event Listener Management

```typescript
class EventEmitter {
  private listeners = new WeakMap<object, Function[]>();
  
  on(target: object, event: string, callback: Function) {
    if (!this.listeners.has(target)) {
      this.listeners.set(target, []);
    }
    this.listeners.get(target)!.push(callback);
  }
  
  // When target is GC'd, listeners are also GC'd
}
```

### 3. Cache Implementation

```typescript
class GC-friendlyCache<K extends object, V> {
  private cache = new WeakMap<K, { value: V; timestamp: number }>();
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
}
```

### 4. Memory Monitoring

```typescript
function monitorMemory() {
  if (performance.memory) {
    const used = performance.memory.usedJSHeapSize;
    const total = performance.memory.jsHeapSizeLimit;
    const percentage = (used / total) * 100;
    
    console.log(`Memory: ${percentage.toFixed(2)}%`);
    
    if (percentage > 80) {
      console.warn('High memory usage!');
    }
  }
}

setInterval(monitorMemory, 5000);
```

## Common Mistakes

### 1. Holding Unnecessary References

```typescript
// Bad: Holding reference after use
function process() {
  const data = fetchData();
  process大数据(data);
  // data still referenced!
}

// Good: Release reference
function process() {
  const data = fetchData();
  process大数据(data);
  data = null;  // Allow GC
}
```

### 2. Global Caches Without Limits

```typescript
// Bad: Unbounded cache
const cache = new Map();
function getCached(key: string) {
  if (!cache.has(key)) {
    cache.set(key, expensiveOperation(key));
  }
  return cache.get(key);
}

// Good: Bounded cache
const cache = new Map();
const MAX_SIZE = 1000;
function getCached(key: string) {
  if (cache.size >= MAX_SIZE) {
    const firstKey = cache.keys().next().value;
    cache.delete(firstKey);
  }
  if (!cache.has(key)) {
    cache.set(key, expensiveOperation(key));
  }
  return cache.get(key);
}
```

### 3. Not Using WeakMap for Object References

```typescript
// Bad: Map prevents GC
const objectCache = new Map();
function process(obj: object) {
  objectCache.set(obj, result);
}

// Good: WeakMap allows GC
const objectCache = new WeakMap();
function process(obj: object) {
  objectCache.set(obj, result);
}
```

### 4. Forgetting to Clear Timers

```typescript
// Bad: Timer keeps running
function start() {
  setInterval(() => {
    updateUI();
  }, 1000);
}

// Good: Clear timer
function start() {
  const id = setInterval(() => {
    updateUI();
  }, 1000);
  
  return () => clearInterval(id);
}
```

## Best Practices

### 1. Minimize Object Creation

```typescript
// Bad: Creates new objects
function process(items: Item[]) {
  return items.map(item => ({
    ...item,
    processed: true
  }));
}

// Good: Reuse objects
function process(items: Item[]) {
  return items.map(item => {
    item.processed = true;
    return item;
  });
}
```

### 2. Use Object Pooling

```typescript
// For frequently created/destroyed objects
const pool = new ObjectPool(() => ({
  x: 0, y: 0, vx: 0, vy: 0
}));

function createParticle() {
  return pool.acquire();
}

function destroyParticle(particle: Particle) {
  pool.release(particle);
}
```

### 3. Implement Bounded Caches

```typescript
class BoundedCache<K, V> {
  private cache = new Map<K, V>();
  private maxSize: number;
  
  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }
  
  set(key: K, value: V) {
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}
```

### 4. Use WeakRef for Large Objects

```typescript
// Allow GC while maintaining access
class DataStore {
  private data = new WeakRef<LargeObject>({});
  
  getData(): LargeObject | undefined {
    return this.data.deref();
  }
  
  setData(data: LargeObject) {
    this.data = new WeakRef(data);
  }
}
```

## Performance Considerations

### GC Pauses

```typescript
// GC can cause pauses
// Mitigate by:
// 1. Reducing allocations in hot paths
// 2. Using object pooling
// 3. Processing data in chunks

// Bad: Large allocation
function process() {
  const hugeArray = new Array(10000000);
  // ... process
}

// Good: Process in chunks
function process() {
  for (let i = 0; i < 10000000; i += 1000) {
    const chunk = new Array(1000);
    // ... process chunk
  }
}
```

### Memory Pressure

```typescript
// Monitor and respond to memory pressure
if ('memory' in performance) {
  const memory = (performance as any).memory;
  
  if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.8) {
    // Reduce cache size, clear unnecessary data
    cache.clear();
  }
}
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is garbage collection in JavaScript?**

A: Garbage collection is the automatic process of reclaiming memory occupied by objects that are no longer in use or reachable.

**Q2: How does JavaScript determine which objects to collect?**

A: JavaScript uses mark-and-sweep algorithm. It marks all reachable objects from roots, then sweeps (collects) unmarked objects.

**Q3: What are root objects?**

A: Root objects are starting points for garbage collection: global object, current call stack, and any object referenced by roots.

**Q4: Can you force garbage collection?**

A: No, you cannot force GC in JavaScript. Some browsers provide `gc()` for debugging, but it's not part of the standard.

**Q5: What is memory pressure?**

A: Memory pressure occurs when the system is low on memory, causing frequent GC cycles and potential performance issues.

### Intermediate (5-10 questions)

**Q6: What is the difference between mark-and-sweep and reference counting?**

A: Mark-and-sweep handles circular references, reference counting doesn't. Mark-and-sweep is used in modern JavaScript engines.

**Q7: What is generational garbage collection?**

A: Objects are divided into young and old generations. Young generation is collected frequently, old generation less frequently.

**Q8: How do closures affect garbage collection?**

A: Closures capture their lexical environment. If a closure is alive, its captured variables cannot be garbage collected.

**Q9: What is WeakMap and how does it relate to GC?**

A: WeakMap allows garbage collection of its keys. When a key has no other references, it and its value can be collected.

**Q10: How do you reduce GC pressure in JavaScript?**

A: Minimize object creation, use object pooling, implement bounded caches, process data in chunks.

### Senior (10-15 questions)

**Q11: Explain V8's garbage collection process.**

A: V8 uses generational GC with Scavenge for young gen and Mark-Sweep-Compact for old gen. It includes incremental and concurrent marking.

**Q12: What are the performance implications of GC pauses?**

A: GC pauses can cause UI jank and reduced throughput. Mitigate by reducing allocations and using object pooling.

**Q13: How do you profile memory usage in production?**

A: Use performance.memory API, Chrome DevTools, heap snapshots, and memory monitoring tools.

**Q14: What is the relationship between GC and memory leaks?**

A: Memory leaks prevent GC from collecting unreachable objects, causing memory usage to grow indefinitely.

**Q15: How do different JavaScript engines optimize GC?**

A: V8 uses concurrent marking, SpiderMonkey uses compartmental GC, JavaScriptCore uses bmalloc.

### FAANG-style (5-10 questions)

**Q16: Design a memory-efficient caching system.**

A: Use WeakMap for object keys, implement LRU eviction, set TTL, limit cache size, monitor memory usage.

**Q17: How would you implement automatic memory cleanup?**

A: Reference counting, weak references, periodic cleanup, automatic disposal patterns.

**Q18: Analyze the memory implications of different data structures.**

A: Arrays vs Maps vs WeakMaps, object pooling, structural sharing, typed arrays.

**Q19: How do you debug memory issues in production?**

A: Memory profiling, heap dumps, growth detection, error tracking, performance monitoring.

**Q20: What are security implications of memory management?**

A: Information leakage through memory dumps, denial of service through memory exhaustion.

### Follow-ups (5-10 questions)

**Q21: Can you give an example of GC-related performance issue?**

A: Frequent object creation in a hot path causes GC pauses, leading to UI jank.

**Q22: How do you handle GC in a real-time application?**

A: Object pooling, pre-allocation, minimize allocations, use typed arrays.

**Q23: What is the relationship between GC and the event loop?**

A: GC can run during idle periods or between tasks. Major GC can cause delays.

**Q24: How do different frameworks handle memory management?**

A: React: memo/useCallback. Vue: reactivity system. Angular: change detection.

**Q25: What are best practices for memory management?**

A: Minimize allocations, use pooling, implement bounded caches, monitor usage, test for leaks.

## Summary

Garbage collection is essential for JavaScript:

1. **Algorithm**: Mark-and-sweep (handles circular refs)
2. **Generational**: Young/old generation optimization
3. **Performance**: GC pauses can impact performance
4. **Best practices**: Minimize allocations, use pooling
5. **WeakMap/WeakRef**: Allow GC of referenced objects
6. **Monitoring**: Track memory usage
7. **Common issues**: Closures, global caches, timers

## Cheat Sheet

```
GARBAGE COLLECTION CHEAT SHEET
═══════════════════════════════════════════════════════════════

ALGORITHM:
• Mark-and-sweep
• Start from roots
• Mark reachable objects
• Sweep unmarked objects

GENERATIONAL GC:
• Young Generation: New objects, collected frequently
• Old Generation: Surviving objects, collected less
• Promotion: Young → Old after surviving collections

V8 OPTIMIZATIONS:
• Scavenge: Young gen collection
• Mark-Sweep-Compact: Old gen collection
• Incremental marking: Breaks work into chunks
• Concurrent marking: Marks while JS runs

CLOSURES AND GC:
• Closures capture lexical environment
• Captured variables kept alive
• Release references to allow GC

WEAKMAP:
• Allows GC of keys
• Use for object caches
• Keys can be garbage collected

BEST PRACTICES:
• Minimize object creation
• Use object pooling
• Implement bounded caches
• Use WeakMap for object references
• Process data in chunks

PERFORMANCE:
• GC causes pauses
• Reduce allocations in hot paths
• Use typed arrays
• Monitor memory usage

DEBUGGING:
• Chrome DevTools Memory tab
• Heap snapshots
• performance.memory API
• Memory monitoring

COMMON ISSUES:
• Unbounded caches
• Global variables
• Forgotten timers
• Closures capturing large objects
```

## References & Learn More

- [MDN: Memory Management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Memory_Management)
- [V8 Blog: Trash Talk - The Orinoco Garbage Collector](https://v8.dev/blog/trash-talk)
- [V8 Blog: Orinoco Project](https://v8.dev/blog/orinoco)
- [FreeCodeCamp: Garbage Collection in JavaScript](https://www.freecodecamp.org/news/how-to-understand-garbage-collection-in-javascript/)
