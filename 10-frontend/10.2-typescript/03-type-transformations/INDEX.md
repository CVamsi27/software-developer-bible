# Type Transformations — TypeScript

> **Study time:** ≈ 47 min of reading (5 files, ~9 min average).
> **5 files.** The composable operations that make TS powerful: built-in utility types, conditional types, mapped types, and template literal types.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Type_Transformations-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [Utility Types](10.2.3.01-utility-types.md) | `Pick`, `Omit`, `Partial`, `Required`, `Readonly`, `Record`, `Exclude`, `Extract`, `Awaited`, and `StrictOmit` | Essential | Foundational | 9 min |
| 02 | [Conditional Types](10.2.3.02-conditional-types.md) | Distributive vs. tuple-wrapped tests, `never` and `any`, deferred conditionals, lookup maps, and `infer` | Important | Specialized | 10 min |
| 03 | [Mapped Types](10.2.3.03-mapped-types.md) | Homomorphic modifiers, `as` key remapping, union-to-map transforms, and `Reflect.ownKeys` runtime mapping | Essential | Foundational | 9 min |
| 04 | [Template Literal Types](10.2.3.04-template-literal-types.md) | Intrinsic casing types, typed `${infer N extends number}`, route builders, deep paths, and TS 7 Unicode inference | Important | Specialized | 14 min |

---

## Read order

Start from a concrete public, editable, or resolved view and choose the built-in utility that describes it. Conditional types then show how alternative inputs choose result contracts; mapped types construct one property at a time, and template literals build or extract permitted string names. Trace the static result and corresponding runtime operation separately. Complete the [revision drill](REVISION.md) before interview practice.

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React, and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic in this category | Docita evidence |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Mapped and indexed access (`Record`) | `packages/types/src/shared/users/roles.ts` - `Record<DayOfWeek, string>` label and index maps |
| Conditional types in practice | `packages/ui/src/lib/rhf-path.ts` - guarded boundary around RHF's deferred conditional `Path<T>` |
| Utility types on props | `packages/ui/src/components/form/debounced-search-input.tsx` - `Omit<React.ComponentProps<typeof Input>, …>` prop derivation |

---

## Navigation

[← Back to TypeScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
