# JavaScript — Index

> **28 files** — Core JavaScript concepts from execution context to async patterns, memory management, functional patterns, modern ES2022+ APIs, and interview questions.

[![Files](https://img.shields.io/badge/files-28-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why this is non-negotiable:** Every frontend, Node.js, and full-stack interview tests JavaScript fundamentals. "What is a closure?" "Explain the event loop." "What does `this` bind to in an arrow function?" — these come up at every level. Senior interviews go deeper: prototype chain internals, microtask queue, V8 GC, WeakRef, generators as iterators. This section covers it all.

---

## 🗂️ Topic Categories

The 28 files are organized into 6 conceptual categories. Files in the same category build on each other — read them in order within a category, then move on.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Execution & Scope](#-execution--scope) | 6 | The "how JS runs" fundamentals — every interview tests these |
| [Objects, Prototypes & `this`](#-objects-prototypes--this) | 3 | The OOP model of JavaScript — different from class-based languages |
| [Async & Concurrency](#-async--concurrency) | 4 | The hardest topic in JS — the event loop, promises, async/await |
| [Data Structures & Memory](#-data-structures--memory) | 7 | Choosing the right collection, avoiding memory leaks, understanding GC |
| [Functional Patterns](#-functional-patterns) | 4 | The patterns you'll use daily: currying, composition, memoization, generators |
| [Modern JS (ES2022+) & Interview Prep](#-modern-js--interview-prep) | 4 | The newest features, Web Workers, and 50+ interview Qs |

---

## ▶ Execution & Scope

How JavaScript actually runs. These 6 files are the foundation — every other concept builds on them.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Execution Context](10.1.01-execution-context.md) | GEC vs FEC, creation/execution phases, scope chain, hoisting internals | 20 min |
| 02 | [Call Stack](10.1.02-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | 15 min |
| 03 | [Hoisting](10.1.03-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | 15 min |
| 04 | [Closures](10.1.04-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | 25 min |
| 05 | [Scope](10.1.05-scope.md) | Global, function, block scope, scope chain, lexical environment | 20 min |
| 06 | [Lexical Environment](10.1.06-lexical-environment.md) | Environment records, outer reference, scope chain internals | 15 min |

**Read order:** Execution Context → Scope → Lexical Environment → Hoisting → Closures → Call Stack.

---

## 🧬 Objects, Prototypes & `this`

JavaScript's object model is prototype-based, not class-based. `this` binding is one of the most-confused topics in JS.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 07 | [`this` Keyword](10.1.07-this.md) | Implicit/explicit binding, arrow functions, `call`/`apply`/`bind` | 25 min |
| 08 | [Prototypes](10.1.08-prototypes.md) | Prototype chain, `__proto__`, `Object.create`, classical inheritance, `class` keyword | 30 min |
| 16 | [Proxy & Reflect](10.1.16-proxy-reflect.md) | Metaprogramming, traps, validation, reactive patterns (Vue 3 uses these!) | 25 min |

---

## ⚡ Async & Concurrency

The most-asked topic in senior JS interviews. JavaScript is single-threaded; understanding how it handles concurrency is essential.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 09 | [Event Loop](10.1.09-event-loop.md) | Microtasks vs macrotasks, callback queue, rendering pipeline, `requestAnimationFrame` | 30 min |
| 10 | [Promises](10.1.10-promises.md) | Promise states, chaining, error handling, `Promise.all`/`race`/`allSettled`/`any` | 30 min |
| 11 | [Async/Await](10.1.11-async-await.md) | Async functions, error handling, concurrency, sequential vs parallel, top-level await | 25 min |
| 12 | [Error Handling](10.1.12-error-handling.md) | try/catch/finally, custom errors, error propagation, async error handling, unhandled rejections | 20 min |

**Read order:** Event Loop → Promises → Async/Await → Error Handling. This is the most-asked cluster in interviews.

---

## 📦 Data Structures & Memory

Choosing the right collection and avoiding memory leaks.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 13 | [Pass by Value](10.1.13-pass-by-value.md) | Primitive vs reference, value/reference semantics, mutation gotchas | 15 min |
| 14 | [Map, Set, WeakMap, WeakSet](10.1.14-map-set-weakmap-weakset.md) | Keyed collections, weak references, memory-efficient lookups, when to use what | 20 min |
| 15 | [Shallow vs Deep Copy](10.1.15-shallow-vs-deep-copy.md) | Spread, `Object.assign`, `structuredClone`, JSON methods, pitfalls | 20 min |
| 17 | [Debounce](10.1.17-debounce.md) | Implementation, leading/trailing edge, real-world use cases (search input, resize) | 15 min |
| 18 | [Throttle](10.1.18-throttle.md) | Implementation, vs debounce, animation frame throttling, scroll handlers | 15 min |
| 19 | [Memory Leaks](10.1.19-memory-leaks.md) | Detached DOM, closures, circular references, detection, debugging | 25 min |
| 20 | [Garbage Collection](10.1.20-garbage-collection.md) | Mark-and-sweep, generational collection, V8 Orinoco, WeakRef, FinalizationRegistry | 25 min |

---

## 🧮 Functional Patterns

The patterns you'll use daily as a senior engineer.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 21 | [Modules](10.1.21-modules.md) | ESM vs CommonJS, dynamic imports, tree shaking, barrel exports | 20 min |
| 22 | [Memoization](10.1.22-memoization.md) | Caching, `_.memoize`, React.memo, useMemo, when to use | 15 min |
| 23 | [Generators](10.1.23-generators.md) | `function*`, yield, iterators, async generators, lazy evaluation | 25 min |
| 24 | [Currying & Composition](10.1.24-currying-composition.md) | Currying, partial application, pipe, compose, functional patterns | 20 min |
| 25 | [Recursion & Tail Call](10.1.25-recursion-tail-call.md) | Recursive patterns, tail call optimization, trampolining, memoized recursion | 20 min |

---

## 🆕 Modern JS & Interview Prep

The newest features + the interview Q&A bank.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 26 | [ES2024+ Features](10.1.27-es2024-features.md) | `structuredClone`, `toSorted`, `Object.groupBy`, `Promise.withResolvers`, `ArrayBuffer.transfer` | 20 min |
| 27 | [Web Workers](10.1.28-web-workers.md) | Dedicated/Shared workers, OffscreenCanvas, Comlink, React hooks for workers | 25 min |
| 28 | [Interview Questions](10.1.26-interview-questions.md) | 50+ curated questions with answers | 3 hrs (review) |

---

## 🛣️ Suggested Study Order

### Path A — New to JS (1-2 weeks)
1. Execution & Scope (all 6 files, ~2 hrs)
2. Async & Concurrency (4 files, ~2 hrs)
3. Data Structures & Memory (7 files, ~2.5 hrs)
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

## 🔗 Cross-References

- [TypeScript](../10.2-typescript/INDEX.md) — type system builds on JS fundamentals
- [Node.js](../../20-backend/20.1-node.js/INDEX.md) — event loop, async patterns
- [React](../10.3-react/INDEX.md) — closures, `this`, hooks use these concepts
- [Coding Patterns](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — JS in algorithm implementations

---

## Navigation

[← Previous: Interview Strategy](../../00-strategy/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: TypeScript →](../10.2-typescript/INDEX.md)
