# Next.js Interview Questions — Comprehensive Guide

## Overview

This guide covers 40 of the most commonly asked Next.js interview questions, categorized by difficulty level from Beginner to FAANG-style. Each answer includes explanations, code examples, and real-world context.

---

## Beginner Questions (1-10)

### 1. What is Next.js and why would you use it?

**Answer:**
Next.js is a React framework for production that provides:

- **Server-Side Rendering (SSR)** — Better SEO and performance
- **Static Site Generation (SSG)** — Fast page loads
- **File-based routing** — No routing library needed
- **API routes** — Built-in backend
- **Image optimization** — Automatic image processing
- **Code splitting** — Automatic bundle optimization

```tsx
// Example: Simple page in Next.js
// app/page.tsx
export default function Home() {
  return <h1>Welcome to Next.js</h1>
}

```

**When to use:** For production React applications needing SEO, performance, and developer experience.

---

### 2. What is the difference between Pages Router and App Router?

**Answer:**

| Feature | Pages Router | App Router |
|---------|-------------|------------|
| Directory | `pages/` | `app/` |
| Default Component | Client | Server |
| Layouts | Single `_app.tsx` | Nested `layout.tsx` |
| Loading | Manual | `loading.tsx` |
| Error | `_error.tsx` | `error.tsx` |
| Server Components | No | Yes |

```tsx
// Pages Router: pages/about.tsx
export default function About() {
  return <h1>About</h1>
}

// App Router: app/about/page.tsx
export default function About() {
  return <h1>About</h1>
}

```

**Recommendation:** Use App Router for new projects — it's the future of Next.js.

---

### 3. What is Server-Side Rendering (SSR)?

**Answer:**
SSR renders pages on the server for every request. The server fetches data, renders HTML, and sends it to the browser.

```tsx
// Pages Router SSR
export const getServerSideProps: GetServerSideProps = async () => {
  const data = await fetch('https://api.example.com/data')
  return { props: { data } }
}

// App Router SSR (default behavior)
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'no-store' // Always fresh
  })
  return <div>{data.value}</div>
}

```

**Benefits:** Fresh data, good SEO, works without JavaScript.

---

### 4. What is Static Site Generation (SSG)?

**Answer:**
SSG generates HTML at build time. Pages are pre-rendered and served from CDN.

```tsx
// Pages Router SSG
export const getStaticProps: GetStaticProps = async () => {
  const data = await fetch('https://api.example.com/data')
  return { props: { data }, revalidate: 3600 }
}

// App Router SSG (default behavior)
export default async function Page() {
  const data = await fetch('https://api.example.com/data')
  return <div>{data.value}</div>
}

```

**Benefits:** Fastest loading, excellent SEO, low server cost.

---

### 5. What is the App Router's layout system?

**Answer:**
Layouts are shared UI that persist across navigations. They don't re-render on route changes.

```tsx
// app/layout.tsx — Root layout (required)
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <nav>Global Nav</nav>
        <main>{children}</main>
      </body>
    </html>
  )
}

// app/dashboard/layout.tsx — Nested layout
export default function DashboardLayout({ children }) {
  return (
    <div className="flex">
      <aside>Sidebar</aside>
      <main>{children}</main>
    </div>
  )
}

```

**Benefits:** Shared UI without prop drilling, performance optimization.

---

### 6. What are Server Components?

**Answer:**
Server Components render on the server and send only HTML to the client. They can't use hooks or browser APIs.

```tsx
// Server Component (default in App Router)
export default async function Page() {
  // Direct database access!
  const posts = await db.post.findMany()
  return posts.map(p => <div key={p.id}>{p.title}</div>)
}

```

**Benefits:** Zero client JS, direct data access, better security.

---

### 7. What are Client Components?

**Answer:**
Client Components render on the client with full interactivity. Use `'use client'` directive.

```tsx
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

```

**When to use:** When you need useState, useEffect, event handlers, or browser APIs.

---

### 8. How do you handle navigation in Next.js?

**Answer:**
Use the `next/link` component for client-side navigation.

```tsx
import Link from 'next/link'

export function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/blog/[slug]" as="/blog/my-post">Blog</Link>
    </nav>
  )
}

```

**Programmatic navigation:**

```tsx
'use client'
import { useRouter } from 'next/navigation'

export function LogoutButton() {
  const router = useRouter()

  const handleLogout = async () => {
    await fetch('/api/logout')
    router.push('/login')
  }

  return <button onClick={handleLogout}>Logout</button>
}

```

