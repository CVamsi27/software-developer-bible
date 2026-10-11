# HTTP Mechanics - REST APIs

> **Study time:** ≈ 30 min of reading (5 files, ~6 min average).
> **5 files.** HTTP semantics to explain through a concrete request trace: method semantics and idempotency, status code families, CORS, and HTTP caching headers.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-HTTP%20Mechanics-blue)](../INDEX.md)

---

## Learning flow

Start with intended request effects and repeatability, then choose responses that communicate the actual outcome. CORS adds the browser's cross-origin read boundary. Caching then combines response reuse, variants and validation. Trace one changed condition in each chapter before using the revision companion.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [HTTP Methods](20.3.2.01-http-methods.md) | GET/POST/PUT/PATCH/DELETE semantics, idempotency, safety | Essential | Foundational | 6 min |
| 02 | [Status Codes](20.3.2.02-status-codes.md) | 2xx/4xx/5xx families, when to use which | Essential | Foundational | 8 min |
| 03 | [CORS](20.3.2.03-cors.md) | Preflight, headers, credentials | Essential | Foundational | 6 min |
| 04 | [HTTP Caching](20.3.2.04-http-caching.md) | ETags, Cache-Control, revalidation | Essential | Foundational | 8 min |
| Revision | [Category recall](REVISION.md) | Recall the trace and changed conditions | Essential | Foundational | — |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare application (NestJS + Prisma + PostgreSQL). Investigate these current-checkout paths; they do not establish deployment readiness:

| Topic | Docita evidence |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Method semantics / idempotency | `apps/api/src/shared/modules/idempotency/idempotency.interceptor.ts` - `Idempotency-Key` header replays stored responses |
| Status codes & error payloads | `apps/api/src/shared/common/errors/domain.errors.ts` - framework-free errors mapped to HTTP statuses by the global filter |
| CORS | `apps/api/src/main.ts` - `getCorsOrigins()` allow-list (+ WebSocket twin) |
| Application response cache (compare with HTTP policy) | `apps/api/src/shared/common/interceptors/cache.interceptor.ts` - hashed-key GET response caching through CACHE_MANAGER |

---

[← Previous: Design & Contract](../01-design-and-contract/INDEX.md) · [Next: Payloads, Errors & Integration →](../03-payloads-errors-integration/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
