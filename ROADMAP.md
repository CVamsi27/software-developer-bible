# The Senior Engineer Roadmap

> Use this order to build senior full-stack interview skills, then adjust the depth to the job description and confirmed interview format. Each phase ends with a practical checkpoint; revisit a weak area before adding more material.
>
> Start with [lane selection](#phase-0--pick-your-lane-day-1-2-hours). Use the [full index](INDEX.md) for individual chapters and the [senior readiness rubric](80-lanes-abroad-full-stack/80.29-topic-brushup-roadmap.md) to assess explanations, implementation, failure analysis and ownership.

[![Checkpoints](https://img.shields.io/badge/checkpoints-8-green)](#checkpoints--do-not-skip)
[![Last Updated](https://img.shields.io/badge/last%20updated-October%202026-purple)](#)

---

## The Path at a Glance

| Stage | Build this capability |
| --------------------- | ------------------------------------------------------------------- |
| Strategy | Confirm the role, assessment format and supported experience claims |
| Language and frontend | Trace execution and build a typed, accessible interaction |
| Backend | Protect API, data and authorization invariants |
| Architecture | Compare designs under explicit workload and failure constraints |
| Platform | Deploy, observe and recover the service |
| Quality | Test critical behavior and measure the actual user experience |
| Interview toolkit | Solve fresh problems and explain real decisions |
| Lane execution | Practice the confirmed format and review application feedback |

The weeks below are sample scheduling blocks, not a predicted hiring outcome. Use the full or focused plan according to your starting skills and available time.

---

## Phase 0 — Pick Your Lane *(Day 1, 2 hours)*

| Confirmed assessment need | Preparation lane | Practice emphasis |
| ------------------------------------------------------ | -------------------------------------------------------- | ------------------------------------------------------------------- |
| Full-stack implementation, take-home or product design | [Abroad full-stack](80-lanes-abroad-full-stack/INDEX.md) | Ship bounded work, test it and defend its trade-offs |
| Algorithmic coding and broader SDE design | [SDE / FAANG](81-lanes-indian-sde-faang/INDEX.md) | Solve fresh problems, analyze complexity and explain design choices |
| A mix of both | Both lanes | Allocate time to the actual assessment stages |

**Checkpoint 0:** State the target responsibilities, expected exercises, language, allowed tools, timing and logistical constraints. Confirm these with the recruiter or published role information; an employer or country label does not establish its hiring loop.

---

## Phase 1 — Language & Frontend Core *(Weeks 1–2)*

Main topic flow — each sub-stack builds on the previous:

| Order | Sub-topic | Study | Files |
| ----- | --------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------: |
| 1.1 | **JavaScript engine** | Execution context → call stack → hoisting → closures → scope → `this` → prototypes → event loop | [10.1-javascript](10-frontend/10.1-javascript/INDEX.md) |
| 1.2 | **JS async** | Promises → async/await → error handling → web workers | [10.1-javascript](10-frontend/10.1-javascript/INDEX.md) |
| 1.3 | **TypeScript** | Generics → utility types → conditional/mapped types → narrowing → `satisfies` | [10.2-typescript](10-frontend/10.2-typescript/INDEX.md) |
| 1.4 | **React** | Reconciliation/Fiber → hooks (incl. 18/19) → Suspense → state management → performance | [10.3-react](10-frontend/10.3-react/INDEX.md) |
| 1.5 | **Next.js** | App Router → RSC → Server Actions → caching layers → streaming | [10.4-next.js](10-frontend/10.4-next.js/INDEX.md) |

Include [forms](10-frontend/10.5-form-handling/INDEX.md) and [HTML/CSS](10-frontend/10.7-html-css/INDEX.md) in frontend preparation: validation, layout, semantics and keyboard behavior are part of implementing a usable feature. Add [animation](10-frontend/10.6-animation/INDEX.md) or [mobile/React Native](10-frontend/10.8-mobile/INDEX.md) when the role needs them.

**Checkpoint 1:** Explain the event loop with a printed-output ordering puzzle; write a typed generic utility live; explain when RSC beats client components. Mock questions: [JavaScript interview questions](10-frontend/10.1-javascript/06-modern-and-interview/10.1.6.05-interview-questions.md).

---

## Phase 2 — Backend Core *(Weeks 3–5, the heart of senior screens)*

### 2.1 Runtime & framework

| Order | Topic | Flow inside |
| ----- | ------------------------------------------- | ----------------------------------------------------------------- |
| 2.1.1 | [Node.js](20-backend/20.1-node.js/INDEX.md) | event loop → streams → clustering → child processes → security |
| 2.1.2 | [NestJS](20-backend/20.2-nestjs/INDEX.md) | modules → DI → pipes/guards/interceptors/filters → CQRS → testing |

### 2.2 API layer

| Order | Topic | Flow inside |
| ----- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2.2.1 | [REST fundamentals](20-backend/20.3-rest-apis/INDEX.md) | principles → methods/status codes → versioning → pagination → error handling → caching |
| 2.2.2 | [API design advanced](20-backend/20.3-rest-apis/INDEX.md) *(in REST APIs stack)* | maturity model → rate limiting algorithms → RFC 9457 Problem Details → webhooks → gRPC streaming ([microservices](20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.02-grpc-streaming.md)) |
| 2.2.3 | [GraphQL](20-backend/20.7-graphql/INDEX.md) *(if JD asks)* | schema design → resolvers → N+1/DataLoader → security |

### 2.3 Data

| Order | Topic | Flow inside |
| ----- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.3.1 | [PostgreSQL core](20-backend/20.4-database/INDEX.md) | normalization → indexes → transactions/MVCC → joins → execution plans → deadlocks |
| 2.3.2 | [Postgres at scale](20-backend/20.4-database/INDEX.md) | connection pooling → replication → partitioning/sharding theory ([30.2 theory](30-architecture/30.2-system-design/01-theory/INDEX.md)) → performance |
| 2.3.3 | ORM & Redis | [Prisma](20-backend/20.4-database/04-orm-and-access/20.4.4.01-prisma.md) → [Prisma advanced](20-backend/20.4-database/04-orm-and-access/20.4.4.02-prisma-advanced.md) → [Redis fundamentals](20-backend/20.8-caching/20.8.02-redis-fundamentals.md) |
| 2.3.4 | [Caching](20-backend/20.8-caching/INDEX.md) | cache-aside/write-through/write-behind → invalidation → stampede defense → advanced Redis |

### 2.4 Auth & Security — *the dedicated learning track*
Study as one connected story, not isolated files → **[20-backend/20.5-security/01-auth/INDEX.md](20-backend/20.5-security/01-auth/INDEX.md)**

| Stage | Topic | Trade-off you must be able to defend |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| 0 | [Fundamentals](20-backend/20.5-security/01-auth/20.5.1.01-auth-fundamentals.md) | hashing vs encryption vs signing; Argon2 params |
| 1 | [Sessions & cookies](20-backend/20.5-security/01-auth/20.5.1.04-sessions-cookies.md) | server state + instant revocation vs scale |
| 2 | [JWT](20-backend/20.5-security/01-auth/20.5.1.05-jwt.md) | statelessness vs revocation; HS256 vs RS256; storage XSS/CSRF matrix |
| 3 | [OAuth2/OIDC](20-backend/20.5-security/01-auth/20.5.1.06-oauth2-oidc.md) | delegation flows; PKCE; scopes vs roles |
| 4 | [RBAC/ABAC](20-backend/20.5-security/01-auth/20.5.1.09-rbac-abac.md) | coarse vs fine-grained authz; policy engines |
| Attacks: [XSS](20-backend/20.5-security/02-attacks-and-defense/20.5.2.01-xss.md) · [CSRF](20-backend/20.5-security/02-attacks-and-defense/20.5.2.02-csrf.md) · [SQLi](20-backend/20.5-security/02-attacks-and-defense/20.5.2.03-sql-injection.md) · [API Top 10](20-backend/20.5-security/02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) | each attack ↔ its exact defense |  |
| Hardening: [headers/CSP](20-backend/20.5-security/03-hardening-and-operations/20.5.3.02-web-security.md) · [STRIDE](20-backend/20.5-security/03-hardening-and-operations/20.5.3.03-threat-modeling-stride.md) · [secrets](20-backend/20.5-security/03-hardening-and-operations/20.5.3.04-secrets-management.md) | threat-model any feature in 5 min |  |
| Drill: [auth Q&A](20-backend/20.5-security/01-auth/20.5.1.11-interview-questions.md) + [full bank](20-backend/20.5-security/04-interview-drills/20.5.4.01-interview-questions.md) | survive the follow-up traps |  |

### 2.5 Distributed backend & ops patterns

| Order | Topic | Flow inside |
| ----- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.5.1 | [Microservices & distributed patterns](20-backend/20.6-microservices/INDEX.md) | foundations (discovery/gateway/gRPC) → data patterns (event sourcing/CQRS/saga/distributed txns) → resilience (circuit breaker/bulkhead/mesh) → messaging (Kafka/RabbitMQ/DLQ/event-driven architecture) |
| 2.5.2 | [Ops patterns](30-architecture/30.3-infra-patterns/INDEX.md) | retries/backoff → idempotency keys → health checks/graceful shutdown → leader election → zero-downtime deploys |
| 2.5.3 | [Real-time](60-realtime/60.1-websockets/INDEX.md) *(JD-dependent)* | WS vs SSE vs polling → scaling with pub/sub → presence |
| 2.5.4 | [AI Engineering](20-backend/20.12-ai-engineering/INDEX.md) *(if the role requires it)* | retrieval, streaming and structured output → evaluation → safety and cost controls. Practice a proposed design; claim production ownership only when supported by your project evidence |

**Checkpoint 2:** Design authorization for a multi-tenant service, trace a concurrent transaction failure and choose pagination for a changing feed. Explain the invariant, enforcement point and recovery behavior. Distinguish a worked study example from an incident you personally handled.

---

## Phase 3 — Architecture & System Design *(Weeks 6–7, the senior differentiator)*

| Order | Topic | Flow inside |
| ----- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3.1 | [Design patterns](30-architecture/30.1-design-patterns/INDEX.md) | SOLID → GoF applied (Strategy, Repository, Observer, DI…) → CQRS in practice |
| 3.2 | [SD method](30-architecture/30.2-system-design/01-theory/30.2.1.15-how-to-approach.md) | clarify requirements → estimate workload → propose boundaries → trace a critical path and its failures |
| 3.3 | [SD theory](30-architecture/30.2-system-design/01-theory/INDEX.md) | CAP → consistency models → sharding → caching → queues → rate limiting → consensus → failure modes → backpressure → multi-region |
| 3.4 | [Case studies ×32](30-architecture/30.2-system-design/02-case-studies/INDEX.md) | URL shortener → WhatsApp → Uber → Netflix → payment gateway → ticket booking → notification service → hospital mgmt… practice 5 aloud with a timer |

**Checkpoint 3:** Record two timed designs, then review their assumptions, capacity estimates, consistency boundaries and failure recovery. Use a URL shortener and a ticket-booking system to expose different constraints; explain your reasoning clearly without narrating every keystroke.

---

## Phase 4 — Platform & Delivery *(Week 8)*

| Order | Topic | Depth needed |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 4.1 | [Docker](40-platform/40.1-docker/INDEX.md) | images/layers → multi-stage builds → compose → volumes/networks |
| 4.2 | [Kubernetes](40-platform/40.2-kubernetes/INDEX.md) | pods/deployments/services/ingress → probes → HPA (concepts, not admin-level) |
| 4.3 | [CI/CD](40-platform/40.3-ci-cd/INDEX.md) | GitHub Actions → blue-green/canary → pipeline-as-code |
| 4.4 | [Observability](40-platform/40.4-observability/INDEX.md) | structured logs → metrics → tracing/OpenTelemetry → SLI/SLO/alerting |
| 4.5 | [Git advanced](40-platform/40.6-git-advanced/INDEX.md) | rebase/cherry-pick/hooks/reflog |
| 4.6 | [Serverless & edge](40-platform/40.7-serverless-edge/INDEX.md) · [Monorepo](40-platform/40.8-monorepo/INDEX.md) · [12-factor](40-platform/40.9-twelve-factor/INDEX.md) · [CDN](40-platform/40.10-cdn/INDEX.md) | JD-dependent depth |

**Checkpoint 4:** Sketch your current project's deploy pipeline end-to-end including failure modes; define an SLO for its main endpoint.

---

## Phase 5 — Quality *(Week 9 or parallel with 4)*

| Order | Topic | Flow inside |
| ----- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 5.1 | [Testing](50-quality/50.1-testing/INDEX.md) | pyramid → Jest/Vitest → RTL → integration → E2E (Playwright) → mocking → test patterns |
| 5.2 | [Performance](50-quality/50.3-performance-monitoring/INDEX.md) | Core Web Vitals → profiling → budgets → RUM |
| 5.3 | [Accessibility](50-quality/50.2-accessibility/INDEX.md) | semantic HTML → keyboard and focus → WCAG → ARIA when needed → testing |
| 5.4 | [Production engineering](50-quality/50.4-production-engineering/INDEX.md) | incident response → SLI/SLO/error budgets → chaos basics |

**Checkpoint 5:** Choose tests for a critical user flow and explain why each belongs at that boundary. Demonstrate keyboard access, measure loading and interaction behavior, and explain a regression using evidence. A memorized test ratio or metric threshold is not enough.

---

## Phase 6 — Interview Toolkit *(continuous from Week 1, intensifies Week 9+)*

| Track | When | Contents |
| --------------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| [Coding patterns](70-interview-toolkit/70.2-coding-patterns/INDEX.md) | According to the confirmed coding format | sliding window → two pointers → BFS/DFS → DP → heap → trie → union-find → backtracking |
| [Behavioral](70-interview-toolkit/70.1-behavioral/INDEX.md) | Weeks 1–2, then weekly reps | STAR(+R) → leadership → conflict → failure stories |
| [Cheat sheets](70-interview-toolkit/70.3-cheatsheets/INDEX.md) | Final week | JS/TS/React/backend/system-design one-pagers |

Start [00-strategy](00-strategy/INDEX.md) items here if not done in Phase 0: [resume](00-strategy/00.02-resume-tips.md) → [STAR](00-strategy/00.03-star-method.md) → [HR questions](00-strategy/00.04-hr-questions.md).

**Checkpoint 6:** Give evidence-backed stories about ownership, conflict, failure and delivery. Solve fresh problems in the assessed format, state complexity and test edge cases; revisiting a memorized solution does not demonstrate transfer.

---

## Phase 7 — Lane Execution *(final 1–2 weeks before applying)*

### Abroad/EU lane → [80-lanes-abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md)
1. [Take-home playbook](80-lanes-abroad-full-stack/80.01-take-home-playbook.md) → ship one practice build ([starter prompt](80-lanes-abroad-full-stack/80.15-take-home-starter-prompt.md))
2. [System design EU patterns](80-lanes-abroad-full-stack/80.03-system-design-eu-patterns.md) + [case bank](80-lanes-abroad-full-stack/80.08-system-design-case-bank.md)
3. **Research targets against current vacancies** → [company prep sheets](80-lanes-abroad-full-stack/80.32-company-prep-sheets.md) + [domain primer: healthtech & geospatial](80-lanes-abroad-full-stack/80.34-germany-target-domain-primer.md)
4. **Weekly operating loop + application pipeline** → [Germany Target Engine](80-lanes-abroad-full-stack/80.35-germany-target-engine.md)
5. Project evidence: **Docita** → [resume defense](80-lanes-abroad-full-stack/80.16-docita-resume-defense.md) · [evidence pack](80-lanes-abroad-full-stack/80.17-docita-interview-evidence-pack.md) · [Google-level bank](80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md) · [topic mapping](80-lanes-abroad-full-stack/80.22-docita-tech-topic-mapping.md)
6. Logistics: [comp benchmarking](80-lanes-abroad-full-stack/80.05-comp-eu-benchmarking.md) · [visa playbook](80-lanes-abroad-full-stack/80.06-visa-relocation-playbook.md)

### FAANG lane → [81-lanes-indian-sde-faang](81-lanes-indian-sde-faang/INDEX.md)
1. [Complete guide](81-lanes-indian-sde-faang/81.01-complete-guide.md) → [LeetCode study plan](81-lanes-indian-sde-faang/81.06-leetcode-study-plan.md) (daily, from Week 3 onward really)
2. [Core CS](81-lanes-indian-sde-faang/81.02-core-cs-fundamentals.md) → [advanced topics](81-lanes-indian-sde-faang/81.05-advanced-topics.md)
3. Company guides: [Google](81-lanes-indian-sde-faang/81.17-google-interview-guide.md) · [Amazon](81-lanes-indian-sde-faang/81.18-amazon-interview-guide.md) · [Meta](81-lanes-indian-sde-faang/81.19-meta-interview-guide.md) · [Microsoft](81-lanes-indian-sde-faang/81.16-microsoft-azure-interview-guide.md)

**Checkpoint 7:** Complete a representative mock, check that resume claims have supporting examples, and submit suitable applications when the role and logistics match. Track feedback and change the next practice block accordingly.

---

## Two Speeds: Full vs Fast

### Full speed — 9–10 weeks (~3 h/day)
A sample plan for filling broad gaps: work through phases 0–5 while practicing phase 6 each week, then increase lane-specific mocks. Adjust the duration after testing your starting skills.

### Focused plan — 4 sample weeks (~2–3 h/day)

| Week | Do | Skip |
| ---- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1 | Phase 0 + Phase 1 (skim 1.1–1.2, full 1.3–1.5) + 8 STAR stories | specialist animation or mobile topics unless required |
| 2 | Phase 2.2–2.3 (APIs + data) + **auth track** + start coding patterns | GraphQL unless JD |
| 3 | Phase 2.5 + Phase 3 + one accessibility/tested user flow + assessed coding format | cluster administration unless required |
| 4 | Phase 4 skim (Docker/CI/observability) + Phase 6 drills + Phase 7 lane execution + apply | monorepo, CDN, chaos |

### Emergency — 1 week
Prioritize the confirmed assessment: one fresh implementation or coding exercise, one relevant design, two mocks and supported project stories. Review authorization, failure recovery and the tests for your critical flow. Use the [lane 80 index](80-lanes-abroad-full-stack/INDEX.md) for practical full-stack exercises. One week cannot close every fundamental gap; spend it on the most consequential ones.

---

## Checkpoints — Do Not Skip

Use these as self-assessment checks. A weak result tells you where to practice next; completing the table does not guarantee an employer's decision.

| # | Gate | Pass condition |
| --- | ------------- | ------------------------------------------------------------------------- |
| 0 | Lane chosen | Responsibilities, format, tools and logistical constraints confirmed |
| 1 | Frontend core | Event-loop ordering puzzle solved live; generic utility written live |
| 2 | Backend core | Multi-tenant auth whiteboarded in 10 min; MVCC explained with example |
| 3 | System design | 2 recorded 45-min designs reviewed against 4-phase rubric |
| 4 | Platform | Deploy pipeline sketched incl. failure modes + one SLO defined |
| 5 | Quality | Critical-flow tests justified; keyboard behavior and performance measured |
| 6 | Toolkit | Supported ownership stories; fresh problems solved with edge-case tests |
| 7 | Lane | Representative mock reviewed; suitable applications and feedback tracked |

---

## Weekly Rhythm (any speed)

| Day | Block 1 (90') | Block 2 (60') |
| ------- | ------------------------------------------------ | -------------------------------------------------------- |
| Mon–Thu | Current phase material | Fresh exercise in the confirmed interview format |
| Fri | Catch-up / re-read flagged files | Flashcards from cheat sheets |
| Sat | Timed mock or recorded design | Story rehearsal out loud |
| Sun | Rest · 15-min weekly review against this roadmap | update tracker |

Trackers: [80.33-weekly-study-tracker](80-lanes-abroad-full-stack/80.33-weekly-study-tracker.md) · [81 daily timer](81-lanes-indian-sde-faang/81.11-daily-study-timer.md)

---

## Where Everything Lives (final structure)

```text
software-developer-bible/
├── ROADMAP.md ← you are here
├── INDEX.md ← every file, one list
├── 00-strategy/ ← resume · STAR · HR · communication
├── 10-frontend/ ← JS → TS → React → Next.js (+ forms/animation/html-css/mobile)
├── 20-backend/ ← 11 sub-stacks:
│ ├── 20.1-node.js runtime internals
│ ├── 20.2-nestjs framework
│ ├── 20.3-rest-apis HTTP API contracts (fundamentals → production → advanced)
│ ├── 20.4-database Postgres + Prisma (Redis lives in caching)
│ ├── 20.5-security/01-auth/ the auth learning track
│ ├── 20.6-microservices single home for distributed patterns (+ event-driven, gRPC streaming)
│ ├── 20.7-graphql
│ ├── 20.8-caching cache patterns + Redis fundamentals + advanced Redis
│ ├── 20.12-ai-engineering LLM architecture · evals · governance
│ └── 20.13-java Java + Spring Boot
├── 30-architecture/
│ ├── 30.1-design-patterns
│ ├── 30.2-system-design/ 01-theory + 02-case-studies
│ └── 30.3-infra-patterns/ ops-only: retries, idempotency, health checks…
├── 40-platform/ ← docker → k8s → CI/CD → observability → git → serverless → monorepo → 12-factor → CDN
├── 50-quality/ ← testing · a11y · performance · production engineering
├── 60-realtime/ ← WebSockets/SSE (the only realtime home)
├── 70-interview-toolkit/ ← coding patterns (18) · behavioral depth · cheat sheets
├── 80-lanes-abroad-full-stack/ ← EU lane: playbooks · Docita pack · Germany cluster
└── 81-lanes-indian-sde-faang/ ← FAANG lane
```

---

## Navigation

[ INDEX.md](INDEX.md) · [README](README.md) · Lane indexes: [Abroad/EU](80-lanes-abroad-full-stack/INDEX.md) · [Indian SDE/FAANG](81-lanes-indian-sde-faang/INDEX.md)

*Last updated: October 2026. Use the linked stack indexes for the current learning flow.*
