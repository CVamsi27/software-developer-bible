# useRef

## Definition

`useRef` is a React Hook that creates a mutable reference object with a `.current` property. It serves two primary purposes:
1. **DOM Access**: Accessing and manipulating DOM elements directly
2. **Persistent Values**: Storing mutable values that don't trigger re-renders when changed

Unlike `useState`, changing a ref's `.current` value does **not** cause a re-render. This makes refs ideal for values that need to persist across renders but shouldn't affect the UI.

## Why Do We Need It?

### The Problem

React components are declarative — you describe what the UI should look like, not how to manipulate the DOM. But sometimes you need to:
1. Focus an input element
2. Measure DOM element dimensions
3. Store timer IDs
4. Hold previous values
5. Access child component instances

### The Solution

`useRef` provides a way to hold mutable values without triggering re-renders:

```typescript
const Input = () => {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus(); // Direct DOM access
  };

  return (
    <>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus</button>
    </>
  );
};
```

## How It Works

### useRef Internals

```
useRef Internals:
═══════════════════════════════════════════════════════════════

First Render:
┌─────────────────────────────────────────────────────────────┐
│ useRef(null) creates:                                       │
│ { current: null }                                           │
│                                                             │
│ Stored in fiber's memoizedState                             │
│ Returns { current: null }                                   │
└─────────────────────────────────────────────────────────────┘

Subsequent Renders:
┌─────────────────────────────────────────────────────────────┐
│ useRef() returns the SAME object:                           │
│ { current: null } (same reference)                          │
│                                                             │
│ The object persists across renders                          │
│ Changing .current does NOT trigger re-render                │
└─────────────────────────────────────────────────────────────┘

DOM Ref Assignment:
┌─────────────────────────────────────────────────────────────┐
│ <input ref={inputRef} />                                    │
│                                                             │
│ React calls:                                                │
│ inputRef.current = <input> DOM node                        │
│                                                             │
│ After unmount:                                              │
│ inputRef.current = null                                     │
└─────────────────────────────────────────────────────────────┘
```

### DOM Ref vs State Ref

```
DOM Ref vs State Ref:
═══════════════════════════════════════════════════════════════

DOM Ref:
┌─────────────────────────────────────────────────────────────┐
│ const inputRef = useRef<HTMLInputElement>(null);            │
│                                                             │
│ <input ref={inputRef} />                                    │
│                                                             │
│ inputRef.current = DOM element                              │
│ Used for: focus, measure, scroll, animations                │
│ Automatically set on mount, null on unmount                 │
└─────────────────────────────────────────────────────────────┘

State Ref:
┌─────────────────────────────────────────────────────────────┐
│ const timerRef = useRef<NodeJS.Timeout | null>(null);       │
│                                                             │
│ useEffect(() => {                                           │
│   timerRef.current = setInterval(() => { ... }, 1000);     │
│   return () => clearInterval(timerRef.current!);            │
│ }, []);                                                     │
│                                                             │
│ timerRef.current = timer ID                                 │
│ Used for: timers, subscriptions, previous values            │
│ Persistent across renders, no re-render on change           │
└─────────────────────────────────────────────────────────────┘
```

### forwardRef

```
forwardRef:
═══════════════════════════════════════════════════════════════

Problem:
┌─────────────────────────────────────────────────────────────┐
│ const Input = ({ placeholder }) => {                        │
│   return <input placeholder={placeholder} />;               │
│ };                                                          │
│                                                             │
│ const Parent = () => {                                      │
│   const inputRef = useRef(null);                            │
│   return <Input ref={inputRef} placeholder="Enter..." />;   │
│   // ❌ Error: Function components don't accept ref         │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

Solution: forwardRef
┌─────────────────────────────────────────────────────────────┐
│ const Input = forwardRef<HTMLInputElement, Props>(           │
│   ({ placeholder }, ref) => {                               │
│     return <input ref={ref} placeholder={placeholder} />;   │
│   }                                                         │
│ );                                                          │
│                                                             │
│ const Parent = () => {                                      │
│   const inputRef = useRef<HTMLInputElement>(null);          │
│   return <Input ref={inputRef} placeholder="Enter..." />;   │
│   // ✅ Works! ref is forwarded to the input                │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘
```

