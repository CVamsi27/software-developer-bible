---
section: Node.js
category: Backend
tags: [concept]
---

# Process & Environment

The `process` object is a global Node.js API that provides information about the current Node.js process and control over its execution. It gives access to environment variables, command-line arguments, process lifecycle events, system information, and process control methods.

## Definition

The `process` object is a global that can be accessed from any module without importing. It provides:

- **Environment**: `process.env` for environment variables
- **Arguments**: `process.argv` for CLI arguments
- **Lifecycle**: process exit, signals (`SIGINT`, `SIGTERM`), `beforeExit`
- **System info**: platform, architecture, Node.js version, memory usage, CPU usage
- **Process control**: `process.exit()`, `process.chdir()`, `process.umask()`, `process.uptime()`
- **Standard I/O**: `process.stdin`, `process.stdout`, `process.stderr`

## Why Do We Need It?

1. **Configuration**: Read environment variables for different environments (dev, staging, prod)

2. **CLI tools**: Parse command-line arguments for building CLI applications

3. **Graceful shutdown**: Handle `SIGTERM`/`SIGINT` for clean process termination

4. **Monitoring**: Track memory usage, CPU usage, and uptime for health checks

5. **Portability**: Write cross-platform code using `process.platform` and `process.arch`

6. **Standard I/O**: Read input from stdin and write formatted output

## How It Works

### Process Lifecycle

```text
┌─────────────────────────────────────────────────────────────┐
│                    NODE.JS PROCESS LIFECYCLE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  node app.js                                                 │
│       │                                                     │
│       ▼                                                     │
│  Module evaluation                                           │
│       │                                                     │
│       ▼                                                     │
│  Event Loop started                                          │
│       │                                                     │
│       ▼                                                     │
│  Process execution (timers, I/O, callbacks)                  │
│       │                                                     │
│       ├── SIGINT → exit(0)                                  │
│       ├── SIGTERM → exit(0)                                 │
│       ├── uncaughtException → exit(1)                       │
│       └── Event loop empty → process.on('beforeExit')       │
│                                                              │
│       ▼                                                     │
│  Process exit                                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples (Node.js)

### Environment Variables

```javascript
// Read environment variables
const env = process.env;

console.log(env.NODE_ENV);        // 'development', 'production', 'test'
console.log(env.PORT);            // '3000'
console.log(env.DATABASE_URL);    // 'postgres://...'

// Set environment variable (only affects current process)
process.env.MY_VAR = 'value';
console.log(process.env.MY_VAR); // 'value'

// Default values pattern
const port = process.env.PORT || 3000;
const nodeEnv = process.env.NODE_ENV || 'development';
const isProduction = nodeEnv === 'production';

// Type conversion
const maxConnections = parseInt(process.env.MAX_CONNECTIONS || '10', 10);
const enableDebug = process.env.DEBUG === 'true';
const timeout = Number(process.env.TIMEOUT_MS) || 5000;

// Required env vars
function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

// .env loading pattern (simplified)
function loadEnvFile(path = '.env') {
  const fs = require('fs');
  try {
    const content = fs.readFileSync(path, 'utf8');
    content.split('\n').forEach((line) => {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) return;
      const sepIndex = trimmed.indexOf('=');
      if (sepIndex === -1) return;
      const key = trimmed.slice(0, sepIndex).trim();
      const value = trimmed.slice(sepIndex + 1).trim();
      if (!process.env[key]) {
        process.env[key] = value;
      }
    });
  } catch (err) {
    if (err.code !== 'ENOENT') throw err;
    // .env file not found — skip
  }
}
```

### Command-Line Arguments

```javascript
// process.argv: [nodePath, scriptPath, ...args]
// Running: node app.js --name Alice --verbose

console.log(process.argv);
// ['/usr/local/bin/node', '/app/app.js', '--name', 'Alice', '--verbose']

// Simple argument parser
function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {};
  const positional = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        parsed[key] = args[++i];
      } else {
        parsed[key] = true;
      }
    } else if (args[i].startsWith('-') && args[i].length === 2) {
      const key = args[i].slice(1);
      if (i + 1 < args.length && !args[i + 1].startsWith('-')) {
        parsed[key] = args[++i];
      } else {
        parsed[key] = true;
      }
    } else {
      positional.push(args[i]);
    }
  }

  return { ...parsed, _: positional };
}

