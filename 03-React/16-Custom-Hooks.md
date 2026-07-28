# Custom Hooks

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

c across React components. They start with `use` by convention, call other React Hooks inside them, and return a value, an array, or an object. Custom Hooks let you extract component logic into reusable functions — enabling composition, separation of concerns, and sharing of stateful behavior without higher-order components or render props.

## Why Do We Need It?

1. **Reusability** — Extract and share stateful logic between components without duplication
2. **Separation of concerns** — Keep components focused on UI, move logic to hooks
3. **Composability** — Combine multiple hooks to build complex behaviors
4. **Testability** — Isolate and test logic independently of component rendering
5. **Cleaner components** — Reduce boilerplate and improve readability

## How It Works

### Custom Hook Convention

```text
Custom Hook Structure:
═══════════════════════════════════════════════════════════════

1. Convention: function must start with "use"
2. Can call other React Hooks (useState, useEffect, etc.)
3. Accepts parameters (optional)
4. Returns values (object, array, or single value)
5. State is isolated per component instance

┌─────────────────────────────────────────────────────────────┐
│ Component A              Component B                         │
│  ├── useCounter()        ├── useCounter()                    │
│  │   ├── count = 0       │   ├── count = 0                  │
│  │   └── increment()     │   └── increment()                 │
│  │                       │                                   │
│  └── Each hook instance  └── Each hook instance              │
│      has ISOLATED state      has ISOLATED state              │
└─────────────────────────────────────────────────────────────┘

Rules:
├── Only call hooks at top level (not inside loops/conditions)
├── Only call hooks from React functions (components or hooks)
└── Hook names must start with "use" (enforced by ESLint)

```

### Data Flow

```text
Custom Hook Data Flow:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│                    Custom Hook Pattern                        │
│                                                              │
│  Component                                                   │
│  ┌───────────────────────────────────────────────┐          │
│  │                                                   │          │
│  │   const { data, loading, error } = useFetch(     │          │
│  │     '/api/users'                                 │          │
│  │   );                                             │          │
│  │                                                   │          │
│  │   if (loading) return <Spinner />                │          │
│  │   if (error) return <Error />                    │          │
│  │   return <List data={data} />                    │          │
│  │                                                   │          │
│  └───────────────────────────────────────────────┘          │
│            │                                                 │
│            ▼                                                 │
│  Custom Hook                                                  │
│  ┌───────────────────────────────────────────────┐          │
│  │   function useFetch(url) {                     │          │
│  │     const [data, setData] = useState(null);   │          │
│  │     const [loading, setLoading] = useState(true);         │
│  │     const [error, setError] = useState(null); │          │
│  │                                                   │          │
│  │     useEffect(() => {                            │          │
│  │       fetch(url)                                 │          │
│  │         .then(r => r.json())                    │          │
│  │         .then(setData)                           │          │
│  │         .catch(setError)                         │          │
│  │         .finally(() => setLoading(false))        │          │
│  │     }, [url]);                                   │          │
│  │                                                   │          │
│  │     return { data, loading, error };             │          │
│  │   }                                               │          │
│  └───────────────────────────────────────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. useCounter

```typescript
import { useState, useCallback } from 'react';

interface UseCounterProps {
  initialValue?: number;
  min?: number;
  max?: number;
  step?: number;
}

interface UseCounterReturn {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
  setCount: (value: number) => void;
}

function useCounter({
  initialValue = 0,
  min = -Infinity,
  max = Infinity,
  step = 1,
}: UseCounterProps = {}): UseCounterReturn {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount(prev => Math.min(prev + step, max));
  }, [step, max]);

  const decrement = useCallback(() => {
    setCount(prev => Math.max(prev - step, min));
  }, [step, min]);

  const reset = useCallback(() => {
    setCount(initialValue);
  }, [initialValue]);

  return { count, increment, decrement, reset, setCount };
}

