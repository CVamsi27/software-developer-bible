# Data & Caching — Next.js

> **Study time:** ≈ 1 h 49 m of reading (7 files, ~16 min average).
> **7 files.** The hardest part of App Router: data fetching patterns, Server Actions, the four caches, streaming SSR, ISR, and static exports.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Data_and_Caching-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Data Fetching Patterns](10.4.3.01-data-fetching-patterns.md) | Server Component fetch, `unstable_cache`, Server Actions, React Query, Suspense, parallel fetches | Important | Important | 12 min |
| 02 | [Server Actions](10.4.3.02-server-actions.md) | Mutations, revalidation, progressive enhancement, form actions | Important | Important | 26 min |
| 03 | [Caching](10.4.3.03-caching.md) | Data cache, full route cache, revalidation, stale-while-revalidate, cache tags | Important | Important | 8 min |
| 04 | [Streaming](10.4.3.04-streaming.md) | Streaming SSR, Suspense boundaries, loading UI, parallel routes | Important | Specialized | 20 min |
| 05 | [Incremental Static Regeneration](10.4.3.05-incremental-static-regeneration.md) | SWR, on-demand revalidation, cache tags, `generateStaticParams`, fallback | Important | Specialized | 21 min |
| 06 | [Static Exports](10.4.3.06-static-exports.md) | Static export config, `generateStaticParams`, client-side data, deployment | Important | Specialized | 18 min |

---

## Read order

1. **Map dependencies:** Decide which reads are independent, which need identity and which belong to interactive client state.
2. **Complete the write contract:** Follow validated actions through authoritative data and affected cached reads.
3. **Choose the installed cache model:** Distinguish request deduplication, persistent data/output and browser navigation reuse before selecting invalidation.
4. **Control delivery:** Trace independent streaming regions, successful/stale ISR output and the no-runtime export boundary.
5. **Recall, then drill:** Use [Revision](REVISION.md) before the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- |
| React Query data layer | `apps/app/src/providers/react-query-provider.tsx` - QueryClient with `staleTime`/retry defaults |
| Stale-while-revalidate policy | `packages/data-access/src/core/stale-time.ts` - per-key-prefix staleTime + garbage-collection windows |

_No Next data cache / RSC fetch / ISR in docita yet — the above are its client-side caching counterparts._

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
