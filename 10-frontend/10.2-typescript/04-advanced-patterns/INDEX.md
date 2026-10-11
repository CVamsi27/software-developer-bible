# Advanced Patterns — TypeScript

> **Study time:** ≈ 1 h 37 m of reading (6 files, ~16 min average).
> **6 files.** The senior toolkit: `satisfies`, branded types, decorators, declaration files, and combined type-level patterns.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Advanced_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [The `satisfies` Operator](10.2.4.01-satisfies-operator.md) | Type validation without widening, literal preservation, config objects, route tables | Essential | Foundational | 11 min |
| 02 | [Branded Types](10.2.4.02-branded-types.md) | Nominal-like branding, units, boundary validation, flavoring, discriminated unions | Important | Specialized | 26 min |
| 03 | [Decorators](10.2.4.03-decorators.md) | Class, method, accessor, property, parameter decorators, metadata reflection | Important | Specialized | 19 min |
| 04 | [Declaration Files](10.2.4.04-declaration-files.md) | .d.ts syntax, module augmentation, global types, asset declarations, triple-slash directives | Important | Specialized | 25 min |
| 05 | [Advanced Patterns](10.2.4.05-advanced-patterns.md) | Class/parameter decorators, typed event emitter, advanced utility combinations | Important | Specialized | 11 min |

---

## Read order

First check a configuration while keeping its written keys with `satisfies`; distinguish finite table keys from an open index signature. Then validate a value and trace how a brand protects later typed calls without installing a runtime tag.

Next follow a decorator through class definition, instance initialization and invocation. Compare the two compiler modes and identify the validator/container that reads metadata. Declaration files then connect a runtime export to its consumer contract; use the separate-file fixture and check package entry paths. Finish by composing an event name with its payload and tracing dispatch, cleanup and failures.

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
