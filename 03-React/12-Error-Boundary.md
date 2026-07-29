# Error Boundary

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

## Definition

Error Boundaries are React components that catch JavaScript errors anywhere in their child component tree, log those errors, and display a fallback UI instead of crashing the entire application. They work like a `try-catch` block for React components.

Error Boundaries must be **class components** with either `componentDidCatch` or `getDerivedStateFromError` methods. They catch errors during:

1. Rendering

2. Lifecycle methods

3. Constructors of child components

They do **not** catch errors in:

1. Event handlers

2. Asynchronous code (setTimeout, promises)

3. Server-side rendering

4. Errors in the error boundary itself

## Why Do We Need It?

### The Problem

Without Error Boundaries, a single error in any component crashes the entire app:

```text
Without Error Boundaries:
═══════════════════════════════════════════════════════════════

App
├── Header (working)
├── Sidebar (working)
└── Content
    └── Article
        └── Comment
            └── ❌ ERROR in Comment component!

Result: ENTIRE APP CRASHES!
White screen of death for the user

```

### The Solution

Error Boundaries catch errors and show fallback UI:

```text
With Error Boundaries:
═══════════════════════════════════════════════════════════════

App
├── Header (working)
├── Sidebar (working)
└── <ErrorBoundary fallback={<ErrorUI />}>
    └── Content
        └── Article
            └── Comment
                └── ❌ ERROR in Comment component!

Result: Comment shows ErrorUI
Rest of the app continues working!

```

## How It Works

### Error Boundary Lifecycle

```text
Error Boundary Lifecycle:
═══════════════════════════════════════════════════════════════

Normal Rendering:
┌─────────────────────────────────────────────────────────────┐
│ Parent renders                                              │
│ └── ErrorBoundary renders                                   │
│     └── Child renders                                       │
│         └── Returns JSX                                     │
└─────────────────────────────────────────────────────────────┘

Error Occurs:
┌─────────────────────────────────────────────────────────────┐
│ Parent renders                                              │
│ └── ErrorBoundary renders                                   │
│     └── Child THROWS ERROR                                  │
│         └── React CATCHES error                             │
│             └── Calls getDerivedStateFromError              │
│                 └── Updates state with error                │
│                     └── Renders fallback UI                 │
└─────────────────────────────────────────────────────────────┘

Error Reporting:
┌─────────────────────────────────────────────────────────────┐
│ componentDidCatch(error, errorInfo)                        │
│ ├── error: The error that was thrown                        │
│ └── errorInfo: Component stack trace                        │
│     └── Log to error reporting service                      │
│     └── Update state to show fallback                       │
└─────────────────────────────────────────────────────────────┘

```

### Error Boundary Methods

```text
Error Boundary Methods:
═══════════════════════════════════════════════════════════════

getDerivedStateFromError (Static):
┌─────────────────────────────────────────────────────────────┐
│ Called during render phase when error occurs                │
│ Use to update state so next render shows fallback           │
│                                                             │
│ static getDerivedStateFromError(error: Error) {             │
│   return { hasError: true, error };                         │
│ }                                                           │
│                                                             │
│ ⚠️ Must be pure — no side effects                           │
└─────────────────────────────────────────────────────────────┘

componentDidCatch (Instance):
┌─────────────────────────────────────────────────────────────┐
│ Called during commit phase when error occurs                │
│ Use for error logging and reporting                         │
│                                                             │
│ componentDidCatch(error: Error, errorInfo: ErrorInfo) {     │
│   logErrorToService(error, errorInfo.componentStack);       │
│ }                                                           │
│                                                             │
│ ✅ Can have side effects (logging, reporting)               │
└─────────────────────────────────────────────────────────────┘

```

### Error Boundary Diagram

```text
Error Boundary Flow:
═══════════════════════════════════════════════════════════════

                    ┌─────────────────┐
                    │   App Component │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Header (OK)    │
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Content        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ <ErrorBoundary> │
                    │ hasError: false │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Article (OK)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  ❌ Comment     │
                    │  THROWS ERROR   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  React CATCHES  │
                    │  Calls          │
                    │  getDerivedState│
                    │  FromError      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  <ErrorBoundary>│
                    │  hasError: true │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  FALLBACK UI    │
                    │  "Something     │
                    │   went wrong"   │
                    └─────────────────┘

```

## Code Examples

### Basic Error Boundary

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error);
    console.error('Component stack:', errorInfo.componentStack);
    // Log to error reporting service
    logErrorToService(error, errorInfo.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

```

### Error Boundary with Retry

```typescript
class ErrorBoundaryWithRetry extends Component<
  { children: ReactNode; fallback?: (error: Error, retry: () => void) => ReactNode },
  State
> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    logErrorToService(error, errorInfo.componentStack);
  }

  retry = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        return this.props.fallback(this.state.error, this.retry);
      }
      return (
        <div>
          <h2>Error</h2>
          <p>{this.state.error.message}</p>
          <button onClick={this.retry}>Retry</button>
        </div>
      );
    }
    return this.props.children;
  }
}

