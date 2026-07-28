[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

# Debounce

## Definition

**Debouncing** is a technique that delays the execution of a function until after a specified period of inactivity. Each time the function is called, the timer resets. The function only executes when there's a pause in calls.

## Why Do We Need It?

- **Performance**: Prevent excessive function calls during rapid events
- **User Experience**: Avoid laggy UI from too many updates
- **Resource Management**: Reduce server/API calls
- **Input Handling**: Handle search, resize, scroll events efficiently

## How It Works

### Debounce Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                      DEBOUNCE FLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WITHOUT DEBOUNCE:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  User types: H -> He -> Hel -> Hell -> Hello       │    │
│  │  API calls: 5 (one per keystroke)                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  WITH DEBOUNCE (300ms):                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  User types: H -> He -> Hel -> Hell -> Hello       │    │
│  │  Timer resets with each keystroke                   │    │
│  │  API calls: 1 (300ms after last keystroke)          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  VISUALIZATION:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Keystrokes:  | H | e | l | l | o |                 │    │
│  │  Timer:       |---|---|---|---|------→ execute      │    │
│  │                                                      │    │
│  │  Each keystroke resets the timer                    │    │
│  │  Function only executes after 300ms of no input    │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Debounce vs Throttle

```text
┌─────────────────────────────────────────────────────────────┐
│                  DEBOUNCE vs THROTTLE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DEBOUNCE:                                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Waits for pause in activity                     │    │
│  │  • Only executes once after pause                  │    │
│  │  • Good for: Search, form validation               │    │
│  │  • Example: Type search query, search when done    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  THROTTLE:                                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Limits execution frequency                      │    │
│  │  • Executes at most once per interval              │    │
│  │  • Good for: Scroll, resize, click events          │    │
│  │  │  Example: Update scroll position, max once/sec  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  TIMING:                                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Events:    ||||||||||||||||||||||||                │    │
│  │  Debounce:              |→ execute                  │    │
│  │  Throttle:  |→ execute |→ execute |→ execute       │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Debounce Implementation

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  return function(this: any, ...args: Parameters<T>) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      func.apply(this, args);
      timeoutId = null;
    }, wait);
  };
}

// Usage
function search(query: string) {
  console.log(`Searching: ${query}`);
}

const debouncedSearch = debounce(search, 300);

input.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});

```

### Debounce with Leading Option

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number,
  options: { leading?: boolean; trailing?: boolean } = {}
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let lastArgs: Parameters<T> | null = null;
  let lastThis: any = null;
  let lastCallTime: number = 0;

  const { leading = false, trailing = true } = options;

  function invokeFunc(time: number) {
    if (lastArgs && lastThis) {
      func.apply(lastThis, lastArgs);
    }
    lastArgs = lastThis = null;
    lastCallTime = time;
  }

  return function(this: any, ...args: Parameters<T>) {
    const now = Date.now();
    const timeSinceLastCall = now - lastCallTime;

    lastArgs = args;
    lastThis = this;
    lastCallTime = now;

    if (timeSinceLastCall >= wait && leading) {
      invokeFunc(now);
    }

    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    if (trailing) {
      timeoutId = setTimeout(() => {
        invokeFunc(Date.now());
      }, wait);
    }
  };
}

// Usage with leading option
const debouncedFn = debounce(fn, 300, { leading: true });

```

### Debounce with Cancel and Flush

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): {
  (...args: Parameters<T>): void;
  cancel: () => void;
  flush: () => void;
} {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let lastArgs: Parameters<T> | null = null;
  let lastThis: any = null;

  function invokeFunc() {
    if (lastArgs && lastThis) {
      func.apply(lastThis, lastArgs);
      lastArgs = lastThis = null;
    }
  }

  const debounced = function(this: any, ...args: Parameters<T>) {
    lastArgs = args;
    lastThis = this;

    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    timeoutId = setTimeout(() => {
      invokeFunc();
      timeoutId = null;
    }, wait);
  };

  debounced.cancel = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
    lastArgs = lastThis = null;
  };

  debounced.flush = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
      invokeFunc();
    }
  };

  return debounced;
}

// Usage
const debouncedSearch = debounce(search, 300);

// Cancel pending call
debouncedSearch.cancel();

// Execute pending call immediately
debouncedSearch.flush();

```

