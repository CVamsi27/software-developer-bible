# Monorepo — Index

> **5 files** — Monorepo architecture from overview and Turborepo to Nx, workspace tooling deep-dive, and curated interview questions.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why monorepo:** More teams are using monorepos (pnpm workspaces, Turborepo, Nx) for shared code, atomic refactors, and consistent tooling. Senior interviews at scale-focused companies (and at modern startups) test monorepo architecture: workspace setup, caching, affected commands, dependency graph.

---

## 🗂️ Topic Categories

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Foundations](#-foundations) | 1 | Monorepo vs polyrepo, pnpm/Yarn/npm workspaces |
| [Build Orchestrators](#-build-orchestrators) | 2 | Turborepo, Nx — the two main options |
| [Tools & Deep-Dive](#-tools--deep-dive) | 1 | pnpm, Yarn Berry, Lerna, Rush, Bazel |
| [Interview Prep](#-interview-prep) | 1 | 30+ Qs |

---

## 🧱 Foundations

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Monorepo Overview](40.8.01-monorepo-overview.md) | Monorepo vs polyrepo, pnpm/Yarn/npm workspaces, workspace protocol, when to use | 30 min |

---

## 🏗️ Build Orchestrators

The two main build/cache systems for monorepos.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 02 | [Turborepo](40.8.02-turborepo.md) | Pipeline, content-hash caching, remote cache, filter, Docker layer caching | Vercel ecosystem, JS/TS monorepos | 30 min |
| 03 | [Nx](40.8.03-nx.md) | Generators, dependency graph, affected commands, module boundaries, Nx Cloud | Large JS/TS monorepos with strict boundaries | 30 min |

**Decision:**

```text
Monorepo tool?
├── Small/medium JS/TS, Vercel user → Turborepo
├── Large JS/TS with strict module boundaries → Nx
├── Polyglot (JS + Go + Python + ...) → Bazel / Nx
└── Just need workspaces, no build orchestration → pnpm/Yarn workspaces
```

---

## 🔧 Tools & Deep-Dive

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 05 | [Monorepo Tools Deep-Dive](40.8.05-monorepo-tools.md) | pnpm, Yarn Berry, Lerna, Rush, Bazel — when each wins | 25 min |

---

## 🎤 Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 04 | [Interview Questions](40.8.04-interview-questions.md) | 30+ curated questions with answers | 2 hrs |

---

## 🛣️ Suggested Study Order

1. **Monorepo Overview** — must know
2. **Turborepo** or **Nx** — for the JD's stack
3. **Tools Deep-Dive** — for senior roles
4. **Interview Questions** — final review

---

## 🎯 Common interview topics

- "Monorepo vs polyrepo — when to use which?"
- "How does Turborepo's content-hash caching work?"
- "What are affected commands in Nx?"
- "How do you share code between packages?"
- "How do you version and publish packages from a monorepo?"

---

## 🔗 Cross-References

- [Build Tools](../40.5-build-tools/INDEX.md) — bundlers for monorepos
- [CI/CD](../40.3-ci-cd/INDEX.md) — CI in monorepos (affected-only builds)
- [Git Advanced](../40.6-git-advanced/INDEX.md) — branching for monorepos

---

## Navigation

[← Previous: Serverless & Edge](../40.7-serverless-edge/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Twelve-Factor App →](../40.9-twelve-factor/INDEX.md)
