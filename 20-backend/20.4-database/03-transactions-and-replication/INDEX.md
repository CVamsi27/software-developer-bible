# Transactions & Replication - Database

> **Study time:** ≈ 31 min of reading (5 files, ~6 min average).
> **5 files.** The hard part — how Postgres handles concurrent access: ACID transactions and isolation levels, deadlocks, optimistic vs pessimistic locking, and replication.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Transactions%20%26%20Replication-8b5cf6)](../INDEX.md)

---

## Reading flow

1. Define a transfer's invariant and commit boundary, then distinguish atomic grouping from concurrency protection.
2. Trace the two-session deadlock cycle. Compare ordinary blocking, timeout and deadlock errors before designing recovery.
3. Compare a stale editor's version predicate with a short held lock; use a single conditional mutation when it expresses the rule.
4. Follow a commit through receipt, flush and replay on replicas. Choose acknowledgment, freshness and failover authority separately.
5. Use [revision](REVISION.md) before applying these contracts to ORM transactions and the [interview bank](../05-operations-and-scaling/20.4.5.06-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ----- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [Transactions](20.4.3.01-transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels (read committed, repeatable read, serializable) | Essential | Foundational | 8 min |
| 02 | [Deadlocks](20.4.3.02-deadlocks.md) | Wait cycles, detector versus timeout, lock ordering, blocker diagnosis, whole-transaction retry | Essential | Foundational | 6 min |
| 03 | [Optimistic & Pessimistic Locking](20.4.3.03-optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks, SELECT FOR UPDATE | Important | Important | 7 min |
| 04 | [Database Replication](20.4.3.04-database-replication.md) | Physical vs logical, acknowledgment milestones, replay freshness, fenced failover, lag | Important | Important | 8 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Use these [Docita](https://github.com/CVamsi27/docita) source paths to investigate the NestJS, Prisma and PostgreSQL mechanisms. Their presence does not establish deployed behavior; check the current implementation, configuration and tests before relying on a guarantee:

| Topic | Docita evidence |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Transactions | `apps/api/src/prisma/transaction-runner.ts` - ITransactionRunner wraps `$transaction` for use cases |
| Advisory locks | `apps/api/src/shared/common/utils/postgres-advisory-lock.ts` - inspect the `pg_try_advisory_xact_lock` transaction boundary, lock identity and every participating job path |
| Transient-failure retries | `apps/api/src/shared/common/interceptors/prisma-retry.interceptor.ts` - P-coded transient errors retried with backoff |
| RLS-aware tx propagation | `apps/api/src/shared/modules/rls/active-tx.storage.ts` - AsyncLocalStorage hands the open tx to RLS session setters |

These source references do not establish the current database topology or failover contract. Inspect the actual deployment and workload before proposing replicas; then verify acknowledgment, replay freshness and promotion authority separately.
---

[← Previous: Querying & Optimization](../02-querying-and-optimization/INDEX.md) · [Next: ORM & Access →](../04-orm-and-access/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
