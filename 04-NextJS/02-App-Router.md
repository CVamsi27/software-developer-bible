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

## Interview Questions

### Beginner (5-10)

1. **What is the App Router in Next.js?**
   The App Router is Next.js's modern routing system using the `app/` directory, built on React Server Components with nested layouts, loading states, and error handling.

2. **How does the App Router differ from the Pages Router?**
   App Router uses Server Components by default, supports nested layouts per route, has built-in loading/error states, and supports parallel and intercepting routes.

3. **What is a route group in the App Router?**
   A route group uses parentheses `(groupName)` to organize routes without affecting the URL structure. It's for logical grouping only.

4. **What is the purpose of `layout.tsx`?**
   Layouts are shared UI that persist across navigations. They don't re-render on route changes, providing performance benefits and consistent UI.

5. **What is the difference between `layout.tsx` and `template.tsx`?**
   Layouts persist across navigations (don't re-render), while templates re-render on every navigation. Use templates for transition animations.

6. **How do you create a loading state for a route?**
   Add a `loading.tsx` file in the route directory. It's automatically wrapped in a Suspense boundary.

7. **What is a parallel route?**
   Parallel routes use `@folder` syntax to render multiple pages simultaneously in the same layout, useful for modals and split views.

8. **What is an intercepting route?**
   Intercepting routes use `(.)` syntax to intercept navigation and render a different UI (like a modal) while preserving the URL.

### Intermediate (5-10)

9. **How do you handle 404 errors in the App Router?**
   Create a `not-found.tsx` file in the route directory. Call `notFound()` from `next/navigation` to trigger it.

10. **What is the purpose of `generateStaticParams`?**
    It pre-generates static pages for dynamic routes at build time, combining the benefits of SSG with dynamic routing.

11. **How do you pass data between layouts?**
    Use React Context, URL search params, or cookies. Layouts can't pass props to each other directly.

12. **What is the `dynamic` route segment config?**
    It controls rendering behavior: `force-dynamic` (SSR), `force-static` (SSG), or `auto` (default based on data fetching).

13. **How do you implement authentication in the App Router?**
    Use middleware for route protection, Server Components for checking auth state, and Server Actions for login/logout.

14. **What is the purpose of `template.tsx`?**
    Templates wrap children like layouts but re-render on every navigation, useful for animations or re-triggering effects.

15. **How do you handle nested dynamic routes?**
    Use nested folders with `[param]` syntax. Each level can have its own `page.tsx`, `layout.tsx`, and `loading.tsx`.

### Senior (10-15)

16. **Design a multi-tenant application using the App Router.**
    Use middleware for tenant detection, route groups for tenant-specific layouts, and Server Components for data fetching with tenant context.

17. **How would you implement a micro-frontend architecture with the App Router?**
    Use Module Federation with `next/dynamic`, parallel routes for independent modules, and shared layouts for consistent UI.

18. **Explain the rendering pipeline for a nested layout.**
    Root layout renders → child layouts render → page renders. Each layout wraps its children. Loading states apply to the nearest Suspense boundary.

19. **How do you optimize bundle splitting in the App Router?**
    Use `next/dynamic` for lazy loading, route groups for logical splitting, and Server Components to keep client bundles small.

20. **Design a real-time dashboard with the App Router.**
    Use Server Components for initial data, client components for real-time updates, parallel routes for multiple views, and WebSocket for live data.

21. **How do you handle complex navigation patterns?**
    Use route groups for organization, parallel routes for simultaneous views, intercepting routes for modals, and middleware for conditional routing.

22. **Explain the relationship between layouts and caching.**
    Layouts are cached by default. Server Component layouts re-render only when their props change. Client Component layouts re-render on state changes.

23. **How do you implement i18n with the App Router?**
    Use middleware for locale detection, route groups for locale-specific content, and `generateStaticParams` for static locale pages.

24. **Design a page with multiple data dependencies with different loading states.**
    Use multiple Suspense boundaries with `loading.tsx` or inline `<Suspense>` components. Each data fetch gets its own loading state.

25. **How do you handle error recovery in nested layouts?**
    Use `error.tsx` at each layout level. Errors bubble up to the nearest error boundary. Implement retry logic in error components.

### FAANG-style (5-10)

26. **Design a routing system that handles 10K+ routes efficiently.**
    Use dynamic imports, implement route preloading, use edge middleware for fast matching, and leverage ISR for popular routes.

27. **How would you implement A/B testing with the App Router?**
    Use middleware to detect variants via cookies, serve different page variants, and cache each variant separately with ISR.

28. **Design a system for handling concurrent route transitions.**
    Use parallel routes for simultaneous rendering, implement optimistic updates, and use React transitions for smooth UI updates.

29. **How would you implement a route-level feature flag system?**
    Use Server Components to check flags, middleware for route protection, and dynamic imports for flag-based component loading.

30. **Design a multi-region routing system with edge functions.**
    Use Edge Runtime middleware for geo-routing, implement region-specific layouts, and use CDN caching for static content.

### Follow-ups (5-10)

31. **What are the limitations of the App Router?**
    Complex mental model, learning curve from Pages Router, potential for excessive server rendering, and compatibility issues with some libraries.

32. **How do you migrate from Pages Router to App Router?**
    Migrate incrementally, use `pages/_app.tsx` alongside `app/layout.tsx`, and leverage `next/dynamic` for gradual migration.

33. **What is the impact of App Router on bundle size?**
    Server Components reduce client bundles, but the framework itself is larger. Use `next/dynamic` for code splitting.

34. **How do you test App Router applications?**
    Use `next/jest` for unit tests, Playwright for E2E tests, and test Server Components with `@testing-library/react`.

35. **What is the future of the App Router?**
    Continued optimization, better DevTools, improved caching, and deeper React Server Component integration.

36. **How do you handle complex form workflows with the App Router?**
    Use Server Actions for form submission, client components for form state, and route handlers for API fallback.

37. **What is the relationship between App Router and React 18+?**
    App Router leverages React 18 features: Server Components, Suspense, transitions, and streaming SSR.

38. **How do you optimize navigation performance?**
    Use `next/link` for prefetching, implement route preloading, use streaming SSR, and leverage caching strategies.

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

## References & Learn More

- [Next.js Docs: App Router](https://nextjs.org/docs/app/building-your-application/routing)
- [App Router Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)
- [Next.js Routing Fundamentals](https://nextjs.org/docs/getting-started/installation)
