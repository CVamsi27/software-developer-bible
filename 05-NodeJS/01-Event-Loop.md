# Node.js Event Loop

## Definition

The **Event Loop** is the core mechanism in Node.js that enables non-blocking I/O operations despite JavaScript being single-threaded. It continuously monitors the call stack and callback queues, executing callbacks when the stack is empty and events are available. Node.js implements the event loop using **libuv**, a C library that provides the underlying event loop and async I/O operations.

## Why Do We Need It?

JavaScript is single-threaded, meaning it can only execute one piece of code at a time. Without the event loop, operations like file I/O, network requests, or database queries would block the entire thread, making Node.js unsuitable for high-concurrency applications. The event loop allows Node.js to:

- Handle thousands of concurrent connections on a single thread
- Perform non-blocking I/O operations
- Scale efficiently with minimal memory overhead
- Process callbacks asynchronously without blocking the main thread

## How It Works

The event loop runs through several **phases** in a specific order. Each phase has its own queue of callbacks to execute.

### Event Loop Phases (in order)

```
   ┌───────────────────────────┐
┌─>│         TIMERS            │  ← setTimeout(), setInterval()
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     PENDING I/O           │  ← callbacks from I/O (e.g., TCP errors)
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       POLL                 │  ← retrieve new I/O events; execute I/O callbacks
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │        CHECK              │  ← setImmediate()
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │    CLOSE CALLBACKS        │  ← sockets.on('close', ...)
│  └─────────────┬─────────────┘
└─────────────────┘
```

### Detailed Phase Breakdown

```
┌───────────────────────────────────────────────────────────────┐
│                        PHASE 1: TIMERS                       │
├───────────────────────────────────────────────────────────────┤
│ • Executes setTimeout() and setInterval() callbacks          │
│ • Processes callbacks whose scheduled time has been reached  │
│ • Note: setTimeout(cb, 0) is not exactly 0ms; minimum ~1ms   │
└───────────────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────────┐
│                    PHASE 2: PENDING I/O                      │
├───────────────────────────────────────────────────────────────┤
│ • Executes callbacks for some system operations              │
│ • E.g., TCP errors like ECONNREFUSED (emitted on next tick)  │
│ • Limited to a fixed number of callbacks per iteration       │
└───────────────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────────┐
│                        PHASE 3: POLL                         │
├───────────────────────────────────────────────────────────────┤
│ • Block here waiting for new I/O events                      │
│ • Process callbacks from completed I/O operations            │
│ • Node checks for timers, then processes ready I/O events    │
│ • Will check for close callbacks, and check for timers       │
│ • If nothing to do: will wait for I/O callbacks or exit      │
└───────────────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────────┐
│                       PHASE 4: CHECK                         │
├───────────────────────────────────────────────────────────────┤
│ • Executes setImmediate() callbacks                          │
│ • setImmediate() is designed for executing code after the    │
│   poll phase completes                                       │
└───────────────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────────┐
│                   PHASE 5: CLOSE CALLBACKS                   │
├───────────────────────────────────────────────────────────────┤
│ • Executes close event callbacks                             │
│ • E.g., socket.on('close', ...)                              │
│ • Handles cleanup of resources                               │
└───────────────────────────────────────────────────────────────┘
```

### Microtasks: process.nextTick and Promise

```
┌───────────────────────────────────────────────────────────────┐
│                    MICROTASK QUEUES                          │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  process.nextTick queue:                                     │
│  • Highest priority among all microtasks                     │
│  • Executed BEFORE any other phase callbacks                 │
│  • Can starve the event loop if recursive                    │
│                                                              │
│  Promise microtask queue:                                    │
│  • Executes resolved Promise .then() callbacks               │
│  • Processed AFTER nextTick queue                            │
│                                                              │
│  Priority Order:                                             │
│  1. process.nextTick (always first)                          │
│  2. Promise microtasks                                       │
│  3. Event loop phases (timers, poll, etc.)                   │
│                                                              │
└───────────────────────────────────────────────────────────────┘
```

