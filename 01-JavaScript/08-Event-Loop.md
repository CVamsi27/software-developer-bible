# Event Loop

## Definition

The **Event Loop** is the mechanism that allows JavaScript to perform non-blocking operations despite being single-threaded. It continuously checks the call stack and callback queues, executing tasks when the stack is empty. The event loop is the heart of JavaScript's asynchronous behavior.

## Why Do We Need It?

- **Non-blocking I/O**: Allows JavaScript to handle multiple operations without waiting
- **UI Responsiveness**: Keeps the browser responsive while processing
- **Concurrency**: Enables handling of multiple tasks in a single thread
- **Async Operations**: Foundation for Promises, async/await, callbacks
- **Performance**: Efficient use of single thread for I/O-bound tasks

## How It Works

### Browser Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                   BROWSER ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              JavaScript Engine (V8)                 │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │           Call Stack                        │    │    │
│  │  │  ┌─────────────────────────────────────┐    │    │    │
│  │  │  │  Frame 3 (current executing)        │    │    │    │
│  │  │  ├─────────────────────────────────────┤    │    │    │
│  │  │  │  Frame 2                            │    │    │    │
│  │  │  ├─────────────────────────────────────┤    │    │    │
│  │  │  │  Frame 1                            │    │    │    │
│  │  │  └─────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Event Loop                              │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  1. Check if call stack is empty            │    │    │
│  │  │  2. If empty, check microtask queue         │    │    │
│  │  │  3. If microtasks empty, check macrotask    │    │    │
│  │  │  4. Repeat                                  │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│           ┌───────────────┼───────────────┐                │
│           ▼               ▼               ▼                │
│  ┌─────────────────┐ ┌─────────────┐ ┌─────────────┐      │
│  │  Microtask Queue│ │Macrotask Queue│ │ Web APIs   │      │
│  │  • Promise.then │ │ • setTimeout │ │ • fetch    │      │
│  │  • queueMicro   │ │ • setInterval│ │ • DOM      │      │
│  │  • MutationObs  │ │ • I/O        │ │ • setTimeout│     │
│  └─────────────────┘ └─────────────┘ └─────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Event Loop Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    EVENT LOOP FLOW                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  START                                                       │
│    │                                                         │
│    ▼                                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Execute synchronous code (call stack)              │    │
│  └─────────────────────────────────────────────────────┘    │
│    │                                                         │
│    ▼                                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Call stack empty?                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│    │              │                                          │
│    │ No           │ Yes                                      │
│    ▼              ▼                                          │
│  ┌────────┐  ┌────────────────────────────────────────┐    │
│  │  Wait  │  │  Process ALL microtasks                │    │
│  │        │  │  (Promise callbacks, queueMicrotask)    │    │
│  └────────┘  └────────────────────────────────────────┘    │
│                  │                                           │
│                  ▼                                           │
│              ┌────────────────────────────────────────┐    │
│              │  Microtasks empty?                      │    │
│              └────────────────────────────────────────┘    │
│                  │              │                            │
│                  │ No           │ Yes                        │
│                  ▼              ▼                            │
│              ┌────────┐  ┌──────────────────────────────┐  │
│              │  Wait  │  │  Process ONE macrotask       │  │
│              │        │  │  (setTimeout, I/O, etc.)     │  │
│              └────────┘  └──────────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│              ┌────────────────────────────────────────┐    │
│              │  Render (if needed - 16ms frame)       │    │
│              └────────────────────────────────────────┘    │
│                              │                              │
│                              ▼                              │
│                          Loop back to start                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Microtasks vs Macrotasks

```text
┌─────────────────────────────────────────────────────────────┐
│                MICROTASKS vs MACROTASKS                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  MICROTASKS (High Priority):                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • Promise.then/catch/finally                      │    │
│  │  • queueMicrotask()                                │    │
│  │  • MutationObserver callbacks                      │    │
│  │                                                      │    │
│  │  • Execute after current task completes            │    │
│  │  • ALL microtasks run before next macrotask        │    │
│  │  • Can block rendering if too many                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  MACROTASKS (Normal Priority):                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • setTimeout/setInterval callbacks                │    │
│  │  • I/O operations                                 │    │
│  │  • UI rendering                                   │    │
│  │  • requestAnimationFrame                          │    │
│  │  • MessageChannel                                 │    │
│  │  • postMessage                                    │    │
│  │                                                      │    │
│  │  • One macrotask per event loop iteration          │    │
│  │  • Render happens after macrotasks                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  EXECUTION ORDER:                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  1. Synchronous code (call stack)                  │    │
│  │  2. ALL microtasks                                 │    │
│  │  3. ONE macrotask                                 │    │
│  │  4. Render (if needed)                            │    │
│  │  5. Repeat from step 2                            │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Event Loop

```typescript
console.log('Start');

