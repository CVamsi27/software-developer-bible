# Next.js — Index

> **16 files** — App Router, rendering strategies, server components, data fetching patterns, caching, streaming, ISR, authentication, static exports, and interview questions.

[![Files](https://img.shields.io/badge/files-16-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Next.js:** The de-facto React framework. Mid-stage startups, FAANG, and most product companies use it. Senior interviews test App Router architecture, RSC vs Client Components, caching strategy, and Server Actions. This section is the canonical reference.

---

## Topic Categories

The 16 files are organized into 5 categories — read in order.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Rendering Fundamentals](#rendering-fundamentals) | 4 | The mental model — when to use SSR, CSR, SSG, RSC |
| [App Router & Routing](#app-router--routing) | 4 | The modern routing model: layouts, nested routes, middleware, route handlers |
| [Data, Caching & Streaming](#data-caching--streaming) | 4 | The hardest part of Next.js — server actions, caching, streaming, ISR |
| [Auth, SEO & Optimization](#auth-seo--optimization) | 3 | Authentication, metadata, image optimization |
| [Interview Prep](#interview-prep) | 1 | 60+ interview Qs |

---

## Rendering Fundamentals

The mental model for choosing the right rendering strategy.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [SSR / CSR / SSG / ISR](10.4.01-ssr-csr-ssg-isr.md) | Rendering strategies comparison, when to use each, hydration, streaming | 25 min |
| 02 | [App Router](10.4.02-app-router.md) | Layouts, nested routes, loading states, error handling, route groups | 25 min |
| 03 | [Server Components](10.4.03-server-components.md) | RSC architecture, server rendering, serialization, "use server" | 30 min |
| 04 | [Client Components](10.4.04-client-components.md) | `'use client'`, interleaving, client boundaries, "use client" placement | 20 min |

---

## App Router & Routing

The modern App Router model — every Next.js interview tests this.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 02 | [App Router](10.4.02-app-router.md) | Layouts, nested routes, loading states, error handling | 25 min |
| 05 | [Middleware](10.4.05-middleware.md) | Edge middleware, matchers, redirects, rewrite, auth gating | 20 min |
| 07 | [Route Handlers](10.4.07-route-handlers.md) | API routes, request/response, caching, dynamic vs static | 15 min |
| 08 | [Metadata](10.4.08-metadata.md) | Static/dynamic metadata, SEO, Open Graph, robots, sitemaps | 15 min |

---

## Data, Caching & Streaming

The hardest part of Next.js — the 4 files every senior engineer must own.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [Server Actions](10.4.06-server-actions.md) | Mutations, revalidation, progressive enhancement, form actions | 25 min |
| 09 | [Caching](10.4.09-caching.md) | Data cache, full route cache, revalidation, stale-while-revalidate, cache tags | 30 min |
| 10 | [Streaming](10.4.10-streaming.md) | Streaming SSR, Suspense boundaries, loading UI, parallel routes | 25 min |
| 14 | [Incremental Static Regeneration](10.4.14-incremental-static-regeneration.md) | SWR, on-demand revalidation, cache tags, `generateStaticParams`, fallback | 20 min |
| 15 | [Static Exports](10.4.15-static-exports.md) | Static export config, `generateStaticParams`, client-side data, deployment | 20 min |
| 16 | [Data Fetching Patterns](10.4.16-data-fetching-patterns.md) | Server Component fetch, `unstable_cache`, Server Actions, React Query, Suspense, parallel fetches | 30 min |

---

## Auth, SEO & Optimization

Production concerns.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 11 | [Image Optimization](10.4.11-image-optimization.md) | `next/image`, lazy loading, responsive images, AVIF/WebP | 15 min |
| 13 | [Authentication](10.4.13-authentication.md) | Auth middleware, JWT, server/client auth flow, NextAuth.js, RBAC | 30 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 12 | [Interview Questions](10.4.12-interview-questions.md) | 60+ curated questions with answers | 3-4 hrs |

---

## Suggested Study Order

### Path A — Coming from Pages Router (3-5 days)
1. Rendering Fundamentals (4 files, ~2 hrs)
2. App Router + Middleware + Route Handlers (1.5 hrs)
3. Data, Caching & Streaming — the core of App Router (4-5 hrs)
4. Auth + Image + Metadata (1.5 hrs)
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
