# Transports

> **Study time:** ≈ 50 min of reading (5 files, ~10 min average).
> **5 files.** The four real-time transport options — raw WebSockets, Server-Sent Events, Socket.IO, and WebTransport — and the decision framework for picking between them.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Pass 1 — Decide Which Direction Carries the Update

Start with [WebSockets Overview](60.1.1.01-websockets-overview.md) to separate a long-lived bidirectional connection from ordinary request/response. Then read [Server-Sent Events](60.1.1.02-server-sent-events.md): the server sends a stream of events while the client can still issue ordinary HTTP requests. Native EventSource reconnects, but retained events and authorized replay remain server responsibilities.

## Pass 2 — Add Application Features Deliberately

[Socket.IO](60.1.1.03-socket-io.md) adds an application protocol, named events, rooms, reconnection and transport choices. It is not interchangeable with a raw WebSocket client. If polling is enabled across several servers, requests for one Engine.IO session need the node that owns it; a shared adapter alone does not create that affinity.

## Pass 3 — Separate Reliable Bytes From Replaceable State

[WebTransport](60.1.1.04-webtransport.md) is useful when independent streams or unreliable datagrams solve a concrete problem. Trace an out-of-order position update, then explain why a full snapshot can tolerate loss while a dependent delta cannot. Verify browser, endpoint and network support before choosing it.

| Need | Starting option | Condition to verify |
| ----------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| Initial document or occasional refresh | Ordinary HTTP; polling if repeated reads are acceptable | Poll frequency, freshness and server cost |
| Server-to-browser updates | SSE | Proxy buffering, authorization and replay |
| Bidirectional messages | WebSocket | Heartbeats, bounded queues and application recovery |
| Named events, rooms and reconnection conveniences | Socket.IO | Protocol compatibility, affinity and adapter semantics |
| Independent streams or replaceable unreliable updates | WebTransport | Complete protocol path and application recovery |

These are starting choices, not speed rankings. WebSocket after an HTTP/1.1 upgrade uses WebSocket frames rather than ordinary HTTP request/response messages. WebSocket over HTTP/2 or HTTP/3 uses extended CONNECT where the deployment supports it; do not assume every browser/proxy combination implements that path. See [RFC 8441](https://www.rfc-editor.org/rfc/rfc8441.html) and [RFC 9220](https://www.rfc-editor.org/rfc/rfc9220.html).

## Finish With Revision, Then Architecture and Practice

Close the chapters and work through [section revision questions](REVISION.md). Explain transport delivery separately from application acknowledgment, replay and durable effects. Continue to architecture/scaling before using the separate [interview bank](../04-interview-prep/60.1.4.01-interview-questions.md).

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
| --------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Socket.IO as chosen transport | `socket.io` dependency in `apps/api/package.json`, wired in `apps/api/src/websockets/websockets.module.ts` |
| SSE (one real, narrow use) | `apps/api/src/shared/modules/ai/ai.controller.ts` streams `text/event-stream` for AI responses |
| Transport-choice rationale | `docs/operations/WEBSOCKET_SCALING.md` — sockets trigger React Query invalidation only |
| Handshake auth at transport level | `apps/api/src/websockets/base-websocket.gateway.ts` (bearer token from `handshake.auth.token`) |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