### setImmediate vs setTimeout(0)

```
┌───────────────────────────────────────────────────────────────┐
│              setImmediate vs setTimeout(0)                   │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  setTimeout(0):                                              │
│  • Callback queued in the TIMERS phase                       │
│  • Executes in the next timers check                         │
│  • Minimum delay is 1ms (even if 0 is passed)               │
│                                                              │
│  setImmediate():                                             │
│  • Callback queued in the CHECK phase                        │
│  • Executes after the POLL phase                             │
│  • Executes after I/O operations complete                    │
│                                                              │
│  Execution Order (outside I/O callback):                     │
│  setTimeout(() => console.log('timeout'))                    │
│  setImmediate(() => console.log('immediate'))                │
│  // Output varies: timeout or immediate can come first      │
│                                                              │
│  Execution Order (inside I/O callback):                      │
│  const fs = require('fs');                                   │
│  fs.readFile('file.txt', () => {                             │
│    setTimeout(() => console.log('timeout'), 0);              │
│    setImmediate(() => console.log('immediate'));              │
│  });                                                        │
│  // Output: always "immediate" then "timeout"               │
│                                                              │
└───────────────────────────────────────────────────────────────┘
```

### Concurrency Handling Flow

```
┌───────────────────────────────────────────────────────────────┐
│                  HOW NODE HANDLES CONCURRENCY                 │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│   Call Stack                                                 │
│   ┌─────────────────────┐                                    │
│   │   execute(request)  │                                    │
│   │   └─> readDB()      │ ─── Libuv Thread Pool ──> async   │
│   │   └─> sendEmail()   │ ─── Libuv Thread Pool ──> async   │
│   │   └─> writeLog()    │ ─── OS Async I/O ──────> async    │
│   └─────────────────────┘                                    │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────────────┐                                    │
│   │   Event Loop        │                                    │
│   │   (libuv)           │ ──── Thread Pool ──> Callbacks    │
│   └─────────────────────┘                                    │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────────────┐                                    │
│   │   Callback Queue    │                                    │
│   │   [cb1] [cb2] [cb3]│ ──── Processed after stack empty  │
│   └─────────────────────┘                                    │
│                                                              │
└───────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Event Loop Demonstration

```typescript
// event-loop-basics.ts

console.log('1. Start');

// setTimeout - TIMERS phase
setTimeout(() => {
  console.log('2. setTimeout callback (TIMERS phase)');
}, 0);

// setImmediate - CHECK phase
setImmediate(() => {
  console.log('3. setImmediate callback (CHECK phase)');
});

// process.nextTick - highest priority microtask
process.nextTick(() => {
  console.log('4. process.nextTick callback');
});

// Promise - microtask
Promise.resolve().then(() => {
  console.log('5. Promise resolved');
});

console.log('6. End');

// Output:
// 1. Start
// 6. End
// 4. process.nextTick callback
// 5. Promise resolved
// 2. setTimeout callback (TIMERS phase)
// 3. setImmediate callback (CHECK phase)
```

### setImmediate vs setTimeout(0) Inside I/O

```typescript
// immediate-vs-timeout.ts

import * as fs from 'fs';

// Inside an I/O callback, setImmediate always runs before setTimeout(0)
fs.readFile('package.json', () => {
  setTimeout(() => {
    console.log('setTimeout(0) - TIMERS phase');
  }, 0);

  setImmediate(() => {
    console.log('setImmediate - CHECK phase');
  });
});
// Output: setImmediate always runs first
```

### Microtask Priority

```typescript
// microtask-priority.ts

const fs = require('fs');

fs.readFile('package.json', () => {
  // Macrotask (I/O callback)
  console.log('1. I/O callback');

  process.nextTick(() => {
    console.log('2. process.nextTick');
  });

  Promise.resolve().then(() => {
    console.log('3. Promise');
  });

  setTimeout(() => {
    console.log('4. setTimeout');
  }, 0);

  setImmediate(() => {
    console.log('5. setImmediate');
  });
});

