[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

# Incremental Static Regeneration (ISR)

## Definition

**Incremental Static Regeneration (ISR)** is a rendering strategy in Next.js that combines the performance of static generation with the freshness of server-side rendering. ISR generates static pages at build time, then **revalidates** them in the background after deployment — updating the cached HTML without rebuilding the entire application. Pages are served from the cache until the revalidation triggers, at which point Next.js regenerates the page in the background while serving the stale version. This creates a **stale-while-revalidate** caching pattern at the framework level.

## Why Do We Need It?

1. **Static speed with dynamic freshness** — Serve instantly from CDN, update when data changes
2. **No full rebuild** — Update individual pages without `next build`
3. **Scale to millions of pages** — Generate on first request if not pre-built
4. **Background regeneration** — Users always get cached pages, never waiting
5. **SEO-friendly** — Full HTML sent to crawlers at edge speed
6. **Reduced server load** — CDN serves most requests, server regenerates only when needed

## How It Works

### ISR Lifecycle

```text
ISR Page Lifecycle:
═══════════════════════════════════════════════════════════════

Build Time:
┌─────────────────────────────────────────────────────────────┐
│  next build                                                  │
│  ├── Generate static page HTML                              │
│  ├── Store in CDN with revalidation timer                   │
│  └── Deploy to production                                    │
└─────────────────────────────────────────────────────────────┘

First Request:
┌─────────────────────────────────────────────────────────────┐
│  User visits /products/123                                   │
│  ├── CDN serves pre-built HTML immediately                  │
│  └── Fast response (no server computation)                  │
└─────────────────────────────────────────────────────────────┘

After Revalidation Window (e.g., 60 seconds):
┌─────────────────────────────────────────────────────────────┐
│  User visits /products/123 (at second 61)                   │
│  ├── CDN serves STALE HTML instantly                       │
│  │   (User sees cached version — no wait!)                  │
│  ├── Next.js triggers background regeneration               │
│  │   ├── Fetch latest data                                  │
│  │   ├── Regenerate HTML                                    │
│  │   └── Update CDN cache                                   │
│  └── NEXT user gets fresh HTML                              │
└─────────────────────────────────────────────────────────────┘

On-Demand Revalidation (webhook/fresh):
┌─────────────────────────────────────────────────────────────┐
│  CMS Webhook: "Product 123 updated!"                        │
│  ├── Call revalidatePath('/products/123')                   │
│  │   OR revalidateTag('product-123')                        │
│  ├── Next.js regenerates immediately (not waiting for 60s)  │
│  └── CDN cache instantly updated                            │
└─────────────────────────────────────────────────────────────┘

```

### Caching Layers

```text
ISR Cache Layers:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                     CACHE HIERARCHY                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. CDN Cache (Edge)                                         │
│     ├── Serves cached HTML immediately                       │
│     ├── Cache-Control: s-maxage=60, stale-while-revalidate   │
│     └── Revalidates via upstream (Next.js server)            │
│                                                              │
│  2. Next.js Data Cache (Server)                              │
│     ├── Caches fetch() results (if fetch configured)         │
│     ├── Shared between ISR regeneration runs                 │
│     └── Invalidated by revalidateTag / revalidatePath        │
│                                                              │
│  3. Full Route Cache (HTML file)                             │
│     ├── Rendered HTML stored as file                         │
│     ├── Served for subsequent requests until revalidation    │
│     └── Replaced atomically on regeneration                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Basic ISR with revalidate

```typescript
// app/products/[id]/page.tsx
interface ProductPageProps {
  params: Promise<{ id: string }>;
}

async function getProduct(id: string) {
  const res = await fetch(`https://api.example.com/products/${id}`);
  return res.json();
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;
  const product = await getProduct(id);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
      <p className="text-sm text-gray-500">
        Price updated at: {new Date(product.updatedAt).toLocaleString()}
      </p>
    </div>
  );
}
```

```typescript
// This generates static pages + ISR at request time
// Not in App Router — ISR uses fetch revalidation or segment config:

// Option A: revalidate in fetch
fetch('https://api.example.com/products/123', {
  next: { revalidate: 60 }, // ISR with 60-second revalidation
});

