# Database — Index

> **20 files** — Database fundamentals from PostgreSQL internals to indexing, transactions, MVCC, joins, locking, connection pooling, Prisma, execution plans, SQL vs NoSQL, zero-downtime migrations, soft delete & tombstones, window functions, JSONB, replication, and interview questions.

[![Files](https://img.shields.io/badge/files-20-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data-8b5cf6)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why databases are non-negotiable:** Every senior backend interview tests database knowledge. Schema design, indexing, transactions, locking, connection pooling, query optimization — these are table stakes. This section is the canonical reference for PostgreSQL + Prisma, the most common stack at product-based companies.

---

## Topic Categories

The 20 files are organized into 5 categories.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [PostgreSQL Fundamentals](#postgresql-fundamentals) | 5 | How Postgres works under the hood — every backend interview starts here |
| [Querying & Optimization](#querying--optimization) | 3 | Indexes, joins, execution plans — the day-to-day performance work |
| [Concurrency & Transactions](#concurrency--transactions) | 4 | MVCC, transactions, locking, deadlocks — the hard part |
| [Operations & Scaling](#operations--scaling) | 4 | Connection pooling, replication, migrations, pooling/observability |
| [ORM & Specialized Features](#orm--specialized-features) | 4 | Prisma, JSONB, window functions, soft delete — production patterns |

---

## PostgreSQL Fundamentals

How Postgres actually works. Every backend interview starts here.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [PostgreSQL](01-postgresql-foundations/20.4.1.01-postgresql.md) | Architecture, WAL, vacuum, configuration, extensions, autovacuum | 30 min |
| 02 | [Normalization](01-postgresql-foundations/20.4.1.02-normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization trade-offs, when to denormalize | 25 min |
| 05 | [MVCC](01-postgresql-foundations/20.4.1.03-mvcc.md) | Multiversion concurrency control, visibility rules, tuple versions, vacuum | 30 min |
| 12 | [SQL vs NoSQL](01-postgresql-foundations/20.4.1.04-nosql-vs-sql.md) | Workload fit, CAP, consistency models, polyglot persistence, when to use what | 25 min |
| 20 | [PostgreSQL Performance](01-postgresql-foundations/20.4.1.05-postgresql-performance.md) | Connection tuning, memory tuning, query optimization, VACUUM, partitioning, monitoring queries | 30 min |

---

## Querying & Optimization

Making queries fast.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 03 | [Indexes](02-querying-and-optimization/20.4.2.01-indexes.md) | B-tree, hash, GiST, GIN, BRIN, composite indexes, index-only scans, partial indexes | 30 min |
| 06 | [Joins](02-querying-and-optimization/20.4.2.02-joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins, join order | 25 min |
| 11 | [Execution Plans](02-querying-and-optimization/20.4.2.03-execution-plans.md) | EXPLAIN ANALYZE, sequential vs index scans, cost estimation, statistics | 30 min |

---

## Concurrency & Transactions

The hard part — how Postgres handles concurrent access.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Transactions](03-transactions-and-replication/20.4.3.01-transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels (read committed, repeatable read, serializable) | 30 min |
| 07 | [Deadlocks](03-transactions-and-replication/20.4.3.02-deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies, lock ordering | 20 min |
| 08 | [Optimistic & Pessimistic Locking](03-transactions-and-replication/20.4.3.03-optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks, SELECT FOR UPDATE | 25 min |
| 22 | [Database Replication](03-transactions-and-replication/20.4.3.04-database-replication.md) | Streaming vs logical, read replicas, Patroni failover, replication lag, conflict resolution | 30 min |

---

## Operations & Scaling

Production concerns — keeping the database healthy at scale.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 09 | [Connection Pooling](05-operations-and-scaling/20.4.5.01-connection-pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling, prepared statements | 25 min |
| 13 | [Migration Strategies](05-operations-and-scaling/20.4.5.02-migration-strategies.md) | Expand/contract, lock-free migrations, backfills, zero-downtime, blue-green DB | 30 min |
| 15 | [Soft Delete & Tombstones](05-operations-and-scaling/20.4.5.03-soft-delete-and-tombstones.md) | `deleted_at` columns, partial indexes, GDPR right-to-erasure, CDC tombstones, log compaction retention | 20 min |
| 14 | [Interview Questions](05-operations-and-scaling/20.4.5.06-interview-questions.md) | 50+ curated questions with answers | 3 hrs |

---

## ORM & Specialized Features

Prisma + Postgres-specific features.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 10 | [Prisma](04-orm-and-access/20.4.4.01-prisma.md) | Schema, migrations, queries, relations, middleware, performance | 30 min |
| 19 | [Prisma Advanced](04-orm-and-access/20.4.4.02-prisma-advanced.md) | Interactive transactions, raw queries, performance optimization, multi-tenancy, schema patterns | 30 min |
| 17 | [Window Functions](02-querying-and-optimization/20.4.2.04-window-functions.md) | ROW_NUMBER, RANK, LAG, LEAD, aggregate OVER, running totals, moving averages | 25 min |
| 18 | [JSONB](02-querying-and-optimization/20.4.2.05-jsonb.md) | Operators, indexing, containment queries, aggregation, real-world patterns | 25 min |

---

## Suggested Study Order

### Path A — Backend new, prepping for senior (2-3 weeks)
1. PostgreSQL Fundamentals (5 files, ~2.5 hrs)
2. Querying & Optimization (3 files, ~1.5 hrs)
3. Concurrency & Transactions (3 files, ~2 hrs)
4. Prisma basics (1.5 hrs)
5. Operations & Scaling (3 files, ~1.5 hrs)
6. Specialized features (JSONB, window functions, soft delete) — as needed
7. Interview Questions (3 hrs)

### Path B — Senior, refresher (1-2 days)
1. MVCC + Transactions + Locking (1.5 hrs)
2. Indexes + Execution Plans (1 hr)
3. Replication + Connection Pooling (1 hr)
4. Migration Strategies (45 min)
5. Interview Questions (focus on the 20 harder Qs)

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- Re-read MVCC + Transactions
- Run through 50+ Interview Questions

---

## Cross-References

- [REST APIs](../20.3-rest-apis/INDEX.md) — pagination, error handling
- [System Design](../../30-architecture/30.2-system-design/INDEX.md) — CAP, sharding, replication
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — DB query performance
- [Microservices (polyglot persistence)](../20.6-microservices/INDEX.md) — DB-per-service, saga, outbox

---

## Navigation

[← Previous: REST APIs](../20.3-rest-apis/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Security →](../20.5-security/INDEX.md)
