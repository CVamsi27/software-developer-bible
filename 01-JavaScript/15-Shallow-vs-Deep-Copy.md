---
section: JavaScript
category: Core
tags: [concept]
---

# Shallow Copy vs Deep Copy

## Definition

A **Shallow Copy** creates a new object with the same property values, but nested objects are still referenced. A **Deep Copy** creates a new object with completely independent copies of all nested objects.

## Why Do We Need It?

- **Immutability**: Prevent unintended mutations
- **State Management**: Create independent state copies
- **Data Isolation**: Prevent shared state bugs
- **Function Purity**: Ensure functions don't modify inputs

## How It Works

### Copy Methods Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                     COPY METHODS                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SHALLOW COPY:                                              │
│  • Spread: { ...obj }                                       │
│  • Object.assign({}, obj)                                   │
│  • Array.from(arr)                                          │
│  • arr.slice()                                              │
│                                                              │
│  DEEP COPY:                                                 │
│  • structuredClone(obj)                                     │
│  • JSON.parse(JSON.stringify(obj))                          │
│  • Recursive function                                       │
│  • Libraries (lodash cloneDeep)                             │
│                                                              │
│  NESTED OBJECTS:                                            │
│  • Shallow: Both point to same nested object               │
│  • Deep: Completely independent nested objects             │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Shallow Copy

```typescript
const original = {
  name: 'Alice',
  hobbies: ['reading', 'gaming']
};

const shallow = { ...original };

shallow.name = 'Bob';
console.log(original.name);  // 'Alice' (unchanged)

shallow.hobbies.push('cooking');
console.log(original.hobbies);  // ['reading', 'gaming', 'cooking'] (changed!)

```

### Deep Copy with structuredClone

```typescript
const original = {
  name: 'Alice',
  address: { city: 'New York', state: 'NY' }
};

const deep = structuredClone(original);

deep.address.city = 'Boston';
console.log(original.address.city);  // 'New York' (unchanged)

```

### JSON Method

```typescript
const original = { name: 'Alice', data: { x: 1 } };

// Limitations: no functions, undefined, circular refs
const copy = JSON.parse(JSON.stringify(original));

// Fails with:
// - Functions
// - undefined values
// - Circular references
// - Date objects (become strings)
// - RegExp (becomes empty object)

```

### Recursive Deep Copy

```typescript
function deepClone(obj: any, seen = new WeakMap()): any {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (seen.has(obj)) {
    return seen.get(obj);
  }

  if (obj instanceof Date) return new Date(obj);
  if (obj instanceof RegExp) return new RegExp(obj);
  if (obj instanceof Map) {
    const map = new Map();
    seen.set(obj, map);
    obj.forEach((val, key) => map.set(deepClone(key, seen), deepClone(val, seen)));
    return map;
  }
  if (obj instanceof Set) {
    const set = new Set();
    seen.set(obj, set);
    obj.forEach(val => set.add(deepClone(val, seen)));
    return set;
  }

  const clone = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));
  seen.set(obj, clone);

  for (const key of Reflect.ownKeys(obj)) {
    clone[key] = deepClone(obj[key as keyof typeof obj], seen);
  }

  return clone;
}

```

### Object.assign for Shallow Copy

```typescript
const original = { a: 1, b: { c: 2 } };
const copy = Object.assign({}, original);

copy.b.c = 999;
console.log(original.b.c);  // 999 (shared nested object)

```

### Array Copying

```typescript
const arr = [1, [2, 3], 4];

// Shallow
const shallow1 = [...arr];
const shallow2 = arr.slice();
const shallow3 = Array.from(arr);

// Deep
const deep1 = structuredClone(arr);
const deep2 = JSON.parse(JSON.stringify(arr));

shallow1[1][0] = 999;
console.log(arr[1][0]);  // 999 (shared)

deep2[1][0] = 888;
console.log(arr[1][0]);  // 999 (independent)

```

## Real-World Use Cases

### React State Updates

```typescript
// Bad: Mutates state
function addItem(state: { items: string[] }, item: string) {
  state.items.push(item);
  return state;
}

// Good: Returns new state
function addItemSafe(state: { items: string[] }, item: string) {
  return { ...state, items: [...state.items, item] };
}

// Deep update
function updateUser(state: State, updates: Partial<User>) {
  return {
    ...state,
    user: { ...state.user, ...updates }
  };
}

```

### Immutable Data in Redux

```typescript
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'UPDATE_NESTED':
      return {
        ...state,
        nested: {
          ...state.nested,
          value: action.payload
        }
      };
    default:
      return state;
  }
}

```

### Undo/Redo Pattern

```typescript
class HistoryManager<T> {
  private history: T[] = [];
  private currentIndex = -1;

  push(state: T) {
    this.history = this.history.slice(0, this.currentIndex + 1);
    this.history.push(structuredClone(state));
    this.currentIndex++;
  }

  undo(): T | undefined {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      return structuredClone(this.history[this.currentIndex]);
    }
    return undefined;
  }

  redo(): T | undefined {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++;
      return structuredClone(this.history[this.currentIndex]);
    }
    return undefined;
  }
}

```

