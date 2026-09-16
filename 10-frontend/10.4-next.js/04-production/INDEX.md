# Production — Next.js

> **Study time:** ≈ 1 h 9 m of reading (3 files, ~23 min average).
> **3 files.** Shipping concerns: authentication across middleware/server/client boundaries, `next/image` optimization, and deploying — Vercel vs self-hosted Docker, ISR cache handlers, env vars, observability.

[![Files](https://img.shields.io/badge/files-3-blue)](#files)
[![Category](https://img.shields.io/badge/category-Production-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Authentication](10.4.4.01-authentication.md) | Auth middleware, JWT, server/client auth flow, NextAuth.js, RBAC | 30 min |
| 02 | [Image Optimization](10.4.4.02-image-optimization.md) | `next/image`, lazy loading, responsive images, AVIF/WebP | 24 min |
| 03 | [Deploying Next.js](10.4.4.03-deploying-nextjs.md) | output standalone + multi-stage Dockerfile, Vercel vs self-hosted, edge limits, ISR cacheHandler, multi-zone, env build-vs-runtime, observability | 15 min |

---

## Read order

Authentication → Image Optimization → Deploying Next.js.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| RBAC permission matrix | `packages/utils/src/access/effective-permissions.ts` - role/tier/plan-mode access checks shared across apps |
| Multi-stage Docker deploy | `apps/api/Dockerfile` - `deps` → `runtime` stages copying built workspace packages |

_No NextAuth/middleware auth or built-in image optimization pipeline in docita yet._

---

## Navigation

[← Back to Next.js](../INDEX.md)
