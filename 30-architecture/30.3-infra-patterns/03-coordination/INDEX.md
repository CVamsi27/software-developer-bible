# Coordination

> **1 file.** Who runs the cron? Who processes the queue? When multiple instances of a service share work, exactly one must lead — and every instance must agree on who. Leader election and consensus answer that question safely.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Coordination-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Scale out to 5 replicas and suddenly scheduled jobs run 5 times, background workers double-process messages. The naive fixes (only deploy one instance, lock in Postgres without fencing) fail exactly when you need them most. This category covers leases, fencing tokens, and consensus-based election — the machinery that keeps duplicated workloads singletons.

---

## File Index

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Leader Election & Consensus](30.3.3.01-leader-election-consensus.md) | Leases, fencing tokens, Raft/Paxos at a distance, split brain, cron and queue coordination | 30 min |

---

## Cross-References

- [Distributed Locks](../../30.2-system-design/01-theory/INDEX.md) — Redlock, ZooKeeper, advisory locks in system-design depth
- [Consensus & Leader Election (theory)](../../30.2-system-design/01-theory/INDEX.md) — the underlying distributed-systems theory

---

## Navigation

[← Failure & Recovery](../02-failure-and-recovery/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Data at Scale →](../04-data-at-scale/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — keeps scheduled work single-flight for real.

| Topic | Docita evidence |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Distributed locks (Postgres advisory) | `shared/common/utils/postgres-advisory-lock.ts` |
| Single-cron leader election | `shared/modules/schedule/cron-heartbeat.ts` — heartbeat + advisory locks so exactly one instance runs each cron |
| Process-level coordination | API ships `ENABLE_SCHEDULERS=false`; crons live in the dedicated worker app |
| Transactional outbox | `shared/modules/outbox/outbox-relay.scheduler.ts` + ADR 0010; CI gate `check-event-emit-via-outbox.mjs` |

_Fencing tokens / Raft-style consensus: no direct docita implementation yet._
