# Database — Index

> **24 files** — Database fundamentals from PostgreSQL internals to indexing, transactions, MVCC, joins, locking, connection pooling, Prisma (plus the ORM/query-builder landscape), execution plans, SQL vs NoSQL, zero-downtime migrations, soft delete & tombstones, backups/PITR recovery, search infrastructure at scale, window functions, JSONB, replication, row-level security, and interview questions.

[![Files](https://img.shields.io/badge/files-24-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Data-8b5cf6)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why databases are non-negotiable:** Every senior backend interview tests database knowledge. Schema design, indexing, transactions, locking, connection pooling, query optimization — these are table stakes. This section is the canonical reference for PostgreSQL + Prisma, the most common stack at product-based companies.

---

## Topic Categories

The 24 files are organized into 5 categories, each with its own INDEX.

| Category | Files | Why it matters |
| ---------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------ |
| [PostgreSQL Foundations](01-postgresql-foundations/INDEX.md) | 6 | How Postgres works under the hood — every backend interview starts here |
| [Querying & Optimization](02-querying-and-optimization/INDEX.md) | 5 | Indexes, joins, execution plans, window functions, JSONB — the day-to-day performance work |
| [Transactions & Replication](03-transactions-and-replication/INDEX.md) | 4 | MVCC, transactions, locking, deadlocks — the hard part |
| [ORM & Access](04-orm-and-access/INDEX.md) | 3 | Prisma fundamentals and advanced patterns, plus the access-layer decision tree |
| [Operations & Scaling](05-operations-and-scaling/INDEX.md) | 6 | Connection pooling, migrations, soft delete, backups/PITR, search infra, interview bank |

---

## The Flow

```text
01 POSTGRES FOUNDATIONS ──→ 02 QUERYING & OPT ──→ 03 TRANSACTIONS ──→ 04 ORM ───────→ 05 OPERATIONS
architecture/WAL/vacuum     indexes              MVCC                 prisma        connection pooling
normalization               joins                transactions         prisma adv    migrations
MVCC                        execution plans      deadlocks            landscape     soft delete
SQL vs NoSQL                window functions     locking                            backups/PITR
performance                 JSONB                replication                        search infra
```

---

## PostgreSQL Foundations

How Postgres actually works. Every backend interview starts here. Category INDEX: [PostgreSQL Foundations](01-postgresql-foundations/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [PostgreSQL](01-postgresql-foundations/20.4.1.01-postgresql.md) | Architecture, WAL, vacuum, configuration, extensions, autovacuum | 30 min |
| 02 | [Normalization](01-postgresql-foundations/20.4.1.02-normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization trade-offs, when to denormalize | 25 min |
| 03 | [MVCC](01-postgresql-foundations/20.4.1.03-mvcc.md) | Multiversion concurrency control, visibility rules, tuple versions, vacuum | 30 min |
| 04 | [SQL vs NoSQL](01-postgresql-foundations/20.4.1.04-nosql-vs-sql.md) | Workload fit, CAP, consistency models, polyglot persistence, when to use what | 25 min |
| 05 | [PostgreSQL Performance](01-postgresql-foundations/20.4.1.05-postgresql-performance.md) | Connection tuning, memory tuning, query optimization, VACUUM, partitioning, monitoring queries | 30 min |

---

## Querying & Optimization

Making queries fast. Category INDEX: [Querying & Optimization](02-querying-and-optimization/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Indexes](02-querying-and-optimization/20.4.2.01-indexes.md) | B-tree, hash, GiST, GIN, BRIN, composite indexes, index-only scans, partial indexes | 30 min |
| 02 | [Joins](02-querying-and-optimization/20.4.2.02-joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins, join order | 25 min |
| 03 | [Execution Plans](02-querying-and-optimization/20.4.2.03-execution-plans.md) | EXPLAIN ANALYZE, sequential vs index scans, cost estimation, statistics | 30 min |
| 04 | [Window Functions](02-querying-and-optimization/20.4.2.04-window-functions.md) | ROW_NUMBER, RANK, LAG, LEAD, aggregate OVER, running totals, moving averages | 25 min |
| 05 | [JSONB](02-querying-and-optimization/20.4.2.05-jsonb.md) | Operators, indexing, containment queries, aggregation, real-world patterns | 25 min |

---

## Transactions & Replication

The hard part — how Postgres handles concurrent access. Category INDEX: [Transactions & Replication](03-transactions-and-replication/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Transactions](03-transactions-and-replication/20.4.3.01-transactions.md) | ACID, BEGIN/COMMIT, SAVEPOINT, isolation levels (read committed, repeatable read, serializable) | 30 min |
| 02 | [Deadlocks](03-transactions-and-replication/20.4.3.02-deadlocks.md) | Detection, prevention, timeout-based resolution, retry strategies, lock ordering | 20 min |
| 03 | [Optimistic & Pessimistic Locking](03-transactions-and-replication/20.4.3.03-optimistic-pessimistic-locking.md) | Version-based locking, row-level locking, advisory locks, SELECT FOR UPDATE | 25 min |
| 04 | [Database Replication](03-transactions-and-replication/20.4.3.04-database-replication.md) | Streaming vs logical, read replicas, Patroni failover, replication lag, conflict resolution | 30 min |

---

## ORM & Access

Prisma. Category INDEX: [ORM & Access](04-orm-and-access/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Prisma](04-orm-and-access/20.4.4.01-prisma.md) | Schema, migrations, queries, relations, middleware, performance | 30 min |
| 02 | [Prisma Advanced](04-orm-and-access/20.4.4.02-prisma-advanced.md) | Interactive transactions, raw queries, performance optimization, multi-tenancy, schema patterns | 30 min |
| 03 | [ORM & Query Builder Landscape](04-orm-and-access/20.4.4.03-orm-query-builder-landscape.md) | Prisma vs Drizzle vs TypeORM vs Knex vs raw decision tree, type-safety spectrum, migration tooling comparison | 25 min |

---

## Operations & Scaling

Production concerns — keeping the database healthy at scale. Category INDEX: [Operations & Scaling](05-operations-and-scaling/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Connection Pooling](05-operations-and-scaling/20.4.5.01-connection-pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling, prepared statements | 25 min |
| 02 | [Migration Strategies](05-operations-and-scaling/20.4.5.02-migration-strategies.md) | Expand/contract, lock-free migrations, backfills, zero-downtime, blue-green DB | 30 min |
| 03 | [Soft Delete & Tombstones](05-operations-and-scaling/20.4.5.03-soft-delete-and-tombstones.md) | `deleted_at` columns, partial indexes, GDPR right-to-erasure, CDC tombstones, log compaction retention | 20 min |
| 04 | [Backups, PITR & Recovery](05-operations-and-scaling/20.4.5.04-backups-pitr-recovery.md) | `pg_dump` vs physical backups, WAL archiving, PITR (`recovery_target_time`), pgBackRest/WAL-G, RPO/RTO, restore drills, cross-region copies | 30 min |
| 05 | [Search Infrastructure at Scale](05-operations-and-scaling/20.4.5.05-search-infrastructure-at-scale.md) | Postgres FTS ceiling (GIN/tsvector), Elasticsearch/OpenSearch vs Meilisearch/Typesense, CDC/outbox sync, BM25 tuning, multilingual analysis | 30 min |
| 06 | [Interview Questions](05-operations-and-scaling/20.4.5.06-interview-questions.md) | 50+ curated questions with answers | 3 hrs |

---

## Suggested Study Order

### Path A — Backend new, prepping for senior (2-3 weeks)
1. PostgreSQL Foundations (6 files, ~2.5 hrs)
2. Querying & Optimization (5 files, ~2 hrs)
3. Transactions & Replication (4 files, ~2 hrs)
4. ORM landscape + Prisma basics (2 hrs)
5. Operations & Scaling (6 files, ~2.5 hrs)
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

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Schema & models | `packages/db/prisma/schema.prisma` (workspace package `@workspace/db`) - the full data model with `@@index` declarations |
| Migrations | `packages/db/prisma/migrations/` - versioned schema migrations |
| Transactions | `apps/api/src/prisma/transaction-runner.ts` + `shared/common/database-transaction-options.ts`; outbox rows append inside the same `prisma.$transaction` as the business write |
| Index & query tuning | `apps/api/src/shared/modules/database/database-index-optimization.service.ts` - index suggestions against real query patterns |
| Pooling | `apps/api/src/shared/modules/database/database-pooling.service.ts` - connection pool management for Prisma |
| Slow queries | `apps/api/src/shared/modules/database/slow-query-logging.service.ts` - logs + surfaces slow statements |
| Repository pattern | `apps/api/src/shared/common/repositories/` (base.repository.ts) + per-domain `infrastructure/repositories/prisma-*.ts` - DB access behind interfaces |
| Multi-tenant RLS | `apps/api/src/shared/modules/rls/` - `rls.service.ts` + `apply-rls-scope.ts` scoping every query to the clinic tenant |
| Backups | `apps/api/src/shared/modules/database/database-backup.service.ts` |
| Replication / read replicas | No read-replica fan-out - single managed Postgres (see `shared/modules/database/database-rds.service.ts`) |
