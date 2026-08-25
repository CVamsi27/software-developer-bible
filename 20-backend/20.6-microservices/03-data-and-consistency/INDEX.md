# Data & Consistency - Microservices

> **5 files.** Atomicity and truth across service boundaries: saga with compensating transactions, distributed transaction patterns (outbox vs 2PC), event sourcing, CQRS, and decomposing the monolith database.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data%20%26%20Consistency-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Saga Pattern](20.6.3.01-saga-pattern.md) | Choreography vs orchestration, compensating transactions, idempotent compensations | 20 min |
| 02 | [Distributed Transactions](20.6.3.02-distributed-transactions.md) | 2PC trade-offs, saga, outbox pattern, idempotent consumers, why distributed locks are usually wrong | 10 min |
| 03 | [Event Sourcing](20.6.3.03-event-sourcing.md) | Event store design, rebuilding state by replay, snapshots, projection rebuilds | 20 min |
| 04 | [CQRS](20.6.3.04-cqrs.md) | Command/query separation, read models, eventual consistency, projection lag | 25 min |
| 05 | [Decomposing the Monolith Database](20.6.3.05-decomposing-monolith-database.md) | Shared-DB hazards, strangulation order for data, schema extraction steps, dual-write vs CDC sync, backfill strategies, cross-service referential integrity | 30 min |

---

[← Back to Microservices](../INDEX.md)