setTimeout(() => {
  console.log('Timeout 1');
}, 0);

setTimeout(() => {
  console.log('Timeout 2');
}, 0);

Promise.resolve().then(() => {
  console.log('Promise 1');
});

Promise.resolve().then(() => {
  console.log('Promise 2');
});

console.log('End');

// Output:
// Start
// End
// Promise 1
// Promise 2
// Timeout 1
// Timeout 2

// Why?
// 1. Synchronous code runs first: 'Start', 'End'
// 2. Microtasks (Promises) run: 'Promise 1', 'Promise 2'
// 3. Macrotasks (setTimeout) run: 'Timeout 1', 'Timeout 2'
```

### Complex Ordering

```typescript
console.log('1');

setTimeout(() => {
  console.log('2');
}, 0);

Promise.resolve().then(() => {
  console.log('3');
}).then(() => {
  console.log('4');
});

console.log('5');

// Output: 1, 5, 3, 4, 2

// Why?
// 1. Sync: '1', '5'
// 2. Microtask: '3' (first .then)
// 3. Microtask: '4' (second .then, scheduled after first)
// 4. Macrotask: '2'
```

### Nested Promises

```typescript
Promise.resolve().then(() => {
  console.log('Promise 1');

  setTimeout(() => {
    console.log('Timeout 1');
  }, 0);

  Promise.resolve().then(() => {
    console.log('Promise 2');
  });
});

setTimeout(() => {
  console.log('Timeout 2');
}, 0);

// Output:
// Promise 1
// Promise 2
// Timeout 2
// Timeout 1

// Why?
// 1. First Promise runs: 'Promise 1'
// 2. Inside Promise: schedules Timeout 1 and Promise 2
// 3. Promise 2 is microtask, runs before Timeout 2
// 4. Timeout 2 is macrotask, runs after all microtasks
// 5. Timeout 1 is macrotask, runs in next iteration
```

### queueMicrotask

```typescript
console.log('Start');

queueMicrotask(() => {
  console.log('Microtask 1');
});

Promise.resolve().then(() => {
  console.log('Promise 1');
});

queueMicrotask(() => {
  console.log('Microtask 2');
});

console.log('End');

// Output:
// Start
// End
// Microtask 1
// Promise 1
// Microtask 2

// queueMicrotask runs in microtask queue
// Order within microtasks: insertion order
```

### requestAnimationFrame

```typescript
console.log('Start');

requestAnimationFrame(() => {
  console.log('RAF 1');
});

requestAnimationFrame(() => {
  console.log('RAF 2');
});

setTimeout(() => {
  console.log('Timeout');
}, 0);

Promise.resolve().then(() => {
  console.log('Promise');
});

console.log('End');

// Output (varies by browser):
// Start
// End
// Promise
// RAF 1
// RAF 2
// Timeout

// RAF runs before rendering, after microtasks
// Timeout runs after rendering
```

### Async/Await

```typescript
async function example() {
  console.log('Async Start');

  await Promise.resolve();

  console.log('After Await');
}

example();

console.log('End');

// Output:
// Async Start
// End
// After Await

// Why?
// 1. 'Async Start' runs synchronously
// 2. await pauses execution, returns to caller
// 3. 'End' runs synchronously
// 4. Microtask: 'After Await' runs after promise resolves
```

### fetch and Event Loop

```typescript
console.log('Start');

fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => {
    console.log('Data received');
  })
  .catch(error => {
    console.log('Error');
  });

console.log('End');

// Output:
// Start
// End
// Data received (or Error)

// Why?
// 1. 'Start' and 'End' run synchronously
// 2. fetch is Web API, doesn't block
// 3. When fetch completes, .then is queued as microtask
// 4. Microtask runs after current synchronous code
```

### MutationObserver

```typescript
const observer = new MutationObserver((mutations) => {
  console.log('DOM changed');
});

