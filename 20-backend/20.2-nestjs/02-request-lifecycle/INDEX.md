# Request Lifecycle - NestJS

> **Study time:** ≈ 48 min of reading (7 files, ~7 min average).
> **7 files.** Follow an HTTP operation through middleware, guards, interceptor before-work, argument pipes, the handler and reverse result mapping; uncaught failures choose an applicable filter. AsyncLocalStorage associates context with the supported continuation, subject to identity and resource lifetime.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Request%20Lifecycle-success)](../INDEX.md)

---

## Reading flow

1. Establish correlation and terminal observation in [Middleware](20.2.2.01-middleware.md); explain who responds or continues.
2. Trace verified identity and metadata override in [Guards](20.2.2.02-guards.md), before input pipes run.
3. Separate missing, valid and malformed arguments in [Pipes](20.2.2.03-pipes.md), then identify which business constraints remain concurrent.
4. Nest [Interceptors](20.2.2.04-interceptors.md) around one result; distinguish stopped observation from cancelled effects.
5. Map uncaught failures through [Exception Filters](20.2.2.05-exception-filters.md), including selection and already-sent response limits.
6. Follow interleaving and retained timers in [Request Context](20.2.2.06-request-context-and-async-local-storage.md); context carries facts without establishing trust or resource validity.
7. Use [Revision](REVISION.md) after the examples and before the later interview bank.

## Chapter map

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Middleware](20.2.2.01-middleware.md) | Functional middleware, class middleware, consumer configuration, `NestModule` | Essential | Important | 7 min |
| 02 | [Guards](20.2.2.02-guards.md) | Auth guards, role-based access, custom guards, `CanActivate`, execution context | Essential | Important | 8 min |
| 03 | [Pipes](20.2.2.03-pipes.md) | Validation pipes, transformation pipes, built-in pipes, custom pipes | Essential | Important | 7 min |
| 04 | [Interceptors](20.2.2.04-interceptors.md) | Request/response transformation, logging, caching, mapping, async interceptors (rxjs pipeline) | Essential | Important | 7 min |
| 05 | [Exception Filters](20.2.2.05-exception-filters.md) | Built-in exceptions, custom exception filters, catch-all filters, `@Catch()` | Essential | Important | 8 min |
| 06 | [Request Context & AsyncLocalStorage](20.2.2.06-request-context-and-async-local-storage.md) | ALS mechanics, trace/tenant/user ids, ALS vs request-scoped DI, transaction propagation, re-entering context in workers, isolation tests | Essential | Important | 8 min |

Lifecycle order: Middleware → Guards → Interceptors (before) → Pipes → Controller → Interceptors (after). Exception filters handle exceptions that escape these stages.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare platform (NestJS + Prisma + Postgres). Inspect the current checkout and deployment before treating these reading pointers as verified behavior:

| Topic | Docita evidence |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Middleware | `apps/api/src/shared/common/middleware/tenant.middleware.ts` - AsyncLocalStorage carries clinicId/user for the whole request |
| Guards | `apps/api/src/shared/modules/auth/auth/jwt-auth.guard.ts` - JWT gate ahead of roles/policy/tenant/rate-limit guards |
| Pipes | `apps/api/src/shared/common/pipes/zod-validation.pipe.ts` - Zod transform+validate before handlers run |
| Interceptors | `apps/api/src/shared/common/interceptors/` - inspect registration/order, response policy, timeout cancellation, cache eligibility and any retry boundaries |
| Exception filters | `apps/api/src/shared/modules/error-handling/filters/http-exception.filter.ts` - catch-all mapping domain errors to status codes + Sentry |

---

[← Back to NestJS](../INDEX.md)
---

[← Previous: Core Architecture](../01-core-architecture/INDEX.md) · [Next: Patterns →](../03-patterns/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
