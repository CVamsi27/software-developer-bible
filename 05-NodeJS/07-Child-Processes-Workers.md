[![Category: Backend](https://img.shields.io/badge/category-Backend-2ea44f)](.)

# Child Processes & Worker Threads

Node.js provides two mechanisms for parallel execution: **child processes** (spawning separate OS processes) and **worker threads** (lightweight threads within the same process). Both enable CPU-intensive operations without blocking the event loop, but they serve different use cases.

## Definition

**Child Processes** (`child_process` module) spawn independent OS processes that:
- Run in separate memory spaces (no shared memory)
- Communicate via IPC (Inter-Process Communication) through message passing
- Can execute any executable (Node.js, Python, shell commands)
- Have their own event loop and V8 instance
- Are heavier to create (new process overhead)

**Worker Threads** (`worker_threads` module) are lightweight threads that:
- Run in the same process (shared memory space)
- Share module loading and V8 instance
- Communicate via message passing or `SharedArrayBuffer`
- Can transfer `ArrayBuffer` ownership (zero-copy)
- Are lighter than child processes

## Why Do We Need It?

1. **CPU-intensive tasks**: Image processing, video encoding, data transformation, complex calculations

2. **Parallelism**: Process multiple tasks simultaneously on multi-core systems

3. **Isolation**: Run untrusted code in isolated processes (security)

4. **Shell commands**: Execute system commands, Git operations, build tools

5. **Non-blocking**: Prevent CPU-intensive operations from blocking the event loop

## How It Works

### Architecture Comparison

```text
Child Process:                    Worker Thread:
┌─────────────────┐              ┌─────────────────┐
│   Main Process   │              │   Main Thread    │
│  ┌───────────┐   │              │  ┌───────────┐   │
│  │ Event Loop │   │              │  │ Event Loop │   │
│  └───────────┘   │              │  └───────────┘   │
│       │          │              │       │          │
├───────┼──────────┤              ├───────┼──────────┤
│       ▼          │              │       ▼          │
│  ┌───────────┐   │   IPC        │  ┌───────────┐   │  Shared
│  │ Child PID  │◄──┼───────────► │  │ Worker #1 │◄──┼──ArrayBuffer
│  │ Separate   │   │             │  └───────────┘   │
│  │ V8/Memory  │   │             │       │          │
│  └───────────┘   │              │  ┌───────────┐   │
│                  │              │  │ Worker #2 │   │
│  Heavier spawn   │              │  └───────────┘   │
│  Better isolation │              │  Lighter spawn   │
└─────────────────┘              └─────────────────┘
```

## Code Examples (Node.js)

### Child Processes: spawn

```javascript
const { spawn } = require('child_process');

// Spawn a long-running process with streaming output
const child = spawn('find', ['.', '-type', 'f', '-name', '*.js']);

child.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

child.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

child.on('close', (code) => {
  console.log(`Child process exited with code ${code}`);
});

child.on('error', (err) => {
  console.error('Failed to start child process:', err);
});
```

### Child Processes: exec (buffered)

```javascript
const { exec } = require('child_process');

// Execute with buffered output (not suitable for large output)
exec('ls -la', { maxBuffer: 1024 * 1024 }, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Stderr: ${stderr}`);
    return;
  }
  console.log(`Stdout:\n${stdout}`);
});

// Promise-based exec
const util = require('util');
const execPromise = util.promisify(require('child_process').exec);

async function runCommand() {
  try {
    const { stdout, stderr } = await execPromise('npm test');
    console.log('Tests passed:', stdout);
  } catch (err) {
    console.error('Tests failed:', err.stderr);
  }
}
```

### Child Processes: fork (IPC)

```javascript
// parent.js
const { fork } = require('child_process');

const child = fork('./child-worker.js');

child.send({ task: 'compute', data: { iterations: 1000000 } });

child.on('message', (result) => {
  console.log('Result from child:', result);
  child.disconnect();
});

child.on('error', (err) => {
  console.error('Child error:', err);
});

// child-worker.js
process.on('message', (msg) => {
  if (msg.task === 'compute') {
    // CPU-intensive work
    let result = 0;
    for (let i = 0; i < msg.data.iterations; i++) {
      result += Math.sqrt(i);
    }
    process.send({ result });
  }
});
```

### Worker Threads: Basic Usage

```javascript
// main.js
const { Worker } = require('worker_threads');

function runWorker(workerData) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', { workerData });

    worker.on('message', resolve);
    worker.on('error', reject);
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`));
      }
    });
  });
}

// CPU-intensive task without blocking the main thread
async function processImages(imagePaths) {
  const promises = imagePaths.map((path) =>
    runWorker({ type: 'process-image', path })
  );
  return Promise.all(promises);
}

// worker.js
const { parentPort, workerData } = require('worker_threads');

if (workerData.type === 'process-image') {
  // Simulate heavy computation
  let result = 0;
  for (let i = 0; i < 10000000; i++) {
    result += Math.sqrt(i);
  }
  parentPort.postMessage({ processed: workerData.path, result });
}
```

### Worker Threads: SharedArrayBuffer

```javascript
// main.js
const { Worker } = require('worker_threads');

const sharedBuffer = new SharedArrayBuffer(4 * 1024); // 4KB shared memory
const sharedArray = new Int32Array(sharedBuffer);

const worker = new Worker('./shared-worker.js', {
  workerData: { sharedBuffer },
});

worker.on('message', () => {
  console.log('Result from worker:', sharedArray[0]);
});

// shared-worker.js
const { parentPort, workerData } = require('worker_threads');

const sharedArray = new Int32Array(workerData.sharedBuffer);

// Atomic operations for thread safety
const result = computeExpensiveTask();
Atomics.store(sharedArray, 0, result);
parentPort.postMessage('done');
```

