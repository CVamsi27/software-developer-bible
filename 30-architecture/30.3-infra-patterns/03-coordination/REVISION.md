<!-- section: Infra Patterns | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-Infra%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

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

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
