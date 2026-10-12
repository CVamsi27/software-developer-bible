# ORM & Access - Database

> **Study time:** ≈ 35 min of reading (4 files, ~9 min average).
> **4 files.** Prisma from first principles to advanced patterns: schema and migrations, then interactive transactions, raw queries, multi-tenancy, and schema patterns — plus the full access-layer landscape (Prisma vs Drizzle vs TypeORM vs Knex vs raw SQL) with a decision tree.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-ORM%20%26%20Access-8b5cf6)](../INDEX.md)

---

## Reading flow

1. Read [Prisma fundamentals](20.4.4.01-prisma.md) to connect the versioned schema, generated client and migration to one bounded write/read.
2. Follow competing transfers and stock reservations in [Prisma Advanced](20.4.4.02-prisma-advanced.md). Locate the conditional mutation, transaction connection, outbox failure and tenant policy before choosing APIs.
3. Use [the access-layer landscape](20.4.4.03-orm-query-builder-landscape.md) to decide who owns query construction, mapping and migrations. Compare equivalent work rather than vendor labels.
4. Finish with [Revision](REVISION.md), explaining each failure boundary without looking at the implementation.

The executable Prisma examples pin Prisma CLI and Client 7.10.0 with PostgreSQL. As of 12 October 2026, Prisma ORM 8 is a release candidate, not a general-availability release; check the [current release status](https://www.prisma.io/docs/orm/release-status) before choosing a version or copying code.

## Chapter map

| Order | File | Topics | Role priority | General importance | Read time |
| ----- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [Prisma](20.4.4.01-prisma.md) | Schema, migrations, queries, relations, version contract, performance | Essential | Foundational | 13 min |
| 02 | [Prisma Advanced](20.4.4.02-prisma-advanced.md) | Interactive transactions, raw queries, performance optimization, multi-tenancy, schema patterns | Essential | Foundational | 11 min |
| 03 | [ORM & Query Builder Landscape](20.4.4.03-orm-query-builder-landscape.md) | Prisma vs Drizzle vs TypeORM vs Knex vs raw decision tree, type-safety spectrum, migration tooling comparison, when NOT to use Prisma, team adoption | Essential | Foundational | 9 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare platform (NestJS + Prisma + Postgres). These paths are inspection pointers; verify the current client versions, extensions and deployment before treating them as behavior evidence:

| Topic | Docita evidence |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Client composition | `apps/api/src/prisma/prisma.service.ts` - `$extends` stack: tenant, encryption, audit-immutability, rls-routing, slow-query, query-budget |
| Multi-tenancy scoping | `apps/api/src/shared/common/extensions/tenant-scope-policy.ts` - per-model rules force clinicId filters |
| Transparent field encryption | `apps/api/src/shared/common/extensions/encryption.extension.ts` - encrypt/decrypt on patient fields inside the query pipeline |
| Repository pattern | `apps/api/src/shared/common/repositories/base.repository.ts` - abstract BaseRepository (pagination + where builders) under every repo |

The ORM landscape decision is made: inspect the current dependencies and repository seams rather than assuming another ORM is absent from every module.
---

[← Previous: Transactions & Replication](../03-transactions-and-replication/INDEX.md) · [Next: Operations & Scaling →](../05-operations-and-scaling/INDEX.md)
