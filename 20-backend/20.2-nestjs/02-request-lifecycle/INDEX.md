# Request Lifecycle - NestJS

> **Study time:** ≈ 1 h 56 m of reading (7 files, ~17 min average).
> **7 files.** What runs in what order for every request: middleware → guards → pipes → interceptors → exception filters — plus the ambient request context (`AsyncLocalStorage`) that crosses all of those stages. Every NestJS interview tests this order — read the files in sequence.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Request%20Lifecycle-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Middleware](20.2.2.01-middleware.md) | Functional middleware, class middleware, consumer configuration, `NestModule` | Essential | Important | 18 min |
| 02 | [Guards](20.2.2.02-guards.md) | Auth guards, role-based access, custom guards, `CanActivate`, execution context | Essential | Important | 23 min |
| 03 | [Pipes](20.2.2.03-pipes.md) | Validation pipes, transformation pipes, built-in pipes, custom pipes | Essential | Important | 24 min |
| 04 | [Interceptors](20.2.2.04-interceptors.md) | Request/response transformation, logging, caching, mapping, async interceptors (rxjs pipeline) | Essential | Important | 16 min |
| 05 | [Exception Filters](20.2.2.05-exception-filters.md) | Built-in exceptions, custom exception filters, catch-all filters, `@Catch()` | Essential | Important | 20 min |
| 06 | [Request Context & AsyncLocalStorage](20.2.2.06-request-context-and-async-local-storage.md) | ALS mechanics, trace/tenant/user ids, ALS vs request-scoped DI, transaction propagation, re-entering context in workers, isolation tests | Essential | Important | 13 min |

Lifecycle order: Middleware → Guards → Interceptors (before) → Pipes → Controller → Interceptors (after). Exception filters handle exceptions that escape these stages.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Middleware | `apps/api/src/shared/common/middleware/tenant.middleware.ts` - AsyncLocalStorage carries clinicId/user for the whole request |
| Guards | `apps/api/src/shared/modules/auth/auth/jwt-auth.guard.ts` - JWT gate ahead of roles/policy/tenant/rate-limit guards |
| Pipes | `apps/api/src/shared/common/pipes/zod-validation.pipe.ts` - Zod transform+validate before handlers run |
| Interceptors | `apps/api/src/shared/common/interceptors/` - eight siblings: logging, request-id, timeout, cache, CSRF, rate-limit, safe-zod serializer, Prisma retry |
| Exception filters | `apps/api/src/shared/modules/error-handling/filters/http-exception.filter.ts` - catch-all mapping domain errors to status codes + Sentry |

---

[← Back to NestJS](../INDEX.md)
---

[← Previous: Core Architecture](../01-core-architecture/INDEX.md) · [Next: Patterns →](../03-patterns/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
