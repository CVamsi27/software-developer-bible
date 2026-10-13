# Routing, HTTP & Metadata — Next.js

> **Study time:** ≈ 40 min of reading (4 files, ~10 min average).
> **4 files.** Follow a request from Proxy's early routing decision through its HTTP handler, then describe the selected page for browsers, sharing platforms and crawlers.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Routing_and_Middleware-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Proxy (formerly Middleware)](10.4.2.01-middleware.md) | Versioned runtime, matchers, redirects, rewrites and authorization boundary | Important | Specialized | 9 min |
| 02 | [Route Handlers](10.4.2.02-route-handlers.md) | API routes, request/response, caching, dynamic vs static | Important | Important | 15 min |
| 03 | [Metadata](10.4.2.03-metadata.md) | Static/dynamic metadata, SEO, Open Graph, robots, sitemaps | Important | Specialized | 13 min |

---

## Read order

1. **Choose a destination before rendering:** Trace redirect, rewrite and continue behavior; name the runtime and trust boundary.
2. **Own the HTTP contract:** Follow params, validation, authorization and response status through a handler. Then examine streaming cancellation and webhook retry boundaries.
3. **Describe the selected document:** Resolve metadata overrides, canonical URLs and structured data without confusing crawl hints with access control.
4. **Recall before interview practice:** Use [Revision](REVISION.md), then the [interview bank](../05-interview-prep/10.4.5.01-interview-questions.md).

---

## Navigation

[← Back to Next.js](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
