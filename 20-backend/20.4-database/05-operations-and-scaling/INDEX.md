# Operations & Scaling - Database

> **Study time:** ≈ 1 h 34 m of reading (6 files, ~16 min average).
> **6 files.** Keeping the database healthy at scale: connection pooling, zero-downtime migrations, soft delete & tombstones, backups/PITR recovery, search infrastructure at scale — plus the interview question bank.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Operations%20%26%20Scaling-8b5cf6)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Connection Pooling](20.4.5.01-connection-pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling, prepared statements | 18 min |
| 02 | [Migration Strategies](20.4.5.02-migration-strategies.md) | Expand/contract, lock-free migrations, backfills, zero-downtime, blue-green DB | 11 min |
| 03 | [Soft Delete & Tombstones](20.4.5.03-soft-delete-and-tombstones.md) | `deleted_at` columns, partial indexes, GDPR right-to-erasure, CDC tombstones, log compaction retention | 22 min |
| 04 | [Backups, PITR & Recovery](20.4.5.04-backups-pitr-recovery.md) | `pg_dump` vs physical backups, WAL archiving, `recovery_target_time` PITR, pgBackRest/WAL-G, RPO/RTO targets, restore drills, retention, cross-region copies | 12 min |
| 05 | [Search Infrastructure at Scale](20.4.5.05-search-infrastructure-at-scale.md) | Postgres FTS ceiling (GIN/tsvector), Elasticsearch/OpenSearch vs Meilisearch/Typesense, CDC/outbox index sync, BM25 relevance tuning, multilingual analysis | 11 min |
| 06 | [Interview Questions](20.4.5.06-interview-questions.md) | 50+ curated questions with answers | 20 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Connection pooling | `apps/api/src/shared/modules/database/database-pooling.service.ts` - min/max/idle/maxUses pool policy |
| Migrations | `packages/db/prisma/migrations/` - 165 ordered Prisma migrations |
| Backups | `apps/api/src/shared/modules/database/database-backup.service.ts` - spawned pg_dump, retention window, Prometheus metrics |
| Soft delete | `apps/api/src/shared/common/prisma/active-user.filter.ts` - `deletedAt: null` filter keeps tombstoned users out of reads |
| Search infrastructure | `apps/api/src/shared/modules/search/strategies/search-strategy.base.ts` - strategy-per-entity search on Postgres full-text |

The interview bank above is answerable entirely from these files plus the slow-query logging service.
---

[← Previous: ../04 Orm And Access/index](../04-orm-and-access/INDEX.md)