// Output:
// 1. I/O callback
// 2. process.nextTick
// 3. Promise
// 5. setImmediate
// 4. setTimeout
```

### Event Loop Blocking Example

```typescript
// blocking-example.ts

import * as http from 'http';

const server = http.createServer((req, res) => {
  // BAD: Blocking the event loop
  const start = Date.now();
  while (Date.now() - start < 5000) {
    // Simulating CPU-intensive work
    // This blocks the entire event loop!
  }
  res.end('Done after 5 seconds');
});

// Good: Non-blocking approach using setImmediate
const serverNonBlocking = http.createServer(async (req, res) => {
  if (req.url === '/process') {
    // Yield to event loop, allowing other requests
    await new Promise<void>((resolve) => {
      setImmediate(resolve);
    });

    // Perform CPU-intensive work in chunks
    await processInChunks();

    res.end('Processed');
  }
});

function processInChunks(): Promise<void> {
  let processed = 0;
  const total = 1000000;

  return new Promise((resolve) => {
    function chunk() {
      const start = Date.now();
      while (processed < total && Date.now() - start < 10) {
        // Process items for up to 10ms
        processed++;
      }

      if (processed < total) {
        // Yield to event loop and continue later
        setImmediate(chunk);
      } else {
        resolve();
      }
    }
    chunk();
  });
}

server.listen(3000);
```

### Real Event Loop Phases in Action

```typescript
// phases-in-action.ts

import * as fs from 'fs';

console.log('=== Event Loop Phases Demo ===');

// Timer phase
setTimeout(() => {
  console.log('[TIMERS] setTimeout callback');
}, 100);

// Check phase
setImmediate(() => {
  console.log('[CHECK] setImmediate callback');
});

// Microtasks
process.nextTick(() => {
  console.log('[MICROTASK] nextTick - before I/O');
});

Promise.resolve().then(() => {
  console.log('[MICROTASK] Promise - before I/O');
});

// Simulate I/O operation
fs.readFile(__filename, () => {
  // After I/O completes

  console.log('\n--- Inside I/O callback ---');

  // These will execute in order within this phase
  process.nextTick(() => {
    console.log('[MICROTASK] nextTick - inside I/O');
  });

  Promise.resolve().then(() => {
    console.log('[MICROTASK] Promise - inside I/O');
  });

  setTimeout(() => {
    console.log('[TIMERS] setTimeout - inside I/O');
  }, 0);

  setImmediate(() => {
    console.log('[CHECK] setImmediate - inside I/O');
  });

  // Close callback
  fs.createReadStream(__filename)
    .on('data', () => {})
    .on('end', () => {
      console.log('[CLOSE] stream close callback');
    });
});
```

### Custom Event Emitter with Event Loop

```typescript
// event-emitter-loop.ts

import { EventEmitter } from 'events';

class TaskScheduler extends EventEmitter {
  private queue: Array<{ task: Function; priority: number }> = [];
  private processing = false;

  addTask(task: Function, priority: number = 0) {
    this.queue.push({ task, priority });
    this.queue.sort((a, b) => b.priority - a.priority);

    if (!this.processing) {
      this.scheduleProcessing();
    }
  }

  private scheduleProcessing() {
    // Use setImmediate to yield to event loop between tasks
    setImmediate(() => this.processNext());
  }

  private processNext() {
    if (this.queue.length === 0) {
      this.processing = false;
      this.emit('drain');
      return;
    }

    this.processing = true;
    const task = this.queue.shift()!;

    try {
      const result = task.task();
      this.emit('task-complete', result);

      // Schedule next task
      this.scheduleProcessing();
    } catch (error) {
      this.emit('task-error', error);
      this.scheduleProcessing();
    }
  }
}

const scheduler = new TaskScheduler();

scheduler.on('task-complete', (result) => {
  console.log('Task completed:', result);
});

scheduler.on('drain', () => {
  console.log('All tasks completed');
});

// Add tasks
scheduler.addTask(() => 'Task 1', 1);
scheduler.addTask(() => 'Task 2', 2);
scheduler.addTask(() => 'Task 3', 1);
```

## Real-World Use Cases

### 1. HTTP Server Request Handling

```typescript
// Production HTTP server
import * as http from 'http';
import * as cluster from 'cluster';

