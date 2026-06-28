# Node.js Interview Questions

## Definition

This chapter contains the **40 most frequently asked Node.js interview questions** with detailed answers, categorized by difficulty level. Each question includes explanations, code examples, and common follow-ups to help you prepare for technical interviews at various levels.

## Why Do We Need It?

Understanding these questions is crucial for:

- **Technical Interviews**: Demonstrate deep knowledge of Node.js
- **Architecture Decisions**: Make informed choices about system design
- **Debugging**: Identify and solve common issues
- **Performance Optimization**: Know what to optimize and when
- **Code Quality**: Write better, more maintainable code

## How It Works

### Question Categories

```text
┌───────────────────────────────────────────────────────────────┐
│                 INTERVIEW QUESTION STRUCTURE                  │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  Difficulty Levels:                                          │
│  ┌─────────────┐                                             │
│  │  Beginner   │  Basic concepts, syntax, simple patterns    │
│  └─────────────┘                                             │
│  ┌─────────────┐                                             │
│  │ Intermediate│  Advanced patterns, error handling          │
│  └─────────────┘                                             │
│  ┌─────────────┐                                             │
│  │   Senior    │  Architecture, performance, scalability     │
│  └─────────────┘                                             │
│  ┌─────────────┐                                             │
│  │   FAANG     │  System design, distributed systems         │
│  └─────────────┘                                             │
│                                                              │
│  Answer Structure:                                           │
│  • Definition and explanation                                │
│  • Code examples                                             │
│  • Common mistakes                                           │
│  • Best practices                                            │
│  • Follow-up questions                                       │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

## Code Examples

### Beginner Questions (5-10)

#### Q1: What is Node.js and why is it used?

**Answer:**

Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine. It's used for building scalable network applications due to its non-blocking I/O model.

**Key Points:**

- Event-driven, non-blocking I/O
- Single-threaded but concurrent
- npm package manager
- Cross-platform

```javascript
// Basic HTTP server example
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World\n');
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});

```

---

#### Q2: What is the event loop in Node.js?

**Answer:**

The event loop is the mechanism that allows Node.js to perform non-blocking I/O operations despite JavaScript being single-threaded. It continuously monitors the call stack and callback queues.

**Event Loop Phases:**

1. Timers: setTimeout(), setInterval()

2. Pending I/O: callbacks from I/O operations

3. Poll: retrieve new I/O events

4. Check: setImmediate()

5. Close Callbacks: close events

```javascript
console.log('Start');

setTimeout(() => {
  console.log('Timeout');
}, 0);

setImmediate(() => {
  console.log('Immediate');
});

Promise.resolve().then(() => {
  console.log('Promise');
});

console.log('End');

// Output: Start → End → Promise → Timeout/Immediate

```

---

#### Q3: What is the difference between `process.nextTick` and `setImmediate`?

**Answer:**

- `process.nextTick()`: Executes immediately after the current operation completes, before the event loop continues
- `setImmediate()`: Executes in the check phase of the event loop

```javascript
setImmediate(() => {
  console.log('setImmediate');
});

process.nextTick(() => {
  console.log('nextTick');
});

console.log('Main');

// Output: Main → nextTick → setImmediate

```

**Use `process.nextTick` when:**

- You need to execute code after the current operation
- You want to ensure a function runs before I/O callbacks

**Use `setImmediate` when:**

- You want to execute code after I/O callbacks
- You want to break up long-running operations

---

#### Q4: What are streams in Node.js?

**Answer:**

Streams are objects that allow you to read or write data sequentially, piece by piece, rather than loading the entire data into memory at once.

**Four Types:**

1. Readable: fs.createReadStream()

2. Writable: fs.createWriteStream()

3. Duplex: net.Socket (both readable and writable)

4. Transform: zlib.createGzip() (modifies data)

```javascript
const fs = require('fs');
const { Transform } = require('stream');

// Readable stream
const readStream = fs.createReadStream('large-file.txt');

// Writable stream
const writeStream = fs.createWriteStream('output.txt');

// Transform stream
const upperCaseTransform = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
});

// Piping streams
readStream
  .pipe(upperCaseTransform)
  .pipe(writeStream);

```

---

#### Q5: What is the difference between `require` and `import`?

**Answer:**

- `require()`: CommonJS module system (synchronous, dynamic)
- `import`: ES Modules (asynchronous, static)

```javascript
// CommonJS
const fs = require('fs');
const myModule = require('./myModule');

// ES Modules
import fs from 'fs';
import { readFile } from 'fs/promises';
import myModule from './myModule.js';

```

**Key Differences:**

- CommonJS is Node.js default, ES Modules need `.mjs` extension or `"type": "module"` in package.json
- ES Modules are tree-shakeable
- CommonJS can be used conditionally, ES Modules are static

---

#### Q6: What is middleware in Express.js?

**Answer:**

Middleware functions are functions that have access to the request, response, and next middleware function. They can execute code, modify request/response objects, and end the request-response cycle.

```javascript
const express = require('express');
const app = express();

// Application-level middleware
app.use((req, res, next) => {
  console.log('Time:', Date.now());
  next();
});

// Route-specific middleware
const authMiddleware = (req, res, next) => {
  if (req.headers.authorization) {
    next();
  } else {
    res.status(401).send('Unauthorized');
  }
};

app.get('/protected', authMiddleware, (req, res) => {
  res.send('Protected content');
});

```

---

#### Q7: How do you handle errors in Node.js?

**Answer:**

Node.js uses error-first callbacks and try-catch for synchronous code.

```javascript
// Error-first callback
fs.readFile('file.txt', (err, data) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log(data);
});

// Try-catch for synchronous code
try {
  JSON.parse('invalid json');
} catch (err) {
  console.error('Parse error:', err.message);
}

// Promise error handling
fetchData()
  .then(data => console.log(data))
  .catch(err => console.error('Error:', err));

// Async/await error handling
async function getData() {
  try {
    const data = await fetchData();
    return data;
  } catch (err) {
    console.error('Error:', err);
    throw err;
  }
}

```

---

#### Q8: What is a Buffer in Node.js?

**Answer:**

A Buffer is a fixed-size block of memory used to store raw binary data. It's used when working with binary data like files, network protocols, or cryptography.

```javascript
// Creating buffers
const buf1 = Buffer.alloc(10); // 10 bytes, zero-filled
const buf2 = Buffer.from('Hello'); // From string
const buf3 = Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]); // From array

// Converting to string
console.log(buf2.toString()); // 'Hello'
console.log(buf2.toString('base64')); // 'SGVsbG8='
console.log(buf2.toString('hex')); // '48656c6c6f'

// Working with binary data
const buffer = Buffer.alloc(4);
buffer.writeUInt32BE(1234567890, 0);
console.log(buffer.readUInt32BE(0)); // 1234567890

```

---

#### Q9: What is the `module.exports` object?

**Answer:**

`module.exports` is used to export functions, objects, or values from a Node.js module so they can be used in other files.

```javascript
// math.js
const add = (a, b) => a + b;
const subtract = (a, b) => a - b;

module.exports = { add, subtract };
// Or: exports.add = add;

