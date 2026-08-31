# Clients & Production - GraphQL

> **3 files.** The client side (normalized cache, optimistic UI), production defenses (query depth limits, complexity analysis, persisted queries, field-level auth), and schema-driven codegen with CI safety gates.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Clients%20%26%20Production-%23ff6b35)](../INDEX.md)

---

## Files

| Order | File                                                                   | Topics                                                                                                                                                                    | Read time |
| --   :  | ------                                                                   | --------                                                                                                                                                                    | ----------: |
| 01    | [Apollo Client](20.7.3.01-apollo-client.md)                            | `InMemoryCache` normalization by `__typename:id`, useQuery/useMutation/useSubscription, optimistic UI; urql/Relay alternatives                                            | 25 min    |
| 02    | [Performance & Security](20.7.3.02-performance-security.md)            | N+1, query depth limits, complexity/cost analysis, persisted queries (APQ), per-operation rate limiting, introspection off in prod, field-level auth, CSRF                | 30 min    |
| 03    | [Codegen & Schema Safety in CI](20.7.3.03-codegen-schema-safety-ci.md) | GraphQL Code Generator setup, TypedDocumentNode, fragment colocation, schema-as-source-of-truth workflow, graphql-inspector breaking-change checks, publishing typed SDKs | 25 min    |

---

[← Back to GraphQL](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

_No direct docita implementation yet._ REST-first choice — no GraphQL dependency anywhere in the workspace. The production-defense counterparts that do exist: response caching (`apps/api/src/shared/common/interceptors/cache.interceptor.ts`) and CSRF protection (`apps/api/src/shared/common/interceptors/csrf.interceptor.ts`).
