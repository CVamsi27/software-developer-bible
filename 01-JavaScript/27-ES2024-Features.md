---
section: JavaScript
category: Core
tags: [concept, reference]
---

# ES2024+ Modern JavaScript Features

## TL;DR

ES2024 (released June 2024) added `Object.groupBy`, `Map.groupBy`, `Promise.withResolvers`, and `ArrayBuffer.prototype.transfer`. ES2023 brought `Array.prototype.toSorted/toReversed/toSpliced/with`, `Array.prototype.findLast/findLastIndex`, `#!` shebang support, and `Symbol.prototype.description`. ES2025 is in progress. These are the modern APIs senior engineers reach for instead of legacy workarounds.

## Why It Matters

Senior interviews increasingly test modern API knowledge. Knowing `structuredClone` (2022), `toSorted` (immutable sort, 2023), `Promise.withResolvers` (no more `let resolve, reject;` boilerplate, 2024), and `Array.groupBy` (group without lodash) signals current, production-grade fluency. They also have real perf wins — `toSorted` doesn't mutate, so React/Redux can rely on it without `immer` overhead.

## Definition

The ECMAScript specification evolves yearly (since ES2015). Each release adds new syntax, methods, and APIs after a 4-stage TC39 process. The most relevant additions for senior full-stack work since 2022 are the immutable array methods, structured cloning, the new grouping helpers, and Promise improvements.

## Why Do We Need It?

1. **Less boilerplate** — `Promise.withResolvers()` removes the `let resolve, reject` dance for hand-rolled promises
2. **Immutable by default** — `toSorted`, `toReversed`, `toSpliced`, `with` (ES2023) avoid mutation, critical for React/Redux
3. **Native grouping** — `Object.groupBy`/`Map.groupBy` (ES2024) replace `_.groupBy` and reduce loops
4. **Deep cloning built-in** — `structuredClone` (ES2022) handles Dates, Maps, Sets, RegExps, ArrayBuffers, and cycles
5. **Better ergonomics** — `findLast`, `findLastIndex`, `Symbol.description` remove common papercuts

## How It Works

### ES2022: Foundational Modern APIs

```typescript
// structuredClone — deep clone with cycle and type support
const original = {
  date: new Date(),
  map: new Map([['k', 'v']]),
  set: new Set([1, 2, 3]),
  regex: /foo/g,
};
const clone = structuredClone(original);
// clone.date instanceof Date === true
// clone.map instanceof Map === true
// structuredClone can even clone cycles
const a = { self: null };
a.self = a;
const c = structuredClone(a); // works! lodash _.cloneDeep throws or recurses infinitely

// ❌ Old way (lossy + unsafe)
const bad = JSON.parse(JSON.stringify(a)); // throws on cycle, loses Date/Map/Set

// Class fields (public/private)
class Counter {
  count = 0;            // public field
  #privateField = 'secret'; // truly private (hard private)
  static instances = 0; // static field
}

// Top-level await in ESM
const config = await fetch('/api/config').then(r => r.json());
```

### ES2023: Immutable Array Methods

```typescript
const nums = [3, 1, 4, 1, 5, 9, 2, 6];

// .toSorted() — returns new sorted array, original untouched
const sorted = nums.toSorted();           // [1, 1, 2, 3, 4, 5, 6, 9]
const desc   = nums.toSorted((a, b) => b - a); // [9, 6, 5, 4, 3, 2, 1, 1]

// .toReversed() — returns new reversed array
const reversed = nums.toReversed();

// .toSpliced() — returns new spliced array
const withoutFirst = nums.toSpliced(0, 1); // [1, 4, 1, 5, 9, 2, 6]

// .with() — returns new array with one element replaced
const replaced = nums.with(2, 99); // [3, 1, 99, 1, 5, 9, 2, 6]

// .findLast() and .findLastIndex() — search from end
const lastEven  = nums.findLast(n => n % 2 === 0);  // 6
const lastEvenI = nums.findLastIndex(n => n % 2 === 0); // 7

// Why it matters: in React/Redux, mutating arrays triggers re-render bugs.
// toSorted/toReversed/etc. enable functional updates without immer/spread copies.
```

### ES2024: Grouping, Promise Improvements, ArrayBuffer

