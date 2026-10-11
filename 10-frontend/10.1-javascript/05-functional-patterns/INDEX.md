# Functional Patterns — JavaScript

> **Study time:** ≈ 1 h 35 m of reading (6 files, ~16 min average).
> **6 files.** Patterns to choose by workload and code structure: modules, memoization, generators, currying/composition, and recursion with tail-call optimization.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Functional_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Modules](10.1.5.01-modules.md) | ESM vs CommonJS, dynamic imports, tree shaking, barrel exports | Essential | Foundational | 20 min |
| 02 | [Memoization](10.1.5.02-memoization.md) | Caching, `_.memoize`, React.memo, useMemo, when to use | Essential | Foundational | 16 min |
| 03 | [Generators](10.1.5.03-generators.md) | `function*`, yield, iterators, async generators, lazy evaluation | Important | Specialized | 24 min |
| 04 | [Currying & Composition](10.1.5.04-currying-composition.md) | Currying, partial application, pipe, compose, functional patterns | Important | Specialized | 13 min |
| 05 | [Recursion & Tail Call](10.1.5.05-recursion-tail-call.md) | Recursive patterns, tail call optimization, trampolining, memoized recursion | Important | Specialized | 15 min |

---

## Read order

Read **Modules** to understand how code and shared state are wired across files. **Memoization** then makes the ownership and equivalence rules of retained function state explicit. **Currying & Composition** uses closures to supply dependencies in stages and pass values through synchronous transformations.

**Generators** adds a consumer-controlled pause/resume exchange, including async work and cleanup. **Recursion & Tail Call** compares nested computation with loops, trampolines and bounded-depth contracts. Finish with revision so you can distinguish reduced repeated work from reduced call-stack depth.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare-platform codebase (NestJS API + React/Astro apps, TypeScript monorepo; source paths alone do not establish deployment status). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Modules & barrel exports | `packages/utils/src/index.ts` - barrel re-exporting a domain-split module tree (date, medical, billing, …) |
| Memoization (`useMemo`) | `packages/ui/src/components/data-display/use-data-table-sort.ts` - sorting cached via `useMemo` over a copied array |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
