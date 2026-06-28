# Streaming in Next.js

## Definition

**Streaming** in Next.js allows you to progressively render and send HTML from the server to the client. Instead of waiting for all data to load before rendering, the server sends the page shell immediately and streams in slower components as they become ready.

## Why Do We Need It?

1. **Faster Time to First Byte (TTFB)** — Users see content immediately
2. **Better user experience** — Progressive loading instead of blank screens
3. **Parallel data fetching** — Multiple data sources load simultaneously
4. **Improved Core Web Vitals** — Better LCP and FCP scores
5. **Reduced latency** — Content appears as it becomes available

## How It Works

### Traditional vs Streaming Rendering

```text
┌─────────────────────────────────────────────────────────────────┐
│               TRADITIONAL RENDERING (Non-Streaming)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Server                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  1. Fetch Data A (2 seconds)                            │   │
│  │  2. Fetch Data B (3 seconds)                            │   │
│  │  3. Fetch Data C (1 second)                             │   │
│  │  4. Render complete page (6 seconds total)              │   │
│  │  5. Send HTML to client                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼ (After 6 seconds)                │
│  Client                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Display complete page                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   STREAMING RENDERING                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Server                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  1. Send shell immediately (Header, Layout)             │   │
│  │  2. Start Data A fetch (2 seconds)                      │   │
│  │  3. Start Data B fetch (3 seconds)                      │   │
│  │  4. Start Data C fetch (1 second)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼ (Immediately)                                          │
│  Client                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Display: Header + Layout + Loading placeholders        │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼ (After 1 second)                                       │
│  Server streams Data C                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Send Data C content                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼                                                        │
│  Client                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Replace Data C loading with actual content              │   │
│  └─────────────────────────────────────────────────────────┘   │
│        │                                                        │
│        ▼ (After 2 seconds)                                      │
│  Server streams Data A                                          │
│        │                                                        │
│        ▼ (After 3 seconds)                                      │
│  Server streams Data B                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  All content loaded progressively!                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Streaming Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMING ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HTML Shell (sent immediately)                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  <html>                                                  │   │
│  │    <body>                                                │   │
│  │      <nav>...</nav>                                      │   │
│  │      <main>                                              │   │
│  │        <!-- Suspense boundary 1 -->                       │   │
│  │        <div class="skeleton">Loading...</div>            │   │
│  │        <!-- Suspense boundary 2 -->                       │   │
│  │        <div class="skeleton">Loading...</div>            │   │
│  │        <!-- Suspense boundary 3 -->                       │   │
│  │        <div class="skeleton">Loading...</div>            │   │
│  │      </main>                                             │   │
│  │    </body>                                               │   │
│  │  </html>                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Streamed Content (sent as ready)                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  <script>                                                │   │
│  │    // Replace suspense boundary 1 with actual content    │   │
│  │    $RC("boundary-1-id", "actual-content-id")             │   │
│  │  </script>                                               │   │
│  │  <div id="actual-content-id">                            │   │
│  │    <!-- Actual content for boundary 1 -->                 │   │
│  │  </div>                                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Streaming with loading.tsx

```tsx
// app/dashboard/page.tsx — Server Component
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      {/* This content renders immediately */}
      <p>Welcome to your dashboard</p>

      {/* These stream in as they load */}
      <Suspense fallback={<StatsLoading />}>
        <Stats />
      </Suspense>

      <Suspense fallback={<ChartLoading />}>
        <AnalyticsChart />
      </Suspense>

      <Suspense fallback={<ActivityLoading />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}

