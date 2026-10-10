# Routing & Middleware — Next.js

> **Study time:** ≈ 1 h 8 m of reading (4 files, ~17 min average).
> **4 files.** The request pipeline: version-scoped middleware/Proxy interception, Route Handlers as the API surface, and the Metadata API for SEO tags.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Routing_and_Middleware-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Middleware](10.4.2.01-middleware.md) | Middleware/Proxy runtimes, matchers, redirects, rewrite, auth gating | Important | Specialized | 20 min |
| 02 | [Route Handlers](10.4.2.02-route-handlers.md) | API routes, request/response, caching, dynamic vs static | Important | Important | 22 min |
| 03 | [Metadata](10.4.2.03-metadata.md) | Static/dynamic metadata, SEO, Open Graph, robots, sitemaps | Important | Specialized | 23 min |

---

## Read order

1. **Choose a destination before rendering:** Trace redirect, rewrite and continue behavior; name the runtime and trust boundary.
2. **Own the HTTP contract:** Follow params, validation, authorization and response status through a handler. Then examine streaming cancellation and webhook retry boundaries.
3. **Describe the selected document:** Resolve metadata overrides, canonical URLs and structured data without confusing crawl hints with access control.
4. **Recall before interview practice:** Use [Revision](REVISION.md), then the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

_No direct docita implementation yet._ (Docita has no Next.js layer — its routing is react-router inside a Vite SPA and NestJS controllers on the API.)

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
