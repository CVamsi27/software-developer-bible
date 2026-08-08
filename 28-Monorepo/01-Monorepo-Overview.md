---
section: Monorepo
category: Reference
tags: [concept, overview]
---

# Monorepo Overview

> A monorepo (monolithic repository) is a software development strategy where code for multiple projects is stored in a single repository. It provides a unified approach to managing multiple packages, applications, or services with shared dependencies and configurations.

## Definition

A monorepo is a single version-controlled repository that hosts the source code for multiple logically distinct projects (apps, libraries, services). It relies on package-manager workspaces plus a task-graph tool (Turborepo, Nx, Lerna) to coordinate builds, tests, and dependencies.

## Why It Matters (TL;DR)

- **Code sharing** — packages are first-class, no need to publish to npm to consume them
- **Atomic changes** — one commit, one PR, one CI run crosses all packages
- **Consistent dependencies** — single source of truth for versions (no `package.json` drift)
- **Simplified refactoring** — rename a symbol across the entire codebase in one PR
- **Better code review** — reviewers see the full impact, not just one repo

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    MONOREPO STRUCTURE                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  my-monorepo/                                                      │
│  ├── package.json          (root)                                  │
│  ├── pnpm-workspace.yaml   (workspace config)                      │
│  ├── turbo.json            (task runner config)                    │
│  ├── tsconfig.base.json    (shared TypeScript config)              │
│  │                                                                 │
│  ├── packages/                                                    │
│  │   ├── ui/              (shared UI components)                   │
│  │   ├── utils/           (shared utilities)                       │
│  │   └── config/          (shared configurations)                  │
│  │                                                                 │
│  ├── apps/                                                        │
│  │   ├── web/             (Next.js app)                            │
│  │   ├── api/             (Node.js API)                            │
│  │   └── mobile/          (React Native app)                       │
│  │                                                                 │
│  └── tools/                                                       │
│      ├── eslint-config/   (shared ESLint config)                   │
│      └── typescript-config/ (shared TS config)                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Monorepo vs Polyrepo

| Dimension | Monorepo | Polyrepo |
|-----------|----------|----------|
| Code sharing | Easy (same repo) | Complex (npm publish or git submodules) |
| Atomic changes | One commit crosses all packages | Many PRs across many repos |
| Dependency management | Single source (root + overrides) | Per repo; drift is common |
| CI/CD | Unified pipeline with task graph | Per-repo pipelines; no cross-cutting view |
| Code review | See full impact in one PR | Separate PRs; cross-cutting changes painful |
| Refactoring | Find-and-replace all in one go | Cross-repo refactor is hero-mode |
| Team independence | Limited (merge conflicts, CODEOWNERS) | High (each team owns its repo) |
| Tooling | Specialized (Turborepo, Nx, Lerna) | Standard npm/yarn |
| Repo size | Large (multi-GB) | Manageable per repo |
| Access control | Code-level (CODEOWNERS) | Repo-level (org permissions) |

## Workspace Setup (pnpm, Yarn, npm)

### pnpm (Most Common in 2026)

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "packageManager": "pnpm@9.0.0",
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "typecheck": "turbo run typecheck"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.4.0"
  }
}
```

```json
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "version": "0.0.1",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "dependencies": {
    "@myorg/utils": "workspace:*",
    "react": "^18.3.0"
  }
}
```

```bash
# Install
pnpm install

# Add dependency to a specific package
pnpm add react --filter @myorg/ui

# Run script in package and its dependencies (topological order)
pnpm --filter @myorg/web... run build

# Run script in all packages
pnpm -r run lint
```

### Yarn Berry (Berry / Yarn 4)

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*", "apps/*"],
  "packageManager": "yarn@4.0.0"
}
```

```bash
yarn install
yarn workspace @myorg/ui add react
yarn workspaces foreach run build
```

### npm Workspaces

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*", "apps/*"]
}
```

```bash
npm install
npm install react --workspace=@myorg/ui
npm run build --workspaces
```

## Code Examples

### 1. Shared TypeScript Config

```json
// tools/typescript-config/base.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "isolatedModules": true,
    "jsx": "react-jsx",
    "skipLibCheck": true,
    "resolveJsonModule": true
  }
}
```

```json
// packages/ui/tsconfig.json
{
  "extends": "../../tools/typescript-config/base.json",
  "compilerOptions": { "outDir": "./dist", "rootDir": "./src" },
  "include": ["src/**/*"]
}
```

### 2. Shared ESLint Config

```javascript
// tools/eslint-config/base.js
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/consistent-type-imports': 'error',
  },
};
```

```javascript
// packages/ui/eslint.config.js
import base from '../../tools/eslint-config/base.js';
export default [
  ...base,
  { rules: { 'react/prop-types': 'off' } },
];
```

### 3. Cross-Package Imports (with Path Mapping or Workspace Protocol)

```typescript
// apps/web/src/components/Button.tsx
// Direct workspace import — no build step needed
import { Button } from '@myorg/ui';

// apps/web/tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@myorg/ui": ["../../packages/ui/src/index.ts"],
      "@myorg/ui/*": ["../../packages/ui/src/*"]
    }
  }
}
```

### 4. Changesets (Versioning and Publishing)

```json
// .changeset/config.json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "access": "restricted",
  "baseBranch": "main",
  "updateInternalDependencies": "patch"
}
```

```bash
# After making changes, create a changeset
pnpm changeset
# → "patch: @myorg/ui — Fixed button hover state"

# Version packages based on changesets
pnpm changeset version

