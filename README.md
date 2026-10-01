# Senior Full Stack Interview Bible

> **A lane-first, stack-deep reference for senior full-stack engineers (5+ YoE)** prepping for product-based companies, FAANG/Big Tech, and EU mid-stage startups. Pick your lane, drill the stacks — or [search all 560 chapters](search.html) by title, section, tag and read time.

[![Lanes](https://img.shields.io/badge/lanes-2-blue)](lanes/INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-7-green)](INDEX.md)
[![Files](https://img.shields.io/badge/files-869-orange)](INDEX.md)
[![Search](https://img.shields.io/badge/search-try%20it-blueviolet)](search.html)
[![API](https://img.shields.io/badge/corpus%20API-json-informational)](api/index.json)
[![GoF Coverage](https://img.shields.io/badge/design%20patterns-23%2F23-success)](30-architecture/30.1-design-patterns/INDEX.md)
[![Last Updated](https://img.shields.io/badge/last%20updated-September%202026-purple)](#)

---

## Pick Your Lane

The bible is split into **2 terminal interview lanes** that draw from the **same 7 study stacks** — plus a **strategy folder** ([00-strategy/](00-strategy/INDEX.md)) everyone starts with before entering a lane. The stacks are the technical material both lanes share; each lane is the prep plan and behavioral overlay for a specific job-market.

**Start with [00-strategy/](00-strategy/INDEX.md)** — resume, STAR, communication — it applies to every interview regardless of lane. Then pick a lane:

| Lane | Folder | Audience | Bar | Time |
| --------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------ |
| **Indian SDE / FAANG** | [81-lanes-indian-sde-faang/](81-lanes-indian-sde-faang/INDEX.md) | Microsoft, Google, Amazon, Meta, Apple, in-country India | LeetCode medium-to-hard, 5-6 rounds | 8-12 weeks @ 4-6 hrs/day |
| **Abroad Full-Stack** | [80-lanes-abroad-full-stack/](80-lanes-abroad-full-stack/INDEX.md) | EU mid-stage startups (n8n, SumUp, Scalable, sennder, THRYVE, Peter Park) + remote-first US | Take-home + system design, 3-4 rounds | 4-6 weeks @ 2-3 hrs/day |

**Quick heuristic:** If the phone screen has a LeetCode medium-to-hard → Indian SDE / FAANG. If the company is mid-stage and uses take-homes → Abroad Full-Stack. Many EU Big Tech (Booking, Spotify) run FAANG-style loops → use both.

 Full decision matrix: [80-lanes-abroad-full-stack/INDEX.md → Lane Decision](80-lanes-abroad-full-stack/INDEX.md#lane-decision--is-this-the-right-lane-for-you)

---

## The 7 Study Stacks

Both lanes pull from the **same 7 study stacks**. Pick a topic, drill the stack. Lanes never reference each other — only the stacks.

| Stack | Folder | What's in it | Files |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----: |
| **Frontend** | [10-frontend/](10-frontend/INDEX.md) | JavaScript, TypeScript, React, Next.js, Forms, Animation, HTML/CSS/PWA, Mobile | 122 |
| **Backend** | [20-backend/](20-backend/INDEX.md) | Node.js, NestJS, REST, GraphQL, Database, **Auth track**, Security, Microservices, **AI Engineering**, Java | 147 |
| **Architecture** | [30-architecture/](30-architecture/INDEX.md) | System design theory + 31 case studies, Design Patterns (categorized: Foundations/Creational/Structural/Behavioral/Architectural — all 23 GoF + modern) | 109 |
| **Platform** | [40-platform/](40-platform/INDEX.md) | Docker, K8s, CI/CD, Observability, Build Tools, Git, Serverless, Monorepo, 12-Factor | 95 |
| **Quality** | [50-quality/](50-quality/INDEX.md) | Testing (Jest/RTL/Playwright/Vitest), Accessibility, Performance | 38 |
| **Real-Time** | [60-realtime/](60-realtime/INDEX.md) | WebSockets, SSE, Socket.IO, scaling patterns | 11 |
| **Interview Toolkit** | [70-interview-toolkit/](70-interview-toolkit/INDEX.md) | Behavioral, Coding Patterns (18 patterns), Cheat Sheets | 34 |

 Full breakdown with file counts per topic: [INDEX.md → The 7 Study Stacks](INDEX.md#the-7-study-stacks-numbered-for-study-order)

---

## Navigation

| If you want to… | Go to |
| --------------------------------------- | ------------------------------------------------------------------ |
| **Follow the study path** | [ROADMAP.md](ROADMAP.md) — phases, checkpoints, weekly schedule |
| See all files in one place | [INDEX.md](INDEX.md) |
| Start with universal interview prep | [00-strategy/](00-strategy/INDEX.md) |
| Prep for FAANG / Indian SDE roles | [81-lanes-indian-sde-faang/](81-lanes-indian-sde-faang/INDEX.md) |
| Prep for EU mid-stage / remote-first US | [80-lanes-abroad-full-stack/](80-lanes-abroad-full-stack/INDEX.md) |
| Learn how to contribute | [contributing.md](contributing.md) |

---

## Chapter Template

Every content file follows a consistent structure:

```text
# Topic

## TL;DR ← 3-5 bullet summary at the top
## Definition ← What it is
## Why Do We Need It? ← When to use it
## How It Works ← Internals with diagrams
## Code Examples ← TypeScript/SQL/Docker examples
## Real-World Use Cases ← Production patterns
## Common Mistakes ← Anti-patterns to avoid
## Best Practices ← Do this, not that
## Performance Considerations ← Latency, memory, scaling
## Summary ← Key takeaways
## Cheat Sheet ← Quick-reference box
## See Also ← Cross-references to related files
## References & Learn More ← External links
```

Interview questions live in dedicated `*-interview-questions.md` files (40 across all stacks).

---

## How to Use

| Goal | Approach |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **New to a topic** | Start with the definition and "Why" sections |
| **Preparing for an interview** | Follow your lane's 4-week or 8-week prep plan; the lane tells you which stack files to read in what order |
| **Quick review** | Use the Cheat Sheet at the bottom of each chapter, or the [70-interview-toolkit/70.3-cheatsheets/](70-interview-toolkit/70.3-cheatsheets/INDEX.md) stack |
| **Deep dive** | Read through internal working and code examples |
| **Cross-reference** | Each stack folder has an `INDEX.md` listing all files with file counts |
| **Trust the numbers** | 20 verification gates re-check every count, link and claim on each push — see the [Verification Gates](docs/verification-gates.md), the [Scripts Map](docs/scripts-map.md), and the [Corpus Health Report](docs/2026-09-19-corpus-health-report.md) |
| **Publishing the site** | The Jekyll build + Cloudflare Pages deploy pipeline: what runs automatically, the one-time setup, and how the private lanes stay unpublished — see [Deployment](docs/deployment.md) |

## Private Study Host

This repository publishes to `study.buildora.work`,
but the production host is not a public mirror. Cloudflare Pages Functions
protect every static route with Supabase Google OAuth; only the exact
`cvamsik99@gmail.com` account is admitted. Other Google accounts are softly
returned to `personal.buildora.work`. The access
cookie is `HttpOnly`, no token is persisted in browser storage, and the
configuration lives in Cloudflare Pages environment variables rather than in
the repository. See [Deployment](docs/deployment.md) for the private entry-flow verification steps.

---

## Quick Lane Summary

### Indian SDE / FAANG (22 files in lane)

DSA-heavy. The bar is **1-2 mediums in 30-45 min, plus 1 system design, plus 1-2 behavioral, plus a Bar Raiser (Amazon) or values round**. 5-6 rounds, 8-12 weeks. US FAANG total comp: USD 150-400K+ (senior, 2026 est.). Indian in-country: INR 30-120 L (SDE-2 to SDE-3).

→ [Indian SDE / FAANG lane →](81-lanes-indian-sde-faang/INDEX.md)

### Abroad Full-Stack (36 files in lane)

Take-home heavy. The bar is **a 5-6 hour take-home, 1-2 mediums in 30 min, 1 system design at 45 min, 1 behavioral round**. 3-4 rounds, 4-6 weeks. EU Tier 1 comp: EUR 75-100K base + 0.05-0.5% equity (canonical: [80.05](80-lanes-abroad-full-stack/80.05-comp-eu-benchmarking.md)). Family-driven geography (NL 30% ruling, EU Blue Card, schools).

→ [Abroad Full-Stack lane →](80-lanes-abroad-full-stack/INDEX.md)

---

*Last updated: September 2026 — 869 files · 362K lines · every topic in one place, 0 broken links. Design Patterns organized by GoF category — all 23 GoF patterns + modern architectural patterns, with detailed INDEX per category.*
