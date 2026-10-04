# Advanced Patterns — TypeScript

> **Study time:** ≈ 1 h 30 m of reading (6 files, ~15 min average).
> **6 files.** The senior toolkit: `satisfies`, branded types, decorators, declaration files, and combined type-level patterns.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Advanced_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [The `satisfies` Operator](10.2.4.01-satisfies-operator.md) | Type validation without widening, literal preservation, config objects, route tables | Essential | Foundational | 10 min |
| 02 | [Branded Types](10.2.4.02-branded-types.md) | Nominal typing, brand patterns, unit types, validation, flavoring, discriminated unions | Important | Specialized | 24 min |
| 03 | [Decorators](10.2.4.03-decorators.md) | Class, method, accessor, property, parameter decorators, metadata reflection | Important | Specialized | 20 min |
| 04 | [Declaration Files](10.2.4.04-declaration-files.md) | .d.ts syntax, module augmentation, global types, asset declarations, triple-slash directives | Important | Specialized | 22 min |
| 05 | [Advanced Patterns](10.2.4.05-advanced-patterns.md) | Class/parameter decorators, typed event emitter, advanced utility combinations | Important | Specialized | 10 min |

---

## Read order

`satisfies` → Branded Types → Decorators → Declaration Files → Advanced Patterns.

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