### Worker Threads: Thread Pool Pattern

```javascript
// thread-pool.js
const { Worker } = require('worker_threads');
const { cpus } = require('os');

class ThreadPool {
  constructor(workerPath, poolSize = cpus().length) {
    this.workers = [];
    this.queue = [];
    this.active = 0;

    for (let i = 0; i < poolSize; i++) {
      const worker = new Worker(workerPath);
      worker.on('message', () => {
        this.active--;
        this.processQueue();
      });
      worker.on('error', () => this.active--);
      this.workers.push(worker);
    }
  }

  processQueue() {
    if (this.queue.length === 0 || this.active >= this.workers.length) return;

    const { data, resolve } = this.queue.shift();
    const worker = this.workers[this.active];
    this.active++;
    worker.postMessage(data);
    worker.once('message', (result) => resolve(result));
  }

  execute(data) {
    return new Promise((resolve) => {
      this.queue.push({ data, resolve });
      this.processQueue();
    });
  }

  terminate() {
    this.workers.forEach((w) => w.terminate());
  }
}

// Usage
const pool = new ThreadPool('./worker.js');
const results = await Promise.all([
  pool.execute({ n: 1000000 }),
  pool.execute({ n: 2000000 }),
  pool.execute({ n: 3000000 }),
]);
```

## Real-World Use Cases

### 1. Image Processing Server

```javascript
const http = require('http');
const { Worker } = require('worker_threads');
const { cpus } = require('os');

const pool = [];

for (let i = 0; i < cpus().length; i++) {
  const worker = new Worker('./image-worker.js');
  pool.push(worker);
}

const server = http.createServer((req, res) => {
  if (req.url.startsWith('/process-image')) {
    const worker = pool[Math.floor(Math.random() * pool.length)];
    worker.postMessage({ image: '/path/to/image.jpg' });
    worker.once('message', (result) => {
      res.writeHead(200);
      res.end(JSON.stringify(result));
    });
  }
});
```

### 2. Batch Data Processing

```javascript
const { fork } = require('child_process');
const path = require('path');

async function processInParallel(data, concurrency = 4) {
  const chunks = [];
  const chunkSize = Math.ceil(data.length / concurrency);

  for (let i = 0; i < data.length; i += chunkSize) {
    chunks.push(data.slice(i, i + chunkSize));
  }

  const results = await Promise.all(
    chunks.map((chunk) => {
      return new Promise((resolve, reject) => {
        const child = fork(path.join(__dirname, 'data-worker.js'));
        child.send({ data: chunk });
        child.on('message', resolve);
        child.on('error', reject);
      });
    })
  );

  return results.flat();
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `exec` with large output buffers | Use `spawn` for streaming or increase `maxBuffer` |
| Not handling `stderr` separately | Always listen for `stderr` data and errors |
| Leaving zombie child processes | Handle `exit` and `error` events; kill on parent shutdown |
| Modifying `SharedArrayBuffer` without atomics | Use `Atomics.load/store/wait/notify` for thread safety |
| Creating too many workers/processes | Use a thread pool limited to `cpus().length` |

## Best Practices

1. **Pool workers/processes** — create once, reuse; don't spawn per-request
2. **Use workers for CPU** — use `worker_threads` for CPU-bound tasks, `child_process` for system commands
3. **Limit concurrency** — don't exceed `os.cpus().length` workers for CPU tasks
4. **Graceful cleanup** — terminate workers on shutdown
5. **Handle errors** — always add error handlers to workers and child processes
6. **Use Transferable** — transfer `ArrayBuffer` with `postMessage` for zero-copy
7. **Timeout workers** — implement timeout to kill unresponsive workers

## Performance Comparison

| Aspect | Child Process | Worker Thread |
|--------|:------------:|:-------------:|
| Memory | Separate (high) | Shared (low) |
| Startup time | ~10-30ms | ~1-5ms |
| Isolation | Full process | Same process |
| IPC overhead | Higher | Lower |
| Use case | Shell commands, security | CPU computation |

## Summary

Child processes and worker threads are essential for parallel execution in Node.js. Use `child_process.fork()` for isolated work with IPC, `spawn()` for streaming shell commands, and `worker_threads` for CPU-intensive tasks within the same process. Pool workers for production workloads and always handle cleanup properly.

## Cheat Sheet

```text
CHILD PROCESSES:
  spawn('cmd', ['args'])    // Streaming, large output
  exec('cmd', cb)           // Buffered, small output
  fork('module.js')         // IPC channel, Node.js only
  child.send(msg)           // Send message
  child.on('message')       // Receive message

WORKER THREADS:
  new Worker('file.js')     // Create worker
  worker.postMessage(data)  // Send data
  worker.on('message')      // Receive data
  worker.terminate()        // Kill worker
  parentPort.postMessage()  // From worker to parent
  SharedArrayBuffer         // Shared memory
  Atomics                   // Thread-safe operations

CONSTRAINTS:
  cpus().length → max CPU workers
  SharedArrayBuffer → zero-copy transfer
  Transferable → ArrayBuffer, MessagePort
```

---

### See Also

- [Clustering](04-Clustering.md) — multi-process web serving
- [Event Loop](01-Event-Loop.md) — how async I/O works
- [Process & Environment](08-Process-Environment.md) — process lifecycle

## References & Learn More

- [Node.js child_process Docs](https://nodejs.org/api/child_process.html)
- [Node.js worker_threads Docs](https://nodejs.org/api/worker_threads.html)
- [Node.js: Don't Block the Event Loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop)
- [Node.js: Worker Threads Guide](https://nodejs.org/api/worker_threads.html)