// app.js
const math = require('./math');
console.log(math.add(1, 2)); // 3

// Destructuring
const { add, subtract } = require('./math');

```

---

#### Q10: What is npm and how do you use it?

**Answer:**

npm (Node Package Manager) is the default package manager for Node.js. It's used to install, share, and manage dependencies.

```bash
# Initialize a project
npm init

# Install a package
npm install express

# Install dev dependency
npm install --save-dev jest

# Install globally
npm install -g typescript

# Run scripts
npm start
npm test

# Update packages
npm update

# Audit for vulnerabilities
npm audit

```

---

### Intermediate Questions (5-10)

#### Q11: What is the difference between `process.nextTick` and `setImmediate` in terms of execution order?

**Answer:**

`process.nextTick` always executes before `setImmediate` because it's processed in the next tick of the event loop, while `setImmediate` is processed in the check phase.

```javascript
setImmediate(() => {
  console.log('setImmediate');
});

process.nextTick(() => {
  console.log('nextTick');
});

Promise.resolve().then(() => {
  console.log('Promise');
});

console.log('Main');

// Output: Main → nextTick → Promise → setImmediate

```

**Performance Consideration:**

- `process.nextTick` can starve the event loop if used recursively
- Use `setImmediate` for heavy operations to allow I/O to be processed

---

#### Q12: How do you implement rate limiting in Node.js?

**Answer:**

Rate limiting controls the number of requests a client can make within a time period.

```javascript
// Simple in-memory rate limiter
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.clients = new Map();
  }

  isAllowed(clientId) {
    const now = Date.now();
    const client = this.clients.get(clientId) || { count: 0, resetTime: now + this.windowMs };

    if (now > client.resetTime) {
      client.count = 0;
      client.resetTime = now + this.windowMs;
    }

    if (client.count >= this.maxRequests) {
      return false;
    }

    client.count++;
    this.clients.set(clientId, client);
    return true;
  }
}

// Express middleware
const limiter = new RateLimiter(100, 60000); // 100 requests per minute

app.use((req, res, next) => {
  if (!limiter.isAllowed(req.ip)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  next();
});

```

---

#### Q13: What is the difference between `spawn`, `exec`, `execFile`, and `fork`?

**Answer:**

- `spawn`: Launches a new process with given command
- `exec`: Runs a command in a shell and buffers output
- `execFile`: Like exec but doesn't spawn a shell
- `fork`: Special case of spawn for Node.js modules

```javascript
const { spawn, exec, execFile, fork } = require('child_process');

// spawn - streaming output
const spawnProcess = spawn('ls', ['-la']);
spawnProcess.stdout.on('data', (data) => {
  console.log(`Output: ${data}`);
});

// exec - buffered output
exec('ls -la', (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});

// execFile - no shell
execFile('node', ['--version'], (error, stdout) => {
  console.log(stdout);
});

// fork - for Node.js modules
const child = fork('./worker.js');
child.send({ task: 'processData' });
child.on('message', (result) => {
  console.log('Result:', result);
});

```

---

#### Q14: How do you handle unhandled promise rejections?

**Answer:**

Unhandled promise rejections occur when a promise is rejected but not caught.

```javascript
// Handle unhandled rejections globally
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  // Log to monitoring service
  // Optionally exit process
  // process.exit(1);
});

// Good practices
async function fetchData() {
  try {
    const response = await fetch('https://api.example.com/data');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error; // Re-throw or handle
  }
}

// Always catch promises
fetchData().catch(console.error);

```

---

#### Q15: What is the difference between `Buffer.alloc` and `Buffer.allocUnsafe`?

**Answer:**

- `Buffer.alloc()`: Creates a new buffer filled with zeros (safe)
- `Buffer.allocUnsafe()`: Creates a new buffer with uninitialized memory (faster but potentially insecure)

```javascript
// Safe: zero-filled
const safeBuffer = Buffer.alloc(10);
console.log(safeBuffer); // <Buffer 00 00 00 00 00 00 00 00 00 00>

// Unsafe: may contain old data
const unsafeBuffer = Buffer.allocUnsafe(10);
console.log(unsafeBuffer); // May contain random data

// For sensitive data, always use alloc
const password = Buffer.alloc(32);
password.write('my-secret-password');

// For temporary buffers where security isn't critical
const tempBuffer = Buffer.allocUnsafe(1024);

```

**When to use `allocUnsafe`:**

- When performance is critical
- When you'll immediately overwrite all data
- When the buffer won't be exposed externally

---

#### Q16: How do you implement authentication in Node.js?

**Answer:**

Common authentication methods include JWT, session-based, and OAuth.

```javascript
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// JWT Authentication
const generateToken = (user) => {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '24h' }
  );
};

const verifyToken = (token) => {
  return jwt.verify(token, process.env.JWT_SECRET);
};

// Middleware
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = verifyToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Password hashing
const hashPassword = async (password) => {
  return await bcrypt.hash(password, 10);
};

const comparePassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};

```

---

#### Q17: What is the difference between `readFile` and `createReadStream`?

**Answer:**

- `readFile`: Reads entire file into memory at once
- `createReadStream`: Reads file in chunks (streaming)

```javascript
const fs = require('fs');

// readFile - loads entire file
fs.readFile('large-file.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data.length); // Entire file in memory
});

// createReadStream - streams in chunks
const readStream = fs.createReadStream('large-file.txt', {
  encoding: 'utf8',
  highWaterMark: 1024 // 1KB chunks
});

readStream.on('data', (chunk) => {
  console.log('Chunk length:', chunk.length);
});

readStream.on('end', () => {
  console.log('File reading complete');
});

```

**When to use each:**

- `readFile`: Small files, when you need all data at once
- `createReadStream`: Large files, when you can process data in chunks

---

#### Q18: How do you implement caching in Node.js?

**Answer:**

Caching improves performance by storing frequently accessed data.

```javascript
// Simple in-memory cache
class Cache {
  constructor(ttl = 60000) {
    this.cache = new Map();
    this.ttl = ttl;
  }

  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.value;
  }

  set(key, value, ttl = this.ttl) {
    this.cache.set(key, {
      value,
      expiry: Date.now() + ttl
    });
  }

  delete(key) {
    this.cache.delete(key);
  }
}

// Redis cache
const redis = require('redis');
const client = redis.createClient();

const cacheMiddleware = async (req, res, next) => {
  const key = req.originalUrl;
  const cached = await client.get(key);

  if (cached) {
    return res.json(JSON.parse(cached));
  }

  // Override res.json to cache response
  const originalJson = res.json.bind(res);
  res.json = (body) => {
    client.setex(key, 3600, JSON.stringify(body));
    return originalJson(body);
  };

  next();
};

```

---

#### Q19: What is the difference between `cluster` and `worker_threads`?

**Answer:**

- `cluster`: Creates multiple processes that share a port
- `worker_threads`: Creates threads within the same process

```javascript
// Cluster - separate processes
const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;

if (cluster.isPrimary) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  http.createServer((req, res) => {
    res.end(`Worker ${process.pid}`);
  }).listen(3000);
}

