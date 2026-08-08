---
section: Monorepo
category: Reference
tags: [concept, reference, tool]
---

# Monorepo Tools Deep-Dive (Lerna, pnpm, Yarn, Rush, Bazel)

> Beyond Turborepo and Nx, the monorepo ecosystem includes Lerna (now in maintenance), pnpm, Yarn Berry, Rush (Microsoft), and Bazel (Google-grade). This file covers the trade-offs and when each wins.

## Definition

The monorepo toolchain splits into three layers: (1) **package manager** (pnpm, Yarn, npm) handles installs and workspaces; (2) **task graph runner** (Turborepo, Nx, Lerna) orchestrates build/test/lint; (3) **advanced build systems** (Bazel, Rush) provide hermetic, multi-language builds at extreme scale.

## Why It Matters (TL;DR)

- **Tooling choice compounds** — picking the right stack upfront saves years of pain
- **Lerna is largely deprecated** — know its legacy role and modern replacements
- **Yarn Berry / pnpm are the 2026 package-manager defaults** for JS/TS
- **Rush / Bazel** solve problems that Turborepo and Nx don't

## Package Managers Compared

| Feature | pnpm 9 | npm 10 | Yarn Berry 4 | Yarn Classic 1 |
|---------|--------|--------|--------------|----------------|
| Install speed | Fastest | Slowest (improved) | Fast (PnP) | Medium |
| Disk usage | Lowest (content-addressable) | High (per-project) | Lowest (PnP) | High |
| Phantom dep prevention | Yes (strict) | No | Yes (PnP) | No |
| Workspace protocol | `workspace:*` | `*` | `workspace:*` | `workspace:*` |
| Node version manager | Built-in (`pnpm env`) | External (nvm) | Built-in (`corepack`) | External |
| Lockfile | `pnpm-lock.yaml` | `package-lock.json` | `yarn.lock` | `yarn.lock` |
| Best for | Most teams in 2026 | Legacy | Hermetic, large monorepos | Legacy |
| Plug'n'Play (PnP) | No | No | Yes (default) | No |

## Task Runners Compared

| Feature | Turborepo | Nx | Lerna (maintenance) | Rush | Bazel |
|---------|-----------|-----|---------------------|------|-------|
| Status | Active (Vercel) | Active (Nrwl) | Maintenance | Active (Microsoft) | Active (Google) |
| Primary IaC | `turbo.json` | `nx.json` + `project.json` | `lerna.json` | `rush.json` | `BUILD` files |
| Cache | Local + Vercel | Local + Nx Cloud | None | Local + Rush storage | Local + remote |
| Affected | `--filter=...<base>` | `nx affected` | `lerna changed` | `rush change` | Query-based |
| Generators | None | First-class | Limited | Plugins | Rules |
| Polyglot | JS/TS only | JS/TS first | JS/TS only | JS/TS only | 20+ languages |
| Learning curve | Low | Medium | Low | Medium | High |
| Best for | Simple to medium | Large JS/TS | Legacy | Microsoft stacks | Multi-language, Google-scale |

## Code Examples

### 1. pnpm Filter (Recursive Operations)

```bash
# Run in a specific package
pnpm --filter @myorg/web dev

# Run in package and its dependencies (build order: deps first)
pnpm --filter @myorg/web... build

# Run in packages that depend on @myorg/utils
pnpm --filter ...@myorg/utils test

# Run in all packages (no filter)
pnpm -r run lint

# Run in all packages with a tag (e.g., "react" tag from package.json)
pnpm --filter "...[tag=scope]" build
```

### 2. Yarn Berry Plug'n'Play (PnP)

```yaml
# .yarnrc.yml
nodeLinker: pnp
enableGlobalCache: true
```

```bash
# Zero-installs — commit .yarn/cache to git
yarn install
yarn workspaces foreach run build

# In CI: just checkout and run — no install needed
```

Trade-offs: PnP breaks some tools (Jest, Webpack legacy loaders) — `.pnp.cjs` shim or `nodeLinker: node-modules` for compatibility.

### 3. Lerna (Maintenance Mode) — What It Used to Do

```bash
# Old Lerna workflow (now superseded by Changesets)
lerna bootstrap     # install all packages' deps
lerna run build     # run script in all packages
lerna changed       # list packages changed since last release
lerna publish       # version bump + npm publish
```

Modern equivalent: **Changesets** for versioning + **Turborepo/Nx** for tasks. Most projects that started with Lerna have migrated.

### 4. Rush (Microsoft) — Polyrepo + Changelogs at Scale

```json
// rush.json (excerpt)
{
  "projects": [
    { "packageName": "@myorg/web",   "projectFolder": "apps/web" },
    { "packageName": "@myorg/ui",    "projectFolder": "packages/ui" },
    { "packageName": "@myorg/utils", "projectFolder": "packages/utils" }
  ],
  "pnpmVersion": "9.0.0",
  "rushVersion": "5.0.0",
  "repository": { "url": "https://github.com/myorg/monorepo" }
}
```

