# useEffect

## Definition

`useEffect` is a React Hook that lets you synchronize a component with an external system. It runs side effects after React has committed changes to the DOM. Side effects include data fetching, subscriptions, manually changing the DOM, and any other operations that can't be done during rendering.

`useEffect` replaces lifecycle methods from class components (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`) with a single, unified API.

## Why Do We Need It?

### The Problem

Function components are pure — they only take props and return JSX. But real applications need to interact with the outside world:
- Fetch data from APIs
- Set up WebSocket connections
- Subscribe to browser events
- Manipulate the DOM directly
- Set timers and intervals

Without `useEffect`, function components couldn't perform these operations.

### The Solution

`useEffect` provides a declarative way to perform side effects:

```typescript
// Data fetching
useEffect(() => {
  fetchData().then(data => setData(data));
}, []); // Run once on mount

// Event listeners
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []); // Clean up on unmount

// Subscriptions
useEffect(() => {
  const subscription = subscribe(channel);
  return () => subscription.unsubscribe();
}, [channel]); // Re-subscribe when channel changes
```

## How It Works

### useEffect Execution Flow

```
useEffect Execution Flow:
═══════════════════════════════════════════════════════════════

First Render:
┌─────────────────────────────────────────────────────────────┐
│ 1. Component function called                               │
│ 2. Virtual DOM created                                     │
│ 3. DOM updated (commit phase)                              │
│ 4. Browser paints                                          │
│ 5. useEffect(() => { ... }, []) runs (async)              │
└─────────────────────────────────────────────────────────────┘

Re-render (deps changed):
┌─────────────────────────────────────────────────────────────┐
│ 1. Component function called                               │
│ 2. New Virtual DOM created                                 │
│ 3. DOM updated                                             │
│ 4. Browser paints                                          │
│ 5. Previous useEffect cleanup runs                         │
│ 6. New useEffect runs                                      │
└─────────────────────────────────────────────────────────────┘

Re-render (deps NOT changed):
┌─────────────────────────────────────────────────────────────┐
│ 1. Component function called                               │
│ 2. New Virtual DOM created                                 │
│ 3. DOM updated                                             │
│ 4. Browser paints                                          │
│ 5. useEffect does NOT run (deps same)                      │
└─────────────────────────────────────────────────────────────┘

Unmount:
┌─────────────────────────────────────────────────────────────┐
│ 1. Component removed from tree                             │
│ 2. useEffect cleanup runs                                  │
│ 3. Component memory freed                                  │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Array

```
Dependency Array Behavior:
═══════════════════════════════════════════════════════════════

No Array (runs every render):
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   console.log('Runs after every render');                   │
│ });                                                         │
└─────────────────────────────────────────────────────────────┘

Empty Array (runs once on mount):
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   console.log('Runs once on mount');                        │
│   return () => console.log('Cleanup on unmount');          │
│ }, []);                                                     │
└─────────────────────────────────────────────────────────────┘

With Dependencies (runs when deps change):
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   console.log(`Runs when userId changes: ${userId}`);      │
│   return () => console.log('Cleanup before re-run');       │
│ }, [userId]);                                               │
└─────────────────────────────────────────────────────────────┘

Multiple Dependencies:
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   console.log('Runs when userId OR theme changes');        │
│ }, [userId, theme]);                                        │
└─────────────────────────────────────────────────────────────┘
```

### Cleanup Function

```
Cleanup Function:
═══════════════════════════════════════════════════════════════

When Cleanup Runs:
┌─────────────────────────────────────────────────────────────┐
│ 1. Before the effect re-runs (deps changed)                │
│ 2. When the component unmounts                              │
└─────────────────────────────────────────────────────────────┘

Example: Subscription with Cleanup
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   const subscription = subscribe(channel);                  │
│                                                             │
│   return () => {                                            │
│     subscription.unsubscribe(); // Cleanup                  │
│   };                                                        │
│ }, [channel]);                                              │
│                                                             │
│ Cleanup order:                                              │
│ 1. Component mounts → effect runs → subscription created   │
│ 2. Channel changes → cleanup runs → old subscription removed│
│ 3. Effect runs again → new subscription created            │
│ 4. Component unmounts → cleanup runs → subscription removed│
└─────────────────────────────────────────────────────────────┘
```

