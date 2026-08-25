# Frameworks & Paradigms

> **1 file** today, **4 planned.** Where transports meet application code: NestJS gateway wiring now; GraphQL subscriptions, WebRTC peer-to-peer, and realtime testing coming next.

[![Files](https://img.shields.io/badge/files-1-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The file

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [NestJS WebSockets](60.1.3.01-nestjs-websockets.md) | Gateways, adapters (Socket.IO / WS), guards, pipes, exception filters | 25 min |

---

## Planned additions

Slots reserved in the renumbered layout — do not link until written:

- **60.1.3.02 — GraphQL Subscriptions & Live Queries** *(upcoming)*: subscription resolvers, pub/sub sources, live queries.
- **60.1.3.03 — WebRTC Peer-to-Peer** *(upcoming)*: signaling, SDP offer/answer, ICE, data channels.
- **60.1.3.04 — Testing Real-Time Systems** *(upcoming)*: socket clients in tests, fake transports, timing assertions.

---

## Why NestJS first

The gateway pattern generalizes beyond NestJS: connection lifecycle hooks, per-connection auth via guards, and message validation via pipes are the same concepts every framework expresses differently. Learn it once here; port it anywhere.

---

## Cross-References

- [Transports](../01-transports/INDEX.md) — Socket.IO vs WS adapters.
- [Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) — adapters are also where the Redis adapter plugs in.
- [NestJS stack](../../../20-backend/20.2-nestjs/INDEX.md) — guards/pipes/filters fundamentals.

---

## Navigation

[← Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) · [↑ WebSockets Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)
