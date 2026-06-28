# Error Boundary

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

## Interview Questions

### Beginner (5-10)

**Q1: What are Error Boundaries?**
A: Error Boundaries are React components that catch JavaScript errors in their child component tree, log errors, and display fallback UI instead of crashing the app.

**Q2: Why do we need Error Boundaries?**
A: Without them, a single error in any component crashes the entire app. Error Boundaries isolate errors and show fallback UI while keeping the rest of the app working.

**Q3: What type of component is an Error Boundary?**
A: Error Boundaries must be class components with `componentDidCatch` or `getDerivedStateFromError` methods.

**Q4: What is `getDerivedStateFromError`?**
A: A static method called when a child component throws an error. It updates the component's state to show fallback UI.

**Q5: What is `componentDidCatch`?**
A: An instance method called when a child component throws an error. It's used for error logging and reporting.

**Q6: What errors do Error Boundaries catch?**
A: They catch errors in:

- Rendering
- Lifecycle methods
- Constructors of child components

**Q7: What errors do Error Boundaries NOT catch?**
A: They don't catch errors in:

- Event handlers
- Asynchronous code (setTimeout, promises)
- Server-side rendering
- Errors in the boundary itself

**Q8: Can you use Error Boundaries with function components?**
A: The Error Boundary itself must be a class component. But it can wrap function components.

**Q9: What is a fallback UI?**
A: The UI displayed when an error occurs. It replaces the crashed component tree.

**Q10: How do you test Error Boundaries?**
A: Throw an error in a child component and verify the fallback UI displays.

### Intermediate (5-10)

**Q11: Explain the complete Error Boundary lifecycle.**
A:

1. Child component throws error during render

2. React catches the error

3. Calls `getDerivedStateFromError` (render phase)

4. Updates state with error

5. Calls `componentDidCatch` (commit phase)

6. Logs error

7. Renders fallback UI

**Q12: How do you implement retry functionality?**
A: Store error in state, provide a retry function that resets state:

```typescript
retry = () => {
  this.setState({ hasError: false, error: null });
};

```

**Q13: How do you log errors to external services?**
A: Use `componentDidCatch` to send errors to services like Sentry, LogRocket, or custom endpoints.

**Q14: How do you use multiple Error Boundaries?**
A: Nest them for different sections:

```typescript
<ErrorBoundary fallback={<AppError />}>
  <Header />
  <ErrorBoundary fallback={<ContentError />}>
    <Content />
  </ErrorBoundary>
</ErrorBoundary>

```

**Q15: What is the difference between Error Boundaries and try-catch?**
A: `try-catch` is imperative and works in event handlers. Error Boundaries are declarative and work in render lifecycle.

**Q16: How do you handle errors in event handlers?**
A: Use `try-catch` blocks:

```typescript
handleClick = () => {
  try {
    // risky operation
  } catch (error) {
    console.error(error);
  }
};

```

**Q17: Can Error Boundaries catch errors in useEffect?**
A: No. `useEffect` runs after render. Errors in `useEffect` are not caught by Error Boundaries.

**Q18: How do you test Error Boundary fallback UI?**
A: Force an error in a child component and check that fallback renders.

**Q19: What is the performance impact of Error Boundaries?**
A: Minimal. They only have overhead when no error (rendering children) and when error occurs (catching and logging).

**Q20: How do you handle errors in async code?**
A: Use `try-catch` in async functions:

```typescript
useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await fetch(url);
      // handle data
    } catch (error) {
      console.error(error);
    }
  };
  fetchData();
}, []);

```

### Senior (10-15)

**Q21: Explain the complete Error Boundary architecture.**
A:

1. Error Boundary component (class)

2. Child component tree

3. Error catching mechanism (React internals)

4. State management (hasError, error)

5. Fallback rendering

6. Error reporting

**Q22: How do Error Boundaries interact with React Suspense?**
A: Error Boundaries catch errors from Suspense boundaries. They work together — Suspense handles loading, Error Boundaries handle errors.

**Q23: What is the relationship between Error Boundaries and error reporting?**
A: Error Boundaries provide the `componentDidCatch` method to log errors to external services like Sentry, LogRocket, or custom endpoints.

**Q24: How do you implement error recovery patterns?**
A:

- Retry mechanism (reset state)
- Fallback UI with navigation
- Graceful degradation
- User feedback collection

**Q25: How do Error Boundaries interact with concurrent rendering?**
A: Error Boundaries catch errors during render phase. Concurrent rendering can pause rendering, but errors are still caught at boundaries.

**Q26: What is the difference between Error Boundaries and error handling in React 18?**
A: React 18 doesn't change Error Boundary behavior. They still catch errors in render phase, lifecycle methods, and constructors.

**Q27: How do you handle errors in Server Components?**
A: Server Components have different error handling. Errors are caught during server rendering and sent to the client.

**Q28: What is the relationship between Error Boundaries and React DevTools?**
A: React DevTools shows Error Boundary state and errors. It helps debug error catching behavior.

**Q29: How do you implement error boundaries with hooks?**
A: You can't use hooks in Error Boundaries (they must be class components). But you can use hooks in child components.

**Q30: What are the common Error Boundary patterns?**
A:

- Route-level boundaries
- Widget-level boundaries
- Form-level boundaries
- Image-level boundaries
- Feature-level boundaries

### FAANG-style (5-10)

**Q31: Design an Error Boundary system for a large app.**
A:

1. **Hierarchy**: App-level → Route-level → Component-level

