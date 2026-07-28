---
section: Next.js
category: Frontend
tags: [concept]
---

# App Router in Next.js

## Definition

The **App Router** is Next.js's modern routing system introduced in Next.js 13, built on top of React Server Components. It uses a file-system based router within the `app/` directory with enhanced features like nested layouts, loading states, error handling, and parallel routes.

## Why Do We Need It?

The Pages Router had limitations:

- No shared layouts without custom `_app.tsx` hacks
- No built-in loading/error states per route
- No route interception or parallel routes
- Server Components not natively supported

The App Router solves these with a more powerful, flexible routing system.

## How It Works

### App Router vs Pages Router Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                    PAGES ROUTER (Legacy)                        │
├─────────────────────────────────────────────────────────────────┤
│  pages/                                                        │
│  ├── index.tsx          → /                                     │
│  ├── about.tsx          → /about                                │
│  ├── blog/                                                    │
│  │   ├── index.tsx      → /blog                                 │
│  │   └── [slug].tsx     → /blog/:slug                           │
│  ├── _app.tsx           → Shared wrapper (only one)             │
│  └── _document.tsx      → Custom HTML document                  │
│                                                                 │
│  Limitations:                                                   │
│  - One layout (_app.tsx)                                        │
│  - No per-route loading/error                                   │
│  - No nested layouts                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     APP ROUTER (Modern)                         │
├─────────────────────────────────────────────────────────────────┤
│  app/                                                          │
│  ├── page.tsx              → /                                  │
│  ├── layout.tsx            → Root layout (shared)               │
│  ├── loading.tsx           → Root loading state                 │
│  ├── error.tsx             → Root error boundary                │
│  ├── about/                                                         │
│  │   └── page.tsx          → /about                             │
│  │   └── layout.tsx        → /about nested layout               │
│  ├── blog/                                                        │
│  │   ├── page.tsx          → /blog                              │
│  │   ├── loading.tsx       → /blog loading state                │
│  │   ├── error.tsx         → /blog error boundary               │
│  │   └── [slug]/                                                    │
│  │       └── page.tsx      → /blog/:slug                        │
│  │       └── layout.tsx    → /blog/:slug nested layout          │
│                                                                 │
│  Features:                                                      │
│  - Nested layouts per route                                     │
│  - Per-route loading/error states                               │
│  - Server Components by default                                 │
│  - Parallel & intercepting routes                               │
└─────────────────────────────────────────────────────────────────┘

```

### File-Based Routing Structure

```text
app/
├── page.tsx                    → /
├── layout.tsx                  → Root layout
├── loading.tsx                 → Root loading
├── error.tsx                   → Root error
├── not-found.tsx               → 404 page
├── template.tsx                → Root template
├── (marketing)/                → Route group (no URL segment)
│   ├── page.tsx                → /
│   ├── about/page.tsx          → /about
│   └── contact/page.tsx        → /contact
├── (dashboard)/                → Route group
│   ├── layout.tsx              → Dashboard layout
│   ├── dashboard/page.tsx      → /dashboard
│   └── settings/page.tsx       → /settings
├── products/
│   ├── page.tsx                → /products
│   ├── [id]/page.tsx           → /products/:id
│   └── [...slug]/page.tsx      → /products/* (catch-all)
├── auth/
│   ├── login/page.tsx          → /auth/login
│   └── register/page.tsx       → /auth/register
├── @modal/                     → Parallel route
│   └── default.tsx
├── (.)photos/                  → Intercepting route
│   └── [id]/page.tsx           → Intercepts /photos/:id
└── api/
    └── users/route.ts          → API route

```

### Layout System

```tsx
// app/layout.tsx — Root Layout (required)
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'My App',
  description: 'Built with Next.js',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav>{/* Global navigation */}</nav>
        <main>{children}</main>
        <footer>{/* Global footer */}</footer>
      </body>
    </html>
  )
}

```

```tsx
// app/dashboard/layout.tsx — Nested Layout
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex">
      <aside className="w-64">
        {/* Dashboard sidebar */}
        <nav>
          <a href="/dashboard">Overview</a>
          <a href="/dashboard/settings">Settings</a>
        </nav>
      </aside>
      <section className="flex-1">
        {children}
      </section>
    </div>
  )
}

```

### Loading States

```tsx
// app/dashboard/loading.tsx — Automatic Suspense boundary
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

### Error Handling

```tsx
// app/dashboard/error.tsx — Error boundary
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

```

```tsx
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

### Route Groups

```tsx
// app/(marketing)/layout.tsx — Marketing layout (no URL segment)
export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>
      <header>Marketing Header</header>
      {children}
      <footer>Marketing Footer</footer>
    </div>
  )
}

