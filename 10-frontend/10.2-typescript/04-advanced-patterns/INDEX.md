# Advanced Patterns — TypeScript

> **Study time:** ≈ 41 min of reading (7 files, ~6 min average).
> **7 files.** The senior toolkit: `satisfies`, branded types, decorators, declarations, composed type patterns, and the compiler pipeline that checks and emits them.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Advanced_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [The `satisfies` Operator](10.2.4.01-satisfies-operator.md) | Finite and open keys, contextual inference, route contracts | Essential | Foundational | 4 min |
| 02 | [Branded Types](10.2.4.02-branded-types.md) | Opaque IDs, validated units and currency, runtime trust boundaries | Important | Specialized | 6 min |
| 03 | [Decorators](10.2.4.03-decorators.md) | Newer and legacy modes, wrappers, accessors, metadata consumers | Important | Specialized | 7 min |
| 04 | [Declaration Files](10.2.4.04-declaration-files.md) | .d.ts scope, module augmentation, bundler assets, package exports | Important | Specialized | 6 min |
| 05 | [Advanced Patterns](10.2.4.05-advanced-patterns.md) | Composed event/payload contracts, dispatch, cleanup and failure policy | Important | Specialized | 6 min |
| 06 | [TypeScript Compiler Pipeline](10.2.4.06-typescript-compiler-pipeline.md) | Program construction, module resolution, parse/bind/check/emit, build and editor boundaries | Important | Specialized | 6 min |

---

## Read order

First check a route table against finite keys with `satisfies`, then follow a validated brand from input to later typed calls. Keep the marker’s static guarantee separate from runtime validation.

Next follow a decorator through definition, initialization and invocation, and name the consumer of any metadata. Declaration files then connect a runtime export to its consumer contract; check both package entry paths. Trace an event name and payload through dispatch, cleanup and failure behavior. Finish by following a configured project through resolution, diagnostics and emit; separate editor feedback from the clean build and runtime artifact.

Use [revision](REVISION.md) after these passes, then move to [interview practice](../05-interview-prep/10.2.5.01-interview-questions.md).

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

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
