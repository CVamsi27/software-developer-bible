# Node.js — Index

> **Study time:** ≈ 2 h 3 m of reading (17 files, ~7 min average).
> **17 files** — Event loop internals, streams (Node + Web), buffers, file system, HTTP servers, parallel processing, process management, security, debugging/profiling, Express/Fastify internals, the built-in test runner, and interview questions.

[![Files](https://img.shields.io/badge/files-17-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-success)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Node.js:** Its execution and I/O model underlies NestJS, Express, Fastify and Node-hosted Next.js routes. Follow one operation from scheduling through bytes, resource ownership and framework dispatch; then use the interview bank to explain its failure boundaries.

---

## Topic Categories

The 13 files are organized into 4 categories, each with its own INDEX.

| Category | Files | Why it matters |
| ---------------------------------------------------------------- | ----: | ---------------------------------------------------------------------------------- |
| [Runtime & Async](01-runtime-and-async/INDEX.md) | 2 | The event loop + Web Streams/test runner — every senior interview tests this |
| [I/O & Data](02-io-and-data/INDEX.md) | 4 | Streams, buffers, file system, HTTP — the I/O primitives |
| [Processes & Concurrency](03-processes-and-concurrency/INDEX.md) | 3 | Clustering, child processes/worker threads, lifecycle — production concerns |
| [Security & Operations](04-security-and-operations/INDEX.md) | 4 | Security, diagnostics (debug/profiling), framework internals, full-stack self-test |

---

## Three reading passes

**Pass 1 — Follow one request.** Start with [event-loop execution](01-runtime-and-async/20.1.1.01-event-loop.md), [HTTP ownership](02-io-and-data/20.1.2.04-http-module.md) and [framework dispatch](04-security-and-operations/20.1.4.03-express-fastify-internals.md). Explain what executes now, what waits and who completes the response.

**Pass 2 — Bound bytes and lifetimes.** Follow the [I/O category](02-io-and-data/INDEX.md) through streams, buffers and filesystem handles. Then read [startup/shutdown](03-processes-and-concurrency/20.1.3.03-process-environment.md), task offload and cluster replication. Track which component owns each allocation, connection and pending task.

**Pass 3 — Test the boundaries.** Use [security and diagnostics](04-security-and-operations/INDEX.md) to reject forbidden/oversized work and measure one suspected bottleneck. Each category ends in a separate revision companion; the interview bank is the final explanation drill.

## Runtime & Async

How an isolate schedules JavaScript while native I/O progresses. Category INDEX: [Runtime & Async](01-runtime-and-async/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Event Loop](01-runtime-and-async/20.1.1.01-event-loop.md) | Phases (timers, pending callbacks, idle/prepare, poll, check, close), microtasks vs macrotasks, `setImmediate` vs `nextTick`, blocking vs non-blocking | 6 min |
| 02 | [Web Streams & Test Runner](01-runtime-and-async/20.1.1.02-web-streams-and-test-runner.md) | ReadableStream/WritableStream/TransformStream, `node:test`, mocking, watch mode, TAP output | 8 min |

---

## I/O & Data

The I/O primitives — every backend service uses these. Category INDEX: [I/O & Data](02-io-and-data/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Streams](02-io-and-data/20.1.2.01-streams.md) | Readable, Writable, Transform, Duplex, backpressure, `pipeline()`, error handling | 10 min |
| 02 | [Buffers](02-io-and-data/20.1.2.02-buffers.md) | Buffer creation, encoding (utf8, base64, hex), allocation, TypedArray interop, memory pooling | 9 min |
| 03 | [File System](02-io-and-data/20.1.2.03-file-system.md) | `fs` module, read/write (sync vs async vs stream), file watching, permissions, atomic writes | 8 min |
| 04 | [HTTP Module](02-io-and-data/20.1.2.04-http-module.md) | `createServer`, routing manually, streaming, client requests, reverse proxy, keep-alive | 9 min |

---

## Processes & Concurrency

Production concerns — making Node.js scale and stay healthy. Category INDEX: [Processes & Concurrency](03-processes-and-concurrency/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Clustering](03-processes-and-concurrency/20.1.3.01-clustering.md) | Cluster module, worker processes, IPC, load balancing, PM2, graceful restart | 9 min |
| 02 | [Child Processes & Workers](03-processes-and-concurrency/20.1.3.02-child-processes-workers.md) | `spawn`/`fork`/`exec`, `worker_threads`, SharedArrayBuffer, thread pool, when to use what | 9 min |
| 03 | [Process & Environment](03-processes-and-concurrency/20.1.3.03-process-environment.md) | `process.env`, `argv`, lifecycle, signals (SIGTERM/SIGINT), graceful shutdown, exit codes | 9 min |

---

## Security & Operations

Category INDEX: [Security & Operations](04-security-and-operations/INDEX.md).

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Node.js Security](04-security-and-operations/20.1.4.01-node-security.md) | Input validation, Helmet.js, rate limiting, prototype pollution, dependency vulnerabilities, npm audit | 9 min |
| 02 | [Debugging & Profiling](04-security-and-operations/20.1.4.02-debugging-profiling-nodejs.md) | `--inspect` + Chrome DevTools, `--prof` tick logs, heap snapshot comparison and capture costs, event-loop lag monitoring, SIGUSR2 diagnostics reports | 9 min |
| 03 | [Express & Fastify Internals](04-security-and-operations/20.1.4.03-express-fastify-internals.md) | Middleware chain + arity-4 error handlers, mount paths, Fastify hooks + plugin encapsulation, schema serialization, benchmark caveats, migration notes | 10 min |
| 04 | [Interview Questions](04-security-and-operations/20.1.4.04-interview-questions.md) | 40 curated questions with answers | 10 min |

---

## Revision after each category

- [Runtime & Async revision](01-runtime-and-async/REVISION.md)
- [I/O & Data revision](02-io-and-data/REVISION.md)
- [Processes & Concurrency revision](03-processes-and-concurrency/REVISION.md)
- [Security & Operations revision](04-security-and-operations/REVISION.md)

---

## Cross-References

- [JavaScript Event Loop](../../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.01-event-loop.md) — the JS-level event loop (Node extends this)
- [NestJS](../20.2-nestjs/INDEX.md) — a framework built on the runtime
- [Docker](../../40-platform/40.1-docker/INDEX.md) — how Node.js apps are deployed
- [Security](../20.5-security/INDEX.md) — broader web security

---

## Navigation

[← Previous: Next.js](../../10-frontend/10.4-next.js/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: NestJS →](../20.2-nestjs/INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare platform (NestJS + Prisma + Postgres). Inspect these paths in the current checkout to compare the mechanisms; the pointers alone are not deployment verification:

| Topic | Docita evidence |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Graceful shutdown | `apps/api/src/main.ts` - gracefulShutdown closes the HTTP server + Prisma on SIGTERM/SIGINT; the same pattern runs in `apps/worker/src/main.ts` |
| Process & environment | `apps/api/src/shared/modules/config/app-config.ts` - zod `validateEnv()` fails fast at boot; runtime values served via `app-configuration.service.ts` |
| Async work off the event loop | `apps/api/src/shared/modules/queue/postgres-queue.service.ts` + `queue.worker.module.ts` - inspect enqueue/worker paths and distinguish durable jobs from work still executed by request handlers |
| File I/O & uploads | `apps/api/src/domains/documents/infrastructure/storage.provider.ts` with `r2-storage.provider.ts` / `local-storage.provider.ts` - pluggable storage backend for uploads (R2 vs local disk) |
| Streaming & WebSockets | `apps/api/src/websockets/notifications.gateway.ts` + `payment.websocket.gateway.ts` - async push I/O layered on the API process |
| Clustering & workers | `apps/worker/src/main.ts` - process-level separation (API vs worker deployable) instead of in-process `cluster`/`worker_threads` |
| Raw `node:http` server | No counterpart - docita builds on NestJS/Express; this chapter is the foundation NestJS abstracts away |
