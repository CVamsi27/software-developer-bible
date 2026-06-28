# Suspense

## Definition

React Suspense is a feature that lets you "suspend" rendering of a component tree until some condition is met (like data loading or code loading). It provides a declarative way to handle loading states in React applications. Suspense works by catching a "promise" thrown by a child component and showing a fallback UI until the promise resolves.

Suspense is the foundation for several React features:

1. **Code Splitting**: Lazy loading components with `React.lazy`

2. **Data Fetching**: Integration with frameworks like Next.js, Relay

3. **Server Components**: Streaming server-rendered HTML

4. **Selective Hydration**: Hydrating urgent components first

## Why Do We Need It?

### The Problem

Before Suspense, handling loading states was manual and repetitive:

```typescript
// ❌ BEFORE: Manual loading states
const UserProfile = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    fetchUser(userId)
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <Spinner />;
  if (error) return <Error message={error} />;
  if (!user) return null;

  return <div>{user.name}</div>;
};

```

### The Solution

Suspense handles loading states declaratively:

```typescript
// ✅ AFTER: Declarative loading with Suspense
const UserProfile = ({ userId }: { userId: string }) => {
  const user = use(fetchUser(userId)); // Suspense-integrated fetch
  return <div>{user.name}</div>;
};

// Parent handles loading state
const App = () => (
  <Suspense fallback={<Spinner />}>
    <UserProfile userId="1" />
  </Suspense>
);

```

## How It Works

### Suspense Mechanism

```text
Suspense Mechanism:
═══════════════════════════════════════════════════════════════

Normal Rendering:
┌─────────────────────────────────────────────────────────────┐
│ Parent renders                                              │
│ └── Child renders                                           │
│     └── Grandchild renders                                  │
│         └── Returns JSX                                     │
└─────────────────────────────────────────────────────────────┘

Suspense Rendering:
┌─────────────────────────────────────────────────────────────┐
│ Parent renders                                              │
│ └── Child renders                                           │
│     └── Grandchild THROWS PROMISE                          │
│         └── React CATCHES promise                           │
│             └── Shows FALLBACK UI                           │
│                 └── When promise RESOLVES:                  │
│                     └── Renders child component              │
└─────────────────────────────────────────────────────────────┘

```

### Code Splitting with React.lazy

```text
Code Splitting:
═══════════════════════════════════════════════════════════════

Without Code Splitting:
┌─────────────────────────────────────────────────────────────┐
│ Main Bundle:                                                │
│ ├── App.js                                                  │
│ ├── Header.js                                               │
│ ├── HomePage.js                                             │
│ ├── Dashboard.js (100KB)                                   │
│ ├── Settings.js (50KB)                                     │
│ └── AdminPanel.js (200KB)                                  │
│                                                             │
│ Total: 351KB loaded on initial page load                    │
│ Even if user only visits HomePage!                          │
└─────────────────────────────────────────────────────────────┘

With Code Splitting:
┌─────────────────────────────────────────────────────────────┐
│ Main Bundle:                                                │
│ ├── App.js                                                  │
│ ├── Header.js                                               │
│ └── HomePage.js                                             │
│                                                             │
│ Lazy Bundles (loaded on demand):                            │
│ ├── Dashboard.chunk.js (100KB)                             │
│ ├── Settings.chunk.js (50KB)                               │
│ └── AdminPanel.chunk.js (200KB)                            │
│                                                             │
│ Initial load: 51KB                                          │
│ Dashboard loads only when user navigates to /dashboard      │
└─────────────────────────────────────────────────────────────┘

```

### Suspense Boundaries

```text
Suspense Boundaries:
═══════════════════════════════════════════════════════════════

Multiple Boundaries:
┌─────────────────────────────────────────────────────────────┐
│ <App>                                                       │
│ ├── <Header /> (no Suspense needed - instant)              │
│ │                                                          │
│ ├── <Suspense fallback={<PageSpinner />}>                  │
│ │   └── <MainContent /> (loads data)                       │
│ │       ├── <Article />                                     │
│ │       └── <Comments />                                    │
│ │                                                          │
│ └── <Suspense fallback={<SidebarSpinner />}>               │
│     └── <Sidebar /> (loads data)                           │
│         ├── <RelatedLinks />                                │
│         └── <Ads />                                        │
│ </App>                                                     │
│                                                             │
│ Benefit: Each section loads independently!                  │
│ MainContent loading doesn't block Sidebar                  │
└─────────────────────────────────────────────────────────────┘

```

