# React & Next.js Cheat Sheet

## Quick Reference Table

| Concept | Key Point | Code/Example |
|---------|-----------|--------------|
| Component | Function that returns JSX; re-renders on state/prop change | `function Button({ label }) { return <button>{label}</button>; }` |
| JSX | Syntax extension; compiles to `createElement` calls | `<div className="x">` → `createElement('div', {className: 'x'})` |
| Virtual DOM | In-memory representation; diffing compares old vs new trees | Enables efficient DOM updates |
| Reconciliation | Diffing algorithm; O(n) by assuming different types = full rebuild | Keys help identify which items changed |
| Fiber | Reconciler architecture; work units with priority; enables scheduling | Allows pausing, resuming, aborting work |
| Concurrent Features | `useTransition`, `useDeferredValue`, Suspense — non-blocking rendering | Keep UI responsive during heavy updates |
| `useState` | State hook; returns `[value, setter]`; setter triggers re-render | `const [count, setCount] = useState(0);` |
| `useEffect` | Side effects after render; cleanup on unmount or before next effect | `useEffect(() => { fetchData(); return cleanup; }, [dep])` |
| `useContext` | Consume context without nesting consumers | `const value = useContext(MyContext);` |
| `useRef` | Mutable ref object; persists across renders; DOM element access | `const inputRef = useRef(null);` |
| `useMemo` | Memoize computed value; recompute only when deps change | `const sorted = useMemo(() => items.sort(), [items]);` |
| `useCallback` | Memoize function reference; prevent child re-renders | `const fn = useCallback(() => doSomething(a), [a]);` |
| `useReducer` | Complex state logic; `(state, action) => newState` | `const [state, dispatch] = useReducer(reducer, init);` |
| `useLayoutEffect` | Fires synchronously after DOM mutations, before paint | Use for measuring DOM elements |
| `useImperativeHandle` | Customize ref value exposed to parent | `useImperativeHandle(ref, () => ({ focus: () => ... }));` |
| `useTransition` | Mark state update as non-urgent; allows interruption | `const [isPending, startTransition] = useTransition();` |
| `useDeferredValue` | Defer re-render of non-urgent part; shows stale value while pending | `const deferredQuery = useDeferredValue(query);` |
| `useId` | Generate unique, stable ID for accessibility | `const id = useId();` → `"::r1"` |
| Server Component | Default in App Router; runs on server; can access DB directly | No `'use client'` directive at top |
| Client Component | `'use client'` directive; runs in browser; can use hooks | Required for `useState`, `useEffect`, event handlers |
| Server Actions | `'use server'` directive; functions called from client, execute on server | `async function submitForm(data: FormData) { 'use server'; }` |
| App Router | File-based routing in `app/` directory; layouts, loading, error boundaries | `app/dashboard/layout.tsx` wraps `app/dashboard/page.tsx` |
| Pages Router | File-based in `pages/` directory; `getServerSideProps`, `getStaticProps` | Legacy, still supported |
| Layouts | Nested layouts persist across navigations; no remount | `app/layout.tsx` → wraps all pages |
| Loading UI | `loading.tsx` — shows Suspense fallback while route segment loads | `app/dashboard/loading.tsx` |
| Error Boundaries | `error.tsx` — catches errors in route segment | `app/dashboard/error.tsx` |
| Not Found | `not-found.tsx` — custom 404 for route segment | `app/not-found.tsx` |
| Middleware | Runs before request completes; can rewrite, redirect, set headers | `middleware.ts` in project root |
| Route Handlers | `route.ts` — API endpoints in App Router | `export async function GET() { return Response.json({}); }` |
| Metadata API | `generateMetadata` — SEO metadata per route | `export const metadata: Metadata = { title: 'Page' };` |
| Dynamic Routes | `[slug]` — catch dynamic segments; `[[...slug]]` for optional | `app/blog/[slug]/page.tsx` |
| Catch-All Routes | `[...slug]` — matches `/a/b/c` as `params.slug = ['a','b','c']` | `app/docs/[...slug]/page.tsx` |
| Parallel Routes | `@slot` — render multiple pages simultaneously in same layout | `app/dashboard/@analytics/page.tsx` |
| Intercepting Routes | `(..)` — intercept modal navigation; `(.)` same level, `(...)` root | `(..)comments` intercepts `/comments` |
| Caching (Data) | `fetch` in Server Components cached by default; `revalidate` controls | `fetch(url, { next: { revalidate: 3600 } })` |
| Caching (Router) | Client-side cache of route segments; preloaded for instant navigation | Router Cache: in-memory, per-session |
| ISR | Incremental Static Regeneration; regenerate static pages at runtime | `export const revalidate = 60;` per page |
| Streaming | Send HTML progressively; Suspense boundaries define chunks | `<Suspense fallback={<Loading />}>` |
| `fetch` in RSC | Deduped, cached by default; set `cache: 'no-store'` for fresh | `const data = await fetch(url, { cache: 'no-store' });` |
| `cookies()` / `headers()` | Read cookies/headers in Server Components and Route Handlers | `const token = cookies().get('token');` |
| `redirect()` | Redirect from Server Component or Server Action | `redirect('/login');` |
| `notFound()` | Trigger 404 from Server Component | `if (!post) notFound();` |
| `useRouter()` | Client-side navigation; `push`, `replace`, `back`, `prefetch` | `const router = useRouter(); router.push('/dashboard');` |
| `usePathname()` | Current URL pathname (client) | `const pathname = usePathname();` |
| `useSearchParams()` | URL search params (client) | `const [searchParams] = useSearchParams();` |
| `useParams()` | Dynamic route params (client) | `const { slug } = useParams();` |
| `useSelectedLayoutSegment()` | Active child segment under a layout | `const segment = useSelectedLayoutSegment('nav');` |
| `next/image` | Optimized images; lazy loading, resize, WebP | `<Image src="/pic.jpg" alt="..." width={500} height={300} />` |
| `next/font` | Self-host fonts; zero layout shift; CSS variables | `const inter = Inter({ subsets: ['latin'] });` |
| `next/link` | Client-side navigation; prefetch on hover/viewport | `<Link href="/about">About</Link>` |
| `next/script` | Script loading strategies: `beforeInteractive`, `afterInteractive`, `lazyOnload` | `<Script src="..." strategy="lazyOnload" />` |
| `next/headers` | Read request headers/cookies (server only) | `import { headers, cookies } from 'next/headers';` |
| Prisma (Next.js) | Instantiate outside route handlers to reuse connection | `const prisma = new PrismaClient();` (singleton in `lib/prisma.ts`) |
| `generateStaticParams` | Pre-generate dynamic routes at build time | `export async function generateStaticParams() { return [{ slug: '...' }]; }` |
| `generateMetadata` | Dynamic metadata per page | `export async function generateMetadata({ params }) { return { title: params.slug }; }` |