// Option B: Segment config
// export const revalidate = 60;
```

### 2. ISR with Dynamic Params (generateStaticParams)

```typescript
// app/products/[id]/page.tsx
interface ProductPageProps {
  params: Promise<{ id: string }>;
}

// Pre-generate popular products at build time
export async function generateStaticParams() {
  const products = await fetch('https://api.example.com/products')
    .then(r => r.json());

  // Pre-generate only top 100 products
  return products.slice(0, 100).map((product: { id: string }) => ({
    id: product.id,
  }));
  // Non-pre-generated IDs will be generated on first visit (ISR fallback)
}

// ISR: revalidate every 60 seconds
export const revalidate = 60;

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;

  const product = await fetch(
    `https://api.example.com/products/${id}`,
    { next: { revalidate: 60 } } // Per-fetch revalidation
  ).then(r => r.json());

  return (
    <div>
      <h1>{product.name}</h1>
      <p>Price: ${product.price}</p>
      <p>Last checked: {new Date().toLocaleTimeString()}</p>
    </div>
  );
}
```

### 3. On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts — On-demand revalidation endpoint
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextResponse } from 'next/server';

// Revalidate by path
export async function POST(request: Request) {
  const body = await request.json();
  const { path, tag, secret } = body;

  // Verify secret token (security)
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ message: 'Invalid secret' }, { status: 401 });
  }

  try {
    if (path) {
      // Revalidate specific route
      await revalidatePath(path);
      return NextResponse.json({
        revalidated: true,
        message: `Path ${path} revalidated`,
      });
    }

    if (tag) {
      // Revalidate all routes using this tag
      await revalidateTag(tag);
      return NextResponse.json({
        revalidated: true,
        message: `Tag ${tag} revalidated`,
      });
    }

    return NextResponse.json(
      { message: 'Provide path or tag' },
      { status: 400 }
    );
  } catch (error) {
    return NextResponse.json(
      { message: 'Revalidation failed', error: String(error) },
      { status: 500 }
    );
  }
}
```

### 4. Tag-Based Revalidation

```typescript
// lib/api.ts — Tagged fetch helpers
interface FetchOptions {
  tags?: string[];
  revalidate?: number;
}

async function fetchWithCache<T>(
  url: string,
  options?: FetchOptions
): Promise<T> {
  const res = await fetch(url, {
    next: {
      revalidate: options?.revalidate ?? false,
      tags: options?.tags ?? [],
    },
  });

  if (!res.ok) throw new Error(`Fetch failed: ${url}`);

  return res.json();
}

// Usage in Server Components
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await fetchWithCache<Product>(
    `https://api.example.com/products/${params.id}`,
    {
      tags: [`product-${params.id}`, 'products'],
      revalidate: 60,
    }
  );

  const reviews = await fetchWithCache<Review[]>(
    `https://api.example.com/products/${params.id}/reviews`,
    {
      tags: [`reviews-${params.id}`, 'reviews'],
      revalidate: 300, // Reviews can be more stale
    }
  );

  return (
    <div>
      <ProductDetail product={product} />
      <ReviewList reviews={reviews} />
    </div>
  );
}

// CMS Webhook handler
export async function handleProductUpdate(productId: string) {
  // This instantly updates ALL pages that use 'product-123' tag
  await revalidateTag(`product-${productId}`);

  // Also revalidate the specific path
  await revalidatePath(`/products/${productId}`);

  // Bulk revalidate all products
  await revalidateTag('products');
}
```

### 5. ISR with Cache Tags for CMS

```typescript
// app/api/cms-webhook/route.ts — CMS integration
import { revalidateTag } from 'next/cache';
import { NextResponse } from 'next/server';
import { headers } from 'next/headers';