// loading.tsx provides automatic Suspense boundary
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/3 mb-4" />
      <div className="h-4 bg-gray-200 rounded w-full mb-2" />
      <div className="h-4 bg-gray-200 rounded w-2/3" />
    </div>
  )
}
```

### Multiple Suspense Boundaries

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-12 gap-6">
      {/* Header renders immediately */}
      <div className="col-span-12">
        <h1>Dashboard</h1>
      </div>

      {/* Stats section streams independently */}
      <div className="col-span-4">
        <Suspense fallback={<StatsSkeleton />}>
          <StatsOverview />
        </Suspense>
      </div>

      {/* Chart section streams independently */}
      <div className="col-span-8">
        <Suspense fallback={<ChartSkeleton />}>
          <AnalyticsChart />
        </Suspense>
      </div>

      {/* Activity section streams independently */}
      <div className="col-span-12">
        <Suspense fallback={<ActivitySkeleton />}>
          <RecentActivity />
        </Suspense>
      </div>
    </div>
  )
}

async function StatsOverview() {
  const stats = await fetchStats() // 2 seconds
  return (
    <div className="border rounded-lg p-4">
      <h2>Stats</h2>
      <p>Total Users: {stats.users}</p>
      <p>Revenue: ${stats.revenue}</p>
    </div>
  )
}

async function AnalyticsChart() {
  const data = await fetchAnalytics() // 3 seconds
  return (
    <div className="border rounded-lg p-4">
      <h2>Analytics</h2>
      <Chart data={data} />
    </div>
  )
}

async function RecentActivity() {
  const activity = await fetchActivity() // 1 second
  return (
    <div className="border rounded-lg p-4">
      <h2>Recent Activity</h2>
      {activity.map(item => (
        <div key={item.id}>{item.description}</div>
      ))}
    </div>
  )
}
```

### Nested Streaming

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<DashboardSkeleton />}>
        <DashboardContent />
      </Suspense>
    </div>
  )
}

async function DashboardContent() {
  // This component streams in
  const user = await getUser()

  return (
    <div>
      <p>Welcome, {user.name}</p>

      {/* Nested Suspense for deeper streaming */}
      <Suspense fallback={<OrdersSkeleton />}>
        <UserOrders userId={user.id} />
      </Suspense>

      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations userId={user.id} />
      </Suspense>
    </div>
  )
}
```

### Streaming with Error Handling

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<Loading />}>
        <DashboardData />
      </Suspense>
    </div>
  )
}

// error.tsx handles errors in Suspense boundaries
// app/dashboard/error.tsx
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

async function DashboardData() {
  try {
    const data = await fetchDashboardData()
    return <div>{data.content}</div>
  } catch (error) {
    throw error // Will be caught by error.tsx
  }
}
```

### Streaming with loading.tsx and error.tsx

```tsx
// app/products/loading.tsx
export default function Loading() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="animate-pulse">
          <div className="h-48 bg-gray-200 rounded mb-4" />
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
          <div className="h-4 bg-gray-200 rounded w-1/2" />
        </div>
      ))}
    </div>
  )
}

// app/products/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="text-center py-10">
      <h2 className="text-2xl font-bold mb-4">Failed to load products</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={() => reset()}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Try again
      </button>
    </div>
  )
}

// app/products/page.tsx
import { Suspense } from 'react'

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      <Suspense fallback={<ProductsLoading />}>
        <ProductGrid />
      </Suspense>
    </div>
  )
}
```

### Parallel Streaming

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* All these stream in parallel */}
      <div className="grid grid-cols-2 gap-4">
        <Suspense fallback={<Skeleton />}>
          <SlowComponentA /> {/* Takes 3 seconds */}
        </Suspense>

        <Suspense fallback={<Skeleton />}>
          <SlowComponentB /> {/* Takes 2 seconds */}
        </Suspense>

        <Suspense fallback={<Skeleton />}>
          <SlowComponentC /> {/* Takes 4 seconds */}
        </Suspense>

        <Suspense fallback={<Skeleton />}>
          <SlowComponentD /> {/* Takes 1 second */}
        </Suspense>
      </div>
    </div>
  )
}

// Each component streams independently
async function SlowComponentA() {
  await new Promise(resolve => setTimeout(resolve, 3000))
  const data = await fetchDataA()
  return <div>Component A: {data.value}</div>
}

