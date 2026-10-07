# React Internals — React

> **Study time:** ≈ 1 h 34 m of reading (6 files, ~16 min average).
> **6 files.** How React actually works under the hood: Virtual DOM diffing, the Fiber data structure, reconciliation heuristics, render/commit phases, and lifecycle.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-React_Internals-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Virtual DOM](10.3.1.01-virtual-dom.md) | VDOM concept, diffing, batching, React elements vs components | Essential | Foundational | 15 min |
| 02 | [Fiber](10.3.1.02-fiber.md) | Fiber architecture, work loop, priority lanes, time slicing | Important | Important | 24 min |
| 03 | [Reconciliation](10.3.1.03-reconciliation.md) | Diffing algorithm, keys, component types, bailout | Essential | Foundational | 6 min |
| 04 | [Rendering](10.3.1.04-rendering.md) | Render phases, commit phase, batching in React 18, automatic batching | Essential | Foundational | 21 min |
| 05 | [Lifecycle](10.3.1.05-lifecycle.md) | Class lifecycle, hooks lifecycle, useEffect cleanup, strict mode double-invoke | Essential | Foundational | 24 min |

---

## Read order

Virtual DOM → Fiber → Reconciliation → Rendering → Lifecycle.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Hooks lifecycle & effect cleanup | `packages/hooks/src/use-mounted.ts` — effect schedules a timer and returns clearTimeout cleanup |
| StrictMode & root mounting | `apps/app/src/main.tsx` — createRoot and StrictMode; extra development checks do not mean every function runs twice in production |

---

## Navigation

[← Back to React](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