observer.observe(document.body, {
  childList: true,
  subtree: true
);

document.body.innerHTML = '<div>Hello</div>';

// Output: 'DOM changed'
// MutationObserver callback runs as microtask
```

## Real-World Use Cases

### 1. UI Responsiveness

```typescript
// Bad: Blocking UI
function processLargeArray(items: any[]) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);  // Blocks UI
  }
}

// Good: Yield to event loop
async function processLargeArrayAsync(items: any[]) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);

    // Yield every 100 items
    if (i % 100 === 0) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}
```

### 2. Debouncing with Microtasks

```typescript
function debounceMicrotask<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;

  return function(...args: Parameters<T>) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// Or using microtask
function debounceMicro<T extends (...args: any[]) => any>(
  func: T
): (...args: Parameters<T>) => void {
  let pending = false;

  return function(...args: Parameters<T>) {
    if (!pending) {
      pending = true;
      queueMicrotask(() => {
        func(...args);
        pending = false;
      });
    }
  };
}
```

### 3. Animation Timing

```typescript
class Animation {
  private running = false;

  start() {
    this.running = true;
    this.animate();
  }

  animate() {
    if (!this.running) return;

    // Update animation state
    this.update();

    // Schedule next frame
    requestAnimationFrame(() => this.animate());
  }

  update() {
    // Animation logic here
  }

  stop() {
    this.running = false;
  }
}
```

### 4. Data Loading with Priority

```typescript
class DataLoader {
  private cache = new Map<string, any>();
  private pending = new Map<string, Promise<any>>();

  async load(url: string, priority: 'high' | 'low' = 'low') {
    if (this.cache.has(url)) {
      return this.cache.get(url);
    }

    if (this.pending.has(url)) {
      return this.pending.get(url);
    }

    const promise = fetch(url)
      .then(response => response.json())
      .then(data => {
        this.cache.set(url, data);
        this.pending.delete(url);
        return data;
      });

    this.pending.set(url, promise);

    // High priority: use microtask
    if (priority === 'high') {
      await new Promise(resolve => queueMicrotask(resolve));
    }

    return promise;
  }
}
```

### 5. Event Delegation

```typescript
function setupEventDelegation(container: HTMLElement) {
  // Single event listener for all child elements
  container.addEventListener('click', (event) => {
    const target = event.target as HTMLElement;

    // Check if clicked element matches a selector
    if (target.matches('.delete-btn')) {
      handleDelete(target.dataset.id);
    } else if (target.matches('.edit-btn')) {
      handleEdit(target.dataset.id);
    }
  });
}
```

## Common Mistakes

### 1. Assuming setTimeout 0 is Immediate

```typescript
console.log('Start');

setTimeout(() => {
  console.log('Timeout');
}, 0);

console.log('End');

// Output: Start, End, Timeout
// setTimeout 0 doesn't mean "run immediately"
// It means "run after current synchronous code and microtasks"
```

### 2. Blocking the Event Loop

```typescript
// Bad: Long-running synchronous code
function heavyComputation() {
  let sum = 0;
  for (let i = 0; i < 1000000000; i++) {
    sum += i;
  }
  return sum;
}

// This blocks the event loop for seconds
// UI becomes unresponsive

// Good: Break up work
function heavyComputationChunked() {
  let sum = 0;
  let i = 0;

  function processChunk() {
    const chunkSize = 1000000;
    const end = Math.min(i + chunkSize, 1000000000);

    for (; i < end; i++) {
      sum += i;
    }

    if (i < 1000000000) {
      setTimeout(processChunk, 0);
    } else {
      return sum;
    }
  }

  processChunk();
}
```

### 3. Microtask Starvation

```typescript
// Bad: Infinite microtask loop
function microtaskStarvation() {
  queueMicrotask(() => {
    console.log('Microtask');
    microtaskStarvation();  // Keeps adding microtasks
  });
}

// This blocks macrotasks and rendering
// UI freezes

// Good: Use setTimeout for long-running tasks
function goodPattern() {
  queueMicrotask(() => {
    console.log('Microtask');
    if (shouldContinue) {
      setTimeout(goodPattern, 0);  // Use macrotask
    }
  });
}
```

### 4. Forgetting await

```typescript
// Bad: Missing await
async function fetchData() {
  const response = fetch('https://api.example.com');  // Missing await!
  const data = response.json();  // Error: response is Promise
  return data;
}