### useImperativeHandle

```
useImperativeHandle:
═══════════════════════════════════════════════════════════════

Problem:
┌─────────────────────────────────────────────────────────────┐
│ Parent wants to call child's methods                        │
│ But child's internal state shouldn't be exposed             │
└─────────────────────────────────────────────────────────────┘

Solution:
┌─────────────────────────────────────────────────────────────┐
│ const Input = forwardRef((props, ref) => {                  │
│   const inputRef = useRef<HTMLInputElement>(null);          │
│                                                             │
│   useImperativeHandle(ref, () => ({                         │
│     focus: () => inputRef.current?.focus(),                 │
│     clear: () => { inputRef.current!.value = ''; },         │
│   }));                                                      │
│                                                             │
│   return <input ref={inputRef} />;                          │
│ });                                                         │
│                                                             │
│ const Parent = () => {                                      │
│   const inputRef = useRef<{focus: () => void; clear: () => void}>(null);│
│                                                             │
│   return (                                                  │
│     <>                                                      │
│       <Input ref={inputRef} />                              │
│       <button onClick={() => inputRef.current?.focus()}>Focus</button>│
│       <button onClick={() => inputRef.current?.clear()}>Clear</button>│
│     </>                                                     │
│   );                                                        │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic DOM Ref

```typescript
import React, { useRef, useEffect } from 'react';

const AutoFocusInput = () => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} placeholder="Auto-focused" />;
};
```

### Multiple DOM Refs

```typescript
const Form = () => {
  const nameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  const focusNextField = (nextRef: React.RefObject<HTMLInputElement>) => {
    nextRef.current?.focus();
  };

  return (
    <form>
      <input
        ref={nameRef}
        placeholder="Name"
        onKeyDown={() => focusNextField(emailRef)}
      />
      <input
        ref={emailRef}
        placeholder="Email"
        onKeyDown={() => focusNextField(passwordRef)}
      />
      <input
        ref={passwordRef}
        placeholder="Password"
        type="password"
      />
    </form>
  );
};
```

### Timer Ref

```typescript
const Timer = () => {
  const [time, setTime] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const startTimer = () => {
    intervalRef.current = setInterval(() => {
      setTime(prev => prev + 1);
    }, 1000);
  };

  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <div>
      <p>Time: {time}s</p>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </div>
  );
};
```

### Previous Value Ref

```typescript
const usePrevious = <T>(value: T): T | undefined => {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
};

const Counter = () => {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
    </div>
  );
};
```

### forwardRef Example

```typescript
import React, { forwardRef, useRef, useImperativeHandle } from 'react';

interface CustomInputRef {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

const CustomInput = forwardRef<CustomInputRef, { placeholder?: string }>(
  ({ placeholder }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      clear: () => {
        if (inputRef.current) {
          inputRef.current.value = '';
        }
      },
      getValue: () => inputRef.current?.value || '',
    }));

    return <input ref={inputRef} placeholder={placeholder} />;
  }
);

const Parent = () => {
  const inputRef = useRef<CustomInputRef>(null);

  return (
    <div>
      <CustomInput ref={inputRef} placeholder="Enter text..." />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
      <button onClick={() => inputRef.current?.clear()}>Clear</button>
      <button onClick={() => alert(inputRef.current?.getValue())}>Get Value</button>
    </div>
  );
};
```

### Measuring DOM Elements

```typescript
const useMeasure = <T extends HTMLElement>(): [
  React.RefObject<T>,
  { width: number; height: number } | null
] => {
  const ref = useRef<T>(null);
  const [dimensions, setDimensions] = useState<{ width: number; height: number } | null>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setDimensions({ width, height });
      }
    });

    observer.observe(element);

    return () => observer.disconnect();
  }, []);

  return [ref, dimensions];
};