### Common Patterns

```
Common useEffect Patterns:
═══════════════════════════════════════════════════════════════

Pattern 1: Data Fetching
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   let cancelled = false;                                    │
│                                                             │
│   const fetchData = async () => {                           │
│     const response = await fetch(url);                      │
│     const data = await response.json();                     │
│     if (!cancelled) setData(data);                          │
│   };                                                        │
│                                                             │
│   fetchData();                                              │
│   return () => { cancelled = true; };                       │
│ }, [url]);                                                  │
└─────────────────────────────────────────────────────────────┘

Pattern 2: Event Listeners
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   const handler = (e: Event) => { /* ... */ };              │
│   window.addEventListener('resize', handler);               │
│   return () => window.removeEventListener('resize', handler);│
│ }, []);                                                     │
└─────────────────────────────────────────────────────────────┘

Pattern 3: Timers
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   const id = setInterval(callback, delay);                  │
│   return () => clearInterval(id);                           │
│ }, [callback, delay]);                                      │
└─────────────────────────────────────────────────────────────┘

Pattern 4: DOM Manipulation
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   const element = ref.current;                              │
│   element.focus();                                          │
│   // No cleanup needed for focus                            │
│ }, []);                                                     │
└─────────────────────────────────────────────────────────────┘

Pattern 5: External Store Subscription
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   const unsubscribe = store.subscribe(handleChange);        │
│   return unsubscribe;                                       │
│ }, [store]);                                                │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Data Fetching

```typescript
import React, { useState, useEffect } from 'react';

const UserProfile = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchUser = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error('Failed to fetch');
        const data = await response.json();

        if (!cancelled) {
          setUser(data);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      }
    };

    fetchUser();

    return () => {
      cancelled = true; // Prevent state update on unmounted component
    };
  }, [userId]); // Re-fetch when userId changes

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return null;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
};
```

### Event Listener

```typescript
const useWindowSize = () => {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
};

const ResponsiveComponent = () => {
  const { width, height } = useWindowSize();

  return (
    <div>
      <p>Width: {width}px, Height: {height}px</p>
      {width > 768 ? <DesktopView /> : <MobileView />}
    </div>
  );
};
```

### Timer with Cleanup

```typescript
const useInterval = (callback: () => void, delay: number | null) => {
  const savedCallback = useRef(callback);

  // Remember the latest callback
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval
  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
};

// Usage
const Clock = () => {
  const [time, setTime] = useState(new Date());

  useInterval(() => {
    setTime(new Date());
  }, 1000);

  return <div>{time.toLocaleTimeString()}</div>;
};
```

### Document Title Sync

```typescript
const useDocumentTitle = (title: string) => {
  useEffect(() => {
    const prevTitle = document.title;
    document.title = title;

    return () => {
      document.title = prevTitle;
    };
  }, [title]);
};

const Dashboard = () => {
  useDocumentTitle('Dashboard - MyApp');
  return <div>Dashboard</div>;
};
```

### Intersection Observer

```typescript
const useIntersectionObserver = (
  ref: React.RefObject<HTMLElement>,
  options?: IntersectionObserverInit
) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsVisible(entry.isIntersecting);
    }, options);

    observer.observe(element);

    return () => observer.disconnect();
  }, [ref, options]);

  return isVisible;
};

// Usage
const LazyImage = ({ src, alt }: { src: string; alt: string }) => {
  const ref = useRef<HTMLDivElement>(null);
  const isVisible = useIntersectionObserver(ref, { threshold: 0.1 });

  return (
    <div ref={ref}>
      {isVisible ? <img src={src} alt={alt} /> : <div className="placeholder" />}
    </div>
  );
};
```

### Fetch with Abort Controller

```typescript
const useFetch = <T>(url: string) => {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(url, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err as Error);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    return () => controller.abort();
  }, [url]);

  return { data, error, loading };
};

