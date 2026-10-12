# Modern React — React

> **Study time:** ≈ 56 min of reading (4 files, ~14 min average).
> **4 files.** React 18/19 scheduling and Actions, native Web Components interop, and React Router v8 modes with data loading, mutations, errors and revalidation.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Modern_React-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Modern Hooks (React 18/19)](10.3.4.01-modern-hooks-react18-19.md) | useTransition, useDeferredValue, useOptimistic, use(promise), ref-as-prop, Form actions | Important | Specialized | 20 min |
| 02 | [Web Components](10.3.4.02-web-components.md) | Custom Elements, Shadow DOM, HTML Templates, Web Components vs React | Important | Specialized | 12 min |
| 03 | [React Router](10.3.4.03-react-router.md) | v8 modes, nested routes + Outlet, loaders/actions, promise data + Await, authorization boundaries, revalidation, relative routing | Essential | Foundational | 20 min |

---

## Read order

1. **Separate pending work from confirmed truth.** Read Modern Hooks; trace a transition, resource read and optimistic Action before choosing an API.
2. **Identify the host boundary.** Read Web Components; compare attributes, properties, events and React ownership without treating Shadow DOM as a sandbox.
3. **Make the URL select the lifecycle.** Read React Router, then [revision](REVISION.md). Trace matching, parallel loaders, a failure, a mutation and revalidation; check the v7-to-v8 migration note before applying the examples to an older codebase.

---

## Docita Anchor

The following examples refer to the local Docita codebase, a healthcare platform with a NestJS API and React/Astro apps in a TypeScript monorepo. Study the chapter, then use these paths to find the implementation:

| Topic in this category | Docita evidence |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| React Router routes & guards | `apps/app/src/App.tsx` - route declarations across layout groups with protected/public route wrappers and Suspense |
| useDeferredValue | `apps/app/src/features/medical-coding/components/CodingQueuePageContent.tsx` - deferred search value over debounced input |
| Router-agnostic history provider | `packages/hooks/src/create-navigation-history-provider.ts` - factory decoupled from react-router via injected pathname hook |

---

## Navigation

[← Back to React](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
