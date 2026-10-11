# Production — Next.js

> **Study time:** ≈ 1 h 10 m of reading (4 files, ~18 min average).
> **4 files.** Shipping concerns: authentication across Proxy/server/client boundaries, responsive image delivery, and deployment — managed hosting vs self-hosted Docker, cache coordination, environment configuration, version skew and observability.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Production-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Authentication](10.4.4.01-authentication.md) | Proxy redirects, session verification, data-boundary authorization, CSRF, NextAuth.js v4 | Important | Important | 32 min |
| 02 | [Image Optimization](10.4.4.02-image-optimization.md) | `next/image`, lazy loading, responsive images, AVIF/WebP | Important | Specialized | 18 min |
| 03 | [Deploying Next.js](10.4.4.03-deploying-nextjs.md) | standalone Docker output, managed vs self-hosted, Edge limits, cacheHandler vs cacheHandlers, replica coordination, rolling releases, multi-zone, environment and observability | Important | Specialized | 17 min |

---

## Read order

1. **Protect operations:** trace a verified session into a current principal and resource permission; distinguish client feedback from server enforcement.
2. **Ship suitable image bytes:** connect displayed width and device density to a variant, then test layout reservation and error feedback.
3. **Operate the artifact:** follow standalone output into a running container; align replicas on build and Server Action keys; decide cache ownership, asset retention, version-skew handling, configuration and rollback.
4. **Check recall:** complete [Production revision](REVISION.md), then the [Next.js interview drill](../05-interview-prep/10.4.5.01-interview-questions.md).

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

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
