# Processes & Concurrency - Node.js

> **Study time:** ≈ 31 min of reading (4 files, ~8 min average).
> **4 files.** Production concurrency: scaling across cores with the cluster module, offloading CPU-bound work to child processes and worker threads, and controlling the process lifecycle (env vars, signals, graceful shutdown).

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Processes%20%26%20Concurrency-success)](../INDEX.md)

---

## Reading flow

Start with the boundary you need to control:

1. Read [Process & Environment](20.1.3.03-process-environment.md) to validate startup configuration and trace admission → draining → resource cleanup → exit.
2. Read [Child Processes & Workers](20.1.3.02-child-processes-workers.md) to choose an execution boundary, then trace task ownership, cancellation and bounded admission.
3. Read [Clustering](20.1.3.01-clustering.md) when one HTTP process needs replication. Follow a connection, a worker crash and a deployment shutdown before choosing a supervisor.
4. Use [Revision](REVISION.md) to explain those choices without copying the examples.

## Chapter map

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Clustering](20.1.3.01-clustering.md) | Cluster module, worker processes sharing a server socket, IPC, load balancing, PM2/systemd, graceful restart, one process per container | Important | Important | 9 min |
| 02 | [Child Processes & Workers](20.1.3.02-child-processes-workers.md) | `spawn`/`exec`/`fork`, `worker_threads`, SharedArrayBuffer + Atomics, thread pool, child process vs worker thread decision | Important | Important | 10 min |
| 03 | [Process & Environment](20.1.3.03-process-environment.md) | `process.env`, `argv`, cwd, lifecycle, signals (SIGTERM/SIGINT), graceful shutdown, exit codes, 12-factor config | Important | Important | 10 min |

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
