<!-- section: Architecture | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Architecture-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Data At Scale — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Database Scaling — Partitioning, Replication, Connection Pooling, Query Optimization

Source: [Database Scaling — Partitioning, Replication, Connection Pooling, Query Optimization](30.3.4.01-database-scaling.md)

**Q:** How can partitioning help without distributing load to new database servers?

**A:** It organizes child tables on one instance, permitting pruning and retention operations. Sharding across servers is an additional routing and storage mechanism.

**Q:** Which measurement distinguishes connection saturation from a slow query?

**A:** Measure how long requests wait to obtain a pooled connection, how many connections are active, and how much time queries spend executing or waiting inside the database. Increasing pool size can overload the database further rather than remove the bottleneck.

**Q:** Does a UUID default establish global uniqueness on a table partitioned by time?

**A:** No. Generation and constraints are separate. A parent unique/primary key must include supported partition keys; uniqueness of `(id, scheduled_at)` does not guarantee id alone is globally unique.

**Q:** Does PgBouncer default_pool_size = 20 limit the entire database to twenty connections?

**A:** No. The size is per user/database pool, with other pools/reserve configuration and direct clients adding demand. Budget fleet-wide useful execution and queueing, not just one setting.

**Q:** In PgBouncer transaction mode, which session assumptions must an application avoid, and when can it use named prepared statements?

**A:** The server connection is released at transaction end, so session `SET` state and session-level advisory locks do not follow the client to its next transaction. PgBouncer supports protocol-level named prepared statements in this mode only when `max_prepared_statements` is nonzero; SQL `PREPARE`/`DEALLOCATE` remains incompatible. Verify the driver's protocol behavior against the [PgBouncer feature matrix](https://www.pgbouncer.org/features.html).

## Data Pipelines — ETL, Stream Processing, Data Lake

Source: [Data Pipelines — ETL, Stream Processing, Data Lake](30.3.4.02-data-pipelines.md)

**Q:** What should a pipeline checkpoint commit together with its output?

**A:** The position/state corresponding to the applied output, within the chosen processing boundary. Otherwise restart may skip work or apply it twice.

**Q:** Why does a highest-version upsert fit an after-image but not every additive event?

**A:** A complete newer image replaces older state. An additive event may carry a distinct required contribution; dropping older events can lose it. Deduplication and ordering/aggregation semantics depend on the event contract.

**Q:** Can deleting a projection tombstone resurrect old data during replay?

**A:** Yes. Without the retained higher deletion version, an older image can insert again. Match tombstone retention to the replay/correction contract and required deletion policy.

**Q:** Is a five-minute floor(timestamp / interval) bucket a sliding window?

**A:** It is a tumbling window. Sliding windows overlap; late data and watermark/correction behavior require additional explicit policies.

## CDN Architecture — Edge Caching, Geographic Distribution, Cache Invalidation

Source: [CDN Architecture — Edge Caching, Geographic Distribution, Cache Invalidation](30.3.4.03-cdn-architecture.md)

**Q:** Why is CDN invalidation not an immediate global transaction?

**A:** Purge propagation and existing browser or intermediary caches have their own lifetimes. Versioned asset names and an explicit freshness contract reduce ambiguity.

**Q:** What changes when a cache key includes too few required response variations?

**A:** Distinct responses merge, potentially leaking private data or serving the wrong variant. Too many irrelevant variations instead fragment reuse. Neither key choice supplies access authorization.

**Q:** Does serving through a chosen region prove where sensitive data is retained?

**A:** No. Origin, backups, logs, telemetry and provider processing have separate location/trust contracts. No-store controls relevant caching, not all processing or compliance.

## Multi-Tenant SaaS Architecture

Source: [Multi-Tenant SaaS Architecture](30.3.4.04-multi-tenant-saas-architecture.md)

**Q:** Why must an RLS tenant setting and queries share one transaction connection?

**A:** Transaction-local context does not follow a query onto another pooled connection. Pin both operations together and use a runtime role that cannot bypass the policy.

**Q:** Why should a tenant filter built with Prisma middleware or an extension name its supported major version and operations?

**A:** Prisma ORM 7 removed the legacy `$use` API, while Prisma ORM 8 provides a different middleware configuration. A filter covering selected operations is not proof that nested, raw or relationship paths enforce the same tenant boundary.

**Q:** Does installing a transaction-local tenant setting protect a later query on another pooled connection?

**A:** No. Context installation and protected statements must use the same transaction/connection. Authorized application context and an RLS-constrained runtime role are also necessary; RLS cannot make SQL injection safe.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