# Publish to npm
pnpm changeset publish
```

## Real-World Use Cases

### 1. Multi-Product SaaS

```text
Use Case: Multiple products sharing core libraries
┌─────────────────────────────────────────────────────────────────┐
│  Products:                                                      │
│  • Web App (Next.js)                                           │
│  • Mobile App (React Native)                                   │
│  • Admin Dashboard (React)                                     │
│  • Marketing Site (Astro)                                      │
│                                                                 │
│  Shared Packages:                                               │
│  • @company/ui (component library)                             │
│  • @company/utils (utilities)                                  │
│  • @company/api-client (API integration)                       │
│  • @company/config (shared configurations)                     │
│                                                                 │
│  Benefits:                                                      │
│  • Consistent UI across products                               │
│  • Single source of truth for API client                       │
│  • Shared type definitions                                     │
│  • Coordinated releases                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Design System Development

```text
Use Case: Shared component library
┌─────────────────────────────────────────────────────────────────┐
│  Packages:                                                      │
│  • @design-system/core (base components)                       │
│  • @design-system/icons (icon library)                         │
│  • @design-system/tokens (design tokens)                       │
│  • @design-system/react (React components)                     │
│  • @design-system/vue (Vue components)                         │
│  • @design-system/docs (documentation site)                    │
│                                                                 │
│  Benefits:                                                      │
│  • Consistent design language                                   │
│  • Single source of truth for design tokens                    │
│  • Coordinated component updates                               │
│  • Shared testing and documentation                            │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many packages (over-modularization) | Start with 3-5 packages; split when a boundary is clear |
| Circular dependencies | Use `dependency-cruiser` to detect; refactor shared types into a common package |
| Different dependency versions across packages | Use a single `pnpm-workspace.yaml` with overrides; lock with `pnpm-lock.yaml` |
| Slow CI builds | Use Turborepo remote cache; only build affected packages |
| Bad tooling choice for the team | pnpm + Turborepo is the 2026 default; pick Nx if you need dependency graph visualization |
| Untyped workspace protocol | Always commit the lockfile; pin major versions in `package.json` |

## Best Practices

1. **Start simple** — 2-3 packages, add boundaries as the codebase grows
2. **Clear package boundaries** — one purpose per package, named for what it does
3. **Consistent tooling** — pnpm + Turborepo (or Nx) for the 2026 stack
4. **Automate everything** — CI/CD, linting, type-checking, dependency updates (Renovate / Dependabot)
5. **Document structure** — keep a top-level ARCHITECTURE.md; automate with `nx graph` or `turbo ls`
6. **Use changesets for versioning** — clear changelogs, atomic multi-package releases
7. **CODEOWNERS for ownership** — explicit reviewers per package

## Performance Considerations

```text
Build Optimization Strategies:
┌─────────────────────────────────────────────────────────────────┐
│  Caching:                                                       │
│  • Turborepo remote caching (Vercel / self-hosted)              │
│  • Nx computation caching                                       │
│  • Local build cache                                            │
│                                                                 │
│  Parallelization:                                               │
│  • Run independent tasks in parallel                            │
│  • Use worker threads for CPU-intensive tasks                   │
│  • Distribute builds across CI machines                        │
│                                                                 │
│  Incremental Builds:                                            │
│  • Only rebuild changed packages (--filter)                     │
│  • Use Turborepo affected commands                             │
│  • Leverage TypeScript project references                       │
│                                                                 │
│  Dependency Optimization:                                       │
│  • Hoist common dependencies (pnpm hoisting)                    │
│  • Use workspace protocol for local packages                    │
│  • Bundle for production                                        │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- Monorepo = single repo, multiple packages, coordinated builds
- pnpm workspaces + Turborepo is the 2026 default; Nx is the alternative with stronger graph visualization
- Triggers atomic refactors, shared types, and consistent dependencies
- Common pitfalls: over-modularization, circular deps, slow CI — fix with clear boundaries and remote cache
- Pair with changesets for versioning and CODEOWNERS for ownership

---

## Cheat Sheet

```text
MONOREPO OVERVIEW CHEAT SHEET
═══════════════════════════════════════════════════════════════

CHOOSE BY STACK (2026):
  • pnpm + Turborepo        → most teams, simplest
  • pnpm + Nx               → need dependency graph / generators
  • Yarn Berry + Nx         → large monorepos, hermetic installs
  • npm workspaces          → legacy, default only

COMMON COMMANDS:
  pnpm install
  pnpm add <pkg> --filter <workspace>
  pnpm -r run build
  turbo run build --filter=<workspace>...

INTERVIEW ANSWER:
  1. Why monorepo (atomic refactors, shared types)
  2. Tooling choice (pnpm + Turbo for greenfield)
  3. CI strategy (affected + remote cache)
  4. Trade-offs (repo size, CODEOWNERS complexity)
```

---

## See Also

- [Build Tools](../23-Build-Tools/)
- [CI/CD](../15-CI-CD/)
- [Git Advanced](../24-Git-Advanced/)
- [Monorepo Tools Deep-Dive](05-Monorepo-Tools.md)
- [Nx](03-Nx.md)
- [Turborepo](02-Turborepo.md)


## References & Learn More

- [Google's Monorepo Paper (Why Google Stores Billions of Lines in One Repo)](https://research.google/pubs/large-scale-monorepo-development-the-relative-effectiveness-of-continuous-architectural-dependency-analysis-and-worker-automation-in-google/)
- [Monorepo.tools](https://monorepo.tools/)
- [Nx Documentation](https://nx.dev/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Turborepo Documentation](https://turborepo.org/docs)
- [Yarn Workspaces](https://yarnpkg.com/features/workspaces)
