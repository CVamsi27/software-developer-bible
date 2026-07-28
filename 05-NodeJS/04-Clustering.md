---
section: Node.js
category: Backend
tags: [concept]
---

# Node.js Clustering

## Definition

**Clustering** is a Node.js module that allows you to create multiple worker processes that share a single port. It enables you to utilize multiple CPU cores by forking the main process into multiple worker processes, each running its own instance of the Node.js event loop. The cluster module uses the `child_process.fork()` method internally to create workers.

## Why Do We Need It?

Node.js runs on a single thread by default, which means:

1. **Single Core Utilization**: A single Node.js process can only use one CPU core

2. **Blocking Operations**: CPU-intensive tasks block the entire event loop

3. **Fault Tolerance**: If the main process crashes, all connections are lost

4. **Scalability Limits**: Single process has memory and performance limits

Clustering solves these problems by:

- Utilizing all available CPU cores
- Providing fault tolerance (worker crashes don't affect others)
- Enabling horizontal scaling on a single machine
- Improving throughput for multi-core systems

## How It Works

### Clustering Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                    CLUSTERING ARCHITECTURE                    │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│                      ┌──────────────┐                        │
│                      │    Master    │                        │
│                      │   Process    │                        │
│                      └──────┬───────┘                        │
│                             │                                │
│           ┌─────────────────┼─────────────────┐              │
│           │                 │                 │              │
│           ▼                 ▼                 ▼              │
│     ┌──────────┐     ┌──────────┐     ┌──────────┐         │
│     │ Worker 1 │     │ Worker 2 │     │ Worker 3 │         │
│     │ (Core 1) │     │ (Core 2) │     │ (Core 3) │         │
│     └──────────┘     └──────────┘     └──────────┘         │
│           │                 │                 │              │
│           └─────────────────┼─────────────────┘              │
│                             │                                │
│                      ┌──────▼───────┐                        │
│                      │    Port      │                        │
│                      │   3000       │                        │
│                      └──────────────┘                        │
│                                                              │
│  Master Process:                                             │
│  • Forks worker processes                                    │
│  • Manages worker lifecycle                                  │
│  • Distributes connections (round-robin)                     │
│  • Listens on the main port                                  │
│                                                              │
│  Worker Processes:                                           │
│  • Run independently                                         │
│  • Handle client connections                                 │
│  • Can communicate with master via IPC                       │
│  • Have own event loop                                       │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

### Connection Distribution

```text
┌───────────────────────────────────────────────────────────────┐
│              CONNECTION DISTRIBUTION METHODS                  │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  Round-Robin (Default on non-Windows):                       │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Request 1 → Worker 1                                   ││
│  │  Request 2 → Worker 2                                   ││
│  │  Request 3 → Worker 3                                   ││
│  │  Request 4 → Worker 1                                   ││
│  │  Request 5 → Worker 2                                   ││
│  │  Request 6 → Worker 3                                   ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  OS-Level Scheduling (Windows):                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Connections distributed by OS                           ││
│  │  Less efficient on Windows                               ││
│  │  May cause uneven load distribution                      ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  Sticky Sessions (for WebSockets):                           │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Request 1 (IP: 192.168.1.1) → Worker 1                ││
│  │  All subsequent requests from same IP → Worker 1        ││
│  │  Request 2 (IP: 192.168.1.2) → Worker 2                ││
│  │  All subsequent requests from same IP → Worker 2        ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

### IPC Communication

```text
┌───────────────────────────────────────────────────────────────┐
│               INTER-PROCESS COMMUNICATION                    │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  Master ←→ Worker Communication:                             │
│                                                              │
│  Master Process                                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  worker.send('message')      →  Send to worker          ││
│  │  worker.on('message', cb)    ←  Receive from worker     ││
│  │  worker.kill()               →  Terminate worker        ││
│  │  worker.disconnect()         →  Graceful shutdown        ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  Worker Process                                              │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  process.send('message')     →  Send to master          ││
│  │  process.on('message', cb)   ←  Receive from master     ││
│  │  process.exit()              →  Exit worker             ││
│  │  process.disconnect()        →  Disconnect from master   ││
│  └──────────────────────────────────────────────────────────┘│
│                                                              │
│  Message Types:                                              │
│  • JSON serializable objects                                 │
│  • Buffer (zero-copy in some cases)                          │
│  • Handle objects (for sharing server sockets)               │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

### Worker Lifecycle

```text
┌───────────────────────────────────────────────────────────────┐
│                   WORKER LIFECYCLE                            │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐                                             │
│  │   Fork      │  Master creates worker                     │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   Online    │  Worker is ready to receive connections     │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │  Handling   │  Worker processes requests                  │
│  │  Requests   │                                             │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   Exit      │  Worker terminates (crash or intentional)   │
│  └──────┬──────┘                                             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                             │
│  │   Restart   │  Master forks new worker (if enabled)       │
│  └─────────────┘                                             │
│                                                              │
│  Events:                                                     │
│  • 'fork': Worker was spawned                                │
│  • 'online': Worker is online                                │
│  • 'listening': Worker started listening                     │
│  • 'message': Worker sent message                            │
│  • 'exit': Worker terminated                                 │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Cluster Setup

```typescript
// basic-cluster.ts

import * as cluster from 'cluster';
import * as http from 'http';
import * as os from 'os';

const numCPUs = os.cpus().length;

if (cluster.isPrimary) {
  console.log(`Primary ${process.pid} is running`);
  console.log(`Forking ${numCPUs} workers...`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Handle worker exit
  cluster.on('exit', (worker, code, signal) => {
    console.log(
      `Worker ${worker.process.pid} died (code: ${code}, signal: ${signal})`
    );
    // Replace dead worker
    cluster.fork();
  });
} else {
  // Worker process
  const server = http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Hello from worker ${process.pid}`);
  });

  server.listen(3000, () => {
    console.log(`Worker ${process.pid} started`);
  });
}

```

### Advanced Cluster with Load Balancing

```typescript
// advanced-cluster.ts

import * as cluster from 'cluster';
import * as http from 'http';
import * as os from 'os';
import * as net from 'net';

const numCPUs = os.cpus().length;
const PORT = 3000;

if (cluster.isPrimary) {
  console.log(`Master ${process.pid} is running`);

  // Track workers
  const workers = new Map<number, cluster.Worker>();

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    const worker = cluster.fork();
    workers.set(worker.id, worker);

    worker.on('message', (msg) => {
      console.log(`Worker ${worker.id}: ${msg}`);
    });
  }

  // Round-robin scheduling (Linux/Mac)
  let currentWorker = 0;
  const server = net.createServer({ pauseOnConnect: true }, (socket) => {
    const workerIds = Array.from(workers.keys());
    const targetWorker = workers.get(workerIds[currentWorker]);

    if (targetWorker) {
      targetWorker.send('socket', socket);
      currentWorker = (currentWorker + 1) % workerIds.length;
    }
  });

  server.listen(PORT);

  // Monitor workers
  cluster.on('exit', (worker, code, signal) => {
    console.log(
      `Worker ${worker.process.pid} died (code: ${code}, signal: ${signal})`
    );
    workers.delete(worker.id);

    // Replace dead worker
    const newWorker = cluster.fork();
    workers.set(newWorker.id, newWorker);
  });

  // Graceful shutdown
  process.on('SIGTERM', () => {
    console.log('Master received SIGTERM, shutting down...');

    for (const [id, worker] of workers) {
      console.log(`Disconnecting worker ${id}`);
      worker.disconnect();

      // Force kill after timeout
      setTimeout(() => {
        if (!worker.isDead()) {
          worker.kill();
        }
      }, 5000);
    }
  });
} else {
  // Worker process
  const server = http.createServer(async (req, res) => {
    try {
      // Simulate work
      const result = await processRequest(req);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result));
    } catch (error) {
      res.writeHead(500);
      res.end('Internal Server Error');
    }
  });

  server.listen(0); // Listen on random port

  // Notify master we're ready
  process.send('Worker ready');

  // Handle messages from master
  process.on('message', (msg, socket) => {
    if (msg === 'socket' && socket) {
      server.emit('connection', socket);
    }
  });
}

async function processRequest(req: http.IncomingMessage): Promise<any> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        pid: process.pid,
        url: req.url,
        timestamp: Date.now(),
      });
    }, 100);
  });
}

```

### Worker Threads vs Cluster

```typescript
// worker-threads-vs-cluster.ts

import * as cluster from 'cluster';
import * as os from 'os';
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads';

// Worker Threads Example
if (isMainThread) {
  // Main thread
  function runWorker(workerData: any): Promise<any> {
    return new Promise((resolve, reject) => {
      const worker = new Worker(__filename, { workerData });

      worker.on('message', resolve);
      worker.on('error', reject);
      worker.on('exit', (code) => {
        if (code !== 0) {
          reject(new Error(`Worker exited with code ${code}`));
        }
      });
    });
  }

  // Use worker threads for CPU-intensive tasks
  async function main() {
    const result = await runWorker({ iterations: 1e9 });
    console.log('Result:', result);
  }

  main();
} else {
  // Worker thread
  const { iterations } = workerData;
  let result = 0;

  for (let i = 0; i < iterations; i++) {
    result += i;
  }

  parentPort?.postMessage(result);
}

// Cluster Example (separate file)
// cluster-example.ts
if (cluster.isPrimary) {
  for (let i = 0; i < os.cpus().length; i++) {
    cluster.fork();
  }
} else {
  // Handle HTTP requests in each worker
  const http = require('http');
  http.createServer((req: any, res: any) => {
    res.end(`Worker ${process.pid}`);
  }).listen(3000);
}

```

### Graceful Shutdown

```typescript
// graceful-shutdown.ts

import * as cluster from 'cluster';
import * as http from 'http';
import * as os from 'os';

const numCPUs = os.cpus().length;

if (cluster.isPrimary) {
  console.log(`Master ${process.pid} is running`);

  const workers = new Map<number, cluster.Worker>();
  let isShuttingDown = false;

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    const worker = cluster.fork();
    workers.set(worker.id, worker);
  }

  // Handle worker exit
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    workers.delete(worker.id);

    if (!isShuttingDown && code !== 0) {
      // Unexpected exit, restart
      const newWorker = cluster.fork();
      workers.set(newWorker.id, newWorker);
    }
  });

  // Graceful shutdown handler
  const shutdown = (signal: string) => {
    console.log(`Received ${signal}, shutting down gracefully...`);
    isShuttingDown = true;

    // Stop accepting new connections
    let disconnectedCount = 0;

    for (const [id, worker] of workers) {
      console.log(`Disconnecting worker ${id}`);
      worker.disconnect();
      disconnectedCount++;
    }

    // Force shutdown after timeout
    setTimeout(() => {
      console.error('Forced shutdown due to timeout');
      process.exit(1);
    }, 30000);

    // Wait for all workers to disconnect
    cluster.on('disconnect', () => {
      disconnectedCount--;
      if (disconnectedCount === 0) {
        console.log('All workers disconnected');
        process.exit(0);
      }
    });
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));

} else {
  const server = http.createServer((req, res) => {
    // Simulate processing
    const start = Date.now();
    while (Date.now() - start < 100) {
      // Some work
    }
    res.end(`Worker ${process.pid} processed request`);
  });

  server.listen(3000, () => {
    console.log(`Worker ${process.pid} started`);
  });

  // Handle shutdown message from master
  process.on('message', (msg) => {
    if (msg === 'shutdown') {
      console.log(`Worker ${process.pid} received shutdown message`);

      // Close server gracefully
      server.close(() => {
        console.log(`Worker ${process.pid} closed server`);
        process.exit(0);
      });
    }
  });
}

```

### Sticky Sessions for WebSockets

```typescript
// sticky-sessions.ts

import * as cluster from 'cluster';
import * as http from 'http';
import * as os from 'os';
import * as net from 'net';

const numCPUs = os.cpus().length;
const PORT = 3000;

if (cluster.isPrimary) {
  console.log(`Master ${process.pid} is running`);

  // Store worker connections
  const workers = new Map<number, cluster.Worker>();
  const connections = new Map<string, cluster.Worker>();

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    const worker = cluster.fork();
    workers.set(worker.id, worker);
  }

  // Sticky session implementation
  const server = net.createServer({ pauseOnConnect: true }, (socket) => {
    const ip = socket.remoteAddress || '127.0.0.1';
    const key = `${ip}:${socket.remotePort}`;

    // Check if we have a worker for this connection
    let worker = connections.get(key);

    if (!worker) {
      // Round-robin to new worker
      const workerIds = Array.from(workers.keys());
      const randomIndex = Math.floor(Math.random() * workerIds.length);
      worker = workers.get(workerIds[randomIndex]);

      if (worker) {
        connections.set(key, worker);
      }
    }

    if (worker) {
      worker.send('connection', socket);
    } else {
      socket.destroy();
    }
  });

  server.listen(PORT);

  // Clean up connections on worker exit
  cluster.on('exit', (worker) => {
    // Remove all connections for this worker
    for (const [key, w] of connections) {
      if (w.id === worker.id) {
        connections.delete(key);
      }
    }
  });

} else {
  // Worker process
  const server = http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Worker ${process.pid}`);
  });

  // Handle WebSocket connections
  const WebSocket = require('ws');
  const wss = new WebSocket.Server({ noServer: true });

  wss.on('connection', (ws: any) => {
    console.log(`Worker ${process.pid}: WebSocket connected`);

    ws.on('message', (message: any) => {
      ws.send(`Worker ${process.pid}: ${message}`);
    });
  });

  server.on('upgrade', (req, socket, head) => {
    wss.handleUpgrade(req, socket, head, (ws) => {
      wss.emit('connection', ws, req);
    });
  });

  server.listen(0);

  // Handle connections from master
  process.on('message', (msg, socket) => {
    if (msg === 'connection' && socket) {
      server.emit('connection', socket);
    }
  });
}

