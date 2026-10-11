# Liveness & Lifecycle

> **Study time:** ≈ 11 min of reading (2 files, ~6 min average).
> **1 file.** The contract between your application and its orchestrator: prove you are alive, prove you are ready, and die gracefully when asked. Get this wrong and Kubernetes restarts healthy pods — or routes traffic to dying ones.

[![Files](https://img.shields.io/badge/files-2-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Lifecycle-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

An orchestrator such as Kubernetes, ECS or Nomad starts and manages application processes. It checks whether a process is alive and ready to serve, and asks it to shut down. Incorrect health responses or ignored termination requests such as SIGTERM can cause repeated restarts, dropped ongoing requests, and incomplete cleanup. This category explains how those checks and shutdown steps work.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Health Checks & Graceful Shutdown](30.3.1.01-health-checks-graceful-shutdown.md) | Liveness vs readiness vs startup probes, health endpoint design, SIGTERM handling, connection draining, shutdown hooks | Essential | Important | 9 min |

---

## Reading Path and Completion Check

Read what each health probe checks before learning shutdown handling. Then follow one request as the platform stops sending new traffic, allows ongoing work to finish, and forcibly stops the process if it exceeds the shutdown deadline.

Distinguish a dependency outage from a stuck process and show why the two produce different probe decisions. Then use [section revision](REVISION.md) without reopening the chapters. Interview banks, where present, are a separate drill after this check.

## Cross-References

- [Failure & Recovery](../02-failure-and-recovery/INDEX.md) — what to do when liveness checks fail
- [Kubernetes Health Checks](../../../40-platform/40.2-kubernetes/04-production-hardening/INDEX.md) — probe configuration on the platform side

---

## Navigation

[↑ Infra & Ops Patterns Home](../INDEX.md) · [Next: Failure & Recovery →](../02-failure-and-recovery/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — provides related lifecycle configuration (Fly.io rather than Kubernetes). The paths are source pointers; verify runtime actions and accepted-work outcomes separately.

| Topic | Docita evidence |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Health endpoints | `shared/common/controllers/health-check.controller.ts` + `apps/api/src/shared/modules/monitoring/monitoring/health.service.ts`, `apps/api/src/shared/modules/monitoring/monitoring/health/prisma.health.ts` |
| Orchestrator probes | Fly `[[http_service.checks]]` requests `/api/health/live` every 15s, with a 5s timeout and 30s grace in the inspected `fly.toml` |
| Liveness vs DB readiness | Live probe kept separate from the Prisma health indicator so a DB blip doesn't kill the machine |
| Scheduler lifecycle | API scheduler disablement separates process roles; heartbeat records runs without preventing concurrent worker execution |
| Suspend/resume lifecycle | `fly.toml` sets suspend, auto-start and min_machines_running=0; this permits cold/resume latency and does not guarantee a warm API |
