# React — Index

> **Study time:** ≈ 3 h 34 m of reading (28 files, ~8 min average).
> **28 files** — React internals from Virtual DOM to Fiber, hooks, patterns, custom hooks, portals, compound components, external stores, server-state ownership with TanStack Query, React Router data routers, React 18 and 19 concurrent APIs, performance, state management, and interview questions.

[![Files](https://img.shields.io/badge/files-28-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Senior React roles test the runtime model and the choices built on it: render and commit, component identity, Suspense, concurrent updates, and the server and client boundary. This section builds from internals through Hooks and composition patterns to interview practice.

---

## Topic Categories

The categories follow prerequisite order; read each learning flow before its revision drill.

| Category | Chapters | Why it matters |
| -------------------------------------------------------------------- | -------: | ----------------------------------------------------------------------------------------------------------------------- |
| [React Internals](01-react-internals/INDEX.md) | 5 | How React turns updates into committed UI, and how identity, scheduling, and state ownership change observable behavior |
| [Core Hooks](02-core-hooks/INDEX.md) | 5 | The 5 essential hooks (state, effect, memo, ref, context) — used daily |
| [Advanced Hooks & Patterns](03-advanced-hooks-and-patterns/INDEX.md) | 7 | Suspense, Error Boundary, Custom Hooks, `useSyncExternalStore`, Performance, State Management, and TanStack Query |
| [Modern React](04-modern-react/INDEX.md) | 3 | Concurrent rendering, transitions, Actions, Web Components, and React Router v8.4 |
| [Patterns & Interview Prep](05-patterns-and-interview/INDEX.md) | 3 | Portals, compound components, and senior interview drills |

---

## Study Flow

Read categories in numeric order — each builds on the previous:

```text
01-react-internals ─▶ 02-core-hooks ─▶ 03-advanced-hooks-and-patterns
    ─▶ 04-modern-react ─▶ 05-patterns-and-interview
```

---

## React Internals

Understand how React turns updates into committed UI, and how identity, scheduling, and state ownership change observable behavior.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Virtual DOM](01-react-internals/10.3.1.01-virtual-dom.md) | Element descriptions, `$$typeof` XSS protection, Fiber vs. DOM layers, and `{children}` stability | Essential | Foundational | 9 min |
| 02 | [Fiber](01-react-internals/10.3.1.02-fiber.md) | Twin `current` and `workInProgress` trees, begin and complete traversal, lanes, and cooperative yielding | Important | Important | 6 min |
| 03 | [Reconciliation](01-react-internals/10.3.1.03-reconciliation.md) | Type, position, and `key` identity, conditional slots, deliberate resets, and fiber bailout | Essential | Foundational | 5 min |
| 04 | [Rendering](01-react-internals/10.3.1.04-rendering.md) | Render, commit, and browser paint, React 18+ batching, `Object.is` bailout, hydration, and `flushSync` | Essential | Foundational | 5 min |
| 05 | [Lifecycle](01-react-internals/10.3.1.05-lifecycle.md) | Effect start-and-stop cycles, `AbortController` + `ignore` guards, bottom-up timing, and React 19 ref cleanups | Essential | Foundational | 5 min |

**Read order:** Virtual DOM → Fiber → Reconciliation → Rendering → Lifecycle.

---

## Core Hooks

The core state, synchronization, caching, handle, and context APIs.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [useState](02-core-hooks/10.3.2.01-usestate.md) | Render snapshots, queued updaters, lazy init, function-in-state, and ownership | Essential | Foundational | 6 min |
| 07 | [useEffect](02-core-hooks/10.3.2.02-useeffect.md) | External synchronization, dependency loops, stale-result guards, and `useEffectEvent` | Essential | Foundational | 8 min |
| 08 | [useMemo / useCallback](02-core-hooks/10.3.2.03-usememo-usecallback.md) | Measured render caches, `{children}` composition, and React Compiler 1.0 | Important | Important | 7 min |
| 09 | [`useRef`](02-core-hooks/10.3.2.04-useref.md) | Imperative handles, lazy init, list ref `Map`s, callback cleanup, and React 19 ref props | Essential | Foundational | 8 min |
| 10 | [Context API](02-core-hooks/10.3.2.05-context-api.md) | Provider scope, `{children}` isolation, split channels, React 19 `use(Context)`, and React 19.3 Server Components | Important | Important | 9 min |

---

## Advanced Hooks & Patterns

The patterns that solve real problems in production code.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 11 | [Suspense](03-advanced-hooks-and-patterns/10.3.3.01-suspense.md) | Suspense boundaries, render-as-you-fetch, sibling pre-warming, `useTransition`, and streaming SSR | Important | Specialized | 8 min |
| 12 | [Error Boundary](03-advanced-hooks-and-patterns/10.3.3.02-error-boundary.md) | Class boundary, `resetKey`, recovery scope, React 19 root error callbacks, and query error reset | Important | Important | 9 min |
| 13 | [Custom Hooks](03-advanced-hooks-and-patterns/10.3.3.03-custom-hooks.md) | Per-caller state, Hook rules, return contracts, callback stability, effect ownership, and lifecycle tests | Essential | Important | 7 min |
| 14 | [`useSyncExternalStore`](03-advanced-hooks-and-patterns/10.3.3.04-usesyncexternalstore.md) | Concurrent tearing, `subscribe` and `getSnapshot` contract, browser adapters, selector caching, and SSR snapshots | Important | Specialized | 7 min |
| 15 | [Performance](03-advanced-hooks-and-patterns/10.3.3.05-performance.md) | Profiler metrics, `memo` comparators, virtualization vs. `content-visibility`, code splitting, and deferred values | Essential | Foundational | 6 min |
| 16 | [State Management](03-advanced-hooks-and-patterns/10.3.3.06-state-management.md) | Ownership boundaries, Zustand, Redux Toolkit, Jotai, reducers, query caches, and version conflicts | Essential | Important | 6 min |
| 17 | [TanStack Query](03-advanced-hooks-and-patterns/10.3.3.07-tanstack-query.md) | Query keys, `queryOptions`, `keepPreviousData`, freshness, mutations, optimistic rollback, and SSR hydration | Essential | Important | 9 min |

---

## Modern React

The newest features — what changed in concurrent React and what you need to know for interviews.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 18 | [Modern React (18–19.3)](04-modern-react/10.3.4.01-modern-hooks-react18-19.md) | Scheduling, `useDeferredValue` initial values, Actions, form reset, Suspense resources, Effect Events, Fragment refs, and View Transitions | Important | Specialized | 14 min |
| 19 | [Web Components](04-modern-react/10.3.4.02-web-components.md) | Custom-element lifecycle, attributes, properties, and events, Declarative Shadow DOM, `ElementInternals`, and React 19 interop | Important | Specialized | 8 min |
| 20 | [React Router](04-modern-react/10.3.4.03-react-router.md) | v8.4 modes, nested routes, middleware, loaders and actions, `isRouteErrorResponse`, Suspense and `Await`, revalidation, and React Router vs. Next.js | Essential | Foundational | 13 min |

---

## Patterns & Interview Prep

Reusable component patterns + interview drills.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 21 | [Portals](05-patterns-and-interview/10.3.5.01-portals.md) | `createPortal`, React vs. native bubbling, outside-click ref guards, `inert`, `<dialog>` and Popover API, and SSR safety | Important | Specialized | 7 min |
| 22 | [Compound Components](05-patterns-and-interview/10.3.5.02-compound-components.md) | Context composition, `asChild` Slot merging, generic factories, controllable state, form fields, and ARIA contracts | Important | Specialized | 11 min |
| 23 | [Interview Questions](05-patterns-and-interview/10.3.5.03-interview-questions.md) | 47 curated mechanism, React 19.2–19.3, trade-off, and system design questions | Important | Specialized | 14 min |

---

## Suggested Study Order

### Path A — Coming from another framework (1 week)
1. React Internals (5 files, ~2 hrs)
2. Core Hooks (5 files, ~2 hrs)
3. Custom Hooks → State Management → TanStack Query; trace a canceled read and an uncertain write
4. Modern React (1 hr)
5. Performance + Suspense + Error Boundary (1.5 hrs)
6. Interview Questions (3 hrs)

### Path B — React experienced, prepping for senior (1-2 days)
1. Fiber + Reconciliation (skim, 1 hr)
2. Modern React (18–19.3) (1 hr)
3. Performance and TanStack Query; distinguish render cost from server-state freshness
4. Interview Questions (focus on the 20 harder Qs)

### Path C — Interview tomorrow
- Review each chapter's definition, example, and summary; focus on the topics listed above
- Re-read Custom Hooks → State Management → TanStack Query, then the category revision
- Run through the interview questions

---

## Cross-References

- [JavaScript](../10.1-javascript/INDEX.md) — closures, `this`, and prototypes
- [Next.js](../10.4-next.js/INDEX.md) — React Server Components, streaming
- [Testing (RTL, Vitest)](../../50-quality/50.1-testing/INDEX.md) — testing React components
- [Form Handling](../10.5-form-handling/INDEX.md) — form state with React
- [Animation (Framer, GSAP, React Spring)](../10.6-animation/INDEX.md) — animation in React
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring React performance

---

## Navigation

[← Previous: TypeScript](../10.2-typescript/INDEX.md) · [Back to Index](../../INDEX.md) · [Next: Next.js →](../10.4-next.js/INDEX.md)
