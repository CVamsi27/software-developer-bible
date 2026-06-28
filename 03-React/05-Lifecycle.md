# Lifecycle

## Definition

The component lifecycle in React refers to the series of events that happen from the moment a component is created (mounted), through updates, to when it's destroyed (unmounted). In class components, lifecycle methods provide hooks into these phases. In function components, `useEffect` and `useLayoutEffect` serve as lifecycle replacements.

Understanding the lifecycle is crucial for managing side effects, subscriptions, DOM operations, and resource cleanup in React applications.

## Why Do We Need It?

### The Problem

Components need to perform actions at specific points in their existence:

1. **On mount**: Fetch data, set up subscriptions, initialize DOM

2. **On update**: Respond to prop/state changes, re-fetch data

3. **On unmount**: Clean up subscriptions, cancel API calls, release resources

Without lifecycle hooks, developers would need manual tracking systems, leading to memory leaks and bugs.

### Evolution of Lifecycle

```text
Lifecycle Evolution:
═══════════════════════════════════════════════════════════════

Class Components (React 16-):
┌─────────────────────────────────────────────────────────────┐
│ componentDidMount()    → After first render                │
│ componentDidUpdate()   → After every re-render             │
│ componentWillUnmount() → Before unmount                    │
│ shouldComponentUpdate() → Before re-render (optimization)  │
│ getDerivedStateFromProps() → Sync state from props         │
│ getSnapshotBeforeUpdate() → Read DOM before update         │
└─────────────────────────────────────────────────────────────┘

Function Components (React 16.8+):
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {}, [])        → After paint (mount/update) │
│ useEffect(() => {}, [deps])    → When deps change          │
│ useEffect(() => {}, undefined) → After every render        │
│ useEffect(() => {              → Cleanup before unmount     │
│   return () => cleanup;        → And before re-run         │
│ }, []);                                                       │
│ useLayoutEffect(() => {}, [])  → After DOM mutation         │
└─────────────────────────────────────────────────────────────┘

```

## How It Works

### Class Component Lifecycle

```text
Class Component Lifecycle Phases:
═══════════════════════════════════════════════════════════════

MOUNTING (Initial Render):
┌─────────────────────────────────────────────────────────────┐
│ 1. constructor()                                            │
│    - Initialize state                                        │
│    - Bind event handlers                                     │
│    - Don't call setState here                                │
│                                                             │
│ 2. static getDerivedStateFromProps(props, state)            │
│    - Sync state from props (rarely used)                    │
│    - Return new state or null                                │
│    - Called on every render                                  │
│                                                             │
│ 3. render()                                                 │
│    - Return JSX (Virtual DOM)                               │
│    - Must be pure (no side effects)                         │
│                                                             │
│ 4. componentDidMount()                                     │
│    - After DOM is painted                                   │
│    - Set up subscriptions                                   │
│    - Fetch data                                             │
│    - Direct DOM manipulation                                │
└─────────────────────────────────────────────────────────────┘

UPDATING (Re-render):
┌─────────────────────────────────────────────────────────────┐
│ 1. static getDerivedStateFromProps(props, state)            │
│    - Sync state from props (if needed)                      │
│                                                             │
│ 2. shouldComponentUpdate(nextProps, nextState)               │
│    - Return false to skip re-render                         │
│    - Performance optimization                               │
│                                                             │
│ 3. render()                                                 │
│    - Return new JSX                                         │
│                                                             │
│ 4. getSnapshotBeforeUpdate(prevProps, prevState)             │
│    - Read DOM before update                                 │
│    - Return value passed to componentDidUpdate              │
│                                                             │
│ 5. componentDidUpdate(prevProps, prevState, snapshot)       │
│    - After DOM is updated                                   │
│    - Compare prevProps/prevState with current                │
│    - Perform side effects based on changes                  │
└─────────────────────────────────────────────────────────────┘

UNMOUNTING (Component Removed):
┌─────────────────────────────────────────────────────────────┐
│ componentWillUnmount()                                     │
│    - Before component is removed from DOM                   │
│    - Clean up subscriptions                                 │
│    - Cancel API calls                                       │
│    - Remove event listeners                                 │
│    - Release resources                                      │
└─────────────────────────────────────────────────────────────┘

ERROR HANDLING:
┌─────────────────────────────────────────────────────────────┐
│ static getDerivedStateFromError(error)                      │
│    - Catch errors in child components                       │
│    - Update state to show fallback UI                       │
│                                                             │
│ componentDidCatch(error, errorInfo)                         │
│    - Log errors to error reporting service                  │
│    - Called during commit phase                             │
└─────────────────────────────────────────────────────────────┘

```

