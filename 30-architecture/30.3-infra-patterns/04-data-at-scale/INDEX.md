# Data at Scale

> **Study time:** ≈ 38 min of reading (5 files, ~8 min average).
> **5 files.** Scale measured data paths: database capacity levers, batch and streaming pipelines, CDN reuse and invalidation under access rules, and multi-tenant SaaS patterns.

[![Files](https://img.shields.io/badge/files-5-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Data%20at%20Scale-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Measure resource and consistency requirements before choosing a lever. Replicas can distribute eligible reads; partitioning can prune queries and simplify retention within one server; caches reuse eligible responses. Pipelines add useful copies and recovery contracts, while tenant isolation must cover every path. These chapters connect theory to those operational boundaries.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Database Scaling](30.3.4.01-database-scaling.md) | Read replicas, vertical vs horizontal scaling, partitioning, connection pooling, measured bottlenecks and independent levers | Important | Specialized | 11 min |
| 02 | [Data Pipelines](30.3.4.02-data-pipelines.md) | ETL vs ELT vs streaming, Bronze/Silver/Gold framing, batch vs stream trade-offs, pipeline reliability | Important | Specialized | 10 min |
| 03 | [CDN Architecture](30.3.4.03-cdn-architecture.md) | Edge reuse, cache identity, authorization, freshness, origin load and invalidation (provider examples: [40.10-cdn](../../../40-platform/40.10-cdn/INDEX.md)) | Important | Specialized | 7 min |
| 04 | [Multi-Tenant SaaS Architecture](30.3.4.04-multi-tenant-saas-architecture.md) | Pool, bridge and silo choices; verified tenant context; database, cache, storage and job boundaries; lifecycle and noisy-neighbor controls | Important | Specialized | 7 min |

---

## Reading Path and Completion Check

Measure the database bottleneck first. Read pipelines and CDN caching as different data paths, then trace one tenant's access and lifecycle through databases, caches, storage, jobs and operations.

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

Candidate implementation locations in [Docita](https://github.com/CVamsi27/docita). Source names and tests guide inspection; verify the actual checked-out revision/configuration and failure evidence before presenting them as deployed capacity or isolation proof.

| Topic | Docita evidence |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backups | `shared/modules/database/database-backup.service.ts` (+ spec) |
| Retention & archival | `apps/api/src/shared/modules/compliance/data-retention.scheduler.ts` (+ spec); DPDP compliance docs in `docs/compliance/*` |
| Query hygiene at scale | `slow-query-logging.service.ts`, `database-index-optimization.service.ts`, connection pooling service |
| Scaling posture | Deliberate single-region Postgres (ADR 0006) + read-base repositories (`prisma-read-base.ts`) |
| Sharding and replicas | No sharding implementation is established here. Read-routing abstractions are not proof of an enabled production replica; verify datasource configuration, lag and read-after-write behavior. |
