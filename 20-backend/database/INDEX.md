# Database — Index

> **15 files** — Database fundamentals from PostgreSQL internals to indexing, transactions, MVCC, joins, locking, connection pooling, Prisma, execution plans, SQL vs NoSQL, zero-downtime migrations, and interview questions.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data-8b5cf6)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

| # | File | Topics |
|---|------|--------|
| 01 | [PostgreSQL](postgresql.md) | Architecture, WAL, vacuum, configuration, extensions |
| 02 | [Normalization](normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization, trade-offs |
| 03 | [Indexes](indexes.md) | B-tree, hash, GiST, GIN, composite indexes, index-only scans |
| 04 | [Transactions](transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels |
| 05 | [MVCC](mvcc.md) | Multiversion concurrency control, visibility rules, tuple versions |
| 06 | [Joins](joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins |
| 07 | [Deadlocks](deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies |
| 08 | [Optimistic & Pessimistic Locking](optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks |
| 09 | [Connection Pooling](connection-pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling |
| 10 | [Prisma](prisma.md) | Schema, migrations, queries, relations, middleware, performance |
| 11 | [Execution Plans](execution-plans.md) | EXPLAIN ANALYZE, sequential vs index scans, cost estimation |
| 13 | [SQL vs NoSQL](nosql-vs-sql.md) | Workload fit, CAP, consistency models, polyglot persistence |
| 14 | [Migration Strategies](migration-strategies.md) | Expand/contract, lock-free migrations, backfills, zero-downtime |
| 15 | [Interview Questions](interview-questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [REST APIs](../rest-api/INDEX.md) | [System Design](../../architecture/system-design/INDEX.md) | [Performance Monitoring](../../quality/performance-monitoring/INDEX.md) | [Microservices (polyglot persistence)](../../backend/INDEX.md)
---

## Navigation

[← Previous: REST APIs](../rest-api/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Security →](../security/INDEX.md)
