# PostgreSQL Foundations - Database

> **Study time:** ≈ 1 h 14 m of reading (7 files, ~11 min average).
> **7 files.** How PostgreSQL works under the hood: architecture and WAL, normalization, MVCC, SQL vs NoSQL trade-offs, performance tuning, and row-level security. This foundation supports the later querying, transaction and operations chapters.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-PostgreSQL%20Foundations-8b5cf6)](../INDEX.md)

---

## Reading flow

1. Start with PostgreSQL's request path: the client session owns transaction state, the backend executes SQL, and WAL supports crash recovery.
2. Design fact ownership with normalization. Trace keys and dependencies before choosing a normal form or a stored copy.
3. Read MVCC next: compare statement and transaction snapshots, then change an ordinary reader into a writer and explain the conflict.
4. Choose a database from the operation's access, atomicity and freshness requirements. Separate data model from product guarantees.
5. Diagnose performance from workload evidence and plans. Compare identical results before and after an access-path change.
6. Apply RLS after roles and transactions are clear. Trace verified tenant context through one connection and test both old-row visibility and new-row checks.
7. Use [revision](REVISION.md) to predict changed conditions, then continue to querying and transaction design before the [database interview bank](../05-operations-and-scaling/20.4.5.06-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| :---: | ------------------------------------------------------------- | ------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 01 | [PostgreSQL](20.4.1.01-postgresql.md) | Architecture, WAL, constraints, MVCC, vacuum, configuration | Essential | Foundational | 11 min |
| 02 | [Normalization](20.4.1.02-normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization trade-offs | Important | Important | 11 min |
| 03 | [MVCC](20.4.1.03-mvcc.md) | Statement and transaction snapshots, own writes, conflicts, cleanup | Important | Important | 14 min |
| 04 | [SQL vs NoSQL](20.4.1.04-nosql-vs-sql.md) | Workload fit, consistency, query shape, product guarantees | Essential | Foundational | 11 min |
| 05 | [PostgreSQL Performance](20.4.1.05-postgresql-performance.md) | Workload diagnosis, plans, memory, vacuum, partitioning | Essential | Foundational | 11 min |
| 06 | [Row-Level Security](20.4.1.06-row-level-security.md) | Policy composition, tenant context, roles, old/new row checks | Essential | Foundational | 11 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Use these [Docita](https://github.com/CVamsi27/docita) source paths as investigation leads. Verify each behavior in the current code and tests before describing it as deployed or effective:

| Topic | Docita evidence | Role priority | General importance |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| Schema as source of truth | `packages/db/prisma/schema.prisma` - canonical relational schema, `pg_trgm` extension, clinicId tenancy columns | Varies | Varies |
| Connections | `apps/api/src/prisma/prisma.service.ts` - Prisma over a `pg` Pool (@prisma/adapter-pg) with UTC session config | Varies | Varies |
| Performance tooling | `apps/api/src/shared/modules/database/slow-query-logging.service.ts` - Prisma query-event listener logs slow statements | Varies | Varies |
| Row-Level Security | `apps/api/src/shared/common/interceptors/tenant-context.interceptor.ts` — request tenant context; verify the actual transaction-local database setting and scoped client path in the [tenant case](../../../projects/docita/02-multi-tenancy-rls.md) | Essential | Important |

Managed PostgreSQL still requires workload-aware maintenance and operational ownership. Its presence does not establish effective vacuum settings or justify every possible data-model choice.
---

[Next: Querying & Optimization →](../02-querying-and-optimization/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