// Worker Threads - same process
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
  const worker = new Worker(__filename);
  worker.on('message', (result) => {
    console.log('Result:', result);
  });
} else {
  // CPU-intensive work
  let sum = 0;
  for (let i = 0; i < 1e9; i++) {
    sum += i;
  }
  parentPort.postMessage(sum);
}

```

**When to use each:**

- `cluster`: For I/O-bound workloads, scaling across CPU cores
- `worker_threads`: For CPU-bound workloads, sharing memory

---

#### Q20: How do you implement logging in Node.js?

**Answer:**

Proper logging is essential for debugging and monitoring.

```javascript
const winston = require('winston');

// Winston logger setup
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

// Usage
logger.info('Server started', { port: 3000 });
logger.error('Database connection failed', { error: err.message });

// Request logging middleware
const morgan = require('morgan');
app.use(morgan('combined'));

```

---

### Senior Questions (10-15)

#### Q21: How would you design a scalable microservices architecture with Node.js?

**Answer:**

Design considerations include service discovery, load balancing, fault tolerance, and data consistency.

```javascript
// Service discovery with Consul
const Consul = require('consul');
const consul = new Consul();

// Register service
await consul.agent.service.register({
  name: 'user-service',
  address: 'localhost',
  port: 3001,
  check: {
    http: 'http://localhost:3001/health',
    interval: '10s'
  }
});

// Discover services
const services = await consul.health.service('user-service');

// Load balancer
class LoadBalancer {
  constructor() {
    this.services = new Map();
  }

  addService(name, instances) {
    this.services.set(name, instances);
  }

  getService(name) {
    const instances = this.services.get(name);
    if (!instances || instances.length === 0) {
      throw new Error(`No instances available for ${name}`);
    }
    // Round-robin
    const index = Math.floor(Math.random() * instances.length);
    return instances[index];
  }
}

// Circuit breaker
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 30000;
    this.failures = 0;
    this.state = 'CLOSED';
    this.nextAttempt = Date.now();
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit is OPEN');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.reset();
      return result;
    } catch (error) {
      this.failures++;
      if (this.failures >= this.failureThreshold) {
        this.state = 'OPEN';
        this.nextAttempt = Date.now() + this.resetTimeout;
      }
      throw error;
    }
  }

  reset() {
    this.failures = 0;
    this.state = 'CLOSED';
  }
}

```

---

#### Q22: How would you implement real-time features with WebSockets?

**Answer:**

WebSockets provide full-duplex communication for real-time applications.

```javascript
const WebSocket = require('ws');
const http = require('http');

const server = http.createServer();
const wss = new WebSocket.Server({ server });

// Connection handling
wss.on('connection', (ws, req) => {
  const userId = req.url.split('=')[1];
  ws.userId = userId;

  console.log(`User ${userId} connected`);

  // Broadcast to all clients
  ws.on('message', (message) => {
    const data = JSON.parse(message);

    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          userId,
          message: data.message,
          timestamp: Date.now()
        }));
      }
    });
  });

  ws.on('close', () => {
    console.log(`User ${userId} disconnected`);
  });
});

// Heartbeat to detect disconnected clients
setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) {
      return ws.terminate();
    }
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

wss.on('connection', (ws) => {
  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });
});

```

---

#### Q23: How do you optimize Node.js performance?

**Answer:**

Performance optimization involves profiling, caching, and code optimization.

```javascript
// 1. Use clustering for multi-core utilization
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isPrimary) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
}

// 2. Implement caching
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 });

const getCachedData = async (key) => {
  let data = cache.get(key);
  if (data) return data;

  data = await fetchExpensiveData();
  cache.set(key, data);
  return data;
};

// 3. Use streaming for large files
const fs = require('fs');
const { pipeline } = require('stream');
const { promisify } = require('util');

const pipelineAsync = promisify(pipeline);

async function processLargeFile(input, output) {
  await pipelineAsync(
    fs.createReadStream(input),
    fs.createWriteStream(output)
  );
}

// 4. Profile and monitor
const { PerformanceObserver } = require('perf_hooks');

const obs = new PerformanceObserver((items) => {
  items.getEntries().forEach((entry) => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});

obs.observe({ entryTypes: ['measure'] });

```

---

#### Q24: How would you implement a task queue system?

**Answer:**

Task queues handle background jobs like sending emails or processing images.

```javascript
const Bull = require('bull');

// Create queues
const emailQueue = new Bull('email', {
  redis: { host: 'localhost', port: 6379 }
});

const imageQueue = new Bull('image', {
  redis: { host: 'localhost', port: 6379 }
});

// Add jobs
await emailQueue.add({
  to: 'user@example.com',
  subject: 'Welcome!',
  template: 'welcome'
});

await imageQueue.add({
  userId: 123,
  imagePath: '/uploads/image.jpg',
  sizes: [100, 200, 400]
}, {
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 2000
  }
});

// Process jobs
emailQueue.process(async (job) => {
  const { to, subject, template } = job.data;
  await sendEmail(to, subject, template);
});

imageQueue.process(async (job) => {
  const { userId, imagePath, sizes } = job.data;

  for (const size of sizes) {
    await resizeImage(imagePath, size);
    await job.progress(size / sizes.length * 100);
  }
});

// Event handlers
emailQueue.on('completed', (job) => {
  console.log(`Email job ${job.id} completed`);
});

emailQueue.on('failed', (job, err) => {
  console.error(`Email job ${job.id} failed:`, err);
});

```

---

#### Q25: How do you implement monitoring and observability?

**Answer:**

Monitoring involves metrics, logging, and tracing.

```javascript
const promClient = require('prom-client');
const opentelemetry = require('@opentelemetry/api');

// Prometheus metrics
const collectDefaultMetrics = promClient.collectDefaultMetrics;
collectDefaultMetrics({ prefix: 'myapp_' });

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

// Middleware to collect metrics
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();

  res.on('finish', () => {
    end({
      method: req.method,
      route: req.route?.path || req.path,
      status_code: res.statusCode
    });
  });

  next();
});

// OpenTelemetry tracing
const tracer = opentelemetry.trace.getTracer('my-app');

app.get('/api/data', async (req, res) => {
  const span = tracer.startSpan('fetch-data');

  try {
    const data = await fetchData();
    span.setStatus({ code: opentelemetry.SpanStatusCode.OK });
    res.json(data);
  } catch (error) {
    span.setStatus({
      code: opentelemetry.SpanStatusCode.ERROR,
      message: error.message
    });
    throw error;
  } finally {
    span.end();
  }
});

```

---

#### Q26: How would you implement API versioning?

**Answer:**

API versioning allows you to evolve your API without breaking existing clients.

```javascript
// URL-based versioning
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Header-based versioning
app.use('/api', (req, res, next) => {
  const version = req.headers['api-version'] || 'v1';

  switch (version) {
    case 'v1':
      return v1Router(req, res, next);
    case 'v2':
      return v2Router(req, res, next);
    default:
      return res.status(400).json({ error: 'Invalid API version' });
  }
});

// Query parameter versioning
app.get('/api/data', (req, res, next) => {
  const version = req.query.version || 'v1';

  if (version === 'v2') {
    return v2Handler(req, res, next);
  }

  return v1Handler(req, res, next);
});