// Good: Proper await
async function fetchDataFixed() {
  const response = await fetch('https://api.example.com');
  const data = await response.json();
  return data;
}
```

## Best Practices

### 1. Use async/await for Readability

```typescript
// Bad: Promise chains
fetch(url)
  .then(response => response.json())
  .then(data => processData(data))
  .then(result => saveResult(result))
  .catch(error => handleError(error));

// Good: async/await
async function processData() {
  try {
    const response = await fetch(url);
    const data = await response.json();
    const result = await saveResult(data);
    return result;
  } catch (error) {
    handleError(error);
  }
}
```

### 2. Avoid Blocking the Event Loop

```typescript
// Bad: Synchronous heavy computation
function processItems(items: any[]) {
  return items.map(item => heavyComputation(item));
}

// Good: Async processing
async function processItemsAsync(items: any[]) {
  const results = [];
  for (const item of items) {
    results.push(heavyComputation(item));

    // Yield periodically
    if (results.length % 100 === 0) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
  return results;
}
```

### 3. Use Web Workers for Heavy Tasks

```typescript
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ data: largeArray });
worker.onmessage = (event) => {
  console.log('Result:', event.data);
};

// worker.js
self.onmessage = (event) => {
  const result = heavyComputation(event.data);
  self.postMessage(result);
};
```

### 4. Prefer Microtasks for High Priority

```typescript
// Use microtask for high-priority updates
function updateUI(data: any) {
  queueMicrotask(() => {
    renderUI(data);
  });
}

// Use macrotask for low-priority work
function backgroundSync() {
  setTimeout(() => {
    syncData();
  }, 0);
}
```

## Performance Considerations

### Task Timing

```typescript
// Measure task execution time
function measureTask(name: string, fn: () => void) {
  const start = performance.now();
  fn();
  const end = performance.now();
  console.log(`${name}: ${end - start}ms`);
}

// Use for performance profiling
measureTask('Heavy computation', () => {
  heavyComputation();
});
```

### Frame Rate

```typescript
// Monitor frame rate
let lastTime = performance.now();
let frameCount = 0;

function checkFrameRate() {
  frameCount++;
  const currentTime = performance.now();

  if (currentTime - lastTime >= 1000) {
    console.log(`FPS: ${frameCount}`);
    frameCount = 0;
    lastTime = currentTime;
  }

  requestAnimationFrame(checkFrameRate);
}

requestAnimationFrame(checkFrameRate);
```

### Task Scheduling

```typescript
class TaskScheduler {
  private highPriority: (() => void)[] = [];
  private lowPriority: (() => void)[] = [];

  schedule(task: () => void, priority: 'high' | 'low' = 'low') {
    if (priority === 'high') {
      this.highPriority.push(task);
    } else {
      this.lowPriority.push(task);
    }

    this.process();
  }

  private process() {
    queueMicrotask(() => {
      // Process all high priority first
      while (this.highPriority.length > 0) {
        const task = this.highPriority.shift()!;
        task();
      }

      // Then process one low priority
      if (this.lowPriority.length > 0) {
        const task = this.lowPriority.shift()!;
        task();
      }

      // Continue if there are more tasks
      if (this.highPriority.length > 0 || this.lowPriority.length > 0) {
        this.process();
      }
    });
  }
}
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is the event loop in JavaScript?**

A: The event loop is the mechanism that allows JavaScript to perform non-blocking operations. It continuously checks the call stack and callback queues, executing tasks when the stack is empty.

**Q2: Why is JavaScript single-threaded?**

A: JavaScript is single-threaded to simplify programming and avoid concurrency issues like race conditions. The event loop allows it to handle asynchronous operations without blocking.

**Q3: What is the difference between synchronous and asynchronous code?**

A:
- **Synchronous**: Executes immediately, blocks further execution
- **Asynchronous**: Scheduled to run later, allows other code to run

**Q4: What is a callback queue?**

A: The callback queue (or task queue) is where callback functions are placed after their associated asynchronous operations complete (e.g., setTimeout, I/O).

**Q5: What is the call stack?**

A: The call stack is a LIFO data structure that tracks function execution. When a function is called, it's pushed onto the stack; when it returns, it's popped off.

### Intermediate (5-10 questions)

**Q6: What is the difference between microtasks and macrotasks?**

A:
- **Microtasks**: Promise callbacks, queueMicrotask - run after current task, before next macrotask
- **Macrotasks**: setTimeout, I/O - one per event loop iteration

