# HTTP Mechanics - REST APIs

> **Study time:** ≈ 1 h 31 m of reading (5 files, ~18 min average).
> **5 files.** The transport semantics you cannot fake in an interview: method semantics and idempotency, status code families, CORS, and HTTP caching headers.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-HTTP%20Mechanics-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [HTTP Methods](20.3.2.01-http-methods.md) | GET/POST/PUT/PATCH/DELETE semantics, idempotency, safety | Essential | Foundational | 29 min |
| 02 | [Status Codes](20.3.2.02-status-codes.md) | 2xx/4xx/5xx families, when to use which | Essential | Foundational | 30 min |
| 03 | [CORS](20.3.2.03-cors.md) | Preflight, headers, credentials | Essential | Foundational | 20 min |
| 04 | [HTTP Caching](20.3.2.04-http-caching.md) | ETags, Cache-Control, revalidation | Essential | Foundational | 9 min |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Method semantics / idempotency | `apps/api/src/shared/modules/idempotency/idempotency.interceptor.ts` - `Idempotency-Key` header replays stored responses |
| Status codes & error payloads | `apps/api/src/shared/common/errors/domain.errors.ts` - framework-free errors mapped to HTTP statuses by the global filter |
| CORS | `apps/api/src/main.ts` - `getCorsOrigins()` allow-list (+ WebSocket twin) |
| HTTP caching | `apps/api/src/shared/common/interceptors/cache.interceptor.ts` - hashed-key GET response caching through CACHE_MANAGER |
---

[← Previous: Design & Contract](../01-design-and-contract/INDEX.md) · [Next: Payloads, Errors & Integration →](../03-payloads-errors-integration/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