### Function Component Lifecycle with useEffect

```text
Function Component Lifecycle:
═══════════════════════════════════════════════════════════════

MOUNTING:
┌─────────────────────────────────────────────────────────────┐
│ Component function called                                   │
│ render() → Virtual DOM created                              │
│ DOM updated (commit phase)                                  │
│ useLayoutEffect(() => { ... }, []) runs                    │
│ Browser paints                                              │
│ useEffect(() => { ... }, []) runs                          │
└─────────────────────────────────────────────────────────────┘

UPDATING:
┌─────────────────────────────────────────────────────────────┐
│ Component function called (new props/state)                 │
│ render() → New Virtual DOM                                  │
│ DOM updated                                                 │
│ useLayoutEffect cleanup → useLayoutEffect run              │
│ Browser paints                                              │
│ useEffect cleanup → useEffect run                          │
└─────────────────────────────────────────────────────────────┘

UNMOUNTING:
┌─────────────────────────────────────────────────────────────┐
│ Component removed from tree                                 │
│ useLayoutEffect cleanup runs                                │
│ useEffect cleanup runs (asynchronously)                    │
└─────────────────────────────────────────────────────────────┘

CLEANUP FUNCTION:
┌─────────────────────────────────────────────────────────────┐
│ useEffect(() => {                                           │
│   const subscription = subscribe();                         │
│                                                             │
│   return () => {                                            │
│     subscription.unsubscribe(); // Cleanup                  │
│   };                                                        │
│ }, [deps]);                                                 │
│                                                             │
│ Cleanup runs:                                               │
│ 1. Before the effect re-runs (deps changed)                │
│ 2. When component unmounts                                  │
└─────────────────────────────────────────────────────────────┘

```

### Lifecycle Method Mapping

```text
Class → Function Component Mapping:
═══════════════════════════════════════════════════════════════

Class Component              Function Component
───────────────────────────────────────────────────────────────
constructor()          →     useState(initialValue)
componentDidMount()    →     useEffect(() => {}, [])
componentDidUpdate()   →     useEffect(() => {}, [deps])
componentWillUnmount() →     useEffect(() => { return cleanup }, [])
shouldComponentUpdate() →    React.memo() + useMemo/useCallback
getDerivedStateFromProps() → derive state during render
getSnapshotBeforeUpdate() → useLayoutEffect + ref
componentDidCatch()    →     Error Boundary component

```

## Code Examples

### Class Component Lifecycle

```typescript
import React, { Component } from 'react';

interface Props {
  userId: string;
}

interface State {
  user: User | null;
  loading: boolean;
}

class UserProfile extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { user: null, loading: true };
    console.log('1. constructor');
  }

  static getDerivedStateFromProps(props: Props, state: State): Partial<State> {
    console.log('2. getDerivedStateFromProps');
    // Sync state from props if needed
    return null;
  }

  componentDidMount() {
    console.log('4. componentDidMount');
    // Set up subscriptions, fetch data
    this.fetchUser();
  }

  async fetchUser() {
    const user = await fetchUser(this.props.userId);
    this.setState({ user, loading: false });
  }

  componentDidUpdate(prevProps: Props) {
    console.log('5. componentDidUpdate');
    // Respond to prop changes
    if (prevProps.userId !== this.props.userId) {
      this.fetchUser();
    }
  }

  componentWillUnmount() {
    console.log('6. componentWillUnmount');
    // Clean up subscriptions
  }

  render() {
    console.log('3. render');
    const { user, loading } = this.state;

    if (loading) return <div>Loading...</div>;
    return <div>{user?.name}</div>;
  }
}

```

