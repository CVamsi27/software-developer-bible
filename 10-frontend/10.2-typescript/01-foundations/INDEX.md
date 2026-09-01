# Foundations — TypeScript

> **4 files.** Type aliases vs interfaces, `keyof`/`typeof`, control-flow-based narrowing, and the tsconfig compiler options that decide what actually gets checked.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Foundations-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order  | File                                                                  | Topics                                                                                                                                        | Read time   |
| --   : | ------                                                                | --------                                                                                                                                      | ----------: |
| 01     | [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md)               | Type aliases, interfaces, declaration merging, when to use each, performance                                                                  | 20 min      |
| 02     | [keyof / typeof](10.2.1.02-keyof-typeof.md)                           | Index type queries, typeof operator, enum types, indexed access types                                                                         | 20 min      |
| 03     | [Type Narrowing](10.2.1.03-type-narrowing.md)                         | typeof guards, instanceof, discriminated unions, type predicates, control flow analysis                                                       | 30 min      |
| 04     | [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md) | strict flag family, moduleResolution bundler/node16/nodenext, isolatedModules, incremental/composite, skipLibCheck, annotated senior tsconfig | 25 min      |

---

## Read order

Types vs Interfaces → keyof / typeof → Type Narrowing → tsconfig & Compiler Options.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category         | Docita evidence                                                                                                                               |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| tsconfig & compiler options    | `packages/typescript-config/base.json` - shared strict config: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `NodeNext` |
| Per-target config presets      | `packages/typescript-config/react-library.json` - thin `extends` of base for JSX packages                                                     |
| Schemas → types (typeof/infer) | `packages/types/src/shared/users/roles.ts` - zod enums with `z.infer` plus `Record<DayOfWeek, string>` maps                                   |

---

## Navigation

[← Back to TypeScript](../INDEX.md)