---

### 9. How do you fetch data in Next.js?

**Answer:**
In App Router, fetch data directly in Server Components.

```tsx
// Server Component — direct fetch
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 } // ISR: revalidate every 60s
  }).then(res => res.json())

  return <div>{data.value}</div>
}

```

**With error handling:**

```tsx
export default async function Page() {
  try {
    const data = await fetch('https://api.example.com/data')
    if (!data.ok) throw new Error('Failed to fetch')
    const json = await data.json()
    return <div>{json.value}</div>
  } catch (error) {
    return <div>Error loading data</div>
  }
}

```

---

### 10. What is middleware in Next.js?

**Answer:**
Middleware runs before a request is completed. It can redirect, rewrite, or modify requests.

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*'],
}

```

**Use cases:** Authentication, redirects, A/B testing, geographic routing.

---

## Intermediate Questions (11-20)

### 11. How do you implement authentication in Next.js?

**Answer:**

```tsx
// middleware.ts — Route protection
import { NextResponse } from 'next/server'

export function middleware(request) {
  const token = request.cookies.get('session')

  if (!token && request.nextUrl.pathname.startsWith('/protected')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

// app/api/login/route.ts — Login handler
export async function POST(request: Request) {
  const { email, password } = await request.json()

  const user = await authenticate(email, password)

  if (!user) {
    return Response.json({ error: 'Invalid credentials' }, { status: 401 })
  }

  const response = Response.json({ success: true })
  response.cookies.set('session', user.sessionId, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
  })

  return response
}

```

---

### 12. How do you handle forms with Server Actions?

**Answer:**

```tsx
// app/actions/post.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await db.post.create({
    data: { title, content },
  })

  revalidatePath('/posts')
  redirect('/posts')
}

// app/posts/new/page.tsx
import { createPost } from '../actions/post'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  )
}

```

---

### 13. How do you optimize images in Next.js?

**Answer:**

```tsx
import Image from 'next/image'

export function ProductImage() {
  return (
    <Image
      src="/product.jpg"
      alt="Product"
      width={800}
      height={600}
      priority // Above the fold
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
      sizes="(max-width: 768px) 100vw, 50vw"
    />
  )
}

```

**Key features:**

- Lazy loading (except priority)
- WebP/AVIF format conversion
- Responsive sizing
- Blur placeholders
- CDN caching

---

### 14. How do you implement caching strategies?

**Answer:**

```tsx
// Time-based revalidation (ISR)
const data = await fetch(url, { next: { revalidate: 60 } })

// No caching (always fresh)
const data = await fetch(url, { cache: 'no-store' })

// Force cache (until manually invalidated)
const data = await fetch(url, { cache: 'force-cache' })

// Tag-based revalidation
const data = await fetch(url, { next: { tags: ['posts'] } })

// On-demand revalidation
import { revalidateTag, revalidatePath } from 'next/cache'
revalidateTag('posts')
revalidatePath('/posts')

```

---

### 15. How do you implement API routes?

**Answer:**

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET() {
  const users = await db.user.findMany()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await db.user.create({ data: body })
  return NextResponse.json(user, { status: 201 })
}

// Dynamic route: app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  const user = await db.user.findUnique({ where: { id } })
  return NextResponse.json(user)
}

```

---

### 16. How do you handle error boundaries?

**Answer:**

```tsx
// app/error.tsx — Route-level error boundary
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}

// app/not-found.tsx — 404 page
export default function NotFound() {
  return (
    <div>
      <h2>404 - Page Not Found</h2>
      <a href="/">Return home</a>
    </div>
  )
}

```

---

### 17. How do you implement metadata for SEO?

**Answer:**

```tsx
// app/layout.tsx — Static metadata
export const metadata: Metadata = {
  title: { template: '%s | MyApp', default: 'MyApp' },
  description: 'My application description',
}

// app/blog/[slug]/page.tsx — Dynamic metadata
export async function generateMetadata({ params }) {
  const { slug } = await params
  const post = await getPost(slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      images: [post.coverImage],
    },
  }
}

```

---

### 18. How do you implement parallel routes?

**Answer:**

