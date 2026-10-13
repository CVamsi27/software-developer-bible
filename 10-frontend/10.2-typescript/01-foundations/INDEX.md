# Foundations — TypeScript

> **Study time:** ≈ 29 min of reading (5 files, ~6 min average).
> **5 files.** Type aliases vs interfaces, `keyof`/`typeof`, control-flow-based narrowing, and the tsconfig compiler options that decide what actually gets checked.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Foundations-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | ----------: |
| 01 | [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md) | Type aliases, interfaces, declaration merging, when to use each, performance | Essential | Foundational | 6 min |
| 02 | [keyof / typeof](10.2.1.02-keyof-typeof.md) | Key unions, value-derived types, indexed access, safe dynamic lookup, mapped-type filtering | Essential | Foundational | 6 min |
| 03 | [Type Narrowing](10.2.1.03-type-narrowing.md) | typeof guards, instanceof, discriminated unions, type predicates, control flow analysis | Essential | Foundational | 6 min |
| 04 | [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md) | strict checks, bundler and compatible Node module modes, TypeScript 6/7 migration, build options and project references | Essential | Foundational | 6 min |

---

## Read order

First choose a named shape or alternative contract. Derive keys and property value types from that contract, then use runtime checks to narrow uncertain values before reading them. Finally trace the compiler project through checking, emission and the actual loader; flags change accepted code but do not validate runtime inputs. Complete the [revision drill](REVISION.md) before the stack interview bank.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| tsconfig & compiler options | `packages/typescript-config/base.json` - shared strict config: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `NodeNext` |
| Per-target config presets | `packages/typescript-config/react-library.json` - thin `extends` of base for JSX packages |
| Schemas → types (typeof/infer) | `packages/types/src/shared/users/roles.ts` - zod enums with `z.infer` plus `Record<DayOfWeek, string>` maps |

---

## Navigation

[← Back to TypeScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
