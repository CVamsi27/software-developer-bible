# Processes & Concurrency - Node.js

> **3 files.** Production concurrency: scaling across cores with the cluster module, offloading CPU-bound work to child processes and worker threads, and controlling the process lifecycle (env vars, signals, graceful shutdown).

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Processes%20%26%20Concurrency-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Clustering](20.1.3.01-clustering.md) | Cluster module, worker processes sharing a server socket, IPC, load balancing, PM2/systemd, graceful restart, one process per container | 25 min |
| 02 | [Child Processes & Workers](20.1.3.02-child-processes-workers.md) | `spawn`/`exec`/`fork`, `worker_threads`, SharedArrayBuffer + Atomics, thread pool, child process vs worker thread decision | 30 min |
| 03 | [Process & Environment](20.1.3.03-process-environment.md) | `process.env`, `argv`, cwd, lifecycle, signals (SIGTERM/SIGINT), graceful shutdown, exit codes, 12-factor config | 20 min |

---

[← Back to Node.js](../INDEX.md)