// app/(marketing)/about/page.tsx → /about
export default function AboutPage() {
  return <h1>About Us</h1>
}

```

### Parallel Routes

```tsx
// app/layout.tsx — Render multiple pages simultaneously
export default function Layout({
  children,
  modal,
  analytics,
}: {
  children: React.ReactNode
  modal: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <div>
      {children}
      {modal}
      {analytics}
    </div>
  )
}

// app/@modal/default.tsx — Default for unmatched URLs
export default function Default() {
  return null
}

// app/@modal/(.)photos/[id]/page.tsx — Intercepted modal
export default function PhotoModal({ params }) {
  return (
    <div className="modal">
      <img src={`/photos/${params.id}`} />
    </div>
  )
}

```

### Intercepting Routes

```text
URL: /photos/123

Normal route:        app/photos/[id]/page.tsx
Intercepted route:   app/(.)photos/[id]/page.tsx

When navigating from /photos → /photos/123:
  Shows intercepted route (modal) over current page

When directly accessing /photos/123:
  Shows full page (non-intercepted route)

```

### Dynamic Routes

```tsx
// app/products/[id]/page.tsx — Dynamic segment
export default function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  return <h1>Product {params.id}</h1>
}

// app/blog/[...slug]/page.tsx — Catch-all segment
export default function BlogPost({
  params,
}: {
  params: Promise<{ slug: string[] }>
}) {
  // /blog/a/b/c → slug: ['a', 'b', 'c']
  return <h1>Blog post: {params.slug.join('/')}</h1>
}

// app/docs/[[...slug]]/page.tsx — Optional catch-all
export default function DocsPage({
  params,
}: {
  params: Promise<{ slug?: string[] }>
}) {
  // /docs → slug: undefined
  // /docs/a → slug: ['a']
  return <h1>Docs: {params.slug?.join('/') || 'Home'}</h1>
}

```

### Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const users = await fetchUsers()
  return NextResponse.json(users)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const user = await createUser(body)
  return NextResponse.json(user, { status: 201 })
}

```

### Templates

```tsx
// app/template.tsx — Re-renders on navigation (unlike layout)
export default function Template({ children }: { children: React.ReactNode }) {
  return <div className="fade-in">{children}</div>
}

```

### Metadata

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
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

export default async function BlogPost({ params }) {
  const { slug } = await params
  const post = await getPost(slug)
  return <article>{post.content}</article>
}

```

### Dynamic Segments with Generate Static Params

```tsx
// app/products/[id]/page.tsx
export async function generateStaticParams() {
  const products = await fetchProducts()
  return products.map(product => ({
    id: product.id,
  }))
}

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const product = await fetchProduct(id)
  return <h1>{product.name}</h1>
}

```

### Route Segment Config

```tsx
// Force dynamic rendering
export const dynamic = 'force-dynamic'

// Force static rendering
export const dynamic = 'force-static'

// Disable caching
export const fetchCache = 'no-store'

// Revalidation
export const revalidate = 60

// Runtime
export const runtime = 'edge' // or 'nodejs'

// Max duration (Vercel)
export const maxDuration = 30

```

## Real-World Use Cases

### E-Commerce Platform

```text
app/
├── layout.tsx                    → Root layout with providers
├── (shop)/
│   ├── layout.tsx               → Shop layout with navigation
│   ├── page.tsx                 → Homepage /products
│   ├── products/
│   │   ├── page.tsx             → Product listing
│   │   └── [id]/
│   │       ├── page.tsx         → Product detail
│   │       └── layout.tsx       → Product detail layout
│   └── cart/
│       └── page.tsx             → Shopping cart
├── (auth)/
│   ├── login/page.tsx           → Login
│   └── register/page.tsx        → Register
├── @modal/
│   ├── (.)cart/page.tsx         → Cart modal overlay
│   └── default.tsx
├── dashboard/
│   ├── layout.tsx               → Dashboard layout
│   ├── page.tsx                 → Dashboard overview
│   └── orders/page.tsx          → Order history
└── api/
    ├── products/route.ts        → Products API
    └── checkout/route.ts        → Checkout API

```

### Blog Platform

```text
app/
├── layout.tsx
├── (marketing)/
│   ├── layout.tsx               → Marketing layout
│   ├── page.tsx                 → Landing page
│   ├── about/page.tsx
│   └── pricing/page.tsx
├── blog/
│   ├── layout.tsx               → Blog layout with sidebar
│   ├── page.tsx                 → Blog listing
│   ├── loading.tsx              → Blog loading state
│   └── [slug]/
│       ├── page.tsx             → Blog post
│       ├── layout.tsx           → Post layout
│       └── loading.tsx          → Post loading state
└── admin/
    ├── layout.tsx               → Admin layout
    ├── posts/page.tsx           → Post management
    └── settings/page.tsx

