# System Design — Case Studies

> **Study time:** ≈ 6 h 26 m of reading (32 files, ~12 min average).
Applied examples of system design interviews. Read [../01-theory/](../01-theory/INDEX.md) first, then choose cases that match your interview goals.

[![Files](https://img.shields.io/badge/files-32-blue)](../../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Treat the architectures and sizing below as interview models with explicit assumptions. Use cited primary sources when describing a company's published implementation, and distinguish those facts from choices made for the exercise.

**Start with the system-design fundamentals, then prioritize cases related to the role.** For example, use the payment and commerce cases for payment products, the messaging cases for chat products, and the feed cases for social products.

---

## Topic Categories — by Difficulty Tier

The 31 cases are grouped by the kind of reasoning they practice. Use the tiers as a study path, then spend more time on designs related to your target roles.

| Tier | Case studies | Why this tier |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Tier 1 — Foundations** | URL Shortener, Rate Limiter, Distributed Counter, Distributed ID Generator | Practice identifiers, routing, limits, contention and recovery in compact designs. |
| **Tier 2 — Product systems** | WhatsApp, Chat System, Notification Service, Twitter Feed, Instagram, Netflix, YouTube, Uber, Lyft, Google Drive, Dropbox | Study messaging, feeds, media delivery, dispatch, storage and synchronization. Prioritize the domains that match the role. |
| **Tier 3 — Correctness-critical workflows** | Payment Gateway, Ticket Booking, E-Commerce, Live Betting, Hospital Management, Ad Click Aggregator | Practice idempotency, concurrency, reconciliation, audit and financial or business invariants. |
| **Tier 4 — Specialized systems** | Web Crawler, Workflow Engine, Real-Time Collaboration, Typeahead Autocomplete, Metrics & Monitoring Pipeline, Distributed Job Scheduler, Parking Lot, Distributed Cache, Message Queue, API Gateway | Study crawling, workflow state, concurrent editing, indexing, telemetry and infrastructure boundaries. |

---

## Case Studies by Domain

| Domain | Case Studies | When to read |
| ------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Web (foundational)** | URL Shortener, Rate Limiter, Distributed Counter, Distributed ID Generator | Compact practice for identifiers, traffic policy and contention |
| **Storage & Sync** | Google Drive, Dropbox | Staged uploads, version history, collaboration, conflict resolution |
| **Messaging & Real-Time** | WhatsApp, Chat System, Notification Service, Real-Time Collaboration | Chat apps, notifications, collaborative editing |
| **Streaming & Media** | Netflix, YouTube | Video platforms, CDN-heavy systems |
| **Social & Feed** | Twitter, Instagram | Social network, fan-out, timeline |
| **Ride-sharing & Geo** | Uber, Lyft | Location-based, dispatch, geo-indexing |
| **Commerce & Fintech** | Payment Gateway, E-Commerce, Ticket Booking, Live Betting | Transactions, consistency, concurrency |
| **Healthcare & Vertical** | Hospital Management | Domain-specific, scheduling, EHR |
| **Search & Data** | Web Crawler, Typeahead Autocomplete | Crawling, dedup, ranking, prefix search |
| **Automation** | Workflow Engine, Distributed Job Scheduler | Background jobs, DAGs, cron at scale, retries |
| **Platform & Telemetry** | Metrics Monitoring Pipeline, Ad Click Aggregator | Time-series ingestion, streaming aggregation, billing-grade correctness |
| **Infrastructure & LLD** | Parking Lot, Distributed Cache, Message Queue, API Gateway | OOD modeling, distributed data structures, async messaging, gateway routing |

---

## Case studies

| # | File | Domain | Key topics | Role priority | General importance |
| --- | ----------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| 01 | [URL Shortener](30.2.2.01-url-shortener.md) | Web (foundational) | Code allocation, uniqueness, redirect caching, analytics durability | Important | Important |
| 02 | [WhatsApp](30.2.2.02-whatsapp.md) | Messaging & Real-Time | Retry-safe acceptance, device delivery, E2EE, group membership | Important | Important |
| 03 | [Uber](30.2.2.03-uber.md) | Ride-sharing & Geo | Location freshness, geo discovery, road ETA, trip and payment boundaries | Important | Important |
| 04 | [Netflix](30.2.2.04-netflix.md) | Streaming & Media | Playback rights, adaptive quality, CDN/origin recovery, progress | Important | Important |
| 05 | [Google Drive](30.2.2.05-google-drive.md) | Storage & Sync | Staged publication, inherited access, quota races, version conflicts and replay | Important | Important |
| 06 | [Payment Gateway](30.2.2.06-payment-gateway.md) | Commerce & Fintech | Unknown outcomes, scoped idempotency, balanced ledger, webhook replay and refunds | Important | Important |
| 07 | [Notification Service](30.2.2.07-notification-service.md) | Messaging & Real-Time | Per-channel identity, fresh consent, quiet hours, outcomes and retries | Important | Important |
| 08 | [Ticket Booking](30.2.2.08-ticket-booking.md) | Commerce & Fintech | Atomic seat groups, expiry-safe holds, payment recovery, single-use admission | Important | Important |
| 09 | [E-Commerce](30.2.2.09-e-commerce.md) | Commerce & Fintech | Checkout snapshots, atomic stock reservations, payment recovery, fulfillment saga | Important | Important |
| 10 | [Hospital Management](30.2.2.10-hospital-management.md) | Healthcare & Vertical | Tenant-safe clinical access, interval constraints, idempotent booking, FHIR adapters | Important | Important |
| 11 | [Live Betting](30.2.2.11-live-betting.md) | Commerce & Fintech | Versioned odds acceptance, idempotent debits, terminal settlement, feed-gap recovery | Important | Important |
| 12 | [Twitter Feed](30.2.2.12-twitter-feed.md) | Social & Feed | Hybrid fan-out, stable pagination, visibility rechecks, tombstones, trend windows | Important | Important |
| 13 | [Rate Limiter](30.2.2.13-rate-limiter.md) | Web (foundational) | Token-bucket request trace, atomic shared budgets, failover overshoot, 429 handling | Important | Important |
| 14 | [Web Crawler](30.2.2.14-web-crawler.md) | Search & Data | Bounded frontier, per-origin scheduling, lease fencing, robots policy, SSRF-safe fetching | Important | Important |
| 15 | [Chat System](30.2.2.15-chat-system.md) | Messaging & Real-Time | Durable acceptance, ordered history, device receipts, change cursors, membership, E2EE and group fan-out | Important | Important |
| 16 | [Instagram](30.2.2.16-instagram.md) | Social & Feed | Validated media publication, hybrid feeds, visibility checks, stable cursors and retry-safe interactions | Important | Important |
| 17 | [YouTube](30.2.2.17-youtube.md) | Streaming & Media | Version-fenced uploads, HLS/DASH adaptive playback, manifest publication, authorized delivery and capacity | Important | Important |
| 18 | [Dropbox](30.2.2.18-dropbox.md) | Storage & Sync | Block-level sync, content-addressable storage, conflict resolution, cursors | Important | Important |
| 19 | [Lyft](30.2.2.19-lyft.md) | Ride-sharing & Geo | S2/H3 geo indexing, dispatch algorithm, ETA service, surge pricing | Important | Important |
| 20 | [Distributed Counter](30.2.2.20-distributed-counter.md) | Web (foundational) | Stable event identity, hot-key sharding, CRDT merge, read contracts | Important | Important |
| 21 | [Workflow Engine](30.2.2.21-workflow-engine.md) | Automation | Dependency eligibility, durable state, action identity, waits, compensation | Important | Important |
| 22 | [Real-Time Collaboration](30.2.2.22-real-time-collaboration.md) | Messaging & Real-Time | OT vs CRDT, WebSocket protocol, Redis Pub/Sub, version history, offline support | Important | Important |
| 23 | [Typeahead Autocomplete](30.2.2.23-typeahead-autocomplete.md) | Search & Data | Trie/radix/FST, bounded typo matching, deterministic ranking, visibility-scoped candidates, versioned index rollout | Important | Important |
| 24 | [Metrics Monitoring Pipeline](30.2.2.24-metrics-monitoring-pipeline.md) | Platform & Telemetry | TSDB ingestion path, downsampling, cardinality explosion control, push vs pull, alert evaluation at scale | Important | Important |
| 25 | [Distributed Job Scheduler](30.2.2.25-distributed-job-scheduler.md) | Automation | Cron at scale, leader election, task leases & fencing, dedup, delayed jobs, fairness/starvation | Important | Important |
| 26 | [Distributed ID Generator](30.2.2.26-distributed-id-generator.md) | Web (foundational) | Snowflake bit layout, clock rollback, worker identity, timestamp ordering limits, UUIDv7 comparison | Important | Important |
| 27 | [Ad Click Aggregator](30.2.2.27-ad-click-aggregator.md) | Platform & Telemetry | Stable event identity, watermarks, revisioned reporting, fraud decisions, settlement | Important | Important |
| 28 | [Parking Lot](30.2.2.28-parking-lot.md) | Infrastructure & LLD | Compatible allocation, live sessions, physical evidence, fee boundaries, payment | Important | Important |
| 29 | [Distributed Cache](30.2.2.29-distributed-cache.md) | Infrastructure & LLD | Consistent hashing, replication, eviction policies, cache stampede, hot key handling | Important | Important |
| 30 | [Message Queue](30.2.2.30-message-queue.md) | Infrastructure & LLD | WAL, consumer groups, delivery guarantees, backpressure, Kafka vs RabbitMQ comparison | Important | Important |
| 31 | [API Gateway](30.2.2.31-api-gateway.md) | Infrastructure & LLD | Routing, rate limiting, JWT validation, BFF pattern, circuit breaker, protocol translation | Important | Important |

---

**Cross-references:** [Theory →](../01-theory/INDEX.md) | [Design Patterns](../../30.1-design-patterns/INDEX.md) | [Microservices](../../../20-backend/20.6-microservices/INDEX.md) | [Database](../../../20-backend/20.4-database/INDEX.md) | [WebSockets](../../../60-realtime/60.1-websockets/INDEX.md)

---

## Reading Path and Completion Check

Choose a compact case first, such as the URL shortener. Move to a scarce-resource case, then a delivery/streaming case and a coordination case. Reuse theory links rather than relearning each mechanism.

For each case, explain one rule that must always hold, which changes must succeed or fail together to preserve it, the largest source of scaling pressure, and one path for recovering from failure. Then use [section revision](REVISION.md) without reopening the chapters. After that, use the [system-design interview bank](../01-theory/30.2.1.16-interview-questions.md) as a separate drill. Change one condition per answer: delay a response, expire a lease, revoke a user, or move ownership to another region. Explain which invariant still holds and which guarantee changes.

## Navigation

[← Previous: Theory](../01-theory/INDEX.md) · [ Back to System Design Index](../INDEX.md) · [Next: Microservices →](../../../20-backend/20.6-microservices/INDEX.md)

---

## Docita implementation anchors

The local Docita checkout at `dc5a97dc3` was inspected on 10 October 2026. These source paths connect study concepts to implementation questions; their presence does not establish deployment status, production scale, or all guarantees in an interview model. Use the [Docita evidence walkthrough](../../../projects/docita/INDEX.md) for measured and dated claims.

| Topic | Source anchor and boundary |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hospital management | `apps/api/src/domains/` contains clinical and operational domain code. The case study remains an illustrative design, not a clinical validation certificate. |
| Notifications | `apps/api/src/shared/modules/messaging/notification-orchestrator.service.ts` selects registered channels and records send results. Provider acceptance is distinct from recipient delivery or reading. |
| Payments | `apps/api/src/shared/modules/webhooks/razorpay-webhook-verification.helper.ts` verifies raw-body signatures and replay state. A helper alone does not establish end-to-end payment or settlement correctness. |
| Workflow recovery | `apps/api/src/shared/modules/imports/bulk-import-orchestrator.service.ts` coordinates import jobs; `apps/api/src/shared/modules/queue/dlq-replay.scheduler.ts` handles queue-recovery work. These are bounded workflows, not evidence of a general user-defined DAG engine. |
| Other product cases | No direct Docita implementation is claimed for URL shortening, ride dispatch, social feeds, or media streaming. |
