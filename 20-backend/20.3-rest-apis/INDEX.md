# REST APIs — Index

> **14 files** — API design patterns (REST vs GraphQL vs gRPC vs WebSocket vs Webhook) + REST API design principles, HTTP methods, status codes, versioning, pagination, authentication, rate limiting, CORS, API gateways, OpenAPI, error envelopes, HTTP caching, and interview questions.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-API-ff6b35)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Start with API design patterns** to pick the right API style for your use case, then dive into the REST-specific deep-dives.

| # | File | Topics |
|---|------|--------|
| 00 | [API Design Patterns](20.3.01-api-design-patterns.md) | REST, GraphQL, gRPC, WebSocket, Webhook, SSE — when to use which, trade-offs |
| 01 | [REST Principles](20.3.02-rest-principles.md) | Resource-oriented design, HATEOAS, statelessness, idempotency |
| 02 | [HTTP Methods](20.3.03-http-methods.md) | GET, POST, PUT, PATCH, DELETE, safe vs unsafe, idempotent methods |
| 03 | [Status Codes](20.3.04-status-codes.md) | 2xx success, 3xx redirection, 4xx client errors, 5xx server errors |
| 04 | [Versioning](20.3.05-versioning.md) | URI versioning, header versioning, content negotiation, best practices |
| 05 | [Pagination](20.3.06-pagination.md) | Offset vs cursor pagination, page size, metadata, performance |
| 06 | [Authentication](20.3.07-authentication.md) | Basic auth, API keys, JWT, OAuth2, session-based auth |
| 07 | [Rate Limiting](20.3.08-rate-limiting.md) | Token bucket, leaky bucket, sliding window, distributed rate limiting |
| 08 | [CORS](20.3.09-cors.md) | Preflight, headers, credentials, wildcard origins, proxy solutions |
| 09 | [API Gateway](20.3.10-api-gateway.md) | Gateway patterns, aggregation, routing, authentication, throttling |
| 11 | [OpenAPI / Swagger](20.3.11-openapi-swagger.md) | OpenAPI spec, Swagger UI, client gen, contract testing, @nestjs/swagger |
| 12 | [Error Handling & Response Design](20.3.12-error-handling-design.md) | RFC 7807 problem details, error envelopes, requestId, retry-after |
| 13 | [HTTP Caching](20.3.13-http-caching.md) | Cache-Control, ETag, Last-Modified, Vary, stale-while-revalidate |
| 14 | [Interview Questions](20.3.14-interview-questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [NestJS](../20.2-nestjs/INDEX.md) | [Security (JWT/OAuth)](../INDEX.md) | [System Design](../../30-architecture/30.2-system-design/INDEX.md) | [Microservices (API Gateway)](../INDEX.md)
---

## Navigation

[← Previous: NestJS](../20.2-nestjs/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Database →](../20.4-database/INDEX.md)
