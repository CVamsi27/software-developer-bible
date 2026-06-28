# Monorepo Overview

## Definition
A monorepo (monolithic repository) is a software development strategy where code for multiple projects is stored in a single repository. It provides a unified approach to managing multiple packages, applications, or services with shared dependencies and configurations.

## Why Do We Need It?

- **Code Sharing**: Easily share code between projects
- **Atomic Changes**: Make changes across multiple packages in one commit
- **Consistent Dependencies**: Single source of truth for dependency versions
- **Simplified Refactoring**: Update all affected projects simultaneously
- **Better Code Review**: See impact of changes across the entire codebase

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
│  ├── tsconfig.json         (shared TypeScript config)              │
│  │                                                                 │
│  ├── packages/                                                    │
│  │   ├── ui/              (shared UI components)                   │
│  │   │   ├── package.json                                           │
│  │   │   └── src/                                                   │
│  │   ├── utils/           (shared utilities)                       │
│  │   │   ├── package.json                                           │
│  │   │   └── src/                                                   │
│  │   └── config/          (shared configurations)                  │
│  │       ├── package.json                                           │
│  │       └── src/                                                   │
│  │                                                                 │
│  ├── apps/                                                        │
│  │   ├── web/             (Next.js app)                            │
│  │   │   ├── package.json                                           │
│  │   │   └── src/                                                   │
│  │   ├── api/             (Node.js API)                            │
│  │   │   ├── package.json                                           │
│  │   │   └── src/                                                   │
│  │   └── mobile/          (React Native app)                       │
│  │       ├── package.json                                           │
│  │       └── src/                                                   │
│  │                                                                 │
│  └── tools/                                                       │
│      ├── eslint-config/   (shared ESLint config)                   │
│      └── typescript-config/ (shared TS config)                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

```

## Monorepo vs Polyrepo

```text
Comparison:
┌─────────────────────────────────────────────────────────────────┐
│                    │ Monorepo              │ Polyrepo            │
├────────────────────┼───────────────────────┼─────────────────────┤
│ Code Sharing       │ Easy (same repo)      │ Complex (npm/pip)   │
│ Atomic Changes     │ Yes                   │ No                  │
│ Dependency Mgmt    │ Single source         │ Per repo            │
│ CI/CD              │ Unified               │ Per repo            │
│ Code Review        │ See all changes       │ Separate PRs        │
│ Refactoring        │ Easy                  │ Complex             │
│ Team Independence  │ Limited               │ High                │
│ Tooling            │ Specialized needed    │ Standard            │
└─────────────────────────────────────────────────────────────────┘

```

## Workspace Concept

### Package Manager Workspaces

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
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "typescript": "^5.0.0"
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
    "react": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}

```

## Code Examples

### 1. pnpm Workspace Setup

```yaml
# pnpm-workspace.yaml
packages:

  - 'packages/*'
  - 'apps/*'
  - 'tools/*'

```

```json
// package.json
{
  "scripts": {
    "dev": "pnpm -r run dev",
    "build": "pnpm -r run build",
    "lint": "pnpm -r run lint",
    "test": "pnpm -r run test",
    "clean": "pnpm -r run clean"
  }
}

```

```bash
# Install dependencies
pnpm install

# Add dependency to specific package
pnpm add react --filter @myorg/ui

# Add dev dependency to root
pnpm add -D typescript -w

# Run script in specific package
pnpm --filter @myorg/web run dev

# Run script in package and its dependencies
pnpm --filter @myorg/web... run build

```

### 2. Yarn Workspace Setup

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*",
    "tools/*"
  ],
  "scripts": {
    "build": "yarn workspaces foreach run build",
    "dev": "yarn workspaces foreach run dev"
  }
}

```

```bash
# Install dependencies
yarn install

# Add dependency to specific package
yarn workspace @myorg/ui add react

# Run script in all workspaces
yarn workspaces foreach run build

# Run script in specific workspace
yarn workspace @myorg/web run dev

```

### 3. npm Workspace Setup

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}

```

```bash
# Install dependencies
npm install

# Add dependency to specific package
npm install react --workspace=@myorg/ui

# Run script in all workspaces
npm run build --workspaces

# Run script in specific workspace
npm run dev --workspace=@myorg/web

```

