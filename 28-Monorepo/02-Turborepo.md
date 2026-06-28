# Turborepo

## Definition
Turborepo is a high-performance build system for JavaScript and TypeScript codebases, designed for scaling monorepos. It provides intelligent caching, parallelization, and task scheduling to dramatically speed up builds and development workflows.

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

## Interview Questions

### Beginner (5)

1. **What is Turborepo?**

   - Answer: A high-performance build system for JavaScript/TypeScript monorepos with intelligent caching and parallelization.

2. **What are the benefits of Turborepo?**

   - Answer: Faster builds through caching, parallelization, remote cache sharing, and zero configuration.

3. **What is a turbo.json pipeline?**

   - Answer: Configuration that defines how tasks relate to each other, what they cache, and their dependencies.

4. **How does Turborepo caching work?**

   - Answer: Content-based hashing of inputs, stores outputs locally and remotely, reuses cache when inputs haven't changed.

5. **What is remote caching?**

   - Answer: Sharing build cache across team members and CI/CD via Vercel or self-hosted solutions.

### Intermediate (5)

6. **How do you configure task dependencies in Turborepo?**

   - Answer: Use `dependsOn` in turbo.json to specify which tasks must run before others.

7. **What are task inputs and outputs?**

   - Answer: Inputs are files that affect task execution; outputs are files produced by the task that should be cached.

8. **How do you run tasks for specific packages?**

   - Answer: Use `--filter` flag: `turbo run build --filter=@myorg/web`

9. **What is the difference between `^build` and `build`?**

   - Answer: `^build` runs build in dependencies first; `build` only runs in the current package.

10. **How do you handle environment variables in Turborepo?**

    - Answer: Use `globalEnv` or task-specific `env` in turbo.json to declare environment dependencies.

### Senior (10)
11. **How does Turborepo determine when to use cache?**

    - Answer: Content-based hashing of all inputs (files, dependencies, environment), compares with stored cache metadata.

12. **Explain Turborepo's parallelization strategy**

    - Answer: Analyzes dependency graph, identifies independent tasks, runs them in parallel using worker threads.

13. **How do you optimize Turborepo cache hit rates?**

    - Answer: Minimize input changes, use stable dependencies, avoid unnecessary env vars, use proper outputs.

14. **What is the impact of global dependencies on caching?**

    - Answer: Changes to global dependencies invalidate cache for all tasks, so minimize them.

15. **How do you debug Turborepo cache issues?**

    - Answer: Use `--dry` and `--verbose` flags, check `.turbo` directory, analyze cache inputs.

16. **How do you handle non-deterministic tasks?**

    - Answer: Mark as `cache: false` or use proper inputs/outputs to capture all affecting files.

17. **What is the difference between local and remote cache?**

    - Answer: Local cache is per machine; remote cache is shared across team/CI via Vercel or self-hosted.

18. **How do you secure remote cache?**

    - Answer: Use token-based authentication, restrict access, enable signature verification.

19. **How do you migrate from Lerna to Turborepo?**

    - Answer: Keep package structure, replace Lerna commands with Turborepo, configure turbo.json.

20. **How do you monitor Turborepo performance?**

    - Answer: Track cache hit rates, build times, use `--dry` to analyze task execution.

### FAANG-style (5)
21. **Design a Turborepo setup for a large organization**

    - Answer:
      - Package structure with clear boundaries
      - Remote caching with Vercel/self-hosted
      - CI/CD with affected-based builds
      - Monitoring and alerting
      - Developer tooling and documentation

22. **How would you optimize Turborepo for a 500+ package monorepo?**

    - Answer:
      - Remote caching with high hit rates
      - Parallelization across packages
      - Incremental builds
      - Distributed builds
      - Monitoring and profiling

23. **Explain Turborepo's architecture at scale**

    - Answer:
      - Task scheduler with dependency graph
      - Content-based hashing
      - Distributed caching
      - Worker thread parallelization
      - Plugin system for extensions

24. **How do you handle Turborepo in a microservices architecture?**

    - Answer:
      - Service-specific pipelines
      - Independent deployments
      - Shared libraries via packages
      - Coordinated releases

25. **Design a CI/CD pipeline with Turborepo**

    - Answer:
      - Detect changes with `turbo run build --dry`
      - Run affected tests
      - Build with caching
      - Deploy changed services
      - Coordinate releases

### Follow-ups (5)
26. **How do you handle Turborepo with Docker?**

    - Answer: Multi-stage builds, copy dependency files first for layer caching, use turbo prune for minimal images.

27. **What is the impact of Turborepo on developer experience?**

    - Answer: Faster builds, less waiting, better productivity, but requires understanding caching concepts.

28. **How do you handle Turborepo in monorepos with multiple languages?**

    - Answer: Use language-specific task runners within Turborepo, configure appropriate inputs/outputs.

29. **How do you handle Turborepo with different Node.js versions?**

    - Answer: Use `.node-version` or `engines` in package.json, ensure consistent environments.

30. **What are the limitations of Turborepo?**

    - Answer: JavaScript/TypeScript focus, learning curve for caching, remote cache costs, and complexity at scale.

## Summary

Turborepo provides a high-performance build system for monorepos with intelligent caching, parallelization, and remote cache sharing. Master its configuration and best practices to dramatically improve build times.

## References & Learn More

- [Turborepo Documentation](https://turborepo.org/docs)
- [Turborepo GitHub](https://github.com/vercel/turborepo)
- [Turborepo Examples](https://github.com/vercel/turborepo/tree/main/examples)
- [Remote Caching](https://turborepo.org/docs/core-concepts/remote-caching)
- [Task Configuration](https://turbo.build/reference/configuration)
