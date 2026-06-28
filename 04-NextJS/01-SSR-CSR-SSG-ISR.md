# SSR, CSR, SSG, and ISR in Next.js

## Definition

Next.js supports multiple rendering strategies that determine **where** and **when** your pages are rendered:

| Strategy | Full Name | Renders On | When |
|----------|-----------|------------|------|
| **CSR** | Client-Side Rendering | Browser | After JavaScript loads |
| **SSR** | Server-Side Rendering | Server | On every request |
| **SSG** | Static Site Generation | Server | At build time |
| **ISR** | Incremental Static Regeneration | Server | At build time + revalidated |

## Why Do We Need It?

Different pages have different requirements:

- A **marketing page** rarely changes → SSG is optimal
- A **user dashboard** with personalized data → SSR ensures fresh data
- A **blog post** published occasionally → ISR gives static performance with freshness
- A **highly interactive** widget → CSR simplifies development

Choosing the wrong strategy leads to stale data, slow loads, or unnecessary server load.

## How It Works

### Rendering Pipeline Comparison

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         CSR (Client-Side)                          │
├─────────────────────────────────────────────────────────────────────┤
│  Browser requests page                                             │
│        │                                                           │
│        ▼                                                           │
│  Server sends empty HTML shell + JavaScript bundle                 │
│        │                                                           │
│        ▼                                                           │
│  Browser downloads & executes JS                                   │
│        │                                                           │
│        ▼                                                           │
│  JS fetches data from API                                          │
│        │                                                           │
│        ▼                                                           │
│  Page renders in browser (FOUC possible)                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         SSR (Server-Side)                          │
├─────────────────────────────────────────────────────────────────────┤
│  Browser requests page                                             │
│        │                                                           │
│        ▼                                                           │
│  Server fetches data                                               │
│        │                                                           │
│        ▼                                                           │
│  Server renders full HTML                                          │
│        │                                                           │
│        ▼                                                           │
│  Browser receives complete HTML (fast first paint)                 │
│        │                                                           │
│        ▼                                                           │
│  JS hydrates page (adds interactivity)                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         SSG (Static)                               │
├─────────────────────────────────────────────────────────────────────┤
│  BUILD TIME:                                                       │
│  Build process fetches data                                        │
│        │                                                           │
│        ▼                                                           │
│  Generates static HTML files                                       │
│        │                                                           │
│        ▼                                                           │
│  Files deployed to CDN                                             │
│                                                                     │
│  REQUEST TIME:                                                     │
│  Browser requests page → CDN serves pre-built HTML instantly       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      ISR (Incremental Static)                      │
├─────────────────────────────────────────────────────────────────────┤
│  BUILD TIME: Same as SSG                                           │
│                                                                     │
│  REQUEST TIME (after revalidation window):                         │
│  Browser requests page → CDN serves stale HTML                     │
│        │                                                           │
│        ▼                                                           │
│  Background regeneration triggered                                  │
│        │                                                           │
│        ▼                                                           │
│  Next request gets fresh HTML                                      │
└─────────────────────────────────────────────────────────────────────┘

```

## Code Examples

### CSR — Client-Side Rendering (Pages Router)

```tsx
// pages/dashboard.tsx
import { useEffect, useState } from 'react'

interface User {
  id: number
  name: string
  email: string
}

export default function Dashboard() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <h1>Dashboard</h1>
      {users.map(user => (
        <div key={user.id}>{user.name} — {user.email}</div>
      ))}
    </div>
  )
}

```

### CSR — Client-Side Rendering (App Router)

```tsx
// app/dashboard/page.tsx
'use client'

import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <h1>Dashboard</h1>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}

```

### SSR — Server-Side Rendering (Pages Router)

```tsx
// pages/profile.tsx
import { GetServerSideProps } from 'next'

interface ProfileProps {
  user: {
    id: number
    name: string
    email: string
    avatar: string
  }
}

