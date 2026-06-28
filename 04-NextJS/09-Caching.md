# Caching in Next.js

## Definition

Next.js implements a multi-layered caching system that improves performance by storing and reusing rendered results, data fetches, and static assets. The caching system includes **Data Cache**, **Full Route Cache**, **Router Cache**, and **Request Memoization**.

## Why Do We Need It?

1. **Performance** — Serve content faster with cached responses
2. **Cost reduction** — Reduce server load and database queries
3. **Scalability** — Handle more users without proportional resource increase
4. **User experience** — Instant navigation with cached pages
5. **SEO** — Fast page loads improve search rankings

## How It Works

### Caching Layers Overview

```text
┌─────────────────────────────────────────────────────────────────┐
│                    NEXT.JS CACHING LAYERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 1: Request Memoization                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - In-memory cache per request                          │   │
│  │  - Deduplicates fetch calls in same request             │   │
│  │  - Automatic                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  Layer 2: Data Cache                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - Persistent cache across requests                     │   │
│  │  - Stores fetch results                                 │   │
│  │  - Revalidated via time or on-demand                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  Layer 3: Full Route Cache                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - Caches entire rendered route                         │   │
│  │  - Static routes only                                   │   │
│  │  - Stores React Server Component output                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  Layer 4: Router Cache                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - Client-side cache                                    │   │
│  │  - Caches RSC payload in browser                        │   │
│  │  - Prefetch cache for route transitions                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Cache Invalidation Flow

```text
┌─────────────────────────────────────────────────────────────────┐
│                 CACHE INVALIDATION METHODS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Time-Based Revalidation                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  fetch(url, { next: { revalidate: 60 } })               │   │
│  │  → Cache expires after 60 seconds                       │   │
│  │  → Next request triggers regeneration                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  On-Demand Revalidation                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  revalidatePath('/posts')                               │   │
│  │  revalidateTag('posts')                                 │   │
│  │  → Immediate cache invalidation                         │   │
│  │  → Triggered by webhooks or user actions                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  No Cache                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  fetch(url, { cache: 'no-store' })                      │   │
│  │  → Always fetch fresh data                              │   │
│  │  → No caching                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Data Cache — Time-Based Revalidation

```tsx
// app/products/page.tsx
export default async function ProductsPage() {
  // Cache for 60 seconds
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 },
  }).then(res => res.json())

  return (
    <div>
      <h1>Products</h1>
      {products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  )
}
```

### Data Cache — No Store (Always Fresh)

```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // Never cache, always fetch fresh
  const data = await fetch('https://api.example.com/dashboard', {
    cache: 'no-store',
  }).then(res => res.json())

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Last updated: {data.lastUpdated}</p>
    </div>
  )
}
```

### Data Cache — Force Cache

```tsx
// app/about/page.tsx
export default async function AboutPage() {
  // Cache indefinitely until manually revalidated
  const content = await fetch('https://api.example.com/about', {
    cache: 'force-cache',
  }).then(res => res.json())

  return (
    <div>
      <h1>About Us</h1>
      <p>{content.description}</p>
    </div>
  )
}
```

### Tag-Based Revalidation

```tsx
// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { tag, secret } = await request.json()

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 })
  }

  revalidateTag(tag)

  return NextResponse.json({ revalidated: true, timestamp: Date.now() })
}
```

```tsx
// app/blog/page.tsx
export default async function BlogPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] },
  }).then(res => res.json())

  return (
    <div>
      <h1>Blog</h1>
      {posts.map(post => (
        <article key={post.id}>{post.title}</article>
      ))}
    </div>
  )
}
```

### Path-Based Revalidation

```tsx
// app/api/revalidate-path/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { path, secret } = await request.json()

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 })
  }

  revalidatePath(path)

  return NextResponse.json({ revalidated: true, timestamp: Date.now() })
}
```

### Full Route Cache

```tsx
// app/products/page.tsx — Automatically cached (static)
export default async function ProductsPage() {
  // This page is statically generated and cached
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 },
  }).then(res => res.json())

  return (
    <div>
      <h1>Products</h1>
      {products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  )
}

// Force dynamic (bypass Full Route Cache)
export const dynamic = 'force-dynamic'
```

### Request Memoization

```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  // Both fetch calls are deduplicated automatically
  const user = await fetch('https://api.example.com/user')
  const posts = await fetch('https://api.example.com/user/posts')

  // Even if user data is fetched twice in same component
  const userData = await fetch('https://api.example.com/user') // Deduplicated!

  return (
    <div>
      <h1>Dashboard</h1>
    </div>
  )
}
```

