<!-- section: System Design | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-System%20Design-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-8_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Theory — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## CAP Theorem & PACELC

Source: [CAP Theorem & PACELC](30.2.1.01-cap-theorem.md)

**Q:** During a partition, what conflict does CAP identify for a replicated register?

**A:** Under the theorem's network-partition assumptions, an implementation cannot guarantee both linearizable operations—operations that appear to take effect one at a time between their start and completion—and an eventual response to every request on a non-failing node. It is not a universal choose-two menu in normal operation.

**Q:** A acknowledges booking during a partition. Trace B's attempt to read the slot.

**A:** B cannot tell whether A booked it. Returning free from its old state can violate the real-time single-copy contract; waiting or refusing the unsafe operation gives up availability for it. A connected majority can still serve safe requests.

**Q:** What changes if a standby has flushed a write's log but not applied it?

**A:** Durability evidence is not yet read visibility. An ordinary standby query can lag; specify remote-apply acknowledgment or a read/version barrier when that visibility is required, with appropriate failover rules.

## Data Consistency Models

Source: [Data Consistency Models](30.2.1.02-consistency-models.md)

**Q:** Why do read-your-writes and monotonic reads not form a single stronger/weaker ladder?

**A:** They constrain different histories: one preserves a client's own writes, the other prevents its reads from moving backward. A system can provide one without the other.

**Q:** Trace a user write on A followed by refresh from a lagging B.

**A:** Returning the old value violates read-your-writes if that session was promised its acknowledged change. Route to an authority containing it or wait for B to reach the carried version. Other clients may still observe older data under a weaker contract.

**Q:** Does seeing x=5 and later x=3 always violate monotonic reads?

**A:** No. It violates the guarantee if 3 comes from an older history/version. A newer accepted update can legitimately decrease the value. Compare observed versions, not arithmetic magnitude.

## Sharding & Replication

Source: [Sharding & Replication](30.2.1.03-sharding-and-replication.md)

**Q:** Why can a good average shard size still hide a scaling failure?

**A:** A hot key or uneven request distribution can overload one shard while others remain idle. Measure work per shard, not just bytes or record counts.

**Q:** Tenant 42 moves A→B. Why is copying its rows insufficient?

**A:** New writes can still arrive at A during the copy. Capture the delta, validate B, transfer routing authority and reject old-generation writes before admitting B as the owner.

**Q:** Does one leader eliminate every write conflict?

**A:** It orders accepted writes, but two clients can still overwrite one another without the required transaction or version check. Replication topology does not replace the data invariant.


## Load Balancing

Source: [Load Balancing](30.2.1.04-load-balancing.md)

**Q:** What failure can sticky routing mask until failover?

**A:** A client's consistency or session state may depend on one backend. Failover needs shared state or explicit consistency tokens rather than assuming the next node is equivalent.

**Q:** Trace 100 HTTP/2 requests over one L4-balanced connection.

**A:** The balancer chooses its backend when the connection begins; multiplexed requests remain on that backend. A configured HTTP-aware proxy can choose upstreams at request granularity.

**Q:** What changes when a draining backend committed an update before losing its reply?

**A:** Routing a retry elsewhere does not prove failure of the first attempt. Preserve operation identity and reconcile the effect under the mutation contract.


## Caching Patterns

Source: [Caching Patterns](30.2.1.05-caching-patterns.md)

**Q:** Why is cache invalidation part of the write contract?

**A:** The system must decide which reads may see old values and how updates, races and TTLs converge. A cache hit is only correct under that staleness contract.

**Q:** A reader loads v1, a writer commits v2 and deletes the key, then the reader fills v1. What did invalidation miss?

**A:** The delayed fill occurs after deletion. Define an authoritative/versioned fill boundary or an acceptable stale window; successful DEL alone does not order source reads.

**Q:** Does a fresh TTL prove that the source value is equally fresh?

**A:** No. The loader may insert an already-old value, and stale-serving policies can extend reuse. TTL bounds an installed entry only under the actual expiry policy.


## Message Queues & Async Patterns

Source: [Message Queues & Async Patterns](30.2.1.06-queues-and-async.md)

**Q:** Why should a consumer acknowledge a message after committing its local effect?

**A:** Acknowledging first can lose work if the process crashes. Committing first permits redelivery, so the local effect also needs transactional deduplication.

