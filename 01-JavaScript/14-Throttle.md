# Throttle

## Definition

**Throttling** is a technique that limits how often a function can execute. It ensures a function is called at most once in a specified time period, regardless of how many times it's triggered.

## Why Do We Need It?

- **Performance**: Limit function execution frequency
- **Resource Management**: Prevent excessive API calls
- **UI Responsiveness**: Keep animations smooth
- **Rate Limiting**: Control event handler execution

## How It Works

### Throttle Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                      THROTTLE FLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WITHOUT THROTTLE:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Scroll events: 100 per second                      │    │
│  │  Function calls: 100 per second                     │    │
│  │  Performance: Poor                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  WITH THROTTLE (100ms):                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Scroll events: 100 per second                      │    │
│  │  Function calls: 10 per second (max)               │    │
│  │  Performance: Good                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  VISUALIZATION:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Events:    ||||||||||||||||||||||||||||||||||||    │    │
│  │  Throttle:  |→ execute  |→ execute  |→ execute     │    │
│  │             0ms         100ms        200ms          │    │
│  │                                                      │    │
│  │  Executes at most once per interval                 │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Throttle Implementation

```typescript
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;
  let lastArgs: Parameters<T> | null = null;
  let lastThis: any = null;

  return function(this: any, ...args: Parameters<T>) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;

      setTimeout(() => {
        inThrottle = false;
        if (lastArgs) {
          func.apply(lastThis, lastArgs);
          lastArgs = lastThis = null;
        }
      }, limit);
    } else {
      lastArgs = args;
      lastThis = this;
    }
  };
}

// Usage
function handleScroll() {
  console.log('Scroll position:', window.scrollY);
}

const throttledScroll = throttle(handleScroll, 100);
window.addEventListener('scroll', throttledScroll);
```

### Throttle with Leading/Trailing

```typescript
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number,
  options: { leading?: boolean; trailing?: boolean } = {}
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let lastArgs: Parameters<T> | null = null;
  let lastThis: any = null;
  let lastCallTime = 0;

  const { leading = true, trailing = true } = options;

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

    if (timeSinceLastCall >= limit) {
      if (leading) {
        invokeFunc(now);
      } else {
        lastCallTime = now;
      }

      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
    } else if (!timeoutId && trailing) {
      timeoutId = setTimeout(() => {
        invokeFunc(Date.now());
        timeoutId = null;
      }, limit - timeSinceLastCall);
    }
  };
}

// Usage
const throttledFn = throttle(fn, 100, { leading: true, trailing: false });
```

### Throttle with Cancel/Flush

```typescript
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): {
  (...args: Parameters<T>): void;
  cancel: () => void;
  flush: () => void;
} {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let lastArgs: Parameters<T> | null = null;
  let lastThis: any = null;
  let lastCallTime = 0;

  function invokeFunc() {
    if (lastArgs && lastThis) {
      func.apply(lastThis, lastArgs);
      lastCallTime = Date.now();
      lastArgs = lastThis = null;
    }
  }

  const throttled = function(this: any, ...args: Parameters<T>) {
    const now = Date.now();

    if (now - lastCallTime >= limit) {
      func.apply(this, args);
      lastCallTime = now;
    } else {
      lastArgs = args;
      lastThis = this;

      if (!timeoutId) {
        timeoutId = setTimeout(() => {
          invokeFunc();
          timeoutId = null;
        }, limit - (now - lastCallTime));
      }
    }
  };

  throttled.cancel = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
    lastArgs = lastThis = null;
    lastCallTime = 0;
  };

  throttled.flush = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
      invokeFunc();
    }
  };

  return throttled;
}
```

### React Hook

```typescript
import { useCallback, useRef, useEffect } from 'react';

function useThrottle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  const lastCallTime = useRef(0);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return useCallback(
    (...args: Parameters<T>) => {
      const now = Date.now();

      if (now - lastCallTime.current >= limit) {
        func(...args);
        lastCallTime.current = now;
      } else if (!timeoutRef.current) {
        timeoutRef.current = setTimeout(() => {
          func(...args);
          lastCallTime.current = Date.now();
          timeoutRef.current = null;
        }, limit - (now - lastCallTime.current));
      }
    },
    [func, limit]
  );
}

// Usage
function ScrollComponent() {
  const throttledScroll = useThrottle(() => {
    console.log('Scroll:', window.scrollY);
  }, 100);

  useEffect(() => {
    window.addEventListener('scroll', throttledScroll);
    return () => window.removeEventListener('scroll', throttledScroll);
  }, [throttledScroll]);

  return <div>Scroll content</div>;
}
```

## Real-World Use Cases

### 1. Scroll Event Handler

```typescript
function useScrollProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const handleScroll = throttle(() => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollTop / docHeight) * 100;
      setProgress(scrollPercent);
    }, 100);

    window.addEventListener('scroll', handleScroll);
    return () => {
      handleScroll.cancel();
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return progress;
}
```

