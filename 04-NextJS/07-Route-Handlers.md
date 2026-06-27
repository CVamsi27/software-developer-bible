# Route Handlers in Next.js

## Definition

**Route Handlers** are the App Router equivalent of API Routes in the Pages Router. They allow you to create API endpoints within the `app/` directory, handling HTTP requests with full access to Web APIs like Request and Response objects.

## Why Do We Need It?

1. **API endpoints** — Serve data to clients, webhooks, and external services
2. **Backend logic** — Handle authentication, validation, and business logic
3. **Third-party integration** — Process webhooks and external API calls
4. **File handling** — Upload/download files
5. **Edge computing** — Run API logic at the edge

## How It Works

### Route Handler Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROUTE HANDLER FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HTTP Request                                                   │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  URL Matching                                            │   │
│  │  /api/users → app/api/users/route.ts                    │   │
│  │  /api/users/123 → app/api/users/[id]/route.ts           │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Method Routing                                          │   │
│  │  export async function GET(request) { ... }              │   │
│  │  export async function POST(request) { ... }             │   │
│  │  export async function PUT(request) { ... }              │   │
│  │  export async function DELETE(request) { ... }           │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Response                                                │   │
│  │  return Response.json(data)                              │   │
│  │  return NextResponse.json(data, { status: 200 })         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Route Handler vs API Route (Pages Router)

```
┌─────────────────────────────────────────────────────────────────┐
│              ROUTE HANDLER vs API ROUTE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Route Handler (App Router):                                    │
│  ├─ File: app/api/users/route.ts                               │
│  ├─ Web standard APIs (Request/Response)                        │
│  ├─ Edge Runtime support                                        │
│  ├─ Streaming support                                           │
│  └─ Next.js 13+ only                                            │
│                                                                 │
│  API Route (Pages Router):                                      │
│  ├─ File: pages/api/users.ts                                   │
│  ├─ Custom req/res objects                                      │
│  ├─ Node.js runtime only                                        │
│  ├─ No streaming                                                │
│  └─ Deprecated in Next.js 13+                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Route Handler

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const users = [
    { id: 1, name: 'John' },
    { id: 2, name: 'Jane' },
  ]

  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()

  const newUser = {
    id: Date.now(),
    name: body.name,
    email: body.email,
  }

  return NextResponse.json(newUser, { status: 201 })
}
```

### Dynamic Route Handler

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  const user = await db.user.findUnique({
    where: { id },
  })

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }

  return NextResponse.json(user)
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const body = await request.json()

  const updatedUser = await db.user.update({
    where: { id },
    data: body,
  })

  return NextResponse.json(updatedUser)
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  await db.user.delete({
    where: { id },
  })

  return NextResponse.json({ success: true })
}
```

### Route Handler with Query Params

```tsx
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const query = searchParams.get('q')
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')

  if (!query) {
    return NextResponse.json(
      { error: 'Query parameter required' },
      { status: 400 }
    )
  }

  const results = await db.post.findMany({
    where: {
      title: { contains: query },
    },
    skip: (page - 1) * limit,
    take: limit,
  })

  return NextResponse.json({
    results,
    page,
    limit,
    total: await db.post.count({
      where: { title: { contains: query } },
    }),
  })
}
```

### Route Handler with Headers

```tsx
// app/api/data/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const apiKey = request.headers.get('x-api-key')

  if (apiKey !== process.env.API_KEY) {
    return NextResponse.json(
      { error: 'Invalid API key' },
      { status: 401 }
    )
  }

  const data = await fetchData()

  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 'public, max-age=3600',
      'X-Custom-Header': 'value',
    },
  })
}
```

### Route Handler with Cookies

```tsx
// app/api/session/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { username, password } = await request.json()

  const user = await authenticate(username, password)

  if (!user) {
    return NextResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    )
  }

  const response = NextResponse.json({ success: true })

  response.cookies.set('session', user.sessionId, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
  })

  return response
}

export async function DELETE(request: NextRequest) {
  const response = NextResponse.json({ success: true })
  response.cookies.delete('session')
  return response
}
```

### Route Handler with Streaming

```tsx
// app/api/stream/route.ts
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify({ count: i })}\n\n`)
        )
        await new Promise(resolve => setTimeout(resolve, 1000))
      }
      controller.close()
    },
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  })
}
```

### Route Handler with Webhooks