// Usage
const CounterComponent = () => {
  const { count, increment, decrement, reset } = useCounter({
    initialValue: 10,
    min: 0,
    max: 100,
  });

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={decrement}>-</button>
      <button onClick={increment}>+</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
};
```

### 2. useLocalStorage

```typescript
import { useState, useCallback } from 'react';

function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  // Initialize state with stored value or default
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Update localStorage whenever state changes
  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      try {
        setStoredValue(prev => {
          const valueToStore = value instanceof Function ? value(prev) : value;
          window.localStorage.setItem(key, JSON.stringify(valueToStore));
          return valueToStore;
        });
      } catch (error) {
        console.error(`Error setting localStorage key "${key}":`, error);
      }
    },
    [key]
  );

  const remove = useCallback(() => {
    try {
      window.localStorage.removeItem(key);
      setStoredValue(initialValue);
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error);
    }
  }, [key, initialValue]);

  return [storedValue, setValue, remove];
}

// Usage
const ThemeToggle = () => {
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');

  return (
    <button onClick={() => setTheme(prev =>
      prev === 'light' ? 'dark' : 'light'
    )}>
      Current: {theme}
    </button>
  );
};
```

### 3. useDebounce

```typescript
import { useState, useEffect } from 'react';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const SearchInput = () => {
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);

  useEffect(() => {
    if (debouncedSearch) {
      api.search(debouncedSearch);
    }
  }, [debouncedSearch]);

  return (
    <input
      value={search}
      onChange={e => setSearch(e.target.value)}
      placeholder="Search..."
    />
  );
};
```

### 4. useMediaQuery

```typescript
import { useState, useEffect } from 'react';

function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => {
    if (typeof window !== 'undefined') {
      return window.matchMedia(query).matches;
    }
    return false;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);

    const handleChange = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [query]);

  return matches;
}

// Usage
const ResponsiveComponent = () => {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const isTablet = useMediaQuery('(min-width: 769px) and (max-width: 1024px)');
  const isDesktop = useMediaQuery('(min-width: 1025px)');

  return (
    <div>
      {isMobile && <MobileLayout />}
      {isTablet && <TabletLayout />}
      {isDesktop && <DesktopLayout />}
    </div>
  );
};
```

### 5. useToggle

```typescript
import { useState, useCallback } from 'react';

function useToggle(
  initialValue: boolean = false
): [boolean, () => void, () => void, () => void] {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue(prev => !prev), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return [value, toggle, setTrue, setFalse];
}

// Usage
const Accordion = () => {
  const [isOpen, toggle, open, close] = useToggle();

  return (
    <div>
      <button onClick={toggle}>
        {isOpen ? 'Hide' : 'Show'} Details
      </button>
      {isOpen && <div className="content">Details content...</div>}
    </div>
  );
};
```

### 6. useFetch

```typescript
import { useState, useEffect, useRef } from 'react';

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

function useFetch<T = unknown>(
  url: string,
  options?: RequestInit
): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Store options ref to prevent infinite effects
  const optionsRef = useRef(options);
  optionsRef.current = options;

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url, optionsRef.current);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = (await response.json()) as T;
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Fetch failed'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
```

### 7. useIntersectionObserver

```typescript
import { useState, useEffect, useRef, RefObject } from 'react';

interface UseIntersectionObserverOptions {
  threshold?: number;
  root?: Element | null;
  rootMargin?: string;
  enabled?: boolean;
}

function useIntersectionObserver<T extends HTMLElement = HTMLDivElement>(
  options: UseIntersectionObserverOptions = {}
): { ref: RefObject<T | null>; isIntersecting: boolean; entry: IntersectionObserverEntry | null } {
  const ref = useRef<T | null>(null);
  const [isIntersecting, setIsIntersecting] = useState(false);
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);

  const { threshold = 0, root = null, rootMargin = '0px', enabled = true } = options;

  useEffect(() => {
    if (!enabled || !ref.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsIntersecting(entry.isIntersecting);
        setEntry(entry);
      },
      { threshold, root, rootMargin }
    );

    observer.observe(ref.current);

    return () => observer.disconnect();
  }, [threshold, root, rootMargin, enabled]);

  return { ref, isIntersecting, entry };
}

