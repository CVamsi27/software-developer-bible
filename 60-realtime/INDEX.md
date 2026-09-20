# Real-Time Stack

> **Study time:** ≈ 4 h 55 m of reading (11 files, ~27 min average).
> **WebSockets, SSE, real-time architecture** — optional stack, study when a JD demands it. Shared by both lanes.
>
> Study in three passes: **I. Protocols** (which transport, and why) → **II. Implementation** (Socket.IO, NestJS gateways) → **III. Architecture at scale** (fan-out, sticky sessions, pub/sub backbones).

[![Files](https://img.shields.io/badge/files-11-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-RealTime-orange)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Docita Anchor

Real-time here is not theoretical: [docita](https://github.com/CVamsi27/docita) runs Socket.IO (`^4.8.3`) with two authenticated NestJS gateways sharing a `BaseWebSocketGateway` base class, `clinic:{id}` tenant-scoped rooms, per-connection rate limits, and one deliberate SSE use (AI streaming). Its scaling story is honestly documented in `docs/operations/WEBSOCKET_SCALING.md`: single-replica boundary, no Redis pub/sub adapter yet. Category INDEXes under [60.1-websockets/](60.1-websockets/INDEX.md) carry verified **Docita Anchor** tables.

---

## Topic Categories

The 11 files organize into 5 conceptual categories — the "GoF classification" of real-time systems. Read in order within each.

| Category | Files | Why it matters |
| ------------------------------------------------------------ | ----: | ---------------------------------------------------------------------------------------------- |
| [Transport Protocols](#transport-protocols) | 3 | WebSockets vs SSE vs WebTransport — pick the right pipe before writing code |
| [Framework Implementation](#framework-implementation) | 3 | Socket.IO semantics, NestJS gateways, GraphQL subscriptions — where code actually gets written |
| [Peer-to-Peer & Data Channels](#peer-to-peer--data-channels) | 1 | WebRTC — media without servers |
| [Architecture & Scale](#architecture--scale) | 2 | Fan-out, presence, sticky sessions, Redis adapter — surviving >1 node |
| [Testing & Drills](#testing--drills) | 2 | Load/chaos/soak testing realtime systems + curated Q&A |

---

## The Track — Read In This Order

```text
Pass I — TRANSPORTS           Pass II — ARCHITECTURE & SCALE    Pass III — DRILLS
websockets-overview     ──┐   real-time-architecture      ──┐   interview-questions
server-sent-events        ├→  scaling-patterns              ├→
socket-io                 │                                 │
webtransport            ──┘                                 ┘

NestJS gateways: read alongside Pass II when wiring production code.
```

**Total time: ~6 hours.** Skip WebTransport if interviewing before next week; it's a bonus-point topic.

---

## Transport Protocols

| Order | File | Topics | Read time |
| ----: | ------------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------: |
| 1 | [WebSockets Overview](60.1-websockets/01-transports/60.1.1.01-websockets-overview.md) | Handshake, frames, heartbeat, when WS beats polling | 31 min |
| 2 | [Server-Sent Events](60.1-websockets/01-transports/60.1.1.02-server-sent-events.md) | Auto-reconnect, `Last-Event-ID`, one-way push over plain HTTP | 37 min |
| 3 | [WebTransport](60.1-websockets/01-transports/60.1.1.04-webtransport.md) | HTTP/3, QUIC streams, unidirectional/bidirectional/datagram | 11 min |

## Framework Implementation

| Order | File | Topics | Read time |
| ----: | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------: |
| 4 | [Socket.IO](60.1-websockets/01-transports/60.1.1.03-socket-io.md) | Rooms, namespaces, acks, fallbacks, reconnection semantics | 41 min |
| 5 | [NestJS WebSockets](60.1-websockets/03-frameworks-and-paradigms/60.1.3.01-nestjs-websockets.md) | Gateways, decorators, lifecycle hooks — production wiring | 33 min |
| 6 | [GraphQL Subscriptions & Live Queries](60.1-websockets/03-frameworks-and-paradigms/60.1.3.02-graphql-subscriptions-live-queries.md) | graphql-ws protocol, Redis pub-sub fan-out, withFilter authz, over-emitting costs | 16 min |

## Peer-to-Peer & Data Channels

| Order | File | Topics | Read time |
| ----: | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------: |
| 7 | [WebRTC Peer-to-Peer](60.1-websockets/03-frameworks-and-paradigms/60.1.3.03-webrtc-peer-to-peer.md) | getUserMedia / RTCPeerConnection / RTCDataChannel, signaling, ICE/STUN/TURN, mesh vs SFU vs MCU cost math | 14 min |

## Architecture & Scale

| Order | File | Topics | Read time |
| ----: | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | --------: |
| 8 | [Real-Time Architecture](60.1-websockets/02-architecture-and-scaling/60.1.2.01-real-time-architecture.md) | Transport decision tree, presence, delivery guarantees | 36 min |
| 9 | [Scaling Patterns](60.1-websockets/02-architecture-and-scaling/60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, pub/sub backbone, connection limits | 12 min |

## Testing & Drills

| Order | File | Topics | Read time |
| ----: | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------: |
| 10 | [Testing Real-Time Systems](60.1-websockets/03-frameworks-and-paradigms/60.1.3.04-testing-realtime-systems.md) | Artillery WS scenarios, churn, ordering/backpressure assertions, chaos drills, soak tests | 17 min |

| File | Contents |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------- |
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