export const getServerSideProps: GetServerSideProps<ProfileProps> = async (context) => {
  const { req } = context

  // Access cookies for authentication
  const token = req.headers.cookie?.split('token=')[1]?.split(';')[0]

  if (!token) {
    return { redirect: { destination: '/login', permanent: false } }
  }

  const res = await fetch('https://api.example.com/profile', {
    headers: { Authorization: `Bearer ${token}` }
  })

  const user = await res.json()

  return {
    props: { user }
  }
}

export default function Profile({ user }: ProfileProps) {
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <img src={user.avatar} alt={user.name} />
    </div>
  )
}

```

### SSR — Server-Side Rendering (App Router)

```tsx
// app/profile/page.tsx
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'

async function getUser() {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')?.value

  if (!token) {
    redirect('/login')
  }

  const res = await fetch('https://api.example.com/profile', {
    headers: { Authorization: `Bearer ${token}` },
    cache: 'no-store' // Ensures fresh data every request
  })

  if (!res.ok) throw new Error('Failed to fetch user')

  return res.json()
}

export default async function ProfilePage() {
  const user = await getUser()

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}

```

### SSG — Static Site Generation (Pages Router)

```tsx
// pages/blog/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next'

interface Post {
  slug: string
  title: string
  content: string
  publishedAt: string
}

interface PostProps {
  post: Post
}

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await fetch('https://api.example.com/posts')
  const posts: Post[] = await res.json()

  const paths = posts.map(post => ({
    params: { slug: post.slug }
  }))

  return {
    paths,
    fallback: false // 404 for unknown slugs
  }
}

export const getStaticProps: GetStaticProps<PostProps> = async ({ params }) => {
  const res = await fetch(`https://api.example.com/posts/${params?.slug}`)
  const post = await res.json()

  return {
    props: { post }
  }
}

export default function BlogPost({ post }: PostProps) {
  return (
    <article>
      <h1>{post.title}</h1>
      <time>{post.publishedAt}</time>
      <div>{post.content}</div>
    </article>
  )
}

```

### SSG — Static Site Generation (App Router)

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

interface Post {
  slug: string
  title: string
  content: string
}

async function getPost(slug: string): Promise<Post | null> {
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    next: { revalidate: false } // Static, no revalidation
  })

  if (!res.ok) return null
  return res.json()
}

// Generate static params at build time
export async function generateStaticParams() {
  const res = await fetch('https://api.example.com/posts')
  const posts: Post[] = await res.json()

  return posts.map(post => ({
    slug: post.slug
  }))
}

export default async function BlogPost({
  params
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  if (!post) notFound()

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}

```

### ISR — Incremental Static Regeneration (Pages Router)

```tsx
// pages/products/[id].tsx
import { GetStaticProps, GetStaticPaths } from 'next'

interface Product {
  id: string
  name: string
  price: number
  description: string
}

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await fetch('https://api.example.com/products')
  const products: Product[] = await res.json()

  return {
    paths: products.slice(0, 10).map(p => ({
      params: { id: p.id }
    })),
    fallback: 'blocking' // Generate on-demand for non-pre-rendered
  }
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const res = await fetch(`https://api.example.com/products/${params?.id}`)
  const product = await res.json()

  return {
    props: { product },
    revalidate: 60 // Revalidate every 60 seconds
  }
}

export default function Product({ product }: { product: Product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
      <p>{product.description}</p>
    </div>
  )
}

```

### ISR — Incremental Static Regeneration (App Router)

```tsx
// app/products/[id]/page.tsx
interface Product {
  id: string
  name: string
  price: number
  description: string
}

async function getProduct(id: string): Promise<Product> {
  const res = await fetch(`https://api.example.com/products/${id}`, {
    next: {
      revalidate: 60, // ISR: revalidate every 60 seconds
      tags: ['products'] // Tag-based revalidation
    }
  })

  if (!res.ok) throw new Error('Product not found')
  return res.json()
}