// Usage — Infinite scroll + lazy loading
const LazyImage = ({ src, alt }: { src: string; alt: string }) => {
  const { ref, isIntersecting } = useIntersectionObserver({
    threshold: 0.1,
    rootMargin: '100px',
  });

  return (
    <div ref={ref} style={{ minHeight: 200 }}>
      {isIntersecting ? (
        <img src={src} alt={alt} loading="lazy" />
      ) : (
        <div className="skeleton">Loading...</div>
      )}
    </div>
  );
};
```

### 8. useEventListener

```typescript
import { useEffect, useRef, RefObject } from 'react';

function useEventListener<K extends keyof WindowEventMap>(
  eventName: K,
  handler: (event: WindowEventMap[K]) => void,
  element?: Window | HTMLElement | RefObject<HTMLElement | null>,
  options?: boolean | AddEventListenerOptions
): void;

function useEventListener<
  K extends keyof HTMLElementEventMap,
  T extends HTMLElement = HTMLDivElement
>(
  eventName: K,
  handler: (event: HTMLElementEventMap[K]) => void,
  element: RefObject<T | null>,
  options?: boolean | AddEventListenerOptions
): void;

function useEventListener(
  eventName: string,
  handler: EventListener,
  element?: Window | HTMLElement | RefObject<HTMLElement | null>,
  options?: boolean | AddEventListenerOptions
): void {
  const savedHandler = useRef(handler);

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    const targetElement: Window | HTMLElement | null =
      element && 'current' in element
        ? element.current
        : (element as HTMLElement) ?? window;

    if (!targetElement?.addEventListener) return;

    const eventListener = (event: Event) => savedHandler.current(event);
    targetElement.addEventListener(eventName, eventListener, options);

    return () => {
      targetElement.removeEventListener(eventName, eventListener, options);
    };
  }, [eventName, element, options]);
}

// Usage
const DocumentClick = () => {
  const [clickCount, setClickCount] = useState(0);

  useEventListener('click', () => {
    setClickCount(prev => prev + 1);
  });

  return <p>Document clicked {clickCount} times</p>;
};
```

### 9. useForm

```typescript
import { useState, useCallback, useMemo } from 'react';

interface UseFormProps<T extends Record<string, any>> {
  initialValues: T;
  validate?: (values: T) => Partial<Record<keyof T, string>>;
  onSubmit: (values: T) => void | Promise<void>;
}

interface UseFormReturn<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
  dirty: boolean;
  isSubmitting: boolean;
  handleChange: (field: keyof T) => (event: React.ChangeEvent<HTMLInputElement>) => void;
  handleBlur: (field: keyof T) => () => void;
  handleSubmit: (event: React.FormEvent) => void;
  setFieldValue: (field: keyof T, value: any) => void;
  resetForm: () => void;
}