```

### Nested Error Boundaries

```typescript
const App = () => (
  <ErrorBoundary fallback={<AppError />}>
    <Header />
    <main>
      <ErrorBoundary fallback={<ContentError />}>
        <Content />
      </ErrorBoundary>
    </main>
    <aside>
      <ErrorBoundary fallback={<SidebarError />}>
        <Sidebar />
      </ErrorBoundary>
    </aside>
  </ErrorBoundary>
);

```

### Error Boundary with Logging

```typescript
class ErrorBoundaryWithLogging extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to multiple services
    console.error('Error:', error);
    console.error('Component stack:', errorInfo.componentStack);

    // Send to error reporting service
    Sentry.captureException(error, {
      extra: { componentStack: errorInfo.componentStack },
    });

    // Send to analytics
    analytics.track('Error Occurred', {
      errorMessage: error.message,
      componentStack: errorInfo.componentStack,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong</h2>
          <p>Please try again later</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

```

### Function Component with Error Boundary

```typescript
const BuggyComponent = () => {
  const [count, setCount] = useState(0);

  if (count === 3) {
    throw new Error('I crashed at count 3!');
  }

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
    </div>
  );
};

const App = () => (
  <ErrorBoundary fallback={<div>Error in counter!</div>}>
    <BuggyComponent />
  </ErrorBoundary>
);

```

## Real-World Use Cases

### 1. Route-Level Error Boundaries

```typescript
const PageError = ({ error, reset }: { error: Error; reset: () => void }) => (
  <div className="error-page">
    <h1>Page Error</h1>
    <p>{error.message}</p>
    <button onClick={reset}>Try Again</button>
    <button onClick={() => window.location.href = '/'}>
      Go Home
    </button>
  </div>
);

const Dashboard = () => (
  <ErrorBoundary fallback={(error, reset) => <PageError error={error} reset={reset} />}>
    <DashboardContent />
  </ErrorBoundary>
);

```

### 2. Widget-Level Error Boundaries

```typescript
const WidgetError = ({ widgetName, error }: { widgetName: string; error: Error }) => (
  <div className="widget-error">
    <h3>{widgetName} Failed</h3>
    <p>{error.message}</p>
    <button onClick={() => window.location.reload()}>Reload Widget</button>
  </div>
);

const Dashboard = () => (
  <div className="dashboard">
    <ErrorBoundary fallback={(error) => <WidgetError widgetName="Sales" error={error} />}>
      <SalesWidget />
    </ErrorBoundary>

    <ErrorBoundary fallback={(error) => <WidgetError widgetName="Users" error={error} />}>
      <UsersWidget />
    </ErrorBoundary>

    <ErrorBoundary fallback={(error) => <WidgetError widgetName="Revenue" error={error} />}>
      <RevenueWidget />
    </ErrorBoundary>
  </div>
);

```

### 3. Form Error Handling

```typescript
const FormError = ({ error, onRetry }: { error: Error; onRetry: () => void }) => (
  <div className="form-error">
    <h3>Form Error</h3>
    <p>{error.message}</p>
    <button onClick={onRetry}>Retry</button>
  </div>
);

const ContactForm = () => (
  <ErrorBoundary fallback={(error, reset) => <FormError error={error} onRetry={reset} />}>
    <Form onSubmit={handleSubmit} />
  </ErrorBoundary>
);

```

### 4. Image Gallery Error Handling

```typescript
const ImageError = ({ src, error }: { src: string; error: Error }) => (
  <div className="image-error">
    <p>Failed to load image</p>
    <img src="/placeholder.png" alt="Placeholder" />
  </div>
);

const GalleryImage = ({ src, alt }: { src: string; alt: string }) => (
  <ErrorBoundary fallback={(error) => <ImageError src={src} error={error} />}>
    <img src={src} alt={alt} />
  </ErrorBoundary>
);

```

## Common Mistakes

### 1. Not Using Error Boundaries

```typescript
// ❌ BAD: No error handling
const App = () => (
  <div>
    <Header />
    <Content /> {/* If Content crashes, entire app crashes */}
    <Sidebar />
  </div>
);

// ✅ GOOD: Error boundaries around critical sections
const App = () => (
  <div>
    <Header />
    <ErrorBoundary fallback={<ContentError />}>
      <Content />
    </ErrorBoundary>
    <ErrorBoundary fallback={<SidebarError />}>
      <Sidebar />
    </ErrorBoundary>
  </div>
);

```

### 2. Using Error Boundaries for Event Handlers

```typescript
// ❌ BAD: Error boundaries don't catch event handler errors
class MyComponent extends Component {
  handleClick = () => {
    // Error here is NOT caught by Error Boundary
    throw new Error('Click error!');
  };

  render() {
    return <button onClick={this.handleClick}>Click</button>;
  }
}

// ✅ GOOD: Use try-catch in event handlers
class MyComponent extends Component {
  handleClick = () => {
    try {
      throw new Error('Click error!');
    } catch (error) {
      console.error('Click error:', error);
    }
  };

  render() {
    return <button onClick={this.handleClick}>Click</button>;
  }
}

```

### 3. Not Providing Recovery Mechanism

```typescript
// ❌ BAD: No way to recover
class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div>Error occurred</div>; // No way to retry!
    }
    return this.props.children;
  }
}