### 2. Mouse Move Handler

```typescript
function useMousePosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = throttle((e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    }, 50);

    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      handleMouseMove.cancel();
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return position;
}
```

### 3. Button Click Handler

```typescript
function LikeButton() {
  const [likes, setLikes] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleLike = throttle(async () => {
    setIsProcessing(true);
    try {
      await api.likePost();
      setLikes(prev => prev + 1);
    } finally {
      setIsProcessing(false);
    }
  }, 1000);

  return (
    <button onClick={handleLike} disabled={isProcessing}>
      Like ({likes})
    </button>
  );
}
```

### 4. Window Resize Handler

```typescript
function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = throttle(() => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    }, 250);

    window.addEventListener('resize', handleResize);
    return () => {
      handleResize.cancel();
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return size;
}
```

### 5. API Rate Limiting

```typescript
class ApiClient {
  private throttledRequest: <T>(url: string) => Promise<T>;

  constructor() {
    this.throttledRequest = throttle(
      async <T>(url: string): Promise<T> => {
        const response = await fetch(url);
        return response.json();
      },
      1000
    );
  }

  async get<T>(url: string): Promise<T> {
    return this.throttledRequest<T>(url);
  }
}
```

## Common Mistakes

### 1. Not Cleaning Up

```typescript
// Bad: No cleanup
useEffect(() => {
  const handleScroll = throttle(updatePosition, 100);
  window.addEventListener('scroll', handleScroll);
  // Missing cleanup!
}, []);

// Good: Proper cleanup
useEffect(() => {
  const handleScroll = throttle(updatePosition, 100);
  window.addEventListener('scroll', handleScroll);
  return () => {
    handleScroll.cancel();
    window.removeEventListener('scroll', handleScroll);
  };
}, []);
```

### 2. Wrong Limit Time

```typescript
// Too short: Still too frequent
const scroll = throttle(updatePosition, 10);

// Too long: Feels unresponsive
const scroll = throttle(updatePosition, 1000);

// Good: Balance based on use case
const scroll = throttle(updatePosition, 100);
```

### 3. Using Throttle for Debounce Cases

```typescript
// Bad: Throttle for search input
const search = throttle(fetchResults, 300);
// Still makes too many API calls

// Good: Use debounce for search
const search = debounce(fetchResults, 300);
```

### 4. Not Handling Trailing Call

```typescript
// Bad: Only leading edge
const fn = throttle(originalFn, 100, { trailing: false });
// Misses last call

// Good: Handle trailing
const fn = throttle(originalFn, 100, { trailing: true });
```

## Best Practices

### 1. Choose Appropriate Limit

```typescript
// Scroll/animation: 100-16ms (60fps)
const scroll = throttle(update, 16);

// Mouse move: 50ms
const mouse = throttle(update, 50);

// Button click: 1000ms
const click = throttle(handleClick, 1000);

// Resize: 250ms
const resize = throttle(update, 250);
```

### 2. Clean Up Throttled Functions

```typescript
useEffect(() => {
  const throttledFn = throttle(fn, limit);

  return () => {
    throttledFn.cancel();
  };
}, [fn, limit]);
```

### 3. Use Cancel Method

```typescript
// Cancel on unmount or when no longer needed
const throttledFn = throttle(fn, limit);

// Cleanup
throttledFn.cancel();
```

### 4. Consider Leading vs Trailing

```typescript
// Leading: Execute immediately, then throttle
const fn = throttle(fn, 100, { leading: true });

// Trailing: Execute at end of interval
const fn = throttle(fn, 100, { trailing: true });

// Both: Execute at start and end
const fn = throttle(fn, 100, { leading: true, trailing: true });
```

## Performance Considerations

### Timer Overhead

```typescript
// Each throttle creates setTimeout
// Minimize by using requestAnimationFrame for animations

// Bad: Throttle for animations
const handleScroll = throttle(updateAnimation, 16);

// Good: Use requestAnimationFrame
const handleScroll = () => {
  requestAnimationFrame(updateAnimation);
};
```

### Memory Usage