```

---

#### Q27: How do you handle database connections in a clustered environment?

**Answer:**

Database connections need careful management in clustered environments.

```javascript
const { Pool } = require('pg');
const cluster = require('cluster');

// Connection pool configuration
const poolConfig = {
  max: 20, // Max connections per worker
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
};

if (cluster.isPrimary) {
  // Primary process
  const pool = new Pool({
    ...poolConfig,
    max: 100 // More connections for primary
  });
} else {
  // Worker process
  const pool = new Pool(poolConfig);

  // Graceful shutdown
  process.on('SIGTERM', async () => {
    await pool.end();
    process.exit(0);
  });
}

// Query helper with retry logic
async function query(text, params) {
  const maxRetries = 3;
  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      const result = await pool.query(text, params);
      return result;
    } catch (error) {
      lastError = error;
      if (error.code === 'ECONNRESET') {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
      } else {
        throw error;
      }
    }
  }

  throw lastError;
}

```

---

#### Q28: How would you implement a message queue system?

**Answer:**

Message queues enable asynchronous communication between services.

```javascript
const amqp = require('amqplib');

class MessageQueue {
  constructor(url) {
    this.url = url;
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    this.connection = await amqp.connect(this.url);
    this.channel = await this.connection.createChannel();
  }

  async publish(queue, message) {
    await this.channel.assertQueue(queue, { durable: true });
    this.channel.sendToQueue(queue, Buffer.from(JSON.stringify(message)), {
      persistent: true
    });
  }

  async consume(queue, handler) {
    await this.channel.assertQueue(queue, { durable: true });

    this.channel.consume(queue, async (msg) => {
      try {
        const content = JSON.parse(msg.content.toString());
        await handler(content);
        this.channel.ack(msg);
      } catch (error) {
        console.error('Error processing message:', error);
        this.channel.nack(msg, false, true);
      }
    });
  }

  async close() {
    await this.channel.close();
    await this.connection.close();
  }
}

// Usage
const mq = new MessageQueue('amqp://localhost');
await mq.connect();

// Publish
await mq.publish('orders', { id: 1, product: 'Widget' });

// Consume
await mq.consume('orders', async (order) => {
  console.log('Processing order:', order);
  await processOrder(order);
});

```

---

#### Q29: How do you implement error boundaries in Express?

**Answer:**

Error boundaries catch and handle errors gracefully.

```javascript
// Custom error classes
class AppError extends Error {
  constructor(message, statusCode, code) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.isOperational = true;
  }
}

class ValidationError extends AppError {
  constructor(message, errors) {
    super(message, 400, 'VALIDATION_ERROR');
    this.errors = errors;
  }
}

// Error handling middleware
const errorHandler = (err, req, res, next) => {
  if (err.isOperational) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.errors
      }
    });
  }

  // Log unexpected errors
  console.error('Unexpected error:', err);

  // Send generic response
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
};

// Async error wrapper
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage
app.get('/api/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    throw new AppError('User not found', 404, 'USER_NOT_FOUND');
  }

  res.json(user);
}));

app.use(errorHandler);

```

---

#### Q30: How would you implement a distributed caching system?

**Answer:**

Distributed caching improves performance across multiple nodes.

```javascript
const Redis = require('ioredis');
const cluster = require('cluster');

class DistributedCache {
  constructor() {
    this.redis = new Redis({
      host: 'localhost',
      port: 6379,
      retryDelayOnFailover: 100,
      maxRetriesPerRequest: 3
    });
  }

  async get(key) {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key, value, ttl = 3600) {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async delete(key) {
    await this.redis.del(key);
  }

  async invalidatePattern(pattern) {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  // Cache-aside pattern
  async getOrSet(key, fetchFn, ttl = 3600) {
    let data = await this.get(key);

    if (!data) {
      data = await fetchFn();
      await this.set(key, data, ttl);
    }

    return data;
  }
}

// Usage in clustered environment
if (cluster.isPrimary) {
  // Primary process manages cache invalidation
  const cache = new DistributedCache();

  cluster.on('message', (worker, msg) => {
    if (msg.type === 'CACHE_INVALIDATE') {
      cache.invalidatePattern(msg.pattern);
    }
  });
} else {
  // Worker process uses cache
  const cache = new DistributedCache();

  app.get('/api/users', async (req, res) => {
    const users = await cache.getOrSet(
      'users:all',
      () => User.findAll(),
      300
    );
    res.json(users);
  });
}

```

---

### FAANG-style Questions (5-10)

#### Q31: Design a URL shortener service like bit.ly

**Answer:**

Key components: URL validation, short code generation, redirect handling, analytics.

```javascript
const express = require('express');
const { nanoid } = require('nanoid');
const redis = require('redis');

const app = express();
const redisClient = redis.createClient();

class UrlShortener {
  constructor() {
    this.cache = new Map();
  }

  async shorten(url) {
    // Validate URL
    if (!this.isValidUrl(url)) {
      throw new Error('Invalid URL');
    }

    // Check cache
    if (this.cache.has(url)) {
      return this.cache.get(url);
    }

    // Generate short code
    const shortCode = nanoid(7);

    // Store in database
    await this.storeUrl(shortCode, url);

    // Cache for future lookups
    this.cache.set(url, shortCode);

    return shortCode;
  }

  async redirect(shortCode) {
    // Check cache first
    const cached = await redisClient.get(`redirect:${shortCode}`);
    if (cached) {
      return cached;
    }

    // Get from database
    const url = await this.getUrl(shortCode);
    if (!url) {
      throw new Error('URL not found');
    }

    // Cache for 1 hour
    await redisClient.setex(`redirect:${shortCode}`, 3600, url);

    // Track analytics
    await this.trackClick(shortCode);

    return url;
  }

  isValidUrl(url) {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  async storeUrl(shortCode, url) {
    // Store in database
  }

  async getUrl(shortCode) {
    // Get from database
  }

  async trackClick(shortCode) {
    // Track click analytics
  }
}

const shortener = new UrlShortener();

app.post('/shorten', async (req, res) => {
  try {
    const shortCode = await shortener.shorten(req.body.url);
    res.json({ shortCode, shortUrl: `http://short.url/${shortCode}` });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.get('/:shortCode', async (req, res) => {
  try {
    const url = await shortener.redirect(req.params.shortCode);
    res.redirect(301, url);
  } catch (error) {
    res.status(404).json({ error: 'URL not found' });
  }
});

```

---

#### Q32: Design a real-time chat application

**Answer:**

Key components: WebSocket server, message persistence, user management, presence.

```javascript
const WebSocket = require('ws');
const http = require('http');
const Redis = require('ioredis');

class ChatServer {
  constructor() {
    this.wss = new WebSocket.Server({ port: 8080 });
    this.redis = new Redis();
    this.clients = new Map(); // userId -> WebSocket

    this.setupWebSocket();
  }

  setupWebSocket() {
    this.wss.on('connection', (ws, req) => {
      const userId = this.authenticate(req);

      if (!userId) {
        ws.close(1008, 'Unauthorized');
        return;
      }

      this.clients.set(userId, ws);
      this.broadcastPresence();

      ws.on('message', (message) => {
        this.handleMessage(userId, JSON.parse(message));
      });

      ws.on('close', () => {
        this.clients.delete(userId);
        this.broadcastPresence();
      });
    });
  }

  async handleMessage(senderId, message) {
    const { type, roomId, content } = message;

    switch (type) {
      case 'chat':
        await this.handleChatMessage(senderId, roomId, content);
        break;
      case 'join':
        await this.handleJoinRoom(senderId, roomId);
        break;
      case 'leave':
        await this.handleLeaveRoom(senderId, roomId);
        break;
    }
  }

  async handleChatMessage(senderId, roomId, content) {
    // Store message in Redis
    const message = {
      senderId,
      roomId,
      content,
      timestamp: Date.now()
    };

    await this.redis.lpush(`room:${roomId}:messages`, JSON.stringify(message));
    await this.redis.ltrim(`room:${roomId}:messages`, 0, 999);

    // Broadcast to room members
    const members = await this.getRoomMembers(roomId);

    for (const memberId of members) {
      const client = this.clients.get(memberId);
      if (client && client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'message',
          message
        }));
      }
    }
  }

  broadcastPresence() {
    const onlineUsers = Array.from(this.clients.keys());

    this.wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'presence',
          users: onlineUsers
        }));
      }
    });
  }

  authenticate(req) {
    // Verify authentication token
    return null;
  }

  async getRoomMembers(roomId) {
    return await this.redis.smembers(`room:${roomId}:members`);
  }
}