```tsx
// app/layout.tsx
export default function Layout({ children, modal }) {
  return (
    <div>
      {children}
      {modal}
    </div>
  )
}

// app/@modal/(.)photos/[id]/page.tsx — Intercepted route
export default function PhotoModal({ params }) {
  return (
    <div className="modal">
      <img src={`/photos/${params.id}`} />
    </div>
  )
}

```

**Use cases:** Modals over existing pages, split views, dashboards.

---

### 19. How do you handle streaming and Suspense?

**Answer:**

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Fast content renders immediately */}
      <DashboardSummary />

      {/* Slow content streams in */}
      <Suspense fallback={<LoadingSkeleton />}>
        <SlowDataComponent />
      </Suspense>
    </div>
  )
}

// app/dashboard/loading.tsx — Automatic Suspense boundary
export default function Loading() {
  return <div>Loading dashboard...</div>
}

```

---

### 20. How do you implement i18n (internationalization)?

**Answer:**

```tsx
// middleware.ts
import { NextResponse } from 'next/server'

export function middleware(request) {
  const locale = request.headers.get('accept-language')?.split(',')[0] || 'en'
  const pathname = request.nextUrl.pathname

  // Check if locale is already in URL
  const pathnameHasLocale = /^\/(en|es|fr)/.test(pathname)

  if (!pathnameHasLocale) {
    return NextResponse.redirect(
      new URL(`/${locale}${pathname}`, request.url)
    )
  }

  return NextResponse.next()
}

// app/[locale]/layout.tsx
export default function LocaleLayout({ children, params }) {
  return (
    <html lang={params.locale}>
      <body>{children}</body>
    </html>
  )
}

```

---

## Senior Questions (21-30)

### 21. Design a rendering strategy for a large-scale application.

**Answer:**

```tsx
// Strategy by page type:
// - Marketing pages: SSG with ISR
// - Product pages: ISR with on-demand revalidation
// - User dashboards: SSR with no cache
// - Admin panels: CSR with dynamic imports

// app/products/[id]/page.tsx — ISR for product pages
export const revalidate = 60 // Revalidate every 60s

export default async function ProductPage({ params }) {
  const { id } = await params
  const product = await getProduct(id)

  return <ProductDetails product={product} />
}

// app/dashboard/page.tsx — SSR for personalized content
export const dynamic = 'force-dynamic'

export default async function DashboardPage() {
  const user = await getCurrentUser()
  const data = await getUserData(user.id)

  return <Dashboard data={data} />
}

```

---

### 22. How would you implement a micro-frontend architecture?

**Answer:**

```tsx
// Using Module Federation
// app/layout.tsx
import dynamic from 'next/dynamic'

const RemoteApp = dynamic(() => import('remote/App'), {
  loading: () => <div>Loading remote app...</div>,
  ssr: false,
})

export default function Layout({ children }) {
  return (
    <div>
      <nav>Shell Navigation</nav>
      <RemoteApp />
      {children}
    </div>
  )
}

```

**Key considerations:**

- Shared React runtime
- Independent deployments
- Shared state management
- Route coordination

---

### 23. How do you optimize performance for a high-traffic application?

**Answer:**

```tsx
// 1. Use ISR for popular pages
export const revalidate = 60

// 2. Implement edge caching
// next.config.js
module.exports = {
  experimental: {
    ppr: true, // Partial Pre-Rendering
  },
}

// 3. Use React cache() for deduplication
import { cache } from 'react'

export const getUser = cache(async (id) => {
  return db.user.findUnique({ where: { id } })
})

// 4. Implement streaming
export default function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <SlowComponent />
    </Suspense>
  )
}

// 5. Use dynamic imports for heavy components
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
})

