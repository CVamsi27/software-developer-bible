# Database — Index

> **18 files** — Database fundamentals from PostgreSQL internals to indexing, transactions, MVCC, joins, locking, connection pooling, Prisma, execution plans, SQL vs NoSQL, zero-downtime migrations, soft delete & tombstones, Redis, window functions, JSONB, and interview questions.

[![Files](https://img.shields.io/badge/files-18-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data-8b5cf6)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

| # | File | Topics |
|---|------|--------|
| 01 | [PostgreSQL](20.4.01-postgresql.md) | Architecture, WAL, vacuum, configuration, extensions |
| 02 | [Normalization](20.4.02-normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization, trade-offs |
| 03 | [Indexes](20.4.03-indexes.md) | B-tree, hash, GiST, GIN, composite indexes, index-only scans |
| 04 | [Transactions](20.4.04-transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels |
| 05 | [MVCC](20.4.05-mvcc.md) | Multiversion concurrency control, visibility rules, tuple versions |
| 06 | [Joins](20.4.06-joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins |
| 07 | [Deadlocks](20.4.07-deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies |
| 08 | [Optimistic & Pessimistic Locking](20.4.08-optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks |
| 09 | [Connection Pooling](20.4.09-connection-pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling |
| 10 | [Prisma](20.4.10-prisma.md) | Schema, migrations, queries, relations, middleware, performance |
| 11 | [Execution Plans](20.4.11-execution-plans.md) | EXPLAIN ANALYZE, sequential vs index scans, cost estimation |
| 13 | [SQL vs NoSQL](20.4.12-nosql-vs-sql.md) | Workload fit, CAP, consistency models, polyglot persistence |
| 14 | [Migration Strategies](20.4.13-migration-strategies.md) | Expand/contract, lock-free migrations, backfills, zero-downtime |
| 14 | [Interview Questions](20.4.14-interview-questions.md) | 50+ curated questions with answers |
| 15 | [Soft Delete & Tombstones](20.4.15-soft-delete-and-tombstones.md) | `deleted_at` columns, partial indexes, GDPR right-to-erasure, CDC tombstones, log compaction retention |
| 16 | [Redis](20.4.16-redis.md) | Data structures, caching patterns, rate limiting, distributed locks, pub/sub |
| 17 | [Window Functions](20.4.17-window-functions.md) | ROW_NUMBER, RANK, LAG, LEAD, aggregate OVER, running totals, moving averages |
| 18 | [JSONB](20.4.18-jsonb.md) | Operators, indexing, containment queries, aggregation, real-world patterns |
| 19 | [Prisma Advanced](20.4.19-prisma-advanced.md) | Interactive transactions, raw queries, performance optimization, multi-tenancy, schema patterns (soft delete, audit trail, versioning) |

---

**Cross-references:** [REST APIs](../20.3-rest-apis/INDEX.md) | [System Design](../../30-architecture/30.2-system-design/INDEX.md) | [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) | [Microservices (polyglot persistence)](../20.6-microservices/INDEX.md)
---

## Navigation

[← Previous: REST APIs](../20.3-rest-apis/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Security →](../20.5-security/INDEX.md)
