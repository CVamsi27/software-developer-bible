[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

# Static Exports in Next.js

## Definition

**Static Exports** (`next export`) is a Next.js feature that generates a fully static version of your application as HTML, CSS, and JS files — with no Node.js server required. The output can be served from any static file server, CDN, or hosting provider (S3, Nginx, GitHub Pages, Netlify). All pages are pre-rendered at build time, and any dynamic features (API routes, server actions, middleware) are either executed at build time or disabled.

## Why Do We Need It?

1. **Zero server cost** — Host on static storage (S3, CDN, GitHub Pages) instead of a Node server
2. **Maximum performance** — Static files served at edge speed with CDN caching
3. **Simplified deployment** — Upload a folder; no server configuration, scaling, or monitoring
4. **Improved security** — No server surface to attack; no environment variables exposed
5. **Great for JAMstack** — Ideal for documentation, marketing sites, blogs, and portfolios

## How It Works

### Build vs Runtime

```text
Static Export Build Process:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                     STATIC EXPORT BUILD                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. next build                                                   │
│     ├── Generate static pages (SSG) at build time               │
│     ├── Execute getStaticProps / generateStaticParams           │
│     ├── Prerender all pages to HTML                             │
│     └── Generate fallback HTML for dynamic routes               │
│                                                                  │
│  2. next export                                                  │
│     ├── Read .next build output                                 │
│     ├── Write static HTML files to /out directory               │
│     ├── Copy static assets (JS, CSS, images)                   │
│     └── Generate 404.html for custom 404 page                  │
│                                                                  │
│  3. Deploy /out folder                                           │
│     ├── Upload to any static host (S3, Nginx, etc.)            │
│     ├── Configure fallback: 404.html → 404                     │
│     └── Configure trailing slash redirects if needed           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

### Features Disabled in Static Export

```text
Static Export Limitations:
═══════════════════════════════════════════════════════════════

❌ DISABLED (will error):
├── API Routes (app/api/*)
├── Server Actions
├── Middleware
├── ISR (revalidate)
├── SSR (getServerSideProps)
├── Dynamic rendering (force-dynamic)
├── next/image default optimizer
├── Rewrites / Redirects (server-side)
├── Headers (server-side)
└── Streaming

✅ AVAILABLE:
├── SSG (getStaticProps / generateStaticParams)
├── Client-side data fetching
├── next/image with unoptimized loader
├── next/link
├── next/router
├── Static assets in /public
├── Custom 404, 500 pages
├── getStaticPaths
└── Client Components

```

## Code Examples

### 1. Basic Static Export Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',  // Enables static export mode

  // Optional: configure export settings
  // distDir: 'build',  // Customize output directory (default: 'out')

  // Disable image optimization (requires server)
  images: {
    unoptimized: true,
  },

  // Optional: ensure trailing slash for static hosting
  trailingSlash: true,

  // Skip middleware (not supported in static export)
  skipMiddlewareUrlNormalize: true,
};

export default nextConfig;
```

```bash
# Build and export
npm run build
# or
npx next build && npx next export

# Output goes to ./out/
ls out/
# 404.html  index.html  _next/  products/
```

### 2. Using generateStaticParams for Dynamic Routes

```typescript
// app/products/[id]/page.tsx
interface ProductPageProps {
  params: Promise<{ id: string }>;
}

// Pre-generate ALL product pages at build time
export async function generateStaticParams() {
  const products = await fetch('https://api.example.com/products')
    .then(r => r.json());

  return products.map((product: { id: string }) => ({
    id: product.id,
  }));
}

// During static export, this runs at BUILD TIME
export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;

  // Data fetching happens at build time
  const product = await fetch(`https://api.example.com/products/${id}`)
    .then(r => r.json());

  return (
    <div>
      <h1>{product.name}</h1>
      <p>Price: ${product.price}</p>
    </div>
  );
}
```

### 3. Static Export with Client-Side Data

```typescript
// app/dashboard/page.tsx — Static shell + client-side data
export const dynamic = 'force-static';

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>This shell is statically generated.</p>

      {/* Client component fetches live data */}
      <DashboardData />
    </div>
  );
}

