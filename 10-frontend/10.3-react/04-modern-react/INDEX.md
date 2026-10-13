# Modern React — React

> **Study time:** ≈ 36 min of reading (4 files, ~9 min average).
> **4 files.** Learn when to defer React rendering, coordinate Actions and Suspense, cross a Web Components boundary, and connect React Router v8.4 navigation to data and server authorization.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Modern_React-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Modern React (18–19.3)](10.3.4.01-modern-hooks-react18-19.md) | scheduling, Actions, Suspense resources, Effect Events, Fragment refs, View Transitions | Important | Specialized | 13 min |
| 02 | [Web Components](10.3.4.02-web-components.md) | custom-element lifecycle, attributes/properties/events, slots, Shadow DOM, React 19 interop | Important | Specialized | 7 min |
| 03 | [React Router](10.3.4.03-react-router.md) | v8.4 modes, nested routes, middleware, loaders/actions, pending UI, Suspense/Await, revalidation and server authorization | Essential | Foundational | 12 min |

---

## Read order

1. **Separate urgent input, pending work and confirmed truth.** Read Modern React; trace expensive rendering, an async save and a Suspense resource before choosing an API.
2. **Identify the host boundary.** Read Web Components; compare attributes, properties, events and React ownership without treating Shadow DOM as a sandbox.
3. **Make the URL select the lifecycle.** Read React Router, then [revision](REVISION.md). Trace middleware, matched loaders, an action, cancellation, failure and revalidation; keep authorization on the server API and check the v7-to-v8 guide before migrating.

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
