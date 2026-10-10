<!-- section: Database | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Database — Postgresql Foundations Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## PostgreSQL for Backend Engineers

Source: [PostgreSQL for Backend Engineers](20.4.1.01-postgresql.md)

**Q:** Why do simultaneous updates to an account balance need database concurrency controls?

**A:** Two readers can calculate incompatible writes from the same old balance. Use an atomic mutation, a protected transaction or version validation for the required invariant; default isolation does not guarantee serializability.

**Q:** How can an index reduce the number of rows examined when searching a large table?

**A:** An index organizes searchable keys so a suitable query can locate candidate rows without scanning the whole table. It adds storage and write maintenance; selectivity and the plan determine whether it is beneficial.

**Q:** How does the write-ahead log help committed changes survive a crash?

**A:** WAL records must be durable before corresponding data pages are written. With appropriate durable-commit settings, recovery can redo committed changes even if the table pages were not flushed before the crash. WAL on lost storage is not a substitute for backups.

**Q:** Why must BEGIN, tenant context and protected statements use one checked-out connection?

**A:** Transaction and local settings belong to a database session. A query sent through another pooled connection does not inherit them; ending the transaction before release prevents the next request from inheriting unfinished state.

## Database Normalization

Source: [Database Normalization](20.4.1.02-normalization.md)

**Q:** How can storing the same customer fact in two rows cause update, insertion, or deletion problems?

**A:** One update can leave conflicting copies; insertion can require an unrelated order; deleting the last order can remove the only customer fact. Give the current customer fact one owner. An invoice's historical address is a different fact with its own owner.

**Q:** How do normal forms decide which facts belong together in a table?

**A:** Normal forms constrain dependencies among attributes to reduce redundant facts and modification anomalies. Check the actual dependencies and whether a decomposition is lossless and preserves needed constraints; 3NF does not remove every possible anomaly.

**Q:** What consistency risk does denormalization introduce, and how can the update path control it?

**A:** Denormalization re-imports duplication deliberately — buying read speed with write-consistency risk — and is only safe when the update path is controlled (materialized views, event-fed caches). The discipline is knowing you're re-introducing axiom 1 and managing it.

**Q:** A current catalog price changes from 3.00 to 4.00. Why should an existing order's purchased total remain unchanged?

**A:** Purchased unit price is a historical fact owned by the order line, while current price is owned by the product. The normalized trace retains the former; recalculating old orders from the latter changes history.

**Q:** Can a lossless BCNF split make a constraint harder to enforce?

**A:** Yes. The Teaching split reconstructs rows through instructor-to-course, but the one-instructor-per-student-per-course rule spans both new tables. Losslessness and dependency preservation are separate properties; a 3NF design may keep a needed rule locally enforceable.

## MVCC (Multi-Version Concurrency Control)

Source: [MVCC (Multi-Version Concurrency Control)](20.4.1.03-mvcc.md)

**Q:** How can multiple row versions let a reporting query run alongside writes?

**A:** MVCC lets ordinary reads use row versions without taking row locks that conflict with writers. Snapshot timing depends on isolation: Read Committed takes a new snapshot per statement, while Repeatable Read and Serializable use a transaction snapshot. Some table locks and explicit locking reads can still block.

**Q:** Why must PostgreSQL delay reclaiming some deleted or updated row versions?

**A:** No version can be removed while any snapshot might still need it — so "DELETE" marks a row dead and "UPDATE" inserts a new version. This is why VACUUM exists: reclaiming that space is a *necessarily deferred* cleanup, not optional housekeeping.

**Q:** How can a long-running transaction cause table bloat?

**A:** A long-lived snapshot can prevent vacuum from reclaiming row versions still needed by that transaction. Monitor transaction age, retained versions and vacuum progress; MVCC reduces ordinary read/write blocking but adds cleanup and storage costs.

**Q:** A writer commits between two SELECTs in a transaction begun with plain BEGIN. Which balance does the second SELECT see?

**A:** At default Read Committed, it takes a new statement snapshot and can see the new commit. An already established Repeatable Read snapshot excludes it; BEGIN alone does not establish that stable snapshot.

**Q:** What changes if the Repeatable Read reader updates the row after the other transaction commits?

**A:** The row changed after its snapshot, so PostgreSQL can raise 40001. Roll back and retry the entire transaction with fresh reads and decisions. The earlier ordinary SELECT could proceed without waiting, but that does not make the write conflict-free.

**Q:** Does a nonzero xmax prove that the returned row has been deleted?

**A:** No. It may encode row-lock information, and visibility also depends on transaction outcomes and the snapshot. The system-column query returns the currently visible version, not an audit history of all versions.

## SQL vs NoSQL — Choosing the Right Database

Source: [SQL vs NoSQL — Choosing the Right Database](20.4.1.04-nosql-vs-sql.md)

**Q:** What becomes harder when relational data is split across database shards?

**A:** Distribution changes the cost of cross-node queries and transactions, but products vary. Some relational databases distribute operations, and some non-relational systems provide transactions or richer queries; compare the exact product guarantees.

