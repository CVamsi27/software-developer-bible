# TypeScript — Index

> **Study time:** ≈ 2 h 58 m of reading (22 files, ~8 min average).
> **22 files** — TypeScript type system mastery from basic types to branded types, template literals, declaration files, advanced generics, variance, decorators, the `satisfies` operator, and interview questions.

[![Files](https://img.shields.io/badge/files-22-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core-blueviolet)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why TypeScript:** TypeScript checks relationships between values before the program runs. A discriminated union connects a tag to the fields available for that case. A branded type separates IDs with otherwise identical representations. Conditional types derive related types from one source. JavaScript can implement the same runtime behavior; TypeScript adds checks that help callers use it correctly. Generics, narrowing and these relationships are common frontend and backend interview topics.

---

## Topic Categories

The 18 files are organized into 5 category folders — read in order.

| Category | Files | Why it matters |
| ---------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------- |
| [Foundations](01-foundations/INDEX.md) | 4 | Types vs interfaces, keyof/typeof, type narrowing, tsconfig options — every interview starts here |
| [Generics & Inference](02-generics-and-inference/INDEX.md) | 4 | Generics, infer, advanced generics, variance — the heart of reusable TS code |
| [Type Transformations](03-type-transformations/INDEX.md) | 4 | Utility types, conditional types, mapped types, template literals — composable type operations |
| [Advanced Patterns](04-advanced-patterns/INDEX.md) | 5 | Satisfies, branded types, decorators, declaration files — the senior toolkit |
| [Interview Prep](05-interview-prep/INDEX.md) | 1 | 50 curated Q&A |

---

## Study Flow

Read categories in numeric order. First explain which shapes are compatible and how a checked branch narrows unknown input. Then carry an input/output relationship through generics, compare assignability under variance, and derive new records or string grammars with transformations.

In Advanced Patterns, follow validated constructors, decorator phases and separate runtime/declaration exports before combining them in a typed event bus. After each category, complete its separate revision companion; finish with the interview bank and change one condition per answer.

```text
01-foundations ─▶ 02-generics-and-inference ─▶ 03-type-transformations
    ─▶ 04-advanced-patterns ─▶ 05-interview-prep
```

---

## Foundations

How TypeScript represents types.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Types vs Interfaces](01-foundations/10.2.1.01-types-vs-interfaces.md) | Type aliases, interfaces, declaration merging, when to use each, performance | Essential | Foundational | 6 min |
| 02 | [keyof / typeof](01-foundations/10.2.1.02-keyof-typeof.md) | Key unions, value-derived types, indexed access, safe dynamic lookup, mapped-type filtering | Essential | Foundational | 6 min |
| 03 | [Type Narrowing](01-foundations/10.2.1.03-type-narrowing.md) | typeof guards, instanceof, discriminated unions, type predicates, control flow analysis | Essential | Foundational | 6 min |
| 04 | [tsconfig & Compiler Options](01-foundations/10.2.1.04-tsconfig-compiler-options.md) | strict flag family, moduleResolution bundler/node16/nodenext, isolatedModules, incremental/composite, skipLibCheck, annotated senior tsconfig | Essential | Foundational | 6 min |

---

## Generics & Inference

Reusable type operations.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Generics](02-generics-and-inference/10.2.2.01-generics.md) | Generic functions, constraints, default type parameters, conditional generics | Essential | Foundational | 9 min |
| 06 | [Infer](02-generics-and-inference/10.2.2.02-infer.md) | Type inference in conditional types, `ReturnType`, `Parameters`, `Awaited`, custom utility types | Important | Specialized | 6 min |
| 07 | [Advanced Generics](02-generics-and-inference/10.2.2.03-advanced-generics.md) | Template literal types, variadic tuples, recursive types, builder patterns | Important | Specialized | 9 min |
| 08 | [Type Variance](02-generics-and-inference/10.2.2.04-type-variance.md) | Covariance/contravariance/invariance, strictFunctionTypes bivariance, unsound covariant arrays, in/out annotations, assignability puzzles | Important | Specialized | 7 min |

---

## Type Transformations

The composable operations that make TS powerful.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 09 | [Utility Types](03-type-transformations/10.2.3.01-utility-types.md) | `Partial`, `Required`, `Pick`, `Omit`, `Record`, `Exclude`, `Extract`, `NonNullable` | Essential | Foundational | 8 min |
| 10 | [Conditional Types](03-type-transformations/10.2.3.02-conditional-types.md) | Ternary types, distributive conditional types, `infer` keyword, `never` | Important | Specialized | 8 min |
| 11 | [Mapped Types](03-type-transformations/10.2.3.03-mapped-types.md) | Index signatures, mapping modifiers, `as` clause, key remapping | Essential | Foundational | 8 min |
| 12 | [Template Literal Types](03-type-transformations/10.2.3.04-template-literal-types.md) | String manipulation, infer patterns, CSS types, route builders, recursive string types | Important | Specialized | 13 min |

---

## Advanced Patterns

Senior-level TS — types as a design tool.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 13 | [The `satisfies` Operator](04-advanced-patterns/10.2.4.01-satisfies-operator.md) | Type validation without widening, literal preservation, config objects, route tables | Essential | Foundational | 4 min |
| 14 | [Branded Types](04-advanced-patterns/10.2.4.02-branded-types.md) | Nominal-like branding, units, boundary validation, flavoring, discriminated unions | Important | Specialized | 6 min |
| 15 | [Decorators](04-advanced-patterns/10.2.4.03-decorators.md) | Class, method, accessor, property, parameter decorators, metadata reflection | Important | Specialized | 7 min |
| 16 | [Declaration Files](04-advanced-patterns/10.2.4.04-declaration-files.md) | .d.ts syntax, module augmentation, global types, asset declarations, triple-slash directives | Important | Specialized | 6 min |
| 17 | [Advanced Patterns](04-advanced-patterns/10.2.4.05-advanced-patterns.md) | Class/parameter decorators, typed event emitter, advanced utility combinations | Important | Specialized | 5 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 18 | [Interview Questions](05-interview-prep/10.2.5.01-interview-questions.md) | 50 curated questions with answers | Essential | Foundational | 39 min |

---

## Suggested Study Order

1. **Foundations** (4 files, ~1.5 hrs) — must know
2. **Generics & Inference** (4 files, ~2 hrs) — must know
3. **Type Transformations** (4 files, ~1.5 hrs) — must know
4. **Advanced Patterns** (5 files, ~2.5 hrs) — senior level
5. **Interview Questions** (39 min to read; reserve 3 hours for timed practice and review)

---

## Check a Type Against its Runtime Promise

An Email brand records construction discipline; only its constructor validates the string. A route type derives parameter names; only the router or builder implements the matching grammar. A declaration describes an exported function; only its JavaScript supplies the behavior. Explain those connections before adding a more complicated type.

For each learning pass, predict one accepted call, one rejected call and one runtime boundary. The category revision companions check those distinctions before [interview practice](05-interview-prep/10.2.5.01-interview-questions.md).

## Cross-References

- [JavaScript](../10.1-javascript/INDEX.md) — TS builds on JS fundamentals
- [React](../10.3-react/INDEX.md) — TS for component props, hooks
- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — TS for backend (decorators, DTOs)

---

## Navigation

[← Previous: JavaScript](../10.1-javascript/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: React →](../10.3-react/INDEX.md)
