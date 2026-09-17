# REST APIs — Index

> **Study time:** ≈ 7 h 7 m of reading (21 files, ~20 min average).
> **19 files — everything HTTP/API, fundamentals through production.** Study in three passes: **I. Fundamentals** (principles → methods → status codes) → **II. Production concerns** (pagination, errors, long-running operations, file uploads, rate limiting, webhooks, caching) → **III. Advanced** (maturity model, gateways, BFF, auth in context).
>
> Absorbed the former `20.10-api-design` stack — rate limiting, error handling (RFC 7807), pagination and webhooks live here once, at full depth.

[![Files](https://img.shields.io/badge/files-21-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 19 content files are organized into 5 categories, each with its own INDEX.

| Category | Files | Why it matters |
| ------------------------------------------------------------------------- | ----: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Design & Contract](01-design-and-contract/INDEX.md) | 5 | Principles, design patterns, versioning, maturity model, OpenAPI — how the API is shaped and specified |
| [HTTP Mechanics](02-http-mechanics/INDEX.md) | 4 | Methods, status codes, CORS, HTTP caching — the transport semantics you can't fake |
| [Payloads, Errors & Integration](03-payloads-errors-integration/INDEX.md) | 7 | Pagination, error handling (RFC 7807), long-running operations, file uploads, webhooks, serialization & wire formats, transactional email — the contract details clients feel daily |
| [Edge & Scale](04-edge-and-scale/INDEX.md) | 4 | Rate limiting, API gateway, BFF, authentication — surviving traffic; auth pairs with the [auth track](../20.5-security/01-auth/INDEX.md) |
| [Interview Drills](05-interview-drills/INDEX.md) | 1 | Curated Q&A |

---

## The Flow

```text
PASS I — FUNDAMENTALS      PASS II — PRODUCTION       PASS III — ADVANCED
01-design-and-contract  →  03-payloads-errors      →  04-edge-and-scale
02-http-mechanics          04-edge-and-scale (auth)    05-interview-drills

principles → methods    pagination → error design   rate limiting → gateway
→ status codes          → async ops + uploads       → BFF → maturity model
→ versioning            → webhooks, CORS, caching   → OpenAPI → drills
```

---

## The Study Order

| Pass | # | File | Topics |
| ---- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| I | 01 | [API Design Patterns](01-design-and-contract/20.3.1.01-api-design-patterns.md) | Resource naming, consistency, evolution |
| I | 02 | [REST Principles](01-design-and-contract/20.3.1.02-rest-principles.md) | Stateless, uniform interface, constraints |
| I | 03 | [HTTP Methods](02-http-mechanics/20.3.2.01-http-methods.md) | GET/POST/PUT/PATCH/DELETE semantics, idempotency |
| I | 04 | [Status Codes](02-http-mechanics/20.3.2.02-status-codes.md) | 2xx/4xx/5xx families, when to use which |
| I | 05 | [Versioning](01-design-and-contract/20.3.1.03-versioning.md) | URL vs header vs query, deprecation policy |
| II | 06 | [Pagination](03-payloads-errors-integration/20.3.3.01-pagination.md) | Offset vs cursor vs keyset — deep dive |
| II | 07 | [Long-Running API Operations](03-payloads-errors-integration/20.3.3.03-long-running-api-operations.md) | `202 Accepted`, operation resources, polling vs webhooks, idempotent resubmission, cancellation |
| II | 08 | [File Upload APIs](03-payloads-errors-integration/20.3.3.04-file-upload-apis.md) | Multipart streaming vs presigned S3 direct, resumable uploads, virus-scan gates |
| II | 09 | [Authentication](04-edge-and-scale/20.3.4.04-authentication.md) | Auth schemes for APIs; pairs with [auth track](../20.5-security/01-auth/INDEX.md) |
| II | 10 | [Rate Limiting](04-edge-and-scale/20.3.4.01-rate-limiting.md) | Algorithms (token bucket, sliding window), distributed limits |
| II | 11 | [CORS](02-http-mechanics/20.3.2.03-cors.md) | Preflight, headers, credentials |
| II | 12 | [Error Handling Design](03-payloads-errors-integration/20.3.3.02-error-handling-design.md) | RFC 7807 problem details, validation errors |
| II | 13 | [Webhooks](03-payloads-errors-integration/20.3.3.05-webhooks.md) | Delivery, HMAC verification, retry, DLQ, idempotency |
| II | 14 | [HTTP Caching](02-http-mechanics/20.3.2.04-http-caching.md) | ETags, Cache-Control, revalidation |
| III | 15 | [REST Maturity Model](01-design-and-contract/20.3.1.04-rest-maturity-model.md) | Richardson L0–L3, HATEOAS |
| III | 16 | [OpenAPI / Swagger](01-design-and-contract/20.3.1.05-openapi-swagger.md) | Spec-first design, codegen |
| III | 17 | [API Gateway](04-edge-and-scale/20.3.4.02-api-gateway.md) | Edge concerns; deep patterns in [microservices](../20.6-microservices/INDEX.md) |
| III | 18 | [BFF](04-edge-and-scale/20.3.4.03-bff.md) | Backend-for-frontend pattern |
| 19 | [Interview Questions](05-interview-drills/20.3.5.01-interview-questions.md) | Curated Q&A |  |

---

**Cross-references:** [Auth track](../20.5-security/01-auth/INDEX.md) · [Microservices & distributed patterns](../20.6-microservices/INDEX.md) · [Caching](../20.8-caching/INDEX.md)

---

## Navigation

[← Previous: NestJS](../20.2-nestjs/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Database →](../20.4-database/INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| URI versioning | `apps/api/src/main.ts` - `VersioningType.URI` enabled app-wide |
| Error contracts | `apps/api/src/shared/modules/error-handling/` - global `http-exception.filter.ts` + `prisma-error.registry.ts`; structured problem responses in `shared/common/errors/` (`forbidden-problem.ts`) |
| Pagination | `apps/api/src/shared/common/pagination.helper.ts` + per-domain list DTOs - cursor/offset helpers for list endpoints |
| Rate limiting | `apps/api/src/shared/common/interceptors/rate-limit.interceptor.ts` + `shared/modules/tenant-rate-limit/tenant-rate-limit.guard.ts` - per-clinic API quotas |
| Idempotent writes | `apps/api/src/shared/modules/idempotency/` - `idempotency.interceptor.ts` + `idempotency.service.ts` + `requires-idempotency.decorator.ts` for payment/order-style POSTs |
| Webhooks | `apps/api/src/domains/webhooks/` + `shared/modules/webhooks/webhook-verifier.ts`, `razorpay-webhook-verification.helper.ts`, `outgoing/` - signed inbound + outbound delivery |
| Response caching | `apps/api/src/cache/cache.module.ts` + `shared/common/interceptors/cache.interceptor.ts` - Cache-Control headers are not centrally set; see the caching sub-stack anchor |
| REST maturity / HATEOAS | No counterpart - pragmatic JSON API with typed DTOs; the maturity model is the interview framing |
