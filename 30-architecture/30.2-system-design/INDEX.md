# System Design — Index

> **42 files** — split into **theory** (20 foundational files in [00-theory/](00-theory/INDEX.md)) and **case studies** (22 applied examples in [10-case-studies/](10-case-studies/INDEX.md)).
>
> Study in three passes: **I. Theory** (CAP → consistency → scaling levers) → **II. The method** (how-to-approach framework) → **III. Case studies** (pick by JD domain).

[![Files](https://img.shields.io/badge/files-42-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## 🗂️ Topic Categories

The two sub-folders classify into 6 conceptual categories — the "GoF classification" of system design.

| Category | Where | Files | Why it matters |
|----------|-------|------:|----------------|
| **Data & Consistency Theory** | [00-theory/](00-theory/INDEX.md) | 6 | CAP/PACELC, consistency models, sharding & replication, distributed transactions, locks, consensus |
| **Traffic, Scale & Capacity** | [00-theory/](00-theory/INDEX.md) | 4 | Load balancing, rate limiting, backpressure, capacity planning |
| **Performance & Delivery** | [00-theory/](00-theory/INDEX.md) | 3 | Caching patterns, queues & async, outbox & CDC |
| **Reliability & Topology** | [00-theory/](00-theory/INDEX.md) | 4 | Failure modes, resilience deep-dive, multi-region, architecture patterns |
| **The Method + Drills** | [00-theory/](00-theory/INDEX.md) | 3 | How-to-approach framework, interview questions, probabilistic data structures |
| **Applied Case Studies** | [10-case-studies/](10-case-studies/INDEX.md) | 22 | URL shortener → Netflix, Uber, WhatsApp, payment gateway — classified by domain |

---

## 🛣️ The Track — Read In This Order

```text
Pass I — THEORY (in order)           Pass II — METHOD              Pass III — CASE STUDIES
CAP → consistency models             how-to-approach               pick by JD domain:
→ sharding & replication             (4-phase framework:            · feed/social    → Twitter
→ load balancing → caching            clarify → estimate →          · chat/realtime  → WhatsApp
→ queues → distributed txns           high-level → deep-dive)       · geo/dispatch   → Uber / Lyft
→ rate limiting → consensus                                        · fintech        → Payment Gateway
→ failure modes → capacity        interview questions              · storage/sync   → Google Drive
   ↓                              (50+ drills)                     · media/streaming→ Netflix
INTERVIEW DRILLS ←────────────────────────────────────────────────· foundational    → URL shortener
```

**Total time:** theory ~14 hrs, case studies ~2 hrs each. Do Pass I once; recycle case studies per application.

---

## 📁 Sub-folders

| Folder | Files | What it is | When to read |
|--------|------:|-----------|--------------|
| [00-theory/](00-theory/INDEX.md) | 20 | Foundational concepts (14, in order) + meta guides (6): approach framework, interview bank, probabilistic structures, outbox/CDC, resilience deep-dive, multi-region | **Read first** — every case study depends on these |
| [10-case-studies/](10-case-studies/INDEX.md) | 22 | Applied examples across 10 domains: web fundamentals, storage/sync, messaging, streaming, social, geo, fintech, healthcare, search, automation | After theory — match the JD's domain |

---

**Cross-references:** [Design Patterns](../30.1-design-patterns/INDEX.md) | [Microservices](../../20-backend/20.6-microservices/INDEX.md) | [Database](../../20-backend/20.4-database/INDEX.md) | [REST APIs](../../20-backend/20.3-rest-apis/INDEX.md) | [WebSockets](../../60-realtime/60.1-websockets/INDEX.md)

---

## Navigation

[← Previous: Design Patterns](../30.1-design-patterns/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Docker →](../../40-platform/40.1-docker/INDEX.md)