**Q:** How should query patterns influence the choice of a relational, document, or key-value store?

**A:** Start with access patterns and consistency needs: key lookup may fit a key-value store, self-contained records may fit a document store, and relational integrity or varied joins may fit a relational database. Verify the product's actual capabilities.

**Q:** Which PostgreSQL features support workloads that might otherwise need a specialized store?

**A:** JSONB can hold optional document attributes, partitioning can align data with query/retention boundaries, and replication can serve additional copies. Each has limits: not every JSON expression is indexed, partitions do not replace access paths, and replicas can lag.

**Q:** A committed order is present in its owner database but absent from search. Which part of the trace needs investigation?

**A:** Publication, consumer progress and search refresh can lag or fail after the owner commit. Verify the durable publication/rebuild contract and the search freshness requirement; a transaction in the owner does not atomically update the derived index.

**Q:** Does “eventual consistency” establish a fixed short delay or guarantee an immediate inventory decision?

**A:** No. Convergence depends on propagation and failure conditions and does not by itself bound staleness. Select an operation-specific read/mutation guarantee for authoritative decisions.

## PostgreSQL Performance Tuning

Source: [PostgreSQL Performance Tuning](20.4.1.05-postgresql-performance.md)

**Q:** How do you distinguish CPU work, I/O waits, and lock waits when tuning PostgreSQL?

**A:** Use execution plans and buffer instrumentation to inspect query work, and activity/wait-event views to identify blocking or I/O waits. EXPLAIN alone does not report every wait cause; correlate observations with workload and host metrics.

**Q:** Why can the same SQL query run with different execution plans?

**A:** Statistics, parameter values, available indexes and settings change estimated costs. Compare estimated with actual rows and loops. A slow request can also wait in a pool or on a lock even with a reasonable plan.

**Q:** Why does keeping frequently accessed data in memory affect query performance?

**A:** Cached pages avoid some storage work, but a PostgreSQL cache miss may still hit the operating system cache. A high aggregate hit ratio does not prove that one critical query is fast; inspect its buffer activity, latency and the workload's memory pressure.

**Q:** The partial index contains only booked visits. What changes when the query requests cancelled visits?

**A:** That index cannot supply the requested rows. The planner needs another access path; retaining the same ORDER BY or clinic does not make the partial predicate apply.

**Q:** How do you identify a slow query?

**A:** Correlate application latency, pool waiting and database activity. Use workload statistics to prioritize, then safely inspect execution plans or wait/blocker evidence. A sequential scan or high mean time alone does not establish the cause.

**Q:** What's the difference between VACUUM and VACUUM FULL?

**A:** Ordinary VACUUM makes eligible space reusable and normally permits ordinary reads/writes. VACUUM FULL rewrites with an exclusive lock and can return space to the operating system; plan capacity and availability before using it.

**Q:** How do you prevent table bloat?

**A:** Keep vacuum able to keep up, bound unnecessarily retained snapshots, and monitor cleanup, version estimates and sizes together. A large table or a dead-tuple estimate alone does not establish wasted bytes; partitioning helps only when its query or retention boundary fits.

## PostgreSQL Row-Level Security (RLS)

Source: [PostgreSQL Row-Level Security (RLS)](20.4.1.06-row-level-security.md)

**Q:** How can row-level security protect against a missing tenant filter in application SQL?

**A:** RLS applies policies to eligible table operations, reducing dependence on every query repeating a tenant filter. Superusers and `BYPASSRLS` roles bypass policies; table owners normally bypass them unless forced, and `TRUNCATE` is outside RLS.

**Q:** How do row-level security policies obtain the identity used to filter rows?

**A:** The application can set transaction-scoped request values for policies to read, but the application still controls those values. Database credentials, transaction handling and role membership remain in the trust boundary.

**Q:** What makes row-level security harder to debug and maintain?

**A:** Policy behavior is implicit in queries; debugging "why no rows?" requires reading the policy expressions and role memberships. Permissive policies combine with `OR`, so overlapping role membership can broaden access.

**Q:** Why can a test as the table owner pass while the API's query returns no rows?

**A:** Owners normally bypass RLS. Test using the subject API role without bypass privileges and establish its context. FORCE can subject an owner to RLS, but does not constrain superusers or BYPASSRLS roles.

**Q:** What happens if enabled RLS has a SELECT policy but no policy permitting INSERT?

**A:** A subject role's proposed insert is denied, even if ordinary table privileges permit INSERT. Missing mutation policies do not create unrestricted writes.

**Q:** An UPDATE can see its old row. Why can changing its tenant ID still fail?

**A:** USING permits the old row as a target, while WITH CHECK independently validates the proposed row. The proposed other-tenant version fails the new-row boundary.

**Q:** Can a narrower doctor policy restrict a broader permissive tenant policy?

**A:** Not by itself: applicable permissive policies combine with OR. Intersect grants with an appropriate restrictive boundary or design each grant to express the full intended condition, then verify inherited roles and every command.

## Summary

Use these prompts after the reading pass to recall the postgresql foundations mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for row visibility, index choices and query evidence

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
