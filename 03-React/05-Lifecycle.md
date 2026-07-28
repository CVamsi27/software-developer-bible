---
section: React
category: Frontend
tags: [concept]
---

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

---

## See Also
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)
- [Form Handling](../29-Form-Handling/)
- [Animation](../30-Animation/)

## References & Learn More

- [React Docs: Lifecycle](https://react.dev/reference/react/Component#componentdidcatch)
- [React Lifecycle Methods Diagram](https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/)
- [React useEffect as lifecycle replacement](https://react.dev/learn/synchronizing-with-effects)
