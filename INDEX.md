# Senior Full Stack Interview Bible — Index

> **Complete navigation hub** — 33 sections, 316+ files, covering the full spectrum of senior full-stack engineering interview preparation across three job-market lanes: **interview strategy** (cross-lane), **Indian SDE / FAANG** (DSA-heavy), and **abroad full-stack** (take-home + system design).

[![Sections](https://img.shields.io/badge/sections-33-blue)](INDEX.md)
[![Files](https://img.shields.io/badge/files-316%2B-green)](INDEX.md)
[![Last Updated](https://img.shields.io/badge/last%20updated-August%202026-orange)](INDEX.md)

---

## 🎯 Pick Your Lane First

The bible is organized around **three job-market lanes**. Pick yours before diving in:

| Lane | Folder | For | Style |
|------|--------|-----|-------|
| **Interview Strategy** (cross-lane) | [00-Interview-Strategy/](00-Interview-Strategy/) | Everyone | Communication, HR, Resume, STAR framework |
| **Indian SDE / FAANG** | [31-SDE-Role/](31-SDE-Role/) | Microsoft, Google, Amazon, Meta, Apple, in-country India | LeetCode-heavy, 8-week intensive, USD 150K-400K+ |
| **Abroad Full-Stack** | [32-Abroad-Full-Stack-Lane/](32-Abroad-Full-Stack-Lane/) | EU / non-Indian mid-stage startups (n8n, SumUp, Scalable, sennder) | Take-home + system design, 4-week plan, EUR 70-110K + visa |

**Not sure?** Default to the cross-lane interview strategy + the lane that matches your target companies. If you're in between (e.g., Booking.com, Spotify, Stripe, remote-first US), use both lanes — start with `31-SDE-Role/` for the FAANG-DSA signal, then `32-Abroad-Full-Stack-Lane/` for the EU-specific family/visa overlay.

---

## 🎯 Quick Navigation

| Jump to |
|---------|
| [Core Fundamentals](#core-fundamentals) · [Backend & Databases](#backend--databases) · [Architecture & Design](#architecture--design) · [DevOps & Infrastructure](#devops--infrastructure) · [Testing & Quality](#testing--quality) · [Real-Time & Communication](#real-time--communication) · [Interview & Career](#interview--career) · [Quick Reference](#quick-reference) |
| [Recommended Study Path](#recommended-study-path) · [Cross-Reference Map](#-cross-reference-map) · [File Indexes](#-section-indexes) |

---

## Core Fundamentals

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 00 | [Interview Strategy](00-Interview-Strategy/) | 4 | `Interview` | Communication, HR, Resume, STAR Method |
| 01 | [JavaScript](01-JavaScript/) | 27 | `Core` | Execution Context, Call Stack, Hoisting, Closures, Scope, Lexical Environment, `this`, Prototypes, Event Loop, Promises, Async/Await, Error Handling, Pass-by-Value, Map/Set/WeakMap, Shallow/Deep Copy, Proxy/Reflect, Debounce, Throttle, Memory Leaks, GC, Modules, Memoization, Generators, Currying/Composition, Recursion/TCO, ES2024 |
| 02 | [TypeScript](02-TypeScript/) | 15 | `Core` | Types vs Interfaces, Generics, Utility Types, Conditional Types, Infer, keyof/typeof, Mapped Types, Narrowing, Decorators, Advanced Generics, `satisfies` Operator |
| 03 | [React](03-React/) | 19 | `Frontend` | Virtual DOM, Fiber, Reconciliation, Rendering, Lifecycle, useState, useEffect, useMemo/useCallback, useRef, Context API, Suspense, Error Boundary, Performance, State Management, Modern Hooks (React 18-19) |
| 04 | [Next.js](04-NextJS/) | 16 | `Frontend` | SSR/CSR/SSG/ISR, App Router, Server Components, Client Components, Middleware, Server Actions, Route Handlers, Metadata, Caching, Streaming, Image Optimization, Data Fetching Patterns |

## Backend, API & Data

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 05 | [Node.js](05-NodeJS/) | 11 | `Backend` | Event Loop, Streams, Buffers, Clustering, File System, HTTP Module, Child Processes/Workers, Process/Environment, Node Security, Web Streams & Test Runner |
| 06 | [NestJS](06-NestJS/) | 14 | `Backend` | Modules, Controllers, Providers, DI, Guards, Pipes, Interceptors, Middleware, Exception Filters, CQRS, Microservices, Testing, Configuration Validation |
| 07 | [REST APIs](07-REST-API/) | 13 | `API` | Principles, HTTP Methods, Status Codes, Versioning, Pagination, Auth, Rate Limiting, CORS, API Gateway, OpenAPI/Swagger, Error Handling, HTTP Caching |
| 08 | [Database](08-Database/) | 14 | `Data` | PostgreSQL, Normalization, Indexes, Transactions, MVCC, Joins, Deadlocks, Locking, Connection Pooling, Prisma, Execution Plans, NoSQL vs SQL, Migration Strategies |
| 17 | [GraphQL](17-GraphQL/) | 8 | `API` | Overview, Schema Design, Queries/Mutations, Resolvers, Apollo Server, Apollo Client, Performance & Security |

## Architecture & Design

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 09 | [Security](09-Security/) | 13 | `Architecture` | JWT, OAuth, XSS, CSRF, SQL Injection, Encryption, RBAC, Session/Cookies, Web Security, Threat Modeling (STRIDE), Secrets Management, API Security Best Practices |
| 10 | [Design Patterns](10-Design-Patterns/) | 15 | `Architecture` | Singleton, Factory, Strategy, Observer, Repository, Builder, Adapter, Facade, Decorator, Proxy, Chain of Responsibility, CQRS/DI, Module Pattern, State Pattern |
| 11 | [System Design](11-System-Design/) | 22 | `Architecture` | URL Shortener, WhatsApp, Uber, Netflix, Google Drive, Payment Gateway, Notification Service, Ticket Booking, E-Commerce, Hospital Mgmt, Live Betting, How to Approach, Instagram, YouTube, Dropbox, Lyft, Distributed Counter |
| 12 | [Microservices](12-Microservices/) | 14 | `Architecture` | Service Discovery, API Gateway, Saga, Circuit Breaker, Kafka, RabbitMQ, Event Sourcing, gRPC, Service Mesh, Distributed Transactions |

## DevOps, Observability & Tooling

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 13 | [Docker](13-Docker/) | 6 | `DevOps` | Images & Containers, Volumes & Networks, Compose, Multi-Stage Builds, Dockerfile Best Practices & Security |
| 14 | [Kubernetes](14-Kubernetes/) | 14 | `DevOps` | Pods & ReplicaSets, Deployments, Services & Ingress, ConfigMaps & Secrets, HPA, Health Checks, Helm, StatefulSets, Jobs, RBAC & Network Policies, PodDisruptionBudgets, ResourceQuotas, PodPresets |
| 15 | [CI/CD](15-CI-CD/) | 7 | `DevOps` | GitHub Actions, Docker Build & Deploy, Blue-Green & Canary, Jenkins, GitLab CI, ArgoCD (GitOps) |
| 22 | [Observability](22-Observability/) | 8 | `Observability` | Logging, Monitoring, Tracing, Error Tracking, Health Checks, SLI/SLO/SLA, Alerting |
| 23 | [Build Tools](23-Build-Tools/) | 9 | `Tooling` | Webpack, Vite, Turbopack, Build Optimization, Babel, ESBuild & SWC, Rspack, Tool Comparison |
| 24 | [Git Advanced](24-Git-Advanced/) | 7 | `Tooling` | Branching Strategies, Rebase/Cherry-Pick, Hooks, Commands, Patch & Bundle, Code Archaeology |
| 27 | [Serverless & Edge](27-Serverless-Edge/) | 7 | `DevOps` | Overview, Edge Functions, Serverless Patterns, AWS Lambda, Vercel, Frameworks (SAM/CDK/SST) |

## Testing & Quality

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 16 | [Testing](16-Testing/) | 11 | `Quality` | Overview, Jest, RTL, Unit, Integration, E2E, Mocking, Test Patterns, Vitest, Performance/Load Testing |
| 25 | [Accessibility](25-Accessibility/) | 7 | `Quality` | WCAG, ARIA, Keyboard Navigation, Testing A11y, Color & Contrast, Forms & Labels |
| 26 | [Performance Monitoring](26-Performance-Monitoring/) | 8 | `Quality` | Core Web Vitals, Performance APIs, Profiling Tools, Lighthouse CI, Bundle Analysis, Real User Monitoring, Performance Budgets |

## Real-Time & Communication

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 21 | [WebSockets](21-WebSockets/) | 8 | `Real-Time` | Overview, Socket.IO, SSE, Real-Time Architecture, NestJS WebSockets, WebTransport, Scaling Patterns |

## Interview & Career

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 18 | [Behavioral](18-Behavioral/) | 4 | `Interview` | STAR Method, HR Questions, Leadership Questions, System Design Behavioral |
| 19 | [Coding Patterns](19-Coding-Patterns/) | 18 | `Interview` | Sliding Window, Two Pointers, Binary Search, DFS/BFS, Backtracking, DP, Heap, Trie, Union Find, Topological Sort, Intervals, Greedy/Prefix Sum, Monotonic Stack, Segment Tree & BIT, Bit Manipulation, String Search (KMP/Rabin-Karp), Quick Select & Reservoir Sampling, Stack & Queue Patterns |
| 31 | [SDE Role — Indian / FAANG Lane](31-SDE-Role/) | 22 | `Interview` | Complete Guide, CS Fundamentals, System Design, DevOps, Advanced Topics + Study Tools (06-15) + Company Guides (16-20). **Indian SDE / FAANG lane — DSA-heavy, 8-week intensive.** |
| 32 | [Abroad Full-Stack Lane](32-Abroad-Full-Stack-Lane/) | 2 | `Interview` | Personal story bank (STAR+R) + 4-week EU mid-stage preparation plan. **Abroad full-stack lane — take-home + system design, no LeetCode grinding.** |

## Reference & Quick-Look

| # | Section | Files | Category | Topics |
|---|---------|------:|----------|--------|
| 20 | [CheatSheets](20-CheatSheets/) | 5 | `Reference` | JavaScript, TypeScript, React/Next.js, Backend, System Design |
| 28 | [Monorepo](28-Monorepo/) | 5 | `Reference` | Overview, Turborepo, Nx, Monorepo Tools (pnpm/Rush/Bazel) |
| 29 | [Form Handling](29-Form-Handling/) | 6 | `Frontend` | React Hook Form, Zod, Formik, TanStack Form, Server Actions & Form Patterns |
| 30 | [Animation](30-Animation/) | 7 | `Frontend` | Framer Motion, CSS Animations, Web Animations API, GSAP, React Spring, View Transitions & Scroll-Driven |

---

## Recommended Study Path

The bible has two parallel interview-prep lanes at the end. Pick yours first, then follow the phase path:

```text
Lane A — Indian SDE / FAANG (use 31):
  Phase 1 — Core JS/TS:    00 → 01 → 02
  Phase 2 — Frontend:      03 → 04 → 29 → 30
  Phase 3 — Backend:       05 → 06 → 07 → 08 → 17
  Phase 4 — Architecture:  09 → 10 → 11 → 12
  Phase 5 — DevOps:        13 → 14 → 15 → 22 → 23 → 27
  Phase 6 — Quality:       16 → 25 → 26
  Phase 7 — Real-Time:     21
  Phase 8 — Interview Prep: 18 → 19 → 20 → 24 → 28 → 31

Lane B — Abroad Full-Stack (use 32):
  Phase 1 — Core JS/TS:    00 → 01 → 02
  Phase 2 — Frontend:      03 → 04 → 29 → 30
  Phase 3 — Backend:       05 → 06 → 07 → 08 → 17
  Phase 4 — Architecture:  09 → 10 → 11 → 12
  Phase 5 — DevOps:        13 → 14 → 15 → 22 → 23 → 27
  Phase 6 — Quality:       16 → 25 → 26
  Phase 7 — Real-Time:     21
  Phase 8 — Interview Prep: 18 → 19 → 20 → 24 → 28 → 32
```

The two lanes share Phases 1-7 (core technical knowledge). They diverge at Phase 8: Lane A (31-SDE-Role) is LeetCode-heavy with 8-week FAANG schedule; Lane B (32-Abroad-Full-Stack-Lane) is take-home + system design heavy with 4-week realistic plan.

---

## 🔗 Cross-Reference Map

| Section | Related Sections |
|---------|------------------|
| **[JavaScript](01-JavaScript/)** | TypeScript, Node.js, Coding Patterns |
| **[TypeScript](02-TypeScript/)** | JavaScript, React, NestJS, Form Handling |
| **[React](03-React/)** | JavaScript, Next.js, Testing, Form Handling, Animation |
| **[Next.js](04-NextJS/)** | React, Serverless & Edge, Performance Monitoring |
| **[Node.js](05-NodeJS/)** | JavaScript, NestJS, Docker |
| **[NestJS](06-NestJS/)** | Node.js, REST APIs, Microservices, Design Patterns |
| **[REST APIs](07-REST-API/)** | NestJS, Security, System Design, Microservices |
| **[Database](08-Database/)** | REST APIs, System Design, Performance Monitoring |
| **[Security](09-Security/)** | REST APIs, System Design |
| **[Design Patterns](10-Design-Patterns/)** | NestJS, JavaScript, System Design, Coding Patterns |
| **[System Design](11-System-Design/)** | Microservices, Database, REST APIs, WebSockets |
| **[Microservices](12-Microservices/)** | NestJS, System Design, Docker, Kubernetes |
| **[Docker](13-Docker/)** | Kubernetes, CI/CD, Microservices |
| **[Kubernetes](14-Kubernetes/)** | Docker, CI/CD, Observability, Serverless & Edge |
| **[CI/CD](15-CI-CD/)** | Docker, Kubernetes, Git Advanced |
| **[Testing](16-Testing/)** | React, NestJS, CI/CD, Coding Patterns |
| **[GraphQL](17-GraphQL/)** | REST APIs, React, NestJS |
| **[Behavioral](18-Behavioral/)** | Interview Strategy, SDE Role |
| **[Coding Patterns](19-Coding-Patterns/)** | JavaScript, System Design, SDE Role |
| **[CheatSheets](20-CheatSheets/)** | JavaScript, TypeScript, React, System Design |
| **[WebSockets](21-WebSockets/)** | System Design, NestJS, Observability |
| **[Observability](22-Observability/)** | Kubernetes, Performance Monitoring, Serverless & Edge |
| **[Build Tools](23-Build-Tools/)** | React, Next.js, Performance Monitoring |
| **[Git Advanced](24-Git-Advanced/)** | CI/CD, Monorepo |
| **[Accessibility](25-Accessibility/)** | React, Testing, Performance Monitoring |
| **[Performance Monitoring](26-Performance-Monitoring/)** | React, Build Tools, Observability, Accessibility |
| **[Serverless & Edge](27-Serverless-Edge/)** | Next.js, Docker, Observability |
| **[Monorepo](28-Monorepo/)** | Build Tools, Git Advanced, CI/CD |
| **[Form Handling](29-Form-Handling/)** | React, TypeScript, Design Patterns |
| **[Animation](30-Animation/)** | React, Performance Monitoring |
| **[SDE Role](31-SDE-Role/)** | JavaScript, TypeScript, React, System Design, Behavioral, Coding Patterns |
| **[Abroad Full-Stack Lane](32-Abroad-Full-Stack-Lane/)** | JavaScript, TypeScript, React, Next.js, NestJS, System Design, Behavioral, Coding Patterns (sibling lane of 31) |

---

## 📂 Section Indexes

Each section now has its own `INDEX.md` file with a detailed file listing and topic descriptions:

| # | Section | INDEX.md |
|---|---------|----------|
| 00 | Interview Strategy | [`00-Interview-Strategy/INDEX.md`](00-Interview-Strategy/INDEX.md) |
| 01 | JavaScript | [`01-JavaScript/INDEX.md`](01-JavaScript/INDEX.md) |
| 02 | TypeScript | [`02-TypeScript/INDEX.md`](02-TypeScript/INDEX.md) |
| 03 | React | [`03-React/INDEX.md`](03-React/INDEX.md) |
| 04 | Next.js | [`04-NextJS/INDEX.md`](04-NextJS/INDEX.md) |
| 05 | Node.js | [`05-NodeJS/INDEX.md`](05-NodeJS/INDEX.md) |
| 06 | NestJS | [`06-NestJS/INDEX.md`](06-NestJS/INDEX.md) |
| 07 | REST APIs | [`07-REST-API/INDEX.md`](07-REST-API/INDEX.md) |
| 08 | Database | [`08-Database/INDEX.md`](08-Database/INDEX.md) |
| 09 | Security | [`09-Security/INDEX.md`](09-Security/INDEX.md) |
| 10 | Design Patterns | [`10-Design-Patterns/INDEX.md`](10-Design-Patterns/INDEX.md) |
| 11 | System Design | [`11-System-Design/INDEX.md`](11-System-Design/INDEX.md) |
| 12 | Microservices | [`12-Microservices/INDEX.md`](12-Microservices/INDEX.md) |
| 13 | Docker | [`13-Docker/INDEX.md`](13-Docker/INDEX.md) |
| 14 | Kubernetes | [`14-Kubernetes/INDEX.md`](14-Kubernetes/INDEX.md) |
| 15 | CI/CD | [`15-CI-CD/INDEX.md`](15-CI-CD/INDEX.md) |
| 16 | Testing | [`16-Testing/INDEX.md`](16-Testing/INDEX.md) |
| 17 | GraphQL | [`17-GraphQL/INDEX.md`](17-GraphQL/INDEX.md) |
| 18 | Behavioral | [`18-Behavioral/INDEX.md`](18-Behavioral/INDEX.md) |
| 19 | Coding Patterns | [`19-Coding-Patterns/INDEX.md`](19-Coding-Patterns/INDEX.md) |
| 20 | CheatSheets | [`20-CheatSheets/INDEX.md`](20-CheatSheets/INDEX.md) |
| 21 | WebSockets | [`21-WebSockets/INDEX.md`](21-WebSockets/INDEX.md) |
| 22 | Observability | [`22-Observability/INDEX.md`](22-Observability/INDEX.md) |
| 23 | Build Tools | [`23-Build-Tools/INDEX.md`](23-Build-Tools/INDEX.md) |
| 24 | Git Advanced | [`24-Git-Advanced/INDEX.md`](24-Git-Advanced/INDEX.md) |
| 25 | Accessibility | [`25-Accessibility/INDEX.md`](25-Accessibility/INDEX.md) |
| 26 | Performance Monitoring | [`26-Performance-Monitoring/INDEX.md`](26-Performance-Monitoring/INDEX.md) |
| 27 | Serverless & Edge | [`27-Serverless-Edge/INDEX.md`](27-Serverless-Edge/INDEX.md) |
| 28 | Monorepo | [`28-Monorepo/INDEX.md`](28-Monorepo/INDEX.md) |
| 29 | Form Handling | [`29-Form-Handling/INDEX.md`](29-Form-Handling/INDEX.md) |
| 30 | Animation | [`30-Animation/INDEX.md`](30-Animation/INDEX.md) |
| 31 | SDE Role — Indian / FAANG Lane | [`31-SDE-Role/INDEX.md`](31-SDE-Role/INDEX.md) |
| 32 | Abroad Full-Stack Lane | [`32-Abroad-Full-Stack-Lane/INDEX.md`](32-Abroad-Full-Stack-Lane/INDEX.md) |

---

*Last updated: August 2026 — 33 sections, 316+ files, 33 INDEX.md files*