async function SlowComponentB() {
  await new Promise(resolve => setTimeout(resolve, 2000))
  const data = await fetchDataB()
  return <div>Component B: {data.value}</div>
}
```

### Selective Streaming

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      {/* Fast content renders immediately */}
      <Header />

      <main>
        {/* Slow content streams in */}
        <Suspense fallback={<SlowContentSkeleton />}>
          <SlowContent />
        </Suspense>
      </main>

      {/* Fast footer renders immediately */}
      <Footer />
    </div>
  )
}

function Header() {
  return <header>Dashboard Header</header>
}

function Footer() {
  return <footer>Dashboard Footer</footer>
}

async function SlowContent() {
  const data = await fetchSlowData() // 5 seconds
  return <div>{data.content}</div>
}
```

### Streaming with Progressive Enhancement

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Essential content renders first */}
      <DashboardSummary />

      {/* Detailed content streams in */}
      <Suspense fallback={<DetailsSkeleton />}>
        <DashboardDetails />
      </Suspense>

      {/* Charts stream in last */}
      <Suspense fallback={<ChartsSkeleton />}>
        <DashboardCharts />
      </Suspense>
    </div>
  )
}

async function DashboardSummary() {
  const summary = await fetchSummary() // Fast
  return (
    <div className="summary">
      <p>Total: {summary.total}</p>
      <p>Active: {summary.active}</p>
    </div>
  )
}