// Usage
const UserList = () => {
  const { data: users, error, loading } = useFetch<User[]>('/api/users');

  if (loading) return <Spinner />;
  if (error) return <div>Error: {error.message}</div>;
  return <ul>{users?.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
};
```

## Real-World Use Cases

### 1. Real-Time Search with Debouncing

```typescript
const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};

const SearchInput = () => {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery).then(results => setResults(results));
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={e => setQuery(e.target.value)} />;
};
```

### 2. WebSocket Connection

```typescript
const useWebSocket = (url: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = (message: any) => {
    // Implementation
  };

  return { messages, isConnected, sendMessage };
};
```

### 3. localStorage Sync

```typescript
const useLocalStorage = <T>(key: string, initialValue: T) => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue] as const;
};

// Usage
const ThemeToggle = () => {
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current: {theme}
    </button>
  );
};
```

### 4. Geolocation

```typescript
const useGeolocation = () => {
  const [location, setLocation] = useState<GeolocationPosition | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('Geolocation not supported');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      position => setLocation(position),
      err => setError(err.message)
    );
  }, []);

  return { location, error };
};
```

## Common Mistakes

### 1. Missing Dependencies

```typescript
// ❌ BAD: Missing dependency
const SearchComponent = ({ query }: { query: string }) => {
  useEffect(() => {
    fetchResults(query); // query not in deps!
  }, []); // Will always use initial query value
};

// ✅ GOOD: Correct dependencies
const SearchComponent = ({ query }: { query: string }) => {
  useEffect(() => {
    fetchResults(query);
  }, [query]); // Re-runs when query changes
};
```

### 2. Missing Cleanup

```typescript
// ❌ BAD: No cleanup - memory leak
const TimerComponent = () => {
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('tick');
    }, 1000);
    // No cleanup! Interval continues after unmount
  }, []);
};

// ✅ GOOD: Proper cleanup
const TimerComponent = () => {
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('tick');
    }, 1000);
    return () => clearInterval(interval); // Cleanup
  }, []);
};
```

### 3. Using useEffect for Derived State

```typescript
// ❌ BAD: useEffect for derived state
const FilteredList = ({ items, query }: Props) => {
  const [filtered, setFiltered] = useState<string[]>([]);

  useEffect(() => {
    setFiltered(items.filter(item => item.includes(query)));
  }, [items, query]); // Runs after render, causes second render

  return <List items={filtered} />;
};

// ✅ GOOD: Compute during render
const FilteredList = ({ items, query }: Props) => {
  const filtered = useMemo(
    () => items.filter(item => item.includes(query)),
    [items, query]
  );

  return <List items={filtered} />;
};
```

### 4. Async Functions in useEffect

```typescript
// ❌ BAD: Async function directly in useEffect
useEffect(async () => {
  const data = await fetchData();
  setData(data);
}, []); // React expects no return value or a cleanup function

// ✅ GOOD: Inner async function
useEffect(() => {
  const fetchDataAsync = async () => {
    const data = await fetchData();
    setData(data);
  };
  fetchDataAsync();
}, []);

// ✅ GOOD: Using .then()
useEffect(() => {
  fetchData().then(data => setData(data));
}, []);
```

### 5. Not Using Abort Controller

```typescript
// ❌ BAD: Race condition
useEffect(() => {
  fetch(`/api/users/${userId}`)
    .then(res => res.json())
    .then(data => setUser(data));
  // If userId changes quickly, old responses may overwrite new ones
}, [userId]);

