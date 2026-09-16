# Next.js — Index

> **Study time:** ≈ 7 h 16 m of reading (17 files, ~26 min average).
> **17 files** — App Router, rendering strategies, server components, data fetching patterns, caching, streaming, ISR, authentication, static exports, deployment (Docker/Vercel/self-hosted), and interview questions.

[![Files](https://img.shields.io/badge/files-17-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Next.js:** The de-facto React framework. Mid-stage startups, FAANG, and most product companies use it. Senior interviews test App Router architecture, RSC vs Client Components, caching strategy, and Server Actions. This section is the canonical reference.

---

## Topic Categories

The 17 files are organized into 5 category folders — read in order.

| Category | Files | Why it matters |
| ------------------------------------------------------------ | ----: | --------------------------------------------------------------------- |
| [Rendering Fundamentals](01-rendering-fundamentals/INDEX.md) | 4 | The mental model — when to use SSR, CSR, SSG, RSC |
| [Routing & Middleware](02-routing-and-middleware/INDEX.md) | 3 | Edge middleware, route handlers, metadata/SEO tags |
| [Data & Caching](03-data-and-caching/INDEX.md) | 6 | The hardest part of Next.js — server actions, caching, streaming, ISR |
| [Production](04-production/INDEX.md) | 3 | Authentication, image optimization, deployment |
| [Interview Prep](05-interview-prep/INDEX.md) | 1 | 60+ interview Qs |

---

## Study Flow

Read categories in numeric order — each builds on the previous:

```text
01-rendering-fundamentals ─▶ 02-routing-and-middleware ─▶ 03-data-and-caching
    ─▶ 04-production ─▶ 05-interview-prep
```

---

## Rendering Fundamentals

The mental model for choosing the right rendering strategy.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [SSR / CSR / SSG / ISR](01-rendering-fundamentals/10.4.1.01-ssr-csr-ssg-isr.md) | Rendering strategies comparison, when to use each, hydration, streaming | 25 min |
| 02 | [App Router](01-rendering-fundamentals/10.4.1.02-app-router.md) | Layouts, nested routes, loading states, error handling, route groups | 24 min |
| 03 | [Server Components](01-rendering-fundamentals/10.4.1.03-server-components.md) | RSC architecture, server rendering, serialization, "use server" | 26 min |
| 04 | [Client Components](01-rendering-fundamentals/10.4.1.04-client-components.md) | `'use client'`, interleaving, client boundaries, "use client" placement | 33 min |

---

## Routing & Middleware

The request pipeline — every Next.js interview tests this.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 05 | [Middleware](02-routing-and-middleware/10.4.2.01-middleware.md) | Edge middleware, matchers, redirects, rewrite, auth gating | 27 min |
| 06 | [Route Handlers](02-routing-and-middleware/10.4.2.02-route-handlers.md) | API routes, request/response, caching, dynamic vs static | 26 min |
| 07 | [Metadata](02-routing-and-middleware/10.4.2.03-metadata.md) | Static/dynamic metadata, SEO, Open Graph, robots, sitemaps | 26 min |

---

## Data & Caching

The hardest part of Next.js — the 6 files every senior engineer must own.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 08 | [Data Fetching Patterns](03-data-and-caching/10.4.3.01-data-fetching-patterns.md) | Server Component fetch, `unstable_cache`, Server Actions, React Query, Suspense, parallel fetches | 14 min |
| 09 | [Server Actions](03-data-and-caching/10.4.3.02-server-actions.md) | Mutations, revalidation, progressive enhancement, form actions | 28 min |
| 10 | [Caching](03-data-and-caching/10.4.3.03-caching.md) | Data cache, full route cache, revalidation, stale-while-revalidate, cache tags | 25 min |
| 11 | [Streaming](03-data-and-caching/10.4.3.04-streaming.md) | Streaming SSR, Suspense boundaries, loading UI, parallel routes | 28 min |
| 12 | [Incremental Static Regeneration](03-data-and-caching/10.4.3.05-incremental-static-regeneration.md) | SWR, on-demand revalidation, cache tags, `generateStaticParams`, fallback | 26 min |
| 13 | [Static Exports](03-data-and-caching/10.4.3.06-static-exports.md) | Static export config, `generateStaticParams`, client-side data, deployment | 18 min |

---

## Production

Production concerns.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 14 | [Authentication](04-production/10.4.4.01-authentication.md) | Auth middleware, JWT, server/client auth flow, NextAuth.js, RBAC | 30 min |
| 15 | [Image Optimization](04-production/10.4.4.02-image-optimization.md) | `next/image`, lazy loading, responsive images, AVIF/WebP | 24 min |
| 16 | [Deploying Next.js](04-production/10.4.4.03-deploying-nextjs.md) | output standalone + multi-stage Dockerfile, Vercel vs self-hosted, edge limits, ISR cacheHandler, multi-zone, env build-vs-runtime, observability | 15 min |

---

## Interview Prep

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 17 | [Interview Questions](05-interview-prep/10.4.5.01-interview-questions.md) | 60+ curated questions with answers | 41 min |

---

## Suggested Study Order

### Path A — Coming from Pages Router (3-5 days)
1. Rendering Fundamentals (4 files, ~2 hrs)
2. Middleware + Route Handlers + Metadata (1 hr)
3. Data & Caching — the core of App Router (2.5-3 hrs)
4. Auth + Image Optimization + Deployment (1.25 hrs)
5. Interview Questions (3-4 hrs)

### Path B — Already know App Router, prepping for senior (1-2 days)
1. Caching deep-dive (1 hr)
2. Server Actions + Data Fetching Patterns (1 hr)
3. Streaming + ISR (45 min)
4. Interview Questions (focus on RSC, caching, streaming)

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- Re-read Caching + Server Components
- Run through 60+ Interview Questions

---

## Cross-References

- [React](../10.3-react/INDEX.md) — Next.js builds on React; React Server Components are a Next.js feature
- [Serverless & Edge](../../40-platform/40.7-serverless-edge/INDEX.md) — Next.js middleware runs on the Edge
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring Next.js performance
- [Auth & Security](../../20-backend/20.5-security/INDEX.md) — auth patterns

---

## Navigation

[← Previous: React](../10.3-react/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Form Handling →](../10.5-form-handling/INDEX.md)
