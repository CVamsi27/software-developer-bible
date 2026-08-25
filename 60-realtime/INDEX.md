# Real-Time Stack

> **WebSockets, SSE, real-time architecture** — optional stack, study when a JD demands it. Shared by both lanes.
>
> Study in three passes: **I. Protocols** (which transport, and why) → **II. Implementation** (Socket.IO, NestJS gateways) → **III. Architecture at scale** (fan-out, sticky sessions, pub/sub backbones).

[![Files](https://img.shields.io/badge/files-8-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-RealTime-orange)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Topic Categories

The 8 files organize into 4 conceptual categories — the "GoF classification" of real-time systems. Read in order within each.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Transport Protocols](#transport-protocols) | 3 | WebSockets vs SSE vs WebTransport — pick the right pipe before writing code |
| [Framework Implementation](#framework-implementation) | 2 | Socket.IO semantics, NestJS gateways — where code actually gets written |
| [Architecture & Scale](#architecture--scale) | 2 | Fan-out, presence, sticky sessions, Redis adapter — surviving >1 node |
| [Interview Drills](#interview-drills) | 1 | Curated Q&A with follow-up traps |

---

## The Track — Read In This Order

```text
Pass I — PROTOCOLS Pass II — IMPLEMENTATION Pass III — ARCHITECTURE & SCALE
01 overview (WebSockets) → 02 Socket.IO → 04 real-time architecture
03 SSE (server→client only) 05 NestJS gateways 08 scaling patterns
07 WebTransport (HTTP/3) ↓
                                                              INTERVIEW DRILLS
                                                                   06 interview questions
```

**Total time: ~6 hours.** Skip WebTransport if interviewing before next week; it's a bonus-point topic.

---

## Transport Protocols

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 1 | [WebSockets Overview](60.1-websockets/01-transports/60.1.1.01-websockets-overview.md) | Handshake, frames, heartbeat, when WS beats polling | 40 min |
| 2 | [Server-Sent Events](60.1-websockets/01-transports/60.1.1.02-server-sent-events.md) | Auto-reconnect, `Last-Event-ID`, one-way push over plain HTTP | 30 min |
| 3 | [WebTransport](60.1-websockets/01-transports/60.1.1.04-webtransport.md) | HTTP/3, QUIC streams, unidirectional/bidirectional/datagram | 30 min |

## Framework Implementation

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 4 | [Socket.IO](60.1-websockets/01-transports/60.1.1.03-socket-io.md) | Rooms, namespaces, acks, fallbacks, reconnection semantics | 45 min |
| 5 | [NestJS WebSockets](60.1-websockets/03-frameworks-and-paradigms/60.1.3.01-nestjs-websockets.md) | Gateways, decorators, lifecycle hooks — production wiring | 40 min |

## Architecture & Scale

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 6 | [Real-Time Architecture](60.1-websockets/02-architecture-and-scaling/60.1.2.01-real-time-architecture.md) | Transport decision tree, presence, delivery guarantees | 40 min |
| 7 | [Scaling Patterns](60.1-websockets/02-architecture-and-scaling/60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, pub/sub backbone, connection limits | 45 min |

## Interview Drills

| File | Contents |
|------|----------|
| [Interview Questions](60.1-websockets/04-interview-prep/60.1.4.01-interview-questions.md) | Curated Q&A: protocol trade-offs, scaling, failure modes |

---

## The 60-Second Orientation

```text
Need server→client push only? → SSE (auto-reconnect, Last-Event-ID)
Need bidirectional (chat/collab)? → WebSockets (Socket.IO for rooms/fallbacks)
Need it behind serverless/edge? → managed pub/sub + polling fallback first
Scaling beyond one node? → Redis adapter / sticky sessions → pub/sub backbone
```

## Common interview topics

- "WebSocket vs SSE vs long-polling — when would you use each?"
- "How do you scale Socket.IO beyond one node?"
- "What breaks first when you have 100K concurrent connections?"
- "How do you guarantee message delivery in a chat app?"
- "Sticky sessions vs stateless gateways — trade-offs?"

---

**Cross-references:** [Microservices & event-driven patterns](../20-backend/20.6-microservices/INDEX.md) · [NestJS](../20-backend/20.2-nestjs/INDEX.md) · [Caching](../20-backend/20.8-caching/INDEX.md)

---

## Navigation

[← Previous: Quality](../50-quality/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Interview Toolkit →](../70-interview-toolkit/INDEX.md)

---

**Lane-specific overlays:** Add interview strategy context, behavioral stories, and prep plans in [Interview Lanes](../80-lanes-abroad-full-stack/INDEX.md) — the stacks stay stack-pure.
