# TypeScript — Index

> **18 files** — TypeScript type system mastery from basic types to branded types, template literals, declaration files, advanced generics, variance, decorators, the `satisfies` operator, and interview questions.

[![Files](https://img.shields.io/badge/files-18-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why TypeScript:** The standard for production JS. Every senior frontend or backend interview expects fluency in the type system — generics, conditional types, narrowing. TypeScript is not "syntactic sugar" — the type system lets you model domains that JS cannot (discriminated unions, branded types, conditional types).

---

## Topic Categories

The 18 files are organized into 5 category folders — read in order.

| Category                                                   | Files | Why it matters                                                                                    |
| ----------                                                   | ------: | ----------------                                                                                    |
| [Foundations](01-foundations/INDEX.md)                     | 4     | Types vs interfaces, keyof/typeof, type narrowing, tsconfig options — every interview starts here |
| [Generics & Inference](02-generics-and-inference/INDEX.md) | 4     | Generics, infer, advanced generics, variance — the heart of reusable TS code                      |
| [Type Transformations](03-type-transformations/INDEX.md)   | 4     | Utility types, conditional types, mapped types, template literals — composable type operations    |
| [Advanced Patterns](04-advanced-patterns/INDEX.md)         | 5     | Satisfies, branded types, decorators, declaration files — the senior toolkit                      |
| [Interview Prep](05-interview-prep/INDEX.md)               | 1     | 50+ curated Q&A                                                                                   |

---

## Study Flow

Read categories in numeric order — each builds on the previous:

```text
01-foundations ─▶ 02-generics-and-inference ─▶ 03-type-transformations
    ─▶ 04-advanced-patterns ─▶ 05-interview-prep
```

---

## Foundations

How TypeScript represents types.

| #  | File                                                                                 | Topics                                                                                                                                        | Read time |
| --:  | ------                                                                                 | --------                                                                                                                                        | ----------: |
| 01 | [Types vs Interfaces](01-foundations/10.2.1.01-types-vs-interfaces.md)               | Type aliases, interfaces, declaration merging, when to use each, performance                                                                  | 20 min    |
| 02 | [keyof / typeof](01-foundations/10.2.1.02-keyof-typeof.md)                           | Index type queries, typeof operator, enum types, indexed access types                                                                         | 20 min    |
| 03 | [Type Narrowing](01-foundations/10.2.1.03-type-narrowing.md)                         | typeof guards, instanceof, discriminated unions, type predicates, control flow analysis                                                       | 30 min    |
| 04 | [tsconfig & Compiler Options](01-foundations/10.2.1.04-tsconfig-compiler-options.md) | strict flag family, moduleResolution bundler/node16/nodenext, isolatedModules, incremental/composite, skipLibCheck, annotated senior tsconfig | 25 min    |

---

## Generics & Inference

Reusable type operations.

| #  | File                                                                          | Topics                                                                                                                                    | Read time |
| --:  | ------                                                                          | --------                                                                                                                                    | ----------: |
| 05 | [Generics](02-generics-and-inference/10.2.2.01-generics.md)                   | Generic functions, constraints, default type parameters, conditional generics                                                             | 25 min    |
| 06 | [Infer](02-generics-and-inference/10.2.2.02-infer.md)                         | Type inference in conditional types, `ReturnType`, `Parameters`, `Awaited`, custom utility types                                          | 25 min    |
| 07 | [Advanced Generics](02-generics-and-inference/10.2.2.03-advanced-generics.md) | Template literal types, variadic tuples, recursive types, builder patterns                                                                | 30 min    |
| 08 | [Type Variance](02-generics-and-inference/10.2.2.04-type-variance.md)         | Covariance/contravariance/invariance, strictFunctionTypes bivariance, unsound covariant arrays, in/out annotations, assignability puzzles | 25 min    |

---

## Type Transformations

The composable operations that make TS powerful.

| #  | File                                                                                  | Topics                                                                                 | Read time |
| --:  | ------                                                                                  | --------                                                                                 | ----------: |
| 09 | [Utility Types](03-type-transformations/10.2.3.01-utility-types.md)                   | `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable`   | 25 min    |
| 10 | [Conditional Types](03-type-transformations/10.2.3.02-conditional-types.md)           | Ternary types, distributive conditional types, `infer` keyword, `never`                | 25 min    |
| 11 | [Mapped Types](03-type-transformations/10.2.3.03-mapped-types.md)                     | Index signatures, mapping modifiers, `as` clause, key remapping                        | 25 min    |
| 12 | [Template Literal Types](03-type-transformations/10.2.3.04-template-literal-types.md) | String manipulation, infer patterns, CSS types, route builders, recursive string types | 30 min    |

---

## Advanced Patterns

Senior-level TS — types as a design tool.

| #  | File                                                                             | Topics                                                                                       | Read time |
| --:  | ------                                                                             | --------                                                                                       | ----------: |
| 13 | [The `satisfies` Operator](04-advanced-patterns/10.2.4.01-satisfies-operator.md) | Type validation without widening, literal preservation, config objects, route tables         | 20 min    |
| 14 | [Branded Types](04-advanced-patterns/10.2.4.02-branded-types.md)                 | Nominal typing, brand patterns, unit types, validation, flavoring, discriminated unions      | 25 min    |
| 15 | [Decorators](04-advanced-patterns/10.2.4.03-decorators.md)                       | Class, method, accessor, property, parameter decorators, metadata reflection                 | 25 min    |
| 16 | [Declaration Files](04-advanced-patterns/10.2.4.04-declaration-files.md)         | .d.ts syntax, module augmentation, global types, asset declarations, triple-slash directives | 25 min    |
| 17 | [Advanced Patterns](04-advanced-patterns/10.2.4.05-advanced-patterns.md)         | Class/parameter decorators, typed event emitter, advanced utility combinations               | 30 min    |

---

## Interview Prep

| #  | File                                                                      | Topics                             | Read time |
| --:  | ------                                                                      | --------                             | ----------: |
| 18 | [Interview Questions](05-interview-prep/10.2.5.01-interview-questions.md) | 50+ curated questions with answers | 3 hrs     |

---

## Suggested Study Order

1. **Foundations** (4 files, ~1.5 hrs) — must know
2. **Generics & Inference** (4 files, ~2 hrs) — must know
3. **Type Transformations** (4 files, ~1.5 hrs) — must know
4. **Advanced Patterns** (5 files, ~2.5 hrs) — senior level
5. **Interview Questions** (3 hrs)

---

## The Senior Pattern

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

## Cross-References

- [JavaScript](../10.1-javascript/INDEX.md) — TS builds on JS fundamentals
- [React](../10.3-react/INDEX.md) — TS for component props, hooks
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — TS for backend (decorators, DTOs)

---

## Navigation

[← Previous: JavaScript](../10.1-javascript/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: React →](../10.3-react/INDEX.md)
