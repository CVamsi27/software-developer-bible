# Data & Consistency - Microservices

> **Study time:** ≈ 2 h of reading (6 files, ~20 min average).
> **6 files.** Atomicity and truth across service boundaries: saga with compensating transactions, distributed transaction patterns (outbox vs 2PC), event sourcing, CQRS, decomposing the monolith database, and the transactional outbox deep dive.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data%20%26%20Consistency-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Saga Pattern](20.6.3.01-saga-pattern.md) | Choreography vs orchestration, compensating transactions, idempotent compensations | 26 min |
| 02 | [Distributed Transactions](20.6.3.02-distributed-transactions.md) | 2PC trade-offs, saga, outbox pattern, idempotent consumers, why distributed locks are usually wrong | 8 min |
| 03 | [Event Sourcing](20.6.3.03-event-sourcing.md) | Event store design, rebuilding state by replay, snapshots, projection rebuilds | 31 min |
| 04 | [CQRS](20.6.3.04-cqrs.md) | Command/query separation, read models, eventual consistency, projection lag | 29 min |
| 05 | [Decomposing the Monolith Database](20.6.3.05-decomposing-monolith-database.md) | Shared-DB hazards, strangulation order for data, schema extraction steps, dual-write vs CDC sync, backfill strategies, cross-service referential integrity | 13 min |
| 06 | [Transactional Outbox](20.6.3.06-transactional-outbox.md) | Dual-write problem, outbox table, polling vs CDC relay, idempotent consumers, DLQ handling, production patterns | 13 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Transactional outbox | `apps/api/src/shared/modules/outbox/outbox.service.ts` - append() inside the same business transaction (ADR-0010) |
| Outbox relay | `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts` - cron drain, attempt escalation, processedAt marking |
| Idempotent consumers | `apps/api/src/shared/modules/idempotency/idempotency.service.ts` - stored keys make handlers replay-safe |
| DLQ discipline | `apps/api/src/shared/modules/queue/dlq-replay.scheduler.ts` - transient-error classification gates auto-replay |

Saga orchestration and event sourcing not used — cross-module consistency currently rides the outbox + idempotency + DLQ trio above.
---

[← Previous: Communication & Messaging](../02-communication-and-messaging/INDEX.md) · [Next: Resilience →](../04-resilience/INDEX.md)
