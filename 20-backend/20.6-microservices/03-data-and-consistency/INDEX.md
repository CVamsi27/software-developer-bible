# Data & Consistency - Microservices

> **Study time:** ≈ 40 min of reading (7 files, ~6 min average).
> **7 files.** Atomicity and truth across service boundaries: saga with compensating transactions, distributed transaction patterns (outbox vs 2PC), event sourcing, CQRS, decomposing the monolith database, and the transactional outbox deep dive.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data%20%26%20Consistency-blue)](../INDEX.md)

---

## Learning flow

Start with visible saga progress and compare it with atomic commit. Then follow accepted event history into replay and separate read models, before moving database ownership and studying publication intent. Use [revision](REVISION.md) before the [interview bank](../05-interview-drills/20.6.5.01-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Saga Pattern](20.6.3.01-saga-pattern.md) | Choreography vs orchestration, compensating transactions, idempotent compensations | Important | Important | 5 min |
| 02 | [Distributed Transactions](20.6.3.02-distributed-transactions.md) | 2PC trade-offs, saga, outbox pattern, idempotent consumers and the limits of locks | Important | Important | 6 min |
| 03 | [Event Sourcing](20.6.3.03-event-sourcing.md) | Event store design, rebuilding state by replay, snapshots, projection rebuilds | Important | Important | 6 min |
| 04 | [CQRS](20.6.3.04-cqrs.md) | Command/query separation, read models, eventual consistency, projection lag | Important | Important | 5 min |
| 05 | [Decomposing the Monolith Database](20.6.3.05-decomposing-monolith-database.md) | Shared-DB hazards, strangulation order for data, schema extraction steps, dual-write vs CDC sync, backfill strategies, cross-service referential integrity | Important | Important | 7 min |
| 06 | [Transactional Outbox](20.6.3.06-transactional-outbox.md) | Dual-write problem, outbox table, polling vs CDC relay, idempotent consumers, DLQ handling, production patterns | Essential | Important | 7 min |

---

[← Back to Microservices](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) source paths illustrate implementation choices; inspect actual transaction, completion and duplicate-handling boundaries:

| Topic | Docita evidence |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Transactional outbox | `apps/api/src/shared/modules/outbox/outbox.service.ts` - append() inside the same business transaction (ADR-0010) |
| Outbox relay | `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.ts` - cron drain, attempt escalation, processedAt marking |
| Idempotent consumers | `apps/api/src/shared/modules/idempotency/idempotency.service.ts` - stored key lifecycle requires a checked mutation/result boundary |
| DLQ discipline | `apps/api/src/shared/modules/queue/dlq-replay.scheduler.ts` - transient-error classification gates auto-replay |

Saga orchestration and event sourcing not used — the listed mechanisms do not alone prove atomic cross-module effects or completed asynchronous handlers.
---

[← Previous: Communication & Messaging](../02-communication-and-messaging/INDEX.md) · [Next: Resilience →](../04-resilience/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
