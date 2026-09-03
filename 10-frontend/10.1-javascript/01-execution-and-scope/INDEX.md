# Execution & Scope — JavaScript

> **6 files.** How JavaScript actually runs: execution contexts, the call stack, hoisting, scope, lexical environments, and closures — the foundation every other JS concept builds on.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Execution_and_Scope-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Execution Context](10.1.1.01-execution-context.md) | GEC vs FEC, creation/execution phases, scope chain, hoisting internals | 20 min |
| 02 | [Call Stack](10.1.1.02-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | 15 min |
| 03 | [Hoisting](10.1.1.03-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | 15 min |
| 04 | [Scope](10.1.1.04-scope.md) | Global, function, block scope, scope chain, lexical environment | 20 min |
| 05 | [Lexical Environment](10.1.1.05-lexical-environment.md) | Environment records, outer reference, scope chain internals | 15 min |
| 06 | [Closures](10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | 25 min |

---

## Read order

Execution Context → Call Stack → Hoisting → Scope → Lexical Environment → Closures.

Why this order: **Execution Context** introduces the creation phase (where hoisting happens), **Hoisting** then explains that phase's behavior in isolation, **Scope** defines the *rules* of name resolution, **Lexical Environment** reveals the *mechanism* (environment records + outer reference) that implements those rules, and only then does **Closures** — a function retaining its lexical environment — make sense. Teaching closures before scope/lexical environment (the old order) forced you to trust an unexplained mechanism.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Closures | `packages/hooks/src/use-interval.ts` - keeps the latest callback in a ref so interval closures never go stale |
| Closure factories & scope | `packages/hooks/src/create-mount-initializer.ts` - factory returning a component that closes over its `initialize` callback |

---

## Navigation

[← Back to JavaScript](../INDEX.md)