```typescript
// Each throttled function holds timer reference
// Clean up to prevent memory leaks

// Bad: Creates new function on each render
const Component = () => {
  const throttledFn = throttle(fn, 100);  // Memory leak!
  return <button onClick={throttledFn}>Click</button>;
};

// Good: Use useCallback or ref
const Component = () => {
  const throttledFn = useCallback(
    throttle(fn, 100),
    [fn]
  );
  return <button onClick={throttledFn}>Click</button>;
};
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is throttling?**

A: Throttling limits how often a function can execute. It ensures a function is called at most once in a specified time period.

**Q2: When would you use throttle?**

A: Scroll events, mouse move, button clicks, or any event that fires rapidly and you need regular updates.

**Q3: What is a good default limit for throttle?**

A: 100ms is a good default. Adjust based on use case (16ms for animations, 1000ms for clicks).

**Q4: What is leading vs trailing throttle?**

A: Leading executes at the start of the interval, trailing at the end. Default is leading only.

**Q5: How do you cancel a throttled function?**

A: Call the cancel method: `throttledFn.cancel()`

### Intermediate (5-10 questions)

**Q6: How do you implement throttle from scratch?**

A: Use a flag and setTimeout. Set flag on execution, clear after limit.

**Q7: What is the difference between throttle and debounce?**

A: Throttle limits execution frequency, debounce delays until inactivity. Throttle executes at regular intervals, debounce once after pause.

**Q8: How do you throttle an async function?**

A: Wrap the async function in throttle. The throttled function will be called at the limit.

**Q9: How do you use throttle in React?**

A: Use useCallback with throttle, or create a custom useThrottle hook with useRef.

**Q10: What are common mistakes with throttle?**

A: Not cleaning up, wrong limit time, using for debounce cases, not handling trailing call.

### Senior (10-15 questions)

**Q11: How do you implement throttle with both leading and trailing options?**

A: Track call time, invoke on leading edge if enabled, set timeout for trailing edge.

**Q12: How do you handle throttled functions in server-side rendering?**

A: Ensure throttle only runs on client side, handle hydration properly.

**Q13: How do you test throttled functions?**

A: Use fake timers (jest.useFakeTimers), advance time, verify calls.

**Q14: How do you optimize throttle for high-frequency events?**

A: Use requestAnimationFrame for visual updates, combine with debounce.

**Q15: How do you handle multiple throttled calls?**

A: Each throttled function has its own timer. Use one throttle per function.

### FAANG-style (5-10 questions)

**Q16: Design a throttle utility with advanced features.**

A: Support leading/trailing, cancel/flush, custom timers, and different modes.

**Q17: How would you implement throttle in a Web Worker?**

A: Post messages to worker, throttle in worker, post results back.

**Q18: Analyze the memory implications of throttle.**

A: Each throttled function holds timer reference. Clean up on unmount.

**Q19: How do you debug throttle issues?**

A: Log timer IDs, track call times, use performance monitoring.

**Q20: What are security implications of throttle?**

A: Rate limiting, DoS prevention, input validation.

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a throttle bug in production?**

A: Not cleaning up timers causes memory leaks and stale state.

**Q22: How do you handle throttle in a micro-frontend architecture?**

A: Each micro-frontend manages its own throttle. Share utilities if needed.

**Q23: What is the relationship between throttle and event loop?**

A: Throttle uses setTimeout (macrotask). Executed after current synchronous code.

**Q24: How do different frameworks handle throttle?**

A: React: custom hooks. Vue: composables. Angular: pipes.

**Q25: What are best practices for throttle?**

A: Choose appropriate limit, clean up, use TypeScript, handle edge cases.

## Summary

Throttling is essential for performance:

1. **Definition**: Limits function execution frequency
2. **Use cases**: Scroll, mouse move, button clicks
3. **Implementation**: Flag + setTimeout
4. **Options**: Leading, trailing, cancel, flush
5. **Performance**: Prevents excessive function calls
6. **Cleanup**: Always clean up timers
7. **Testing**: Use fake timers

## Cheat Sheet

```text
THROTTLE CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHAT IS THROTTLE?
• Limits execution frequency
• At most once per interval
• Regular execution pattern
• Good for scroll, resize, clicks

IMPLEMENTATION:
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

OPTIONS:
• leading: Execute at start (default)
• trailing: Execute at end
• cancel: Cancel pending call
• flush: Execute pending call immediately

USE CASES:
• Scroll events (100ms)
• Mouse move (50ms)
• Button clicks (1000ms)
• Window resize (250ms)

VS DEBOUNCE:
• Throttle: Regular intervals
• Debounce: Wait for pause

CLEANUP:
• Cancel on unmount
• Remove event listeners
• Clear timers

COMMON MISTAKES:
• Not cleaning up
• Wrong limit time
• Using for debounce cases
• Not handling trailing

REACT:
• Use useCallback with throttle
• Custom useThrottle hook
• Store in useRef

TESTING:
• jest.useFakeTimers()
• jest.advanceTimersByTime()
• Verify call counts
```

## References & Learn More

- [Lodash: throttle()](https://lodash.com/docs/4.17.15#throttle)
- [MDN: throttling](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)
- [CSS-Tricks: Throttle and Debounce in JavaScript](https://css-tricks.com/throttle-and-debounce-in-javascript/)
- [GeeksforGeeks: Throttle vs Debounce](https://www.geeksforgeeks.org/throttle-in-javascript/)
