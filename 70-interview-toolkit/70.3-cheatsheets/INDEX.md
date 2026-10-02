# Cheat Sheets — Index

> **Study time:** ≈ 43 min of reading (8 files, ~5 min average).
> **8 files** — Quick reference cheat sheets covering JavaScript, TypeScript, React/Next.js, Backend, System Design, Docker/K8s/CI-CD, and SQL/Data Modeling for rapid interview review.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why these references:** Follow a concrete operation, identify each component’s role, and check the contract or version that limits it. Use linked owner chapters for deeper derivations and complete implementations.

---

## Reading Passes

1. **Follow a value through execution and checking.** JavaScript explains bindings, calls, and scheduling; TypeScript explains which relationships can be checked before runtime and which need validation.
2. **Follow a user operation through application boundaries.** React/Next.js connects server rendering to browser interaction; the backend sheet follows identity, validation, and a committed operation. System design explains why distribution, caches, and delivery paths are added.
3. **Follow the artifact and stored rows.** The platform sheet traces build inputs through running workloads. SQL traces row meaning through joins, windows, access paths, and concurrency.
4. **Close the sheets and explain the contracts.** Finish with [section revision](REVISION.md), then return only to a source whose role or limit remains unclear.

## Topic Categories

Pick a sheet by the operation you need to explain; the passes above show how the categories connect.

| Category | Files | When to use |
| -------------------------- | ----: | --------------------------------------------------------------------------------- |
| **Language** | 2 | JavaScript (any JS role), TypeScript (when the JD names TS) — fundamentals rounds |
| **Framework & Full-Stack** | 2 | React/Next.js (frontend loops), Backend (Node/NestJS/DB/API loops) |
| **Architecture** | 1 | Architecture or trade-off discussion |
| **Platform / DevOps** | 1 | Docker/K8s/CI-CD questions; platform-heavy full-stack loops |
| **Data** | 1 | SQL/data-modeling deep-dives in backend loops |

---

## The 7 Cheat Sheets

| # | File | What it covers | When to use | Read time |
| --: | ------ | ---------------- | ------------- | ----------: |
| 01 | [JavaScript Cheat Sheet](70.3.01-javascript-cheat-sheet.md) | ES6+, promises, async/await, closures, event loop, prototype chain, this binding | Frontend interview, JS fundamentals round | 4 min |
| 02 | [TypeScript Cheat Sheet](70.3.02-typescript-cheat-sheet.md) | Types, generics, utility types, decorators, configuration, `satisfies`, `infer` | Frontend interview with TS focus | 5 min |
| 03 | [React & Next.js Cheat Sheet](70.3.03-react-nextjs-cheat-sheet.md) | Hooks, component patterns, App Router, server components, RSC, caching | React/Next.js interview | 10 min |
| 04 | [Backend Cheat Sheet](70.3.04-backend-cheat-sheet.md) | Node.js, NestJS, PostgreSQL, Prisma, REST APIs, Auth, Microservices | Backend interview | 5 min |
| 05 | [System Design Cheat Sheet](70.3.05-system-design-cheat-sheet.md) | CAP theorem, caching, database sharding, load balancing, CDN, message queues, rate limiting | System design interview | 4 min |
| 06 | [Docker, Kubernetes & CI/CD Cheat Sheet](70.3.06-docker-kubernetes-cicd-cheat-sheet.md) | Multi-stage Dockerfiles, kubectl debugging/rollouts, probes/PDB/resources, Helm, GitHub Actions caching, Argo CD sync | DevOps-adjacent and platform-heavy full-stack loops | 7 min |
| 07 | [SQL & Data Modeling Cheat Sheet](70.3.07-sql-data-modeling-cheat-sheet.md) | Join types, window functions, indexing rules, EXPLAIN reading, normal forms, audit/soft-delete/junction patterns, isolation levels | Data-heavy backend loops and system design DB deep-dives | 6 min |

---

## Use a Reference Without Losing the Model

Read the opening trace first, then use the role tables to find the relevant component. The short examples illustrate a specific contract rather than a full application. When the implementation needs more context, follow its canonical chapter link instead of copying several overlapping summaries.

## Cross-References

- [JavaScript](../../10-frontend/10.1-javascript/INDEX.md)
- [TypeScript](../../10-frontend/10.2-typescript/INDEX.md)
- [React](../../10-frontend/10.3-react/INDEX.md)
- [Backend](../../20-backend/INDEX.md)
- [System Design](../../30-architecture/30.2-system-design/INDEX.md)
- [Docker](../../40-platform/40.1-docker/INDEX.md)
- [Kubernetes](../../40-platform/40.2-kubernetes/INDEX.md)
- [CI/CD](../../40-platform/40.3-ci-cd/INDEX.md)

---

## Navigation

[← Previous: Coding Patterns](../70.2-coding-patterns/INDEX.md) · [ Back to Index](../INDEX.md) · [Next: Abroad Full-Stack Lane →](../../80-lanes-abroad-full-stack/INDEX.md)

---

## Docita Anchor

These references summarize mechanisms. Use a codebase artifact only after checking how it implements the stated contract. Docita itself lives at [github.com/CVamsi27/docita](https://github.com/CVamsi27/docita).

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