### Function Component with useEffect

```typescript
import React, { useState, useEffect, useLayoutEffect } from 'react';

const UserProfile = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  console.log('1. Component function called (render phase)');

  // ComponentDidMount equivalent
  useEffect(() => {
    console.log('4. useEffect (after paint) - componentDidMount');

    fetchUser(userId).then(data => {
      setUser(data);
      setLoading(false);
    });
  }, []); // Empty deps = run once on mount

  // ComponentDidUpdate equivalent
  useEffect(() => {
    console.log('5. useEffect - componentDidUpdate');

    fetchUser(userId).then(data => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]); // Run when userId changes

  // ComponentWillUnmount equivalent
  useEffect(() => {
    const controller = new AbortController();

    fetchUser(userId, { signal: controller.signal })
      .then(data => {
        setUser(data);
        setLoading(false);
      });

    // Cleanup function
    return () => {
      console.log('6. useEffect cleanup - componentWillUnmount');
      controller.abort(); // Cancel fetch on unmount
    };
  }, [userId]);

  // useLayoutEffect for DOM measurements
  useLayoutEffect(() => {
    console.log('3. useLayoutEffect (after DOM, before paint)');
    // Measure DOM, set refs
  }, []);

  console.log('2. About to return JSX (render phase)');

  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
};

```

### Cleanup Function Patterns

```typescript
// Pattern 1: Subscription with cleanup
const useSubscription = (channel: string) => {
  useEffect(() => {
    const subscription = subscribe(channel);

    return () => {
      subscription.unsubscribe(); // Cleanup
    };
  }, [channel]);
};

// Pattern 2: Event listener with cleanup
const useEventListener = (event: string, handler: Function) => {
  useEffect(() => {
    window.addEventListener(event, handler);

    return () => {
      window.removeEventListener(event, handler); // Cleanup
    };
  }, [event, handler]);
};

// Pattern 3: Timer with cleanup
const useInterval = (callback: Function, delay: number) => {
  useEffect(() => {
    const id = setInterval(callback, delay);

    return () => {
      clearInterval(id); // Cleanup
    };
  }, [callback, delay]);
};

// Pattern 4: Abort controller for fetch
const useFetch = (url: string) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(setData);

    return () => {
      controller.abort(); // Cleanup
    };
  }, [url]);

  return data;
};

```

### Conditional Lifecycle

```typescript
// Class: conditional componentDidUpdate
class MyComponent extends Component<Props, State> {
  componentDidUpdate(prevProps: Props) {
    // Only fetch when specific prop changes
    if (prevProps.userId !== this.props.userId) {
      this.fetchData(this.props.userId);
    }
  }
}

// Function: equivalent with useEffect
const MyComponent = ({ userId }: Props) => {
  useEffect(() => {
    fetchData(userId);
  }, [userId]); // Only runs when userId changes
};

// Multiple effects for different concerns
const MyComponent = ({ userId, theme }: Props) => {
  // Effect 1: Fetch user data
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);

  // Effect 2: Apply theme
  useEffect(() => {
    document.body.className = theme;
    return () => {
      document.body.className = ''; // Cleanup
    };
  }, [theme]);

  // Effect 3: Set up analytics
  useEffect(() => {
    const tracker = trackPageView(userId);
    return () => tracker.stop();
  }, [userId]);
};

```

## Real-World Use Cases

### 1. Data Fetching with Cleanup

```typescript
const UserProfile = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    const fetchUser = async () => {
      try {
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal,
        });
        const data = await response.json();
        setUser(data);
        setError(null);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      }
    };

    fetchUser();

    return () => {
      controller.abort(); // Cleanup: cancel fetch if userId changes or unmount
    };
  }, [userId]);

  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
};

```

### 2. WebSocket Connection Management

```typescript
const useWebSocket = (url: string) => {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      ws.close(); // Cleanup: close WebSocket on unmount
    };
  }, [url]);

  return messages;
};

```

### 3. Document Title Sync

