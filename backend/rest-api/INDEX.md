# REST APIs — Index

> **15 files** — API design patterns (REST vs GraphQL vs gRPC vs WebSocket vs Webhook) + REST API design principles, HTTP methods, status codes, versioning, pagination, authentication, rate limiting, CORS, API gateways, OpenAPI, error envelopes, HTTP caching, and interview questions.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-API-ff6b35)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Start with API design patterns** to pick the right API style for your use case, then dive into the REST-specific deep-dives.

| # | File | Topics |
|---|------|--------|
| 00 | [API Design Patterns](api-design-patterns.md) | REST, GraphQL, gRPC, WebSocket, Webhook, SSE — when to use which, trade-offs |
| 01 | [REST Principles](rest-principles.md) | Resource-oriented design, HATEOAS, statelessness, idempotency |
| 02 | [HTTP Methods](http-methods.md) | GET, POST, PUT, PATCH, DELETE, safe vs unsafe, idempotent methods |
| 03 | [Status Codes](status-codes.md) | 2xx success, 3xx redirection, 4xx client errors, 5xx server errors |
| 04 | [Versioning](versioning.md) | URI versioning, header versioning, content negotiation, best practices |
| 05 | [Pagination](pagination.md) | Offset vs cursor pagination, page size, metadata, performance |
| 06 | [Authentication](authentication.md) | Basic auth, API keys, JWT, OAuth2, session-based auth |
| 07 | [Rate Limiting](rate-limiting.md) | Token bucket, leaky bucket, sliding window, distributed rate limiting |
| 08 | [CORS](cors.md) | Preflight, headers, credentials, wildcard origins, proxy solutions |
| 09 | [API Gateway](api-gateway.md) | Gateway patterns, aggregation, routing, authentication, throttling |
| 11 | [OpenAPI / Swagger](openapi-swagger.md) | OpenAPI spec, Swagger UI, client gen, contract testing, @nestjs/swagger |
| 12 | [Error Handling & Response Design](error-handling-design.md) | RFC 7807 problem details, error envelopes, requestId, retry-after |
| 13 | [HTTP Caching](http-caching.md) | Cache-Control, ETag, Last-Modified, Vary, stale-while-revalidate |
| 14 | [Interview Questions](interview-questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [NestJS](../nestjs/INDEX.md) | [Security (JWT/OAuth)](../../backend/INDEX.md) | [System Design](../../architecture/system-design/INDEX.md) | [Microservices (API Gateway)](../../backend/INDEX.md)
---

## Navigation

[← Previous: NestJS](../nestjs/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Database →](../database/INDEX.md)
