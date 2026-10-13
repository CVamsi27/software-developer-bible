# Next.js — Index

> **Study time:** ≈ 4 h 8 m of reading (21 files, ~12 min average).
> **21 files** — App Router, rendering strategies, server components, data fetching patterns, caching, streaming, ISR, authentication, static exports, deployment (Docker/Vercel/self-hosted), and interview questions.

[![Files](https://img.shields.io/badge/files-21-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Next.js:** A React framework that integrates routing, server rendering and deployment conventions. This section follows the concepts in dependency order and points to the contract that applies to each router and cache model.

---

## Topic Categories

The 17 files are organized into 5 category folders — read in order.

| Category | Files | Why it matters |
| -------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------ |
| [Rendering Fundamentals](01-rendering-fundamentals/INDEX.md) | 4 | Request rendering, reusable output, streaming, and server/client boundaries |
| [Routing, HTTP & Metadata](02-routing-and-middleware/INDEX.md) | 3 | Next.js 16 Proxy, Route Handlers, and page metadata |
| [Data & Caching](03-data-and-caching/INDEX.md) | 6 | Data access, mutations, two cache models, streaming, regeneration, and static export |
| [Production](04-production/INDEX.md) | 3 | Authentication, image optimization, deployment |
| [Interview Prep](05-interview-prep/INDEX.md) | 1 | 40 interview questions |

---

## Study Flow

Read categories in numeric order — each builds on the previous. After each learning category, complete its separate revision companion before continuing to the interview bank:

```text
01-rendering-fundamentals ─▶ 02-routing-and-middleware ─▶ 03-data-and-caching
    ─▶ 04-production ─▶ 05-interview-prep
```

---

## Rendering Fundamentals

The mental model for choosing the right rendering strategy.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [SSR / CSR / SSG / ISR](01-rendering-fundamentals/10.4.1.01-ssr-csr-ssg-isr.md) | Rendering strategies comparison, when to use each, hydration, streaming | Important | Specialized | 10 min |
| 02 | [App Router](01-rendering-fundamentals/10.4.1.02-app-router.md) | URL segments, persistent layouts, navigation, and fallback boundaries | Important | Important | 12 min |
| 03 | [Server Components](01-rendering-fundamentals/10.4.1.03-server-components.md) | Authorized server reads, RSC payload, serialization, and streaming | Important | Important | 10 min |
| 04 | [Client Components](01-rendering-fundamentals/10.4.1.04-client-components.md) | Hydration, browser state, client module boundaries, and server-validated writes | Important | Specialized | 12 min |

---

## Routing and Request Boundaries

Trace how a URL reaches a page or handler, then place request-specific policy at the right boundary.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Proxy and Middleware](02-routing-and-middleware/10.4.2.01-middleware.md) | Next.js 16 Proxy, earlier Middleware, matchers, redirects, rewrites, early routing versus authorization | Important | Specialized | 9 min |
| 06 | [Route Handlers](02-routing-and-middleware/10.4.2.02-route-handlers.md) | API routes, request/response, caching, dynamic vs static | Important | Important | 15 min |
| 07 | [Metadata](02-routing-and-middleware/10.4.2.03-metadata.md) | Static/dynamic metadata, SEO, Open Graph, robots, sitemaps | Important | Specialized | 13 min |

---

## Data and Caching

Six chapters explain data access, mutations, reuse, streaming, regeneration and the static-output boundary.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 08 | [Data Fetching Patterns](03-data-and-caching/10.4.3.01-data-fetching-patterns.md) | Server Component data, request deduplication, external query caches, Suspense, and parallel work | Important | Important | 10 min |
| 09 | [Server Actions](03-data-and-caching/10.4.3.02-server-actions.md) | Mutations, revalidation, progressive enhancement, form actions | Important | Important | 10 min |
| 10 | [Caching](03-data-and-caching/10.4.3.03-caching.md) | Previous App Router cache model, Next.js 16 Cache Components, freshness, tags, and invalidation | Important | Important | 9 min |
| 11 | [Streaming](03-data-and-caching/10.4.3.04-streaming.md) | Streaming SSR, Suspense boundaries, loading UI, parallel routes | Important | Specialized | 7 min |
| 12 | [Incremental Static Regeneration](03-data-and-caching/10.4.3.05-incremental-static-regeneration.md) | SWR, on-demand revalidation, cache tags, `generateStaticParams`, fallback | Important | Specialized | 10 min |
| 13 | [Static Exports](03-data-and-caching/10.4.3.06-static-exports.md) | Static export config, `generateStaticParams`, client-side data, deployment | Important | Specialized | 9 min |

---

## Production

Protect current identity/resource boundaries, deliver appropriate image variants and operate a compatible runtime artifact.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 14 | [Authentication](04-production/10.4.4.01-authentication.md) | Proxy redirects, session verification, data-boundary authorization, CSRF, NextAuth.js v4 | Important | Important | 32 min |
| 15 | [Image Optimization](04-production/10.4.4.02-image-optimization.md) | `next/image`, lazy loading, responsive images, AVIF/WebP | Important | Specialized | 18 min |
| 16 | [Deploying Next.js](04-production/10.4.4.03-deploying-nextjs.md) | Standalone output, managed vs self-hosted, Edge limits, cacheHandler vs cacheHandlers, replica coordination, rolling releases, multi-zone, runtime configuration, observability | Important | Specialized | 17 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 17 | [Interview Questions](05-interview-prep/10.4.5.01-interview-questions.md) | 40 questions with answers | Important | Specialized | 31 min |

---

## Suggested Study Order

### Path A — Coming from Pages Router (3-5 days)
1. Rendering Fundamentals (4 files, ~2 hrs)
2. Proxy (and Middleware migration) + Route Handlers + Metadata (about 1 hr)
3. Data and Caching — compare the previous model with Cache Components (2.5-3 hrs)
4. Auth + Image Optimization + Deployment (1.25 hrs)
5. Interview Questions (about 30 min to read; allow longer to answer aloud and trace each failure case)

### Path B — Already know App Router, prepping for senior (1-2 days)
1. Caching deep-dive (1 hr)
2. Server Actions + Data Fetching Patterns (1 hr)
3. Streaming + ISR (45 min)
4. Interview Questions (focus on RSC, caching, streaming)

### Path C — Interview tomorrow
- Review each chapter’s definition, example and summary; focus on the topics listed above
- Re-read Caching + Server Components
- Run through the 40 Interview Questions

---

## Cross-References

- [React](../10.3-react/INDEX.md) — Next.js builds on React; Next.js integrates React Server Components with its router
- [Serverless & Edge](../../40-platform/40.7-serverless-edge/INDEX.md) — middleware/Proxy runtime choices depend on framework version and host
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring Next.js performance
- [Auth & Security](../../20-backend/20.5-security/INDEX.md) — auth patterns

---

## Navigation

[← Previous: React](../10.3-react/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Form Handling →](../10.5-form-handling/INDEX.md)
