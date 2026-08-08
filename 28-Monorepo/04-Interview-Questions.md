---
section: Monorepo
category: Reference
tags: [interview-questions, practice]
---

# Monorepo Interview Questions

> 30+ curated questions on monorepo architecture, from fundamentals to FAANG-style system design.

## Definition

This guide covers the questions a senior full-stack engineer should be able to answer about monorepo structure, tooling (Turborepo, Nx, pnpm), caching, affected-based CI, module boundaries, and migration strategies. Grouped by difficulty.

## Why It Matters (TL;DR)

- **Technical interviews** — monorepo questions appear at every level above mid
- **Architectural discussions** — interviewers test trade-off reasoning (mono vs poly)
- **CI/CD performance** — affected-based builds are a senior topic
- **Tooling knowledge** — Turborepo, Nx, pnpm, Yarn, Lerna

## Answer Framework

```text
ANSWER STRUCTURE:
  1. Definition        (1-2 sentences — what it is)
  2. Benefits          (atomic refactors, shared types, unified CI)
  3. Challenges        (build performance, tooling, ownership)
  4. Implementation    (pnpm + Turborepo / Nx + changesets + CODEOWNERS)
  5. Trade-offs        (vs polyrepo, repo size, lock-in)
```

## Beginner

**Q1: What is a monorepo?**

A: A single version-controlled repository that contains the source code for multiple logically distinct projects (apps, libraries, services). It relies on package-manager workspaces (pnpm, Yarn, npm) and a task-graph tool (Turborepo, Nx, Lerna) to coordinate builds, tests, and dependencies.

**Q2: What are the benefits of a monorepo?**

A: (1) Code sharing — packages are first-class, no need to publish to npm. (2) Atomic changes — one commit crosses all packages. (3) Consistent dependencies — single source of truth for versions. (4) Easier refactoring — find-and-replace all in one go. (5) Unified CI — single pipeline with full visibility.

**Q3: What is the difference between monorepo and polyrepo?**

A: Monorepo stores all code in one repository with shared dependencies and a single task graph. Polyrepo stores each project in its own repository with independent dependencies and CI. The trade-off: monorepo is better for cross-cutting changes and shared types; polyrepo gives stronger team isolation and smaller, faster clones.

**Q4: What are package-manager workspaces?**

A: A feature of pnpm, Yarn, and npm that lets a single root `package.json` reference multiple sub-packages by glob (e.g., `packages/*`). The package manager hoists compatible dependencies to the root `node_modules` and links workspace packages by the `workspace:*` protocol. The result: a single install for the whole repo.

**Q5: What is the `workspace:*` protocol?**

A: A package.json dependency value (e.g., `"@myorg/ui": "workspace:*"`) that means "use the local workspace version of this package, not a published one." Lets you develop across packages without publishing. In Yarn Berry, the syntax is `*` or a specific workspace constraint.

**Q6: What is hoisting in monorepos?**

A: The package manager deduplicates compatible versions of dependencies and installs them once at the root `node_modules` rather than per-package. pnpm uses a content-addressable store with symlinks (faster installs, stricter isolation by default); npm and Yarn hoist by default. pnpm's strict mode prevents phantom dependencies — packages can only import what they explicitly declare.

## Intermediate

**Q7: How do you structure a monorepo?**

A: A common layout:
- `apps/` — deployable applications (web, api, mobile, worker)
- `packages/` or `libs/` — shared libraries (ui, utils, data, config)
- `tools/` — build tooling, codegen, eslint/tsconfig presets
- `.changeset/` — version bumps and changelogs
- `CODEOWNERS` — per-package ownership for PRs
Naming: scoped `@myorg/<name>` for all packages.

**Q8: What are the main challenges of monorepos?**

A: (1) Build performance — large monorepos are slow without caching. (2) Tooling complexity — must invest in Turborepo/Nx. (3) Team coordination — merge conflicts at busy boundaries. (4) CI/CD complexity — naive full builds don't scale. (5) Access control — must use CODEOWNERS, not repo permissions. (6) Learning curve for new engineers.

**Q9: How do you handle versioning in a monorepo?**

A: Three main approaches: (1) **Independent versioning** — each package has its own version, bumped via Changesets or Release Please based on commit messages. (2) **Coordinated versioning** — all packages share a version, simpler but causes unnecessary bumps. (3) **Lockstep** — only when packages are tightly coupled. Changesets is the 2026 default: write a changeset in your PR, the release bot versions and publishes on merge.

**Q10: What is the difference between Turborepo and Nx?**