```

## Real-World Use Cases

### 1. Web Server with Load Balancing

```typescript
// web-server-cluster.ts

import * as cluster from 'cluster';
import * as http from 'http';
import * as os from 'os';
import * as express from 'express';

const numCPUs = os.cpus().length;

if (cluster.isPrimary) {
  console.log(`Master ${process.pid} is running`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Track worker health
  const healthCheckInterval = setInterval(() => {
    for (const id in cluster.workers) {
      const worker = cluster.workers[id];
      if (worker) {
        worker.send('health-check');
      }
    }
  }, 30000);

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    cluster.fork(); // Replace dead worker
  });

  process.on('SIGTERM', () => {
    clearInterval(healthCheckInterval);
    // Graceful shutdown
  });

} else {
  const app = express();

  // Middleware
  app.use(express.json());

  // Routes
  app.get('/', (req, res) => {
    res.json({
      pid: process.pid,
      timestamp: Date.now(),
      hostname: os.hostname(),
    });
  });

  app.get('/health', (req, res) => {
    res.json({
      pid: process.pid,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
    });
  });

  // Start server on random port
  const server = app.listen(0, () => {
    console.log(`Worker ${process.pid} started`);
  });

  // Handle graceful shutdown
  process.on('message', (msg) => {
    if (msg === 'shutdown') {
      server.close(() => {
        process.exit(0);
      });
    }
  });
}