// ✅ GOOD: Abort controller
useEffect(() => {
  const controller = new AbortController();

  fetch(`/api/users/${userId}`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => setUser(data))
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort();
}, [userId]);
```

## Best Practices

1. **Always include dependencies**: Every external value used inside the effect should be in the dependency array.
2. **Always return cleanup functions**: For subscriptions, timers, event listeners, and fetch requests.
3. **Use AbortController for fetch**: Prevent race conditions and memory leaks.
4. **Don't use useEffect for derived state**: Compute during render instead.
5. **Split effects by concern**: One effect per side effect.
6. **Use `useLayoutEffect` for DOM measurements**: When you need to measure before paint.
7. **Avoid async functions directly**: Use inner async function or `.then()`.

## Performance Considerations

### useEffect Timing

| Type | Timing | Use Case |
|------|--------|----------|
| `useEffect(() => {})` | After paint (async) | Side effects |
| `useEffect(() => {}, [])` | After first paint | Mount setup |
| `useEffect(() => {}, [deps])` | After deps change | Conditional effects |
| `useLayoutEffect(() => {})` | After DOM mutation (sync) | DOM measurements |

### Effect Frequency

| Dependency Array | When It Runs | Use Case |
|-----------------|--------------|----------|
| No array | Every render | Rarely used |
| `[]` | Once on mount | Initial setup |
| `[dep1, dep2]` | When deps change | Conditional effects |

## Interview Questions

### Beginner (5-10)

**Q1: What is useEffect?**
A: `useEffect` is a React Hook that lets you perform side effects after rendering. It runs after the browser paints the screen. It's used for data fetching, subscriptions, event listeners, and DOM manipulation.

**Q2: What is the dependency array?**
A: The dependency array is the second argument to `useEffect`. It tells React when to re-run the effect. If any dependency changes, the effect runs again. If the array is empty, the effect runs only once.

**Q3: What is the cleanup function?**
A: The cleanup function is returned from `useEffect`. It runs before the effect re-runs (when deps change) and when the component unmounts. It's used to cancel subscriptions, clear timers, and remove event listeners.

**Q4: When does useEffect run?**
A: `useEffect` runs after the browser paints the screen (asynchronous). This means it doesn't block rendering.

**Q5: What is the difference between useEffect and useLayoutEffect?**
A: `useLayoutEffect` runs after DOM mutation but before paint (synchronous). `useEffect` runs after paint (asynchronous). Use `useLayoutEffect` for DOM measurements, `useEffect` for everything else.

**Q6: How do you fetch data in useEffect?**
A: Use `useEffect` with an async function or `.then()`:
```typescript
useEffect(() => {
  fetch(url).then(res => res.json()).then(data => setData(data));
}, [url]);
```

**Q7: What happens if you don't provide a dependency array?**
A: If you don't provide a dependency array, the effect runs after every render.

**Q8: What happens if you provide an empty dependency array?**
A: If you provide an empty array `[]`, the effect runs only once, after the first render (mount).

**Q9: Can you use async functions in useEffect?**
A: Not directly. Use an inner async function or `.then()`:
```typescript
useEffect(() => {
  const fetchData = async () => { /* ... */ };
  fetchData();
}, []);
```

**Q10: What is the cleanup function used for?**
A: The cleanup function is used to:
- Cancel subscriptions
- Clear timers
- Remove event listeners
- Cancel fetch requests
- Any other cleanup needed before unmount or re-run

### Intermediate (5-10)

**Q11: Explain the complete useEffect lifecycle.**
A:
1. Component renders
2. DOM is updated
3. Browser paints
4. `useEffect` callback runs (async)
5. If deps change:
   - Previous cleanup function runs
   - New effect runs
6. On unmount:
   - Cleanup function runs

**Q12: How do you handle race conditions in useEffect?**
A: Use `AbortController` to cancel previous requests:
```typescript
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then(res => res.json())
    .then(setData);
  return () => controller.abort();
}, [url]);
```

**Q13: What is the "stale closure" problem in useEffect?**
A: Stale closures occur when useEffect captures stale values. Solution: include all used values in the dependency array, or use refs.

**Q14: How do you avoid infinite loops?**
A: Don't set state inside useEffect without proper dependencies. If you must set state based on other state, do it during render:
```typescript
if (condition && state !== expectedValue) {
  setState(expectedValue);
}
```

**Q15: What is the difference between useEffect and useLayoutEffect?**
A: `useLayoutEffect` runs synchronously after DOM mutation, before paint. `useEffect` runs asynchronously after paint. Use `useLayoutEffect` for DOM measurements.

**Q16: How do you fetch data when a prop changes?**
A: Include the prop in the dependency array:
```typescript
useEffect(() => {
  fetch(`/api/users/${userId}`).then(res => res.json()).then(setUser);
}, [userId]); // Re-fetch when userId changes
```

**Q17: How do you subscribe to events in useEffect?**
A:
```typescript
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

