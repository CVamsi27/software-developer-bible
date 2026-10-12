# Frontend Stack

> **Study time:** ≈ 26 h 3 m of reading (145 files, ~11 min average).
> **JavaScript, TypeScript, React, Next.js, Form Handling, Animation, HTML/CSS/PWA, Mobile** — the frontend foundation for the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> 145 files across 8 sub-stacks, organized by what you need to know in what order.

**Real-world anchor:** category anchor tables link available [Docita evidence](https://github.com/CVamsi27/docita) and identify topics without a direct implementation. Read those gaps before claiming production experience.

[![Files](https://img.shields.io/badge/files-145-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-8-green)](#the-8-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Start with one product flow

Use a public page and an authenticated edit form as a running example. Explain how JavaScript runs the handler, TypeScript constrains its inputs, React updates the interface, and the server validates and persists the edit. Include loading, rejected input, expired authorization and a slow response; the happy path alone hides the important boundaries.

The category indexes below guide each mechanism in study order. Their source-linked revision companions come after the learning chapters, followed by separate interview practice.

---

## The 8 Sub-Stacks (in study order)

| Order | Sub-stack | Files | Categories | Topics |
| ----: | ----------------------------------------------- | ----: | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | [JavaScript](10.1-javascript/INDEX.md) | 34 | 6 categories | [Execution & Scope](10.1-javascript/01-execution-and-scope/INDEX.md), [Objects/Prototypes/`this`](10.1-javascript/02-objects-prototypes-this/INDEX.md), [Async & Concurrency](10.1-javascript/03-async-concurrency/INDEX.md), [Memory & Data](10.1-javascript/04-memory-and-data/INDEX.md), [Functional Patterns](10.1-javascript/05-functional-patterns/INDEX.md), [Modern JS](10.1-javascript/06-modern-and-interview/INDEX.md) |
| 2 | [TypeScript](10.2-typescript/INDEX.md) | 18 | 5 categories | [Foundations](10.2-typescript/01-foundations/INDEX.md), [Generics & Inference](10.2-typescript/02-generics-and-inference/INDEX.md), [Type Transformations](10.2-typescript/03-type-transformations/INDEX.md), [Advanced Patterns](10.2-typescript/04-advanced-patterns/INDEX.md), [Interview Prep](10.2-typescript/05-interview-prep/INDEX.md) |
| 3 | [React](10.3-react/INDEX.md) | 22 | 5 categories | [React Internals](10.3-react/01-react-internals/INDEX.md), [Core Hooks](10.3-react/02-core-hooks/INDEX.md), [Advanced Hooks & Patterns](10.3-react/03-advanced-hooks-and-patterns/INDEX.md), [Modern React](10.3-react/04-modern-react/INDEX.md), [Patterns & Interview Prep](10.3-react/05-patterns-and-interview/INDEX.md) |
| 4 | [Next.js](10.4-next.js/INDEX.md) | 17 | 5 categories | [Rendering Fundamentals](10.4-next.js/01-rendering-fundamentals/INDEX.md), [Routing & Middleware](10.4-next.js/02-routing-and-middleware/INDEX.md), [Data & Caching](10.4-next.js/03-data-and-caching/INDEX.md), [Production](10.4-next.js/04-production/INDEX.md), [Interview Prep](10.4-next.js/05-interview-prep/INDEX.md) |
| 5 | [Form Handling](10.5-form-handling/INDEX.md) | 7 | — | React Hook Form, Zod, Formik, TanStack Form, Server Actions, Autosave & Draft Recovery |
| 6 | [Animation](10.6-animation/INDEX.md) | 8 | — | Framer Motion, CSS Animations, GSAP, React Spring, View Transitions, Canvas & SVG |
| 7 | [HTML/CSS & PWA](10.7-html-css/INDEX.md) | 9 | — | Semantic HTML, CSS layout/responsive, CSS architecture (layers, BEM, Modules/Tailwind/CSS-in-JS), theming & design tokens, PWA/service workers, browser storage, SEO, browser rendering |
| 8 | [Mobile & Cross-Platform](10.8-mobile/INDEX.md) | 7 | — | React Native architecture (JSI/Fabric), Expo decision, RN vs native vs PWA matrix, deep linking/universal links, RN testing (Detox/Maestro), EAS builds, OTA updates, store release automation, interview questions |

---

## Pass 1 — make execution and data boundaries explicit

Read [JavaScript](10.1-javascript/INDEX.md) for execution/scope, objects, asynchronous work and memory. Follow with [TypeScript](10.2-typescript/INDEX.md) for narrowing, generics and transformations. Trace actual values before constructing advanced types; TypeScript's static guarantees do not validate network data at runtime.

## Pass 2 — connect React rendering to user behavior

[React](10.3-react/INDEX.md) explains render/commit, component identity, hooks and server-state coordination. Keep local UI state distinct from cached server state and test the loading/error/race behavior of the running edit form.

[HTML/CSS & PWA](10.7-html-css/INDEX.md) supplies semantic controls, keyboard relationships, layout and browser rendering. These remain part of the product when a framework owns the components.

## Pass 3 — follow requests through a full-stack framework

[Next.js](10.4-next.js/INDEX.md) connects routes, Server Components, client boundaries, data caching and mutations. Explain where authentication and validation execute, which data a cache may share, and how a successful write makes the next read fresh.

[Form Handling](10.5-form-handling/INDEX.md) completes the edit flow with runtime schemas, field state, submission and durable drafts. Select a library for the form behavior, then exercise retries, reset and recovery.

## Pass 4 — add the capabilities the role requires

[Animation](10.6-animation/INDEX.md) connects visual changes to lifecycle, reduced motion and rendering cost. [Mobile & Cross-Platform](10.8-mobile/INDEX.md) adds native runtime, linking and release boundaries. Use these when the product or role requires them; preserve the same correctness and accessibility standards.

## Before an interview

Use each category's revision companion to recall mechanisms. Then answer its interview bank with a concrete trace, a failure case and a decision boundary. Reopen the canonical chapter for a missed mechanism rather than rereading several overlapping summaries.

---

## Cross-References

- [Backend Stack](../20-backend/INDEX.md) — for full-stack interviews
- [System Design](../30-architecture/30.2-system-design/INDEX.md) — frontend-side system design (CDN, edge, caching)
- [Quality Stack](../50-quality/INDEX.md) — testing, a11y, performance

---

## Navigation

[← Back to Bible Index](../INDEX.md) · [Next: Backend →](../20-backend/INDEX.md)
