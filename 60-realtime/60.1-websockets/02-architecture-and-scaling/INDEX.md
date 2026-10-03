# Architecture & Scaling

> **Study time:** ≈ 48 min of reading (3 files, ~16 min average).
> **3 files.** Real-time system design: pub/sub topologies, presence, state sync — then the concrete scaling patterns (sticky sessions, Redis adapter, sharding) that keep connections alive past one node.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this is the hard part

Transports are solved problems; scale is where real-time systems die. A single Node process holds ~10K+ sockets comfortably — the interesting questions start at node two: who receives this message, which instance owns which connection, and what happens during reconnect.

---

## The 2 files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Real-Time Architecture](60.1.2.01-real-time-architecture.md) | Pub/sub, message brokers, scaling WebSockets, state sync, presence | Important | Specialized | 34 min |
| 02 | [Scaling Patterns](60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, sharding, edge platforms (Cloudflare Durable Objects) | Important | Specialized | 11 min |

---

## The escalation path

```text
1 node            → done, skip the rest
N nodes, same LB  → sticky sessions + Socket.IO Redis adapter
10K+ connections  → shard connection space; pub/sub backbone (Redis/Kafka)
Global users      → edge termination (Durable Objects / managed pub-sub)
```

Interview favorite: "How do you broadcast to a room whose members are spread across 20 servers?" — the answer is always an off-box bus (Redis pub/sub or broker fan-out), never inter-server socket chatter.

---

## Cross-References

- [Transports](../01-transports/INDEX.md) — the pipes being scaled.
- [Microservices event-driven patterns](../../../20-backend/20.6-microservices/INDEX.md) — brokers in depth.

---

## Navigation

[← Transports](../01-transports/INDEX.md) · [↑ WebSockets Home](../INDEX.md) · [Next: Frameworks & Paradigms →](../03-frameworks-and-paradigms/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to — each topic below points at where it actually runs in that codebase.

| Topic | Docita evidence |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tenant-scoped rooms | `apps/api/src/websockets/notifications.gateway.ts` joins `clinic:{clinicId}` / `user:{sub}` rooms |
| Connection auth | `ws-jwt-auth.guard.ts` (in `shared/modules/auth/auth/`) + base-gateway handshake verification |
| Per-connection rate limiting | `base-websocket.gateway.ts` rate-limit map + error envelope |
| Scaling honesty | `docs/operations/WEBSOCKET_SCALING.md`: single-replica boundary documented; **no Redis pub/sub adapter yet** — sticky sessions alone called out as insufficient, adoption deferred until a second replica is real |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