```

---

### 24. How would you implement real-time features?

**Answer:**

```tsx
// Using Server-Sent Events
// app/api/events/route.ts
export async function GET() {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      // Subscribe to database changes
      const unsubscribe = subscribeToChanges((change) => {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify(change)}\n\n`)
        )
      })

      // Cleanup on disconnect
      return () => unsubscribe()
    },
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
    },
  })
}

// Client component
'use client'
import { useEffect, useState } from 'react'

export function RealTimeData() {
  const [data, setData] = useState(null)

  useEffect(() => {
    const eventSource = new EventSource('/api/events')
    eventSource.onmessage = (event) => {
      setData(JSON.parse(event.data))
    }
    return () => eventSource.close()
  }, [])

  return <div>{data?.value}</div>
}

```

---

### 25. How do you implement comprehensive testing?

**Answer:**

```tsx
// Unit tests with Jest
// __tests__/components/Counter.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Counter } from '@/components/Counter'

test('increments count', () => {
  render(<Counter />)
  fireEvent.click(screen.getByText('Increment'))
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})

// E2E tests with Playwright
// tests/home.spec.ts
import { test, expect } from '@playwright/test'

test('homepage loads correctly', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('h1')).toHaveText('Welcome')
})

// API tests
// tests/api/users.test.ts
test('GET /api/users returns users', async ({ request }) => {
  const response = await request.get('/api/users')
  expect(response.ok()).toBeTruthy()
  const users = await response.json()
  expect(Array.isArray(users)).toBeTruthy()
})

```

---

### 26. How would you implement feature flags?

**Answer:**

```tsx
// lib/feature-flags.ts
export const featureFlags = {
  newDashboard: process.env.FEATURE_NEW_DASHBOARD === 'true',
  betaFeatures: process.env.FEATURE_BETA === 'true',
}

// app/dashboard/page.tsx
import { featureFlags } from '@/lib/feature-flags'

export default function DashboardPage() {
  if (featureFlags.newDashboard) {
    return <NewDashboard />
  }
  return <LegacyDashboard />
}

// Middleware for route-based flags
export function middleware(request) {
  if (request.nextUrl.pathname === '/beta') {
    if (!featureFlags.betaFeatures) {
      return NextResponse.redirect(new URL('/', request.url))
    }
  }
  return NextResponse.next()
}

```

---

### 27. How do you handle complex state management?

**Answer:**

```tsx
// Using URL state for shareable state
'use client'
import { useSearchParams, useRouter } from 'next/navigation'

export function Filters() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const category = searchParams.get('category') || 'all'

  const setCategory = (cat: string) => {
    const params = new URLSearchParams(searchParams)
    params.set('category', cat)
    router.push(`?${params.toString()}`)
  }

  return (
    <select value={category} onChange={(e) => setCategory(e.target.value)}>
      <option value="all">All</option>
      <option value="electronics">Electronics</option>
    </select>
  )
}

// Using React Context for app state
'use client'
import { createContext, useContext, useState } from 'react'

const AppContext = createContext()

export function AppProvider({ children }) {
  const [state, setState] = useState({ theme: 'light' })
  return (
    <AppContext.Provider value={{ state, setState }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)

```

---

### 28. How would you implement monitoring and observability?

**Answer:**

```tsx
// lib/monitoring.ts
export function trackMetric(name: string, value: number) {
  if (typeof window !== 'undefined') {
    // Send to analytics
    fetch('/api/metrics', {
      method: 'POST',
      body: JSON.stringify({ name, value, timestamp: Date.now() }),
    })
  }
}

// Server Component with performance tracking
export default async function Page() {
  const start = performance.now()

  const data = await fetchData()

  const duration = performance.now() - start
  trackMetric('page.fetch.duration', duration)

  return <div>{data.value}</div>
}

// Error tracking
export function withErrorTracking<T>(fn: () => T): T {
  try {
    return fn()
  } catch (error) {
    console.error('Error:', error)
    // Send to error tracking service
    throw error
  }
}

```

---

### 29. How do you implement A/B testing?

**Answer:**

```tsx
// middleware.ts
import { NextResponse } from 'next/server'

export function middleware(request) {
  let variant = request.cookies.get('ab-variant')?.value

  if (!variant) {
    variant = Math.random() > 0.5 ? 'a' : 'b'
  }

  const response = NextResponse.next()
  response.cookies.set('ab-variant', variant, {
    httpOnly: true,
    maxAge: 60 * 60 * 24 * 30, // 30 days
  })

  return response
}

// app/page.tsx
import { cookies } from 'next/headers'

export default async function Page() {
  const cookieStore = await cookies()
  const variant = cookieStore.get('ab-variant')?.value || 'a'

  return variant === 'a' ? <VersionA /> : <VersionB />
}

```

---

### 30. How would you migrate from Pages Router to App Router?

**Answer:**

```tsx
// Step 1: Create app/ directory alongside pages/
// Step 2: Migrate pages incrementally
// Step 3: Move data fetching logic
// Step 4: Update imports and components

// Before (Pages Router):
// pages/about.tsx
export default function About({ data }) {
  return <div>{data.content}</div>
}

export async function getStaticProps() {
  const data = await fetchAbout()
  return { props: { data } }
}

// After (App Router):
// app/about/page.tsx
export default async function AboutPage() {
  const data = await fetchAbout()
  return <div>{data.content}</div>
}

```

**Migration strategy:**

1. Start with static pages

2. Migrate dynamic pages

3. Update API routes

4. Test thoroughly

5. Deploy with feature flags

---

## FAANG-Style Questions (31-35)

### 31. Design a system for 1M+ daily active users.

**Answer:**

**Architecture:**

- **Edge rendering:** Use Edge Runtime for fast cold starts
- **CDN caching:** Cache static pages at edge
- **Database:** Connection pooling, read replicas
- **State:** Redis for session management
- **Monitoring:** APM, error tracking, metrics

```tsx
// Edge middleware for fast routing
export const runtime = 'edge'

export function middleware(request) {
  // Fast routing logic at edge
  return NextResponse.next()
}

// ISR with aggressive caching
export const revalidate = 60

// Connection pooling
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
})

```

---

### 32. How would you implement a real-time collaborative editing system?

**Answer:**

**Architecture:**

- WebSocket for real-time sync
- Operational Transformation (OT) or CRDT for conflict resolution
- Server Components for initial load
- Client Components for editing

```tsx
// WebSocket connection
'use client'
import { useEffect, useRef } from 'react'

export function CollaborativeEditor({ documentId }) {
  const wsRef = useRef(null)

  useEffect(() => {
    wsRef.current = new WebSocket(`wss://api.example.com/ws/${documentId}`)

    wsRef.current.onmessage = (event) => {
      const change = JSON.parse(event.data)
      applyChange(change)
    }

    return () => wsRef.current?.close()
  }, [documentId])

  return <Editor onChange={handleChange} />
}

