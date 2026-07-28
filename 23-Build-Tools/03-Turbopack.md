---
section: Build Tools
category: DevOps
tags: [concept]
---

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

```text
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

```text
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


## Summary
Turbopack represents the future of frontend bundling, offering unprecedented performance through incremental computation and Rust implementation. While still in development, it shows immense potential for large-scale applications and monorepos. Its integration with Next.js and Turborepo makes it a compelling choice for modern web development.

---

## See Also
- [React](../03-React/)
- [Next.js](../04-NextJS/)
- [Performance Monitoring](../26-Performance-Monitoring/)

## References & Learn More

- [Turbopack Official Documentation](https://turbo.build/pack)
- [Turborepo Documentation](https://turbo.build/repo)
- [Next.js with Turbopack](https://nextjs.org/docs/app/api-reference/next-config-js/turbo)
- [Vercel Blog - Turbopack](https://vercel.com/blog/turbopack)
- [Turbopack GitHub](https://github.com/vercel/turborepo)
