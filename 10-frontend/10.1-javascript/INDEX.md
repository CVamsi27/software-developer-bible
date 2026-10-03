# JavaScript — Index

> **Study time:** ≈ 7 h 20 m of reading (40 files, ~11 min average).
> **40 files** — Core JavaScript concepts from execution context to async patterns, memory management, functional patterns, modern ES2022+ APIs, cancellation, DOM events, cross-tab communication, and interview questions.

[![Files](https://img.shields.io/badge/files-40-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why this is non-negotiable:** Every frontend, Node.js, and full-stack interview tests JavaScript fundamentals. "What is a closure?" "Explain the event loop." "What does `this` bind to in an arrow function?" — these come up at every level. Senior interviews go deeper: prototype chain internals, microtask queue, V8 GC, WeakRef, generators as iterators. This section covers it all.

---

## Topic Categories

The 33 files are organized into 6 category folders. Files in the same category build on each other — read them in order within a category, then move on.

| Category | Files | Why it matters |
| ------------------------------------------------------------------------ | ----: | -------------------------------------------------------------------------------------------- |
| [Execution & Scope](01-execution-and-scope/INDEX.md) | 6 | The "how JS runs" fundamentals — every interview tests these |
| [Objects, Prototypes & `this`](02-objects-prototypes-this/INDEX.md) | 3 | The OOP model of JavaScript — different from class-based languages |
| [Async & Concurrency](03-async-concurrency/INDEX.md) | 5 | The hardest topic in JS — the event loop, promises, async/await, cancellation |
| [Memory & Data](04-memory-and-data/INDEX.md) | 9 | Choosing the right collection, hash table internals, avoiding memory leaks, understanding GC |
| [Functional Patterns](05-functional-patterns/INDEX.md) | 5 | The patterns you'll use daily: currying, composition, memoization, generators |
| [Modern JS (ES2022+) & Interview Prep](06-modern-and-interview/INDEX.md) | 5 | The newest features, Web Workers, DOM events, cross-tab communication, and 50+ interview Qs |

---

## Study Flow

Read categories in numeric order — each builds on the previous:

```text
01-execution-and-scope ─▶ 02-objects-prototypes-this ─▶ 03-async-concurrency
    ─▶ 04-memory-and-data ─▶ 05-functional-patterns ─▶ 06-modern-and-interview
```

---

## ▶ Execution & Scope

How JavaScript actually runs. These 6 files are the foundation — every other concept builds on them.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Execution Context](01-execution-and-scope/10.1.1.01-execution-context.md) | GEC vs FEC, creation/execution phases, scope chain, hoisting internals | 4 min |
| 02 | [Scope](01-execution-and-scope/10.1.1.02-scope.md) | Global, function, block scope, scope chain, lexical environment | 5 min |
| 03 | [Call Stack](01-execution-and-scope/10.1.1.03-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | 5 min |
| 04 | [Hoisting](01-execution-and-scope/10.1.1.04-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | 7 min |
| 05 | [Lexical Environment](01-execution-and-scope/10.1.1.05-lexical-environment.md) | Environment records, outer reference, scope chain internals | 6 min |
| 06 | [Closures](01-execution-and-scope/10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | 5 min |

**Read order:** Execution Context → Scope → Call Stack → Hoisting → Lexical Environment → Closures (matches the category's numbering and its read-order rationale — see [01-execution-and-scope/INDEX.md](01-execution-and-scope/INDEX.md)).

---

## Objects, Prototypes & `this`

JavaScript's object model is prototype-based, not class-based. `this` binding is one of the most-confused topics in JS.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 07 | [`this` Keyword](02-objects-prototypes-this/10.1.2.01-this.md) | Implicit/explicit binding, arrow functions, `call`/`apply`/`bind` | 7 min |
| 08 | [Prototypes](02-objects-prototypes-this/10.1.2.02-prototypes.md) | Prototype chain, `__proto__`, `Object.create`, classical inheritance, `class` keyword | 7 min |
| 09 | [Proxy & Reflect](02-objects-prototypes-this/10.1.2.03-proxy-reflect.md) | Metaprogramming, traps, validation, reactive patterns (Vue 3 uses these!) | 8 min |

---

## Async & Concurrency

The most-asked topic in senior JS interviews. JavaScript is single-threaded; understanding how it handles concurrency is essential.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 10 | [Event Loop](03-async-concurrency/10.1.3.01-event-loop.md) | Microtasks vs macrotasks, callback queue, rendering pipeline, `requestAnimationFrame` | 6 min |
| 11 | [Promises](03-async-concurrency/10.1.3.02-promises.md) | Promise states, chaining, error handling, `Promise.all`/`race`/`allSettled`/`any` | 8 min |
| 12 | [Async/Await](03-async-concurrency/10.1.3.03-async-await.md) | Async functions, error handling, concurrency, sequential vs parallel, top-level await | 7 min |
| 13 | [Error Handling](03-async-concurrency/10.1.3.04-error-handling.md) | try/catch/finally, custom errors, error propagation, async error handling, unhandled rejections | 17 min |
| 14 | [Aborting & Cancellation](03-async-concurrency/10.1.3.05-abort-and-cancellation.md) | AbortController/AbortSignal, stale-request races, `AbortSignal.timeout`/`any`, listener cleanup, cooperative cancellation | 7 min |

**Read order:** Event Loop → Promises → Async/Await → Error Handling → Aborting & Cancellation. This is the most-asked cluster in interviews.

---

## Memory & Data

Choosing the right collection and avoiding memory leaks.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 15 | [Bounded Concurrency](03-async-concurrency/10.1.3.06-bounded-concurrency.md) | Worker pools, fail-fast vs collect-all, AbortSignal threading, p-limit | 12 min |
| 16 | [Pass by Value](04-memory-and-data/10.1.4.01-pass-by-value.md) | Primitive vs reference, value/reference semantics, mutation gotchas | 6 min |
| 17 | [Map, Set, WeakMap, WeakSet](04-memory-and-data/10.1.4.02-map-set-weakmap-weakset.md) | Keyed collections, weak references, memory-efficient lookups, when to use what | 15 min |
| 18 | [Shallow vs Deep Copy](04-memory-and-data/10.1.4.03-shallow-vs-deep-copy.md) | Spread, `Object.assign`, `structuredClone`, JSON methods, pitfalls | 14 min |
| 19 | [Debounce](04-memory-and-data/10.1.4.04-debounce.md) | Implementation, leading/trailing edge, real-world use cases (search input, resize) | 22 min |
| 20 | [Throttle](04-memory-and-data/10.1.4.05-throttle.md) | Implementation, vs debounce, animation frame throttling, scroll handlers | 21 min |
| 21 | [Memory Leaks](04-memory-and-data/10.1.4.06-memory-leaks.md) | Detached DOM, closures, circular references, detection, debugging | 21 min |
| 22 | [Garbage Collection](04-memory-and-data/10.1.4.07-garbage-collection.md) | Mark-and-sweep, generational collection, V8 Orinoco, WeakRef, FinalizationRegistry | 21 min |
| 23 | [Hash Tables & HashMaps](04-memory-and-data/10.1.4.08-hash-tables-internals.md) | Collision resolution, load factor, rehashing, V8 internals, Robin Hood, interview patterns | 27 min |
| 24 | [Equality & Coercion](04-memory-and-data/10.1.4.09-equality-and-coercion.md) | `==` vs `===`, ToNumber/ToPrimitive/truthiness, `??` vs `\|\|`, `Object.is`, deriving the classics | 9 min |

---

## Functional Patterns

The patterns you'll use daily as a senior engineer.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 25 | [Modules](05-functional-patterns/10.1.5.01-modules.md) | ESM vs CommonJS, dynamic imports, tree shaking, barrel exports | 19 min |
| 26 | [Memoization](05-functional-patterns/10.1.5.02-memoization.md) | Caching, `_.memoize`, React.memo, useMemo, when to use | 16 min |
| 27 | [Generators](05-functional-patterns/10.1.5.03-generators.md) | `function*`, yield, iterators, async generators, lazy evaluation | 21 min |
| 28 | [Currying & Composition](05-functional-patterns/10.1.5.04-currying-composition.md) | Currying, partial application, pipe, compose, functional patterns | 10 min |
| 29 | [Recursion & Tail Call](05-functional-patterns/10.1.5.05-recursion-tail-call.md) | Recursive patterns, tail call optimization, trampolining, memoized recursion | 12 min |

---

## Modern JS & Interview Prep

The newest features + the interview Q&A bank.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------    : |
| 30 | [ES2024+ Features](06-modern-and-interview/10.1.6.01-es2024-features.md) | `?.`/`??` syntax foundations (ES2020), `structuredClone`, `toSorted`, `Object.groupBy`, `Promise.withResolvers`, iterator helpers, Set methods (ES2025) | 13 min |
| 31 | [Web Workers](06-modern-and-interview/10.1.6.02-web-workers.md) | Dedicated/Shared workers, OffscreenCanvas, Comlink, React hooks for workers | 10 min |
| 32 | [DOM Events & Delegation](06-modern-and-interview/10.1.6.03-dom-events-delegation.md) | Capture/bubble phases, target vs currentTarget, delegation patterns, passive listeners, CustomEvent, React synthetic events | 16 min |
| 33 | [Cross-Tab Communication](06-modern-and-interview/10.1.6.04-cross-tab-communication.md) | BroadcastChannel, storage events, SharedWorker vs postMessage, localStorage mutex, sync logout, IndexedDB payloads, service-worker messaging | 14 min |
| 34 | [Interview Questions](06-modern-and-interview/10.1.6.05-interview-questions.md) | 55+ curated questions with answers | 10 min |

---

## Suggested Study Order

### Path A — New to JS (1-2 weeks)
1. Execution & Scope (all 6 files, ~2 hrs)
2. Async & Concurrency (5 files, ~2.5 hrs)
3. Memory & Data (9 files, ~2.75 hrs)
4. Objects, Prototypes & `this` (3 files, ~1.5 hrs)
5. Functional Patterns (5 files, ~2 hrs)
6. Interview Questions (review)

### Path B — Refresher for senior (1-2 days)
1. Event Loop + Promises + Async/Await (1 hr)
2. Prototypes + `this` (45 min)
3. Memory Leaks + Garbage Collection (45 min)
4. Interview Questions (focus on the 20+ harder Qs)

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- Read 50+ Interview Questions end-to-end
- Practice the top 10 most-asked questions out loud

---

## Cross-References

- [TypeScript](../10.2-typescript/INDEX.md) — type system builds on JS fundamentals
- [Node.js](../../20-backend/20.1-node.js/INDEX.md) — event loop, async patterns
- [React](../10.3-react/INDEX.md) — closures, `this`, hooks use these concepts
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — JS in algorithm implementations

---

## Navigation

[← Previous: Interview Strategy](../../00-strategy/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: TypeScript →](../10.2-typescript/INDEX.md)
