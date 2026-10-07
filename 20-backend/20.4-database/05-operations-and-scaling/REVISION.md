<!-- section: Database | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Database — Operations And Scaling Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Connection Pooling

Source: [Connection Pooling](20.4.5.01-connection-pooling.md)

**Q:** Why reuse database connections instead of opening one for every request?

**A:** Opening a new database connection for every request adds setup cost and can overwhelm the server. A pool reuses a bounded set of connections; size it from measured concurrency, query time, and database capacity.

**Q:** Why can a smaller connection pool improve throughput?

**A:** More connections can increase contention and memory use without increasing useful query throughput. Start with a conservative pool and measure wait time, query latency, and database saturation; there is no universal cores-based formula.

**Q:** How do leaked connections and long transactions affect request latency?

**A:** Leaked connections, missing timeouts, and long transactions holding connections  all present as mysterious latency at p99, because waiting-for-connection time lands at the tail.

## Database Migrations & Zero-Downtime Schema Changes

Source: [Database Migrations & Zero-Downtime Schema Changes](20.4.5.02-migration-strategies.md)

**Q:** Why must a schema change work with both application versions during a rolling deployment?

**A:** Rolling deploys mean v1 and v2 of the app hit the same database simultaneously — so a breaking schema change (rename, drop, tighten) breaks whichever version is still running. Every safe-migration pattern is an answer to this.

**Q:** What does each phase of expand, migrate, and contract change?

**A:** add the new shape (expand, backward-compatible), backfill and switch code over (migrate), remove the old shape only when nothing reads it (contract). Three steps because coexistence is unavoidable.

**Q:** Why can a short ALTER TABLE statement still interrupt application traffic?

**A:** Even a fast metadata change needs a table lock and may wait behind a long transaction; some defaults or clauses also rewrite the table. Check PostgreSQL version and exact DDL, then test lock acquisition and rewrite behavior on representative data.

## Soft Delete & Tombstones

Source: [Soft Delete & Tombstones](20.4.5.03-soft-delete-and-tombstones.md)

**Q:** How does soft deletion change the ability to restore data and preserve references?

**A:** A hard delete may be irreversible for the application and may be blocked or cascaded by foreign keys. A `deleted_at` flag can support an undo flow, but every relevant query and unique constraint must account for inactive rows.

**Q:** What must ordinary queries do when a table uses soft deletion?

**A:** Queries that should show active rows need a consistent filter, such as `deleted_at IS NULL`. Centralize that rule where useful, and test privileged or administrative queries separately. RLS enforces access policies; it is not automatically a soft-delete filter.

**Q:** Why does a synchronization system need an explicit record of deletion?

**A:** Replicas cannot infer a deletion from a missing update alone. A deletion event or tombstone tells consumers to remove the older value; its format and retention depend on the system.

## Backups, PITR & Recovery

Source: [Backups, PITR & Recovery](20.4.5.04-backups-pitr-recovery.md)

**Q:** Why is a replica insufficient protection against an incorrect UPDATE?

**A:** A replica faithfully replicates the bad `UPDATE` — copies are not backups. Only point-in-time history lets you recover *before* the mistake, which is why WAL archiving (PITR) is the backbone, not full dumps.

**Q:** What must a restore test prove about a backup?

**A:** Recovery involves RTO (how long to restore) and RPO (how much data you can lose) — both are *measured by restoring*, regularly. The test is the backup; the file is just an ingredient.

**Q:** How do recovery-point and recovery-time targets influence the backup design?

**A:** RPO sets archival frequency and WAL granularity; RTO sets restore tooling, sizing, and whether warm standbys are worth paying for.

## Search Infrastructure at Scale

Source: [Search Infrastructure at Scale](20.4.5.05-search-infrastructure-at-scale.md)

**Q:** How does relevance ranking differ from simply selecting matching rows?

**A:** Relevance ranking (BM25, vector similarity) is a scoring problem over inverted indexes / vector indexes — a different data structure than a B-tree, hence a different engine (Elasticsearch, pg_trgm for small scale, pgvector for embeddings).

**Q:** Why can an asynchronously updated search index return older data?

**A:** Search indexes lag the source of truth by design (async indexing) — the same read-your-writes problem as replicas , usually solved by indexing on write-path events and accepting seconds of staleness.

**Q:** What workload and expected growth should determine whether search needs a separate engine?

**A:** Compare search features, query latency, update rate, operational cost, and measured load. PostgreSQL text search or extensions may fit some workloads; a separate engine may help when requirements or workload justify it. Row count alone is not a reliable cutoff.

## Summary

Use these prompts after the reading pass to recall the operations and scaling mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
