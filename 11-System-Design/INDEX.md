# System Design — Index

> **22 files** — Real-world system design case studies from URL shorteners to Netflix, WhatsApp, Uber, payment gateways, Twitter Feed, Rate Limiter, Chat System, Instagram, YouTube, Dropbox, Lyft, distributed counters, a meta-guide on how to approach any system-design problem, and interview questions.

[![Files](https://img.shields.io/badge/files-22-blue)](INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

| # | File | Topics |
|---|------|--------|
| 01 | [URL Shortener](01-URL-Shortener.md) | Base62 encoding, hash collision, distributed ID generation |
| 02 | [WhatsApp](02-WhatsApp.md) | Real-time messaging, end-to-end encryption, last-seen, group chats |
| 03 | [Uber](03-Uber.md) | Ride matching, geospatial indexing, real-time tracking, ETA |
| 04 | [Netflix](04-Netflix.md) | Video streaming, CDN, recommendation engine, content delivery |
| 05 | [Google Drive](05-Google-Drive.md) | File storage, sync, upload optimization, conflict resolution |
| 06 | [Payment Gateway](06-Payment-Gateway.md) | Payment processing, idempotency, reconciliation, fraud detection |
| 07 | [Notification Service](07-Notification-Service.md) | Push, email, SMS, template system, delivery guarantees |
| 08 | [Ticket Booking](08-Ticket-Booking.md) | Concurrent booking, row-level locking, two-phase commit |
| 09 | [E-Commerce](09-E-Commerce.md) | Product catalog, cart, inventory, order management, payment flow |
| 10 | [Hospital Management](10-Hospital-Management.md) | Appointment scheduling, EHR, billing, interoperability |
| 11 | [Live Betting](11-Live-Betting.md) | Real-time odds, event processing, concurrency, consistency |
| 12 | [Twitter Feed](12-Twitter-Feed.md) | News feed fanout, timeline caching, trending topics, hashtag search |
| 13 | [Rate Limiter](13-Rate-Limiter.md) | Token bucket, sliding window, distributed rate limit, 429 handling |
| 14 | [Web Crawler](14-Web-Crawler.md) | URL frontier, politeness, content dedup, robots.txt, simhash |
| 15 | [Chat System](15-Chat-System.md) | WebSocket messaging, presence, typing indicators, offline sync |
| 16 | [Interview Questions](16-Interview-Questions.md) | 50+ curated questions with answers |
| 17 | [How to Approach](17-How-to-Approach.md) | 4-phase framework: clarify, estimate, high-level, deep-dive |
| 18 | [Instagram](18-Instagram.md) | Photo/video sharing, fan-out feed, media pipeline, social graph |
| 19 | [YouTube](19-YouTube.md) | Video transcoding ladder, HLS/DASH streaming, CDN economics, recommendations |
| 20 | [Dropbox](20-Dropbox.md) | Block-level sync, content-addressable storage, conflict resolution, cursors |
| 21 | [Lyft](21-Lyft.md) | S2/H3 geo indexing, dispatch algorithm, ETA service, surge pricing |
| 22 | [Distributed Counter](22-Distributed-Counter.md) | Hot-key sharding, G-Counter CRDT, local pre-aggregation, tiered storage |

---

**Cross-references:** [Microservices](../12-Microservices/) | [Database](../08-Database/) | [REST APIs](../07-REST-API/) | [WebSockets](../21-WebSockets/)

---

## Navigation

[← Previous: Design Patterns](../10-Design-Patterns/INDEX.md) · [🏠 Back to Index](../INDEX.md) · [Next: Microservices →](../12-Microservices/INDEX.md)
