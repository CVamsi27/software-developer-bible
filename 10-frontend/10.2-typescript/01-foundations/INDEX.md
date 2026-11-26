# Foundations — TypeScript

> **Study time:** ≈ 34 min of reading (5 files, ~7 min average).
> **5 files.** Type aliases versus interfaces (open vs. closed assignability), `keyof` / `typeof` / `(typeof T)[number]`, control-flow narrowing & `asserts`, and `tsconfig.json` strictness.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Foundations-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [Types vs Interfaces](10.2.1.01-types-vs-interfaces.md) | Type aliases, interfaces, declaration merging, `Record` index-signature assignability, and performance | Essential | Foundational | 7 min |
| 02 | [keyof / typeof](10.2.1.02-keyof-typeof.md) | Key unions, `(typeof T)[number]` tuple unions, `Object.keys` `string[]` semantics, and safe dynamic lookup | Essential | Foundational | 7 min |
| 03 | [Type Narrowing](10.2.1.03-type-narrowing.md) | `typeof` guards, `asserts value is T` assertion functions, discriminated unions, and callback flow narrowing | Essential | Foundational | 7 min |
| 04 | [tsconfig & Compiler Options](10.2.1.04-tsconfig-compiler-options.md) | `strict`, `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`, module modes, and TypeScript 6 and 7 upgrades | Essential | Foundational | 8 min |

---

## Read order

First choose a named shape or alternative contract. Derive keys and property value types from that contract, then use runtime checks to narrow uncertain values before reading them. Finally trace the compiler project through checking, emission, and the actual loader; flags change accepted code but do not validate runtime inputs. Complete the [revision drill](REVISION.md) before the stack interview bank.

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React, and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic in this category | Docita evidence |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| tsconfig & compiler options | `packages/typescript-config/base.json` - shared strict config: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `NodeNext` |
| Per-target config presets | `packages/typescript-config/react-library.json` - thin `extends` of base for JSX packages |
| Schemas → types (`typeof` and `infer`) | `packages/types/src/shared/users/roles.ts` - zod enums with `z.infer` plus `Record<DayOfWeek, string>` maps |

---

## Navigation

[← Back to TypeScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
