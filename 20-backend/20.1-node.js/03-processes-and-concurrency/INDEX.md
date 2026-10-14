# Processes & Concurrency - Node.js

> **Study time:** ≈ 41 min of reading (6 files, ~7 min average).
> Production concurrency: choose an execution boundary, manage process lifecycle, supervise server processes, then compare that model with Watt's in-process application workers.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Processes%20%26%20Concurrency-success)](../INDEX.md)

---

## Reading flow

Start with the boundary you need to control:

1. Start with [Process & Environment](20.1.3.03-process-environment.md): validate startup configuration, then trace admission → draining → cleanup → exit.
2. Read [Child Processes & Workers](20.1.3.02-child-processes-workers.md) to distinguish an operating-system process from a worker thread and bound offloaded work.
3. Read [Clustering](20.1.3.01-clustering.md) to see how server processes share a port, what remains process-local and what happens to an in-flight request when a worker exits.
4. Read [PM2 Process Supervision](20.1.3.04-pm2-process-supervision.md) to see which lifecycle responsibilities move outside the application and where readiness and restart guarantees stop.
5. Read [Watt Runtime Architecture](20.1.3.05-watt-runtime-architecture.md) to compare process supervision with application-worker supervision inside one Node process.
6. Use [Revision](REVISION.md) to explain the ownership and failure boundaries without copying the examples.

## Chapter map

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Clustering](20.1.3.01-clustering.md) | Cluster module, worker processes sharing a server socket, IPC, load balancing, PM2/systemd, graceful restart, one process per container | Important | Important | 9 min |
| 02 | [Child Processes & Workers](20.1.3.02-child-processes-workers.md) | `spawn`/`exec`/`fork`, `worker_threads`, SharedArrayBuffer + Atomics, thread pool, child process vs worker thread decision | Important | Important | 10 min |
| 03 | [Process & Environment](20.1.3.03-process-environment.md) | `process.env`, `argv`, cwd, lifecycle, signals (SIGTERM/SIGINT), graceful shutdown, exit codes, 12-factor config | Important | Important | 9 min |
| 04 | [PM2 Process Supervision](20.1.3.04-pm2-process-supervision.md) | PM2 daemon and process list, fork vs cluster mode, readiness, reload limits, restart policy, host/container boundary | Important | Important | 5 min |
| 05 | [Watt Runtime Architecture](20.1.3.05-watt-runtime-architecture.md) | Application worker threads, V8 isolate boundaries, `.plt.local` routing, runtime health, shared process and deployment failure domains | Important | Important | 5 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

The [Docita case study](../../../projects/docita/INDEX.md) supplies code pointers to inspect. Current deployment topology, process isolation and signal handling require runtime evidence beyond these paths.

| Topic | Docita evidence |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Process separation over clustering | `apps/worker/src/main.ts` - crons/jobs run in a second deployable (`apps/worker/fly.toml`), not `cluster` workers |
| Child processes | `apps/api/src/shared/modules/database/database-backup.service.ts` - `spawn()`s pg_dump/pg_restore as child processes |
| Background offload | `apps/api/src/shared/modules/queue/queue.worker.module.ts` - job handlers execute in the worker app, off the API event loop |
| Environment & shutdown signals | `apps/api/src/shared/modules/config/env-schema.ts` - inspect validation at boot and verify the current signal handlers and deployment grace period |

Inspect current deployables, process boundaries and lifecycle policies before attributing a scale model to the case study. Chapter fixtures establish their own isolated cluster/worker contracts.
---

[← Previous: I/O & Data](../02-io-and-data/INDEX.md) · [Next: Security & Operations →](../04-security-and-operations/INDEX.md)
