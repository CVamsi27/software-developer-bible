# Senior Full Stack Interview Bible — Index

> **Study time:** ≈ 176 h 59 m of reading (560 files, ~19 min average).
> **Start here: [ROADMAP.md](ROADMAP.md) — the canonical study path with phases, checkpoints, and weekly schedule.**
>
> **Pick your lane first.** The bible is organized into **2 interview lanes** (`80-lanes-abroad-full-stack`, `81-lanes-indian-sde-faang`) that draw from **7 shared study stacks** — plus the [00-strategy](00-strategy/INDEX.md) **strategy folder** everyone starts with. Each lane has its own preparation strategy; the stacks are the technical material both lanes share.
>
> **Folders are numbered for the recommended study order.** `00-` is everyone starts here. `10-` through `60-` are the 7 technical stacks in dependency order. `70-` is interview toolkit. `80-` and `81-` are the two lanes.

[![Lanes](https://img.shields.io/badge/lanes-2-blue)](lanes/INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-7-green)](#the-7-study-stacks-numbered-for-study-order)
[![Files](https://img.shields.io/badge/files-867-orange)](#the-7-study-stacks-numbered-for-study-order)
[![Design Patterns](https://img.shields.io/badge/GoF%20Coverage-23%2F23-success)](30-architecture/30.1-design-patterns/INDEX.md)
[![Last Updated](https://img.shields.io/badge/last%20updated-September%202026-purple)](#)

---

## Pick Your Lane

**Everyone starts with the [00-strategy](00-strategy/INDEX.md) strategy folder** — communication, resume, STAR, HR questions — it is shared by both lanes, not a lane itself. Then pick one of the two lanes:

| Lane | Folder | For | Style |
| ------------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Abroad Full-Stack** (recommended for EU) | [80-lanes-abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md) | EU / non-Indian mid-stage startups (n8n, SumUp, Langfuse, sennder) | Take-home + system design, 4-week plan, EUR 75-100K + equity, visa |
| **Indian SDE / FAANG** | [81-lanes-indian-sde-faang](81-lanes-indian-sde-faang/INDEX.md) | Microsoft, Google, Amazon, Meta, Apple, in-country India | LeetCode-heavy, 8-week intensive, USD 150-400K+ |

**Not sure?** Read the [lane decision matrix in abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md#lane-decision--is-this-the-right-lane-for-you). If you're in between (e.g., Booking.com, Spotify, Stripe, remote-first US), use both lanes — start with `81-lanes-indian-sde-faang/` for the FAANG-DSA signal, then `80-lanes-abroad-full-stack/` for the EU-specific family/visa overlay.

---

## The 7 Study Stacks (numbered for study order)

The technical material is grouped by **what you're studying**, not by which interview you're prepping for. Both lanes pull from the same stacks. **The number prefix tells you the recommended study order.**

### Study order cheat sheet

| Order | Folder | Topic | Time | When |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | --------- | ------------------------- |
| 1 | [00-strategy](00-strategy/INDEX.md) | Interview strategy (resume, STAR, comm) | 1-2 days | **Always** |
| 2 | [10-frontend](10-frontend/INDEX.md) | Frontend (JS → TS → React → Next.js) | 2-3 weeks | Before any senior screen |
| 3 | [20-backend](20-backend/INDEX.md) | Backend (Node → NestJS → REST → DB → Security) | 2-3 weeks | Before any senior screen |
| 4 | [30-architecture](30-architecture/INDEX.md) | System design (theory + case studies) + design patterns | 1-2 weeks | Before any senior screen |
| 5 | [40-platform](40-platform/INDEX.md) | DevOps (Docker, CI/CD, K8s) | 1 week | Before any senior screen |
| 6 | [50-quality](50-quality/INDEX.md) | Quality (testing, a11y, performance) | 1 week | Before any senior screen |
| 7 | [60-realtime](60-realtime/INDEX.md) | Real-time (WebSockets) | Optional | Only if JD requires |
| 8 | [70-interview-toolkit](70-interview-toolkit/INDEX.md) | Behavioral + coding patterns + cheatsheets | 1 week | Before any interview |
| 9 | [80-lanes-abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md) or [81-lanes-indian-sde-faang](81-lanes-indian-sde-faang/INDEX.md) | Lane-specific prep | 1-2 weeks | After stacks |
| 10 | [projects](projects/INDEX.md) | Project deep-dives (Docita interview defense) | As needed | Before project interviews |

**Total: 8-12 weeks if you're starting from zero, 4-6 weeks if you're already strong on most of it.**

---

### 00-strategy — Interview strategy (everyone starts here)

> 4 files. Cross-lane. Universal — applies to all interviews regardless of company or lane.

- [Communication](00-strategy/00.01-communication.md)
- [Resume Tips](00-strategy/00.02-resume-tips.md)
- [STAR Method](00-strategy/00.03-star-method.md)
- [HR Questions](00-strategy/00.04-hr-questions.md)

---

### 10-frontend — Frontend (122 files in 8 sub-stacks)

| Order | Sub-stack | Files | Topics |
| ----- | ----------------------------------------------------------- | ----: | --------------------------------------------------------------------------------------------------------------------------------- |
| 10.1 | [JavaScript](10-frontend/10.1-javascript/INDEX.md) | 34 | Execution context, closures, prototypes, event loop, promises, async/await, cancellation, ES2024, hash tables |
| 10.2 | [TypeScript](10-frontend/10.2-typescript/INDEX.md) | 18 | Generics, utility types, conditional types, narrowing, `satisfies` operator |
| 10.3 | [React](10-frontend/10.3-react/INDEX.md) | 22 | Virtual DOM, Fiber, hooks (18-19), Suspense, performance, state management |
| 10.4 | [Next.js](10-frontend/10.4-next.js/INDEX.md) | 17 | App Router, Server Components, Server Actions, Middleware, caching, streaming |
| 10.5 | [Form Handling](10-frontend/10.5-form-handling/INDEX.md) | 7 | React Hook Form, Zod, Formik, TanStack Form, Server Actions |
| 10.6 | [Animation](10-frontend/10.6-animation/INDEX.md) | 8 | Framer Motion, CSS Animations, GSAP, React Spring, View Transitions |
| 10.7 | [HTML/CSS & PWA](10-frontend/10.7-html-css/INDEX.md) | 9 | Semantic HTML, CSS layout/responsive, service workers, SEO, browser rendering |
| 10.8 | [Mobile & Cross-Platform](10-frontend/10.8-mobile/INDEX.md) | 7 | React Native (JSI/Fabric), Expo decision matrix, RN vs native vs PWA, EAS builds, OTA updates, store release, interview questions |

### 20-backend — Backend (147 files in 11 sub-stacks)

| Order | Sub-stack | Files | Topics |
| ----- | ------------------------------------------------------------------------------ | ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 20.1 | [Node.js](20-backend/20.1-node.js/INDEX.md) | 13 | Event loop, streams, clustering, web streams, child processes, test runner |
| 20.2 | [NestJS](20-backend/20.2-nestjs/INDEX.md) | 19 | Modules, DI, guards, pipes, interceptors, CQRS, microservices |
| 20.3 | [REST APIs](20-backend/20.3-rest-apis/INDEX.md) | 21 | HTTP methods, status codes, versioning, pagination, rate limiting, RFC 7807 errors, webhooks, HTTP caching, maturity model |
| 20.4 | [Database](20-backend/20.4-database/INDEX.md) | 24 | PostgreSQL, indexes, transactions, MVCC, Prisma, pooling, replication, row-level security |
| 20.5 | [Auth & Security](20-backend/20.5-security/INDEX.md) | 21 | **[auth track](20-backend/20.5-security/01-auth/INDEX.md):** fundamentals → sessions → JWT → OAuth → RBAC → ABAC deep-dive · attacks (XSS, CSRF, SQLi) · hardening (CSP, STRIDE, secrets) |
| 20.6 | [Microservices & Distributed Patterns](20-backend/20.6-microservices/INDEX.md) | 19 | Service discovery, gateway, saga, circuit breaker, event sourcing/CQRS, transactional outbox, Kafka/RabbitMQ, gRPC streaming, service mesh, event-driven architecture |
| 20.7 | [GraphQL](20-backend/20.7-graphql/INDEX.md) | 9 | Schema design, queries/mutations, Apollo Server, performance, security |
| 20.8 | [Caching](20-backend/20.8-caching/INDEX.md) | 4 | Cache patterns, invalidation, stampede prevention, Redis fundamentals + advanced patterns |
| 20.9 | [Message Brokers](20-backend/20.9-message-brokers/INDEX.md) | 4 | Kafka vs RabbitMQ models, delivery semantics, acks/ISR durability, consumer groups & rebalances, lag SLI, envelopes/schema evolution, DLQs, transactional outbox |
| 20.12 | [AI Engineering](20-backend/20.12-ai-engineering/INDEX.md) | 7 | LLM app architecture (RAG/streaming/structured output), prompts & evals, safety & cost governance |
| 20.13 | [Java](20-backend/20.13-java/INDEX.md) | 6 | Language fundamentals, OOP & SOLID, concurrency, JUnit/Mockito testing, Spring Boot, interview Q&A |

### 30-architecture — Architecture (109 files in 3 sub-stacks)

| Order | Sub-stack | Files | Topics |
| ----- | ----------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 30.1 | [Design Patterns](30-architecture/30.1-design-patterns/INDEX.md) | 38 | **Foundations** (SOLID, OOP, UML) + **Creational** (Singleton, Factory Method, Abstract Factory, Builder, Prototype) + **Structural** (Adapter, Facade, Decorator, Proxy, Module, Composite, Bridge, Flyweight) + **Behavioral** (Strategy, Observer, Chain, State, Template Method, Iterator, Mediator, Memento, Command, Visitor, Interpreter) + **Architectural** (Repository, CQRS+DI, Event Sourcing, Saga) + 50+ interview questions. **All 23 GoF patterns** + modern patterns, organized by category. |
| 30.2 | [System Design](30-architecture/30.2-system-design/INDEX.md) | 54 | 21 theory files (CAP, consistency, sharding, caching, queues, rate limiting, consensus, failure modes, architecture patterns, capacity planning, backpressure, distributed locks, probabilistic data structures, outbox & CDC, resilience patterns, multi-region) + how-to-approach + interview questions + 31 case studies (URL shortener, WhatsApp, Uber, Netflix, payment gateway, ticket booking, ...) |
| 30.3 | [Infrastructure Patterns](30-architecture/30.3-infra-patterns/INDEX.md) | 17 | Database scaling, resilience patterns (circuit breaker, bulkhead, retry), idempotency-retry deep dive, leader election & consensus, zero-downtime deployments, data pipelines, multi-tenant SaaS |

### Platform (95 files in 12 sub-stacks)

| Sub-stack | Files | Topics |
| -------------------------------------------------------------- | ----: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Docker](40-platform/40.1-docker/INDEX.md) | 10 | Images, containers, volumes, networks, compose, multi-stage builds |
| [Kubernetes](40-platform/40.2-kubernetes/INDEX.md) | 17 | Pods, deployments, services, ingress, ConfigMaps, HPA, Helm, RBAC |
| [CI/CD](40-platform/40.3-ci-cd/INDEX.md) | 11 | GitHub Actions, Docker build/deploy, blue-green/canary, Jenkins, GitLab CI, ArgoCD |
| [Observability](40-platform/40.4-observability/INDEX.md) | 11 | Logging, monitoring, tracing, OpenTelemetry, error tracking, SLI/SLO/SLA, alerting |
| [Build Tools](40-platform/40.5-build-tools/INDEX.md) | 10 | Webpack, Vite, Turbopack, Rspack, ESBuild, SWC, Babel |
| [Git Advanced](40-platform/40.6-git-advanced/INDEX.md) | 10 | Branching, rebase, cherry-pick, hooks, patch workflow, code archaeology |
| [Serverless & Edge](40-platform/40.7-serverless-edge/INDEX.md) | 10 | Lambda, Vercel Edge, serverless patterns, SAM/CDK/SST, Fly.io, Vite SPA on Cloudflare |
| [Monorepo](40-platform/40.8-monorepo/INDEX.md) | 6 | Turborepo, Nx, pnpm, Rush, Bazel |
| [Twelve-Factor App](40-platform/40.9-twelve-factor/INDEX.md) | 2 | The canonical cloud-native methodology — codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes |
| [CDN & Edge](40-platform/40.10-cdn/INDEX.md) | 4 | CDN caching strategies, invalidation, edge functions, PHI-at-edge considerations |
| [Reverse Proxy](40-platform/40.11-reverse-proxy/INDEX.md) | 2 | Nginx internals: C10K, master–worker + epoll event loop, config contexts, upstream LB, TLS termination, buffering, rate limiting, proxy_cache, nginx vs HAProxy vs Envoy |
| [IaC & Terraform](40-platform/40.12-iac/INDEX.md) | 2 | Infrastructure as Code, HCL, state & drift, plan/apply, backends & locking, modules, workspaces, import, OpenTofu/Pulumi/CDKTF, IaC in CI/CD |

### Quality (38 files in 4 sub-stacks)

| Sub-stack | Files | Topics |
| ------------------------------------------------------------------------- | ----: | ----------------------------------------------------------------------------------- |
| [Testing](50-quality/50.1-testing/INDEX.md) | 14 | Jest, RTL, unit, integration, E2E, mocking, Vitest, load testing, chaos engineering |
| [Accessibility](50-quality/50.2-accessibility/INDEX.md) | 9 | WCAG, ARIA, keyboard navigation, color contrast, forms & labels |
| [Performance Monitoring](50-quality/50.3-performance-monitoring/INDEX.md) | 9 | Core Web Vitals, profiling, Lighthouse CI, bundle analysis, RUM |
| [Production Engineering](50-quality/50.4-production-engineering/INDEX.md) | 6 | Incident response, SLI/SLO/error budgets, chaos engineering |

### Real-Time (11 files)

| Sub-stack | Files | Topics |
| -------------------------------------------------- | ----: | ----------------------------------------------------------------------- |
| [WebSockets](60-realtime/60.1-websockets/INDEX.md) | 11 | Socket.IO, SSE, real-time architecture, NestJS WebSockets, WebTransport |

### Interview Toolkit (34 files in 3 sub-stacks)

| Sub-stack | Files | Topics |
| --------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------- |
| [Behavioral](70-interview-toolkit/70.1-behavioral/INDEX.md) | 5 | Leadership questions, system-design behavioral (STAR + HR basics live in [00-strategy](00-strategy/INDEX.md)) |
| [Coding Patterns](70-interview-toolkit/70.2-coding-patterns/INDEX.md) | 22 | Sliding window, two pointers, BFS/DFS, DP, heap, trie, union find, backtracking |
| [Cheat Sheets](70-interview-toolkit/70.3-cheatsheets/INDEX.md) | 7 | JavaScript, TypeScript, React/Next.js, backend, system design |

---

## Recommended Study Path

After you pick your lane (above), the two lanes share all 7 study stacks. They diverge in the final interview-prep phase.

```text
00-strategy → Communication → Resume Tips → STAR Method → HR Questions
10-frontend → JavaScript → TypeScript → React → Next.js → Forms → Animation → HTML/CSS/PWA → Mobile (optional)
20-backend → Node.js → NestJS → REST APIs → Database → Auth & Security track → Microservices & Distributed Patterns → GraphQL → Caching → AI Engineering → Java
30-architecture → Design Patterns (Foundations → Creational → Structural → Behavioral → Architectural → Interview Prep) → System Design (00-theory: CAP, sharding, caching, queues, ... → 10-case-studies: URL shortener, Uber, Netflix, ...)
40-platform → Docker → Kubernetes → CI/CD → Observability → Build Tools → Git Advanced → Serverless & Edge → Monorepo → Twelve-Factor → CDN & Edge → Reverse Proxy → IaC & Terraform
50-quality → Testing → Accessibility → Performance Monitoring → Production Engineering
60-realtime → WebSockets
70-interview-toolkit → Behavioral → Coding Patterns → Cheat Sheets
80-lanes-abroad-full-stack OR 81-lanes-indian-sde-faang (terminal phase)
projects → Docita architecture deep-dives, interview defense
```

**For Indian SDE / FAANG:** Coding Patterns is the priority (22 files, all patterns). 8-12 week intensive, 4-6 hrs/day.
**For Abroad Full-Stack:** Coding Patterns is light (30-40 mediums across 6 patterns only). Heavy on System Design + take-home prep. 4-week realistic, 2-3 hrs/day.

---

## Cross-Reference Map

| Stack | Depends on | Used by |
| ------------------------------------------------------------------------------------------------------------------------------------ | ---------- | -------------------------------------------------------------- |
| [00-strategy](00-strategy/INDEX.md) | — | Both lanes (everyone starts here) |
| [10-frontend](10-frontend/INDEX.md) | — | Both lanes |
| [20-backend](20-backend/INDEX.md) | — | Both lanes |
| [30-architecture](30-architecture/INDEX.md) | — | Both lanes |
| [40-platform](40-platform/INDEX.md) | — | Both lanes |
| [50-quality](50-quality/INDEX.md) | — | Both lanes |
| [60-realtime](60-realtime/INDEX.md) | — | Abroad Full-Stack (occasionally) |
| [70-interview-toolkit](70-interview-toolkit/INDEX.md) | All stacks | Both lanes (Indian SDE / FAANG heavy, Abroad Full-Stack light) |
| [80-lanes-abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md) or [81-lanes-indian-sde-faang](81-lanes-indian-sde-faang/INDEX.md) | All stacks | Terminal phase |
| [projects](projects/INDEX.md) | — | Project-specific (Docita interview prep) |

---

## Direct Indexes

**Strategy & lanes:**

- [00-strategy/index](00-strategy/INDEX.md) — Cross-lane strategy
- [80-lanes-abroad-full-stack/index](80-lanes-abroad-full-stack/INDEX.md) — Abroad Full-Stack lane (recommended for EU)
- [81-lanes-indian-sde-faang/index](81-lanes-indian-sde-faang/INDEX.md) — Indian SDE / FAANG lane
- [projects/index](projects/INDEX.md) — Project deep-dives (Docita)

**Stacks (in study order):**

- **00-strategy** — [Communication](00-strategy/00.01-communication.md) · [Resume Tips](00-strategy/00.02-resume-tips.md) · [STAR Method](00-strategy/00.03-star-method.md) · [HR Questions](00-strategy/00.04-hr-questions.md)
- **10-frontend** — [JavaScript](10-frontend/10.1-javascript/INDEX.md) · [TypeScript](10-frontend/10.2-typescript/INDEX.md) · [React](10-frontend/10.3-react/INDEX.md) · [Next.js](10-frontend/10.4-next.js/INDEX.md) · [Form Handling](10-frontend/10.5-form-handling/INDEX.md) · [Animation](10-frontend/10.6-animation/INDEX.md) · [HTML/CSS & PWA](10-frontend/10.7-html-css/INDEX.md) · [Mobile & Cross-Platform](10-frontend/10.8-mobile/INDEX.md)
- **20-backend** — [Node.js](20-backend/20.1-node.js/INDEX.md) · [NestJS](20-backend/20.2-nestjs/INDEX.md) · [REST APIs](20-backend/20.3-rest-apis/INDEX.md) · [Database](20-backend/20.4-database/INDEX.md) · [Auth & Security](20-backend/20.5-security/INDEX.md) · [Microservices & Distributed Patterns](20-backend/20.6-microservices/INDEX.md) · [GraphQL](20-backend/20.7-graphql/INDEX.md) · [Caching](20-backend/20.8-caching/INDEX.md) · [AI Engineering](20-backend/20.12-ai-engineering/INDEX.md) · [Java](20-backend/20.13-java/INDEX.md)
- **30-architecture** — [Design Patterns](30-architecture/30.1-design-patterns/INDEX.md) (categorized: [Foundations](30-architecture/30.1-design-patterns/01-foundations/INDEX.md) · [Creational](30-architecture/30.1-design-patterns/02-creational/INDEX.md) · [Structural](30-architecture/30.1-design-patterns/03-structural/INDEX.md) · [Behavioral](30-architecture/30.1-design-patterns/04-behavioral/INDEX.md) · [Architectural](30-architecture/30.1-design-patterns/05-architectural/INDEX.md) · [Interview Prep](30-architecture/30.1-design-patterns/06-interview-prep/INDEX.md)) · [System Design](30-architecture/30.2-system-design/INDEX.md) · [Infrastructure Patterns](30-architecture/30.3-infra-patterns/INDEX.md)
- **40-platform** — [Docker](40-platform/40.1-docker/INDEX.md) · [Kubernetes](40-platform/40.2-kubernetes/INDEX.md) · [CI/CD](40-platform/40.3-ci-cd/INDEX.md) · [Observability](40-platform/40.4-observability/INDEX.md) · [Build Tools](40-platform/40.5-build-tools/INDEX.md) · [Git Advanced](40-platform/40.6-git-advanced/INDEX.md) · [Serverless & Edge](40-platform/40.7-serverless-edge/INDEX.md) · [Monorepo](40-platform/40.8-monorepo/INDEX.md) · [Twelve-Factor](40-platform/40.9-twelve-factor/INDEX.md) · [CDN & Edge](40-platform/40.10-cdn/INDEX.md) · [Reverse Proxy](40-platform/40.11-reverse-proxy/INDEX.md) · [IaC & Terraform](40-platform/40.12-iac/INDEX.md)
- **50-quality** — [Testing](50-quality/50.1-testing/INDEX.md) · [Accessibility](50-quality/50.2-accessibility/INDEX.md) · [Performance Monitoring](50-quality/50.3-performance-monitoring/INDEX.md) · [Production Engineering](50-quality/50.4-production-engineering/INDEX.md)
- **60-realtime** — [WebSockets](60-realtime/60.1-websockets/INDEX.md)
- **70-interview-toolkit** — [Behavioral](70-interview-toolkit/70.1-behavioral/INDEX.md) · [Coding Patterns](70-interview-toolkit/70.2-coding-patterns/INDEX.md) · [Cheat Sheets](70-interview-toolkit/70.3-cheatsheets/INDEX.md)

---

*Last updated: September 2026 — 867 files, 366K lines, 0 broken links — folders numbered for study order. Every large stack organized into numbered category subfolders; auth track complete through passkeys/SAML; sequences contiguous inside every stack folder (the 80.x lane numbering intentionally gaps into projects/docita prep docs).
