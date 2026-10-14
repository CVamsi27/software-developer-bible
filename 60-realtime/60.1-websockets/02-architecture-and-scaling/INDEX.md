# Architecture & Scaling

> **Study time:** ≈ 19 min of reading (3 files, ~6 min average).
> **3 files.** Real-time system design: pub/sub topologies, presence, state sync — then the concrete scaling patterns (sticky sessions, Redis adapter, sharding) that keep connections alive past one node.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Real--Time-%2300b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this is the hard part

Start with a durable change and trace how an authorized client learns about it. Then distribute connections across gateways and identify what fails between commit, publication and recovery. Measure the real workload; a single-node demonstration does not establish a universal capacity limit.

---

## Two learning chapters

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Real-Time Architecture](60.1.2.01-real-time-architecture.md) | Pub/sub, message brokers, scaling WebSockets, state sync, presence | Important | Specialized | 9 min |
| 02 | [Scaling Patterns](60.1.2.02-scaling-patterns.md) | Sticky sessions, Redis adapter, sharding, edge platforms (Cloudflare Durable Objects) | Important | Specialized | 8 min |

---

## Learning Passes

1. **Delivery contract:** read the architecture chapter and trace a booking committed before notification fails. Separate live fan-out, retained history and work distribution.
2. **Fleet behavior:** read scaling patterns and trace one room across two gateways. Explain polling affinity, recovery on another node, slow-client policy and failure headroom.
3. **Revision:** complete the [source-linked revision questions](REVISION.md), then move to framework implementation and interview practice.

A cross-node audience needs routing that reaches its owning gateways. A broker/adapter is one implementation; an explicit inter-gateway routing service is another. Choose from workload and failure requirements rather than an “always use Redis” rule.

---

## Cross-References

- [Transports](../01-transports/INDEX.md) — the pipes being scaled.
- [Microservices event-driven patterns](../../../20-backend/20.6-microservices/INDEX.md) — brokers in depth.

---

## Navigation

[← Transports](../01-transports/INDEX.md) · [↑ WebSockets Home](../INDEX.md) · [Next: Frameworks & Paradigms →](../03-frameworks-and-paradigms/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is a companion project. The paths below were checked in the local checkout on 14 October 2026; source presence does not establish a deployed topology or successful recovery drill.

| Topic | Docita evidence |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tenant-scoped rooms | `apps/api/src/websockets/notifications.gateway.ts` joins `clinic:{clinicId}` / `user:{sub}` rooms |
| Connection auth | `ws-jwt-auth.guard.ts` (in `shared/modules/auth/auth/`) + base-gateway handshake verification |
| Per-connection rate limiting | `base-websocket.gateway.ts` rate-limit map + error envelope |
| Scaling honesty | `docs/operations/WEBSOCKET_SCALING.md`: single-replica boundary documented; **no Redis pub/sub adapter yet** — sticky sessions alone called out as insufficient, adoption deferred until a second replica is real |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
