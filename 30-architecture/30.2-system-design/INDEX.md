# System Design — Index

> **Study time:** ≈ 16 h 46 m of reading (56 files, ~18 min average).
> **56 files** — split into **theory** (21 foundational files in [01-theory/](01-theory/INDEX.md)) and **case studies** (31 applied examples in [02-case-studies/](02-case-studies/INDEX.md)).
>
> Study in three passes: **I. Theory** (CAP → consistency → scaling levers) → **II. The method** (how-to-approach framework) → **III. Case studies** (pick by JD domain).

[![Files](https://img.shields.io/badge/files-56-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The two sub-folders group the material into six conceptual categories so you can find theory, design methods and applied examples.

| Category | Where | Files | Why it matters |
| ----------------------------- | -------------------------------------------- | ----: | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Data & Consistency Theory** | [01-theory/](01-theory/INDEX.md) | 6 | CAP/PACELC, consistency models, sharding & replication, distributed transactions, locks, consensus |
| **Traffic, Scale & Capacity** | [01-theory/](01-theory/INDEX.md) | 5 | Load balancing, TCP/UDP transport, rate limiting, backpressure, capacity planning |
| **Performance & Delivery** | [01-theory/](01-theory/INDEX.md) | 3 | Caching patterns, queues & async, outbox & CDC |
| **Reliability & Topology** | [01-theory/](01-theory/INDEX.md) | 4 | Failure modes, resilience deep-dive, multi-region, architecture patterns |
| **The Method + Drills** | [01-theory/](01-theory/INDEX.md) | 3 | How-to-approach framework, interview questions, probabilistic data structures |
| **Applied Case Studies** | [02-case-studies/](02-case-studies/INDEX.md) | 31 | URL shortener → Netflix, Uber, WhatsApp, payment gateway, typeahead, metrics pipeline, job scheduler, ID generator — classified by domain |

---

## The Track — Read In This Order

```text
Pass I — THEORY (in order) Pass II — METHOD Pass III — CASE STUDIES
CAP → consistency models how-to-approach pick by JD domain:
→ sharding & replication (4-phase framework: · feed/social → Twitter
→ load balancing → caching clarify → estimate → · chat/realtime → WhatsApp
→ queues → distributed txns high-level → deep-dive) · geo/dispatch → Uber / Lyft
→ rate limiting → consensus · fintech → Payment Gateway
→ failure modes → capacity interview questions · storage/sync → Google Drive
   ↓ (50+ drills) · media/streaming→ Netflix
INTERVIEW DRILLS ←────────────────────────────────────────────────· foundational → URL shortener
```

**Total time:** theory ~14 hrs, case studies ~2 hrs each. Do Pass I once; recycle case studies per application.

---

## Sub-folders

| Folder | Files | What it is | When to read |
| -------------------------------------------- | ----: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [01-theory/](01-theory/INDEX.md) | 21 | Foundational concepts (14, in order) + meta guides (6) + transport deep-dive: approach framework, interview bank, probabilistic structures, outbox/CDC, resilience deep-dive, multi-region, TCP/UDP fundamentals | **Read first** — every case study depends on these |
| [02-case-studies/](02-case-studies/INDEX.md) | 31 | Applied examples across 11 domains: web fundamentals, storage/sync, messaging, streaming, social, geo, fintech, healthcare, search, automation, platform/telemetry | After theory — match the JD's domain |

---

**Cross-references:** [Design Patterns](../30.1-design-patterns/INDEX.md) | [Microservices](../../20-backend/20.6-microservices/INDEX.md) | [Database](../../20-backend/20.4-database/INDEX.md) | [REST APIs](../../20-backend/20.3-rest-apis/INDEX.md) | [WebSockets](../../60-realtime/60.1-websockets/INDEX.md)

---

## Navigation

[← Previous: Design Patterns](../30.1-design-patterns/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Docker →](../../40-platform/40.1-docker/INDEX.md)
