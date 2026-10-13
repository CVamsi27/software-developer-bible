# Patterns - NestJS

> **Study time:** ≈ 16 min of reading (3 files, ~5 min average).
> **3 files.** The architectural patterns NestJS supports out of the box: CQRS (commands, queries, events, sagas) and microservice transports (TCP, Redis, RabbitMQ, Kafka, gRPC).

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Patterns-success)](../INDEX.md)

---

## Reading flow

Start with [CQRS](20.2.3.01-cqrs.md) and follow one command and query through their registered handlers on a shared state owner. Then change the read side to an asynchronous projection and explain the new lag and recovery boundary.

Next, follow [Microservices](20.2.3.02-microservices.md) from subscription to a correlated remote reply. Compare a lost reply with a broker acknowledgment before choosing a transport. Use [Revision](REVISION.md) after both traces; deployment separation and durable effects require their own application contracts.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [CQRS](20.2.3.01-cqrs.md) | Commands, queries, events, sagas, command/query buses, `@nestjs/cqrs` | Essential | Important | 7 min |
| 02 | [Microservices](20.2.3.02-microservices.md) | TCP, Redis, RabbitMQ, Kafka, gRPC transports, hybrid apps, message patterns | Important | Important | 7 min |

---

## See also

- [CQRS deep-dive (architectural pattern)](../../../30-architecture/30.1-design-patterns/05-architectural/30.1.5.02-cqrs-di.md) — the architectural theory behind the framework's @nestjs/cqrs implementation
- [Microservices & Distributed Patterns stack](../../20.6-microservices/INDEX.md) — where the architecture decisions behind Nest's transports are made

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare application (NestJS + Prisma + PostgreSQL). Use the following paths to investigate the current checkout; these references do not establish deployment readiness:

Docita ships neither `@nestjs/cqrs` nor `@nestjs/microservices` — both patterns appear in pragmatic form:

| Topic | Docita evidence |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CQRS-lite commands | `apps/api/src/domains/appointments/application/use-cases/create-appointment.use-case.ts` - command-style use case against repository ports, no cqrs bus |
| Query / read side | `apps/api/src/domains/analytics/core/factories/base-analytics.factory.ts` - cached analytics projections act as read models |
| Domain events | `apps/api/src/shared/common/events/event.service.ts` - inspect the typed in-process EventEmitter2 bus; it does not establish remote delivery or persistence |

TCP/Redis/Kafka/gRPC transports are not used here. They could be introduced when a domain becomes a separate deployable service. The transactional outbox and PostgreSQL queue already carry asynchronous work between components.

---

[← Back to NestJS](../INDEX.md)
---

[← Previous: Request Lifecycle](../02-request-lifecycle/INDEX.md) · [Next: Quality & Operations →](../04-quality-and-operations/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