```typescript
const useDocumentTitle = (title: string) => {
  useEffect(() => {
    const prevTitle = document.title;
    document.title = title;

    return () => {
      document.title = prevTitle; // Cleanup: restore previous title
    };
  }, [title]);
};

// Usage
const Dashboard = () => {
  useDocumentTitle('Dashboard - MyApp');
  return <div>Dashboard</div>;
};

```

### 4. Intersection Observer for Lazy Loading

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

    return () => {
      observer.disconnect(); // Cleanup
    };
  }, [ref, options]);

  return isVisible;
};

```

### 5. Window Resize Handler

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

    return () => {
      window.removeEventListener('resize', handleResize); // Cleanup
    };
  }, []);

  return size;
};

```

## Common Mistakes

### 1. Missing Cleanup Functions

```typescript
// ❌ BAD: No cleanup - memory leak
const BadComponent = () => {
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('tick');
    }, 1000);

    // No cleanup! Interval continues after unmount
  }, []);
};

// ✅ GOOD: Proper cleanup
const GoodComponent = () => {
  useEffect(() => {
    const interval = setInterval(() => {
      console.log('tick');
    }, 1000);

    return () => clearInterval(interval); // Cleanup
  }, []);
};

```

### 2. Using useEffect for Derived State

```typescript
// ❌ BAD: useEffect for derived state causes extra re-render
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

### 3. Incorrect Dependency Arrays

```typescript
// ❌ BAD: Missing dependency
const BadComponent = ({ userId }: { userId: string }) => {
  useEffect(() => {
    fetchUser(userId); // userId not in deps!
  }, []); // Will always fetch with initial userId
};

// ❌ BAD: Unnecessary dependencies
const BadComponent = ({ data }: { data: Data }) => {
  const processed = processData(data);

  useEffect(() => {
    saveToDatabase(processed);
  }, [data, processed]); // processed changes on every render

  return <div>{processed}</div>;
};

// ✅ GOOD: Correct dependencies
const GoodComponent = ({ userId }: { userId: string }) => {
  useEffect(() => {
    fetchUser(userId);
  }, [userId]); // Only runs when userId changes
};

```

### 4. Calling setState Without Condition

```typescript
// ❌ BAD: Infinite loop
const InfiniteLoop = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(count + 1); // Causes re-render, triggers effect again
  }); // No dependency array - runs every render

  return <div>{count}</div>;
};

// ✅ GOOD: Conditional update
const GoodComponent = () => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (count < 10) {
      setCount(count + 1);
    }
  }, [count]);

  return <div>{count}</div>;
};