**Q:** Trace a crash after the local effect commits but before acknowledgment.

**A:** The broker may redeliver. A processed-event identity committed with the effect lets the consumer skip the repeated effect; a separate marker written later leaves a crash window.

**Q:** Why can per-partition delivery order still produce out-of-order effects?

**A:** The consumer can start parallel tasks or retry earlier work while later work completes. Control in-flight work and define aggregate versions or a gap policy when effect order matters.


## Distributed Transactions

Source: [Distributed Transactions](30.2.1.07-distributed-transactions.md)

**Q:** What contract does a saga give up compared with atomic commit?

**A:** It permits visible intermediate local commits and attempts recovery with later business actions. It does not provide one globally atomic rollback; retry limits, terminal failures and reconciliation need explicit design.

**Q:** Both participants prepare, order commits, stock times out. Can stock abort on its own?

**A:** No. The coordinator may have durably decided commit and already delivered it elsewhere. Stock must learn the durable decision; uncertainty can block conflicting work.

**Q:** Does shared atomic commit mean arbitrary readers see both databases switch simultaneously?

**A:** No. The eventual commit/abort decision is shared; read visibility and isolation across independent resources need their own contract.


## Rate Limiting

Source: [Rate Limiting](30.2.1.08-rate-limiting.md)

**Q:** Why can two independent local token buckets exceed a global limit?

**A:** Each grants capacity without knowing the other's grants. A global contract needs coordination or a documented allocation/approximation strategy.

**Q:** The Redis script starts EXPIRE on the first INCR. Is that a sliding window?

**A:** No. It is a first-arrival window with one counter until expiry. A true rolling-window log retains timestamps; a weighted two-window counter is approximate.

**Q:** Two local buckets each grant 100 requests. What is the shared allowance?

**A:** Without coordination or safely allocated budgets they can grant 200. A local fallback changes the global quota even if each local decision is atomic.


## Consensus & Leader Election

Source: [Consensus & Leader Election](30.2.1.09-consensus-and-leader-election.md)

**Q:** Can an isolated old Raft leader safely commit new writes alone?

**A:** No. A leader needs the protocol's quorum and commit rules. Its old role label does not authorize an external side effect; a protected resource may need to reject stale fencing tokens as well.

**Q:** A commits X on A+B, then A is isolated. Trace the safe replacement.

**A:** B+C can elect an eligible newer-term leader. Voting/log rules preserve X; A cannot commit fresh entries alone even if it still calls itself leader.

**Q:** What stops a later Paxos proposer replacing an already-chosen value?

**A:** Prepare promises reject lower proposals, and the proposer must carry the highest-numbered accepted value returned by its prepare quorum. Quorum intersection connects the accepted history.


## Failure Modes

Source: [Failure Modes](30.2.1.10-failure-modes.md)

**Q:** Why is a timeout a dangerous trigger for retrying a mutation?

**A:** The first attempt may have committed while its response was lost. Retry only under an appropriate idempotency and reconciliation contract.

**Q:** A 100 ms dependency slows to 2 s and each caller adds two retries. Where does pressure go?

**A:** More work remains in flight, and three attempts per logical request can add load during reduced capacity. Bound admission, waits and retries; isolate critical resources and observe the recovery wave.


## Architecture Patterns — Monolith, Microservices, Event-Driven, Hexagonal

Source: [Architecture Patterns — Monolith, Microservices, Event-Driven, Hexagonal](30.2.1.11-architecture-patterns.md)

**Q:** What should justify a microservice boundary beyond a diagram box?

**A:** A cohesive domain or operational ownership boundary whose independent evolution is worth its network, consistency and deployment costs.

**Q:** Trace an HTTP request through a hexagonal stock reservation.

**A:** The HTTP adapter calls a use case, which applies rules and uses a repository port. The PostgreSQL adapter implements that port; source dependency points toward the interface even though runtime calls reach the adapter.

**Q:** What does an in-memory adapter test fail to establish?

**A:** It can test use-case decisions but cannot establish real database locks, constraints, transactional isolation or provider integration.


## Capacity Planning & Back-of-Envelope Estimation

Source: [Capacity Planning & Back-of-Envelope Estimation](30.2.1.12-capacity-planning.md)

**Q:** Why should capacity calculations use peak load and headroom rather than average QPS alone?

**A:** Bursts, skew, failover and maintenance can concentrate work. Average load hides queues and saturation at the periods that determine service reliability.

