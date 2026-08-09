---
section: React
category: Frontend
tags: [concept]
---

# Modern React Hooks: useTransition, useDeferredValue, use, useOptimistic, and React 19 APIs

## TL;DR

React 18 introduced concurrent rendering and two key hooks: `useTransition` (mark state updates as non-urgent) and `useDeferredValue` (defer a value to keep the UI responsive). React 19 (stable) adds `use(promise)` to read resources in render, `useOptimistic` for instant UI feedback on mutations, ref-as-prop (no more `forwardRef`), and the `<Form>` Actions API. These are the modern primitives for senior-level React work.

## Why It Matters

Senior interviews increasingly test knowledge of concurrent React, suspense for data fetching, and React 19's new patterns. Knowing the difference between `useTransition` and `useDeferredValue` (one wraps a setter, the other wraps a value) and when to use `useOptimistic` (mutations with rollback) is what separates senior from mid-level candidates. These hooks also unlock measurable UX wins: typing in a search box stays at 60fps even during a slow filter.

## Definition

These are the post-React-18 hooks that handle asynchronous, deferred, or optimistic UI state. They integrate with the concurrent renderer and Suspense to keep the UI responsive even when work is slow.

## Why Do We Need It?

1. **Keep input responsive during slow renders** — `useTransition` and `useDeferredValue` prevent the UI from freezing
2. **Read promises directly in render** — `use(promise)` (React 19) eliminates manual `useEffect` + state for async data
3. **Instant UI feedback** — `useOptimistic` shows the expected result before the server confirms
4. **Less boilerplate** — Actions (`<Form action={fn}>`) replace `onSubmit` + `fetch` + `useState` patterns
5. **Native form handling** — React 19's `<Form>` integrates with Server Actions and progressive enhancement

## How It Works

### useTransition — Mark Updates as Non-Urgent

```typescript
import { useTransition, useState } from 'react';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Result[]>([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Urgent: keep the input responsive
    setQuery(value);
    // Non-urgent: can be interrupted, deferred, or abandoned
    startTransition(async () => {
      const data = await fetchResults(value);
      setResults(data);
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultList results={results} />
    </>
  );
}
```

`useTransition` returns `[isPending, startTransition]`. The wrapped update runs at a lower priority — if a more urgent update (like typing) comes in, the in-progress transition is interrupted and restarted.

### useDeferredValue — Defer a Value

```typescript
import { useDeferredValue, useState, useMemo } from 'react';

function FilteredList({ items }: { items: Item[] }) {
  const [filter, setFilter] = useState('');
  // deferredFilter lags behind filter on slow renders
  const deferredFilter = useDeferredValue(filter);
  const isStale = filter !== deferredFilter;

  const filtered = useMemo(
    () => items.filter(i => i.name.includes(deferredFilter)),
    [items, deferredFilter]
  );

  return (
    <>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      <div style={{ opacity: isStale ? 0.6 : 1 }}>
        {filtered.map(item => <Item key={item.id} {...item} />)}
      </div>
    </>
  );
}
```

**`useTransition` vs `useDeferredValue`:**
- `useTransition` wraps a state setter. Use when YOU control the update.
- `useDeferredValue` wraps a value. Use when a value comes from props or a parent.

### useOptimistic — Instant UI for Mutations

```typescript
import { useOptimistic, useState } from 'react';

function CommentList({ serverComments, addComment }: Props) {
  const [optimisticComments, addOptimistic] = useOptimistic(
    serverComments,
    (state, action: { text: string; id: number }) => [
      ...state,
      { id: action.id, text: action.text, pending: true },
    ]
  );

  const handleAdd = async (text: string) => {
    const tempId = Date.now();
    addOptimistic({ text, id: tempId });
    await addComment(text); // server mutation
    // If it throws, optimistic update is rolled back
  };

  return (
    <ul>
      {optimisticComments.map(c => (
        <li key={c.id} style={{ opacity: c.pending ? 0.5 : 1 }}>
          {c.text} {c.pending && '(sending...)'}
        </li>
      ))}
    </ul>
  );
}
```

The optimistic state is shown immediately; if the mutation fails, React rolls it back automatically.

