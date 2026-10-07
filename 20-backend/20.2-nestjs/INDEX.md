# NestJS — Index

> **Study time:** ≈ 6 h 4 m of reading (24 files, ~15 min average).
> **24 files** — NestJS framework from modules and controllers to guards, pipes, interceptors, CQRS, microservices, testing, configuration, lifecycle/shutdown, scheduling, OpenAPI docs, custom decorators, and interview questions.

[![Files](https://img.shields.io/badge/files-24-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-success)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why NestJS:** The most common Node.js framework for production TypeScript backends. Used by mid-stage startups (n8n, SumUp, etc.), enterprises, and increasingly at FAANG adjacent companies. Senior interviews test NestJS architecture (modules, DI), request lifecycle (middleware → guards → pipes → interceptors → controller), and patterns (CQRS, microservices, custom decorators).

---

## Topic Categories

The 18 files are organized into 5 categories, each with its own INDEX.

| Category | Files | Why it matters |
| ---------------------------------------------------------- | ----: | ----------------------------------------------------------------------------------------------------------- |
| [Core Architecture](01-core-architecture/INDEX.md) | 4 | Modules, Controllers, Providers, DI — the foundation |
| [Request Lifecycle](02-request-lifecycle/INDEX.md) | 6 | Middleware, Guards, Pipes, Interceptors, Exception Filters, Request Context (ALS) — what runs in what order |
| [Patterns](03-patterns/INDEX.md) | 2 | CQRS, Microservices — the patterns NestJS supports out of the box |
| [Quality & Operations](04-quality-and-operations/INDEX.md) | 5 | Config validation, Testing, Lifecycle/shutdown, Scheduling/jobs, OpenAPI docs |
| [Advanced & Interview](05-advanced-and-interview/INDEX.md) | 2 | Custom decorators, 50+ interview Qs |

---

## The Flow

```text
01 CORE ARCHITECTURE ──→ 02 REQUEST LIFECYCLE ──→ 03 PATTERNS ──→ 04 QUALITY & OPS ──→ 05 ADVANCED
modules                  middleware                CQRS           configuration       custom decorators
controllers              guards                    microservices  testing             interview Qs
providers                pipes                                    lifecycle/shutdown
DI                       interceptors                             scheduling/jobs
                         exception filters                        swagger/openapi
```

**Lifecycle order:** Middleware → Guards → Pipes → Controller → Interceptors (rxjs pipeline) → Exception Filters.

---

## Core Architecture

How NestJS apps are structured. Read these first. Category INDEX: [Core Architecture](01-core-architecture/INDEX.md).

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Modules](01-core-architecture/20.2.1.01-modules.md) | Feature modules, shared modules, global modules, dynamic modules, module re-exports | Essential | Important | 7 min |
| 02 | [Controllers](01-core-architecture/20.2.1.02-controllers.md) | Route handlers, request/response objects, decorators, version controllers | Essential | Important | 27 min |
| 03 | [Providers](01-core-architecture/20.2.1.03-providers.md) | Service providers, custom providers, provider scopes (default, request, transient) | Essential | Important | 22 min |
| 04 | [Dependency Injection](01-core-architecture/20.2.1.04-dependency-injection.md) | DI container, custom providers, circular dependencies, `forwardRef` | Essential | Important | 23 min |

---

## Request Lifecycle

The order of execution for every request — **every NestJS interview tests this**. Read in order. Category INDEX: [Request Lifecycle](02-request-lifecycle/INDEX.md).

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Middleware](02-request-lifecycle/20.2.2.01-middleware.md) | Functional middleware, class middleware, consumer configuration, `NestModule` | Essential | Important | 18 min |
| 02 | [Guards](02-request-lifecycle/20.2.2.02-guards.md) | Auth guards, role-based access, custom guards, `CanActivate`, execution context | Essential | Important | 23 min |
| 03 | [Pipes](02-request-lifecycle/20.2.2.03-pipes.md) | Validation pipes, transformation pipes, built-in pipes, custom pipes | Essential | Important | 24 min |
| 04 | [Interceptors](02-request-lifecycle/20.2.2.04-interceptors.md) | Request/response transformation, logging, caching, mapping, async interceptors | Essential | Important | 16 min |
| 05 | [Exception Filters](02-request-lifecycle/20.2.2.05-exception-filters.md) | Built-in exceptions, custom exception filters, catch-all filters, `@Catch()` | Essential | Important | 20 min |

---

## Patterns

The patterns NestJS supports out of the box. Category INDEX: [Patterns](03-patterns/INDEX.md).

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [CQRS](03-patterns/20.2.3.01-cqrs.md) | Commands, queries, events, sagas, command/query buses, `@nestjs/cqrs` | Essential | Important | 19 min |
| 02 | [Microservices](03-patterns/20.2.3.02-microservices.md) | TCP, Redis, RabbitMQ, Kafka, gRPC transports, hybrid apps, message patterns | Important | Important | 22 min |

---

## Quality & Operations

