# Frameworks & Paradigms

> **Study time:** ≈ 1 h 16 m of reading (5 files, ~15 min average).
> **5 files.** Where transports meet application code: NestJS gateway wiring, GraphQL subscriptions over pub-sub, WebRTC peer-to-peer media, and how to test all of it under load.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [NestJS WebSockets](60.1.3.01-nestjs-websockets.md) | Gateways, adapters (Socket.IO / WS), guards, pipes, exception filters | Important | Specialized | 32 min |
| 02 | [GraphQL Subscriptions & Live Queries](60.1.3.02-graphql-subscriptions-live-queries.md) | graphql-ws protocol, Redis pub-sub, withFilter server-side authz, live queries vs subscriptions, fan-out scaling, over-emitting costs | Optional | Specialized | 15 min |
| 03 | [WebRTC Peer-to-Peer](60.1.3.03-webrtc-peer-to-peer.md) | getUserMedia / RTCPeerConnection / RTCDataChannel, signaling, ICE/STUN/TURN, mesh vs SFU vs MCU cost math, NAT types | Optional | Specialized | 12 min |
| 04 | [Testing Real-Time Systems](60.1.3.04-testing-realtime-systems.md) | Artillery WS scenarios (connect rate, churn, throughput), ordering/backpressure assertions, killing Redis mid-stream, soak tests for fd leaks, CI smoke suites | Important | Specialized | 15 min |

---

## Why NestJS first

The gateway pattern applies beyond NestJS. Frameworks provide different ways to respond when connections open or close, check each connection's permissions through guards, and validate messages through pipes. Learn those responsibilities here, then map them to the corresponding tools in another framework.

Subscriptions (02) build on that gateway foundation; WebRTC (03) needs signaling but no media servers; testing (04) closes the loop on everything above.

---

## Cross-References

- [Transports](../01-transports/INDEX.md) — Socket.IO vs WS adapters.
- [Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) — adapters are also where the Redis adapter plugs in.
- [NestJS stack](../../../20-backend/20.2-nestjs/INDEX.md) — guards/pipes/filters fundamentals.
- [GraphQL stack](../../../20-backend/20.7-graphql/INDEX.md) — schema/resolver fundamentals behind subscriptions.

---

## Navigation

[← Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) · [↑ WebSockets Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| NestJS gateways | `apps/api/src/websockets/notifications.gateway.ts`, `payment.websocket.gateway.ts` |
| Shared base class (template-method paradigm) | `apps/api/src/websockets/base-websocket.gateway.ts` — auth + rate-limit plumbing, gateways own room joins |
| WS auth guard | `apps/api/src/shared/modules/auth/auth/ws-jwt-auth.guard.ts` (+ its spec) |
| Realtime testing reality | only `ws-jwt-auth.guard.spec.ts` exists — no gateway specs yet (_honest gap_) |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
