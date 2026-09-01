# Backend Stack

> **Node.js, NestJS, REST, GraphQL, Database, Auth & Security, Microservices, AI Engineering** — shared by both the [indian-sde-faang lane](../81-lanes-indian-sde-faang/INDEX.md) and the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> 110 files across 9 sub-stacks, organized by what you need to know in what order.

[![Files](https://img.shields.io/badge/files-110-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-9-green)](#the-9-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

> **Real-world anchor:** every category INDEX below ends with a **Docita Anchor** table mapping its chapters to production code in [docita](https://github.com/CVamsi27/docita) — a healthcare platform (NestJS + Prisma + Postgres, modular monolith with a separate worker deployable). Read the chapter, then read the file that ships it. Where docita has no counterpart (GraphQL, Redis-backed caching, Kafka/gRPC), the anchor says so honestly instead of pretending.

---

## Why this stack matters

Backend is the deepest stack in the bible. Every senior full-stack interview tests:
- Node.js event loop, streams, async patterns
- REST API design (status codes, pagination, versioning, error formats)
- SQL + transactions + indexing
- Auth: JWT, OAuth, sessions, RBAC
- Security: XSS, CSRF, SQLi, OWASP Top 10
- Microservices: saga, CQRS, circuit breaker, event-driven

This stack is the canonical reference. Each sub-stack has its own INDEX with detailed categorization, decision flowcharts, and interview Q&A.

---

## The 9 Sub-Stacks (in study order)

| Order | Sub-stack                                                           | Files | Topics                                                                                                                                                                      |
| ----: | ------------------------------------------------------------------- | ----: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | [Node.js](20.1-node.js/INDEX.md)                                    | 11    | Event loop, streams, clustering, web streams, child processes, test runner                                                                                                  |
| 2     | [NestJS](20.2-nestjs/INDEX.md)                                      | 15    | Modules, DI, guards, pipes, interceptors, CQRS, microservices                                                                                                               |
| 3     | [REST APIs](20.3-rest-apis/INDEX.md)                                | 17    | HTTP methods, status codes, versioning, pagination, rate limiting, RFC 7807 errors, webhooks, HTTP caching, maturity model                                                  |
| 4     | [Database](20.4-database/INDEX.md)                                  | 20    | PostgreSQL, indexes, transactions, MVCC, Prisma, pooling, replication (5 categories)                                                                                        |
| 5     | [Auth & Security](20.5-security/INDEX.md)                           | 15    | [auth track](20.5-security/01-auth/INDEX.md): fundamentals → sessions → JWT → OAuth → RBAC/ABAC · attacks (XSS, CSRF, SQLi) · hardening (CSP, STRIDE, secrets) · API Top 10 |
| 6     | [Microservices & Distributed Patterns](20.6-microservices/INDEX.md) | 17    | Service discovery, gateway, saga, circuit breaker, event sourcing/CQRS, Kafka/RabbitMQ, gRPC streaming, service mesh, event-driven architecture                             |
| 7     | [GraphQL](20.7-graphql/INDEX.md)                                    | 8     | Schema design, queries/mutations, Apollo Server, performance, security                                                                                                      |
| 8     | [Caching](20.8-caching/INDEX.md)                                    | 3     | Cache patterns, invalidation, stampede prevention, Redis fundamentals + advanced patterns                                                                                   |
| 9     | [AI Engineering](20.12-ai-engineering/INDEX.md)                     | 4     | LLM app architecture (RAG/streaming/structured output), prompts & evals, safety & cost governance                                                                           |

---

## Category Map (high-level)

The backend stack is organized into 5 conceptual layers. Read in this order.

### Runtime & Language (read first)
- **Node.js** — the runtime; event loop, streams, async patterns
- **NestJS** — the most common framework; modules, DI, guards (read after Node.js)

### API Layer (read second)
- **REST APIs** — the canonical web API style; status codes, pagination, errors
- **GraphQL** — alternative to REST; schema-first design
- **Caching** — patterns every API needs

### Data Layer (read third)
- **Database** — PostgreSQL internals, Prisma ORM, performance

### Cross-Cutting (read fourth)
- **Auth & Security** — JWT, OAuth, RBAC, OWASP, threat modeling

### Distributed (read last)
- **Microservices** — saga, CQRS, event sourcing, service mesh
- **AI Engineering** — RAG, evals, cost governance (if JD requires)

---

## Suggested Study Order

### Path A — Full-stack senior, 4-week prep (most lanes)
1. Node.js TL;DR + Event Loop (1 hr)
2. NestJS TL;DR + Modules + DI (1.5 hrs)
3. REST APIs (3 hrs) — must know
4. Database (4-6 hrs) — must know
5. Auth (3 hrs) — must know
6. Caching (45 min)
7. Microservices (skim, 2 hrs)
8. GraphQL + AI Engineering — as needed

### Path B — Backend specialist, deep dive (3-4 weeks)
1. Node.js: full (4-5 hrs)
2. NestJS: full (5-6 hrs)
3. REST APIs: full (6-7 hrs)
4. Database: full (8-10 hrs)
5. Auth & Security: full (6-8 hrs)
6. Microservices: full (8-10 hrs)
7. GraphQL, Caching, AI Engineering — as needed

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- Node.js: re-read Event Loop
- REST: re-read Status Codes + Pagination
- Database: re-read MVCC + Transactions + Indexes
- Auth: re-read JWT + Sessions
- Microservices: re-read Saga + Circuit Breaker

---

## Cross-References

- [Frontend Stack](../10-frontend/INDEX.md) — for full-stack interviews
- [System Design](../INDEX.md) — backend patterns at scale
- [Platform Stack](../INDEX.md) — deployment, observability
- [Design Patterns](../INDEX.md) — Repository, Saga, CQRS, Event Sourcing, DI

---

## Navigation

[← Previous: Frontend](../10-frontend/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Architecture →](../30-architecture/INDEX.md)
