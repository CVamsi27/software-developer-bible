# Real-Time Stack

> **Study time:** ≈ 2 h 3 m of reading (14 files, ~9 min average).
> **WebSockets, SSE, real-time architecture** — optional stack, study when a JD demands it. Shared by both lanes.
>
> Study in three passes: **I. Protocols** (which transport, and why) → **II. Implementation** (Socket.IO, NestJS gateways) → **III. Architecture at scale** (fan-out, sticky sessions, pub/sub backbones).

[![Files](https://img.shields.io/badge/files-14-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-RealTime-orange)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Docita Anchor

The [Docita companion](https://github.com/CVamsi27/docita) has notification/payment gateways, a shared base class and clinic/user room routing in the local source checked on 9 October 2026. Its `docs/operations/WEBSOCKET_SCALING.md` documents a single-replica boundary and required cross-replica verification before scaling. These source references do not establish live production capacity, successful recovery or a deployed Redis adapter.

---

## Topic Categories

The topics below group transport choices, application integration, peer connectivity, architecture and practice. Use the learning passes to connect their mechanisms.

| Category | Files | Why it matters |
| ------------------------------------------------------------ | ----: | ---------------------------------------------------------------------------------------------- |
| [Transport Protocols](#transport-protocols) | 3 | WebSockets vs SSE vs WebTransport — pick the right pipe before writing code |
| [Framework Implementation](#framework-implementation) | 3 | Socket.IO semantics, NestJS gateways, GraphQL subscriptions — where code actually gets written |
| [Peer-to-Peer & Data Channels](#peer-to-peer--data-channels) | 1 | WebRTC — direct routes, relay fallback and conferencing |
| [Architecture & Scale](#architecture--scale) | 2 | Fan-out, presence, sticky sessions, Redis adapter — surviving >1 node |
| [Testing & Drills](#testing--drills) | 2 | Load/chaos/soak testing realtime systems + curated Q&A |

---

## Learning Passes

Use the [WebSockets learning flow](60.1-websockets/INDEX.md) for category prerequisites, revision companions and interview practice.

1. **Choose a channel:** compare WebSocket, SSE and Socket.IO. Read WebTransport when its stream/datagram behavior is relevant to the role. Complete the [transport revision](60.1-websockets/01-transports/REVISION.md).
2. **Explain state and recovery:** trace a committed update, missed publication and reconnect in architecture/scaling. Complete the [architecture revision](60.1-websockets/02-architecture-and-scaling/REVISION.md).
3. **Implement and verify:** follow the relevant NestJS, GraphQL or WebRTC mechanism, then separate local protocol evidence from network, load and recovery checks. Complete the [framework revision](60.1-websockets/03-frameworks-and-paradigms/REVISION.md).
4. **Practice:** answer the interview bank and its follow-ups aloud, reproducing a focused canonical example when an explanation is incomplete.

Reading estimates do not include reproducing examples or interview rehearsal. Prioritize by the role's requirements and the mechanisms you cannot yet explain.

---

## Transport Protocols

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 1 | [WebSockets Overview](60.1-websockets/01-transports/60.1.1.01-websockets-overview.md) | Handshake, frames, heartbeat, when WS beats polling | Important | Specialized | 13 min |
| 2 | [Server-Sent Events](60.1-websockets/01-transports/60.1.1.02-server-sent-events.md) | Auto-reconnect, `Last-Event-ID`, one-way push over plain HTTP | Important | Specialized | 12 min |
| 3 | [WebTransport](60.1-websockets/01-transports/60.1.1.04-webtransport.md) | HTTP/3, QUIC streams, unidirectional/bidirectional/datagram | Optional | Specialized | 9 min |

## Framework Implementation

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 4 | [Socket.IO](60.1-websockets/01-transports/60.1.1.03-socket-io.md) | Rooms, namespaces, acks, fallbacks, reconnection semantics | Important | Specialized | 14 min |
| 5 | [NestJS WebSockets](60.1-websockets/03-frameworks-and-paradigms/60.1.3.01-nestjs-websockets.md) | Gateways, decorators, lifecycle hooks — production wiring | Important | Specialized | 11 min |
| 6 | [GraphQL Subscriptions & Live Queries](60.1-websockets/03-frameworks-and-paradigms/60.1.3.02-graphql-subscriptions-live-queries.md) | graphql-ws protocol, Redis pub-sub fan-out, withFilter authz, over-emitting costs | Optional | Specialized | 11 min |

## Peer-to-Peer & Data Channels

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 7 | [WebRTC Peer-to-Peer](60.1-websockets/03-frameworks-and-paradigms/60.1.3.03-webrtc-peer-to-peer.md) | getUserMedia / RTCPeerConnection / RTCDataChannel, signaling, ICE/STUN/TURN, mesh vs SFU vs MCU cost math | Optional | Specialized | 11 min |

## Architecture & Scale

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 8 | [Real-Time Architecture](60.1-websockets/02-architecture-and-scaling/60.1.2.01-real-time-architecture.md) | Transport decision tree, presence, delivery guarantees | Important | Specialized | 9 min |
| 9 | [Scaling Patterns](60.1-websockets/02-architecture-and-scaling/60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, pub/sub backbone, connection limits | Important | Specialized | 8 min |

## Testing & Drills

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 10 | [Testing Real-Time Systems](60.1-websockets/03-frameworks-and-paradigms/60.1.3.04-testing-realtime-systems.md) | Protocol smoke checks, workload/churn design, recovery oracles and soak evidence | Important | Specialized | 10 min |

| File | Contents | Role priority | General importance |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------- | ------------------ |
| [Interview Questions](60.1-websockets/04-interview-prep/60.1.4.01-interview-questions.md) | Curated Q&A: protocol trade-offs, scaling, failure modes | Important | Specialized |

---

## The 60-Second Orientation

```text
Need server→client push only? → SSE (auto-reconnect, Last-Event-ID)
Need bidirectional (chat/collab)? → WebSockets (Socket.IO for rooms/fallbacks)
Managed connection service? → verify ownership, protocol, quotas and recovery
Multiple gateways? → cross-node routing; polling affinity where required; recover state
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
