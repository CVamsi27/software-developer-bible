# Rendering Fundamentals — Next.js

> **Study time:** ≈ 47 min of reading (5 files, ~9 min average).
> **5 files.** Decide when output is produced and reused, then follow one route from its URL and server data to the small client controls that need hydration.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Rendering_Fundamentals-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [SSR / CSR / SSG / ISR](10.4.1.01-ssr-csr-ssg-isr.md) | Separate execution location, output timing and cache policy; distinguish hydration from CSR | Important | Specialized | 10 min |
| 02 | [App Router](10.4.1.02-app-router.md) | Map URL segments to pages, persistent layouts, and loading or failure boundaries | Important | Important | 12 min |
| 03 | [Server Components](10.4.1.03-server-components.md) | Trace authorized server reads into the RSC payload and safe client props | Important | Important | 9 min |
| 04 | [Client Components](10.4.1.04-client-components.md) | Start hydration at interaction, keep browser dependencies narrow, and validate writes on the server | Important | Specialized | 12 min |

---

## Read order

1. **Choose output timing and reuse:** Compare build, request and browser work, then set a freshness contract separately.
2. **Give the route an owner:** Follow a dashboard URL through its layout, page, pending state and error boundary.
3. **Trace one product result:** See what the server reads, what the RSC payload sends, and where browser state begins.
4. **Check recall, then practice:** Use [Revision](REVISION.md) before the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
