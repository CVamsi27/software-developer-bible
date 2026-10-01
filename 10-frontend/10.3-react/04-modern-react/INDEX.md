# Modern React — React

> **Study time:** ≈ 48 min of reading (3 files, ~16 min average).
> **3 files.** What changed in React 18/19 — concurrent rendering, transitions, `use(promise)` — interop with the native Web Components platform, and React Router v6/v7 data routers.

[![Files](https://img.shields.io/badge/files-3-blue)](#files)
[![Category](https://img.shields.io/badge/category-Modern_React-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Modern Hooks (React 18/19)](10.3.4.01-modern-hooks-react18-19.md) | useTransition, useDeferredValue, useOptimistic, use(promise), ref-as-prop, Form actions | 17 min |
| 02 | [Web Components](10.3.4.02-web-components.md) | Custom Elements, Shadow DOM, HTML Templates, Web Components vs React | 12 min |
| 03 | [React Router](10.3.4.03-react-router.md) | createBrowserRouter data routers, nested routes + Outlet, loaders/actions, defer + Await, protected routes, relative routing, RR vs Next.js | 19 min |

---

## Read order

Modern Hooks (React 18/19) → Web Components → React Router.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| React Router routes & guards | `apps/app/src/App.tsx` - ~108 `<Route>` declarations across layout groups with protected/public route wrappers and Suspense |
| useDeferredValue | `apps/app/src/features/medical-coding/components/CodingQueuePageContent.tsx` - deferred search value over debounced input |
| Router-agnostic history provider | `packages/hooks/src/create-navigation-history-provider.ts` - factory decoupled from react-router via injected pathname hook |

---

## Navigation

[← Back to React](../INDEX.md)
