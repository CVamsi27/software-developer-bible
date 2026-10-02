# Execution & Scope — JavaScript

> **Study time:** ≈ 35 min of reading (7 files, ~5 min average).
> **7 files.** How JavaScript actually runs: execution contexts, the call stack, hoisting, scope, lexical environments, and closures — the foundation every other JS concept builds on.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Execution_and_Scope-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Execution Context](10.1.1.01-execution-context.md) | GEC vs FEC, creation/execution phases, scope chain, hoisting internals | 4 min |
| 02 | [Scope](10.1.1.02-scope.md) | Global, function, block scope, scope chain, lexical environment | 5 min |
| 03 | [Call Stack](10.1.1.03-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | 5 min |
| 04 | [Hoisting](10.1.1.04-hoisting.md) | `var`/`let`/`const` hoisting, temporal dead zone, function hoisting | 7 min |
| 05 | [Lexical Environment](10.1.1.05-lexical-environment.md) | Environment records, outer reference, scope chain internals | 6 min |
| 06 | [Closures](10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | 5 min |

---

## Read order

Execution Context → Scope → Call Stack → Hoisting → Lexical Environment → Closures.

Why this order: **Execution Context** introduces the creation phase (where hoisting happens), **Scope** defines the *rules* of name resolution before anything else leans on them, **Call Stack** shows where those contexts live at runtime, **Hoisting** then explains the creation phase's observable behavior in isolation, **Lexical Environment** reveals the *mechanism* (environment records + outer reference) that implements the scope rules, and only then does **Closures** — a function retaining its lexical environment — make sense. Teaching closures before scope/lexical environment (the old order) forced you to trust an unexplained mechanism.

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
