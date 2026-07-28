---
section: React
category: Frontend
tags: [concept]
---

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

---

## See Also
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)
- [Form Handling](../29-Form-Handling/)
- [Animation](../30-Animation/)

## References & Learn More

- [React Docs: Rendering](https://react.dev/learn/react-dom-server-rendering)
- [A Comprehensive Guide to React Rendering Behavior](https://blog.savut.se/2021/03/a-comprehensive-guide-to-react-rendering-behavior/)
- [React Rendering](https://www.reactjs.org/docs/rendering-elements.html)
