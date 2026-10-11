# Frameworks & Paradigms

> **Study time:** ≈ 45 min of reading (5 files, ~9 min average).
> **5 files.** Where transports meet application code: NestJS gateway wiring, GraphQL subscriptions over pub-sub, WebRTC peer-to-peer media, and how to test all of it under load.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [NestJS WebSockets](60.1.3.01-nestjs-websockets.md) | Gateways, adapters (Socket.IO / WS), guards, pipes, exception filters | Important | Specialized | 11 min |
| 02 | [GraphQL Subscriptions & Live Queries](60.1.3.02-graphql-subscriptions-live-queries.md) | graphql-ws protocol, Redis pub-sub, withFilter server-side authz, live queries vs subscriptions, fan-out scaling, over-emitting costs | Optional | Specialized | 11 min |
| 03 | [WebRTC Peer-to-Peer](60.1.3.03-webrtc-peer-to-peer.md) | getUserMedia / RTCPeerConnection / RTCDataChannel, signaling, ICE/STUN/TURN, mesh vs SFU vs MCU cost math, route discovery | Optional | Specialized | 11 min |
| 04 | [Testing Real-Time Systems](60.1.3.04-testing-realtime-systems.md) | Protocol smoke tests, workload/ramp/churn design, state-recovery oracles, slow consumers and resource trends | Important | Specialized | 10 min |

---

## Why NestJS first

The gateway pattern applies beyond NestJS. Frameworks provide different ways to respond when connections open or close, authenticate connections at acceptance and authorize individual actions through message guards, and validate message payloads through pipes. Learn those responsibilities here, then map them to the corresponding tools in another framework.

Continue with GraphQL subscription execution and its permissions, then WebRTC negotiation and direct/relay/conferencing paths. Finish with protocol testing and state recovery. NestJS is one implementation, not a prerequisite for GraphQL or WebRTC.

---

## Cross-References

- [Transports](../01-transports/INDEX.md) — Socket.IO vs WS adapters.
- [Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) — adapters are also where cross-node fan-out and recovery are explained.
- [NestJS stack](../../../20-backend/20.2-nestjs/INDEX.md) — guards/pipes/filters fundamentals.
- [GraphQL stack](../../../20-backend/20.7-graphql/INDEX.md) — schema/resolver fundamentals behind subscriptions.

---

## Navigation

[← Architecture & Scaling](../02-architecture-and-scaling/INDEX.md) · [↑ WebSockets Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is a companion project. These local paths are source references, not proof of deployment capacity or complete gateway test coverage.

| Topic | Docita evidence |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| NestJS gateways | `apps/api/src/websockets/notifications.gateway.ts`, `payment.websocket.gateway.ts` |
| Shared base class (template-method paradigm) | `apps/api/src/websockets/base-websocket.gateway.ts` — auth + rate-limit plumbing, gateways own room joins |
| WS auth guard | `apps/api/src/shared/modules/auth/auth/ws-jwt-auth.guard.ts` (+ its spec) |
| Realtime testing reality | The local source scan found no gateway-named spec; use the testing chapter to define protocol/permission/recovery checks. A guard unit test alone cannot establish gateway integration coverage. |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