## Top 10 Things to Remember

1. **Server Components are the default in App Router**. They run only on the server, can directly access databases, and send zero JavaScript to the client. Add `'use client'` only when you need hooks, event handlers, or browser APIs.

2. **Fiber architecture enables scheduling**. React can pause, resume, and prioritize renders. `useTransition` and `useDeferredValue` leverage this for non-blocking updates.

3. **Keys matter for reconciliation**. Always provide stable, unique keys. Never use array index as key (causes reorder bugs). Keys help React identify which items changed, were added, or removed.

4. **Layouts persist across navigations**. A layout in `app/dashboard/layout.tsx` wraps all children under `/dashboard`. It does NOT remount when navigating between child routes — preserving state and DOM.

5. **Server Actions replace API routes for mutations**. Define with `'use server'`. Called directly from client components. Handle form submissions, data mutations, and revalidation without writing fetch calls.

6. **Streaming sends HTML progressively**. Wrap slow data fetches in `<Suspense>` to send the shell immediately, then stream resolved content. Users see the UI faster.

7. **Middleware runs on the Edge**. It intercepts requests before they reach the route. Use for auth checks, redirects, rewrites, geo-based routing. Runs on Edge runtime (limited APIs).

8. **`fetch` in Server Components is deduped and cached**. Multiple `fetch` calls for the same URL in one render are deduplicated. Set `cache: 'no-store'` or `next: { revalidate: N }` to control caching.

