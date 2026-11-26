# Generics & Inference — TypeScript

> **Study time:** ≈ 42 min of reading (5 files, ~8 min average).
> **5 files.** Reusable type-safe abstractions: generics with constraints and defaults, `infer` extraction in conditional types, recursive and variadic type-level programming, and the variance rules that decide assignability.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Generics_and_Inference-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | ----------: |
| 01 | [Generics](10.2.2.01-generics.md) | Generic functions, `const` and `NoInfer` inference, constraints, default type parameters, and validated decoders | Essential | Foundational | 11 min |
| 02 | [Infer](10.2.2.02-infer.md) | Conditional `infer` extraction, `ReturnType` and `Parameters`, constrained and repeated `infer`, and recursive unwrapping | Important | Specialized | 8 min |
| 03 | [Advanced Generics](10.2.2.03-advanced-generics.md) | Keyed container encodings, nested dot-path types, variadic pipelines, and tail-recursive transforms | Important | Specialized | 10 min |
| 04 | [Type Variance](10.2.2.04-type-variance.md) | Producer and consumer direction, strict callback constraints, method bivariance, mutable array holes, and variance annotations | Important | Specialized | 8 min |

---

## Read order

Begin with one input and output type relationship, constraints, and defaults. Then capture nested parts of an existing static structure with `infer`. Compose these steps into container, path, and tuple APIs and check every transition, including nonmatches and empty inputs. Variance then asks whether a different producer or consumer can safely substitute for the original. Use the [revision drill](REVISION.md) before interview practice.

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React, and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic in this category | Docita evidence |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Generic functions & constraints | `packages/data-access/src/core/use-api-query.ts` - `<T, TError>` query wrapper using `Omit<UseQueryOptions, …>` |
| Generic component contracts | `packages/ui/src/components/data-display/data-table.types.ts` - `DataTableColumn<T>` with typed `cell` and `sort` callbacks |
| Two-type-param inference | `packages/utils/src/async/map-with-concurrency.ts` - `<T, R>` inferred end-to-end through the worker pool |

---

## Navigation

[← Back to TypeScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
