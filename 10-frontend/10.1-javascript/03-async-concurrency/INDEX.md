# Async & Concurrency — JavaScript

> **Study time:** ≈ 1 h 3 m of reading (7 files, ~9 min average).
> **7 files.** The most-asked topic in senior JS interviews: the event loop, promises, async/await, error propagation across asynchronous boundaries, and cancellation with AbortSignal.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Async_and_Concurrency-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Event Loop](10.1.3.01-event-loop.md) | Microtasks vs macrotasks, callback queue, rendering pipeline, `requestAnimationFrame` | 6 min |
| 02 | [Promises](10.1.3.02-promises.md) | Promise states, chaining, error handling, `Promise.all`/`race`/`allSettled`/`any` | 8 min |
| 03 | [Async/Await](10.1.3.03-async-await.md) | Async functions, error handling, concurrency, sequential vs parallel, top-level await | 7 min |
| 04 | [Error Handling](10.1.3.04-error-handling.md) | try/catch/finally, custom errors, error propagation, async error handling, unhandled rejections | 17 min |
| 05 | [Aborting & Cancellation](10.1.3.05-abort-and-cancellation.md) | AbortController/AbortSignal, stale-request races, `AbortSignal.timeout`/`any`, listener cleanup, cooperative cancellation | 7 min |
| 06 | [Bounded Concurrency & Promise Pools](10.1.3.06-bounded-concurrency.md) | Worker-pool pattern, fail-fast vs allSettled policies, AbortSignal threading, `p-limit` in production | 12 min |

---

## Read order

Event Loop → Promises → Async/Await → Error Handling → Aborting & Cancellation. This is the most-asked cluster in interviews.

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
