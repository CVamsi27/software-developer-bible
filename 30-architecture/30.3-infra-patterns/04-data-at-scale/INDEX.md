# Data at Scale

> **Study time:** ≈ 45 min of reading (5 files, ~9 min average).
> **5 files.** Scaling the data layer once your single Postgres stops being enough: database scaling levers, data pipelines that move and transform data continuously, CDN architecture that pushes reads to the edge, and multi-tenant SaaS architecture patterns.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Data%20at%20Scale-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Vertical scaling buys you months, not years. At real scale you need to know which lever to pull — replicas for read load, partitioning for write load, caching for hot keys — and how data flows between systems: batch vs streaming pipelines, medallion architectures, edge delivery. These three chapters are the operational counterpart to system-design theory.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Database Scaling](30.3.4.01-database-scaling.md) | Read replicas, vertical vs horizontal scaling, partitioning, connection pooling, scaling levers in order | 9 min |
| 02 | [Data Pipelines](30.3.4.02-data-pipelines.md) | ETL vs ELT vs streaming, Bronze/Silver/Gold framing, batch vs stream trade-offs, pipeline reliability | 16 min |
| 03 | [CDN Architecture](30.3.4.03-cdn-architecture.md) | Edge caching strategy, PoPs, cache keys, invalidation (also: [40.10-cdn](../../../40-platform/40.10-cdn/INDEX.md)) | 12 min |
| 04 | [Multi-Tenant SaaS Architecture](30.3.4.04-multi-tenant-saas-architecture.md) | Shared vs separate schemas, tenant context propagation, RLS defense-in-depth, noise neighbors, per-tenant caching | 6 min |

---

## Reading Path and Completion Check

Measure the database bottleneck first. Read pipelines and CDN caching as different data paths, then apply tenant isolation across their repositories, caches and workers.

Explain which bottleneck each added component removes and how consistency, authorization and recovery remain enforced. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [System Design Theory](../../30.2-system-design/01-theory/INDEX.md) — sharding & replication, caching patterns in depth
- [Database Stack](../../../20-backend/20.4-database/INDEX.md) — PostgreSQL-level mechanics
- [Coordination](../03-coordination/INDEX.md) — who runs the pipeline

---

## Navigation

[← Coordination](../03-coordination/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Shipping & Evolution →](../05-shipping-and-evolution/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — manages data growth for real.

| Topic | Docita evidence |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Backups | `shared/modules/database/database-backup.service.ts` (+ spec) |
| Retention & archival | `compliance/data-retention.scheduler.ts` (+ spec); DPDP compliance docs in `docs/compliance/*` |
| Query hygiene at scale | `slow-query-logging.service.ts`, `database-index-optimization.service.ts`, connection pooling service |
| Scaling posture | Deliberate single-region Postgres (ADR 0006) + read-base repositories (`prisma-read-base.ts`) |
| Sharding / pipelines / replicas | _No direct docita implementation yet._ |