### React cache() for Deduplication

```tsx
// lib/data.ts
import { cache } from 'react'

export const getUser = cache(async (id: string) => {
  const res = await fetch(`https://api.example.com/users/${id}`)
  return res.json()
})

export const getUserPosts = cache(async (userId: string) => {
  const res = await fetch(`https://api.example.com/users/${userId}/posts`)
  return res.json()
})
```

```tsx
// app/users/[id]/page.tsx
import { getUser, getUserPosts } from '@/lib/data'

export default async function UserPage({ params }) {
  const { id } = await params

  // These are deduplicated across the component tree
  const user = await getUser(id)
  const posts = await getUserPosts(id)

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{posts.length} posts</p>
    </div>
  )
}
```

### Route Segment Config for Caching

```tsx
// Force static (enable Full Route Cache)
export const dynamic = 'force-static'

// Force dynamic (disable Full Route Cache)
export const dynamic = 'force-dynamic'

// Disable fetch cache
export const fetchCache = 'no-store'

// Revalidate every 60 seconds
export const revalidate = 60
```

### Cache with Headers

```tsx
// app/api/products/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const products = await fetchProducts()

  return NextResponse.json(products, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate',
      'CDN-Cache-Control': 'public, max-age=300',
    },
  })
}
```

### Incremental Static Regeneration (ISR)

```tsx
// app/products/[id]/page.tsx
export default async function ProductPage({ params }) {
  const { id } = await params

  // ISR: Stale while revalidate pattern
  const product = await fetch(`https://api.example.com/products/${id}`, {
    next: {
      revalidate: 60, // Revalidate after 60 seconds
      tags: [`product-${id}`], // Tag for on-demand revalidation
    },
  }).then(res => res.json())

  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
    </div>
  )
}
```

### On-Demand Revalidation via Webhook

```tsx
// app/api/webhooks/stripe/route.ts
import { revalidateTag } from 'next/cache'
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
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  if (event.type === 'product.updated') {
    const product = event.data.object as Stripe.Product
    revalidateTag(`product-${product.id}`)
    revalidateTag('products')
  }

  return NextResponse.json({ received: true })
}
```

### Cache Monitoring

```tsx
// app/api/cache-status/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    cacheStats: {
      dataCache: 'active',
      routeCache: 'active',
      routerCache: 'active',
    },
    timestamp: Date.now(),
  })
}
```

## Real-World Use Cases

| Use Case | Caching Strategy |
|----------|-----------------|
| E-commerce products | ISR with 60s revalidation |
| Blog posts | ISR with on-demand revalidation |
| User dashboard | No cache (always fresh) |
| Static pages | Full Route Cache |
| API responses | Data Cache with tags |
| Search results | Data Cache with short revalidation |
| User preferences | No cache |
| Public data | Force cache with long revalidation |

## Common Mistakes

### 1. Caching Sensitive Data

```tsx
// ❌ BAD: Caching user-specific data
export default async function Dashboard() {
  const data = await fetch('https://api.example.com/dashboard', {
    next: { revalidate: 300 } // Cached for all users!
  })
  return <div>{data.privateInfo}</div>
}

// ✅ GOOD: Don't cache personalized data
export default async function Dashboard() {
  const data = await fetch('https://api.example.com/dashboard', {
    cache: 'no-store' // Always fresh
  })
  return <div>{data.privateInfo}</div>
}
```

### 2. Not Invalidating Stale Cache

```tsx
// ❌ BAD: Data never updates after mutation
export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 } // Hour-old data!
  })
  return <ProductList products={products} />
}

// ✅ GOOD: Use on-demand revalidation
export async function addProduct(product) {
  await db.product.create({ data: product })
  revalidateTag('products') // Invalidate cache
}
```

### 3. Over-Caching

```tsx
// ❌ BAD: Caching everything aggressively
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'force-cache' // Never updates!
  })
  return <div>{data.value}</div>
}

// ✅ GOOD: Cache appropriately
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 } // Updates every minute
  })
  return <div>{data.value}</div>
}
```

### 4. Not Handling Cache Errors

```tsx
// ❌ BAD: No error handling for cache misses
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 }
  })
  return <div>{data.value}</div> // What if fetch fails?
}

