<!-- section: Database | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
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

**Q:** A network failure occurs during COMMIT. Why is it different from a confirmed 40001 rollback?

**A:** The commit outcome may be unknown. Reconcile a durable operation key/result before repeating a transfer; a known serialization rollback instead permits bounded whole-transaction retry with fresh reads.

## Deadlocks

Source: [Deadlocks](20.4.3.02-deadlocks.md)

**Q:** How does PostgreSQL detect and break a deadlock condition?

**A:** PostgreSQL checks for a deadlock after `deadlock_timeout`, detects a cycle in the lock dependency graph, and aborts one participant with `deadlock_detected` (`40P01`). Which participant is chosen is not an application contract. Retry the whole transaction when safe; this differs from a serialization failure (`40001`).

**Q:** What architectural rule prevents deadlocks across multi-row database updates?

**A:** Acquire all participating resources in a deterministic global order to remove circular wait. Ordering only the explicit rows is insufficient if triggers, foreign keys, lock upgrades or another writer acquire additional resources differently.

**Q:** What changes when a worker uses SKIP LOCKED instead of waiting for the first queued row?

**A:** It can claim another unlocked row, so the result is not strict FIFO or proof that an empty result means no pending work. The claim must atomically transition state; a crashed worker still needs lease recovery and idempotent effects.

## Optimistic vs Pessimistic Locking

Source: [Optimistic vs Pessimistic Locking](20.4.3.03-optimistic-pessimistic-locking.md)

**Q:** Under what workload characteristics does optimistic concurrency control outperform pessimistic locking?

**A:** Expected-version writes can avoid holding protective locks throughout an earlier read or editing period when conflicts are rare. The UPDATE still takes write locks and validates its predicate when it executes, not automatically at commit. Measure conflict/recomputation cost; stale human intent needs reconciliation.

**Q:** Why must an optimistic concurrency update verify the version in the `WHERE` clause rather than purely in memory?

**A:** Verification in application memory is subject to race conditions between the read and write steps. The database update statement `WHERE id = $1 AND version = $2` enforces atomic check-and-set at the storage engine level.

**Q:** Two editors both read version 1. What does the second write return after the first increments the version?

**A:** Its expected-version UPDATE returns zero rows. Every writer must increment the token; refreshing the token and repeating the same stale replacement defeats the protection.

## Database Replication

Source: [Database Replication](20.4.3.04-database-replication.md)

**Q:** What failure mode emerges when reading from an asynchronous replica immediately following a write to the primary?

**A:** Replication lag creates a read-your-own-writes inconsistency where the replica snapshot has not applied the WAL record from the primary, returning stale data to the user.

**Q:** How does synchronous replication trade off write latency against durability?

**A:** The configured synchronous set and synchronous_commit choose whether acknowledgment waits for standby write, durable flush or replay. Waiting adds latency and dependence on that set. Survival also requires failover to a copy containing the write and surviving storage; arbitrary replica promotion is not lossless.

**Q:** A standby has caught up, but a Repeatable Read transaction established its snapshot before replay. Is its next read current?

**A:** No. Replay progress and snapshot visibility are separate. Start a fresh business-read snapshot after the trusted watermark check, and handle failover/timeline identity in the routing protocol.

## Summary

Use these prompts after the reading pass to recall the transaction and replication mechanisms and their boundaries.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for isolation, locks and replication freshness

## References & Learn More

The linked source chapters provide the transactional and replication documentation and further reading.
