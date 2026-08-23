# WebSockets — Index

> **Real-time communication inside the backend stack** — protocol mechanics, scaling, failure handling. For the dedicated realtime stack see [60-realtime](../../60-realtime/60.1-websockets/INDEX.md).

[![Files](https://img.shields.io/badge/files-2-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

## Study Order

| # | File | Topics |
|---|------|--------|
| 1 | [WebSockets Deep Dive](20.9.01-websockets-deep-dive.md) | Protocol handshake, Socket.IO, rooms/namespaces, scaling with Redis adapter, reconnection strategies |
| 2 | [Server-Sent Events](20.9.02-server-sent-events.md) | SSE vs WebSocket decision, NestJS SSE implementation, auto-reconnect, Last-Event-ID, heartbeats |

## WS vs SSE vs Polling (the interview answer)

| | WebSockets | SSE | Long-polling |
|---|---|---|---|
| Direction | Bidirectional | Server→client | Client-initiated |
| Transport | Own protocol (upgrade) | Plain HTTP | HTTP |
| Proxy/firewall pain | Some | Minimal | Minimal |
| Reconnect semantics | Manual/library | Built-in (`Last-Event-ID`) | Manual |
| Use when | Chat, collab, games | Feeds, notifications, progress | Fallback only |

## Cross-references

- [Realtime stack](../../60-realtime/60.1-websockets/INDEX.md) · [NestJS gateways](../20.2-nestjs/INDEX.md) · [Event-driven architecture](../20.11-event-driven/INDEX.md)

---

## Navigation

[← Previous: Caching](../20.8-caching/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: API Design →](../20.10-api-design/INDEX.md)
