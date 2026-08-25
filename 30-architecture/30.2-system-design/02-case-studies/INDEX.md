# System Design — Case Studies

> **27 files** — Applied examples of system design interviews. Read [../01-theory/](../01-theory/INDEX.md) first, then work through these in any order.

[![Files](https://img.shields.io/badge/files-27-blue)](../../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Pick the case study that matches the JD's domain.** For an Uber-style role, do Uber. For a payment role, do Payment Gateway. For a chat/messaging role, do WhatsApp + Chat System. For a feed/social role, do Twitter + Instagram.

---

## Topic Categories — by Difficulty Tier

The 27 case studies classify into 4 tiers. Do Tier 1 cold before touching the others.

| Tier | Case studies | Why this tier |
|------|--------------|---------------|
| **Tier 1 — Foundational** (always asked) | URL Shortener, Rate Limiter, Distributed Counter, Distributed ID Generator | Small enough to fully design in 40 min; exercises IDs, caching, limits, delivery guarantees |
| **Tier 2 — Core domains** (pick 2-3 by JD) | WhatsApp, Chat System, Twitter Feed, Instagram, Netflix, YouTube, Uber, Lyft, Google Drive, Dropbox | The classic senior-loop prompts; each stresses one hard subsystem (fan-out, geo-indexing, sync, transcoding) |
| **Tier 3 — Consistency-critical** (fintech/regulated) | Payment Gateway, Ticket Booking, E-Commerce, Live Betting, Hospital Management, Ad Click Aggregator | Idempotency, locking, reconciliation, audit — where correctness beats scale in the rubric |
| **Tier X — Senior differentiators** | Web Crawler, Workflow Engine, Real-Time Collaboration, Typeahead Autocomplete, Metrics & Monitoring Pipeline, Distributed Job Scheduler | Non-CRUD shapes: crawling politeness, DAG execution, OT/CRDT, prefix indexes, cardinality control, leases & fairness |

---

## Case Studies by Domain

| Domain | Case Studies | When to read |
|--------|--------------|--------------|
| **Web (foundational)** | URL Shortener, Rate Limiter, Distributed Counter, Distributed ID Generator | Always — easiest, asked at all levels |
| **Storage & Sync** | Google Drive, Dropbox | File-storage, collaboration, conflict resolution |
| **Messaging & Real-Time** | WhatsApp, Chat System, Notification Service, Real-Time Collaboration | Chat apps, notifications, collaborative editing |
| **Streaming & Media** | Netflix, YouTube | Video platforms, CDN-heavy systems |
| **Social & Feed** | Twitter, Instagram | Social network, fan-out, timeline |
| **Ride-sharing & Geo** | Uber, Lyft | Location-based, dispatch, geo-indexing |
| **Commerce & Fintech** | Payment Gateway, E-Commerce, Ticket Booking, Live Betting | Transactions, consistency, concurrency |
| **Healthcare & Vertical** | Hospital Management | Domain-specific, scheduling, EHR |
| **Search & Data** | Web Crawler, Typeahead Autocomplete | Crawling, dedup, ranking, prefix search |
| **Automation** | Workflow Engine, Distributed Job Scheduler | Background jobs, DAGs, cron at scale, retries |
| **Platform & Telemetry** | Metrics Monitoring Pipeline, Ad Click Aggregator | Time-series ingestion, streaming aggregation, billing-grade correctness |

---

## Case studies

| # | File | Domain | Key topics |
|---|------|--------|-----------|
| 01 | [URL Shortener](30.2.2.01-url-shortener.md) | Web (foundational) | Base62 encoding, hash collision, distributed ID generation |
| 02 | [WhatsApp](30.2.2.02-whatsapp.md) | Messaging & Real-Time | Real-time messaging, end-to-end encryption, last-seen, group chats |
| 03 | [Uber](30.2.2.03-uber.md) | Ride-sharing & Geo | Ride matching, geospatial indexing, real-time tracking, ETA |
| 04 | [Netflix](30.2.2.04-netflix.md) | Streaming & Media | Video streaming, CDN, recommendation engine, content delivery |
| 05 | [Google Drive](30.2.2.05-google-drive.md) | Storage & Sync | File storage, sync, upload optimization, conflict resolution |
| 06 | [Payment Gateway](30.2.2.06-payment-gateway.md) | Commerce & Fintech | Payment processing, idempotency, reconciliation, fraud detection |
| 07 | [Notification Service](30.2.2.07-notification-service.md) | Messaging & Real-Time | Push, email, SMS, template system, delivery guarantees |
| 08 | [Ticket Booking](30.2.2.08-ticket-booking.md) | Commerce & Fintech | Concurrent booking, row-level locking, two-phase commit |
| 09 | [E-Commerce](30.2.2.09-e-commerce.md) | Commerce & Fintech | Product catalog, cart, inventory, order management, payment flow |
| 10 | [Hospital Management](30.2.2.10-hospital-management.md) | Healthcare & Vertical | Appointment scheduling, EHR, billing, interoperability |
| 11 | [Live Betting](30.2.2.11-live-betting.md) | Commerce & Fintech | Real-time odds, event processing, concurrency, consistency |
| 12 | [Twitter Feed](30.2.2.12-twitter-feed.md) | Social & Feed | News feed fanout, timeline caching, trending topics, hashtag search |
| 13 | [Rate Limiter](30.2.2.13-rate-limiter.md) | Web (foundational) | Token bucket, sliding window, distributed rate limit, 429 handling |
| 14 | [Web Crawler](30.2.2.14-web-crawler.md) | Search & Data | URL frontier, politeness, content dedup, robots.txt, simhash |
| 15 | [Chat System](30.2.2.15-chat-system.md) | Messaging & Real-Time | WebSocket messaging, presence, typing indicators, offline sync |
| 16 | [Instagram](30.2.2.16-instagram.md) | Social & Feed | Photo/video sharing, fan-out feed, media pipeline, social graph |
| 17 | [YouTube](30.2.2.17-youtube.md) | Streaming & Media | Video transcoding ladder, HLS/DASH streaming, CDN economics, recommendations |
| 18 | [Dropbox](30.2.2.18-dropbox.md) | Storage & Sync | Block-level sync, content-addressable storage, conflict resolution, cursors |
| 19 | [Lyft](30.2.2.19-lyft.md) | Ride-sharing & Geo | S2/H3 geo indexing, dispatch algorithm, ETA service, surge pricing |
| 20 | [Distributed Counter](30.2.2.20-distributed-counter.md) | Web (foundational) | Hot-key sharding, G-Counter CRDT, local pre-aggregation, tiered storage |
| 21 | [Workflow Engine](30.2.2.21-workflow-engine.md) | Automation | DAG execution, state machine, BullMQ workers, idempotency, retry strategy |
| 22 | [Real-Time Collaboration](30.2.2.22-real-time-collaboration.md) | Messaging & Real-Time | OT vs CRDT, WebSocket protocol, Redis Pub/Sub, version history, offline support |
| 23 | [Typeahead Autocomplete](30.2.2.23-typeahead-autocomplete.md) | Search & Data | Trie/prefix index, offline top-k ranking, geo-sharded indexes, freshness vs latency, personalization |
| 24 | [Metrics Monitoring Pipeline](30.2.2.24-metrics-monitoring-pipeline.md) | Platform & Telemetry | TSDB ingestion path, downsampling, cardinality explosion control, push vs pull, alert evaluation at scale |
| 25 | [Distributed Job Scheduler](30.2.2.25-distributed-job-scheduler.md) | Automation | Cron at scale, leader election, task leases & fencing, dedup, delayed jobs, fairness/starvation |
| 26 | [Distributed ID Generator](30.2.2.26-distributed-id-generator.md) | Web (foundational) | Snowflake bit layout, clock skew handling, k-orderability, node-ID coordination, UUIDv7 comparison |
| 27 | [Ad Click Aggregator](30.2.2.27-ad-click-aggregator.md) | Platform & Telemetry | Streaming ingestion, layered dedup, tumbling windows & watermarks, exactly-once sinks, fraud filtering |

---

**Cross-references:** [Theory →](../01-theory/INDEX.md) | [Design Patterns](../../30.1-design-patterns/INDEX.md) | [Microservices](../../../20-backend/20.6-microservices/INDEX.md) | [Database](../../../20-backend/20.4-database/INDEX.md) | [WebSockets](../../../60-realtime/60.1-websockets/INDEX.md)

---

## Navigation

[← Previous: Theory](../01-theory/INDEX.md) · [ Back to System Design Index](../INDEX.md) · [Next: Microservices →](../../../20-backend/20.6-microservices/INDEX.md)