2. **Recovery**: Retry, navigation, fallback

3. **Logging**: Error reporting, analytics

4. **Monitoring**: Error tracking, alerts

5. **Testing**: Error state verification

**Q32: How would you debug an Error Boundary issue?**
A:

1. React DevTools: Check Error Boundary state

2. Console: Log errors

3. Error reporting: Check Sentry/LogRocket

4. Testing: Force errors in tests

5. Monitoring: Check error rates

**Q33: Analyze the performance implications of Error Boundaries.**
A:

- Rendering: Minimal overhead (only when no error)
- Error catching: One-time cost (only on error)
- Logging: Network cost (sending to services)
- Memory: Low (class component overhead)

**Q34: How would you implement a centralized error handling system?**
A:

```typescript
class GlobalErrorBoundary extends Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Centralized logging
    ErrorService.log(error, errorInfo);
    // Analytics
    Analytics.track('Error', { error: error.message });
  }

  render() {
    if (this.state.hasError) {
      return <GlobalErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}

```

**Q35: Design an Error Boundary testing strategy.**
A:

1. **Unit tests**: Test Error Boundary in isolation

2. **Integration tests**: Test Error Boundary with children

3. **E2E tests**: Test error recovery flows

4. **Chaos testing**: Inject errors randomly

5. **Monitoring**: Track error rates in production

**Q36: How does Error Boundary handle the "error in error boundary" problem?**
A: If an Error Boundary itself throws, React will unmount the entire tree. Prevention:

- Keep Error Boundaries simple
- Test Error Boundaries thoroughly
- Use try-catch in lifecycle methods

**Q37: Analyze the memory implications of Error Boundaries.**
A:

- Each Error Boundary: ~100 bytes
- Error state: ~50 bytes
- For 100 boundaries: ~15KB
- Error objects: Additional memory

**Q38: How would you implement a self-healing Error Boundary?**
A:

```typescript
class SelfHealingBoundary extends Component {
  state = { hasError: false, errorCount: 0 };

  static getDerivedStateFromError(error: Error) {
    return (prevState: State) => ({
      hasError: true,
      error: error,
      errorCount: prevState.errorCount + 1,
    }));
  }

  retry = () => {
    if (this.state.errorCount < 3) {
      this.setState({ hasError: false });
    }
  };

  render() {
    if (this.state.hasError) {
      return this.state.errorCount < 3
        ? <button onClick={this.retry}>Retry</button>
        : <div>Too many errors</div>;
    }
    return this.props.children;
  }
}

```

**Q39: How does Error Boundary interact with React Suspense?**
A: Error Boundaries catch errors from Suspense boundaries. They work together — Suspense handles loading, Error Boundaries handle errors.

**Q40: Design an Error Boundary monitoring system.**
A:

1. **Error tracking**: Sentry, LogRocket

2. **Analytics**: Error rates, user impact

3. **Alerting**: Threshold-based alerts

4. **Dashboards**: Error visualization

5. **Reporting**: Error trends, resolution

### Follow-ups (5-10)

**Q41: How would you explain Error Boundaries to a junior developer?**
A: "Error Boundaries are like safety nets. If a component crashes, the safety net catches the error and shows a friendly message instead of breaking the entire app."

**Q42: What are the edge cases in Error Boundaries?**
A:

- Errors in event handlers (not caught)
- Async errors (not caught)
- Errors in the boundary itself (unmounts tree)
- Multiple errors (only first caught)

**Q43: How does Error Boundary handle the "race condition" problem?**
A: Error Boundaries don't handle race conditions. They only catch synchronous errors during render phase.

**Q44: What is the relationship between Error Boundaries and React DevTools?**
A: React DevTools shows Error Boundary state and errors. It helps debug error catching behavior.

**Q45: How does Error Boundary interact with React StrictMode?**
A: StrictMode double-renders in development. Error Boundaries catch errors normally.

**Q46: What is the future of Error Boundaries in React?**
A: React is exploring:

- Better error reporting
- Improved recovery patterns
- Integration with Suspense
- Better DevTools support

**Q47: How would you implement a user feedback Error Boundary?**
A:

```typescript
class FeedbackErrorBoundary extends Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h2>Something went wrong</h2>
          <p>Please describe what you were doing:</p>
          <textarea placeholder="What happened?" />
          <button onClick={() => {
            // Send feedback
            sendFeedback(this.state.error, feedback);
            this.setState({ hasError: false });
          }}>
            Submit Feedback
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

```

**Q48: How does Error Boundary handle the "graceful degradation" pattern?**
A: Error Boundaries enable graceful degradation by:

- Showing fallback UI
- Providing recovery mechanisms
- Keeping rest of app working
- Logging errors for debugging

**Q49: What is the relationship between Error Boundaries and React.memo?**
A: `React.memo` prevents re-renders. Error Boundaries catch errors. They work independently.

**Q50: How would you implement a progressive Error Boundary system?**
A:

1. **Level 1**: App-level boundary (catches everything)

2. **Level 2**: Route-level boundaries (catches route errors)

3. **Level 3**: Component-level boundaries (catches component errors)

4. **Fallback hierarchy**: More specific fallbacks at lower levels

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

## References & Learn More

- [React Docs: Error Boundaries](https://react.dev/reference/react/Component#componentdidcatch)
- [Error Handling in React](https://www.freecodecamp.org/news/error-handling-in-react/)
- [React Error Boundary Guide](https://blog.logrocket.com/complete-guide-error-handling-react/)
