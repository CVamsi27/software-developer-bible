# Turbopack

## Definition
Turbopack is an incremental bundler optimized for JavaScript and TypeScript, built in Rust by Vercel. It's designed as a successor to Webpack, focusing on performance through incremental computation and caching.

## Why Do We Need It?
Traditional bundlers rebuild entire dependency graphs on changes, causing slow development cycles in large applications. Turbopack addresses this by:
- **Incremental Bundling**: Only recomputes what changed
- **Rust Performance**: 10x faster than Webpack, 700x faster than Vite for large apps
- **Incremental Computation**: Remembers work done across sessions
- **Next.js Integration**: Optimized for Next.js applications

## How It Works
Turbopack uses an incremental computation engine that tracks dependencies at a granular level:

### Turbopack Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Turbopack Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  File       │───▶│  Module     │───▶│  Chunk              │  │
│  │  System     │    │  Graph      │    │  Generation         │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│         │                   │                    │               │
│         ▼                   ▼                    ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  Content    │    │  Dependency │    │  Output             │  │
│  │  Addressable│    │  Tracking   │    │  Bundles            │  │
│  │  Cache      │    │             │    │                     │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Incremental Computation
```
Initial Build:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  All Files  │───▶│  Full Build │───▶│  Output     │
│  Processed  │    │  Cache      │    │  Bundles    │
└─────────────┘    └─────────────┘    └─────────────┘

After File Change:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Changed    │───▶│  Incremental│───▶│  Updated    │
│  File Only  │    │  Recompute  │    │  Output     │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Code Examples

### Basic Configuration
```javascript
// turbo.json (Turborepo configuration)
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {
      "dependsOn": ["build"]
    }
  }
}
```

### Next.js with Turbopack
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: {
      // Custom webpack loader alternatives
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
      // Resolve aliases
      resolveAlias: {
        '@': './src',
      },
      // Resolve extensions
      resolveExtensions: [
        '.mdx',
        '.tsx',
        '.ts',
        '.jsx',
        '.js',
        '.json',
      ],
    },
  },
};

module.exports = nextConfig;
```

### Running Turbopack
```bash
# Next.js with Turbopack
npx next dev --turbo

# Turborepo
npx turbo run build

# Watch mode
npx turbo run dev --watch
```

### Package.json Scripts
```json
{
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "turbo:build": "turbo run build",
    "turbo:dev": "turbo run dev",
    "turbo:lint": "turbo run lint"
  },
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
```

