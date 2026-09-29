# Abroad Full-Stack Lane — The Complete Reference

> **For senior full-stack engineers (5+ YoE) targeting mid-stage EU / non-Indian startups** — companies like LiveEO, Snke, MVST, n8n, SumUp, Scalable Capital, Tanso. Take-home + system design + behavioral heavy. **No LeetCode grinding.** 4-6 week realistic prep, 50-55 hours total.

[![Files](https://img.shields.io/badge/files-36-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Table of Contents

| # | Section | Purpose |
| --- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | [Lane Decision](#lane-decision--is-this-the-right-lane-for-you) | When to use this lane (decision matrix with / per company type) |
| 2 | [Reference Topics — What You Need to Know](#reference-topics--what-you-need-to-know) | The checklist — what you need to know (3 tiers: mandatory / common / differentiator + skip list). This is the "perfect reference" part. |
| 3 | [Interview Process — Round-by-Round](#interview-process--round-by-round) | Round-by-round — what each round tests, format, duration, what gets you rejected, how to prep |
| 4 | [Strategy — How to Prep, What to Skip, When to Apply](#strategy--how-to-prep-what-to-skip-when-to-apply) | The 80/20 — what to skip, when to start applying, comp strategy (5 country tiers), visa strategy (8 countries) |
| 5 | [Files in This Lane](#files-in-this-lane) | Current deliverables (with file counts) |
| 6 | [Cross-references to Core Sections (1-7 + 0)](#cross-references-to-core-sections) | Where to study (the 8 themed groups) |
| 7 | [FAQ](#faq) | Common questions |
| 8 | [Navigation](#navigation) | ← Previous · Home · Sibling Lane → |

---

## Lane Decision — Is This the Right Lane for You?

| If you are targeting... | Use this lane (80)? | Or use Indian SDE (81)? |
| ---------------------------------------------------------------------------------------- | :---------------------: | :---------------------------------------------------------------------------------------------: |
| **EU / non-Indian mid-stage startups** (LiveEO, Snke, MVST, n8n, SumUp, Scalable, Tanso) | **primary** | — |
| **Remote-first US companies** (Stripe, Linear, Vercel, Supabase, Resend, Clerk) | **primary** | — |
| **EU Big Tech** (Booking.com, Spotify, Klarna, Truecaller) | **primary + secondary** | use 81 too for the DSA signal |
| **FAANG in EU** (Google Zürich, Meta London, Microsoft Dublin, Apple Cork) | secondary | **primary** |
| **Indian in-country** (in Bengaluru, Hyderabad, etc.) | — | **primary** |
| **US FAANG on-site** (Google MTV, Meta Menlo Park) | — | **primary** |
| **Junior roles (under 3 YoE)** | — | start with `10-frontend/10.1-javascript/` and `10-frontend/10.2-typescript/` fundamentals first |

**Quick heuristic:** if you need **work authorization in the target country** (EU Blue Card applies with an offer — no employer sponsorship needed) AND the company is **mid-stage (Series A–D, 50-1000 people)**, you're in this lane. If you're targeting a US-based company from India without needing US visa, you're also in this lane. Everything else → 31.

**The "both" case:** European companies like Booking.com and Spotify run FAANG-style loops (DSA + system design + behavioral). For them, **use both lanes** — start with 31 for the FAANG-DSA signal, then layer 32's family/visa/relocation overlay.

---

## Reference Topics — What You Need to Know

This is a **reference checklist** of every topic a senior abroad full-stack candidate should be able to discuss confidently. It is **non-duplicative** with the core stacks 1-7 + 0 (which contain the actual deep-dive content). This is the **what to be ready for**; the core sections are **where to study it**.

### Tier 1 — Mandatory, will be asked in 90%+ of interviews

| Topic | What you need to demonstrate | Where to study |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **TypeScript at senior level** | Generics, conditional types, `satisfies` operator, narrowing, mapped types, declaration files. Can read and write type-safe APIs without `any`. | [TypeScript](../10-frontend/10.2-typescript/INDEX.md) |
| **React 18-19 + hooks** | `useTransition`, `useDeferredValue`, `use(promise)`, `useOptimistic`, ref-as-prop, Suspense + Error Boundary, Server Components understanding. | [React](../10-frontend/10.3-react/INDEX.md) |
| **Next.js 15 App Router** | Server Components vs Client Components, Server Actions, Middleware, Route Handlers, streaming, image optimization, caching. | [Next.js](../10-frontend/10.4-next.js/INDEX.md) |
| **Node.js runtime** | Event loop, streams, child processes, clustering, file system, web streams API, test runner. Can debug a memory leak or event loop stall. | [Node.js](../20-backend/20.1-node.js/INDEX.md) |
| **NestJS or similar backend framework** | Modules, DI, guards, pipes, interceptors, exception filters, middleware. Comfortable with a TS-first backend. | [NestJS](../20-backend/20.2-nestjs/INDEX.md) |
| **REST or GraphQL API design** | Status codes, versioning, pagination, auth flows, OpenAPI spec, error handling, HTTP caching. | [REST API](../20-backend/20.3-rest-apis/INDEX.md), [GraphQL](../20-backend/20.7-graphql/INDEX.md) |
| **PostgreSQL** | Schema design, normalization, indexes (B-tree, partial, covering), transactions + MVCC, query planning, connection pooling, migrations. | [Database](../20-backend/20.4-database/INDEX.md) |
| **Auth + security** | JWT vs session, RBAC, audit logging for regulated domains, OWASP API Top 10 (BOLA, BFLA, mass assignment, SSRF), secrets management. | [Security](../20-backend/20.5-security/INDEX.md) |
| **System design at 45 min** | URL shortener, notification service, ticket booking, hospital mgmt, payment gateway, rate limiter, message broker. 4-phase approach: clarify → estimate → high-level → deep-dive. | [System Design](../30-architecture/30.2-system-design/INDEX.md) |
| **Microservices patterns** | Service discovery, API gateway, saga, circuit breaker, event sourcing, idempotency, distributed transactions. | [Microservices](../20-backend/20.6-microservices/INDEX.md) |
| **CI/CD + Docker** | GitHub Actions, multi-stage Dockerfiles, blue-green/canary, observability integration. | [Docker](../40-platform/40.1-docker/INDEX.md), [CI/CD](../40-platform/40.3-ci-cd) |
| **Testing strategy** | Unit + integration + E2E layering, mocking patterns, when to use Testcontainers, coverage gates, Playwright for E2E. | [Testing](../50-quality/50.1-testing/INDEX.md) |
| **Observability basics** | Structured logging, request IDs, alerting, SLI/SLO, on-call etiquette. You don't have to be an SRE but you should know what good looks like. | [Observability](../40-platform/40.4-observability/INDEX.md) |
| **Behavioral — STAR stories** | 5-8 stories mapped to common questions, punchline-first, with Reflection. Senior signal = "what would you do differently." | [Behavioral](../70-interview-toolkit/70.1-behavioral/INDEX.md) + your own [story-bank.md](80.12-story-bank.md) |

### Tier 2 — Asked in 50-70% of interviews (mid-stage senior)

| Topic | What you need to demonstrate | Where to study |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **K8s basics** | Pods, deployments, services, ingress, ConfigMaps, HPA, health checks. You don't have to be a K8s admin, but you should know what a Deployment does. | [Kubernetes](../40-platform/40.2-kubernetes/INDEX.md) |
| **Performance + Core Web Vitals** | LCP / INP / CLS, RUM, Lighthouse CI, bundle analysis, performance budgets. | [Performance Monitoring](../50-quality/50.3-performance-monitoring/INDEX.md) |
| **Accessibility (a11y)** | WCAG 2.1 AA basics, ARIA, keyboard navigation, color contrast, form labels. | [Accessibility](../50-quality/50.2-accessibility/INDEX.md) |
| **Build tooling** | Webpack vs Vite vs Turbopack vs Rspack — when to use which. SWC vs Babel. Module federation. | [Build Tools](../40-platform/40.5-build-tools/INDEX.md) |
| **WebSockets / real-time** | When to use WS vs SSE vs polling, Socket.IO patterns, scaling. | [WebSockets](../60-realtime/60.1-websockets/INDEX.md) |
| **Serverless / Edge** | When to use Lambda/Vercel Edge vs containers, cold starts, edge functions. | [Serverless & Edge](../40-platform/40.7-serverless-edge/INDEX.md) |
| **Design patterns** | Repository, Strategy, Observer, DI, CQRS, Module, State. Don't memorize — apply when relevant. | [Design Patterns](../30-architecture/30.1-design-patterns/INDEX.md) |
| **Git beyond basics** | Rebase vs merge, cherry-pick, reflog, hooks, patch workflow. | [Git Advanced](../40-platform/40.6-git-advanced/INDEX.md) |
| **DSA — defensive (light)** | HashMap, Sliding Window, Two Pointers, BFS/DFS, basic DP, Stack/Queue. 30-40 mediums across these 6 patterns. **Not 100+ problems.** | [Coding Patterns](../70-interview-toolkit/70.2-coding-patterns/INDEX.md) |

### Tier 3 — Differentiator (asked 20-30%, distinguishes senior from staff)

| Topic | What you need to demonstrate | Where to study |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Frontend architecture** | State management strategy, design system, micro-frontends, performance optimization at scale. | [React](../10-frontend/10.3-react/INDEX.md) + [Build Tools](../40-platform/40.5-build-tools/INDEX.md) |
| **Distributed systems trade-offs** | CAP, eventual consistency, idempotency keys, exactly-once semantics, distributed locks. | [Microservices](../20-backend/20.6-microservices/INDEX.md) |
| **Threat modeling** | STRIDE, attack trees, secrets management at scale. | [Security](../20-backend/20.5-security/INDEX.md) |
| **Cost optimization** | AWS/GCP cost levers, multi-region trade-offs, data egress. | [Docker](../40-platform/40.1-docker/INDEX.md), [Kubernetes](../40-platform/40.2-kubernetes/INDEX.md) |
| **Engineering culture** | Mentorship, code review as teaching, RFC process, postmortem culture. | [Behavioral](../70-interview-toolkit/70.1-behavioral/INDEX.md) |
| **Compensation negotiation** | Base vs RSU trade-offs, EU 30% ruling (NL), EU Blue Card salary thresholds, sign-on vs equity. | [Compensation Benchmarking](../81-lanes-indian-sde-faang/81.22-compensation-benchmarking.md) |

### Topics to SKIP (overkill for this lane)

- Hard DP (2D, bitmask, interval)
- Segment tree, BIT, union-find, KMP/Rabin-Karp
- Bit manipulation
- Monotonic stack, queue, sliding window maximum (LeetCode hard)
- FAANG-style Bar Raiser rounds
- Onsite whiteboard (n8n / SumUp / Scalable don't do this — they use take-homes)
- Multi-round LP grind (5+ rounds is FAANG; mid-stage EU is usually 3-4 rounds)

---

## Interview Process — Round-by-Round

The mid-stage EU full-stack interview loop is **3-4 rounds**, with a heavy take-home at the front. Compared to FAANG's 5-6 rounds of LeetCode + system design + behavioral, this is shorter, faster, and more focused on shipping-production-code signal.

### Round 0: Recruiter Screen (15-30 min)

| Who | What they test | What they ask |
| ------------------------------------ | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Internal recruiter or talent partner | Basic fit: years of experience, stack, visa, location, comp expectation, motivation. | "Tell me about your current role." "Why are you looking?" "Are you open to relocation to [Berlin / Amsterdam]?" "Do you require visa sponsorship?" — answer **No** on the Blue Card path (no sponsorship needed) — "What's your comp expectation?" |

**How to prep:** Know your CV cold. Have a 60-second "tell me about yourself" answer. Have your comp range in EUR (see compensation section in [story-bank.md](80.12-story-bank.md)). Know your visa status (Blue Card eligibility, Skilled Worker visa path, 30% ruling for NL).

### Round 1: Take-Home Project (4-8 hours of your time, 1-2 weeks to complete)

| Format | What they test | Typical scope |
| --------------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Async take-home** (most common at mid-stage) | Can you ship a small full-stack feature production-quality? | A small app: REST endpoint + DB schema + minimal frontend, OR a workflow engine, OR a CLI tool, OR a frontend feature with a small backend. Usually 4-8 hours of work. |
| **Pair-programming take-home** (less common, more senior) | Same as above, but in a live coding session. | 60-90 min live build, often on a Zoom with a senior engineer. |

**What they actually evaluate (in order of importance):**
1. **Code quality** — clean structure, type-safe, readable, tests where they matter
2. **Product sense** — did you think about edge cases, UX, error states?
3. **System thinking** — schema design, API design, observability hooks, security basics
4. **Commit hygiene** — meaningful commit messages, logical PR structure
5. **Documentation** — README that explains design decisions and how to run

**What gets you REJECTED on a take-home:**
- No tests
- No README
- `any` everywhere in TypeScript
- Hardcoded credentials
- No error handling
- `git push --force` history
- "I'll add tests later" comments
- Looks AI-generated without modification

**How to ship a strong take-home:**
- Plan for 5-6 hours minimum, even if the brief says "2 hours"
- Lead with: schema design, then backend, then frontend, then tests, then README
- Use the bible's [NestJS](../20-backend/20.2-nestjs/INDEX.md) + [Database](../20-backend/20.4-database/INDEX.md) + [Security](../20-backend/20.5-security/INDEX.md) sections as your reference
- Include a short Loom video walkthrough if the brief allows
- Have a "what I'd do with 24 more hours" note in the README

### Round 2: Technical Screen (60-90 min)

| Format | What they test | Typical structure |
| ------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Live coding on a small problem** (most common) | Can you think through a coding problem in real-time? | 1-2 mediums (HashMap, sliding window, two pointers, simple BFS/DFS). 25-30 min per problem. **Not LeetCode hard.** |
| **Take-home review** (less common) | Can you defend your design decisions? | 30-45 min walk-through of your take-home code, 15-20 min deep-dive on a specific choice. |
| **System design lite** (sometimes combined) | Can you sketch an architecture for a small system? | 20-30 min on a focused problem (e.g., "design a URL shortener" at 1/3 the depth of a full SD round). |

**The DSA bar for this round is "1-2 mediums in 30 min each."** You're not expected to solve LeetCode hards. You're expected to demonstrate clear thinking, code that compiles, edge cases handled.

**What gets you REJECTED on a tech screen:**
- Cannot solve a 2-sum variant in 25 min
- Cannot debug a small bug in your own code when prompted
- No questions asked back
- Silent for 5+ minutes when stuck

**How to prep:** Practice 30-40 mediums across 6 patterns (HashMap, Sliding Window, Two Pointers, BFS/DFS, 1D DP, Stack/Queue). Time-boxed at 25-30 min each. The bible's [Coding Patterns](../70-interview-toolkit/70.2-coding-patterns/INDEX.md) has the patterns.

### Round 3: System Design (45-60 min)

| Format | What they test | What they ask |
| ----------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Whiteboard / shared doc** (most common) | Can you design a system end-to-end under ambiguity? | 1 system design problem, often company-adjacent. For n8n: workflow engine / event-driven system. For SumUp: payment gateway. For sennder: event-driven microservices. |
| **Architecture review of your take-home** (sometimes) | Can you scale your design? | "How would you scale this to 1M users?" "What breaks first?" |

**The 4-phase framework (use this every time):**
1. **Clarify** (5 min) — Functional requirements, non-functional requirements, scale estimates, out-of-scope. Ask questions. Don't start drawing.
2. **Estimate** (2 min) — QPS, storage, bandwidth. Just rough numbers. "10K DAU, 100 req/s peak, 1GB/day storage."
3. **High-level design** (10 min) — Boxes and arrows. Client → CDN → API gateway → service → DB. Don't dive deep yet.
4. **Deep-dive** (20 min) — Pick 2-3 critical components and go deep. Database schema, indexing, caching, queue, consistency. Be ready to discuss trade-offs (CAP, eventual consistency, idempotency).

**What gets you REJECTED on system design:**
- Start drawing boxes before clarifying
- No estimates (QPS, storage, bandwidth)
- Single point of failure everywhere
- "I'll just add Redis" without explaining what for
- Cannot discuss trade-offs (always picks "scale" or "consistency" without nuance)
- No observability / no failure modes

**The system design case studies the bible has:**
- [URL Shortener](../30-architecture/30.2-system-design/02-case-studies/30.2.2.01-url-shortener.md) — classic
- [Notification Service](../30-architecture/30.2-system-design/02-case-studies/30.2.2.07-notification-service.md) — retry, DLQ, fanout
- [Ticket Booking](../30-architecture/30.2-system-design/02-case-studies/30.2.2.08-ticket-booking.md) — consistency, "two users grab the last seat"
- [Hospital Management](../30-architecture/30.2-system-design/02-case-studies/30.2.2.10-hospital-management.md) — domain fit for healthcare
- [Payment Gateway](../30-architecture/30.2-system-design/02-case-studies/30.2.2.06-payment-gateway.md) — SumUp / fintech
- [Rate Limiter](../30-architecture/30.2-system-design/02-case-studies/30.2.2.13-rate-limiter.md) — n8n workflow throttling
- [Distributed Counter](../30-architecture/30.2-system-design/02-case-studies/30.2.2.20-distributed-counter.md) — hot-key sharding
- [Lyft](../30-architecture/30.2-system-design/02-case-studies/30.2.2.19-lyft.md) — geo indexing
- [How to Approach](../30-architecture/30.2-system-design/01-theory/30.2.1.15-how-to-approach.md) — read this first

**Practice 5 of these with a timer + recording.** 45 min each, then review the recording.

### Round 4: Behavioral + Culture (30-60 min, often combined with system design or async)

| Format | What they test | What they ask |
| ------------------------------------------------------ | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Async written questions** (common at EU mid-stage) | Reflection, async communication, English fluency. | "Tell me about a time you had a hard technical disagreement." "Why [company]?" "What would you do in your first 90 days?" |
| **Live behavioral** (less common) | Same. | Same questions but verbal. |
| **Founder / hiring manager call** (common for senior+) | Vision, ownership, long-term fit. | "What's your 3-year plan?" "How do you stay current?" "Why us specifically?" |

**The 8 STAR stories you should have ready** (in your own [story-bank.md](80.12-story-bank.md)):
1. **0→1 founding at Docita** — sole engineer shipped production multi-tenant SaaS
2. **30% API latency reduction at MAQ** — query tuning + indexing + caching
3. **25% faster delivery at MAQ** — refactoring around reusable TS patterns
4. **4 engineers mentored, 20% better sprint predictability**
5. **Microservices platform at Cognizant** — Spring Boot + Eureka + Zuul
6. **RBAC + audit logging for healthcare compliance**
7. **85% test coverage, 15% fewer production incidents**
8. **Production observability + incident response**

**The "Why this company?" answer (60 sec, specific, not generic):**
- Mention 1 product feature or engineering blog post that excited you
- Mention 1 specific person/team you'd learn from
- Mention 1 thing about the company culture that aligns with how you work
- Close with "and I'm particularly excited about [specific recent product/launch]"

---

## Strategy — How to Prep, What to Skip, When to Apply

### The 4-week prep plan (50-55 hours, ~2-3h/day)

| Week | Focus | Hours | Deliverable |
| ---------- | ----------------------------------------- | ------: | --------------------------------------------------------------------------------------------------------- |
| **Week 1** | Foundation + behavioral + company mapping | ~12-14h | All 8 STAR stories practiced out loud, recorded. "Tell me about yourself" at 90 sec. Mock 1 scheduled. |
| **Week 2** | Take-home project + DSA + first mock | ~14-16h | Working take-home (public GitHub, demo). 8-10 DSA mediums solved. Mock 1 done. |
| **Week 3** | System design + frontend deep-dive + DSA | ~14-16h | 4 system designs explained with timer + recording. 14-18 DSA mediums. 1-pager on Next.js 15. Mock 2 done. |
| **Week 4** | Mocks + final polish + applications | ~12-14h | 3-4 mocks completed. 4-6 applications sent. CV polished. |

Full plan in [study-plan.md](80.13-study-plan.md).

### The 80/20 — what to skip if time is short

If you have **less than 4 weeks**, drop in this order:
1. **Skip the DSA pattern practice entirely** (Tier 1 mid-stage companies don't ask hard algo, only 1-2 mediums at most)
2. **Skip advanced system design cases** (URL shortener + 1 company-adjacent case is enough)
3. **Skip the 6-pattern DSA exposure** (replace with 5 HashMap + 5 Sliding Window = 10 problems, 2 days)
4. **Skip the flashcard / spaced repetition work** (low-ROI for short timelines)
5. **Skip the 8-week FAANG schedule** (in 81-SDE-Role, not for you)

**The non-negotiable 1-week MVP:**
- 8 STAR stories practiced out loud
- 1 system design case (URL shortener) explained cold
- 1 take-home project shipped (any TS full-stack)
- 2 mock interviews done

If you can ship those, you're ready to apply. Real interview feedback is more useful than any prep.

### When to start applying

| Trigger | Apply now |
| ------------------------------------------------------------ | -------------- |
| Stories practiced cold (8 stories) | after Week 1 |
| 1 take-home shipped OR strong portfolio of personal projects | after Week 1-2 |
| 1 system design case explained cold | after Week 1-2 |
| 1 mock interview done | after Week 1-2 |

**Rule of thumb:** Send 2-3 applications in Week 1 (n8n, SumUp, etc.) while still prepping. Real interview feedback is more useful than any prep. Don't wait until "perfect."

### Comp strategy

| Tier | City | Base (senior, 5+ YoE) | Equity | Notes |
| ------- | --------------------------------- | ---------------------------: | --------- | ----------------------------------- |
| Tier 1 | Amsterdam, Berlin, Munich | EUR 75K-100K | 0.05-0.5% | Senior at mid-stage startup |
| Tier 2 | Helsinki, Stockholm, Copenhagen | EUR 65K-90K | 0.05-0.3% | Slightly tighter market |
| Tier 3 | Vienna, Lisbon, Warsaw, remote-EU | EUR 60K-85K | 0.05-0.3% | Lower cost of living, decent comp |
| Tier 4 | Paris, Madrid, Rome | EUR 70K-100K | 0.05-0.3% | Bigger cities, similar comp |
| Premium | London, Zurich | GBP 90K-130K / CHF 120K-160K | 0.05-0.2% | Higher cost of living, higher gross |

**EU Blue Card minimum (2024-25):** ~EUR 48,300/year gross (lower threshold for shortage occupations; IT usually qualifies). All Tier 1-4 base salaries above this.

**Netherlands 30% ruling:** For 5 years, 30% of your salary is tax-free. Strong comp negotiation tool.

**Family comp:** When comparing offers, factor in: spouse's Pega market in the city (Tier 1 Pega hubs: Amsterdam, London, Berlin), international school costs (EUR 15-30K/year per child), housing (Munich > Berlin > Amsterdam > Helsinki for cost).

### Visa strategy

| Country | Visa | Process time | Family |
| --------------- | -------------------------------------- | ------------ | ---------------------------------------------------------------- |
| **Netherlands** | Highly Skilled Migrant (kennismigrant) | 2-4 weeks | Spouse auto-work-permit. 30% ruling. |
| **Germany** | EU Blue Card | 6-12 weeks | Spouse work permit included. |
| **Ireland** | Critical Skills Employment Permit | 4-8 weeks | Spouse Stamp (auto work permit). |
| **Sweden** | Work Permit | 8-16 weeks | Spouse work permit included. |
| **Finland** | EU Blue Card / Residence Permit | 6-12 weeks | Spouse work permit included. |
| **UK** | Skilled Worker visa | 4-8 weeks | Spouse Dependant visa (work allowed). Minimum salary GBP 41,700. |
| **Switzerland** | B Permit | 8-12 weeks | Spouse work permit included. Quota applies. |
| **Austria** | Red-White-Red Card | 8-12 weeks | Spouse work permit included. |

**For all countries: employer typically pays visa costs + relocation package.** This is a negotiation lever, not something you pay for.

---

## Files in This Lane

### Playbooks & Reference

| # | File | Purpose | Personal example |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 01 | [Take-Home Playbook](80.01-take-home-playbook.md) | How to ship a winning take-home: 4-phase framework, 6-phase build, README template, what gets you rejected. The single highest-leverage file in this lane. | 5-6 hour take-home for a workflow engine, Loom walkthrough, full README |
| 02 | [Tech Screen Patterns](80.02-tech-screen-patterns.md) | Defensive DSA: 6 patterns, 30-40 problem set, what to skip. The bar is 1-2 mediums in 30 min, not 4 FAANG-hards. | The 35-problem recommended set across HashMap, Sliding Window, Two Pointers, BFS/DFS, 1D DP, Stack/Queue |
| 03 | [System Design — EU Patterns](80.03-system-design-eu-patterns.md) | The 4-phase framework + 6 EU-specific cases (payment gateway, workflow engine, multi-tenant SaaS, real-time booking, event-driven microservices, notification service). | Workflow engine with state machine, queue, idempotency, retries, DLQ |
| 04 | [Behavioral — EU Style](80.04-behavioral-eu-style.md) | STAR+R framework, 15 common questions with answer skeletons, EU-specific cultural fit, async written questions. | "Why this company?" 60-sec answer for n8n / SumUp / Scalable |
| 05 | [Comp — EU Benchmarking](80.05-comp-eu-benchmarking.md) | 5 city tiers, NL 30% ruling, EU Blue Card, family comp considerations, negotiation scripts, company-by-company ranges. | Tier 1 (Amsterdam, Berlin, Munich, London): EUR 75-100K base + 0.05-0.5% equity |
| 06 | [Visa & Relocation Playbook](80.06-visa-relocation-playbook.md) | 8 EU countries with visa matrix, family-driven country decision framework, relocation package negotiation, 90-day timeline. | NL Highly Skilled Migrant: 2-4 weeks, 30% ruling, family inclusion |
| 07 | [Company Profiles](80.07-company-profiles.md) | 1-pager per Tier 1/2 company: stack, interview process, comp, who to follow, recent news. The 30-min pre-interview research recipe. | n8n: TS + Vue + NestJS, EUR 80-100K + 0.05-0.2% equity, 4-day workweek |
| 08 | [System Design Case Bank](80.08-system-design-case-bank.md) | 5 EU cases to practice: workflow engine, payment gateway, multi-tenant SaaS, real-time booking, event-driven microservices. Each with framework + sample answer + trade-offs. | Workflow engine: queue + worker + state DB + idempotency, 100K executions/day at scale |
| 09 | [Quick Reference Cards](80.09-quick-reference-cards.md) | 10 one-page cheat sheets: STAR prompts, system design framework, take-home checklist, comp negotiation, country tier matrix, common DSA patterns, red flags. Print and use. | 4 highest-value cards: STAR, system design, take-home, country tier |
| 10 | [Weekly Tracker](80.10-weekly-tracker.md) | 4-week prep tracker: daily breakdown, deliverable checklist, readiness scoring, cumulative tracker. | Week 1: stories + company mapping. Week 2: take-home + DSA. Week 3: system design + DSA. Week 4: mocks + applications. |
| 11 | [Mock Interview Bank](80.11-mock-interview-bank.md) | 20 curated mock questions: 8 behavioral + 7 technical + 5 system design. 90-min mock structure. | Q1: "Tell me about yourself" 60-90 sec. Q16: "Design a workflow engine." |

### Personal Stories & Plan

| # | File | Purpose | Personal example |
| --- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 12 | [Personal Story Bank](80.12-story-bank.md) | 5-8 STAR+R stories using your real projects, ready to deliver out loud in interviews. Library, not a script — adapt to each question. | **Vamsi's 8 stories** (Docita founding, MAQ perf wins, Cognizant microservices, RBAC + audit, etc.) |
| 13 | [EU Mid-Stage Preparation Plan](80.13-study-plan.md) | 4-week, 50-55 hour plan: foundation week, take-home week, system design week, mocks + applications week. Drops LeetCode grinding in favor of take-home + system design reps. | **Vamsi's 4-week plan** with n8n / SumUp / Scalable / sennder / THRYVE targets |
| 14 | [Berlin Dual-Career Plan](80.14-berlin-dual-career-plan.md) | Vamsi + wife relocation playbook: visa, schools, neighborhoods, comp, child education, 6-week job-search plan. | 21 sections covering K-12, university, budget, sports/extracurriculars |
| 15 | [Take-Home Starter Prompt](80.15-take-home-starter-prompt.md) | Workflow engine on NestJS + Prisma + Next.js 15 — the canonical EU mid-stage take-home build. | 5-6 hour build with state machine, queue, idempotency, retries, DLQ |
| 16 | [Docita Resume Defense](80.16-docita-resume-defense.md) | 130 fact-bounded questions anchored to the current Docita code, in a three-level truth contract (code-confirmed / product metric / personal). Covers architecture, backend, frontend, security, reliability, delivery, ownership, plus deep-dive and cost sections (v2-corrected to real infra: Fly.io/Cloudflare/RDS). Read before any call. | 20 sections: product → architecture → NestJS/Prisma → security → reliability → migrations → multi-region design exercises → cost |
| 17 | [Docita Interview Evidence Pack](80.17-docita-interview-evidence-pack.md) | Fast pre-interview refresh: approved metrics, 60-second pitch, source-grounded technical answers, trade-offs, safe evidence map. | 25+ clinics, 1,000+ appointments/month, ABAC, RLS, outbox, idempotency, safe performance-answer rules |
| 18 | [Resume Claim Crosswalk](80.18-resume-claim-crosswalk.md) | Claim-by-claim Docita evidence ledger plus coverage map for resume skills, role questions, proof packet, and explicit exclusions. | 149-model schema, five-application topology, ABAC/RLS/audit evidence, analytics-only metrics |
| 19 | [Langfuse Interview Prep](80.19-langfuse-interview-prep.md) | Q&A for **Langfuse** (separate target — not Docita): Turborepo, tRPC, Next.js App Router, Prisma, OpenTelemetry, ClickHouse, LLM observability, system design. Verify company facts on their careers page before quoting figures. | Full TypeScript monorepo stack, tRPC type safety, ClickHouse OLAP schema, OpenTelemetry instrumentation |
| 20 | [Germany Visa & Relocation-Support Companies](80.20-germany-visa-relocation-companies.md) | 100+ German tech companies that hire non-EU engineers. EU Blue Card needs no employer sponsorship (offer letter + degree recognition). Tier 1-4 company lists, visa timeline, anabin degree check, how to find Blue Card-ready employers. | EU Blue Card EUR 48,300 threshold, 60-90 day timeline, Berlin/Munich/Hamburg hubs |
| 21 | [Google-Level Docita Prep](80.21-docita-google-level-prep.md) | **v2 — rebuilt against the actual repo.** 70+ senior/staff questions: verified fact sheet + deployment topology, multi-tenancy (ALS+RLS), Postgres queue & outbox, field-level encryption with versioned keys, security pipeline, reliability drills, system-design cases, behavioral anchors, rapid-fire. Each answer: 30-sec version → depth → follow-ups → what-NOT-to-claim. | Postgres-as-queue (SKIP LOCKED), outbox produce-once, ABAC engine, refresh-family revocation, Hono edge proxy, Fly scale-to-zero |
| 22 | [Docita × Tech Topic Mapping](80.22-docita-tech-topic-mapping.md) | Concept→domain vocabulary map for 13 topic areas. Rows tagged: untagged = code-grounded; **[future]** = aspirational design exercise — present as roadmap, never current practice. | Cache stampede at clinic opening, DLQ replay flow, tenancy in every design dimension |
| 23 | [German Companies Database](80.23-german-companies-database.md) | 50+ German product companies with stack, comp, interview process, visa support. Tier 1-3 classification. Best companies by category (fintech, SaaS, e-commerce, data, remote-first). | Scalable Capital EUR 90-110K, n8n 4-day workweek, SumUp profitable payments, Celonis process mining, Trade Republic EUR 85-110K |
| 24 | [EU Regulatory Compliance](80.24-eu-regulatory-compliance.md) | GDPR principles and implementation, BaFin fintech requirements (KYC/AML/PSD2), EU AI Act risk categories, Digital Services Act, DORA. Includes DPIA template and compliance checklist. | GDPR data subject rights, BaFin KYC/AML implementation, EU AI Act healthcare classification, incident response within 72 hours |
| 25 | [German Workplace Culture](80.25-german-workplace-culture.md) | German engineering culture (Gründlichkeit, Ordnung, Pünktlichkeit), interview etiquette, communication style, work-life balance, probation period, salary negotiation, red flags. | Punctuality, directness, 25-30 days vacation, 37.5-40h/week, Probezeit 6 months |
| 26 | [Take-Home Masterclass](80.26-take-home-masterclass.md) | 6-phase take-home process, 4 common patterns (CRUD, workflow, multi-tenant, real-time), what separates good from great, README template, time management, common mistakes. | Architecture first, tests as you go, RFC 7807 errors, Docker Compose, 'what I'd do with 24 more hours' section |
| 27 | [German System Design Patterns](80.27-german-system-design-patterns.md) | Company-adjacent system design for fintech (payment processing, trading, portfolio), logistics (freight matching, real-time tracking), healthtech (appointment scheduling, PHI), SaaS (multi-tenant, workflow engine). | Idempotent payments, PostGIS freight matching, concurrent booking with SELECT FOR UPDATE, DAG workflow execution |
| 28 | [Interview Prep Roadmap](80.28-interview-prep-roadmap.md) | 4-week plan: Week 1 (stories + foundation), Week 2 (system design + take-home), Week 3 (deep-dives + company research), Week 4 (mocks + applications). Daily tasks with checkboxes, progress tracker, 1-week emergency plan. | 868 files, 366K lines, Docita v2 bank, 31 SD cases, 8 STAR stories |
| 29 | [Topic Brushup Roadmap](80.29-topic-brushup-roadmap.md) | 30-day systematic brushup of every section: Week 1 (Frontend), Week 2 (Backend), Week 3 (Architecture + Platform), Week 4 (Quality + Toolkit). 550 files, daily checkboxes, progress tracker. | Covers all 868 files (10-frontend through 80-lanes) |
| 30 | [Mock Interview Script](80.30-mock-interview-script.md) | 10 high-impact questions with timing, scoring rubric, and follow-up probes. Covers system design, PostgreSQL, caching, Kafka, security, API design, observability, testing, and behavioral. | Record yourself, score 1-5, retake until 45/50 |
| 31 | [Salary Negotiation Guide](80.31-salary-negotiation-guide.md) | German tech salary ranges by tier, Blue Card thresholds, total comp breakdown, counter-offer scripts, relocation negotiation, contract tips. | €80K-€130K senior range, 10-20% above first offer, negotiate via phone |
| 32 | [Company Prep Sheets](80.32-company-prep-sheets.md) | Deep-dive prep ordered by current target priority: **LiveEO** (satellite analytics — verified stack/process), **Snke** (Brainlab-spin-off hospital platform), **MVST** (digital product studio — corrected profile), plus Redcare, Tanso, n8n. Verified talking points, likely questions, questions-to-ask per company. | Read before each interview; pair with the domain primer |
| 33 | [Weekly Study Tracker](80.33-weekly-study-tracker.md) | 4-week daily checklist with time tracking, progress metrics, mock interview scores, story practice, and company applications. | Print and check off daily, review progress every Sunday |
| 34 | [Germany Target Domain Primer](80.34-germany-target-domain-primer.md) | Domain fluency for the target cluster: healthtech (MDR vs certified, FHIR/DICOM/HL7, gematik/TI/ePA, hospital IT landscape) and geospatial (PostGIS patterns, COG/STAC/tiles, change-detection pipeline drill) — plus a Docita→domain mapping table and night-before glossary. | Study alongside company sheets for LiveEO/Snke/MVST interviews |
| 35 | [Germany Target Engine](80.35-germany-target-engine.md) | Status-aware Munich-first (+Berlin) pipeline: ATS auto-rejection diagnosis + fixes shipped to the resume, new English-speaking targets (NavVis , Konux, DeepOpinion, Helsing…), weekly operating loop with career-ops, DM skeletons, and funnel metrics. | Review every Sunday; update status tables |
| 36 | [Docita Complete Interview Defense](80.36-docita-complete-interview-defense.md) | **Comprehensive guide:** clinic workflows (29 domains), architecture overview, 7 key decisions with trade-offs, testing strategy (~1,092 executed E2E across the browser matrix; ~5,077 non-e2e test cases), metrics breakdown, 7-layer security, 8 Q&A scripts, code evidence map. The single file to read before any interview. | Memorize: metrics table, architecture diagram, trade-off answers |
| — | [**Docita Architecture Deep Dives**](../projects/docita/INDEX.md) | **22 files** — every decision justified: alternatives considered, what worked, what failed, what could be better, code evidence, interview scripts. Covers: DDD, Zod-first, multi-tenancy/RLS, async processing, payment flows, clinic workflows, WhatsApp, prescriptions, billing, subscriptions, deployment, retrospective, insurance claims, IPD, inventory, analytics/dashboards, doctors & public booking, patient portal, ABDM, enterprise contracts, documents/uploads, clinical/lab & medical coding, long-tail domains. | Read the numbered 01–22 series before any Docita-heavy interview |
| — | [Personal workspace](personal/README.md) | Single source of truth for personal data — CV, portals config, profile, **live** application tracker, [outreach playbook with recruiter DMs](personal/outreach-playbook.md), targets, relocation bible. career-ops accesses these via symlinks; `doctor.sh` verifies the wiring. | Edit freely here · run doctor.sh after tool runs · commit = backup |

---

## Cross-references to Core Sections

These are the **where to study** sections. The reference topics above are the **what to be ready for** checklist.

**Core fundamentals:** [Interview Strategy](../00-strategy/INDEX.md) · [JavaScript](../10-frontend/10.1-javascript/INDEX.md) · [TypeScript](../10-frontend/10.2-typescript/INDEX.md) · [React](../10-frontend/10.3-react/INDEX.md) · [Next.js](../10-frontend/10.4-next.js/INDEX.md)

**Backend, API & Data:** [Node.js](../20-backend/20.1-node.js/INDEX.md) · [NestJS](../20-backend/20.2-nestjs/INDEX.md) · [REST API](../20-backend/20.3-rest-apis/INDEX.md) · [Database](../20-backend/20.4-database/INDEX.md) · [GraphQL](../20-backend/20.7-graphql/INDEX.md)

**Architecture & Design:** [Security](../20-backend/20.5-security/INDEX.md) · [Design Patterns](../30-architecture/30.1-design-patterns/INDEX.md) · [System Design](../30-architecture/30.2-system-design/INDEX.md) · [Microservices](../20-backend/20.6-microservices/INDEX.md)

**DevOps, Observability & Tooling:** [Docker](../40-platform/40.1-docker/INDEX.md) · [Kubernetes](../40-platform/40.2-kubernetes/INDEX.md) · [CI/CD](../40-platform/40.3-ci-cd) · [Observability](../40-platform/40.4-observability/INDEX.md) · [Build Tools](../40-platform/40.5-build-tools/INDEX.md) · [Git Advanced](../40-platform/40.6-git-advanced/INDEX.md) · [Serverless & Edge](../40-platform/40.7-serverless-edge/INDEX.md)

**Testing & Quality:** [Testing](../50-quality/50.1-testing/INDEX.md) · [Accessibility](../50-quality/50.2-accessibility/INDEX.md) · [Performance Monitoring](../50-quality/50.3-performance-monitoring/INDEX.md)

**Real-time:** [WebSockets](../60-realtime/60.1-websockets/INDEX.md)

**Interview prep:** [Behavioral](../70-interview-toolkit/70.1-behavioral/INDEX.md) · [Coding Patterns](../70-interview-toolkit/70.2-coding-patterns/INDEX.md)

**Reference & quick-look:** [Cheat Sheets](../70-interview-toolkit/70.3-cheatsheets/INDEX.md) · [Monorepo](../40-platform/40.8-monorepo/INDEX.md) · [Form Handling](../10-frontend/10.5-form-handling/INDEX.md) · [Animation](../10-frontend/10.6-animation/INDEX.md)

---

## FAQ

**Q: I want to apply to Booking.com (Amsterdam) AND Microsoft (Dublin). Which lane?**
A: Both. Use `81-lanes-indian-sde-faang/` for the Microsoft DSA signal (phone screen, 28-phase LeetCode), `80-lanes-abroad-full-stack/` for the Booking take-home + system design + family/visa overlay. The lanes are complementary, not exclusive.

**Q: I'm a frontend specialist. Do I still need the take-home?**
A: Yes. Even for frontend-heavy roles, the take-home often includes a small backend (NestJS/Express endpoint, JWT auth, Prisma schema). The [NestJS](../20-backend/20.2-nestjs/INDEX.md), [Database](../20-backend/20.4-database/INDEX.md), and [Security](../20-backend/20.5-security/INDEX.md) sections are the prep.

**Q: I'm targeting remote-first US companies (Stripe, Linear, Vercel) from India. Which lane?**
A: Primarily this lane (English-only, take-home + system design, visa not needed). The remote-first US market is closer to EU mid-stage than to FAANG. Adjust the comp expectations up ($130-180K TC) but the prep structure is the same.

**Q: How long should I prep?**
A: 4 weeks is the realistic minimum at 2-3 hrs/day. 6 weeks if you have more time and want a slower ramp. The plan is designed to be flexible.

**Q: When should I start applying?**
A: After Week 1 of the plan. Send 2-3 applications in Week 1 (n8n, SumUp, etc.) while still prepping — the actual application feedback is more useful than any prep. Real applications > perfect prep.

**Q: I have a non-TS stack (Java / Python / Go). Do I still fit?**
A: Yes, but the bible's bias is TypeScript. Adjust the take-home project to your stack. Most of the system design, security, and observability content is stack-agnostic.

**Q: How many applications should I send?**
A: 10-15 well-targeted over 4-6 weeks. Below 5 = low offer probability. Above 25 = preparation dilution. The 3 application packages ready (n8n, SumUp, Scalable Capital) cover Tier 1.

**Q: My wife is in a different field (Pega, healthcare, etc.). How does the country choice work?**
A: Tier 1 Pega market: Netherlands (Rabobank, ING, ABN AMRO), UK (HSBC, Barclays), Germany (T-Systems, Allianz). For healthcare: Germany (largest EU market), UK, France. For consulting: all Tier 1 cities. **This is why the family/relocation question is part of the country tier list** — the country that maximizes both your job and your spouse's job is the right one.

---

## When to add to this lane

This lane is a living scaffold. As you go through interviews, add:

- **New company profiles** — for each Tier 1 company, add a 1-pager in `interview-prep/{company}-research.md`
- **New system design case studies** — once you solve a case interview well, add the case + your answer framework
- **New take-home projects** — once you ship one, link it here as a reference build
- **Post-interview retrospectives** — what worked, what didn't, what to adjust

---

## Navigation

[← Previous: Animation](../10-frontend/10.6-animation/INDEX.md) · [ Back to Index](../INDEX.md) · [Sibling Lane: Indian SDE / FAANG (81) →](../81-lanes-indian-sde-faang/INDEX.md)