```

### 2. API Gateway with Rate Limiting

```typescript
// api-gateway-cluster.ts

import * as cluster from 'cluster';
import * as http from 'http';
import * as os from 'os';

const numCPUs = os.cpus().length;

if (cluster.isPrimary) {
  console.log(`Master ${process.pid} is running`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Distribute connections using round-robin
  let currentWorker = 0;
  const server = http.createServer((req, res) => {
    const workerIds = Object.keys(cluster.workers);
    const targetWorker = cluster.workers[workerIds[currentWorker]];

    if (targetWorker) {
      targetWorker.send('request', {
        url: req.url,
        method: req.method,
        headers: req.headers,
      });

      currentWorker = (currentWorker + 1) % workerIds.length;
    }
  });

  server.listen(8080);

} else {
  // Rate limiter in each worker
  const rateLimits = new Map<string, { count: number; resetTime: number }>();

  function isRateLimited(ip: string): boolean {
    const now = Date.now();
    const limit = rateLimits.get(ip);

    if (!limit || now > limit.resetTime) {
      rateLimits.set(ip, { count: 1, resetTime: now + 60000 });
      return false;
    }

    if (limit.count >= 100) {
      return true;
    }

    limit.count++;
    return false;
  }

  // Worker process
  process.on('message', (msg, data) => {
    if (msg === 'request') {
      // Check rate limit
      const ip = '127.0.0.1'; // Get from request
      if (isRateLimited(ip)) {
        // Return 429
        return;
      }

      // Process request
      // ...
    }
  });
}

```

## Common Mistakes

### 1. Not Handling Worker Crashes

```typescript
// BAD: No crash handling
cluster.on('exit', (worker) => {
  console.log('Worker died');
});

// GOOD: Replace dead workers
cluster.on('exit', (worker, code, signal) => {
  console.log(`Worker ${worker.process.pid} died`);
  cluster.fork(); // Replace immediately
});

```

### 2. Sharing State Between Workers

```typescript
// BAD: Trying to share memory
let counter = 0;

cluster.on('message', (worker, msg) => {
  counter++; // Each worker has own counter
});

// GOOD: Use shared storage (Redis)
const Redis = require('ioredis');
const redis = new Redis();

cluster.on('message', async (worker, msg) => {
  await redis.incr('counter'); // Shared counter
});

```

### 3. Not Implementing Graceful Shutdown

```typescript
// BAD: Immediate exit
process.on('SIGTERM', () => {
  process.exit(0); // May lose connections
});

// GOOD: Graceful shutdown
process.on('SIGTERM', () => {
  server.close(() => {
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 30000);
});

```

### 4. Incorrect Port Sharing

```typescript
// BAD: Each worker tries to bind same port
for (let i = 0; i < numCPUs; i++) {
  cluster.fork(); // May fail if port already in use
}

// GOOD: Let cluster handle port sharing
for (let i = 0; i < numCPUs; i++) {
  cluster.fork(); // Cluster manages port sharing
}

```

### 5. Not Monitoring Workers

```typescript
// BAD: No monitoring
cluster.fork();

// GOOD: Monitor worker health
cluster.on('message', (worker, msg) => {
  if (msg === 'health-check') {
    // Worker is alive
  }
});

setInterval(() => {
  for (const id in cluster.workers) {
    cluster.workers[id]?.send('health-check');
  }
}, 30000);

```

## Best Practices

### 1. Use Environment Variables

```typescript
// Set environment variables for workers
if (cluster.isPrimary) {
  process.env.WORKER_ID = '0';
  cluster.fork();
  process.env.WORKER_ID = '1';
  cluster.fork();
} else {
  console.log(`Worker ${process.env.WORKER_ID} started`);
}

```

### 2. Implement Health Checks

```typescript
// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    pid: process.pid,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    status: 'healthy',
  });
});

