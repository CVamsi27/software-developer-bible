# Rendering Fundamentals — Next.js

> **Study time:** ≈ 1 h 39 m of reading (4 files, ~25 min average).
> **4 files.** The mental model for choosing the right rendering strategy: SSR vs CSR vs SSG vs ISR, App Router conventions, React Server Components, and Client Component boundaries.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Rendering_Fundamentals-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [SSR / CSR / SSG / ISR](10.4.1.01-ssr-csr-ssg-isr.md) | Rendering strategies comparison, when to use each, hydration, streaming | 24 min |
| 02 | [App Router](10.4.1.02-app-router.md) | Layouts, nested routes, loading states, error handling, route groups | 23 min |
| 03 | [Server Components](10.4.1.03-server-components.md) | RSC architecture, server rendering, serialization, "use server" | 21 min |
| 04 | [Client Components](10.4.1.04-client-components.md) | `'use client'`, interleaving, client boundaries, "use client" placement | 31 min |

---

## Read order

SSR / CSR / SSG / ISR → App Router → Server Components → Client Components.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------ | ------------------------------------------------------------------------------------------------------ |
| CSR corner of the matrix | `apps/app/src/main.tsx` - pure client-side rendered SPA shell via `createRoot` |
| Server-rendered marketing site | `apps/landing/astro.config.mjs` - Astro server-output build (Cloudflare adapter) alongside the CSR app |

_No direct docita Next.js implementation (App Router / RSC / `"use client"`) yet._

---

## Navigation

[← Back to Next.js](../INDEX.md)