new ChatServer();

```

---

#### Q33: Design a distributed file storage system

**Answer:**

Key components: chunking, replication, metadata management, consistency.

```javascript
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class DistributedStorage {
  constructor(storageNodes) {
    this.nodes = storageNodes;
    this.replicationFactor = 3;
  }

  async upload(file) {
    const fileHash = await this.calculateHash(file);
    const chunks = await this.chunkFile(file);

    // Store metadata
    await this.storeMetadata(fileHash, {
      chunks: chunks.length,
      size: file.size,
      createdAt: Date.now()
    });

    // Distribute chunks across nodes
    for (let i = 0; i < chunks.length; i++) {
      const chunk = chunks[i];
      const nodes = this.selectNodes(i, this.replicationFactor);

      for (const node of nodes) {
        await this.storeChunk(node, fileHash, i, chunk);
      }
    }

    return fileHash;
  }

  async download(fileHash) {
    const metadata = await this.getMetadata(fileHash);
    const chunks = [];

    for (let i = 0; i < metadata.chunks; i++) {
      const chunk = await this.retrieveChunk(fileHash, i);
      chunks.push(chunk);
    }

    return Buffer.concat(chunks);
  }

  async chunkFile(file, chunkSize = 1024 * 1024) {
    const buffer = fs.readFileSync(file);
    const chunks = [];

    for (let i = 0; i < buffer.length; i += chunkSize) {
      chunks.push(buffer.slice(i, i + chunkSize));
    }

    return chunks;
  }

  selectNodes(chunkIndex, count) {
    // Consistent hashing to select nodes
    const nodes = [];
    for (let i = 0; i < count; i++) {
      nodes.push(this.nodes[(chunkIndex + i) % this.nodes.length]);
    }
    return nodes;
  }

  async calculateHash(file) {
    return new Promise((resolve) => {
      const hash = crypto.createHash('sha256');
      const stream = fs.createReadStream(file);

      stream.on('data', (data) => hash.update(data));
      stream.on('end', () => resolve(hash.digest('hex')));
    });
  }
}

```

---

#### Q34: Design a task scheduling system

**Answer:**

Key components: job queues, scheduling, retry logic, monitoring.

```javascript
const Bull = require('bull');
const cron = require('cron');

class TaskScheduler {
  constructor() {
    this.queues = new Map();
    this.jobs = new Map();
  }

  createQueue(name, options = {}) {
    const queue = new Bull(name, {
      redis: { host: 'localhost', port: 6379 },
      ...options
    });

    this.queues.set(name, queue);
    return queue;
  }

  async scheduleRecurringJob(queueName, cronExpression, data) {
    const queue = this.queues.get(queueName);

    // Add job with repeat option
    await queue.add(data, {
      repeat: { cron: cronExpression },
      removeOnComplete: 100,
      removeOnFail: 50
    });
  }

  async scheduleDelayedJob(queueName, data, delay) {
    const queue = this.queues.get(queueName);

    await queue.add(data, {
      delay,
      attempts: 3,
      backoff: {
        type: 'exponential',
        delay: 2000
      }
    });
  }

  processJob(queueName, handler) {
    const queue = this.queues.get(queueName);

    queue.process(async (job) => {
      try {
        console.log(`Processing job ${job.id} in queue ${queueName}`);
        const result = await handler(job.data);
        return result;
      } catch (error) {
        console.error(`Job ${job.id} failed:`, error);
        throw error;
      }
    });

    queue.on('completed', (job) => {
      console.log(`Job ${job.id} completed`);
    });

    queue.on('failed', (job, error) => {
      console.error(`Job ${job.id} failed:`, error);
    });
  }

  async getJobStats(queueName) {
    const queue = this.queues.get(queueName);

    const [waiting, active, completed, failed] = await Promise.all([
      queue.getWaitingCount(),
      queue.getActiveCount(),
      queue.getCompletedCount(),
      queue.getFailedCount()
    ]);

    return { waiting, active, completed, failed };
  }
}

// Usage
const scheduler = new TaskScheduler();

// Create queues
scheduler.createQueue('emails');
scheduler.createQueue('reports');

// Schedule recurring job (daily at 9 AM)
await scheduler.scheduleRecurringJob('reports', '0 9 * * *', {
  type: 'daily-report'
});

// Schedule delayed job (process in 5 minutes)
await scheduler.scheduleDelayedJob('emails', {
  to: 'user@example.com',
  subject: 'Reminder'
}, 5 * 60 * 1000);

// Process jobs
scheduler.processJob('emails', async (data) => {
  await sendEmail(data.to, data.subject);
});

scheduler.processJob('reports', async (data) => {
  await generateReport(data.type);
});

