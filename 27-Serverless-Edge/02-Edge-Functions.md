# Edge Functions

## Definition
Edge functions are serverless functions that run at the edge of a network, close to end users, rather than in a centralized data center. They execute on CDN nodes (Points of Presence) to reduce latency and improve performance for user-facing operations.

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

## Interview Questions

### Beginner (5)

1. **What are edge functions?**

   - Answer: Serverless functions that run at CDN edge locations, close to users, reducing latency for dynamic content processing.

2. **What is Cloudflare Workers?**

   - Answer: A serverless execution environment that allows you to run JavaScript at Cloudflare's edge network.

3. **What is the difference between edge and serverless?**

   - Answer: Edge functions run at multiple CDN locations globally; serverless functions run in a single region.

4. **When should you use edge functions?**

   - Answer: For latency-sensitive tasks like authentication, routing, A/B testing, and personalization.

5. **What is Vercel Edge Middleware?**

   - Answer: Code that runs at the edge before page rendering, used for redirects, rewrites, and headers.

### Intermediate (5)

6. **How do edge functions handle cold starts?**

   - Answer: Edge functions use V8 isolates with cold starts under 5ms, much faster than traditional serverless.

7. **What are the limitations of edge functions?**

   - Answer: CPU time limits (10ms-30s), memory limits (128MB), limited Node.js API support, stateless execution.

8. **How do you store state at the edge?**

   - Answer: Use Cloudflare KV for key-value storage, Durable Objects for stateful coordination, or external databases.

9. **What is the execution model for Cloudflare Workers?**

   - Answer: Each request runs in an isolated V8 isolate, with no shared memory between requests.

10. **How do you handle errors in edge functions?**

    - Answer: Implement try-catch, use error boundaries, provide fallback responses, monitor with logging.

### Senior (10)
11. **Design a real-time personalization system using edge functions**

    - Answer: Use edge for user segmentation, KV for segment storage, Durable Objects for session state, and streaming for dynamic content.

12. **How do you implement rate limiting at the edge?**

    - Answer: Use KV to store request counts with TTL, implement sliding window algorithm, handle concurrent requests.

13. **What is the relationship between edge and CDN?**

    - Answer: Edge functions execute on CDN nodes, leveraging the same global distribution but adding compute capability.

14. **How do you debug edge functions in production?**

    - Answer: Use structured logging, implement request tracing, leverage provider debugging tools, test with wrangler.

15. **Explain the trade-offs of edge computing**

    - Answer: Lower latency vs limited compute, global distribution vs consistency challenges, reduced origin load vs complexity.

16. **How do you handle authentication at the edge?**

    - Answer: Verify JWTs at the edge, use KV for token blacklists, implement refresh token rotation.

17. **What are Durable Objects?**

    - Answer: Cloudflare's stateful primitives that provide single-instance coordination for edge applications.

18. **How do you optimize edge function performance?**

    - Answer: Minimize dependencies, use streaming responses, leverage caching, avoid heavy computation.

19. **How do you test edge functions locally?**

    - Answer: Use Wrangler for local development, Miniflare for testing, mock edge runtime APIs.

20. **What is the difference between edge middleware and edge functions?**

    - Answer: Middleware runs before request handling (routing, auth); functions handle specific endpoints.

### FAANG-style (5)
21. **Design a global API gateway using edge functions**

    - Answer: Edge for routing/auth, Durable Objects for session management, KV for configuration, origin for heavy computation.

22. **How would you implement A/B testing at scale with edge functions?**

    - Answer: Use consistent hashing for user assignment, KV for experiment configuration, Durable Objects for metrics aggregation.

23. **Explain edge computing for real-time applications**

    - Answer: Use edge for WebSocket handling, Durable Objects for room coordination, streaming for real-time updates.

24. **How do you handle data consistency in edge applications?**

    - Answer: Use eventual consistency with KV, Durable Objects for strong consistency, CRDTs for conflict resolution.

25. **Design a serverless edge architecture for e-commerce**

    - Answer: Edge for personalization/pricing, origin for inventory/payment, KV for product data, Durable Objects for cart state.

### Follow-ups (5)
26. **How do you migrate from serverless to edge?**

    - Answer: Identify edge-appropriate workloads, refactor for edge constraints, implement gradually, test thoroughly.

27. **What is the impact of edge computing on SEO?**

    - Answer: Faster page loads improve SEO, edge rendering can improve Core Web Vitals, dynamic rendering for bots.

28. **How do you handle security at the edge?**

    - Answer: WAF integration, DDoS protection, rate limiting, input validation, secure headers.

29. **What are the cost considerations for edge functions?**

    - Answer: Request-based pricing, CPU time billing, compare with origin costs, optimize for cost efficiency.

30. **How do you monitor edge function performance?**

    - Answer: Use provider analytics, implement custom metrics, track latency percentiles, monitor error rates.

## Summary

Edge functions provide a powerful way to reduce latency and improve performance by executing code at CDN edge locations. They are ideal for latency-sensitive tasks but have computational limitations compared to traditional serverless functions.

## References & Learn More

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Edge Computing Fundamentals](https://web.dev/edge-computing/)
- [Cloudflare KV](https://developers.cloudflare.com/workers/learning/how-kv-works/)
- [Durable Objects](https://developers.cloudflare.com/durable-objects/)