**Q7: Why does `setTimeout(() => {}, 0)` not execute immediately?**

A: Because it's a macrotask. It's queued and runs after:
1. Current synchronous code completes
2. All microtasks complete
3. Rendering (if needed)

**Q8: What is `queueMicrotask` used for?**

A: `queueMicrotask` schedules a function to run in the microtask queue. It's useful for high-priority updates that need to run before the next macrotask or render.

**Q9: How does `requestAnimationFrame` relate to the event loop?**

A: `requestAnimationFrame` runs before the browser paints, after microtasks. It's used for smooth animations and is tied to the browser's refresh rate (typically 60fps).

**Q10: What is microtask starvation?**

A: Microtask starvation occurs when microtasks keep being added faster than they can be processed. This blocks macrotasks and rendering, causing the UI to freeze.

### Senior (10-15 questions)

**Q11: Explain the complete event loop flow in the browser.**

A:
1. Execute synchronous code (call stack)
2. When call stack empty:
   a. Process ALL microtasks
   b. If microtasks added more microtasks, process them too
   c. Process ONE macrotask
   d. Render if needed (every ~16ms)
3. Repeat from step 2

**Q12: How does the event loop differ between browser and Node.js?**

A:
- **Browser**: Single event loop, microtasks then macrotasks, rendering
- **Node.js**: Multiple phases (timers, I/O, poll, check, close callbacks), process.nextTick before microtasks

**Q13: What is `process.nextTick` in Node.js?**

A: `process.nextTick` schedules a callback to run after the current operation completes, before the event loop continues. It has higher priority than microtasks.

**Q14: How do you prevent UI blocking in the browser?**

A:
1. Break up heavy computations into chunks
2. Use `setTimeout` or `requestAnimationFrame` to yield
3. Use Web Workers for CPU-intensive tasks
4. Use `requestIdleCallback` for low-priority work

**Q15: What is the rendering pipeline and how does it relate to the event loop?**

A: The rendering pipeline: JavaScript → Style → Layout → Paint → Composite. The event loop runs JavaScript, then rendering if needed. `requestAnimationFrame` runs before Style.

### FAANG-style (5-10 questions)

**Q16: Design a task scheduler with priority queues.**

A:
```typescript
class TaskScheduler {
  private queues = {
    critical: [] as (() => void)[],
    high: [] as (() => void)[],
    medium: [] as (() => void)[],
    low: [] as (() => void)[]
  };

  schedule(task: () => void, priority: keyof typeof this.queues) {
    this.queues[priority].push(task);
    this.process();
  }

  private process() {
    queueMicrotask(() => {
      // Process in priority order
      for (const priority of ['critical', 'high', 'medium', 'low']) {
        if (this.queues[priority].length > 0) {
          const task = this.queues[priority].shift()!;
          task();
          break;
        }
      }

      // Continue if tasks remain
      if (Object.values(this.queues).some(q => q.length > 0)) {
        this.process();
      }
    });
  }
}
```

**Q17: How would you implement a non-blocking deep clone?**

A:
```typescript
async function deepCloneAsync<T>(obj: T): Promise<T> {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    const clone = [];
    for (let i = 0; i < obj.length; i++) {
      clone[i] = await deepCloneAsync(obj[i]);

      // Yield every 100 items
      if (i % 100 === 0) {
        await new Promise(resolve => setTimeout(resolve, 0));
      }
    }
    return clone as T;
  }

  const clone = {} as T;
  const keys = Object.keys(obj);
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i];
    (clone as any)[key] = await deepCloneAsync((obj as any)[key]);

    // Yield periodically
    if (i % 100 === 0) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }

  return clone;
}
```

**Q18: Analyze the performance implications of microtasks vs macrotasks.**

A:
- **Microtasks**: Run immediately after current task, block rendering
- **Macrotasks**: Run in separate iterations, allow rendering between

Use microtasks for: High-priority updates, state synchronization
Use macrotasks for: Low-priority work, animations, UI updates

**Q19: How do you debug event loop issues?**

A:
1. **Chrome DevTools**: Performance tab, flame chart
2. **console.trace()**: See call stack
3. **Performance API**: measureTask, performance.now()
4. **requestAnimationFrame**: Monitor frame rate
5. **Web Workers**: Isolate heavy computations

