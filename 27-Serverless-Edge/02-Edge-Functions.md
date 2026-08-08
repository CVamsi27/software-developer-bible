---
section: Serverless & Edge
category: DevOps
tags: [concept, reference]
---

# Edge Functions

> Edge functions are serverless functions that run at the edge of a network, close to end users, rather than in a centralized data center. They execute on CDN Points of Presence (PoPs) to reduce latency and improve performance for user-facing operations.

## Definition

An edge function is a serverless compute unit that runs in a CDN edge location (Point of Presence) rather than a centralized cloud region. Most edge runtimes use V8 isolates rather than full containers, giving sub-5ms cold starts but limited APIs and short CPU budgets.

## Why It Matters (TL;DR)

- **Reduced latency** — code runs physically close to users
- **Better performance** — no origin round-trip for personalization, auth, or routing
- **Global distribution** — code runs in 200+ locations simultaneously
- **Real-time processing** — handle requests at the network edge
- **Cost efficiency** — reduce origin server load

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    EDGE FUNCTION ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐     ┌───────────────────────────────────────────┐   │
│  │  User    │ ──▶ │              CDN Edge Network              │   │
│  │ Request  │     │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │   │
│  └──────────┘     │  │ Edge    │ │ Edge    │ │ Edge    │     │   │
│                   │  │ (US)    │ │ (EU)    │ │ (Asia)  │     │   │
│                   │  └────┬────┘ └────┬────┘ └────┬────┘     │   │
│                   │       │           │           │           │   │
│                   └───────┼───────────┼───────────┼───────────┘   │
│                           │           │           │                 │
│                           ▼           ▼           ▼                 │
│                   ┌─────────────────────────────────────────┐     │
│                   │         Origin Server (if needed)       │     │
│                   └─────────────────────────────────────────┘     │
│                                                                     │
│  Edge Function Execution:                                          │
│  • Request hits nearest CDN edge                                   │
│  • Edge function executes (no round-trip to origin)                │
│  • Response cached or passed through                               │
│  • Only cache misses go to origin server                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Edge Runtimes: Cloudflare Workers vs Vercel Edge vs Lambda@Edge

| Feature | Cloudflare Workers | Vercel Edge | Lambda@Edge |
|---------|-------------------|-------------|-------------|
| Runtime | V8 isolates | V8 isolates | Node.js / Python in sandboxed container |
| Cold start | < 5 ms | < 5 ms | 50–200 ms |
| CPU time | 10 ms (free) / 30 s (paid) | 25 s | 5 s (viewer) / 30 s (origin) |
| Memory | 128 MB | 256 MB (configurable) | 128–3,008 MB |
| State | KV, Durable Objects, D1 | Edge Config, in-memory | None persistent |
| Web Standard APIs | Full | Full | Partial |
| Node.js APIs | None (use `node:` polyfills) | None | Yes |
| Best for | High-QPS auth, A/B, geolocation | Next.js middleware, personalization | CloudFront request/response modification |

## Code Examples

### 1. Cloudflare Worker (Basic)

```typescript
// worker.ts
interface Env {
  API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/api/hello') {
      return Response.json({ message: 'Hello from the edge!' });
    }

    // Proxy to origin with edge caching
    const cache = caches.default;
    const cached = await cache.match(request);
    if (cached) return cached;

    const response = await fetch(request);
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('X-Edge-Location', request.cf?.colo ?? 'unknown');
    ctx.waitUntil(cache.put(request, newResponse.clone()));
    return newResponse;
  },
};
```

### 2. Vercel Edge Function (Next.js App Router)

```typescript
// app/api/edge/route.ts
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';
export const preferredRegion = ['iad1', 'fra1']; // optional region pinning

export async function GET(request: NextRequest) {
  return NextResponse.json({
    message: 'Hello from the edge',
    region: request.geo?.region ?? 'unknown',
    country: request.geo?.country ?? 'unknown',
  });
}
```

### 3. Next.js Edge Middleware (Auth, A/B, Geo)