const server = http.createServer(async (req, res) => {
  // Event loop phases handle:
  // - Connection establishment (POLL phase)
  // - Request data parsing (POLL phase)
  // - Response writing (POLL phase)

  // Use process.nextTick for cleanup
  process.nextTick(() => {
    // Cleanup logic runs before next request
  });

  // Handle request
  const data = await handleRequest(req);
  res.end(JSON.stringify(data));
});

function handleRequest(req: http.IncomingMessage): Promise<any> {
  return new Promise((resolve) => {
    // Simulate async DB operation
    setTimeout(() => resolve({ status: 'ok' }), 10);
  });
}
```

### 2. Rate Limiter Using Event Loop

```typescript
// rate-limiter.ts

class RateLimiter {
  private requests: number[] = [];
  private maxRequests: number;
  private windowMs: number;

  constructor(maxRequests: number, windowMs: number) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
  }

  isAllowed(): boolean {
    const now = Date.now();
    const windowStart = now - this.windowMs;

    // Remove old requests outside window
    this.requests = this.requests.filter(
      (timestamp) => timestamp > windowStart
    );

    if (this.requests.length < this.maxRequests) {
      this.requests.push(now);
      return true;
    }

    return false;
  }
}

const limiter = new RateLimiter(100, 60000); // 100 requests per minute

const server = http.createServer((req, res) => {
  if (!limiter.isAllowed()) {
    res.writeHead(429);
    res.end('Too Many Requests');
    return;
  }
  // Process request
  res.end('OK');
});
```

### 3. Graceful Shutdown

```typescript
// graceful-shutdown.ts

import * as http from 'http';
import * as net from 'net';

let isShuttingDown = false;
const server = http.createServer((req, res) => {
  if (isShuttingDown) {
    res.writeHead(503);
    res.end('Service Unavailable');
    return;
  }
  // Handle request
  res.end('OK');
});

process.on('SIGTERM', () => {
  console.log('Received SIGTERM, shutting down gracefully...');
  isShuttingDown = true;

  // Stop accepting new connections
  server.close(() => {
    console.log('All connections closed');

    // Use nextTick for final cleanup
    process.nextTick(() => {
      process.exit(0);
    });
  });

  // Force close after timeout
  setTimeout(() => {
    console.error('Forced shutdown due to timeout');
    process.exit(1);
  }, 30000);
});
```

## Common Mistakes

### 1. Blocking the Event Loop

```typescript
// BAD: CPU-intensive operation blocks event loop
app.get('/compute', (req, res) => {
  let result = 0;
  for (let i = 0; i < 1e9; i++) {
    result += i;
  }
  res.json({ result });
});

// GOOD: Use worker threads or break into chunks
import { Worker } from 'worker_threads';

app.get('/compute', (req, res) => {
  const worker = new Worker('./compute-worker.js', {
    workerData: { iterations: 1e9 },
  });

  worker.on('message', (result) => {
    res.json({ result });
  });

  worker.on('error', (error) => {
    res.status(500).json({ error: error.message });
  });
});
```

### 2. Using process.nextTick Recursively

```typescript
// BAD: Starves the event loop
function processAll() {
  process.nextTick(() => {
    // This creates infinite recursive nextTicks
    // No I/O, setTimeout, or setImmediate callbacks will run
    processAll();
  });
}

// GOOD: Use setImmediate for recursive async work
function processAllSafe() {
  setImmediate(() => {
    // This allows I/O and other phases to execute
    processAllSafe();
  });
}
```

### 3. Not Handling Unhandled Rejections

```typescript
// BAD: No handler for unhandled promise rejections
Promise.reject(new Error('Something failed'));

// GOOD: Always handle rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  // Optionally exit process
  // process.exit(1);
});

Promise.reject(new Error('Something failed'));
```

### 4. Misunderstanding setTimeout Minimum Delay

```typescript
// The 0ms timeout is not exactly 0ms
setTimeout(() => {
  console.log('This runs after at least ~1ms');
}, 0);