**Q20: What are the security implications of the event loop?**

A:
1. **Timing attacks**: Measure task execution time
2. **DoS**: Starve microtask queue
3. **Information leakage**: Task scheduling reveals code structure
4. **Mitigation**: Limit task frequency, use rate limiting

### Follow-ups (5-10 questions)

**Q21: Can you give an example of an event loop bug in production?**

A: Common bug: Microtask starvation
```typescript
// Bug: Infinite microtask loop
function processData(data: any[]) {
  queueMicrotask(() => {
    processItem(data[0]);
    if (data.length > 1) {
      processData(data.slice(1));  // Adds more microtasks
    }
  });
}

// This blocks UI because microtasks never stop
// Fix: Use setTimeout for long-running tasks
```

**Q22: How do you handle event loop delays in production?**

A:
1. Monitor task execution time
2. Use performance APIs to measure delays
3. Break up long-running tasks
4. Use Web Workers for heavy computations
5. Implement task scheduling with priorities

**Q23: What is the relationship between event loop and Web Workers?**

A: Web Workers have their own event loops and call stacks. They communicate via messages, not shared memory. The main thread's event loop is unaffected by worker operations.

**Q24: How do different frameworks handle the event loop?**

A:
- **React**: Uses microtasks for state updates, batch processing
- **Vue**: NextTick for DOM updates, microtask-based
- **Angular**: Zone.js patches async operations
- **Svelte**: Compiled to efficient async operations

**Q25: What are best practices for working with the event loop?**

A:
1. Use async/await for readability
2. Avoid blocking the event loop
3. Use Web Workers for heavy tasks
4. Prefer microtasks for high-priority work
5. Monitor frame rate and task timing
6. Break up long-running operations
7. Use requestAnimationFrame for animations
8. Implement proper error handling

## Summary

The event loop is fundamental to JavaScript:

1. **Single-threaded**: Uses event loop for concurrency
2. **Two queues**: Microtasks (high priority) and macrotasks (low priority)
3. **Execution order**: Sync → Microtasks → Macrotask → Render
4. **Non-blocking**: Allows handling multiple operations
5. **Performance**: Don't block the event loop
6. **Debugging**: Use DevTools and performance APIs
7. **Best practices**: Use async/await, Web Workers, proper scheduling

Understanding the event loop is essential for writing responsive, efficient JavaScript applications.

## Cheat Sheet

```text
EVENT LOOP CHEAT SHEET
═══════════════════════════════════════════════════════════════

BROWSER ARCHITECTURE:
• Call Stack: Synchronous execution
• Web APIs: setTimeout, fetch, DOM
• Microtask Queue: Promises, queueMicrotask
• Macrotask Queue: setTimeout, I/O, rendering

EXECUTION ORDER:
1. Synchronous code (call stack)
2. ALL microtasks
3. ONE macrotask
4. Render (if needed)
5. Repeat

MICROTASKS (High Priority):
• Promise.then/catch/finally
• queueMicrotask()
• MutationObserver
• Run after current task, before next macrotask

MACROTASKS (Normal Priority):
• setTimeout/setInterval
• I/O operations
• UI rendering
• requestAnimationFrame
• One per event loop iteration

KEY BEHAVIORS:
• setTimeout 0 ≠ immediate
• Microtasks block rendering
• requestAnimationFrame runs before paint
• process.nextTick (Node.js) > microtasks

COMMON MISTAKES:
• Assuming setTimeout 0 is immediate
• Blocking event loop with heavy computation
• Microtask starvation
• Forgetting await

PERFORMANCE:
• Don't block event loop
• Use Web Workers for heavy tasks
• Break up long-running operations
• Monitor frame rate

DEBUGGING:
• Chrome DevTools: Performance tab
• console.trace(): Call stack
• performance.now(): Timing
• requestAnimationFrame(): Frame rate

BEST PRACTICES:
• Use async/await
• Avoid blocking operations
• Use Web Workers
• Prefer microtasks for high priority
• Implement task scheduling
```

## References & Learn More

- [MDN: Concurrency Model and the Event Loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)
- [JavaScript.info: Event Loop](https://javascript.info/event-loop)
- [Jake Archibald: Tasks, microtasks, queues and schedules](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/)
- [Node.js: Event Loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop)
- [Latent Flip: What the heck is the event loop anyway?](https://latentflip.com/loupe/)
