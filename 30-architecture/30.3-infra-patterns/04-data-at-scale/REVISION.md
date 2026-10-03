<!-- section: Architecture | category: Reference | tags: revision, retrieval-practi | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Architecture-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
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

**A:** Measure pool borrow wait, active connections and query execution/wait events separately. Increasing pool size can worsen database saturation rather than remove it.

## Data Pipelines — ETL, Stream Processing, Data Lake

Source: [Data Pipelines — ETL, Stream Processing, Data Lake](30.3.4.02-data-pipelines.md)

**Q:** What should a pipeline checkpoint commit together with its output?

**A:** The position/state corresponding to the applied output, within the chosen processing boundary. Otherwise restart may skip work or apply it twice.

## CDN Architecture — Edge Caching, Geographic Distribution, Cache Invalidation

Source: [CDN Architecture — Edge Caching, Geographic Distribution, Cache Invalidation](30.3.4.03-cdn-architecture.md)

**Q:** Why is CDN invalidation not an immediate global transaction?

**A:** Purge propagation and existing browser or intermediary caches have their own lifetimes. Versioned asset names and an explicit freshness contract reduce ambiguity.

## Multi-Tenant SaaS Architecture

Source: [Multi-Tenant SaaS Architecture](30.3.4.04-multi-tenant-saas-architecture.md)

**Q:** Why must an RLS tenant setting and queries share one transaction connection?

**A:** Transaction-local context does not follow a query onto another pooled connection. Pin both operations together and use a runtime role that cannot bypass the policy.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