// In practice, delays can be longer depending on system load
// Never use setTimeout(fn, 0) for precise timing
```

### 5. Not Using setImmediate for I/O Callbacks

```typescript
// BAD: setTimeout(0) inside I/O
fs.readFile('file.txt', () => {
  setTimeout(() => {
    // This may execute before setImmediate
  }, 0);
});

// GOOD: Use setImmediate for post-I/O work
fs.readFile('file.txt', () => {
  setImmediate(() => {
    // This executes in the CHECK phase after POLL
  });
});
```

## Best Practices

### 1. Understand Phase Ordering

```typescript
// Remember the order: timers → pending → poll → check → close
// process.nextTick and Promise microtasks run between phases
```

### 2. Use setImmediate for Chunked Processing

```typescript
// Process large datasets without blocking
async function processLargeDataset(items: any[]) {
  const CHUNK_SIZE = 1000;
  let index = 0;

  return new Promise<void>((resolve) => {
    function processChunk() {
      const start = index;
      const end = Math.min(start + CHUNK_SIZE, items.length);

      for (let i = start; i < end; i++) {
        // Process item
        processItem(items[i]);
      }

      index = end;

      if (index < items.length) {
        setImmediate(processChunk); // Yield to event loop
      } else {
        resolve();
      }
    }

    processChunk();
  });
}
```

### 3. Monitor Event Loop Lag

```typescript
// Monitor event loop lag
function monitorEventLoop() {
  const start = process.hrtime.bigint();

  setInterval(() => {
    const delay = Number(process.hrtime.bigint() - start) / 1e6;
    const lag = delay - 1000; // Expected 1000ms interval

    if (lag > 100) {
      console.warn(`Event loop lag: ${lag.toFixed(2)}ms`);
    }

    // Reset for next measurement
    start = process.hrtime.bigint();
  }, 1000);
}
```

### 4. Prefer Async/Await Over Callbacks

```typescript
// Modern approach: async/await
async function fetchData() {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}
```

### 5. Handle Backpressure in Streams

```typescript
import { createReadStream, createWriteStream } from 'fs';

const readStream = createReadStream('large-file.txt');
const writeStream = createWriteStream('output.txt');

readStream.on('data', (chunk) => {
  // Check if we should pause
  if (!writeStream.write(chunk)) {
    readStream.pause();
    writeStream.once('drain', () => {
      readStream.resume();
    });
  }
});
```

## Performance Considerations

### 1. Thread Pool Size Configuration

```typescript
// Default thread pool size is 4
// Increase for CPU-bound operations
process.env.UV_THREADPOOL_SIZE = '8';

// Or set before starting the application
// UV_THREADPOOL_SIZE=8 node app.js
```

### 2. Event Loop Monitoring

```typescript
import { monitorEventLoopDelay } from 'perf_hooks';

const histogram = monitorEventLoopDelay({ resolution: 20 });
histogram.enable();