```

## Best Practices

1. **Always return cleanup functions**: For subscriptions, timers, event listeners, and fetch requests.

2. **Use dependency arrays correctly**: Include all values the effect uses.

3. **Compute derived state during render**: Don't use `useEffect` for data transformation.

4. **Split effects by concern**: One effect per side effect.

5. **Use `useLayoutEffect` for DOM measurements**: When you need to measure before paint.

6. **Use `useEffect` for everything else**: Subscriptions, data fetching, logging.

7. **Avoid async functions in useEffect**: Use inner async function or `.then()`.

## Performance Considerations

### Lifecycle Timing

| Method | Timing | Use Case |
|--------|--------|----------|
| constructor | Before first render | Initialize state |
| render | During render phase | Return JSX |
| componentDidMount | After first paint | Setup side effects |
| componentDidUpdate | After re-renders | Respond to changes |
| componentWillUnmount | Before unmount | Cleanup |
| useEffect | After paint (async) | Side effects |
| useLayoutEffect | After DOM mutation (sync) | DOM measurements |

### Effect Frequency

| Dependency Array | When It Runs | Use Case |
|-----------------|--------------|----------|
| `[]` | Once on mount | Initial setup |
| `[dep1, dep2]` | When deps change | Conditional effects |
| No array | Every render | Rarely used |

## Interview Questions

### Beginner (5-10)

**Q1: What is the component lifecycle in React?**
A: The lifecycle is the series of events from when a component is created (mounted), through updates, to when it's destroyed (unmounted). It has three main phases: mounting, updating, and unmounting.

**Q2: What are the main lifecycle methods in class components?**
A: Main methods:

- `componentDidMount()`: After first render
- `componentDidUpdate()`: After re-renders
- `componentWillUnmount()`: Before unmount
- `shouldComponentUpdate()`: Control re-renders
- `render()`: Return JSX

**Q3: How does `useEffect` replace lifecycle methods?**
A: `useEffect` with `[]` deps = `componentDidMount`. `useEffect` with deps = `componentDidUpdate`. `useEffect` return function = `componentWillUnmount`. Multiple `useEffect` calls handle different concerns.

**Q4: What is the cleanup function in `useEffect`?**
A: The cleanup function runs before the effect re-runs (when deps change) and when the component unmounts. It's used to cancel subscriptions, clear timers, and remove event listeners.

**Q5: When does `useLayoutEffect` run?**
A: `useLayoutEffect` runs synchronously after DOM mutations but before the browser paints. Use it for DOM measurements that need to happen before paint.

**Q6: What is `componentDidMount` used for?**
A: `componentDidMount` runs after the first render and DOM paint. It's used for:

- Setting up subscriptions
- Fetching initial data
- Direct DOM manipulation
- Starting timers/intervals

**Q7: What is `componentWillUnmount` used for?**
A: `componentWillUnmount` runs before the component is removed from the DOM. It's used to:

- Clean up subscriptions
- Cancel API calls
- Remove event listeners
- Clear timers

**Q8: Can you use lifecycle methods in function components?**
A: No, lifecycle methods are class component features. Function components use hooks (`useEffect`, `useLayoutEffect`) as replacements.

**Q9: What is the difference between `useEffect` and `useLayoutEffect`?**
A: `useLayoutEffect` runs after DOM mutation, before paint (synchronous). `useEffect` runs after paint (asynchronous). Use `useLayoutEffect` for DOM measurements, `useEffect` for everything else.

**Q10: What is the order of lifecycle events in a class component?**
A: Mounting: constructor → getDerivedStateFromProps → render → componentDidMount. Updating: getDerivedStateFromProps → shouldComponentUpdate → render → getSnapshotBeforeUpdate → componentDidUpdate. Unmounting: componentWillUnmount.

### Intermediate (5-10)

**Q11: How do you handle data fetching in function components?**
A:

```typescript
const fetchData = async (id: string) => {
  const response = await fetch(`/api/data/${id}`);
  return response.json();
};

const MyComponent = ({ id }: { id: string }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    fetchData(id).then(result => {
      if (!cancelled) {
        setData(result);
        setLoading(false);
      }
    });

    return () => {
      cancelled = true; // Prevent state update on unmounted component
    };
  }, [id]);

  if (loading) return <Spinner />;
  return <DataDisplay data={data} />;
};

```

**Q12: How do you handle multiple side effects?**
A: Use multiple `useEffect` calls, each handling a single concern:

```typescript
const MyComponent = ({ userId, theme }: Props) => {
  // Effect 1: Fetch user data
  useEffect(() => {
    fetchUser(userId);
  }, [userId]);

  // Effect 2: Apply theme
  useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  // Effect 3: Track analytics
  useEffect(() => {
    trackPageView(userId);
  }, [userId]);
};

```

**Q13: What is `getDerivedStateFromProps` and when should you use it?**
A: `getDerivedStateFromProps` syncs state from props. It's rarely needed — most use cases can be handled by computing during render or using controlled components.

**Q14: What is `getSnapshotBeforeUpdate` and when should you use it?**
A: `getSnapshotBeforeUpdate` reads DOM before update (e.g., scroll position). The returned value is passed to `componentDidUpdate`. Use it for preserving scroll position during list updates.

**Q15: How do you handle errors in lifecycle methods?**
A: Use error boundaries (class components with `componentDidCatch` or `getDerivedStateFromError`). Function components use the same pattern.

**Q16: What is the difference between `componentDidMount` and `useEffect` with `[]`?**
A: Functionally similar, but timing differs:

- `componentDidMount`: After first render, before paint
- `useEffect([])`: After first render, after paint
`useEffect` is slightly delayed but doesn't block paint.

**Q17: How do you handle async operations in `useEffect`?**
A: Don't use async functions directly. Use inner async function or `.then()`:

```typescript
useEffect(() => {
  const asyncFn = async () => {
    const data = await fetchData();
    setData(data);
  };
  asyncFn();
}, []);

