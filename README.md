---
layout: post
title: Senior Full Stack Interview Bible
permalink: /README.html
---

# Senior Full Stack Interview Bible

> **A lane-first, stack-deep reference for senior full-stack engineers (5+ YoE)** prepping for product-based companies, FAANG/Big Tech, and EU mid-stage startups. Pick your lane, drill the stacks — or [search all 671 chapters](search.html) by title, section, tag and read time.

[![Lanes](https://img.shields.io/badge/lanes-2-blue)](lanes/INDEX.md)
[![Stacks](https://img.shields.io/badge/stacks-7-green)](INDEX.md)
[![Files](https://img.shields.io/badge/files-1014-orange)](INDEX.md)
[![Search](https://img.shields.io/badge/search-try%20it-blueviolet)](search.html)
[![API](https://img.shields.io/badge/corpus%20API-json-informational)](api/index.json)
[![GoF Coverage](https://img.shields.io/badge/design%20patterns-23%2F23-success)](30-architecture/30.1-design-patterns/INDEX.md)
[![Last Updated](https://img.shields.io/badge/last%20updated-October%202026-purple)](#)

---

## Choose work from the confirmed interview format

Start with [interview strategy](00-strategy/INDEX.md) to prepare clear communication and supported experience claims. Then choose the lane matching the assessed work:

| Preparation need | Start here |
| ------------------------------------------------------------- | ------------------------------------------------------------- |
| Algorithmic coding and broader SDE preparation | [SDE / FAANG lane](81-lanes-indian-sde-faang/INDEX.md) |
| Practical full-stack work, take-homes and relocation research | [Abroad full-stack lane](80-lanes-abroad-full-stack/INDEX.md) |

A vacancy may need both. Confirm its format, language, allowed tools and location requirements; a country or employer label does not establish a universal hiring loop, preparation period or compensation band.

See the [lane decision](80-lanes-abroad-full-stack/INDEX.md#lane-decision--is-this-the-right-lane-for-you) for how the paths fit together.

---

## The 7 Study Stacks

Both lanes use the same technical chapters. Follow a stack’s reading stages to learn a mechanism, use its category revision afterward, and select interview-bank prompts when practicing that format.

| Stack | Folder | What's in it | Files |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----: |
| **Frontend** | [10-frontend/](10-frontend/INDEX.md) | JavaScript, TypeScript, React, Next.js, Forms, Animation, HTML/CSS/PWA, Mobile | 145 |
| **Backend** | [20-backend/](20-backend/INDEX.md) | Node.js, NestJS, REST, GraphQL, Database, **Auth track**, Security, Microservices, **AI Engineering**, Java | 179 |
| **Architecture** | [30-architecture/](30-architecture/INDEX.md) | System design theory + 31 case studies, Design Patterns (categorized: Foundations/Creational/Structural/Behavioral/Architectural — all 23 GoF + modern) | 121 |
| **Platform** | [40-platform/](40-platform/INDEX.md) | Docker, K8s, CI/CD, Observability, Build Tools, Git, Serverless, Monorepo, 12-Factor | 118 |
| **Quality** | [50-quality/](50-quality/INDEX.md) | Testing (Jest/RTL/Playwright/Vitest), Accessibility, Performance | 48 |
| **Real-Time** | [60-realtime/](60-realtime/INDEX.md) | WebSockets, SSE, Socket.IO, scaling patterns | 14 |
| **Interview Toolkit** | [70-interview-toolkit/](70-interview-toolkit/INDEX.md) | Behavioral, Coding Patterns (18 patterns), Cheat Sheets | 41 |

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

## How a chapter should teach

A chapter introduces the concept once, explains the constraint behind it, then traces a focused example before comparing decisions and failure boundaries. Headings state the relationship or problem being explained. A new component is connected to the whole before its variants are listed.

Concept chapters start with Definition and First Principles, then use the sections that advance understanding. They end with one Summary, See Also and References. TL;DR and duplicated in-chapter cheat sheets are retired.

Questions and answers live in one separate `REVISION.md` per category, linked as the final learning stage in its index. Dedicated interview banks provide longer drills. The [contribution guide](contributing.md) defines the full contract.

## Use the resource for the task at hand

| Task | Path |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Learn a new mechanism | Follow the category’s staged `INDEX.md`, then trace its chapter examples |
| Check recall after a category | Use its separate `REVISION.md` before reopening the sources |
| Repair an interview gap | Choose the relevant canonical chapter, then test a changed case |
| Find a topic quickly | [Search](search.html), [master index](INDEX.md) or [reference guides](70-interview-toolkit/70.3-cheatsheets/INDEX.md) |
| Plan preparation | [Roadmap](ROADMAP.md) and the lane matching your confirmed format |
| Check repository validation | [Verification gates](docs/verification-gates.md) and [scripts map](docs/scripts-map.md) |
| Understand publishing and access | [Deployment](docs/deployment.md) |

Use the [two-axis topic importance guide](docs/topic-importance.md) to choose what to study: prioritize core full-stack engineering and system design, keep HTML/CSS basics, and defer animation specialization.

The [personal-site sync contract](docs/planner-site-sync.md) explains how to refresh the roadmap snapshot and preserve planner evidence when this corpus changes.

Automated gates check defined structural, link, metadata and regression rules. Passing them does not prove every technical claim or teaching explanation correct. The [corpus readability review and per-page inventory](docs/2026-10-03-readability-review.md) distinguish automated screening, close reading and remaining rewrites. Dated [health reports](docs/2026-09-19-corpus-health-report.md) describe the snapshot they measured; rerun the gates for current evidence.

The latest [reading and senior interview quality review](docs/2026-10-07-reading-quality-report.md) records formal definition coverage, reader fixes, resume validation and the limits of the technical review.

## Private study host and personal records

The study host uses the access controls described in [deployment](docs/deployment.md). Account configuration belongs in deployment environment variables. Personal CVs, contacts, application records and relocation details are canonical under [personal/](80-lanes-abroad-full-stack/personal/README.md); keep them out of general teaching pages.

---

*Repository counts and reading-time metadata are generated from disk. Run the required verification gates before committing or pushing.*