```typescript
// Object.groupBy() — group by key, returns plain object
const inventory = [
  { name: 'asparagus', type: 'vegetables' },
  { name: 'bananas',   type: 'fruit' },
  { name: 'goat',      type: 'meat' },
  { name: 'cherries',  type: 'fruit' },
  { name: 'fish',      type: 'meat' },
];

const grouped = Object.groupBy(inventory, item => item.type);
// {
//   vegetables: [{ name: 'asparagus', type: 'vegetables' }],
//   fruit:      [{ name: 'bananas', type: 'fruit' }, { name: 'cherries', type: 'fruit' }],
//   meat:       [{ name: 'goat', type: 'meat' }, { name: 'fish', type: 'meat' }],
// }

// Map.groupBy() — same but returns a Map (preserves insertion order, any key type)
const byType = Map.groupBy(inventory, item => item.type);

// Promise.withResolvers() — no more "let resolve, reject" boilerplate
const { promise, resolve, reject } = Promise.withResolvers();

// Use case: timeout-style cancellation
function withTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
  const { promise, reject } = Promise.withResolvers<T>();
  const timer = setTimeout(() => reject(new Error('Timeout')), ms);
  p.then(v => { clearTimeout(timer); resolve(v); },
         e => { clearTimeout(timer); reject(e); });
  return promise;
}

// ArrayBuffer.prototype.transfer() / transferToFixedLength()
// Detach the original buffer and return a new one with the same byte contents.
// Useful for moving binary data between threads (postMessage) without copying.
const source = new Uint8Array([1, 2, 3, 4]).buffer;
const dest = source.transfer(); // source is now detached (byteLength 0)
```

### ES2023: Shebang and Symbol.description

```typescript
// #! (shebang) at the top of a JS file is now valid
#!/usr/bin/env node
console.log('runs as a CLI');

// Symbol.description
const sym = Symbol('my description');
sym.description; // 'my description' (was previously sym.toString().slice(7, -1))
```

## Code Examples

### Real-World: React useState with Immutable Sort

```typescript
// ❌ Pre-ES2023: had to spread to avoid mutating state
const [items, setItems] = useState([3, 1, 2]);
const sortAsc = () => setItems([...items].sort((a, b) => a - b));

// ✅ ES2023: toSorted returns a new array, original untouched
const [items, setItems] = useState([3, 1, 2]);
const sortAsc = () => setItems(prev => prev.toSorted((a, b) => a - b));
// Cleaner, safer, no accidental mutation if state is shared
```

### Real-World: Cancelable Fetch with withResolvers

```typescript
async function fetchWithCancel(url: string, signal: AbortSignal) {
  const { promise, resolve, reject } = Promise.withResolvers<Response>();

  const controller = new AbortController();
  signal.addEventListener('abort', () => {
    controller.abort();
    reject(new DOMException('Aborted', 'AbortError'));
  });

  fetch(url, { signal: controller.signal }).then(resolve, reject);
  return promise;
}
```

### Real-World: Group Orders by Status

```typescript
type Order = { id: string; status: 'pending' | 'shipped' | 'delivered'; amount: number };
const orders: Order[] = await fetchOrders();

// ES2024: native grouping, no lodash needed
const byStatus = Map.groupBy(orders, o => o.status);

const pending = byStatus.get('pending') ?? [];
const totalPending = pending.reduce((sum, o) => sum + o.amount, 0);
```

## Real-World Use Cases

1. **React/Redux state updates** — `toSorted`/`toReversed`/`with` enable immutable updates without `immer` overhead
2. **Form array manipulation** — `toSpliced` for remove-from-list without `slice` + `concat` chains
3. **Async cancellation** — `Promise.withResolvers` for timeout patterns, retry wrappers, abort signals
4. **Binary data (WebAssembly, file uploads)** — `ArrayBuffer.transfer` for zero-copy postMessage between workers
5. **Reporting dashboards** — `Object.groupBy` for aggregating orders, users, events by category
6. **Search & filter UIs** — `findLast` for "most recent" queries (e.g., last message in a thread)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `sort()` in React state updater (mutates state) | Use `toSorted()` (ES2023) — always returns a new array |
| `JSON.parse(JSON.stringify(obj))` to deep clone | Use `structuredClone(obj)` — handles Date/Map/Set/cycles |
| `_.groupBy(items, fn)` for simple grouping | Use `Object.groupBy(items, fn)` (ES2024) — zero dependency |
| `let resolve, reject; new Promise((res, rej) => { resolve = res; reject = rej; })` | Use `Promise.withResolvers()` (ES2024) — cleaner and safer |
| `arr[arr.length - 1]` to find last matching element | Use `arr.findLast(predicate)` — readable, handles edge cases |
| `const buf2 = buf1.slice(0)` for "transfer" | Use `buf1.transfer()` — detaches original, no copy |
| Hand-rolling deep clone with recursion | Use `structuredClone` — handles cycles, typed arrays, Maps |

