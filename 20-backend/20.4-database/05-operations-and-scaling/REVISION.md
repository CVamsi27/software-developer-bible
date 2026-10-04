<!-- section: Database | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
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

**A:** TLS + auth + backend fork per request cannot survive real traffic — so connections are created once and *reused*, and the pool is the rental contract between app and DB.

**Q:** Why can a smaller connection pool improve throughput?

**A:** Postgres can actively serve only ~`max_connections` queries; a pool of 200 against 100 cores just queues — context-switching worse than a smaller pool. The formula (cores × 2 + spindles) surprises everyone: *smaller* pools often mean *more* throughput.

**Q:** How do leaked connections and long transactions affect request latency?

**A:** Leaked connections, missing timeouts, and long transactions holding connections  all present as mysterious latency at p99, because waiting-for-connection time lands at the tail.

## Database Migrations & Zero-Downtime Schema Changes

Source: [Database Migrations & Zero-Downtime Schema Changes](20.4.5.02-migration-strategies.md)

**Q:** Why must a schema change work with both application versions during a rolling deployment?

**A:** Rolling deploys mean v1 and v2 of the app hit the same database simultaneously — so a breaking schema change (rename, drop, tighten) breaks whichever version is still running. Every safe-migration pattern is an answer to this.

**Q:** What does each phase of expand, migrate, and contract change?

**A:** add the new shape (expand, backward-compatible), backfill and switch code over (migrate), remove the old shape only when nothing reads it (contract). Three steps because coexistence is unavoidable.

**Q:** Why can a short ALTER TABLE statement still interrupt application traffic?

**A:** `ALTER TABLE` can take an ACCESS EXCLUSIVE lock even for "add nullable column" — on a hot table that's an outage. Zero-downtime migration is therefore lock-awareness, not just backward compatibility.

## Soft Delete & Tombstones

Source: [Soft Delete & Tombstones](20.4.5.03-soft-delete-and-tombstones.md)

**Q:** How does soft deletion change the ability to restore data and preserve references?

**A:** FKs cascade or block, audits lose their subject, and "undo" is impossible. Keeping the row and flagging `deleted_at` preserves history, enables restore, and makes deletes as cheap as an UPDATE.

**Q:** What must ordinary queries do when a table uses soft deletion?

**A:** Forget one WHERE and ghosts appear in prod. The mitigations (views, default scopes, RLS ) each move the filter somewhere it can't be forgotten — the same "make it structural, not remembered" principle.

**Q:** Why does a synchronization system need an explicit record of deletion?

**A:** a delete must propagate as *data*, because an absence cannot be replicated. This is why event systems and sync engines speak of tombstones — deletion is information.

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

**A:** Postgres full-text/trgm to millions of rows, dedicated engines past that, pgvector when embeddings join the party. Migrations between them are expensive — pick by expected 2-year scale.

## Summary

Use these prompts after the reading pass to recall the operations and scaling mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