const ResizableBox = () => {
  const [ref, dimensions] = useMeasure<HTMLDivElement>();

  return (
    <div ref={ref} style={{ width: '100%', height: '200px', background: 'lightblue' }}>
      {dimensions && (
        <p>Width: {dimensions.width}px, Height: {dimensions.height}px</p>
      )}
    </div>
  );
};
```

## Real-World Use Cases

### 1. Form with Programmatic Focus

```typescript
const LoginForm = () => {
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const email = emailRef.current?.value;
    const password = passwordRef.current?.value;

    if (!email || !password) {
      if (!email) emailRef.current?.focus();
      else passwordRef.current?.focus();
      return;
    }

    await login(email, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input ref={emailRef} type="email" placeholder="Email" />
      <input ref={passwordRef} type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
};
```

### 2. Video Player Controls

```typescript
const VideoPlayer = ({ src }: { src: string }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const play = () => videoRef.current?.play();
  const pause = () => videoRef.current?.pause();
  const seek = (time: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = time;
    }
  };

  return (
    <div>
      <video ref={videoRef} src={src} />
      <button onClick={isPlaying ? pause : play}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <button onClick={() => seek(0)}>Restart</button>
    </div>
  );
};
```

### 3. Canvas Drawing

```typescript
const Canvas = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Draw something
    ctx.fillStyle = 'blue';
    ctx.fillRect(10, 10, 100, 100);
  }, []);

  return <canvas ref={canvasRef} width={400} height={300} />;
};
```

### 4. Scroll Position Tracking

```typescript
const useScrollPosition = () => {
  const [scrollPosition, setScrollPosition] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollPosition(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return scrollPosition;
};

const ScrollProgress = () => {
  const scrollPosition = useScrollPosition();
  const progress = (scrollPosition / document.body.scrollHeight) * 100;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        height: '3px',
        width: `${progress}%`,
        background: 'blue',
      }}
    />
  );
};
```

## Common Mistakes

### 1. Using Ref Instead of State for Displayed Values

```typescript
// ❌ BAD: Using ref for value that should trigger re-render
const Counter = () => {
  const countRef = useRef(0);

  const increment = () => {
    countRef.current += 1;
    // No re-render! UI won't update
  };

  return (
    <div>
      <p>Count: {countRef.current}</p> {/* Shows 0 forever */}
      <button onClick={increment}>+1</button>
    </div>
  );
};

// ✅ GOOD: Use state for values that should trigger re-render
const Counter = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
    </div>
  );
};
```

### 2. Reading Ref During Render

```typescript
// ❌ BAD: Reading ref during render
const Component = () => {
  const inputRef = useRef<HTMLInputElement>(null);

  // inputRef.current is null during first render!
  // Only set after DOM is committed
  const value = inputRef.current?.value; // undefined

  return <input ref={inputRef} />;
};

// ✅ GOOD: Read ref in useEffect or event handlers
const Component = () => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Now inputRef.current is the DOM element
    console.log(inputRef.current?.value);
  }, []);

  const handleClick = () => {
    console.log(inputRef.current?.value);
  };

  return (
    <div>
      <input ref={inputRef} />
      <button onClick={handleClick}>Get Value</button>
    </div>
  );
};
```

### 3. Not Cleaning Up Ref-Based Subscriptions

```typescript
// ❌ BAD: No cleanup
const Timer = () => {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      console.log('tick');
    }, 1000);
    // No cleanup! Timer continues after unmount
  }, []);

  return <div>Timer running</div>;
};