// Accept webhooks from Strapi, Contentful, Sanity, etc.
export async function POST(request: Request) {
  const body = await request.json();
  const headersList = await headers();
  const signature = headersList.get('x-cms-signature');

  // Verify webhook signature
  if (!verifySignature(signature, process.env.CMS_WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  // Handle different CMS events
  const { model, entry, action } = body;

  switch (model) {
    case 'product':
      // Invalidate specific product and product list
      revalidateTag(`product-${entry.id}`);
      revalidateTag('products');
      revalidatePath('/products');
      revalidatePath(`/products/${entry.slug}`);
      break;

    case 'category':
      revalidateTag(`category-${entry.id}`);
      revalidateTag('categories');
      revalidatePath('/categories');
      break;

    case 'page':
      revalidateTag('pages');
      revalidatePath(`/${entry.slug}`);
      break;
  }

  return NextResponse.json({ revalidated: true });
}
```

### 6. ISR with Conditional Revalidation

```typescript
// lib/conditional-revalidation.ts
import { revalidateTag, revalidatePath } from 'next/cache';

interface RevalidationRules {
  paths: string[];
  tags: string[];
  condition: (data: any) => boolean;
}

const revalidationRules: RevalidationRules[] = [
  {
    paths: ['/products/bestsellers'],
    tags: ['bestsellers'],
    condition: (data) => data.rating > 4.5,
  },
  {
    paths: ['/products/new-arrivals'],
    tags: ['new-arrivals'],
    condition: (data) => data.isNew === true,
  },
];

async function conditionalRevalidate(productData: any) {
  for (const rule of revalidationRules) {
    if (rule.condition(productData)) {
      // Only revalidate if conditions are met
      rule.paths.forEach(p => revalidatePath(p));
      rule.tags.forEach(t => revalidateTag(t));
      console.log(`Revalidated: ${rule.paths.join(', ')}`);
    }
  }
}

// Usage in webhook handler
export async function handleProductUpdate(product: any) {
  await conditionalRevalidate(product);
}
```

### 7. ISR with Stale-While-Revalidate Headers

```typescript
// This is what ISR sets automatically:
// Cache-Control: public, s-maxage=60, stale-while-revalidate=120

// Custom cache headers if you need more control:
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // Override cache headers for specific paths
  if (request.nextUrl.pathname.startsWith('/products')) {
    response.headers.set(
      'Cache-Control',
      'public, s-maxage=30, stale-while-revalidate=60'
    );
  }

  return response;
}

export const config = {
  matcher: '/products/:path*',
};
```

### 8. ISR with Fallback Strategies

```typescript
// pages/products/[id].tsx — Pages Router (has explicit fallback)
import { GetStaticPaths, GetStaticProps } from 'next';

interface ProductPageProps {
  product: { id: string; name: string; price: number };
}

// Pre-generate some pages
export const getStaticPaths: GetStaticPaths = async () => {
  const products = await fetch('https://api.example.com/products')
    .then(r => r.json());

  const paths = products.slice(0, 100).map((p: { id: string }) => ({
    params: { id: p.id },
  }));

  return {
    paths,
    // 'blocking': Wait for SSR on first request (SEO-friendly)
    // true: Show fallback UI then replace with static page
    // false: Return 404 for non-pre-generated paths
    fallback: 'blocking',
  };
};

export const getStaticProps: GetStaticProps<ProductPageProps> = async ({ params }) => {
  const product = await fetch(`https://api.example.com/products/${params!.id}`)
    .then(r => r.json());

  if (!product) {
    return { notFound: true };
  }

  return {
    props: { product },
    revalidate: 60, // ISR
  };
};
```

### 9. ISR with Time-Based Cascading

```typescript
// app/posts/[slug]/page.tsx
// Different revalidation times for different sections
interface PostPageProps {
  params: Promise<{ slug: string }>;
}

export default async function PostPage({ params }: PostPageProps) {
  const { slug } = await params;

  // Core content — revalidate every 5 minutes
  const post = await fetch(`https://cms.example.com/posts/${slug}`, {
    next: { revalidate: 300, tags: [`post-${slug}`] },
  }).then(r => r.json());

  // Comments — revalidate every 30 seconds
  const comments = await fetch(`https://cms.example.com/posts/${slug}/comments`, {
    next: { revalidate: 30, tags: [`comments-${slug}`] },
  }).then(r => r.json());

  // Related posts — revalidate every hour
  const related = await fetch(`https://cms.example.com/posts/${slug}/related`, {
    next: { revalidate: 3600, tags: [`related-${slug}`] },
  }).then(r => r.json());

  // Blog stats — revalidate daily
  const stats = await fetch(`https://cms.example.com/posts/${slug}/stats`, {
    next: { revalidate: 86400, tags: [`stats-${slug}`] },
  }).then(r => r.json());

  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.body }} />
      <h2>Comments ({comments.length})</h2>
      <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>
    </article>
  );
}
```

### 10. ISR with Incremental Adoption

```typescript
// app/page.tsx — Hybrid rendering: ISR + Client-side fetch
import { Suspense } from 'react';

