---
section: Monorepo
category: Reference
tags: [concept, tool, reference]
---

# Turborepo

> Turborepo is a high-performance build system for JavaScript and TypeScript monorepos. It provides intelligent caching, parallelization, and task scheduling to dramatically speed up builds and development workflows.

## Definition

Turborepo is an incremental bundler and task runner from Vercel that builds a dependency graph of workspace tasks, runs them in topological order, parallelizes independent work, and caches every output locally and (optionally) remotely. It's the de-facto choice for new JS/TS monorepos in 2026.

## Why It Matters (TL;DR)

- **Build speed** — content-hash caching reduces build times by 70-95%
- **Parallelization** — runs independent tasks concurrently across packages
- **Remote cache** — share cache across team and CI, so CI almost never re-does work
- **Zero config** — works with existing npm/yarn/pnpm setups
- **Incremental** — only rebuilds what changed, downstream, and what's affected

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    TURBOREPO ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    turbo.json (Pipeline)                     │   │
│  │  • Define task dependencies                                 │   │
│  │  • Configure caching (inputs/outputs)                        │   │
│  │  • Set environment variables that affect the hash           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Task Scheduler                             │   │
│  │  • Analyze workspace dependency graph                       │   │
│  │  • Determine execution order (topological)                  │   │
│  │  • Parallelize independent tasks                            │   │
│  │  • Check cache before running                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│         ┌────────────────────┼────────────────────┐                │
│         ▼                    ▼                    ▼                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │   Package   │    │   Package   │    │   Package   │            │
│  │     A       │    │     B       │    │     C       │            │
│  │  (cached)   │    │  (build)    │    │  (pending)  │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Cache Layer                               │   │
│  │  • Local cache (node_modules/.cache/turbo)                  │   │
│  │  • Remote cache (Vercel, self-hosted)                       │   │
│  │  • Content-hash based (inputs + env + deps)                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Pipeline Configuration (Turborepo 2.x)

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "globalEnv": ["NODE_ENV", "CI"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"],
      "inputs": ["src/**", "package.json", "tsconfig.json", "vite.config.ts"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "env": ["NODE_ENV", "TEST_DATABASE_URL"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "outputs": []
    },
    "clean": {
      "cache": false
    }
  }
}
```

## Code Examples

### 1. Basic Pipeline (Build, Test, Lint)

```json
// turbo.json (minimal)
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": { "outputs": [] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

```json
// Root package.json
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "typecheck": "turbo run typecheck"
  }
}
```

### 2. Filter (Run on Affected Packages)

```bash
# Only run build for @myorg/web and its dependencies
turbo run build --filter=@myorg/web...

# Only run if the package changed since main
turbo run build --filter=...[origin/main]

# Run on a specific package
turbo run test --filter=@myorg/utils

# All packages with a given tag
turbo run build --filter=...#canary
```

### 3. Remote Caching (Vercel / Self-Hosted)

```bash
# Login to Vercel for remote caching
npx turbo login

# Link the repo
npx turbo link

# Or use self-hosted / custom
export TURBO_TOKEN=your-token
export TURBO_TEAM=your-team
```

```json
// turbo.json — enable remote cache signing
{
  "remoteCache": {
    "signature": true
  }
}
```

```yaml
# .github/workflows/ci.yml — pass the cache credentials
jobs:
  build:
    env:
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: ${{ vars.TURBO_TEAM }}
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo build test lint
```

### 4. Docker Layer Caching with Turborepo