```tsx
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(request: NextRequest) {
  const body = await request.text()
  const sig = request.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    return NextResponse.json(
      { error: 'Webhook signature verification failed' },
      { status: 400 }
    )
  }

  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object as Stripe.PaymentIntent
      await handlePaymentSuccess(paymentIntent)
      break
    case 'payment_intent.payment_failed':
      const failedPayment = event.data.object as Stripe.PaymentIntent
      await handlePaymentFailure(failedPayment)
      break
  }

  return NextResponse.json({ received: true })
}
```

### Route Handler with File Upload

```tsx
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { put } from '@vercel/blob'

export async function POST(request: NextRequest) {
  const formData = await request.formData()
  const file = formData.get('file') as File

  if (!file) {
    return NextResponse.json(
      { error: 'No file provided' },
      { status: 400 }
    )
  }

  const blob = await put(file.name, file, {
    access: 'public',
  })

  return NextResponse.json({
    url: blob.url,
    pathname: blob.pathname,
  })
}
```

### Route Handler with Edge Runtime

```tsx
// app/api/edge/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  const geo = request.geo
  const country = geo?.country || 'Unknown'

  return Response.json({
    message: 'Hello from Edge!',
    country,
    timestamp: Date.now(),
  })
}
```

### Route Handler with Revalidation

```tsx
// app/api/revalidate/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { revalidatePath, revalidateTag } from 'next/cache'

export async function POST(request: NextRequest) {
  const { path, tag, secret } = await request.json()

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json(
      { error: 'Invalid secret' },
      { status: 401 }
    )
  }

  if (path) {
    revalidatePath(path)
  }

  if (tag) {
    revalidateTag(tag)
  }

  return NextResponse.json({
    revalidated: true,
    timestamp: Date.now(),
  })
}
```

### Route Handler with Error Handling

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const users = await db.user.findMany()
    return NextResponse.json(users)
  } catch (error) {
    console.error('Failed to fetch users:', error)

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validation
    if (!body.name || !body.email) {
      return NextResponse.json(
        { error: 'Name and email are required' },
        { status: 400 }
      )
    }

    const user = await db.user.create({ data: body })
    return NextResponse.json(user, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Route Handler with Middleware Integration

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add API key validation for all /api routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const apiKey = request.headers.get('x-api-key')

    if (!apiKey || apiKey !== process.env.API_KEY) {
      return NextResponse.json(
        { error: 'Invalid API key' },
        { status: 401 }
      )
    }
  }

  return NextResponse.next()
}
```

### Route Handler with ISR

```tsx
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server'

export const revalidate = 60 // Revalidate every 60 seconds

export async function GET(request: NextRequest) {
  const products = await db.product.findMany()

  return NextResponse.json(products, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate',
    },
  })
}
```

## Real-World Use Cases

| Use Case | Implementation |
|----------|---------------|
| REST API | CRUD operations for resources |
| Authentication | Login/logout/session management |
| Webhooks | Stripe, GitHub, Slack integrations |
| File uploads | Image/document processing |
| Search API | Query processing and filtering |
| Analytics | Event tracking and reporting |
| Email sending | Transactional emails |
| Payment processing | Stripe/PayPal integration |
| External API proxy | CORS handling, rate limiting |
| Real-time updates | SSE/WebSocket endpoints |

## Common Mistakes

### 1. Using Node.js APIs in Edge Runtime

```tsx
// ❌ BAD: Node.js APIs not available in Edge
export const runtime = 'edge'

export async function GET() {
  const fs = require('fs') // Error!
  const data = fs.readFileSync('file.txt')
  return Response.json({ data })
}

// ✅ GOOD: Use Web APIs
export async function GET() {
  const response = await fetch('https://api.example.com/data')
  const data = await response.json()
  return Response.json(data)
}
```

### 2. Not Handling All HTTP Methods

```tsx
// ❌ BAD: Only handling GET
export async function GET() {
  return Response.json({ data: [] })
}
// What about POST, PUT, DELETE?

// ✅ GOOD: Handle all needed methods
export async function GET() {
  return Response.json({ data: [] })
}

export async function POST(request: Request) {
  const body = await request.json()
  return Response.json(body, { status: 201 })
}

export async function PUT(request: Request) {
  const body = await request.json()
  return Response.json(body)
}

