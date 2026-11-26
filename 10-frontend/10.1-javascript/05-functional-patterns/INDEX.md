# Functional Patterns — JavaScript

> **Study time:** ≈ 42 min of reading (6 files, ~7 min average).
> **6 files.** Patterns to choose by workload and code structure: modules, memoization, generators, currying and composition, and recursion with tail-call behavior.

[![Files](https://img.shields.io/badge/files-6-blue)](#chapters)
[![Category](https://img.shields.io/badge/category-Functional_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Chapters

The Files badge counts these 5 chapters plus the revision companion.

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Modules](10.1.5.01-modules.md) | ESM versus CommonJS live bindings, dual-package hazard, `"exports"` map, `import.meta.dirname`, and tree shaking | Essential | Foundational | 7 min |
| 02 | [Memoization](10.1.5.02-memoization.md) | Key equivalence, JSON key traps, bounded LRU and TTL retention, promises, and React memoization | Essential | Foundational | 8 min |
| 03 | [Generators](10.1.5.03-generators.md) | Protocol keys, `Iterator.from` helpers, `yield*` delegation, async pages, and `finally` cleanup | Important | Specialized | 9 min |
| 04 | [Currying & Composition](10.1.5.04-currying-composition.md) | Currying versus partial application, `Function.length`, `pipe` and `pipeAsync`, and handler factories | Important | Specialized | 5 min |
| 05 | [Recursion & Tail Calls](10.1.5.05-recursion-tail-call.md) | Base cases, proper tail calls, trampolines, explicit cycle-safe stacks, and `BigInt` bottom-up DP | Important | Specialized | 6 min |

---

## Read order

Read **Modules** to understand how code and shared state are wired across files. **Memoization** then makes the equivalence and lifetime rules of retained results explicit. **Generators** adds a consumer-controlled pause and resume exchange, the `Symbol.iterator` contract that makes any object consumable, and async work with cleanup. **Currying & Composition** uses closures to supply dependencies in stages and connects synchronous and async transformations. Finish with **Recursion & Tail Calls** to compare nested computation with explicit stacks, trampolines, and proper-tail-call guarantees, then use revision to distinguish repeated-work savings from reduced call-stack depth.

---

## Docita Anchor

Real code from [Docita](https://github.com/CVamsi27/docita) - healthcare-platform codebase (NestJS API + React and Astro apps, TypeScript monorepo; source paths alone do not establish deployment status). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Modules & barrel exports | `packages/utils/src/index.ts` - barrel re-exporting a domain-split module tree (date, medical, billing, …) |
| Memoization (`useMemo`) | `packages/ui/src/components/data-display/use-data-table-sort.ts` - sorting cached via `useMemo` over a copied array |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
