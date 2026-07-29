# Map, Set, WeakMap, WeakSet

[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

## Definition

**Map**, **Set**, **WeakMap**, and **WeakSet** are ES6 (ECMAScript 2015) collection data structures that provide specialized ways to store and manage data. `Map` stores key-value pairs with any value type as keys, `Set` stores unique values of any type, and their "Weak" counterparts (`WeakMap`, `WeakSet`) hold weak references that don't prevent garbage collection, enabling memory-efficient caches and metadata storage.

## Why Do We Need It?

1. **Map vs Object**: Maps accept any value type as keys (objects, functions, primitives), maintain insertion order, and have better performance for frequent add/delete operations

2. **Set vs Array**: Sets automatically enforce uniqueness and provide O(1) lookup instead of O(n)

3. **WeakMap**: Prevents memory leaks when associating metadata with objects — the metadata is garbage collected when the object is no longer referenced

4. **WeakSet**: Efficiently tracks object membership without preventing GC

5. **Memory Safety**: Weak collections eliminate the need for manual cleanup in cache-like scenarios

## How It Works

### Map Internal Structure

```text
Map
┌─────────────────────────────────────────────┐
│  [[MapData]]                                 │
│  ┌───────────────────────────────────────┐  │
│  │  [key: any, value: any][]             │  │
│  │                                       │  │
│  │  Entry: [key1 → value1]              │  │
│  │  Entry: [key2 → value2]              │  │
│  │  Iteration order = insertion order   │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  Size tracking: map.size                     │
│  Lookup: O(1) average                        │
└─────────────────────────────────────────────┘
```

### WeakMap Internal Structure

```text
WeakMap
┌─────────────────────────────────────────────┐
│  [[WeakMapData]]                             │
│  ┌───────────────────────────────────────┐  │
│  │  Key:   Object (weak reference)      │  │
│  │  Value: any                          │  │
│  │                                       │  │
│  │  ObjectA → metadata                  │  │
│  │  ObjectB → metadata                  │  │
│  │                                       │  │
│  │  When ObjectA is GC'd → entry auto   │  │
│  │  removed from WeakMap                 │  │
│  └───────────────────────────────────────┘  │
│                                              │
│  NOT iterable, NOT enumerable                │
│  Keys must be objects                        │
└─────────────────────────────────────────────┘
```

## Code Examples

### Map: Key-Value Storage

```typescript
// Creating a Map
const userMap = new Map<string, User>();

// Using objects as keys (impossible with plain objects)
const userRoles = new Map<object, string[]>();
const alice = { id: 1, name: 'Alice' };
const bob = { id: 2, name: 'Bob' };

userRoles.set(alice, ['admin', 'editor']);
userRoles.set(bob, ['viewer']);

console.log(userRoles.get(alice)); // ['admin', 'editor']
console.log(userRoles.has(bob));   // true

// Map preserves insertion order
const ordered = new Map<string, number>();
ordered.set('first', 1);
ordered.set('second', 2);
ordered.set('third', 3);

for (const [key, value] of ordered) {
  console.log(key, value); // 'first' 1, 'second' 2, 'third' 3
}

// Map size and iteration
console.log(userMap.size);                    // Number of entries
userMap.forEach((value, key) => console.log(key, value));

// Converting between Map and Object
const obj = { a: 1, b: 2, c: 3 };
const fromObj = new Map(Object.entries(obj)); // Map(3) {'a' => 1, 'b' => 2, 'c' => 3}
const backToObj = Object.fromEntries(fromObj); // { a: 1, b: 2, c: 3 }

// Map methods
const map = new Map<string, number>();
map.set('x', 10);
map.get('x');           // 10
map.has('x');           // true
map.delete('x');        // true
map.clear();            // Remove all entries
```

### Set: Unique Values

```typescript
// Creating a Set
const numbers = new Set([1, 2, 3, 2, 1]); // Set(3) {1, 2, 3}
console.log(numbers.size); // 3

// Common operations
numbers.add(4);
numbers.has(2);   // true
numbers.delete(2); // true
numbers.clear();

// Deduplication
const duplicates = [1, 2, 2, 3, 3, 4];
const unique = [...new Set(duplicates)]; // [1, 2, 3, 4]

// Set operations
const setA = new Set([1, 2, 3, 4]);
const setB = new Set([3, 4, 5, 6]);

// Union
const union = new Set([...setA, ...setB]); // {1, 2, 3, 4, 5, 6}

// Intersection
const intersection = new Set([...setA].filter(x => setB.has(x))); // {3, 4}

// Difference
const difference = new Set([...setA].filter(x => !setB.has(x))); // {1, 2}

// Iteration
for (const item of numbers) { /* ... */ }
numbers.forEach(value => console.log(value));

// Checking subsets
const isSubset = (subset: Set<unknown>, superset: Set<unknown>) =>
  [...subset].every(item => superset.has(item));
```

### WeakMap: Memory-Safe Metadata

```typescript
// Private data without memory leaks
const privateData = new WeakMap<object, { secret: string }>();

class User {
  constructor(name: string, secret: string) {
    privateData.set(this, { secret });
  }

  getSecret(): string {
    return privateData.get(this)?.secret ?? 'none';
  }
}

const user = new User('Alice', 'mySecret123');
console.log(user.getSecret()); // 'mySecret123'
// privateData is not accessible from outside
// When 'user' is garbage collected → the entry is auto-removed

// Caching without memory leaks
const cache = new WeakMap<object, CachedData>();

function getExpensiveData(obj: object): CachedData {
  if (!cache.has(obj)) {
    cache.set(obj, computeExpensiveData(obj));
  }
  return cache.get(obj)!;
}

// Dom node metadata (browser)
const elementMetadata = new WeakMap<Element, Metadata>();

function trackElement(el: Element): void {
  elementMetadata.set(el, {
    clickCount: 0,
    lastInteraction: Date.now(),
  });
}
// When element is removed from DOM → GC cleans up the metadata too
```

### WeakSet: Memory-Safe Tracking

```typescript
// Track visited objects without preventing GC
const visited = new WeakSet<object>();

function markVisited(obj: object): void {
  visited.add(obj);
}

function hasVisited(obj: object): boolean {
  return visited.has(obj);
}

// Track active DOM elements
const activeElements = new WeakSet<HTMLElement>();

function markActive(el: HTMLElement): void {
  activeElements.add(el);
}

function isActive(el: HTMLElement): boolean {
  return activeElements.has(el);
}
// Elements removed from DOM → auto-removed from WeakSet
```

### Map vs Object Performance

```typescript
// When to use Map vs Object

// USE MAP when:
// 1. Keys are not strings (objects, numbers, symbols)
const objectMap = new Map<object, string>();

// 2. Frequent additions/removals (Map.delete is faster)
const frequentChanges = new Map<string, number>();

// 3. Need insertion order guarantees
const orderedMap = new Map<string, number>();

// 4. Need size property
console.log(frequentChanges.size);

// 5. Lots of entries (10k+) — Map performs better
const largeMap = new Map<string, number>();

// USE OBJECT when:
// 1. JSON serialization needed (no toJSON for Map)
const obj = { a: 1, b: 2 };
JSON.stringify(obj); // Works
// JSON.stringify(map); // {} — empty!

// 2. Simple string key lookups with known keys
const config = { apiUrl: 'https://api.example.com', timeout: 5000 };

// 3. Spreading/computed properties
const merged = { ...obj, c: 3 };
```

### Chaining and Composition

```typescript
// Map methods return the map, enabling chaining
const config = new Map<string, unknown>()
  .set('host', 'localhost')
  .set('port', 3000)
  .set('ssl', true);

// Combining collections
class CollectionManager {
  private items = new Map<string, Set<number>>();

  addItem(category: string, value: number): void {
    if (!this.items.has(category)) {
      this.items.set(category, new Set());
    }
    this.items.get(category)!.add(value);
  }

  hasItem(category: string, value: number): boolean {
    return this.items.get(category)?.has(value) ?? false;
  }

  getCategories(): string[] {
    return [...this.items.keys()];
  }
}
```

## Real-World Use Cases

### 1. LRU Cache Implementation

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();

  constructor(private capacity: number) {}

  get(key: K): V | undefined {
    if (!this.cache.has(key)) return undefined;

    // Move to end (most recently used)
    const value = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  put(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      // Delete least recently used (first item)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}
```

### 2. Object Pool with WeakMap

```typescript
const objectPool = new WeakMap<object, boolean>();

function acquireObject<T extends object>(ctor: new () => T): T {
  const obj = new ctor();
  objectPool.set(obj, true);
  return obj;
}

function releaseObject(obj: object): void {
  objectPool.delete(obj);
}
```

## Common Mistakes

### 1. Using Objects as Map Keys Accidentally

```typescript
// ❌ BAD: Using plain object with numeric keys
const obj: Record<number, string> = {};
obj[1] = 'one';
obj['1'] = 'two'; // Overwrites! Coerces to same key

// ✅ GOOD: Use Map for non-string keys
const map = new Map<number, string>();
map.set(1, 'one');
map.set(2, 'two');
// map.has('1') // TypeScript error — correct!
```

### 2. Expecting WeakMap/WeakSet to Be Iterable

```typescript
// ❌ BAD: Trying to iterate WeakMap
const wm = new WeakMap();
// for (const [key, value] of wm) {} // TypeError: wm is not iterable

// ✅ GOOD: Use regular Map when iteration is needed
const regular = new Map();
```

## Best Practices

1. **Use Map over Object** for dynamic keys, frequent updates, or non-string keys

2. **Use Set for uniqueness** — simpler and faster than manual deduplication

3. **Use WeakMap for private data** attached to specific object instances

4. **Use WeakSet for membership tracking** that shouldn't prevent GC

5. **Prefer Map.size** over Object.keys(obj).length

6. **Convert with spread** — `[...map.entries()]`, `[...set.values()]`

7. **Use `Object.fromEntries()`** to convert Map to plain object for JSON

## Performance Considerations

| Operation | Map | Object | Set | Array |
|-----------|:---:|:------:|:---:|:-----:|
| Insert | O(1) | O(1) | O(1) | O(1) |
| Lookup | O(1) | O(1) | O(1) | O(n) |
| Delete | O(1) | O(1) | O(1) | O(n) |
| Size | O(1) | O(n)* | O(1) | O(1) |

\* `Object.keys(obj).length` requires enumerating all keys

## Summary

Map, Set, WeakMap, and WeakSet are essential ES6 collections. Map provides better key-value storage than plain objects for most use cases. Set efficiently enforces uniqueness. WeakMap and WeakSet enable memory-safe metadata and tracking without preventing garbage collection. Choose the right collection based on your key types, iteration needs, and memory requirements.

## Cheat Sheet

```text
COLLECTIONS CHEAT SHEET
═══════════════════════════════════════

MAP:
• Any key type (objects, functions, primitives)
• Insertion order preserved
• Iterable, .size property
• .set(k, v) / .get(k) / .has(k) / .delete(k) / .clear()

SET:
• Unique values of any type
• Insertion order preserved
• .add(v) / .has(v) / .delete(v) / .clear()
• Dedup: [...new Set(arr)]

WEAKMAP:
• Keys MUST be objects (weak references)
• NOT iterable, NO .size
• .set(k, v) / .get(k) / .has(k) / .delete(k)
• Use for: private data, caches, DOM metadata

WEAKSET:
• Values MUST be objects (weak references)
• NOT iterable, NO .size
• .add(v) / .has(v) / .delete(v)
• Use for: membership tracking without GC leaks

KEY DIFFERENCES:
┌────────────┬───────┬───────┬─────────┬─────────┐
│            │ Map   │ Object│ WeakMap │ WeakSet │
├────────────┼───────┼───────┼─────────┼─────────┤
│ Key types  │ Any   │ Str/Sym│ Object │ Object  │
│ Iterable   │ Yes   │ No    │ No      │ No      │
│ Size prop  │ Yes   │ No    │ No      │ No      │
│ GC-safe    │ No    │ No    │ Yes     │ Yes     │
│ JSON       │ No    │ Yes   │ No      │ No      │
└────────────┴───────┴───────┴─────────┴─────────┘

```

---

## See Also
- [Garbage Collection](20-Garbage-Collection.md)
- [Memory Leaks](19-Memory-Leaks.md)
- [Pass by Value](13-Pass-by-Value.md)
- [Shallow vs Deep Copy](15-Shallow-vs-Deep-Copy.md)

## References & Learn More

- [MDN: Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
- [MDN: Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
- [MDN: WeakMap](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap)
- [MDN: WeakSet](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakSet)
- [V8 Blog: Hash Maps in V8](https://v8.dev/blog/hash-map)