// ✅ GOOD: Provide recovery mechanism
class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  retry = () => {
    this.setState({ hasError: false });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <div>Error occurred</div>
          <button onClick={this.retry}>Try Again</button>
        </div>
      );
    }
    return this.props.children;
  }
}

```

### 4. Using Function Components

```typescript
// ❌ BAD: Function components can't be Error Boundaries
const ErrorBoundary = ({ children, fallback }) => {
  const [hasError, setHasError] = useState(false);

  // This won't work! Function components can't have lifecycle methods
  return hasError ? fallback : children;
};

// ✅ GOOD: Use class components
class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}

```

## Best Practices

1. **Use class components**: Error Boundaries must be class components.

2. **Place them strategically**: Around critical sections, not the entire app.

3. **Provide recovery mechanisms**: Allow users to retry or navigate away.

4. **Log errors**: Use `componentDidCatch` to report to error services.

5. **Use multiple boundaries**: Different fallbacks for different sections.

6. **Don't catch event handler errors**: Use try-catch for those.

7. **Test error states**: Verify fallback UI displays correctly.

## Performance Considerations

### Error Boundary Overhead

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| Rendering | Minimal overhead | Only runs when no error |
| Error catching | One-time cost | Only when error occurs |
| Fallback rendering | One-time cost | Only on error |
| Memory | Low | Class component overhead |

### When to Use Error Boundaries

| Scenario | Use Error Boundary? | Reason |
|----------|---------------------|--------|
| Route sections | ✅ | Isolate page errors |
| Widgets | ✅ | Isolate widget errors |
| Forms | ✅ | Isolate form errors |
| Entire app | ⚠️ | Last resort |
| Event handlers | ❌ | Use try-catch |

## Summary

Error Boundaries are React class components that catch errors in their child component tree and display fallback UI. They use `getDerivedStateFromError` for state updates and `componentDidCatch` for error logging. Error Boundaries are essential for building resilient React applications that don't crash on errors.

## Cheat Sheet
```text
Error Boundary Key Points:
├── What: Catch errors in child component tree
├── Type: Class components (must be)
├── Methods: getDerivedStateFromError, componentDidCatch
├── Catches: Render, lifecycle, constructor errors
├── Does NOT catch: Event handlers, async, SSR
├── Fallback: UI shown when error occurs

Methods:
├── getDerivedStateFromError(error):
│   ├── Static method
│   ├── Called during render phase
│   ├── Updates state for fallback
│   └── Must be pure (no side effects)
└── componentDidCatch(error, errorInfo):
    ├── Instance method
    ├── Called during commit phase
    ├── Used for logging/reporting
    └── Can have side effects

What It Catches:
├── ✅ Rendering errors
├── ✅ Lifecycle method errors
├── ✅ Constructor errors
├── ❌ Event handler errors (use try-catch)
├── ❌ Async code errors (use try-catch)
├── ❌ SSR errors
└── ❌ Errors in boundary itself

Common Patterns:
├── Route-level boundaries
├── Widget-level boundaries
├── Form-level boundaries
├── Image-level boundaries
└── Feature-level boundaries

Best Practices:
├── Use class components
├── Place strategically (not entire app)
├── Provide recovery mechanisms
├── Log errors to services
├── Use multiple boundaries
├── Don't catch event handler errors
└── Test error states

Common Mistakes:
├── Not using Error Boundaries
├── Using for event handlers
├── Not providing recovery
├── Using function components
└── Not logging errors

Performance:
├── Minimal overhead when no error
├── One-time cost on error
├── Low memory usage
└── Network cost for logging

```

---

## See Also
- [Animation](../30-Animation/)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Portals](17-Portals.md)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: Error Boundaries](https://react.dev/reference/react/Component#componentdidcatch)
- [Error Handling in React](https://www.freecodecamp.org/news/error-handling-react/)
- [React Error Boundary Guide](https://blog.logrocket.com/error-handling-react/)
