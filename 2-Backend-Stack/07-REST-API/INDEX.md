# REST APIs — Index

> **15 files** — API design patterns (REST vs GraphQL vs gRPC vs WebSocket vs Webhook) + REST API design principles, HTTP methods, status codes, versioning, pagination, authentication, rate limiting, CORS, API gateways, OpenAPI, error envelopes, HTTP caching, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-API-ff6b35)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

**Start with API design patterns** to pick the right API style for your use case, then dive into the REST-specific deep-dives.

| # | File | Topics |
|---|------|--------|
| 00 | [API Design Patterns](00-API-Design-Patterns.md) | REST, GraphQL, gRPC, WebSocket, Webhook, SSE — when to use which, trade-offs |
| 01 | [REST Principles](01-REST-Principles.md) | Resource-oriented design, HATEOAS, statelessness, idempotency |
| 02 | [HTTP Methods](02-HTTP-Methods.md) | GET, POST, PUT, PATCH, DELETE, safe vs unsafe, idempotent methods |
| 03 | [Status Codes](03-Status-Codes.md) | 2xx success, 3xx redirection, 4xx client errors, 5xx server errors |
| 04 | [Versioning](04-Versioning.md) | URI versioning, header versioning, content negotiation, best practices |
| 05 | [Pagination](05-Pagination.md) | Offset vs cursor pagination, page size, metadata, performance |
| 06 | [Authentication](06-Authentication.md) | Basic auth, API keys, JWT, OAuth2, session-based auth |
| 07 | [Rate Limiting](07-Rate-Limiting.md) | Token bucket, leaky bucket, sliding window, distributed rate limiting |
| 08 | [CORS](08-CORS.md) | Preflight, headers, credentials, wildcard origins, proxy solutions |
| 09 | [API Gateway](09-API-Gateway.md) | Gateway patterns, aggregation, routing, authentication, throttling |
| 11 | [OpenAPI / Swagger](11-OpenAPI-Swagger.md) | OpenAPI spec, Swagger UI, client gen, contract testing, @nestjs/swagger |
| 12 | [Error Handling & Response Design](12-Error-Handling-Design.md) | RFC 7807 problem details, error envelopes, requestId, retry-after |
| 13 | [HTTP Caching](13-HTTP-Caching.md) | Cache-Control, ETag, Last-Modified, Vary, stale-while-revalidate |
| 14 | [Interview Questions](14-Interview-Questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [NestJS](../06-NestJS/) | [Security (JWT/OAuth)](../09-Security/) | [System Design](../../30-Architecture-Stack/11-System-Design/) | [Microservices (API Gateway)](../12-Microservices/)
---

## Navigation

[← Previous: NestJS](../06-NestJS/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Database →](../08-Database/INDEX.md)