```

## Common Mistakes

### 1. Forgetting 'use client' in Interactive Components

```tsx
// ❌ BAD: Trying to use useState without 'use client'
export default function Counter() {
  const [count, setCount] = useState(0) // Error!
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// ✅ GOOD: Add 'use client' directive
'use client'
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

```

### 2. Mutating Props Directly

```tsx
// ❌ BAD: Mutating params directly
export default async function Page({ params }) {
  params.id = 'new-id' // Never mutate params!
  return <h1>{params.id}</h1>
}

// ✅ GOOD: Destructure and use
export default async function Page({ params }) {
  const { id } = await params
  return <h1>{id}</h1>
}

```

### 3. Missing Layout in Nested Routes

```tsx
// ❌ BAD: Inconsistent layout across nested routes
app/
├── dashboard/page.tsx
└── dashboard/settings/page.tsx
// Each page needs its own layout or shares root layout

// ✅ GOOD: Add shared layout
app/
├── dashboard/
│   ├── layout.tsx    → Shared dashboard layout
│   ├── page.tsx
│   └── settings/page.tsx

```

### 4. Not Handling Async Params

```tsx
// ❌ BAD: Accessing params synchronously
export default function Page({ params }) {
  return <h1>{params.id}</h1> // params is a Promise in Next.js 15!
}

// ✅ GOOD: Await params
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  return <h1>{id}</h1>
}

```

### 5. Using Client Components Unnecessarily

```tsx
// ❌ BAD: Marking entire page as client component
'use client'
export default function ProductPage({ product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  )
}

// ✅ GOOD: Keep page as server component, isolate client parts
export default async function ProductPage({ params }) {
  const { id } = await params
  const product = await getProduct(id)

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />
    </div>
  )
}

// Only the interactive component needs 'use client'
'use client'
export function AddToCartButton({ productId }: { productId: string }) {
  // ...
}

```

## Best Practices

1. **Keep server components as the default** — Only add `'use client'` when interactivity is needed

2. **Use route groups** — Organize routes without affecting URL structure

3. **Add loading.tsx** — Provide instant loading feedback for every route

4. **Use error.tsx boundaries** — Catch and handle errors per route segment

5. **Leverage nested layouts** — Share UI across route segments efficiently

6. **Use parallel routes** — For modals, dashboards with multiple views

7. **Implement intercepting routes** — For modal patterns over existing pages

8. **Use generateStaticParams** — Pre-render dynamic routes at build time

9. **Export metadata** — Per-page SEO optimization
10. **Use templates** — For transition animations between routes

## Performance Considerations

```text
App Router Performance Benefits:

- Server Components reduce client bundle size
- Nested layouts avoid re-rendering shared UI
- Loading states provide instant feedback
- Parallel routes enable concurrent rendering
- Streaming SSR improves TTFB

Performance Costs:

- More complex mental model
- Additional server rendering overhead
- Potential for excessive server component usage
- Build time increases with more routes

```


## Summary

| Feature | Pages Router | App Router |
|---------|-------------|------------|
| Directory | `pages/` | `app/` |
| Default Component | Client | Server |
| Layouts | Single `_app.tsx` | Nested `layout.tsx` |
| Loading | Manual | `loading.tsx` |
| Error | `_error.tsx` | `error.tsx` |
| 404 | `_error.tsx` | `not-found.tsx` |
| Parallel Routes | No | Yes |
| Intercepting | No | Yes |
| Server Components | No | Yes |

## Cheat Sheet
```text
File Structure:
├── page.tsx          → Route page
├── layout.tsx        → Persistent layout
├── template.tsx      → Re-rendering template
├── loading.tsx       → Suspense loading
├── error.tsx         → Error boundary
├── not-found.tsx     → 404 page
├── default.tsx       → Parallel route default
└── route.ts          → API route handler

Route Types:
[slug]              → Dynamic segment
[...slug]           → Catch-all
[[...slug]]         → Optional catch-all
(group)             → Route group (no URL)
@folder             → Parallel route
(.)folder           → Intercepting route

Directives:
'use client'        → Client Component
'use server'        → Server Action

Config:
dynamic             → Rendering mode
revalidate          → ISR interval
runtime             → Edge or Node.js

```

---

## See Also
- [React](../03-React/)
- [Serverless & Edge](../27-Serverless-Edge/)
- [Performance Monitoring](../26-Performance-Monitoring/)

## References & Learn More

- [Next.js Docs: App Router](https://nextjs.org/docs/app/building-your-application/routing)
- [App Router Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)
- [Next.js Routing Fundamentals](https://nextjs.org/docs/getting-started/installation)