### API Response Caching

```typescript
class Cache {
  private cache = new Map<string, any>();

  set(key: string, value: any) {
    this.cache.set(key, structuredClone(value));
  }

  get(key: string) {
    const value = this.cache.get(key);
    return value ? structuredClone(value) : undefined;
  }
}

```

## Common Mistakes

### 1. Assuming Spread is Deep Copy

```typescript
const original = { nested: { value: 1 } };
const copy = { ...original };

copy.nested.value = 2;
console.log(original.nested.value);  // 2 (shared!)

```

### 2. JSON.stringify Limitations

```typescript
const obj = {
  date: new Date(),
  fn: () => {},
  undef: undefined,
  nan: NaN,
  infinity: Infinity
};

const copy = JSON.parse(JSON.stringify(obj));
// date becomes string, fn/undef lost, NaN -> null, Infinity -> null

```

### 3. Circular References

```typescript
const obj: any = { name: 'Alice' };
obj.self = obj;  // Circular reference

// JSON.stringify throws TypeError
// structuredClone handles it correctly
const copy = structuredClone(obj);

```

### 4. Not Freezing After Copy

```typescript
const original = { nested: { value: 1 } };
const copy = { ...original };

// copy.nested is still mutable
// Need to freeze if immutability is desired
Object.freeze(copy);

```

## Best Practices

### 1. Choose the Right Method

```typescript
// Shallow: Simple objects, no nesting
const shallow = { ...original };

// Deep: Complex nested objects
const deep = structuredClone(original);

// Performance critical: Consider immutable libraries

```

### 2. Use TypeScript for Type Safety

```typescript
function updateItem<T extends { id: string }>(
  items: T[],
  id: string,
  updates: Partial<T>
): T[] {
  return items.map(item =>
    item.id === id ? { ...item, ...updates } : item
  );
}

```

### 3. Document Mutation Behavior

```typescript
/**

 - Returns new array (original unchanged)
 */
function addItem<T>(arr: T[], item: T): T[] {
  return [...arr, item];
}

/**

 - Mutates original array
 */
function addItemInPlace<T>(arr: T[], item: T): void {
  arr.push(item);
}

```

### 4. Use Object.freeze for Constants

```typescript
const CONFIG = Object.freeze({
  apiUrl: 'https://api.example.com',
  timeout: 5000
});

// CONFIG.apiUrl = 'other'; // Silently fails

```

## Performance Considerations

### Copy Overhead

```typescript
// Shallow copy: O(n) where n = number of properties
const shallow = { ...largeObject };

// Deep copy: O(n*m) where m = depth of nesting
const deep = structuredClone(largeObject);

// For large objects, prefer:
// 1. Reference when possible
// 2. Lazy copying
// 3. Structural sharing

```

### Memory Usage

```typescript
// Each copy consumes memory
// Large objects: Use references when safe
// Shared state: Consider immutable data structures

// Measure before optimizing
console.time('copy');
const copy = structuredClone(largeObject);
console.timeEnd('copy');

```

## Summary

Understanding shallow vs deep copy is essential:

1. **Shallow copy**: Fast, but nested objects are shared

2. **Deep copy**: Independent, but more expensive

3. **structuredClone**: Modern, handles most types

4. **JSON method**: Simple but limited

5. **Performance**: Choose based on needs

6. **Best practices**: Document behavior, use TypeScript

7. **Common bugs**: Assume deep when it's shallow

## Cheat Sheet
```dockerfile
SHALLOW vs DEEP COPY CHEAT SHEET
═══════════════════════════════════════════════════════════════

SHALLOW COPY:
• Spread: { ...obj }
• Object.assign({}, obj)
• Array.from(arr), arr.slice()
• Nested objects are shared references

DEEP COPY:
• structuredClone(obj) - recommended
• JSON.parse(JSON.stringify(obj)) - limited
• Recursive function - customizable
• Libraries: lodash cloneDeep

WHEN TO USE:
• Shallow: Simple objects, shared nested state
• Deep: Complex objects, complete independence

LIMITATIONS:
JSON.stringify:
• No functions
• No undefined
• No circular refs
• Date -> string
• RegExp -> empty object

structuredClone:
• Handles most types
• Supports circular refs
• Modern browsers only

PERFORMANCE:
• Shallow: O(n)
• Deep: O(n*m)
• Consider object size and nesting depth

BEST PRACTICES:
• Choose appropriate method
• Document mutation behavior
• Use TypeScript
• Freeze when needed
• Measure before optimizing

```

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Node.js](../05-NodeJS/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [MDN: Object.assign()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
- [MDN: structuredClone()](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone)
- [JavaScript.info: Copying by Reference](https://javascript.info/copying-by-reference)
- [MDN: Spread Syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax)
