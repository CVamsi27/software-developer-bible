# Data & Consistency - Microservices

> **4 files.** Atomicity and truth across service boundaries: saga with compensating transactions, distributed transaction patterns (outbox vs 2PC), event sourcing, and CQRS.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data%20%26%20Consistency-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Saga Pattern](20.6.3.01-saga-pattern.md) | Choreography vs orchestration, compensating transactions, idempotent compensations | 20 min |
| 02 | [Distributed Transactions](20.6.3.02-distributed-transactions.md) | 2PC trade-offs, saga, outbox pattern, idempotent consumers, why distributed locks are usually wrong | 10 min |
| 03 | [Event Sourcing](20.6.3.03-event-sourcing.md) | Event store design, rebuilding state by replay, snapshots, projection rebuilds | 20 min |
| 04 | [CQRS](20.6.3.04-cqrs.md) | Command/query separation, read models, eventual consistency, projection lag | 25 min |

---

[← Back to Microservices](../INDEX.md)