A:
- **Turborepo**: lightweight task runner focused on caching and parallelization. Config in `turbo.json`. Easier learning curve, framework-agnostic. Good for simple to medium monorepos.
- **Nx**: full build platform with generators, dependency graph, module-boundary enforcement, and a large plugin ecosystem. Config in `nx.json` + per-project `project.json`. Steeper learning curve but better for large organizations with strict architecture.

**Q11: How do you manage dependencies in a monorepo?**

A: (1) Use `workspace:*` for local packages. (2) Pin major versions in root `package.json`; let the lockfile pin exact versions. (3) Use pnpm's `overrides` or Yarn's `resolutions` to force a single version of transitive deps. (4) Add `dependency-cruiser` to detect circular and unwanted imports. (5) Renovate / Dependabot for automated PRs.

**Q12: What is the difference between `pnpm`, `npm`, and `Yarn` workspaces?**

A: All three support workspaces but differ in implementation:
- **pnpm**: content-addressable store, symlinked `node_modules` (fast, strict, no phantom deps)
- **Yarn Berry (v4)**: Plug'n'Play (PnP) by default; zero-installs; hermetic
- **npm**: traditional `node_modules` tree; workspaces since npm 7; least strict

In 2026, pnpm is the default for new monorepos due to speed, strict mode, and disk efficiency.

## Senior

**Q13: How do you optimize build performance in a monorepo?**