export default async function ProductPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const product = await getProduct(id)

  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
      <p>{product.description}</p>
    </div>
  )
}

```

### On-Demand Revalidation (ISR)

```tsx
// app/api/revalidate/route.ts
import { revalidateTag, revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { tag, path, secret } = await request.json()

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 })
  }

  // Revalidate by tag
  if (tag) {
    revalidateTag(tag)
  }

  // Revalidate by path
  if (path) {
    revalidatePath(path)
  }

  return NextResponse.json({ revalidated: true, timestamp: Date.now() })
}

```

### Fallback Rendering Strategies

```tsx
// Pages Router fallback options
export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [
      { params: { id: '1' } }, // Pre-rendered at build
      { params: { id: '2' } },
    ],
    fallback: 'blocking'
    // false: 404 for non-pre-rendered
    // true: show fallback UI, render in background
    // 'blocking': wait for server render, no fallback UI
  }
}

```

```tsx
// App Router: generateStaticParams + dynamicParams
export const dynamicParams = true // Allow on-demand generation

export async function generateStaticParams() {
  const posts = await fetchPosts()
  return posts.map(post => ({ slug: post.slug }))
}

```

### Middleware with ISR

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Add custom headers for ISR debugging
  const response = NextResponse.next()
  response.headers.set('x-render-mode', 'isr')
  return response
}

export const config = {
  matcher: '/products/:path*'
}

```

## Real-World Use Cases

| Page Type | Strategy | Reason |
|-----------|----------|--------|
| Marketing landing page | SSG | Content rarely changes |
| Blog posts | ISR | Static performance, occasional updates |
| User dashboard | SSR | Personalized, real-time data |
| E-commerce product page | ISR | Mostly static, price updates via on-demand revalidation |
| Admin panel | CSR | Highly interactive, authenticated |
| Documentation | SSG | Built from markdown, rarely changes |
| News article | ISR | Published once, updated rarely |
| Search results | SSR | Dynamic based on query parameters |

## Common Mistakes

### 1. Using SSR When SSG Would Suffice

```tsx
// ❌ BAD: Fetching static data on every request
export const getServerSideProps: GetServerSideProps = async () => {
  const data = await fetchStaticContent()
  return { props: { data } }
}

// ✅ GOOD: Pre-render at build time
export const getStaticProps: GetStaticProps = async () => {
  const data = await fetchStaticContent()
  return { props: { data }, revalidate: 3600 }
}

```

### 2. Exposing Sensitive Data in SSG

```tsx
// ❌ BAD: API keys in client bundle
export const getStaticProps: GetStaticProps = async () => {
  const res = await fetch(`https://api.example.com/data?key=${process.env.API_KEY}`)
  // API key may be exposed in build logs
  return { props: { data: await res.json() } }
}

// ✅ GOOD: Use environment variables properly
export const getStaticProps: GetStaticProps = async () => {
  const res = await fetch('https://api.example.com/data', {
    headers: { Authorization: `Bearer ${process.env.API_KEY}` }
  })
  return { props: { data: await res.json() } }
}

```

### 3. Forgetting revalidate in ISR

```tsx
// ❌ BAD: Page will never update after build
export const getStaticProps: GetStaticProps = async () => {
  return { props: { data: await fetchData() } } // Missing revalidate
}

// ✅ GOOD: Set appropriate revalidation
export const getStaticProps: GetStaticProps = async () => {
  return {
    props: { data: await fetchData() },
    revalidate: 300 // Update every 5 minutes
  }
}

```

### 4. Mixing CSR and SSR Incorrectly

```tsx
// ❌ BAD: Using window in SSR
export const getServerSideProps: GetServerSideProps = async () => {
  const width = window.innerWidth // Error! window is undefined on server
  return { props: { width } }
}

// ✅ GOOD: Use useEffect for browser APIs
export default function Page({ initialData }) {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    setWidth(window.innerWidth)
  }, [])

  return <div>Width: {width}</div>
}