```

---

#### Q35: How would you implement a payment processing system?

**Answer:**

Key components: idempotency, webhook handling, retry logic, reconciliation.

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

class PaymentProcessor {
  constructor() {
    this.idempotencyKeys = new Map();
  }

  async createPaymentIntent(amount, currency, metadata) {
    const idempotencyKey = this.generateIdempotencyKey();

    try {
      const paymentIntent = await stripe.paymentIntents.create({
        amount,
        currency,
        metadata,
        automatic_payment_methods: { enabled: true }
      }, {
        idempotencyKey
      });

      return {
        id: paymentIntent.id,
        clientSecret: paymentIntent.client_secret,
        status: paymentIntent.status
      };
    } catch (error) {
      console.error('Payment creation failed:', error);
      throw error;
    }
  }

  async handleWebhook(event) {
    // Verify webhook signature
    const sig = event.headers['stripe-signature'];
    let stripeEvent;

    try {
      stripeEvent = stripe.webhooks.constructEvent(
        event.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } catch (err) {
      throw new Error(`Webhook signature verification failed`);
    }

    // Handle different event types
    switch (stripeEvent.type) {
      case 'payment_intent.succeeded':
        await this.handlePaymentSuccess(stripeEvent.data.object);
        break;
      case 'payment_intent.payment_failed':
        await this.handlePaymentFailure(stripeEvent.data.object);
        break;
      case 'charge.refunded':
        await this.handleRefund(stripeEvent.data.object);
        break;
    }
  }

  async handlePaymentSuccess(paymentIntent) {
    // Update order status
    await this.updateOrderStatus(paymentIntent.metadata.orderId, 'paid');

    // Send confirmation email
    await this.sendConfirmationEmail(paymentIntent.metadata.email);

    // Update inventory
    await this.updateInventory(paymentIntent.metadata.items);
  }

  async handlePaymentFailure(paymentIntent) {
    // Notify customer
    await this.sendPaymentFailedEmail(paymentIntent.metadata.email);

    // Update order status
    await this.updateOrderStatus(paymentIntent.metadata.orderId, 'payment_failed');
  }

  generateIdempotencyKey() {
    return `pay_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Webhook endpoint
app.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  try {
    await paymentProcessor.handleWebhook({
      headers: req.headers,
      body: req.body
    });
    res.json({ received: true });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

```

---

#### Q36: Design a content delivery network (CDN) edge

**Answer:**

Key components: caching, routing, origin selection, health checks.

```javascript
const httpProxy = require('http-proxy');
const Redis = require('ioredis');

class CDNEdge {
  constructor() {
    this.proxy = httpProxy.createProxyServer({});
    this.redis = new Redis();
    this.origins = [
      { url: 'http://origin1.example.com', weight: 1 },
      { url: 'http://origin2.example.com', weight: 1 }
    ];
    this.healthStatus = new Map();
  }

  async handleRequest(req, res) {
    const cacheKey = this.getCacheKey(req);

    // Check cache
    const cached = await this.getFromCache(cacheKey);
    if (cached) {
      res.writeHead(200, { 'X-Cache': 'HIT' });
      res.end(cached);
      return;
    }

    // Select origin
    const origin = this.selectOrigin();

    // Proxy request
    this.proxy.web(req, res, {
      target: origin.url,
      changeOrigin: true
    }, (error) => {
      console.error('Proxy error:', error);
      res.writeHead(502);
      res.end('Bad Gateway');
    });

    // Cache response
    this.proxy.on('proxyRes', (proxyRes, req, res) => {
      let body = [];
      proxyRes.on('data', (chunk) => body.push(chunk));
      proxyRes.on('end', () => {
        const content = Buffer.concat(body);
        this.cacheResponse(cacheKey, content, proxyRes.headers);
      });
    });
  }

  selectOrigin() {
    // Weighted random selection based on health
    const healthyOrigins = this.origins.filter(
      (origin) => this.healthStatus.get(origin.url) !== false
    );

    if (healthyOrigins.length === 0) {
      return this.origins[0]; // Fallback
    }

    const totalWeight = healthyOrigins.reduce(
      (sum, origin) => sum + origin.weight, 0
    );

    let random = Math.random() * totalWeight;

    for (const origin of healthyOrigins) {
      random -= origin.weight;
      if (random <= 0) {
        return origin;
      }
    }

    return healthyOrigins[0];
  }

  async getFromCache(key) {
    const data = await this.redis.get(`cache:${key}`);
    return data ? Buffer.from(data, 'base64') : null;
  }

  async cacheResponse(key, content, headers) {
    const ttl = this.getCacheTTL(headers);
    await this.redis.setex(
      `cache:${key}`,
      ttl,
      content.toString('base64')
    );
  }

  getCacheKey(req) {
    return `${req.method}:${req.url}`;
  }

  getCacheTTL(headers) {
    // Default 1 hour, can be overridden by origin
    return parseInt(headers['cache-control']?.maxage) || 3600;
  }

  async checkOriginHealth(origin) {
    try {
      const response = await fetch(`${origin.url}/health`);
      this.healthStatus.set(origin.url, response.ok);
    } catch {
      this.healthStatus.set(origin.url, false);
    }
  }
}

```

---

#### Q37: How would you implement feature flags in Node.js?

**Answer:**

Feature flags enable gradual rollouts and A/B testing.

```javascript
class FeatureFlagService {
  constructor() {
    this.flags = new Map();
    this.userSegments = new Map();
  }

  async initialize() {
    // Load flags from database/config
    const flags = await this.loadFlags();

    for (const flag of flags) {
      this.flags.set(flag.key, {
        enabled: flag.enabled,
        percentage: flag.percentage,
        variants: flag.variants,
        rules: flag.rules
      });
    }
  }

  isEnabled(flagKey, context = {}) {
    const flag = this.flags.get(flagKey);

    if (!flag) {
      return false;
    }

    // Check if globally disabled
    if (!flag.enabled) {
      return false;
    }

    // Check rules
    if (flag.rules && flag.rules.length > 0) {
      return this.evaluateRules(flag.rules, context);
    }

    // Check percentage rollout
    if (flag.percentage < 100) {
      return this.isInPercentage(context.userId, flag.percentage);
    }

    return true;
  }

  getVariant(flagKey, context = {}) {
    const flag = this.flags.get(flagKey);

    if (!flag || !flag.variants) {
      return null;
    }

    // Consistent hashing for variant assignment
    const hash = this.hashString(`${flagKey}:${context.userId}`);
    const variantIndex = hash % flag.variants.length;

    return flag.variants[variantIndex];
  }

  evaluateRules(rules, context) {
    for (const rule of rules) {
      if (this.matchRule(rule, context)) {
        return rule.enabled;
      }
    }
    return false;
  }

  matchRule(rule, context) {
    const { attribute, operator, values } = rule;
    const value = context[attribute];

    switch (operator) {
      case 'in':
        return values.includes(value);
      case 'not_in':
        return !values.includes(value);
      case 'greater_than':
        return value > values[0];
      case 'less_than':
        return value < values[0];
      default:
        return false;
    }
  }

  isInPercentage(userId, percentage) {
    const hash = this.hashString(userId.toString());
    return (hash % 100) < percentage;
  }

  hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash);
  }
}

// Middleware
const featureFlags = new FeatureFlagService();
await featureFlags.initialize();

app.use((req, res, next) => {
  req.featureFlags = {
    isEnabled: (flag) => featureFlags.isEnabled(flag, {
      userId: req.user?.id,
      ...req.query
    }),
    getVariant: (flag) => featureFlags.getVariant(flag, {
      userId: req.user?.id
    })
  };
  next();
});

// Usage
app.get('/api/checkout', (req, res) => {
  if (req.featureFlags.isEnabled('new-checkout-flow')) {
    return newCheckoutHandler(req, res);
  }
  return legacyCheckoutHandler(req, res);
});

```

---

#### Q38: Design a real-time analytics pipeline

**Answer:**

Key components: event ingestion, processing, storage, visualization.

```javascript
const { Transform } = require('stream');
const Kafka = require('kafkajs');

