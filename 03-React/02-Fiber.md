---
section: React
category: Frontend
tags: [concept]
---

# React Fiber

[![Section](https://img.shields.io/badge/section-React-00b4d8)](.)
[![Type](https://img.shields.io/badge/type-Concept-informational)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

## Definition

React Fiber is the **reconciliation engine** (reconciler) introduced in React 16 that replaced the previous stack-based reconciler. It is a reimplementation of React's core algorithm that enables **incremental rendering** — the ability to split rendering work into chunks and spread it out over multiple frames. Fiber is not a feature you use directly; it's the internal architecture that powers React's ability to pause, resume, and prioritize rendering work.

Fiber represents each component as a **fiber node** (a JavaScript object) containing the component's state, props, effects, and scheduling information. The collection of fiber nodes forms a **fiber tree** (also called the React element tree or virtual DOM tree).

## Why Do We Need It?

### The Problem with the Stack Reconciler

The previous reconciler (React 15 and earlier) was synchronous and unblockable:

1. **Main thread blocking**: Once React started rendering, it couldn't be interrupted. Long component trees would block the main thread.

2. **No prioritization**: All updates were treated equally. A typing event and a data fetch completion got the same priority.

3. **Janky animations**: Long renders caused frame drops, making animations janky.

4. **No pause/resume**: React couldn't pause rendering to handle urgent events.

```text
Stack Reconciler (React 15):
┌──────────────────────────────────────────────┐
│ Render Start                                 │
│ ┌──────────────────────────────────────────┐ │
│ │ Component Tree Rendering (SYNC)          │ │
│ │ 500ms - CANNOT BE INTERRUPTED           │ │
│ │ Main thread BLOCKED                      │ │
│ └──────────────────────────────────────────┘ │
│ Render Complete                              │
│ Total: 500ms of jank                        │
└──────────────────────────────────────────────┘

Fiber Reconciler (React 16+):
┌──────────────────────────────────────────────┐
│ Frame 1 (16ms budget)                        │
│ ┌──────────────────────────────────────────┐ │
│ │ Render 200 fibers (INTERRUPTIBLE)       │ │
│ │ → Yield to browser for events            │ │
│ └──────────────────────────────────────────┘ │
│ Frame 2 (16ms budget)                        │
│ ┌──────────────────────────────────────────┐ │
│ │ Render 200 more fibers                   │ │
│ │ → Yield again                            │ │
│ └──────────────────────────────────────────┘ │
│ Frame 3 (16ms budget)                        │
│ ┌──────────────────────────────────────────┐ │
│ │ Render remaining fibers                  │ │
│ │ → Commit all changes to DOM              │ │
│ └──────────────────────────────────────────┘ │
│ Total: 3 frames, no jank, events handled    │
└──────────────────────────────────────────────┘

```

## How It Works

### Fiber Node Structure

Each fiber node contains:

```typescript
interface FiberNode {
  // Instance properties
  tag: WorkTag;                    // Component type (FunctionComponent, ClassComponent, HostComponent, etc.)
  key: string | null;              // React key
  type: any;                       // Component function/class or string (div, span, etc.)
  stateNode: any;                  // Reference to DOM node or class instance

  // Tree structure (linked list)
  return: FiberNode | null;        // Parent fiber
  child: FiberNode | null;         // First child fiber
  sibling: FiberNode | null;       // Next sibling fiber
  index: number;                   // Child index

  // Pending work
  pendingProps: any;               // Props being received
  memoizedProps: any;              // Props from last render
  memoizedState: any;              // State from last render
  updateQueue: UpdateQueue<any> | null; // Pending state updates

  // Effects
  flags: Flags;                    // Side effect tags (Placement, Update, Deletion, etc.)
  subtreeFlags: Flags;             // Combined flags from subtree
  deletions: FiberNode[] | null;   // Fibers to delete

  // Scheduling
  lanes: Lanes;                    // Priority lanes (pending work)
  childLanes: Lanes;               // Child's pending work
  alternate: FiberNode | null;     // Reference to the other tree (current vs work-in-progress)

  // Effects
  updateEffect: Effect | null;     // useEffect effects
  layoutEffect: Effect | null;     // useLayoutEffect effects
  destroyEffect: Effect | null;    // Cleanup functions
}

```

### Fiber Tree Structure

```text
Fiber Tree (Linked List):
═══════════════════════════════════════════════════════════════

    App (Fiber)
    ├── return: null (root)
    ├── child: Header (Fiber)
    │   ├── return: App
    │   ├── child: Logo (Fiber)
    │   │   ├── return: Header
    │   │   ├── sibling: Nav (Fiber)
    │   │   │   ├── return: Header
    │   │   │   └── sibling: null
    │   │   └── sibling: Nav
    │   └── sibling: Main (Fiber)
    │       ├── return: App
    │       ├── child: Card (Fiber)
    │       │   ├── return: Main
    │       │   ├── child: Title (Fiber)
    │       │   │   ├── return: Card
    │       │   │   └── sibling: Content (Fiber)
    │       │   └── sibling: Sidebar (Fiber)
    │       └── sibling: Footer (Fiber)
    └── sibling: null

Traversal Order:

1. App → Header → Logo (child-first, depth-first)

2. → Nav (sibling of Logo)

3. → Main (sibling of Header)

4. → Card → Title → Content

5. → Sidebar (sibling of Card)

6. → Footer (sibling of Main)

```

### Work Loop

The Fiber work loop processes fibers in a depth-first traversal:

```text
Work Loop Algorithm:
═══════════════════════════════════════════════════════════════

function workLoop(deadline) {
  // Continue working while there's time remaining in the frame
  while (nextUnitOfWork && deadline.timeRemaining() > 1) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
  }

  if (nextUnitOfWork) {
    // Not done yet, yield to browser and continue next frame
    requestIdleCallback(workLoop);
  } else {
    // All work done, commit to DOM
    commitRoot();
  }
}

performUnitOfWork(fiber) {
  // 1. Begin phase: Process current fiber
  beginWork(fiber);

  // 2. If fiber has child, return child
  if (fiber.child) {
    return fiber.child;
  }

  // 3. Complete phase: Go up the tree
  let current = fiber;
  while (current) {
    completeWork(current);

    if (current.sibling) {
      return current.sibling;
    }
    current = current.return;
  }

  return null;
}

```

### Two-Phase Rendering

```text
Fiber Rendering Phases:
═══════════════════════════════════════════════════════════════

Render Phase (BEGIN + COMPLETE):
┌─────────────────────────────────────────────────┐
│ Begin Work: Traverse tree downward              │
│ ┌─────────────────────────────────────────────┐ │
│ │ App → Header → Logo → Nav → Main → Card... │ │
│ │                                             │ │
│ │ For each fiber:                             │ │
│ │ - Call component function/class             │ │
│ │ - Compare with previous props               │ │
│ │ - Add work to fiber if needed               │ │
│ │ - Can be INTERRUPTED at any point           │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ Complete Work: Traverse tree upward             │
│ ┌─────────────────────────────────────────────┐ │
│ │ Logo → Nav → Header → Title → Card → Main  │ │
│ │                                             │ │
│ │ For each fiber:                             │ │
│ │ - Create/update DOM nodes                   │ │
│ │ - Queue effects                             │ │
│ │ - Cannot be interrupted (fast operations)   │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                    │
                    ▼
Commit Phase (不可中断):
┌─────────────────────────────────────────────────┐
│ 1. Before mutation: getSnapshotBeforeUpdate     │
│ 2. Mutation: Apply DOM changes                  │
│    - Insertions, Updates, Deletions             │
│ 3. Layout: useLayoutEffect callbacks            │
│ 4. Passive: useEffect callbacks (async)         │
└─────────────────────────────────────────────────┘

```

### Priority Lanes

React 18 uses a **lanes model** for priority scheduling:

```text
Priority Lanes (React 18):
═══════════════════════════════════════════════════════════════

Highest Priority
│
├── Sync Lane (0b0000000000000000000000000000001)
│   └── Synchronous updates (flushSync, ReactDOM.flushSync)
│
├── Input Continuous Lane (0b0000000000000000000000000000100)
│   └── Continuous inputs (scroll, drag)
│
├── Input Transition Lane (0b0000000000000000000000000001000)
│   └── Urgent transitions (clicks, keypresses)
│
├── Default Lane (0b00000000000000000000000000100000)
│   └── Default updates (setState without flushSync)
│
├── Transition Lane 1-8 (various bitmasks)
│   └── Low priority transitions (useTransition, startTransition)
│
├── Idle Lane (0b01000000000000000000000000000000)
│   └── Idle work (preparation for future interactions)
│
└── Offscreen Lane (various)
    └── Offscreen rendering (pre-rendering for Suspense)

Lane Example:
┌────────────────────────────────────────────────────────────┐
│ Frame 1: Process Sync + Input lanes (high priority)       │
│ Frame 2: Process Default lane (medium priority)           │
│ Frame 3: Process Transition lanes (low priority)          │
│ Frame 4: Process Idle lane (background)                   │
└────────────────────────────────────────────────────────────┘

```

## Code Examples

### Understanding Fiber Internals

```typescript
// React DevTools shows the fiber tree
// You can inspect fiber nodes in browser DevTools

// Fiber node types (WorkTag enum values):
enum WorkTag {
  FunctionComponent = 0,
  ClassComponent = 1,
  IndeterminateComponent = 2,
  HostRoot = 3,
  HostPortal = 4,
  HostComponent = 5,    // div, span, etc.
  HostText = 6,
  Fragment = 7,
  Mode = 8,
  ContextConsumer = 9,
  ContextProvider = 10,
  ForwardRef = 11,
  SuspenseComponent = 12,
  MemoComponent = 13,
  LazyComponent = 14,
  // ... more types
}

```

### Demonstrating Concurrent Rendering

```typescript
import React, { useState, useTransition, useDeferredValue } from 'react';

const SearchApp = () => {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const deferredQuery = useDeferredValue(query);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value); // High priority: update input immediately

    startTransition(() => {
      // Low priority: update search results
      // Can be interrupted if user types again
      setFilteredResults(filterData(value));
    });
  };

  return (
    <div>
      <input value={query} onChange={handleSearch} />
      {isPending && <Spinner />}
      <Results query={deferredQuery} />
    </div>
  );
};

```

### Demonstrating Time Slicing

```typescript
import React, { useState, useEffect, useTransition } from 'react';

const LargeList = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    // Fetch large dataset
    fetchLargeDataset().then(data => {
      startTransition(() => {
        // This update can be interrupted
        // React will render in chunks across multiple frames
        setItems(data);
      });
    });
  }, []);

  return (
    <div>
      {isPending && <div>Updating list...</div>}
      <VirtualList items={items} />
    </div>
  );
};

```

### useTransition vs useDeferredValue

```typescript
import React, { useState, useTransition, useDeferredValue } from 'react';

// useTransition: Mark state updates as non-urgent
const useTransitionExample = () => {
  const [isPending, startTransition] = useTransition();
  const [count, setCount] = useState(0);

  const handleClick = () => {
    startTransition(() => {
      // This update is low priority
      // React can defer it if there's urgent work
      setCount(c => c + 1);
    });
  };

  return <button onClick={handleClick}>{count} {isPending && '...'}</button>;
};

// useDeferredValue: Defer a derived value
const useDeferredValueExample = () => {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        <Results query={deferredQuery} />
      </div>
    </div>
  );
};

```

### Concurrent Features in Action

```typescript
import React, { useState, useTransition, Suspense } from 'react';

const ConcurrentApp = () => {
  const [resource, setResource] = useState(initialResource);
  const [isPending, startTransition] = useTransition();

  const handleTabChange = (tab: string) => {
    startTransition(() => {
      // This state update is non-urgent
      // React keeps old UI visible while preparing new one
      setResource(fetchResource(tab));
    });
  };

  return (
    <div>
      <TabBar onChange={handleTabChange} />
      {/* isPending shows loading state for the transition */}
      {isPending && <Spinner />}
      <Suspense fallback={<Loading />}>
        <ResourcePanel resource={resource} />
      </Suspense>
    </div>
  );
};

```

## Real-World Use Cases

### 1. Search with Large Dataset

```typescript
const SearchDashboard = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isPending, startTransition] = useTransition();

  const handleSearch = useCallback((value: string) => {
    setQuery(value); // Immediate: update input

    startTransition(() => {
      // Deferred: update results (can be interrupted)
      const filtered = filterAndSort(hugeDataset, value);
      setResults(filtered);
    });
  }, []);

  return (
    <div>
      <SearchInput value={query} onChange={handleSearch} />
      {isPending && <LoadingIndicator />}
      <ResultList results={results} />
    </div>
  );
};

```

### 2. Tab Switching with Heavy Content

```typescript
const TabContainer = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isPending, startTransition] = useTransition();

  const handleTabSwitch = (tab: string) => {
    startTransition(() => {
      setActiveTab(tab); // Non-urgent: React can defer
    });
  };

  return (
    <div>
      <TabBar
        tabs={['overview', 'details', 'reviews']}
        active={activeTab}
        onChange={handleTabSwitch}
      />
      {isPending && <TabSpinner />}
      <TabContent tab={activeTab} />
    </div>
  );
};

```

### 3. Animation with Priority

```typescript
const AnimatedList = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [animationPhase, setAnimationPhase] = useState<'idle' | 'animating'>('idle');

  useEffect(() => {
    // High priority: handle user interaction
    // Low priority: animate between states
    const unsubscribe = subscribeToData(newItems => {
      startTransition(() => {
        setItems(newItems);
      });
    });
    return unsubscribe;
  }, []);

  return (
    <div>
      {items.map(item => (
        <AnimatedItem key={item.id} item={item} isPending={animationPhase === 'animating'} />
      ))}
    </div>
  );
};

```

### 4. Server-Side Rendering with Streaming

```typescript
// Server component (simplified)
const App = () => (
  <html>
    <body>
      <Suspense fallback={<Loading />}>
        <Header /> {/* Renders immediately */}
      </Suspense>
      <Suspense fallback={<Loading />}>
        <SlowComponent /> {/* Streams when ready */}
      </Suspense>
    </body>
  </html>
);

// Client hydration (simplified)
const root = ReactDOM.hydrateRoot(
  document.getElementById('root'),
  <App />,
  {
    // React can hydrate in chunks, not all at once
    onHydrated: () => console.log('Hydrated'),
  }
);

```

## Common Mistakes

### 1. Confusing Fiber with Feature

```typescript
// ❌ WRONG: "I'll use Fiber to make my app faster"
// Fiber is internal architecture, not a feature you use directly

// ✅ CORRECT: Use concurrent features that Fiber enables
const App = () => {
  const [isPending, startTransition] = useTransition();
  // ...
};

```

### 2. Assuming All Updates Are Low Priority

```typescript
// ❌ WRONG: Wrapping everything in startTransition
const handleClick = () => {
  startTransition(() => {
    setIsOpen(true); // This should be HIGH priority (user interaction)
  });
};

// ✅ CORRECT: Only use startTransition for non-urgent updates
const handleSearch = (value: string) => {
  setSearchQuery(value); // Urgent: update input immediately

  startTransition(() => {
    setFilteredResults(filterData(value)); // Non-urgent: can be deferred
  });
};

```

### 3. Misunderstanding `useDeferredValue`

```typescript
// ❌ WRONG: Using useDeferredValue as a memoization tool
const expensiveValue = useMemo(() => computeExpensiveValue(input), [input]);
const deferredValue = useDeferredValue(expensiveValue); // Wrong: defeats the purpose

// ✅ CORRECT: Use useDeferredValue for derived values that can lag
const query = useDeferredValue(searchInput); // OK: search results can lag

```

### 4. Not Understanding Lane Priorities

```typescript
// ❌ WRONG: Assuming all state updates have the same priority
const handleEverything = () => {
  setState1(a + 1); // Priority depends on context
  setState2(b + 1); // Might be different priority
};

// ✅ CORRECT: Understand priority ordering
const handleMixed = () => {
  // This gets Sync Lane (highest priority)
  flushSync(() => {
    setUrgentState(true);
  });

  // This gets Default Lane (medium priority)
  setNormalState(value);

  // This gets Transition Lane (low priority)
  startTransition(() => {
    setDeferredState(newValue);
  });
};

```

## Best Practices

1. **Use `useTransition` for non-urgent state updates**: Search filtering, tab switching, list updates.

2. **Use `useDeferredValue` for derived values**: When a value can lag behind its source.

3. **Keep urgent updates outside `startTransition`**: Input values, click handlers should be immediate.

4. **Profile before using concurrent features**: Not all apps need them.

5. **Combine with `React.memo`**: Concurrent features work best with memoized components.

6. **Use Suspense with concurrent features**: Boundaries help React prioritize hydration.

7. **Understand the lanes model**: Know which updates get which priority.

## Performance Considerations

### Fiber Overhead

Fiber adds memory overhead compared to the stack reconciler:

- Each fiber node is ~1KB (vs ~100B for stack frames)
- Linked list structure requires more memory
- Scheduling logic adds CPU overhead

### When Concurrent Features Help

| Scenario | Without Concurrent | With Concurrent |
|----------|-------------------|-----------------|
| Search with 10K items | Janky input, delayed results | Smooth input, deferred results |
| Tab switching (heavy content) | UI freezes during switch | Old tab visible until new ready |
| Animation + data load | Frame drops | Smooth animation |
| Large list rendering | Stuttering during scroll | Smooth scrolling |

### When Concurrent Features Hurt

- **Small apps**: Overhead not worth it
- **Simple state updates**: `startTransition` adds unnecessary complexity
- **Synchronous requirements**: Some updates must be immediate


## Summary

React Fiber is the internal architecture that powers React's reconciliation and scheduling. It represents each component as a fiber node in a linked list tree, enabling incremental rendering, prioritization, and concurrent features. Fiber replaced the stack reconciler to solve the problem of main thread blocking, enabling React to keep UIs responsive during heavy renders.

## Cheat Sheet
```text
Fiber Architecture:
├── What: React's reconciliation engine (React 16+)
├── Why: Enable incremental rendering & prioritization
├── Fiber Node: JS object with state, props, effects, scheduling
├── Two Trees: Current (on screen) + Work-in-progress (being built)
├── Work Loop: Depth-first traversal, yields when frame budget expires
├── Phases: Render (interruptible) → Commit (synchronous)
├── Lanes: Priority model for scheduling updates
├── Concurrent: React 18 features built on Fiber (transitions, deferred values)

Key Concepts:
├── alternate: Link between current and work-in-progress trees
├── flags: Side effect tags (Placement, Update, Deletion)
├── lanes: Priority levels for updates
├── subtreeFlags: Combined flags from child fibers
├── work-in-progress: Fiber tree being constructed
└── commitRoot: Apply all changes atomically

Concurrent Features:
├── useTransition: Mark state updates as non-urgent
├── useDeferredValue: Defer derived values
├── Suspense: Pause rendering for async data
├── startTransition: Standalone transition function
├── flushSync: Force synchronous rendering
└── useDeferredValue: Lag behind source value

When to Use Concurrent Features:
├── Search filtering (defer results)
├── Tab switching (keep old tab visible)
├── Large list updates (smooth scrolling)
├── Animation + data load (prevent jank)
└── Any non-urgent state update

Common Pitfalls:
├── Wrapping urgent updates in startTransition
├── Using useDeferredValue for memoization
├── Assuming all updates are equal priority
├── Not profiling before using concurrent features
└── Over-using startTransition for simple updates

```

---

## See Also
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)
- [Form Handling](../29-Form-Handling/)
- [Animation](../30-Animation/)

## References & Learn More

- [React Fiber Architecture](https://github.com/acdlite/react-fiber-architecture)
- [A Complete Guide to React Fiber](https://blog.bitsrc.io/react-fiber-an-in-depth-explanation-of-changes-in-react-16-fc63e88e1d8e)
- [React 16 Fiber Architecture](https://medium.com/react-in-depth/the-fiber-reconciler-changed-in-react-16-90074b96e017)
