# API Design

> **REST maturity, versioning, rate limiting, error handling, pagination, webhooks** — production API patterns.

| File | Topics |
|------|--------|
| [20.10.01-rest-maturity-model.md](20.10.01-rest-maturity-model.md) | Richardson Maturity Model (L0-L3), HATEOAS, API versioning strategies (URL, header, query param), deprecation timeline |
| [20.10.02-rate-limiting.md](20.10.02-rate-limiting.md) | Fixed window, sliding window, token bucket, leaky bucket, distributed rate limiting with Redis, per-tenant rate limiting |
| [20.10.03-error-handling.md](20.10.03-error-handling.md) | RFC 7807 problem details, NestJS exception filter, validation errors, PHI-safe error messages, batch operation errors |
| [20.10.04-pagination.md](20.10.04-pagination.md) | Offset vs cursor vs keyset pagination, infinite scroll with React Query, virtual scrolling |
| [20.10.05-webhooks.md](20.10.05-webhooks.md) | Webhook registration, delivery, HMAC signature verification, retry with backoff, DLQ, idempotency |
| [20.10.08-grpc-streaming.md](20.10.08-grpc-streaming.md) | gRPC streaming modes, Protocol Buffers, gRPC-Web, when to use gRPC vs REST |

---

**Study order:**
1. REST maturity model and versioning (foundation)
2. Error handling with RFC 7807 (consistent error shapes)
3. Pagination patterns (cursor vs offset)
4. Rate limiting algorithms (token bucket, sliding window)
5. Webhooks (delivery, verification, retry)
