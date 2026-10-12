# Operations & Scaling - Database

> **Study time:** ≈ 1 h 3 m of reading (7 files, ~9 min average).
> **7 files.** Keeping the database healthy at scale: connection pooling, zero-downtime migrations, soft delete & tombstones, backups/PITR recovery, search infrastructure at scale — plus the interview question bank.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Operations%20%26%20Scaling-8b5cf6)](../INDEX.md)

---

## Learning Flow

Start with transaction, locking and WAL basics from the foundations/transactions categories. Then follow the operational ownership changes:

1. Bound connection borrowers and keep each transaction on one session.
2. Change a representation while old/new application versions coexist; verify writer ownership and backfill completeness.
3. Follow deletion through restoration, conflicting keys, delayed jobs and derived-store cleanup.
4. Recover a reachable historical state and reconcile excluded work before exposing a restored service.
5. Build search as a useful projection with explicit visibility, ordering and rebuild contracts.
6. Use the [revision companion](REVISION.md) to explain the traces and changed conditions.
7. Attempt the interview bank after you can reason through each operational boundary.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Connection Pooling](20.4.5.01-connection-pooling.md) | PgBouncer, connection lifecycle, pool sizing, transaction pooling, prepared statements | Important | Important | 10 min |
| 02 | [Migration Strategies](20.4.5.02-migration-strategies.md) | Expand/contract, lock-aware migrations, backfills, zero-downtime, blue-green DB | Important | Important | 9 min |
| 03 | [Soft Delete & Tombstones](20.4.5.03-soft-delete-and-tombstones.md) | `deleted_at` columns, partial indexes, GDPR right-to-erasure, CDC tombstones, log compaction retention | Essential | Foundational | 11 min |
| 04 | [Backups, PITR & Recovery](20.4.5.04-backups-pitr-recovery.md) | `pg_dump` vs physical backups, WAL archiving, incremental backup dependencies, `recovery_target_time` PITR, RPO/RTO targets and restore drills | Important | Important | 10 min |
| 05 | [Search Infrastructure at Scale](20.4.5.05-search-infrastructure-at-scale.md) | Term analysis, PostgreSQL matching/ranking, measured engine choice, item/task outcomes, ordered deletion, snapshot/replay rebuilds | Essential | Foundational | 11 min |
| Revision | [Revision](REVISION.md) | Explain pool wait, schema/backfill races, deletion generations, restore boundaries and search ordering | Essential | Foundational | 4 min |
| 06 | [Interview Questions](20.4.5.06-interview-questions.md) | Authored database questions with mechanism and changed-condition follow-ups | Essential | Foundational | 8 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

The [Docita case study](../../../projects/docita/INDEX.md) provides implementation pointers to inspect against these contracts. Paths describe examples to examine; they do not establish current deployment or restore/freshness guarantees.

| Topic | Docita evidence |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Connection pooling | `apps/api/src/shared/modules/database/database-pooling.service.ts` - min/max/idle/maxUses pool policy |
| Migrations | `packages/db/prisma/migrations/` - inspect ordering and compatibility gates |
| Backups | `apps/api/src/shared/modules/database/database-backup.service.ts` - spawned pg_dump, retention window, Prometheus metrics |
| Soft delete | `apps/api/src/shared/common/prisma/active-user.filter.ts` - `deletedAt: null` filter keeps tombstoned users out of reads |
| Search infrastructure | `apps/api/src/shared/modules/search/strategies/search-strategy.base.ts` - strategy-per-entity search on Postgres full-text |

Use the learning chapters for the interview explanations. Case-study code still needs current runtime and operational evidence for any claimed production guarantee.
---

[← Previous: ORM & Access](../04-orm-and-access/INDEX.md)
