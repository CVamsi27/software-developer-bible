# Edge & Scale - REST APIs

> **4 files.** Surviving traffic and integrating systems: rate limiting algorithms, API gateways, backend-for-frontend, and authentication schemes in the API context.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Edge%20%26%20Scale-blue)](../INDEX.md)

---

## Files

| Order | File                                          | Topics                                                                                                                     | Read time |
| --   :  | ------                                          | --------                                                                                                                     | ----------: |
| 01    | [Rate Limiting](20.3.4.01-rate-limiting.md)   | Algorithms (token bucket, sliding window), distributed limits                                                              | 25 min    |
| 02    | [API Gateway](20.3.4.02-api-gateway.md)       | Routing, aggregation, auth, rate limiting at the edge; deep patterns in [microservices](../../20.6-microservices/INDEX.md) | 20 min    |
| 03    | [BFF](20.3.4.03-bff.md)                       | Backend-for-frontend pattern, per-client payload shaping, gateway-routes vs dedicated-BFF vs GraphQL-BFF variants          | 25 min    |
| 04    | [Authentication](20.3.4.04-authentication.md) | Auth schemes for APIs; pairs with the [auth track](../../20.5-security/01-auth/INDEX.md)                                   | 25 min    |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic                      | Docita evidence                                                                                                                          |
| -------                      | -----------------                                                                                                                          |
| Rate limiting algorithms   | `apps/api/src/shared/common/interceptors/rate-limit.interceptor.ts` - windowed counters stored in CACHE_MANAGER                          |
| Distributed limits         | `apps/api/src/shared/modules/auth/guards/ip-rate-limit.guard.ts` - IP buckets beside user-rate-limit.guard.ts and global ThrottlerModule |
| Bot protection at the edge | `apps/api/src/shared/modules/turnstile/turnstile-verify.service.ts` - Cloudflare Turnstile gate on public booking routes                 |
| Authentication schemes     | `apps/api/src/shared/modules/auth/auth/api-key.service.ts` - hashed API keys for machines alongside JWT for users                        |

_No API gateway or BFF yet_ — a single Fly.io-deployed API serves all clients today; per-client shaping would start as dedicated route controllers before any gateway product.
