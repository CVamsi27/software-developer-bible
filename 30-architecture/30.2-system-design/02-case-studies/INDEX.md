# System Design — Case Studies

> **Study time:** ≈ 6 h 36 m of reading (32 files, ~12 min average).
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
| --------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Web (foundational)** | URL Shortener, Rate Limiter, Distributed Counter, Distributed ID Generator | Compact practice for identifiers, traffic policy and contention |
| **Storage and Sync** | Google Drive, Dropbox | Staged uploads, version history, collaboration, conflict resolution |
| **Messaging and Real-Time** | WhatsApp, Chat System, Notification Service, Real-Time Collaboration | Chat apps, notifications, collaborative editing |
| **Streaming and Media** | Netflix, YouTube | Video platforms, content delivery network (CDN)-heavy systems |
| **Social and Feed** | Twitter, Instagram | Social network, fan-out, timeline |
| **Ride-sharing and Geo** | Uber, Lyft | Location-based dispatch, geo-indexing |
| **Commerce and Fintech** | Payment Gateway, E-Commerce, Ticket Booking, Live Betting | Transactions, consistency, concurrency |
| **Healthcare and Vertical** | Hospital Management | Domain-specific scheduling, electronic health record (EHR) |
| **Search and Data** | Web Crawler, Typeahead Autocomplete | Crawling, deduplication, ranking, prefix search |
| **Automation** | Workflow Engine, Distributed Job Scheduler | Background jobs, directed acyclic graphs (DAGs), cron at scale, retries |
| **Platform and Telemetry** | Metrics Monitoring Pipeline, Ad Click Aggregator | Time-series ingestion, streaming aggregation, billing-grade correctness |
| **Infrastructure and Low-Level Design (LLD)** | Parking Lot, Distributed Cache, Message Queue, API Gateway | Object-oriented design (OOD) modeling, distributed data structures, async messaging, gateway routing |

---

## Case studies

| # | File | Domain | Key topics | Role priority | General importance |
| --- | ----------------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| 01 | [URL Shortener](30.2.2.01-url-shortener.md) | Web (foundational) | Code allocation, uniqueness, redirect caching, analytics durability | Important | Important |
| 02 | [WhatsApp](30.2.2.02-whatsapp.md) | Messaging and Real-Time | Retry-safe acceptance, device delivery, end-to-end encryption (E2EE), group membership | Important | Important |
| 03 | [Uber](30.2.2.03-uber.md) | Ride-sharing and Geo | Location freshness, geo discovery, road estimated time of arrival (ETA), trip and payment boundaries | Important | Important |
| 04 | [Netflix](30.2.2.04-netflix.md) | Streaming and Media | Playback rights, adaptive quality, CDN and origin recovery, progress | Important | Important |
| 05 | [Google Drive](30.2.2.05-google-drive.md) | Storage and Sync | Staged publication, inherited access, quota races, version conflicts and replay | Important | Important |
| 06 | [Payment Gateway](30.2.2.06-payment-gateway.md) | Commerce and Fintech | Unknown outcomes, scoped idempotency, balanced ledger, webhook replay and refunds | Important | Important |
| 07 | [Notification Service](30.2.2.07-notification-service.md) | Messaging and Real-Time | Per-channel identity, fresh consent, quiet hours, outcomes and retries | Important | Important |
| 08 | [Ticket Booking](30.2.2.08-ticket-booking.md) | Commerce and Fintech | Atomic seat groups, expiry-safe holds, payment recovery, single-use admission | Important | Important |
| 09 | [E-Commerce](30.2.2.09-e-commerce.md) | Commerce and Fintech | Checkout snapshots, atomic stock reservations, payment recovery, fulfillment saga | Important | Important |
| 10 | [Hospital Management](30.2.2.10-hospital-management.md) | Healthcare and Vertical | Tenant-safe clinical access, interval constraints, idempotent booking, Fast Healthcare Interoperability Resources (FHIR) adapters | Important | Important |
| 11 | [Live Betting](30.2.2.11-live-betting.md) | Commerce and Fintech | Versioned odds acceptance, idempotent debits, terminal settlement, feed-gap recovery | Important | Important |
| 12 | [Twitter Feed](30.2.2.12-twitter-feed.md) | Social and Feed | Hybrid fan-out, stable pagination, visibility rechecks, tombstones, trend windows | Important | Important |
| 13 | [Rate Limiter](30.2.2.13-rate-limiter.md) | Web (foundational) | Token-bucket request trace, atomic shared budgets, failover overshoot, 429 handling | Important | Important |
| 14 | [Web Crawler](30.2.2.14-web-crawler.md) | Search and Data | Bounded frontier, per-origin scheduling, lease fencing, robots policy, server-side request forgery (SSRF)-safe fetching | Important | Important |
| 15 | [Chat System](30.2.2.15-chat-system.md) | Messaging and Real-Time | Durable acceptance, ordered history, device receipts, change cursors, membership, E2EE and group fan-out | Important | Important |
| 16 | [Instagram](30.2.2.16-instagram.md) | Social and Feed | Validated media publication, hybrid feeds, visibility checks, stable cursors and retry-safe interactions | Important | Important |
| 17 | [YouTube](30.2.2.17-youtube.md) | Streaming and Media | Version-fenced uploads, HTTP Live Streaming (HLS) and Dynamic Adaptive Streaming over HTTP (DASH) adaptive playback, manifest publication, authorized delivery and capacity | Important | Important |
| 18 | [Dropbox](30.2.2.18-dropbox.md) | Storage and Sync | Block-level sync, content-addressable storage, conflict resolution, cursors | Important | Important |
| 19 | [Lyft](30.2.2.19-lyft.md) | Ride-sharing and Geo | S2 and H3 geo indexing, dispatch algorithm, ETA service, surge pricing | Important | Important |
| 20 | [Distributed Counter](30.2.2.20-distributed-counter.md) | Web (foundational) | Stable event identity, hot-key sharding, conflict-free replicated data type (CRDT) merge, read contracts | Important | Important |
| 21 | [Workflow Engine](30.2.2.21-workflow-engine.md) | Automation | Dependency eligibility, durable state, action identity, waits, compensation | Important | Important |
| 22 | [Real-Time Collaboration](30.2.2.22-real-time-collaboration.md) | Messaging and Real-Time | Operational transformation (OT) vs CRDT, WebSocket protocol, Redis publish-subscribe (Pub/Sub), version history, offline support | Important | Important |
| 23 | [Typeahead Autocomplete](30.2.2.23-typeahead-autocomplete.md) | Search and Data | Trie, radix tree, and finite-state transducer (FST), bounded typo matching, deterministic ranking, visibility-scoped candidates, versioned index rollout | Important | Important |
| 24 | [Metrics Monitoring Pipeline](30.2.2.24-metrics-monitoring-pipeline.md) | Platform and Telemetry | Time-series database (TSDB) ingestion, OpenTelemetry (OTel) identity and temporality, exact cardinality admission, late samples, rollups, alert lifecycle | Important | Important |
| 25 | [Distributed Job Scheduler](30.2.2.25-distributed-job-scheduler.md) | Automation | Occurrence identity, leases and fencing scope, outbox recovery, daylight saving time (DST) and misfire policy, retries, tenant fairness | Important | Important |
| 26 | [Distributed ID Generator](30.2.2.26-distributed-id-generator.md) | Web (foundational) | Snowflake capacity, restart-safe clocks, stale-owner fencing, range allocation, UUIDv7 ordering | Important | Important |
| 27 | [Ad Click Aggregator](30.2.2.27-ad-click-aggregator.md) | Platform and Telemetry | Producer identity, exact deduplication, late-event corrections, revisioned totals, auditable settlement | Important | Important |
| 28 | [Parking Lot](30.2.2.28-parking-lot.md) | Infrastructure and LLD | Atomic spot ownership, compatible allocation, versioned fees, payment outcomes, physical reconciliation | Important | Important |
| 29 | [Distributed Cache](30.2.2.29-distributed-cache.md) | Infrastructure and LLD | Scoped keys, stale-fill races, partition and failover, hot-key control, origin-safe recovery | Important | Important |
| 30 | [Message Queue](30.2.2.30-message-queue.md) | Infrastructure and LLD | In-sync replica (ISR) acknowledgments, partition ordering, idempotent effects, retention, poison messages, broker boundaries | Important | Important |
| 31 | [API Gateway](30.2.2.31-api-gateway.md) | Infrastructure and LLD | JSON Web Token (JWT) trust vs resource authorization, route normalization, deadlines and retries, scoped caching, Backend for Frontend (BFF) failure budgets | Important | Important |