// ✅ GOOD: Proper cleanup
const Timer = () => {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      console.log('tick');
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return <div>Timer running</div>;
};
```

### 4. Using Ref to Store State

```typescript
// ❌ BAD: Using ref to store state
const Component = () => {
  const dataRef = useRef<Data[]>([]);

  const fetchData = async () => {
    const data = await api.getData();
    dataRef.current = data; // No re-render! UI won't update
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch</button>
      <ul>
        {dataRef.current.map(item => ( // Always empty
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
};

// ✅ GOOD: Use state for data that should trigger re-render
const Component = () => {
  const [data, setData] = useState<Data[]>([]);

  const fetchData = async () => {
    const newData = await api.getData();
    setData(newData); // Triggers re-render
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch</button>
      <ul>
        {data.map(item => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
};
```

## Best Practices

1. **Use ref for DOM access**: Focus, measure, scroll, animations.
2. **Use ref for persistent values**: Timers, subscriptions, previous values.
3. **Don't use ref for displayed values**: Use state instead.
4. **Clean up ref-based subscriptions**: In useEffect cleanup function.
5. **Use forwardRef to expose refs**: When parent needs child's DOM access.
6. **Use useImperativeHandle to limit exposure**: Only expose necessary methods.
7. **Don't read ref during render**: Only in useEffect or event handlers.

## Performance Considerations

### Ref vs State

| Aspect | Ref | State |
|--------|-----|-------|
| Triggers re-render | No | Yes |
| Mutable | Yes | No |
| DOM access | Yes | No |
| Persistent across renders | Yes | Yes |
| Use case | DOM access, timers | Displayed values |

### Ref Performance

- **No overhead**: Refs don't trigger re-renders
- **Direct DOM access**: Faster than state-driven updates
- **Memory efficient**: Single object persisted across renders

## Interview Questions

### Beginner (5-10)

**Q1: What is useRef?**
A: `useRef` is a React Hook that creates a mutable reference object with a `.current` property. It's used for DOM access and storing persistent values that don't trigger re-renders.

**Q2: What is the difference between useRef and useState?**
A: `useState` triggers re-renders when the value changes. `useRef` doesn't trigger re-renders. Use `useState` for values that should update the UI. Use `useRef` for DOM access and persistent values.

**Q3: When does useRef.current get set?**
A: For DOM refs, `current` is set after the component mounts (commit phase). For non-DOM refs, you set `current` yourself.

**Q4: What is forwardRef?**
A: `forwardRef` is a higher-order component that lets a function component accept a `ref` prop and forward it to a child component.

**Q5: What is useImperativeHandle?**
A: `useImperativeHandle` customizes the value exposed via `ref`. It lets you control what parent components can access when they ref your component.

**Q6: Can you use useRef with class components?**
A: `useRef` is a hook, so it's only for function components. Class components use `React.createRef()` or callback refs.

**Q7: What happens to ref.current when component unmounts?**
A: React sets DOM ref's `current` to `null` when the component unmounts.

**Q8: Can you pass refs as props?**
A: No. Refs are special props that React handles. Use `forwardRef` to pass refs to child components.

**Q9: What is the use case for useRef besides DOM access?**
A: Common uses:
- Storing timer/interval IDs
- Holding previous values
- Storing subscriptions
- Any mutable value that shouldn't trigger re-render

**Q10: How do you clean up ref-based resources?**
A: In the `useEffect` cleanup function:
```typescript
useEffect(() => {
  const interval = setInterval(() => {}, 1000);
  return () => clearInterval(interval);
}, []);
```

### Intermediate (5-10)

**Q11: Explain the internal mechanism of useRef.**
A: `useRef` stores the reference object in the fiber's `memoizedState`. On subsequent renders, it returns the same object. The object persists across renders, and changing `.current` doesn't trigger re-renders.

**Q12: What is the difference between useRef and createRef?**
A: `useRef` is a hook — it persists across renders. `createRef` creates a new ref each time it's called. Use `useRef` in function components, `createRef` in class components.

**Q13: How do you use useRef to store previous values?**
A:
```typescript
const usePrevious = <T>(value: T) => {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
};
```

**Q14: What is the relationship between useRef and useEffect?**
A: `useRef` provides persistent values across renders. `useEffect` runs after render. Together, they enable DOM manipulation and persistent side effects.

**Q15: Can you use useRef to store state?**
A: You can, but it won't trigger re-renders. Use `useState` for values that should update the UI. Use `useRef` for values that shouldn't.

**Q16: What is the use case for useImperativeHandle?**
A: `useImperativeHandle` limits what parent components can access via ref. It's useful for encapsulating child component logic.

**Q17: How do you handle multiple refs?**
A: Use multiple `useRef` calls:
```typescript
const inputRef1 = useRef<HTMLInputElement>(null);
const inputRef2 = useRef<HTMLInputElement>(null);
```

**Q18: What is the performance impact of useRef?**
A: `useRef` has minimal overhead — it stores a single object that persists across renders. No re-renders are triggered.

**Q19: Can you use useRef with TypeScript?**
A: Yes. Provide a type parameter:
```typescript
const inputRef = useRef<HTMLInputElement>(null);
```

**Q20: What are the common patterns for useRef?**
A:
- DOM access (focus, measure, scroll)
- Timer management (setInterval, setTimeout)
- Previous values
- Subscriptions
- Mutable state that shouldn't trigger re-render

### Senior (10-15)

**Q21: Explain the complete lifecycle of a ref.**
A:
1. `useRef()` creates the reference object
2. On first render, `current` is set to initial value (or null for DOM refs)
3. After commit, DOM refs get `current` set to DOM node
4. On subsequent renders, same object returned
5. On unmount, DOM refs get `current` set to null

**Q22: How does useRef interact with React's concurrent rendering?**
A: `useRef` persists across renders, even during concurrent rendering. This makes it useful for storing values that need to persist across interrupted renders.

**Q23: What is the relationship between useRef and React.memo?**
A: `React.memo` prevents re-renders when props haven't changed. `useRef` persists values across renders. Together, they enable efficient DOM manipulation without unnecessary re-renders.

**Q24: How do you use useRef for animation?**
A:
```typescript
const useAnimation = () => {
  const frameRef = useRef<number>();
  const startAnimation = (callback: () => void) => {
    const animate = () => {
      callback();
      frameRef.current = requestAnimationFrame(animate);
    };
    frameRef.current = requestAnimationFrame(animate);
  };
  const stopAnimation = () => {
    if (frameRef.current) {
      cancelAnimationFrame(frameRef.current);
    }
  };
  return { startAnimation, stopAnimation };
};
```

**Q25: What is the difference between ref and state for DOM measurements?**
A: Use `ref` for DOM measurements in `useLayoutEffect` (before paint) or `useEffect` (after paint). State triggers re-renders; refs don't.

**Q26: How do you handle ref-based animations?**
A: Use `requestAnimationFrame` with refs:
```typescript
const useAnimationFrame = (callback: () => void) => {
  const requestRef = useRef<number>();
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    const animate = () => {
      callbackRef.current();
      requestRef.current = requestAnimationFrame(animate);
    };
    requestRef.current = requestAnimationFrame(animate);
    return () => {
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, []);
};
```

**Q27: What is the relationship between useRef and React DevTools?**
A: React DevTools shows ref values in the component tree. You can inspect `current` values to debug DOM access and persistent values.

**Q28: How do you test ref-based components?**
A: Use React Testing Library's `ref` testing utilities:
```typescript
test('focuses input', () => {
  const ref = { current: null };
  render(<Input ref={ref} />);
  act(() => ref.current.focus());
  expect(ref.current).toHaveFocus();
});
```

**Q29: What is the performance impact of ref-based DOM access?**
A: Ref-based DOM access is faster than state-driven updates because it doesn't trigger re-renders. However, excessive DOM manipulation can cause layout thrashing.

**Q30: How do you handle ref-based subscriptions?**
A:
```typescript
const useSubscription = <T>(subscribe: (callback: (data: T) => void) => () => void) => {
  const callbackRef = useRef<(data: T) => void>();
  const [data, setData] = useState<T>();

  useEffect(() => {
    callbackRef.current = setData;
  }, []);

  useEffect(() => {
    return subscribe((data) => callbackRef.current?.(data));
  }, [subscribe]);
};
```

### FAANG-style (5-10)

**Q31: Design a ref-based animation system.**
A:
1. **Frame tracking**: Use `requestAnimationFrame` with refs
2. **Animation state**: Store animation progress in refs
3. **Cleanup**: Cancel animation frames on unmount
4. **Performance**: Use `useLayoutEffect` for DOM mutations

```typescript
const useAnimation = (duration: number) => {
  const startTimeRef = useRef<number>();
  const frameRef = useRef<number>();
  const progressRef = useRef(0);

  const animate = (callback: (progress: number) => void) => {
    startTimeRef.current = performance.now();
    const step = (timestamp: number) => {
      const elapsed = timestamp - startTimeRef.current!;
      progressRef.current = Math.min(elapsed / duration, 1);
      callback(progressRef.current);
      if (progressRef.current < 1) {
        frameRef.current = requestAnimationFrame(step);
      }
    };
    frameRef.current = requestAnimationFrame(step);
  };

  const cancel = () => {
    if (frameRef.current) {
      cancelAnimationFrame(frameRef.current);
    }
  };

  useEffect(() => cancel, []);

  return { animate, cancel };
};
```

**Q32: How would you implement a ref-based virtual scroll?**
A:
```typescript
const useVirtualScroll = (items: any[], itemHeight: number) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [scrollTop, setScrollTop] = useState(0);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleScroll = () => {
      setScrollTop(container.scrollTop);
    };

    container.addEventListener('scroll', handleScroll);
    return () => container.removeEventListener('scroll', handleScroll);
  }, []);

  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + Math.ceil(containerRef.current?.clientHeight / itemHeight || 0) + 1, items.length);
  const visibleItems = items.slice(startIndex, endIndex);

  return { containerRef, visibleItems, startIndex };
};
```

**Q33: Analyze the memory implications of useRef.**
A:
- Each ref: ~100 bytes (object with `.current`)
- DOM refs: Additional memory for DOM node reference
- Persistent across renders: No memory churn
- Cleanup: DOM refs set to null on unmount

**Q34: How would you implement a ref-based form validator?**
A:
```typescript
const useFormField = (validator: (value: string) => string | null) => {
  const ref = useRef<HTMLInputElement>(null);
  const [error, setError] = useState<string | null>(null);

  const validate = () => {
    const value = ref.current?.value || '';
    const validationError = validator(value);
    setError(validationError);
    return validationError === null;
  };

  return { ref, error, validate };
};
```

**Q35: Design a ref-based component communication system.**
A:
```typescript
const useImperativeHandle = <T>(ref: React.Ref<T>, createHandle: () => T) => {
  const instanceRef = useRef<T>();

  useEffect(() => {
    if (typeof ref === 'function') {
      ref(instanceRef.current);
    } else if (ref) {
      ref.current = instanceRef.current;
    }
  }, [ref, createHandle]);
};
```

**Q36: How does useRef interact with React Suspense?**
A: `useRef` persists across suspended renders. This makes it useful for storing values that need to persist across suspended states.

**Q37: Analyze the performance characteristics of ref-based DOM access.**
A:
- Direct DOM access: ~0.1ms
- State-driven DOM update: ~1ms
- Re-render overhead: ~0.5ms per component
- Layout thrashing: Avoid multiple DOM reads/writes

**Q38: How would you implement a ref-based drag and drop?**
A:
```typescript
const useDragDrop = (onDrop: (data: any) => void) => {
  const dragRef = useRef<any>(null);
  const dropRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const dropElement = dropRef.current;
    if (!dropElement) return;

    const handleDragOver = (e: DragEvent) => {
      e.preventDefault();
    };

    const handleDrop = (e: DragEvent) => {
      e.preventDefault();
      onDrop(dragRef.current);
    };

    dropElement.addEventListener('dragover', handleDragOver);
    dropElement.addEventListener('drop', handleDrop);

    return () => {
      dropElement.removeEventListener('dragover', handleDragOver);
      dropElement.removeEventListener('drop', handleDrop);
    };
  }, [onDrop]);

  return { dragRef, dropRef };
};
```

**Q39: How does useRef handle the "stale closure" problem?**
A: Refs don't have stale closures because they always access the current value via `.current`. This makes them ideal for storing values that need to be accessed in callbacks.

**Q40: Design a ref-based testing utility.**
A:
```typescript
const useRefTester = <T>() => {
  const ref = useRef<T>(null);

  const getValue = () => ref.current;
  const setValue = (value: T) => {
    ref.current = value;
  };

  return { ref, getValue, setValue };
};
```

### Follow-ups (5-10)

**Q41: How would you explain useRef to a junior developer?**
A: "`useRef` is like a sticky note that stays on your desk. You can write things on it, and it stays there even when React redraws the screen. It's useful for things like remembering which input to focus or storing timer IDs."

**Q42: What are the edge cases in useRef?**
A:
- Reading ref during render (DOM ref is null)
- Not cleaning up ref-based subscriptions
- Using ref for values that should trigger re-renders
- Forgetting to set ref.current to null on unmount

**Q43: How does useRef handle the "previous value" pattern?**
A:
```typescript
const usePrevious = <T>(value: T) => {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
};
```

**Q44: What is the relationship between useRef and React DevTools?**
A: React DevTools shows ref values in the component tree. You can inspect `current` values to debug DOM access and persistent values.

**Q45: How does useRef interact with React StrictMode?**
A: StrictMode double-renders in development. `useRef` persists across double-renders, so it's not affected.

**Q46: What is the future of useRef in React?**
A: React is exploring better ref handling and potential improvements to `useImperativeHandle`. The core concept of mutable references is likely to remain.

**Q47: How would you implement a ref-based chart interaction?**
A:
```typescript
const useChartInteraction = (chartRef: React.RefObject<HTMLCanvasElement>) => {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  useEffect(() => {
    const canvas = chartRef.current;
    if (!canvas) return;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      // Find point at (x, y)
    };

    canvas.addEventListener('mousemove', handleMouseMove);
    return () => canvas.removeEventListener('mousemove', handleMouseMove);
  }, [chartRef]);

  return { hoveredPoint };
};
```

**Q48: How does useRef handle the "mutable state" pattern?**
A: Refs are perfect for mutable state that shouldn't trigger re-renders:
```typescript
const useMutableState = <T>(initialValue: T) => {
  const ref = useRef(initialValue);
  const getValue = () => ref.current;
  const setValue = (value: T) => { ref.current = value; };
  return { getValue, setValue };
};
```

**Q49: What is the relationship between useRef and React.memo?**
A: `React.memo` prevents re-renders. `useRef` persists values across renders. Together, they enable efficient DOM manipulation without unnecessary re-renders.

**Q50: How would you implement a ref-based keyboard shortcut?**
A:
```typescript
const useKeyboardShortcut = (key: string, callback: () => void) => {
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === key) {
        callbackRef.current();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [key]);
};
```

## Summary

`useRef` is a versatile React Hook for DOM access and persistent values. It creates a mutable reference object that persists across renders without triggering re-renders. Key features include DOM ref assignment, `forwardRef` for child component access, and `useImperativeHandle` for limiting exposed methods.

## Cheat Sheet

```
useRef Key Points:
├── What: Mutable reference object with .current property
├── Purpose: DOM access and persistent values
├── No re-render: Changing .current doesn't trigger re-render
├── Persistent: Same object across renders
├── DOM refs: Set after mount, null on unmount

