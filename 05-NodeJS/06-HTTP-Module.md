[![Category: Backend](https://img.shields.io/badge/category-Backend-2ea44f)](.)

# HTTP Module

The Node.js `http` module enables creating HTTP servers and making HTTP client requests. It's the foundation for web frameworks like Express, NestJS, and Fastify, and provides low-level control over the HTTP protocol.

## Definition

The `http` module is a built-in Node.js module that implements the HTTP protocol. It provides:

- **`http.createServer()`** — creates an HTTP server
- **`http.request()`** / **`http.get()`** — makes HTTP client requests
- **`http.Server`** class — represents the server instance
- **`http.IncomingMessage`** — the request object (readable stream)
- **`http.ServerResponse`** — the response object (writable stream)
- **`http.Agent`** — connection pooling and socket management

Node.js also has `https` module (same API with TLS) and `http2` module for HTTP/2.

## Why Do We Need It?

1. **Foundation**: Every Node.js web framework is built on the `http` module

2. **Fine-grained control**: Direct access to raw request/response streams

3. **Custom protocols**: Build specialized servers (WebSocket upgrade, proxy)

4. **Performance**: Bypass framework overhead for high-throughput endpoints

5. **Understanding**: Knowing HTTP internals helps debug framework-level issues

6. **Proxies & middleware**: Build reverse proxies, load balancers, API gateways

## How It Works

### Request-Response Cycle

```text
┌─────────────────────────────────────────────────────────────┐
│                  HTTP REQUEST-RESPONSE CYCLE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client → TCP Connection → Node.js HTTP Parser              │
│                                                              │
│  HTTP Parser parses headers → creates IncomingMessage        │
│                                                              │
│  Server emits 'request' event with (req, res)                │
│                                                              │
│  Handler processes request → writes to ServerResponse        │
│                                                              │
│  res.end() → HTTP Parser serializes → TCP → Client          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### HTTP Server Lifecycle

```text
createServer → listen → connection → request → response → close
```

## Code Examples (Node.js)

### Basic HTTP Server

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello, World!\n');
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
```

### Advanced Server with Routing

```javascript
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const { pathname, query } = parsedUrl;
  const method = req.method.toUpperCase();

  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Router
  try {
    if (pathname === '/api/users' && method === 'GET') {
      handleGetUsers(req, res, query);
    } else if (pathname === '/api/users' && method === 'POST') {
      handleCreateUser(req, res);
    } else if (pathname.match(/^\/api\/users\/(\d+)$/) && method === 'GET') {
      const userId = pathname.match(/^\/api\/users\/(\d+)$/)[1];
      handleGetUser(req, res, userId);
    } else {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not Found' }));
    }
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Internal Server Error' }));
  }
});

// Request body parsing helper
function parseBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => {
      const body = Buffer.concat(chunks).toString();
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        reject(new Error('Invalid JSON'));
      }
    });
    req.on('error', reject);
  });
}

async function handleGetUsers(req, res, query) {
  const users = [
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' },
  ];
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(users));
}

async function handleCreateUser(req, res) {
  try {
    const body = await parseBody(req);
    const user = { id: Date.now(), ...body };
    res.writeHead(201, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(user));
  } catch (err) {
    res.writeHead(400, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: err.message }));
  }
}

async function handleGetUser(req, res, id) {
  const user = { id: parseInt(id), name: `User ${id}` };
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(user));
}

server.listen(3000);
```

### Streaming Responses

```javascript
const http = require('http');
const fs = require('fs');
const { Transform } = require('stream');

const server = http.createServer((req, res) => {
  if (req.url === '/stream') {
    res.writeHead(200, {
      'Content-Type': 'text/plain',
      'Transfer-Encoding': 'chunked',
    });

    // Stream data as it becomes available
    let count = 0;
    const interval = setInterval(() => {
      res.write(`Chunk ${++count}\n`);
      if (count >= 10) {
        clearInterval(interval);
        res.end('Done\n');
      }
    }, 100);
  } else if (req.url === '/download') {
    // Stream a file
    const readStream = fs.createReadStream('large-file.zip');
    res.writeHead(200, {
      'Content-Type': 'application/octet-stream',
      'Content-Disposition': 'attachment; filename="file.zip"',
    });
    readStream.pipe(res);
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});
```

### Making HTTP Client Requests

```javascript
const http = require('http');
const https = require('https');

// GET request
http.get('http://api.example.com/users', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log(JSON.parse(data));
  });
}).on('error', (err) => {
  console.error('Request failed:', err.message);
});

// POST request with http.request()
const postData = JSON.stringify({ name: 'Alice', email: 'alice@example.com' });

const req = http.request(
  {
    hostname: 'api.example.com',
    port: 80,
    path: '/users',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
    },
  },
  (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => console.log('Response:', body));
  }
);

req.on('error', (err) => console.error('Error:', err));
req.write(postData);
req.end();

// Promise-based wrapper
function fetch(url, options = {}) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    const parsedUrl = new URL(url);

    const req = mod.request(
      {
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (url.startsWith('https') ? 443 : 80),
        path: parsedUrl.pathname + parsedUrl.search,
        method: options.method || 'GET',
        headers: options.headers || {},
      },
      (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: options.json ? JSON.parse(body) : body,
          });
        });
      }
    );

    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}
```

### HTTP Server with Timeout and Graceful Shutdown

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  // Per-request timeout
  req.setTimeout(30000, () => {
    res.writeHead(408);
    res.end('Request Timeout');
  });

  // Response timeout
  res.setTimeout(30000, () => {
    res.writeHead(503);
    res.end('Response Timeout');
  });

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('OK');
});

