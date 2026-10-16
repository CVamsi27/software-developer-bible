# Async & Concurrency — JavaScript

> **Study time:** ≈ 59 min of reading (7 files, ~8 min average).
> **7 files.** Trace how host scheduling runs promise work, how failures travel, when cancellation stops supported work, and how a pool limits task starts and buffered results.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Async_and_Concurrency-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Event Loop](10.1.3.01-event-loop.md) | Synchronous tasks, microtask checkpoints, browser rendering, Node host loop | Essential | Foundational | 9 min |
| 02 | [Promises](10.1.3.02-promises.md) | Promise states, chaining, error handling, `Promise.all`/`race`/`allSettled`/`any` | Essential | Foundational | 9 min |
| 03 | [Async/Await](10.1.3.03-async-await.md) | Async functions, error handling, concurrency, sequential vs parallel, top-level await | Essential | Foundational | 11 min |
| 04 | [Error Handling](10.1.3.04-error-handling.md) | try/catch/finally, custom errors, error propagation, async error handling, unhandled rejections | Essential | Foundational | 9 min |
| 05 | [Aborting & Cancellation](10.1.3.05-abort-and-cancellation.md) | AbortController/AbortSignal, stale-request races, `AbortSignal.timeout`/`any`, listener cleanup, cooperative cancellation | Essential | Foundational | 8 min |
| 06 | [Bounded Concurrency & Promise Pools](10.1.3.06-bounded-concurrency.md) | Start limits, fail-fast or collect-all outcomes, cancellation, ordered results and backpressure | Essential | Foundational | 7 min |

---

## Read order

Read Event Loop → Promises → Async/Await to separate scheduling, outcomes and suspension. Then follow Error Handling → Aborting & Cancellation → Bounded Concurrency: deciding who owns failure comes before stopping work or limiting starts. Use the revision companion after tracing a pool where one mapper fails while another is still active.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Promises & concurrency limits | `packages/utils/src/async/map-with-concurrency.ts` - bounded async worker pool resolved via `Promise.all` |
| Async/await + timers polling | `apps/app/src/hooks/use-phone-signature-polling.ts` - awaited status checks driving an interval-based poll loop |
| Error handling for async failures | `packages/utils/src/errors/network-error.ts` - `instanceof Error` narrowing to classify fetch/network failures |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
