# Interview Prep — TypeScript

> **Study time:** ≈ 38 min of reading (1 files, ~38 min average).
> **1 file.** The self-test bank: 50+ curated TypeScript interview questions grouped by difficulty.

[![Files](https://img.shields.io/badge/files-1-blue)](#files)
[![Category](https://img.shields.io/badge/category-Interview_Prep-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Interview Questions](10.2.5.01-interview-questions.md) | 50+ curated questions with answers | Essential | Foundational | 38 min |

---

## Practice Order

Complete each category's revision companion before opening the bank: [foundations](../01-foundations/REVISION.md), [generics](../02-generics-and-inference/REVISION.md), [transformations](../03-type-transformations/REVISION.md) and [advanced patterns](../04-advanced-patterns/REVISION.md). Begin with accepted shapes and narrowing, then derive types and trace runtime contracts in the design drills.

Answer without reading the explanation, predict a call or output, and change one assumption: unknown data, a union input, a missing dependency or cleanup during dispatch. Revisit the linked canonical chapter when you cannot explain why the boundary holds. The bank is practice; it does not replace learning the implementation.

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

Practice the question bank against real artifacts:

| Topic in this category | Docita evidence |
| --------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Schema-first typing drills | `packages/types/src/shared/users/roles.ts` - enums, `z.infer`, and `Record` maps to reason about |
| `satisfies` / literal narrowing puzzles | `packages/types/src/billing/tier.ts` - const arrays checked against union types |
| Strictness trivia made concrete | `packages/typescript-config/base.json` - every strict flag from the questions, in a real config |

---

## Navigation

[← Back to TypeScript](../INDEX.md)