9. **`useTransition` for non-urgent updates**. Wrapping a setState in `startTransition` marks it as low-priority. React can interrupt it for urgent updates (typing, clicks). Returns `isPending` for loading states.

10. **`useDeferredValue` defers re-renders**. Pass a value that React can defer updating. Shows stale value while computing new one. Great for search inputs filtering large lists.

## Common Patterns

### Data Fetching with Loading States
```tsx
// app/posts/page.tsx (Server Component)
import { Suspense } from 'react';

export default function PostsPage() {
  return (
    <div>
      <h1>Posts</h1>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsList />
      </Suspense>
    </div>
  );
}

async function PostsList() {
  const posts = await fetch('https://api.example.com/posts')
    .then(res => res.json());
  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  );
}
```

### Form with Server Action
```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.post.create({ data: { title, content } });
  revalidatePath('/posts');
  redirect('/posts');
}

// app/posts/new/page.tsx
import { createPost } from '../actions';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Auth Middleware
```ts
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add user info to headers for downstream use
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-user-id', decoded.userId);

  return NextResponse.next({ request: { headers: requestHeaders } });
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

### Parallel Routes (Modal)
```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
}) {
  return (
    <div className="dashboard">
      {children}
      {analytics}
    </div>
  );
}

// app/dashboard/@analytics/page.tsx
export default function AnalyticsPage() {
  return <div className="analytics-panel">...</div>;
}
```

### Intercepting Routes (Modal)
```tsx
// app/@modal/(..)photos/[id]/page.tsx
import Modal from '@/components/Modal';

export default function PhotoModal({ params }: { params: { id: string } }) {
  return (
    <Modal>
      <img src={`/photos/${params.id}`} alt="Photo" />
    </Modal>
  );
}
```

### Optimistic Updates with `useOptimistic`
```tsx
'use client';
import { useOptimistic } from 'react';

function TodoList({ todos, addTodo }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: string) => [...state, { id: Date.now(), text: newTodo, done: false }]
  );

  async function handleAdd(formData: FormData) {
    const text = formData.get('text') as string;
    addOptimisticTodo(text); // Show immediately
    await addTodo(text);     // Server mutation
  }

  return (
    <form action={handleAdd}>
      <ul>{optimisticTodos.map(t => <li key={t.id}>{t.text}</li>)}</ul>
      <input name="text" />
    </form>
  );
}
```

### Route Handler (API)
```ts
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const page = searchParams.get('page') || '1';

  const users = await db.user.findMany({
    skip: (parseInt(page) - 1) * 10,
    take: 10,
  });

  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}
```

### Streaming with Suspense + Loading
```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/3 mb-4" />
      <div className="grid grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="h-32 bg-gray-200 rounded" />
        ))}
      </div>
    </div>
  );
}
```

### Context + Provider Pattern
```tsx
// contexts/theme.tsx
'use client';
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext<{
  theme: 'light' | 'dark';
  toggle: () => void;
} | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const toggle = () => setTheme(t => t === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be inside ThemeProvider');
  return ctx;
};
```

### `generateStaticParams` + `generateMetadata`
```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }) {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(r => r.json());
  return { title: post.title, description: post.excerpt };
}

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(r => r.json());
  return <article><h1>{post.title}</h1><p>{post.content}</p></article>;
}
```

## Red Flags (Things NOT to Say)