### 4. Shared TypeScript Configuration

```json
// tools/typescript-config/base.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}

```

```json
// packages/ui/tsconfig.json
{
  "extends": "../../tools/typescript-config/base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}

```

### 5. Shared ESLint Configuration

```javascript
// tools/eslint-config/base.js
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
  },
};

```

```javascript
// packages/ui/.eslintrc.js
module.exports = {
  extends: ['../../tools/eslint-config/base.js'],
  rules: {
    // Package-specific rules
    'react/prop-types': 'off',
  },
};

```

### 6. Package.json Scripts for Monorepo

```json
// package.json (root)
{
  "scripts": {
    "build": "turbo run build",
    "build:scope": "turbo run build --filter=",
    "dev": "turbo run dev",
    "dev:web": "turbo run dev --filter=@myorg/web",
    "lint": "turbo run lint",
    "lint:fix": "turbo run lint -- --fix",
    "test": "turbo run test",
    "test:coverage": "turbo run test -- --coverage",
    "clean": "turbo run clean",
    "clean:node_modules": "find . -name node_modules -type d -exec rm -rf {} +",
    "typecheck": "turbo run typecheck"
  }
}

```

## Real-World Use Cases

### Large Enterprise Applications

```text
Use Case: Multiple products sharing core libraries
┌─────────────────────────────────────────────────────────────────┐
│  Products:                                                      │
│  • Web App (Next.js)                                           │
│  • Mobile App (React Native)                                   │
│  • Admin Dashboard (React)                                     │
│  • Marketing Site (Gatsby)                                     │
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

### Design System Development

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

1. **Too many packages**: Over-modularizing leads to complexity

2. **Circular dependencies**: Packages depending on each other

3. **Inconsistent versions**: Different packages using different versions

4. **Slow builds**: Not optimizing build pipelines

5. **Poor tooling**: Not using appropriate monorepo tools

## Best Practices

1. **Start simple**: Begin with fewer packages, split when needed

2. **Clear boundaries**: Define package responsibilities clearly

3. **Consistent tooling**: Use Turborepo, Nx, or Lerna

4. **Automate everything**: CI/CD, testing, linting

5. **Document structure**: Keep architecture documentation updated

## Performance Considerations

```text
Build Optimization Strategies:
┌─────────────────────────────────────────────────────────────────┐
│  Caching:                                                       │
│  • Turborepo remote caching                                    │
│  • Nx computation caching                                      │
│  • Local build cache                                           │
│                                                                 │
│  Parallelization:                                               │
│  • Run independent tasks in parallel                           │
│  • Use worker threads for CPU-intensive tasks                   │
│  • Distribute builds across machines                           │
│                                                                 │
│  Incremental Builds:                                            │
│  • Only rebuild changed packages                               │
│  • Use affected commands                                       │
│  • Leverage TypeScript project references                      │
│                                                                 │
│  Dependency Optimization:                                       │
│  • Hoist common dependencies                                   │
│  • Use workspace protocol for local packages                   │
│  • Bundle for production                                       │
└─────────────────────────────────────────────────────────────────┘