class AnalyticsPipeline {
  constructor() {
    this.kafka = new Kafka({
      clientId: 'analytics',
      brokers: ['localhost:9092']
    });
    this.producer = this.kafka.producer();
    this.consumer = this.kafka.consumer({ groupId: 'analytics-group' });
  }

  async initialize() {
    await this.producer.connect();
    await this.consumer.connect();

    await this.consumer.subscribe({ topic: 'events' });
    await this.consumer.run({
      eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value.toString());
        await this.processEvent(event);
      }
    });
  }

  async ingestEvent(event) {
    await this.producer.send({
      topic: 'events',
      messages: [{
        key: event.userId,
        value: JSON.stringify({
          ...event,
          timestamp: Date.now()
        })
      }]
    });
  }

  async processEvent(event) {
    // Enrich event
    const enriched = await this.enrichEvent(event);

    // Store in real-time database
    await this.storeRealTime(enriched);

    // Aggregate for time series
    await this.aggregate(enriched);

    // Check for alerts
    await this.checkAlerts(enriched);
  }

  async enrichEvent(event) {
    // Add user properties, location, etc.
    const user = await this.getUser(event.userId);

    return {
      ...event,
      userProperties: user.properties,
      geoLocation: await this.getGeoLocation(event.ip)
    };
  }

  async storeRealTime(event) {
    // Store in Redis for real-time access
    await this.redis.zadd(
      `analytics:${event.eventName}`,
      event.timestamp,
      JSON.stringify(event)
    );

    // Keep only last 24 hours
    const cutoff = Date.now() - 24 * 60 * 60 * 1000;
    await this.redis.zremrangebyscore(
      `analytics:${event.eventName}`,
      0,
      cutoff
    );
  }

  async aggregate(event) {
    // Time-based aggregation
    const minute = Math.floor(event.timestamp / 60000) * 60000;

    await this.redis.hincrby(
      `aggregated:${event.eventName}:${minute}`,
      'count',
      1
    );

    await this.redis.hincrbyfloat(
      `aggregated:${event.eventName}:${minute}`,
      'totalValue',
      event.value || 0
    );
  }

  async getMetrics(eventName, timeRange) {
    const metrics = [];
    const now = Date.now();

    for (let i = 0; i < timeRange; i++) {
      const minute = now - (i * 60000);
      const key = `aggregated:${eventName}:${minute}`;

      const data = await this.redis.hgetall(key);
      metrics.unshift({
        timestamp: minute,
        count: parseInt(data.count) || 0,
        totalValue: parseFloat(data.totalValue) || 0
      });
    }

    return metrics;
  }
}

```

---

#### Q39: How would you implement a service mesh for microservices?

**Answer:**

Service mesh handles service-to-service communication, security, and observability.

```javascript
const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader');

class ServiceMesh {
  constructor() {
    this.services = new Map();
    this.proxy = new ProxyService();
    this.circuitBreakers = new Map();
  }

  registerService(name, config) {
    this.services.set(name, {
      name,
      endpoints: config.endpoints,
      healthCheck: config.healthCheck,
      loadBalancer: config.loadBalancer || 'round-robin'
    });

    // Start health checking
    this.startHealthCheck(name);
  }

  async route(serviceName, request) {
    // Get healthy endpoints
    const endpoints = await this.getHealthyEndpoints(serviceName);

    if (endpoints.length === 0) {
      throw new Error(`No healthy endpoints for ${serviceName}`);
    }

    // Select endpoint based on load balancing
    const endpoint = this.selectEndpoint(endpoints, serviceName);

    // Check circuit breaker
    const circuitBreaker = this.getCircuitBreaker(serviceName);

    try {
      const response = await circuitBreaker.call(async () => {
        return await this.proxy.forward(endpoint, request);
      });

      this.recordSuccess(serviceName, endpoint);
      return response;
    } catch (error) {
      this.recordFailure(serviceName, endpoint, error);
      throw error;
    }
  }

  getCircuitBreaker(serviceName) {
    if (!this.circuitBreakers.has(serviceName)) {
      this.circuitBreakers.set(serviceName, new CircuitBreaker({
        failureThreshold: 5,
        resetTimeout: 30000
      }));
    }
    return this.circuitBreakers.get(serviceName);
  }

  selectEndpoint(endpoints, serviceName) {
    const service = this.services.get(serviceName);

    switch (service.loadBalancer) {
      case 'round-robin':
        return this.roundRobin(endpoints);
      case 'weighted':
        return this.weightedRandom(endpoints);
      case 'least-connections':
        return this.leastConnections(endpoints);
      default:
        return endpoints[0];
    }
  }

  roundRobin(endpoints) {
    const index = Math.floor(Math.random() * endpoints.length);
    return endpoints[index];
  }

  async startHealthCheck(serviceName) {
    const service = this.services.get(serviceName);

    setInterval(async () => {
      for (const endpoint of service.endpoints) {
        try {
          const healthy = await this.checkHealth(endpoint);
          endpoint.healthy = healthy;
        } catch {
          endpoint.healthy = false;
        }
      }
    }, 10000);
  }

  async checkHealth(endpoint) {
    // Implement health check logic
    return true;
  }
}

class CircuitBreaker {
  constructor(options) {
    this.failureThreshold = options.failureThreshold;
    this.resetTimeout = options.resetTimeout;
    this.failures = 0;
    this.state = 'CLOSED';
    this.nextAttempt = Date.now();
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit is OPEN');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.failures = 0;
      this.state = 'CLOSED';
      return result;
    } catch (error) {
      this.failures++;
      if (this.failures >= this.failureThreshold) {
        this.state = 'OPEN';
        this.nextAttempt = Date.now() + this.resetTimeout;
      }
      throw error;
    }
  }
}

```

---

#### Q40: Design a distributed rate limiter

**Answer:**

Key components: algorithm choice, distribution, consistency, failure handling.

```javascript
const Redis = require('ioredis');

class DistributedRateLimiter {
  constructor(options = {}) {
    this.redis = new Redis(options.redis);
    this.windowMs = options.windowMs || 60000;
    this.maxRequests = options.maxRequests || 100;
    this.algorithm = options.algorithm || 'sliding-window';
  }

  async isAllowed(identifier) {
    switch (this.algorithm) {
      case 'token-bucket':
        return await this.tokenBucket(identifier);
      case 'sliding-window':
        return await this.slidingWindow(identifier);
      case 'fixed-window':
        return await this.fixedWindow(identifier);
      case 'leaky-bucket':
        return await this.leakyBucket(identifier);
      default:
        return await this.slidingWindow(identifier);
    }
  }

  async slidingWindow(identifier) {
    const key = `ratelimit:${identifier}`;
    const now = Date.now();
    const windowStart = now - this.windowMs;

    // Use Redis pipeline for atomicity
    const pipeline = this.redis.pipeline();

    // Remove old entries
    pipeline.zremrangebyscore(key, 0, windowStart);

    // Add current request
    pipeline.zadd(key, now, `${now}`);

    // Count requests in window
    pipeline.zcard(key);

    // Set expiry
    pipeline.expire(key, Math.ceil(this.windowMs / 1000));

    const results = await pipeline.exec();
    const requestCount = results[2][1];

    return requestCount <= this.maxRequests;
  }

