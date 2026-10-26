# Monorepo — Index

> **Study time:** ≈ 44 min of reading (7 files, ~6 min average).
> **7 files** — Learn repository and package boundaries, compare task-graph tools, evaluate workspace/build systems, then follow a package change through publication and interview practice.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why study monorepos:** A shared repository can coordinate source changes and tooling, but it does not define package resolution, build order, access control, or deployment. Senior discussions probe how those boundaries interact and how you verify them.

---

## Topic Categories

| Category | Files | Why it matters |
| -------------------------------------------------- | ----: | --------------------------------------------------------------------------------------- |
| [Foundations](#foundations) | 1 | Repository boundaries, package/task/release graphs, workspace linking, consumer exports |
| [Build Orchestrators](#build-orchestrators) | 2 | Compare task graphs, affected selection, cache contracts, generators, and boundaries |
| [Tools & Deep-Dive](#tools--deep-dive) | 1 | pnpm, Yarn Berry, Lerna, Rush, Bazel |
| [Versioning & Publishing](#versioning--publishing) | 1 | Changesets, fixed vs independent versions, provenance |
| [Interview Prep](#interview-prep) | 1 | 30+ interview prompts |

---

## Foundations

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Monorepo Overview](40.8.01-monorepo-overview.md) | Monorepo vs polyrepo, pnpm/Yarn/npm workspaces, workspace protocol, when to use | Important | Specialized | 7 min |

---

## Build Orchestrators

Two task-graph approaches; choose by the contracts your workspace needs.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 02 | [Turborepo](40.8.02-turborepo.md) | Task dependencies, input/output hashes, filtering, affected selection, remote cache | A workspace that benefits from a compact task graph and cache model | Important | Specialized | 8 min |
| 03 | [Nx](40.8.03-nx.md) | Project discovery, inferred targets, task ordering, affected selection, cache correctness, generators, module boundaries | Workspaces that benefit from plugins, architectural constraints, and richer project/task graphs | Important | Specialized | 7 min |

**Decision:**

```text
Monorepo tool?
├── Need workspace linking and scripts only → package-manager workspaces
├── Need a compact task graph and output cache → evaluate Turborepo
├── Need inferred targets, generators, or enforceable project boundaries → evaluate Nx
└── Need explicitly declared actions across toolchains → evaluate Bazel and maintained rules
```

---

## Tools & Deep-Dive

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 04 | [Monorepo Tools Deep-Dive](40.8.04-monorepo-tools.md) | Workspace resolution, task runners, package-release tooling, declared multi-language builds | Important | Specialized | 7 min |

---

## Versioning & Publishing

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Versioning & Publishing Strategies](40.8.05-versioning-publishing-strategies.md) | Consumer-driven version policy, Changesets, workspace-to-registry artifacts, prereleases, OIDC publishing, provenance, release verification | Important | Specialized | 7 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [Interview Questions](40.8.06-interview-questions.md) | 30+ curated questions with answers | Important | Specialized | 6 min |

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

Candidate source locations in [Docita](https://github.com/CVamsi27/docita), a healthcare application built with NestJS, React and TypeScript. Inspect the checked-out revision and relevant tests before using a path as implementation evidence; source configuration alone does not establish deployed behavior.

| Topic | Docita evidence |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| pnpm workspaces | `pnpm-workspace.yaml`: `apps/*` (api, app, internal, landing, worker) + `packages/*` (ui, auth, data-access, db, types, utils…) |
| Turborepo task graph | `turbo.json`: `build` depends on `^build` + `check-types` + `lint`; per-app env allowlists scope cache keys |
| Shared tooling | One `vitest.shared.config.ts`, one `packages/typescript-config`, shared eslint config |
| Dead-code control | Repo-wide `knip.json`; check the current release report for the actual gate result; configuration alone is not a passing run |
| Versioning/publishing | Not applicable — private app monorepo, no npm publishing |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
