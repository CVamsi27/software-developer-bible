# Core Architecture - NestJS

> **Study time:** ≈ 1 h 20 m of reading (5 files, ~16 min average).
> **5 files.** How NestJS apps are structured: modules, controllers, providers, and the dependency-injection container that wires them together. Read these first.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Core%20Architecture-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Modules](20.2.1.01-modules.md) | Feature modules, shared modules, global modules, dynamic modules, module re-exports | Essential | Important | 7 min |
| 02 | [Controllers](20.2.1.02-controllers.md) | Route handlers, request/response objects, decorators, version controllers | Essential | Important | 26 min |
| 03 | [Providers](20.2.1.03-providers.md) | Service providers, custom providers, provider scopes (default, request, transient) | Essential | Important | 22 min |
| 04 | [Dependency Injection](20.2.1.04-dependency-injection.md) | DI container, custom providers, circular dependencies, `forwardRef` | Essential | Important | 23 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modules | `apps/api/src/app.module.ts` - root module composing ~20 domain modules plus SharedModule and PrismaModule |
| Feature-module layering | `apps/api/src/domains/appointments/` - presentation/application/core/infrastructure layers inside one feature folder |
| Controllers | `apps/api/src/domains/appointments/presentation/controllers/appointments-schedule.controller.ts` - thin HTTP surface delegating to use cases |
| Providers & ports | `apps/api/src/domains/appointments/application/ports/appointment-persistence.port.ts` - interface bound to an infrastructure adapter via DI token |
| Provider composition | `apps/api/src/prisma/prisma.service.ts` - single PrismaService provider assembled with tenant/encryption/RLS extensions |
---

[Next: Request Lifecycle →](../02-request-lifecycle/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
