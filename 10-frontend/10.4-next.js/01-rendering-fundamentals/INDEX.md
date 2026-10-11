# Rendering Fundamentals — Next.js

> **Study time:** ≈ 1 h 38 m of reading (5 files, ~20 min average).
> **5 files.** Choose where data is read, when output is cached, and where browser code begins; then trace App Router boundaries, Server Components, Client Components, and Next.js 16 Cache Components.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Rendering_Fundamentals-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [SSR / CSR / SSG / ISR](10.4.1.01-ssr-csr-ssg-isr.md) | Rendering strategies comparison, when to use each, hydration, streaming | Important | Specialized | 24 min |
| 02 | [App Router](10.4.1.02-app-router.md) | Layouts, nested routes, loading states, error handling, route groups | Important | Important | 24 min |
| 03 | [Server Components](10.4.1.03-server-components.md) | RSC payload, server rendering, serialization, authorized data access | Important | Important | 20 min |
| 04 | [Client Components](10.4.1.04-client-components.md) | `'use client'`, interleaving, client boundaries, "use client" placement | Important | Specialized | 27 min |

---

## Read order

1. **Decide when content is available:** Compare build, request and browser rendering; separate freshness from where interaction runs.
2. **Give navigation shared owners:** Trace a dashboard layout, page replacement and loading/error scope in App Router.
3. **Follow the execution boundary:** Trace a database result through a Server Component into a hydrated client control. Explain what is serialized and what code ships.
4. **Check recall, then practice:** Use [Revision](REVISION.md) before the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