const args = parseArgs();
console.log(args.name);    // 'Alice'
console.log(args.verbose); // true
console.log(args._);       // positional args
```

### Process Lifecycle Events

```javascript
// Graceful shutdown
async function shutdown(signal) {
  console.log(`Received ${signal}. Shutting down gracefully...`);

  // Close database connections
  await db.close();

  // Stop HTTP server
  await new Promise((resolve) => server.close(resolve));

  // Clean up resources
  await cleanup();

  console.log('Shutdown complete');
  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// Graceful shutdown with timeout
const shutdownTimeout = setTimeout(() => {
  console.error('Forced shutdown after timeout');
  process.exit(1);
}, 30000);
shutdownTimeout.unref(); // Don't prevent process exit

// Handle uncaught exceptions
process.on('uncaughtException', (error, origin) => {
  console.error('Uncaught Exception:', error);
  // Perform minimal cleanup
  // Then exit — process is in unstable state
  process.exit(1);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // In Node.js 15+, unhandled rejections crash the process
});

// beforeExit — runs when event loop is empty
process.on('beforeExit', (code) => {
  console.log('Event loop is empty, about to exit');
  // Can schedule more work (e.g., flush logs)
});

// exit — synchronous, no async work possible
process.on('exit', (code) => {
  console.log(`Process exiting with code ${code}`);
  // Only synchronous operations here
  fs.writeFileSync('exit.log', `Exited at ${Date.now()}`); // OK
  // fs.writeFile() would never execute (async)
});
```

### System Information

```javascript
// Platform
console.log(process.platform);  // 'darwin', 'linux', 'win32'
console.log(process.arch);      // 'x64', 'arm64', 'arm'

// Node.js version
console.log(process.version);       // 'v20.11.0'
console.log(process.versions);      // { node: '20.11.0', v8: '11.8.172', ... }

// Process information
console.log(process.pid);           // Process ID
console.log(process.ppid);          // Parent process ID
console.log(process.title);         // Process title (can be set)
console.log(process.cwd());         // Current working directory
console.log(process.uptime());      // Seconds since process started

// CPU usage
const startUsage = process.cpuUsage();
// ... do work ...
const endUsage = process.cpuUsage(startUsage);
console.log('CPU used:', endUsage.user + endUsage.system, 'microseconds');

// Memory usage
const mem = process.memoryUsage();
console.log({
  rss: `${(mem.rss / 1024 / 1024).toFixed(1)} MB`,         // Resident Set Size
  heapTotal: `${(mem.heapTotal / 1024 / 1024).toFixed(1)} MB`, // Total heap
  heapUsed: `${(mem.heapUsed / 1024 / 1024).toFixed(1)} MB`,  // Used heap
  external: `${(mem.external / 1024 / 1024).toFixed(1)} MB`,  // C++ objects
  arrayBuffers: `${(mem.arrayBuffers / 1024 / 1024).toFixed(1)} MB`, // ArrayBuffers
});

// Resource usage (high-resolution)
const resourceUsage = process.resourceUsage();
console.log({
  maxRSS: resourceUsage.maxRSS,
  fileReads: resourceUsage.fsRead,
  fileWrites: resourceUsage.fsWrite,
  ipcMessages: resourceUsage.ipcMessages,
  contextSwitches: resourceUsage.voluntaryContextSwitches,
});
```

### Standard I/O

```javascript
// Writing to stdout
process.stdout.write('Hello, World!\n');
console.log('Hello, World!'); // Same as process.stdout.write + \n

// Writing to stderr
process.stderr.write('Error: Something went wrong\n');
console.error('Error: Something went wrong'); // Same as process.stderr.write + \n

// Reading from stdin (line by line)
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('What is your name? ', (name) => {
  console.log(`Hello, ${name}!`);
  rl.close();
});

// Streaming stdin
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => {
  console.log('Received:', chunk.trim());
});

// Piping stdin to stdout (echo)
process.stdin.pipe(process.stdout);
```

### Process Control

```javascript
// Exit with specific code
process.exit(0);   // Success
process.exit(1);   // General error
process.exit(2);   // Misuse of shell builtins

// Change working directory
process.chdir('/tmp');
console.log(process.cwd()); // '/tmp'

// Set process title
process.title = 'my-node-app';

// High-resolution time
const start = process.hrtime.bigint();
// ... do work ...
const end = process.hrtime.bigint();
console.log(`Duration: ${(end - start) / 1000000n} ms`);

// Next tick (microtask)
process.nextTick(() => {
  console.log('This runs before any I/O');
});

// Abort controller
const ac = new AbortController();
process.on('SIGINT', () => ac.abort());
```

### Process Configuration

```javascript
// File descriptor limits
console.log(process.getuid());        // User ID
console.log(process.getgid());        // Group ID
console.log(process.geteuid());       // Effective user ID

// umask (file creation mask)
console.log(process.umask().toString(8)); // e.g., '22'
// process.umask(0o022); // Set umask

// Process group
console.log(process.getgroups());     // Supplementary group IDs

