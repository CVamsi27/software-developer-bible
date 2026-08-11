# System Design — Case Studies

> **20 files** — Applied examples of system design interviews. Read [../00-theory/](../00-theory/INDEX.md) first, then work through these in any order.

[![Files](https://img.shields.io/badge/files-20-blue)](../../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Pick the case study that matches the JD's domain.** For an Uber-style role, do Uber. For a payment role, do Payment Gateway. For a chat/messaging role, do WhatsApp + Chat System. For a feed/social role, do Twitter + Instagram.

---

## Case studies

| # | File | Domain | Key topics |
|---|------|--------|-----------|
| 01 | [URL Shortener](30.2.2.01-url-shortener.md) | Web | Base62 encoding, hash collision, distributed ID generation |
| 02 | [WhatsApp](30.2.2.02-whatsapp.md) | Messaging | Real-time messaging, end-to-end encryption, last-seen, group chats |
| 03 | [Uber](30.2.2.03-uber.md) | Ride-sharing | Ride matching, geospatial indexing, real-time tracking, ETA |
| 04 | [Netflix](30.2.2.04-netflix.md) | Streaming | Video streaming, CDN, recommendation engine, content delivery |
| 05 | [Google Drive](30.2.2.05-google-drive.md) | Storage | File storage, sync, upload optimization, conflict resolution |
| 06 | [Payment Gateway](30.2.2.06-payment-gateway.md) | Fintech | Payment processing, idempotency, reconciliation, fraud detection |
| 07 | [Notification Service](30.2.2.07-notification-service.md) | Messaging | Push, email, SMS, template system, delivery guarantees |
| 08 | [Ticket Booking](30.2.2.08-ticket-booking.md) | Ticketing | Concurrent booking, row-level locking, two-phase commit |
| 09 | [E-Commerce](30.2.2.09-e-commerce.md) | Retail | Product catalog, cart, inventory, order management, payment flow |
| 10 | [Hospital Management](30.2.2.10-hospital-management.md) | Healthcare | Appointment scheduling, EHR, billing, interoperability |
| 11 | [Live Betting](30.2.2.11-live-betting.md) | Betting | Real-time odds, event processing, concurrency, consistency |
| 12 | [Twitter Feed](30.2.2.12-twitter-feed.md) | Social | News feed fanout, timeline caching, trending topics, hashtag search |
| 13 | [Rate Limiter](30.2.2.13-rate-limiter.md) | Web | Token bucket, sliding window, distributed rate limit, 429 handling |
| 14 | [Web Crawler](30.2.2.14-web-crawler.md) | Search | URL frontier, politeness, content dedup, robots.txt, simhash |
| 15 | [Chat System](30.2.2.15-chat-system.md) | Messaging | WebSocket messaging, presence, typing indicators, offline sync |
| 16 | [Instagram](30.2.2.16-instagram.md) | Social | Photo/video sharing, fan-out feed, media pipeline, social graph |
| 17 | [YouTube](30.2.2.17-youtube.md) | Streaming | Video transcoding ladder, HLS/DASH streaming, CDN economics, recommendations |
| 18 | [Dropbox](30.2.2.18-dropbox.md) | Storage | Block-level sync, content-addressable storage, conflict resolution, cursors |
| 19 | [Lyft](30.2.2.19-lyft.md) | Ride-sharing | S2/H3 geo indexing, dispatch algorithm, ETA service, surge pricing |
| 20 | [Distributed Counter](30.2.2.20-distributed-counter.md) | Web | Hot-key sharding, G-Counter CRDT, local pre-aggregation, tiered storage |

---

**Cross-references:** [Theory →](../00-theory/INDEX.md) | [Design Patterns](../../30.1-design-patterns/INDEX.md) | [Microservices](../../../20-backend/20.6-microservices/INDEX.md) | [Database](../../../20-backend/20.4-database/INDEX.md) | [WebSockets](../../../60-realtime/60.1-websockets/INDEX.md)

---

## Navigation

[← Previous: Theory](../00-theory/INDEX.md) · [🏠 Back to System Design Index](../INDEX.md) · [Next: Microservices →](../../../20-backend/20.6-microservices/INDEX.md)
