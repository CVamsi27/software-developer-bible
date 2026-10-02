# PostgreSQL Foundations - Database

> **Study time:** ≈ 1 h 34 m of reading (7 files, ~13 min average).
> **7 files.** How Postgres works under the hood: architecture and WAL, normalization, MVCC, SQL vs NoSQL trade-offs, performance tuning, and row-level security. Every backend interview starts here.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-PostgreSQL%20Foundations-8b5cf6)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [PostgreSQL](20.4.1.01-postgresql.md) | Architecture, WAL, vacuum, configuration, extensions, autovacuum | 23 min |
| 02 | [Normalization](20.4.1.02-normalization.md) | 1NF, 2NF, 3NF, BCNF, denormalization trade-offs, when to denormalize | 19 min |
| 03 | [MVCC](20.4.1.03-mvcc.md) | Multiversion concurrency control, visibility rules, tuple versions, vacuum | 17 min |
| 04 | [SQL vs NoSQL](20.4.1.04-nosql-vs-sql.md) | Workload fit, CAP, consistency models, polyglot persistence, when to use what | 9 min |
| 05 | [PostgreSQL Performance](20.4.1.05-postgresql-performance.md) | Connection tuning, memory tuning, query optimization, VACUUM, partitioning, monitoring queries | 12 min |
| 06 | [Row-Level Security](20.4.1.06-row-level-security.md) | RLS policies, tenant isolation, session variables, defense-in-depth, multi-tenant SaaS | 11 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Schema as source of truth | `packages/db/prisma/schema.prisma` - canonical 149-model schema, `pg_trgm` extension, clinicId tenancy columns |
| Connections | `apps/api/src/prisma/prisma.service.ts` - Prisma over a `pg` Pool (@prisma/adapter-pg) with UTC session config |
| Performance tooling | `apps/api/src/shared/modules/database/slow-query-logging.service.ts` - Prisma query-event listener logs slow statements |
| Row-Level Security | `apps/api/src/shared/modules/tenant/tenant-context.middleware.ts` - sets `app.current_tenant` session variable for RLS |

MVCC/vacuum tuning is delegated to managed Postgres; the SQL-vs-NoSQL question is answered — relational all the way for clinical data.
---

[Next: Querying & Optimization →](../02-querying-and-optimization/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