Two Types:
├── DOM Ref: <input ref={inputRef} /> → .current = DOM node
└── State Ref: useRef(value) → .current = value (persistent)

forwardRef:
├── Purpose: Pass ref to child components
├── Syntax: forwardRef((props, ref) => ...)
└── Use case: Parent needs child's DOM access

useImperativeHandle:
├── Purpose: Limit ref exposure
├── Syntax: useImperativeHandle(ref, () => ({ ... }))
└── Use case: Only expose necessary methods

Common Use Cases:
├── DOM access: focus, measure, scroll
├── Timer management: setInterval, setTimeout
├── Previous values: usePrevious hook
├── Subscriptions: event listeners, WebSocket
├── Animations: requestAnimationFrame
└── Mutable state: values that don't trigger re-render

Common Mistakes:
├── Using ref for displayed values (use state instead)
├── Reading ref during render (DOM ref is null)
├── Not cleaning up ref-based subscriptions
├── Using ref to store state that should trigger re-render
└── Forgetting to forwardRef when parent needs child ref

Best Practices:
├── Use ref for DOM access (focus, measure, scroll)
├── Use ref for persistent values (timers, subscriptions)
├── Use state for displayed values
├── Clean up ref-based subscriptions in useEffect
├── Use forwardRef to expose refs to parent
├── Use useImperativeHandle to limit exposure
└── Don't read ref during render (only in useEffect/events)

Performance:
├── No re-render overhead
├── Direct DOM access (faster than state)
├── Memory efficient (single object)
└── Persistent across renders (no memory churn)
```

## References & Learn More

- [React Docs: useRef](https://react.dev/reference/react/useRef)
- [React useRef Guide](https://www.freecodecamp.org/news/useref-hook-explained/)
- [useRef vs useState](https://dmitripavlutin.com/useref-vs-usestate/)
