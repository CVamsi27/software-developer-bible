# Middleware in Next.js

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

## Definition

**Middleware** in Next.js is code that runs **before** a request is completed. It executes on the Edge Runtime, allowing you to modify the request/response, redirect, rewrite URLs, set headers, and implement authentication — all before the page renders.

## Why Do We Need It?

1. **Authentication** — Protect routes without per-page auth checks

2. **Redirects** — URL-based redirects without page-level logic

3. **A/B Testing** — Route users to different variants

4. **Geographic routing** — Serve different content by location

5. **Headers/Cookies** — Modify request before it reaches the page

6. **Bot detection** — Serve different content to bots vs users

## How It Works

### Middleware Execution Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                    MIDDLEWARE EXECUTION FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Browser Request                                                │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Edge Runtime                                            │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  1. Match URL against matcher config              │  │   │
│  │  │  2. Execute middleware function                    │  │   │
│  │  │  3. Modify request/response                       │  │   │
│  │  │  4. Return NextResponse or Response               │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Next.js Server                                         │   │
│  │  ┌───────────────────────────────────────────────────┐  │   │
│  │  │  - Route matching                                 │  │   │
│  │  │  - Server/Client Components                       │  │   │
│  │  │  - Data fetching                                  │  │   │
│  │  └───────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  Browser Response                                                │
└─────────────────────────────────────────────────────────────────┘

```

### Middleware vs API Routes vs Server Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                   WHEN TO USE EACH                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Middleware:                                                     │
│  ├─ Runs BEFORE page rendering                                  │
│  ├─ Modifies request/response                                   │
│  ├─ Redirects/Rewrites                                          │
│  ├─ Authentication checks                                       │
│  └─ Edge Runtime (fast, no Node.js APIs)                        │
│                                                                 │
│  API Routes:                                                    │
│  ├─ Handles HTTP requests                                       │
│  ├─ Full Node.js runtime                                        │
│  ├─ Database access                                             │
│  ├─ External API calls                                          │
│  └─ Webhooks, file uploads                                      │
│                                                                 │
│  Server Components:                                             │
│  ├─ Renders page content                                        │
│  ├─ Data fetching for display                                   │
│  ├─ Direct database access                                      │
│  └─ Page-level logic                                            │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Middleware

```typescript
// middleware.ts (root of project)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add custom header
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'my-value')

  return response
}

// Only run on specific paths
export const config = {
  matcher: '/dashboard/:path*',
}

```

### Authentication Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  // Protected routes
  const protectedPaths = ['/dashboard', '/settings', '/profile']
  const isProtected = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  if (isProtected && !token) {
    // Redirect to login
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', request.nextUrl.pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect logged-in users away from auth pages
  const authPaths = ['/login', '/register']
  const isAuthPage = authPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*', '/profile/:path*',
            '/login', '/register'],
}

```

### Role-Based Access Control

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { jwtVerify } from 'jose'

const rolePermissions: Record<string, string[]> = {
  admin: ['/admin', '/dashboard', '/settings'],
  user: ['/dashboard', '/profile'],
  viewer: ['/dashboard'],
}

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  try {
    const { payload } = await jwtVerify(
      token,
      new TextEncoder().encode(process.env.JWT_SECRET)
    )

    const userRole = payload.role as string
    const pathname = request.nextUrl.pathname

    const allowedPaths = rolePermissions[userRole] || []
    const hasAccess = allowedPaths.some(path => pathname.startsWith(path))

    if (!hasAccess) {
      return NextResponse.redirect(new URL('/unauthorized', request.url))
    }

    // Add user info to headers for server components
    const response = NextResponse.next()
    response.headers.set('x-user-id', payload.sub as string)
    response.headers.set('x-user-role', userRole)

    return response
  } catch {
    // Invalid token
    const response = NextResponse.redirect(new URL('/login', request.url))
    response.cookies.delete('auth-token')
    return response
  }
}

```

### A/B Testing Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Check if user already has a variant
  let variant = request.cookies.get('ab-variant')?.value

  if (!variant) {
    // Randomly assign variant
    variant = Math.random() > 0.5 ? 'a' : 'b'
  }

  const response = NextResponse.next()
  response.cookies.set('ab-variant', variant, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 30, // 30 days
  })

  // Rewrite to variant-specific page
  if (request.nextUrl.pathname === '/') {
    const variantUrl = new URL(`/variant-${variant}`, request.url)
    return NextResponse.rewrite(variantUrl)
  }

  return response
}

```

