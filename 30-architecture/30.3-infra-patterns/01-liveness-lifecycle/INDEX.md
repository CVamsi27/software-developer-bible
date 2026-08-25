# Liveness & Lifecycle

> **1 file.** The contract between your application and its orchestrator: prove you are alive, prove you are ready, and die gracefully when asked. Get this wrong and Kubernetes restarts healthy pods — or routes traffic to dying ones.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Lifecycle-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

Every orchestrator (Kubernetes, ECS, Nomad) manages your process through two questions — "are you alive?" and "are you ready?" — plus one command: "shut down now." If your health endpoints lie or your process ignores SIGTERM, you get crash-loop restarts, dropped in-flight requests, and corrupted shutdowns. This category covers the mechanics once, properly.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Health Checks & Graceful Shutdown](30.3.1.01-health-checks-graceful-shutdown.md) | Liveness vs readiness vs startup probes, health endpoint design, SIGTERM handling, connection draining, shutdown hooks | 25 min |

---

## Cross-References

- [Failure & Recovery](../02-failure-and-recovery/INDEX.md) — what to do when liveness checks fail
- [Kubernetes Health Checks](../../../40-platform/40.2-kubernetes/04-production-hardening/INDEX.md) — probe configuration on the platform side

---

## Navigation

[↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Failure & Recovery →](../02-failure-and-recovery/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — proves liveness for real (on Fly.io, not Kubernetes).

| Topic | Docita evidence |
|-------|-----------------|
| Health endpoints | `shared/common/controllers/health-check.controller.ts` + `monitoring/health.service.ts`, `monitoring/health/prisma.health.ts` |
| Orchestrator probes | Fly `[checks.health]` hits `/api/health/live` every 15s with a 240s deploy grace period (`fly.toml`) |
| Liveness vs DB readiness | Live probe kept separate from the Prisma health indicator so a DB blip doesn't kill the machine |
| Scheduler lifecycle | `ENABLE_SCHEDULERS=false` on the API + `cron-heartbeat.ts` in the worker prevent double-running jobs |
| Suspend/resume lifecycle | ADR 0011: `auto_stop_machines='suspend'` off-hours, auto-start on request |
