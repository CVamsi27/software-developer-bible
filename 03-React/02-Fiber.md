# React Fiber

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

## Interview Questions

### Beginner (5-10)

**Q1: What is React Fiber?**
A: React Fiber is React's reconciliation engine introduced in React 16. It's an internal architecture that represents each component as a "fiber node" (a JavaScript object) and enables incremental rendering — splitting work into chunks that can be paused and resumed.

**Q2: Why was Fiber created?**
A: The previous stack reconciler was synchronous and couldn't be interrupted. Fiber enables incremental rendering, allowing React to pause rendering to handle urgent events, prioritize updates, and avoid blocking the main thread.

**Q3: What is a fiber node?**
A: A fiber node is a JavaScript object representing a component or element in React's tree. It contains references to parent, child, and sibling fibers, as well as state, props, effects, and scheduling information (priority lanes).

**Q4: What is the work loop?**
A: The work loop is the algorithm that processes fiber nodes. It traverses the fiber tree depth-first, performing "begin work" (going down) and "complete work" (going up), yielding to the browser when frame time runs out.

**Q5: What is the difference between the render phase and commit phase?**
A: The render phase (begin work + complete work) is interruptible and happens in memory. The commit phase applies DOM changes and runs effects — it cannot be interrupted and runs synchronously.

**Q6: What are lanes in React 18?**
A: Lanes are a priority model for scheduling work. React assigns different lanes (priority levels) to updates: sync lane for urgent work, default lane for normal updates, and transition lanes for non-urgent work.

**Q7: What is `useTransition`?**
A: `useTransition` is a hook that marks state updates as non-urgent (transitions). React can defer these updates if there's urgent work, keeping the old UI visible until the new state is ready.

**Q8: What is `useDeferredValue`?**
A: `useDeferredValue` returns a deferred version of a value that can lag behind its source. React prioritizes updating the source immediately and defers updating the derived value.

**Q9: How does Fiber improve performance?**
A: Fiber improves performance by:
1. Not blocking the main thread during rendering
2. Prioritizing urgent updates over non-urgent ones
3. Allowing React to keep the UI responsive during heavy renders
4. Enabling concurrent features like transitions

**Q10: Is Fiber a new API or internal architecture?**
A: Fiber is an internal architecture change, not a new API. Developers don't interact with Fiber directly; they use features enabled by Fiber (like `useTransition` and `useDeferredValue`).

### Intermediate (5-10)

**Q11: Explain the two-tree architecture in Fiber.**
A: Fiber maintains two fiber trees:
1. **Current tree**: Represents what's currently on screen
2. **Work-in-progress tree**: Being constructed during rendering
When rendering completes, the work-in-progress tree becomes the current tree (via the `alternate` link).

**Q12: What is the `alternate` property?**
A: The `alternate` property on a fiber node points to the corresponding fiber in the other tree (current ↔ work-in-progress). React uses this to diff between the two trees and determine what needs updating.

**Q13: How does Fiber handle side effects?**
A: Effects (like `useEffect`) are collected during the render phase and applied during the commit phase. Each fiber can have:
- `updateEffect`: For `useEffect`
- `layoutEffect`: For `useLayoutEffect`
- `destroyEffect`: For cleanup functions

**Q14: What is `flushSync` and when should you use it?**
A: `flushSync` forces React to synchronously flush all pending updates. Use it when you need to ensure DOM updates happen immediately (e.g., measuring DOM after state change).

```typescript
import { flushSync } from 'react-dom';

const handleClick = () => {
  flushSync(() => {
    setCount(c => c + 1);
  });
  // DOM is now updated
  console.log(document.getElementById('count')?.textContent); // Shows new count
};
```

**Q15: How does React schedule work?**
A: React uses a scheduler based on `MessageChannel` (or `requestIdleCallback` polyfill). The scheduler:
1. Accepts tasks with priority levels
2. Uses a task queue sorted by priority
3. Executes tasks within frame budget (~16ms)
4. Yields to browser when time runs out

**Q16: What is the difference between `useTransition` and `setTimeout`?**
A: `useTransition` is integrated with React's scheduler and knows about frame budgets. `setTimeout` is browser-scheduled and doesn't coordinate with React's rendering. `useTransition` also tracks `isPending` state.

