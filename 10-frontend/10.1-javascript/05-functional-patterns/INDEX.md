# Functional Patterns — JavaScript

> **Study time:** ≈ 1 h 27 m of reading (5 files, ~17 min average).
> **5 files.** The patterns you will use daily as a senior engineer: modules, memoization, generators, currying/composition, and recursion with tail-call optimization.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Functional_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Modules](10.1.5.01-modules.md) | ESM vs CommonJS, dynamic imports, tree shaking, barrel exports | 20 min |
| 02 | [Memoization](10.1.5.02-memoization.md) | Caching, `_.memoize`, React.memo, useMemo, when to use | 18 min |
| 03 | [Generators](10.1.5.03-generators.md) | `function*`, yield, iterators, async generators, lazy evaluation | 26 min |
| 04 | [Currying & Composition](10.1.5.04-currying-composition.md) | Currying, partial application, pipe, compose, functional patterns | 10 min |
| 05 | [Recursion & Tail Call](10.1.5.05-recursion-tail-call.md) | Recursive patterns, tail call optimization, trampolining, memoized recursion | 13 min |

---

## Read order

Modules → Memoization → Currying & Composition → Generators → Recursion & Tail Call.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Modules & barrel exports | `packages/utils/src/index.ts` - barrel re-exporting a domain-split module tree (date, medical, billing, …) |
| Memoization (`useMemo`) | `packages/ui/src/components/data-display/use-data-table-sort.ts` - sorting cached via `useMemo` over a copied array |

---

## Navigation

[← Back to JavaScript](../INDEX.md)
