# Rendering

## Definition

Rendering in React is the process of calling component functions to produce a Virtual DOM tree, which React then uses to determine what changes to apply to the real DOM. It's important to understand that "rendering" in React does **not** mean updating the DOM — it means calling your component functions to produce a description of what the UI should look like.

React's rendering process has two distinct phases:
1. **Render Phase**: Calls component functions, creates Virtual DOM, diffs (reconciliation). This phase is **interruptible** and has **no side effects**.
2. **Commit Phase**: Applies changes to the DOM, runs effects. This phase is **synchronous** and **cannot be interrupted**.

## Why Do We Need It?

### Understanding Rendering Triggers

Many React performance issues stem from misunderstanding when and why re-renders happen. Understanding rendering helps you:
1. **Avoid unnecessary re-renders**: Know what triggers a re-render
2. **Optimize performance**: Use memoization effectively
3. **Debug issues**: Understand why components re-render unexpectedly
4. **Use concurrent features**: Know when updates can be deferred

### Common Misconceptions

```text
Common Rendering Misconceptions:
═══════════════════════════════════════════════════════════════

❌ "setState immediately updates the DOM"
✅ setState schedules a re-render. DOM updates happen in commit phase.

❌ "Re-rendering means the component function runs again"
✅ Re-rendering means React calls your component function to produce new Virtual DOM.

❌ "useEffect runs after rendering"
✅ useEffect runs after the browser paints (commit phase + paint).

❌ "useLayoutEffect runs after DOM updates"
✅ useLayoutEffect runs after DOM mutations but before browser paint.

❌ "React only re-renders changed components"
✅ React re-renders changed components AND their ancestors (unless memoized).
```

## How It Works

### The Rendering Pipeline

```text
Rendering Pipeline:
═══════════════════════════════════════════════════════════════

State Change / Prop Change / Parent Re-render
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                 RENDER PHASE (Interruptible)            │
│                                                         │
│ 1. Call component function                              │
│    - Execute function body                              │
│    - Call hooks in order                                │
│    - Return JSX (Virtual DOM)                           │
│                                                         │
│ 2. Reconcile (Diff)                                     │
│    - Compare new Virtual DOM with previous              │
│    - Determine what changed                             │
│    - Mark fibers with flags (Placement, Update, etc.)  │
│                                                         │
│ 3. Collect Effects                                      │
│    - Gather useEffect callbacks                         │
│    - Gather useLayoutEffect callbacks                   │
│    - Gather cleanup functions                           │
│                                                         │
│ ⚡ Can be INTERRUPTED at any point                      │
│ ⚡ No DOM changes, no side effects                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 COMMIT PHASE (Synchronous)               │
│                                                         │
│ 1. Before Mutation                                      │
│    - getSnapshotBeforeUpdate                            │
│                                                         │
│ 2. Mutation (DOM Updates)                                │
│    - Apply Placement (insert DOM nodes)                 │
│    - Apply Update (modify DOM attributes/text)          │
│    - Apply Deletion (remove DOM nodes)                  │
│                                                         │
│ 3. Layout                                               │
│    - useLayoutEffect callbacks                          │
│    - ref.current = ... (assign refs)                    │
│    - componentDidMount / componentDidUpdate            │
│                                                         │
│ 4. Passive (After Paint)                                │
│    - useEffect callbacks (async)                        │
│                                                         │
│ ❌ CANNOT be interrupted                                │
│ ❌ Synchronous, blocks rendering                        │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                 BROWSER PAINT                           │
│                                                         │
│ - Browser calculates layout (reflow)                    │
│ - Browser paints pixels (repaint)                       │
│ - Screen updates                                        │
└─────────────────────────────────────────────────────────┘
```

### Triggers for Re-render

```text
Re-render Triggers:
═══════════════════════════════════════════════════════════════

✅ Will trigger re-render:
├── setState() / useState setter
├── forceUpdate() (class components)
├── Parent component re-render (unless memoized)
├── Context value change
├── Custom hook returning new reference
└── useReducer dispatch

❌ Will NOT trigger re-render:
├── Direct DOM manipulation
├── Reading state without updating
├── Changing a ref (useRef)
├── Updating state to same value (primitives)
├── Updating state to same reference (objects)
└── Unmounted component
```