async function DashboardDetails() {
  const details = await fetchDetails() // Slow
  return (
    <div className="details">
      {details.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  )
}

async function DashboardCharts() {
  const chartData = await fetchChartData() // Very slow
  return <Chart data={chartData} />
}
```

## Real-World Use Cases

| Use Case | Streaming Benefit |
|----------|------------------|
| Dashboard | Stats load first, charts stream in |
| E-commerce | Product info first, reviews stream in |
| Blog | Article loads first, comments stream in |
| Search results | Results appear as found |
| Social feed | Posts stream in progressively |
| Admin panel | Overview first, details stream in |
| Analytics | Summary first, detailed charts stream in |

## Common Mistakes

### 1. Not Using Suspense Boundaries

```tsx
// ❌ BAD: No Suspense boundaries
export default function Page() {
  return (
    <div>
      <h1>Page</h1>
      <SlowComponent /> {/* Blocks entire page */}
    </div>
  )
}

// ✅ GOOD: Wrap in Suspense
export default function Page() {
  return (
    <div>
      <h1>Page</h1>
      <Suspense fallback={<Loading />}>
        <SlowComponent />
      </Suspense>
    </div>
  )
}
```

### 2. Making Everything a Suspense Boundary

```tsx
// ❌ BAD: Too many boundaries
export default function Page() {
  return (
    <div>
      <Suspense fallback={<Loading />}>
        <Header />
      </Suspense>
      <Suspense fallback={<Loading />}>
        <Navigation />
      </Suspense>
      <Suspense fallback={<Loading />}>
        <Content />
      </Suspense>
      <Suspense fallback={<Loading />}>
        <Footer />
      </Suspense>
    </div>
  )
}

// ✅ GOOD: Strategic boundaries for slow content
export default function Page() {
  return (
    <div>
      <Header /> {/* Fast, no boundary needed */}
      <Navigation /> {/* Fast, no boundary needed */}
      <Suspense fallback={<ContentSkeleton />}>
        <Content /> {/* Slow, needs boundary */}
      </Suspense>
      <Footer /> {/* Fast, no boundary needed */}
    </div>
  )
}
```

### 3. Not Handling Loading States

```tsx
// ❌ BAD: No loading state
export default function Page() {
  return (
    <div>
      <h1>Page</h1>
      <Suspense>
        <SlowComponent />
      </Suspense>
    </div>
  )
}

// ✅ GOOD: Always provide fallback
export default function Page() {
  return (
    <div>
      <h1>Page</h1>
      <Suspense fallback={<LoadingSkeleton />}>
        <SlowComponent />
      </Suspense>
    </div>
  )
}
```

### 4. Streaming Too Much Content

```tsx
// ❌ BAD: Streaming everything
export default function Page() {
  return (
    <div>
      <Suspense fallback={<Loading />}>
        <EntirePage /> {/* Too much content to stream */}
      </Suspense>
    </div>
  )
}

// ✅ GOOD: Stream only slow parts
export default function Page() {
  return (
    <div>
      <Header /> {/* Fast */}
      <Suspense fallback={<Loading />}>
        <SlowData /> {/* Only slow data streams */}
      </Suspense>
      <Footer /> {/* Fast */}
    </div>
  )
}
```

### 5. Not Using loading.tsx

```tsx
// ❌ BAD: Manual Suspense everywhere
export default function Page() {
  return (
    <div>
      <Suspense fallback={<Loading />}>
        <Content />
      </Suspense>
    </div>
  )
}

// ✅ GOOD: Use loading.tsx for route-level loading
// app/page.tsx
export default function Page() {
  return <Content />
}

// app/loading.tsx
export default function Loading() {
  return <LoadingSkeleton />
}
```

## Best Practices

1. **Use loading.tsx for route-level loading** — Automatic Suspense boundary
2. **Strategic Suspense boundaries** — Only for slow content
3. **Provide meaningful loading states** — Skeletons, not spinners
4. **Parallel streaming** — Multiple Suspense boundaries stream simultaneously
5. **Error boundaries** — Handle errors per Suspense boundary
6. **Progressive enhancement** — Fast content first, slow content streams in
7. **Test streaming behavior** — Verify in development and production
8. **Monitor performance** — Track streaming metrics
9. **Optimize data fetching** — Parallel fetches for faster streaming
10. **Use nested streaming** — For complex page hierarchies

## Performance Considerations

```text
Streaming Performance Benefits:
- TTFB: Immediate (shell sent first)
- FCP: Fast (essential content renders)
- LCP: Progressive (main content streams)
- CLS: Minimal (skeletons prevent layout shift)

Optimization:
- Parallel data fetching
- Strategic Suspense boundaries
- Loading state design
- Error handling per boundary
```

## Interview Questions

### Beginner (5-10)

1. **What is streaming in Next.js?**
   Streaming allows progressive rendering where the server sends the page shell immediately and streams in slower components as they load.

2. **How do you enable streaming?**
   Use `loading.tsx` for automatic Suspense boundaries, or wrap components in `<Suspense>` with a fallback.

3. **What is a Suspense boundary?**
   A boundary that shows a fallback UI while its children load. When children are ready, they replace the fallback.

4. **What is `loading.tsx`?**
   A file that automatically wraps the route in a Suspense boundary. It shows while the route's content loads.

5. **How does streaming improve performance?**
   It reduces TTFB by sending the shell immediately, and improves FCP by showing essential content first.

6. **What should you put in loading.tsx?**
   Skeleton loaders, placeholders, or loading indicators that match the layout of the actual content.

7. **Can you have multiple Suspense boundaries?**
   Yes! Multiple boundaries can stream independently, showing loading states for different parts of the page.

8. **What is the relationship between streaming and SSR?**
   Streaming is an enhancement to SSR that allows progressive rendering instead of waiting for all data before sending HTML.

### Intermediate (5-10)

9. **How do you handle errors in streaming?**
   Use `error.tsx` files alongside `loading.tsx`. Each Suspense boundary can have its own error handling.

10. **How do you design good loading states?**
    Use skeleton loaders that match the final layout, avoid layout shift, and provide meaningful feedback.

11. **What is nested streaming?**
    Suspense boundaries inside other Suspense boundaries, allowing hierarchical progressive loading.

12. **How does streaming affect Core Web Vitals?**
    Improves TTFB and FCP by sending content progressively. Can improve LCP by prioritizing main content.

13. **How do you test streaming behavior?**
    Use throttled network in dev tools, simulate slow data fetches, and verify progressive loading.

14. **What is the relationship between streaming and caching?**
    Cached content renders immediately, uncached content streams. Streaming works with ISR and SSR.

15. **How do you handle streaming with client components?**
    Client components hydrate after the shell loads. Use `'use client'` only for interactive parts.

### Senior (10-15)

16. **Design a streaming architecture for a complex dashboard.**
    Use nested Suspense boundaries, prioritize critical data, stream charts and secondary data, and implement error recovery.

17. **How would you implement streaming with real-time data?**
    Use Server Components for initial data, Client Components for real-time updates, and WebSocket for live data.

18. **Explain the streaming rendering pipeline.**
    Server renders shell → Sends HTML → Starts data fetches → Streams chunks as ready → Client hydrates progressively.

19. **How do you optimize streaming for slow networks?**
    Prioritize critical content, implement chunked loading, use service workers, and optimize payload size.

20. **Design a streaming system for a social media feed.**
    Stream posts as they load, implement infinite scrolling, handle real-time updates, and optimize for mobile.

21. **How would you implement streaming with authentication?**
    Stream public content first, delay authenticated content until verification, and handle auth errors gracefully.

22. **Explain the relationship between streaming and React Suspense.**
    Next.js streaming uses React Suspense under the hood. Server Components can be async and stream their output.

23. **How do you handle streaming with internationalization?**
    Stream locale-independent content first, load translations progressively, and handle locale switching.

24. **Design a streaming system for e-commerce.**
    Stream product info first, load reviews and recommendations in parallel, and handle dynamic pricing.

25. **How would you implement streaming analytics?**
    Track streaming performance, monitor TTFB/FCP, measure chunk delivery, and optimize based on metrics.

### FAANG-style (5-10)

26. **Design a streaming system for millions of concurrent users.**
    Use edge streaming, implement CDN caching, optimize chunk sizes, and handle traffic spikes.

27. **How would you implement adaptive streaming?**
    Detect network conditions, adjust chunk sizes, prioritize content, and fallback for slow connections.

28. **Design a streaming architecture with edge computing.**
    Use edge functions for streaming, implement geo-distributed streaming, and optimize for latency.

29. **How would you implement streaming with machine learning?**
    Predict optimal streaming strategies, prioritize content based on user behavior, and optimize delivery.

30. **Design a streaming system with fault tolerance.**
    Implement fallback rendering, handle chunk failures, retry lost chunks, and ensure delivery.

### Follow-ups (5-10)

31. **What are the limitations of streaming?**
    Some content can't be streamed, client hydration has overhead, and debugging is more complex.

32. **How does streaming affect SEO?**
    Search engines see the complete content, but streaming improves page speed which benefits SEO.

33. **What is the future of streaming in Next.js?**
    Better chunk optimization, improved DevTools, and more granular streaming controls.

34. **How do you debug streaming issues?**
    Use React DevTools, monitor network chunks, check server logs, and verify Suspense boundaries.

35. **What security considerations apply to streaming?**
    Stream only public content initially, verify authentication before streaming sensitive data.

36. **How does streaming interact with caching?**
    Cached content renders immediately, uncached content streams. Cache hit = no streaming needed.

37. **What are alternatives to streaming?**
    Traditional SSR, CSR with loading states, and lazy loading with dynamic imports.

38. **How do you measure streaming performance?**
    Track TTFB, FCP, LCP, chunk delivery time, and streaming success rates.

## Summary

| Feature | Streaming |
|---------|-----------|
| Mechanism | Progressive HTML delivery |
| Trigger | Suspense boundaries |
| Files | `loading.tsx`, `<Suspense>` |
| Benefit | Faster TTFB, better UX |
| Use case | Slow data fetching |
| Error handling | `error.tsx` per boundary |
| Performance | Improved Core Web Vitals |

## Cheat Sheet

```text
Route-level streaming:
app/loading.tsx → Automatic Suspense boundary

Component-level streaming:
<Suspense fallback={<Skeleton />}>
  <AsyncComponent />
</Suspense>

Nested streaming:
<Suspense fallback={<Outer />}>
  <OuterComponent>
    <Suspense fallback={<Inner />}>
      <InnerComponent />
    </Suspense>
  </OuterComponent>
</Suspense>

Error handling:
app/error.tsx → Error boundary for route

Performance:
- TTFB: Immediate shell
- FCP: Fast essential content
- LCP: Progressive main content
- CLS: Minimal with skeletons
```

## References & Learn More

- [Next.js Docs: Streaming](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming)
- [React Suspense](https://react.dev/reference/react/Suspense)
- [Streaming SSR](https://nextjs.org/docs/app/building-your-application/rendering/server-components#streaming)
