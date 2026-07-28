---
section: Next.js
category: Frontend
tags: [concept]
---

# Server Components in Next.js

## Definition

**Server Components** are React components that render on the server and send only the HTML (and minimal JavaScript) to the client. They cannot use React hooks like `useState`, `useEffect`, or browser APIs. In Next.js App Router, all components are Server Components by default.

## Why Do We Need It?

1. **Reduced bundle size** — Server Components don't ship JavaScript to the client

2. **Direct data access** — Can query databases, read files, access secrets without API layers

3. **Better performance** — Server rendering is faster than client-side data fetching

4. **Security** — Sensitive logic stays on the server

5. **Streaming** — Can progressively render and stream HTML to the client

## How It Works

### Server vs Client Component Rendering

```text
┌─────────────────────────────────────────────────────────────────┐
│                    SERVER COMPONENT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Server                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. Execute component function                          │    │
│  │  2. Fetch data (direct DB/API access)                   │    │
│  │  3. Render to HTML                                      │    │
│  │  4. Send HTML to client                                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  Client                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Receive HTML → Display (no JS needed for this part)    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Bundle impact: ZERO JavaScript sent                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT COMPONENT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Server                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. Execute component (minimal)                         │    │
│  │  2. Render placeholder/skeleton                         │    │
│  │  3. Send HTML shell + JavaScript bundle                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  Client                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. Receive HTML shell                                  │    │
│  │  2. Download JavaScript bundle                          │    │
│  │  3. Execute JavaScript (hydration)                      │    │
│  │  4. Fetch data (if needed)                              │    │
│  │  5. Render interactive UI                               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Bundle impact: Full component JavaScript sent                  │
└─────────────────────────────────────────────────────────────────┘

```

### Component Composition Pattern

```text
┌─────────────────────────────────────────────────────────────────┐
│                      Page (Server Component)                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │        Header (Server Component)                  │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │        ProductList (Server Component)             │   │    │
│  │  │  ┌────────────────────────────────────────────┐  │   │    │
│  │  │  │     ProductCard (Server Component)          │  │   │    │
│  │  │  │  ┌──────────────────────────────────────┐  │  │   │    │
│  │  │  │  │   AddToCartButton (Client Component)  │  │  │   │    │
│  │  │  │  └──────────────────────────────────────┘  │  │   │    │
│  │  │  └────────────────────────────────────────────┘  │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                         │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │        Footer (Server Component)                  │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Server Component

```tsx
// app/page.tsx — Server Component by default
import { db } from '@/lib/database'

export default async function HomePage() {
  // Direct database access — no API layer needed!
  const posts = await db.post.findMany({
    orderBy: { createdAt: 'desc' },
    take: 10,
  })

  return (
    <div>
      <h1>Latest Posts</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
          <time>{post.createdAt.toLocaleDateString()}</time>
        </article>
      ))}
    </div>
  )
}

```

### Server Component with Data Fetching

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'
import { AnalyticsChart } from './analytics-chart'
import { RecentActivity } from './recent-activity'
import { StatsOverview } from './stats-overview'

export default async function DashboardPage() {
  return (
    <div className="grid grid-cols-12 gap-6">
      <div className="col-span-12">
        <h1>Dashboard</h1>
      </div>

      {/* Each section streams independently */}
      <div className="col-span-4">
        <Suspense fallback={<StatsSkeleton />}>
          <StatsOverview />
        </Suspense>
      </div>

      <div className="col-span-8">
        <Suspense fallback={<ChartSkeleton />}>
          <AnalyticsChart />
        </Suspense>
      </div>

      <div className="col-span-12">
        <Suspense fallback={<ActivitySkeleton />}>
          <RecentActivity />
        </Suspense>
      </div>
    </div>
  )
}

```

### Nested Server Components

```tsx
// app/products/page.tsx — Parent Server Component
import { ProductCard } from './product-card'
import { db } from '@/lib/database'

export default async function ProductsPage() {
  const products = await db.product.findMany()

  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

```

```tsx
// app/products/product-card.tsx — Child Server Component
import { AddToCartButton } from './add-to-cart-button'

interface ProductCardProps {
  product: {
    id: string
    name: string
    price: number
    image: string
  }
}

// Server Component — can access database directly
export async function ProductCard({ product }: ProductCardProps) {
  // Could fetch additional data here
  const reviews = await db.review.findMany({
    where: { productId: product.id },
    take: 3,
  })

  return (
    <div className="border rounded-lg overflow-hidden">
      <img src={product.image} alt={product.name} />
      <div className="p-4">
        <h3>{product.name}</h3>
        <p>${product.price}</p>
        <div className="stars">
          {/* Render reviews */}
        </div>
        {/* Client Component for interactivity */}
        <AddToCartButton productId={product.id} />
      </div>
    </div>
  )
}

```

### Server Component with External API

