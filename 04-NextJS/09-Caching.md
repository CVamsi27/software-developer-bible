---
section: Next.js
category: Frontend
tags: [concept]
---

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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

---

## See Also
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Next.js Docs: Caching](https://nextjs.org/docs/app/building-your-application/caching)
- [Data Cache in Next.js](https://nextjs.org/docs/app/building-your-application/caching#data-cache)
- [Caching in Next.js](https://nextjs.org/blog/next-14#caching-revalidated)