## Best Practices

1. **Reach for `structuredClone` over `JSON.parse(JSON.stringify(...))`** for any non-trivial object — it's lossless and handles cycles
2. **Prefer immutable methods (`toSorted`, `toReversed`, `with`) in React/Redux** — no immer needed for simple updates
3. **Use `Promise.withResolvers` for cancellable/timed promises** — cleaner than the resolve/reject closure pattern
4. **Use `Object.groupBy`/`Map.groupBy` for ad-hoc grouping** — no need to install lodash for one helper
5. **Check Node/browser support before adopting** — `toSorted` requires Node 20+, `Object.groupBy` requires Node 21+
6. **For binary data, prefer `ArrayBuffer.transfer()` over `slice()`** when you need ownership transfer, not a copy
7. **Avoid `Array.prototype.group`/`groupBy` polyfills in old environments** — they predate the spec; use `Map.group` or a manual reduce instead

## Performance Considerations

| Operation | Old Way | New Way | Notes |
|-----------|---------|---------|-------|
| Immutable sort | `[...arr].sort()` (full copy) | `arr.toSorted()` | Engine-optimized copy; similar perf, clearer intent |
| Deep clone | `JSON.parse(JSON.stringify(x))` | `structuredClone(x)` | 2-5× faster on V8 for large objects; lossless |
| Group by key | Reduce + push loops | `Object.groupBy` / `Map.groupBy` | Comparable perf; one line vs. five |
| Cancelable promise | `new Promise((res, rej) => { ... })` | `Promise.withResolvers()` | Marginal perf; better readability |
| Find last match | Reverse + find (O(2n)) | `findLast` (O(n) worst case) | Half the comparisons in worst case |

**Browser/Node support (as of Jan 2026):**
- ES2022 features: baseline (Node 18+, all modern browsers)
- ES2023 features (`toSorted`, `findLast`): Node 20+, Chrome 110+, Safari 16.4+
- ES2024 features (`Object.groupBy`, `Promise.withResolvers`, `ArrayBuffer.transfer`): Node 21+, Chrome 117+, Safari 17.4+

## Summary

ES2022+ added the modern APIs senior engineers reach for daily: `structuredClone`, immutable array methods (`toSorted`, `toReversed`, `toSpliced`, `with`), `findLast`/`findLastIndex`, `Object.groupBy`/`Map.groupBy`, and `Promise.withResolvers`. They reduce dependency footprint, eliminate mutation bugs, and have measurable performance wins. Know their support matrix — `toSorted` and `groupBy` are recent enough to require Node 20+/21+.

## Cheat Sheet

| Feature | Year | Use Case | Replaces |
|---------|------|----------|----------|
| `structuredClone` | 2022 | Deep clone | `JSON.parse(JSON.stringify(...))`, lodash `_.cloneDeep` |
| Class fields (`#private`) | 2022 | True private class state | `_underscore` convention |
| Top-level await | 2022 | ESM config loading | IIFE wrapper for async init |
| `toSorted`/`toReversed`/`toSpliced`/`with` | 2023 | Immutable updates | `[...arr].sort()` |
| `findLast`/`findLastIndex` | 2023 | Reverse search | Manual reverse + find |
| `Symbol.description` | 2023 | Read symbol description | `sym.toString().slice(7, -1)` |
| `#!` shebang | 2023 | CLI scripts | Comment-based hacks |
| `Object.groupBy` / `Map.groupBy` | 2024 | Group arrays | `_.groupBy`, reduce loops |
| `Promise.withResolvers` | 2024 | Cancelable/timed Promises | `let resolve, reject` pattern |
| `ArrayBuffer.prototype.transfer` | 2024 | Zero-copy transfer | `slice(0)` |

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Map, Set, WeakMap, WeakSet](14-Map-Set-WeakMap-WeakSet.md)
- [Promises](10-Promises.md)
- [Shallow vs Deep Copy](15-Shallow-vs-Deep-Copy.md)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [TC39 Finished Proposals](https://github.com/tc39/proposals/blob/main/finished-proposals.md)
- [MDN: structuredClone](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone)
- [MDN: Array.prototype.toSorted](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted)
- [MDN: Object.groupBy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy)
- [MDN: Promise.withResolvers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/withResolvers)
- [V8 Blog: ES2024 features](https://v8.dev/features/temporal)
- [Node.js ESM Documentation](https://nodejs.org/api/esm.html)
