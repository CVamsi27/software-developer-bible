---
section: Next.js
category: Frontend
tags: [concept]
---

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

---

## See Also
- [React](../03-React/)
- [Serverless & Edge](../27-Serverless-Edge/)
- [Performance Monitoring](../26-Performance-Monitoring/)

## References & Learn More

- [Next.js Docs: Rendering](https://nextjs.org/docs/app/building-your-application/rendering)
- [Next.js: Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Next.js: Static vs Dynamic Rendering](https://nextjs.org/docs/app/building-your-application/rendering/static-and-dynamic-rendering)