// ✅ GOOD: Handle errors gracefully
export default async function Page() {
  try {
    const data = await fetch('https://api.example.com/data', {
      next: { revalidate: 60 }
    })
    if (!data.ok) throw new Error('Failed to fetch')
    const json = await data.json()
    return <div>{json.value}</div>
  } catch (error) {
    return <div>Failed to load data</div>
  }
}
```

### 5. Mixing Cache Strategies Incorrectly

```tsx
// ❌ BAD: Conflicting cache settings
export const dynamic = 'force-dynamic' // No Full Route Cache
export const revalidate = 60 // But trying to ISR?

export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'force-cache' // And force cache?
  })
  return <div>{data.value}</div>
}

// ✅ GOOD: Consistent cache strategy
export const revalidate = 60 // ISR

export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 }
  })
  return <div>{data.value}</div>
}
```

## Best Practices

1. **Cache by default** — Start with caching, opt out when needed
2. **Use tags for granular invalidation** — More precise cache control
3. **Implement on-demand revalidation** — Update cache when data changes
4. **Cache at the right level** — Data cache for fetches, route cache for pages
5. **Monitor cache hit rates** — Track and optimize cache usage
6. **Handle cache misses gracefully** — Fallback for uncached content
7. **Use Request Memoization** — Deduplicate fetches automatically
8. **Implement proper error handling** — Cache failures shouldn't break the app
9. **Document caching strategies** — Team needs to understand the approach
10. **Test cache behavior** — Verify in development and production

## Performance Considerations

```text
Cache Performance Impact:
- First request: Normal performance (cache miss)
- Subsequent requests: Fast performance (cache hit)
- Revalidation: Background regeneration
- Cache invalidation: Triggers fresh fetch

