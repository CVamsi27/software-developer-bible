# Quality & Operations - NestJS

> **Study time:** ≈ 1 h 12 m of reading (6 files, ~12 min average).
> **6 files.** Follow application settings from startup into request handling, choose tests by the behavior they can prove, then trace shutdown and background work through recovery. Finish by comparing generated OpenAPI with runtime behavior.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality%20%26%20Operations-success)](../INDEX.md)

---

## Reading flow

1. Validate startup settings before constructing their clients, then distinguish those checks from request validation in [Configuration](20.2.4.01-configuration-validation.md).
2. Use [Testing](20.2.4.02-testing.md) to choose which graph, request path or database contract needs real components. A mocked success is evidence only for that configured collaboration.
3. Follow [Lifecycle](20.2.4.03-lifecycle-hooks-graceful-shutdown.md) from stopped admission through tracked work to dependency closure. Then trace [Jobs](20.2.4.04-scheduling-background-jobs.md) through lease loss and an uncertain external effect.
4. Generate [OpenAPI](20.2.4.05-swagger-openapi-nestjs.md) and compare it with runtime validation and responses. Use [Revision](REVISION.md) after these operational traces, before interview practice.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Configuration & Validation](20.2.4.01-configuration-validation.md) | Startup schemas with Zod/Standard Schema (Joi 18+ supported); class DTO or schema-first request validation; settings vs authorization | Essential | Important | 8 min |
| 02 | [Testing](20.2.4.02-testing.md) | Vitest/Jest, TestingModule, Supertest, Testcontainers; evidence at unit, integration, and HTTP boundaries | Essential | Important | 12 min |
| 03 | [Lifecycle Hooks & Graceful Shutdown](20.2.4.03-lifecycle-hooks-graceful-shutdown.md) | OnModuleInit/OnApplicationBootstrap/OnModuleDestroy/BeforeApplicationShutdown/OnApplicationShutdown, ordering guarantees, `enableShutdownHooks()`, SIGTERM, Kubernetes terminationGracePeriod, draining connections, closing pools in order | Essential | Important | 15 min |
| 04 | [Scheduling & Background Jobs](20.2.4.04-scheduling-background-jobs.md) | @nestjs/schedule (cron/interval/timeout + dynamic API), distributed cron locks (Redis NX / leader election), BullMQ queues, retries with backoff, rate limits, idempotent handlers, job observability | Essential | Important | 19 min |
| 05 | [Swagger & OpenAPI](20.2.4.05-swagger-openapi-nestjs.md) | @nestjs/swagger setup, DocumentBuilder composition, @ApiProperty DTO mapping, generics + @ApiExtraModels, bearer/apikey/cookie schemes, response decorators, spec JSON for client codegen, CI contract checks | Essential | Important | 15 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare application (NestJS + Prisma + PostgreSQL). Use the following paths to investigate the current checkout; these references do not establish deployment readiness:

| Topic | Docita evidence |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Configuration & validation | `apps/api/src/shared/modules/config/env-schema.ts` - Zod env schema parsed fail-fast at boot |
| Testing | `apps/api/test/seed-contract.parity.e2e-spec.ts` - e2e suite running against seed factories from `src/test-utils/` |
| Lifecycle hooks & graceful shutdown | `apps/api/src/prisma/prisma.service.ts` - OnModuleInit/OnModuleDestroy around the pg pool; worker drains on SIGTERM |
| Scheduling | `apps/api/src/shared/modules/schedule/cron-heartbeat.ts` - @TrackHeartbeat on every cron; a CI check enforces coverage |
| Background jobs | `apps/api/src/shared/modules/queue/postgres-queue.service.ts` - Postgres-backed queue with DLQ replay scheduler |
| Swagger & OpenAPI | `apps/api/src/main.ts` - DocumentBuilder spec generated from Zod-typed DTOs via nestjs-zod |

---

[← Previous: Patterns](../03-patterns/INDEX.md) · [Next: Advanced & Interview →](../05-advanced-and-interview/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