### Batch Updates

```text
Batch Updates (React 18):
═══════════════════════════════════════════════════════════════

React 18 automatically batches all state updates:

Event Handlers:
┌─────────────────────────────────────────────────────────────┐
│ const handleClick = () => {                                 │
│   setCount(c => c + 1);  // Update 1                       │
│   setName('John');       // Update 2                        │
│   setFlag(true);         // Update 3                        │
│ };                                                          │
│ // Only ONE re-render, not three!                           │
└─────────────────────────────────────────────────────────────┘

setTimeout:
┌─────────────────────────────────────────────────────────────┐
│ setTimeout(() => {                                          │
│   setCount(c => c + 1);  // Update 1                       │
│   setName('John');       // Update 2                        │
│ }, 1000);                                                   │
│ // Only ONE re-render (React 18)                            │
└─────────────────────────────────────────────────────────────┘

Promises:
┌─────────────────────────────────────────────────────────────┐
│ fetchData().then(data => {                                  │
│   setData(data);          // Update 1                       │
│   setLoading(false);      // Update 2                        │
│ });                                                         │
│ // Only ONE re-render (React 18)                            │
└─────────────────────────────────────────────────────────────┘

escape hatch: flushSync
┌─────────────────────────────────────────────────────────────┐
│ import { flushSync } from 'react-dom';                      │
│                                                             │
│ flushSync(() => {                                           │
│   setCount(c => c + 1);  // Update 1                       │
│ });                                                         │
│ // DOM updated immediately after this line                   │
│                                                             │
│ flushSync(() => {                                           │
│   setName('John');       // Update 2                        │
│ });                                                         │
│ // DOM updated again immediately                            │
└─────────────────────────────────────────────────────────────┘
```

### Concurrent Rendering

```text
Concurrent Rendering (React 18):
═══════════════════════════════════════════════════════════════

Traditional (Synchronous) Rendering:
┌─────────────────────────────────────────────────────────────┐
│ Frame 1: Render everything (50ms)                           │
│ Frame 2: Browser paints                                     │
│ Frame 3: Render more (50ms)                                 │
│ Frame 4: Browser paints                                     │
│                                                             │
│ Problem: Frame 1 and 3 are BLOCKED (jank)                  │
└─────────────────────────────────────────────────────────────┘

Concurrent Rendering:
┌─────────────────────────────────────────────────────────────┐
│ Frame 1: Render 20ms (yield to browser)                     │
│ Frame 2: Browser handles input (responsive!)                │
│ Frame 3: Render 20ms (yield to browser)                     │
│ Frame 4: Browser handles input (responsive!)                │
│ Frame 5: Render 20ms (yield to browser)                     │
│ Frame 6: All done! Commit to DOM                            │
│                                                             │
│ Benefit: Browser never blocked, UI stays responsive         │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Understanding Render Phase vs Commit Phase

```typescript
import React, { useState, useLayoutEffect, useEffect } from 'react';

