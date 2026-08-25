# Transactions & Replication - Database

> **4 files.** The hard part — how Postgres handles concurrent access: ACID transactions and isolation levels, deadlocks, optimistic vs pessimistic locking, and replication.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Transactions%20%26%20Replication-8b5cf6)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Transactions](20.4.3.01-transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels (read committed, repeatable read, serializable) | 30 min |
| 02 | [Deadlocks](20.4.3.02-deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies, lock ordering | 20 min |
| 03 | [Optimistic & Pessimistic Locking](20.4.3.03-optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks, SELECT FOR UPDATE | 25 min |
| 04 | [Database Replication](20.4.3.04-database-replication.md) | Streaming vs logical, read replicas, Patroni failover, replication lag, conflict resolution | 30 min |

---

[← Back to Database](../INDEX.md)
