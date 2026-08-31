# PostgreSQL Foundations - Database

> **5 files.** How Postgres works under the hood: architecture and WAL, normalization, MVCC, SQL vs NoSQL trade-offs, and performance tuning. Every backend interview starts here.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-PostgreSQL%20Foundations-8b5cf6)](../INDEX.md)

---

## Files

| Order | File                                                          | Topics                                                                                         | Read time |
| --   :  | ------                                                          | --------                                                                                         | ----------: |
| 01    | [PostgreSQL](20.4.1.01-postgresql.md)                         | Architecture, WAL, vacuum, configuration, extensions, autovacuum                               | 30 min    |
| 02    | [Normalization](20.4.1.02-normalization.md)                   | 1NF, 2NF, 3NF, BCNF, denormalization trade-offs, when to denormalize                           | 25 min    |
| 03    | [MVCC](20.4.1.03-mvcc.md)                                     | Multiversion concurrency control, visibility rules, tuple versions, vacuum                     | 30 min    |
| 04    | [SQL vs NoSQL](20.4.1.04-nosql-vs-sql.md)                     | Workload fit, CAP, consistency models, polyglot persistence, when to use what                  | 25 min    |
| 05    | [PostgreSQL Performance](20.4.1.05-postgresql-performance.md) | Connection tuning, memory tuning, query optimization, VACUUM, partitioning, monitoring queries | 30 min    |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic                     | Docita evidence                                                                                                         |
| -------                     | -----------------                                                                                                         |
| Schema as source of truth | `packages/db/prisma/schema.prisma` - canonical 149-model schema, `pg_trgm` extension, clinicId tenancy columns          |
| Connections               | `apps/api/src/prisma/prisma.service.ts` - Prisma over a `pg` Pool (@prisma/adapter-pg) with UTC session config          |
| Performance tooling       | `apps/api/src/shared/modules/database/slow-query-logging.service.ts` - Prisma query-event listener logs slow statements |

MVCC/vacuum tuning is delegated to managed Postgres; the SQL-vs-NoSQL question is answered — relational all the way for clinical data.