const RenderCommitDemo = () => {
  const [count, setCount] = useState(0);

  console.log('1. RENDER PHASE: Component function called');

  useLayoutEffect(() => {
    console.log('2. COMMIT PHASE (Layout): After DOM mutation, before paint');
    // DOM is updated here, but browser hasn't painted yet
  }, [count]);

  useEffect(() => {
    console.log('3. COMMIT PHASE (Passive): After paint');
    // Browser has painted, safe to measure DOM
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
};

// Console output on click:
// 1. RENDER PHASE: Component function called
// 2. COMMIT PHASE (Layout): After DOM mutation, before paint
// 3. COMMIT PHASE (Passive): After paint
```

### Batch Updates

```typescript
import React, { useState } from 'react';

const BatchUpdateExample = () => {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  const [flag, setFlag] = useState(false);

  console.log('Render! Count:', count, 'Name:', name, 'Flag:', flag);

  const handleClick = () => {
    // React 18 batches ALL of these into ONE re-render
    setCount(c => c + 1);
    setName('John');
    setFlag(true);
    // Only "Render!" logs once, with all three values updated
  };

  return (
    <div>
      <p>{count} - {name} - {flag ? 'ON' : 'OFF'}</p>
      <button onClick={handleClick}>Update All</button>
    </div>
  );
};
```

### flushSync for Immediate DOM Updates

```typescript
import { flushSync } from 'react-dom';

const FlushSyncExample = () => {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  const handleClick = () => {
    // Without flushSync: DOM updates after event handler
    // With flushSync: DOM updates immediately

    flushSync(() => {
      setCount(c => c + 1);
    });

    // DOM is now updated
    console.log(ref.current?.textContent); // Shows new count

    flushSync(() => {
      setCount(c => c + 1);
    });

    // DOM updated again
    console.log(ref.current?.textContent); // Shows count + 2
  };

  return (
    <div ref={ref}>
      <p>Count: {count}</p>
      <button onClick={handleClick}>Flush Sync</button>
    </div>
  );
};
```

### createRoot vs hydrateRoot

```typescript
import { createRoot, hydrateRoot } from 'react-dom/client';

// Client-side rendering (CSR)
const root = createRoot(document.getElementById('root')!);
root.render(<App />);
// React calls component functions, creates Virtual DOM, commits to DOM

// Server-side rendering (SSR) hydration
hydrateRoot(
  document.getElementById('root')!,
  <App />,
  {
    onHydrated: () => {
      console.log('Hydration complete');
    },
  }
);
// React skips calling component functions (server already did)
// React attaches event listeners and reconciles with server HTML
```

### Concurrent Features

```typescript
import React, { useState, useTransition, useDeferredValue } from 'react';

const ConcurrentRenderingDemo = () => {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const deferredQuery = useDeferredValue(query);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value); // High priority: update input immediately

    startTransition(() => {
      // Low priority: update results (can be interrupted)
      setFilteredResults(filterData(value));
    });
  };

  return (
    <div>
      <input value={query} onChange={handleSearch} />
      {isPending && <Spinner />}
      {/* deferredQuery lags behind query for smoother UI */}
      <Results query={deferredQuery} />
    </div>
  );
};
```

### Controlling Re-renders with React.memo

```typescript
import React, { useState, memo } from 'react';

const ExpensiveChild = memo(({ data, onClick }: { data: Data; onClick: () => void }) => {
  console.log('ExpensiveChild rendered'); // Only logs when props change
  return (
    <div onClick={onClick}>
      <p>{data.text}</p>
    </div>
  );
});

const Parent = () => {
  const [count, setCount] = useState(0);
  const [data] = useState({ text: 'Hello' });

  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  console.log('Parent rendered');

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      {/* ExpensiveChild only re-renders when data or onClick changes */}
      <ExpensiveChild data={data} onClick={handleClick} />
    </div>
  );
};
```

## Real-World Use Cases

### 1. Form with Real-time Validation

```typescript
const FormWithValidation = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Render phase: called on every keystroke
  // Validation runs in render phase (pure computation)
  const validate = useMemo(() => {
    const newErrors: Record<string, string> = {};
    if (formData.email && !formData.email.includes('@')) {
      newErrors.email = 'Invalid email';
    }
    if (formData.password && formData.password.length < 8) {
      newErrors.password = 'Password too short';
    }
    return newErrors;
  }, [formData]);

  // Update errors in render phase (no re-render needed)
  // React will use the new errors in the next render
  if (JSON.stringify(validate) !== JSON.stringify(errors)) {
    setErrors(validate); // This causes a re-render with updated errors
  }

  return (
    <form>
      <input
        value={formData.email}
        onChange={e => setFormData(prev => ({ ...prev, email: e.target.value }))}
      />
      {errors.email && <span>{errors.email}</span>}
      <input
        type="password"
        value={formData.password}
        onChange={e => setFormData(prev => ({ ...prev, password: e.target.value }))}
      />
      {errors.password && <span>{errors.password}</span>}
    </form>
  );
};
```

### 2. Dashboard with Auto-refresh

```typescript
const Dashboard = () => {
  const [metrics, setMetrics] = useState<Metrics>(initialMetrics);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      fetchMetrics().then(newMetrics => {
        setMetrics(newMetrics); // Triggers re-render
        setLastUpdated(new Date()); // Batched with above
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Last updated: {lastUpdated.toLocaleTimeString()}</p>
      <MetricCards metrics={metrics} />
    </div>
  );
};
```

### 3. Image Gallery with Lazy Loading

```typescript
const ImageGallery = ({ images }: { images: Image[] }) => {
  const [visibleImages, setVisibleImages] = useState<Image[]>([]);

  useEffect(() => {
    // Lazy load images as user scrolls
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const imageId = entry.target.getAttribute('data-image-id');
          setVisibleImages(prev => [...prev, images.find(i => i.id === imageId)!]);
        }
      });
    });

    // Observe image placeholders
    document.querySelectorAll('.image-placeholder').forEach(el => {
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, [images]);

  return (
    <div className="gallery">
      {images.map(image => (
        <div key={image.id} className="image-placeholder" data-image-id={image.id}>
          {visibleImages.includes(image) ? (
            <img src={image.url} alt={image.alt} />
          ) : (
            <Skeleton />
          )}
        </div>
      ))}
    </div>
  );
};
```

### 4. Context Provider with Performance

```typescript
const AppContext = React.createContext<AppContextType>(null!);

const AppProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [user, setUser] = useState<User | null>(null);

  // Memoize context value to prevent unnecessary re-renders
  const contextValue = useMemo(() => ({
    theme,
    user,
    setTheme,
    setUser,
  }), [theme, user]);

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};
```

## Common Mistakes

### 1. Assuming setState Updates DOM Immediately

```typescript
const Counter = () => {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  const handleClick = () => {
    setCount(c => c + 1);
    // ❌ WRONG: DOM not updated yet
    console.log(ref.current?.textContent); // Still shows old count
  };

  return (
    <div ref={ref}>
      <p>Count: {count}</p>
      <button onClick={handleClick}>Increment</button>
    </div>
  );
};

// ✅ CORRECT: Use flushSync or useEffect
const handleClick = () => {
  flushSync(() => {
    setCount(c => c + 1);
  });
  // DOM now updated
  console.log(ref.current?.textContent); // Shows new count
};
```

### 2. Re-rendering Entire Component Tree

```typescript
// ❌ BAD: Parent re-render causes all children to re-render
const Parent = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <Child1 /> {/* Re-renders unnecessarily */}
      <Child2 /> {/* Re-renders unnecessarily */}
      <Child3 /> {/* Re-renders unnecessarily */}
    </div>
  );
};

// ✅ GOOD: Memoize children
const Parent = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <React.memo(Child1) /> {/* Only re-renders if props change */}
      <React.memo(Child2) />
      <React.memo(Child3) />
    </div>
  );
};
```

### 3. Using useEffect for Derived State

```typescript
// ❌ BAD: useEffect for derived state causes unnecessary re-renders
const FilteredList = ({ items, query }: Props) => {
  const [filtered, setFiltered] = useState<string[]>([]);

  useEffect(() => {
    // This runs AFTER render, causing a second render
    setFiltered(items.filter(item => item.includes(query)));
  }, [items, query]);

  return <List items={filtered} />;
};

// ✅ GOOD: Compute during render (no extra re-render)
const FilteredList = ({ items, query }: Props) => {
  const filtered = useMemo(
    () => items.filter(item => item.includes(query)),
    [items, query]
  );

  return <List items={filtered} />;
};
```

### 4. Creating New References in Render

```typescript
// ❌ BAD: New object/function on every render
const Parent = () => {
  return (
    <Child
      style={{ color: 'red' }} // New object every render
      onClick={() => console.log('clicked')} // New function every render
    />
  );
};

