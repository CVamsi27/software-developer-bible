---
section: Serverless & Edge
category: DevOps
tags: [concept, reference]
---

# Vercel Deployments

> **Vercel** is a deployment platform optimized for frontend frameworks (Next.js, SvelteKit, Nuxt, Astro). It provides a global edge network, serverless functions, automatic HTTPS, preview deployments per branch, and Git integration. Vercel pioneered the **Edge Runtime** and **Fluid Compute** model for Jamstack and SSR applications.

## Definition

Vercel is a managed cloud platform that builds, deploys, and serves web applications with zero configuration for supported frameworks. It abstracts CDN, edge functions, serverless compute, image optimization, and CI/CD behind a single Git push.

## Why Do We Need It?

| Problem | Solution |
|---------|----------|
| Manual CI/CD setup | Git-integrated — every push auto-deploys; every PR gets a preview URL |
| Long TTFB from origin servers | Global edge network serves static + cached dynamic content close to the user |
| Image transformation bottlenecks | Built-in `next/image` and `/image` route: WebP/AVIF, CDN-cached |
| Deploying Next.js SSR/ISR to a complex cluster | Native support — `next start` becomes a managed runtime with zero infra |

## How It Works

```text
┌──────────────────────────────────────────────────────────────────┐
│                    VERCEL DEPLOYMENT FLOW                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  git push ──▶ GitHub ──▶ Vercel Build (containerized)           │
│                                  │                               │
│                                  ▼                               │
│                          Build Output:                           │
│                          ├── .next/  (SSR/ISR)                  │
│                          ├── static/                            │
│                          └── api/    (serverless fns)           │
│                                  │                               │
│                                  ▼                               │
│              ┌───────────────────┴───────────────────┐          │
│              ▼                                       ▼          │
│      Edge Network (CDN)                  Compute (Vercel)      │
│      • Static assets                     • Serverless fns     │
│      • Edge Functions (V8)               • Node.js runtime     │
│      • Image Optimization                • Streaming SSR       │
│      • Middleware                        • ISR/On-demand reval │
│              │                                       │          │
│              └───────────────┬───────────────────────┘          │
│                              ▼                                  │
│                         User Request                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Preview Deployments** | Unique URL per branch / PR with build logs and comments bot |
| **Edge Config** | Globally replicated KV store; sub-5ms reads via Vercel Edge Network |
| **Edge Middleware** | Runs *before* a request hits a serverless function (auth, A/B, redirects) |
| **Image Optimization** | On-the-fly WebP/AVIF, resize, format negotiation, CDN-cached |
| **Analytics** | Real Web Vitals (LCP, INP, CLS) from real users, not synthetic |
| **Fluid Compute** | Hybrid model — functions can stream, handle I/O, and avoid cold starts at lower cost |
| **Vercel Cron** | Scheduled serverless invocations via `vercel.json` |

## Code Examples

### 1. Vercel Project Configuration (`vercel.json`)

```json
{
  "version": 2,
  "builds": [
    { "src": "package.json", "use": "@vercel/next" }
  ],
  "crons": [
    { "path": "/api/cron/daily-report", "schedule": "0 5 * * *" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000" }
      ]
    }
  ],
  "redirects": [
    { "source": "/old-blog/:slug", "destination": "/blog/:slug", "statusCode": 308 }
  ]
}
```

### 2. Edge Middleware (Auth + Geolocation)

```typescript
// middleware.ts (Next.js App Router)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value;
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Geo-based routing at the edge
  const country = request.geo?.country ?? 'US';
  const response = NextResponse.next();
  response.headers.set('x-user-country', country);
  return response;
}
```

### 3. Edge Function (Geolocation-Aware API)

```typescript
// app/api/edge/route.ts
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const city = searchParams.get('city') ?? 'world';

  return NextResponse.json({
    message: `Hello, ${city}!`,
    region: request.geo?.region ?? 'unknown',
    country: request.geo?.country ?? 'unknown',
    timestamp: Date.now(),
  });
}
```

### 4. Serverless Function (Node.js Runtime)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { getUsers } from '@/lib/db';

export const runtime = 'nodejs';     // or 'edge' for V8
export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const limit = Number(searchParams.get('limit') ?? '20');

  const users = await getUsers({ limit });
  return NextResponse.json(users);
}
```

### 5. ISR with On-Demand Revalidation

```typescript
// app/blog/[slug]/page.tsx
export const revalidate = 3600; // revalidate every hour

// Trigger on demand from a webhook
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { slug, secret } = await req.json();
  if (secret !== process.env.REVALIDATE_SECRET) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  revalidatePath(`/blog/${slug}`);
  return NextResponse.json({ revalidated: true });
}
```

### 6. Image Optimization

```typescript
import Image from 'next/image';

export function Avatar({ src, alt }: { src: string; alt: string }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={120}
      height={120}
      priority={false}        // lazy by default
      placeholder="blur"       // auto blur-up
      sizes="(max-width: 768px) 100vw, 120px"
    />
  );
}
```

## Real-World Use Cases

