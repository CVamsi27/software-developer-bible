# React — Index

> **Study time:** ≈ 8 h 31 m of reading (22 files, ~23 min average).
> **22 files** — React internals from Virtual DOM to Fiber, hooks, patterns, custom hooks, portals, compound components, external stores, React Router data routers, React 18/19 concurrent APIs, performance, state management, and interview questions.

[![Files](https://img.shields.io/badge/files-22-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why React is non-negotiable:** Every senior frontend interview tests React deeply. Not just "how to use useState" — but the render/commit phases, why keys matter, how Suspense works, what changed in React 18/19 (Server Components, transitions, `use()` hook). This section goes from internals to patterns to interview Q&A.

---

## Topic Categories

The 22 files are organized into 5 category folders — read in order within a category.

| Category | Files | Why it matters |
| -------------------------------------------------------------------- | ----: | ----------------------------------------------------------------------------------------------- |
| [React Internals](01-react-internals/INDEX.md) | 5 | How React actually renders — the mental model that distinguishes senior engineers |
| [Core Hooks](02-core-hooks/INDEX.md) | 5 | The 5 essential hooks (state, effect, memo, ref, context) — used daily |
| [Advanced Hooks & Patterns](03-advanced-hooks-and-patterns/INDEX.md) | 6 | Suspense, Error Boundary, Custom Hooks, useSyncExternalStore, Performance, State Management |
| [Modern React](04-modern-react/INDEX.md) | 3 | Concurrent rendering, transitions, server components, `use(promise)`, React Router data routers |
| [Patterns & Interview Prep](05-patterns-and-interview/INDEX.md) | 3 | Portals, compound components, 60+ Qs |

---

## Study Flow

Read categories in numeric order — each builds on the previous:

```text
01-react-internals ─▶ 02-core-hooks ─▶ 03-advanced-hooks-and-patterns
    ─▶ 04-modern-react ─▶ 05-patterns-and-interview
```

---

## React Internals

How React actually works under the hood. The mental model that distinguishes a senior engineer from someone who only knows the API.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Virtual DOM](01-react-internals/10.3.1.01-virtual-dom.md) | VDOM concept, diffing, batching, React elements vs components | 19 min |
| 02 | [Fiber](01-react-internals/10.3.1.02-fiber.md) | Fiber architecture, work loop, priority lanes, time slicing | 26 min |
| 03 | [Reconciliation](01-react-internals/10.3.1.03-reconciliation.md) | Diffing algorithm, keys, component types, bailout | 25 min |
| 04 | [Rendering](01-react-internals/10.3.1.04-rendering.md) | Render phases, commit phase, batching in React 18, automatic batching | 26 min |
| 05 | [Lifecycle](01-react-internals/10.3.1.05-lifecycle.md) | Class lifecycle, hooks lifecycle, useEffect cleanup, strict mode double-invoke | 27 min |

**Read order:** Virtual DOM → Fiber → Reconciliation → Rendering → Lifecycle.

---

## Core Hooks

The 5 essential hooks. Used in 95% of React code.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 06 | [useState](02-core-hooks/10.3.2.01-usestate.md) | State initialization, batching, functional updates, lazy init | 28 min |
| 07 | [useEffect](02-core-hooks/10.3.2.02-useeffect.md) | Dependencies, cleanup, effect timing, strict mode, race conditions | 29 min |
| 08 | [useMemo / useCallback](02-core-hooks/10.3.2.03-usememo-usecallback.md) | Memoization, dependency tracking, when to use (and when not to) | 26 min |
| 09 | [useRef](02-core-hooks/10.3.2.04-useref.md) | DOM refs, mutable refs, forwardRef, callback refs, useImperativeHandle | 28 min |
| 10 | [Context API](02-core-hooks/10.3.2.05-context-api.md) | createContext, Provider, useContext, performance pitfalls, splitting context | 32 min |

---

## Advanced Hooks & Patterns

The patterns that solve real problems in production code.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 11 | [Suspense](03-advanced-hooks-and-patterns/10.3.3.01-suspense.md) | Suspense boundaries, data fetching, useTransition, streaming SSR | 23 min |
| 12 | [Error Boundary](03-advanced-hooks-and-patterns/10.3.3.02-error-boundary.md) | Error boundaries, error recovery, logging, Sentry integration | 25 min |
| 13 | [Custom Hooks](03-advanced-hooks-and-patterns/10.3.3.03-custom-hooks.md) | Composition patterns, useLocalStorage, useDebounce, useFetch, testing, best practices | 43 min |
| 14 | [useSyncExternalStore](03-advanced-hooks-and-patterns/10.3.3.04-usesyncexternalstore.md) | Tearing in concurrent rendering, subscribe/getSnapshot contract, snapshot caching, Zustand/Redux integration, infinite-loop mistakes | 16 min |
| 15 | [Performance](03-advanced-hooks-and-patterns/10.3.3.05-performance.md) | Profiler, React.memo, virtualization, windowing, debouncing, Web Workers | 11 min |
| 16 | [State Management](03-advanced-hooks-and-patterns/10.3.3.06-state-management.md) | Redux Toolkit, Zustand, Jotai, Context vs external state, when to use which | 14 min |

---

## Modern React

The newest features — what changed in concurrent React and what you need to know for interviews.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 17 | [Modern Hooks (React 18/19)](04-modern-react/10.3.4.01-modern-hooks-react18-19.md) | useTransition, useDeferredValue, useOptimistic, use(promise), ref-as-prop, Form actions | 13 min |
| 18 | [Web Components](04-modern-react/10.3.4.02-web-components.md) | Custom Elements, Shadow DOM, HTML Templates, Web Components vs React | 10 min |
| 19 | [React Router](04-modern-react/10.3.4.03-react-router.md) | createBrowserRouter data routers, nested routes + Outlet, loaders/actions, defer + Await, protected routes, relative routing, RR vs Next.js | 18 min |

---

## Patterns & Interview Prep

Reusable component patterns + 60+ interview Qs.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 20 | [Portals](05-patterns-and-interview/10.3.5.01-portals.md) | createPortal, event bubbling, modals, tooltips, overflow escape, SSR safety | 31 min |
| 21 | [Compound Components](05-patterns-and-interview/10.3.5.02-compound-components.md) | Context-based pattern, tabs, accordion, select, form fields, generics | 27 min |
| 22 | [Interview Questions](05-patterns-and-interview/10.3.5.03-interview-questions.md) | 60+ curated questions with answers | 14 min |

---

## Suggested Study Order

### Path A — Coming from another framework (1 week)
1. React Internals (5 files, ~2 hrs)
2. Core Hooks (5 files, ~2 hrs)
3. Custom Hooks + State Management (1.5 hrs)
4. Modern React (1 hr)
5. Performance + Suspense + Error Boundary (1.5 hrs)
6. Interview Questions (3 hrs)

### Path B — React experienced, prepping for senior (1-2 days)
1. Fiber + Reconciliation (skim, 1 hr)
2. Modern Hooks (React 18/19) (1 hr)
3. Performance deep-dive (1 hr)
4. Interview Questions (focus on the 20 harder Qs)

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- Re-read Custom Hooks + State Management
- Run through the 60+ Interview Questions

---

## Cross-References

- [JavaScript](../10.1-javascript/INDEX.md) — closures, `this`, prototypes
- [Next.js](../10.4-next.js/INDEX.md) — React Server Components, streaming
- [Testing (RTL, Vitest)](../../50-quality/50.1-testing/INDEX.md) — testing React components
- [Form Handling](../10.5-form-handling/INDEX.md) — form state with React
- [Animation (Framer, GSAP, React Spring)](../10.6-animation/INDEX.md) — animation in React
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring React performance

---

## Navigation

[← Previous: TypeScript](../10.2-typescript/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Next.js →](../10.4-next.js/INDEX.md)
