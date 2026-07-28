[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

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

```text
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

```text
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

```text
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

```text
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

## Summary

`useEffect` is the primary hook for performing side effects in React function components. It runs after the browser paints, making it ideal for data fetching, subscriptions, and DOM manipulation. Proper use of dependency arrays and cleanup functions is essential for correctness and performance.

## Cheat Sheet
```text
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

---

## See Also
- [Animation](../30-Animation/)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: useEffect](https://react.dev/reference/react/useEffect)
- [A Complete Guide to useEffect](https://overreacted.io/a-complete-guide-to-useeffect/)
- [React useEffect: Complete Guide](https://www.freecodecamp.org/news/useeffect-hook-in-react/)