1. **Marketing site** — Next.js + ISR + image optimization; sub-100ms TTFB globally.
2. **SaaS dashboard** — Mixed SSR + client components; auth via Edge Middleware; protected APIs via `nodejs` runtime.
3. **A/B testing** — Edge Middleware reads Edge Config feature flags, rewrites to variant routes.
4. **Per-user personalization at the edge** — Geo-headers, cookie-based segmentation, locale routing.
5. **Webhooks** — `/api/*` serverless functions handle Stripe / GitHub / Slack events with zero ops.
6. **Scheduled jobs** — Vercel Cron → API route for daily reports, cleanup, billing cycles.
7. **Preview environments for design review** — Every PR gets a stable URL; designers and PMs click into the running app.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `edge` runtime for Node-specific APIs (fs, child_process) | Switch to `runtime = 'nodejs'` for that route |
| Forgetting ISR / cache semantics for sensitive data | Mark route `dynamic = 'force-dynamic'` or use `revalidate = 0` |
| Secrets in `NEXT_PUBLIC_*` env vars | Only public keys should be `NEXT_PUBLIC_*`; secrets stay server-side |
| Hardcoding region assumption in Edge Middleware | Use `request.geo` (provided by Vercel/Cloudflare) for region-aware logic |
| No structured logging / observability | Use `@vercel/analytics`, Axiom, or Datadog for serverless log aggregation |
| Large `node_modules` in serverless bundle | Mark deps as `external` in `serverComponentsExternalPackages` for tree-shaking |

## Best Practices

1. **Use the right runtime per route** — Edge for latency-sensitive, auth, and small payloads. Node for heavy compute, DB drivers, file system.
2. **Co-locate data with compute** — If you must use a regional DB, set the function's region (`regions: ['iad1']`) to colocate.
3. **Cache aggressively, revalidate precisely** — Use ISR + on-demand revalidation for content that changes infrequently.
4. **Lock down Edge Middleware** — It runs on every matched request; keep it fast and don't do expensive synchronous work.
5. **Use Edge Config for global flags** — Sub-5ms reads; ideal for feature flags, kill switches, and A/B variants.
6. **Preview deployments as review environments** — Wire the bot into Slack/Linear so reviewers see the running app.
7. **Set explicit `maxDuration`** — Vercel has a 300s default on Pro; set a per-route ceiling to prevent runaway billing.

## Performance Considerations

```text
RUNTIME COMPARISON:
┌──────────────────────────────────────────────────────────────────┐
│                  │ Edge Runtime     │ Node.js Runtime            │
├──────────────────┼──────────────────┼───────────────────────────┤
│ Cold start       │ < 5ms (V8)       │ 100-500ms (V8 + node)     │
│ APIs available   │ Web Standard    │ Full Node.js + native     │
│ Max duration     │ 25s (Hobby)      │ 300s (Pro)                │
│ Bundle limit     │ 1 MB             │ 250 MB                    │
│ Best for         │ Middleware, auth │ DB calls, ML inference    │
│                  │ A/B, redirects   │ Long compute, file system │
└──────────────────────────────────────────────────────────────────┘

COST MODEL (per 1M invocations, US):
  • Edge Function:        $2.00
  • Serverless Function:  $0.40
  • ISR reads (cached):   free at edge, $0.40/GB at origin
  • Image Optimization:   $5.00 per 1000 optimized images (Hobby free)
```

## Summary

- Vercel provides serverless deployment for frontend frameworks with automatic HTTPS and CDN distribution
- Edge Functions run at the network edge for sub-50ms response times using the V8 runtime
- Serverless Functions (Node.js, Python, Go, Ruby) auto-scale and support region selection for data locality
- Preview deployments for every git branch enable instant collaboration and review environments
- Edge Middleware runs before request handling for auth, A/B routing, and geolocation-aware rewrites
- ISR with on-demand revalidation balances freshness and performance for content-heavy sites

---

## Cheat Sheet

```text
VERCEL DEPLOYMENTS CHEAT SHEET
═══════════════════════════════════════════════════════════════

RUNTIMES:
  • nodejs  — full Node.js API, slower cold start, longer tasks
  • edge    — V8 only, Web Standard APIs, sub-5ms cold start
  • fluid   — Node + I/O concurrency, low cold-start cost

COMMON APIs:
  • request.geo.country / region / city
  • request.cookies / headers
  • Edge Config (sub-5ms global KV)
  • request.ip (Pro/Enterprise)

INTERVIEW TIPS:
  - Distinguish Edge (V8) from Lambda (Node) — when each wins
  - Explain ISR + on-demand revalidation for content sites
  - Mention region pinning to colocate with RDS / ElastiCache
  - Cover the cost / performance trade-off of preview deploys
```

---

## See Also

- [AWS Lambda](05-AWS-Lambda.md)
- [Docker](../13-Docker/)
- [Edge Functions](02-Edge-Functions.md)
- [Next.js](../04-NextJS/)
- [Observability](../22-Observability/)


## References & Learn More

- [Edge Middleware](https://vercel.com/docs/functions/edge-middleware)
- [Edge Runtime](https://vercel.com/docs/functions/edge-functions)
- [Fluid Compute](https://vercel.com/docs/functions/fluid-compute)
- [On-Demand ISR](https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-on-demand)
- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Pricing](https://vercel.com/docs/pricing)
