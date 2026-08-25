# Request Lifecycle - NestJS

> **5 files.** What runs in what order for every request: middleware → guards → pipes → interceptors → exception filters. Every NestJS interview tests this order — read the files in sequence.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Request%20Lifecycle-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Middleware](20.2.2.01-middleware.md) | Functional middleware, class middleware, consumer configuration, `NestModule` | 15 min |
| 02 | [Guards](20.2.2.02-guards.md) | Auth guards, role-based access, custom guards, `CanActivate`, execution context | 25 min |
| 03 | [Pipes](20.2.2.03-pipes.md) | Validation pipes, transformation pipes, built-in pipes, custom pipes | 25 min |
| 04 | [Interceptors](20.2.2.04-interceptors.md) | Request/response transformation, logging, caching, mapping, async interceptors (rxjs pipeline) | 25 min |
| 05 | [Exception Filters](20.2.2.05-exception-filters.md) | Built-in exceptions, custom exception filters, catch-all filters, `@Catch()` | 20 min |

Lifecycle order: Middleware → Guards → Pipes → Controller → Interceptors → Exception Filters.

---

[← Back to NestJS](../INDEX.md)