export async function DELETE() {
  return Response.json({ success: true })
}
```

### 3. Not Validating Request Body

```tsx
// ❌ BAD: No validation
export async function POST(request: Request) {
  const body = await request.json()
  await db.user.create({ data: body }) // Trusts client data!
  return Response.json({ success: true })
}

// ✅ GOOD: Validate with Zod
import { z } from 'zod'

const userSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
})

export async function POST(request: Request) {
  const body = await request.json()
  const validated = userSchema.parse(body)
  await db.user.create({ data: validated })
  return Response.json({ success: true }, { status: 201 })
}
```

### 4. Not Returning Proper Status Codes

```tsx
// ❌ BAD: Always returning 200
export async function POST(request: Request) {
  try {
    const user = await createUser(request)
    return Response.json(user) // 200 for creation?
  } catch (error) {
    return Response.json({ error: 'Failed' }) // 200 for error?
  }
}

// ✅ GOOD: Proper status codes
export async function POST(request: Request) {
  try {
    const user = await createUser(request)
    return Response.json(user, { status: 201 }) // 201 Created
  } catch (error) {
    return Response.json(
      { error: 'Failed' },
      { status: 500 } // 500 Internal Server Error
    )
  }
}
```

### 5. Not Handling CORS

```tsx
// ❌ BAD: No CORS headers
export async function GET() {
  return Response.json({ data: [] })
  // Browser blocks cross-origin requests!
}

// ✅ GOOD: Handle CORS
export async function GET() {
  return Response.json(
    { data: [] },
    {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    }
  )
}
```

## Best Practices

1. **Use proper HTTP methods** — GET for reading, POST for creating, etc.
2. **Return appropriate status codes** — 200, 201, 400, 401, 404, 500
3. **Validate all inputs** — Use Zod or similar for request validation
4. **Handle errors gracefully** — Try/catch with proper error responses
5. **Use Edge Runtime when possible** — For better performance
6. **Implement rate limiting** — Prevent abuse
7. **Add CORS headers** — For cross-origin requests
8. **Use streaming** — For long-running operations
9. **Cache responses** — Use Cache-Control headers
10. **Document your API** — Clear endpoint documentation

## Performance Considerations

```
Route Handler Performance:
- Edge Runtime: Fast cold starts, limited APIs
- Node.js Runtime: Full API access, slower starts
- Streaming: Progressive response delivery
- Caching: Reduce server load with proper headers

