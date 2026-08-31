# System Design — Foundational Theory

> **21 files** — The conceptual foundation you need BEFORE doing any case study. Every system design interview question touches at least 3-4 of these.

[![Files](https://img.shields.io/badge/files-21-blue)](../../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Read all 14 foundational files first**, then the 6 meta guides and the transport deep-dive. After this, move to [../02-case-studies/](../02-case-studies/INDEX.md).

---

## Topic Categories

The 21 files classify into 6 conceptual categories — the "GoF classification" of distributed systems theory.

| Category                   | Files | Why it matters                                                                                                                   |
| ----------                   | ------: | ----------------                                                                                                                   |
| **Data & Consistency**     | 6     | CAP/PACELC, consistency models, sharding & replication, distributed transactions, consensus & leader election, distributed locks |
| **Traffic & Scale**        | 5     | Load balancing, TCP/UDP transport fundamentals, rate limiting, backpressure & flow control, capacity planning                    |
| **Performance & Delivery** | 3     | Caching patterns, queues & async, outbox & CDC                                                                                   |
| **Reliability & Topology** | 4     | Failure modes, resilience deep-dive, multi-region deployment, architecture patterns                                              |
| **The Method + Drills**    | 2     | How-to-approach framework, 50+ interview questions                                                                               |
| **Senior Toolkit**         | 1     | Probabilistic data structures — bounded-memory answers at scale                                                                  |

---

## Foundational concepts (read in order)

These 14 are the building blocks. Read in this order — each builds on the previous.

| #  | File                                                                      | Concepts                                                                                                   | Why it matters                                                                            |
| ---  | ------                                                                      | ----------                                                                                                   | ----------------                                                                            |
| 1  | [CAP Theorem & PACELC](30.2.1.01-cap-theorem.md)                          | Consistency, Availability, Partition tolerance, CP vs AP trade-offs, PACELC extension                      | The single most important distributed systems concept. Pick CP or AP for every operation. |
| 2  | [Data Consistency Models](30.2.1.02-consistency-models.md)                | Linearizability, eventual, causal, read-your-writes, monotonic reads                                       | Pick per operation, not per system. Most real systems are a mix.                          |
| 3  | [Sharding & Replication](30.2.1.03-sharding-and-replication.md)           | Hash/range/directory sharding, single-leader/multi-leader/leaderless replication                           | How to actually scale a database. Both are needed.                                        |
| 4  | [Load Balancing](30.2.1.04-load-balancing.md)                             | L4 vs L7, round-robin/least-connections/consistent-hashing/IP-hash, health checks                          | Traffic distribution. Pick the wrong algorithm and one server melts.                      |
| 5  | [Caching Patterns](30.2.1.05-caching-patterns.md)                         | Cache-aside, read-through, write-through, write-behind, refresh-ahead, write-around + LRU/LFU/TTL eviction | The #1 lever for performance. Know all 6 patterns.                                        |
| 6  | [Queues & Async](30.2.1.06-queues-and-async.md)                           | Point-to-point vs pub/sub, at-least-once vs exactly-once, idempotency, DLQ, ordering                       | Async is the backbone of scalable systems. Know delivery guarantees.                      |
| 7  | [Distributed Transactions](30.2.1.07-distributed-transactions.md)         | 2PC, 3PC, Saga (choreography + orchestration)                                                              | Atomicity across services. Saga is the production answer.                                 |
| 8  | [Rate Limiting](30.2.1.08-rate-limiting.md)                               | Fixed/sliding window, token bucket, leaky bucket, Redis-based distributed                                  | Protect from abuse. Token bucket is the default.                                          |
| 9  | [Consensus & Leader Election](30.2.1.09-consensus-and-leader-election.md) | Paxos, Raft, Zab, leader election, split brain, distributed locks                                          | How databases agree on who's leader. Raft is the default.                                 |
| 10 | [Failure Modes](30.2.1.10-failure-modes.md)                               | Hardware, software, network, human failures, retries, circuit breakers, bulkheads                          | Everything fails. Plan for it.                                                            |
| 11 | [Architecture Patterns](30.2.1.11-architecture-patterns.md)               | Monolith, modular monolith, microservices, event-driven, hexagonal, clean, microkernel                     | Pick the right architecture for the team and domain.                                      |
| 12 | [Capacity Planning](30.2.1.12-capacity-planning.md)                       | QPS, storage, bandwidth, memory, Little's Law                                                              | Estimate first, design second. Numbers, not vibes.                                        |
| 13 | [Backpressure & Flow Control](30.2.1.13-backpressure-and-flow-control.md) | Blocking, dropping, load shedding, circuit breakers                                                        | When consumer is slower than producer. Without it, OOM.                                   |
| 14 | [Distributed Locks](30.2.1.14-distributed-locks.md)                       | Redis Redlock, ZooKeeper, etcd, Postgres advisory, fencing tokens                                          | Mutual exclusion across machines. Know the fencing problem.                               |

## Meta guides & transport deep-dive (read after the 14)

| #  | File                                                                            | What it covers                                                                                                                                                                                                                                      |
| ---  | ------                                                                            | ----------------                                                                                                                                                                                                                                      |
| 15 | [How to Approach](30.2.1.15-how-to-approach.md)                                 | 4-phase framework: clarify → estimate → high-level → deep-dive. The structure to use in every interview.                                                                                                                                            |
| 16 | [Interview Questions](30.2.1.16-interview-questions.md)                         | 50+ curated system design questions with answers, organized by difficulty.                                                                                                                                                                          |
| 17 | [Probabilistic Data Structures](30.2.1.17-probabilistic-data-structures.md)     | Bloom filter, HyperLogLog, Count-Min Sketch, Cuckoo filter, Merkle tree — fixed-memory, bounded-error answers to "seen?", "how many unique?", "how often?"                                                                                          |
| 18 | [Outbox & CDC](30.2.1.18-outbox-and-cdc.md)                                     | Transactional outbox + change data capture — solving the dual-write problem for reliable event publication                                                                                                                                          |
| 19 | [Resilience Patterns Deep-Dive](30.2.1.19-resilience-patterns-deep-dive.md)     | Request hedging, load shedding, request coalescing, deadline propagation — the senior-level tail-latency toolkit                                                                                                                                    |
| 20 | [Multi-Region Deployment](30.2.1.20-multi-region-deployment.md)                 | Active-passive vs active-active, geo-routing, cross-region replication, conflict resolution, GDPR data residency, RPO/RTO                                                                                                                           |
| 21 | [TCP & UDP Transport Fundamentals](30.2.1.21-tcp-udp-transport-fundamentals.md) | Where transport sits, three-way handshake + cost arithmetic, seq/ack retransmission, flow/congestion control (slow start/AIMD), UDP datagram model, TCP-vs-UDP decision table, HOL blocking, connection reuse economics, TLS-on-TCP, QUIC rationale |

---

**Next:** [Case studies →](../02-case-studies/INDEX.md)

**Cross-references:** [Design Patterns](../../30.1-design-patterns/INDEX.md) | [Microservices](../../../20-backend/20.6-microservices/INDEX.md) | [Database](../../../20-backend/20.4-database/INDEX.md) | [REST APIs](../../../20-backend/20.3-rest-apis/INDEX.md) | [WebSockets](../../../60-realtime/60.1-websockets/INDEX.md)

---

## Navigation

[← Previous: System Design Index](../INDEX.md) · [ Back to System Design Index](../INDEX.md) · [Next: Case Studies →](../02-case-studies/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — actually implements this theory.

| Topic                       | Docita evidence                                                                                                                                                 |
| -------                       | -----------------                                                                                                                                                 |
| Rate limiting               | `shared/modules/tenant-rate-limit/*` (guard + service + repository), plus `ip-rate-limit.service.ts`, `user-rate-limit.service.ts`, `rate-limit.interceptor.ts` |
| Queues & DLQ                | `queue/postgres-queue.service.ts` + `dlq-replay.scheduler.ts`/`dlq.controller.ts`; ADR 0001 "Postgres as queue"; dedicated `apps/worker` process                |
| Distributed locks           | `shared/common/utils/postgres-advisory-lock.ts`                                                                                                                 |
| Consensus / leader election | `schedule/cron-heartbeat.ts` + advisory locks for single-flight crons; `ENABLE_SCHEDULERS=false` on the API keeps cron in the worker                            |
| Backpressure                | `extensions/query-budget.extension.ts`; Fly-level concurrency caps (`soft_limit 60 / hard_limit 100`) in `fly.toml`                                             |
| Failure modes & resilience  | `ops-alert.service.ts` + listener; runbooks in `docs/operations/playbooks/*` (razorpay outage, DB exhaustion, queue backlog)                                    |

_Capacity planning and multi-region: no direct docita implementation yet._ The TCP/UDP chapter stays conceptual here — nearest real anchors are `fetch-with-timeout.ts` (every outbound call budgeted) and Cloudflare edge termination in front of the API.