// ✅ GOOD: Stabilize references
const Parent = () => {
  const style = useMemo(() => ({ color: 'red' }), []);
  const handleClick = useCallback(() => console.log('clicked'), []);

  return <Child style={style} onClick={handleClick} />;
};
```

## Best Practices

1. **Understand render phase vs commit phase**: Render is pure, commit has side effects.
2. **Don't call setState in render phase**: It causes infinite loops (except in conditions).
3. **Compute during render, not in useEffect**: Derived state should be computed synchronously.
4. **Use flushSync when you need immediate DOM updates**: For measurements after state change.
5. **Memoize expensive computations**: Use `useMemo` for costly calculations.
6. **Stabilize references**: Use `useCallback` for functions passed as props.
7. **Profile before optimizing**: Use React DevTools Profiler to find actual bottlenecks.

## Performance Considerations

### Rendering Cost Factors

| Factor | Impact | Mitigation |
|--------|--------|------------|
| Component count | More components = more rendering | Virtualization, lazy loading |
| Render complexity | Complex logic = slower render | Memoize, move to workers |
| Re-render frequency | Frequent updates = more renders | `React.memo`, state colocation |
| Tree depth | Deep trees = longer traversal | Flatten hierarchy |
| Context changes | Context updates re-render all consumers | Split contexts |

### When Rendering Is Expensive

- **Large component trees**: 1000+ components
- **Complex calculations**: Heavy computations in render
- **Frequent updates**: State changes every frame
- **Deep nesting**: 50+ levels of components
- **Unmemoized children**: All children re-render on parent update

### Optimization Checklist

1. ✅ Profile with React DevTools Profiler
2. ✅ Add `React.memo` to pure components
3. ✅ Use `useMemo` for expensive computations
4. ✅ Use `useCallback` for stable function references
5. ✅ Colocate state near where it's used
6. ✅ Split contexts to reduce consumer re-renders
7. ✅ Virtualize long lists
8. ✅ Lazy load heavy components

## Interview Questions

### Beginner (5-10)

**Q1: What is rendering in React?**
A: Rendering in React is the process of calling component functions to produce a Virtual DOM tree. It's not about updating the DOM — it's about producing a description of what the UI should look like.

**Q2: What is the difference between render phase and commit phase?**
A: The render phase calls component functions and creates Virtual DOM (interruptible, no side effects). The commit phase applies DOM changes and runs effects (synchronous, has side effects).

**Q3: When does useEffect run?**
A: `useEffect` runs after the browser paints the screen. It's asynchronous and doesn't block rendering. It's the right place for side effects that don't need to block paint.

**Q4: What is batch updating?**
A: Batch updating is React's optimization that groups multiple state updates into a single re-render. React 18 batches all updates automatically (in event handlers, setTimeout, promises, etc.).

**Q5: How do you prevent unnecessary re-renders?**
A: Use `React.memo` for pure components, `useMemo` for expensive computations, `useCallback` for stable function references, and colocate state near where it's used.

**Q6: What triggers a re-render?**
A: Re-renders are triggered by: state changes, parent re-renders, context changes, or force updates. Direct DOM manipulation, reading state, and ref changes do NOT trigger re-renders.

**Q7: What is `flushSync`?**
A: `flushSync` forces React to synchronously flush all pending updates. It's used when you need immediate DOM updates (e.g., measuring DOM after state change).

**Q8: What is `createRoot` vs `hydrateRoot`?**
A: `createRoot` is for client-side rendering — React calls component functions and creates the DOM. `hydrateRoot` is for SSR — React attaches event listeners to server-rendered HTML without calling component functions again.

**Q9: Can you call setState during render?**
A: Generally no — it causes infinite loops. Exception: calling setState conditionally (e.g., to update state based on props) is allowed if it terminates.

**Q10: What is the difference between `useLayoutEffect` and `useEffect`?**
A: `useLayoutEffect` runs synchronously after DOM mutations but before browser paint. `useEffect` runs asynchronously after paint. Use `useLayoutEffect` for DOM measurements, `useEffect` for everything else.

### Intermediate (5-10)

**Q11: Explain the complete rendering pipeline from state change to screen update.**
A:
1. State change triggers re-render
2. React calls component function (render phase)
3. Virtual DOM is created
4. React diffs new vs old Virtual DOM (reconciliation)
5. React marks fibers with flags (Placement, Update, Deletion)
6. React commits changes to DOM (commit phase)
7. Browser paints pixels to screen
8. useEffect callbacks run (passive effects)

**Q12: How does React batch updates in React 18?**
A: React 18 uses automatic batching. All state updates (in event handlers, setTimeout, promises, native event handlers) are batched into a single re-render. This is implemented via the `flushSync` escape hatch.

**Q13: What is the difference between synchronous and concurrent rendering?**
A: Synchronous rendering blocks the main thread until all rendering is complete. Concurrent rendering can pause, resume, and prioritize rendering work, keeping the UI responsive during heavy renders.

**Q14: How does `React.memo` prevent re-renders?**
A: `React.memo` wraps a component to skip re-rendering when props haven't changed (shallow comparison). If props are the same, React reuses the previous Virtual DOM, avoiding the render phase.

**Q15: What is the performance impact of inline objects in JSX?**
A: Inline objects create new references on every render. This causes child components to re-render (if not memoized) because the props have changed. Use `useMemo` to stabilize references.

**Q16: How does React handle re-renders during transitions?**
A: `useTransition` marks updates as non-urgent. React keeps the old UI visible while preparing the new one in the background. The transition can be interrupted if there's urgent work (e.g., user input).

**Q17: What is the difference between `useEffect` and `useLayoutEffect` timing?**
A:
```text
useLayoutEffect: DOM mutation → useLayoutEffect → browser paint
useEffect: DOM mutation → browser paint → useEffect
```
`useLayoutEffect` blocks paint; `useEffect` doesn't.

**Q18: How does React handle re-renders from context changes?**
A: When a context value changes, all consumers re-render. This is why you should split contexts — a single large context causes all consumers to re-render even if they only use a small part of the value.

**Q19: What is `React.Profiler` and how does it work?**
A: `React.Profiler` is a component that measures rendering performance. It provides an `onRender` callback with timing information (actual time, base time, commit time) for its subtree.

**Q20: How do you measure rendering performance in production?**
A:
1. React Profiler (development only)
2. Chrome DevTools Performance tab (record interactions)
3. React.Profiler component (programmatic profiling)
4. User-centric metrics (First Contentful Paint, Time to Interactive)

### Senior (10-15)

**Q21: Explain the relationship between React rendering and browser rendering.**
A: React rendering produces Virtual DOM and computes DOM changes. Browser rendering (paint) happens after React commits changes. They're separate processes — React runs in JavaScript, browser rendering runs in the rendering engine.

**Q22: How does concurrent rendering affect the rendering pipeline?**
A: Concurrent rendering adds interruption points in the render phase. React can pause rendering to handle urgent work, resume later, and prioritize different updates. The commit phase remains synchronous.

**Q23: What is the `startTransition` API and when should you use it?**
A: `startTransition` marks state updates as non-urgent transitions. Use it for:
- Search filtering (defer results)
- Tab switching (keep old tab visible)
- List updates (smooth scrolling)
Not for: input values, click handlers, urgent updates.

**Q24: How does React handle the "zombie children" problem?**
A: Zombie children occur when a component updates state after unmounting. React handles this by checking if the component is still mounted before committing. However, async operations in `useEffect` can still cause this — use AbortController to cancel them.

**Q25: Explain the performance implications of `useDeferredValue`.**
A: `useDeferredValue` creates a lagging version of a value. The source value updates immediately (high priority); the deferred value updates later (low priority). This keeps the UI responsive while allowing expensive updates to lag.

**Q26: How does React handle the "tearing" problem in concurrent rendering?**
A: Tearing occurs when different parts of the UI show inconsistent states during concurrent rendering. React prevents this by keeping the old UI visible until the new one is ready. `useDeferredValue` and `useTransition` help avoid tearing.

**Q27: What is the relationship between rendering and React DevTools?**
A: React DevTools hooks into React's internal rendering pipeline. It tracks component renders, measures performance, and displays the component tree. The Profiler uses `onRender` callbacks from `React.Profiler`.

**Q28: How does rendering differ between class and function components?**
A: Class components call `render()` method; function components call the function directly. The rendering process is the same — both produce Virtual DOM. Function components use hooks instead of lifecycle methods.

**Q29: What is the performance impact of nested memoization?**
A: Nested memoization (e.g., `React.memo` around components with `useMemo`/`useCallback`) creates a tree of memoized components. The overhead is minimal compared to the benefit of preventing unnecessary re-renders.

**Q30: How does React handle the "double render" in StrictMode?**
A: StrictMode intentionally double-renders components in development to detect side effects. This works because the render phase should be idempotent. Double-rendering catches bugs like missing cleanup functions.

### FAANG-style (5-10)

**Q31: Design a rendering optimization strategy for a large-scale application.**
A:
1. **Component architecture**: Flat hierarchy, small focused components
2. **State design**: Normalize state, colocate state, split contexts
3. **Memoization**: `React.memo` for pure components, `useMemo`/`useCallback` for expensive computations
4. **Virtualization**: Only render visible components
5. **Code splitting**: Lazy load heavy components
6. **Profiling**: Regular profiling with React DevTools

**Q32: How would you debug a rendering performance issue in production?**
A:
1. **User metrics**: Track FCP, TTI, LCP
2. **Chrome DevTools Performance**: Record interactions, analyze flame charts
3. **React.Profiler**: Add to suspected slow components
4. **Custom logging**: Log render times in production
5. **Sentry/error tracking**: Track slow renders

**Q33: Analyze the memory implications of rendering.**
A: Each render creates:
- New Virtual DOM tree (~1-2KB per component)
- New hooks state (if references change)
- New effect queues
For 10,000 components, that's ~10-20MB per render. Mitigate with virtualization and memoization.

**Q34: How would you implement a custom rendering scheduler?**
A:
1. **Priority model**: Define update priorities (urgent, normal, low)
2. **Task queue**: Sort tasks by priority
3. **Frame budget**: Execute tasks within 16ms frame
4. **Interruption**: Yield to browser when time runs out
5. **Integration**: Use React's `scheduler` package

**Q35: Design a rendering pipeline for a real-time collaborative app.**
A:
1. **CRDT state**: Conflict-free replicated data types
2. **Priority updates**: User's own changes > remote changes
3. **Batching**: Group related updates
4. **Virtualization**: Only render visible collaboration elements
5. **Concurrency**: Use `useTransition` for remote updates

**Q36: How does React Server Components affect rendering?**
A: Server Components don't participate in client-side rendering. They're serialized as references. Client Components render normally. React merges the server and client trees, reconciling only the client parts.

**Q37: Analyze the performance characteristics of different rendering strategies.**
A:
| Strategy | When to Use | Trade-off |
|----------|-------------|-----------|
| Full render | Simple apps | Simple but slow |
| Memoized render | Complex apps | Fast but memory overhead |
| Virtualized render | Long lists | Complex but efficient |
| Concurrent render | Heavy UI | Responsive but complex |
| Server render | SEO, initial load | Complex but fast first paint |

**Q38: How would you implement a rendering profiler for production?**
A:
1. **React.Profiler**: Add to components
2. **Custom hook**: Track render times
3. **Performance API**: Use `performance.mark()` and `performance.measure()`
4. **Analytics**: Send render metrics to backend
5. **Dashboard**: Visualize slow renders

**Q39: How does rendering interact with React Suspense?**
A: Suspense can "suspend" rendering during the render phase. When a component suspends, React pauses rendering of that subtree and shows the fallback. When the data loads, React resumes and completes the render.

**Q40: Design a system for A/B testing React rendering performance.**
A:
1. **Feature flags**: Toggle rendering optimizations
2. **Metrics**: Track render times, user engagement
3. **Randomization**: Randomly assign users to variants
4. **Analysis**: Compare performance between variants
5. **Rollback**: Quick rollback if performance degrades

### Follow-ups (5-10)

**Q41: How would you explain rendering to a non-technical stakeholder?**
A: "When you interact with our app, React figures out what parts of the screen need to change. It's like having a smart assistant who only updates the parts that actually need to change, instead of rebuilding the entire screen every time."

**Q42: What are the edge cases in rendering?**
A:
- Conditional hooks (illegal in React)
- Side effects in render phase (should be idempotent)
- Dynamic component types
- Suspense boundaries during concurrent rendering
- Error boundaries catching during render

**Q43: How does rendering handle the "state upgrade" pattern?**
A: State upgrades happen during render. If a component receives props that differ from state, you can compute derived state during render. This is the recommended pattern over `useEffect` for derived state.

**Q44: What is the relationship between rendering and React's strict mode?**
A: StrictMode intentionally double-renders in development to detect side effects. It doesn't affect production. Double-rendering catches bugs like missing cleanup functions and impure render functions.

**Q45: How does rendering differ in development vs production?**
A: Development: StrictMode double-renders, more warnings, slower. Production: No StrictMode checks, minified code, faster. Rendering logic is the same.

**Q46: What is the impact of React Compiler on rendering?**
A: React Compiler (experimental) automatically memoizes components and hooks. It reduces the need for manual `React.memo`, `useMemo`, and `useCallback`. It analyzes code at build time and adds memoization.

**Q47: How does rendering interact with React DevTools Profiler?**
A: Profiler uses `React.Profiler`'s `onRender` callback. It tracks render times, identifies slow components, and visualizes the rendering timeline. You can record interactions and analyze performance.

**Q48: How would you optimize rendering for a low-end device?**
A:
1. **Reduce component count**: Fewer components to render
2. **Simplify UI**: Less complex layouts
3. **Virtualization**: Only render visible content
4. **Code splitting**: Load only necessary code
5. **Defer non-urgent updates**: Use `useTransition`

**Q49: What is the future of React rendering?**
A: React is exploring:
- Automatic memoization via React Compiler
- Better concurrent rendering
- Offscreen rendering (Activity component)
- Improved Suspense integration
- Better error handling during concurrent rendering

**Q50: How does rendering interact with React's hydration?**
A: Hydration is the process of attaching React to server-rendered HTML. React skips calling component functions (server already did). It reconciles the client Virtual DOM with server HTML, attaching event listeners and updating DOM.

## Summary

Rendering in React is the process of calling component functions to produce a Virtual DOM tree. It has two phases: render (interruptible, no side effects) and commit (synchronous, applies DOM changes). Understanding rendering is crucial for performance optimization, debugging, and using concurrent features effectively.

## Cheat Sheet

```text
Rendering Key Points:
├── What: Calling component functions to produce Virtual DOM
├── Two Phases: Render (interruptible) → Commit (synchronous)
├── Render Phase: Call functions, create Virtual DOM, reconcile
├── Commit Phase: Apply DOM changes, run effects
├── Browser Paint: After commit phase
├── useEffect: Runs after paint (async)
├── useLayoutEffect: Runs after DOM mutation, before paint

