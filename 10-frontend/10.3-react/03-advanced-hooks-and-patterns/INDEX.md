# Advanced Hooks & Patterns — React

> **Study time:** ≈ 55 min of reading (8 files, ~7 min average).
> **8 files.** Production-grade patterns: Suspense, error boundaries, custom hooks, external stores via useSyncExternalStore, performance profiling and optimization, state management, and server-state ownership with TanStack Query.

[![Files](https://img.shields.io/badge/files-8-blue)](#files)
[![Category](https://img.shields.io/badge/category-Advanced_Hooks_and_Patterns-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Suspense](10.3.3.01-suspense.md) | Suspense boundaries, data fetching, useTransition, streaming SSR | Important | Specialized | 7 min |
| 02 | [Error Boundary](10.3.3.02-error-boundary.md) | Class boundary, recovery scope, safe reporting, resource retry | Important | Important | 8 min |
| 03 | [Custom Hooks](10.3.3.03-custom-hooks.md) | Per-caller state, Hook rules, effect ownership, shared-state boundaries, lifecycle tests | Essential | Important | 7 min |
| 04 | [useSyncExternalStore](10.3.3.04-usesyncexternalstore.md) | Tearing in concurrent rendering, subscribe/getSnapshot contract, snapshot caching, Zustand/Redux integration, infinite-loop mistakes | Important | Specialized | 6 min |
| 05 | [Performance](10.3.3.05-performance.md) | Profiling, memo boundaries, virtualization, code splitting, transitions | Essential | Foundational | 5 min |
| 06 | [State Management](10.3.3.06-state-management.md) | Local/shared/server state, query caches, reducers, version conflicts and ownership boundaries | Essential | Important | 6 min |
| 07 | [TanStack Query](10.3.3.07-tanstack-query.md) | Query keys, stale-while-revalidate, retries, dedupe, optimistic updates, SSR hydration | Essential | Important | 8 min |

---

## Read order

1. **Define pending and failed regions.** Read Suspense and Error Boundary. Explain the separate pending, rejected and ordinary event-error paths.
2. **Reuse behavior without hiding ownership.** Read Custom Hooks and useSyncExternalStore. Trace independent Hook state, resource cleanup and stable external snapshots.
3. **Choose the measured solution.** Read Performance and State Management. Separate draft, cache and authoritative server state; practice changed-condition cases in [revision](REVISION.md) before timed interview drills.

---

## Docita Anchor

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

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
