# Runtime & Async - Node.js

> **Study time:** ≈ 46 min of reading (2 files, ~23 min average).
> **2 files.** How Node.js actually runs JavaScript: the libuv event loop — the most-asked topic in Node interviews — plus the modern Web Streams API and the built-in test runner.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Runtime%20%26%20Async-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Event Loop](20.1.1.01-event-loop.md) | Phases (timers, pending callbacks, idle/prepare, poll, check, close), microtasks vs macrotasks, `setImmediate` vs `nextTick`, blocking vs non-blocking | 32 min |
| 02 | [Web Streams & Test Runner](20.1.1.02-web-streams-and-test-runner.md) | ReadableStream/WritableStream/TransformStream (WHATWG, global in Node 18+), cross-runtime streams, `node:test`, mocking, watch mode, TAP output | 14 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Event loop & non-blocking I/O | `apps/api/src/prisma/prisma.service.ts` - every DB call is a promise over one shared pg pool; nothing blocks the loop |
| Timeouts instead of blocked workers | `apps/api/src/shared/common/interceptors/timeout.interceptor.ts` - rxjs `timeout()` fails hung requests so no route stalls the loop |
| Event-loop pressure guards | `apps/api/src/shared/common/extensions/query-budget.extension.ts` - per-request Prisma query budget surfaces N+1 storms early |

_Web Streams & `node:test`: no direct docita implementation yet._ Streaming lives inside libraries (PDFKit renders to a `Buffer`), and tests run on Jest (`apps/api/jest.config.ts`), not the built-in runner.
---

[Next: I/O & Data →](../02-io-and-data/INDEX.md)
