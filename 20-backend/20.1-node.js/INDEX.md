# Node.js — Index

> **11 files** — Event loop internals, streams (Node + Web), buffers, file system, HTTP servers, parallel processing, process management, security, the built-in test runner, and interview questions.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-success)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Node.js:** The runtime for most modern full-stack apps. Every senior backend interview tests Node.js fundamentals — event loop, streams, async patterns, clustering, process management, and security. NestJS, Express, Fastify, Next.js (server side) all run on Node.

---

## Topic Categories

The 11 files are organized into 4 conceptual categories.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Runtime & Async](#runtime--async) | 2 | The Node.js event loop — every senior interview tests this |
| [I/O & Data Handling](#io--data-handling) | 4 | Streams, buffers, file system, HTTP — the I/O primitives |
| [Process & Concurrency](#process--concurrency) | 3 | Clustering, child processes, lifecycle — production concerns |
| [Security & Testing](#security--testing) | 2 | Node-specific security, the built-in test runner |

---

## Runtime & Async

How Node.js actually runs JavaScript. The event loop is the most-asked topic in Node interviews.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Event Loop](01-runtime-and-async/20.1.1.01-event-loop.md) | Phases (timers, I/O callbacks, poll, check, close), microtasks vs macrotasks, `setImmediate` vs `nextTick`, blocking vs non-blocking | 30 min |
| 11 | [Web Streams & Test Runner](01-runtime-and-async/20.1.1.02-web-streams-and-test-runner.md) | ReadableStream/WritableStream/TransformStream, `node:test`, mocking, watch mode, TAP output | 30 min |

---

## I/O & Data Handling

The I/O primitives — every backend service uses these.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [Streams](02-io-and-data/20.1.2.01-streams.md) | Readable, Writable, Transform, Duplex, backpressure, `pipeline()`, error handling | 30 min |
| 03 | [Buffers](02-io-and-data/20.1.2.02-buffers.md) | Buffer creation, encoding (utf8, base64, hex), allocation, TypedArray interop, memory pooling | 20 min |
| 05 | [File System](02-io-and-data/20.1.2.03-file-system.md) | `fs` module, read/write (sync vs async vs stream), file watching, permissions, atomic writes | 25 min |
| 06 | [HTTP Module](02-io-and-data/20.1.2.04-http-module.md) | `createServer`, routing manually, streaming, client requests, reverse proxy, keep-alive | 30 min |

---

## Process & Concurrency

Production concerns — making Node.js scale and stay healthy.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Clustering](03-processes-and-concurrency/20.1.3.01-clustering.md) | Cluster module, worker processes, IPC, load balancing, PM2, graceful restart | 25 min |
| 07 | [Child Processes & Workers](03-processes-and-concurrency/20.1.3.02-child-processes-workers.md) | `spawn`/`fork`/`exec`, `worker_threads`, SharedArrayBuffer, thread pool, when to use what | 30 min |
| 08 | [Process & Environment](03-processes-and-concurrency/20.1.3.03-process-environment.md) | `process.env`, `argv`, lifecycle, signals (SIGTERM/SIGINT), graceful shutdown, exit codes | 20 min |

---

## Security & Testing

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 09 | [Node.js Security](04-security-and-operations/20.1.4.01-node-security.md) | Input validation, Helmet.js, rate limiting, prototype pollution, dependency vulnerabilities, npm audit | 25 min |
| 10 | [Interview Questions](04-security-and-operations/20.1.4.04-interview-questions.md) | 50+ curated questions with answers | 3 hrs |

---

## Suggested Study Order

1. **Event Loop** — must know, asked in every loop
2. **Streams** — production I/O, asked at senior level
3. **Buffers** — file/network I/O
4. **HTTP Module** — what Express sits on top of
5. **Clustering + Child Processes** — production scale
6. **Process & Environment** — lifecycle, signals
7. **File System** — I/O operations
8. **Security + Test Runner** — quality & safety
9. **Interview Questions** — final review

---

## Cross-References

- [JavaScript Event Loop](../../10-frontend/10.1-javascript/03-async-concurrency/10.1.3.01-event-loop.md) — the JS-level event loop (Node extends this)
- [NestJS](../20.2-nestjs/INDEX.md) — the most common Node.js framework
- [Docker](../../40-platform/40.1-docker/INDEX.md) — how Node.js apps are deployed
- [Security](../20.5-security/INDEX.md) — broader web security

---

## Navigation

[← Previous: Next.js](../../10-frontend/10.4-next.js/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: NestJS →](../20.2-nestjs/INDEX.md)