  async tokenBucket(identifier) {
    const key = `ratelimit:${identifier}`;
    const now = Date.now();

    const script = `
      local key = KEYS[1]
      local maxTokens = tonumber(ARGV[1])
      local refillRate = tonumber(ARGV[2])
      local now = tonumber(ARGV[3])

      local bucket = redis.call('hmget', key, 'tokens', 'last_refill')
      local tokens = tonumber(bucket[1]) or maxTokens
      local lastRefill = tonumber(bucket[2]) or now

      -- Refill tokens
      local elapsed = now - lastRefill
      local refill = math.floor(elapsed * refillRate / 1000)
      tokens = math.min(maxTokens, tokens + refill)

      -- Try to consume token
      if tokens >= 1 then
        tokens = tokens - 1
        redis.call('hmset', key, 'tokens', tokens, 'last_refill', now)
        redis.call('expire', key, math.ceil(maxTokens / refillRate * 1000))
        return 1
      else
        return 0
      end
    `;

    const result = await this.redis.eval(
      script,
      1,
      key,
      this.maxRequests,
      this.maxRequests / (this.windowMs / 1000),
      now
    );

    return result === 1;
  }

  async fixedWindow(identifier) {
    const window = Math.floor(Date.now() / this.windowMs);
    const key = `ratelimit:${identifier}:${window}`;

    const pipeline = this.redis.pipeline();
    pipeline.incr(key);
    pipeline.expire(key, Math.ceil(this.windowMs / 1000));

    const results = await pipeline.exec();
    const requestCount = results[0][1];

    return requestCount <= this.maxRequests;
  }

  async leakyBucket(identifier) {
    const key = `ratelimit:${identifier}`;
    const now = Date.now();

    const script = `
      local key = KEYS[1]
      local capacity = tonumber(ARGV[1])
      local leakRate = tonumber(ARGV[2])
      local now = tonumber(ARGV[3])

      local bucket = redis.call('hmget', key, 'water', 'last_leak')
      local water = tonumber(bucket[1]) or 0
      local lastLeak = tonumber(bucket[2]) or now

      -- Leak water
      local elapsed = now - lastLeak
      local leaked = math.floor(elapsed * leakRate / 1000)
      water = math.max(0, water - leaked)

      -- Try to add request
      if water < capacity then
        water = water + 1
        redis.call('hmset', key, 'water', water, 'last_leak', now)
        redis.call('expire', key, math.ceil(capacity / leakRate * 1000))
        return 1
      else
        return 0
      end
    `;

    const result = await this.redis.eval(
      script,
      1,
      key,
      this.maxRequests,
      this.maxRequests / (this.windowMs / 1000),
      now
    );

    return result === 1;
  }

  async reset(identifier) {
    const key = `ratelimit:${identifier}`;
    await this.redis.del(key);
  }

  async getUsage(identifier) {
    const key = `ratelimit:${identifier}`;
    const windowStart = Date.now() - this.windowMs;

    const count = await this.redis.zcount(key, windowStart, '+inf');
    return {
      used: count,
      remaining: Math.max(0, this.maxRequests - count),
      total: this.maxRequests
    };
  }
}

// Express middleware
const rateLimiter = new DistributedRateLimiter({
  windowMs: 60000,
  maxRequests: 100,
  algorithm: 'sliding-window'
});

app.use(async (req, res, next) => {
  const identifier = `${req.ip}:${req.path}`;

  try {
    const allowed = await rateLimiter.isAllowed(identifier);
    const usage = await rateLimiter.getUsage(identifier);

    res.set({
      'X-RateLimit-Limit': usage.total,
      'X-RateLimit-Remaining': usage.remaining,
      'X-RateLimit-Reset': new Date(Date.now() + 60000).toISOString()
    });

    if (!allowed) {
      return res.status(429).json({
        error: 'Too many requests',
        retryAfter: Math.ceil(60000 / 1000)
      });
    }

    next();
  } catch (error) {
    // Fail open - allow request if rate limiter fails
    next();
  }
});

```

---

## Summary

These 40 questions cover the most important Node.js concepts for technical interviews. Key areas include:

- **Event Loop**: Understanding phases and microtasks
- **Streams**: Processing data efficiently
- **Buffers**: Handling binary data
- **Clustering**: Scaling across CPU cores
- **Error Handling**: Graceful error management
- **Performance**: Optimization techniques
- **Architecture**: System design patterns
- **Security**: Authentication and authorization
- **Monitoring**: Observability and metrics
- **Distributed Systems**: Scaling and reliability

## Cheat Sheet

```text
┌───────────────────────────────────────────────────────────────┐
│              NODE.JS INTERVIEW CHEAT SHEET                   │
├───────────────────────────────────────────────────────────────┤
│                                                              │
│  CORE CONCEPTS:                                              │
│  • Event Loop: phases (timers, pending, poll, check, close)  │
│  • Microtasks: process.nextTick > Promise callbacks          │
│  • Streams: Readable, Writable, Duplex, Transform            │
│  • Buffers: binary data handling, encoding                   │
│  • Clustering: multi-core utilization                        │
│                                                              │
│  COMMON PATTERNS:                                            │
│  • Error-first callbacks                                     │
│  • Promise chains / async-await                              │
│  • Middleware pattern                                         │
│  • Observer pattern                                          │
│  • Factory pattern                                           │
│                                                              │
│  PERFORMANCE:                                                │
│  • Use clustering for I/O-bound                              │
│  • Use worker_threads for CPU-bound                          │
│  • Implement caching (Redis)                                 │
│  • Use streams for large data                                │
│  • Monitor event loop lag                                    │
│                                                              │
│  SECURITY:                                                   │
│  • Use HTTPS                                                 │
│  • Validate input                                            │
│  • Rate limiting                                             │
│  • Authentication (JWT, OAuth)                               │
│  • Security headers (helmet)                                 │
│                                                              │
│  TESTING:                                                    │
│  • Unit tests (Jest, Mocha)                                  │
│  • Integration tests                                         │
│  • Load testing (Artillery)                                  │
│  • Mock external services                                    │
│                                                              │
│  TOOLS:                                                      │
│  • npm/yarn/pnpm - package management                        │
│  • ESLint/Prettier - code quality                            │
│  • TypeScript - type safety                                  │
│  • PM2/forever - process management                          │
│  • Docker - containerization                                 │
│                                                              │
│  DEBUGGING:                                                  │
│  • node --inspect                                            │
│  • Chrome DevTools                                           │
│  • Winston/Morgan - logging                                  │
│  • APM tools (New Relic, Datadog)                            │
│                                                              │
└───────────────────────────────────────────────────────────────┘

```

## References & Learn More

- [Node.js Official Docs](https://nodejs.org/en/docs)
- [Node.js Design Patterns](https://www.nodejsdesignpatterns.com/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Awesome Node.js](https://github.com/sindresorhus/awesome-nodejs)