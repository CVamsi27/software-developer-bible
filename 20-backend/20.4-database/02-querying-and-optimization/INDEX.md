# Querying & Optimization - Database

> **5 files.** Making queries fast: index types (B-tree to BRIN), join algorithms, execution plans with `EXPLAIN ANALYZE`, window functions, and JSONB.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Querying%20%26%20Optimization-8b5cf6)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Indexes](20.4.2.01-indexes.md) | B-tree, hash, GiST, GIN, BRIN, composite indexes, index-only scans, partial indexes | 30 min |
| 02 | [Joins](20.4.2.02-joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins, join order | 25 min |
| 03 | [Execution Plans](20.4.2.03-execution-plans.md) | EXPLAIN ANALYZE, sequential vs index scans, cost estimation, statistics | 30 min |
| 04 | [Window Functions](20.4.2.04-window-functions.md) | ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, aggregate OVER, running totals, moving averages | 25 min |
| 05 | [JSONB](20.4.2.05-jsonb.md) | Operators (`->`, `->>`, `@>`, `?`), GIN indexing, containment queries, aggregation, real-world patterns | 25 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Indexes | `packages/db/prisma/schema.prisma` - composite `@@index([clinicId])` and friends on every tenanted model |
| Index ROI analysis | `apps/api/src/shared/modules/database/database-index-optimization.service.ts` - pg_stat scan/tuple counts flag dead indexes |
| Full-text / trigram support | `apps/api/src/shared/modules/search/search-full-text-support.service.ts` - runtime probe of Postgres FTS capability per entity |
| JSONB boundaries | `apps/api/src/shared/common/json/to-prisma-input-json-value.ts` - typed writer for JSONB columns |

_No EXPLAIN harness or window-function showcase yet_ — plan inspection is manual psql work today.
