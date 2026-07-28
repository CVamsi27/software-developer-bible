# Edge Functions

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

 a network, close to end users, rather than in a centralized data center. They execute on CDN nodes (Points of Presence) to reduce latency and improve performance for user-facing operations.

## Why Do We Need It?

- **Reduced Latency**: Execute code physically closer to users
- **Better Performance**: Faster response times for dynamic content
- **Global Distribution**: Code runs in multiple regions simultaneously
- **Real-time Processing**: Handle requests at the network edge
- **Cost Efficiency**: Reduce origin server load

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
│  • Only misses go to origin server                                 │
└─────────────────────────────────────────────────────────────────────┘

```

## Cloudflare Workers

### Worker Execution Model

```text
Cloudflare Worker Lifecycle:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Fetch   │ ──▶ │  Parse   │ ──▶ │ Execute  │ ──▶ │ Response │ │
│  │  Event   │    │  Request │    │  Handler │    │          │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                 │
│  Isolate Model:                                                 │
│  • Each Worker runs in isolated V8 isolate                     │
│  • No shared memory between Workers                            │
│  • Cold start < 5ms (V8 isolates)                              │
│  • CPU time limit: 10ms (free), 30s (paid)                     │
│  • Memory limit: 128MB                                         │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Basic Cloudflare Worker

```typescript
// worker.ts
interface Env {
  API_KEY: string;
  DATABASE_URL: string;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    const url = new URL(request.url);

    // Handle different routes
    if (url.pathname === '/api/hello') {
      return new Response(
        JSON.stringify({ message: 'Hello from the edge!' }),
        {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        }
      );
    }

    if (url.pathname === '/api/echo') {
      const body = await request.text();
      return new Response(body, {
        headers: { 'Content-Type': 'text/plain' },
      });
    }

    // Proxy to origin with edge caching
    const response = await fetch(request);
    const newResponse = new Response(response.body, response);

    // Add custom headers
    newResponse.headers.set('X-Edge-Location', request.cf?.colo || 'unknown');

    return newResponse;
  },
};

```

### 2. Vercel Edge Function

```typescript
// api/edge-hello.ts
import { NextRequest, NextResponse } from 'next/server';

export const config = {
  runtime: 'edge',
};

export default async function handler(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get('name') || 'World';

  // Edge-compatible operations
  const response = {
    message: `Hello, ${name}!`,
    timestamp: Date.now(),
    region: request.geo?.country || 'unknown',
  };

  return NextResponse.json(response);
}

```

### 3. Edge Middleware (Next.js)

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Run at the edge before page rendering

  // 1. Authentication check
  const token = request.cookies.get('auth-token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. A/B Testing
  const bucket = Math.random() < 0.5 ? 'control' : 'variant';
  const response = NextResponse.next();
  response.cookies.set('ab-test', bucket);

  // 3. Geolocation-based routing
  const country = request.geo?.country;
  if (country === 'DE') {
    response.headers.set('X-Language', 'de');
  }

  // 4. Rate limiting (basic)
  const ip = request.ip;
  // In production, use KV store for rate limiting

  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};

```

### 4. Edge with KV Storage

```typescript
// Cloudflare Worker with KV
interface Env {
  CACHE_KV: KVNamespace;
  API_SECRET: string;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    const cacheKey = new URL(request.url).pathname;

    // Check cache first
    const cached = await env.CACHE_KV.get(cacheKey, 'json');
    if (cached) {
      return new Response(JSON.stringify(cached), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Fetch from origin
    const response = await fetch(`https://api.origin.com${cacheKey}`, {
      headers: { Authorization: `Bearer ${env.API_SECRET}` },
    });

    const data = await response.json();

    // Cache in KV (with TTL)
    ctx.waitUntil(
      env.CACHE_KV.put(cacheKey, JSON.stringify(data), {
        expirationTtl: 3600, // 1 hour
      })
    );

    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
    });
  },
};

