# Quality & Operations - NestJS

> **Study time:** ≈ 1 h 13 m of reading (6 files, ~12 min average).
> **6 files.** Production hygiene: configuration management with env validation, the testing story (unit, integration, e2e) built on `TestingModule`, lifecycle hooks and graceful shutdown, scheduling and background jobs, and OpenAPI/Swagger documentation with contract checks.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality%20%26%20Operations-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Configuration & Validation](20.2.4.01-configuration-validation.md) | ConfigModule, ValidationPipe, class-validator, Joi, DTOs, env validation | Essential | Important | 11 min |
| 02 | [Testing](20.2.4.02-testing.md) | Jest, TestingModule, supertest, Testcontainers, e2e/integration/unit | Essential | Important | 12 min |
| 03 | [Lifecycle Hooks & Graceful Shutdown](20.2.4.03-lifecycle-hooks-graceful-shutdown.md) | OnModuleInit/OnApplicationBootstrap/OnModuleDestroy/BeforeApplicationShutdown/OnApplicationShutdown, ordering guarantees, `enableShutdownHooks()`, SIGTERM, Kubernetes terminationGracePeriod, draining connections, closing pools in order | Essential | Important | 14 min |
| 04 | [Scheduling & Background Jobs](20.2.4.04-scheduling-background-jobs.md) | @nestjs/schedule (cron/interval/timeout + dynamic API), distributed cron locks (Redis NX / leader election), BullMQ queues, retries with backoff, rate limits, idempotent handlers, job observability | Essential | Important | 18 min |
| 05 | [Swagger & OpenAPI](20.2.4.05-swagger-openapi-nestjs.md) | @nestjs/swagger setup, DocumentBuilder composition, @ApiProperty DTO mapping, generics + @ApiExtraModels, bearer/apikey/cookie schemes, response decorators, spec JSON for client codegen, CI contract checks | Essential | Important | 15 min |

---

[← Back to NestJS](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

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
