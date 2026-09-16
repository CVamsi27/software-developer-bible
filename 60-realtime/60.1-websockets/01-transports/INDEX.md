# Transports

> **Study time:** ≈ 2 h of reading (4 files, ~30 min average).
> **4 files.** The four real-time transport options — raw WebSockets, Server-Sent Events, Socket.IO, and WebTransport — and the decision framework for picking between them.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The 4 transports

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 01 | [WebSockets Overview](60.1.1.01-websockets-overview.md) | Protocol, handshake (HTTP Upgrade), frames, vs HTTP, use cases | Bidirectional real-time | 31 min |
| 02 | [Server-Sent Events](60.1.1.02-server-sent-events.md) | EventSource API, auto-reconnect, vs WebSockets, use cases | Server→client only (notifications, live updates) | 37 min |
| 03 | [Socket.IO](60.1.1.03-socket-io.md) | Client/server setup, rooms, namespaces, events, fallback to polling | Quick bidirectional with rich features | 41 min |
| 04 | [WebTransport](60.1.1.04-webtransport.md) | QUIC-based transport, datagrams, streams, vs WebSocket | Modern, low-latency, unreliable delivery OK | 11 min |

---

## Decision tree

```text
Need real-time communication?
├── Server → client only? ──────────→ SSE (simple, auto-reconnect)
├── Bidirectional, simple? ─────────→ WebSocket (raw)
├── Bidirectional, rich features,
│   fallback? ──────────────────────→ Socket.IO
├── Low-latency, datagrams OK? ─────→ WebTransport (modern)
└── Just initial load? ─────────────→ Polling (or HTTP/2 push)
```

---

## Interview traps

- "WebSocket is just HTTP after the upgrade" — true post-handshake; know what changes (frames, no CORS model, no caching).
- "SSE over HTTP/2 vs WebSocket" — SSE multiplexes fine on HTTP/2; WebSocket still needs its own TCP connection.
- "Why does Socket.IO need fallbacks?" — proxies/CDNs that break the Upgrade handshake.

---

## Cross-References

- [Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) — what happens when one server is not enough.
- [Frameworks & Paradigms](../03-frameworks-and-paradigms/INDEX.md) — where transports get wired into application code.

---

## Navigation

[↑ WebSockets Home](../INDEX.md) · [Next: Architecture & Scaling →](../02-architecture-and-scaling/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| --------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Socket.IO as chosen transport | `socket.io ^4.8.3` in `apps/api/package.json`, wired in `apps/api/src/websockets/websockets.module.ts` |
| SSE (one real, narrow use) | `apps/api/src/shared/modules/ai/ai.controller.ts` streams `text/event-stream` for AI responses |
| Transport-choice rationale | `docs/operations/WEBSOCKET_SCALING.md` — sockets trigger React Query invalidation only |
| Handshake auth at transport level | `apps/api/src/websockets/base-websocket.gateway.ts` (bearer token from `handshake.auth.token`) |
