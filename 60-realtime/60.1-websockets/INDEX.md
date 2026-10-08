# WebSockets — Index

> **Study time:** ≈ 4 h 47 m of reading (14 files, ~20 min average).
> **14 files across 4 categories.** Real-time communication from WebSocket fundamentals and Socket.IO to Server-Sent Events, real-time architecture, NestJS WebSockets, GraphQL subscriptions, WebRTC peer-to-peer, testing realtime systems, WebTransport, scaling patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-14-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why real-time:** Mid-stage startups increasingly build chat, collaboration, or live-tracking features. Senior interviews test WebSocket protocol knowledge, scaling patterns (sticky sessions, Redis adapter), and the choice between SSE / WebSocket / WebTransport / polling. Read this section when the JD requires it.

---

## The 4 Categories (in study order)

| Category | Files | Purpose |
| ------------------------------------------------------------------- | ----: | -------------------------------------------------------------------- |
| [01 — Transports](01-transports/INDEX.md) | 4 | WebSocket, SSE, Socket.IO, WebTransport — the options |
| [02 — Architecture & Scaling](02-architecture-and-scaling/INDEX.md) | 2 | Real-time architecture, scaling patterns |
| [03 — Frameworks & Paradigms](03-frameworks-and-paradigms/INDEX.md) | 4 | NestJS gateways, GraphQL subscriptions, WebRTC P2P, realtime testing |
| [04 — Interview Prep](04-interview-prep/INDEX.md) | 1 | 50+ Qs |

---

## Transports

The 4 main real-time transports.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [WebSockets Overview](01-transports/60.1.1.01-websockets-overview.md) | Protocol, handshake (HTTP Upgrade), frames, vs HTTP, use cases | Bidirectional real-time | Important | Specialized | 30 min |
| 02 | [Server-Sent Events](01-transports/60.1.1.02-server-sent-events.md) | EventSource API, auto-reconnect, vs WebSockets, use cases | Server→client only (notifications, live updates) | Important | Specialized | 36 min |
| 03 | [Socket.IO](01-transports/60.1.1.03-socket-io.md) | Client/server setup, rooms, namespaces, events, fallback to polling | Quick bidirectional with rich features | Important | Specialized | 40 min |
| 04 | [WebTransport](01-transports/60.1.1.04-webtransport.md) | QUIC-based transport, datagrams, streams, vs WebSocket | Modern, low-latency, unreliable delivery OK | Optional | Specialized | 9 min |

**Decision tree:**

```text
Need real-time communication?
├── Server → client only? ──→ SSE (simple, auto-reconnect)
├── Bidirectional, simple? ──→ WebSocket (raw)
├── Bidirectional, rich features, fallback? ──→ Socket.IO
├── Low-latency, unreliable, datagrams? ──→ WebTransport (modern)
└── Just initial load? ──→ ordinary HTTP request (poll only for repeated updates)
```

---

## Architecture & Scaling

The hard part — making it work at scale.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Real-Time Architecture](02-architecture-and-scaling/60.1.2.01-real-time-architecture.md) | Pub/sub, message brokers, scaling WebSockets, state sync, presence | Important | Specialized | 35 min |
| 02 | [Scaling Patterns](02-architecture-and-scaling/60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, sharding, edge platforms (Cloudflare Durable Objects) | Important | Specialized | 11 min |

---

## Frameworks & Paradigms

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [NestJS WebSockets](03-frameworks-and-paradigms/60.1.3.01-nestjs-websockets.md) | Gateways, adapters (Socket.IO / WS), guards, pipes, exception filters | Important | Specialized | 32 min |
| 02 | [GraphQL Subscriptions & Live Queries](03-frameworks-and-paradigms/60.1.3.02-graphql-subscriptions-live-queries.md) | graphql-ws protocol, Redis pub-sub, withFilter, live queries, fan-out scaling | Optional | Specialized | 15 min |
| 03 | [WebRTC Peer-to-Peer](03-frameworks-and-paradigms/60.1.3.03-webrtc-peer-to-peer.md) | getUserMedia, RTCPeerConnection, RTCDataChannel, ICE/STUN/TURN, mesh vs SFU vs MCU | Optional | Specialized | 12 min |
| 04 | [Testing Real-Time Systems](03-frameworks-and-paradigms/60.1.3.04-testing-realtime-systems.md) | Artillery WS scenarios, churn, ordering/backpressure assertions, chaos drills, soak tests | Important | Specialized | 15 min |

---

## Interview Prep

| # | File | Contents | Time | Role priority | General importance |
| --: | ------ | ---------- | ------ | --- | --- |
| 01 | [Interview Questions](04-interview-prep/60.1.4.01-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs | Important | Specialized |

---

## Suggested Study Order

1. **WebSockets Overview** — the protocol
2. **SSE** — the simpler alternative
3. **Real-Time Architecture** — pub/sub, scaling
4. **Socket.IO** — most common production lib
5. **Scaling Patterns** — for senior roles
6. **NestJS WebSockets** — if NestJS stack
7. **GraphQL Subscriptions** — schema-first realtime
8. **WebRTC Peer-to-Peer** — video/audio/data without servers
9. **Testing Real-Time Systems** — prove it survives production
10. **WebTransport** — modern, optional
11. **Interview Questions** — final review

---

## Common interview topics

- "WebSocket vs SSE — when to use which?"
- "How do you scale WebSockets across multiple servers?"
- "How do you authenticate WebSocket connections?"
- "What's the difference between Socket.IO and raw WebSockets?"
- "How do you handle reconnection and message ordering?"

---

## Cross-References

- [NestJS](../../20-backend/20.2-nestjs/INDEX.md) — NestJS WebSockets gateways
- [Observability](../../40-platform/40.4-observability/INDEX.md) — monitoring real-time
- [System Design (WhatsApp, Chat System)](../../30-architecture/30.2-system-design/02-case-studies/INDEX.md) — real-time case studies

---

## Navigation

[← Previous: Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Behavioral →](../../70-interview-toolkit/70.1-behavioral/INDEX.md)