```typescript
// middleware.ts
import { NextResponse, type NextRequest } from 'next/server';

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};

export function middleware(request: NextRequest) {
  // 1. Auth check
  const token = request.cookies.get('session')?.value;
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. A/B test bucketing (sticky via cookie)
  let bucket = request.cookies.get('ab-bucket')?.value;
  if (!bucket) {
    bucket = Math.random() < 0.5 ? 'control' : 'variant';
  }
  const response = NextResponse.next();
  response.cookies.set('ab-bucket', bucket, { maxAge: 60 * 60 * 24 * 30 });

  // 3. Geolocation-based headers
  const country = request.geo?.country;
  if (country === 'DE') response.headers.set('X-Language', 'de');

  return response;
}
```

### 4. Cloudflare Worker with KV Caching

```typescript
interface Env {
  CACHE_KV: KVNamespace;
  API_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const key = new URL(request.url).pathname;

    const cached = await env.CACHE_KV.get(key, 'json');
    if (cached) return Response.json(cached);

    const upstream = await fetch(`https://api.origin.com${key}`, {
      headers: { Authorization: `Bearer ${env.API_SECRET}` },
    });
    const data = await upstream.json();

    // Edge-cache with TTL — survives across requests
    ctx.waitUntil(
      env.CACHE_KV.put(key, JSON.stringify(data), { expirationTtl: 3600 })
    );

    return Response.json(data, { headers: { 'Cache-Control': 'public, max-age=60' } });
  },
};
```

### 5. Edge JWT Verification (Sub-50ms Auth)

```typescript
import { verify } from '@tsndr/cloudflare-worker-jwt';

interface Env {
  JWT_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const auth = request.headers.get('Authorization');
    if (!auth?.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }
    const token = auth.substring(7);

    try {
      const isValid = await verify(token, env.JWT_SECRET);
      if (!isValid) return new Response('Invalid token', { status: 401 });
      return fetch(request); // pass through
    } catch {
      return new Response('Token verification failed', { status: 401 });
    }
  },
};
```

### 6. Durable Objects (Stateful Edge Compute)

```typescript
// Counter Durable Object — a single instance per room
export class Counter {
  state: DurableObjectState;
  count: number = 0;

