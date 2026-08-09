# Senior Full Stack Interview Bible — Index

> **Pick your lane first.** The bible is organized into **3 interview lanes** that draw from **7 shared study stacks**. Each lane has its own preparation strategy; the stacks are the technical material both lanes share.

[![Lanes](https://img.shields.io/badge/lanes-3-blue)](lanes/INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-7-green)](#-the-7-study-stacks-shared-by-both-lanes)
[![Files](https://img.shields.io/badge/files-400%2B-orange)](#-the-7-study-stacks-shared-by-both-lanes)
[![Last Updated](https://img.shields.io/badge/last%20updated-August%202026-purple)](#)

---

## 🎯 Pick Your Lane

| Lane | Folder | For | Style |
|------|--------|-----|-------|
| **Cross-Lane** (everyone starts here) | [Interview Strategy](strategy/INDEX.md) | Communication, resume, STAR method, HR questions | Universal — applies to all lanes |
| **Indian SDE / FAANG** | [Indian SDE / FAANG](lanes/indian-sde-faang/INDEX.md) | Microsoft, Google, Amazon, Meta, Apple, in-country India | LeetCode-heavy, 8-week intensive, USD 150-400K+ |
| **Abroad Full-Stack** | [Abroad Full-Stack](lanes/abroad-full-stack/INDEX.md) | EU / non-Indian mid-stage startups (n8n, SumUp, Scalable, sennder) | Take-home + system design, 4-week plan, EUR 70-110K + visa |

**Not sure?** Read the [lane decision matrix in abroad-full-stack](lanes/abroad-full-stack/INDEX.md#lane-decision--is-this-the-right-lane-for-you). If you're in between (e.g., Booking.com, Spotify, Stripe, remote-first US), use both lanes — start with `indian-sde-faang/` for the FAANG-DSA signal, then `abroad-full-stack/` for the EU-specific family/visa overlay.

---

## 📚 The 7 Study Stacks (shared by both lanes)

The technical material is grouped by **what you're studying**, not by which interview you're prepping for. Both lanes pull from the same stacks.

### Frontend (90 files in 6 sub-stacks)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [JavaScript](frontend/javascript/INDEX.md) | 27 | Execution context, closures, prototypes, event loop, promises, async/await, ES2024 |
| [TypeScript](frontend/typescript/INDEX.md) | 15 | Generics, utility types, conditional types, narrowing, `satisfies` operator |
| [React](frontend/react/INDEX.md) | 19 | Virtual DOM, Fiber, hooks (18-19), Suspense, performance, state management |
| [Next.js](frontend/nextjs/INDEX.md) | 16 | App Router, Server Components, Server Actions, Middleware, caching, streaming |
| [Form Handling](frontend/form-handling/INDEX.md) | 6 | React Hook Form, Zod, Formik, TanStack Form, Server Actions |
| [Animation](frontend/animation/INDEX.md) | 7 | Framer Motion, CSS Animations, GSAP, React Spring, View Transitions |

### Backend (107 files in 8 sub-stacks)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [Node.js](backend/nodejs/INDEX.md) | 11 | Event loop, streams, clustering, web streams, child processes, test runner |
| [NestJS](backend/nestjs/INDEX.md) | 14 | Modules, DI, guards, pipes, interceptors, CQRS, microservices |
| [REST APIs](backend/rest-api/INDEX.md) | 13 | HTTP methods, status codes, versioning, pagination, auth, OpenAPI, caching |
| [Database](backend/database/INDEX.md) | 14 | PostgreSQL, indexes, transactions, MVCC, Prisma, query planning, migrations |
| [Security](backend/security/INDEX.md) | 13 | JWT, OAuth, XSS, CSRF, RBAC, threat modeling, secrets management |
| [Design Patterns](backend/design-patterns/INDEX.md) | 15 | Singleton, Factory, Strategy, Repository, CQRS, Module, State |
| [Microservices](backend/microservices/INDEX.md) | 14 | Service discovery, saga, circuit breaker, event sourcing, gRPC, service mesh |
| [GraphQL](backend/graphql/INDEX.md) | 8 | Schema design, queries/mutations, Apollo Server, performance, security |

### Architecture (36 files)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [System Design](architecture/system-design/INDEX.md) | 36 | URL shortener, WhatsApp, Uber, Netflix, payment gateway, ticket booking + 14 theory files (CAP, sharding, caching, queues, consensus, ...) |

### Platform (63 files in 8 sub-stacks)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [Docker](platform/docker/INDEX.md) | 6 | Images, containers, volumes, networks, compose, multi-stage builds |
| [Kubernetes](platform/kubernetes/INDEX.md) | 14 | Pods, deployments, services, ingress, ConfigMaps, HPA, Helm, RBAC |
| [CI/CD](platform/ci-cd/INDEX.md) | 7 | GitHub Actions, Docker build/deploy, blue-green/canary, Jenkins, GitLab CI, ArgoCD |
| [Observability](platform/observability/INDEX.md) | 8 | Logging, monitoring, tracing, error tracking, SLI/SLO/SLA, alerting |
| [Build Tools](platform/build-tools/INDEX.md) | 9 | Webpack, Vite, Turbopack, Rspack, ESBuild, SWC, Babel |
| [Git Advanced](platform/git-advanced/INDEX.md) | 7 | Branching, rebase, cherry-pick, hooks, patch workflow, code archaeology |
| [Serverless & Edge](platform/serverless-edge/INDEX.md) | 7 | Lambda, Vercel Edge, serverless patterns, SAM/CDK/SST |
| [Monorepo](platform/monorepo/INDEX.md) | 5 | Turborepo, Nx, pnpm, Rush, Bazel |

### Quality (26 files in 3 sub-stacks)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [Testing](quality/testing/INDEX.md) | 11 | Jest, RTL, unit, integration, E2E, mocking, Vitest, load testing |
| [Accessibility](quality/accessibility/INDEX.md) | 7 | WCAG, ARIA, keyboard navigation, color contrast, forms & labels |
| [Performance Monitoring](quality/performance-monitoring/INDEX.md) | 8 | Core Web Vitals, profiling, Lighthouse CI, bundle analysis, RUM |

### Real-Time (8 files)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [WebSockets](realtime/websockets/INDEX.md) | 8 | Socket.IO, SSE, real-time architecture, NestJS WebSockets, WebTransport |

### Interview Toolkit (27 files in 3 sub-stacks)

| Sub-stack | Files | Topics |
|-----------|------:|--------|
| [Behavioral](interview-toolkit/behavioral/INDEX.md) | 4 | STAR method, HR questions, leadership questions, system design behavioral |
| [Coding Patterns](interview-toolkit/coding-patterns/INDEX.md) | 18 | Sliding window, two pointers, BFS/DFS, DP, heap, trie, union find, backtracking |
| [Cheat Sheets](interview-toolkit/cheatsheets/INDEX.md) | 5 | JavaScript, TypeScript, React/Next.js, backend, system design |

---

## 🛣️ Recommended Study Path

After you pick your lane (above), the two lanes share all 7 study stacks. They diverge in the final interview-prep phase.

```text
Frontend      → JavaScript → TypeScript → React → Next.js → Form Handling → Animation
Backend       → Node.js → NestJS → REST API → Database → Security → Design Patterns → Microservices → GraphQL
Architecture  → System Design (case studies + theory: CAP, sharding, caching, queues, ...)
Platform      → Docker → Kubernetes → CI/CD → Observability → Build Tools → Git Advanced → Serverless & Edge → Monorepo
Quality       → Testing → Accessibility → Performance Monitoring
Real-Time     → WebSockets
Toolkit       → Behavioral → Coding Patterns → Cheat Sheets
Lane overlay  → Indian SDE / FAANG (8-week plan) OR Abroad Full-Stack (4-week plan)
```

**For Indian SDE / FAANG:** Coding Patterns is the priority (18 files, all patterns). 8-12 week intensive, 4-6 hrs/day.
**For Abroad Full-Stack:** Coding Patterns is light (30-40 mediums across 6 patterns only). Heavy on System Design + take-home prep. 4-week realistic, 2-3 hrs/day.

---

## 🔗 Cross-Reference Map

| Stack | Depends on | Used by |
|-------|-----------|---------|
| [Frontend](frontend/INDEX.md) | — | Both lanes |
| [Backend](backend/INDEX.md) | — | Both lanes |
| [Architecture](architecture/INDEX.md) | — | Both lanes |
| [Platform](platform/INDEX.md) | — | Both lanes |
| [Quality](quality/INDEX.md) | — | Both lanes |
| [Real-Time](realtime/INDEX.md) | — | Abroad Full-Stack (occasionally) |
| [Interview Toolkit](interview-toolkit/INDEX.md) | All stacks | Both lanes (Indian SDE / FAANG heavy, Abroad Full-Stack light) |
| [Interview Lanes](lanes/INDEX.md) | All stacks | Terminal phase |

---

## 📂 Direct Indexes

**Lanes:**

- [Interview Strategy/index](strategy/INDEX.md) — Cross-lane strategy
- [Indian SDE / FAANG/index](lanes/indian-sde-faang/INDEX.md) — Indian SDE / FAANG lane
- [Abroad Full-Stack/index](lanes/abroad-full-stack/INDEX.md) — Abroad Full-Stack lane

**Stacks:**

- **Frontend** — [JavaScript](frontend/javascript/INDEX.md) · [TypeScript](frontend/typescript/INDEX.md) · [React](frontend/react/INDEX.md) · [Next.js](frontend/nextjs/INDEX.md) · [Form Handling](frontend/form-handling/INDEX.md) · [Animation](frontend/animation/INDEX.md)
- **Backend** — [Node.js](backend/nodejs/INDEX.md) · [NestJS](backend/nestjs/INDEX.md) · [REST APIs](backend/rest-api/INDEX.md) · [Database](backend/database/INDEX.md) · [Security](backend/security/INDEX.md) · [Design Patterns](backend/design-patterns/INDEX.md) · [Microservices](backend/microservices/INDEX.md) · [GraphQL](backend/graphql/INDEX.md)
- **Architecture** — [System Design](architecture/system-design/INDEX.md)
- **Platform** — [Docker](platform/docker/INDEX.md) · [Kubernetes](platform/kubernetes/INDEX.md) · [CI/CD](platform/ci-cd/INDEX.md) · [Observability](platform/observability/INDEX.md) · [Build Tools](platform/build-tools/INDEX.md) · [Git Advanced](platform/git-advanced/INDEX.md) · [Serverless & Edge](platform/serverless-edge/INDEX.md) · [Monorepo](platform/monorepo/INDEX.md)
- **Quality** — [Testing](quality/testing/INDEX.md) · [Accessibility](quality/accessibility/INDEX.md) · [Performance Monitoring](quality/performance-monitoring/INDEX.md)
- **Real-Time** — [WebSockets](realtime/websockets/INDEX.md)
- **Interview Toolkit** — [Behavioral](interview-toolkit/behavioral/INDEX.md) · [Coding Patterns](interview-toolkit/coding-patterns/INDEX.md) · [Cheat Sheets](interview-toolkit/cheatsheets/INDEX.md)

---

*Last updated: August 2026 — 3 lanes, 7 stacks, 400+ files, 0 broken links*
