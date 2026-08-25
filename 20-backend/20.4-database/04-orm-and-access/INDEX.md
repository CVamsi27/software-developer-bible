# ORM & Access - Database

> **3 files.** Prisma from first principles to advanced patterns: schema and migrations, then interactive transactions, raw queries, multi-tenancy, and schema patterns — plus the full access-layer landscape (Prisma vs Drizzle vs TypeORM vs Knex vs raw SQL) with a decision tree.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-ORM%20%26%20Access-8b5cf6)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Prisma](20.4.4.01-prisma.md) | Schema, migrations, queries, relations, middleware, performance | 30 min |
| 02 | [Prisma Advanced](20.4.4.02-prisma-advanced.md) | Interactive transactions, raw queries, performance optimization, multi-tenancy, schema patterns | 30 min |
| 03 | [ORM & Query Builder Landscape](20.4.4.03-orm-query-builder-landscape.md) | Prisma vs Drizzle vs TypeORM vs Knex vs raw decision tree, type-safety spectrum, migration tooling comparison, when NOT to use Prisma, team adoption | 25 min |

---

[← Back to Database](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
|-------|-----------------|
| Client composition | `apps/api/src/prisma/prisma.service.ts` - `$extends` stack: tenant, encryption, audit-immutability, rls-routing, slow-query, query-budget |
| Multi-tenancy scoping | `apps/api/src/shared/common/extensions/tenant-scope-policy.ts` - per-model rules force clinicId filters |
| Transparent field encryption | `apps/api/src/shared/common/extensions/encryption.extension.ts` - encrypt/decrypt on patient fields inside the query pipeline |
| Repository pattern | `apps/api/src/shared/common/repositories/base.repository.ts` - abstract BaseRepository (pagination + where builders) under every repo |

The ORM landscape decision is made: Prisma everywhere; no Drizzle/TypeORM/Knex in the workspace.