```

---

### 33. Design a globally distributed application.

**Answer:**

**Architecture:**

- **Multi-region:** Deploy to multiple regions
- **Geo-routing:** Route users to nearest region
- **Data replication:** Sync data across regions
- **Edge functions:** Run logic at edge

```tsx
// middleware.ts — Geo-based routing
export function middleware(request) {
  const country = request.geo?.country || 'US'

  // Route to region-specific content
  if (country === 'EU') {
    return NextResponse.rewrite(new URL('/eu' + request.nextUrl.pathname, request.url))
  }

  return NextResponse.next()
}

// Regional data fetching
async function getData(region) {
  const dbUrl = process.env[`DATABASE_${region.toUpperCase()}`]
  return fetch(dbUrl)
}

```

---

### 34. How would you implement a microservices architecture?

**Answer:**

**Architecture:**

- **API Gateway:** Next.js as BFF (Backend for Frontend)
- **Service discovery:** Environment-based service URLs
- **Circuit breakers:** Handle service failures
- **Load balancing:** Distribute requests

```tsx
// lib/services.ts
const services = {
  users: process.env.USER_SERVICE_URL,
  products: process.env.PRODUCT_SERVICE_URL,
  orders: process.env.ORDER_SERVICE_URL,
}

export async function callService(service, path, options) {
  const url = `${services[service]}${path}`

  try {
    const response = await fetch(url, options)
    if (!response.ok) throw new Error('Service error')
    return await response.json()
  } catch (error) {
    // Circuit breaker logic
    throw error
  }
}

// API route as gateway
// app/api/users/route.ts
export async function GET() {
  return callService('users', '/users')
}

```

---

### 35. Design a system for handling Black Friday traffic spikes.

**Answer:**

**Architecture:**

- **Pre-rendering:** ISR for popular products
- **CDN:** Aggressive caching at edge
- **Queue:** Order processing queue
- **Fallback:** Graceful degradation

```tsx
// Pre-render popular products
export async function generateStaticParams() {
  const popularProducts = await getPopularProducts()
  return popularProducts.map(p => ({ id: p.id }))
}

// Queue for order processing
// app/api/checkout/route.ts
export async function POST(request) {
  const order = await request.json()

  // Add to queue instead of processing immediately
  await queue.add('process-order', order)

  return Response.json({
    success: true,
    message: 'Order queued for processing',
  })
}

// Graceful degradation
export default async function ProductPage({ params }) {
  try {
    const product = await getProduct(params.id)
    return <ProductDetails product={product} />
  } catch (error) {
    // Fallback to cached version
    const cached = await getCachedProduct(params.id)
    return <ProductDetails product={cached} degraded />
  }
}

