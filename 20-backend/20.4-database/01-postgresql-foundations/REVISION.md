<!-- section: Database | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Database — Postgresql Foundations Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## PostgreSQL for Backend Engineers

Source: [PostgreSQL for Backend Engineers](20.4.1.01-postgresql.md)

**Q:** Why do simultaneous updates to an account balance need database concurrency controls?

**A:** Two writers to the same account balance cannot be allowed to interleave blindly — the DB's core promise is serializability where it matters, which forces locking or its equivalent (MVCC, → 20.4.1.03).

**Q:** How can an index reduce the number of rows examined when searching a large table?

**A:** Finding "orders by customer 42 in October" in a billion rows demands structure — hence indexes , which trade write cost and space for read time, irreversibly.

**Q:** How does the write-ahead log help committed changes survive a crash?

**A:** "Committed" that evaporates on power loss is worthless — hence the write-ahead log: changes hit durable log before pages. Durability is engineered, not assumed.

## Database Normalization

Source: [Database Normalization](20.4.1.02-normalization.md)

**Q:** How can storing the same customer fact in two rows cause update, insertion, or deletion problems?

**A:** Two rows saying different cities for the same customer isn't a bug you can fix — it's a state you've made *representable*. Anomalies (update, insert, delete) are all this one defect wearing three hats.

**Q:** How do normal forms decide which facts belong together in a table?

**A:** Each normal form (1NF→3NF and beyond) is a progressively stricter statement of "no fact depends on anything except its key." 3NF is the practical stopping point because it eliminates all modify-anomalies at the cost of joins.

**Q:** What consistency risk does denormalization introduce, and how can the update path control it?

**A:** Denormalization re-imports duplication deliberately — buying read speed with write-consistency risk — and is only safe when the update path is controlled (materialized views, event-fed caches). The discipline is knowing you're re-introducing axiom 1 and managing it.

## MVCC (Multi-Version Concurrency Control)

Source: [MVCC (Multi-Version Concurrency Control)](20.4.1.03-mvcc.md)

**Q:** How can multiple row versions let a reporting query run alongside writes?

**A:** If consistency requires locks, a long reporting query freezes every write. The escape: keep *multiple versions* of each row so every transaction sees a consistent snapshot without waiting.

**Q:** Why must PostgreSQL delay reclaiming some deleted or updated row versions?

**A:** No version can be removed while any snapshot might still need it — so "DELETE" marks a row dead and "UPDATE" inserts a new version. This is why VACUUM exists: reclaiming that space is a *necessarily deferred* cleanup, not optional housekeeping.

**Q:** How can a long-running transaction cause table bloat?

**A:** Long transactions pin old versions alive (bloat) or fail (snapshot-too-old). MVCC doesn't eliminate cost — it converts blocking cost into space/time cost, which is usually the better trade but must be understood as one.

## SQL vs NoSQL — Choosing the Right Database

Source: [SQL vs NoSQL — Choosing the Right Database](20.4.1.04-nosql-vs-sql.md)

**Q:** What becomes harder when relational data is split across database shards?

**A:** Scale-out sharding breaks cross-shard joins and transactions. NoSQL families each abandon a different part of the contract to gain horizontal scale: key-value stores abandon structure, document stores abandon joins, wide-column stores abandon ad-hoc query.

**Q:** How should query patterns influence the choice of a relational, document, or key-value store?

**A:** Lookup-by-key at massive scale → KV. Self-contained aggregates (user profiles, product docs) → documents. Deep relational integrity and analytical queries → SQL. The data's *shape and access pattern* picks the store; picking the store first is the mistake.

**Q:** Which PostgreSQL features support workloads that might otherwise need a specialized store?

**A:** (JSONB, partitioning, logical replication) — which is why "default Postgres, specialize when a specific constraint bites" is the modern baseline answer.

## PostgreSQL Performance Tuning

Source: [PostgreSQL Performance Tuning](20.4.1.05-postgresql-performance.md)

**Q:** How do you distinguish CPU work, I/O waits, and lock waits when tuning PostgreSQL?

**A:** Every optimization question is "which one?" — EXPLAIN answers it by showing plan shape (CPU), buffer counts (I/O), and wait events (locks). Measuring before optimizing isn't virtue; it's taxonomy.

**Q:** Why can the same SQL query run with different execution plans?

**A:** The same query can scan or index-lookup depending on statistics and selectivity; the planner is a cost-based guesser whose inputs you control (ANALYZE freshness, statistics, index availability). "Why is my query slow?" is almost always "why did the planner pick this plan?".

**Q:** Why does keeping frequently accessed data in memory affect query performance?

**A:** Hot working set in memory ⇒ microseconds; cold ⇒ milliseconds, a 100× cliff. Sizing memory to the working set and reading hit ratios is therefore the first performance conversation, not the last.

## PostgreSQL Row-Level Security (RLS)

Source: [PostgreSQL Row-Level Security (RLS)](20.4.1.06-row-level-security.md)

**Q:** How can row-level security protect against a missing tenant filter in application SQL?

**A:** If isolation depends on every developer remembering `WHERE tenant_id = $1` in every query forever, the guarantee is only as strong as the most tired engineer. RLS moves the filter into the engine, applied to *every* access regardless of source.

**Q:** How do row-level security policies obtain the identity used to filter rows?

**A:** — app sets `SET LOCAL app.user_id` per request; policies reference it. The app can no longer forget, but it also can't opt out — which is exactly the point.

**Q:** What makes row-level security harder to debug and maintain?

**A:** policies apply silently, superusers bypass them, and debugging "why no rows?" means reasoning about policy expressions. RLS trades developer discipline for engine guarantees — the right trade for multi-tenancy, a wrong one for simple single-tenant apps.

## Summary

Use these prompts after the reading pass to recall the postgresql foundations mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