// ISR for the main page shell
export const revalidate = 3600; // 1 hour

export default async function HomePage() {
  // This data ISR-caches
  const categories = await fetch('https://api.example.com/categories', {
    next: { revalidate: 3600 },
  }).then(r => r.json());

  return (
    <div>
      <h1>Store</h1>
      <nav>
        {categories.map((cat: any) => (
          <a key={cat.id} href={`/category/${cat.slug}`}>{cat.name}</a>
        ))}
      </nav>

      {/* Client-fetched data — always fresh */}
      <Suspense fallback={<div>Loading deals...</div>}>
        <DailyDeals /> {/* Client component fetches fresh */ }
      </Suspense>
    </div>
  );
}
```

## Real-World Use Cases

| Use Case | Revalidation Strategy | Why ISR |
|----------|----------------------|---------|
| **E-commerce product pages** | 60s + on-demand on price change | SEO, scale to 1M+ products |
| **Blog/News articles** | 300s + webhook on publish | Instant publish, CDN speed |
| **Documentation site** | 3600s + webhook on update | Near-static, always current |
| **Marketing pages** | 86400s (1 day) | Rare changes, instant load |
| **User dashboard (non-sensitive)** | 30s | Near-real-time without server load |
| **Category/Listing pages** | 60s + on-demand on stock change | Fresh inventory, high traffic |
| **Job listings** | 300s | Balances freshness vs CDN hit rate |
| **Weather/financial data** | 60-300s | Acceptable staleness for better perf |

## Common Mistakes

### 1. Over-Revalidating

```typescript
// ❌ BAD: Revalidating too frequently negates ISR benefits
export const revalidate = 1; // Revalidates every second!
// At this point, just use SSR (dynamic rendering)

// ✅ GOOD: Use longer intervals + on-demand for freshness
export const revalidate = 300; // 5 minutes
// Plus on-demand revalidation via webhooks
```

### 2. Forgetting On-Demand Revalidation

```typescript
// ❌ BAD: Time-based only — users see stale data until window expires
export const revalidate = 3600; // 1 hour stale!

// ✅ GOOD: Add on-demand revalidation for instant updates
// Call this from CMS webhooks
await revalidatePath('/products/123');
await revalidateTag('product-123');
```

### 3. Not Handling Missing Data

```typescript
// ❌ BAD: No fallback when API fails during revalidation
export default async function Page({ params }) {
  const data = await fetch('https://api.example.com/data');
  // If this fails during revalidation, the page breaks!
}

// ✅ GOOD: Handle errors gracefully
export default async function Page({ params }) {
  try {
    const data = await fetch('https://api.example.com/data');
    return <div>{data.content}</div>;
  } catch {
    // Return cached version — don't break the page
    // Next.js keeps serving stale version on fetch errors
    return <div>Content temporarily unavailable</div>;
  }
}
```

### 4. ISR with User-Specific Content

```typescript
// ❌ BAD: User-specific content in ISR
export const revalidate = 60;
export default async function Dashboard({ params }) {
  const userData = await fetch(`https://api.example.com/users/${params.id}`, {
    next: { revalidate: 60 },
  });
  // Same HTML served to ALL users!  User data is incorrectly cached.
}

// ✅ GOOD: Use SSR or client-side fetch for user data
export const dynamic = 'force-dynamic'; // Skip ISR for user pages
```

### 5. Not Using generateStaticParams for Large Sets

```typescript
// ❌ BAD: Letting ISR generate every page on first request
// First user for each product ID pays the cold-start penalty

