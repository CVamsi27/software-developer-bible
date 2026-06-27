# JavaScript Cheat Sheet

## Quick Reference Table

| Concept | Key Point | Code/Example |
|---------|-----------|--------------|
| Execution Context | Global + Function + Eval. Created in 2 phases: Creation (hoisting) then Execution | `this` is set during creation phase |
| Lexical Environment | Scope chain; each context has a reference to its outer environment | Inner functions access outer vars via [[Environment]] |
| Hoisting | `var` → undefined; `function` → fully hoisted; `let`/`const` → TDZ | `console.log(a); var a = 5;` → `undefined` |
| Temporal Dead Zone | `let`/`const` exist but are inaccessible before declaration | `let x = 1;` — x is in TDZ until this line runs |
| Closures | Function + its lexical environment; retains access to outer scope variables | `const counter = () => { let n = 0; return () => ++n; }` |
| `this` — Global | `this === window` (non-strict) or `undefined` (strict) | `this` outside any function = `window` |
| `this` — Method | `this` = the object that owns the method | `obj.method()` → `this === obj` |
| `this` — Function | `this` = `window` (non-strict) or `undefined` (strict) — not the caller | `const fn = obj.method; fn();` → `this === window` |
| `this` — Arrow | Inherits `this` from enclosing lexical scope; cannot be rebound | `const fn = () => this` |
| `this` — `new` | `this` = newly created object | `new Foo()` → `this === new Foo()` |
| `this` — `call/apply/bind` | Explicitly set `this`; `bind` returns a new function | `fn.call(obj, arg1)` / `fn.apply(obj, [args])` |
| Prototypes | Every object has `__proto__`; methods live on prototype for shared access | `Object.getPrototypeOf(obj)` |
| Prototypal Inheritance | `Child.__proto__ === Parent`; method lookup walks the chain | `obj.toString()` walks up to `Object.prototype` |
| `class` sugar | Syntactic sugar over prototypes + `new`; `extends` sets prototype chain | `class Dog extends Animal {}` |
| Event Loop | Call Stack → Microtask Queue → Macrotask Queue | Promises are microtasks; setTimeout is macrotask |
| Microtasks | `Promise.then`, `Promise.catch`, `queueMicrotask`, `MutationObserver` | Run BEFORE next macrotask |
| Macrotasks | `setTimeout`, `setInterval`, `setImmediate`, I/O, UI rendering | One per event loop tick |
| Promises | `pending → fulfilled/rejected`; chain with `.then().catch()` | `fetch(url).then(r => r.json())` |
| `async/await` | Syntactic sugar over Promises; `await` pauses until settled | `const data = await fetch(url).then(r => r.json())` |
| Promise.all | Fulfills when ALL promises fulfill; rejects on FIRST rejection | `await Promise.all([p1, p2, p3])` |
| Promise.allSettled | Always resolves; returns `{status, value/reason}` for each | `await Promise.allSettled([p1, p2])` |
| Promise.race | Settles with FIRST settled promise (fulfill or reject) | `await Promise.race([p1, p2])` |
| Promise.any | Fulfills with FIRST fulfilled; rejects if ALL reject (AggregateError) | `await Promise.any([p1, p2])` |
| IIFE | Immediately Invoked Function Expression; creates a scope | `(function() { var x = 1; })()` |
| Module — ES | `import/export` — static, tree-shakeable, top-level await | `import { fn } from './mod.js'` |
| Module — CJS | `require/module.exports` — dynamic, synchronous | `const mod = require('./mod')` |
| WeakRef/DWeakMap | Weak references don't prevent GC; key can be GC'd | `new WeakMap()` — keys must be objects |
| Memory Leak | Forgotten timers, unclosed listeners, growing arrays, closures holding refs | Use `--inspect` Chrome DevTools Memory tab |
| GC Mark-and-Sweep | Reachable from root = live; unreachable = collectable | `global` → stack → closures = roots |
| Typed Arrays | `ArrayBuffer`, `Uint8Array`, `Float32Array` — binary data views | `new ArrayBuffer(16)` + `new Uint8Array(buf)` |
| Proxy/Reflect | Intercept operations on objects (get, set, has, deleteProperty) | `new Proxy(target, handler)` |
| Symbol | Unique, immutable identifier; used as object keys | `const id = Symbol('id'); obj[id] = 123` |
| Iterators | `{ next() → { value, done } }` — protocol for `for...of` | `[Symbol.iterator]` method on iterable |
| Generators | `function*` — lazy evaluation, yield values one at a time | `function* range() { yield 1; yield 2; }` |
| Destructuring | Extract values from arrays/objects; supports defaults | `const { name, age = 25 } = person` |
| Spread/Rest | `...` — expand (spread) or collect (rest) | `[...arr]` / `function(...args) {}` |
| Optional Chaining | `?.` — short-circuits if null/undefined | `user?.address?.city` |
| Nullish Coalescing | `??` — returns right side only if left is null/undefined | `val ?? 'default'` (NOT `0` or `''`) |
| Template Literals | Backticks — interpolation, multiline, tagged | `` `Hello ${name}` `` |
| Coercion | `==` does type coercion; `===` does not | `0 == '' → true`, `0 === '' → false` |
| `typeof` | Returns `"undefined"`, `"boolean"`, `"number"`, `"string"`, `"object"`, `"function"`, `"symbol"`, `"bigint"` | `typeof null === "object"` (bug) |
| `instanceof` | Checks prototype chain | `arr instanceof Array → true` |
| Error Handling | `try/catch/finally`; custom errors extend `Error` | `class AppError extends Error {}` |
| Map/Set | `Map` — key-value (any key type); `Set` — unique values | `new Map([['a', 1]])` / `new Set([1,2,3])` |
| Object.freeze | Shallow freeze; immutable at top level | `Object.freeze(obj)` — nested still mutable |
| Structured Clone | Deep copy (handles dates, regex, Map, Set) | `structuredClone(obj)` |
| Event Delegation | Attach listener to parent; use `e.target` to find actual element | Faster for many children |
| Debounce | Wait until delay passes since last call | Search input after user stops typing |
| Throttle | Execute at most once per interval | Scroll event handler |
| Currying | `f(a)(b)(c)` — transform multi-arg into chain of single-arg | `const add = a => b => a + b` |
| Composition | `f(g(x))` — combine functions | `const compose = (f, g) => x => f(g(x))` |
| Immutability | New values instead of mutation; spread + map/filter/reduce | `const next = [...arr, newItem]` |