Production hygiene. Category INDEX: [Quality & Operations](04-quality-and-operations/INDEX.md).

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Configuration & Validation](04-quality-and-operations/20.2.4.01-configuration-validation.md) | ConfigModule, ValidationPipe, class-validator, Joi, DTOs, env validation | Essential | Important | 12 min |
| 02 | [Testing](04-quality-and-operations/20.2.4.02-testing.md) | Jest, TestingModule, supertest, Testcontainers, e2e/integration/unit | Essential | Important | 12 min |
| 03 | [Lifecycle Hooks & Graceful Shutdown](04-quality-and-operations/20.2.4.03-lifecycle-hooks-graceful-shutdown.md) | Lifecycle hook map + ordering, `enableShutdownHooks()`, SIGTERM, Kubernetes terminationGracePeriod, draining connections, closing pools in order | Essential | Important | 14 min |
| 04 | [Scheduling & Background Jobs](04-quality-and-operations/20.2.4.04-scheduling-background-jobs.md) | @nestjs/schedule + dynamic API, distributed cron locks (Redis NX), BullMQ queues, retries/backoff/rate limits, idempotent handlers, job observability | Essential | Important | 19 min |
| 05 | [Swagger & OpenAPI](04-quality-and-operations/20.2.4.05-swagger-openapi-nestjs.md) | @nestjs/swagger setup, DocumentBuilder, @ApiProperty DTOs, generics + @ApiExtraModels, security schemes, spec JSON codegen, CI contract checks | Essential | Important | 15 min |

---

## Advanced & Interview

Category INDEX: [Advanced & Interview](05-advanced-and-interview/INDEX.md).

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Custom Decorators](05-advanced-and-interview/20.2.5.01-custom-decorators.md) | Parameter decorators (@CurrentUser, @ClinicId, @Pagination), method decorators (@RateLimit, @Cache, @Audit), decorator composition | Essential | Important | 10 min |
| 02 | [Interview Questions](05-advanced-and-interview/20.2.5.02-interview-questions.md) | 50+ curated questions with answers | Essential | Important | 38 min |

---

## Suggested Study Order

1. **Core Architecture** (4 files, ~2 hrs) — must know
2. **Request Lifecycle** (6 files, ~2.5 hrs) — must know, the most-asked cluster
3. **Patterns** (CQRS + Microservices) — for senior/DDD roles
4. **Quality & Operations** (5 files) — production hygiene
5. **Custom Decorators** — senior-level
6. **Interview Questions** — final review

---

## Cross-References

- [Node.js](../20.1-node.js/INDEX.md) — the runtime NestJS sits on
- [REST APIs](../20.3-rest-apis/INDEX.md) — NestJS controllers map to REST routes
- [Microservices (gRPC, Service Mesh)](../20.6-microservices/INDEX.md) — microservices patterns NestJS implements
- [Design Patterns (CQRS)](../../30-architecture/30.1-design-patterns/05-architectural/30.1.5.02-cqrs-di.md) — CQRS deep-dive
- [Testing](../../50-quality/50.1-testing/INDEX.md) — testing patterns

---

## Navigation

[← Previous: Node.js](../20.1-node.js/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: REST APIs →](../20.3-rest-apis/INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Modules & DI | `apps/api/src/app.module.ts` composing per-domain feature modules, e.g. `apps/api/src/domains/clinical/clinical.module.ts` - providers wired through the Nest container |
| Controllers | `apps/api/src/domains/clinical/presentation/controllers/{lab-tests,lab-workflow,medical-coding}.controller.ts` - thin route handlers delegating to services |
| Middleware | `apps/api/src/shared/common/middleware/tenant.middleware.ts` - resolves the active clinic tenant before guards run |
| Guards | `apps/api/src/shared/modules/auth/auth/jwt-auth.guard.ts`, `roles.guard.ts`, `tier.guard.ts` + `auth/guards/` (consent, tenant, policy, subscription-status, rate-limit) - authN/authZ gate the request lifecycle |
| Pipes (validation) | `apps/api/src/shared/common/pipes/zod-validation.pipe.ts` - global `ZodValidationPipe` (nestjs-zod) wired in `apps/api/src/main.ts` |
| Interceptors | `apps/api/src/shared/common/interceptors/` - request-id, request-logging, cache, timeout, tenant-context, csrf, rate-limit, idempotency cross-cutting behavior |
| Exception filters | `apps/api/src/shared/modules/error-handling/filters/http-exception.filter.ts` + `prisma-error.registry.ts` - global filter mapping Prisma/domain errors to HTTP responses |
| Scheduling | `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts`, `apps/api/src/domains/clinical/medical-code-sync.cron.ts`, `apps/api/src/domains/reminders/reminders.scheduler.module.ts` - @nestjs/schedule crons |
| Swagger / OpenAPI | `apps/api/src/main.ts` - SwaggerModule setup + `cleanupOpenApiDoc`; DTOs annotated via nestjs-zod |
| CQRS / Nest transports | No counterpart - domain flow uses services + outbox events (EventEmitter2), not `@nestjs/cqrs` or Nest microservice transports |
