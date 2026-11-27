# Data & Caching — Next.js

> **Study time:** ≈ 1 h of reading (7 files, ~9 min average).
> **7 files.** Follow a read from its execution boundary through reuse, mutation, delivery, and deployment constraints.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Data_and_Caching-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | ----------: |
| 01 | [Data Fetching Patterns](10.4.3.01-data-fetching-patterns.md) | Server and client reads, `Promise.allSettled`, preload pattern, React `use()`, and interactive queries | Important | Important | 10 min |
| 02 | [Server Actions](10.4.3.02-server-actions.md) | Mutation validation, authorization, closure encryption keys, `useActionState`, idempotency, and cache refresh | Important | Important | 10 min |
| 03 | [Caching](10.4.3.03-caching.md) | Traditional caches vs. Next.js 16 `'use cache'` (`remote`, `private`), `updateTag`, `revalidateTag`, and `after()` | Important | Important | 10 min |
| 04 | [Streaming](10.4.3.04-streaming.md) | Suspense boundaries, `loading.tsx`, parallel route slot streaming, HTTP commitment, and crawler behavior | Important | Specialized | 6 min |
| 05 | [Incremental Static Regeneration](10.4.3.05-incremental-static-regeneration.md) | Time-based and on-demand ISR, webhook validation, `generateStaticParams`, multi-replica stampedes, and fallback | Important | Specialized | 10 min |
| 06 | [Static Exports](10.4.3.06-static-exports.md) | `output: 'export'`, build-time routes, static GET files, CDN immutable-vs-HTML headers, and host routing | Important | Specialized | 8 min |

---

## Read order

1. **Map dependencies:** Decide which reads are independent, which need identity, and which belong to interactive client state.
2. **Complete the write contract:** Follow validated actions through authoritative data and affected cached reads.
3. **Choose the installed cache model:** Distinguish request deduplication, persistent data and output, and browser navigation reuse before selecting invalidation.
4. **Control delivery:** Trace independent streaming regions, successful and stale ISR output, and the no-runtime export boundary.
5. **Recall, then drill:** Use [Revision](REVISION.md) before the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
