# REST APIs — Index

> **17 files — everything HTTP/API, fundamentals through production.** Study in three passes: **I. Fundamentals** (principles → methods → status codes) → **II. Production concerns** (pagination, errors, rate limiting, webhooks, caching) → **III. Advanced** (maturity model, gateways, BFF, auth in context).
>
> Absorbed the former `20.10-api-design` stack — rate limiting, error handling (RFC 7807), pagination and webhooks live here once, at full depth.

[![Files](https://img.shields.io/badge/files-17-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 17 content files classify into 6 conceptual categories — the "GoF classification" of API design.

| Category | Files | Why it matters |
|----------|------:|----------------|
| **Design & Contract** | 5 | Principles, design patterns, versioning, maturity model, OpenAPI — how the API is shaped and specified |
| **HTTP Mechanics** | 4 | Methods, status codes, CORS, HTTP caching — the transport semantics you can't fake |
| **Payloads & Errors** | 2 | Pagination, error handling (RFC 7807) — the contract details clients feel daily |
| **Edge, Scale & Integration** | 4 | Rate limiting, API gateway, BFF, webhooks — surviving traffic and integrating systems |
| **Security** | 1 | Authentication schemes; pairs with the [auth track](../20.5-security/auth/INDEX.md) |
| **Interview Drills** | 1 | Curated Q&A |

---

## The Flow

```text
PASS I — FUNDAMENTALS PASS II — PRODUCTION PASS III — ADVANCED
02 principles → 03 methods → 06 pagination → 08 rate limiting → 17 maturity model
04 status codes 12 error handling 13 HTTP caching 10 API gateway
01 design patterns 15 webhooks 09 CORS 16 BFF
                                   11 OpenAPI 07 authentication
```

| Pass | # | File | Topics |
|---|---|------|--------|
| I | 01 | [API Design Patterns](01-design-and-contract/20.3.1.01-api-design-patterns.md) | Resource naming, consistency, evolution |
| I | 02 | [REST Principles](01-design-and-contract/20.3.1.02-rest-principles.md) | Stateless, uniform interface, constraints |
| I | 03 | [HTTP Methods](02-http-mechanics/20.3.2.01-http-methods.md) | GET/POST/PUT/PATCH/DELETE semantics, idempotency |
| I | 04 | [Status Codes](02-http-mechanics/20.3.2.02-status-codes.md) | 2xx/4xx/5xx families, when to use which |
| I | 05 | [Versioning](01-design-and-contract/20.3.1.03-versioning.md) | URL vs header vs query, deprecation policy |
| II | 06 | [Pagination](03-payloads-errors-integration/20.3.3.01-pagination.md) | Offset vs cursor vs keyset — deep dive |
| II | 07 | [Authentication](04-edge-and-scale/20.3.4.04-authentication.md) | Auth schemes for APIs; pairs with [auth track](../20.5-security/auth/INDEX.md) |
| II | 08 | [Rate Limiting](04-edge-and-scale/20.3.4.01-rate-limiting.md) | Algorithms (token bucket, sliding window), distributed limits |
| II | 09 | [CORS](02-http-mechanics/20.3.2.03-cors.md) | Preflight, headers, credentials |
| II | 10 | [Error Handling Design](03-payloads-errors-integration/20.3.3.02-error-handling-design.md) | RFC 7807 problem details, validation errors |
| II | 11 | [Webhooks](03-payloads-errors-integration/20.3.3.05-webhooks.md) | Delivery, HMAC verification, retry, DLQ, idempotency |
| II | 12 | [HTTP Caching](02-http-mechanics/20.3.2.04-http-caching.md) | ETags, Cache-Control, revalidation |
| III | 13 | [REST Maturity Model](01-design-and-contract/20.3.1.04-rest-maturity-model.md) | Richardson L0–L3, HATEOAS |
| III | 14 | [OpenAPI / Swagger](01-design-and-contract/20.3.1.05-openapi-swagger.md) | Spec-first design, codegen |
| III | 15 | [API Gateway](04-edge-and-scale/20.3.4.02-api-gateway.md) | Edge concerns; deep patterns in [microservices](../20.6-microservices/INDEX.md) |
| III | 16 | [BFF](04-edge-and-scale/20.3.4.03-bff.md) | Backend-for-frontend pattern |
| | 17 | [Interview Questions](05-interview-drills/20.3.5.01-interview-questions.md) | Curated Q&A |

---

**Cross-references:** [Auth track](../20.5-security/auth/INDEX.md) · [Microservices & distributed patterns](../20.6-microservices/INDEX.md) · [Caching](../20.8-caching/INDEX.md)

---

## Navigation

[← Previous: NestJS](../20.2-nestjs/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Database →](../20.4-database/INDEX.md)
