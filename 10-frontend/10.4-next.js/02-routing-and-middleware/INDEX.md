# Routing, HTTP & Metadata — Next.js

> **Study time:** ≈ 44 min of reading (4 files, ~11 min average).
> **4 files.** Follow a request from Proxy's early routing decision through its HTTP handler, then describe the selected page for browsers, sharing platforms, and crawlers.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Routing_and_Middleware-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------ | ----------: |
| 01 | [Proxy (formerly Middleware)](10.4.2.01-middleware.md) | Next.js 16 Node Proxy, matchers and prefetch skipping, rewrites, header stripping, CSP nonces, and authorization boundaries | Important | Specialized | 10 min |
| 02 | [Route Handlers](10.4.2.02-route-handlers.md) | HTTP methods, validation, SSE abort handling, webhooks and `after()`, uploads, Cache Components, and CORS | Important | Important | 16 min |
| 03 | [Metadata](10.4.2.03-metadata.md) | Static and dynamic metadata, `React.cache()` deduplication, JSON-LD escaping, `next/og` images, robots, and sitemaps | Important | Specialized | 14 min |

---

## Read order

1. **Choose a destination before rendering:** Trace redirect, rewrite, and continue behavior; name the runtime and trust boundary.
2. **Own the HTTP contract:** Follow `params`, validation, authorization, and response status through a handler. Then examine streaming cancellation and webhook retry boundaries.
3. **Describe the selected document:** Resolve metadata overrides, canonical URLs, and structured data without confusing crawl hints with access control.
4. **Recall before interview practice:** Use [Revision](REVISION.md), then the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
