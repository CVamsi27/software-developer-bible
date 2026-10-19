# Generics & Inference — TypeScript

> **Study time:** ≈ 35 min of reading (5 files, ~7 min average).
> **5 files.** Reusable type-safe abstractions: generics with constraints and defaults, `infer` extraction in conditional types, recursive/variadic type-level programming, and the variance rules that decide assignability.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Generics_and_Inference-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | ----------: |
| 01 | [Generics](10.2.2.01-generics.md) | Generic functions, constraints, default type parameters, conditional generics | Essential | Foundational | 9 min |
| 02 | [Infer](10.2.2.02-infer.md) | Type inference in conditional types, `ReturnType`, `Parameters`, `Awaited`, custom utility types | Important | Specialized | 6 min |
| 03 | [Advanced Generics](10.2.2.03-advanced-generics.md) | Keyed container encodings, nested path reads and writes, variadic pipelines, recursive transforms and runtime boundaries | Important | Specialized | 9 min |
| 04 | [Type Variance](10.2.2.04-type-variance.md) | Producer/consumer direction, strict callback parameters, method bivariance, mutable array holes, variance annotations | Important | Specialized | 7 min |

---

## Read order

Begin with one input/output type relationship, constraints and defaults. Then capture nested parts of an existing static structure with infer. Compose these steps into container/path/tuple APIs and check every transition, including nonmatches and empty inputs. Variance then asks whether a different producer or consumer can safely substitute for the original. Use the [revision drill](REVISION.md) before interview practice.

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

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