// app/dashboard/DashboardData.tsx
'use client';

import { useState, useEffect } from 'react';

const DashboardData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // This runs on the client after the static page loads
    fetch('/api/data.json') // Fetch from static JSON file
      .then(r => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;
  return <div>{JSON.stringify(data)}</div>;
};
```

### 4. Custom 404 and Error Pages

```typescript
// app/not-found.tsx — Custom 404 page
// In static export, this generates 404.html
export default function NotFound() {
  return (
    <div style={{ textAlign: 'center', padding: 100 }}>
      <h1>404 — Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <a href="/">Go Home</a>
    </div>
  );
}

// app/error.tsx — Custom error page
'use client';

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div style={{ textAlign: 'center', padding: 100 }}>
      <h1>Something went wrong</h1>
      <button onClick={() => reset()}>Try Again</button>
    </div>
  );
}
```

### 5. Static Export with Images

```typescript
// next.config.ts
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true, // Required for static export
    // OR use a CDN loader:
    // loader: 'cloudinary',
    // path: 'https://res.cloudinary.com/my-cloud/',
  },
};

// Usage — works without optimization
import Image from 'next/image';

export default function StaticPage() {
  return (
    <Image
      src="/images/hero.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority
      // In static export, images are served as-is from /public
    />
  );
}
```

### 6. Static Export with getStaticPaths Fallback

```typescript
// pages/products/[id].tsx — Pages Router
import { GetStaticPaths, GetStaticProps } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {
  const products = await fetch('https://api.example.com/products')
    .then(r => r.json());

  const paths = products.map((p: { id: string }) => ({
    params: { id: p.id },
  }));

  return {
    paths,
    // In static export, ALL paths must be specified at build time
    // fallback: false is required (blocking not supported)
    fallback: false,
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const product = await fetch(
    `https://api.example.com/products/${params!.id}`
  ).then(r => r.json());

  return {
    props: { product },
    // revalidate is NOT supported in static export
  };
};
```

### 7. Static Export with Static JSON Data

```typescript
// Generate static JSON files at build time
// app/api/data/route.ts — This WON'T work in static export

// Instead, generate .json files in /public during build:
// scripts/generate-data.ts
import { writeFileSync } from 'fs';
import path from 'path';

async function generateStaticData() {
  const products = await fetch('https://api.example.com/products')
    .then(r => r.json());

  // Write to /public directory
  writeFileSync(
    path.join(process.cwd(), 'public', 'data', 'products.json'),
    JSON.stringify(products)
  );

  console.log('Generated static data files for export');
}

generateStaticData();

// Then in package.json:
// "build": "tsx scripts/generate-data.ts && next build && next export"
```

### 8. Deployment Configuration

```yaml
# .github/workflows/deploy.yml — Deploy to GitHub Pages
name: Deploy static export to Pages

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./out

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

```nginx
# nginx.conf — Serve static export
server {
    listen 80;
    server_name example.com;
    root /var/www/out;

    # Serve static files
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    # 404 fallback
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
}
```

## Real-World Use Cases

| Use Case | Why Static Export | Hosting |
|----------|------------------|---------|
| **Documentation site** | Full SSG, SEO-friendly, no dynamic data | GitHub Pages, Cloudflare Pages |
| **Marketing site** | Static content, fast load, no server cost | S3 + CloudFront, Netlify |
| **Blog** | All content at build time, RSS feed | GitHub Pages, Vercel (static) |
| **Portfolio** | One-page static, images | Any static host |
| **Knowledge base** | Search can be client-side | S3, Nginx |

## Static Hosting Comparison

| Feature | GitHub Pages | Netlify | S3 + CloudFront | Cloudflare Pages |
|---------|:-----------:|:-------:|:--------------:|:----------------:|
| **Free tier** | ✅ | ✅ | 12-month free | ✅ |
| **Custom domain** | ✅ | ✅ | ✅ | ✅ |
| **HTTPS** | ✅ | ✅ | ✅ | ✅ |
| **CDN** | Fastly | Netlify CDN | CloudFront | Cloudflare |
| **Build integration** | Actions | Git push | Manual | Git push |
| **Redirects** | Limited | _redirects file | CloudFront rules | _redirects file |

## Common Mistakes

### 1. Using Unsupported Features

```typescript
// ❌ BAD: ISR in static export
export const revalidate = 60; // Error during export!

// ❌ BAD: API Routes
// app/api/hello/route.ts — won't work in static export

// ✅ GOOD: Use static generation or client-side fetching
export async function generateStaticParams() { /* ... */ }
// Use client-side fetch for dynamic data
```

### 2. Missing generateStaticParams for Dynamic Routes

```typescript
// ❌ BAD: Dynamic route without generateStaticParams
// app/products/[id]/page.tsx
export default function Page({ params }: { params: { id: string } }) {
  return <div>Product {params.id}</div>;
}
// Error: Dynamic routes need generateStaticParams in static export

// ✅ GOOD: Specify all paths
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }, { id: '3' }];
}
```

### 3. Forgetting to Configure Images

```typescript
// ❌ BAD: Default image optimization (requires server)
// Build will fail with: Image Optimization requires a server

// ✅ GOOD: Disable image optimization
// next.config.ts
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
};
```

## Best Practices

1. **Use `generateStaticParams` for ALL dynamic routes** — Every possible path must be enumerated
2. **Disable image optimization** — Set `images.unoptimized: true` in config
3. **Use client-side fetching for dynamic data** — Fetch JSON from `/data/*.json` or external APIs
4. **Generate static JSON files during build** — Write data to `/public` before export
5. **Set `trailingSlash: true`** — Ensures compatibility with static hosts
6. **Add custom 404 page** — Generates `404.html` for fallback
7. **Test export locally** — Use `npx serve out/` before deploying
8. **Consider incrementally adopting** — Start with static pages, add client-side data as needed

## Summary

- Static exports generate a fully static HTML/CSS/JS build with no server requirements
- API routes, middleware, ISR, server actions, and image optimization are disabled
- All dynamic routes must use `generateStaticParams` with `fallback: false`
- Data fetching happens at build time via `generateStaticParams` or client-side after mount
- Deploy to any static host: GitHub Pages, Netlify, S3, Cloudflare Pages

## Cheat Sheet

```typescript
// next.config.ts
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
};
export default nextConfig;
```

```text
Static Export Key Points:
├── Build: next build → static HTML in /out/
├── Server: NONE — runs on any static host
├── Dynamic routes: MUST use generateStaticParams
├── fallback: false (blocking not supported)
├── Data: Build-time SSG or client-side fetch
├── Images: unoptimized: true
├── API/Middleware/ISR: DISABLED
└── Deploy: GitHub Pages, Netlify, S3, Nginx

Commands:
├── npm run build (if configured)
├── npx next build && npx next export
├── npx serve out/  (test locally)
├── du -sh out/     (check output size)
└── tree out/       (view output structure)
```

---

## See Also

- [Authentication](13-Authentication.md)
- [Caching in Next.js](09-Caching.md)
- [Server Components](03-Server-Components.md)
- [SSR / CSR / SSG / ISR](01-SSR-CSR-SSG-ISR.md)
- [Streaming](10-Streaming.md)

## References & Learn More

- [Next.js Docs: Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [Next.js Docs: Static Export Configuration](https://nextjs.org/docs/app/api-reference/next-config-js/output)
- [Next.js: generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)
- [Vercel: Deploying Static Sites](https://vercel.com/docs/deployments/static-deployments)
