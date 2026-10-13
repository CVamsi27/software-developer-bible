# Fundamentals - GraphQL

> **Study time:** ≈ 32 min of reading (4 files, ~8 min average).
> **4 files.** The mental model: GraphQL's typed operation contract, schema design, field selection and variables, mutation ordering, and subscription event boundaries.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Fundamentals-%23ff6b35)](../INDEX.md)

---

## Reading Flow

Read the overview to follow one selection from validation to its result. Next, design the schema's types and failure boundaries. Then build operations and trace a partially failing mutation before choosing retry behavior.

After the chapters, use [revision](REVISION.md), then continue to [execution](../02-execution/INDEX.md). The [interview bank](../04-interview-prep/20.7.4.01-interview-questions.md) comes after the complete GraphQL learning pass.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [GraphQL Overview](20.7.1.01-graphql-overview.md) | Typed query language + runtime, client-specified shapes, vs REST (over/under-fetching), when to use GraphQL | Optional | Specialized | 8 min |
| 02 | [Schema Design](20.7.1.02-schema-design.md) | Object/Interface/Union/Enum/Input/Scalar types, OneOf inputs, nullability, Relay connections, deprecation-aware evolution | Optional | Specialized | 12 min |
| 03 | [Queries & Mutations](20.7.1.03-queries-mutations.md) | Selection sets, variables, fragments, conditional selections (`@include`/`@skip`), operation names, serial mutation execution, errors and idempotency boundaries | Optional | Specialized | 10 min |

---

[← Back to GraphQL](../INDEX.md)

---

## Docita Anchor

_No direct Docita GraphQL implementation is cited here._ Docita is deliberately REST-first — URI-versioned REST documented via OpenAPI (`apps/api/src/main.ts`); `apps/api/package.json` carries no `@nestjs/graphql` or Apollo dependency. If GraphQL ever lands, schemas would start from these same domain modules and repository ports.
---

[Next: Execution →](../02-execution/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