```bash
rush install              # install everything
rush build                # build all projects
rush change               # write changelog entries
rush publish              # version + publish
```

### 5. Bazel (Google) — When You Need Multi-Language

```python
# packages/ui/BUILD.bazel
load("@npm//@myorg/utils:package_json.bzl", utils = "utils")

ts_library(
    name = "ui",
    srcs = glob(["src/**/*.ts"]),
    deps = [
        "//packages/utils:utils",
        "@npm//react",
        "@npm//react-dom",
    ],
    visibility = ["//visibility:public"],
)
```

```bash
bazel build //packages/ui:ui
bazel test //packages/ui:ui
bazel query 'deps(//apps/web:web)'   # show dependency graph
```

When to reach for Bazel: large polyglot monorepo (TS + Go + Python + Java), need hermetic reproducible builds, or matching Google-scale CI.

## Real-World Architecture Decisions

```text
DECISION TREE:
┌─────────────────────────────────────────────────────────────────┐
│  JS/TS only, small team (< 20)                                  │
│  → pnpm workspaces + Turborepo                                  │
│                                                                 │
│  JS/TS only, medium team (20-100)                               │
│  → pnpm + Nx (for generators + module boundaries)               │
│  OR pnpm + Turborepo + Changesets                              │
│                                                                 │
│  JS/TS only, large team (100+)                                 │
│  → pnpm + Nx + Nx Cloud                                        │
│  OR Yarn Berry + Rush                                          │
│                                                                 │
│  Multi-language (TS + Go + Python + Rust)                      │
│  → Bazel                                                        │
│                                                                 │
│  Migrating from Lerna                                           │
│  → Changesets + Turborepo (or Nx)                              │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Choosing Bazel for a small monorepo | Bazel's learning curve is brutal; only adopt for multi-language or >100 eng |
| Phantom dependencies in npm/Yarn | Use pnpm strict mode or Yarn PnP |
| Lerna for new projects in 2026 | Use Changesets + Turborepo/Nx |
| Mixing Rush and pnpm | Rush manages its own pnpm install; don't run `pnpm install` at root |
| Committing `node_modules` | Use pnpm's content-addressable store or Yarn Berry's PnP cache |

## Best Practices

1. **Pick one package manager** — don't mix pnpm and Yarn in the same repo
2. **Use `workspace:*` consistently** — every internal package reference should use it
3. **Pin the toolchain** — `packageManager: pnpm@9.0.0` in root `package.json`
4. **Adopt Changesets for versioning** — even for private packages
5. **Set up remote cache early** — biggest ROI of Turborepo / Nx
6. **Document the choice** — explain in CONTRIBUTING.md why the team uses X over Y
7. **Re-evaluate annually** — the monorepo ecosystem moves fast

## Summary

- The 2026 monorepo stack for most JS/TS teams is **pnpm + Turborepo (or Nx) + Changesets**
- Lerna is in maintenance mode — prefer Changesets for new projects
- Yarn Berry's PnP is excellent for large monorepos with zero-install
- Rush is the Microsoft-grade alternative for very large JS/TS
- Bazel is the right answer for multi-language or Google-scale builds

---

## Cheat Sheet

```text
MONOREPO TOOLS CHEAT SHEET
═══════════════════════════════════════════════════════════════

CHOOSE BY SCALE:
  < 20 engineers (JS/TS)        → pnpm + Turborepo
  20-100 engineers (JS/TS)     → pnpm + Nx (or Turbo)
  100+ engineers (JS/TS)       → pnpm + Nx + Nx Cloud
                                OR Yarn Berry + Rush
  Multi-language               → Bazel

PACKAGE MANAGER PICK (2026):
  Most teams                   → pnpm
  Hermetic / large monorepo    → Yarn Berry (PnP)
  Legacy                       → npm / Yarn Classic

INTERVIEW ANSWER:
  1. Why you chose the tool (scale, language, team)
  2. How the cache works (content hash, remote)
  3. How you enforce boundaries (tags, depConstraints)
  4. Migration story from polyrepo / Lerna
```

---

## See Also

- [Build Tools](../23-Build-Tools/)
- [CI/CD](../15-CI-CD/)
- [Git Advanced](../24-Git-Advanced/)
- [Monorepo Overview](01-Monorepo-Overview.md)
- [Nx](03-Nx.md)
- [Turborepo](02-Turborepo.md)


## References & Learn More

- [Bazel](https://bazel.build/)
- [Google Monorepo Paper](https://research.google/pubs/large-scale-monorepo-development-the-relative-effectiveness-of-continuous-architectural-dependency-analysis-and-worker-automation-in-google/)
- [Lerna (maintenance mode)](https://lerna.js.org/)
- [pnpm](https://pnpm.io/)
- [Rush](https://rushjs.io/)
- [Turborepo vs Nx Comparison](https://blog.nrwl.io/turborepo-vs-nx-why-you-should-use-nx-for-your-next-monorepo-d04ccb54a2d4)
- [Yarn Berry](https://yarnpkg.com/)
