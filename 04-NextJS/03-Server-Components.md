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

## Interview Questions

### Beginner (5-10)

1. **What is a Server Component?**
   A Server Component renders on the server and sends only HTML to the client. It can't use React hooks or browser APIs but can directly access databases and files.

2. **How do Server Components differ from Client Components?**
   Server Components render on the server with zero client JS. Client Components render on the client with full interactivity. Server Components are the default in App Router.

3. **Why can't Server Components use useState?**
   useState is a client-side hook. Server Components execute once on the server and don't maintain state. Use Client Components for stateful UI.

4. **What are the benefits of Server Components?**
   Reduced bundle size, direct data access, better security, faster initial rendering, and streaming capabilities.

5. **How do you make a component a Server Component?**
   In App Router, all components are Server Components by default. No special directive needed.

6. **Can Server Components fetch data?**
   Yes, directly! No useEffect or API routes needed. Just use async/await with fetch, databases, or any data source.

7. **How do Server Components handle errors?**
   Errors throw in Server Components are caught by the nearest `error.tsx` boundary. Use `notFound()` for 404 errors.

8. **What is the relationship between Server Components and streaming?**
   Server Components can be wrapped in Suspense to stream HTML progressively. Fast components render first, slow ones stream in later.

### Intermediate (5-10)

9. **How do Server Components and Client Components compose?**
   Server Components can import Client Components, but not vice versa. Client Components receive Server Components as `children` or `props`.

10. **What is the component composition pattern?**
    Server Components at the top fetch data and compose the page. Client Components handle specific interactive elements. This minimizes client-side JavaScript.

11. **How do you pass data from Server to Client Components?**
    Use props — but only serializable data (no functions, no Date objects, no Maps/Sets). Convert complex types to plain objects.

12. **Can Server Components use context?**
    Not React Context directly. Use `headers()`, `cookies()`, or `params` for server-side context. Client Components can use React Context normally.

13. **How do Server Components affect SEO?**
    Excellent SEO — content is rendered on the server, so crawlers see full HTML without executing JavaScript.

14. **What is the `async` keyword in Server Components?**
    Server Components can be async functions, allowing direct use of await for data fetching. This is not possible in Client Components.

15. **How do you test Server Components?**
    Use `@testing-library/react` with a server rendering mock, or test the data fetching logic separately. Integration tests are most valuable.

### Senior (10-15)

16. **Design a data fetching architecture using Server Components.**
    Use a composition pattern: top-level Server Component orchestrates data fetching, child Server Components fetch their own data, wrap each in Suspense for streaming. Use React cache() for deduplication.

17. **How would you implement optimistic updates with Server Components?**
    Use Server Actions for mutations, client-side state for optimistic updates, and revalidateTag/revalidatePath to refresh Server Component data.

18. **Explain the Server Component rendering pipeline in detail.**

    1. Server receives request

    2. React tree walks Server Components

    3. Each async Server Component awaits data

    4. HTML is generated and streamed

    5. Client receives and displays HTML

    6. Client Components hydrate separately

19. **How do Server Components interact with caching?**
    Server Components can use fetch with cache options, React cache() for deduplication, and revalidation strategies. The Full Route Cache stores rendered output.

20. **Design a system for real-time updates with Server Components.**
    Use Server Components for initial render, WebSocket/SSE for live updates via Client Components, and revalidation for periodic data refresh.

21. **How do you handle complex state management with Server Components?**
    Keep state in Client Components. Use URL state for shared state. Server Components handle data fetching and initial state. Use Server Actions for mutations.

22. **Explain the security implications of Server Components.**
    Sensitive logic stays on the server, no API keys in bundles, direct database access is safe. But be careful not to leak secrets through props or errors.

23. **How would you implement a micro-frontend with Server Components?**
    Use Module Federation or import maps, each micro-frontend as a Server Component tree, with shared layouts and parallel routes for composition.

24. **Design a performance monitoring system for Server Components.**
    Track render times, data fetching duration, cache hit rates, streaming performance. Use React DevTools profiling and custom performance marks.

25. **How do Server Components affect bundle analysis?**
    Server Components don't appear in client bundles. Use `next build` output to verify. Client Components should be isolated and code-split.

### FAANG-style (5-10)

26. **Design a Server Component architecture that handles 1M+ concurrent users.**
    Use edge rendering, implement connection pooling for databases, use streaming for progressive rendering, and leverage CDN caching for static Server Component output.

27. **How would you implement A/B testing with Server Components?**
    Use middleware to detect variants, Server Components to render variant-specific content, and cache each variant separately with ISR.

28. **Design a system for Server Component composition across microservices.**
    Use Federation patterns, each microservice exports Server Components, compose them in a shell application, and handle cross-service data dependencies.

29. **How would you optimize Server Component performance for slow databases?**
    Use connection pooling, implement query optimization, use streaming to show partial results, and cache aggressively with ISR.

30. **Design a Server Component architecture for global distribution.**
    Use edge functions for geo-routing, replicate databases regionally, implement smart caching, and use streaming to minimize latency.

### Follow-ups (5-10)

31. **What are the limitations of Server Components?**
    No hooks, no browser APIs, no context, serialization constraints, debugging complexity, and learning curve.

32. **How do Server Components affect debugging?**
    Server-side errors don't appear in browser console. Use server logs, React DevTools, and error boundaries for debugging.

33. **What is the future of Server Components?**
    Better DevTools, improved streaming, more server-side APIs, and deeper integration with React features.

34. **How do Server Components interact with Service Workers?**
    Server Components don't affect Service Workers directly. Service Workers cache client-side assets, not server-rendered HTML.

35. **What is the relationship between Server Components and React Server Actions?**
    Server Actions are Server Components that can be called from Client Components. They enable mutations without API routes.

36. **How do you migrate existing Client Components to Server Components?**
    Identify components that don't need interactivity, move data fetching to Server Components, and isolate truly interactive parts as Client Components.

37. **What testing strategies work best for Server Components?**
    Test data fetching logic separately, use integration tests for full pages, mock external services, and test error handling scenarios.

38. **How do Server Components affect accessibility?**
    Server-rendered HTML is immediately accessible. No FOUC or layout shift from hydration. Better for screen readers and assistive technologies.

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

## References & Learn More

- [React Server Components: A Comprehensive Guide](https://www.pluralsight.com/guides/server-side-rendering-with-react)
- [Server Components Explained](https://www.joshwcomeau.com/react/server-components/)
- [Next.js: Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