**Q18: What is the performance impact of useEffect?**
A: `useEffect` runs after paint, so it doesn't block rendering. However, too many effects or effects with wrong dependencies can cause unnecessary re-renders.

**Q19: How do you test useEffect?**
A: Use React Testing Library's `act` to handle async operations:
```typescript
test('fetches data', async () => {
  render(<Component />);
  await waitFor(() => {
    expect(screen.getByText('Data')).toBeInTheDocument();
  });
});
```

**Q20: What are the common useEffect patterns?**
A:
- Data fetching with cleanup
- Event listener setup/teardown
- Timer management
- Document title sync
- localStorage sync
- External store subscriptions

### Senior (10-15)

**Q21: Explain the timing of useEffect relative to browser painting.**
A: `useEffect` runs after the browser paints. This means:
1. React commits DOM changes
2. Browser calculates layout
3. Browser paints pixels
4. `useEffect` runs (async)
This is ideal for side effects that don't need to block paint.

**Q22: How does useEffect handle concurrent rendering?**
A: During concurrent rendering, React can pause rendering. Effects are batched and applied after commit. `useEffect` can be deferred to idle time. Cleanup functions still run before new effects.

**Q23: What is the relationship between useEffect and React Suspense?**
A: Suspense can suspend rendering during the render phase. When a component suspends, React pauses and shows the fallback. Effects run after the component resumes and commits.

**Q24: How do you handle multiple async operations in useEffect?**
A: Use `AbortController` and track which operation is current:
```typescript
useEffect(() => {
  let cancelled = false;
  fetch(url).then(data => {
    if (!cancelled) setData(data);
  });
  return () => { cancelled = true; };
}, [url]);
```

**Q25: What is the difference between useEffect and useMemo?**
A: `useMemo` memoizes a computed value during render. `useEffect` performs side effects after render. `useMemo` is synchronous; `useEffect` is asynchronous.

**Q26: How do you handle errors in useEffect?**
A: Use try/catch in async functions:
```typescript
useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await fetch(url);
      setData(data);
    } catch (err) {
      setError(err.message);
    }
  };
  fetchData();
}, [url]);
```

**Q27: What is the "zombie children" problem?**
A: When a component updates state after unmounting (often in async operations). Prevention: use `AbortController`, check if component is still mounted, use cleanup functions.

**Q28: How does useEffect interact with React.memo?**
A: `React.memo` prevents re-renders when props haven't changed. This means `useEffect` won't run if the component doesn't re-render (because props didn't change).

**Q29: What is the performance impact of wrong dependencies?**
A: Wrong dependencies cause:
- Missing dependencies: Stale values, bugs
- Extra dependencies: Unnecessary effect runs
- Both impact performance and correctness

**Q30: How do you handle cleanup for complex subscriptions?**
A: Use a cleanup registry:
```typescript
useEffect(() => {
  const cleanups: (() => void)[] = [];
  cleanups.push(subscribeToChannel1());
  cleanups.push(subscribeToChannel2());
  return () => cleanups.forEach(cleanup => cleanup());
}, []);
```

### FAANG-style (5-10)