```

### 3. Use Sticky Sessions for WebSocket

```typescript
// For WebSocket connections, use sticky sessions
const server = net.createServer({ pauseOnConnect: true }, (socket) => {
  const ip = socket.remoteAddress;
  const worker = getWorkerForIP(ip);
  worker.send('connection', socket);
});

```

### 4. Monitor Worker Metrics

```typescript
// Collect metrics from workers
cluster.on('message', (worker, msg) => {
  if (msg.type === 'metrics') {
    metricsCollector.record(worker.id, msg.data);
  }
});

```

### 5. Implement Circuit Breaker

```typescript
// Circuit breaker pattern
class CircuitBreaker {
  private failures = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  async call(fn: () => Promise<any>): Promise<any> {
    if (this.state === 'open') {
      throw new Error('Circuit is open');
    }

    try {
      const result = await fn();
      this.failures = 0;
      this.state = 'closed';
      return result;
    } catch (error) {
      this.failures++;
      if (this.failures >= 5) {
        this.state = 'open';
        setTimeout(() => {
          this.state = 'half-open';
        }, 30000);
      }
      throw error;
    }
  }
}

```

## Performance Considerations

### 1. Optimize Worker Count

```typescript
// Don't use more workers than CPU cores
const numCPUs = os.cpus().length;
const workerCount = Math.min(numCPUs, 8); // Cap at 8

