<!-- section: System Design | category: Reference | tags: revision, retrieval-practice| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-System%20Design-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Theory — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## CAP Theorem & PACELC

Source: [CAP Theorem & PACELC](30.2.1.01-cap-theorem.md)

**Q:** During a partition, what conflict does CAP identify for a replicated register?

**A:** An implementation cannot guarantee both linearizable operations and eventual responses to every request on non-failing nodes under the theorem's partition assumptions. It is not a universal choose-two menu in normal operation.

## Data Consistency Models

Source: [Data Consistency Models](30.2.1.02-consistency-models.md)

**Q:** Why do read-your-writes and monotonic reads not form a single stronger/weaker ladder?

**A:** They constrain different histories: one preserves a client's own writes, the other prevents its reads from moving backward. A system can provide one without the other.

## Sharding & Replication

Source: [Sharding & Replication](30.2.1.03-sharding-and-replication.md)

**Q:** Why can a good average shard size still hide a scaling failure?

**A:** A hot key or uneven request distribution can overload one shard while others remain idle. Measure work per shard, not just bytes or record counts.

## Load Balancing

Source: [Load Balancing](30.2.1.04-load-balancing.md)

**Q:** What failure can sticky routing mask until failover?

**A:** A client's consistency or session state may depend on one backend. Failover needs shared state or explicit consistency tokens rather than assuming the next node is equivalent.

## Caching Patterns

Source: [Caching Patterns](30.2.1.05-caching-patterns.md)

**Q:** Why is cache invalidation part of the write contract?

**A:** The system must decide which reads may see old values and how updates, races and TTLs converge. A cache hit is only correct under that staleness contract.

## Message Queues & Async Patterns

Source: [Message Queues & Async Patterns](30.2.1.06-queues-and-async.md)

**Q:** Why should a consumer acknowledge a message after committing its local effect?

**A:** Acknowledging first can lose work if the process crashes. Committing first permits redelivery, so the local effect also needs transactional deduplication.

## Distributed Transactions

Source: [Distributed Transactions](30.2.1.07-distributed-transactions.md)

**Q:** What contract does a saga give up compared with atomic commit?

**A:** It permits visible intermediate local commits and recovers with later business actions. It does not provide one globally atomic rollback.

## Rate Limiting

Source: [Rate Limiting](30.2.1.08-rate-limiting.md)

**Q:** Why can two independent local token buckets exceed a global limit?

**A:** Each grants capacity without knowing the other's grants. A global contract needs coordination or a documented allocation/approximation strategy.

## Consensus & Leader Election

Source: [Consensus & Leader Election](30.2.1.09-consensus-and-leader-election.md)

**Q:** Can an isolated old Raft leader safely commit new writes alone?

**A:** No. A leader needs the protocol's quorum and commit rules. Its old role label does not establish authority to commit or authorize an external side effect.

## Failure Modes

Source: [Failure Modes](30.2.1.10-failure-modes.md)

**Q:** Why is a timeout a dangerous trigger for retrying a mutation?

**A:** The first attempt may have committed while its response was lost. Retry only under an appropriate idempotency and reconciliation contract.

## Architecture Patterns — Monolith, Microservices, Event-Driven, Hexagonal

Source: [Architecture Patterns — Monolith, Microservices, Event-Driven, Hexagonal](30.2.1.11-architecture-patterns.md)

**Q:** What should justify a microservice boundary beyond a diagram box?

**A:** A cohesive domain or operational ownership boundary whose independent evolution is worth its network, consistency and deployment costs.

## Capacity Planning & Back-of-Envelope Estimation

Source: [Capacity Planning & Back-of-Envelope Estimation](30.2.1.12-capacity-planning.md)

**Q:** Why should capacity calculations use peak load and headroom rather than average QPS alone?

**A:** Bursts, skew, failover and maintenance can concentrate work. Average load hides queues and saturation at the periods that determine service reliability.

## Backpressure & Flow Control

Source: [Backpressure & Flow Control](30.2.1.13-backpressure-and-flow-control.md)

**Q:** How can a push protocol provide backpressure without becoming a pull API?

**A:** Credits, bounded windows or explicit pause/resume signals restrict producer progress to consumer capacity. The key is bounded admitted work and a defined overload policy.

## Distributed Locks & Coordination

Source: [Distributed Locks & Coordination](30.2.1.14-distributed-locks.md)

**Q:** Why is a lease insufficient to stop a paused worker writing after expiry?

**A:** The worker may resume without noticing it lost the lease. The resource must reject stale authority, for example with fencing tokens, or use another transactional safety boundary.

## How to Approach Any System Design Problem

Source: [How to Approach Any System Design Problem](30.2.1.15-how-to-approach.md)

**Q:** Why should requirements precede choosing databases in a design interview?

**A:** Required invariants, access patterns and failure behavior determine storage tradeoffs. Choosing products first can produce a design that solves the wrong problem.

## Probabilistic Data Structures

Source: [Probabilistic Data Structures](30.2.1.17-probabilistic-data-structures.md)

**Q:** Why may a Bloom negative skip an exact read but not an authoritative uniqueness write?

**A:** A correctly populated filter can rule out membership in its represented set. Concurrent insertion and durable uniqueness still require atomic enforcement; a hint is not a claim.

## Outbox Pattern & Change Data Capture (CDC)

Source: [Outbox Pattern & Change Data Capture (CDC)](30.2.1.18-outbox-and-cdc.md)

**Q:** Which crash window does a transactional outbox close, and which remains?

**A:** It commits business data and publication intent together. The relay can still publish and crash before marking sent, so consumers must tolerate duplicate delivery.

## Resilience Patterns Deep-Dive: Hedging, Load Shedding, Request Coalescing, Deadlines

Source: [Resilience Patterns Deep-Dive: Hedging, Load Shedding, Request Coalescing, Deadlines](30.2.1.19-resilience-patterns-deep-dive.md)

**Q:** Why should a hedged request share the original deadline and operation identity?

**A:** Otherwise hedging expands work beyond the caller's latency budget and can repeat a costly effect. Cancel losers where possible and hedge only safe operations.

## Multi-Region Deployment

Source: [Multi-Region Deployment](30.2.1.20-multi-region-deployment.md)

**Q:** What must a failover plan decide before declaring both regions writable?

**A:** The write authority, conflict policy and fencing/reconciliation behavior during partitions. Routing traffic alone does not preserve invariants.

## TCP & UDP Transport Fundamentals

Source: [TCP & UDP Transport Fundamentals](30.2.1.21-tcp-udp-transport-fundamentals.md)

**Q:** Why does TCP's reliable byte stream not guarantee one business operation?

**A:** It preserves stream delivery within a connection, but connection failure can leave the caller uncertain about application commit. Framing and operation identity remain application concerns.

## DNS & Name Resolution

Source: [DNS & Name Resolution](30.2.1.22-dns-and-name-resolution.md)

**Q:** Why can a DNS change fail to move all clients immediately?

**A:** Resolvers and clients cache answers, connections may be reused, and propagation includes TTL and implementation behavior. Plan overlap instead of assuming an instantaneous cutover.

## TLS, HTTPS & the Certificate Lifecycle

Source: [TLS, HTTPS & the Certificate Lifecycle](30.2.1.23-tls-https-and-certificates.md)

**Q:** What does a valid TLS certificate fail to prove about an application?

**A:** It authenticates the certified endpoint identity under the trust model and supports encrypted transport. It does not prove authorization, business correctness or harmless content.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
