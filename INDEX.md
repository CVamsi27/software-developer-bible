# Senior Full Stack Interview Bible — Index

> **Pick your lane first.** The bible is organized into **3 interview lanes** that draw from **7 shared study stacks**. Each lane has its own preparation strategy; the stacks are the technical material both lanes share.

[![Lanes](https://img.shields.io/badge/lanes-3-blue)](INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-7-green)](INDEX.md)
[![Files](https://img.shields.io/badge/files-400%2B-orange)](INDEX.md)
[![Last Updated](https://img.shields.io/badge/last%20updated-August%202026-purple)](INDEX.md)

---

## 🎯 Pick Your Lane

| Lane | Folder | For | Style |
|------|--------|-----|-------|
| **Cross-Lane** (everyone starts here) | [0-Interview-Strategy/](0-Interview-Strategy/) | Communication, resume, STAR method, HR questions | Universal — applies to all lanes |
| **Indian SDE / FAANG** | [8-Interview-Lanes/1-Indian-SDE-FAANG/](8-Interview-Lanes/1-Indian-SDE-FAANG/) | Microsoft, Google, Amazon, Meta, Apple, in-country India | LeetCode-heavy, 8-week intensive, USD 150-400K+ |
| **Abroad Full-Stack** | [8-Interview-Lanes/2-Abroad-Full-Stack/](8-Interview-Lanes/2-Abroad-Full-Stack/) | EU / non-Indian mid-stage startups (n8n, SumUp, Scalable, sennder) | Take-home + system design, 4-week plan, EUR 70-110K + visa |

**Not sure?** Read the [lane decision matrix in 2-Abroad-Full-Stack](8-Interview-Lanes/2-Abroad-Full-Stack/INDEX.md). If you're in between (e.g., Booking.com, Spotify, Stripe, remote-first US), use both lanes — start with `1-Indian-SDE-FAANG/` for the FAANG-DSA signal, then `2-Abroad-Full-Stack/` for the EU-specific family/visa overlay.

---

## 📚 The 7 Study Stacks (shared by both lanes)

The technical material is grouped by **what you're studying**, not by which interview you're prepping for. Both lanes pull from the same stacks.

### Frontend Stack — [1-Frontend-Stack/](1-Frontend-Stack/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 01 | [JavaScript](1-Frontend-Stack/01-JavaScript/) | 27 | Execution context, closures, prototypes, event loop, promises, async/await, ES2024 |
| 02 | [TypeScript](1-Frontend-Stack/02-TypeScript/) | 15 | Generics, utility types, conditional types, narrowing, `satisfies` operator |
| 03 | [React](1-Frontend-Stack/03-React/) | 19 | Virtual DOM, Fiber, hooks (18-19), Suspense, performance, state management |
| 04 | [Next.js](1-Frontend-Stack/04-NextJS/) | 16 | App Router, Server Components, Server Actions, Middleware, caching, streaming |
| 29 | [Form Handling](1-Frontend-Stack/29-Form-Handling/) | 6 | React Hook Form, Zod, Formik, TanStack Form, Server Actions |
| 30 | [Animation](1-Frontend-Stack/30-Animation/) | 7 | Framer Motion, CSS Animations, GSAP, React Spring, View Transitions |

### Backend Stack — [2-Backend-Stack/](2-Backend-Stack/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 05 | [Node.js](2-Backend-Stack/05-NodeJS/) | 11 | Event loop, streams, clustering, web streams, child processes, test runner |
| 06 | [NestJS](2-Backend-Stack/06-NestJS/) | 14 | Modules, DI, guards, pipes, interceptors, CQRS, microservices |
| 07 | [REST APIs](2-Backend-Stack/07-REST-API/) | 13 | HTTP methods, status codes, versioning, pagination, auth, OpenAPI, caching |
| 08 | [Database](2-Backend-Stack/08-Database/) | 14 | PostgreSQL, indexes, transactions, MVCC, Prisma, query planning, migrations |
| 09 | [Security](2-Backend-Stack/09-Security/) | 13 | JWT, OAuth, XSS, CSRF, RBAC, threat modeling, secrets management |
| 10 | [Design Patterns](2-Backend-Stack/10-Design-Patterns/) | 15 | Singleton, Factory, Strategy, Repository, CQRS, Module, State |
| 12 | [Microservices](2-Backend-Stack/12-Microservices/) | 14 | Service discovery, saga, circuit breaker, event sourcing, gRPC, service mesh |
| 17 | [GraphQL](2-Backend-Stack/17-GraphQL/) | 8 | Schema design, queries/mutations, Apollo Server, performance, security |

### Architecture Stack — [3-Architecture-Stack/](3-Architecture-Stack/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 11 | [System Design](3-Architecture-Stack/11-System-Design/) | 22 | URL shortener, WhatsApp, Uber, Netflix, payment gateway, ticket booking, 17 case studies |

### Platform Stack — [4-Platform-Stack/](4-Platform-Stack/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 13 | [Docker](4-Platform-Stack/13-Docker/) | 6 | Images, containers, volumes, networks, compose, multi-stage builds |
| 14 | [Kubernetes](4-Platform-Stack/14-Kubernetes/) | 14 | Pods, deployments, services, ingress, ConfigMaps, HPA, Helm, RBAC |
| 15 | [CI/CD](4-Platform-Stack/15-CI-CD/) | 7 | GitHub Actions, Docker build/deploy, blue-green/canary, Jenkins, GitLab CI, ArgoCD |
| 22 | [Observability](4-Platform-Stack/22-Observability/) | 8 | Logging, monitoring, tracing, error tracking, SLI/SLO/SLA, alerting |
| 23 | [Build Tools](4-Platform-Stack/23-Build-Tools/) | 9 | Webpack, Vite, Turbopack, Rspack, ESBuild, SWC, Babel |
| 24 | [Git Advanced](4-Platform-Stack/24-Git-Advanced/) | 7 | Branching, rebase, cherry-pick, hooks, patch workflow, code archaeology |
| 27 | [Serverless & Edge](4-Platform-Stack/27-Serverless-Edge/) | 7 | Lambda, Vercel Edge, serverless patterns, SAM/CDK/SST |
| 28 | [Monorepo](4-Platform-Stack/28-Monorepo/) | 5 | Turborepo, Nx, pnpm, Rush, Bazel |

### Quality Stack — [5-Quality-Stack/](5-Quality-Stack/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 16 | [Testing](5-Quality-Stack/16-Testing/) | 11 | Jest, RTL, unit, integration, E2E, mocking, Vitest, load testing |
| 25 | [Accessibility](5-Quality-Stack/25-Accessibility/) | 7 | WCAG, ARIA, keyboard navigation, color contrast, forms & labels |
| 26 | [Performance Monitoring](5-Quality-Stack/26-Performance-Monitoring/) | 8 | Core Web Vitals, profiling, Lighthouse CI, bundle analysis, RUM |

### Real-Time Stack — [6-Real-Time-Stack/](6-Real-Time-Stack/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 21 | [WebSockets](6-Real-Time-Stack/21-WebSockets/) | 8 | Socket.IO, SSE, real-time architecture, NestJS WebSockets, WebTransport |

### Interview Toolkit — [7-Interview-Toolkit/](7-Interview-Toolkit/)

| # | Section | Files | Topics |
|---|---------|------:|--------|
| 18 | [Behavioral](7-Interview-Toolkit/18-Behavioral/) | 4 | STAR method, HR questions, leadership questions, system design behavioral |
| 19 | [Coding Patterns](7-Interview-Toolkit/19-Coding-Patterns/) | 18 | Sliding window, two pointers, BFS/DFS, DP, heap, trie, union find, backtracking |
| 20 | [Cheat Sheets](7-Interview-Toolkit/20-CheatSheets/) | 5 | JavaScript, TypeScript, React/Next.js, backend, system design |

---

## 🛣️ Recommended Study Path

After you pick your lane (above), the two lanes share Phases 1-7 (the 7 study stacks). They diverge at Phase 8 (Interview Prep).

```text
Phase 1 — Frontend Stack:      1-Frontend-Stack/01-JavaScript → 02-TypeScript → 03-React → 04-NextJS → 29-Form-Handling → 30-Animation
Phase 2 — Backend Stack:       2-Backend-Stack/05-NodeJS → 06-NestJS → 07-REST-API → 08-Database → 17-GraphQL → 09-Security → 10-Design-Patterns → 12-Microservices
Phase 3 — Architecture Stack:  3-Architecture-Stack/11-System-Design
Phase 4 — Platform Stack:      4-Platform-Stack/13-Docker → 14-Kubernetes → 15-CI-CD → 22-Observability → 23-Build-Tools → 24-Git-Advanced → 27-Serverless-Edge → 28-Monorepo
Phase 5 — Quality Stack:       5-Quality-Stack/16-Testing → 25-Accessibility → 26-Performance-Monitoring
Phase 6 — Real-Time Stack:     6-Real-Time-Stack/21-WebSockets
Phase 7 — Cross-Lane:          0-Interview-Strategy + 7-Interview-Toolkit/18-Behavioral
Phase 8 — Lane-Specific Prep:
  → Indian SDE / FAANG:        7-Interview-Toolkit/19-Coding-Patterns + 8-Interview-Lanes/1-Indian-SDE-FAANG (8-week plan)
  → Abroad Full-Stack:         7-Interview-Toolkit/20-CheatSheets + 8-Interview-Lanes/2-Abroad-Full-Stack (4-week plan)
```

**For Lane 81 (FAANG):** Phase 8 is heavy on `19-Coding-Patterns/` (18 files, all patterns). 8-12 week intensive, 4-6 hrs/day.
**For Lane 82 (EU):** Phase 8 is light on coding patterns (30-40 mediums, 6 patterns), heavy on system design + take-home prep. 4-week realistic, 2-3 hrs/day.

---

## 🔗 Cross-Reference Map

| Stack | Depends on | Used by |
|-------|-----------|---------|
| [10-Frontend](1-Frontend-Stack/) | — | 81, 82 |
| [20-Backend](2-Backend-Stack/) | 10 | 81, 82 |
| [30-Architecture](3-Architecture-Stack/) | 20 | 81, 82 |
| [40-Platform](4-Platform-Stack/) | 20 | 81, 82 |
| [50-Quality](5-Quality-Stack/) | 10, 20 | 81, 82 |
| [60-Real-Time](6-Real-Time-Stack/) | 20 | 82 (occasionally) |
| [7-Interview-Toolkit](7-Interview-Toolkit/) | All stacks | 81 (heavy), 82 (light) |
| [8-Interview-Lanes](8-Interview-Lanes/) | All stacks | (terminal phase) |

---

## 📂 Direct Indexes

**Lanes:**

- [0-Interview-Strategy/INDEX.md](0-Interview-Strategy/INDEX.md) — Cross-lane strategy
- [8-Interview-Lanes/1-Indian-SDE-FAANG/INDEX.md](8-Interview-Lanes/1-Indian-SDE-FAANG/INDEX.md) — Indian SDE / FAANG lane
- [8-Interview-Lanes/2-Abroad-Full-Stack/INDEX.md](8-Interview-Lanes/2-Abroad-Full-Stack/INDEX.md) — Abroad full-stack lane

**Stacks:**

- [1-Frontend-Stack/01-JavaScript/INDEX.md](1-Frontend-Stack/01-JavaScript/INDEX.md) · [02-TypeScript](1-Frontend-Stack/02-TypeScript/INDEX.md) · [03-React](1-Frontend-Stack/03-React/INDEX.md) · [04-NextJS](1-Frontend-Stack/04-NextJS/INDEX.md) · [29-Form-Handling](1-Frontend-Stack/29-Form-Handling/INDEX.md) · [30-Animation](1-Frontend-Stack/30-Animation/INDEX.md)
- [2-Backend-Stack/05-NodeJS/INDEX.md](2-Backend-Stack/05-NodeJS/INDEX.md) · [06-NestJS](2-Backend-Stack/06-NestJS/INDEX.md) · [07-REST-API](2-Backend-Stack/07-REST-API/INDEX.md) · [08-Database](2-Backend-Stack/08-Database/INDEX.md) · [09-Security](2-Backend-Stack/09-Security/INDEX.md) · [10-Design-Patterns](2-Backend-Stack/10-Design-Patterns/INDEX.md) · [12-Microservices](2-Backend-Stack/12-Microservices/INDEX.md) · [17-GraphQL](2-Backend-Stack/17-GraphQL/INDEX.md)
- [3-Architecture-Stack/11-System-Design/INDEX.md](3-Architecture-Stack/11-System-Design/INDEX.md)
- [4-Platform-Stack/13-Docker/INDEX.md](4-Platform-Stack/13-Docker/INDEX.md) · [14-Kubernetes](4-Platform-Stack/14-Kubernetes/INDEX.md) · [15-CI-CD](4-Platform-Stack/15-CI-CD/INDEX.md) · [22-Observability](4-Platform-Stack/22-Observability/INDEX.md) · [23-Build-Tools](4-Platform-Stack/23-Build-Tools/INDEX.md) · [24-Git-Advanced](4-Platform-Stack/24-Git-Advanced/INDEX.md) · [27-Serverless-Edge](4-Platform-Stack/27-Serverless-Edge/INDEX.md) · [28-Monorepo](4-Platform-Stack/28-Monorepo/INDEX.md)
- [5-Quality-Stack/16-Testing/INDEX.md](5-Quality-Stack/16-Testing/INDEX.md) · [25-Accessibility](5-Quality-Stack/25-Accessibility/INDEX.md) · [26-Performance-Monitoring](5-Quality-Stack/26-Performance-Monitoring/INDEX.md)
- [6-Real-Time-Stack/21-WebSockets/INDEX.md](6-Real-Time-Stack/21-WebSockets/INDEX.md)
- [7-Interview-Toolkit/18-Behavioral/INDEX.md](7-Interview-Toolkit/18-Behavioral/INDEX.md) · [19-Coding-Patterns](7-Interview-Toolkit/19-Coding-Patterns/INDEX.md) · [20-CheatSheets](7-Interview-Toolkit/20-CheatSheets/INDEX.md)

---

*Last updated: August 2026 — 3 lanes, 7 stacks, 400+ files, 33 INDEX.md files*
