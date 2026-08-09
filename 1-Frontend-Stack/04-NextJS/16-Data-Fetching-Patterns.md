---
section: Next.js
category: Frontend
tags: [concept]
---

# Data Fetching Patterns in Next.js (App Router)

## TL;DR

In the App Router, data fetching is a first-class concern with three patterns: (1) `fetch` in Server Components with automatic request memoization + Data Cache, (2) Server Actions for mutations with `revalidatePath`/`revalidateTag`, and (3) Client-side fetching with React Query / SWR for interactive data. The choice depends on whether data is read-once vs. interactive, server-rendered vs. client-cached, and mutation frequency.

## Why It Matters

Senior Next.js interviews test whether you can architect a data layer across Server Components, Client Components, and Server Actions. The wrong pattern (e.g., `useEffect`+`fetch` in a Server Component, or `fetch` without cache control in production) leads to waterfalls, stale data, and unnecessary origin load. Knowing when each pattern applies is what separates senior from mid-level.

## Definition

Data fetching in the App Router is the set of patterns for reading and mutating data across Server Components, Client Components, and Server Actions, integrated with Next.js's caching and revalidation model.

## Why Do We Need It?

1. **Performance** — Server-side fetching eliminates client-side waterfalls and reduces TTFB
2. **Freshness** — Different patterns offer different staleness guarantees (cached, ISR, no-store, on-demand)
3. **Interactivity** — Some data needs to be client-side reactive (search, infinite scroll, optimistic updates)
4. **Mutations** — Server Actions handle writes with automatic revalidation integration
5. **Type safety** — Each pattern has different type-safety implications (Zod, tRPC, generated types)

## How It Works

### Pattern 1: Server Component `fetch` (Default)

```typescript
// app/products/page.tsx — Server Component
async function ProductsPage() {
  // Automatically memoized within a single request
  // Automatically cached across requests (Data Cache)
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }, // ISR-style: revalidate every hour
  });
  const products: Product[] = await res.json();
  return <ProductList products={products} />;
}
```

**Key behaviors:**
- `fetch` calls in Server Components are deduplicated per request (Request Memoization)
- The Data Cache persists the response across requests, keyed by URL + options
- `next: { revalidate: N }` enables time-based revalidation (ISR)
- `cache: 'no-store'` opts out of the Data Cache (always fresh)
- `next: { tags: ['products'] }` enables tag-based revalidation

### Pattern 2: Database / ORM in Server Components

```typescript
// app/dashboard/page.tsx
import { db } from '@/lib/db';
import { unstable_cache } from 'next/cache';

const getStats = unstable_cache(
  async () => {
    return db.order.aggregate({ _sum: { amount: true }, _count: true });
  },
  ['dashboard-stats'],
  { revalidate: 60, tags: ['stats'] }
);

async function DashboardPage() {
  const stats = await getStats();
  return <StatsCards stats={stats} />;
}
```

For non-`fetch` data sources (DB, filesystem, internal APIs), wrap in `unstable_cache` to get the same caching/revalidation behavior.

### Pattern 3: Server Actions for Mutations

```typescript
// app/products/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createProduct(formData: FormData) {
  const product = await db.product.create({
    data: { name: formData.get('name') as string },
  });

  // Invalidate caches
  revalidateTag('products');          // all queries tagged 'products'
  revalidatePath('/products');         // specific path
  revalidatePath('/');                 // home (if it lists products)

  redirect(`/products/${product.id}`);
}
```

```typescript
// app/products/new/page.tsx
import { createProduct } from '../actions';

export default function NewProductPage() {
  return (
    <form action={createProduct}>
      <input name="name" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### Pattern 4: Client-Side Fetching with React Query

```typescript
// For data that's highly interactive: search, live updates, optimistic UI
'use client';

import { useQuery } from '@tanstack/react-query';

