# Processes & Concurrency - Node.js

> **3 files.** Production concurrency: scaling across cores with the cluster module, offloading CPU-bound work to child processes and worker threads, and controlling the process lifecycle (env vars, signals, graceful shutdown).

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Processes%20%26%20Concurrency-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Clustering](20.1.3.01-clustering.md) | Cluster module, worker processes sharing a server socket, IPC, load balancing, PM2/systemd, graceful restart, one process per container | 25 min |
| 02 | [Child Processes & Workers](20.1.3.02-child-processes-workers.md) | `spawn`/`exec`/`fork`, `worker_threads`, SharedArrayBuffer + Atomics, thread pool, child process vs worker thread decision | 30 min |
| 03 | [Process & Environment](20.1.3.03-process-environment.md) | `process.env`, `argv`, cwd, lifecycle, signals (SIGTERM/SIGINT), graceful shutdown, exit codes, 12-factor config | 20 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Process separation over clustering | `apps/worker/src/main.ts` - crons/jobs run in a second deployable (`apps/worker/fly.toml`), not `cluster` workers |
| Child processes | `apps/api/src/shared/modules/database/database-backup.service.ts` - `spawn()`s pg_dump/pg_restore as child processes |
| Background offload | `apps/api/src/shared/modules/queue/queue.worker.module.ts` - job handlers execute in the worker app, off the API event loop |
| Environment & shutdown signals | `apps/api/src/shared/modules/config/env-schema.ts` - Zod-validated env at boot; SIGTERM drains the worker in 15 s |

_No `cluster` module or `worker_threads` yet._ The scale model is one process per container plus the split worker deployable.