```

### 5. Edge Authentication

```typescript
// Edge JWT verification
import { verify } from '@tsndr/cloudflare-worker-jwt';

interface Env {
  JWT_SECRET: string;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    const authHeader = request.headers.get('Authorization');

    if (!authHeader?.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }

    const token = authHeader.substring(7);

    try {
      const isValid = await verify(token, env.JWT_SECRET);

      if (!isValid) {
        return new Response('Invalid token', { status: 401 });
      }

      // Token is valid, proceed
      return fetch(request);
    } catch (error) {
      return new Response('Token verification failed', { status: 401 });
    }
  },
};

```

### 6. Edge Image Optimization

```typescript
// Cloudflare Worker for image optimization
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    // Parse image parameters
    const width = parseInt(url.searchParams.get('w') || '800');
    const quality = parseInt(url.searchParams.get('q') || '80');
    const format = url.searchParams.get('f') || 'auto';

    // Fetch original image
    const response = await fetch(request);

    // Use Cloudflare Image Resizing
    const resizedResponse = new Response(response.body, {
      headers: {
        ...Object.fromEntries(response.headers),
        'cf-resized-json': JSON.stringify({ width, quality, format }),
      },
    });

    return resizedResponse;
  },
};

```

## Real-World Use Cases

### A/B Testing at the Edge

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

### API Gateway with Edge Authentication

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

1. **Using Node.js APIs**: Edge runtimes have limited Node.js API support

2. **Heavy computation**: Edge functions have CPU time limits

3. **Large dependencies**: Bundle size affects cold start time

4. **State assumptions**: Each request is stateless

5. **Ignoring limits**: CPU time, memory, and subrequest limits

## Best Practices

1. **Keep functions small**: Focus on edge-appropriate tasks

2. **Use streaming**: For better performance with large responses

3. **Leverage caching**: Use KV/Durable Objects for state

4. **Handle errors gracefully**: Edge functions can fail

5. **Monitor performance**: Track latency and error rates

## Performance Considerations

```text
Edge vs Serverless Comparison:
┌─────────────────────────────────────────────────────────────────┐
│                      │ Edge Functions    │ Serverless (Lambda)  │
├──────────────────────┼───────────────────┼──────────────────────┤
│ Cold Start           │ < 5ms             │ 100ms - 2s           │
│ Execution Location   │ CDN edge          │ Single region        │
│ CPU Time Limit       │ 10ms - 30s        │ 15 minutes           │
│ Memory Limit         │ 128MB             │ 10GB                 │
│ Use Case             │ Latency-sensitive │ Heavy computation    │
│ Best For             │ Auth, routing     │ Data processing      │
│ State Management     │ KV, Durable Obj   │ External DB          │
└─────────────────────────────────────────────────────────────────┘

```

## Summary

Edge functions provide a powerful way to reduce latency and improve performance by executing code at CDN edge locations. They are ideal for latency-sensitive tasks but have computational limitations compared to traditional serverless functions.

---

## Cheat Sheet
```text
EDGE FUNCTIONS CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  Cloudflare Worker Lifecycle:
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
  │  │  Fetch   │ ──▶ │  Parse   │ ──▶ │ Execute  │ ──▶ │ Response │ │
  │  │  Event   │    │  Request │    │  Handler │    │          │ │
```
```
  import { NextRequest, NextResponse } from 'next/server';
  export const config = {
    runtime: 'edge',
  };
  export default async function handler(request: NextRequest) {
    const { searchParams } = new URL(request.url);
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [Docker](../13-Docker/)
- [Next.js](../04-NextJS/)
- [Observability](../22-Observability/)

## References & Learn More

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Edge Computing Fundamentals](https://web.dev/articles/edge-computing)
- [Cloudflare KV](https://developers.cloudflare.com/workers/learning/how-kv-works/)
- [Durable Objects](https://developers.cloudflare.com/durable-objects/)