### Error Handling with Error Boundaries

```text
Error Handling:
═══════════════════════════════════════════════════════════════

Suspense + Error Boundary:
┌─────────────────────────────────────────────────────────────┐
│ <ErrorBoundary fallback={<ErrorUI />}>                      │
│   <Suspense fallback={<Spinner />}>                        │
│     <AsyncComponent />                                      │
│   </Suspense>                                              │
│ </ErrorBoundary>                                           │
│                                                             │
│ Loading: Shows Spinner                                      │
│ Success: Shows AsyncComponent                               │
│ Error: Shows ErrorUI                                        │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic React.lazy

```typescript
import React, { Suspense, lazy } from 'react';

// Lazy load components
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
const AdminPanel = lazy(() => import('./AdminPanel'));

const App = () => {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <div>
      <nav>
        <button onClick={() => setCurrentPage('home')}>Home</button>
        <button onClick={() => setCurrentPage('dashboard')}>Dashboard</button>
        <button onClick={() => setCurrentPage('settings')}>Settings</button>
        <button onClick={() => setCurrentPage('admin')}>Admin</button>
      </nav>

      <Suspense fallback={<div>Loading...</div>}>
        {currentPage === 'home' && <HomePage />}
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'settings' && <Settings />}
        {currentPage === 'admin' && <AdminPanel />}
      </Suspense>
    </div>
  );
};

```

### Nested Suspense Boundaries

```typescript
const App = () => (
  <div className="app">
    <Header /> {/* No Suspense - loads instantly */}

    <main>
      <Suspense fallback={<MainSpinner />}>
        <Content /> {/* Loads data */}
      </Suspense>
    </main>

    <aside>
      <Suspense fallback={<SidebarSpinner />}>
        <Sidebar /> {/* Loads data independently */}
      </Suspense>
    </aside>
  </div>
);

```

### Suspense with React.lazy and Error Boundary

```typescript
import React, { Suspense, lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

const App = () => (
  <ErrorBoundary fallback={<div>Something went wrong</div>}>
    <Suspense fallback={<div>Loading component...</div>}>
      <HeavyComponent />
    </Suspense>
  </ErrorBoundary>
);

```

### Suspense for Data Fetching (with React 18+)

```typescript
// Using Suspense for data fetching (React 18+)
const UserProfile = ({ userId }: { userId: string }) => {
  // This component suspends while data is loading
  const user = use(fetchUser(userId));

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
};

// Parent component
const App = () => (
  <Suspense fallback={<div>Loading user...</div>}>
    <UserProfile userId="1" />
  </Suspense>
);

```

### Multiple Lazy Components

```typescript
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Contact = lazy(() => import('./pages/Contact'));

const App = () => {
  const [route, setRoute] = useState('/');

  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </nav>

      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </Suspense>
    </div>
  );
};

```

## Real-World Use Cases

### 1. Route-Based Code Splitting

```typescript
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const Profile = lazy(() => import('./pages/Profile'));

const Loading = () => (
  <div className="page-loader">
    <Spinner />
    <p>Loading page...</p>
  </div>
);

const App = () => (
  <BrowserRouter>
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Suspense>
  </BrowserRouter>
);

```

### 2. Heavy Component Lazy Loading

```typescript
const RichTextEditor = lazy(() => import('./RichTextEditor'));
const Chart = lazy(() => import('./Chart'));
const VideoPlayer = lazy(() => import('./VideoPlayer'));

const DocumentEditor = () => {
  const [showEditor, setShowEditor] = useState(false);
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowEditor(true)}>Open Editor</button>
      <button onClick={() => setShowChart(true)}>Show Chart</button>

      {showEditor && (
        <Suspense fallback={<div>Loading editor...</div>}>
          <RichTextEditor />
        </Suspense>
      )}

      {showChart && (
        <Suspense fallback={<div>Loading chart...</div>}>
          <Chart data={chartData} />
        </Suspense>
      )}
    </div>
  );
};

```

### 3. Dashboard with Independent Sections

```typescript
const SalesChart = lazy(() => import('./SalesChart'));
const RecentOrders = lazy(() => import('./RecentOrders'));
const CustomerList = lazy(() => import('./CustomerList'));