## Top 10 Things to Remember

1. **Execution Contexts have two phases**: Creation (hoisting, variable initialization) and Execution (actual code runs). This explains why `var` is `undefined` before declaration but `let`/`const` throw.

2. **`this` is determined at call time, not definition time** — except arrow functions which inherit lexically. This is the #1 source of confusion.

3. **The Event Loop processes ALL microtasks before ANY macrotask**. `Promise.then` always runs before `setTimeout(..., 0)`. Priority: microtasks > macrotasks.

4. **Closures capture references, not values**. A `for` loop with `var` captures the same variable reference in each iteration — classic bug.

5. **Prototypes are objects**. Every function has a `.prototype` property; every object has a `[[Prototype]]` link. `class` is sugar over this.

6. **`==` performs type coercion**, `===` checks type AND value. Use `===` always unless you specifically want coercion.

7. **Modules (ES) are hoisted and static**. You can't conditionally `import`. Use dynamic `import()` for code splitting.

8. **WeakRef/WeakMap don't prevent garbage collection**. Keys can be collected even if referenced by WeakMap — useful for caches and metadata.

9. **`typeof null === "object"`** is a historical bug. Always check `value === null` explicitly.

10. **Generators are lazy**. They produce values on demand, making them ideal for large sequences, infinite streams, or async control flow (sagas).

## Common Patterns

### Module Pattern (IIFE)
```js
const Module = (function() {
  let private = 0;
  return {
    increment() { private++; },
    getCount() { return private; }
  };
})();
```

### Observer Pattern (Pub/Sub)
```js
class EventEmitter {
  constructor() { this.events = {}; }
  on(event, fn) {
    (this.events[event] = this.events[event] || []).push(fn);
    return () => this.off(event, fn);
  }
  off(event, fn) {
    this.events[event] = this.events[event]?.filter(f => f !== fn);
  }
  emit(event, ...args) {
    this.events[event]?.forEach(fn => fn(...args));
  }
}
```

### Currying
```js
const curry = (fn) => {
  const arity = fn.length;
  return function curried(...args) {
    if (args.length >= arity) return fn(...args);
    return (...moreArgs) => curried(...args, ...moreArgs);
  };
};
const add = curry((a, b, c) => a + b + c);
add(1)(2)(3); // 6
add(1, 2)(3); // 6
```

### Memoization
```js
const memo = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
```

### Debounce / Throttle
```js
const debounce = (fn, ms) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
};
const throttle = (fn, ms) => {
  let last = 0;
  return (...args) => {
    const now = Date.now();
    if (now - last >= ms) { last = now; fn(...args); }
  };
};
```

### Promise Retry
```js
const retry = (fn, maxRetries, delay) =>
  fn().catch(err => maxRetries > 0
    ? new Promise(r => setTimeout(r, delay)).then(() => retry(fn, maxRetries - 1, delay))
    : Promise.reject(err));
```

