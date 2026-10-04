# Execution & Scope — JavaScript

> **Study time:** ≈ 38 min of reading (7 files, ~5 min average).
> **7 files.** How JavaScript actually runs: execution contexts, the call stack, hoisting, scope, lexical environments, and closures — the foundation every other JS concept builds on.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Execution_and_Scope-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Execution Context](10.1.1.01-execution-context.md) | GEC vs FEC, creation/execution phases, scope chain, hoisting internals | Essential | Foundational | 5 min |
| 02 | [Scope](10.1.1.02-scope.md) | Global, function, block scope, scope chain, lexical environment | Essential | Foundational | 5 min |
| 03 | [Call Stack](10.1.1.03-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | Essential | Foundational | 5 min |
| 04 | [Hoisting](10.1.1.04-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | Essential | Foundational | 7 min |
| 05 | [Lexical Environment](10.1.1.05-lexical-environment.md) | Environment records, outer reference, scope chain internals | Essential | Foundational | 8 min |
| 06 | [Closures](10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | Essential | Foundational | 5 min |

---

## Read order

Execution Context → Scope → Call Stack → Hoisting → Lexical Environment → Closures.

Why this order: **Execution Context** introduces the information needed to run code and set up declarations. **Scope** explains how names refer to variables. **Call Stack** follows active calls and returns. **Hoisting** then shows why a declaration can affect code before its source line runs. **Lexical Environment** explains the records and surrounding-scope links used to find variables. Finally, **Closures** shows how a function keeps access to those variables after the creating call returns.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Closures | `packages/hooks/src/use-mounted.ts` — effect returns cleanup closing over the timer ID |
| Closure factories & scope | `packages/hooks/src/create-navigation-history-provider.ts` — returned provider closes over the injected pathname hook and tracker |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