const Dashboard = () => (
  <div className="dashboard">
    <h1>Dashboard</h1>

    <div className="dashboard-grid">
      <div className="chart-section">
        <Suspense fallback={<ChartSkeleton />}>
          <SalesChart />
        </Suspense>
      </div>

      <div className="orders-section">
        <Suspense fallback={<OrdersSkeleton />}>
          <RecentOrders />
        </Suspense>
      </div>

      <div className="customers-section">
        <Suspense fallback={<CustomersSkeleton />}>
          <CustomerList />
        </Suspense>
      </div>
    </div>
  </div>
);

```

### 4. Modal with Lazy Content

```typescript
const HeavyModalContent = lazy(() => import('./HeavyModalContent'));

const Modal = ({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <button className="close-btn" onClick={onClose}>×</button>
        <Suspense fallback={<ModalSpinner />}>
          <HeavyModalContent />
        </Suspense>
      </div>
    </div>
  );
};

```

## Common Mistakes

### 1. No Suspense Boundary

```typescript
// ❌ BAD: Lazy component without Suspense
const App = () => {
  const Dashboard = lazy(() => import('./Dashboard'));
  return <Dashboard />; // Error: No Suspense boundary!
};

// ✅ GOOD: Wrap with Suspense
const App = () => {
  const Dashboard = lazy(() => import('./Dashboard'));
  return (
    <Suspense fallback={<Spinner />}>
      <Dashboard />
    </Suspense>
  );
};

```

### 2. Too Broad Suspense Boundaries

```typescript
// ❌ BAD: One Suspense for entire app
const App = () => (
  <Suspense fallback={<FullPageSpinner />}>
    <Header />
    <Content />
    <Sidebar />
  </Suspense>
);
// Content loading blocks Header and Sidebar

// ✅ GOOD: Specific Suspense boundaries
const App = () => (
  <>
    <Header />
    <Suspense fallback={<ContentSpinner />}>
      <Content />
    </Suspense>
    <Suspense fallback={<SidebarSpinner />}>
      <Sidebar />
    </Suspense>
  </>
);

```

### 3. Not Handling Errors

```typescript
// ❌ BAD: No error handling
const App = () => (
  <Suspense fallback={<Spinner />}>
    <LazyComponent />
  </Suspense>
);
// If LazyComponent fails to load, error is not caught

// ✅ GOOD: Error boundary
const App = () => (
  <ErrorBoundary fallback={<ErrorMessage />}>
    <Suspense fallback={<Spinner />}>
      <LazyComponent />
    </Suspense>
  </ErrorBoundary>
);

```

### 4. Lazy Loading Too Much

```typescript
// ❌ BAD: Lazy loading small components
const Button = lazy(() => import('./Button')); // 1KB - unnecessary!
const Icon = lazy(() => import('./Icon')); // 0.5KB - unnecessary!

// ✅ GOOD: Lazy load large components
const RichTextEditor = lazy(() => import('./RichTextEditor')); // 100KB - worth it!
const Chart = lazy(() => import('./Chart')); // 50KB - worth it!