function useForm<T extends Record<string, any>>({
  initialValues,
  validate,
  onSubmit,
}: UseFormProps<T>): UseFormReturn<T> {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const dirty = useMemo(
    () => JSON.stringify(values) !== JSON.stringify(initialValues),
    [values, initialValues]
  );

  const validateForm = useCallback(
    (currentValues: T) => {
      if (validate) {
        const validationErrors = validate(currentValues);
        setErrors(validationErrors);
        return Object.keys(validationErrors).length === 0;
      }
      return true;
    },
    [validate]
  );

  const handleChange = useCallback(
    (field: keyof T) => (event: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = event.target.type === 'checkbox'
        ? event.target.checked
        : event.target.value;

      setValues(prev => ({ ...prev, [field]: newValue }));

      // Validate on change if field has been touched
      if (touched[field] && validate) {
        const newValues = { ...values, [field]: newValue };
        const validationErrors = validate(newValues);
        setErrors(prev => ({
          ...prev,
          [field]: validationErrors[field] || undefined,
        }));
      }
    },
    [values, touched, validate]
  );

  const handleBlur = useCallback(
    (field: keyof T) => () => {
      setTouched(prev => ({ ...prev, [field]: true }));
      if (validate) {
        const validationErrors = validate(values);
        setErrors(prev => ({
          ...prev,
          [field]: validationErrors[field] || undefined,
        }));
      }
    },
    [values, validate]
  );

  const handleSubmit = useCallback(
    async (event: React.FormEvent) => {
      event.preventDefault();

      // Mark all fields as touched
      const allTouched = Object.keys(values).reduce(
        (acc, key) => ({ ...acc, [key]: true }),
        {} as Partial<Record<keyof T, boolean>>
      );
      setTouched(allTouched);

      if (!validateForm(values)) return;

      setIsSubmitting(true);
      try {
        await onSubmit(values);
      } finally {
        setIsSubmitting(false);
      }
    },
    [values, onSubmit, validateForm]
  );

  const setFieldValue = useCallback((field: keyof T, value: any) => {
    setValues(prev => ({ ...prev, [field]: value }));
  }, []);

  const resetForm = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    dirty,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    setFieldValue,
    resetForm,
  };
}

// Usage
const LoginForm = () => {
  const {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
  } = useForm({
    initialValues: { email: '', password: '' },
    validate: (values) => {
      const errors: Record<string, string> = {};
      if (!values.email) errors.email = 'Required';
      if (!values.password) errors.password = 'Required';
      return errors;
    },
    onSubmit: async (values) => {
      await api.login(values);
    },
  });

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="email"
        value={values.email}
        onChange={handleChange('email')}
        onBlur={handleBlur('email')}
      />
      {touched.email && errors.email && <span>{errors.email}</span>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};
```

### 10. useAsync

```typescript
import { useState, useCallback, useRef } from 'react';

type AsyncState<T> = {
  data: T | null;
  loading: boolean;
  error: Error | null;
};

type UseAsyncReturn<T, Args extends unknown[]> = AsyncState<T> & {
  execute: (...args: Args) => Promise<T | undefined>;
  reset: () => void;
};

function useAsync<T, Args extends unknown[] = unknown[]>(
  asyncFunction: (...args: Args) => Promise<T>,
  immediate: boolean = false
): UseAsyncReturn<T, Args> {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const isMounted = useRef(true);

  const execute = useCallback(
    async (...args: Args): Promise<T | undefined> => {
      setState(prev => ({ ...prev, loading: true, error: null }));

      try {
        const result = await asyncFunction(...args);

        if (isMounted.current) {
          setState({ data: result, loading: false, error: null });
        }

        return result;
      } catch (error) {
        if (isMounted.current) {
          setState({
            data: null,
            loading: false,
            error: error instanceof Error ? error : new Error(String(error)),
          });
        }
        return undefined;
      }
    },
    [asyncFunction]
  );

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return { ...state, execute, reset };
}

// Usage
const UserProfile = ({ userId }: { userId: string }) => {
  const { data: user, loading, error, execute } = useAsync(
    () => fetchUser(userId),
    true // Execute immediately
  );

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <div>{user?.name}</div>;
};
```

## Real-World Use Cases

### 1. useAuth — Authentication Hook

```typescript
import { createContext, useContext, useState, useCallback, useEffect } from 'react';

interface AuthUser {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  error: string | null;
}

// Simple useAuth hook
function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    loading: true,
    error: null,
  });

  const login = useCallback(async (email: string, password: string) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const user = await api.login(email, password);
      setState({ user, loading: false, error: null });
    } catch (err) {
      setState({ user: null, loading: false, error: err.message });
    }
  }, []);

  const logout = useCallback(async () => {
    await api.logout();
    setState({ user: null, loading: false, error: null });
  }, []);

  useEffect(() => {
    api.getCurrentUser()
      .then(user => setState({ user, loading: false, error: null }))
      .catch(() => setState({ user: null, loading: false, error: null }));
  }, []);

  return { ...state, login, logout };
}
```

### 2. useWebSocket — Real-Time Connection

```typescript
import { useState, useEffect, useRef, useCallback } from 'react';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  reconnect?: boolean;
  reconnectInterval?: number;
  maxReconnects?: number;
}

