---
section: JavaScript
category: Core
tags: [concept]
---

# Proxy & Reflect

## Definition

**Proxy** and **Reflect** are ES6 (ECMAScript 2015) APIs for metaprogramming. A `Proxy` wraps an object and intercepts fundamental operations (property access, assignment, function invocation, etc.) via customizable **handler traps**. The `Reflect` API provides methods that correspond to each Proxy trap, enabling default behavior to be invoked programmatically. Together, they allow you to intercept, modify, and extend the behavior of objects without modifying the original object.

## Why Do We Need It?

1. **Interception**: Monitor and intercept operations on objects (get, set, delete, etc.)

2. **Validation**: Enforce constraints on object properties at runtime

3. **Reactivity**: Implement reactive programming patterns (like Vue 3's reactivity)

4. **Virtualization**: Create objects with computed or virtual properties

5. **Logging & Debugging**: Automatically log property access and mutations

6. **Access Control**: Implement permissions and data masking layers

7. **The `Reflect` API**: Provides consistent, functional alternatives to `delete`, `in`, etc.

## How It Works

### Proxy Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     PROXY ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  target = { message: 'hello' }                              │
│                                                              │
│  handler = {                                                 │
│    get(target, prop, receiver) {                            │
│      // Custom behavior when property is accessed           │
│      return target[prop];                                   │
│    }                                                         │
│  }                                                           │
│                                                              │
│  proxy = new Proxy(target, handler)                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │   proxy.message → handler.get(target, 'message')    │    │
│  │   Every operation goes through handler traps        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Available Proxy Traps

```text
PROXY TRAPS:
═══════════════════════════════════════

Object Operations:
├── get(target, prop, receiver)          → [[Get]]
├── set(target, prop, value, receiver)   → [[Set]]
├── has(target, prop)                    → in operator
├── deleteProperty(target, prop)         → delete
├── ownKeys(target)                      → Object.keys/Reflect.ownKeys
├── getOwnPropertyDescriptor(target, p)  → Object.getOwnPropertyDescriptor
├── defineProperty(target, prop, desc)   → Object.defineProperty
├── preventExtensions(target)            → Object.preventExtensions
├── getPrototypeOf(target)               → Object.getPrototypeOf
├── setPrototypeOf(target, proto)        → Object.setPrototypeOf
├── isExtensible(target)                 → Object.isExtensible

Function Operations:
├── apply(target, thisArg, args)         → function call ()
├── construct(target, args, newTarget)   → new operator

Property Descriptor Operations:
├── getOwnPropertyDescriptor
├── defineProperty
└── preventExtensions
```

## Code Examples

### Basic Proxy: Property Interception

```typescript
const target = { name: 'Alice', age: 30 };

const handler: ProxyHandler<typeof target> = {
  get(target, prop, receiver) {
    console.log(`GET ${String(prop)}`);
    return Reflect.get(target, prop, receiver);
  },

  set(target, prop, value, receiver) {
    console.log(`SET ${String(prop)} = ${value}`);
    return Reflect.set(target, prop, value, receiver);
  },
};

const proxy = new Proxy(target, handler);

console.log(proxy.name);  // Logs: "GET name" → "Alice"
proxy.age = 31;            // Logs: "SET age = 31"
```

### Validation Proxy

```typescript
function createValidatedObject<T extends object>(obj: T, schema: Record<string, (v: unknown) => boolean>): T {
  return new Proxy(obj, {
    set(target, prop, value, receiver) {
      const validator = schema[prop as string];
      if (validator && !validator(value)) {
        throw new TypeError(`Invalid value for property '${String(prop)}': ${value}`);
      }
      return Reflect.set(target, prop, value, receiver);
    },
  });
}

const user = createValidatedObject(
  { name: 'Alice', age: 25, email: '' },
  {
    age: (v) => typeof v === 'number' && v >= 0 && v < 150,
    name: (v) => typeof v === 'string' && v.length > 0,
    email: (v) => typeof v === 'string' && v.includes('@'),
  }
);

user.age = 30;   // ✅ OK
// user.age = -5; // TypeError: Invalid value for property 'age'
// user.name = ''; // TypeError: Invalid value for property 'name'
```

### Reactivity System (Vue-like)

```typescript
type Subscriber = () => void;

class ReactiveSystem {
  private subscribers = new Map<string | symbol, Set<Subscriber>>();
  private activeEffect: Subscriber | null = null;

  track(prop: string | symbol): void {
    if (!this.activeEffect) return;
    if (!this.subscribers.has(prop)) {
      this.subscribers.set(prop, new Set());
    }
    this.subscribers.get(prop)!.add(this.activeEffect);
  }

  trigger(prop: string | symbol): void {
    this.subscribers.get(prop)?.forEach(fn => fn());
  }

  effect(fn: Subscriber): void {
    this.activeEffect = fn;
    fn(); // Run to collect dependencies
    this.activeEffect = null;
  }

  createReactive<T extends object>(obj: T): T {
    return new Proxy(obj, {
      get: (target, prop, receiver) => {
        this.track(prop);
        return Reflect.get(target, prop, receiver);
      },
      set: (target, prop, value, receiver) => {
        const result = Reflect.set(target, prop, value, receiver);
        this.trigger(prop);
        return result;
      },
    });
  }
}

// Usage
const reactive = new ReactiveSystem();
const state = reactive.createReactive({ count: 0, name: 'Reactive' });

reactive.effect(() => {
  console.log(`Count changed to: ${state.count}`);
});

state.count = 1; // Logs: "Count changed to: 1"
state.count = 2; // Logs: "Count changed to: 2"
```

### Logging Proxy

```typescript
function createLoggingProxy<T extends object>(obj: T, name: string = 'target'): T {
  return new Proxy(obj, {
    get(target, prop, receiver) {
      const value = Reflect.get(target, prop, receiver);

      // Log function calls
      if (typeof value === 'function') {
        return function(this: unknown, ...args: unknown[]) {
          console.log(`[${name}] Calling ${String(prop)}(${args.map(a => JSON.stringify(a)).join(', ')})`);
          const result = value.apply(this, args);
          console.log(`[${name}] ${String(prop)} returned:`, result);
          return result;
        };
      }

      console.log(`[${name}] Accessing ${String(prop)} →`, value);
      return value;
    },

    set(target, prop, value, receiver) {
      const oldValue = target[prop as keyof typeof target];
      const result = Reflect.set(target, prop, value, receiver);
      console.log(`[${name}] ${String(prop)}: ${JSON.stringify(oldValue)} → ${JSON.stringify(value)}`);
      return result;
    },
  });
}

const obj = { x: 10, y: 20, sum() { return this.x + this.y; } };
const logged = createLoggingProxy(obj, 'math');
logged.x;       // Logs: [math] Accessing x → 10
logged.sum();   // Logs: [math] Calling sum() → [math] sum returned: 30
```

### Read-Only Proxy

```typescript
function readonly<T extends object>(obj: T): Readonly<T> {
  return new Proxy(obj, {
    set(_target, prop, _value, _receiver) {
      throw new Error(`Cannot assign to read-only property '${String(prop)}'`);
    },
    deleteProperty(_target, prop) {
      throw new Error(`Cannot delete read-only property '${String(prop)}'`);
    },
    defineProperty(_target, prop) {
      throw new Error(`Cannot define property on read-only object '${String(prop)}'`);
    },
  });
}

const config = readonly({ apiKey: 'secret123', endpoint: 'https://api.example.com' });
// config.apiKey = 'new'; // Error: Cannot assign to read-only property 'apiKey'
```

### Property Defaults with Proxy

```typescript
function withDefaults<T extends object>(obj: T, defaults: Partial<T>): T {
  return new Proxy(obj, {
    get(target, prop, receiver) {
      if (prop in target) {
        return Reflect.get(target, prop, receiver);
      }
      // Return default value for missing properties
      return (defaults as Record<string, unknown>)[prop as string];
    },
  });
}

const settings = withDefaults(
  { theme: 'dark' },
  { theme: 'light', fontSize: 14, language: 'en' }
);

console.log(settings.theme);    // 'dark' (from object)
console.log(settings.fontSize); // 14 (from defaults)
console.log(settings.language); // 'en' (from defaults)
```

### Negating Array Index with Proxy

```typescript
// Support negative indices like Python: arr[-1] returns last element
function negativeIndexArray<T>(arr: T[]): T[] {
  return new Proxy(arr, {
    get(target, prop, receiver) {
      if (typeof prop === 'string' && /^-?\d+$/.test(prop)) {
        const index = parseInt(prop, 10);
        if (index < 0) {
          // Convert negative index to positive
          prop = String(target.length + index);
        }
      }
      return Reflect.get(target, prop, receiver);
    },
  });
}

const arr = negativeIndexArray([10, 20, 30, 40]);
console.log(arr[-1]); // 40 (last element)
console.log(arr[-2]); // 30 (second to last)
```

### Reflect API

```typescript
// Reflect provides methods for all Proxy traps
const obj = { a: 1, b: 2 };

// Instead of: prop in obj
console.log(Reflect.has(obj, 'a')); // true

// Instead of: delete obj.a
console.log(Reflect.deleteProperty(obj, 'b')); // true

// Instead of: Object.keys(obj)
console.log(Reflect.ownKeys(obj)); // ['a']

// Safer property access
const result = Reflect.get(obj, 'c', undefined);
console.log(result); // undefined (no error)

// Construct with variable args
class MyClass {
  constructor(public x: number, public y: number) {}
}
const instance = Reflect.construct(MyClass, [10, 20]);
```

## Real-World Use Cases

### 1. API Client with Metrics

```typescript
function createInstrumentedAPI<T extends Record<string, Function>>(api: T): T {
  const metrics = new Map<string, { calls: number; totalTime: number }>();

  // Expose metrics
  (api as any).getMetrics = () => Object.fromEntries(metrics);

  return new Proxy(api, {
    apply(target, thisArg, args) {
      // ...instrumentation logic
      return Reflect.apply(target, thisArg, args);
    },
    get(target, prop, receiver) {
      const value = Reflect.get(target, prop, receiver);
      if (typeof value !== 'function') return value;

      return function(this: unknown, ...args: unknown[]) {
        const start = performance.now();
        try {
          return value.apply(this, args);
        } finally {
          const duration = performance.now() - start;
          if (!metrics.has(prop as string)) {
            metrics.set(prop as string, { calls: 0, totalTime: 0 });
          }
          const m = metrics.get(prop as string)!;
          m.calls++;
          m.totalTime += duration;
        }
      };
    },
  });
}
```

### 2. Form State Validation

```typescript
function createFormState<T extends Record<string, unknown>>(initial: T) {
  return new Proxy(initial, {
    set(target, prop, value, receiver) {
      // Trim strings
      if (typeof value === 'string') {
        value = value.trim();
      }
      return Reflect.set(target, prop, value, receiver);
    },
  });
}
```

## Common Mistakes

### 1. Proxying Primitives

```typescript
// ❌ BAD: Proxy requires an object target
// new Proxy(42, {}); // TypeError: Cannot create proxy with a non-object

// ✅ GOOD: Wrap in object
new Proxy(new Number(42), {});
```

### 2. Forgetting to Return from `set` Trap

```typescript
// ❌ BAD: set trap returns undefined (falsy)
const bad = new Proxy({}, {
  set(target, prop, value) {
    target[prop as keyof typeof target] = value;
    // Missing return — strict mode throws TypeError
  },
});

// ✅ GOOD: Return true for successful set
const good = new Proxy({}, {
  set(target, prop, value, receiver) {
    return Reflect.set(target, prop, value, receiver);
  },
});
```

## Best Practices

1. **Always use `Reflect` methods** inside traps — they provide correct `this` binding and return values

2. **Return proper values** from traps (`set` → boolean, `deleteProperty` → boolean, `get` → value)

3. **Revocable proxies** for temporary access — use `Proxy.revocable()` for security-sensitive scenarios

4. **Don't overuse** — proxies add overhead; use them where interception adds clear value

5. **Compose proxies** — wrap proxies around proxies for layered behavior

## Performance Considerations

- **Proxy overhead**: Each intercepted operation is ~50-100x slower than direct access
- **Hot path caution**: Avoid proxies in performance-critical loops
- **Revocable proxies**: `Proxy.revocable()` enables clean teardown
- **Memory**: Proxy creates a new wrapper object; the target remains unmodified
- **V8 optimization**: Proxies can prevent V8's inline caching optimizations

## Summary

Proxy and Reflect are powerful metaprogramming tools in JavaScript. Proxy wraps an object to intercept operations via handler traps, while Reflect provides default implementations for those traps. Used together, they enable validation, reactivity, logging, access control, and virtualization patterns. Use them judiciously — they add flexibility but incur performance overhead.

## Cheat Sheet

```text
PROXY CHEAT SHEET
═══════════════════════════════════════

CONSTRUCTION:
const proxy = new Proxy(target, handler);

TRAPS:
get, set, has, deleteProperty, ownKeys
apply, construct
getPrototypeOf, setPrototypeOf
defineProperty, getOwnPropertyDescriptor
preventExtensions, isExtensible

REFLECT METHODS:
Reflect.get(obj, prop, receiver)
Reflect.set(obj, prop, value, receiver)
Reflect.has(obj, prop)
Reflect.deleteProperty(obj, prop)
Reflect.ownKeys(obj)
Reflect.apply(fn, thisArg, args)
Reflect.construct(Ctor, args)

BEST PRACTICES:
• Use Reflect inside traps
• Return proper boolean values
• Proxy.revocable() for temporary access
• Don't proxy in hot paths
• Compose for layered behavior

REVOCABLE:
const { proxy, revoke } = Proxy.revocable(target, handler);
revoke(); // Disables all proxy operations

```

---

## See Also
- [Shallow vs Deep Copy](15-Shallow-vs-Deep-Copy.md)
- [Generators](23-Generators.md)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [MDN: Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
- [MDN: Reflect](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect)
- [MDN: Proxy Handler](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy/Proxy)
- [Vue 3 Reactivity System](https://vuejs.org/guide/extras/reactivity-in-depth.html)