```

## Best Practices

1. **Always wrap lazy components with Suspense**: Without it, React throws an error.

2. **Use specific Suspense boundaries**: Don't wrap entire app in one Suspense.

3. **Combine with Error Boundaries**: Handle both loading and error states.

4. **Lazy load large components**: Don't lazy load small, frequently used components.

5. **Use route-based code splitting**: Lazy load entire pages/routes.

6. **Provide meaningful fallbacks**: Show loading indicators, not blank screens.

7. **Preload when possible**: Start loading before user navigates.

## Performance Considerations

### Code Splitting Impact

| Metric | Without Splitting | With Splitting |
|--------|-------------------|----------------|
| Initial bundle | 500KB | 100KB |
| Time to interactive | 2s | 0.5s |
| Subsequent loads | Instant | 100-200ms |
| Network requests | 1 | Multiple |

### When to Lazy Load

| Component | Lazy Load? | Reason |
|-----------|------------|--------|
| Routes | ✅ | User may not visit all pages |
| Heavy components | ✅ | Large bundle size |
| Modals | ✅ | Not always visible |
| Small utilities | ❌ | Overhead not worth it |
| Critical components | ❌ | Need immediately |

## Interview Questions

### Beginner (5-10)

**Q1: What is React Suspense?**
A: React Suspense is a feature that lets you "suspend" rendering of a component tree until some condition is met (like data loading). It shows a fallback UI while waiting.

**Q2: What is React.lazy?**
A: `React.lazy` is a function that lets you lazily load components. It imports a component dynamically and shows a fallback while loading.

**Q3: How do you use React.lazy?**
A: `const MyComponent = lazy(() => import('./MyComponent'));` Then wrap it with `<Suspense fallback={<Spinner />}>`.

**Q4: What is a Suspense boundary?**
A: A Suspense boundary is a `<Suspense>` component that catches promises from child components and shows a fallback UI until the promise resolves.

**Q5: Can you have multiple Suspense boundaries?**
A: Yes. Multiple boundaries allow different parts of the UI to load independently.

**Q6: What happens without a Suspense boundary?**
A: React throws an error if a lazy component is rendered without a Suspense boundary.

**Q7: What is the fallback prop?**
A: The `fallback` prop specifies the UI to show while the Suspense boundary is waiting (loading).

**Q8: Can Suspense handle errors?**
A: No. Use Error Boundaries to handle errors. Suspense only handles loading states.

**Q9: What is code splitting?**
A: Code splitting is the practice of splitting your bundle into smaller chunks that are loaded on demand.

**Q10: When should you use Suspense?**
A: Use Suspense for:

- Lazy loading components
- Data fetching (with frameworks)
- Any asynchronous operation that needs a loading state

### Intermediate (5-10)

**Q11: How does Suspense work internally?**
A: When a component suspends, it throws a Promise. React catches the Promise at the nearest Suspense boundary, shows the fallback, and resumes rendering when the Promise resolves.

**Q12: How do you preload lazy components?**
A: Call the lazy function before rendering:

```typescript
const Dashboard = lazy(() => import('./Dashboard'));
// Preload
Dashboard.preload();

```

**Q13: Can you use Suspense with data fetching?**
A: Yes, but you need a framework or library that supports it (like React 18's `use` hook, Next.js, or Relay).

**Q14: How do you handle errors in lazy components?**
A: Wrap Suspense with an Error Boundary:

```typescript
<ErrorBoundary fallback={<Error />}>
  <Suspense fallback={<Spinner />}>
    <LazyComponent />
  </Suspense>
</ErrorBoundary>

```

**Q15: What is the difference between Suspense and loading states?**
A: Suspense is declarative — you wrap components. Loading states are imperative — you manage them manually with state.

**Q16: How do you test Suspense boundaries?**
A: Use `waitFor` in tests:

```typescript
render(<Component />);
await waitFor(() => {
  expect(screen.getByText('Content')).toBeInTheDocument();
});

```

**Q17: Can you nest Suspense boundaries?**
A: Yes. Nested boundaries allow granular loading states.

**Q18: What is the performance impact of Suspense?**
A: Suspense adds minimal overhead. The main benefit is code splitting, which reduces initial bundle size.

**Q19: How does Suspense interact with React Router?**
A: Wrap Routes with Suspense for route-based code splitting:

```typescript
<Suspense fallback={<Spinner />}>
  <Routes>...</Routes>
</Suspense>

```

**Q20: What are the common Suspense patterns?**
A:

- Route-based code splitting
- Heavy component lazy loading
- Modal content lazy loading
- Dashboard section loading

### Senior (10-15)

**Q21: Explain the complete Suspense lifecycle.**
A:

1. Component calls `lazy()` or throws a Promise

2. React catches the Promise at the nearest Suspense boundary

3. Fallback UI is shown

4. Promise resolves

5. React retries rendering

6. Component renders successfully

**Q22: How does Suspense interact with concurrent rendering?**
A: Concurrent rendering can pause Suspense boundaries. React keeps the old UI visible while preparing the new one. Transitions can defer Suspense updates.

**Q23: What is the relationship between Suspense and Server Components?**
A: Server Components can suspend during server rendering. React streams HTML as components resolve. Client hydration respects Suspense boundaries.

**Q24: How does Suspense handle the "shell" pattern?**
A: The shell pattern keeps the app shell visible while content loads:

```typescript
<Layout>
  <Suspense fallback={<ContentSpinner />}>
    <Content />
  </Suspense>
</Layout>