### Custom Turborepo Pipeline
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env.*"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["src/**"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "__tests__/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "clean": {
      "cache": false
    }
  }
}
```

### Workspace Configuration
```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
```

## Real-World Use Cases
1. **Large Next.js Applications**: Optimized build times for complex pages
2. **Monorepos**: Efficient builds across multiple packages
3. **Enterprise Applications**: Fast development cycles for large teams
4. **E-commerce Platforms**: Quick iteration on product pages
5. **Content-heavy Sites**: Efficient builds for MDX/markdown content

## Common Mistakes
1. **Assuming Turbopack is production-ready**: Currently in development, not for production yet
2. **Ignoring cache invalidation**: Understanding when Turbopack rebuilds
3. **Not using proper inputs/outputs**: Missing this reduces caching efficiency
4. **Overcomplicating configuration**: Turbopack works well with defaults
5. **Mixing with Webpack**: Don't use both simultaneously
6. **Ignoring Rust dependencies**: Some native modules may have issues

## Best Practices
1. **Use with Next.js**: Turbopack is optimized for Next.js applications
2. **Configure proper inputs/outputs**: Maximize cache hits
3. **Use persistent caching**: Enable across sessions
4. **Monitor build performance**: Use built-in profiling
5. **Keep dependencies updated**: Turbopack evolves rapidly
6. **Use with Turborepo**: For monorepo management
7. **Test thoroughly**: Verify outputs match Webpack

## Performance Considerations
- **Cold Start**: 700x faster than Vite for large apps
- **Incremental Builds**: Only recomputes changed modules
- **Memory Usage**: More efficient than Webpack for large projects
- **Cache Efficiency**: Persistent caching across sessions
- **Rust Performance**: Native code for maximum speed
- **Parallel Processing**: Multi-core utilization

## Interview Questions

### Beginner (5-10)
1. **What is Turbopack and who created it?**
   - Turbopack is an incremental bundler created by Vercel, built in Rust.

2. **How does Turbopack differ from Webpack?**
   - Turbopack uses incremental computation and Rust for 10x faster performance.

3. **What is the primary benefit of Turbopack?**
   - Incremental bundling that only recomputes what changed.

4. **Is Turbopack production-ready?**
   - No, currently in development. Recommended for development only.

5. **How do you enable Turbopack in Next.js?**
   - Run `next dev --turbo` or add `turbo: true` to next.config.js.

6. **What is Turborepo?**
   - A monorepo tool that uses Turbopack for build caching and task orchestration.

7. **What language is Turbopack written in?**
   - Rust, for maximum performance and memory safety.

8. **What is incremental computation?**
   - Technique where only changed parts of computation are redone.

### Intermediate (5-10)
9. **How does Turbopack's caching work?**
   - Filesystem caching stores build artifacts for reuse across sessions.

10. **What is the purpose of `turbo.json`?**
    - Configuration file for Turborepo task pipeline and caching.

11. **How do you configure custom rules in Turbopack?**
    - Use `experimental.turbo.rules` in next.config.js for loader alternatives.

12. **What are the limitations of Turbopack currently?**
    - No production builds yet, limited plugin ecosystem, some features missing.

13. **How does Turbopack handle CSS?**
    - Native CSS support with automatic processing and optimization.

14. **What is the difference between Turbopack and Turborepo?**
    - Turbopack is the bundler, Turborepo is the monorepo build system.

15. **How do you migrate from Webpack to Turbopack?**
    - Currently limited migration path; best for new Next.js projects.

16. **What is persistent caching?**
    - Cache that survives process restarts, stored on filesystem.

### Senior (10-15)
17. **Explain Turbopack's incremental computation engine.**
    - Uses a graph-based approach tracking dependencies at file level.

18. **How does Turbopack achieve 10x faster builds than Webpack?**
    - Rust performance, incremental computation, and efficient caching.

19. **What is the role of Rust in Turbopack's architecture?**
    - Memory safety, zero-cost abstractions, and parallel processing.

20. **How does Turbopack handle large monorepos?**
    - Through Turborepo's task orchestration and shared caching.

21. **What are Turbopack's memory management strategies?**
    - Efficient Rust memory management, incremental computation cleanup.

22. **How does Turbopack compare to Vite's architecture?**
    - Turbopack uses incremental computation, Vite uses native ES modules.

23. **What is the future roadmap for Turbopack?**
    - Production builds, plugin system, broader framework support.

24. **How do you debug Turbopack performance issues?**
    - Use built-in profiling, analyze cache hits, monitor file changes.

### FAANG-style (5-10)
25. **Design a Turbopack configuration for a 100+ package monorepo.**
    - Consider: shared dependencies, incremental builds, cache strategies, task dependencies.

26. **How would you optimize Turbopack for a Next.js application with 500+ pages?**
    - Page-based code splitting, shared chunks, optimized caching.

27. **Explain the technical trade-offs between Turbopack and Webpack.**
    - Performance vs ecosystem maturity, Rust vs JavaScript, incremental vs full rebuilds.

28. **How would you implement a custom plugin for Turbopack?**
    - Currently limited; wait for plugin API or use Webpack alternatives.

29. **Design a migration strategy from Webpack to Turbopack for an enterprise application.**
    - Phased approach, feature parity testing, fallback strategies.

### Follow-ups (5-10)
30. **How does Turbopack handle circular dependencies?**
    - Tracks them at module level, handles appropriately in output.

31. **What happens when Turbopack encounters a JavaScript error?**
    - Stops compilation, provides error details, waits for fixes.

32. **How does Turbopack's performance scale with application size?**
    - Remains efficient due to incremental computation, unlike linear scaling of traditional bundlers.

33. **What is the impact of Turbopack on developer experience?**
    - Faster iteration cycles, reduced wait times, improved productivity.

34. **How does Turbopack handle code splitting?**
    - Automatic code splitting based on dynamic imports and routes.

## Summary
Turbopack represents the future of frontend bundling, offering unprecedented performance through incremental computation and Rust implementation. While still in development, it shows immense potential for large-scale applications and monorepos. Its integration with Next.js and Turborepo makes it a compelling choice for modern web development.

## References & Learn More
- [Turbopack Official Documentation](https://turbo.build/pack)
- [Turborepo Documentation](https://turbo.build/repo)
- [Next.js with Turbopack](https://nextjs.org/docs/app/api-reference/next-config-js/turbo)
- [Vercel Blog - Turbopack](https://vercel.com/blog/turbopack)
- [Turbopack GitHub](https://github.com/vercel/turborepo)