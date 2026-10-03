# Foundations — TypeScript

> **Study time:** ≈ 57 min of reading (5 files, ~11 min average).
> **5 files.** Type aliases vs interfaces, `keyof`/`typeof`, control-flow-based narrowing, and the tsconfig compiler options that decide what actually gets checked.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Foundations-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md) | Type aliases, interfaces, declaration merging, when to use each, performance | Essential | Foundational | 7 min |
| 02 | [keyof / typeof](10.2.1.02-keyof-typeof.md) | Index type queries, typeof operator, enum types, indexed access types | Essential | Foundational | 15 min |
| 03 | [Type Narrowing](10.2.1.03-type-narrowing.md) | typeof guards, instanceof, discriminated unions, type predicates, control flow analysis | Essential | Foundational | 18 min |
| 04 | [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md) | strict flag family, moduleResolution bundler/node16/nodenext, isolatedModules, incremental/composite, skipLibCheck, annotated senior tsconfig | Essential | Foundational | 13 min |

---

## Read order

Types vs Interfaces → keyof / typeof → Type Narrowing → tsconfig & Compiler Options.

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