```

**Q25: What is the difference between Suspense and useEffect?**
A: Suspense is declarative and handles loading states. `useEffect` is imperative and handles side effects. They serve different purposes.

**Q26: How do you optimize Suspense performance?**
A:

1. Use specific Suspense boundaries

2. Preload lazy components

3. Combine with React.memo

4. Use SuspenseList for ordered loading

**Q27: What is SuspenseList?**
A: `SuspenseList` coordinates the loading of multiple Suspense boundaries:

```typescript
<SuspenseList revealOrder="forwards">
  <Suspense fallback={<Spinner1 />}>...</Suspense>
  <Suspense fallback={<Spinner2 />}>...</Suspense>
</SuspenseList>

```

**Q28: How does Suspense handle the "fallback cascade" problem?**
A: Fallback cascade occurs when nested Suspense boundaries all show spinners. Prevent by using specific boundaries and meaningful fallbacks.

**Q29: What is the relationship between Suspense and React DevTools?**
A: React DevTools shows Suspense boundaries and their states (suspended, resolved). It helps debug loading issues.

**Q30: How do you handle Suspense in testing?**
A: Use `act` and `waitFor`:

```typescript
test('loads component', async () => {
  render(<SuspenseComponent />);
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});

```

### FAANG-style (5-10)

**Q31: Design a Suspense-based architecture for a large app.**
A:

1. **Route-based splitting**: Lazy load routes

2. **Component splitting**: Lazy load heavy components

3. **Error boundaries**: Handle loading and errors

4. **Preloading**: Start loading before navigation

5. **SuspenseList**: Coordinate multiple loads

**Q32: How would you debug a Suspense performance issue?**
A:

1. React DevTools: Check Suspense states

2. Network tab: Monitor chunk loading

3. Chrome DevTools: Record interactions

4. Profiler: Measure render times

5. Bundle analyzer: Check chunk sizes

**Q33: Analyze the memory implications of Suspense.**
A:

- Lazy components: Loaded and cached in memory
- Multiple boundaries: Each has state
- Memory overhead: Minimal compared to benefits
- Cleanup: Components unmount when not needed

**Q34: How would you implement a Suspense-based loading system?**
A:

```typescript
const useSuspenseData = <T>(fetcher: () => Promise<T>) => {
  const [data, setData] = useState<T | null>(null);
  const [promise, setPromise] = useState<Promise<T> | null>(null);

  useEffect(() => {
    const p = fetcher();
    setPromise(p);
    p.then(setData);
  }, [fetcher]);

  if (promise && !data) {
    throw promise; // Suspend!
  }

  return data;
};

```

**Q35: Design a Suspense-based error handling system.**
A:

```typescript
const SuspenseErrorBoundary = ({ children, fallback, errorFallback }) => (
  <ErrorBoundary fallback={errorFallback}>
    <Suspense fallback={fallback}>
      {children}
    </Suspense>
  </ErrorBoundary>
);

```

**Q36: How does Suspense interact with React Server Components?**
A: Server Components can suspend during server rendering. React streams HTML as components resolve. Client hydration respects Suspense boundaries.

**Q37: Analyze the performance characteristics of Suspense.**
A:

| Metric | Without Suspense | With Suspense |
|--------|------------------|---------------|
| Initial bundle | 500KB | 100KB |
| Time to interactive | 2s | 0.5s |
| Subsequent loads | Instant | 100-200ms |
| Memory usage | Lower | Higher |

**Q38: How would you implement a Suspense-based image loading system?**
A:

```typescript
const LazyImage = ({ src, alt }: { src: string; alt: string }) => {
  const [loaded, setLoaded] = useState(false);

  return (
    <Suspense fallback={<ImagePlaceholder />}>
      <img
        src={src}
        alt={alt}
        onLoad={() => setLoaded(true)}
        style={{ opacity: loaded ? 1 : 0 }}
      />
    </Suspense>
  );
};

```

**Q39: How does Suspense handle the "infinite loading" problem?**
A: Infinite loading occurs when Suspense never resolves. Prevention:

- Set timeouts for loading states
- Provide retry mechanisms
- Show error states after timeout

**Q40: Design a Suspense-based virtualization system.**
A:

```typescript
const VirtualizedList = ({ items }: { items: Item[] }) => {
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 10 });

  return (
    <div onScroll={handleScroll}>
      {items.slice(visibleRange.start, visibleRange.end).map(item => (
        <Suspense key={item.id} fallback={<ListItemSkeleton />}>
          <ListItem item={item} />
        </Suspense>
      ))}
    </div>
  );
};

