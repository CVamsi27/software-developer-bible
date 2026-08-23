# 🗺️ The Senior Engineer Roadmap

> **One page. One path. Zero ambiguity.** This is the canonical order to work through the bible for a senior full-stack interview (5+ YoE). Every box links to its folder; every phase ends with a checkpoint you must pass before moving on.
>
> Pick your lane first (2 min): [Lane Decision](#phase-0--pick-your-lane-day-1) · Full index: [INDEX.md](INDEX.md)

[![Full path](https://img.shields.io/badge/duration-8_weeks_full_|_4_weeks_fast-blue)](#two-speeds-full-vs-fast)
[![Checkpoints](https://img.shields.io/badge/checkpoints-8-green)](#checkpoints-do-not-skip)
[![Last Updated](https://img.shields.io/badge/last%20updated-August%202026-purple)](#)

---

## The Path at a Glance

```text
 PHASE 0        PHASE 1          PHASE 2          PHASE 3           PHASE 4         PHASE 5         PHASE 6       PHASE 7
 Strategy   →   Language    →    Backend     →    Architecture →    Platform   →    Quality    →   Toolkit   →   LANE EXECUTION
 (2 days)       & Frontend       Core              & System Design   & Delivery      & Testing       & mocks      (your target market)
                (2 wks)          (3 wks)           (2 wks)           (1 wk)          (1 wk)          (ongoing)    (final 1-2 wks)
   │               │                │                 │                 │               │               │             │
   ├─ resume       ├─ JS core       ├─ Node.js        ├─ design         ├─ Docker       ├─ testing      ├─ 18 coding  ├─ lane plan
   ├─ STAR         ├─ TS deep       ├─ NestJS         │  patterns       ├─ K8s basics   ├─ a11y         │  patterns   ├─ take-home
   ├─ comms        ├─ React         ├─ API design     ├─ SD theory      ├─ CI/CD        ├─ performance  ├─ behavioral ├─ system design
   └─ HR qs        └─ Next.js       ├─ databases      └─ 20 case        ├─ observability└─ production   │  + stories  └─ company sheets
                                    ├─ AUTH track ←     studies            git, serverless   engineering
                                    └─ microservices                                         drills
```

**Total: 8–12 weeks from cold · 4–6 weeks if strong on most stacks.** Two speeds below.

---

## Phase 0 — Pick Your Lane *(Day 1, 2 hours)*

| If your targets look like… | Lane | Then in Phase 7 |
|---|---|---|
| EU mid-stage startups, remote-first US (take-homes, 3–4 rounds) | [80-lanes-abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md) | Take-home reps + EU system-design patterns |
| FAANG/Big Tech India or US (5–6 rounds, LeetCode mediums-hard) | [81-lanes-indian-sde-faang](81-lanes-indian-sde-faang/INDEX.md) | DSA volume + FAANG-style SD + LP/value rounds |
| Booking.com, Spotify-style loops | Both lanes | Do both: 81's DSA signal + 80's overlay |

**Checkpoint 0:** You can state your lane, your bar ("1–2 mediums in 30 min" vs "5–6h take-home"), and your comp range out loud.

---

## Phase 1 — Language & Frontend Core *(Weeks 1–2)*

Main topic flow — each sub-stack builds on the previous:

| Order | Sub-topic | Study | Files |
|---|---|-------|------:|
| 1.1 | **JavaScript engine** | Execution context → call stack → hoisting → closures → scope → `this` → prototypes → event loop | [10.1-javascript](10-frontend/10.1-javascript/INDEX.md) |
| 1.2 | **JS async** | Promises → async/await → error handling → web workers | [10.1-javascript](10-frontend/10.1-javascript/INDEX.md) |
| 1.3 | **TypeScript** | Generics → utility types → conditional/mapped types → narrowing → `satisfies` | [10.2-typescript](10-frontend/10.2-typescript/INDEX.md) |
| 1.4 | **React** | Reconciliation/Fiber → hooks (incl. 18/19) → Suspense → state management → performance | [10.3-react](10-frontend/10.3-react/INDEX.md) |
| 1.5 | **Next.js** | App Router → RSC → Server Actions → caching layers → streaming | [10.4-next.js](10-frontend/10.4-next.js/INDEX.md) |

*Skip-until-needed:* forms ([10.5](10-frontend/10.5-form-handling/INDEX.md)), animation ([10.6](10-frontend/10.6-animation/INDEX.md)), HTML/CSS ([10.7](10-frontend/10.7-html-css/INDEX.md)).

**Checkpoint 1:** Explain the event loop with a printed-output ordering puzzle; write a typed generic utility live; explain when RSC beats client components. Mock questions: [10.1.26-interview-questions](10-frontend/10.1-javascript/10.1.26-interview-questions.md).

---

## Phase 2 — Backend Core *(Weeks 3–5, the heart of senior screens)*

### 2.1 Runtime & framework
| Order | Topic | Flow inside |
|---|---|---|
| 2.1.1 | [Node.js](20-backend/20.1-node.js/INDEX.md) | event loop → streams → clustering → child processes → security |
| 2.1.2 | [NestJS](20-backend/20.2-nestjs/INDEX.md) | modules → DI → pipes/guards/interceptors/filters → CQRS → testing |

### 2.2 API layer
| Order | Topic | Flow inside |
|---|---|---|
| 2.2.1 | [REST fundamentals](20-backend/20.3-rest-apis/INDEX.md) | principles → methods/status codes → versioning → pagination → error handling → caching |
| 2.2.2 | [API design advanced](20-backend/20.10-api-design/INDEX.md) | maturity model → rate limiting algorithms → RFC 7807 → webhooks → gRPC streaming |
| 2.2.3 | [GraphQL](20-backend/20.7-graphql/INDEX.md) *(if JD asks)* | schema design → resolvers → N+1/DataLoader → security |

### 2.3 Data
| Order | Topic | Flow inside |
|---|---|---|
| 2.3.1 | [PostgreSQL core](20-backend/20.4-database/INDEX.md) | normalization → indexes → transactions/MVCC → joins → execution plans → deadlocks |
| 2.3.2 | [Postgres at scale](20-backend/20.4-database/INDEX.md) | connection pooling → replication → partitioning/sharding theory ([30.2 theory](30-architecture/30.2-system-design/00-theory/INDEX.md)) → performance |
| 2.3.3 | ORM & Redis | [Prisma](20-backend/20.4-database/20.4.10-prisma.md) → [Prisma advanced](20-backend/20.4-database/20.4.19-prisma-advanced.md) → [Redis patterns](20-backend/20.4-database/20.4.16-redis.md) |
| 2.3.4 | [Caching](20-backend/20.8-caching/INDEX.md) | cache-aside/write-through/write-behind → invalidation → stampede defense → advanced Redis |

### 2.4 🔐 Auth & Security — *the dedicated learning track*
Study as one connected story, not isolated files → **[20-backend/20.5-security/auth/INDEX.md](20-backend/20.5-security/auth/INDEX.md)**

| Stage | Topic | Trade-off you must be able to defend |
|---|---|---|
| 0 | [Fundamentals](20-backend/20.5-security/auth/auth-fundamentals.md) | hashing vs encryption vs signing; Argon2 params |
| 1 | [Sessions & cookies](20-backend/20.5-security/auth/sessions-cookies.md) | server state + instant revocation vs scale |
| 2 | [JWT](20-backend/20.5-security/auth/jwt.md) | statelessness vs revocation; HS256 vs RS256; storage XSS/CSRF matrix |
| 3 | [OAuth2/OIDC](20-backend/20.5-security/auth/oauth2-oidc.md) | delegation flows; PKCE; scopes vs roles |
| 4 | [RBAC/ABAC](20-backend/20.5-security/auth/rbac-abac.md) | coarse vs fine-grained authz; policy engines |
| ⚔️ | Attacks: [XSS](20-backend/20.5-security/20.5.03-xss.md) · [CSRF](20-backend/20.5-security/20.5.04-csrf.md) · [SQLi](20-backend/20.5-security/20.5.05-sql-injection.md) · [API Top 10](20-backend/20.5-security/20.5.12-api-security-best-practices.md) | each attack ↔ its exact defense |
| 🛡️ | Hardening: [headers/CSP](20-backend/20.5-security/20.5.09-web-security.md) · [STRIDE](20-backend/20.5-security/20.5.10-threat-modeling-stride.md) · [secrets](20-backend/20.5-security/20.5.11-secrets-management.md) | threat-model any feature in 5 min |
| 🎤 | Drill: [auth Q&A](20-backend/20.5-security/auth/interview-questions.md) + [full bank](20-backend/20.5-security/20.5.13-interview-questions.md) | survive the follow-up traps |

### 2.5 Distributed backend
| Order | Topic | Flow inside |
|---|---|---|
| 2.5.1 | [Microservices patterns](20-backend/20.6-microservices/INDEX.md) | gateway → discovery → saga → circuit breaker → Kafka/RabbitMQ → event sourcing/CQRS → idempotency |
| 2.5.2 | [Event-driven](20-backend/20.11-event-driven/INDEX.md) | when events beat requests; outbox pattern; DLQ discipline |
| 2.5.3 | [Infra patterns mirror](30-architecture/30.3-infra-patterns/INDEX.md) | retry/backoff, bulkhead, strangler fig, health checks, graceful shutdown |
| 2.5.4 | [Real-time](60-realtime/60.1-websockets/INDEX.md) *(JD-dependent)* | WS vs SSE vs polling → scaling with pub/sub → presence |

**Checkpoint 2:** Whiteboard "design the auth for a multi-tenant SaaS" in 10 min using only the trade-off tables; explain MVCC + one deadlock you've debugged; pick pagination strategy for a cursor-per-feed and defend it.

---

## Phase 3 — Architecture & System Design *(Weeks 6–7, the senior differentiator)*

| Order | Topic | Flow inside |
|---|---|---|
| 3.1 | [Design patterns](30-architecture/30.1-design-patterns/INDEX.md) | SOLID → GoF applied (Strategy, Repository, Observer, DI…) → CQRS in practice |
| 3.2 | [SD method](30-architecture/30.2-system-design/00-theory/30.2.1.15-how-to-approach.md) | clarify → estimate → high-level → deep-dive (memorize this skeleton) |
| 3.3 | [SD theory](30-architecture/30.2-system-design/00-theory/INDEX.md) | CAP → consistency models → sharding → caching → queues → rate limiting → consensus → failure modes → backpressure → multi-region |
| 3.4 | [Case studies ×20](30-architecture/30.2-system-design/10-case-studies/INDEX.md) | URL shortener → WhatsApp → Uber → Netflix → payment gateway → ticket booking → notification service → hospital mgmt… practice 5 aloud with a timer |

**Checkpoint 3:** Record yourself doing URL shortener + ticket booking in 45 min each; review against the 4-phase rubric; no silent minutes.

---

## Phase 4 — Platform & Delivery *(Week 8)*

| Order | Topic | Depth needed |
|---|---|---|
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
|---|---|---|
| 5.1 | [Testing](50-quality/50.1-testing/INDEX.md) | pyramid → Jest/Vitest → RTL → integration → E2E (Playwright) → mocking → test patterns |
| 5.2 | [Performance](50-quality/50.3-performance-monitoring/INDEX.md) | Core Web Vitals → profiling → budgets → RUM |
| 5.3 | [Accessibility](50-quality/50.2-accessibility/INDEX.md) | WCAG → ARIA → keyboard → testing (asked less, cheap to know) |
| 5.4 | [Production engineering](50-quality/50.4-production-engineering/INDEX.md) | incident response → SLI/SLO/error budgets → chaos basics |

**Checkpoint 5:** State your testing pyramid ratios and what you'd never leave untested; name INP/LCP/CLS thresholds cold.

---

## Phase 6 — Interview Toolkit *(continuous from Week 1, intensifies Week 9+)*

| Track | When | Contents |
|---|---|---|
| [Coding patterns](70-interview-toolkit/70.2-coding-patterns/INDEX.md) | FAANG lane: daily · Abroad lane: light (30–40 mediums) | sliding window → two pointers → BFS/DFS → DP → heap → trie → union-find → backtracking |
| [Behavioral](70-interview-toolkit/70.1-behavioral/INDEX.md) | Weeks 1–2, then weekly reps | STAR(+R) → leadership → conflict → failure stories |
| [Cheat sheets](70-interview-toolkit/70.3-cheatsheets/INDEX.md) | Final week | JS/TS/React/backend/system-design one-pagers |

Start [00-strategy](00-strategy/INDEX.md) items here if not done in Phase 0: [resume](00-strategy/00.02-resume-tips.md) → [STAR](00-strategy/00.03-star-method.md) → [HR questions](00-strategy/00.04-hr-questions.md).

**Checkpoint 6:** 8 STAR stories rehearsed out loud and recorded; 18 patterns each solved once fresh.

---

## Phase 7 — Lane Execution *(final 1–2 weeks before applying)*

### Abroad/EU lane → [80-lanes-abroad-full-stack](80-lanes-abroad-full-stack/INDEX.md)
1. [Take-home playbook](80-lanes-abroad-full-stack/80.01-take-home-playbook.md) → ship one practice build ([starter prompt](80-lanes-abroad-full-stack/80.15-take-home-starter-prompt.md))
2. [System design EU patterns](80-lanes-abroad-full-stack/80.03-system-design-eu-patterns.md) + [case bank](80-lanes-abroad-full-stack/80.08-system-design-case-bank.md)
3. Company prep: [profiles](80-lanes-abroad-full-stack/80.07-company-profiles.md) · [prep sheets](80-lanes-abroad-full-stack/80.32-company-prep-sheets.md)
4. Target-company packs: **Docita** → [resume defense](80-lanes-abroad-full-stack/80.16-docita-resume-defense.md) · [evidence pack](80-lanes-abroad-full-stack/80.17-docita-interview-evidence-pack.md) · [Google-level bank](80-lanes-abroad-full-stack/80.21-docita-google-level-prep.md) · [topic mapping](80-lanes-abroad-full-stack/80.22-docita-tech-topic-mapping.md)
5. Logistics: [comp benchmarking](80-lanes-abroad-full-stack/80.05-comp-eu-benchmarking.md) · [visa playbook](80-lanes-abroad-full-stack/80.06-visa-relocation-playbook.md)

### FAANG lane → [81-lanes-indian-sde-faang](81-lanes-indian-sde-faang/INDEX.md)
1. [Complete guide](81-lanes-indian-sde-faang/81.01-complete-guide.md) → [LeetCode study plan](81-lanes-indian-sde-faang/81.06-leetcode-study-plan.md) (daily, from Week 3 onward really)
2. [Core CS](81-lanes-indian-sde-faang/81.02-core-cs-fundamentals.md) → [advanced topics](81-lanes-indian-sde-faang/81.05-advanced-topics.md)
3. Company guides: [Google](81-lanes-indian-sde-faang/81.17-google-interview-guide.md) · [Amazon](81-lanes-indian-sde-faang/81.18-amazon-interview-guide.md) · [Meta](81-lanes-indian-sde-faang/81.19-meta-interview-guide.md) · [Microsoft](81-lanes-indian-sde-faang/81.16-microsoft-azure-interview-guide.md)

**Checkpoint 7:** 3 applications sent while still polishing (real feedback > perfect prep).

---

## Two Speeds: Full vs Fast

### 🐢 Full speed — 9–10 weeks (~3 h/day)
Follow phases 0→7 in order exactly as laid out. Best if switching stacks or rustier than you admit.

### 🐇 Fast speed — 4 weeks (~2–3 h/day), for the currently-employed-and-sharp
| Week | Do | Skip |
|---|---|---|
| 1 | Phase 0 + Phase 1 (skim 1.1–1.2, full 1.3–1.5) + 8 STAR stories | animation, HTML/CSS |
| 2 | Phase 2.2–2.3 (APIs + data) + **auth track** + start coding patterns | GraphQL unless JD |
| 3 | Phase 2.5 (microservices skim) + Phase 3 (method + 5 cases) + take-home OR DSA block | K8s depth, a11y |
| 4 | Phase 4 skim (Docker/CI/observability) + Phase 6 drills + Phase 7 lane execution + apply | monorepo, CDN, chaos |

### 🚨 Emergency — 1 week
Non-negotiables only: 8 STAR stories · URL shortener + 1 domain case cold · auth trade-off table memorized · take-home template ready · 2 mocks (details in the [lane 80 index](80-lanes-abroad-full-stack/INDEX.md)).

---

## Checkpoints — Do Not Skip

Every checkpoint is a gate: fail it, revisit that phase before advancing.

| # | Gate | Pass condition |
|---|------|----------------|
| 0 | Lane chosen | Bar + comp range stated out loud |
| 1 | Frontend core | Event-loop ordering puzzle solved live; generic utility written live |
| 2 | Backend core | Multi-tenant auth whiteboarded in 10 min; MVCC explained with example |
| 3 | System design | 2 recorded 45-min designs reviewed against 4-phase rubric |
| 4 | Platform | Deploy pipeline sketched incl. failure modes + one SLO defined |
| 5 | Quality | Pyramid ratios + CWV thresholds stated cold |
| 6 | Toolkit | 8 STAR stories recorded; all 18 patterns solved once fresh |
| 7 | Lane | 3 applications sent; mock loop completed |

---

## Weekly Rhythm (any speed)

| Day | Block 1 (90') | Block 2 (60') |
|-----|---------------|---------------|
| Mon–Thu | Current phase material | Coding pattern of the day (FAANG) or SD reading (abroad) |
| Fri | Catch-up / re-read flagged files | Flashcards from cheat sheets |
| Sat | Timed mock or recorded design | Story rehearsal out loud |
| Sun | Rest · 15-min weekly review against this roadmap | update tracker |

Trackers: [80.33-weekly-study-tracker](80-lanes-abroad-full-stack/80.33-weekly-study-tracker.md) · [81 daily timer](81-lanes-indian-sde-faang/81.11-daily-study-timer.md)

---

## Navigation

[🏠 INDEX.md](INDEX.md) · [README](README.md) · Lane indexes: [Abroad/EU](80-lanes-abroad-full-stack/INDEX.md) · [Indian SDE/FAANG](81-lanes-indian-sde-faang/INDEX.md)

*Last updated: August 2026*
