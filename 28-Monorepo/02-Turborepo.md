# Turborepo

[![Category: Reference](https://img.shields.io/badge/category-Reference-808080)](.)

cript codebases, designed for scaling monorepos. It provides intelligent caching, parallelization, and task scheduling to dramatically speed up builds and development workflows.

## Why Do We Need It?

- **Build Speed**: Intelligent caching reduces build times by 85%+
- **Parallelization**: Run tasks in parallel across packages
- **Remote Sharing**: Share cache across team and CI/CD
- **Zero Configuration**: Works with existing npm/yarn/pnpm setups
- **Incremental Builds**: Only rebuild what changed

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    TURBOREPO ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    turbo.json (Pipeline)                     │   │
│  │  • Define task dependencies                                 │   │
│  │  • Configure caching                                        │   │
│  │  • Set inputs/outputs                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Task Scheduler                             │   │
│  │  • Analyze dependency graph                                 │   │
│  │  • Determine execution order                                │   │
│  │  • Parallelize independent tasks                            │   │
│  │  • Apply caching strategy                                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│         ┌────────────────────┼────────────────────┐                │
│         ▼                    ▼                    ▼                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │   Package   │    │   Package   │    │   Package   │            │
│  │     A       │    │     B       │    │     C       │            │
│  │  (Cached)   │    │  (Build)    │    │  (Pending)  │            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Cache Layer                               │   │
│  │  • Local cache (node_modules/.cache/turbo)                  │   │
│  │  • Remote cache (Vercel, self-hosted)                       │   │
│  │  • Content-based hashing                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

```

## Pipeline Configuration

### turbo.json Structure

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env.*"],
  "globalEnv": ["NODE_ENV"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"],
      "inputs": ["src/**", "package.json", "tsconfig.json"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "clean": {
      "cache": false
    }
  }
}

```

## Code Examples

### 1. Basic Turborepo Setup

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "outputs": []
    }
  }
}

```

```json
// package.json
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "clean": "turbo run clean"
  },
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}

```

### 2. Task Dependencies

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  }
}

```

### 3. Package-Specific Configuration

```json
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "scripts": {
    "build": "tsc && vite build",
    "dev": "vite build --watch",
    "lint": "eslint src --ext .ts,.tsx",
    "test": "vitest run",
    "typecheck": "tsc --noEmit"
  },
  "turbo": {
    "build": {
      "outputs": ["dist/**"]
    }
  }
}

```

### 4. Remote Caching Setup

```bash
# Login to Vercel for remote caching
npx turbo login

# Link your repository
npx turbo link

# Or use self-hosted remote cache
export TURBO_TOKEN=your-token
export TURBO_TEAM=your-team

```

```json
// turbo.json with remote cache
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "env": ["NODE_ENV"]
    }
  },
  "remoteCache": {
    "signature": true
  }
}

```

### 5. Custom Turborepo Tasks

```typescript
// scripts/turbo-tasks.ts
import { execSync } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

// Custom task to generate API types
export function generateApiTypes() {
  const packages = ['packages/api-client', 'packages/web'];

  packages.forEach((pkg) => {
    const configPath = join(pkg, 'turbo.json');
    const config = JSON.parse(readFileSync(configPath, 'utf-8'));

    // Add custom task
    config.pipeline['generate:types'] = {
      dependsOn: ['^build'],
      outputs: ['src/types/**'],
    };

    writeFileSync(configPath, JSON.stringify(config, null, 2));
  });
}

// Custom task to update dependencies
export function updateDependencies() {
  execSync('pnpm update -r', { stdio: 'inherit' });
  execSync('turbo run build', { stdio: 'inherit' });
}

```

### 6. Turborepo with Docker

```dockerfile
# Dockerfile for monorepo
FROM node:18-alpine AS base
RUN npm install -g turbo

# Copy dependency files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/ui/package.json ./packages/ui/
COPY packages/utils/package.json ./packages/utils/
COPY apps/web/package.json ./apps/web/

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build with turbo
RUN turbo run build --filter=@myorg/web

# Production stage
FROM node:18-alpine AS production
WORKDIR /app

COPY --from=base /app/apps/web/dist ./dist
COPY --from=base /app/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "dist/server.js"]

```

### 7. Turborepo CI/CD Configuration

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:

      - uses: actions/checkout@v3
        with:
          fetch-depth: 2

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'pnpm'

      - name: Install pnpm
        run: npm install -g pnpm

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo build --cache-dir=.turbo

      - name: Lint
        run: pnpm turbo lint

      - name: Test
        run: pnpm turbo test

```

### 8. Turborepo with Changesets

```json
// .changeset/config.json
{
  "$schema": "https://unpkg.com/@changesets/config@2.3.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "restricted",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}

```

```bash
# Create a changeset
pnpm changeset

# Version packages
pnpm changeset version

# Publish packages
pnpm changeset publish

```

## Real-World Use Cases

### Large-Scale Application

```text
Monorepo Structure:
┌─────────────────────────────────────────────────────────────────┐
│  Apps:                                                          │
│  • web (Next.js) - Build: 45s → 3s (cached)                   │
│  • admin (React) - Build: 30s → 2s (cached)                    │
│  • api (Node.js) - Build: 20s → 1s (cached)                    │
│                                                                 │
│  Packages:                                                      │
│  • ui - Build: 15s → 1s (cached)                               │
│  • utils - Build: 5s → 0.5s (cached)                           │
│  • config - Build: 2s → 0.2s (cached)                          │
│                                                                 │
│  Total Build Time: 117s → 7.7s (93% faster)                    │
└─────────────────────────────────────────────────────────────────┘

```

## Common Mistakes

1. **Incorrect outputs**: Not specifying build outputs correctly

2. **Missing dependencies**: Not declaring task dependencies

3. **Ignoring global dependencies**: Forgetting env files or configs

4. **Over-caching**: Caching tasks that shouldn't be cached

5. **Not using remote caching**: Missing out on team-wide cache

## Best Practices

1. **Define clear outputs**: Specify exactly what each task produces

2. **Use content hashing**: Let Turborepo determine when to rebuild

3. **Leverage remote caching**: Share cache across team and CI/CD

4. **Monitor cache hit rates**: Track and optimize cache effectiveness

5. **Use affected commands**: Only run tasks for changed packages

## Performance Considerations

```text
Cache Hit Rate Optimization:
┌─────────────────────────────────────────────────────────────────┐
│  High Cache Hit Rate (>80%):                                    │
│  • Clear task outputs                                          │
│  • Stable dependencies                                         │
│  • Consistent environment                                      │
│                                                                 │
│  Low Cache Hit Rate (<50%):                                     │
│  • Check for unnecessary input changes                         │
│  • Review global dependencies                                  │
│  • Verify environment variables                                │
│  • Check for non-deterministic builds                          │
└─────────────────────────────────────────────────────────────────┘

```

## Summary

Turborepo provides a high-performance build system for monorepos with intelligent caching, parallelization, and remote cache sharing. Master its configuration and best practices to dramatically improve build times.

---

## See Also
- [Build Tools](../23-Build-Tools/)
- [CI/CD](../15-CI-CD/)
- [Git Advanced](../24-Git-Advanced/)

## References & Learn More

- [Turborepo Documentation](https://turborepo.org/docs)
- [Turborepo GitHub](https://github.com/vercel/turborepo)
- [Turborepo Examples](https://github.com/vercel/turborepo/tree/main/examples)
- [Remote Caching](https://turborepo.org/docs/core-concepts/remote-caching)
- [Task Configuration](https://turbo.build/reference/configuration)