---

**Cross-references:** [Theory →](../01-theory/INDEX.md) | [Design Patterns](../../30.1-design-patterns/INDEX.md) | [Microservices](../../../20-backend/20.6-microservices/INDEX.md) | [Database](../../../20-backend/20.4-database/INDEX.md) | [WebSockets](../../../60-realtime/60.1-websockets/INDEX.md)

---

## Reading Path and Completion Check

Choose a compact case first, such as the URL shortener. Move to a scarce-resource case, then a delivery or streaming case and a coordination case. Reuse theory links rather than relearning each mechanism.

For each case, explain one rule that must always hold, which changes must succeed or fail together to preserve it, the largest source of scaling pressure, and one path for recovering from failure. Then use [section revision](REVISION.md) without reopening the chapters. After that, use the [system-design interview bank](../01-theory/30.2.1.16-interview-questions.md) as a separate drill.

Change one condition per answer: delay a response, expire a lease, revoke a user, or move ownership to another region. Explain which invariant still holds and which guarantee changes.

## Navigation

[← Previous: Theory](../01-theory/INDEX.md) · [Back to System Design Index](../INDEX.md) · [Next: Microservices →](../../../20-backend/20.6-microservices/INDEX.md)

---

## Docita implementation anchors

The local Docita checkout at `dc5a97dc3` was inspected on October 10, 2026. These source paths connect study concepts to implementation questions; their presence does not establish deployment status, production scale, or all guarantees in an interview model. Use the [Docita evidence walkthrough](../../../projects/docita/INDEX.md) for measured and dated claims.

| Topic | Source anchor and boundary |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hospital management | `apps/api/src/domains/` contains clinical and operational domain code. The case study remains an illustrative design, not a clinical validation certificate. |
| Notifications | `apps/api/src/shared/modules/messaging/notification-orchestrator.service.ts` selects registered channels and records send results. Provider acceptance is distinct from recipient delivery or reading. |
| Payments | `apps/api/src/shared/modules/webhooks/razorpay-webhook-verification.helper.ts` verifies raw-body signatures and replay state. A helper alone does not establish end-to-end payment or settlement correctness. |
| Workflow recovery | `apps/api/src/shared/modules/imports/bulk-import-orchestrator.service.ts` coordinates import jobs; `apps/api/src/shared/modules/queue/dlq-replay.scheduler.ts` handles dead-letter queue (DLQ) recovery work. These are bounded workflows, not evidence of a general user-defined DAG engine. |
| Other product cases | No direct Docita implementation is claimed for URL shortening, ride dispatch, social feeds, or media streaming. |
