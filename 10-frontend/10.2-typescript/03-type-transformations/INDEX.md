# Type Transformations — TypeScript

> **4 files.** The composable operations that make TS powerful: built-in utility types, conditional types, mapped types, and template literal types.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Type_Transformations-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File                                                          | Topics                                                                                 | Read time |
| --   :  | ------                                                          | --------                                                                                 | ----------: |
| 01    | [Utility Types](10.2.3.01-utility-types.md)                   | `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable`   | 25 min    |
| 02    | [Conditional Types](10.2.3.02-conditional-types.md)           | Ternary types, distributive conditional types, `infer` keyword, `never`                | 25 min    |
| 03    | [Mapped Types](10.2.3.03-mapped-types.md)                     | Index signatures, mapping modifiers, `as` clause, key remapping                        | 25 min    |
| 04    | [Template Literal Types](10.2.3.04-template-literal-types.md) | String manipulation, infer patterns, CSS types, route builders, recursive string types | 30 min    |

---

## Read order

Utility Types → Conditional Types → Mapped Types → Template Literal Types.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category           | Docita evidence                                                                                                              |
| ------------------------           | -----------------                                                                                                              |
| Mapped/indexed access (`Record`) | `packages/types/src/shared/users/roles.ts` - `Record<DayOfWeek, string>` label and index maps                                |
| Conditional types in practice    | `packages/ui/src/lib/rhf-path.ts` - guarded boundary around RHF's deferred conditional `Path<T>`                             |
| Utility types on props           | `packages/ui/src/components/form/debounced-search-input.tsx` - `Omit<React.ComponentProps<typeof Input>, …>` prop derivation |

---

## Navigation

[← Back to TypeScript](../INDEX.md)
