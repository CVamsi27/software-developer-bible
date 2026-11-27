# Async & Concurrency — JavaScript

> **Study time:** ≈ 1 h 12 m of reading (7 files, ~10 min average).
> **7 files.** Trace how host scheduling runs promise work, how failures travel, when cancellation stops supported work, and how a pool limits task starts and buffered results.

[![Files](https://img.shields.io/badge/files-7-blue)](#chapters)
[![Category](https://img.shields.io/badge/category-Async_and_Concurrency-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Chapters

The Files badge counts these 6 chapters plus the revision companion.

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Event Loop](10.1.3.01-event-loop.md) | Synchronous tasks, microtask checkpoints, `MessageChannel` yielding, browser rendering, and Node host loop | Essential | Foundational | 10 min |
| 02 | [Promises](10.1.3.02-promises.md) | Promise states, `[[PromiseIsHandled]]`, chaining, `Promise.withResolvers` and `Promise.try`, combinators, and deduplication | Essential | Foundational | 11 min |
| 03 | [Async/Await](10.1.3.03-async-await.md) | Async suspension, `forEach(async)` pitfalls, Top-Level `await`, error boundaries, and payload validation | Essential | Foundational | 13 min |
| 04 | [Error Handling](10.1.3.04-error-handling.md) | `try`, `catch`, and `finally`, `Error.isError`, `AggregateError`, `Error.cause`, JSON serialization, and retry boundaries | Essential | Foundational | 12 min |
| 05 | [Aborting & Cancellation](10.1.3.05-abort-and-cancellation.md) | `AbortController` and `AbortSignal`, `AbortSignal.abort`, `{ signal }` teardown, stale-request guards, and limits | Essential | Foundational | 9 min |
| 06 | [Bounded Concurrency & Promise Pools](10.1.3.06-bounded-concurrency.md) | Start limits, fail-fast abort propagation or collect-all outcomes, cancellation, ordered results, and backpressure | Essential | Foundational | 10 min |

---

## Read order

Read Event Loop → Promises → Async/Await to separate scheduling, outcomes and suspension. Then follow Error Handling → Aborting & Cancellation → Bounded Concurrency: deciding who owns failure comes before stopping work or limiting starts. Use the revision companion after tracing a pool where one mapper fails while another is still active.

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic in this category | Docita evidence |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Promises & concurrency limits | `packages/utils/src/async/map-with-concurrency.ts` - bounded async worker pool resolved via `Promise.all` |
| `async` and `await` + timers polling | `apps/app/src/hooks/use-phone-signature-polling.ts` - awaited status checks driving an interval-based poll loop |
| Error handling for async failures | `packages/utils/src/errors/network-error.ts` - `instanceof Error` narrowing to classify fetch and network failures |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
