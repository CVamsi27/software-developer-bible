<!-- section: Database | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
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

**A:** A checked-out connection is unavailable to other borrowers. Leaks never release it; long transactions retain it while queries, locks or application work continue. Measure acquisition wait separately from execution and impose the relevant deadlines.

**Q:** In the max-one-connection fixture, what does the queued borrower consume while waiting?

**A:** It is a waiting request, not a second physical connection. waitingCount is 1 until the checked-out connection is released; with max 2, the second borrower can acquire another connection and need not queue. Across ten processes, each local maximum still contributes to the server/proxy budget.

**Q:** What changes if a transaction helper runs its UPDATE through pool.query after acquiring a client?

**A:** It can execute on another connection outside the original BEGIN. A later rollback cannot undo that write. Every statement belonging to the transaction must use the same checked-out client, with release/discard and uncertain-commit handling defined.

## Database Migrations & Zero-Downtime Schema Changes

Source: [Database Migrations & Zero-Downtime Schema Changes](20.4.5.02-migration-strategies.md)

**Q:** Why must a schema change work with both application versions during a rolling deployment?

**A:** Rolling deploys mean v1 and v2 of the app hit the same database simultaneously — so a breaking schema change (rename, drop, tighten) breaks whichever version is still running. Every safe-migration pattern is an answer to this.

**Q:** What does each phase of expand, migrate, and contract change?

**A:** Expansion adds a compatible representation; migration establishes writer ownership, backfills current values, verifies invariants and switches readers; contraction retires old writers/readers and removes the obsolete representation after the rollback window. The phases can require several deployments and validation gates.

**Q:** Why can a short ALTER TABLE statement still interrupt application traffic?

**A:** Even a fast metadata change needs a table lock and may wait behind a long transaction; some defaults or clauses also rewrite the table. Check PostgreSQL version and exact DDL, then test lock acquisition and rewrite behavior on representative data.

**Q:** What does an empty SKIP LOCKED backfill batch prove when an old-format writer remains active?

**A:** It proves neither completion nor continuing consistency. A locked mismatch may be skipped, and an old writer can later create another mismatch. Establish writer ownership, repeat bounded batches and verify the invariant separately before cutover.

**Q:** Why must an old NOT NULL column be addressed before new-only inserts?

**A:** Once writers stop providing the old representation, its constraint can reject otherwise valid new-format inserts. Retire the old requirement only after compatibility gates permit it, and preserve the intended rollback contract.

## Soft Delete & Tombstones

Source: [Soft Delete & Tombstones](20.4.5.03-soft-delete-and-tombstones.md)

**Q:** How does soft deletion change the ability to restore data and preserve references?

**A:** A hard delete may be irreversible for the application and may be blocked or cascaded by foreign keys. A `deleted_at` flag can support an undo flow, but every relevant query and unique constraint must account for inactive rows.

**Q:** What must ordinary queries do when a table uses soft deletion?

**A:** Queries that should show active rows need a consistent filter, such as `deleted_at IS NULL`. Centralize that rule where useful, and test privileged or administrative queries separately. RLS enforces access policies; it is not automatically a soft-delete filter.

**Q:** Why does a synchronization system need an explicit record of deletion?

**A:** Replicas cannot infer a deletion from a missing update alone. A deletion event or tombstone tells consumers to remove the older value; its format and retention depend on the system.

**Q:** A job saw deletion generation 1; the row was restored to 2 then deleted to 3. May that job purge the expired row now?

**A:** No. It must match current inactive state, current deadline and its expected generation at the mutation. Generation 1 is stale even if generation 3 is now expired. The current lifecycle needs its own authorized purge intent.

**Q:** Why can restoring an inactive account fail after another account reuses its email?

**A:** The active-only unique index permits reuse while the original is inactive, then rejects making both active. The fixture raises SQLSTATE 23505 and rolls back; resolve the product/authorization conflict without silently replacing another account.

## Backups, PITR & Recovery

Source: [Backups, PITR & Recovery](20.4.5.04-backups-pitr-recovery.md)

**Q:** Why is a replica insufficient protection against an incorrect UPDATE?

**A:** A standby can apply the same bad commit. Recovering an earlier state requires retained history: an older logical export can recover its snapshot; a compatible physical base plus the required uninterrupted WAL can reach a later historical target. Neither live replication nor artifact existence proves recovery.

**Q:** What must a restore test prove about a backup?

**A:** Prove artifact/key access, compatible environment, a reachable target, application invariants, isolation of side effects and usable cutover. Measure the whole recovery path and newest independently recoverable work, rather than inferring success from file existence or server startup.

**Q:** How do recovery-point and recovery-time targets influence the backup design?

**A:** RPO limits lost business work and drives independently durable history; segment switching alone does not guarantee upload. RTO includes detection, provisioning, retrieval, restore/replay, validation and cutover. Measure the deployed chain at representative volume and revisit its dependencies.

**Q:** What if the before_bad restore marker is placed after the destructive commit?

**A:** The named target includes that committed bad state. Verify marker/commit order and the recovered values. An earlier target also omits legitimate later writes, so choose whole-service rollback or selective repair with reconciliation.

**Q:** Why can a retained base backup become unusable despite every recent upload succeeding?

**A:** It may require an older missing WAL segment or inaccessible key/extension. Recovery needs a continuous applicable chain and environment; recent success does not repair a historical gap. A sixty-second archive_timeout does not prove archive durability or RPO.

**Q:** Why can PostgreSQL 18 not restore an incremental `pg_basebackup` by itself, and what must the drill validate?

**A:** The incremental depends on earlier backups. Retain the required chain and manifests, combine backups from oldest to newest, and use `pg_verifybackup` to check integrity. Then replay the required WAL and validate a reachable target in a restore drill; `pg_combinebackup` alone does not prove the files are intact or recoverable.

## Search Infrastructure at Scale

Source: [Search Infrastructure at Scale](20.4.5.05-search-infrastructure-at-scale.md)

**Q:** How does relevance ranking differ from simply selecting matching rows?

**A:** Filtering decides which documents satisfy a query; ranking orders those candidates by a scoring policy. PostgreSQL supports term-based ranking as well as filtering. A separate engine is justified by evaluated capabilities/workload, not by assuming that SQL cannot score matches.

**Q:** Why can an asynchronously updated search index return older data?

**A:** Source commit, remote application and search visibility are separate milestones. An asynchronous projection can serve older versions until publication and visibility complete. Define a measured freshness contract and, where required, bounded version/task waiting or an authoritative read; delays are not universally seconds.

**Q:** What workload and expected growth should determine whether search needs a separate engine?

**A:** Compare search features, query latency, update rate, operational cost, and measured load. PostgreSQL text search or extensions may fit some workloads; a separate engine may help when requirements or workload justify it. Row count alone is not a reliable cutoff.

**Q:** In the text-search fixture, why does wirel fail through websearch_to_tsquery while wirel:* succeeds through to_tsquery?

**A:** The former parses an ordinary full term; the latter explicitly requests a prefix. Neither operation provides typo correction. The chapter's tenant filter also excludes another tenant before ordering matches.

**Q:** A bulk request returns HTTP success, and an old upsert arrives after a deletion. Is the projection confirmed correct?

**A:** No. Inspect per-item failures/task completion and the required visibility milestone. Enforce per-key/version/delete ordering so the old event cannot recreate the document; SKIP LOCKED claims and individually idempotent upserts alone do not provide that ordering.

## Summary

Use these prompts after the reading pass to recall the operations and scaling mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — trace deletion, recovery and index freshness before scaling decisions

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
