# TypeScript — Index

> **15 files** — TypeScript type system mastery from basic types to branded types, template literals, declaration files, advanced generics, decorators, the `satisfies` operator, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why TypeScript:** The standard for production JS. Every senior frontend or backend interview expects fluency in the type system — generics, conditional types, narrowing. TypeScript is not "syntactic sugar" — the type system lets you model domains that JS cannot (discriminated unions, branded types, conditional types).

---

## 🗂️ Topic Categories

The 15 files are organized into 5 categories — read in order.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Foundations](#-foundations) | 3 | Types vs interfaces, keyof/typeof, type narrowing — every interview starts here |
| [Generics & Inference](#-generics--inference) | 3 | Generics, infer, advanced generics — the heart of reusable TS code |
| [Type System Tools](#-type-system-tools) | 4 | Utility types, conditional types, mapped types — composable type operations |
| [Advanced Patterns](#-advanced-patterns) | 4 | Decorators, template literals, branded types, declaration files, satisfies — the senior toolkit |
| [Interview Prep](#-interview-prep) | 1 | 50+ curated Q&A |

---

## 🧱 Foundations

How TypeScript represents types.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Types vs Interfaces](10.2.01-types-vs-interfaces.md) | Type aliases, interfaces, declaration merging, when to use each, performance | 20 min |
| 06 | [keyof / typeof](10.2.06-keyof-typeof.md) | Index type queries, typeof operator, enum types, indexed access types | 20 min |
| 08 | [Type Narrowing](10.2.08-type-narrowing.md) | typeof guards, instanceof, discriminated unions, type predicates, control flow analysis | 30 min |

---

## 🔁 Generics & Inference

Reusable type operations.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [Generics](10.2.02-generics.md) | Generic functions, constraints, default type parameters, conditional generics | 25 min |
| 05 | [Infer](10.2.05-infer.md) | Type inference in conditional types, `ReturnType`, `Parameters`, `Awaited`, custom utility types | 25 min |
| 10 | [Advanced Generics](10.2.10-advanced-generics.md) | Template literal types, variadic tuples, recursive types, builder patterns | 30 min |

---

## 🛠️ Type System Tools

The composable operations that make TS powerful.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Utility Types](10.2.03-utility-types.md) | `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable` | 25 min |
| 04 | [Conditional Types](10.2.04-conditional-types.md) | Ternary types, distributive conditional types, `infer` keyword, `never` | 25 min |
| 07 | [Mapped Types](10.2.07-mapped-types.md) | Index signatures, mapping modifiers, `as` clause, key remapping | 25 min |
| 16 | [Advanced Patterns](10.2.16-advanced-patterns.md) | Class/parameter decorators, typed event emitter, advanced utility combinations | 30 min |

---

## 🚀 Advanced Patterns

Senior-level TS — types as a design tool.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 09 | [Decorators](10.2.09-decorators.md) | Class, method, accessor, property, parameter decorators, metadata reflection | 25 min |
| 12 | [Template Literal Types](10.2.12-template-literal-types.md) | String manipulation, infer patterns, CSS types, route builders, recursive string types | 30 min |
| 13 | [Branded Types](10.2.13-branded-types.md) | Nominal typing, brand patterns, unit types, validation, flavoring, discriminated unions | 25 min |
| 14 | [Declaration Files](10.2.14-declaration-files.md) | .d.ts syntax, module augmentation, global types, asset declarations, triple-slash directives | 25 min |
| 15 | [The `satisfies` Operator](10.2.15-satisfies-operator.md) | Type validation without widening, literal preservation, config objects, route tables | 20 min |

---

## 🎤 Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 11 | [Interview Questions](10.2.11-interview-questions.md) | 50+ curated questions with answers | 3 hrs |

---

## 🛣️ Suggested Study Order

1. **Foundations** (3 files, ~1.5 hrs) — must know
2. **Generics & Inference** (3 files, ~1.5 hrs) — must know
3. **Type System Tools** (3 files, ~1.5 hrs) — must know
4. **Advanced Patterns** (5 files, ~2.5 hrs) — senior level
5. **Interview Questions** (3 hrs)

---

## 🎯 The Senior Pattern

```typescript
// TypeScript lets you model "this is a validated email" not just "this is a string"
type Email = string & { readonly __brand: 'Email' };

// TypeScript lets you make a function that only accepts valid routes
type Route = `/${string}`;
const go = (route: Route) => { /* ... */ };

// TypeScript lets you infer the return type of an async function
type AsyncReturn<T> = T extends Promise<infer R> ? R : never;
```

If you can read and write these patterns cold, you are ready for any senior TS interview.

---

## 🔗 Cross-References

- [JavaScript](../10.1-javascript/INDEX.md) — TS builds on JS fundamentals
- [React](../10.3-react/INDEX.md) — TS for component props, hooks
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — TS for backend (decorators, DTOs)

---

## Navigation

[← Previous: JavaScript](../10.1-javascript/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: React →](../10.3-react/INDEX.md)
