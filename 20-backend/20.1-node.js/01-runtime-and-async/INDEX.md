# Runtime & Async - Node.js

> **Study time:** ≈ 19 min of reading (3 files, ~6 min average).
> **3 files.** How Node.js actually runs JavaScript: the libuv event loop, plus the modern Web Streams API and the built-in test runner.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Runtime%20%26%20Async-success)](../INDEX.md)

---

## Reading flow

1. Read the event-loop request trace and predict the CommonJS/I/O scheduling example.
2. Read Web Streams next: follow pressure, cancellation, and split-byte decoding across a full pipeline.
3. Run the small test-runner example, then answer [Revision](REVISION.md) without the sources open.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Event Loop](20.1.1.01-event-loop.md) | Phases (timers, pending callbacks, idle/prepare, poll, check, close), microtasks vs macrotasks, `setImmediate` vs `nextTick`, blocking vs non-blocking | Essential | Foundational | 7 min |
| 02 | [Web Streams & Test Runner](20.1.1.02-web-streams-and-test-runner.md) | Versioned WHATWG stream interfaces, pressure/cancellation, split-byte decoding, Node adapters, `node:test`, mocking, watch mode, TAP output | Important | Important | 10 min |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

The [Docita case study](../../../projects/docita/INDEX.md) provides code pointers to inspect for these mechanisms. Current pool, cancellation and operational behavior requires runtime evidence; the paths do not alone establish production guarantees.

| Topic | Docita evidence |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Event loop & non-blocking I/O | `apps/api/src/prisma/prisma.service.ts` - every DB call is a promise over one shared pg pool; async database waits alone do not block JavaScript; inspect continuation CPU work |
| Timeouts instead of blocked workers | `apps/api/src/shared/common/interceptors/timeout.interceptor.ts` - RxJS timeout bounds observable waiting; it does not preempt CPU work or necessarily cancel the underlying operation |
| Event-loop pressure guards | `apps/api/src/shared/common/extensions/query-budget.extension.ts` - per-request Prisma query budget surfaces N+1 storms early |

Inspect the actual project runtime and runner configuration when using its examples. The chapter's Web Stream and node:test fixtures establish their own versioned contracts independently of a case-study implementation.
---

[Next: I/O & Data →](../02-io-and-data/INDEX.md)