### React Hook

```typescript
import { useCallback, useRef } from 'react';

function useDebounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  return useCallback(
    (...args: Parameters<T>) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        func(...args);
      }, wait);
    },
    [func, wait]
  );
}

// Usage
function SearchComponent() {
  const debouncedSearch = useDebounce((query: string) => {
    fetchSearchResults(query);
  }, 300);

  return (
    <input
      type="text"
      onChange={(e) => debouncedSearch(e.target.value)}
    />
  );
}

```

## Real-World Use Cases

### 1. Search Input

```typescript
function SearchInput() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const debouncedSearch = useDebounce(async (searchQuery: string) => {
    if (searchQuery.length < 2) {
      setResults([]);
      return;
    }

    const response = await fetch(`/api/search?q=${searchQuery}`);
    const data = await response.json();
    setResults(data.results);
  }, 300);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    debouncedSearch(value);
  };

  return (
    <div>
      <input value={query} onChange={handleChange} />
      <ul>
        {results.map(result => (
          <li key={result.id}>{result.title}</li>
        ))}
      </ul>
    </div>
  );
}

```

### 2. Window Resize Handler

```typescript
function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = debounce(() => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    }, 250);

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      handleResize.cancel();
    };
  }, []);

  return size;
}

```

### 3. Form Validation

```typescript
function Form() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const validateEmail = useDebounce(async (value: string) => {
    if (!value) {
      setError('');
      return;
    }

    const response = await fetch(`/api/validate-email?email=${value}`);
    const data = await response.json();

    if (!data.valid) {
      setError('Invalid email address');
    }
  }, 500);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    validateEmail(value);
  };

  return (
    <div>
      <input value={email} onChange={handleChange} />
      {error && <span className="error">{error}</span>}
    </div>
  );
}

```

### 4. Scroll Event Handler

```typescript
function useScrollPosition() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = debounce(() => {
      setScrollY(window.scrollY);
    }, 100);

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      handleScroll.cancel();
    };
  }, []);

  return scrollY;
}

```

### 5. Button Click Handler

```typescript
function SubmitButton() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = useDebounce(async () => {
    setIsSubmitting(true);
    try {
      await submitForm();
    } finally {
      setIsSubmitting(false);
    }
  }, 1000);

  return (
    <button onClick={handleSubmit} disabled={isSubmitting}>
      {isSubmitting ? 'Submitting...' : 'Submit'}
    </button>
  );
}

```

## Common Mistakes

### 1. Not Cleaning Up

```typescript
// Bad: No cleanup
useEffect(() => {
  const handleResize = debounce(() => {
    setWidth(window.innerWidth);
  }, 250);

  window.addEventListener('resize', handleResize);
  // Missing cleanup!
}, []);

// Good: Proper cleanup
useEffect(() => {
  const handleResize = debounce(() => {
    setWidth(window.innerWidth);
  }, 250);

  window.addEventListener('resize', handleResize);
  return () => {
    handleResize.cancel();
    window.removeEventListener('resize', handleResize);
  };
}, []);

```

### 2. Using Debounce Everywhere

```typescript
// Bad: Debouncing scroll for animation
const handleScroll = debounce(() => {
  updateAnimation();  // Needs immediate response
}, 100);

// Good: Use requestAnimationFrame for animations
const handleScroll = () => {
  requestAnimationFrame(() => {
    updateAnimation();
  });
};

```

### 3. Wrong Wait Time

```typescript
// Too short: Still causes excessive calls
const search = debounce(fetchResults, 50);

// Too long: Feels unresponsive
const search = debounce(fetchResults, 2000);

// Good: Balance based on use case
const search = debounce(fetchResults, 300);

```

