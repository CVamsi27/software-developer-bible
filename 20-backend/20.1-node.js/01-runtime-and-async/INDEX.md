# Runtime & Async - Node.js

> **Study time:** ≈ 16 min of reading (3 files, ~5 min average).
> **3 files.** How Node.js actually runs JavaScript: the libuv event loop — the most-asked topic in Node interviews — plus the modern Web Streams API and the built-in test runner.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Runtime%20%26%20Async-success)](../INDEX.md)

---

## Reading flow

1. Read the event-loop request trace and predict the CommonJS/I/O scheduling example.
2. Read Web Streams next: follow pressure, cancellation, and split-byte decoding across a full pipeline.
3. Run the small test-runner example, then answer [Revision](REVISION.md) without the sources open.

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Event Loop](20.1.1.01-event-loop.md) | Phases (timers, pending callbacks, idle/prepare, poll, check, close), microtasks vs macrotasks, `setImmediate` vs `nextTick`, blocking vs non-blocking | 6 min |
| 02 | [Web Streams & Test Runner](20.1.1.02-web-streams-and-test-runner.md) | ReadableStream/WritableStream/TransformStream (WHATWG, global in Node 18+), cross-runtime streams, `node:test`, mocking, watch mode, TAP output | 8 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Event loop & non-blocking I/O | `apps/api/src/prisma/prisma.service.ts` - every DB call is a promise over one shared pg pool; async database waits alone do not block JavaScript; inspect continuation CPU work |
| Timeouts instead of blocked workers | `apps/api/src/shared/common/interceptors/timeout.interceptor.ts` - RxJS timeout bounds observable waiting; it does not preempt CPU work or necessarily cancel the underlying operation |
| Event-loop pressure guards | `apps/api/src/shared/common/extensions/query-budget.extension.ts` - per-request Prisma query budget surfaces N+1 storms early |

_Web Streams & `node:test`: no direct docita implementation yet._ Streaming lives inside libraries (PDFKit renders to a `Buffer`), and tests run on Jest (`apps/api/jest.config.ts`), not the built-in runner.
---

[Next: I/O & Data →](../02-io-and-data/INDEX.md)