```tsx
// app/github/page.tsx
import { Suspense } from 'react'

async function GitHubRepos() {
  const res = await fetch('https://api.github.com/users/facebook/repos', {
    next: { revalidate: 3600 } // Cache for 1 hour
  })
  const repos = await res.json()

  return (
    <ul>
      {repos.map((repo: any) => (
        <li key={repo.id}>
          <a href={repo.html_url}>{repo.name}</a>
          <span>{repo.stargazers_count} ⭐</span>
        </li>
      ))}
    </ul>
  )
}

export default function GitHubPage() {
  return (
    <div>
      <h1>Facebook Repos</h1>
      <Suspense fallback={<div>Loading repos...</div>}>
        <GitHubRepos />
      </Suspense>
    </div>
  )
}

```

### Streaming Server Components

```tsx
// app/streaming/page.tsx
import { Suspense } from 'react'

// Slow data fetch
async function SlowComponent() {
  await new Promise(resolve => setTimeout(resolve, 3000))
  const data = await fetchExpensiveData()

  return <div>{data.map(item => <p key={item.id}>{item.name}</p>)}</div>
}

// Fast data fetch
async function FastComponent() {
  const data = await fetchQuickData()
  return <div>{data.summary}</div>
}

export default function StreamingPage() {
  return (
    <div>
      <h1>Streaming Demo</h1>

      {/* Fast component renders first */}
      <Suspense fallback={<div>Loading summary...</div>}>
        <FastComponent />
      </Suspense>

      {/* Slow component streams in when ready */}
      <Suspense fallback={<div>Loading detailed data...</div>}>
        <SlowComponent />
      </Suspense>
    </div>
  )
}

```

### Server Component with Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

interface BlogPost {
  title: string
  content: string
  author: string
  publishedAt: string
}

async function getPost(slug: string): Promise<BlogPost> {
  const res = await fetch(`https://api.example.com/posts/${slug}`)
  return res.json()
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)

  return {
    title: post.title,
    description: post.content.substring(0, 160),
    openGraph: {
      title: post.title,
      description: post.content.substring(0, 160),
      authors: [post.author],
    },
  }
}

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = await getPost(slug)

  return (
    <article>
      <h1>{post.title}</h1>
      <p>By {post.author}</p>
      <time>{post.publishedAt}</time>
      <div>{post.content}</div>
    </article>
  )
}

```

### Error Handling in Server Components

```tsx
// app/dashboard/page.tsx
import { notFound } from 'next/navigation'

async function getUser(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}`)

  if (res.status === 404) {
    notFound() // Triggers nearest not-found.tsx
  }

  if (!res.ok) {
    throw new Error('Failed to fetch user') // Triggers error.tsx
  }

  return res.json()
}

export default async function DashboardPage() {
  const user = await getUser('123')

  return (
    <div>
      <h1>Welcome, {user.name}</h1>
    </div>
  )
}

```

### Server Component with Context

```tsx
// lib/user-context.tsx
import { cookies } from 'next/headers'
import { db } from '@/lib/database'

export async function getCurrentUser() {
  const cookieStore = await cookies()
  const sessionId = cookieStore.get('session')?.value

  if (!sessionId) return null

  const session = await db.session.findUnique({
    where: { id: sessionId },
    include: { user: true },
  })

  return session?.user ?? null
}

```

```tsx
// app/dashboard/page.tsx
import { getCurrentUser } from '@/lib/user-context'

export default async function DashboardPage() {
  const user = await getCurrentUser()

  if (!user) {
    return <div>Please log in</div>
  }

  return (
    <div>
      <h1>Dashboard for {user.name}</h1>
    </div>
  )
}

```

### Server Component Composition Pattern

```tsx
// app/page.tsx — Composition pattern for data fetching
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <Header />
      <main>
        <Suspense fallback={<PostListSkeleton />}>
          <PostList />
        </Suspense>
      </main>
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />
      </Suspense>
      <Footer />
    </div>
  )
}

// Each component fetches its own data
async function Header() {
  const user = await getUser()
  return <header>{user?.name || 'Guest'}</header>
}

async function PostList() {
  const posts = await getPosts()
  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  )
}

async function Sidebar() {
  const categories = await getCategories()
  return (
    <aside>
      {categories.map(cat => <div key={cat.id}>{cat.name}</div>)}
    </aside>
  )
}

function Footer() {
  return <footer>© 2024</footer>
}

```

## Real-World Use Cases

| Use Case | Server Component Benefit |
|----------|------------------------|
| Blog/Content pages | Direct CMS access, no API layer |
| E-commerce product pages | Database queries, SEO optimization |
| Dashboard overview | Aggregate data without client fetching |
| Documentation | Static generation with dynamic data |
| User profiles | Secure data access with session handling |
| Search results | Server-side filtering and pagination |
| Admin panels | Secure operations without exposing APIs |
| Landing pages | Fast rendering, minimal JS |

## Common Mistakes

### 1. Using useState/useEffect in Server Components