```

### 5. Not Handling Loading States

```tsx
// ❌ BAD: No loading state for SSR/ISR
export default function Page({ data }) {
  return <div>{data.items.map(...)}</div> //闪烁 with slow data
}

// ✅ GOOD: Use loading.tsx or Suspense
// app/products/loading.tsx
export default function Loading() {
  return <div>Loading products...</div>
}

```

## Best Practices

1. **Default to SSG** — Start with static, add revalidation only when needed

2. **Use ISR for content that updates** — Blog posts, product pages, news

3. **Use SSR only when required** — Personalized dashboards, real-time data

4. **Use CSR for highly interactive widgets** — When server rendering adds no value

5. **Set appropriate revalidation intervals** — Balance freshness vs performance

6. **Use on-demand revalidation** — Trigger updates via webhooks instead of polling

7. **Implement proper error boundaries** — Handle failures gracefully

8. **Use `next/dynamic` for heavy client components** — Code-split when possible

9. **Test all rendering strategies** — They behave differently in development
10. **Monitor build times** — Too many static pages increase build duration

## Performance Considerations

| Strategy | TTFB | FCP | LCP | SEO | Server Load |
|----------|------|-----|-----|-----|-------------|
| CSR | Fast | Slow | Slow | Poor | Low |
| SSR | Slow | Fast | Fast | Excellent | High |
| SSG | Instant | Instant | Instant | Excellent | Zero |
| ISR | Fast* | Fast | Fast | Excellent | Low |

*ISR serves cached HTML instantly, regenerates in background.

### Bundle Size Impact

```text
CSR:  Large JS bundle (full React + page logic)
SSR:  Large JS bundle + server rendering overhead
SSG:  Large JS bundle, but pre-rendered HTML (fast paint)
ISR:  Same as SSG, with periodic regeneration