function useWebSocket({
  url,
  onMessage,
  reconnect = true,
  reconnectInterval = 3000,
  maxReconnects = 5,
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectCount = useRef(0);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout>>();

  const connect = useCallback(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setIsConnected(true);
      reconnectCount.current = 0;
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage?.(data);
    };

    ws.onclose = () => {
      setIsConnected(false);
      if (reconnect && reconnectCount.current < maxReconnects) {
        reconnectTimer.current = setTimeout(() => {
          reconnectCount.current++;
          connect();
        }, reconnectInterval);
      }
    };

    ws.onerror = () => ws.close();
    wsRef.current = ws;
  }, [url, onMessage, reconnect, reconnectInterval, maxReconnects]);

  const send = useCallback((data: any) => {
    wsRef.current?.send(JSON.stringify(data));
  }, []);

  const disconnect = useCallback(() => {
    clearTimeout(reconnectTimer.current);
    wsRef.current?.close();
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return { isConnected, send, disconnect };
}
```

## Common Mistakes

### 1. Breaking the Rules of Hooks

```typescript
// ❌ BAD: Hook inside condition
function useBadHook(condition: boolean) {
  if (condition) {
    useState(0); // ❌ Conditional hook call
  }
}

// ❌ BAD: Hook inside loop
function useBadHook(items: any[]) {
  items.forEach(() => {
    useEffect(() => {}); // ❌ Hook inside loop
  });
}

// ✅ GOOD: Always at top level
function useGoodHook(condition: boolean) {
  const [value] = useState(0);

  useEffect(() => {
    if (condition) {
      // Logic inside effect is fine
    }
  }, [condition]);
}
```

### 2. Not Memoizing Return Values

```typescript
// ❌ BAD: New object on every render
function useUser(id: string) {
  const [user, setUser] = useState(null);

  useEffect(() => { fetchUser(id).then(setUser); }, [id]);

  return { user, id }; // New object every render!
}

// ✅ GOOD: Memoize return value
function useUser(id: string) {
  const [user, setUser] = useState(null);

  useEffect(() => { fetchUser(id).then(setUser); }, [id]);

  return useMemo(() => ({ user, id }), [user, id]);
}
```

### 3. Creating Stale Closures

```typescript
// ❌ BAD: Stale closure
function useInterval(callback: () => void, delay: number) {
  useEffect(() => {
    const id = setInterval(callback, delay); // Stale callback!
    return () => clearInterval(id);
  }, [delay]); // Missing callback dependency
}

// ✅ GOOD: Use ref for callback
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  });

  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}
```

### 4. Over-Abstracting

```typescript
// ❌ BAD: One-line custom hook adds no value
function useDouble(value: number) {
  return value * 2; // Just use `value * 2` inline!
}

// ✅ GOOD: Custom hook encapsulates real logic
function useDouble(value: number) {
  const [result, setResult] = useState(value * 2);

  useEffect(() => {
    setResult(value * 2);
  }, [value]);

  return result;
}
```

## Best Practices

1. **Start with `use`** — Convention enforced by React and ESLint

2. **Return a single object** — Named properties are easier to destructure

3. **Memoize return values** — Prevent unnecessary re-renders in consumers

4. **Accept arguments sparingly** — Use an options object for multiple params

5. **Clean up side effects** — Always return cleanup functions from `useEffect`

6. **Handle errors gracefully** — Return error state from async hooks

7. **Use refs for latest values** — Avoid stale closures with `useRef`

8. **Test in isolation** — Use `renderHook` from `@testing-library/react`

9. **Keep hooks focused** — Each hook should do one thing well

10. **Compose hooks** — Build complex hooks from simpler ones

## Performance Considerations

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| Over-memoization | Wasted render cycles | Only memoize when passed to context or memoized children |
| Stale closures | Buggy behavior | Use `useRef` for callbacks |
| State isolation | Clean per-instance state | No mitigation needed (it's by design) |
| Large return objects | Memory overhead | Return only what's needed |
| Frequent re-creation | Performance degradation | `useCallback` for returned functions |

## Testing Custom Hooks

```typescript
import { renderHook, act } from '@testing-library/react';

