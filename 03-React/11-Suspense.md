---
section: React
category: Frontend
tags: [concept]
---

# Suspense

## TL;DR

Suspense lets components 'wait' for something before rendering, showing a fallback. Originally for `React.lazy` (code splitting), now extended to data fetching with React Query, Relay, and the experimental `use(promise)` API. `<Suspense boundary>` catches the wait and shows fallback.

## Why It Matters

Senior engineers use Suspense to: split code with `React.lazy` + fallback UI, integrate with data-fetching libraries (React Query's `suspense: true`), and orchestrate loading states. In React 19, `use(promise)` is the new way to read resources, and Suspense boundaries can be nested for granular loading.

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

---

## See Also
- [Animation](../30-Animation/)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: Suspense](https://react.dev/reference/react/Suspense)
- [React Docs: Lazy Loading](https://react.dev/reference/react/lazy)
- [React Suspense Guide](https://www.freecodecamp.org/news/react-suspense-and-error-boundaries/)
