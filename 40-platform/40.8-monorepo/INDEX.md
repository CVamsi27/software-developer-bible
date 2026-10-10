# Monorepo — Index

> **Study time:** ≈ 1 h 7 m of reading (7 files, ~10 min average).
> **7 files** — Monorepo architecture from overview and Turborepo to Nx, workspace tooling deep-dive, versioning & publishing strategies, and curated interview questions.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why monorepo:** More teams are using monorepos (pnpm workspaces, Turborepo, Nx) for shared code, atomic refactors, and consistent tooling. Senior interviews at scale-focused companies (and at modern startups) test monorepo architecture: workspace setup, caching, affected commands, dependency graph.

---

## Topic Categories

| Category | Files | Why it matters |
| -------------------------------------------------- | ----: | ----------------------------------------------------- |
| [Foundations](#foundations) | 1 | Monorepo vs polyrepo, pnpm/Yarn/npm workspaces |
| [Build Orchestrators](#build-orchestrators) | 2 | Turborepo, Nx — the two main options |
| [Tools & Deep-Dive](#tools--deep-dive) | 1 | pnpm, Yarn Berry, Lerna, Rush, Bazel |
| [Versioning & Publishing](#versioning--publishing) | 1 | Changesets, fixed vs independent versions, provenance |
| [Interview Prep](#interview-prep) | 1 | 30+ Qs |

---

## Foundations

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Monorepo Overview](40.8.01-monorepo-overview.md) | Monorepo vs polyrepo, pnpm/Yarn/npm workspaces, workspace protocol, when to use | Important | Specialized | 13 min |

---

## Build Orchestrators

The two main build/cache systems for monorepos.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 02 | [Turborepo](40.8.02-turborepo.md) | Pipeline, content-hash caching, remote cache, filter, Docker layer caching | Vercel ecosystem, JS/TS monorepos | Important | Specialized | 12 min |
| 03 | [Nx](40.8.03-nx.md) | Generators, dependency graph, affected commands, module boundaries, Nx Cloud | Large JS/TS monorepos with strict boundaries | Important | Specialized | 12 min |

**Decision:**

```text
Monorepo tool?
├── Small/medium JS/TS, Vercel user → Turborepo
├── Large JS/TS with strict module boundaries → Nx
├── Polyglot (JS + Go + Python + ...) → Bazel / Nx
└── Just need workspaces, no build orchestration → pnpm/Yarn workspaces
```

---

## Tools & Deep-Dive

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Monorepo Tools Deep-Dive](40.8.04-monorepo-tools.md) | pnpm, Yarn Berry, Lerna, Rush, Bazel — when each wins | Important | Specialized | 7 min |

---

## Versioning & Publishing

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Versioning & Publishing Strategies](40.8.05-versioning-publishing-strategies.md) | Fixed vs independent versioning, changesets workflow (version PRs, publish, prereleases), private packages & scopes, npm provenance, lockstep decision matrix, breaking-change policy | Important | Specialized | 14 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [Interview Questions](40.8.06-interview-questions.md) | 30+ curated questions with answers | Important | Specialized | 7 min |

---

## Suggested Study Order

1. **Monorepo Overview** — must know
2. **Turborepo** or **Nx** — for the JD's stack
3. **Tools Deep-Dive** — for senior roles
4. **Versioning & Publishing** — "how do you release from a monorepo?"
5. **Revision** — explain the mechanisms from memory using [source-linked prompts](REVISION.md)
6. **Interview Questions** — final practice

---

## Common interview topics

- "Monorepo vs polyrepo — when to use which?"
- "How does Turborepo's content-hash caching work?"
- "What are affected commands in Nx?"
- "How do you share code between packages?"
- "How do you version and publish packages from a monorepo?"

---

## Cross-References

- [Build Tools](../40.5-build-tools/INDEX.md) — bundlers for monorepos
- [CI/CD](../40.3-ci-cd/INDEX.md) — CI in monorepos (affected-only builds)
- [Git Advanced](../40.6-git-advanced/INDEX.md) — branching for monorepos

---

## Navigation

[← Previous: Serverless & Edge](../40.7-serverless-edge/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Twelve-Factor App →](../40.9-twelve-factor/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) — my production hospital-management SaaS — IS the monorepo case study.

| Topic | Docita evidence |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| pnpm workspaces | `pnpm-workspace.yaml`: `apps/*` (api, app, internal, landing, worker) + `packages/*` (ui, auth, data-access, db, types, utils…) |
| Turborepo task graph | `turbo.json`: `build` depends on `^build` + `check-types` + `lint`; per-app env allowlists scope cache keys |
| Shared tooling | One `vitest.shared.config.ts`, one `packages/typescript-config`, shared eslint config |
| Dead-code control | Repo-wide `knip.json`; check the current release report for the actual gate result; configuration alone is not a passing run |
| Versioning/publishing | Not applicable — private app monorepo, no npm publishing |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