**Q31: Design a data fetching layer using useEffect.**
A:
1. **Custom hook**: Encapsulate fetch logic
2. **Cache**: Store fetched data
3. **Deduplication**: Avoid duplicate requests
4. **Retry**: Automatic retry on failure
5. **Abort**: Cancel stale requests
6. **Optimistic updates**: Show data immediately

```typescript
const useFetch = <T>(url: string) => {
  const [state, dispatch] = useReducer(fetchReducer, {
    data: null,
    error: null,
    loading: true,
  });

  useEffect(() => {
    const controller = new AbortController();
    dispatch({ type: 'FETCH_START' });

    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(data => dispatch({ type: 'FETCH_SUCCESS', payload: data }))
      .catch(err => {
        if (err.name !== 'AbortError') {
          dispatch({ type: 'FETCH_ERROR', payload: err.message });
        }
      });

    return () => controller.abort();
  }, [url]);

  return state;
};
```

**Q32: How would you implement a custom useEffect with different timing?**
A:
```typescript
const useInterval = (callback: () => void, delay: number) => {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    const tick = () => savedCallback.current();
    const id = setInterval(tick, delay);
    return () => clearInterval(id);
  }, [delay]);
};
```

**Q33: Analyze the memory implications of useEffect.**
A:
- Each effect stores a closure (references to outer variables)
- Cleanup functions prevent memory leaks
- Missing cleanup causes memory leaks (subscriptions, timers)
- `AbortController` prevents fetch-related memory leaks

**Q34: How would you debug a useEffect issue?**
A:
1. **React DevTools**: Check component re-renders
2. **Console logging**: Log effect execution and cleanup
3. **Network tab**: Monitor fetch requests
4. **Memory tab**: Detect memory leaks
5. **React StrictMode**: Double-renders to detect issues

**Q35: Design a useEffect-based state machine.**
A:
```typescript
const useStateMachine = <T>(initialState: T, transitions: Record<string, (state: T) => T>) => {
  const [state, setState] = useState(initialState);

  const transition = (action: string) => {
    setState(prev => transitions[action](prev));
  };

  return [state, transition];
};
```

**Q36: How does useEffect interact with React Server Components?**
A: Server Components don't have `useEffect`. Client Components hydrate with normal `useEffect` behavior. Server effects don't run on client.

**Q37: Analyze the performance characteristics of useEffect.**
A: `useEffect` runs asynchronously, so it doesn't block rendering. However:
- Too many effects cause unnecessary work
- Wrong dependencies cause re-runs
- Cleanup functions add overhead
- Async operations cause state updates

**Q38: How would you implement a useEffect-based animation?**
A:
```typescript
const useAnimation = (ref: React.RefObject<HTMLElement>, deps: any[]) => {
  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const animation = element.animate([
      { transform: 'scale(1)' },
      { transform: 'scale(1.1)' },
    ], {
      duration: 300,
      easing: 'ease-in-out',
    });

    return () => animation.cancel();
  }, deps);
};
```

**Q39: How does useEffect handle the "state update after unmount" problem?**
A: React 18 warns about state updates after unmount. Prevention:
- Use `AbortController` for fetch
- Check if component is still mounted
- Use cleanup functions
- Use `useEffect` cleanup

**Q40: Design a useEffect-based testing utility.**
A:
```typescript
const renderWithEffects = async (component: React.ReactElement) => {
  const result = render(component);
  await act(async () => {
    // Wait for all effects to complete
  });
  return result;
};
```

### Follow-ups (5-10)

**Q41: How would you explain useEffect to a junior developer?**
A: "`useEffect` is like a postcard you send after painting a picture. React paints the screen first, then runs your effect. If you need to clean up (like canceling a subscription), you return a cleanup function."

**Q42: What are the edge cases in useEffect?**
A:
- Stale closures in async callbacks
- Race conditions with multiple fetches
- Missing dependencies causing bugs
- Cleanup functions not running
- Effect running after unmount

**Q43: How does useEffect handle the "derived state" pattern?**
A: Don't use `useEffect` for derived state. Compute during render:
```typescript
const filtered = useMemo(() => items.filter(...), [items, query]);
```

