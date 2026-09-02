# Frontend Stack

> **JavaScript, TypeScript, React, Next.js, Form Handling, Animation, HTML/CSS/PWA, Mobile** — shared by both the [indian-sde-faang lane](../81-lanes-indian-sde-faang/INDEX.md) and the [abroad-full-stack lane](../80-lanes-abroad-full-stack/INDEX.md).
>
> 111 files across 8 sub-stacks, organized by what you need to know in what order.

**Real-world anchor:** every category page below ends with a [Docita Anchor](https://github.com/CVamsi27/docita) table pointing at the matching production code.

[![Files](https://img.shields.io/badge/files-113-blue)](../INDEX.md)
[![Sub-stacks](https://img.shields.io/badge/sub--stacks-8-green)](#the-8-sub-stacks-in-study-order)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this stack matters

Every senior full-stack interview tests frontend fundamentals. Even if you specialize in backend, you must be able to:
- Explain how the JS event loop works
- Read and write modern React (hooks, Suspense, Server Components)
- Discuss Next.js App Router architecture
- Debugg performance issues (Core Web Vitals, bundle size)

This stack is the canonical reference. Each sub-stack has its own INDEX with detailed categorization, decision flowcharts, and interview Q&A.

---

## The 8 Sub-Stacks (in study order)

| Order | Sub-stack                                       | Files | Categories   | Topics                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----: | ----------------------------------------------- | ----: | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | [JavaScript](10.1-javascript/INDEX.md)          | 30    | 6 categories | [Execution & Scope](10.1-javascript/01-execution-and-scope/INDEX.md), [Async & Concurrency](10.1-javascript/03-async-concurrency/INDEX.md), [Objects/Prototypes/`this`](10.1-javascript/02-objects-prototypes-this/INDEX.md), [Memory & Data](10.1-javascript/04-memory-and-data/INDEX.md), [Functional Patterns](10.1-javascript/05-functional-patterns/INDEX.md), [Modern JS](10.1-javascript/06-modern-and-interview/INDEX.md) |
| 2     | [TypeScript](10.2-typescript/INDEX.md)          | 18    | 5 categories | [Foundations](10.2-typescript/01-foundations/INDEX.md), [Generics & Inference](10.2-typescript/02-generics-and-inference/INDEX.md), [Type Transformations](10.2-typescript/03-type-transformations/INDEX.md), [Advanced Patterns](10.2-typescript/04-advanced-patterns/INDEX.md), [Interview Prep](10.2-typescript/05-interview-prep/INDEX.md)                                                                                    |
| 3     | [React](10.3-react/INDEX.md)                    | 22    | 5 categories | [React Internals](10.3-react/01-react-internals/INDEX.md), [Core Hooks](10.3-react/02-core-hooks/INDEX.md), [Advanced Hooks & Patterns](10.3-react/03-advanced-hooks-and-patterns/INDEX.md), [Modern React](10.3-react/04-modern-react/INDEX.md), [Patterns & Interview Prep](10.3-react/05-patterns-and-interview/INDEX.md)                                                                                                      |
| 4     | [Next.js](10.4-next.js/INDEX.md)                | 16    | 5 categories | [Rendering Fundamentals](10.4-next.js/01-rendering-fundamentals/INDEX.md), [Routing & Middleware](10.4-next.js/02-routing-and-middleware/INDEX.md), [Data & Caching](10.4-next.js/03-data-and-caching/INDEX.md), [Production](10.4-next.js/04-production/INDEX.md), [Interview Prep](10.4-next.js/05-interview-prep/INDEX.md)                                                                                                     |
| 5     | [Form Handling](10.5-form-handling/INDEX.md)    | 7     | —            | React Hook Form, Zod, Formik, TanStack Form, Server Actions, Autosave & Draft Recovery                                                                                                                                                                                                                                                                                                                                            |
| 6     | [Animation](10.6-animation/INDEX.md)            | 8     | —            | Framer Motion, CSS Animations, GSAP, React Spring, View Transitions, Canvas & SVG                                                                                                                                                                                                                                                                                                                                                 |
| 7     | [HTML/CSS & PWA](10.7-html-css/INDEX.md)        | 7     | —            | Semantic HTML, CSS layout/responsive, CSS architecture (layers, BEM, Modules/Tailwind/CSS-in-JS), theming & design tokens, PWA/service workers, SEO, browser rendering                                                                                                                                                                                                                                                            |
| 8     | [Mobile & Cross-Platform](10.8-mobile/INDEX.md) | 3     | —            | React Native architecture (JSI/Fabric), Expo decision, RN vs native vs PWA matrix, deep linking/universal links, RN testing (Detox/Maestro)                                                                                                                                                                                                                                                                                       |

---

## Category Map (high-level)

The frontend stack is large. Here's the topic map so you know what to read in what order.

### Fundamentals (read first)
- **JavaScript** — execution, scope, async, prototypes, `this` — every interview tests these
- **TypeScript** — generics, conditional types, narrowing — type system fluency

### Frameworks (read second)
- **React** — internals, hooks, patterns, modern (18/19) APIs
- **Next.js** — App Router, RSC, caching, streaming, Server Actions

### Specialized (read as needed by JD)
- **Form Handling** — React Hook Form, Zod, Server Actions
- **Animation** — Framer Motion, GSAP, React Spring, Canvas/SVG
- **HTML/CSS & PWA** — semantic HTML, responsive, CSS architecture & tokens, PWA
- **Mobile** — React Native, Expo, deep linking, RN testing

---

## Suggested Study Order

### Path A — Full-stack senior prepping for mid-stage (1-2 weeks)
1. **JavaScript TL;DR + Async & Concurrency** (1.5 hrs) — must know
2. **TypeScript TL;DR + Generics** (1 hr)
3. **React TL;DR + Core Hooks + Modern Hooks** (3 hrs) — must know
4. **Next.js TL;DR + Caching + RSC** (2 hrs) — must know
5. Skim: Form Handling, Animation, HTML/CSS

### Path B — Frontend specialist, deep dive (3-4 weeks)
1. JavaScript: all 6 categories (6-8 hrs)
2. TypeScript: all 5 categories (4-5 hrs)
3. React: all 5 categories (8-10 hrs)
4. Next.js: all 5 categories (6-8 hrs)
5. Specialized topics as relevant

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- JavaScript: re-read Event Loop + Promises + Closures
- React: re-read Modern Hooks (18/19)
- Next.js: re-read Caching + Server Components

---

## Cross-References

- [Backend Stack](../20-backend/INDEX.md) — for full-stack interviews
- [System Design](../INDEX.md) — frontend-side system design (CDN, edge, caching)
- [Quality Stack](../INDEX.md) — testing, a11y, performance
- [Coding Patterns](../INDEX.md) — algorithm patterns in JS/TS

---

## Navigation

[← Back to Bible Index](../INDEX.md) · [Next: Backend →](../20-backend/INDEX.md)
