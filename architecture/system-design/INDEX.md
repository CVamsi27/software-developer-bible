# System Design — Index

> **36 files** — 14 foundational theory files (CAP, consistency models, sharding, replication, load balancing, caching, queues, distributed transactions, rate limiting, consensus, failure modes, architecture patterns, capacity planning, backpressure, distributed locks), 22 case studies from URL shorteners to Netflix, WhatsApp, Uber, payment gateways, Twitter, Rate Limiter, Chat System, Instagram, YouTube, Dropbox, Lyft, distributed counters, and a meta-guide on how to approach any system-design problem.

[![Files](https://img.shields.io/badge/files-36-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

**Read the theory first.** The 14 `00-*` files below cover the foundational concepts. Then read the case studies for applied examples.

---

## Foundational Theory (read these first)

These are the concepts you need to know BEFORE doing any case study. Every system design interview question touches at least 3-4 of these.

| # | File | Concepts covered | Why it matters |
|---|------|------------------|----------------|
| 00 | [CAP Theorem & PACELC](cap-theorem.md) | Consistency, Availability, Partition tolerance, CP vs AP trade-offs, PACELC extension | The single most important distributed systems concept. Pick CP or AP for every operation. |
| 00 | [Data Consistency Models](consistency-models.md) | Linearizability, eventual, causal, read-your-writes, monotonic reads | Pick per operation, not per system. Most real systems are a mix. |
| 00 | [Sharding & Replication](sharding-and-replication.md) | Hash/range/directory sharding, single-leader/multi-leader/leaderless replication | How to actually scale a database. Both are needed. |
| 00 | [Load Balancing](load-balancing.md) | L4 vs L7, round-robin/least-connections/consistent-hashing/IP-hash, health checks | Traffic distribution. Pick the wrong algorithm and one server melts. |
| 00 | [Caching Patterns](caching-patterns.md) | Cache-aside, read-through, write-through, write-behind, refresh-ahead, write-around + LRU/LFU/TTL eviction | The #1 lever for performance. Know all 6 patterns. |
| 00 | [Queues & Async](queues-and-async.md) | Point-to-point vs pub/sub, at-least-once vs exactly-once, idempotency, DLQ, ordering | Async is the backbone of scalable systems. Know delivery guarantees. |
| 00 | [Distributed Transactions](distributed-transactions.md) | 2PC, 3PC, Saga (choreography + orchestration) | Atomicity across services. Saga is the production answer. |
| 00 | [Rate Limiting](rate-limiting.md) | Fixed/sliding window, token bucket, leaky bucket, Redis-based distributed | Protect from abuse. Token bucket is the default. |
| 00 | [Consensus & Leader Election](consensus-and-leader-election.md) | Paxos, Raft, Zab, leader election, split brain, distributed locks | How databases agree on who's leader. Raft is the default. |
| 00 | [Failure Modes](failure-modes.md) | Hardware, software, network, human failures, retries, circuit breakers, bulkheads | Everything fails. Plan for it. |
| 00 | [Architecture Patterns](architecture-patterns.md) | Monolith, modular monolith, microservices, event-driven, hexagonal, clean, microkernel | Pick the right architecture for the team and domain. |
| 00 | [Capacity Planning](capacity-planning.md) | QPS, storage, bandwidth, memory, Little's Law | Estimate first, design second. Numbers, not vibes. |
| 00 | [Backpressure & Flow Control](backpressure-and-flow-control.md) | Blocking, dropping, load shedding, circuit breakers | When consumer is slower than producer. Without it, OOM. |
| 00 | [Distributed Locks](distributed-locks.md) | Redis Redlock, ZooKeeper, etcd, Postgres advisory, fencing tokens | Mutual exclusion across machines. Know the fencing problem. |

---

## Case Studies (apply the theory)

| # | File | Topics |
|---|------|--------|
| 01 | [URL Shortener](url-shortener.md) | Base62 encoding, hash collision, distributed ID generation |
| 02 | [WhatsApp](whatsapp.md) | Real-time messaging, end-to-end encryption, last-seen, group chats |
| 03 | [Uber](uber.md) | Ride matching, geospatial indexing, real-time tracking, ETA |
| 04 | [Netflix](netflix.md) | Video streaming, CDN, recommendation engine, content delivery |
| 05 | [Google Drive](google-drive.md) | File storage, sync, upload optimization, conflict resolution |
| 06 | [Payment Gateway](payment-gateway.md) | Payment processing, idempotency, reconciliation, fraud detection |
| 07 | [Notification Service](notification-service.md) | Push, email, SMS, template system, delivery guarantees |
| 08 | [Ticket Booking](ticket-booking.md) | Concurrent booking, row-level locking, two-phase commit |
| 09 | [E-Commerce](e-commerce.md) | Product catalog, cart, inventory, order management, payment flow |
| 10 | [Hospital Management](hospital-management.md) | Appointment scheduling, EHR, billing, interoperability |
| 11 | [Live Betting](live-betting.md) | Real-time odds, event processing, concurrency, consistency |
| 12 | [Twitter Feed](twitter-feed.md) | News feed fanout, timeline caching, trending topics, hashtag search |
| 13 | [Rate Limiter](rate-limiter.md) | Token bucket, sliding window, distributed rate limit, 429 handling |
| 14 | [Web Crawler](web-crawler.md) | URL frontier, politeness, content dedup, robots.txt, simhash |
| 15 | [Chat System](chat-system.md) | WebSocket messaging, presence, typing indicators, offline sync |
| 16 | [Interview Questions](interview-questions.md) | 50+ curated questions with answers |
| 17 | [How to Approach](how-to-approach.md) | 4-phase framework: clarify, estimate, high-level, deep-dive |
| 18 | [Instagram](instagram.md) | Photo/video sharing, fan-out feed, media pipeline, social graph |
| 19 | [YouTube](youtube.md) | Video transcoding ladder, HLS/DASH streaming, CDN economics, recommendations |
| 20 | [Dropbox](dropbox.md) | Block-level sync, content-addressable storage, conflict resolution, cursors |
| 21 | [Lyft](lyft.md) | S2/H3 geo indexing, dispatch algorithm, ETA service, surge pricing |
| 22 | [Distributed Counter](distributed-counter.md) | Hot-key sharding, G-Counter CRDT, local pre-aggregation, tiered storage |

---

**Cross-references:** [Microservices](../../backend/microservices/) | [Database](../../backend/database/) | [REST APIs](../../backend/rest-api/) | [WebSockets](../../realtime/websockets/)

---

## Navigation

[← Previous: Design Patterns](../../backend/design-patterns/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Microservices →](../../backend/microservices/INDEX.md)
