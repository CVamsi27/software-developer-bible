# Patterns - NestJS

> **Study time:** ≈ 41 min of reading (2 files, ~20 min average).
> **2 files.** The architectural patterns NestJS supports out of the box: CQRS (commands, queries, events, sagas) and microservice transports (TCP, Redis, RabbitMQ, Kafka, gRPC).

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Patterns-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [CQRS](20.2.3.01-cqrs.md) | Commands, queries, events, sagas, command/query buses, `@nestjs/cqrs` | 19 min |
| 02 | [Microservices](20.2.3.02-microservices.md) | TCP, Redis, RabbitMQ, Kafka, gRPC transports, hybrid apps, message patterns | 22 min |

---

## See also

- [CQRS deep-dive (architectural pattern)](../../../30-architecture/30.1-design-patterns/05-architectural/30.1.5.02-cqrs-di.md) — the architectural theory behind the framework's @nestjs/cqrs implementation
- [Microservices & Distributed Patterns stack](../../20.6-microservices/INDEX.md) — where the architecture decisions behind Nest's transports are made

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

Docita ships neither `@nestjs/cqrs` nor `@nestjs/microservices` — both patterns appear in pragmatic form:

| Topic | Docita evidence |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CQRS-lite commands | `apps/api/src/domains/appointments/application/use-cases/create-appointment.use-case.ts` - command-style use case against repository ports, no cqrs bus |
| Query / read side | `apps/api/src/domains/analytics/core/factories/base-analytics.factory.ts` - cached analytics projections act as read models |
| Domain events | `apps/api/src/shared/common/events/event.service.ts` - typed EventEmitter2 bus stands in for message-pattern transports |

TCP/Redis/Kafka/gRPC transports not used; would introduce them when a domain extracts into its own deployable — the transactional outbox + Postgres queue already form the async spine.

---

[← Back to NestJS](../INDEX.md)
---

[← Previous: Request Lifecycle](../02-request-lifecycle/INDEX.md) · [Next: Quality & Operations →](../04-quality-and-operations/INDEX.md)