```

**Q18: What is the "zombie children" problem?**
A: When a component updates state after unmounting (often in async operations). Prevention:

- Use AbortController for fetch
- Check if component is still mounted
- Use cleanup functions

**Q19: How do you handle window focus/blur events?**
A:

```typescript
useEffect(() => {
  const handleFocus = () => console.log('focused');
  const handleBlur = () => console.log('blurred');

  window.addEventListener('focus', handleFocus);
  window.addEventListener('blur', handleBlur);

  return () => {
    window.removeEventListener('focus', handleFocus);
    window.removeEventListener('blur', handleBlur);
  };
}, []);

```

**Q20: What is the order of useEffect execution?**
A: Effects run in the order they're defined, after the browser paints. Multiple effects execute sequentially, not in parallel.

### Senior (10-15)

**Q21: Explain the complete lifecycle of a Suspense boundary.**
A: When a component suspends:

1. React pauses rendering of the suspended subtree

2. The Suspense boundary shows the fallback

3. React continues rendering other parts of the tree

4. When the promise resolves, React resumes rendering

5. React commits all changes atomically

6. The real UI replaces the fallback

**Q22: How does the lifecycle differ with React Server Components?**
A: Server Components don't have lifecycle methods or hooks. They run once on the server and are serialized. Client Components have normal lifecycles. Server Components can't use state or effects.

**Q23: How do you test lifecycle behavior?**
A:

```typescript
import { render, act, cleanup } from '@testing-library/react';

afterEach(cleanup);

test('fetches data on mount', async () => {
  const mockFetch = jest.spyOn(global, 'fetch')
    .mockResolvedValue({ json: () => ({ name: 'John' }) });

  render(<UserProfile userId="1" />);

  expect(mockFetch).toHaveBeenCalledWith('/api/users/1');

  await act(async () => {
    // Wait for async operations
  });

  expect(screen.getByText('John')).toBeInTheDocument();

  mockFetch.mockRestore();
});

```

**Q24: How do you handle lifecycle in custom hooks?**
A: Custom hooks encapsulate lifecycle logic:

```typescript
const useDocumentTitle = (title: string) => {
  useEffect(() => {
    const prevTitle = document.title;
    document.title = title;
    return () => { document.title = prevTitle; };
  }, [title]);
};

const useInterval = (callback: Function, delay: number) => {
  useEffect(() => {
    const id = setInterval(callback, delay);
    return () => clearInterval(id);
  }, [callback, delay]);
};

```

**Q25: What are the performance implications of lifecycle methods?**
A:

- `componentDidMount`/`useEffect([])`: One-time cost
- `componentDidUpdate`/`useEffect([deps])`: Per-change cost
- `render`/component function: Every render
- Overhead: Class methods have `this` binding overhead

**Q26: How does React handle lifecycle during concurrent rendering?**
A: During concurrent rendering:

- Render phase can be interrupted
- Effects are batched and applied after commit
- `useLayoutEffect` still runs synchronously
- `useEffect` can be deferred to idle time

**Q27: What is the relationship between lifecycle and React DevTools?**
A: React DevTools shows:

- Component mount/unmount timing
- Re-render reasons (which props/state changed)
- Effect timing and dependencies
- Profiling data for lifecycle performance

**Q28: How do you handle lifecycle in error boundaries?**
A: Error boundaries use:

- `getDerivedStateFromError`: Update state on error
- `componentDidCatch`: Log errors
- They don't have mount/update lifecycle for error handling

**Q29: How do you handle lifecycle with React.memo?**
A: `React.memo` wraps components to skip re-renders. This affects lifecycle:

- `componentDidUpdate`/`useEffect` only run when props change
- Skipped renders don't call component function
- Memoization reduces lifecycle calls

**Q30: What are the common lifecycle patterns in production apps?**
A:

- Data fetching with caching
- WebSocket connection management
- Document title sync
- Window resize handling
- Intersection observer for lazy loading
- Analytics tracking
- Form state management

### FAANG-style (5-10)

**Q31: Design a lifecycle management system for a complex app.**
A:

1. **Custom hooks**: Encapsulate lifecycle logic

2. **Context providers**: Global lifecycle management

3. **Error boundaries**: Catch lifecycle errors

4. **Suspense**: Handle async lifecycle

5. **Cleanup registry**: Centralized cleanup management

**Q32: How would you debug a lifecycle-related memory leak?**
A:

1. **Chrome DevTools Memory**: Heap snapshots to find leaked objects

2. **React DevTools**: Check for unmounted component state updates

3. **Custom logging**: Log mount/unmount events

4. **Network tab**: Check for pending requests after unmount

5. **Profilers**: React.Profiler for lifecycle performance

**Q33: Analyze the performance impact of lifecycle in large apps.**
A:

- **Mount**: 1000 components × 1ms each = 1s total
- **Update**: Frequent updates cause cascading re-renders
- **Unmount**: Cleanup functions add overhead
- **Optimization**: Memoization, virtualization, lazy loading

**Q34: How would you implement a lifecycle observer pattern?**
A:

```typescript
const useLifecycleObserver = (callbacks: LifecycleCallbacks) => {
  useEffect(() => {
    callbacks.onMount?.();
    return () => callbacks.onUnmount?.();
  }, []);

  useEffect(() => {
    callbacks.onUpdate?.();
  });
};