// Collect metrics every 5 seconds
setInterval(() => {
  console.log({
    min: histogram.min / 1e6,
    max: histogram.max / 1e6,
    mean: histogram.mean / 1e6,
    p99: histogram.percentile(99) / 1e6,
  });
  histogram.reset();
}, 5000);
```

### 3. Memory Usage Tracking

```typescript
function getMemoryUsage() {
  const usage = process.memoryUsage();
  return {
    rss: `${(usage.rss / 1024 / 1024).toFixed(2)} MB`,
    heapTotal: `${(usage.heapTotal / 1024 / 1024).toFixed(2)} MB`,
    heapUsed: `${(usage.heapUsed / 1024 / 1024).toFixed(2)} MB`,
    external: `${(usage.external / 1024 / 1024).toFixed(2)} MB`,
  };
}
```

## Interview Questions

### Beginner

1. **What is the event loop in Node.js?**
   - The event loop is the mechanism that enables non-blocking I/O in Node.js. It continuously monitors the call stack and callback queues, executing callbacks when the stack is empty and events are available.

2. **Name the phases of the event loop.**
   - Timers, Pending I/O, Poll, Check, Close Callbacks.

3. **What is the difference between setTimeout and setImmediate?**
   - setTimeout schedules a callback in the timers phase, while setImmediate schedules in the check phase. Inside I/O callbacks, setImmediate always runs before setTimeout(0).

4. **What is process.nextTick?**
   - process.nextTick schedules a callback to run before the event loop continues. It has the highest priority among microtasks.

5. **Can Node.js handle multiple concurrent connections?**
   - Yes, through the event loop's non-blocking I/O model, Node.js can handle thousands of concurrent connections on a single thread.

6. **What is a callback queue?**
   - The callback queue is where callbacks wait after being triggered by async operations. The event loop processes these callbacks when the call stack is empty.

7. **How does Node.js achieve non-blocking I/O?**
   - Node.js offloads I/O operations to the system kernel or thread pool (via libuv), allowing the event loop to continue processing other tasks while I/O completes.

8. **What is libuv?**
   - libuv is a C library that provides the event loop implementation, thread pool, and async I/O operations for Node.js.

9. **What is a microtask?**
   - A microtask is a high-priority task (like process.nextTick or Promise callbacks) that runs before the event loop continues to the next phase.

10. **What happens when you call setTimeout with 0ms delay?**
    - The callback is queued in the timers phase, but the minimum delay is actually ~1ms due to system timer resolution.

### Intermediate

11. **What is event loop starvation and how does it occur?**
    - Event loop starvation happens when synchronous or long-running tasks block the event loop, preventing callbacks from being processed. This can occur with CPU-intensive operations or recursive process.nextTick calls.

12. **Explain the order of execution when multiple async operations are queued.**
    - process.nextTick > Promise microtasks > timers > pending I/O > poll > check > close. Microtasks always run before the event loop progresses to the next phase.

13. **How would you handle a CPU-intensive task without blocking the event loop?**
    - Use worker threads, child processes, or break the task into smaller chunks with setImmediate between them. This allows the event loop to continue processing.

14. **What is the difference between process.nextTick and setImmediate?**
    - process.nextTick runs before the event loop continues to the next phase (microtask), while setImmediate runs in the check phase (macrotask). nextTick has higher priority.

15. **How does Node.js handle errors in async operations?**
    - Errors in async operations are caught through error-first callbacks or Promise.catch(). Unhandled rejections trigger the 'unhandledRejection' event.

16. **What is the purpose of the poll phase?**
    - The poll phase retrieves new I/O events, executes I/O callbacks, and determines when to block for new I/O. It balances between processing callbacks and waiting for new events.

17. **How can you monitor event loop lag?**
    - Use setInterval to measure actual vs expected execution time, or use the perf_hooks.monitorEventLoopDelay() API for accurate measurements.

18. **What is the maximum number of callbacks Node.js processes per event loop iteration?**
    - It depends on the phase. For example, the poll phase processes up to a fixed number of I/O callbacks before moving to the check phase.

19. **Explain the relationship between libuv thread pool and the event loop.**
    - The libuv thread pool handles CPU-intensive and blocking operations off the main event loop thread. When these operations complete, callbacks are queued back to the event loop.

20. **What happens if you use process.nextTick inside a loop?**
    - It can starve the event loop because process.nextTick callbacks are processed before any other phase. Use setImmediate instead for recursive async work.

### Senior

21. **How would you design a system to handle 100K concurrent WebSocket connections?**
    - Use clustering for multi-core utilization, implement connection pooling, use efficient memory management, implement heartbeat mechanisms, and consider load balancers with sticky sessions.

22. **Explain how Node.js handles backpressure in streams.**
    - Backpressure occurs when readable stream produces data faster than writable can consume. Node.js handles this through pause/resume mechanisms, highWaterMark, and drain events.

23. **How would you debug an event loop performance issue in production?**
    - Use --inspect flag with Chrome DevTools, monitor event loop lag with perf_hooks, analyze CPU profiles, check for memory leaks, and use APM tools.

24. **What are the trade-offs between using process.nextTick vs setImmediate?**
    - nextTick has higher priority but can starve the event loop. setImmediate is safer but runs later. Use nextTick for critical cleanup, setImmediate for non-critical async work.

25. **How would you implement a rate limiter using the event loop?**
    - Use timestamps to track requests within a time window, implement sliding window algorithm, and use setImmediate to avoid blocking during cleanup.

26. **Explain the performance implications of Promise.all vs sequential awaits.**
    - Promise.all runs operations concurrently, reducing total wait time. Sequential awaits execute one after another, which is slower but uses fewer resources and is easier to debug.

27. **How would you handle memory leaks in long-running Node.js applications?**
    - Monitor heap usage, use --expose-gc for manual garbage collection, implement memory leak detection with tools like memwatch-next, and regularly profile memory usage.

28. **What is the impact of V8's garbage collection on the event loop?**
    - V8's GC can cause pauses, especially minor GCs. These pauses block the event loop. Optimize by reducing object allocations and using object pooling.

29. **How would you implement a work queue system with backpressure?**
    - Use a bounded queue with configurable capacity, implement producer-consumer pattern, and pause producers when queue is full using stream backpressure mechanisms.

30. **Explain the event loop behavior in clustered vs single-process mode.**
    - Each worker has its own event loop. The master process distributes connections using round-robin or OS-level scheduling. Workers don't share memory, communicating via IPC.

### FAANG-style

31. **Design a chat application supporting 1M concurrent users with Node.js.**
    - Use clustering, sticky sessions for WebSocket, Redis pub/sub for message broadcasting, horizontal scaling with load balancers, and implement connection pooling with heartbeat monitoring.

32. **How would you implement a distributed task queue using Node.js event loop concepts?**
    - Use Redis/RabbitMQ for task distribution, implement worker pools with concurrency control, add retry logic with exponential backoff, and monitor task processing time.

33. **Explain how to optimize Node.js for high-throughput HTTP APIs.**
    - Use clustering, implement caching layers, optimize database queries, use HTTP/2, implement connection pooling, enable gzip compression, and use efficient serialization.

34. **How would you handle graceful shutdown in a distributed system?**
    - Implement health check endpoints, use process.nextTick for cleanup, implement connection draining, use load balancer deregistration, and handle in-flight requests.

35. **Design a real-time data processing pipeline with Node.js.**
    - Use streams for data flow, implement backpressure handling, use worker threads for CPU-intensive operations, implement checkpointing for fault tolerance, and monitor processing latency.

36. **How would you implement a circuit breaker pattern in Node.js?**
    - Track failure rates, implement state machine (closed/open/half-open), use timers for reset periods, integrate with event loop phases, and add fallback mechanisms.

37. **Explain how to achieve zero-downtime deployments with Node.js.**
    - Use graceful shutdown, implement health checks, use load balancer deregistration, implement session persistence, and coordinate with process managers.

38. **How would you optimize Node.js memory usage in production?**
    - Use stream processing for large data, implement object pooling, optimize V8 garbage collection, use weak references for caching, and monitor heap usage.

39. **Design a WebSocket server supporting 100K concurrent connections.**
    - Use clustering, implement connection pooling, use Redis for pub/sub, implement heartbeat monitoring, optimize buffer usage, and handle backpressure.

40. **How would you implement distributed tracing in a Node.js microservices architecture?**
    - Use OpenTelemetry, propagate trace context via HTTP headers, implement span creation, collect metrics, and integrate with monitoring systems.

### Follow-ups

41. **How does Node.js handle I/O operations differently from CPU-bound operations?**
    - I/O operations are offloaded to the system kernel or thread pool, while CPU-bound operations block the main thread. Use worker threads for CPU-intensive tasks.

42. **What happens when you mix process.nextTick and setImmediate in a loop?**
    - process.nextTick callbacks will execute first, potentially starving the event loop. setImmediate allows other phases to process between iterations.

43. **How would you implement a custom event loop monitor?**
    - Use setInterval to measure execution timing, implement histogram for lag distribution, track phase-specific metrics, and export to monitoring systems.

44. **Explain the memory model implications of closures in async code.**
    - Closures capture variables by reference, preventing garbage collection. This can cause memory leaks if not managed properly, especially in long-running applications.

45. **How does Node.js handle signal handling in the event loop?**
    - Signals are processed outside the event loop using libuv's signal handling. They interrupt the current operation and execute signal handlers synchronously.

46. **What is the impact of DNS resolution on the event loop?**
    - DNS resolution can block the event loop if not async. Use dns.lookup() for cached results or dns.resolve() for fresh resolution.

47. **How would you implement a connection pool with backpressure support?**
    - Use a bounded pool, implement request queuing, add timeout mechanisms, monitor pool utilization, and implement pool resizing based on load.

48. **Explain how to debug event loop delays in production.**
    - Use --inspect with Chrome DevTools, implement custom monitoring with perf_hooks, analyze CPU profiles, and use APM tools for distributed tracing.

49. **How does Node.js handle concurrent file I/O operations?**
    - File I/O uses the libuv thread pool for async operations. The thread pool size limits concurrent file operations. Increase UV_THREADPOOL_SIZE for more concurrency.

50. **What are the trade-offs between using cluster vs worker threads?**
    - Cluster provides process isolation and multi-core utilization. Worker threads share memory and have lower overhead. Use cluster for I/O-bound, worker threads for CPU-bound.

## Summary

The Node.js event loop is the foundation of its non-blocking I/O architecture. Understanding the phases, microtasks, and how to avoid blocking is crucial for building performant applications. Key takeaways:

- The event loop has 5 main phases: timers, pending I/O, poll, check, close
- process.nextTick has highest priority but can cause starvation
- setImmediate is safer for recursive async work
- Always monitor event loop lag in production
- Use worker threads for CPU-intensive operations
- Understand the trade-offs between different async patterns

## Cheat Sheet

```
┌───────────────────────────────────────────────────────────────┐
│                    EVENT LOOP CHEAT SHEET                    │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  PHASES (in order):                                          │
│  1. TIMERS: setTimeout(), setInterval()                      │
│  2. PENDING I/O: error callbacks, TCP errors                 │
│  3. POLL: I/O callbacks, blocking when no work               │
│  4. CHECK: setImmediate()                                    │
│  5. CLOSE CALLBACKS: socket.on('close')                      │
│                                                              │
│  MICROTASKS (run between phases):                            │
│  • process.nextTick() - highest priority                     │
│  • Promise.then() - second priority                          │
│                                                              │
│  KEY RULES:                                                  │
│  • nextTick always before setImmediate                       │
│  • Inside I/O: setImmediate before setTimeout(0)             │
│  • Never use recursive nextTick - use setImmediate           │
│  • setTimeout minimum delay is ~1ms                          │
│                                                              │
│  DEBUGGING:                                                  │
│  • node --inspect server.js                                  │
│  • perf_hooks.monitorEventLoopDelay()                        │
│  • process.hrtime.bigint() for precise timing                │
│                                                              │
│  COMMON PATTERNS:                                            │
│  • Chunked processing: setImmediate between chunks           │
│  • Backpressure: pause/resume streams                        │
│  • Graceful shutdown: process.nextTick for cleanup           │
│                                                              │
│  WATCH OUT:                                                  │
│  • Event loop starvation from CPU-bound tasks                │
│  • Memory leaks from closures                                │
│  • Unhandled promise rejections                              │
│  • DNS resolution blocking                                   │
│                                                              │
└───────────────────────────────────────────────────────────────┘
```

## References & Learn More

- [Node.js Event Loop Docs](https://nodejs.org/en/learn/asynchronous-work/the-nodejs-event-loop)
- [Node.js Event Loop Phases](https://docs.libuv.org/en/latest/guide/design.html)
- [libuv Documentation](https://docs.libuv.org/)
- [Node.js Timers Docs](https://nodejs.org/api/timers.html)