- **"I put everything in `'use client'`"** — Defeats the purpose of Server Components. Keep as much as possible on the server.
- **"useEffect is the right place for data fetching"** — In Next.js App Router, fetch directly in Server Components. `useEffect` for data fetching leads to waterfalls, no SSR, and extra loading states.
- **"I use `any` for props"** — Define proper interfaces. `FC<Props>` or explicit prop types.
- **"I never use keys on list items"** — Causes reconciliation bugs. Always use stable, unique keys.
- **"useCallback and useMemo are always needed"** — Premature optimization. Profile first. Most components don't need them.
- **"Server Components can't use state"** — Correct, but say: "Server Components handle rendering and data fetching. Client Components handle interactivity. They compose together."
- **"I don't see the point of layouts"** — Layouts prevent remounting, preserve state, and share UI across routes. Essential for dashboard-style apps.
- **"Middleware is for heavy logic"** — Middleware runs on Edge (limited runtime). Keep it lightweight: auth checks, redirects, headers.
- **"I use Pages Router, App Router is too new"** — App Router is the recommended approach. Pages Router is legacy. Know both, prefer App Router.
- **"I don't need loading states"** — Streaming + Suspense + `loading.tsx` provide instant feedback. Users should never stare at a blank screen.

## Green Flags (Things TO Say)

- **"Server Components are the default; I only add `'use client'` when interactivity is needed."** — Shows understanding of the architecture.
- **"I use Server Actions for mutations — no manual fetch calls for form submissions."** — Modern Next.js pattern.
- **"Layouts preserve state across navigations; I use them for shared UI and persistent sidebars."** — Core App Router concept.
- **"Streaming with Suspense sends the shell immediately, then streams data-dependent content."** — Performance optimization.
- **"I use `useTransition` for non-urgent state updates to keep the UI responsive."** — Concurrent React features.
- **"Middleware handles auth checks and redirects at the edge before the route renders."** — Correct middleware use case.
- **"I use `generateStaticParams` to pre-render dynamic routes at build time for performance."** — ISR/static generation.
- **"Keys should be stable, unique IDs — never array indices."** — Reconciliation best practice.
- **"I separate server and client concerns: data fetching on server, interactivity on client."** — Clean architecture.
- **"I use optimistic updates with `useOptimistic` for instant UI feedback during mutations."** — Advanced UX pattern.

## 5-Minute Pre-Interview Review

- **Component**: Function returning JSX. Re-renders on state/prop changes. Server Components (default in App Router) run on server; Client Components (`'use client'`) run in browser.
- **Hooks**: `useState` (state), `useEffect` (side effects), `useContext` (context), `useRef` (mutable ref), `useMemo` (memoize value), `useCallback` (memoize function), `useReducer` (complex state), `useTransition` (non-urgent updates), `useDeferredValue` (defer re-render).
- **Fiber**: Reconciler architecture. Work units with priority. Enables scheduling, interruption, and concurrent features. O(n) diffing with keys.
- **App Router**: File-based in `app/`. Layouts (`layout.tsx`), loading (`loading.tsx`), error (`error.tsx`), not-found (`not-found.tsx`). Nested layouts persist across navigations.
- **Server Components**: Default. Run on server. Can access DB, files, secrets. Zero JS sent to client. Compose with Client Components.
- **Client Components**: `'use client'` at top. Can use hooks, event handlers, browser APIs. Send JS to client. Use for interactivity.
- **Server Actions**: `'use server'` directive. Functions called from client, execute on server. Handle form submissions without API routes. `revalidatePath`/`revalidateTag` for cache invalidation.
- **Middleware**: `middleware.ts` in root. Runs before request completes. Auth, redirects, rewrites, headers. Edge runtime.
- **Caching**: `fetch` in RSC cached by default. `revalidate: N` for ISR. `cache: 'no-store'` for dynamic. Router Cache for client-side navigation.
- **Streaming**: `<Suspense>` boundaries define chunks. HTML sent progressively. `loading.tsx` for route-level loading UI.
- **Key APIs**: `generateStaticParams`, `generateMetadata`, `cookies()`, `headers()`, `redirect()`, `notFound()`, `useRouter()`, `usePathname()`, `useSearchParams()`, `useParams()`.

---

## References & Learn More
- [Cheat Sheet Collection](https://github.com/detailyang/awesome-cheatsheet)
- [DevHints](https://devhints.io/)
- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
