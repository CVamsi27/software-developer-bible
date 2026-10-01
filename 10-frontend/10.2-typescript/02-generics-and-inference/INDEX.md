# Generics & Inference — TypeScript

> **Study time:** ≈ 1 h 6 m of reading (4 files, ~16 min average).
> **4 files.** Reusable type-safe abstractions: generics with constraints and defaults, `infer` extraction in conditional types, recursive/variadic type-level programming, and the variance rules that decide assignability.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Generics_and_Inference-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Generics](10.2.2.01-generics.md) | Generic functions, constraints, default type parameters, conditional generics | 17 min |
| 02 | [Infer](10.2.2.02-infer.md) | Type inference in conditional types, `ReturnType`, `Parameters`, `Awaited`, custom utility types | 14 min |
| 03 | [Advanced Generics](10.2.2.03-advanced-generics.md) | Template literal types, variadic tuples, recursive types, builder patterns | 21 min |
| 04 | [Type Variance](10.2.2.04-type-variance.md) | Covariance/contravariance/invariance, strictFunctionTypes bivariance, unsound covariant arrays, in/out annotations, assignability puzzles | 14 min |

---

## Read order

Generics → Infer → Advanced Generics → Type Variance.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Generic functions & constraints | `packages/data-access/src/core/use-api-query.ts` - `<T, TError>` query wrapper using `Omit<UseQueryOptions, …>` |
| Generic component contracts | `packages/ui/src/components/data-display/data-table.types.ts` - `DataTableColumn<T>` with typed `cell`/`sort` callbacks |
| Two-type-param inference | `packages/utils/src/async/map-with-concurrency.ts` - `<T, R>` inferred end-to-end through the worker pool |

---

## Navigation

[← Back to TypeScript](../INDEX.md)