// ✅ GOOD: Pre-generate popular pages
export async function generateStaticParams() {
  const popularProducts = await fetch('/api/products/popular')
    .then(r => r.json());

  return popularProducts.map(p => ({ id: p.id }));
  // These are pre-built, others generate on-demand
}
```

## Best Practices

1. **Use on-demand revalidation** — Webhooks for instant updates, don't rely only on time

2. **Tag-based invalidation** — `revalidateTag` is more granular than `revalidatePath`

3. **Graceful degradation** — Handle API failures during revalidation (stale cache persists)

4. **Pre-generate popular pages** — `generateStaticParams` for your top 20% of pages

5. **Don't ISR user-specific pages** — Use SSR or client-side fetch for personalized content

6. **Set appropriate revalidation windows** — Align with your content update frequency

7. **Monitor revalidation rates** — Track how often pages are regenerating

8. **Use stale-while-revalidate headers** — CDN caching policy for optimal performance

9. **Test cache invalidation** — Verify webhooks actually trigger revalidation

10. **Combine ISR with client-side fetching** — ISR for shell, client fetch for real-time data

## Performance Considerations

```text
ISR Performance Characteristics:

CDN Cache Hit Ratio:
├── High revalidate window (3600s) → ~99% cache hit
├── Medium revalidate window (60s) → ~95% cache hit
├── Low revalidate window (5s) → ~70% cache hit
└── No revalidate (static) → ~100% cache hit

Server Load:
├── ISR 60s, 1000 pages: ~17 regenerations/minute
├── ISR 300s, 1000 pages: ~3 regenerations/minute
└── SSR: Every request hits the server

Trade-offs:
├── Longer revalidate = Better CDN hit rate, more stale data
├── Shorter revalidate = Fresher data, more server load
├── On-demand = Best of both worlds (if webhooks set up)
└── generateStaticParams = Zero cold starts for popular pages

```

## Summary

ISR combines the performance of static generation with the flexibility of dynamic updates. Time-based revalidation provides automatic freshness, while on-demand revalidation (via `revalidatePath` and `revalidateTag`) enables instant updates. For maximum performance, pre-generate popular pages, use tag-based invalidation, and pair ISR with CDN caching for optimal cache hit ratios.

## Cheat Sheet

```typescript
// App Router — Time-based ISR
export const revalidate = 60; // Seconds

// Per-fetch revalidation
fetch(url, { next: { revalidate: 60 } });

// Per-fetch cache tags
fetch(url, { next: { tags: ['products', 'product-123'] } });

// On-demand revalidation
import { revalidatePath, revalidateTag } from 'next/cache';

await revalidatePath('/products/123');
await revalidateTag('product-123');

// Pre-generate pages
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }];
}

// Pages Router
export async function getStaticProps() {
  return {
    props: { data },
    revalidate: 60, // ISR
  };
}
```

```text
ISR Key Points:
├── Static speed + Dynamic freshness
├── Background regeneration (user never waits)
├── Cache-Control: s-maxage, stale-while-revalidate
├── Time-based: revalidate: 60 (seconds)
├── On-demand: revalidatePath, revalidateTag
├── Fallback: 'blocking' (wait) | true (loading) | false (404)
├── Don't ISR: User-specific, auth-protected pages
├── Do ISR: Product pages, blog posts, listings
└── Best: Time-based + On-demand (webhooks)
```

---

## See Also

- [Caching in Next.js](09-Caching.md)
- [Client Components](04-Client-Components.md)
- [Image Optimization](11-Image-Optimization.md)
- [Metadata](08-Metadata.md)
- [Server Components](03-Server-Components.md)
- [SSR / CSR / SSG / ISR](01-SSR-CSR-SSG-ISR.md)
- [Streaming](10-Streaming.md)

## References & Learn More

- [Next.js Docs: ISR](https://nextjs.org/docs/app/building-your-application/data-fetching/incremental-static-regeneration)
- [Next.js Docs: revalidatePath](https://nextjs.org/docs/app/api-reference/functions/revalidatePath)
- [Next.js Docs: revalidateTag](https://nextjs.org/docs/app/api-reference/functions/revalidateTag)
- [Next.js Docs: generateStaticParams](https://nextjs.org/docs/app/api-reference/functions/generate-static-params)
- [Vercel: ISR on Vercel](https://vercel.com/docs/deployments/isr)
- [Web Vitals: Stale-While-Revalidate](https://web.dev/stale-while-revalidate/)