### Geographic Routing

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const country = request.geo?.country || 'US'
  const city = request.geo?.city || 'Unknown'

  // Add geo headers
  const response = NextResponse.next()
  response.headers.set('x-country', country)
  response.headers.set('x-city', city)

  // Redirect based on country
  if (country === 'DE' && !request.nextUrl.pathname.startsWith('/de')) {
    return NextResponse.redirect(
      new URL(`/de${request.nextUrl.pathname}`, request.url)
    )
  }

  if (country === 'JP' && !request.nextUrl.pathname.startsWith('/ja')) {
    return NextResponse.redirect(
      new URL(`/ja${request.nextUrl.pathname}`, request.url)
    )
  }

  return response
}

```

### URL Rewriting

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Rewrite /blog/:slug to /posts/:slug
  if (pathname.startsWith('/blog/')) {
    const slug = pathname.replace('/blog/', '')
    const rewriteUrl = new URL(`/posts/${slug}`, request.url)
    return NextResponse.rewrite(rewriteUrl)
  }

  // Rewrite API versioning
  if (pathname.startsWith('/api/v1/')) {
    const newPath = pathname.replace('/api/v1/', '/api/')
    const rewriteUrl = new URL(newPath, request.url)
    return NextResponse.rewrite(rewriteUrl)
  }

  return NextResponse.next()
}

```

### Bot Detection

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const userAgent = request.headers.get('user-agent') || ''

  const botPatterns = [
    /googlebot/i,
    /bingbot/i,
    /slurp/i,
    /duckduckbot/i,
    /baiduspider/i,
  ]

  const isBot = botPatterns.some(pattern => pattern.test(userAgent))

  const response = NextResponse.next()

  if (isBot) {
    // Serve pre-rendered content for bots
    response.headers.set('x-is-bot', 'true')
  } else {
    response.headers.set('x-is-bot', 'false')
  }

  return response
}

```

### Rate Limiting

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Simple in-memory rate limiting (use Redis in production)
const rateLimit = new Map<string, { count: number; timestamp: number }>()

const WINDOW_MS = 60 * 1000 // 1 minute
const MAX_REQUESTS = 100

export function middleware(request: NextRequest) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown'
  const now = Date.now()

  const record = rateLimit.get(ip)

  if (!record || now - record.timestamp > WINDOW_MS) {
    rateLimit.set(ip, { count: 1, timestamp: now })
    return NextResponse.next()
  }

  if (record.count >= MAX_REQUESTS) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    )
  }

  record.count++
  return NextResponse.next()
}

```

### Header Manipulation

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const response = NextResponse.next()

  // Security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('Referrer-Policy', 'origin-when-cross-origin')
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=()'
  )

  // Cache control for static assets
  if (request.nextUrl.pathname.startsWith('/static/')) {
    response.headers.set(
      'Cache-Control',
      'public, max-age=31536000, immutable'
    )
  }

  // CORS headers for API routes
  if (request.nextUrl.pathname.startsWith('/api/')) {
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
  }

  return response
}

```

### Cookie Handling

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Read cookies
  const session = request.cookies.get('session')?.value
  const preferences = request.cookies.get('preferences')?.value

  const response = NextResponse.next()

  // Set cookies
  response.cookies.set('last-visit', new Date().toISOString(), {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 365, // 1 year
  })

  // Delete cookies
  if (request.nextUrl.pathname === '/logout') {
    response.cookies.delete('session')
    response.cookies.delete('preferences')
  }

  // Modify cookie values
  if (preferences) {
    const updated = JSON.parse(preferences)
    updated.lastPage = request.nextUrl.pathname
    response.cookies.set('preferences', JSON.stringify(updated), {
      httpOnly: true,
      secure: true,
    })
  }

  return response
}

```

### Conditional Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Skip middleware for static files
  if (request.nextUrl.pathname.startsWith('/_next')) {
    return NextResponse.next()
  }

  // Skip for API routes
  if (request.nextUrl.pathname.startsWith('/api')) {
    return NextResponse.next()
  }

  // Only run in production
  if (process.env.NODE_ENV === 'development') {
    return NextResponse.next()
  }

  // Production middleware logic
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Match all paths except:
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}

```

### Chaining Middleware

```typescript
// lib/middleware/auth.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function authMiddleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

```

```typescript
// lib/middleware/rate-limit.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const requests = new Map<string, number[]>()

export function rateLimitMiddleware(request: NextRequest) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown'
  const now = Date.now()
  const windowMs = 60 * 1000

  const timestamps = requests.get(ip) || []
  const recentTimestamps = timestamps.filter(t => now - t < windowMs)

  if (recentTimestamps.length >= 100) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 })
  }

  recentTimestamps.push(now)
  requests.set(ip, recentTimestamps)

  return NextResponse.next()
}

```

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { authMiddleware } from './lib/middleware/auth'
import { rateLimitMiddleware } from './lib/middleware/rate-limit'

export function middleware(request: NextRequest) {
  // Apply rate limiting first
  const rateLimitResponse = rateLimitMiddleware(request)
  if (rateLimitResponse.status !== 200) {
    return rateLimitResponse
  }

  // Apply auth for protected routes
  const protectedPaths = ['/dashboard', '/settings']
  const isProtected = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  if (isProtected) {
    return authMiddleware(request)
  }

  return NextResponse.next()
}

```

