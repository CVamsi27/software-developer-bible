# Coordination

> **Study time:** ≈ 12 min of reading (2 files, ~6 min average).
> **1 file.** Who runs the cron? Who processes the queue? Multiple workers can share a queue through atomic claims; some tasks instead require a single owner. Learn which invariant needs coordination and how stale owners are rejected.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Coordination-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Running five application instances can cause a scheduled job to run five times or background workers to process the same message twice. Running only one instance limits availability and capacity. A database lock also needs protection against an old owner resuming after its ownership expires. This category explains time-limited ownership (leases), increasing ownership numbers that reject old owners (fencing tokens), and leader election through agreement between nodes (consensus).

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Leader Election & Consensus](30.3.3.01-leader-election-consensus.md) | Leases, fencing tokens, Raft/Paxos at a distance, split brain, cron and queue coordination | Important | Specialized | 10 min |

---

## Reading Path and Completion Check

Read [Consensus & Leader Election](../../30.2-system-design/01-theory/30.2.1.09-consensus-and-leader-election.md) first. Then compare the tools used to coordinate running processes, checking how ownership is renewed and how the protected resource rejects an old owner.

Trace a conflict-row wait during acquisition, then show a paused owner resuming after a successor acquires the lease and explain exactly which write the resource rejects. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [Distributed Locks](../../30.2-system-design/01-theory/INDEX.md) — Redlock, ZooKeeper, advisory locks in system-design depth
- [Consensus & Leader Election (theory)](../../30.2-system-design/01-theory/30.2.1.09-consensus-and-leader-election.md) — the underlying distributed-systems theory

---

## Navigation

[← Failure & Recovery](../02-failure-and-recovery/INDEX.md) · [↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Data at Scale →](../04-data-at-scale/INDEX.md)

---

## Docita Anchor

The inspected Docita source separates scheduler telemetry, process placement and selective coordination. These are different mechanisms; none proves every cron is single-flight.

| Topic | Docita evidence |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Distributed locks (Postgres advisory) | `apps/api/src/shared/common/utils/postgres-advisory-lock.ts` — a transaction-scoped try-lock for callers using this helper, not a universal scheduler lock |
| Scheduler telemetry | `apps/api/src/shared/modules/schedule/cron-heartbeat.ts` — records success/failure; it does not acquire a lock or elect a leader |
| Process-level coordination | `fly.toml` disables API schedulers; worker placement does not serialize multiple worker replicas |
| Transactional outbox | `shared/modules/outbox/outbox-relay.scheduler.ts` + ADR 0010; CI gate `check-event-emit-via-outbox.mjs` |

The helper holds a PostgreSQL transaction-scoped lock while awaiting its callback; its timeout argument is unused and the callback does not receive the transaction. Inspect actual callers before claiming protected database writes, fencing or bounded execution. See [async processing](../../../projects/docita/03-async-processing.md) for queue/outbox boundaries.
