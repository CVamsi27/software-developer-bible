# JavaScript — Index

> **Study time:** ≈ 6 h 2 m of reading (42 files, ~9 min average).
> Core JavaScript concepts from execution context through async patterns, memory management, functional techniques, modern language APIs, cancellation, browser events, cross-tab coordination, and interview practice.

[![Files](https://img.shields.io/badge/files-42-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

JavaScript fundamentals commonly appear in frontend, Node.js, and full-stack interviews. Be ready to trace scope and promise behavior, explain object identity, and distinguish language rules from host/runtime behavior. The chapters and drills organize those topics; they are a study path, not a guarantee of interview coverage.

---

## Topic Categories

The numbered chapters are organized into six category folders. Files in the same category build on each other; follow each category's reading order, then use its revision companion before interview practice.

| Category | Chapters | Why it matters |
| ------------------------------------------------------------------------ | -------: | -------------------------------------------------------------------------------------------------------------------- |
| [Execution & Scope](01-execution-and-scope/INDEX.md) | 7 | The language's binding, lookup, execution and lifetime model |
| [Objects, Prototypes & `this`](02-objects-prototypes-this/INDEX.md) | 3 | Property lookup, prototype links, method calls and `this` |
| [Async & Concurrency](03-async-concurrency/INDEX.md) | 6 | Event-loop scheduling, promises, async/await, cancellation and bounded work |
| [Memory & Data](04-memory-and-data/INDEX.md) | 9 | Choosing the right collection, hash table internals, avoiding memory leaks, understanding GC |
| [Functional Patterns](05-functional-patterns/INDEX.md) | 5 | The patterns you'll use daily: currying, composition, memoization, generators |
| [Modern JS & Interview Prep](06-modern-and-interview/INDEX.md) | 6 | Selected ES2022–2026 APIs, workers, DOM events, cross-tab coordination, regular expressions, and interview questions |

The 36 chapters above plus the 6 revision companions make the 42 content files in the badge; section and category `INDEX.md` files are navigation, not counted.

---

## Study Flow

Read categories in numeric order — each builds on the previous:

```text
01-execution-and-scope ─▶ 02-objects-prototypes-this ─▶ 03-async-concurrency
    ─▶ 04-memory-and-data ─▶ 05-functional-patterns ─▶ 06-modern-and-interview
```

---

## ▶ Execution & Scope

Start with the language's evaluation and binding model, then distinguish it from the V8 implementation example.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Execution Context](01-execution-and-scope/10.1.1.01-execution-context.md) | Evaluation state, environment references, declaration setup, parameter bindings | Essential | Foundational | 7 min |
| 02 | [Scope](01-execution-and-scope/10.1.1.02-scope.md) | Binding lookup, block boundaries, global/module scopes | Essential | Foundational | 9 min |
| 03 | [Call Stack](01-execution-and-scope/10.1.1.03-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | Essential | Foundational | 7 min |
| 04 | [Hoisting](01-execution-and-scope/10.1.1.04-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | Essential | Foundational | 7 min |
| 05 | [Lexical Environment](01-execution-and-scope/10.1.1.05-lexical-environment.md) | Record hierarchy, outer lookup, global object versus module bindings | Essential | Foundational | 9 min |
| 06 | [Closures](01-execution-and-scope/10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | Essential | Foundational | 8 min |
| 07 | [V8 Execution and Optimization](01-execution-and-scope/10.1.1.07-v8-execution-and-optimization.md) | Pre-parsing, bytecode caching, JIT tiers, Smi and pointer compression, Hidden Classes, Elements Kinds, inline caches, closure contexts, OSR, and deoptimization | Important | Specialized | 15 min |

**Read order:** Execution Context → Scope → Call Stack → Hoisting → Lexical Environment → Closures → V8 execution and optimization (matches the category's numbering and its read-order rationale — see [01-execution-and-scope/INDEX.md](01-execution-and-scope/INDEX.md)).

---

## Objects, Prototypes & `this`

JavaScript object properties resolve through prototype chains; class syntax builds on that model. The value of `this` depends on call form for ordinary functions and is lexical for arrows.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [`this` Keyword](02-objects-prototypes-this/10.1.2.01-this.md) | Implicit and explicit binding, sloppy boxing, `.bind()` slots, arrow functions, callbacks, and construction | Essential | Foundational | 11 min |
| 09 | [Prototypes](02-objects-prototypes-this/10.1.2.02-prototypes.md) | Prototype chain, 4-step `new`, descriptors, `__proto__`, `Object.create`, `instanceof`, `class`, and pollution | Essential | Foundational | 11 min |
| 10 | [Proxy & Reflect](02-objects-prototypes-this/10.1.2.03-proxy-reflect.md) | Metaprogramming traps, receiver forwarding, invariants, internal slots, and lazy `WeakMap` wrapping | Important | Specialized | 11 min |

---

## Async & Concurrency

Async behavior is subtle and commonly tested. One agent runs one active synchronous evaluation at a time; host I/O and workers add concurrency. Trace completion order and cancellation ownership separately.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 11 | [Event Loop](03-async-concurrency/10.1.3.01-event-loop.md) | Synchronous tasks, microtask checkpoints, `MessageChannel` yielding, browser rendering, and Node host loop | Essential | Foundational | 10 min |
| 12 | [Promises](03-async-concurrency/10.1.3.02-promises.md) | Promise states, `[[PromiseIsHandled]]`, chaining, `Promise.withResolvers` and `Promise.try`, combinators, and deduplication | Essential | Foundational | 11 min |
| 13 | [Async/Await](03-async-concurrency/10.1.3.03-async-await.md) | Async suspension, `forEach(async)` pitfalls, Top-Level `await`, error boundaries, and payload validation | Essential | Foundational | 13 min |
| 14 | [Error Handling](03-async-concurrency/10.1.3.04-error-handling.md) | `try`, `catch`, and `finally`, `Error.isError`, `AggregateError`, `Error.cause`, JSON serialization, and retry boundaries | Essential | Foundational | 12 min |
| 15 | [Aborting & Cancellation](03-async-concurrency/10.1.3.05-abort-and-cancellation.md) | `AbortController` and `AbortSignal`, `AbortSignal.abort`, `{ signal }` teardown, stale-request guards, and limits | Essential | Foundational | 9 min |
| 16 | [Bounded Concurrency](03-async-concurrency/10.1.3.06-bounded-concurrency.md) | Start limits, fail-fast abort propagation or collect-all outcomes, cancellation, ordered results, and backpressure | Essential | Foundational | 10 min |

**Read order:** Event Loop → Promises → Async/Await → Error Handling → Aborting & Cancellation → Bounded Concurrency. Together, these chapters explain scheduling, failure, cancellation and limits on parallel work.

---

## Memory & Data

Choosing the right collection and avoiding memory leaks.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 17 | [Pass by Value](04-memory-and-data/10.1.4.01-pass-by-value.md) | Primitive vs. reference, call-by-sharing, shallow immutability (`freeze`/`seal`), and pure `toSorted` arrays | Essential | Foundational | 6 min |
| 18 | [Map, Set, WeakMap, WeakSet](04-memory-and-data/10.1.4.02-map-set-weakmap-weakset.md) | Key identity, insertion order, `getOrInsert` and `getOrInsertComputed`, set methods, and weak symbol boundaries | Essential | Foundational | 7 min |
| 19 | [Shallow vs Deep Copy](04-memory-and-data/10.1.4.03-shallow-vs-deep-copy.md) | Reference graphs, `structuredClone`, transferable buffers, JSON coercion limits, and path copying | Essential | Foundational | 7 min |
| 20 | [Debounce](04-memory-and-data/10.1.4.04-debounce.md) | Quiet-time scheduling, leading/trailing/maxWait policies, cancellation, and React lifecycle cleanup | Essential | Foundational | 11 min |
| 21 | [Throttle](04-memory-and-data/10.1.4.05-throttle.md) | Periodic scheduling, hybrid edge policies, `requestAnimationFrame` gating, cancellation, and concurrency limits | Essential | Foundational | 10 min |
| 22 | [Memory Leaks](04-memory-and-data/10.1.4.06-memory-leaks.md) | Retaining paths, `{ signal }` listener cleanup, bounded caches, DevTools retainers, and `v8.writeHeapSnapshot()` | Essential | Foundational | 8 min |
| 23 | [Garbage Collection](04-memory-and-data/10.1.4.07-garbage-collection.md) | Tracing, V8 spaces (`getHeapSpaceStatistics`), Orinoco, `WeakRef`, and ES2026 `using` deterministic disposal | Essential | Foundational | 7 min |
| 24 | [Hash Tables and Hash Maps](04-memory-and-data/10.1.4.08-hash-tables-internals.md) | Hash lookup, probing tombstones, object integer-key hoisting vs. `Map`, V8 `OrderedHashTable`, and resize pauses | Important | Specialized | 7 min |
| 25 | [Equality & Coercion](04-memory-and-data/10.1.4.09-equality-and-coercion.md) | Equality algorithms, `Symbol.toPrimitive`, `BigInt` rules, `??`, and explicit string/boolean boundary parsing | Essential | Foundational | 8 min |

---

## Functional Patterns

Patterns for explicit data flow, reusable computations, lazy iteration and function composition.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 26 | [Modules](05-functional-patterns/10.1.5.01-modules.md) | ESM versus CommonJS live bindings, dual-package hazard, `"exports"` map, `import.meta.dirname`, and tree shaking | Essential | Foundational | 7 min |
| 27 | [Memoization](05-functional-patterns/10.1.5.02-memoization.md) | Key equivalence, JSON key traps, bounded LRU and TTL retention, promises, and React memoization | Essential | Foundational | 8 min |
| 28 | [Generators](05-functional-patterns/10.1.5.03-generators.md) | Protocol keys, `Iterator.from` helpers, `yield*` delegation, async pages, and `finally` cleanup | Important | Specialized | 9 min |
| 29 | [Currying & Composition](05-functional-patterns/10.1.5.04-currying-composition.md) | Currying versus partial application, `Function.length`, `pipe` and `pipeAsync`, and handler factories | Important | Specialized | 5 min |
| 30 | [Recursion & Tail Calls](05-functional-patterns/10.1.5.05-recursion-tail-call.md) | Base cases, proper tail calls, trampolines, explicit cycle-safe stacks, and `BigInt` bottom-up DP | Important | Specialized | 6 min |

---

## Modern JS & Interview Prep

Selected recent APIs, browser execution/event models and interview practice.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 31 | [Recent ECMAScript Features](06-modern-and-interview/10.1.6.01-es2024-features.md) | Selected ES2022–2026 built-ins; compare ownership, evaluation, and runtime support | Important | Specialized | 8 min |
| 32 | [Web Workers](06-modern-and-interview/10.1.6.02-web-workers.md) | Dedicated, shared, and service workers; message ownership and cancellation limits | Important | Important | 7 min |
| 33 | [DOM Events & Delegation](06-modern-and-interview/10.1.6.03-dom-events-delegation.md) | Event path, target and listener ownership, delegation, propagation, default actions, and cleanup | Essential | Foundational | 6 min |
| 34 | [Cross-Tab Communication](06-modern-and-interview/10.1.6.04-cross-tab-communication.md) | Transient messages, persistent recovery, shared owners, locks, and safe cross-tab session updates | Important | Specialized | 7 min |
| 35 | [Regular Expressions and Text Matching](06-modern-and-interview/10.1.6.06-regexp-and-text.md) | Character classes, flags, `lastIndex` state, backtracking risk, Unicode and a redaction trace | Essential | Important | 9 min |
| 36 | [Interview Questions](06-modern-and-interview/10.1.6.05-interview-questions.md) | 74 questions with model answers, implementation prompts, and changed-condition checks | Essential | Foundational | 17 min |

---

## Suggested Study Order

### Path A — New to JS (1-2 weeks)
1. Execution & Scope: trace bindings, contexts and the engine-model boundary
2. Objects, Prototypes & `this`: trace receivers and descriptor lookup
3. Async & Concurrency: trace scheduling, cancellation and bounded work
4. Memory & Data: trace identity, copy policy and retention
5. Functional Patterns: explain module and computation ownership
6. Category revision → Interview Questions: explain traces and changed conditions

### Path B — Refresher for senior (1-2 days)
1. Event Loop + Promises + Async/Await (1 hr)
2. Prototypes + `this` (45 min)
3. Memory Leaks + Garbage Collection (45 min)
4. Interview Questions (focus on the 20+ harder Qs)

### Path C — Interview tomorrow
- Read each chapter's definition and summary
- Use each category `REVISION.md`, then the Interview Questions bank
- Practice scope, receiver, async and object-identity traces out loud

---

## Cross-References

- [TypeScript](../10.2-typescript/INDEX.md) — type system builds on JS fundamentals
- [Node.js](../../20-backend/20.1-node.js/INDEX.md) — event loop, async patterns
- [React](../10.3-react/INDEX.md) — closures, `this`, hooks use these concepts
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — JS in algorithm implementations

---

## Navigation

[← Previous: Interview Strategy](../../00-strategy/INDEX.md) · [Back to Index](../../INDEX.md) · [Next: TypeScript →](../10.2-typescript/INDEX.md)
