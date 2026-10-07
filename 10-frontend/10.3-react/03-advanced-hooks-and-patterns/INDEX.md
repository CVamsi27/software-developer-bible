# Advanced Hooks & Patterns — React

> **Study time:** ≈ 1 h 50 m of reading (7 files, ~16 min average).
> **7 files.** Production-grade patterns: Suspense, error boundaries, custom hooks, external stores via useSyncExternalStore, performance profiling and optimization, and state management.

[![Files](https://img.shields.io/badge/files-7-blue)](#files)
[![Category](https://img.shields.io/badge/category-Advanced_Hooks_and_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Suspense](10.3.3.01-suspense.md) | Suspense boundaries, data fetching, useTransition, streaming SSR | Important | Specialized | 19 min |
| 02 | [Error Boundary](10.3.3.02-error-boundary.md) | Error boundaries, error recovery, logging, Sentry integration | Important | Important | 7 min |
| 03 | [Custom Hooks](10.3.3.03-custom-hooks.md) | Composition patterns, useLocalStorage, useDebounce, useFetch, testing, best practices | Essential | Important | 37 min |
| 04 | [useSyncExternalStore](10.3.3.04-usesyncexternalstore.md) | Tearing in concurrent rendering, subscribe/getSnapshot contract, snapshot caching, Zustand/Redux integration, infinite-loop mistakes | Important | Specialized | 16 min |
| 05 | [Performance](10.3.3.05-performance.md) | Profiler, React.memo, virtualization, windowing, debouncing, Web Workers | Essential | Foundational | 9 min |
| 06 | [State Management](10.3.3.06-state-management.md) | Redux Toolkit, Zustand, Jotai, Context vs external state, when to use which | Essential | Important | 15 min |

---

## Read order

Suspense → Error Boundary → Custom Hooks → useSyncExternalStore → Performance → State Management.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Error boundary (+ Sentry hook) | `packages/ui/src/components/feedback/error-boundary.tsx` - class boundary with `onError` capture and reset |
| Custom hooks library | `packages/hooks/src/index.ts` - reusable hook exports (debounce, storage, media query, shortcuts, …) |
| useSyncExternalStore contract | `apps/app/src/hooks/use-can-go-back.ts` - storage-event-backed store with server snapshot fallback |
| State management (Zustand) | `apps/app/src/lib/stores/appearance-store.ts` - store with devtools + persist middleware |

---

## Navigation

[← Back to React](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