```

---

## Follow-Up Questions (36-40)

### 36. What are the trade-offs between SSR and ISR?

**Answer:**

| Aspect | SSR | ISR |
|--------|-----|-----|
| Freshness | Real-time | Stale-while-revalidate |
| Performance | Slower TTFB | Faster TTFB |
| Server load | High | Low |
| Use case | Personalized content | Public content |

**When to use SSR:** User dashboards, personalized pages, real-time data.
**When to use ISR:** Product pages, blog posts, marketing pages.

---

### 37. How do you handle database connections in Server Components?

**Answer:**

```tsx
// lib/db.ts
import { Pool } from 'pg'

const globalForDb = globalThis as unknown as {
  pool: Pool | undefined
}

export const pool = globalForDb.pool ?? new Pool({
  connectionString: process.env.DATABASE_URL,
})

if (process.env.NODE_ENV !== 'production') {
  globalForDb.pool = pool
}

// Usage in Server Component
export default async function Page() {
  const result = await pool.query('SELECT * FROM users')
  return <div>{result.rows.length} users</div>
}

```

**Connection pooling:** Reuse connections across requests in development.

---

### 38. How do you implement rate limiting?

**Answer:**

```tsx
// middleware.ts
import { NextResponse } from 'next/server'

const rateLimit = new Map()

export function middleware(request) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown'
  const now = Date.now()
  const windowMs = 60 * 1000 // 1 minute
  const maxRequests = 100

  const record = rateLimit.get(ip) || { count: 0, timestamp: now }

  if (now - record.timestamp > windowMs) {
    record.count = 1
    record.timestamp = now
  } else {
    record.count++
  }

  rateLimit.set(ip, record)

  if (record.count > maxRequests) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    )
  }

  return NextResponse.next()
}

```

---

### 39. How do you handle offline support?

**Answer:**

```tsx
// next.config.js
module.exports = {
  experimental: {
    ppr: true,
  },
}

// Service Worker registration
'use client'
import { useEffect } from 'react'

export function ServiceWorkerRegistration() {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
    }
  }, [])

  return null
}

// public/sw.js
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request)
    })
  )
})

```

---

### 40. How do you monitor and debug Next.js applications?

**Answer:**

```tsx
// Performance monitoring
export default async function Page() {
  const start = performance.now()

  const data = await fetchData()

  const duration = performance.now() - start
  console.log(`Data fetch took ${duration}ms`)

  return <div>{data.value}</div>
}

// Error tracking
// app/error.tsx
'use client'

export default function Error({ error, reset }) {
  useEffect(() => {
    // Send to error tracking service
    trackError(error)
  }, [error])

  return (
    <div>
      <h2>Error occurred</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}

// Logging middleware
// middleware.ts
export function middleware(request) {
  console.log(`${request.method} ${request.nextUrl.pathname}`)
  return NextResponse.next()
}

```

**Tools:**

- React DevTools
- Next.js DevTools
- Vercel Analytics
- Custom performance marks

---

## Summary

| Level | Topics |
|-------|--------|
| Beginner | Basics, routing, SSR/SSG, components |
| Intermediate | Auth, forms, caching, API routes, error handling |
| Senior | Architecture, performance, testing, migrations |
| FAANG | Scale, distributed systems, real-time, microservices |
| Follow-ups | Trade-offs, debugging, monitoring, edge cases |

## Quick Reference

```text
Key Concepts:

- App Router: app/ directory, Server Components, nested layouts
- Data Fetching: fetch() in Server Components, ISR, SSR
- Caching: Data Cache, Full Route Cache, Router Cache
- Forms: Server Actions, useFormState, useFormStatus
- Images: next/image, lazy loading, optimization
- Middleware: Edge Runtime, redirects, rewrites

Performance:

- Use ISR for static content
- Use SSR for personalized content
- Use streaming for slow data
- Use Suspense for progressive loading

Best Practices:

- Default to Server Components
- Use 'use client' sparingly
- Implement proper error handling
- Monitor performance metrics

```

## References & Learn More

- [Next.js Docs](https://nextjs.org/docs)
- [Next.js Learn Course](https://nextjs.org/learn)
- [Next.js GitHub](https://github.com/vercel/next.js)
- [Next.js Discord](https://discord.gg/bUG2bvbtHy)