// Set process name (ps command)
process.title = 'my-app';
```

## Real-World Use Cases

### 1. Configuration Manager

```javascript
class Config {
  constructor() {
    this.env = process.env.NODE_ENV || 'development';
    this.port = parseInt(process.env.PORT, 10) || 3000;
    this.database = {
      url: process.env.DATABASE_URL || 'postgres://localhost:5432/app',
      pool: parseInt(process.env.DB_POOL, 10) || 10,
    };
    this.redis = {
      url: process.env.REDIS_URL || 'redis://localhost:6379',
    };
    this.logging = {
      level: process.env.LOG_LEVEL || (this.isProduction ? 'info' : 'debug'),
    };
  }

  get isProduction() {
    return this.env === 'production';
  }

  get isDevelopment() {
    return this.env === 'development';
  }

  get isTest() {
    return this.env === 'test';
  }
}

const config = new Config();
```

### 2. Health Check Endpoint

```javascript
const http = require('http');
const startTime = Date.now();

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    const mem = process.memoryUsage();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'healthy',
      uptime: process.uptime(),
      uptimeHuman: formatUptime(process.uptime()),
      pid: process.pid,
      memory: {
        rss: mem.rss,
        heapUsed: mem.heapUsed,
        heapTotal: mem.heapTotal,
      },
      cpuUsage: process.cpuUsage(),
      version: process.version,
      platform: process.platform,
      arch: process.arch,
      nodeEnv: process.env.NODE_ENV,
      startTime,
    }));
  }
});

function formatUptime(seconds) {
  const d = Math.floor(seconds / 86400);
  const h = Math.floor((seconds % 86400) / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${d}d ${h}h ${m}m ${s}s`;
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mutating `process.env` expecting it to persist | Changes only affect current process and children |
| Using `process.exit()` without cleanup | Handle cleanup in SIGTERM/SIGINT handlers |
| Not handling `uncaughtException` at all | At minimum log the error before exiting |
| Blocking in `process.on('exit')` callback | Only sync operations allowed; `exit` halts event loop |
| Assuming `process.argv[0]` is always node | Use `process.argv0` for the original node binary name |

## Best Practices

1. **Use environment variables** for configuration, not code changes
2. **Implement graceful shutdown** — handle SIGTERM for containerized deployments
3. **Set NODE_ENV** — always set `NODE_ENV=production` in production
4. **Validate config on startup** — fail fast if required env vars are missing
5. **Monitor memory usage** — track `process.memoryUsage()` for leak detection
6. **Use `process.nextTick()` sparingly** — prefer `queueMicrotask()` or `Promise.resolve()`
7. **Log process info on startup** — log pid, platform, version for debugging

## Summary

The `process` object is a powerful global API for controlling and introspecting Node.js processes. It provides environment configuration, CLI argument parsing, lifecycle management, system information, and graceful shutdown capabilities. Understanding `process` is essential for building production-ready Node.js applications.

## Cheat Sheet

```text
PROCESS CHEAT SHEET
═══════════════════════════════════════

ENVIRONMENT:
  process.env.NODE_ENV          // 'development' | 'production' | 'test'
  process.argv                  // CLI arguments array
  process.argv0                 // Original node binary name

SYSTEM:
  process.pid                   // Process ID
  process.ppid                  // Parent PID
  process.platform              // 'darwin' | 'linux' | 'win32'
  process.arch                  // 'x64' | 'arm64'
  process.version               // Node.js version
  process.cwd()                 // Current working directory
  process.uptime()              // Seconds since start
  process.memoryUsage()         // { rss, heapTotal, heapUsed, ... }
  process.cpuUsage()            // { user, system } microseconds

LIFECYCLE:
  process.exit(code)            // Exit with code
  process.on('SIGTERM', cb)     // Graceful shutdown
  process.on('SIGINT', cb)      // Ctrl+C
  process.on('uncaughtException', cb)
  process.on('unhandledRejection', cb)
  process.on('beforeExit', cb)
  process.on('exit', cb)

I/O:
  process.stdin                 // Readable stream
  process.stdout                // Writable stream
  process.stderr                // Writable stream

CONTROL:
  process.nextTick(fn)          // Schedule microtask
  process.chdir(path)           // Change directory
  process.title                 // Process name
  process.hrtime.bigint()       // High-res time
```

---

### See Also

- [Event Loop](../01-Event-Loop.md) — process event loop phases
- [Child Processes & Workers](../08-Child-Processes-Workers.md) — spawning subprocesses
- [File System](../06-File-System.md) — file I/O in Node.js
- [Clustering](../04-Clustering.md) — multi-process serving

### References

- [Node.js Process Documentation](https://nodejs.org/api/process.html)
- [Node.js CLI Documentation](https://nodejs.org/api/cli.html)
- [Node.js: Environment Variables](https://nodejs.org/en/learn/command-line/how-to-read-environment-variables-from-nodejs)
- [12-Factor App: Config](https://12factor.net/config)
