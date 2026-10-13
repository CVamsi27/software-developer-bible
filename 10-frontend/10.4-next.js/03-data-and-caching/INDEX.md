# Data & Caching — Next.js

> **Study time:** ≈ 56 min of reading (7 files, ~8 min average).
> **7 files.** Follow a read from its execution boundary through reuse, mutation, delivery and deployment constraints.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Data_and_Caching-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Data Fetching Patterns](10.4.3.01-data-fetching-patterns.md) | Server and client reads, dependencies, request reuse, React `use()`, interactive queries | Important | Important | 9 min |
| 02 | [Server Actions](10.4.3.02-server-actions.md) | Mutation validation, authorization, form state, idempotency, and cache refresh | Important | Important | 9 min |
| 03 | [Caching](10.4.3.03-caching.md) | Data cache, full route cache, revalidation, stale-while-revalidate, cache tags | Important | Important | 9 min |
| 04 | [Streaming](10.4.3.04-streaming.md) | Suspense boundaries, useful fallbacks, HTTP commitment, crawler and host behavior | Important | Specialized | 6 min |
| 05 | [Incremental Static Regeneration](10.4.3.05-incremental-static-regeneration.md) | SWR, on-demand revalidation, cache tags, `generateStaticParams`, fallback | Important | Specialized | 10 min |
| 06 | [Static Exports](10.4.3.06-static-exports.md) | `output: 'export'`, build-time routes, static GET files, host routing | Important | Specialized | 8 min |

---

## Read order

1. **Map dependencies:** Decide which reads are independent, which need identity and which belong to interactive client state.
2. **Complete the write contract:** Follow validated actions through authoritative data and affected cached reads.
3. **Choose the installed cache model:** Distinguish request deduplication, persistent data/output and browser navigation reuse before selecting invalidation.
4. **Control delivery:** Trace independent streaming regions, successful/stale ISR output and the no-runtime export boundary.
5. **Recall, then drill:** Use [Revision](REVISION.md) before the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
