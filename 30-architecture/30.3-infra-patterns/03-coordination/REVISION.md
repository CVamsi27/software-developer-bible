<!-- section: Infra Patterns | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Infra%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# Coordination — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## Leader Election & Consensus — Raft, Paxos, Practical Patterns

Source: [Leader Election & Consensus — Raft, Paxos, Practical Patterns](30.3.3.01-leader-election-consensus.md)

**Q:** Why must fencing epochs come from a durable monotonic authority?

**A:** A worker-local or reset counter can reuse old authority. The protected resource must reject older epochs and the issuer must account for failover and restoration.

**Q:** Why may two leaders exist transiently even with a lease?

**A:** A paused or partitioned holder may not observe expiry. External resources must validate authority rather than relying on each worker's local role belief.

**Q:** Should a resource reject every repeated fencing epoch?

**A:** Not necessarily. Several valid writes can belong to one ownership epoch. Reject older epochs and enforce the current lease or operation identity when its contract requires it.

**Q:** Why must renewal compare the owner atomically?

**A:** A check followed by expiry extension can renew a successor's lease after a race. Compare token and extend in one store operation.

**Q:** Does Redis SET NX PX implement Raft consensus?

**A:** No. It is a single-store lease primitive with the durability and failover behavior of that store. Consensus and multi-node lock algorithms have different contracts.

**Q:** A replacement INSERT computed its expiry before waiting on a locked lease row. Why can reusing that expiry be unsafe?

**A:** The wait can consume the interval, so ON CONFLICT may return an already-expired grant. Recompute replacement expiry from the database clock after the conflict-row wait.

**Q:** Does rejecting an old fencing epoch prove the caller still owns a live lease?

**A:** No. It rejects stale epochs after a newer one reaches the resource. Current ownership needs a checked owner/epoch/expiry boundary serialized with replacement, and an external effect needs its own contract.

**Q:** What does etcd's `LeaderKey.rev` prove, and what does it not prove about a database write?

**A:** The creation revision can be compared in an etcd transaction to verify that the election key still represents the current leader. A separate database must still enforce the revision as a fence or check current ownership with the mutation; after snapshot restore, configure a revision bump if that revision is used for ordering. See the [etcd concurrency API](https://etcd.io/docs/v3.6/dev-guide/api_concurrency_reference_v3/) and [recovery guidance](https://etcd.io/docs/v3.6/op-guide/recovery/).

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