```

## Interview Questions

### Beginner (5-10)

1. **What is the difference between SSR and CSR?**
   CSR renders in the browser after JS loads; SSR renders on the server on every request. SSR provides faster first paint and better SEO.

2. **What does SSG stand for and when should you use it?**
   Static Site Generation pre-builds HTML at build time. Use for content that doesn't change frequently (marketing pages, docs, blogs).

3. **What is ISR?**
   Incremental Static Regeneration allows static pages to be updated after build time through revalidation, combining static performance with dynamic data.

4. **Which rendering strategy is best for SEO?**
   SSG and SSR are best for SEO because they provide fully rendered HTML. CSR is worse for SEO because crawlers may not execute JavaScript.

5. **Can you use all rendering strategies in the App Router?**
   Yes, but the API is different. Use `fetch` with `cache` and `next.revalidate` options instead of `getServerSideProps`/`getStaticProps`.

6. **What is `fallback` in `getStaticPaths`?**
   It determines what happens when a page is requested that wasn't pre-rendered: `false` = 404, `true` = show fallback UI, `'blocking'` = server-render on demand.

7. **How does hydration work?**
   Hydration is when React attaches event listeners to pre-rendered HTML, making it interactive. The HTML is served from the server, then React takes over.

8. **What is TTFB?**
   Time to First Byte — how long it takes for the browser to receive the first byte of data. SSG has the best TTFB, SSR is slower.

### Intermediate (5-10)

9. **Explain the difference between `revalidate: 60` and on-demand revalidation.**
   `revalidate: 60` revalidates after 60 seconds (time-based). On-demand revalidation uses `revalidateTag()` or `revalidatePath()` triggered by events like webhook calls.

10. **How do you handle authentication with SSR?**
    Access cookies/headers in `getServerSideProps` (Pages Router) or directly in the Server Component (App Router) to check authentication before rendering.

11. **What is the `stale-while-revalidate` pattern in ISR?**
    Serve the stale (cached) page immediately while regenerating in the background. Next request gets the fresh version.

12. **How do you generate static pages dynamically in the App Router?**
    Use `generateStaticParams()` to define which paths to pre-render and `dynamicParams = true/false` to control on-demand generation.

13. **When would you use `force-dynamic` in the App Router?**
    When you need SSR behavior (fresh data on every request) — for personalized pages, real-time dashboards, or pages with user-specific content.

14. **How do you debug rendering strategy?**
    Use `next.config.js` to enable debug headers, check the `x-render-mode` header, or use `next build` to see which pages are static vs dynamic.

15. **What happens if `getStaticProps` throws an error?**
    In Pages Router, the page shows a 500 error. In build mode, the build fails. You should handle errors gracefully.

### Senior (10-15)

16. **Design a rendering strategy for an e-commerce platform with 100K+ products.**
    Use ISR with `generateStaticParams` for the top 10K products, `dynamicParams: true` for the rest. Set `revalidate: 300` for prices, use on-demand revalidation for inventory changes via webhooks. Use SSR for cart/checkout pages.

17. **How would you implement ISR with database-backed content?**
    Use on-demand revalidation triggered by CMS webhooks or database change events. Store a version/hash in the database, compare at request time. Implement a stale-while-revalidate pattern with Redis caching as a fallback.

18. **Explain the performance tradeoffs between SSR and ISR for a news site.**
    SSR: Always fresh, but slower TTFB and higher server cost. ISR: Fast TTFB, lower server cost, but content can be stale. Solution: Use ISR with short revalidation (30s) and on-demand revalidation for breaking news.

19. **How do you handle edge cases in `getStaticPaths` with fallback?**
    For `fallback: 'blocking'`, implement rate limiting to prevent abuse. For `fallback: true`, ensure proper loading states. Consider using `getServerSideProps` fallback for personalized content.

20. **How would you migrate a large CRA app to Next.js with mixed rendering?**
    Identify page types: static pages → SSG, dynamic pages → SSR, interactive widgets → CSR. Migrate incrementally using `next/dynamic` for lazy loading. Set up proper caching headers and monitor performance.

21. **Design a system for A/B testing with different rendering strategies.**
    Use middleware to detect A/B test variants via cookies/headers. Serve different page variants using `getStaticProps` with different data based on the variant. Cache each variant separately. Use edge functions for low-latency routing.

22. **How do you handle streaming SSR with React Suspense?**
    Use `loading.tsx` in App Router for automatic Suspense boundaries. Wrap slow data fetches in `<Suspense>` components. The shell renders first, then streaming fills in delayed content.

23. **Explain the relationship between ISR and CDN caching.**
    ISR stores rendered pages in the data cache. When deployed to Vercel/CDN, the CDN serves cached HTML. Revalidation triggers a background regeneration. The CDN invalidates its cache when the data cache updates.

24. **How do you prevent stale data in ISR for critical pages?**
    Use short revalidation intervals (5-30s) combined with on-demand revalidation. Implement client-side polling for real-time updates. Use WebSocket connections for live data. Monitor cache hit rates.

25. **How would you implement ISR with a headless CMS?**
    Set up webhook handlers in Next.js to receive publish/unpublish events from the CMS. Trigger `revalidateTag()` for the affected content. Use `revalidatePath()` for navigation/menu changes. Implement draft mode for content preview.

### FAANG-style (5-10)

26. **Design a rendering architecture that handles 1M+ daily users with 99.9% availability.**
    Use SSG for public pages, ISR with aggressive caching for product pages, SSR for authenticated dashboards. Implement circuit breakers for data fetching, fallback rendering strategies, and edge caching. Monitor with observability tools.

27. **How would you optimize rendering performance for a page with 50+ data dependencies?**
    Use parallel data fetching with `Promise.all()`. Implement streaming SSR to render the shell first. Use React Suspense boundaries for progressive loading. Consider using React cache() for deduplication. Profile with React DevTools.

28. **Explain how you'd implement a rendering strategy that adapts based on user device/network.**
    Detect device type and network quality in middleware. Serve lightweight CSR for slow connections, full SSR for fast ones. Use Service Workers for offline support. Implement adaptive image loading.

29. **Design a system for real-time collaborative editing with SSR.**
    Use WebSocket connections for real-time sync. Implement operational transformation or CRDT for conflict resolution. Use SSR for initial page load with pre-populated data. Switch to CSR for interactive editing. Implement presence indicators.

30. **How would you handle rendering failures gracefully in a distributed system?**
    Implement retry logic with exponential backoff. Use fallback rendering (serve stale cache). Implement circuit breakers to prevent cascade failures. Use health checks and alerting. Design degraded mode rendering.

### Follow-ups (5-10)

31. **What are the limitations of ISR compared to SSR?**
    ISR can serve stale data within the revalidation window. It doesn't support request-time data like headers/cookies. It requires a data cache layer. On-demand revalidation has latency.

32. **How do you handle SEO with CSR-heavy applications?**
    Use pre-rendering services (Prerender.io), implement SSR for critical pages, use dynamic sitemaps, and implement proper meta tags. Consider using a hybrid approach.

33. **What is the impact of rendering strategy on Core Web Vitals?**
    CSR: Poor LCP/FCP, good CLS. SSR: Good LCP/FP, potential CLS. SSG: Excellent all metrics. ISR: Same as SSG with background updates.

34. **How do you test different rendering strategies?**
    Use `next build && next start` to test production builds. Test ISR with time-based and on-demand revalidation. Use Lighthouse for performance testing. Implement E2E tests for each strategy.

35. **What are the cost implications of each strategy?**
    CSR: Low server cost, high CDN cost. SSR: High server cost, low CDN cost. SSG: Zero server cost, high CDN cost. ISR: Low server cost, high CDN cost.

36. **How do you handle internationalization with different rendering strategies?**
    Use SSG for statically translated pages, ISR for content that changes per locale, SSR for user-specific localized content. Use middleware for locale detection and routing.

37. **What is the relationship between rendering strategy and caching layers?**
    SSG: Build-time cache only. SSR: No caching by default (add cache headers). ISR: Data cache + full route cache. Understanding cache hierarchy is crucial for performance.

38. **How do you handle form submissions with different rendering strategies?**
    CSR: Client-side form handling. SSR: Server Actions or API routes. SSG: Static forms with client-side submission. ISR: Same as SSG. Use progressive enhancement for maximum compatibility.

## Summary

| Feature | CSR | SSR | SSG | ISR |
|---------|-----|-----|-----|-----|
| Rendering | Client | Server | Build | Build + Revalidate |
| Freshness | Real-time | Real-time | Static | Stale-while-revalidate |
| Performance | Slow FCP | Fast FCP | Instant | Instant |
| Server Load | None | High | None | Low |
| SEO | Poor | Excellent | Excellent | Excellent |
| Complexity | Low | Medium | Low | Medium |

## Cheat Sheet

```text
CSR  → 'use client' + useEffect (App Router)
SSR  → fetch() in Server Component, cache: 'no-store' (App Router)
       getServerSideProps (Pages Router)
SSG  → fetch() in Server Component (default) (App Router)
       getStaticProps + getStaticPaths (Pages Router)
ISR  → fetch() with next.revalidate (App Router)
       getStaticProps + revalidate (Pages Router)

# Force rendering strategy (App Router):
force-static    → Force SSG
force-dynamic   → Force SSR
no-store        → No caching (SSR)
no-cache        → Revalidate every time

```

## References & Learn More

- [Next.js Docs: Rendering](https://nextjs.org/docs/app/building-your-application/rendering)
- [Next.js: Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Next.js: Static vs Dynamic Rendering](https://nextjs.org/docs/app/building-your-application/rendering/static-and-dynamic-rendering)
