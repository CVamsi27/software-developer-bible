# React — Index

> **20 files** — React internals from Virtual DOM to Fiber, hooks, patterns, custom hooks, portals, compound components, React 18/19 concurrent APIs, performance, state management, and interview questions.

[![Files](https://img.shields.io/badge/files-20-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why React is non-negotiable:** Every senior frontend interview tests React deeply. Not just "how to use useState" — but the render/commit phases, why keys matter, how Suspense works, what changed in React 18/19 (Server Components, transitions, `use()` hook). This section goes from internals to patterns to interview Q&A.

---

## 🗂️ Topic Categories

The 20 files are organized into 5 conceptual categories — read in order within a category.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [React Internals](#-react-internals) | 5 | How React actually renders — the mental model that distinguishes senior engineers |
| [Core Hooks](#-core-hooks) | 5 | The 5 essential hooks (state, effect, memo, ref, context) — used daily |
| [Advanced Hooks & Patterns](#-advanced-hooks--patterns) | 5 | Suspense, Error Boundary, Performance, State Management, Custom Hooks |
| [React 18/19 Modern APIs](#-react-1819-modern-apis) | 2 | Concurrent rendering, transitions, server components, `use(promise)` |
| [Patterns & Interview Prep](#-patterns--interview-prep) | 3 | Portals, compound components, 60+ Qs |

---

## ⚙️ React Internals

How React actually works under the hood. The mental model that distinguishes a senior engineer from someone who only knows the API.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Virtual DOM](10.3.01-virtual-dom.md) | VDOM concept, diffing, batching, React elements vs components | 25 min |
| 02 | [Fiber](10.3.02-fiber.md) | Fiber architecture, work loop, priority lanes, time slicing | 30 min |
| 03 | [Reconciliation](10.3.03-reconciliation.md) | Diffing algorithm, keys, component types, bailout | 25 min |
| 04 | [Rendering](10.3.04-rendering.md) | Render phases, commit phase, batching in React 18, automatic batching | 25 min |
| 05 | [Lifecycle](10.3.05-lifecycle.md) | Class lifecycle, hooks lifecycle, useEffect cleanup, strict mode double-invoke | 20 min |

**Read order:** Virtual DOM → Fiber → Reconciliation → Rendering → Lifecycle.

---

## 🪝 Core Hooks

The 5 essential hooks. Used in 95% of React code.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [useState](10.3.06-usestate.md) | State initialization, batching, functional updates, lazy init | 20 min |
| 07 | [useEffect](10.3.07-useeffect.md) | Dependencies, cleanup, effect timing, strict mode, race conditions | 30 min |
| 08 | [useMemo / useCallback](10.3.08-usememo-usecallback.md) | Memoization, dependency tracking, when to use (and when not to) | 20 min |
| 09 | [useRef](10.3.09-useref.md) | DOM refs, mutable refs, forwardRef, callback refs, useImperativeHandle | 20 min |
| 10 | [Context API](10.3.10-context-api.md) | createContext, Provider, useContext, performance pitfalls, splitting context | 25 min |

---

## 🚀 Advanced Hooks & Patterns

The patterns that solve real problems in production code.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 11 | [Suspense](10.3.11-suspense.md) | Suspense boundaries, data fetching, useTransition, streaming SSR | 25 min |
| 12 | [Error Boundary](10.3.12-error-boundary.md) | Error boundaries, error recovery, logging, Sentry integration | 15 min |
| 13 | [Performance](10.3.13-performance.md) | Profiler, React.memo, virtualization, windowing, debouncing, Web Workers | 30 min |
| 14 | [State Management](10.3.14-state-management.md) | Redux Toolkit, Zustand, Jotai, Context vs external state, when to use which | 30 min |
| 16 | [Custom Hooks](10.3.16-custom-hooks.md) | Composition patterns, useLocalStorage, useDebounce, useFetch, testing, best practices | 30 min |

---

## 🆕 React 18/19 Modern APIs

The newest features — what changed in concurrent React and what you need to know for interviews.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 19 | [Modern Hooks (React 18/19)](10.3.19-modern-hooks-react18-19.md) | useTransition, useDeferredValue, useOptimistic, use(promise), ref-as-prop, Form actions | 30 min |
| 20 | [Web Components](10.3.11-web-components.md) | Custom Elements, Shadow DOM, HTML Templates, Web Components vs React | 20 min |

---

## 🧩 Patterns & Interview Prep

Reusable component patterns + 60+ interview Qs.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 17 | [Portals](10.3.17-portals.md) | createPortal, event bubbling, modals, tooltips, overflow escape, SSR safety | 15 min |
| 18 | [Compound Components](10.3.18-compound-components.md) | Context-based pattern, tabs, accordion, select, form fields, generics | 20 min |
| 15 | [Interview Questions](10.3.15-interview-questions.md) | 60+ curated questions with answers | 3-4 hrs |

---

## 🛣️ Suggested Study Order

### Path A — Coming from another framework (1 week)
1. React Internals (5 files, ~2 hrs)
2. Core Hooks (5 files, ~2 hrs)
3. Custom Hooks + State Management (1.5 hrs)
4. React 18/19 (1 hr)
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

## 🔗 Cross-References

- [JavaScript](../10.1-javascript/INDEX.md) — closures, `this`, prototypes
- [Next.js](../10.4-next.js/INDEX.md) — React Server Components, streaming
- [Testing (RTL, Vitest)](../../50-quality/50.1-testing/INDEX.md) — testing React components
- [Form Handling](../10.5-form-handling/INDEX.md) — form state with React
- [Animation (Framer, GSAP, React Spring)](../10.6-animation/INDEX.md) — animation in React
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — measuring React performance

---

## Navigation

[← Previous: TypeScript](../10.2-typescript/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Next.js →](../10.4-next.js/INDEX.md)