```tsx
// ❌ BAD: Hooks don't work in Server Components
export default async function Page() {
  const [count, setCount] = useState(0) // Error!
  useEffect(() => { /* ... */ }, []) // Error!

  return <div>{count}</div>
}

// ✅ GOOD: Use Client Component for interactivity
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// Keep page as Server Component
import { Counter } from './counter'

export default function Page() {
  return (
    <div>
      <h1>Counting</h1>
      <Counter />
    </div>
  )
}

```

### 2. Passing Functions as Props

```tsx
// ❌ BAD: Can't pass functions from Server to Client Components
async function Page() {
  const handleClick = () => console.log('clicked') // Can't pass this!

  return <ClientButton onClick={handleClick} />
}

// ✅ GOOD: Define the handler in the Client Component
'use client'
export function ClientButton() {
  const handleClick = () => console.log('clicked')
  return <button onClick={handleClick}>Click me</button>
}

```

### 3. Accessing Browser APIs

```tsx
// ❌ BAD: Browser APIs don't exist on the server
export default async function Page() {
  const width = window.innerWidth // Error!
  const localStorage = window.localStorage // Error!

  return <div>Width: {width}</div>
}

// ✅ GOOD: Use useEffect for browser APIs
'use client'
import { useState, useEffect } from 'react'

export function BrowserInfo() {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    setWidth(window.innerWidth)
  }, [])

  return <div>Width: {width}</div>
}

```

### 4. Not Handling Loading States

```tsx
// ❌ BAD: Slow data fetch blocks entire page
export default async function Page() {
  const data = await fetchSlowData() // 3 second delay
  return <div>{data.items.map(...)}</div> // User waits 3 seconds
}

// ✅ GOOD: Use Suspense for streaming
export default function Page() {
  return (
    <div>
      <h1>Fast content renders immediately</h1>
      <Suspense fallback={<Loading />}>
        <SlowDataComponent />
      </Suspense>
    </div>
  )
}

```

### 5. Exposing Sensitive Data

```tsx
// ❌ BAD: Leaking secrets to client
export default async function Page() {
  const apiKey = process.env.API_KEY
  return <div>{apiKey}</div> // Exposed!
}

// ✅ GOOD: Only pass safe data
export default async function Page() {
  const apiKey = process.env.API_KEY
  const data = await fetchWithKey(apiKey) // Key stays on server
  return <div>{data.publicField}</div> // Only public data
}

```

## Best Practices

1. **Default to Server Components** — Only use `'use client'` when interactivity is needed

2. **Compose with Suspense** — Stream slow data fetches without blocking the page

3. **Keep data fetching close to usage** — Each component fetches its own data

4. **Use Server Components for data access** — Avoid unnecessary API layers

5. **Isolate Client Components** — Keep them small and specific

6. **Use error boundaries** — Handle failures gracefully per route

7. **Cache data appropriately** — Use `next.revalidate` or `cache: 'force-cache'`

8. **Avoid over-fetching** — Fetch only what each component needs

9. **Use `notFound()` for missing data** — Trigger 404 pages properly
10. **Test both component types** — Server and Client Components behave differently

## Performance Considerations

### Bundle Size Comparison

```text
Server Component:

- Component code: 0 bytes to client
- Data fetching: 0 bytes to client
- Dependencies: 0 bytes to client
- Total: Minimal HTML only

Client Component:

- Component code: ~2-5KB minified
- React runtime: ~40KB gzipped
- Dependencies: Variable
- Total: Full JavaScript bundle

```

### Rendering Performance

```text
Server Component Rendering:

1. Server executes (fast, no network latency)

2. Data fetching (parallelized)

3. HTML generation (fast)

4. Stream to client (progressive)

Client Component Rendering:

1. Server renders placeholder (fast)

2. HTML shell sent (fast)

3. JavaScript downloads (network dependent)

4. Hydration (CPU intensive)

5. Data fetching (network dependent)

6. Re-render (CPU intensive)

```

## Summary

| Aspect | Server Component | Client Component |
|--------|-----------------|------------------|
| Renders | Server | Client |
| JS Bundle | 0 bytes | Full component |
| Hooks | No | Yes |
| Browser APIs | No | Yes |
| Data Access | Direct | Via API |
| Interactivity | No | Yes |
| Streaming | Yes | Via Suspense |
| Default | Yes | No |

## Cheat Sheet
```text
Server Component (default):

- async function
- Direct data access
- No useState/useEffect
- No browser APIs
- Zero client JS

Client Component:
'use client' directive

- useState/useEffect
- Event handlers
- Browser APIs
- Full interactivity

Composition:
Server → can import → Client ✅
Client → can import → Server ❌
Client → receives Server as children ✅

Data Passing:
Server → Client: Props (serializable only)
Client → Server: Server Actions

```

---

## See Also
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [React Server Components: A Comprehensive Guide](https://www.pluralsight.com/guides/server-side-rendering-with-react)
- [Server Components Explained](https://www.joshwcomeau.com/react/server-components/)
- [Next.js: Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
