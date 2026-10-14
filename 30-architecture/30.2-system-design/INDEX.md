# System Design — Index

> **Study time:** ≈ 10 h 58 m of reading (56 files, ~12 min average).
> **56 files** — split into **theory** (foundational chapters in [01-theory/](01-theory/INDEX.md)) and **case studies** (31 applied examples in [02-case-studies/](02-case-studies/INDEX.md)).
>
> Study in three passes: **I. Interview method and workload assumptions** (How to Approach, capacity estimates, network prerequisites as needed) → **II. Theory mechanisms** (CAP → consistency → placement, traffic and recovery) → **III. Case studies** (pick by JD domain).

[![Files](https://img.shields.io/badge/files-56-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The two sub-folders group the material into six conceptual categories so you can find theory, design methods and applied examples.

| Category | Where | Why it matters |
| ----------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Data & Consistency Theory** | [01-theory/](01-theory/INDEX.md) | CAP/PACELC, consistency, sharding, replication, shared commits, locks and consensus |
| **Traffic, Scale & Capacity** | [01-theory/](01-theory/INDEX.md) | Load balancing, transport, DNS, TLS, admission, backpressure and capacity |
| **Performance & Delivery** | [01-theory/](01-theory/INDEX.md) | Caching, queues, approximate data structures, outbox and CDC |
| **Reliability & Topology** | [01-theory/](01-theory/INDEX.md) | Failure modes, resilience, regions and architecture boundaries |
| **The Method & Practice** | [01-theory/](01-theory/INDEX.md) | Frame the problem, retrieve concepts, then attempt the separate interview bank |
| **Applied Case Studies** | [02-case-studies/](02-case-studies/INDEX.md) | Follow an invariant through normal execution, failure and recovery |

---

## The Track — Read In This Order

1. Read the theory's problem-framing and prerequisite flow, then work through mechanisms and focused traces.
2. Close the learning chapters and use [theory revision](01-theory/REVISION.md), followed by its separate interview prompts.
3. Choose case studies by the job description (JD): messaging, storage, payments, healthcare, geo/dispatch or media. Trace the stated invariant and recovery path, then use [case revision](02-case-studies/REVISION.md).

Study-time badges above estimate reading time; solving prompts and implementing experiments take additional time. The diagrams and examples are teaching designs unless a chapter explicitly provides measured implementation evidence.

## Sub-folders

| Folder | What it is | When to read |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [01-theory/](01-theory/INDEX.md) | Foundational mechanisms, problem-framing method, deeper reliability/data topics and network prerequisites; revision precedes the separate drill | Begin here; revisit the relevant mechanism while designing a case |
| [02-case-studies/](02-case-studies/INDEX.md) | Applied designs across web, storage, messaging, media, geo, payments, healthcare, search, automation and telemetry | After foundations; choose by the role and trace recovery, not just the happy-path diagram |

---

**Cross-references:** [Design Patterns](../30.1-design-patterns/INDEX.md) | [Microservices](../../20-backend/20.6-microservices/INDEX.md) | [Database](../../20-backend/20.4-database/INDEX.md) | [REST APIs](../../20-backend/20.3-rest-apis/INDEX.md) | [WebSockets](../../60-realtime/60.1-websockets/INDEX.md)

---

## Navigation

[← Previous: Design Patterns](../30.1-design-patterns/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Docker →](../../40-platform/40.1-docker/INDEX.md)
