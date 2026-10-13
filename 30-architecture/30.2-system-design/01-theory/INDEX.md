# System Design — Foundational Theory

> **Study time:** ≈ 4 h 56 m of reading (24 files, ~12 min average).
> **Study time and file counts are generated from the current chapter set.**

[![Files](https://img.shields.io/badge/files-24-blue)](../../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Begin with [How to Approach](30.2.1.15-how-to-approach.md) and [Capacity Planning](30.2.1.12-capacity-planning.md). Review the TCP, DNS and TLS prerequisites when a prompt depends on network behavior; then follow the consistency, placement, traffic and recovery sequence below. After the theory revision and separate interview drill, move to [../02-case-studies/](../02-case-studies/INDEX.md).

---

## Topic Categories

The theory chapters are grouped by the question they help answer.

| Category | Files | Why it matters |
| -------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data & Consistency** | 6 | CAP/PACELC, consistency models, sharding and replication, distributed transactions, consensus and leader election, distributed locks |
| **Traffic & Scale** | 7 | Load balancing, TCP/UDP transport, DNS, TLS/HTTPS, rate limiting, backpressure, capacity planning |
| **Performance & Delivery** | 3 | Caching, queues and asynchronous work, transactional outbox and CDC |
| **Reliability & Topology** | 4 | Failure modes, resilience, multi-region deployment, architecture patterns |
| **The Method + Drills** | 2 | Interview approach and 30 system-design practice prompts |
| **Senior Toolkit** | 1 | Probabilistic structures and Merkle trees, with their different uses and limits |

---

## Foundational concepts (read in order)

These chapters supply the main building blocks. The sequence moves from data guarantees to traffic, coordination and recovery; revisit a prerequisite when a later example depends on it.

| # | File | Concepts | Why it matters | Role priority | General importance |
| --- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| 1 | [CAP Theorem & PACELC](30.2.1.01-cap-theorem.md) | Consistency, availability, partitions, and the PACELC trade-off | Understand which guarantees can be kept during a partition and what latency or consistency trade-offs remain. | Essential | Foundational |
| 2 | [Data Consistency Models](30.2.1.02-consistency-models.md) | Linearizability, eventual and causal consistency, read-your-writes, monotonic reads | Match the read guarantee to what each operation needs users to observe. | Essential | Foundational |
| 3 | [Sharding & Replication](30.2.1.03-sharding-and-replication.md) | Hash, range and directory sharding; single-leader, multi-leader and leaderless replication | Distinguish splitting data for capacity from copying it for availability or read scale. | Essential | Foundational |
| 4 | [Load Balancing](30.2.1.04-load-balancing.md) | L4 vs L7, routing algorithms, health checks | Understand what information each routing strategy uses and how health decisions affect traffic. | Essential | Foundational |
| 5 | [Caching Patterns](30.2.1.05-caching-patterns.md) | Cache-aside and other read/write patterns; capacity eviction and independent expiry | Choose what can be cached, how it stays acceptably fresh, and what happens on a miss or cache loss. | Essential | Foundational |
| 6 | [Queues & Async](30.2.1.06-queues-and-async.md) | Point-to-point and pub/sub, delivery scope, idempotency, recovery, ordering | Decide when deferred work helps and how consumers recover from retries, duplicates and backlog. | Essential | Foundational |
| 7 | [Distributed Transactions](30.2.1.07-distributed-transactions.md) | Two-phase commit, three-phase commit, saga choreography and orchestration | Compare coordination protocols and workflows; a saga uses local transactions and compensation, not global atomicity. | Essential | Foundational |
| 8 | [Rate Limiting](30.2.1.08-rate-limiting.md) | Fixed and sliding windows, token and leaky buckets, distributed limits | Select a policy and algorithm based on burst, fairness, precision and coordination requirements. | Essential | Foundational |
| 9 | [Consensus & Leader Election](30.2.1.09-consensus-and-leader-election.md) | Paxos, Raft, Zab, leader election and split brain | Learn how replicated systems agree and why a lease or elected leader alone may not prevent stale writes. | Essential | Foundational |
| 10 | [Failure Modes](30.2.1.10-failure-modes.md) | Hardware, software, network and human failures; retries, circuit breakers and bulkheads | Trace failures across dependencies and choose bounded recovery behavior. | Essential | Foundational |
| 11 | [Architecture Patterns](30.2.1.11-architecture-patterns.md) | Monolith, modular monolith, microservices, event-driven, hexagonal, clean and microkernel | Compare boundaries and operating costs before choosing a structure for a team and domain. | Essential | Foundational |
| 12 | [Capacity Planning](30.2.1.12-capacity-planning.md) | Request rates, storage, bandwidth, memory and Little's Law | Estimate resource needs from explicit assumptions and validate them with measurements. | Essential | Foundational |
| 13 | [Backpressure & Flow Control](30.2.1.13-backpressure-and-flow-control.md) | Blocking, buffering, dropping, load shedding and flow control | Keep producers from overwhelming consumers and make overload behavior explicit. | Essential | Foundational |
| 14 | [Distributed Locks](30.2.1.14-distributed-locks.md) | Redis, ZooKeeper, etcd, PostgreSQL advisory locks and fencing tokens | Compare coordination options and protect writes against expired or stale lock holders. | Essential | Foundational |

## Supporting guides and network prerequisites (consult as needed)

| # | File | What it covers | Role priority | General importance |
| --- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ |
| 15 | [How to Approach](30.2.1.15-how-to-approach.md) | A practical interview flow: clarify → estimate → sketch → deep-dive. Adapt it to the prompt and time available. | Essential | Foundational |
| 17 | [Probabilistic Data Structures](30.2.1.17-probabilistic-data-structures.md) | Bloom filter, HyperLogLog, Count-Min Sketch and Cuckoo filter for approximate membership, cardinality and frequency; Merkle trees as a deterministic integrity structure; t-digest quantiles and deterministic HDR histogram quantization. | Essential | Foundational |
| 18 | [Outbox & CDC](30.2.1.18-outbox-and-cdc.md) | Transactional outbox + change data capture — solving the dual-write problem for reliable event publication | Essential | Foundational |
| 19 | [Resilience Patterns Deep-Dive](30.2.1.19-resilience-patterns-deep-dive.md) | Tail latency and overload controls: hedging, bounded admission, coalescing, deadlines, adaptive concurrency | Essential | Foundational |
| 20 | [Multi-Region Deployment](30.2.1.20-multi-region-deployment.md) | Active-passive vs active-active, geo-routing, cross-region replication, conflict resolution, explicit data-location requirements, RPO/RTO | Essential | Foundational |
| 21 | [TCP & UDP Transport Fundamentals](30.2.1.21-tcp-udp-transport-fundamentals.md) | Where transport sits, three-way handshake + cost arithmetic, seq/ack retransmission, flow/congestion control (slow start/AIMD), UDP datagram model, TCP-vs-UDP decision table, HOL blocking, connection reuse economics, TLS-on-TCP, QUIC rationale | Essential | Foundational |
| 22 | [DNS & Name Resolution](30.2.1.22-dns-and-name-resolution.md) | Hierarchy and delegation, the resolution walk (stub → recursive → root → TLD → authoritative), record types, TTL as the agility-vs-cache trade, negative caching and the propagation myth, DNS as traffic steering with measured recovery behavior, anycast, DoH/DoT, DNSSEC, Kubernetes `ndots` traps | Essential | Foundational |
| 23 | [TLS, HTTPS & the Certificate Lifecycle](30.2.1.23-tls-https-and-certificates.md) | Handshake vs record layer, hybrid crypto (ECDHE + AEAD), certificates and the chain of trust, DV/OV/EV, forward secrecy, resumption and 0-RTT replay risk, revocation/HSTS, termination points and mTLS, ACME automation | Essential | Foundational |

---

After the learning chapters, use [Theory revision](REVISION.md), then the separate [30 design prompts](30.2.1.16-interview-questions.md). Chapter IDs remain stable even though interview practice comes last in the learning flow.

**Next:** [Case studies →](../02-case-studies/INDEX.md)

**Cross-references:** [Design Patterns](../../30.1-design-patterns/INDEX.md) | [Microservices](../../../20-backend/20.6-microservices/INDEX.md) | [Database](../../../20-backend/20.4-database/INDEX.md) | [REST APIs](../../../20-backend/20.3-rest-apis/INDEX.md) | [WebSockets](../../../60-realtime/60.1-websockets/INDEX.md)

---

## Reading Path and Completion Check

Begin with problem framing and capacity estimates, then review network fundamentals as the design requires. Work through storage and consistency before coordination, delivery and resilience; return to the relevant prerequisite when a case exposes a dependency.

Trace a partition, timeout and retry through a chosen design; state the exact invariant, authority and recovery mechanism. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Navigation

[← Previous: System Design Index](../INDEX.md) · [ Back to System Design Index](../INDEX.md) · [Next: Case Studies →](../02-case-studies/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — actually implements this theory.

| Topic | Docita evidence |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rate limiting | `shared/modules/tenant-rate-limit/*` (guard + service + repository), plus `ip-rate-limit.service.ts`, `user-rate-limit.service.ts`, `rate-limit.interceptor.ts` |
| Queues & DLQ | `apps/api/src/shared/modules/queue/postgres-queue.service.ts` + `dlq-replay.scheduler.ts`/`dlq.controller.ts`; ADR 0001 "Postgres as queue"; dedicated `apps/worker` process |
| Distributed locks | `shared/common/utils/postgres-advisory-lock.ts` |
| Consensus / leader election | `apps/api/src/shared/modules/schedule/cron-heartbeat.ts` records runs, not ownership; selective advisory-lock callers and API scheduler disablement are separate controls |
| Backpressure | `apps/api/src/shared/common/extensions/query-budget.extension.ts`; Fly-level concurrency caps (`soft_limit 60 / hard_limit 100`) in `fly.toml` |
| Failure modes & resilience | `ops-alert.service.ts` + listener; runbooks in `docs/operations/playbooks/*` (razorpay outage, DB exhaustion, queue backlog) |

_Capacity planning and multi-region: no direct docita implementation yet._ The network-stack chapters (TCP/UDP, DNS, TLS) stay conceptual here — nearest real anchors are `fetch-with-timeout.ts` for calls using that helper and the configured Fly/Cloudflare hosting boundaries. Verify actual DNS, TLS and egress paths rather than inferring universal coverage.