```

### 2. Memory Management

```typescript
// Monitor memory usage per worker
const memUsage = process.memoryUsage();
if (memUsage.heapUsed > 500 * 1024 * 1024) {
  // Restart worker if using too much memory
  process.exit(1);
}

```

### 3. Load Balancing

```typescript
// Use round-robin for even distribution
cluster.schedulingPolicy = cluster.SCHED_RR;

```

### 4. Connection Pooling

```typescript
// Share database connections across workers
const pool = require('generic-pool').createPool({
  create: () => createConnection(),
  destroy: (conn) => conn.close(),
  max: 10,
});

```


## Summary

Clustering is essential for scaling Node.js applications across multiple CPU cores. Key takeaways:

- Use clustering for I/O-bound workloads
- Use worker_threads for CPU-bound workloads
- Implement proper health monitoring and auto-restart
- Use sticky sessions for stateful connections
- Implement graceful shutdown for zero-downtime deployments
- Monitor resource usage per worker

## Cheat Sheet
```text
┌───────────────────────────────────────────────────────────────┐
│                   CLUSTERING CHEAT SHEET                     │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  BASICS:                                                     │
│  • cluster.isPrimary - check if primary process              │
│  • cluster.isWorker - check if worker process                │
│  • cluster.fork() - create worker process                    │
│  • cluster.workers - list of active workers                  │
│                                                              │
│  WORKER METHODS:                                             │
│  • worker.send(msg) - send message to worker                 │
│  • worker.kill() - terminate worker                          │
│  • worker.disconnect() - graceful shutdown                   │
│  • worker.id - worker identifier                             │
│  • worker.process.pid - worker process ID                    │
│                                                              │
│  EVENTS:                                                     │
│  • 'fork': Worker spawned                                    │
│  • 'online': Worker is ready                                 │
│  • 'listening': Worker started listening                     │
│  • 'message': Worker sent message                            │
│  • 'exit': Worker terminated                                 │
│  • 'disconnect': Worker disconnected                         │
│                                                              │
│  SCHEDULING:                                                 │
│  • cluster.SCHED_RR - round-robin (default on Linux/Mac)     │
│  • cluster.SCHED_NONE - OS-level scheduling (Windows)        │
│                                                              │
│  BEST PRACTICES:                                             │
│  • Fork workers equal to CPU cores                           │
│  • Handle worker crashes with auto-restart                   │
│  • Use sticky sessions for WebSockets                        │
│  • Implement graceful shutdown                               │
│  • Monitor worker health and memory                         │
│                                                              │
│  COMMON PITFALLS:                                            │
│  • Not handling worker crashes                               │
│  • Trying to share memory between workers                    │
│  • Not implementing graceful shutdown                        │
│  • Incorrect port binding                                    │
│  • Not monitoring workers                                    │
│                                                              │
│  CLUSTER vs WORKER_THREADS:                                  │
│  • Cluster: separate processes, IPC communication            │
│  • Worker Threads: same process, shared memory               │
│  • Cluster: better for I/O-bound                             │
│  • Worker Threads: better for CPU-bound                      │
│                                                              │
│  DEBUGGING:                                                  │
│  • Worker-specific logging                                   │
│  • Process ID tracking                                       │
│  • Health check endpoints                                    │
│  • Memory usage monitoring                                   │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

---

## See Also
- [JavaScript](../01-JavaScript/)
- [NestJS](../06-NestJS/)
- [Docker](../13-Docker/)

## References & Learn More

- [Node.js Cluster Docs](https://nodejs.org/api/cluster.html)
- [Node.js Cluster Example](https://nodejs.org/api/cluster.html#clusterExample)
- [PM2 Process Manager](https://pm2.keymetrics.io/)
- [Node.js Worker Threads](https://nodejs.org/api/worker_threads.html)
