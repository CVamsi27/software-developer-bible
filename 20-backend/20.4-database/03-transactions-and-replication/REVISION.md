<!-- section: Database | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Transactions & Replication — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Database Transactions

Source: [Database Transactions](20.4.3.01-transactions.md)

**Q:** Why does Read Committed isolation still permit non-repeatable reads within the same transaction?

**A:** Read Committed takes a new snapshot for each query execution rather than at transaction start. Rows modified and committed by other transactions between two statements become visible in the second query.

**Q:** What distinguishes write skew from a standard dirty or non-repeatable read?

**A:** Write skew occurs when two concurrent transactions read overlapping datasets, make disjoint updates based on shared premises, and commit without conflicting on the same physical rows, violating a cross-row constraint. Repeatable Read does not prevent it in standard snapshot isolation.

## Deadlocks

Source: [Deadlocks](20.4.3.02-deadlocks.md)

**Q:** How does PostgreSQL detect and break a deadlock condition?

**A:** PostgreSQL checks for a deadlock after `deadlock_timeout`, detects a cycle in the lock dependency graph, and aborts one participant with `deadlock_detected` (`40P01`). Which participant is chosen is not an application contract. Retry the whole transaction when safe; this differs from a serialization failure (`40001`).

**Q:** What architectural rule prevents deadlocks across multi-row database updates?

**A:** Acquiring locks on rows in a deterministic, globally agreed order (such as sorted primary keys) guarantees the wait-for graph cannot form a cycle.

## Optimistic vs Pessimistic Locking

Source: [Optimistic vs Pessimistic Locking](20.4.3.03-optimistic-pessimistic-locking.md)

**Q:** Under what workload characteristics does optimistic concurrency control outperform pessimistic locking?

**A:** OCC excels in low-to-moderate contention workloads where conflicts are rare, eliminating lock acquisition overhead and database round-trips until commit time verification.

**Q:** Why must an optimistic concurrency update verify the version in the `WHERE` clause rather than purely in memory?

**A:** Verification in application memory is subject to race conditions between the read and write steps. The database update statement `WHERE id = $1 AND version = $2` enforces atomic check-and-set at the storage engine level.

## Database Replication

Source: [Database Replication](20.4.3.04-database-replication.md)

**Q:** What failure mode emerges when reading from an asynchronous replica immediately following a write to the primary?

**A:** Replication lag creates a read-your-own-writes inconsistency where the replica snapshot has not applied the WAL record from the primary, returning stale data to the user.

**Q:** How does synchronous replication trade off write latency against durability?

**A:** Synchronous replication blocks transaction commit on the primary until at least one replica confirms write-ahead log flush, increasing commit latency by the network round-trip while preventing data loss upon primary failure.

## Summary

Use these prompts after the reading pass to recall the transaction and replication mechanisms and their boundaries.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide the transactional and replication documentation and further reading.