**Q:** At 10K arrivals/s and 1K completions/s, how long to accumulate 1M messages?

**A:** About 1,000,000÷9,000=111 seconds under constant rates and no shedding. Memory depends on payload and overhead; this is not a universal crash point.

**Q:** A tested instance serves 1K/s, demand is 35K/s, and one instance may fail. What is the minimum under those assumptions?

**A:** 36 instances keep 35 tested instances after one loss. Zone-loss, autoscaling delay, traffic skew and downstream limits can require a different topology or more headroom.


## Backpressure & Flow Control

Source: [Backpressure & Flow Control](30.2.1.13-backpressure-and-flow-control.md)

**Q:** How can a push protocol provide backpressure without becoming a pull API?

**A:** Credits, bounded windows or explicit pause/resume signals restrict producer progress to consumer capacity. The key is bounded admitted work and a defined overload policy.

**Q:** A blocked enqueue wakes, but a newcomer fills the slot first. What must the awakened writer do?

**A:** Recheck the capacity condition before storing its item. One wakeup is not a reserved slot; an if-only check can overfill the queue.

**Q:** Does bounding stored items bound total process memory?

**A:** No. Waiting producers, request bodies and in-flight jobs can still accumulate. Bound admission, waiters and deadlines as well as the stored queue.


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

**Q:** Why should a Count-Min estimate not enforce a hard per-user rate limit by itself?

**A:** Hash collisions can make one key's estimate include counts from other keys. Use an authoritative counter when a false throttle or quota breach is unacceptable.

## Outbox Pattern & Change Data Capture (CDC)

Source: [Outbox Pattern & Change Data Capture (CDC)](30.2.1.18-outbox-and-cdc.md)

**Q:** Which crash window does a transactional outbox close, and which remains?

**A:** It commits business data and publication intent together. The relay can still publish and crash before marking sent, so consumers must tolerate duplicate delivery.

**Q:** Why does an autocommit SKIP LOCKED select fail to claim through publication?

**A:** Its transaction ends when the statement finishes, releasing row locks before the broker call. Use one explicit claim transaction or a recoverable owner/lease protocol.

**Q:** Worker A holds aggregate v1; worker B skips it and publishes v2. Does the same Kafka key restore order?

**A:** No. Kafka preserves append order within its partition, not the desired order of competing relays. Serialize aggregate dispatch or enforce a durable consumer version/gap policy.


## Resilience Patterns Deep-Dive: Hedging, Load Shedding, Request Coalescing, Deadlines

Source: [Resilience Patterns Deep-Dive: Hedging, Load Shedding, Request Coalescing, Deadlines](30.2.1.19-resilience-patterns-deep-dive.md)

**Q:** Why should a hedged request share the original deadline and operation identity?

**A:** Otherwise hedging expands work beyond the caller's latency budget and can repeat a costly effect. Cancel losers where possible and hedge only safe operations.

**Q:** When is a hedged request likely to help, and what should be measured?

**A:** It can help when the second attempt has an independent chance of finishing sooner. Measure the latency change, duplicate work, cancellation, and shared downstream load; the gain is not guaranteed. See [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/).

**Q:** With p-memoize cache:false, when do same-key callers share work?

**A:** Concurrent executions share their in-flight result; settled results are not retained for later calls. A time-expiring result cache is a distinct policy.

**Q:** Does aborting fetch prove the remote operation stopped?

**A:** No. The client can stop waiting or reading while the server continues. Propagate cancellation and verify the actual remote lifecycle when that matters.


## Multi-Region Deployment

Source: [Multi-Region Deployment](30.2.1.20-multi-region-deployment.md)

**Q:** What must a failover plan decide before declaring both regions writable?

**A:** The write authority, conflict policy and fencing/reconciliation behavior during partitions. Routing traffic alone does not preserve invariants.

**Q:** Why are RPO and RTO not guaranteed by choosing warm standby or active-active?