**Q17: How does Fiber handle error boundaries?**
A: Error boundaries catch errors during the render phase. When a component throws, React walks up the fiber tree looking for error boundaries (`componentDidCatch` or `getDerivedStateFromError`). The error boundary's fiber gets updated with the error state.

**Q18: What is the priority inversion problem?**
A: Priority inversion occurs when a low-priority update blocks a high-priority update. React's lanes model prevents this by allowing urgent updates to interrupt non-urgent ones. However, nested transitions can still cause unexpected behavior.

**Q19: How does `React.memo` interact with Fiber?**
A: `React.memo` marks a fiber as memoized. During the render phase, React compares the fiber's `memoizedProps` with new props. If they're equal (shallow comparison), React skips rendering that subtree, avoiding unnecessary fiber creation.

**Q20: What is the `NoMode` and how does it relate to concurrent features?**
A: `NoMode` is a fiber mode flag. In React 18, the default mode enables concurrent features. Strict Mode (`<StrictMode>`) runs effects twice and enables additional checks for development.

### Senior (10-15)

**Q21: Explain the complete Fiber work loop algorithm.**
A:
```typescript
function workLoop(deadline) {
  while (nextUnitOfWork && !shouldYield()) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
  }
  if (nextUnitOfWork) {
    scheduleCallback(workLoop); // Not done, continue later
  } else if (root.pendingLanes !== NoLanes) {
    commitRoot(); // All work done, commit
  }
}

function performUnitOfWork(fiber) {
  beginWork(fiber); // Process current fiber
  if (fiber.child) return fiber.child; // Go deeper

  // Complete: go up the tree
  let completedFiber = fiber;
  while (completedFiber) {
    completeWork(completedFiber);
    if (completedFiber.sibling) return completedFiber.sibling;
    completedFiber = completedFiber.return;
  }
  return null;
}
```

**Q22: How does React determine if a transition is "urgent"?**
A: React uses a heuristic based on whether the update is caused by user input (clicks, keypresses) or programmatic changes. Updates in event handlers are typically urgent; updates in `startTransition` are non-urgent. The `isInputPending` API helps detect if there's pending user input.

**Q23: What is the difference between `useTransition` and `startTransition`?**
A: `useTransition` returns `isPending` (a boolean tracking if the transition is active) and a `startTransition` function. `startTransition` is a standalone function (from `react`) that doesn't provide `isPending`. Use `useTransition` when you need to show loading states.

**Q24: How does Fiber handle Suspense boundaries?**
A: When a component suspends (throws a Promise), React:
1. Catches the promise at the Suspense boundary
2. Marks the suspended fiber as "suspended"
3. Shows the fallback UI
4. When the promise resolves, React resumes rendering and commits the real UI
5. This works because Fiber can pause/resume rendering

**Q25: Explain the `subtreeFlags` property.**
A: `subtreeFlags` is a bitmask of all effect flags in a fiber's subtree. During the complete phase, React propagates flags upward. When committing, React can skip subtrees with no flags (`subtreeFlags === 0`), optimizing the commit phase.

**Q26: How does React handle concurrent rendering of multiple roots?**
A: React maintains separate fiber trees for each root (each `createRoot` call). Each root has its own pending lanes. The scheduler processes all roots in priority order. Higher-priority roots get processed first, but all share the same frame budget.

**Q27: What is the `enableSyncDefaultUpdates` feature?**
A: When enabled (React 18), all updates default to sync lane unless wrapped in `startTransition`. This ensures all updates are processed synchronously for backward compatibility. Without this flag, some updates might be deferred unexpectedly.

**Q28: How does Fiber interact with React DevTools?**
A: React DevTools hooks into Fiber internals via `react-devtools-shared`. It reads fiber nodes to display the component tree, props, state, and hooks. The DevTools can also highlight re-renders, measure performance, and show why components re-rendered.

**Q29: What is the `Offscreen` component and how does it work?**
A: `Offscreen` (experimental, now called `Activity`) is a component that can "hide" its subtree without unmounting it. React can prepare the hidden subtree in the background and instantly show it when needed. This is useful for pre-rendering tabs or off-screen content.

**Q30: How does Fiber handle the `key` prop in reconciliation?**
A: During the render phase, React uses keys to match old and new children. If a key changes, React treats it as a new component (unmounts old, mounts new). Keys help React efficiently track element identity across renders, minimizing unnecessary fiber creation and destruction.