```

### Follow-ups (5-10)

**Q41: How would you explain Suspense to a junior developer?**
A: "Suspense is like a 'please wait' screen. When a component needs to load something (like code or data), Suspense shows a loading spinner. When it's done, it shows the actual content."

**Q42: What are the edge cases in Suspense?**
A:

- Missing Suspense boundary
- Fallback cascade (nested spinners)
- Infinite loading states
- Error handling gaps
- Preloading failures

**Q43: How does Suspense handle the "race condition" problem?**
A: Suspense handles race conditions by catching the latest promise. Previous promises are ignored when new ones are thrown.

**Q44: What is the relationship between Suspense and React DevTools?**
A: React DevTools shows Suspense boundaries and their states. It helps debug loading issues and performance problems.

**Q45: How does Suspense interact with React StrictMode?**
A: StrictMode double-renders in development. Suspense boundaries work normally — they show fallback during loading.

**Q46: What is the future of Suspense in React?**
A: React is exploring:

- Better data fetching integration
- Improved concurrent features
- Better error handling
- Streaming server rendering

**Q47: How would you implement Suspense for a form?**
A:

```typescript
const LazyForm = lazy(() => import('./LazyForm'));

const FormContainer = () => (
  <Suspense fallback={<FormSkeleton />}>
    <LazyForm />
  </Suspense>
);

```

**Q48: How does Suspense handle the "preloading" pattern?**
A: Preloading starts loading before navigation:

```typescript
const Dashboard = lazy(() => import('./Dashboard'));

const NavLink = () => (
  <Link
    to="/dashboard"
    onMouseEnter={() => Dashboard.preload()}
  >
    Dashboard
  </Link>
);

```

**Q49: What is the relationship between Suspense and React.memo?**
A: `React.memo` prevents re-renders. Suspense handles loading states. They work together — memoized components can still suspend.

**Q50: How would you implement Suspense for a chat application?**
A:

```typescript
const Chat = () => (
  <div>
    <Suspense fallback={<MessagesSkeleton />}>
      <MessageList />
    </Suspense>
    <Suspense fallback={<InputSkeleton />}>
      <MessageInput />
    </Suspense>
  </div>
);

```

## Summary

React Suspense is a powerful feature for handling loading states declaratively. It works by catching promises thrown by child components and showing fallback UI. Combined with `React.lazy`, it enables code splitting for better performance. Suspense is the foundation for modern React features like data fetching and server components.

## Cheat Sheet

```text
Suspense Key Points:
├── What: Declarative loading states
├── Mechanism: Catches thrown promises, shows fallback
├── React.lazy: Lazy load components
├── Suspense boundaries: Independent loading sections
├── Error boundaries: Handle loading and errors
├── Code splitting: Reduce initial bundle size

How to Use:
├── Lazy: const C = lazy(() => import('./C'))
├── Boundary: <Suspense fallback={<Spinner />}>
├── Error: <ErrorBoundary><Suspense>...</Suspense></ErrorBoundary>
└── Multiple: Use specific boundaries for sections

Common Patterns:
├── Route-based splitting: Lazy load routes
├── Heavy components: Lazy load large components
├── Modal content: Lazy load modal content
├── Dashboard sections: Independent loading
└── Preloading: Start loading before navigation

Common Mistakes:
├── No Suspense boundary around lazy components
├── Too broad Suspense (entire app)
├── Not handling errors with Error Boundaries
├── Lazy loading small components
└── Not providing meaningful fallbacks

Best Practices:
├── Always wrap lazy components with Suspense
├── Use specific Suspense boundaries
├── Combine with Error Boundaries
├── Lazy load large components only
├── Provide meaningful fallbacks
├── Preload when possible
└── Test loading states

Performance:
├── Reduces initial bundle size
├── Improves time to interactive
├── Subsequent loads are fast
└── Memory overhead is minimal

Relationships:
├── Suspense + React.lazy = Code splitting
├── Suspense + Error Boundaries = Loading + error handling
├── Suspense + React Router = Route-based splitting
└── Suspense + React.memo = Memoized loading states

```

## References & Learn More

- [React Docs: Suspense](https://react.dev/reference/react/Suspense)
- [React Docs: Lazy Loading](https://react.dev/reference/react/lazy)
- [React Suspense Guide](https://www.freecodecamp.org/news/suspense-in-react/)