```

## Interview Questions

### Beginner (5)

1. **What is a monorepo?**

   - Answer: A software development strategy where code for multiple projects is stored in a single repository.

2. **What are the benefits of a monorepo?**

   - Answer: Code sharing, atomic changes, consistent dependencies, simplified refactoring, better code review.

3. **What is a workspace in package managers?**

   - Answer: A feature that allows managing multiple packages in a single repository with shared dependencies.

4. **What is the difference between monorepo and polyrepo?**

   - Answer: Monorepo stores all code in one repository; polyrepo stores each project in separate repositories.

5. **Which package managers support workspaces?**

   - Answer: npm, yarn, and pnpm all support workspaces for monorepo management.

### Intermediate (5)

6. **How do you manage dependencies in a monorepo?**

   - Answer: Use workspace protocol for local packages, hoist common dependencies, maintain consistent versions across packages.

7. **What is the workspace protocol?**

   - Answer: Using `workspace:*` in package.json to reference local packages instead of published versions.

8. **How do you handle versioning in a monorepo?**

   - Answer: Use tools like Changesets or Lerna for coordinated versioning, or independent versioning per package.

9. **What are the challenges of monorepos?**

   - Answer: Build performance, tooling complexity, team coordination, CI/CD complexity, code ownership.

10. **How do you structure a monorepo?**

    - Answer: Separate packages (shared libraries) from apps (deployable applications), use clear naming conventions.

### Senior (10)
11. **How do you optimize build performance in a monorepo?**

    - Answer: Use caching (Turborepo/Nx), parallelization, incremental builds, affected commands, and remote caching.

12. **Explain Turborepo's caching strategy**

    - Answer: Turborepo caches build outputs locally and remotely, only rebuilding packages that changed based on content hashing.

13. **How do you handle circular dependencies?**

    - Answer: Restructure packages, extract shared code to a new package, use dependency injection, or refactor to break the cycle.

14. **What is the impact of monorepo on CI/CD?**

    - Answer: Unified pipelines, build caching, affected-based testing, coordinated deployments, but increased complexity.

15. **How do you manage code ownership in a monorepo?**

    - Answer: Use CODEOWNERS file, package-level ownership, clear documentation, and team boundaries.

16. **Explain Nx's computation cache**

    - Answer: Nx caches task results based on inputs, using content hashing to determine when to rebuild vs reuse cached results.

17. **How do you handle database migrations in a monorepo?**

    - Answer: Shared migration directory, version-controlled schemas, coordinated migrations across packages.

18. **What is the strangler fig pattern in monorepo migration?**

    - Answer: Gradually migrating from polyrepo to monorepo by moving packages incrementally while maintaining both systems.

19. **How do you test in a monorepo?**

    - Answer: Unit tests per package, integration tests across packages, end-to-end tests for apps, use affected commands.

20. **How do you handle different TypeScript versions across packages?**

    - Answer: Use a shared TypeScript version, or isolate packages with their own TypeScript configurations.

### FAANG-style (5)
21. **Design a monorepo architecture for a large organization**

    - Answer:
      - Package structure: core, shared, domain-specific packages
      - Tooling: Nx/Turborepo with remote caching
      - CI/CD: Affected-based pipelines, canary deployments
      - Code ownership: Team-based CODEOWNERS
      - Documentation: Architecture decision records

22. **How would you migrate from polyrepo to monorepo?**

    - Answer:
      - Phase 1: Set up monorepo structure
      - Phase 2: Move shared packages
      - Phase 3: Migrate applications
      - Phase 4: Update CI/CD
      - Phase 5: Deprecate old repositories

23. **Explain monorepo at scale**

    - Answer:
      - Thousands of packages
      - Hundreds of developers
      - Multiple programming languages
      - Distributed builds
      - Advanced caching strategies

24. **How do you handle monorepo security?**

    - Answer:
      - Dependency scanning
      - Secret management
      - Access control per package
      - Audit logging
      - Vulnerability detection

25. **Design a CI/CD pipeline for a monorepo**

    - Answer:
      - Detect changes (affected packages)
      - Run tests for affected packages
      - Build with caching
      - Deploy only changed applications
      - Coordinate releases

### Follow-ups (5)
26. **How do you handle monorepo with multiple programming languages?**

    - Answer: Use language-agnostic tooling, separate build systems per language, shared configuration where possible.

27. **What is the impact of monorepo on developer experience?**

    - Answer: Single clone, easy code navigation, atomic changes, but potential complexity with tooling.

28. **How do you handle monorepo in distributed teams?**

    - Answer: Clear ownership, documentation, CODEOWNERS, automated testing, code review guidelines.

29. **What are the alternatives to monorepo?**

    - Answer: Polyrepo, multi-repo, or hybrid approaches with shared packages via npm.

30. **How do you optimize monorepo for large teams?**

    - Answer: Clear package boundaries, ownership, documentation, automated tooling, and communication.

## Summary

Monorepo provides a unified approach to managing multiple projects with shared code and dependencies. Understand the benefits, challenges, and best practices for effective monorepo management.

## References & Learn More

- [Turborepo Documentation](https://turborepo.org/docs)
- [Nx Documentation](https://nx.dev/)
- [pnpm Workspaces](https://pnpm.io/workspaces)
- [Yarn Workspaces](https://classic.yarnpkg.com/en/docs/workspaces)
- [Monorepo by Example](https://monorepo.tools/)
