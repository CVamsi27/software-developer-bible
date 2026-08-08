# Database — Index

> **15 files** — Database fundamentals from PostgreSQL internals to indexing, transactions, MVCC, joins, locking, connection pooling, Prisma, execution plans, SQL vs NoSQL, zero-downtime migrations, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-green)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

| # | File | Topics |
|---|------|--------|
| 01 | [PostgreSQL](01-PostgreSQL.md) | Architecture, WAL, vacuum, configuration, extensions |
| 02 | [Normalization](02-Normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization, trade-offs |
| 03 | [Indexes](03-Indexes.md) | B-tree, hash, GiST, GIN, composite indexes, index-only scans |
| 04 | [Transactions](04-Transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels |
| 05 | [MVCC](05-MVCC.md) | Multiversion concurrency control, visibility rules, tuple versions |
| 06 | [Joins](06-Joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins |
| 07 | [Deadlocks](07-Deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies |
| 08 | [Optimistic & Pessimistic Locking](08-Optimistic-Pessimistic-Locking.md) | Version-based locking, row-level locking, advisory locks |
| 09 | [Connection Pooling](09-Connection-Pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling |
| 10 | [Prisma](10-Prisma.md) | Schema, migrations, queries, relations, middleware, performance |
| 11 | [Execution Plans](11-Execution-Plans.md) | EXPLAIN ANALYZE, sequential vs index scans, cost estimation |
| 13 | [SQL vs NoSQL](13-NoSQL-vs-SQL.md) | Workload fit, CAP, consistency models, polyglot persistence |
| 14 | [Migration Strategies](14-Migration-Strategies.md) | Expand/contract, lock-free migrations, backfills, zero-downtime |
| 15 | [Interview Questions](15-Interview-Questions.md) | 50+ curated questions with answers |

---

**Cross-references:** [REST APIs](../07-REST-API/) | [System Design](../11-System-Design/) | [Performance Monitoring](../26-Performance-Monitoring/) | [Microservices (polyglot persistence)](../12-Microservices/)
---

## Navigation

[← Previous: REST APIs](../07-REST-API/INDEX.md) · [🏠 Back to Index](../INDEX.md) · [Next: Security →](../09-Security/INDEX.md)