### 4. Not Handling Edge Cases

```typescript
// Bad: No leading edge
const search = debounce(fetchResults, 300);
// First keystroke waits 300ms

// Good: Leading edge for immediate feedback
const search = debounce(fetchResults, 300, { leading: true });

```

## Best Practices

### 1. Choose Appropriate Wait Time

```typescript
// Search: 300ms (user typing speed)
const search = debounce(fetchResults, 300);

// Form validation: 500ms (less frequent)
const validate = debounce(validateField, 500);

// Resize: 100ms (responsive but not too frequent)
const resize = debounce(handleResize, 100);

```

### 2. Clean Up Debounced Functions

```typescript
useEffect(() => {
  const debouncedFn = debounce(fn, wait);

  // Store reference for cleanup
  debouncedFnRef.current = debouncedFn;

  return () => {
    debouncedFn.cancel();
  };
}, [fn, wait]);

```

### 3. Use TypeScript

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  // Implementation
}

```

### 4. Add Cancel and Flush Methods

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): {
  (...args: Parameters<T>): void;
  cancel: () => void;
  flush: () => void;
} {
  // Implementation with cancel and flush
}

```

## Performance Considerations

### Memory Usage

```typescript
// Each debounced function holds a timer reference
// Clean up when component unmounts

// Bad: Creates new debounced function on each render
const Component = () => {
  const debouncedFn = debounce(fn, 300);  // Memory leak!
  return <button onClick={debouncedFn}>Click</button>;
};

// Good: Use useCallback or ref
const Component = () => {
  const debouncedFn = useCallback(
    debounce(fn, 300),
    [fn]
  );
  return <button onClick={debouncedFn}>Click</button>;
};

```

### Timer Precision

```typescript
// setTimeout is not precise
// Expect delays of 1-16ms depending on browser

// For precise timing, use:
// - requestAnimationFrame for animations
// - Performance.now() for measurements

```

## Summary

Debouncing is essential for performance:

1. **Definition**: Delays execution until pause in calls

2. **Use cases**: Search, resize, form validation

3. **Implementation**: setTimeout with clearTimeout

4. **Options**: Leading, trailing, cancel, flush

5. **Performance**: Prevents excessive function calls

6. **Cleanup**: Always clean up timers

7. **Testing**: Use fake timers

## Cheat Sheet
```text
DEBOUNCE CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHAT IS DEBOUNCE?
• Delays function execution
• Waits for pause in calls
• Resets timer with each call
• Executes once after inactivity

IMPLEMENTATION:
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

OPTIONS:
• leading: Execute at start
• trailing: Execute at end (default)
• cancel: Cancel pending call
• flush: Execute pending call immediately

USE CASES:
• Search input (300ms)
• Form validation (500ms)
• Window resize (100ms)
• Button clicks (1000ms)

VS THROTTLE:
• Debounce: Waits for pause
• Throttle: Limits frequency

CLEANUP:
• Cancel on unmount
• Remove event listeners
• Clear timers

COMMON MISTAKES:
• Not cleaning up
• Wrong wait time
• Using for animations
• Not handling edge cases

REACT:
• Use useCallback with debounce
• Custom useDebounce hook
• Store in useRef

TESTING:
• jest.useFakeTimers()
• jest.advanceTimersByTime()
• Verify call counts

```

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Node.js](../05-NodeJS/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [Lodash: debounce()](https://lodash.com/docs/4.17.15#debounce)
- [JavaScript.info: Task Throttle & Debounce](https://web.archive.org/web/20240701000000/https://javascript.info/task-throttle-debounce)
- [FreeCodeCamp: Debounce vs Throttle](https://www.freecodecamp.org/news/debouncing-and-throttling-in-javascript/)
- [CSS-Tricks: Debouncing and Throttling](https://css-tricks.com/debouncing-throttling-explained/)