  constructor(state: DurableObjectState) {
    this.state = state;
    this.state.blockConcurrencyWhile(async () => {
      this.count = (await this.state.storage.get<number>('count')) ?? 0;
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === '/increment') {
      this.count++;
      await this.state.storage.put('count', this.count);
    }
    return new Response(JSON.stringify({ count: this.count }), {
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
```

## Real-World Use Cases

### 1. A/B Testing at the Edge

```text
Use Case: Personalized content delivery
┌─────────────────────────────────────────────────────────────────┐
│  User Request → Edge Function → Check User Segment → Serve     │
│                                 ┌─────────────────┐            │
│                                 │ Control Group   │ → Version A│
│                                 │ Variant A       │ → Version B│
│                                 │ Variant B       │ → Version C│
│                                 └─────────────────┘            │
│                                                                 │
│  Benefits:                                                      │
│  • No origin server load for personalization                    │
│  • Instant response (no round-trip)                             │
│  • Consistent experience (same user gets same variant)          │
└─────────────────────────────────────────────────────────────────┘
```

### 2. API Gateway with Edge Authentication

```text
Use Case: Centralized auth at the edge
┌─────────────────────────────────────────────────────────────────┐
│  Client → Edge Function (Auth) → Origin API → Response         │
│               │                                                  │
│               ├─ Verify JWT                                      │
│               ├─ Check permissions                               │
│               ├─ Rate limiting                                   │
│               └─ Request transformation                          │
│                                                                 │
│  Benefits:                                                      │
│  • Reduced origin load                                          │
│  • Consistent auth logic                                        │
│  • Lower latency for auth checks                                │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using Node.js APIs (`fs`, `child_process`) in edge runtime | Use Web Standard APIs (Fetch, Streams, URL) or pin runtime to `nodejs` |
| Heavy computation (image processing, ML) at the edge | Move to Lambda or Cloud Run; edge has 10ms–30s CPU budget |
| Large dependencies bundled (100KB+ on first load) | Use tree-shakeable libs, dynamic imports, or split into multiple smaller workers |
| Assuming state between invocations | Edge is stateless; use KV / Durable Objects / Edge Config |
| Ignoring subrequest limits (Cloudflare: 50/req free, 1000 paid) | Batch upstream calls, cache aggressively |

## Best Practices

1. **Keep functions small and edge-appropriate** — auth, A/B, redirects, geolocation, header manipulation
2. **Use streaming** — `ReadableStream` responses for large payloads
3. **Leverage caching** — `Cache-Control` + KV / Edge Config for state
4. **Handle errors gracefully** — edge failures fall back to origin or 5xx; design the fallback
5. **Monitor performance** — track TTFB, origin requests avoided (cache hit ratio)
6. **Respect subrequest and CPU limits** — design for the worst-case budget
7. **Use Durable Objects for stateful edge logic** — coordination, locks, real-time counters

## Performance Considerations

```text
Edge vs Serverless Comparison:
┌──────────────────────┬───────────────────┬──────────────────────┐
│                      │ Edge Functions    │ Serverless (Lambda)  │
├──────────────────────┼───────────────────┼──────────────────────┤
│ Cold Start           │ < 5 ms            │ 100 ms – 2 s         │
│ Execution Location   │ CDN edge PoP      │ Single region        │
│ CPU Time Limit       │ 10 ms – 30 s      │ 15 minutes           │
│ Memory Limit         │ 128 – 256 MB      │ 10 GB                │
│ Node.js APIs         │ None              │ Full                 │
│ Best for             │ Latency-sensitive │ Heavy computation    │
│                      │ Auth, routing     │ Data processing      │
│ State Management     │ KV, DO, Edge Config│ External DB         │
│ Subrequest Limit     │ 50–1000           │ Unlimited            │
└──────────────────────┴───────────────────┴──────────────────────┘
```

## Summary

- Edge functions run in CDN PoPs close to users, cutting latency for auth, routing, and personalization
- Cloudflare Workers, Vercel Edge, and Lambda@Edge differ in runtime (V8 vs Node), CPU budget, and state options
- Sub-5ms cold starts come from V8 isolates; the trade-off is limited APIs and small CPU/memory budgets
- Use edge for: auth verification, A/B routing, geolocation, header transformation, KV-backed personalization
- Use serverless/containers for: heavy compute, large dependencies, Node.js-specific APIs, stateful work

---

## Cheat Sheet

```text
EDGE FUNCTIONS CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHEN TO USE EDGE:
  • Latency-critical auth / personalization
  • A/B testing, geo-redirects, header manipulation
  • Caching layer in front of origin
  • Sub-50ms p99 requirement

WHEN TO AVOID EDGE:
  • Heavy compute (image processing, ML)
  • Node.js-specific APIs (fs, child_process)
  • Long-running jobs (>30s)
  • Large dependency bundles

STATE STORAGE:
  • Cloudflare: KV, Durable Objects, D1
  • Vercel:    Edge Config (read-only KV)
  • Lambda@Edge: none (use DynamoDB / ElastiCache)

INTERVIEW ANSWER:
  1. Edge = V8 isolate at CDN PoP, sub-5ms cold start
  2. Trade-off: limited CPU/memory vs proximity to user
  3. Best for auth, A/B, personalization — not heavy compute
  4. Real example: Vercel middleware doing geo-redirects in <30ms
```

---

## See Also

- [AWS Lambda](05-AWS-Lambda.md)
- [Docker](../13-Docker/)
- [Next.js](../04-NextJS/)
- [Observability](../22-Observability/)
- [Serverless Overview](01-Serverless-Overview.md)
- [Vercel Deployments](06-Vercel-Deployments.md)


## References & Learn More

- [Cloudflare KV](https://developers.cloudflare.com/workers/learning/how-kv-works/)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Durable Objects](https://developers.cloudflare.com/durable-objects/)
- [Edge Computing Fundamentals (web.dev)](https://web.dev/articles/edge-computing)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Workers V8 Isolates](https://developers.cloudflare.com/workers/reference/how-workers-works/)
