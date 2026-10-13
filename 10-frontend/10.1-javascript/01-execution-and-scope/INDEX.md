# Execution & Scope — JavaScript

> **Study time:** ≈ 38 min of reading (7 files, ~5 min average).
> Follow a JavaScript evaluation from its active call to the names it can read, then see how declaration timing and closures change what remains accessible.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Execution_and_Scope-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Execution Context](10.1.1.01-execution-context.md) | Evaluation state, LE/VE roles, block transitions, parameter environments | Essential | Foundational | 5 min |
| 02 | [Scope](10.1.1.02-scope.md) | Global, function, block and module boundaries, binding lookup, lifetime | Essential | Foundational | 5 min |
| 03 | [Call Stack](10.1.1.03-call-stack.md) | LIFO, stack frames, stack overflow, max call stack size, debugging | Essential | Foundational | 6 min |
| 04 | [Hoisting](10.1.1.04-hoisting.md) | Declaration setup, temporal dead zone, function and resource declarations | Essential | Foundational | 7 min |
| 05 | [Lexical Environment](10.1.1.05-lexical-environment.md) | One lookup trace, the record roles behind names, global and module boundaries | Essential | Foundational | 5 min |
| 06 | [Closures](10.1.1.06-closures.md) | Lexical scoping, closure lifecycle, module pattern, memory implications | Essential | Foundational | 6 min |

---

## Read order

Execution Context → Scope → Call Stack → Hoisting → Lexical Environment → Closures.

Why this order: **Execution Context** introduces the state of one evaluation. **Scope** answers where names are visible, and **Call Stack** follows active calls and returns. **Hoisting** explains when bindings are established and initialized; **Lexical Environment** traces how a read finds one. **Closures** finishes the path by showing why a returned function can still reach its defining bindings.

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
