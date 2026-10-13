# Functional Patterns — JavaScript

> **Study time:** ≈ 33 min of reading (6 files, ~6 min average).
> **6 files.** Patterns to choose by workload and code structure: modules, memoization, generators, currying/composition, and recursion with tail-call optimization.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Functional_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Modules](10.1.5.01-modules.md) | ESM/CommonJS, module identity, resolution, dynamic import and tree shaking | Essential | Foundational | 6 min |
| 02 | [Memoization](10.1.5.02-memoization.md) | Key equivalence, cache lifetime, bounded retention, promises and React memoization | Essential | Foundational | 6 min |
| 03 | [Generators](10.1.5.03-generators.md) | Pull iteration, async pages, sent values and iterator cleanup | Important | Specialized | 6 min |
| 04 | [Currying & Composition](10.1.5.04-currying-composition.md) | Currying vs partial application, composition order and framework handlers | Important | Specialized | 4 min |
| 05 | [Recursion & Tail Calls](10.1.5.05-recursion-tail-call.md) | Base cases, proper tail calls, explicit stacks and depth limits | Important | Specialized | 5 min |

---

## Read order

Read **Modules** to understand how code and shared state are wired across files. **Memoization** then makes the equivalence and lifetime rules of retained results explicit. **Generators** adds a consumer-controlled pause/resume exchange, including async work and cleanup. **Currying & Composition** uses closures to supply dependencies in stages and connects synchronous transformations. Finish with **Recursion & Tail Calls** to compare nested computation with explicit stacks and proper-tail-call guarantees, then use revision to distinguish repeated-work savings from reduced call-stack depth.

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
