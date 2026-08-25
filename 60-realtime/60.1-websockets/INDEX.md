# WebSockets — Index

> **8 files** — Real-time communication from WebSocket fundamentals and Socket.IO to Server-Sent Events, real-time architecture, NestJS WebSockets, WebTransport, scaling patterns, and interview questions.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why real-time:** Mid-stage startups increasingly build chat, collaboration, or live-tracking features. Senior interviews test WebSocket protocol knowledge, scaling patterns (sticky sessions, Redis adapter), and the choice between SSE / WebSocket / WebTransport / polling. Read this section when the JD requires it.

---

## Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Transports](#transports) | 4 | WebSocket, SSE, Socket.IO, WebTransport — the options |
| [Architecture & Scaling](#architecture--scaling) | 2 | Real-time architecture, scaling patterns |
| [Frameworks](#frameworks) | 1 | NestJS WebSockets — the production framework |
| [Interview Prep](#interview-prep) | 1 | 50+ Qs |

---

## Transports

The 4 main real-time transports.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 01 | [WebSockets Overview](01-transports/60.1.1.01-websockets-overview.md) | Protocol, handshake (HTTP Upgrade), frames, vs HTTP, use cases | Bidirectional real-time | 30 min |
| 03 | [Server-Sent Events](01-transports/60.1.1.02-server-sent-events.md) | EventSource API, auto-reconnect, vs WebSockets, use cases | Server→client only (notifications, live updates) | 25 min |
| 02 | [Socket.IO](01-transports/60.1.1.03-socket-io.md) | Client/server setup, rooms, namespaces, events, fallback to polling | Quick bidirectional with rich features | 30 min |
| 07 | [WebTransport](01-transports/60.1.1.04-webtransport.md) | QUIC-based transport, datagrams, streams, vs WebSocket | Modern, low-latency, unreliable delivery | 25 min |

**Decision tree:**

```text
Need real-time communication?
├── Server → client only? ──→ SSE (simple, auto-reconnect)
├── Bidirectional, simple? ──→ WebSocket (raw)
├── Bidirectional, rich features, fallback? ──→ Socket.IO
├── Low-latency, unreliable, datagrams? ──→ WebTransport (modern)
└── Just initial load? ──→ Polling (or HTTP/2 push)
```

---

## Architecture & Scaling

The hard part — making it work at scale.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Real-Time Architecture](02-architecture-and-scaling/60.1.2.01-real-time-architecture.md) | Pub/sub, message brokers, scaling WebSockets, state sync, presence | 30 min |
| 08 | [Scaling Patterns](02-architecture-and-scaling/60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, sharding, edge platforms (Cloudflare Durable Objects) | 30 min |

---

## Frameworks

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 05 | [NestJS WebSockets](03-frameworks-and-paradigms/60.1.3.01-nestjs-websockets.md) | Gateways, adapters (Socket.IO / WS), guards, pipes, exception filters | 25 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Interview Questions](04-interview-prep/60.1.4.01-interview-questions.md) | 50+ curated questions with answers | 2-3 hrs |

---

## Suggested Study Order

1. **WebSockets Overview** — the protocol
2. **SSE** — the simpler alternative
3. **Real-Time Architecture** — pub/sub, scaling
4. **Socket.IO** — most common production lib
5. **Scaling Patterns** — for senior roles
6. **NestJS WebSockets** — if NestJS stack
7. **WebTransport** — modern, optional
8. **Interview Questions** — final review

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
