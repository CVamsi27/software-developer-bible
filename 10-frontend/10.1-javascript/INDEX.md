# JavaScript — Index

> **Study time:** ≈ 6 h 19 m of reading (40 files, ~9 min average).
> Core JavaScript concepts from execution context through async patterns, memory management, functional techniques, modern language APIs, cancellation, browser events, cross-tab coordination, and interview practice.

[![Files](https://img.shields.io/badge/files-40-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

JavaScript fundamentals commonly appear in frontend, Node.js, and full-stack interviews. Be ready to trace scope and promise behavior, explain object identity, and distinguish language rules from host/runtime behavior. The chapters and drills organize those topics; they are a study path, not a guarantee of interview coverage.

---

## Topic Categories

The numbered chapters are organized into six category folders. Files in the same category build on each other; follow each category's reading order, then use its revision companion before interview practice.

| Category | Files | Why it matters |
| ------------------------------------------------------------------------ | ----: | ----------------------------------------------------------------------------------------------- |
| [Execution & Scope](01-execution-and-scope/INDEX.md) | 6 | The language's binding, lookup, execution and lifetime model |
| [Objects, Prototypes & `this`](02-objects-prototypes-this/INDEX.md) | 3 | Property lookup, prototype links, method calls and `this` |
| [Async & Concurrency](03-async-concurrency/INDEX.md) | 6 | Event-loop scheduling, promises, async/await, cancellation and bounded work |
| [Memory & Data](04-memory-and-data/INDEX.md) | 9 | Choosing the right collection, hash table internals, avoiding memory leaks, understanding GC |
| [Functional Patterns](05-functional-patterns/INDEX.md) | 5 | The patterns you'll use daily: currying, composition, memoization, generators |
| [Modern JS & Interview Prep](06-modern-and-interview/INDEX.md) | 5 | Selected ES2022–2026 APIs, workers, DOM events, cross-tab coordination, and interview questions |

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

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Execution Context](01-execution-and-scope/10.1.1.01-execution-context.md) | Evaluation state, environment references, declaration setup, parameter bindings | Essential | Foundational | 9 min |
| 02 | [Scope](01-execution-and-scope/10.1.1.02-scope.md) | Binding lookup, block boundaries, global/module scopes | Essential | Foundational | 6 min |
| 03 | [Call Stack](01-execution-and-scope/10.1.1.03-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | Essential | Foundational | 6 min |
| 04 | [Hoisting](01-execution-and-scope/10.1.1.04-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | Essential | Foundational | 7 min |
| 05 | [Lexical Environment](01-execution-and-scope/10.1.1.05-lexical-environment.md) | Record hierarchy, outer lookup, global object versus module bindings | Essential | Foundational | 15 min |
| 06 | [Closures](01-execution-and-scope/10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | Essential | Foundational | 6 min |

**Read order:** Execution Context → Scope → Call Stack → Hoisting → Lexical Environment → Closures (matches the category's numbering and its read-order rationale — see [01-execution-and-scope/INDEX.md](01-execution-and-scope/INDEX.md)).

---

## Objects, Prototypes & `this`

JavaScript object properties resolve through prototype chains; class syntax builds on that model. The value of `this` depends on call form for ordinary functions and is lexical for arrows.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 07 | [`this` Keyword](02-objects-prototypes-this/10.1.2.01-this.md) | Implicit/explicit binding, arrow functions, `call`/`apply`/`bind` | Essential | Foundational | 8 min |
| 08 | [Prototypes](02-objects-prototypes-this/10.1.2.02-prototypes.md) | Prototype chain, `__proto__`, `Object.create`, inheritance and `class` syntax | Essential | Foundational | 8 min |
| 09 | [Proxy & Reflect](02-objects-prototypes-this/10.1.2.03-proxy-reflect.md) | Metaprogramming, traps, validation, reactive patterns (Vue 3 uses these!) | Important | Specialized | 9 min |

---

## Async & Concurrency

Async behavior is subtle and commonly tested. One agent runs one active synchronous evaluation at a time; host I/O and workers add concurrency. Trace completion order and cancellation ownership separately.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 10 | [Event Loop](03-async-concurrency/10.1.3.01-event-loop.md) | Microtasks vs macrotasks, callback queue, rendering pipeline, `requestAnimationFrame` | Essential | Foundational | 7 min |
| 11 | [Promises](03-async-concurrency/10.1.3.02-promises.md) | Promise states, chaining, error handling, `Promise.all`/`race`/`allSettled`/`any` | Essential | Foundational | 9 min |
| 12 | [Async/Await](03-async-concurrency/10.1.3.03-async-await.md) | Async functions, error handling, concurrency, sequential vs parallel, top-level await | Essential | Foundational | 8 min |
| 13 | [Error Handling](03-async-concurrency/10.1.3.04-error-handling.md) | try/catch/finally, custom errors, error propagation, async error handling, unhandled rejections | Essential | Foundational | 5 min |
| 14 | [Aborting & Cancellation](03-async-concurrency/10.1.3.05-abort-and-cancellation.md) | AbortController/AbortSignal, stale-request races, `AbortSignal.timeout`/`any`, listener cleanup, cooperative cancellation | Essential | Foundational | 8 min |
| 15 | [Bounded Concurrency](03-async-concurrency/10.1.3.06-bounded-concurrency.md) | Worker-pool ownership, failure and cancellation | Essential | Foundational | 8 min |

**Read order:** Event Loop → Promises → Async/Await → Error Handling → Aborting & Cancellation → Bounded Concurrency. Together, these chapters explain scheduling, failure, cancellation and limits on parallel work.

---

## Memory & Data

Choosing the right collection and avoiding memory leaks.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 16 | [Pass by Value](04-memory-and-data/10.1.4.01-pass-by-value.md) | Primitive vs reference, value/reference semantics, mutation gotchas | Essential | Foundational | 6 min |
| 17 | [Map, Set, WeakMap, WeakSet](04-memory-and-data/10.1.4.02-map-set-weakmap-weakset.md) | Key identity and order, weak metadata, conversion, bounded eviction | Essential | Foundational | 7 min |
| 18 | [Shallow vs Deep Copy](04-memory-and-data/10.1.4.03-shallow-vs-deep-copy.md) | Reference graphs, structured cloning, transfer, JSON boundary, path copying | Essential | Foundational | 6 min |
| 19 | [Debounce](04-memory-and-data/10.1.4.04-debounce.md) | Quiet-time scheduling, edge policies, cancellation, stale async results | Essential | Foundational | 6 min |
| 20 | [Throttle](04-memory-and-data/10.1.4.05-throttle.md) | Periodic scheduling, edge policies, cancellation, concurrency boundaries | Essential | Foundational | 6 min |
| 21 | [Memory Leaks](04-memory-and-data/10.1.4.06-memory-leaks.md) | Retaining paths, cleanup ownership, bounded caches, heap diagnosis | Essential | Foundational | 5 min |
| 22 | [Garbage Collection](04-memory-and-data/10.1.4.07-garbage-collection.md) | Tracing, generations, scheduling, weak references, process memory | Essential | Foundational | 4 min |
| 23 | [Hash Tables & HashMaps](04-memory-and-data/10.1.4.08-hash-tables-internals.md) | Collision resolution, load factor, rehashing, V8 internals, Robin Hood, interview patterns | Important | Specialized | 30 min |
| 24 | [Equality & Coercion](04-memory-and-data/10.1.4.09-equality-and-coercion.md) | Equality, object-to-primitive conversion, truthiness, nullish defaults | Essential | Foundational | 5 min |

---

## Functional Patterns

Patterns for explicit data flow, reusable computations, lazy iteration and function composition.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 25 | [Modules](05-functional-patterns/10.1.5.01-modules.md) | ESM vs CommonJS, dynamic imports, tree shaking, barrel exports | Essential | Foundational | 19 min |
| 26 | [Memoization](05-functional-patterns/10.1.5.02-memoization.md) | Caching, `_.memoize`, React.memo, useMemo, when to use | Essential | Foundational | 14 min |
| 27 | [Generators](05-functional-patterns/10.1.5.03-generators.md) | `function*`, yield, iterators, async generators, lazy evaluation | Important | Specialized | 17 min |
| 28 | [Currying & Composition](05-functional-patterns/10.1.5.04-currying-composition.md) | Currying, partial application, pipe, compose, functional patterns | Important | Specialized | 13 min |
| 29 | [Recursion & Tail Call](05-functional-patterns/10.1.5.05-recursion-tail-call.md) | Recursive patterns, tail call optimization, trampolining, memoized recursion | Important | Specialized | 15 min |

---

## Modern JS & Interview Prep

Selected recent APIs, browser execution/event models and interview practice.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------    : |
| 30 | [Recent ECMAScript Features](06-modern-and-interview/10.1.6.01-es2024-features.md) | Selected ES2022–2026 APIs; distinguish language features from host APIs and runtime support | Important | Specialized | 18 min |
| 31 | [Web Workers](06-modern-and-interview/10.1.6.02-web-workers.md) | Dedicated/Shared workers, OffscreenCanvas, Comlink, React hooks for workers | Important | Important | 11 min |
| 32 | [DOM Events & Delegation](06-modern-and-interview/10.1.6.03-dom-events-delegation.md) | Capture/bubble phases, target vs currentTarget, delegation patterns, passive listeners, CustomEvent, React synthetic events | Essential | Foundational | 13 min |
| 33 | [Cross-Tab Communication](06-modern-and-interview/10.1.6.04-cross-tab-communication.md) | BroadcastChannel, storage events, SharedWorker vs postMessage, non-atomic storage races and Web Locks, sync logout, IndexedDB payloads, service-worker messaging | Important | Specialized | 16 min |
| 34 | [Interview Questions](06-modern-and-interview/10.1.6.05-interview-questions.md) | 62 questions with model answers, implementation prompts and changed-condition checks | Essential | Foundational | 12 min |

---

## Suggested Study Order

### Path A — New to JS (1-2 weeks)
1. Execution & Scope (all 6 files, ~2 hrs)
2. Async & Concurrency (5 files, ~2.5 hrs)
3. Memory & Data (9 files, ~2.75 hrs)
4. Objects, Prototypes & `this` (3 files, ~1.5 hrs)
5. Functional Patterns (5 files, ~2 hrs)
6. Category revision → Interview Questions (explain traces and changed conditions)

### Path B — Refresher for senior (1-2 days)
1. Event Loop + Promises + Async/Await (1 hr)
2. Prototypes + `this` (45 min)
3. Memory Leaks + Garbage Collection (45 min)
4. Interview Questions (focus on the 20+ harder Qs)

### Path C — Interview tomorrow
- Read each chapter's definition and summary
- Use each category REVISION, then the Interview Questions bank
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
