# Core Architecture - NestJS

> **Study time:** ≈ 33 min of reading (5 files, ~7 min average).
> **5 files.** How NestJS apps are structured: modules, controllers, providers, and the dependency-injection container that wires them together. Read these first.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core%20Architecture-success)](../INDEX.md)

---

## Reading flow

1. Begin with [Modules](20.2.1.01-modules.md): identify the provider owner and the consumer's import/export path.
2. Trace [Controllers](20.2.1.02-controllers.md) from untrusted bytes through registered pipes into one service result and HTTP response.
3. Follow [Providers](20.2.1.03-providers.md) through a shared alias fixture, then compare construction bindings and state lifetimes.
4. Resolve [Dependency Injection](20.2.1.04-dependency-injection.md) in two explicit contexts; explain which token/visibility/context fact causes each failure.
5. Use [Revision](REVISION.md) after the examples, then continue to request lifecycle and later interview practice.

## Chapter map

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Modules](20.2.1.01-modules.md) | Feature modules, shared modules, global modules, dynamic modules, module re-exports | Essential | Important | 7 min |
| 02 | [Controllers](20.2.1.02-controllers.md) | Route handlers, request/response objects, decorators, version controllers | Essential | Important | 9 min |
| 03 | [Providers](20.2.1.03-providers.md) | Service providers, custom providers, provider scopes (default, request, transient) | Essential | Important | 7 min |
| 04 | [Dependency Injection](20.2.1.04-dependency-injection.md) | DI container, custom providers, circular dependencies, `forwardRef` | Essential | Important | 7 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare platform (NestJS + Prisma + Postgres). Inspect the current checkout and deployment before treating these reading pointers as verified behavior:

| Topic | Docita evidence |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modules | `apps/api/src/app.module.ts` - inspect root imports and each feature's exports |
| Feature-module layering | `apps/api/src/domains/appointments/` - presentation/application/core/infrastructure layers inside one feature folder |
| Controllers | `apps/api/src/domains/appointments/presentation/controllers/appointments-schedule.controller.ts` - thin HTTP surface delegating to use cases |
| Providers & ports | `apps/api/src/domains/appointments/application/ports/appointment-persistence.port.ts` - interface bound to an infrastructure adapter via DI token |
| Provider composition | `apps/api/src/prisma/prisma.service.ts` - single PrismaService provider assembled with tenant/encryption/RLS extensions |

---

[Next: Request Lifecycle →](../02-request-lifecycle/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
