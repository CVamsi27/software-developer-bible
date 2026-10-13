<!-- section: System Design | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-System%20Design-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-12_min-informational)](#)
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

**Q:** A's write finishes before B invokes a read, but B reads the previous value. Which ordering distinction matters?

**A:** Sequential consistency can order B's read before A's write if their separate client program orders permit it. Linearizability cannot: the write's response precedes the read's invocation. A read overlapping the write can instead return the previous value if the entire history admits that order.

**Q:** Must a causally consistent reader retrieve every intermediate value of a repeatedly overwritten register?

**A:** No. A later version can incorporate its causal predecessors without exposing their obsolete values separately. A reply that refers to a separately stored parent still needs a view that respects that dependency. Independent changes need not have one shared total order.

**Q:** Two clients each make a linearizable read of the last item, then each writes a sale. What guarantee is missing?

**A:** The check and claim are separate operations. Their legal order can still allow both clients to decide from stock one. Use an invariant-preserving transaction or authoritative atomic conditional claim. Serializability orders transactions; strict serializability additionally respects real time.

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

**Q:** Do more virtual nodes distribute one extremely popular cache key across servers?

**A:** No. They smooth ownership across many keys; one key still selects one destination. Replicating, caching or splitting that key needs a separate design and consistency contract.


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

**Q:** The API saves a report request, crashes before publishing its message and already returned success. What boundary was missing?

**A:** The database save and broker publish were separate commits. A transactional outbox or another durable recovery protocol must preserve the pending handoff. Returning acceptance alone does not enqueue it.

**Q:** Must a new high-priority message interrupt a low-priority task already executing?

**A:** No. Priority usually selects among eligible queued work. Existing execution, prefetched deliveries and starvation limits affect observed behavior.

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

**Q:** Does two-phase commit imply that a transaction uses two-phase locking?

**A:** No. 2PC coordinates a shared commit/abort decision. 2PL constrains lock acquisition and release for concurrency control. A system can combine them, but atomic outcome and isolation are separate obligations.


## Rate Limiting

Source: [Rate Limiting](30.2.1.08-rate-limiting.md)

Additional sources: [RFC 6585 §4 — 429](https://www.rfc-editor.org/rfc/rfc6585.html#section-4), [RFC 9110 §10.2.3 — Retry-After](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.2.3), [IETF Datatracker — RateLimit header-field draft status](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/)

**Q:** Why can two independent local token buckets exceed a global limit?

**A:** Each grants capacity without knowing the other's grants. A global contract needs coordination or a documented allocation/approximation strategy.

**Q:** The Redis script starts EXPIRE on the first INCR. Is that a sliding window?

**A:** No. It is a first-arrival window with one counter until expiry. A true rolling-window log retains timestamps; a weighted two-window counter is approximate.

**Q:** Two local buckets each grant 100 requests. What is the shared allowance?

**A:** Without coordination or safely allocated budgets they can grant 200. A local fallback changes the global quota even if each local decision is atomic.

**Q:** Is the `RateLimit` header-field document already an HTTP standard?

**A:** No. The IETF Datatracker currently lists it as an active Internet-Draft with no intended RFC status. Treat those fields as draft until the Datatracker shows publication, and follow each API's documented contract.


## Consensus & Leader Election

Source: [Consensus & Leader Election](30.2.1.09-consensus-and-leader-election.md)

**Q:** Can an isolated old Raft leader safely commit new writes alone?

**A:** No. A leader needs the protocol's quorum and commit rules. Its old role label does not authorize an external side effect; a protected resource may need to reject stale fencing tokens as well.

**Q:** A commits X on A+B, then A is isolated. Trace the safe replacement.

**A:** B+C can elect an eligible newer-term leader. Voting/log rules preserve X; A cannot commit fresh entries alone even if it still calls itself leader.

**Q:** What stops a later Paxos proposer replacing an already-chosen value?

**A:** Prepare promises reject lower proposals, and the proposer must carry the highest-numbered accepted value returned by its prepare quorum. Quorum intersection connects the accepted history.

**Q:** Raft commits a debit but the client loses the response. Does retrying guarantee one debit?

**A:** No. Agreement preserves the log, but a retry can become another command. Preserve a stable operation identity and result in the replicated application state; external effects need their own deduplication boundary.

**Q:** Does Zab make every ZooKeeper read current at every replica?

**A:** No. It orders committed state changes; replicas can be at different applied positions. Read freshness follows the service's API contract, not merely its broadcast protocol.


## Failure Modes

Source: [Failure Modes](30.2.1.10-failure-modes.md)

**Q:** Why is a timeout a dangerous trigger for retrying a mutation?

**A:** The first attempt may have committed while its response was lost. Retry only under an appropriate idempotency and reconciliation contract.

**Q:** A 100 ms dependency slows to 2 s and each caller adds two retries. Where does pressure go?

**A:** More work remains in flight, and three attempts per logical request can add load during reduced capacity. Bound admission, waits and retries; isolate critical resources and observe the recovery wave.

**Q:** A heartbeat expires. Does that establish a fail-stop process, or only suspicion?

**A:** Without a reliable failure detector or a bounded-delay assumption, it establishes suspicion. A paused or partitioned process may resume and act. A safe transfer of authority needs the protocol's quorum, epoch or resource-enforced fencing rules, not only a missed heartbeat.


## Architecture Patterns — Monolith, Microservices, Event-Driven, Hexagonal

Source: [Architecture Patterns — Monolith, Microservices, Event-Driven, Hexagonal](30.2.1.11-architecture-patterns.md)

**Q:** What should justify a microservice boundary beyond a diagram box?

**A:** A cohesive domain or operational ownership boundary whose independent evolution is worth its network, consistency and deployment costs.

**Q:** Trace a web request through a hexagonal stock reservation.

**A:** The web adapter calls a use case, which applies rules and uses a repository port. The PostgreSQL adapter implements that port; source dependency points toward the interface even though runtime calls reach the adapter.

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

**Q:** In the same example, what capacity survives losing any one of three equal zones?

**A:** Place 18 instances in each zone, 54 total. Losing one zone leaves 36 instances, enough for the 35K/s tested demand under the stated assumptions.


## Backpressure and Flow Control

Source: [Backpressure and Flow Control](30.2.1.13-backpressure-and-flow-control.md)

**Q:** How can a push protocol provide backpressure without becoming a pull API?

**A:** Credits, bounded windows or explicit pause/resume signals restrict producer progress to consumer capacity. The key is bounded admitted work and a defined overload policy.

**Q:** Arrivals are 10,000 events/s, completions are 1,000/s, and the buffer has 10,000 free slots. About how long until it fills?

**A:** The backlog grows by 9,000 events/s, so 10,000 ÷ 9,000 ≈ 1.11 seconds, assuming constant rates and an initially empty buffer.

**Q:** Does bounding stored items bound total process memory?

**A:** No. Waiting producers, request bodies and in-flight jobs can still accumulate. Bound admission, waiters and deadlines as well as the stored queue.

**Q:** When does an HTTP overload response actually slow its caller?

**A:** Only when the caller respects the rejection and retry delay. Bound attempts and deadlines, add jitter to spread retries, and make duplicate effects safe.


## Distributed Locks and Coordination

Source: [Distributed Locks and Coordination](30.2.1.14-distributed-locks.md)

**Q:** Why is a lease insufficient to stop a paused worker writing after expiry?

**A:** The worker may resume without noticing it lost the lease. The resource must reject stale authority, for example with fencing tokens, or use another transactional safety boundary.

**Q:** Does a random owner token protect a resource from stale writes?

**A:** No. It can make release conditional on the current owner, but a fencing generation must increase across acquisitions and the protected resource must enforce it atomically.

**Q:** A lease expires, but the resource has never seen the replacement's higher epoch. Must an epoch-only fence reject the expired holder?

**A:** No. A fence rejects older epochs only after the resource has observed a newer one. A separate lease check followed by a write still races; ownership and mutation need one atomic enforcement boundary.

**Q:** The acquisition call timed out. Is it safe to retry under a new owner identity and start work?

**A:** No. The coordinator may have granted the first lease before its response was lost. Resolve ownership with a stable operation identity or wait for the possible lease to expire.

## How to Approach Any System Design Problem

Source: [How to Approach Any System Design Problem](30.2.1.15-how-to-approach.md)

**Q:** Why should requirements precede choosing databases in a design interview?

**A:** Required invariants, access patterns and failure behavior determine storage tradeoffs. Choosing products first can produce a design that solves the wrong problem.

**Q:** The interviewer adds globally unique custom aliases after you have sketched the redirect path. What should you do next?

**A:** Restate the new uniqueness invariant, then trace its effect through alias creation, concurrent writes and redirect lookup. Keep unaffected parts of the design and revise only the decisions this requirement changes.

## Probabilistic Data Structures

Source: [Probabilistic Data Structures](30.2.1.17-probabilistic-data-structures.md)

Additional source: [Redis HyperLogLog documentation](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/)
Additional source: [KLL quantile-sketch paper](https://arxiv.org/abs/1603.05346)

**Q:** Why may a Bloom negative skip an exact read but not an authoritative uniqueness write?

**A:** A correctly populated filter can rule out membership in its represented set. Concurrent insertion and durable uniqueness still require atomic enforcement; a hint is not a claim.

**Q:** Why should a Count-Min estimate not enforce a hard per-user rate limit by itself?

**A:** Hash collisions can make one key's estimate include counts from other keys. Use an authoritative counter when a false throttle or quota breach is unacceptable.

**Q:** Why is averaging two shard p99 values not a fleet p99?

**A:** A percentile is a rank in a distribution, not an additive value. Merge compatible histogram bins or quantile sketches with their counts, then estimate the combined rank. A small slow shard and a large fast shard must contribute their actual sample counts.

**Q:** Are HDR histograms probabilistic in the same sense as Bloom filters?

**A:** No. HDR uses deterministic value-range and precision quantization. A t-digest instead compresses samples into weighted centroids with implementation-dependent approximation. Neither recovers every original request latency.

**Q:** Does one HLL hash with a seven-bit rank mean eight distinct values were seen?

**A:** No. Its rank updates one register's maximum. Cardinality is estimated from all registers together, with corrections for the estimator's range and implementation.

**Q:** What does a KLL error of epsilon mean, and why is it not a percent error in latency?

**A:** It bounds rank error by about epsilon times the number of samples, with the configured confidence. For one million observations and epsilon 0.01, the answer may be about 10,000 positions from the target rank; the latency value can differ by much more or much less than one percent.

## Outbox Pattern & Change Data Capture (CDC)

Source: [Outbox Pattern & Change Data Capture (CDC)](30.2.1.18-outbox-and-cdc.md)

**Q:** Which crash window does a transactional outbox close, and which remains?

**A:** It commits business data and publication intent together. The relay can still publish and crash before marking sent, so consumers must tolerate duplicate delivery.

**Q:** Why does an autocommit SKIP LOCKED select fail to claim through publication?

**A:** Its transaction ends when the statement finishes, releasing row locks before the broker call. Use one explicit claim transaction or a recoverable owner/lease protocol.

**Q:** Worker A holds aggregate v1; worker B skips it and publishes v2. Does the same Kafka key restore order?

**A:** No. Kafka preserves append order within its partition, not the desired order of competing relays. Serialize aggregate dispatch or enforce a durable consumer version/gap policy.

**Q:** The API times out while committing the order and outbox row. Is retrying with a new request ID safe?

**A:** No. The commit may have succeeded even though its response was lost. Retry with the same persisted idempotency key and resolve the existing outcome before creating another order or event.


## Resilience Patterns Deep-Dive: Hedging, Load Shedding, Request Coalescing, Deadlines

Source: [Resilience Patterns Deep-Dive: Hedging, Load Shedding, Request Coalescing, Deadlines](30.2.1.19-resilience-patterns-deep-dive.md)

**Q:** Why should a hedged request share the original deadline and operation identity?

**A:** Otherwise hedging expands work beyond the caller's latency budget and can repeat a costly effect. Cancel losers where possible and hedge only safe operations.

**Q:** When is a hedged request likely to help, and what should be measured?

**A:** It can help when the second attempt has an independent chance of finishing sooner. Measure the latency change, duplicate work, cancellation, and shared downstream load; the gain is not guaranteed. See [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/).

**Q:** If two tenants request `user:42`, what must a coalescing key include before they can share a load?

**A:** Include the tenant and every authorization or input dimension that can change the result. Otherwise one caller can receive data loaded for another. Same-key singleflight shares only in-flight work within that process; it does not define a settled-result cache.

**Q:** Does timing out a caller prove the downstream operation stopped?

**A:** No. A local timeout can stop the caller from waiting while remote work continues. Propagate cancellation through the actual client and dependency, then verify that the operation responds to it.


**Q:** Why install a singleflight promise before invoking the loader?

**A:** A synchronous throw must become the shared rejection, and a reentrant caller should find the existing flight. Deferring the loader to a microtask establishes that ordering. The loader must not recursively await its own key.

**Q:** Why is forwarding a wall-clock deadline unchanged across machines unsafe?

**A:** Their clocks can differ. Propagate a remaining budget with elapsed time accounted for, as gRPC does, or define an explicit clock-skew policy for absolute timestamps. A fresh timeout at every hop expands the original budget.

## Multi-Region Deployment

Source: [Multi-Region Deployment](30.2.1.20-multi-region-deployment.md)

**Q:** What must a failover plan decide before declaring both regions writable?

**A:** The write authority, conflict policy and fencing/reconciliation behavior during partitions. Routing traffic alone does not preserve invariants.

**Q:** Why are RPO and RTO not guaranteed by choosing warm standby or active-active?

**A:** They depend on replication state, recovery decisions, dependencies, capacity, and routing. Measure them in a recovery exercise; [AWS's DR options](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html) describe strategies, not universal recovery times.

**Q:** Why can a region failover lose acknowledged writes even when a replica exists?

**A:** With asynchronous replication, a primary can acknowledge a write before the standby receives it. The recovery point depends on lag and the failure. Check replication state and the application's RPO before promoting; do not assume that a replica is current.

**Q:** What does DynamoDB's MRSC mode require, and what does its zero-RPO guarantee cost?

**A:** MRSC requires exactly three supported Regions, configured as three replicas or two replicas plus a witness. Cross-region coordination raises write and strong-read latency; transactions, TTL and local secondary indexes are unsupported. Competing same-item writes can fail with `ReplicatedWriteConflictException`; retry only with an application-safe, bounded policy. This is a DynamoDB contract, not a universal property of synchronous replication. See [AWS's global-table behavior](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_HowItWorks.html).

**Q:** Can a transaction written to an MREC replica be assumed atomic when read from another Region?

**A:** No. MREC replicates items individually. A transaction is atomic in the Region that runs it, but another replica can expose a partial set while its writes propagate. Keep cross-item invariants behind one authority or a protocol that provides the needed global atomicity. See [AWS's MREC and MRSC limits](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_HowItWorks.html).

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


**Q:** SOA TTL is 300 seconds and SOA.MINIMUM is 60. What bounds ordinary negative caching?

**A:** The lesser value, 60 seconds, under RFC 2308. A positive A record's TTL is a different cache policy; changing it does not flush a previously cached NXDOMAIN.

**Q:** Can an HTTPS DNS record change which hostname the TLS certificate must identify?

**A:** No. HTTPS/SVCB records can advertise a target, port, ALPN and ECH configuration, but the client still validates the certificate against its intended service identity. ECH can hide the inner SNI when negotiated; the chosen DNS resolver still sees its query. See [RFC 9460](https://www.rfc-editor.org/rfc/rfc9460.html), [RFC 9848](https://www.rfc-editor.org/rfc/rfc9848.html), and [RFC 9525](https://www.rfc-editor.org/rfc/rfc9525.html).

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


**Q:** Does TLS 1.3 resumption always remove a handshake round trip?

**A:** No. Normal full and resumed handshakes commonly both take one RTT. Resumption avoids certificate exchange and some authentication work; eligible 0-RTT early data changes when application data can be sent and introduces replay and forward-secrecy limits.

**Q:** Does a DNS CNAME change the name a TLS client checks in a certificate?

**A:** No. The client matches a `subjectAltName` to the reference identity it intended to reach. A CNAME changes how DNS locates the endpoint; it does not replace that expected identity, and a Common Name fallback is not valid under current service-identity rules. See [RFC 9525](https://www.rfc-editor.org/rfc/rfc9525.html).

**Q:** Does HTTP/3 carry application data in TLS records over TCP?

**A:** No. QUIC uses the TLS 1.3 handshake and key schedule, then carries HTTP/3 in QUIC streams and protects QUIC packets. UDP carries those packets; QUIC provides the transport guarantees. See [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html).

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