Optimization:
- Set appropriate revalidation times
- Use on-demand revalidation for critical updates
- Implement cache warming for popular content
- Monitor cache hit rates
```

## Interview Questions

### Beginner (5-10)

1. **What are the caching layers in Next.js?**
   Request Memoization, Data Cache, Full Route Cache, and Router Cache. Each serves different purposes.

2. **What is the Data Cache?**
   Persistent cache for fetch results across requests. Can be revalidated by time or on-demand.

3. **What is the Full Route Cache?**
   Caches the entire rendered output of static routes. Stores React Server Component HTML/RSC payload.

4. **What is the Router Cache?**
   Client-side cache in the browser. Caches RSC payload for instant navigation.

5. **How do you enable caching?**
   Use `next.revalidate` for time-based caching, `cache: 'force-cache'` for permanent, or `cache: 'no-store'` for no caching.

6. **What is Request Memoization?**
   Automatic deduplication of fetch calls in the same request. If you fetch the same URL twice, it only runs once.

7. **How do you invalidate cache?**
   Use `revalidatePath()` or `revalidateTag()` for on-demand invalidation, or wait for time-based expiration.

8. **What is ISR?**
   Incremental Static Regeneration combines static generation with periodic revalidation, updating pages after build time.

### Intermediate (5-10)

9. **How does tag-based revalidation work?**
   Tag fetch calls with `next.tags`, then call `revalidateTag()` to invalidate all fetches with that tag.

10. **How do you cache API responses?**
    Use Cache-Control headers in Route Handlers, or `next.revalidate` in Server Components.

11. **What is the difference between `force-cache` and `revalidate`?**
    `force-cache` caches indefinitely until manually invalidated. `revalidate` caches for a specified time period.

12. **How do you handle cache for personalized content?**
    Don't cache personalized content, or use `cache: 'no-store'`. Cache only public, non-user-specific data.

13. **How do you implement cache warming?**
    Pre-fetch popular pages at build time, use ISR to keep them fresh, and implement background regeneration.

14. **What is the relationship between ISR and CDN caching?**
    ISR stores in Data Cache. CDN serves cached content. Revalidation triggers background regeneration at edge.

15. **How do you monitor cache performance?**
    Track cache hit rates, monitor revalidation frequency, and log cache misses for optimization.

### Senior (10-15)

16. **Design a caching strategy for an e-commerce platform.**
    Use ISR for product pages (60s revalidation), on-demand revalidation for inventory changes, no cache for cart/checkout, and CDN caching for static assets.

17. **How would you implement cache invalidation at scale?**
    Use tag-based invalidation, implement webhook handlers, use message queues for async invalidation, and monitor cache freshness.

18. **Explain the cache hierarchy and when to use each layer.**
    Request Memoization for deduplication, Data Cache for persistent fetches, Full Route Cache for static pages, Router Cache for client navigation.

19. **How do you handle cache consistency in distributed systems?**
    Implement cache versioning, use eventual consistency models, handle stale reads, and implement cache coherence protocols.

20. **Design a cache monitoring and alerting system.**
    Track hit rates, monitor latency, alert on anomalies, and implement dashboards for cache performance.

21. **How would you implement multi-region caching?**
    Use CDN edge caching, implement regional cache invalidation, handle data residency, and optimize for latency.

22. **Design a cache warming strategy for high-traffic events.**
    Predict popular content, pre-fetch at scale, implement background warming, and handle traffic spikes.

23. **How do you handle cache for real-time data?**
    Use short revalidation periods, implement WebSocket for live updates, and combine with client-side polling.

24. **Design a cache invalidation system with webhooks.**
    Handle webhook events, implement idempotent invalidation, use message queues, and ensure reliability.

25. **How would you implement cache for internationalized content?**
    Cache per locale, implement locale-based tags, handle language switching, and optimize for multi-language sites.

### FAANG-style (5-10)

26. **Design a distributed caching system for millions of pages.**
    Use multi-tier caching, implement cache sharding, handle cache stampedes, and optimize for consistency.

27. **How would you implement machine learning for cache optimization?**
    Predict cache hits, optimize revalidation timing, implement adaptive caching, and learn from access patterns.

28. **Design a cache system with automatic optimization.**
    Implement self-tuning caches, use heuristics for revalidation, and adapt to traffic patterns.

29. **How would you implement cache for a CDN at global scale?**
    Use edge caching, implement cache consistency across regions, handle failover, and optimize for latency.

30. **Design a cache system with fault tolerance.**
    Implement cache fallbacks, handle cache failures gracefully, use circuit breakers, and ensure availability.

### Follow-ups (5-10)

31. **What are the limitations of Next.js caching?**
    Limited to fetch API, no fine-grained cache control, and caching behavior can be confusing.

32. **How does caching affect debugging?**
    Cached responses may show stale data, making debugging difficult. Use cache bypass for debugging.

33. **What is the future of caching in Next.js?**
    Better cache controls, improved DevTools, and more granular invalidation options.

34. **How do you test caching behavior?**
    Test cache hits/misses, verify revalidation, monitor cache statistics, and test error scenarios.

35. **What security considerations apply to caching?**
    Don't cache sensitive data, implement cache poisoning prevention, and handle cache-based attacks.

36. **How do you handle cache for offline support?**
    Implement Service Worker caching, use IndexedDB for offline data, and handle sync when online.

37. **What are alternatives to Next.js caching?**
    CDN caching, Redis caching, browser caching, and custom caching solutions.

38. **How do you migrate caching strategies?**
    Analyze current caching, implement gradually, monitor performance, and adjust based on metrics.

## Summary

| Cache Layer | Location | Purpose | Revalidation |
|-------------|----------|---------|--------------|
| Request Memoization | Server (in-memory) | Deduplicate fetches | Per request |
| Data Cache | Server (persistent) | Cache fetch results | Time/On-demand |
| Full Route Cache | Server (persistent) | Cache rendered routes | Time/On-demand |
| Router Cache | Client (browser) | Cache RSC payload | Navigation |

## Cheat Sheet

```text
Data Cache options:
fetch(url)                              → Default caching
fetch(url, { cache: 'force-cache' })    → Cache indefinitely
fetch(url, { cache: 'no-store' })       → No caching
fetch(url, { next: { revalidate: 60 } }) → ISR (60s)
fetch(url, { next: { tags: ['tag'] } })  → Tag for invalidation

Route Config:
export const dynamic = 'force-dynamic'   → Disable Full Route Cache
export const dynamic = 'force-static'    → Enable Full Route Cache
export const revalidate = 60             → ISR for route
export const fetchCache = 'no-store'     → Disable fetch cache

Invalidation:
revalidatePath('/path')                  → Invalidate path
revalidateTag('tag')                     → Invalidate by tag

React cache():
import { cache } from 'react'
export const getData = cache(async () => { ... })
```

## References & Learn More

- [Next.js Docs: Caching](https://nextjs.org/docs/app/building-your-application/caching)
- [Data Cache in Next.js](https://nextjs.org/docs/app/building-your-application/caching#data-cache)
- [Caching in Next.js](https://nextjs.org/blog/next-14#caching-revalidated)