```dockerfile
# Dockerfile (multi-stage)
FROM node:20-alpine AS base
RUN corepack enable

# 1. Deps layer — only rebuilds when package.json files change
FROM base AS deps
WORKDIR /app
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY packages/ui/package.json ./packages/ui/
COPY packages/utils/package.json ./packages/utils/
COPY apps/web/package.json ./apps/web/
RUN pnpm install --frozen-lockfile

# 2. Build layer — uses Turborepo's hash to skip when unchanged
FROM base AS builder
WORKDIR /app
COPY --from=deps /app /app
COPY . .
RUN pnpm turbo build --filter=@myorg/web

# 3. Runtime — minimal final image
FROM base AS runner
WORKDIR /app
COPY --from=builder /app/apps/web/dist ./dist
COPY --from=builder /app/apps/web/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### 5. Per-Package Overrides

```json
// packages/ui/package.json — package-specific turbo config
{
  "name": "@myorg/ui",
  "scripts": {
    "build": "tsc && vite build",
    "dev": "vite build --watch",
    "lint": "eslint src --ext .ts,.tsx",
    "test": "vitest run"
  },
  "turbo": {
    "extends": ["//"],
    "tasks": {
      "build": { "outputs": ["dist/**"] }
    }
  }
}
```

### 6. With Changesets for Versioning

```bash
# .changeset workflow
pnpm changeset              # write a changeset describing the change
pnpm changeset version      # bump versions, update CHANGELOG
pnpm changeset publish      # publish to npm
```

## Real-World Use Case: Large-Scale Application

```text
Monorepo Structure (1 app + 6 packages):
┌─────────────────────────────────────────────────────────────────┐
│  Apps:                                                          │
│  • web (Next.js) — Build: 45s → 3s (cached)                   │
│  • admin (React) — Build: 30s → 2s (cached)                    │
│  • api (Node.js) — Build: 20s → 1s (cached)                    │
│                                                                 │
│  Packages:                                                      │
│  • ui — Build: 15s → 1s (cached)                               │
│  • utils — Build: 5s → 0.5s (cached)                           │
│  • config — Build: 2s → 0.2s (cached)                          │
│                                                                 │
│  Total Build Time: 117s → 7.7s (93% faster)                    │
│  Remote cache hit rate: ~85% on CI, ~95% locally                │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `outputs` declaration | Specify every file the task produces — Turborepo can't cache what it doesn't know about |
| Wrong `dependsOn` (missing `^`) | Use `^build` for upstream (npm dependency) builds; `build` for same-package prerequisites |
| Caching non-deterministic tasks (e.g., deploy) | Set `cache: false` for tasks with side effects |
| Forgetting to set `globalEnv` | Env vars (NODE_ENV, secrets) affect the cache hash — declare them explicitly |
| Not using remote cache in CI | Set `TURBO_TOKEN` and `TURBO_TEAM`; without them, CI redoes work your laptop already did |
| Pinning `turbo` to `^1` | Turborepo 2.x changed `pipeline` → `tasks` and added `tasks`; upgrade for the modern config |

## Best Practices

1. **Define `outputs` precisely** — every file the task produces should be in the outputs list
2. **Use content hashing** — let Turborepo determine cache validity from inputs
3. **Leverage remote caching in CI** — share cache across team and CI
4. **Monitor cache hit rate** — `turbo run build --summarize` writes a JSON report
5. **Use `filter` for affected builds** — only build what changed since main
6. **Cache Docker layers with Turborepo** — see example above
7. **Use `env` for secrets** — declare env vars that affect the cache hash

## Performance Considerations

```text
Cache Hit Rate Optimization:
┌─────────────────────────────────────────────────────────────────┐
│  High Hit Rate (>80%):                                          │
│  • Clear task outputs                                          │
│  • Stable dependencies                                         │
│  • Consistent environment across dev / CI                      │
│  • Pin tool versions                                            │
│                                                                 │
│  Low Hit Rate (<50%):                                           │
│  • Check for unnecessary input changes (e.g., timestamps)      │
│  • Review globalDependencies / globalEnv                       │
│  • Verify environment variables                                │
│  • Check for non-deterministic builds                          │
│  • Look for missing outputs (cache misses silently)             │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- Turborepo is a build orchestrator that runs tasks in dependency order, parallelizes where possible, and caches everything
- Configure with `turbo.json` — declare `tasks`, `inputs`, `outputs`, `dependsOn`, and `env`
- Remote cache (`TURBO_TOKEN` + `TURBO_TEAM`) is the killer feature — shared across team and CI
- Use `filter` to build only what changed; `--filter=...<base>` for affected changes
- Common pitfalls: missing outputs, missing env declarations, caching non-deterministic tasks

---

## Cheat Sheet

```text
TURBOREPO CHEAT SHEET
═══════════════════════════════════════════════════════════════

PIPELINE ANATOMY:
  dependsOn: ["^build"]  → build upstream deps first
  outputs:   ["dist/**"] → what to cache
  inputs:    ["src/**"]  → what affects the cache hash
  env:       ["API_URL"] → env vars that affect the hash
  cache:     false       → skip caching
  persistent: true       → long-running (dev servers)

KEY COMMANDS:
  turbo run build                       # all packages
  turbo run build --filter=@myorg/web   # one package
  turbo run build --filter=...[main]    # affected since main
  turbo run build --summarize           # cache hit report

INTERVIEW ANSWER:
  1. What problem Turborepo solves (build time, cache)
  2. How the cache key is computed (inputs + env + deps)
  3. Why remote cache matters (CI / team share)
  4. How you handle non-deterministic tasks
```

---

## See Also

- [Build Tools](../23-Build-Tools/)
- [CI/CD](../15-CI-CD/)
- [Git Advanced](../24-Git-Advanced/)
- [Monorepo Overview](01-Monorepo-Overview.md)
- [Monorepo Tools Deep-Dive](05-Monorepo-Tools.md)
- [Nx](03-Nx.md)


## References & Learn More

- [Remote Caching](https://turbo.build/docs/core-concepts/remote-caching)
- [Task Configuration Reference](https://turbo.build/reference/configuration)
- [Turborepo Documentation](https://turbo.build/)
- [Turborepo Examples](https://github.com/vercel/turborepo/tree/main/examples)
- [Turborepo GitHub](https://github.com/vercel/turborepo)