### use(promise) — Read Resources in Render (React 19)

```typescript
import { use, Suspense } from 'react';

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  // 'use' suspends the component until the promise resolves
  const user = use(userPromise);
  return <h1>{user.name}</h1>;
}

function App() {
  const userPromise = fetchUser(123);
  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

`use` differs from `await`:
- `use` is a hook that works in render (not async functions)
- Suspends the component until the promise resolves
- Works with `<Suspense>` boundary for fallback UI
- Replaces the `useEffect` + `useState` + loading boolean pattern

### `<Form>` Actions (React 19)

```typescript
// Before: manual submit + state + error handling
function OldForm() {
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  return (
    <form onSubmit={async e => {
      e.preventDefault();
      setIsSubmitting(true);
      try { await api.updateName(name); } catch (err) { setError(err.message); }
      finally { setIsSubmitting(false); }
    }}>
      {/* ... */}
    </form>
  );
}

// After: declarative form action
function NewForm({ updateName }: { updateName: (formData: FormData) => Promise<void> }) {
  return (
    <form action={updateName}>
      <input name="name" />
      <SubmitButton />
    </form>
  );
}

import { useFormStatus, useFormState } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>;
}
```

### Refs as Props (React 19)

```typescript
// Before: forwardRef wrapper
const OldInput = forwardRef<HTMLInputElement, Props>((props, ref) => (
  <input ref={ref} {...props} />
));

