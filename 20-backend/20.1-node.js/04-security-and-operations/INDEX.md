# Security & Operations - Node.js

> **Study time:** ≈ 46 min of reading (5 files, ~9 min average).
> **5 files.** Node-specific security hygiene (input validation, headers, rate limiting, dependency scanning, prototype pollution), runtime diagnostics (debugging, profiling, leak hunts), framework internals (Express chain vs Fastify hooks), plus the full-stack interview self-test for the whole runtime.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Security%20%26%20Operations-success)](../INDEX.md)

---

## Reading flow

1. Trace [Node.js Security](20.1.4.01-node-security.md): bytes → validated values → authenticated context → authorized operation → bounded output. Keep each control attached to its boundary.
2. Follow a slow request in [Debugging & Profiling](20.1.4.02-debugging-profiling-nodejs.md), then choose the measurement that tests the suspected wait or resource.
3. Read [Express & Fastify Internals](20.1.4.03-express-fastify-internals.md) to locate each policy in the dispatch/lifecycle and understand its scope.
4. Recall mechanisms with [Revision](REVISION.md), then use [Interview Questions](20.1.4.04-interview-questions.md) for trade-off and failure explanations across the Node stack.

## Chapter map

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Node.js Security](20.1.4.01-node-security.md) | Explicit query/configuration shapes, subprocess arguments, SSRF/path boundaries, Helmet/browser policy, bounded work, dependency authority | Essential | Foundational | 10 min |
| 02 | [Debugging & Profiling](20.1.4.02-debugging-profiling-nodejs.md) | `node --inspect` + Chrome DevTools, `--prof` tick logs, heap snapshots + comparison for leaks, built-in CPU capture, Clinic maintenance limits, event-loop lag monitoring, diagnostics reports without restarts | Essential | Foundational | 10 min |
| 03 | [Express & Fastify Internals](20.1.4.03-express-fastify-internals.md) | Middleware chain model, arity-4 error handlers, mount paths, Fastify hook lifecycle, plugin encapsulation, schema-based serialization, benchmark caveats, migration notes | Essential | Foundational | 13 min |
| 04 | [Interview Questions](20.1.4.04-interview-questions.md) | 40 curated questions covering event loop, streams, buffers, clustering, child processes, security; practice mechanism, trade-off and failure follow-ups | Essential | Foundational | 11 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare platform (NestJS + Prisma + Postgres). These paths are reading pointers; inspect the current checkout and deployment before treating them as verified behavior:

| Topic | Docita evidence |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Input validation at the boundary | `apps/api/src/shared/common/pipes/zod-validation.pipe.ts` - inspect which controllers use these boundary schemas |
| Security headers & edge hygiene | `apps/api/src/main.ts` - helmet() CSP headers, CORS allow-list, Sentry wired before first request |
| Express middleware chain | `apps/api/src/app.module.ts` - inspect guard/interceptor registration and Nest lifecycle; this differs from Express middleware dispatch |
| Runtime observability | `apps/api/src/shared/common/interceptors/request-logging.interceptor.ts` - structured request logs beside slow-query logging |
| Rate limiting | `apps/api/src/shared/common/interceptors/rate-limit.interceptor.ts` - cache-backed per-route limits next to IP/user guards |

_Compare the current checkout for diagnostics tooling: these pointers do not establish inspector/snapshot deployment policy or the current observability providers._
---

[← Previous: Processes & Concurrency](../03-processes-and-concurrency/INDEX.md)
