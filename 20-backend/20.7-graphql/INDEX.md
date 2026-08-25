# GraphQL — Index

> **8 files** — GraphQL fundamentals from schema design and queries/mutations/subscriptions to resolvers, Apollo Server, Apollo Client, performance, security, and interview questions.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-API-%23ff6b35)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why GraphQL:** The alternative to REST. Used at GitHub, Shopify, Facebook, and increasingly at mid-stage startups. Senior interviews for full-stack roles may include GraphQL schema design, N+1 query prevention, and DataLoader patterns. Read this section if the JD mentions GraphQL or if you're interviewing at companies that have moved from REST.

---

## Topic Categories

The 8 files are organized into 4 categories, each with its own INDEX.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Fundamentals](01-fundamentals/INDEX.md) | 3 | Overview vs REST, schema design, queries/mutations/subscriptions |
| [Execution](02-execution/INDEX.md) | 2 | Resolvers + DataLoader, Apollo Server — the runtime side |
| [Clients & Production](03-clients-and-production/INDEX.md) | 2 | Apollo Client cache, performance & security defenses |
| [Interview Prep](04-interview-prep/INDEX.md) | 1 | 30+ curated Qs at senior depth |

---

## The Flow

```text
01 FUNDAMENTALS ──→ 02 EXECUTION ──→ 03 CLIENTS & PRODUCTION ──→ 04 INTERVIEW PREP
overview            resolvers         apollo client              30+ Q&A
schema design       apollo server     performance & security
queries/mutations
```

---

## Fundamentals

The mental model — schema-first design. Category INDEX: [Fundamentals](01-fundamentals/INDEX.md).

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [GraphQL Overview](01-fundamentals/20.7.1.01-graphql-overview.md) | Schema, queries, mutations, subscriptions, vs REST, when to use GraphQL | 20 min |
| 02 | [Schema Design](01-fundamentals/20.7.1.02-schema-design.md) | Types, fields, arguments, enums, unions, interfaces, input types, schema-first design | 30 min |
| 03 | [Queries & Mutations](01-fundamentals/20.7.1.03-queries-mutations.md) | Query structure, variables, directives, input types, fragments, alias | 20 min |

---

## Execution

How the server resolves queries. Category INDEX: [Execution](02-execution/INDEX.md).

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Resolvers](02-execution/20.7.2.01-resolvers.md) | Resolver chain, DataLoader (N+1 prevention), context, error handling | 30 min |
| 02 | [Apollo Server](02-execution/20.7.2.02-apollo-server.md) | Server setup, plugins, federation, subscriptions, schema stitching | 25 min |

---

## Clients & Production

The client-side and the production concerns. Category INDEX: [Clients & Production](03-clients-and-production/INDEX.md).

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Apollo Client](03-clients-and-production/20.7.3.01-apollo-client.md) | Client setup, queries, mutations, normalized cache, fragments, optimistic UI | 25 min |
| 02 | [Performance & Security](03-clients-and-production/20.7.3.02-performance-security.md) | N+1, DataLoader, query depth limits, complexity analysis, APQs (persisted queries), CSRF, auth | 30 min |

---

## Interview Prep

Category INDEX: [Interview Prep](04-interview-prep/INDEX.md).

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [GraphQL Interview Questions](04-interview-prep/20.7.4.01-interview-questions.md) | 30+ curated questions with answers | 2 hrs |

---

## Suggested Study Order

1. **Overview + Schema Design** (50 min) — must know
2. **Queries & Mutations** (20 min) — must know
3. **Resolvers** (30 min) — must know, especially DataLoader
4. **Apollo Server** (25 min) — production runtime
5. **Apollo Client** (25 min) — if frontend focus
6. **Performance & Security** (30 min) — senior level
7. **Interview Questions** (2 hrs)

---

## Cross-References

- [REST APIs](../20.3-rest-apis/INDEX.md) — the alternative; most senior interviews cover REST first
- [React](../../10-frontend/10.3-react/INDEX.md) — Apollo Client + React
- [NestJS](../20.2-nestjs/INDEX.md) — NestJS GraphQL module
- [System Design](../../30-architecture/30.2-system-design/INDEX.md) — GraphQL in system design (federation, schema stitching)

---

## Navigation

[← Previous: Microservices](../20.6-microservices/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Design Patterns →](../../30-architecture/30.1-design-patterns/INDEX.md)