A: (1) Content-hash caching (Turborepo / Nx) — local cache + remote cache. (2) Affected-based builds — only build projects that depend on changed files (`nx affected` / `turbo run --filter=...<base>`). (3) Parallel execution across packages and across CI agents (Nx Cloud's distributed task execution). (4) Incremental builds — TypeScript project references, Vite HMR. (5) Docker layer caching with Turborepo.

**Q14: How do you handle circular dependencies?**

A: (1) Detect early with `dependency-cruiser` or Nx's graph. (2) Refactor: extract the shared types/utilities into a new package that both can import. (3) Use dependency injection to invert the direction. (4) Re-examine the boundary — circular deps usually mean the two modules should be merged, or the shared concern should be a third module. (5) Add CI to fail the build on new circular imports.

**Q15: What is the strangler fig pattern in monorepo migration?**

A: Incrementally migrating from polyrepo to monorepo without a big-bang: (1) Create the monorepo skeleton (apps/, packages/). (2) Move one package at a time — clone it, transform it into a workspace package, point dependents at the new path. (3) Keep the old repo as the source of truth until consumers are migrated. (4) Deprecate the old repo once nothing imports it. (5) Use a transitional npm alias (`"@myorg/ui": "npm:@myorg/ui@npm:1.2.3"`) for cross-boundary compatibility.

**Q16: How do you enforce architectural boundaries in a monorepo?**

A: (1) Nx tags + ESLint `depConstraints` (e.g., `scope:ui` can only depend on `scope:utils`). (2) Directory structure + import-restriction linting (e.g., eslint-plugin-import's `no-restricted-paths`). (3) CODEOWNERS — per-directory owners. (4) Architecture Decision Records (ADRs). (5) Automated dependency-graph review in PRs.

**Q17: How do you handle code ownership in a monorepo?**

A: (1) `CODEOWNERS` file at the repo root (GitHub / GitLab syntax). (2) One team per major path (e.g., `/apps/web` → Web team, `/packages/ui` → Design System team). (3) Cross-cutting packages get a shared owner or rotating reviewer. (4) Auto-assign reviewers from CODEOWNERS on PR. (5) Pair with tags in Nx for an additional ownership layer.

**Q18: How do you handle database migrations in a monorepo?**

A: (1) Single migration directory at the repo root (e.g., `packages/db/migrations/`). (2) Version-controlled schema (Prisma, Drizzle, Atlas). (3) Migrations run as a CI/CD step before deployment. (4) Backward-compatible changes only — add column, deploy, write data, deploy, drop column. (5) Each app references the shared schema package; one source of truth for types.

**Q19: How do you test in a monorepo?**

A: Three layers: (1) **Unit** — per-package, run on `affected` change. (2) **Integration** — across packages, in a `tests/integration/` directory or per-feature. (3) **E2E** — Playwright/Cypress in `apps/e2e/`, scoped to the affected app. Run all three on PR but only affected on `nx affected` / `turbo run`. Share test utilities in `packages/test-utils/`.

**Q20: How do you migrate from Lerna to Turborepo or Nx?**

A: (1) Audit current Lerna setup — what packages, scripts, versions, publishing. (2) Initialize Turborepo/Nx alongside Lerna (don't delete Lerna yet). (3) Convert Lerna scripts to `turbo.json` tasks or `project.json` targets. (4) Move Lerna publishing to Changesets. (5) Remove Lerna when all tasks are migrated and tests pass. (6) Update CI to use the new runner. Lerna is largely in maintenance mode in 2026 — most teams migrate to Changesets + Turborepo/Nx.

**Q21: How do you handle monorepo with multiple programming languages?**

A: (1) Separate package managers per language (pnpm for JS, Cargo for Rust, Poetry for Python). (2) Use Bazel or Nx with polyglot plugins for a unified task graph. (3) Shared interfaces via gRPC, Protobuf, or OpenAPI. (4) Per-language test runners; unified CI via Buildkite / GitHub Actions matrix. (5) Common release tooling (e.g., Release Please for all languages).

**Q22: How do you handle monorepo security?**

A: (1) Dependency scanning — `pnpm audit`, `npm audit`, Snyk, Dependabot. (2) Secret scanning — git-secrets, TruffleHog, GitHub secret scanning. (3) CODEOWNERS + signed commits. (4) Branch protection rules. (5) Limit who can publish to the registry (release bot with scoped tokens). (6) SBOM generation for compliance.

## FAANG-style

**Q23: Design a monorepo architecture for a 200-engineer organization.**

A:
- **Layout**: `apps/{web, mobile, api, worker, admin}`, `packages/{ui, utils, data, config}`, `tools/{eslint, tsconfig, ci}`
- **Tooling**: pnpm + Nx (or Turborepo); Nx for generators and module-boundary enforcement
- **CI/CD**: Nx affected on PRs, distributed execution via Nx Cloud, separate `main` / `staging` / `prod` deploy jobs per app
- **Code ownership**: CODEOWNERS per `apps/*` and `packages/*`; ADR for cross-cutting decisions
- **Versioning**: Changesets for internal-only packages; npm publish for OSS-extractable libs
- **Observability**: Turborepo cache hit rate, Nx graph complexity, CI duration, build failure rate
- **Caching**: Remote cache shared across team; Docker layer cache for production images

**Q24: How would you migrate from polyrepo to monorepo?**

A: Phased:
1. **Foundation** — create empty monorepo, set up pnpm workspaces, basic CI
2. **Shared packages first** — `@myorg/ui`, `@myorg/utils`, `@myorg/config` (highest value, lowest risk)
3. **Internal apps** — move one app at a time, keep its git history via `git subtree` or `git filter-repo`
4. **Dual-publishing window** — packages published to internal registry, consumers migrate gradually
5. **CI unification** — single pipeline with affected-based builds
6. **Decommission** — archive old repos, redirect pointers, sunset
Use a 3-6 month timeline with weekly checkpoints.

**Q25: Explain monorepo at scale (Google, Meta, Microsoft).**

A: Google has one monorepo with 2B+ lines of code, 50K+ commits/day, and uses Piper + CitC for source control. Bazel orchestrates builds with aggressive caching. Key techniques: (1) Trunk-based development, (2) pre-commit / post-commit automated testing (TAP), (3) team-based file ownership with global visibility, (4) cross-language build system (Bazel supports 20+ languages), (5) virtual file system for IDE speed (CitC). Meta uses similar patterns with Hack and Buck. Microsoft moved to monorepo via One Engineering System. Common denominators: strong tooling, automated enforcement, code ownership, and a dedicated platform team.

**Q26: Design a CI/CD pipeline for a monorepo.**

A:
- **Trigger**: PR → GitHub Actions
- **Step 1 — Detect changes**: `nx affected --target=test,lint,build --base=origin/main` (or `turbo run ... --filter=...<main>`)
- **Step 2 — Cache restore**: remote cache (Turbo/Nx) restored via `TURBO_TOKEN` / Nx Cloud token
- **Step 3 — Lint + typecheck** for affected
- **Step 4 — Unit + integration tests** for affected, with shard parallelism
- **Step 5 — Build** for affected, push Docker images to registry with `cache-from`
- **Step 6 — E2E** for affected apps (Playwright)
- **Step 7 — Preview deploy** (Vercel) for web changes
- **Step 8 — Notify** with PR comment (affected list, build artifacts)
- **Main branch**: full pipeline + version bump via Changesets + publish to registry + deploy

**Q27: How do you handle a monorepo with conflicting TypeScript versions?**

A: (1) Single `tsconfig.base.json` with one `typescript` version installed at root. (2) All packages `extend` the base config. (3) Per-package overrides are allowed but discouraged. (4) When a new TS version lands, bump it everywhere in one PR; CI catches any breakage. (5) `tsc --build` with project references for incremental builds. (6) For unavoidable version conflicts (e.g., a legacy lib), use `peerDependencies` and TypeScript's `paths` to redirect.

## Follow-ups

**Q28: What is the impact of monorepo on developer experience?**

A: Pros: single clone, full codebase search (ripgrep / IDE), atomic refactors, no version drift. Cons: longer initial clone, larger IDE index, learning curve for new tooling, occasional merge conflicts at busy files.

**Q29: What are the alternatives to a monorepo?**

A: (1) **Polyrepo** — independent repos, npm publishing for shared code. (2) **Multi-repo with versioned SDK** — one team owns the SDK, others consume via npm. (3) **Git submodules** — sparse checkouts of shared libs. (4) **Hybrid** — monorepo for internal, polyrepo for customer-facing services. (5) **Versioned monorepo** — like Google's, where external dependencies are still packaged.

**Q30: How do you handle monorepo secrets?**

A: (1) Never commit — use `.env.local` (gitignored), copy from `.env.example`. (2) CI secrets in GitHub Actions / GitLab CI / Buildkite. (3) For runtime: AWS Secrets Manager, HashiCorp Vault, Doppler. (4) Reference via environment variables in code, never hardcode. (5) Rotate secrets regularly; scan for accidental commits.

**Q31: How do you measure monorepo success?**

A: Track: (1) Build duration (p50, p95) — should decrease after caching lands. (2) Cache hit rate — target >80%. (3) Time to first PR feedback — should drop. (4) Cross-package refactor success rate. (5) Mean time to onboard a new engineer. (6) Number of `package.json` conflicts per week. (7) Onboarding satisfaction scores.

## Key Concepts to Master

| Concept | Key Points |
|---------|------------|
| Workspaces | pnpm/Yarn/npm — single install, hoisted deps, `workspace:*` |
| Caching | Local + remote, content-hash based, shared across team |
| Affected | Only run tasks for changed projects (Nx) / `filter=...<base>` (Turborepo) |
| Generators | Code scaffolding (Nx first-class, Turborepo none) |
| Dependency Graph | Visualize with `nx graph`; enforce with `depConstraints` |
| Versioning | Changesets for atomic multi-package releases |
| CI/CD | Affected-based pipelines + remote cache |
| Module Boundaries | Tags + ESLint prevent cross-module imports |

## Common Follow-up Questions

- "How would you implement this in production?"
- "What are the cost / time implications of migration?"
- "How do you handle failures (cache miss storm, broken build)?"
- "What are the alternatives — why not polyrepo?"
- "How do you test this?"
- "How would you convince leadership to adopt a monorepo?"

## Summary

- Monorepo = single repo, multiple packages, coordinated builds
- pnpm + Turborepo (or Nx) is the 2026 default
- Caching + affected-based CI are the two biggest wins
- Module boundary enforcement prevents coupling
- Migration from polyrepo is gradual — strangler fig works

---

## Cheat Sheet

```text
MONOREPO INTERVIEW CHEAT SHEET
═══════════════════════════════════════════════════════════════

ANSWER FRAMEWORK:
  1. Definition
  2. Benefits (atomic, shared, consistent)
  3. Challenges (build perf, tooling, ownership)
  4. Tooling choice (pnpm + Turbo / Nx)
  5. CI strategy (affected + remote cache)
  6. Trade-offs (vs polyrepo, repo size)

QUICK COMPARISON:
  Turborepo  → simple, fast, framework-agnostic
  Nx         → generators, dep graph, module boundaries
  pnpm       → fast, strict, content-addressable

KEY COMMANDS:
  turbo run build --filter=...[main]   # affected since main
  nx affected --target=test --base=main
  pnpm add <pkg> --filter <workspace>
  pnpm changeset && pnpm changeset version

INTERVIEW WINNERS:
  - Mention `workspace:*` and hoisting
  - Discuss `affected` + remote cache in CI
  - Bring up Nx depConstraints for module boundaries
  - Reference Changesets for versioning
  - Compare to Google's Piper / Bazel at scale
```

---

## See Also

- [Build Tools](../23-Build-Tools/)
- [CI/CD](../15-CI-CD/)
- [Git Advanced](../24-Git-Advanced/)
- [Monorepo Overview](01-Monorepo-Overview.md)
- [Monorepo Tools Deep-Dive](05-Monorepo-Tools.md)
- [Nx](03-Nx.md)
- [Turborepo](02-Turborepo.md)


## References & Learn More

- [Changesets](https://github.com/changesets/changesets)
- [Google's "Why Google Stores Billions of Lines in One Repo"](https://research.google/pubs/large-scale-monorepo-development-the-relative-effectiveness-of-continuous-architectural-dependency-analysis-and-worker-automation-in-google/)
- [Monorepo.tools](https://monorepo.tools/)
- [Nx Documentation](https://nx.dev/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Turborepo Documentation](https://turbo.build/)
- [Yarn Workspaces](https://yarnpkg.com/features/workspaces)
