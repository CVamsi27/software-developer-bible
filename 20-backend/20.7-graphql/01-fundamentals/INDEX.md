# Fundamentals - GraphQL

> **3 files.** The mental model: GraphQL as a typed query language vs REST, schema-first contract design, and queries/mutations/subscriptions syntax.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Fundamentals-%23ff6b35)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [GraphQL Overview](20.7.1.01-graphql-overview.md) | Typed query language + runtime, client-specified shapes, vs REST (over/under-fetching), when to use GraphQL | 20 min |
| 02 | [Schema Design](20.7.1.02-schema-design.md) | Object/Interface/Union/Enum/Input/Scalar types, nullability, Relay connections, input types for mutations, deprecation-aware evolution | 30 min |
| 03 | [Queries & Mutations](20.7.1.03-queries-mutations.md) | Selection sets, variables, fragments, directives (`@include`/`@skip`/`@deprecated`), subscriptions, idempotency keys for mutations | 20 min |

---

[← Back to GraphQL](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

_No direct docita implementation yet._ Docita is deliberately REST-first — URI-versioned REST documented via OpenAPI (`apps/api/src/main.ts`); `apps/api/package.json` carries no `@nestjs/graphql` or Apollo dependency. If GraphQL ever lands, schemas would start from these same domain modules and repository ports.
---

[Next: ../02 Execution/index →](../02-execution/INDEX.md)