function SearchResults({ query }: { query: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetch(`/api/search?q=${query}`).then(r => r.json()),
    enabled: query.length > 2,
    staleTime: 30_000,
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error />;
  return <Results data={data} />;
}
```

Use this for: search-as-you-type, infinite scroll, polling, optimistic updates on data the user is actively interacting with.

### Pattern 5: `useSWR` (Alternative Client Pattern)

```typescript
'use client';
import useSWR from 'swr';

function UserProfile({ id }: { id: string }) {
  const { data, error, isLoading, mutate } = useSWR(`/api/users/${id}`, fetcher, {
    revalidateOnFocus: true,
    refreshInterval: 0,
  });
  // ...
}
```

SWR is similar to React Query but with a smaller API surface. Choose based on team preference.

### Pattern 6: Parallel Data Fetching (Avoid Waterfalls)

```typescript
// ❌ Waterfall: each await blocks the next
async function Page() {
  const user = await getUser();
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  return <Dashboard user={user} posts={posts} comments={comments} />;
}

// ✅ Parallel: kick off all fetches simultaneously
async function Page() {
  const userPromise = getUser();
  const user = await userPromise;
  const [posts, comments] = await Promise.all([
    getPosts(user.id),
    getComments(user.id),  // pass id, not posts[0]
  ]);
  return <Dashboard user={user} posts={posts} comments={comments} />;
}

// ✅ Preload in parallel using the data layer
async function Page() {
  // Next.js's request memoization dedupes these if they share keys
  const [user, posts, comments] = await Promise.all([
    getUser(),
    getPosts(),
    getComments(),
  ]);
  return <Dashboard user={user} posts={posts} comments={comments} />;
}
```

### Pattern 7: Streaming with Suspense

```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function DashboardPage() {
  return (
    <div>
      <Header /> {/* Renders immediately */}
      <Suspense fallback={<StatsSkeleton />}>
        <Stats /> {/* Streams when ready */}
      </Suspense>
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity /> {/* Independent of Stats, streams in parallel */}
      </Suspense>
    </div>
  );
}

async function Stats() {
  const data = await fetchStats(); // slow
  return <StatsCards data={data} />;
}
```

Each Suspense boundary becomes an independent streaming unit. The page shell ships immediately, and each section fills in as its data resolves.

## Code Examples

### Real-World: E-commerce Product Page

```typescript
// app/products/[id]/page.tsx
import { notFound } from 'next/navigation';
import { Suspense } from 'react';

// Static shell renders at build, revalidates every hour
async function getProduct(id: string) {
  const res = await fetch(`https://api.example.com/products/${id}`, {
    next: { revalidate: 3600, tags: [`product-${id}`] },
  });
  if (!res.ok) notFound();
  return res.json();
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);
  return (
    <div>
      <h1>{product.name}</h1>
      {/* Reviews are slower, stream them independently */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

### Real-World: Search-as-you-Type with React Query

```typescript
'use client';
import { useQuery } from '@tanstack/react-query';
import { useDeferredValue } from 'react';

function SearchBox() {
  const [query, setQuery] = useState('');
  const deferred = useDeferredValue(query);

  const { data, isFetching } = useQuery({
    queryKey: ['search', deferred],
    queryFn: () => fetch(`/api/search?q=${deferred}`).then(r => r.json()),
    enabled: deferred.length > 2,
    placeholderData: keepPreviousData, // smooth transitions
  });

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      {isFetching && <Spinner />}
      <Results items={data ?? []} />
    </>
  );
}
```

### Real-World: Form Mutation with Optimistic Update

```typescript
'use client';
import { useOptimistic } from 'react';
import { addTodo } from './actions';

function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  return (
    <form action={async (formData) => {
      const tempId = crypto.randomUUID();
      addOptimistic({ id: tempId, text: formData.get('text') as string, pending: true });
      await addTodo(formData);
    }}>
      {/* ... */}
    </form>
  );
}
```

## Real-World Use Cases

1. **Marketing pages** — Server Component `fetch` with `revalidate: 3600` (hourly ISR)
2. **User dashboards** — Server Component fetch + Suspense for slow sections
3. **Search** — Client Component with React Query + `useDeferredValue`
4. **Forms** — Server Actions with `revalidateTag`/`revalidatePath`
5. **Live data** (chat, stock prices) — Client Component with WebSocket + SWR
6. **Admin panels** — Mixed: Server Component for initial render, Client Component for interactions
7. **E-commerce catalog** — SSG for category pages, SSR for product detail, Server Actions for cart

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `useEffect` + `fetch` in a Server Component | Use `async` + `await` directly in the Server Component |
| No cache control on production `fetch` | Use `next: { revalidate, tags }` or `cache: 'no-store'` explicitly |
| Sequential `await`s in a Server Component | Use `Promise.all` to parallelize independent fetches |
| Fetching in Client Components when Server Components would work | Push the boundary down; fetch on the server to avoid waterfalls |
| Using `useEffect` to derive data from props | Compute it directly in render (or use a Server Component) |
| Not invalidating caches after mutations | Call `revalidatePath`/`revalidateTag` from Server Actions |
| Using Server Actions for reads | Use Server Components for reads, Server Actions for writes |
| Not setting `next.tags` on `fetch` | Without tags, you can't selectively revalidate |

## Best Practices

1. **Default to Server Component `fetch`** — for any data that doesn't need to be reactive on the client
2. **Use `unstable_cache` for non-`fetch` data** — DB queries, internal APIs, file reads
3. **Always set cache strategy explicitly** — `revalidate`, `no-store`, or `tags` — don't rely on defaults in production
4. **Parallelize independent fetches with `Promise.all`** — eliminate request waterfalls
5. **Use Suspense boundaries to stream slow sections** — each boundary is an independent streaming unit
6. **Use Server Actions for mutations, Route Handlers for full HTTP endpoints** — they have different semantics
7. **Tag your fetches** — `tags: ['products', `product-${id}`]` enables fine-grained revalidation
8. **Use React Query for client-side reactive data only** — search, infinite scroll, polling, optimistic UI
9. **Invalidate caches after every mutation** — `revalidateTag`/`revalidatePath` in Server Actions
10. **Pass data through props, not via fetch** — if a Server Component has the data, pass it to a Client Component via props instead of refetching

## Performance Considerations

| Pattern | TTFB | Waterfall Risk | Cache | Use For |
|---------|------|----------------|-------|---------|
| Server Component `fetch` + revalidate | Low (cached) | Low (parallel) | Data Cache | Static-ish content, dashboards |
| Server Component `fetch` + no-store | Higher (always fresh) | Low | None | Personalized/authenticated data |
| Server Component `unstable_cache` | Low | Low | Per-tag | DB queries, internal APIs |
| Server Actions | — | — | N/A (mutations) | Forms, mutations |
| React Query (client) | N/A (client-side) | Higher (round trips) | In-memory | Search, infinite scroll, polling |
| SWR (client) | N/A (client-side) | Higher | In-memory | Same as React Query |
| Streaming + Suspense | Low (TTFB on shell) | None (parallel) | Inherits | Slow-data pages with fast shell |

**Decision tree:**
- Read-only, mostly static? → Server Component + `revalidate`
- Read-only, personalized/authenticated? → Server Component + `cache: 'no-store'`
- Mutation? → Server Action + `revalidateTag`/`revalidatePath`
- Highly interactive (search, live updates)? → Client Component + React Query/SWR
- Slow data, fast shell needed? → Server Component + Suspense streaming

## Summary

Next.js App Router data fetching is pattern-based, not framework-magic. Use Server Component `fetch` (with explicit revalidate/tags) for read-only, mostly static data; Server Actions for mutations; React Query for client-side reactive data; and Suspense for streaming slow sections. Default to the server, push the client boundary down, parallelize independent fetches, and always invalidate caches after mutations.

## Cheat Sheet

| Pattern | Where | Cache | Use For |
|---------|-------|-------|---------|
| `await fetch(url, { next: { revalidate } })` | Server Component | Data Cache | Static-ish, time-based ISR |
| `await fetch(url, { cache: 'no-store' })` | Server Component | None | Per-request fresh data |
| `await fetch(url, { next: { tags } })` | Server Component | Data Cache + tags | Tag-based invalidation |
| `unstable_cache(fn, keys, { revalidate, tags })` | Server Component | Custom | DB queries, internal APIs |
| Server Action + `revalidatePath`/`revalidateTag` | Mutation | N/A | Form submissions, updates |
| `useQuery` (React Query) | Client Component | In-memory | Search, infinite scroll, polling |
| `useSWR` | Client Component | In-memory | Same as React Query |
| `<Suspense>` boundaries | Page layout | Inherits | Streaming slow sections |
| `Promise.all([...])` | Server Component | Inherits | Parallel independent fetches |

---

## See Also
- [App Router](02-App-Router.md)
- [Caching](09-Caching.md)
- [React State Management](../03-React/14-State-Management.md)
- [Server Actions](06-Server-Actions.md)
- [Server Components](03-Server-Components.md)
- [Streaming](10-Streaming.md)

## References & Learn More

- [Next.js Docs: Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Next.js Docs: Caching](https://nextjs.org/docs/app/building-your-application/caching)
- [Next.js Docs: Server Actions and Mutations](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Next.js Docs: Streaming](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming)
- [Patterns.dev: App Router Data Fetching](https://www.patterns.dev/vanilla-rsc/)
- [Vercel: Data Fetching in Next.js 14](https://vercel.com/blog/next-js-app-router-data-fetching)