// Server timeout
server.timeout = 60000;
server.keepAliveTimeout = 5000;
server.headersTimeout = 40000;

server.listen(3000, () => {
  console.log('Server running');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down gracefully...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });

  // Force shutdown after 10s
  setTimeout(() => {
    console.error('Forced shutdown');
    process.exit(1);
  }, 10000);
});
```

### Connection Pooling with http.Agent

```javascript
const http = require('http');

// Custom agent with connection pooling
const agent = new http.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10,
  timeout: 60000,
  scheduling: 'lifo', // or 'fifo'
});

async function makeRequests() {
  const requests = Array.from({ length: 100 }, (_, i) => {
    return new Promise((resolve, reject) => {
      const req = http.request(
        {
          hostname: 'api.example.com',
          path: `/items/${i}`,
          agent, // Reuses connections
        },
        (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => resolve(data));
        }
      );
      req.on('error', reject);
      req.end();
    });
  });

  const results = await Promise.all(requests);
  console.log(`Completed ${results.length} requests`);
}
```

## Real-World Use Cases

### 1. Reverse Proxy

```javascript
const http = require('http');
const httpProxy = http.createServer((clientReq, clientRes) => {
  const options = {
    hostname: 'localhost',
    port: 3001,
    path: clientReq.url,
    method: clientReq.method,
    headers: clientReq.headers,
  };

  const proxyReq = http.request(options, (proxyRes) => {
    clientRes.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(clientRes);
  });

  proxyReq.on('error', (err) => {
    clientRes.writeHead(502);
    clientRes.end('Bad Gateway');
  });

  clientReq.pipe(proxyReq);
});
```

### 2. Health Check Endpoint

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'healthy',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
    }));
  }
});
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not calling `res.end()` | Always call `res.end()` to complete the response |
| Blocking the event loop in request handler | Use async/await; offload CPU work to worker threads |
| Not handling `req.on('error')` | Always add error listeners to request and response streams |
| Forgetting to parse request body | Body arrives as chunks; must be manually concatenated |
| Not setting `Content-Length` or using chunked | Send the right Content-Length or use Transfer-Encoding: chunked |

## Best Practices

1. **Always handle errors** — add error listeners on req, res, and server
2. **Use response timeouts** — prevent hanging connections
3. **Implement graceful shutdown** — close server on SIGTERM/SIGINT
4. **Use connection pooling** — `keepAlive: true` for client requests
5. **Validate input** — sanitize URLs, headers, and body data
6. **Stream large responses** — don't buffer entire responses in memory
7. **Set appropriate timeouts** — request timeout, keep-alive timeout, headers timeout

## Performance Considerations

- **Keep-Alive connections** reduce TCP handshake overhead
- **Connection pooling** limits concurrent connections and reuses sockets
- **Streaming** avoids buffering large payloads in memory
- **Cluster mode** utilizes multiple CPU cores for HTTP serving
- **HTTP/2** enables multiplexing (multiple requests over one connection)

## Summary

The `http` module is the foundation of Node.js web development. It provides low-level server and client capabilities with streaming, connection pooling, and fine-grained control over the HTTP protocol. Understanding its internals is essential for debugging, performance tuning, and building custom web infrastructure.

## Cheat Sheet

```text
HTTP MODULE CHEAT SHEET
═══════════════════════════════════════

SERVER:
  http.createServer((req, res) => { ... })
  server.listen(port, host, callback)
  server.close(callback)

REQUEST (IncomingMessage):
  req.method, req.url, req.headers
  req.socket.remoteAddress
  req.on('data'), req.on('end')

RESPONSE (ServerResponse):
  res.writeHead(statusCode, headers)
  res.setHeader(name, value)
  res.write(data)
  res.end(data)

CLIENT:
  http.get(url, callback)
  http.request(options, callback)
  http.Agent({ keepAlive, maxSockets })

HTTPS:
  https.createServer(options, handler)
  https.request(options, callback)

TIMEOUTS:
  server.timeout
  server.keepAliveTimeout
  server.headersTimeout
  req.setTimeout(ms)
  res.setTimeout(ms)
```

---

### See Also

- [Express / NestJS](../06-NestJS/) — higher-level frameworks
- [Event Loop](01-Event-Loop.md) — how HTTP is processed
- [Streams](02-Streams.md) — streaming request/response
- [WebSockets](../21-WebSockets/) — upgrade from HTTP
- [REST APIs](../07-REST-API/) — API design principles

## References & Learn More

- [Node.js http Documentation](https://nodejs.org/api/http.html)
- [Node.js https Documentation](https://nodejs.org/api/https.html)
- [Node.js http2 Documentation](https://nodejs.org/api/http2.html)
- [Node.js: Anatomy of an HTTP Transaction](https://nodejs.org/en/learn/modules/anatomy-of-an-http-transaction)