// After: ref is a regular prop
function NewInput({ ref, ...props }: Props & { ref?: Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

No more `forwardRef`, no more `useImperativeHandle` boilerplate. `ref` is just a prop.

## Code Examples

### Real-World: Search with Smooth UX

```typescript
function ProductSearch() {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const filtered = useDeferredValue(products); // pretend filtering is slow
  // ... use query + filtered to render
}

// Pattern: keep input fast, defer the expensive part
```

### Real-World: Like Button with Optimistic Update

```typescript
function LikeButton({ postId, initialLikes, isLiked }: Props) {
  const [liked, setLiked] = useState(isLiked);
  const [optimisticLikes, setOptimisticLikes] = useOptimistic(
    initialLikes,
    (state) => liked ? state - 1 : state + 1
  );

  const handleClick = async () => {
    setOptimisticLikes(null); // trigger update
    setLiked(!liked);
    await api.toggleLike(postId);
  };

  return <button onClick={handleClick}>♥ {optimisticLikes}</button>;
}
```

### Real-World: Async Data Without useEffect

```typescript
// Before (React 18+): useEffect + state
function Profile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true);
    fetchUser(userId).then(u => {
      setUser(u);
      setLoading(false);
    });
  }, [userId]);
  if (loading) return <Spinner />;
  return <h1>{user?.name}</h1>;
}

// After (React 19): use + Suspense
function Profile({ userId }: { userId: string }) {
  const user = use(fetchUser(userId)); // suspends until resolved
  return <h1>{user.name}</h1>;
}
// Wrap in <Suspense fallback={<Spinner />}> higher up
```

## Real-World Use Cases

1. **Search-as-you-type** — `useTransition` keeps the input snappy while filtering/ranking runs
2. **Long lists with filters** — `useDeferredValue` defers heavy re-renders when filters change
3. **Mutations with rollback** — `useOptimistic` for likes, comments, todos, cart updates
4. **Data fetching** — `use(promise)` + `<Suspense>` for clean async data without `useEffect` boilerplate
5. **Form submissions** — React 19's `<Form action>` for progressive-enhancement-friendly forms
6. **Server Components + Client Islands** — `use` lets client components suspend on promises passed from server components

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wrapping the input value setter in `useTransition` | Only wrap slow updates; keep input updates urgent |
| Using `useTransition` for every state update | It's for non-urgent work. Synchronous trivial updates don't need it |
| Using `useDeferredValue` for a value that's already fast | Only use it for values that cause slow renders (large lists, complex derived data) |
| `useOptimistic` for non-undoable operations | Optimistic updates roll back on failure — if the user expects confirmation, don't use it |
| Using `use` in a Server Component | `use` only works in Client Components. Server Components `await` directly |
| Putting `use(promise)` outside a `<Suspense>` boundary | Without a boundary, the suspension bubbles to the root and shows nothing |
| Forgetting that `use` re-suspends on every render with a new promise | The promise should be stable (cached, deduped) — use React Query, SWR, or a memoized fetch |

## Best Practices

1. **Use `useTransition` for state updates triggered by user input that you expect to be slow** — typing, clicking, dragging
2. **Use `useDeferredValue` for values that come from props or external state** — derived data, search filters
3. **Always wrap `use(promise)` consumers in `<Suspense>`** — the boundary defines the fallback UI
4. **Use `useOptimistic` only for idempotent, low-risk operations** — likes, toggles; not for payments or destructive actions
5. **Cache the promises you pass to `use`** — without caching, every render creates a new promise and triggers a new fetch
6. **For React 19: use `ref` as a prop** — `forwardRef` is no longer needed
7. **For React 19: prefer `<Form action>` over `onSubmit` + state** — the framework handles pending, errors, and progressive enhancement
8. **Don't reach for these hooks for trivial updates** — `useState` is still the default. Concurrent hooks solve specific UX problems.

## Performance Considerations

| Pattern | Use Case | Tradeoff |
|---------|----------|----------|
| `useTransition` | Slow state updates from user input | Adds slight overhead; interrupts can cause minor re-work |
| `useDeferredValue` | Slow derived values from input | Doubles render count in worst case (urgent + deferred) |
| `useOptimistic` | Mutations with fast feedback | Requires rollback handling; can confuse if server fails |
| `use(promise)` + Suspense | Async data fetching | Suspends the tree; needs a boundary; caching is your responsibility |
| `<Form action>` | Form submissions | Server Actions require framework support (Next.js, Remix) or a custom integration |

**Heuristic:**
- Render time < 16ms (one frame)? → No concurrent hooks needed
- Render time 16-100ms? → `useTransition` or `useDeferredValue`
- Render time > 100ms? → Optimize the work first (virtualization, memoization); then add concurrent hooks if needed
- Mutation should feel instant? → `useOptimistic` (with rollback)

## Summary

React 18's concurrent hooks (`useTransition`, `useDeferredValue`) and React 19's new APIs (`use`, `useOptimistic`, ref-as-prop, `<Form action>`) are the modern primitives for senior-level React work. Use them to keep input responsive, integrate async data without `useEffect`, and ship instant feedback on mutations. Default to plain `useState` — these are for specific UX problems, not everyday state.

## Cheat Sheet

| Hook / API | Version | Use When | Replaces |
|------------|---------|----------|----------|
| `useTransition` | 18 | Wrapping a slow state update you control | `setTimeout(0)` hacks, debounced setState |
| `useDeferredValue` | 18 | Deferring a value that causes slow renders | `useMemo` with custom debounce |
| `useOptimistic` | 19 | Show mutation result before server confirms | Manual optimistic + rollback state |
| `use(promise)` | 19 | Read a Promise in render with Suspense | `useEffect` + `useState` + loading boolean |
| `useFormStatus` | 19 | Read pending state inside a `<Form>` | Manual `isSubmitting` state |
| `useFormState` | 19 | Form action with return value (errors, etc.) | Manual form state management |
| Refs as props | 19 | Pass `ref` without `forwardRef` | `forwardRef` + `useImperativeHandle` |
| `<Form action>` | 19 | Form submissions with progressive enhancement | `onSubmit` + `fetch` + state |

---

## See Also
- [Fiber](02-Fiber.md)
- [Performance](13-Performance.md)
- [Reconciliation](03-Reconciliation.md)
- [State Management](14-State-Management.md)
- [Suspense](11-Suspense.md)

## References & Learn More

- [React Docs: useTransition](https://react.dev/reference/react/useTransition)
- [React Docs: useDeferredValue](https://react.dev/reference/react/useDeferredValue)
- [React Docs: useOptimistic](https://react.dev/reference/react/useOptimistic)
- [React 19 Blog Post](https://react.dev/blog/2024/12/05/react-19)
- [React Docs: use (React 19)](https://react.dev/reference/react/use)
- [Patterns.dev: Concurrent UI Patterns](https://www.patterns.dev/react/concurrent-patterns)