```

**Q35: Design a lifecycle-aware state management system.**
A:

1. **State containers**: Manage state with lifecycle hooks

2. **Subscriptions**: Auto-cleanup on unmount

3. **Side effects**: Lifecycle-bound effects

4. **Error handling**: Graceful degradation

5. **Performance**: Memoized selectors

**Q36: How does lifecycle interact with React Suspense and transitions?**
A: Suspense can suspend lifecycle effects. Transitions can defer effect execution. This creates complex timing:

- Suspense boundaries pause effects
- Transitions keep old effects until new ones are ready
- Cleanup runs during transition

**Q37: Analyze the lifecycle of React Server Components.**
A: Server Components:

- Run once on the server (no lifecycle)
- Serialized as references
- Client Components hydrate with normal lifecycle
- Server effects don't run on client
- Client effects run normally

**Q38: How would you implement cross-component lifecycle coordination?**
A:

1. **Context**: Share lifecycle state across components

2. **Event emitter**: Component communication

3. **Custom hooks**: Coordinated lifecycle logic

4. **Ref forwarding**: Imperative lifecycle access

5. **Render props**: Lifecycle-aware rendering

**Q39: What are the testing strategies for lifecycle behavior?**
A:

1. **Unit tests**: Test individual lifecycle methods

2. **Integration tests**: Test component interactions

3. **E2E tests**: Test real user scenarios

4. **Performance tests**: Measure lifecycle impact

5. **Memory tests**: Detect lifecycle-related leaks

**Q40: How do you handle lifecycle in micro-frontends?**
A:

1. **Isolation**: Each micro-frontend has its own lifecycle

2. **Communication**: Event bus between lifecycles

3. **Shared state**: Cross-lifecycle state management

4. **Cleanup**: Proper teardown on unmount

5. **Error boundaries**: Isolate lifecycle failures

### Follow-ups (5-10)

**Q41: How would you explain lifecycle to a junior developer?**
A: "A component's lifecycle is like a person's life: birth (mount), growing up (update), and passing away (unmount). React gives you hooks to run code at each stage: when the component is born, when it changes, and when it's about to be destroyed."

**Q42: What are the edge cases in lifecycle management?**
A:

- Conditional effects with changing dependencies
- Async operations completing after unmount
- Nested effects with complex dependencies
- Concurrent rendering interrupting effects
- Suspense boundaries affecting effect timing

**Q43: How does lifecycle handle the "race condition" problem?**
A: Race conditions occur when multiple async operations complete out of order. Solutions:

- AbortController to cancel previous requests
- Race condition detection (latest request wins)
- State flags to prevent stale updates

**Q44: What is the relationship between lifecycle and React strict mode?**
A: StrictMode double-renders in development to detect lifecycle issues:

- Missing cleanup functions
- Impure render functions
- Unsafe lifecycle methods
- Side effects in render phase

**Q45: How does lifecycle interact with React DevTools Profiler?**
A: Profiler tracks:

- Component mount/unmount timing
- Re-render frequency and duration
- Effect execution time
- Lifecycle method performance

**Q46: What is the future of lifecycle in React?**
A: React is moving toward:

- Automatic memoization (React Compiler)
- Better concurrent lifecycle handling
- Server Components (no lifecycle)
- Improved Suspense integration
- Automatic cleanup detection

**Q47: How would you implement a lifecycle debugger?**
A:

1. **Custom hook**: Log lifecycle events

2. **React DevTools plugin**: Extend DevTools

3. **Performance API**: Measure lifecycle timing

4. **Visual timeline**: Display lifecycle events

5. **Production logging**: Track lifecycle in production

**Q48: How does lifecycle handle the "state update after unmount" problem?**
A: React 18 warns about state updates after unmount. Prevention:

- Use AbortController for fetch
- Check component mounted status
- Use cleanup functions
- Use `useEffect` cleanup

**Q49: What are the testing patterns for lifecycle behavior?**
A:

```typescript
// Test mount behavior
test('fetches data on mount', async () => {
  render(<Component />);
  await waitFor(() => {
    expect(screen.getByText('Data')).toBeInTheDocument();
  });
});