### Object Pool (Memory Management)
```js
class ObjectPool {
  constructor(create, reset, maxSize) {
    this.create = create; this.reset = reset;
    this.pool = []; this.maxSize = maxSize;
  }
  acquire() {
    return this.pool.length ? this.reset(this.pool.pop()) : this.create();
  }
  release(obj) {
    if (this.pool.length < this.maxSize) this.pool.push(obj);
  }
}
```

### Iterator / Generator Pattern
```js
function* fibonacci() {
  let [a, b] = [0, 1];
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}
const take = (gen, n) => [...Array(n)].map(() => gen.next().value);
take(fibonacci(), 10); // [0,1,1,2,3,5,8,13,21,34]
```

### Proxy Validation
```js
const validated = (obj, schema) => new Proxy(obj, {
  set(target, prop, value) {
    if (schema[prop] && !schema[prop](value)) {
      throw new TypeError(`Invalid value for ${prop}: ${value}`);
    }
    return Reflect.set(target, prop, value);
  }
});
```

## Red Flags (Things NOT to Say)

- **"Closures are slow"** — They're a fundamental feature, not an optimization concern. Say: "Closures retain references to lexical scope variables."
- **"Arrow functions are always better"** — They can't be constructors, don't have their own `this`, and can't be generators.
- **"var is fine, I use it sometimes"** — Shows outdated habits. Always prefer `const` (default), then `let` when reassignment is needed.
- **"I use `==` for simplicity"** — Shows lack of understanding. Use `===` unless you specifically need coercion.
- **"Prototypes are confusing, I just use classes"** — Shows shallow understanding. `class` IS prototypes underneath.
- **"setTimeout(fn, 0) runs immediately"** — It runs after the current call stack and all microtasks clear.
- **"async/await is completely different from Promises"** — It's syntactic sugar over Promises; `await` is just `.then()`.
- **"Deep clone with JSON.parse(JSON.stringify(obj))"** — Fails on dates, functions, undefined, circular refs, Maps, Sets, etc. Use `structuredClone()`.
- **"JavaScript is single-threaded"** — The event loop is single-threaded, but Web Workers and Node worker_threads provide actual parallelism.
- **"Garbage collection never causes pauses"** — Modern GC is great, but large heaps and object churn can cause measurable pauses.

## Green Flags (Things TO Say)

- **"Event Loop: microtasks run before macrotasks each tick."** — Shows deep understanding of async behavior.
- **"Closures capture references, not values, which can cause bugs in loops with `var`."** — Classic insight, shows practical experience.
- **"I use `const` by default, `let` when reassignment is needed, and avoid `var` entirely."** — Modern best practice.
- **"Arrow functions inherit `this` lexically; regular functions get `this` from the caller."** — Key distinction.
- **"WeakMap/WeakRef allow garbage collection of keys, preventing memory leaks in caches."** — Shows awareness of memory management.
- **"I prefer `Promise.allSettled` over `Promise.all` for independent operations to avoid fail-fast behavior."** — Practical production knowledge.
- **"Proxy and Reflect enable metaprogramming patterns like validation and reactive systems."** — Advanced awareness.
- **"Generators are great for lazy evaluation and implementing iterators/sagas."** — Shows depth beyond basic JS.
- **"Tree-shaking requires ES modules because they're statically analyzable."** — Connects module format to build tooling.
- **"I use `structuredClone` for deep copies — it handles dates, regex, and circular references."** — Shows awareness of modern APIs.

## 5-Minute Pre-Interview Review

- **Execution Context**: Creation phase (hoisting) → Execution phase. `this` assigned during creation.
- **Closures**: Function retains access to its outer lexical scope even after outer function returns.
- **Event Loop**: Call stack → microtasks (`Promise.then`) → macrotasks (`setTimeout`). ALL microtasks before ANY macrotask.
- **`this` binding rules**: `new` > `call/apply/bind` > method call > default (`window`/`undefined`). Arrow = lexical.
- **Prototypes**: `Object.getPrototypeOf(obj)` gets the prototype. `__proto__` is deprecated. Prototype chain: child → parent → Object.prototype → null.
- **Hoisting**: `var` → undefined, `function` → full definition, `let`/`const` → TDZ (access throws ReferenceError).
- **Promises**: `pending → fulfilled/rejected`. `.then()` returns new Promise. `.catch()` catches all previous rejections.
- **Modules**: ES modules are static (`import` at top), CJS is dynamic (`require` can be conditional). ES modules are always in strict mode.
- **Memory**: Avoid global variables, forgotten timers, unremoved event listeners, and closures holding large objects. Use WeakMap for metadata.
- **Key operators**: `??` (nullish), `?.` (optional chaining), `...` (spread/rest), `typeof` (but `typeof null === "object"`).

---

## References & Learn More
- [Cheat Sheet Collection](https://github.com/detailyang/awesome-cheatsheet)
- [DevHints](https://devhints.io/)
- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