Optimization:
- Use Edge Runtime for simple handlers
- Implement response caching
- Use streaming for slow operations
- Minimize database queries
- Use connection pooling
```

## Interview Questions

### Beginner (5-10)

1. **What are Route Handlers?**
   Route Handlers are API endpoints in the App Router. They handle HTTP requests using Web standard APIs (Request/Response) and can run on Edge or Node.js runtime.

2. **Where do Route Handlers live?**
   In the `app/` directory, typically under `api/`. File name must be `route.ts`.

3. **How do you create a Route Handler?**
   Create a `route.ts` file and export named functions for HTTP methods (GET, POST, PUT, DELETE).

4. **What is the difference between Route Handlers and API Routes?**
   Route Handlers use Web standard APIs, support Edge Runtime, and are in the App Router. API Routes use custom req/res objects and are in Pages Router.

5. **How do you access request body in Route Handlers?**
   Use `await request.json()` for JSON, `await request.formData()` for forms, or `await request.text()` for raw text.

6. **How do you return JSON from Route Handlers?**
   Use `Response.json(data)` or `NextResponse.json(data)` with optional status and headers.

7. **Can Route Handlers run on Edge Runtime?**
   Yes! Add `export const runtime = 'edge'` to use Edge Runtime for faster execution.

8. **How do you handle errors in Route Handlers?**
   Use try/catch blocks and return appropriate HTTP status codes with error messages.

### Intermediate (5-10)

9. **How do you handle authentication in Route Handlers?**
   Check headers for tokens, validate JWTs, verify API keys, or check session cookies.

10. **How do you implement rate limiting?**
    Use in-memory stores or Redis to track requests per IP/client and return 429 when exceeded.

11. **How do you handle file uploads?**
    Use `request.formData()` to access files, process them, and upload to storage services.

12. **How do you implement streaming responses?**
    Return a `ReadableStream` with appropriate Content-Type headers for SSE or chunked responses.

13. **How do you handle CORS?**
    Add CORS headers to responses or use middleware to handle preflight requests.

14. **How do you implement webhook handling?**
    Verify webhook signatures, parse payloads, and process events with proper error handling.

15. **How do you cache Route Handler responses?**
    Use Cache-Control headers or Next.js caching with `revalidate` option.

### Senior (10-15)

16. **Design a RESTful API using Route Handlers.**
    Implement proper HTTP methods, status codes, pagination, filtering, and error handling. Use middleware for authentication and rate limiting.

17. **How would you implement a GraphQL API with Route Handlers?**
    Handle POST requests, parse GraphQL queries, resolve data, and return responses. Use DataLoader for efficient data fetching.

18. **Explain the Route Handler execution model.**
    Request → Middleware → Route Matching → Method Handler → Response. Edge Runtime for fast execution, Node.js for full API access.

19. **How do you implement real-time features with Route Handlers?**
    Use Server-Sent Events (SSE) or WebSocket upgrades for real-time communication.

20. **Design a webhook processing system.**
    Implement signature verification, idempotency handling, retry logic, and event queue processing.

21. **How would you implement API versioning?**
    Use URL-based versioning (/api/v1/, /api/v2/) or header-based versioning with proper routing.

22. **Design a rate limiting system for Route Handlers.**
    Implement token bucket or sliding window algorithms, use Redis for distributed limiting, and handle rate limit headers.

23. **How do you implement request validation middleware?**
    Create reusable validation functions, use Zod schemas, and return structured error responses.

24. **Design an API monitoring system.**
    Track response times, error rates, request volumes, and implement alerting for anomalies.

25. **How would you implement API documentation?**
    Use OpenAPI/Swagger, generate documentation from code, and provide interactive API explorer.

### FAANG-style (5-10)

26. **Design a globally distributed API with Route Handlers.**
    Use edge computing, implement geo-routing, handle data replication, and optimize for latency.

27. **How would you implement a microservices API gateway?**
    Handle service discovery, load balancing, authentication, and request routing across services.

28. **Design an API that handles millions of requests per day.**
    Implement caching, connection pooling, query optimization, and horizontal scaling.

29. **How would you implement API rate limiting at scale?**
    Use distributed rate limiting, implement adaptive limits, and handle rate limit abuse.

30. **Design a system for API versioning and deprecation.**
    Implement version detection, migration tools, deprecation warnings, and backward compatibility.

### Follow-ups (5-10)

31. **What are the limitations of Route Handlers?**
    Edge Runtime limitations, no streaming in some cases, and debugging complexity.

32. **How do Route Handlers affect SEO?**
    API endpoints aren't directly SEO-relevant, but they serve data for SEO-optimized pages.

33. **What is the future of Route Handlers?**
    Better Edge support, improved streaming, and enhanced Developer Experience.

34. **How do you test Route Handlers?**
    Use Jest for unit tests, supertest for integration tests, and Playwright for E2E tests.

35. **What security considerations apply?**
    Input validation, authentication, rate limiting, CORS, and secure headers.

36. **How do Route Handlers interact with caching?**
    They can use HTTP caching, Next.js data cache, and full route cache.

37. **What are alternatives to Route Handlers?**
    Server Actions, external API services, and serverless functions.

38. **How do you monitor Route Handlers in production?**
    Log requests, track metrics, implement alerting, and use APM tools.

## Summary

| Feature | Route Handlers |
|---------|---------------|
| Location | `app/api/*/route.ts` |
| Runtime | Edge or Node.js |
| APIs | Web standard (Request/Response) |
| Methods | GET, POST, PUT, DELETE, etc. |
| Streaming | Yes |
| Edge support | Yes |
| Use case | API endpoints |

## Cheat Sheet

```
File: app/api/[...]/route.ts

Methods:
export async function GET(request: Request) {}
export async function POST(request: Request) {}
export async function PUT(request: Request) {}
export async function DELETE(request: Request) {}

Request:
await request.json()        → JSON body
await request.formData()    → Form data
await request.text()        → Raw text
request.headers             → Headers
request.nextUrl             → URL object
request.geo                 → Geographic info

Response:
Response.json(data)         → JSON response
Response.json(data, { status: 200 })
NextResponse.json(data)     → With Next.js helpers
new Response(stream)        → Streaming response

Config:
export const runtime = 'edge'
export const revalidate = 60
export const dynamic = 'force-dynamic'
```

## References & Learn More

- [Next.js Docs: Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [Route Handler API](https://nextjs.org/docs/app/api-reference/functions/next-response)
- [Web APIs in Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