// Test cleanup
test('cleans up on unmount', () => {
  const { unmount } = render(<Component />);
  unmount();
  // Assert cleanup occurred
});

```

**Q50: How does lifecycle interact with React's concurrent features?**
A: Concurrent features affect lifecycle:

- Render phase can be interrupted
- Effects are batched and deferred
- `useLayoutEffect` still synchronous
- `useEffect` can be deferred to idle time
- Transitions keep old effects until new ones ready

## Summary

The component lifecycle in React manages the series of events from mounting to unmounting. Class components use lifecycle methods (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`). Function components use `useEffect` and `useLayoutEffect`. Understanding lifecycle is crucial for managing side effects, subscriptions, and resource cleanup.

## Cheat Sheet

```text
Lifecycle Key Points:
├── What: Series of events from mount to unmount
├── Three Phases: Mount → Update → Unmount
├── Class: Lifecycle methods (componentDidMount, etc.)
├── Function: useEffect, useLayoutEffect hooks
├── Cleanup: Return function from useEffect
├── Dependencies: Control when effects run
├── Timing: useEffect (after paint), useLayoutEffect (before paint)

Class Methods → Function Hooks:
├── componentDidMount → useEffect(() => {}, [])
├── componentDidUpdate → useEffect(() => {}, [deps])
├── componentWillUnmount → useEffect(() => { return cleanup }, [])
├── shouldComponentUpdate → React.memo + useMemo/useCallback
├── getDerivedStateFromProps → Compute during render
├── getSnapshotBeforeUpdate → useLayoutEffect + ref
└── componentDidCatch → Error Boundary component

Effect Patterns:
├── Mount: useEffect(() => { ... }, [])
├── Update: useEffect(() => { ... }, [deps])
├── Unmount: useEffect(() => { return () => cleanup }, [])
├── Every render: useEffect(() => { ... })
├── DOM measurement: useLayoutEffect(() => { ... }, [])
└── Async operation: useEffect(() => { asyncFn() }, [])

Common Mistakes:
├── Missing cleanup functions (memory leaks)
├── Using useEffect for derived state (extra re-render)
├── Incorrect dependency arrays
├── Calling setState without condition (infinite loop)
├── Async functions directly in useEffect
└── Not cleaning up subscriptions

Best Practices:
├── Always return cleanup functions
├── Use dependency arrays correctly
├── Compute derived state during render
├── Split effects by concern
├── Use useLayoutEffect for DOM measurements
├── Use useEffect for side effects
└── Handle async operations properly

```

## References & Learn More

- [React Docs: Lifecycle](https://react.dev/reference/react/Component#componentdidcatch)
- [React Lifecycle Methods Diagram](https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/)
- [React useEffect as lifecycle replacement](https://react.dev/learn/synchronizing-with-effects)