**Q44: What is the relationship between useEffect and React DevTools?**
A: React DevTools shows:
- Which effects are running
- When effects run
- Effect dependencies
- Cleanup functions

**Q45: How does useEffect interact with React StrictMode?**
A: StrictMode double-renders in development, causing effects to run twice. This helps detect missing cleanup functions and impure effects.

**Q46: What is the future of useEffect in React?**
A: React is exploring:
- Better concurrent effect handling
- Automatic cleanup detection
- Improved dependency arrays
- Better error handling

**Q47: How would you implement a useEffect-based form validator?**
A:
```typescript
const useFormValidation = <T>(values: T, rules: Record<string, (value: any) => string | null>) => {
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    const newErrors: Record<string, string> = {};
    Object.entries(rules).forEach(([field, validate]) => {
      const error = validate(values[field]);
      if (error) newErrors[field] = error;
    });
    setErrors(newErrors);
  }, [values, rules]);

  return errors;
};
```

**Q48: How does useEffect handle the "multiple async operations" problem?**
A: Use `AbortController` and track which operation is current:
```typescript
useEffect(() => {
  let cancelled = false;
  const fetchData = async () => {
    const data = await fetch(url);
    if (!cancelled) setData(data);
  };
  fetchData();
  return () => { cancelled = true; };
}, [url]);
```

**Q49: What is the relationship between useEffect and React Suspense?**
A: Suspense can suspend rendering during the render phase. When a component suspends, React pauses and shows the fallback. Effects run after the component resumes and commits.

**Q50: How would you implement a useEffect-based real-time data sync?**
A:
```typescript
const useRealtimeSync = <T>(url: string) => {
  const [data, setData] = useState<T | null>(null);

  useEffect(() => {
    const eventSource = new EventSource(url);
    eventSource.onmessage = (event) => {
      setData(JSON.parse(event.data));
    };
    return () => eventSource.close();
  }, [url]);

  return data;
};
```

## Summary

`useEffect` is the primary hook for performing side effects in React function components. It runs after the browser paints, making it ideal for data fetching, subscriptions, and DOM manipulation. Proper use of dependency arrays and cleanup functions is essential for correctness and performance.

## Cheat Sheet

```
useEffect Key Points:
├── What: Hook for side effects after render
├── Timing: After browser paint (async)
├── Dependencies: Controls when effect runs
├── Cleanup: Return function to clean up
├── Cleanup runs: Before re-run and on unmount

Dependency Array:
├── No array: Runs every render
├── []: Runs once on mount
├── [deps]: Runs when deps change
└── Always include all used values

Cleanup Function:
├── Runs before effect re-runs
├── Runs on component unmount
├── Used for: subscriptions, timers, fetch, events
└── Always return cleanup for side effects

Common Patterns:
├── Data fetching with AbortController
├── Event listener setup/teardown
├── Timer management (setInterval)
├── Document title sync
├── localStorage sync
├── External store subscriptions
└── WebSocket connections

Common Mistakes:
├── Missing dependencies (stale values)
├── Missing cleanup (memory leaks)
├── Using useEffect for derived state
├── Async functions directly in useEffect
├── Not using AbortController for fetch
└── Infinite loops (setting state without deps)

Best Practices:
├── Always include dependencies
├── Always return cleanup functions
├── Use AbortController for fetch
├── Don't use useEffect for derived state
├── Split effects by concern
├── Use useLayoutEffect for DOM measurements
└── Handle async operations properly

Performance:
├── useEffect runs asynchronously (doesn't block paint)
├── Wrong dependencies cause unnecessary re-runs
├── Cleanup prevents memory leaks
├── Too many effects cause performance issues
└── Use React.memo to prevent unnecessary re-renders
```

## References & Learn More

- [React Docs: useEffect](https://react.dev/reference/react/useEffect)
- [A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/)
- [React useEffect: Complete Guide](https://www.freecodecamp.org/news/useeffect-hook-explained/)
