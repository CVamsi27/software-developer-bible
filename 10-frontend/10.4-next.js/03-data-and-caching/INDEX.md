# Data & Caching — Next.js

> **6 files.** The hardest part of App Router: data fetching patterns, Server Actions, the four caches, streaming SSR, ISR, and static exports.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Data_and_Caching-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File                                                                            | Topics                                                                                            | Read time |
| --   :  | ------                                                                            | --------                                                                                            | ----------: |
| 01    | [Data Fetching Patterns](10.4.3.01-data-fetching-patterns.md)                   | Server Component fetch, `unstable_cache`, Server Actions, React Query, Suspense, parallel fetches | 30 min    |
| 02    | [Server Actions](10.4.3.02-server-actions.md)                                   | Mutations, revalidation, progressive enhancement, form actions                                    | 25 min    |
| 03    | [Caching](10.4.3.03-caching.md)                                                 | Data cache, full route cache, revalidation, stale-while-revalidate, cache tags                    | 30 min    |
| 04    | [Streaming](10.4.3.04-streaming.md)                                             | Streaming SSR, Suspense boundaries, loading UI, parallel routes                                   | 25 min    |
| 05    | [Incremental Static Regeneration](10.4.3.05-incremental-static-regeneration.md) | SWR, on-demand revalidation, cache tags, `generateStaticParams`, fallback                         | 20 min    |
| 06    | [Static Exports](10.4.3.06-static-exports.md)                                   | Static export config, `generateStaticParams`, client-side data, deployment                        | 20 min    |

---

## Read order

Data Fetching Patterns → Server Actions → Caching → Streaming → ISR → Static Exports.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category        | Docita evidence                                                                                       |
| ------------------------        | -----------------                                                                                       |
| React Query data layer        | `apps/app/src/providers/react-query-provider.tsx` - QueryClient with `staleTime`/retry defaults       |
| Stale-while-revalidate policy | `packages/data-access/src/core/stale-time.ts` - per-key-prefix staleTime + garbage-collection windows |

_No Next data cache / RSC fetch / ISR in docita yet — the above are its client-side caching counterparts._

---

## Navigation

[← Back to Next.js](../INDEX.md)
