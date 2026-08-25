# Quality & Operations - NestJS

> **5 files.** Production hygiene: configuration management with env validation, the testing story (unit, integration, e2e) built on `TestingModule`, lifecycle hooks and graceful shutdown, scheduling and background jobs, and OpenAPI/Swagger documentation with contract checks.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Quality%20%26%20Operations-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Configuration & Validation](20.2.4.01-configuration-validation.md) | ConfigModule, ValidationPipe, class-validator, Joi, DTOs, env validation | 25 min |
| 02 | [Testing](20.2.4.02-testing.md) | Jest, TestingModule, supertest, Testcontainers, e2e/integration/unit | 30 min |
| 03 | [Lifecycle Hooks & Graceful Shutdown](20.2.4.03-lifecycle-hooks-graceful-shutdown.md) | OnModuleInit/OnApplicationBootstrap/OnModuleDestroy/BeforeApplicationShutdown/OnApplicationShutdown, ordering guarantees, `enableShutdownHooks()`, SIGTERM, Kubernetes terminationGracePeriod, draining connections, closing pools in order | 25 min |
| 04 | [Scheduling & Background Jobs](20.2.4.04-scheduling-background-jobs.md) | @nestjs/schedule (cron/interval/timeout + dynamic API), distributed cron locks (Redis NX / leader election), BullMQ queues, retries with backoff, rate limits, idempotent handlers, job observability | 30 min |
| 05 | [Swagger & OpenAPI](20.2.4.05-swagger-openapi-nestjs.md) | @nestjs/swagger setup, DocumentBuilder composition, @ApiProperty DTO mapping, generics + @ApiExtraModels, bearer/apikey/cookie schemes, response decorators, spec JSON for client codegen, CI contract checks | 25 min |

---

[← Back to NestJS](../INDEX.md)
