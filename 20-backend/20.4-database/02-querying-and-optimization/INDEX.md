# Querying & Optimization - Database

> **Study time:** ≈ 51 min of reading (6 files, ~8 min average).
> **6 files.** Making queries fast: index types (B-tree to BRIN), join algorithms, execution plans with `EXPLAIN ANALYZE`, window functions, and JSONB.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Querying%20%26%20Optimization-8b5cf6)](../INDEX.md)

---

## Learning Flow

Start with relational keys, MVCC visibility and an explicit result requirement. Then study:

1. Match access methods, keys, predicates and visible-row retrieval to measured queries.
2. Construct the correct join pairs/grain before optimizing physical matching.
3. Read the chosen operator tree and observed work without confusing costs, loops or cache layers.
4. Preserve analytical input rows while choosing tie/order/frame and calendar policies.
5. Query variable JSON values with explicit type/null/mutation and operator-class contracts.
6. Use the [revision companion](REVISION.md) after the learning examples, then practice the operations interview bank.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| :---: | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 01 | [Indexes](20.4.2.01-indexes.md) | B-tree, hash, GiST, GIN, BRIN, composite indexes, index-only scans, partial indexes | Essential | Foundational | 9 min |
| 02 | [Joins](20.4.2.02-joins.md) | INNER, LEFT, RIGHT, FULL, CROSS, LATERAL, hash/merge/nested loop joins, join order | Essential | Foundational | 10 min |
| 03 | [Execution Plans](20.4.2.03-execution-plans.md) | EXPLAIN ANALYZE, row estimates and loops, buffers, PostgreSQL 18 generic plans/serialization | Essential | Foundational | 8 min |
| 04 | [Window Functions](20.4.2.04-window-functions.md) | ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, aggregate OVER, running totals, moving averages | Essential | Foundational | 10 min |
| 05 | [JSONB](20.4.2.05-jsonb.md) | Extraction, missing vs null, operator-compatible GIN, SQL/JSON `JSON_TABLE` (PostgreSQL 17+) | Essential | Foundational | 10 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

The [Docita case study](../../../projects/docita/INDEX.md) provides code pointers to inspect. These pointers do not establish current production behavior, query plans or index value without current evidence.

| Topic | Docita evidence |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Indexes | `packages/db/prisma/schema.prisma` - inspect tenant access paths and actual composite-key coverage |
| Index ROI analysis | `apps/api/src/shared/modules/database/database-index-optimization.service.ts` - pg_stat scan/tuple counts flag dead indexes |
| Full-text / trigram support | `apps/api/src/shared/modules/search/search-full-text-support.service.ts` - runtime probe of Postgres FTS capability per entity |
| JSONB boundaries | `apps/api/src/shared/common/json/to-prisma-input-json-value.ts` - typed writer for JSONB columns |

Inspect the actual case-study schema/query/runtime before claiming an access path or optimization. The chapter fixtures establish their own stated examples, independently of that application.
---

[← Previous: PostgreSQL Foundations](../01-postgresql-foundations/INDEX.md) · [Next: Transactions & Replication →](../03-transactions-and-replication/INDEX.md)