### FAANG-style (5-10)

**Q31: Design a system that uses concurrent features for a real-time collaborative editor.**
A:
1. **Priority model**: User keystrokes → Sync lane; remote changes → Transition lanes
2. **useTransition**: Mark remote changes as non-urgent
3. **useDeferredValue**: Defer rendering of non-visible collaborators
4. **Suspense**: Lazy load collaborative features
5. **State management**: CRDT-based with React state

```typescript
const CollaborativeEditor = () => {
  const [localContent, setLocalContent] = useState('');
  const [remoteChanges, setRemoteChanges] = useState<Change[]>([]);
  const [isPending, startTransition] = useTransition();

  const handleLocalEdit = (newContent: string) => {
    setLocalContent(newContent); // Urgent: update immediately
  };

  useEffect(() => {
    const unsubscribe = subscribeToChanges((change: Change) => {
      startTransition(() => {
        // Non-urgent: remote changes can lag
        setRemoteChanges(prev => [...prev, change]);
      });
    });
    return unsubscribe;
  }, []);

  return (
    <div>
      <Editor value={localContent} onChange={handleLocalEdit} />
      {isPending && <RemoteChangeIndicator />}
      <RemoteCursors changes={remoteChanges} />
    </div>
  );
};
```

**Q32: How would you debug a Fiber-related performance issue?**
A:
1. **React DevTools Profiler**: Record interactions, identify slow commits
2. **Chrome DevTools Performance**: Record and analyze fiber processing time
3. **React.Profiler component**: Programmatic profiling with `onRender` callback
4. **Lane analysis**: Log which lanes are being processed
5. **Custom fiber inspection**: Access fiber nodes via `__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED`

**Q33: Explain the memory model of Fiber and how to optimize it.**
A: Each fiber node contains:
- ~50 properties (1-2KB each)
- References to other fibers (parent, child, sibling, alternate)
- State, props, effects

Optimization:
- **Component unmounting**: Ensure components unmount when not needed
- **Virtualization**: Only render visible components
- **State cleanup**: Clean up state when components unmount
- **Memoization**: Skip fiber creation for unchanged components

**Q34: How would you implement a custom scheduler on top of Fiber?**
A:
1. **Access fiber internals**: Use React's internal APIs (not recommended for production)
2. **Custom lanes**: Define custom lane priorities for your use case
3. **Task scheduling**: Use `scheduler` package to schedule work
4. **Priority inversion**: Implement priority inheritance for nested updates

```typescript
// Conceptual example (not production code)
const CustomScheduler = () => {
  const scheduleTask = (priority: number, task: () => void) => {
    // Map your priority to React lanes
    const lane = priorityToLane(priority);
    // Use React's internal scheduler
    scheduleCallback(priority, task);
  };

  return { scheduleTask };
};
```

**Q35: How does Fiber handle the interaction between concurrent rendering and Suspense?**
A: When a component suspends during concurrent rendering:
1. React pauses rendering of the suspended subtree
2. The Suspense boundary shows the fallback
3. React continues rendering other parts of the tree
4. When the promise resolves, React resumes rendering the suspended subtree
5. React commits all changes atomically

**Q36: Analyze the performance characteristics of the Fiber architecture.**
A:
| Metric | Stack Reconciler | Fiber Reconciler |
|--------|-----------------|------------------|
| Memory per component | ~100B | ~1-2KB |
| Render speed (simple) | ~0.1ms | ~0.15ms |
| Render speed (complex) | Blocks main thread | Chunked, non-blocking |
| Worst-case blocking | O(n) | O(1) per frame |
| Priority support | None | Full lanes model |

**Q37: How would you test concurrent features in a CI environment?**
A:
1. **React Testing Library**: Use `act()` to wrap concurrent updates
2. **Fake timers**: Control `setTimeout` and `MessageChannel` for deterministic testing
3. **Custom scheduler**: Mock React's scheduler for testing priority
4. **End-to-end tests**: Use Cypress/Playwright with `waitFor` for async updates

```typescript
import { render, screen, act } from '@testing-library/react';

test('concurrent update', async () => {
  const { result } = renderHook(() => useTransition());

  await act(async () => {
    result.current.startTransition(() => {
      // Test transition behavior
    });
  });

  expect(result.current.isPending).toBe(false);
});
```