// Test useCounter
test('should increment counter', () => {
  const { result } = renderHook(() => useCounter({ initialValue: 0 }));

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});

// Test useDebounce
test('should debounce value changes', async () => {
  jest.useFakeTimers();

  const { result, rerender } = renderHook(
    ({ value }) => useDebounce(value, 500),
    { initialProps: { value: 'hello' } }
  );

  expect(result.current).toBe('hello');

  rerender({ value: 'world' });
  expect(result.current).toBe('hello'); // Not updated yet

  act(() => { jest.advanceTimersByTime(500); });
  expect(result.current).toBe('world'); // Updated after delay
});

// Test useLocalStorage
test('should persist value to localStorage', () => {
  const key = 'test-key';
  const { result } = renderHook(() => useLocalStorage(key, 'default'));

  act(() => {
    result.current[1]('updated');
  });

  expect(localStorage.getItem(key)).toBe('"updated"');
});
```

## Summary

Custom Hooks are the primary mechanism for reusing stateful logic in React. They follow the Hook rules (top-level only, React-only, `use` prefix) and can encapsulate any combination of built-in hooks. Well-designed custom hooks improve code organization, testability, and reusability across components.

## Cheat Sheet

```text
Custom Hooks Key Points:
├── Function name must start with "use"
├── Can call other hooks (useState, useEffect, etc.)
├── State is isolated per component instance
├── Return values: object, array, or single value
├── Compose hooks -> build complex from simple

Common Patterns:
├── useCounter: Increment/decrement/reset counter
├── useLocalStorage: Persist state to localStorage
├── useDebounce: Debounce rapidly changing values
├── useMediaQuery: Responsive breakpoint detection
├── useToggle: Boolean toggle with helpers
├── useFetch: Data fetching with loading/error states
├── useIntersectionObserver: Element visibility detection
├── useEventListener: Type-safe event binding
├── useForm: Form state management with validation
├── useAsync: Generic async operation wrapper

Rules (ESLint Plugin: react-hooks):
├── Only call hooks at the top level
├── Only call hooks from React functions
└── Hook names must start with "use"

Best Practices:
├── Memoize return values with useMemo
├── Use refs for callbacks to avoid stale closures
├── Return errors from async operations
├── Accept options objects for multiple params
├── Keep hooks focused (single responsibility)
├── Test with renderHook from testing-library
└── Don't over-abstract simple logic

Performance:
├── Use useCallback for returned functions
├── Use useMemo for returned objects/arrays
├── Clean up side effects in useEffect return
└── Only memoize when it provides benefit
```

---

## See Also
- [Compound Components](18-Compound-Components.md)
- [Form Handling (React Hook Form, Formik)](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Performance](13-Performance.md)
- [Testing](../16-Testing/)
- [useEffect](07-UseEffect.md)
- [useMemo / useCallback](08-UseMemo-UseCallback.md)
- [useRef](09-UseRef.md)
- [useState](06-UseState.md)

## References & Learn More

- [React Docs: Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)
- [React Docs: Built-in React Hooks](https://react.dev/reference/react)
- [React Hooks Rules](https://react.dev/reference/rules/rules-of-hooks)
- [Testing Library: renderHook](https://testing-library.com/docs/react-testing-library/api/#renderhook)
- [useHooks: Collection of Custom Hooks](https://usehooks.com/)
- [React Custom Hooks Patterns](https://www.robinwieruch.de/react-custom-hook/)
