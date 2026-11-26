# Advanced Patterns — TypeScript

> **Study time:** ≈ 46 min of reading (7 files, ~7 min average).
> **7 files.** The senior toolkit: `satisfies`, branded types, decorators, declarations, composed type patterns, and the compiler pipeline that checks and emits them.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Advanced_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [The `satisfies` Operator](10.2.4.01-satisfies-operator.md) | Finite and open keys, contextual inference, `as const satisfies`, and `satisfies never` | Essential | Foundational | 5 min |
| 02 | [Branded Types](10.2.4.02-branded-types.md) | Opaque `unique symbol` IDs, validated units and currency, flavors, and runtime trust boundaries | Important | Specialized | 7 min |
| 03 | [Decorators](10.2.4.03-decorators.md) | Newer TC39 and legacy modes, `@bound` initializers, accessors, metadata consumers, and `erasableSyntaxOnly` | Important | Specialized | 8 min |
| 04 | [Declaration Files](10.2.4.04-declaration-files.md) | `.d.ts` scope, module augmentation, `exports` `"types"` order, and `isolatedDeclarations` | Important | Specialized | 7 min |
| 05 | [Advanced Patterns](10.2.4.05-advanced-patterns.md) | Correlated event and payload tuples, `void` events, dispatch, cleanup, and failure policy | Important | Specialized | 7 min |
| 06 | [TypeScript Compiler Pipeline](10.2.4.06-typescript-compiler-pipeline.md) | Program graph, resolution, parse, bind, check, emit, `composite` references, and transpiler boundaries | Important | Specialized | 6 min |

---

## Read order

First check a route table against finite keys with `satisfies`, then follow a validated brand from input to later typed calls. Keep the marker's static guarantee separate from runtime validation.

Next follow a decorator through definition, initialization, and invocation, and name the consumer of any metadata. Declaration files then connect a runtime export to its consumer contract; check both package entry paths. Trace an event name and payload through dispatch, cleanup, and failure behavior. Finish by following a configured project through resolution, diagnostics, and emit; separate editor feedback from the clean build and runtime artifact.

Use [revision](REVISION.md) after these passes, then move to [interview practice](../05-interview-prep/10.2.5.01-interview-questions.md).

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React, and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic in this category | Docita evidence |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `satisfies` on const data | `packages/types/src/billing/tier.ts` - `as const satisfies readonly TierName[]` |
| `satisfies` for config tables | `apps/app/src/features/consultation/workspace/shell/consultation-palette-actions.ts` - palette action arrays validated against `CommandPaletteAction` |
| Decorator runtime usage | `apps/api/src/domains/appointments/presentation/controllers/appointment-request.controller.ts` - `@Controller`, `@UseGuards`, `@Get`, `@Body` decorators |
| Enabling decorators via tsconfig | `packages/typescript-config/nestjs.json` - `experimentalDecorators` + `emitDecoratorMetadata` |

---

## Navigation

[← Back to TypeScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