**Q38: How does Fiber interact with React Server Components?**
A: Server Components run on the server and don't have Fiber nodes. They're serialized as a reference tree. Client Components hydrate with Fiber nodes. React reconciles the server tree with the client tree, creating fibers only for client components. Server Components are "invisible" to Fiber.

**Q39: Explain the `enableSuspenseAvoidThisFallback` feature.**
A: This experimental feature allows React to avoid showing Suspense fallbacks during concurrent rendering. React keeps the previous content visible while preparing new content, preventing layout shifts. This works because Fiber can keep the old tree visible while creating the new tree.

**Q40: How would you implement a priority queue for custom React scheduling?**
A:
1. **Define lanes**: Create custom lane constants for your priorities
2. **Schedule updates**: Use `React.startTransition` with custom priorities
3. **Lane merging**: Implement lane intersection for priority inheritance
4. **Scheduler integration**: Use `scheduler` package with custom priorities

### Follow-ups (5-10)

**Q41: What is the relationship between Fiber and React 18's concurrent rendering?**
A: Fiber is the foundation that enables concurrent rendering. React 18 builds on Fiber to add:
- Time-sliced rendering
- Priority-based scheduling
- Transitions
- Deferred values
- Selective hydration

**Q42: How would you explain Fiber to a non-technical stakeholder?**
A: "Fiber is like a smart scheduling system for React. Instead of doing all the work at once and making the app freeze, it breaks the work into small chunks and does them when there's time. This keeps the app responsive even when doing heavy work."

**Q43: What are the limitations of the current Fiber implementation?**
A:
- Memory overhead (2x compared to stack reconciler)
- Complexity (harder to debug)
- Some concurrent features are still experimental
- Not all updates can be deferred (DOM measurements need sync updates)

**Q44: How does Fiber handle the `shouldComponentUpdate` optimization?**
A: In class components, `shouldComponentUpdate` is called during the begin phase. If it returns `false`, React skips the entire subtree. In function components, `React.memo` provides similar functionality by comparing props.

**Q45: What is the `StrictMode` double-rendering and why does it exist?**
A: StrictMode intentionally double-renders components in development to detect side effects. This works because Fiber's render phase is idempotent (no side effects). Double-rendering catches bugs like missing cleanup functions or impure render functions.

**Q46: How does Fiber interact with React DevTools Profiler?**
A: The Profiler hooks into Fiber's `onRender` callback. During the commit phase, React calls `onRender` for each component, passing render timing information. The Profiler aggregates this data to show which components are slow.

**Q47: What is the future of Fiber?**
A: React is exploring:
- Better time-slicing algorithms
- Offscreen rendering (now called Activity)
- Automatic memoization via React Compiler
- Improved Suspense integration
- Better error handling during concurrent rendering

**Q48: How would you optimize Fiber for a specific use case (e.g., games)?**
A: For games:
1. **Direct DOM manipulation**: Use refs for high-frequency updates
2. **requestAnimationFrame**: Bypass React's scheduler for animations
3. **Minimal state**: Store game state outside React state
4. **Web Workers**: Offload heavy computation
5. **Custom reconciler**: If needed, create a game-specific reconciler

**Q49: How does Fiber handle the interaction between `useEffect` and concurrent rendering?**
A: `useEffect` runs after the commit phase, during browser idle time. During concurrent rendering:
1. Effects are collected during render phase
2. Previous effects are cleaned up during commit
3. New effects are scheduled via `requestIdleCallback` or `MessageChannel`
4. React can batch multiple effect runs

**Q50: What is the `NoCommit` flag and how does it affect Fiber?**
A: `NoCommit` is a flag that prevents a fiber's subtree from being committed. This is used during concurrent rendering to keep the old UI visible while preparing the new UI. When the transition completes, React commits the new tree atomically.

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

## References & Learn More

- [React Fiber Architecture](https://github.com/acdlite/react-fiber-architecture)
- [A Complete Guide to React Fiber](https://blog.bitsrc.io/react-fiber-an-in-depth-explanation-of-changes-in-react-16-fc63e88e1d8e)
- [React 16 Fiber Architecture](https://medium.com/react-in-depth/the-fiber-reconciler-changed-in-react-16-90074b96e017)