## Real-World Use Cases

| Use Case | Implementation |
|----------|---------------|
| Authentication | Check tokens, redirect to login |
| A/B Testing | Assign variants via cookies |
| Geographic routing | Redirect based on country |
| Bot detection | Serve different content to bots |
| Rate limiting | Throttle requests per IP |
| Redirects | URL-based redirects |
| Rewrites | Internal URL mapping |
| Security headers | Add CSP, CORS headers |
| Feature flags | Enable/disable features by path |
| Maintenance mode | Redirect all traffic during maintenance |

## Common Mistakes

### 1. Running Node.js APIs in Middleware

```typescript
// ❌ BAD: Node.js APIs not available in Edge Runtime
import fs from 'fs'
import { db } from './database'

export function middleware(request) {
  const data = fs.readFileSync('file.txt') // Error!
  const user = db.user.findFirst() // Error!
  return NextResponse.next()
}

// ✅ GOOD: Use Edge-compatible APIs
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token') // OK
  const country = request.geo?.country // OK
  return NextResponse.next()
}

```

### 2. Not Matching All Required Paths

```typescript
// ❌ BAD: Only matches /dashboard
export const config = {
  matcher: '/dashboard',
}

// ✅ GOOD: Match all dashboard paths
export const config = {
  matcher: ['/dashboard/:path*', '/dashboard'],
}

```

### 3. Infinite Redirects

```typescript
// ❌ BAD: Redirect loop
export function middleware(request: NextRequest) {
  if (!request.cookies.get('token')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  // Login page might also trigger middleware
  return NextResponse.next()
}

// ✅ GOOD: Exclude auth pages from middleware
export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*'],
}

```

### 4. Not Handling Edge Cases

```typescript
// ❌ BAD: No error handling
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value
  const payload = jwt.verify(token) // Might throw!
  return NextResponse.next()
}

// ✅ GOOD: Proper error handling
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  try {
    const payload = jwt.verify(token, secret)
    return NextResponse.next()
  } catch {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

```

### 5. Modifying Request Body

```typescript
// ❌ BAD: Can't modify request body in middleware
export function middleware(request: NextRequest) {
  const body = request.body // Can't read!
  request.body = modifiedBody // Can't modify!
  return NextResponse.next()
}

// ✅ GOOD: Use API routes for body modification
// app/api/route.ts
export async function POST(request: Request) {
  const body = await request.json()
  // Process body
  return Response.json({ success: true })
}

```

## Best Practices

1. **Keep middleware thin** — Only essential logic (auth, redirects)

2. **Use Edge-compatible APIs** — No Node.js modules

3. **Be specific with matchers** — Don't run on unnecessary paths

4. **Handle errors gracefully** — Always have fallback behavior

5. **Cache when possible** — Use Response caching headers

6. **Test thoroughly** — Middleware affects all matched routes

7. **Monitor performance** — Middleware adds latency to every request

8. **Use environment variables** — Don't hardcode secrets

9. **Implement in stages** — Start with logging, then add logic
10. **Document middleware behavior** — Team needs to understand the flow

## Performance Considerations

```text
Middleware Performance:

- Executes on Edge Runtime (fast cold starts)
- Adds latency to every matched request
- Should be lightweight (< 10ms typical)
- Avoid complex computations
- Cache responses when possible

Optimization:

- Use specific matchers
- Short-circuit early
- Avoid synchronous operations
- Use Response caching
- Monitor execution time

```

## Summary

| Feature | Middleware |
|---------|-----------|
| Location | `middleware.ts` at root |
| Runtime | Edge |
| When | Before page rendering |
| Can do | Redirect, rewrite, headers, cookies |
| Can't do | Node.js APIs, DB access, request body |
| Use case | Auth, redirects, A/B testing |
| Performance | Fast, adds minimal latency |

## Cheat Sheet
```text
File: middleware.ts (root)
Runtime: Edge
Matcher: export const config = { matcher: [...] }

Common patterns:
NextResponse.next()           → Continue
NextResponse.redirect(url)    → Change URL
NextResponse.rewrite(url)     → Internal rewrite
NextResponse.json(data)       → JSON response
response.headers.set(...)     → Add headers
response.cookies.set(...)     → Add cookies
response.cookies.delete(...)  → Remove cookies

Access:
request.nextUrl               → URL object
request.cookies               → Cookie access
request.headers               → Headers
request.geo                   → Geographic info

```

---

## See Also
- [Authentication](13-Authentication.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Next.js Docs: Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [Middleware API Reference](https://nextjs.org/docs/app/api-reference/functions/next-request)
- [Edge Runtime](https://nextjs.org/docs/app/api-reference/edge)