**A:** They depend on replication state, recovery decisions, dependencies, capacity, and routing. Measure them in a recovery exercise; [AWS's DR options](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html) describe strategies, not universal recovery times.

**Q:** Why can a region failover lose acknowledged writes even when a replica exists?

**A:** With asynchronous replication, a primary can acknowledge a write before the standby receives it. The recovery point depends on lag and the failure. Check replication state and the application's RPO before promoting; do not assume that a replica is current.

**Q:** A has component 3 and B has 2; merge B twice. What is the count?

**A:** The component-wise maximum remains {A:3,B:2}, total 5. Repeated state delivery does not add B twice.

**Q:** Two writers both increment actor A from 3 to 4. Does merge retain both increments?

**A:** No. Maximum yields 4, losing one increment. Each actor component requires one durable monotonic owner; region labels alone do not supply that protocol.


## TCP & UDP Transport Fundamentals

Source: [TCP & UDP Transport Fundamentals](30.2.1.21-tcp-udp-transport-fundamentals.md)

**Q:** Why does TCP's reliable byte stream not guarantee one business operation?

**A:** It preserves stream delivery within a connection, but connection failure can leave the caller uncertain about application commit. Framing and operation identity remain application concerns.

**Q:** What does QUIC's 0-RTT mode trade, and why is it unsuitable for some requests?

**A:** It can send application data before the handshake finishes, reducing setup delay on eligible resumed connections. Early data can be replayed, so the operation must be safe under replay; see [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).

**Q:** What should you include when estimating the first HTTPS response on a new connection?

**A:** Count DNS if needed, TCP setup, TLS setup, the request/response path, and server work. State whether resumption or connection reuse applies; [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html) specifies TCP, while TLS 1.3 setup is described in [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).

**Q:** Why does HTTP/3 use QUIC over UDP instead of sending HTTP directly over UDP?

**A:** QUIC provides reliable ordered streams, flow control, congestion control, encryption, and connection migration. UDP is its carrier, not the source of those guarantees; see [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html) and [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html).

## DNS & Name Resolution

Source: [DNS & Name Resolution](30.2.1.22-dns-and-name-resolution.md)

**Q:** Why can a DNS change fail to move all clients immediately?

**A:** Resolvers and clients cache answers, connections may be reused, and propagation includes TTL and implementation behavior. Plan overlap instead of assuming an instantaneous cutover.

**Q:** A new DNS record exists, but some clients still report NXDOMAIN. What should you check?

**A:** Check whether a resolver cached a negative answer before the record was created, then inspect the SOA data and resolver cache lifetime. Keep the old path available during a change when possible; see [RFC 2308](https://www.rfc-editor.org/rfc/rfc2308.html).

**Q:** Why can lowering a record's TTL shortly before a migration fail to speed up the cutover?

**A:** Resolvers may already have cached the record using its previous, longer TTL. Lower the TTL ahead of the change, allow old cached answers to expire, and account for open connections and client behavior. See [Kubernetes DNS guidance](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) for resolver settings in pods.

**Q:** A TTL expires. Has the authoritative DNS record disappeared?

**A:** No. Only that cached answer expires. The resolver can refresh from the authoritative record; unavailable or incorrect authority then determines the result.


## TLS, HTTPS & the Certificate Lifecycle

Source: [TLS, HTTPS & the Certificate Lifecycle](30.2.1.23-tls-https-and-certificates.md)

**Q:** What does a valid TLS certificate fail to prove about an application?

**A:** It authenticates the certified endpoint identity under the trust model and supports encrypted transport. It does not prove authorization, business correctness or harmless content.

**Q:** What security properties does TLS 1.3 early data give up compared with normal application data?

**A:** 0-RTT data can be replayed and does not have full forward secrecy. Applications should accept it only when repeated processing is safe; TLS itself does not make a request idempotent. See [RFC 8446, Sections 2.3 and 8](https://www.rfc-editor.org/rfc/rfc8446.html).

**Q:** Why does renewing a certificate require more than obtaining a new certificate file?

**A:** The deployed endpoint must load the renewed certificate and chain, keep the private key protected, and continue validating correctly. Monitor the certificate clients receive after deployment; [ACME (RFC 8555)](https://www.rfc-editor.org/rfc/rfc8555.html) defines an issuance protocol, not your deployment or reload process.

**Q:** In a full TLS 1.3 certificate handshake, when does the server send Finished?

**A:** It sends Finished in its first server flight after the encrypted certificate and CertificateVerify. The client validates that flight and sends its own Finished.

**Q:** Does enabling OCSP stapling work for a current Let's Encrypt certificate?

**A:** No. Let's Encrypt ended its OCSP service on 6 August 2025 and supplies CRLs. Revocation configuration must match the issuer and client mechanism.


## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