Triggers:
├── setState / useState setter
├── Parent re-render (unless memoized)
├── Context value change
├── forceUpdate (class components)
├── Custom hook returning new reference

NOT Triggers:
├── Direct DOM manipulation
├── Reading state without updating
├── Changing a ref
├── Updating state to same value
└── Unmounted component

Batch Updates (React 18):
├── All state updates are batched automatically
├── Event handlers, setTimeout, promises — all batched
├── Use flushSync for immediate DOM updates
└── One re-render per batch

Performance:
├── Profile with React DevTools Profiler
├── Memoize pure components (React.memo)
├── Memoize expensive computations (useMemo)
├── Stabilize function references (useCallback)
├── Colocate state near usage
├── Split contexts to reduce re-renders
└── Virtualize long lists

Common Pitfalls:
├── Assuming setState updates DOM immediately
├── Re-rendering entire tree unnecessarily
├── Using useEffect for derived state
├── Creating new references in render
└── Not understanding render vs commit phase
```

## References & Learn More

- [React Docs: Rendering](https://react.dev/learn/react-dom-server-rendering)
- [A Comprehensive Guide to React Rendering Behavior](https://blog.savut.se/2021/03/a-comprehensive-guide-to-react-rendering-behavior/)
- [React Rendering](https://www.reactjs.org/docs/rendering-elements.html)
