---
section: Node.js
category: Backend
tags: [concept]
---

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

```text
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

```text
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

```text
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

```text
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

```text
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

## Summary

The Node.js event loop is the foundation of its non-blocking I/O architecture. Understanding the phases, microtasks, and how to avoid blocking is crucial for building performant applications. Key takeaways:

- The event loop has 5 main phases: timers, pending I/O, poll, check, close
- process.nextTick has highest priority but can cause starvation
- setImmediate is safer for recursive async work
- Always monitor event loop lag in production
- Use worker threads for CPU-intensive operations
- Understand the trade-offs between different async patterns

## Cheat Sheet
```text
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

---

## See Also
- [Docker](../13-Docker/)
- [JavaScript](../01-JavaScript/)
- [NestJS](../06-NestJS/)

## References & Learn More

- [Node.js Event Loop Docs](https://nodejs.org/en/learn/asynchronous-work/the-nodejs-event-loop)
- [Node.js Event Loop Phases](https://docs.libuv.org/en/latest/guide/design.html)
- [libuv Documentation](https://docs.libuv.org/)
- [Node.js Timers Docs](https://nodejs.org/api/timers.html)
