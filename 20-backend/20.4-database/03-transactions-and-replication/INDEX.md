# Transactions & Replication - Database

> **Study time:** ≈ 1 h 12 m of reading (4 files, ~18 min average).
> **4 files.** The hard part — how Postgres handles concurrent access: ACID transactions and isolation levels, deadlocks, optimistic vs pessimistic locking, and replication.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Transactions%20%26%20Replication-8b5cf6)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Transactions](20.4.3.01-transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels (read committed, repeatable read, serializable) | 18 min |
| 02 | [Deadlocks](20.4.3.02-deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies, lock ordering | 18 min |
| 03 | [Optimistic & Pessimistic Locking](20.4.3.03-optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks, SELECT FOR UPDATE | 22 min |
| 04 | [Database Replication](20.4.3.04-database-replication.md) | Streaming vs logical, read replicas, Patroni failover, replication lag, conflict resolution | 14 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Transactions | `apps/api/src/prisma/transaction-runner.ts` - ITransactionRunner wraps `$transaction` for use cases |
| Advisory locks | `apps/api/src/shared/common/utils/postgres-advisory-lock.ts` - `pg_try_advisory_xact_lock` gives scheduled jobs single-flight |
| Transient-failure retries | `apps/api/src/shared/common/interceptors/prisma-retry.interceptor.ts` - P-coded transient errors retried with backoff |
| RLS-aware tx propagation | `apps/api/src/shared/modules/rls/active-tx.storage.ts` - AsyncLocalStorage hands the open tx to RLS session setters |

Replication/failover not used — a single managed Postgres instance; read replicas would arrive with reporting load.
---

[← Previous: Querying & Optimization](../02-querying-and-optimization/INDEX.md) · [Next: ORM & Access →](../04-orm-and-access/INDEX.md)
