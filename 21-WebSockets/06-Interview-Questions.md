# WebSockets & Real-Time Interview Questions

## Definition

This chapter contains the **30 most frequently asked interview questions** about WebSockets, real-time communication, and related technologies. Each question includes a detailed answer, code examples, and follow-up points to help you ace your next interview.

## Why Do We Need It?

Interview questions test your understanding of:

- **Protocol knowledge**: How WebSockets work at a low level
- **Architecture decisions**: When to use what technology
- **Scaling strategies**: How to handle millions of connections
- **Problem solving**: Real-world scenarios and trade-offs

## How It Works

### Question Categories

```text
Beginner (1-10):     Fundamentals, basic concepts
Intermediate (11-20): Architecture, implementation details
Senior (21-30):      System design, scaling, trade-offs

```

## Code Examples & Detailed Answers

### Beginner Questions (1-10)

---

**Q1: What are WebSockets and how do they differ from HTTP?**

**Answer:**

WebSockets provide **full-duplex, bidirectional communication** over a single TCP connection, while HTTP follows a request-response model.

| Feature | HTTP | WebSockets |
|---|---|---|
| Communication | Unidirectional (request-response) | Bidirectional (full-duplex) |
| Connection | New connection per request | Single persistent connection |
| Overhead | High (headers with every request) | Low (~2-14 bytes per frame) |
| Latency | High (100-500ms) | Low (1-10ms) |
| Server Push | Not native (needs SSE/polling) | Native support |

**Code Example:**

```typescript
// HTTP: Client must initiate every request
const response = await fetch('/api/data');
const data = await response.json();

// WebSocket: Both client and server can send messages anytime
const ws = new WebSocket('wss://example.com');
ws.onmessage = (event) => console.log('Received:', event.data);
ws.send('Hello Server'); // Client can send anytime

```

**Follow-up:** When would you choose SSE over WebSockets?

---

**Q2: Explain the WebSocket handshake process.**

**Answer:**

The WebSocket connection starts with an HTTP upgrade request:

1. **Client sends HTTP request** with `Upgrade: websocket` header

2. **Server responds with 101 Switching Protocols**

3. **TCP connection established**, full-duplex communication begins

**Code Example:**

```text
Client Request:
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

Server Response:
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

```

**Follow-up:** What is the purpose of `Sec-WebSocket-Key`?

---

**Q3: What is Socket.io and how does it differ from raw WebSockets?**

**Answer:**

Socket.io is a **real-time library** built on top of WebSockets that provides:

- Automatic fallback to HTTP long-polling
- Built-in reconnection
- Rooms and namespaces
- Acknowledgments
- Binary support

**Code Example:**

```typescript
// Raw WebSocket: Manual fallback and reconnection
const ws = new WebSocket(url);
ws.onclose = () => {
  // Manual reconnection logic
  setTimeout(() => reconnect(), 1000);
};

// Socket.io: Automatic handling
const socket = io(url);
socket.on('disconnect', () => {
  // Automatic reconnection with backoff
});

```

**Follow-up:** When would you use raw WebSockets over Socket.io?

---

**Q4: What are Server-Sent Events (SSE) and when should you use them?**

**Answer:**

SSE is a **standard for server-to-client streaming** over HTTP. Use SSE when:

- You only need server-to-client communication
- You want automatic reconnection
- You need to work through proxies/firewalls
- You want simpler implementation

**Code Example:**

```typescript
// Server (Express)
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const sendEvent = (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  setInterval(() => sendEvent({ time: Date.now() }), 1000);
});

// Client
const eventSource = new EventSource('/events');
eventSource.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data));
};

```

**Follow-up:** How does SSE handle reconnection?

---

**Q5: What is the difference between WebSockets and HTTP Long Polling?**

**Answer:**

| Feature | HTTP Long Polling | WebSockets |
|---|---|---|
| Connection | Repeated HTTP requests | Single persistent connection |
| Latency | 50-200ms | 1-10ms |
| Server Load | High (new connections) | Low (persistent) |
| Bandwidth | High (headers) | Low (minimal frames) |
| Bidirectional | No (client initiates) | Yes (full-duplex) |

**Code Example:**

```typescript
// Long Polling: Client repeatedly requests
async function longPoll() {
  const response = await fetch('/poll');
  const data = await response.json();
  process(data);
  longPoll(); // Immediately request again
}

// WebSocket: Server pushes when available
const ws = new WebSocket(url);
ws.onmessage = (event) => process(JSON.parse(event.data));

```

**Follow-up:** What are the scaling challenges with long polling?

---

**Q6: How do you handle WebSocket reconnection?**

**Answer:**

Implement **exponential backoff** with jitter to prevent thundering herd:

**Code Example:**

```typescript
class ReconnectingWebSocket {
  private reconnectAttempts = 0;
  private maxAttempts = 10;
  private baseDelay = 1000;

  connect(url: string): void {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      this.reconnectAttempts = 0; // Reset on success
    };

    this.ws.onclose = (event) => {
      if (!event.wasClean) {
        this.attemptReconnect(url);
      }
    };
  }

  private attemptReconnect(url: string): void {
    if (this.reconnectAttempts >= this.maxAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    const delay = this.baseDelay * Math.pow(2, this.reconnectAttempts);
    const jitter = delay * 0.1 * Math.random();

    setTimeout(() => {
      this.reconnectAttempts++;
      this.connect(url);
    }, delay + jitter);
  }
}

```

**Follow-up:** How do you handle missed messages during reconnection?

---

**Q7: What are WebSocket rooms and how do they work?**

**Answer:**

Rooms are **logical channels** that clients can join/leave, enabling scoped broadcasting.

**Code Example:**

```typescript
// Server (Socket.io)
io.on('connection', (socket) => {
  socket.on('join-room', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('user-joined', socket.id);
  });

  socket.on('message', ({ roomId, text }) => {
    io.to(roomId).emit('new-message', {
      userId: socket.id,
      text,
    });
  });

  socket.on('leave-room', (roomId) => {
    socket.leave(roomId);
  });
});

// Client
socket.emit('join-room', 'general');
socket.emit('message', { roomId: 'general', text: 'Hello!' });

```

**Follow-up:** How do you track room membership at scale?

---

**Q8: What are WebSocket namespaces?**

**Answer:**

Namespaces allow **logical separation** of concerns on a single connection. Each namespace can have its own event handlers and middleware.

**Code Example:**

```typescript
// Server
const chatNamespace = io.of('/chat');
const adminNamespace = io.of('/admin');

chatNamespace.on('connection', (socket) => {
  socket.on('message', (data) => {
    chatNamespace.emit('new-message', data);
  });
});

adminNamespace.use((socket, next) => {
  if (isAdmin(socket.handshake.auth.token)) {
    next();
  } else {
    next(new Error('Unauthorized'));
  }
});

// Client
const chatSocket = io('/chat');
const adminSocket = io('/admin');

```

**Follow-up:** When would you use namespaces vs rooms?

---

**Q9: How do you secure WebSocket connections?**

**Answer:**

Security measures include:

1. **Authentication**: Verify identity on connection

2. **Authorization**: Check permissions for actions

3. **Encryption**: Use WSS (WebSocket Secure)

4. **Validation**: Validate all incoming data

5. **Rate Limiting**: Prevent abuse

**Code Example:**

```typescript
// Server authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = jwt.verify(token, SECRET);
    socket.data.user = user;
    next();
  } catch (err) {
    next(new Error('Authentication error'));
  }
});

// Rate limiting
const rateLimiter = new Map();

io.use((socket, next) => {
  const now = Date.now();
  const record = rateLimiter.get(socket.handshake.address) || { count: 0, resetAt: now + 60000 };

  if (now > record.resetAt) {
    record.count = 0;
    record.resetAt = now + 60000;
  }

  if (record.count >= 100) {
    return next(new Error('Rate limit exceeded'));
  }

  record.count++;
  rateLimiter.set(socket.handshake.address, record);
  next();
});

```

**Follow-up:** How do you prevent cross-site WebSocket hijacking?

---

**Q10: What is the WebSocket frame structure?**

**Answer:**

WebSocket frames have a specific binary format:

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+

|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |

+-+-+-+-+-------+-+-------------+-------------------------------+

|     Extended payload length continued, if payload len == 127  |

+-------------------------------+-------------------------------+

|                               |Masking-key, if MASK set to 1  |

+-------------------------------+-------------------------------+

| Masking-key (continued)       |          Payload Data         |

+-------------------------------+-------------------------------+

|                     Payload Data continued ...                |

+---------------------------------------------------------------+

```

Key fields:

- **FIN**: Indicates final fragment
- **Opcode**: Message type (text, binary, ping, pong, close)
- **MASK**: Whether payload is masked (client-to-server must be masked)
- **Payload length**: Length of message data

**Follow-up:** Why must client-to-server messages be masked?

---

### Intermediate Questions (11-20)

---

**Q11: How do you scale WebSockets across multiple servers?**

**Answer:**

Use **Redis Pub/Sub** for cross-server communication:

**Code Example:**

```typescript
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

io.adapter(createAdapter(pubClient, subClient));

// Now all servers share the same pub/sub
io.to('room-1').emit('message', 'Hello'); // Delivered across all servers

```

Architecture:

```text
Server 1 <---> Redis Pub/Sub <---> Server 2

   |                                   |

   v                                   v
Client 1                          Client 2

All servers receive messages published to Redis

```

**Follow-up:** What are the limitations of Redis Pub/Sub at scale?

---

**Q12: How do you handle message ordering in distributed WebSockets?**

**Answer:**

Use **sequence numbers** or **vector clocks**:

**Code Example:**

```typescript
interface OrderedMessage {
  sequence: number;
  vectorClock: Record<string, number>;
  data: unknown;
  timestamp: number;
}

class MessageSequencer {
  private sequence = 0;
  private vectorClock: Record<string, number> = {};

  createMessage(data: unknown, nodeId: string): OrderedMessage {
    this.sequence++;
    this.vectorClock[nodeId] = (this.vectorClock[nodeId] || 0) + 1;

    return {
      sequence: this.sequence,
      vectorClock: { ...this.vectorClock },
      data,
      timestamp: Date.now(),
    };
  }

  // For causal ordering
  isInOrder(msg1: OrderedMessage, msg2: OrderedMessage): boolean {
    // Check if msg1 happens-before msg2
    for (const [node, time] of Object.entries(msg1.vectorClock)) {
      if (time > (msg2.vectorClock[node] || 0)) {
        return false;
      }
    }
    return true;
  }
}

```

**Follow-up:** When would you use CRDTs instead of sequence numbers?

---

**Q13: What is backpressure and how do you handle it?**

**Answer:**

Backpressure occurs when the **producer generates data faster than the consumer can process it**.

**Code Example:**

```typescript
class BackpressureHandler {
  private buffer: unknown[] = [];
  private maxBufferSize = 1000;
  private isProcessing = false;

  addMessage(message: unknown): boolean {
    if (this.buffer.length >= this.maxBufferSize) {
      // Option 1: Drop message
      console.warn('Buffer full, dropping message');
      return false;

      // Option 2: Block producer
      // await this.waitForSpace();

      // Option 3: Evict oldest
      // this.buffer.shift();
    }

    this.buffer.push(message);
    this.processBuffer();
    return true;
  }

  private async processBuffer(): Promise<void> {
    if (this.isProcessing) return;
    this.isProcessing = true;

    while (this.buffer.length > 0) {
      const message = this.buffer.shift()!;
      await this.processMessage(message);
    }

    this.isProcessing = false;
  }
}

// Monitor buffer health
ws.on('bufferedAmountChange', () => {
  if (ws.bufferedAmount > 1024 * 1024) { // 1MB
    console.warn('High buffer usage:', ws.bufferedAmount);
  }
});

```

**Follow-up:** What are the trade-offs between dropping vs buffering messages?

---

**Q14: How do you implement real-time notifications?**

**Answer:**

Use **user-specific rooms** with Redis for scaling:

**Code Example:**

```typescript
// Server
io.on('connection', (socket) => {
  const userId = socket.handshake.auth.userId;
  socket.join(`user:${userId}`);

  socket.on('subscribe', (topics) => {
    topics.forEach((topic) => socket.join(`topic:${topic}`));
  });
});

// Send notification to specific user
function sendNotification(userId: string, notification: Notification): void {
  io.to(`user:${userId}`).emit('notification', notification);
}

// Broadcast to topic subscribers
function broadcastToTopic(topic: string, data: unknown): void {
  io.to(`topic:${topic}`).emit('topic-update', data);
}

// With Redis for scaling
import { createAdapter } from '@socket.io/redis-adapter';
io.adapter(createAdapter(pubClient, subClient));

```

**Follow-up:** How do you handle offline users?

---

**Q15: How do you test WebSocket applications?**

**Answer:**

Test at multiple levels:

**Code Example:**

```typescript
import { Server } from 'socket.io';
import { io as Client } from 'socket.io-client';
import { createServer } from 'http';

describe('WebSocket Server', () => {
  let httpServer;
  let io;
  let clientSocket;

  beforeAll((done) => {
    httpServer = createServer();
    io = new Server(httpServer);
    httpServer.listen(() => {
      const port = (httpServer.address() as any).port;
      clientSocket = Client(`http://localhost:${port}`);
      clientSocket.on('connect', done);
    });
  });

  afterAll(() => {
    io.close();
    clientSocket.close();
    httpServer.close();
  });

  test('should receive message', (done) => {
    clientSocket.on('message', (data) => {
      expect(data).toBe('Hello');
      done();
    });

    clientSocket.emit('send-message', 'Hello');
  });

  test('should join room', (done) => {
    clientSocket.emit('join-room', 'test-room');
    setTimeout(() => {
      expect(clientSocket.rooms.has('test-room')).toBe(true);
      done();
    }, 100);
  });
});

// Load testing with Artillery
// artillery.yml
// config:
//   target: "ws://localhost:3000"
//   phases:
//     - duration: 60
//       arrivalRate: 50
//   defaults:
//     ws:
//       subprotocols: ["graphql-ws"]
//   scenarios:
//     - engine: "socketio"
//       flow:
//         - emit: { channel: "message", data: "Hello" }

```

**Follow-up:** How do you test reconnection behavior?

---

**Q16: How do you handle WebSocket authentication?**

**Answer:**

Authenticate on connection using JWT:

**Code Example:**

```typescript
// Server
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) {
    return next(new Error('Authentication required'));
  }

  try {
    const user = jwt.verify(token, process.env.JWT_SECRET);
    socket.data.user = user;
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

// Client
const socket = io('http://localhost:3000', {
  auth: {
    token: localStorage.getItem('token'),
  },
});

// Token refresh
socket.on('token-expired', async () => {
  const newToken = await refreshToken();
  socket.auth.token = newToken;
  socket.connect();
});

```

**Follow-up:** How do you handle token expiration during long connections?

---

**Q17: What is the difference between polling, long polling, SSE, and WebSockets?**

**Answer:**

| Technology | Direction | Connection | Latency | Use Case |
|---|---|---|---|---|
| Polling | Client -> Server | Multiple HTTP | High | Simple updates |
| Long Polling | Client -> Server | Persistent HTTP | Medium | Occasional updates |
| SSE | Server -> Client | Persistent HTTP | Low | Server push only |
| WebSockets | Bidirectional | Persistent TCP | Very Low | Real-time interaction |

**Code Example:**

```typescript
// Polling: Client repeatedly requests
setInterval(async () => {
  const data = await fetch('/api/updates').then(r => r.json());
  process(data);
}, 5000);

// Long Polling: Server holds request
async function longPoll() {
  const data = await fetch('/api/poll').then(r => r.json());
  process(data);
  longPoll(); // Immediately reconnect
}

// SSE: Server pushes via HTTP
const es = new EventSource('/events');
es.onmessage = (e) => process(JSON.parse(e.data));

// WebSockets: Full duplex
const ws = new WebSocket('ws://localhost:3000');
ws.onmessage = (e) => process(JSON.parse(e.data));
ws.send('Hello'); // Can send anytime

```

**Follow-up:** How do you choose between these technologies?

---

**Q18: How do you handle binary data in WebSockets?**

**Answer:**

WebSockets support binary data via ArrayBuffer or Blob:

**Code Example:**

```typescript
// Client: Sending binary
function sendBinary(ws: WebSocket): void {
  // ArrayBuffer
  const buffer = new ArrayBuffer(32);
  const view = new Uint8Array(buffer);
  for (let i = 0; i < 32; i++) view[i] = i;
  ws.send(buffer);

  // Typed Array
  const floatArray = new Float32Array([1.1, 2.2, 3.3]);
  ws.send(floatArray.buffer);

  // Blob
  const blob = new Blob(['Hello Binary'], { type: 'text/plain' });
  ws.send(blob);
}

// Server: Handling binary
wss.on('connection', (ws) => {
  ws.on('message', (data, isBinary) => {
    if (isBinary) {
      const buffer = Buffer.from(data);
      console.log('Binary data:', buffer.length, 'bytes');
    } else {
      const text = data.toString();
      console.log('Text data:', text);
    }
  });
});

// Set binary type
ws.binaryType = 'arraybuffer'; // or 'blob'

```

**Follow-up:** When would you use ArrayBuffer vs Blob?

---

**Q19: How do you implement rate limiting for WebSockets?**

**Answer:**

Use sliding window or token bucket algorithms:

**Code Example:**

```typescript
class SlidingWindowRateLimiter {
  private windows = new Map<string, number[]>();

  isAllowed(clientId: string, limit: number, windowMs: number): boolean {
    const now = Date.now();
    const windowStart = now - windowMs;

    if (!this.windows.has(clientId)) {
      this.windows.set(clientId, []);
    }

    const timestamps = this.windows.get(clientId)!;

    // Remove old timestamps
    while (timestamps.length > 0 && timestamps[0] < windowStart) {
      timestamps.shift();
    }

    if (timestamps.length >= limit) {
      return false;
    }

    timestamps.push(now);
    return true;
  }
}

// Usage in Socket.io
const limiter = new SlidingWindowRateLimiter();

io.use((socket, next) => {
  if (!limiter.isAllowed(socket.id, 100, 60000)) {
    return next(new Error('Rate limit exceeded'));
  }
  next();
});

```

**Follow-up:** How do you handle rate limiting across multiple servers?

---

**Q20: What are WebSocket subprotocols?**

**Answer:**

Subprotocols define **application-level protocols** negotiated during the handshake:

**Code Example:**

```typescript
// Server with subprotocol support
const wss = new WebSocketServer({
  port: 8080,
  handleProtocols: (protocols, req) => {
    if (protocols.includes('graphql-ws')) {
      return 'graphql-ws';
    }
    return false;
  },
});

// Client specifying subprotocol
const ws = new WebSocket('wss://example.com', ['graphql-ws', 'socket.io']);

// Socket.io with custom protocol
const socket = io('http://localhost:3000', {
  protocols: ['graphql-ws'],
});

```

Common subprotocols:

- `graphql-ws`: GraphQL subscriptions
- `graphql-transport-ws`: Apollo Server
- `wamp`: Web Application Messaging Protocol

**Follow-up:** How do you implement GraphQL subscriptions with WebSockets?

---

### Senior Questions (21-30)

---

**Q21: Design a chat system supporting 10 million concurrent users.**

**Answer:**

**Architecture:**

```text
                    +-- Load Balancer --+

                    |                  |

              +-----+-----+      +-----+-----+

              |  WS Server |      |  WS Server |

              +-----+-----+      +-----+-----+

                    |                  |

              +-----+------------------+

              |      Redis Pub/Sub     |

              +-----+------------------+

                    |

              +-----+-----+

              |  Message   |
              |  Queue     |

              +-----+-----+

                    |

              +-----+-----+

              | Cassandra  |

              +-----------+

```

**Code Example:**

```typescript
// Connection management with consistent hashing
class ChatSystem {
  private consistentHash = new ConsistentHash();
  private redis: Redis;
  private kafka: Kafka;

  constructor() {
    // Add servers to consistent hash ring
    this.consistentHash.addNode('server-1');
    this.consistentHash.addNode('server-2');
    this.consistentHash.addNode('server-3');
  }

  routeConnection(userId: string): string {
    return this.consistentHash.getNode(userId);
  }

  async handleMessage(message: ChatMessage): Promise<void> {
    // 1. Validate and save to Kafka for durability
    await this.kafka.produce('chat-messages', message);

    // 2. Publish to Redis for real-time delivery
    await this.redis.publish(
      `room:${message.roomId}`,
      JSON.stringify(message)
    );

    // 3. Update read model asynchronously
    await this.updateReadModel(message);
  }

  private async updateReadModel(message: ChatMessage): Promise<void> {
    // Update Cassandra for persistence
    await this.cassandra.execute(
      'INSERT INTO messages (id, room_id, user_id, content, created_at) VALUES (?, ?, ?, ?, ?)',
      [message.id, message.roomId, message.userId, message.content, message.timestamp]
    );
  }
}

```

**Key considerations:**

- Consistent hashing for connection routing
- Redis Pub/Sub for cross-server messaging
- Kafka for message durability
- Cassandra for message storage
- CDN for media delivery

**Follow-up:** How do you handle message ordering at this scale?

---

**Q22: How do you implement real-time collaboration (Google Docs style)?**

**Answer:**

Use **Operational Transform (OT)** or **CRDTs**:

**Code Example:**

```typescript
// CRDT-based collaboration
class CollaborativeDocument {
  private state: CRDTDocument;
  private clients = new Map<string, Client>();

  applyOperation(clientId: string, operation: Operation): void {
    // Transform against concurrent operations
    const transformed = this.transform(operation, this.pendingOperations);

    // Apply to local state
    this.state.apply(transformed);

    // Broadcast to other clients
    this.broadcast(clientId, transformed);

    // Store in operation log
    this.operationLog.push(transformed);
  }

  private transform(op1: Operation, op2: Operation): Operation {
    // OT transformation logic
    if (op1.type === 'insert' && op2.type === 'insert') {
      if (op1.position <= op2.position) {
        return op2.withPosition(op2.position + op1.text.length);
      }
      return op2;
    }
    // ... more cases
    return op1;
  }

  // Cursor presence
  updateCursor(clientId: string, position: Position): void {
    this.clients.get(clientId)!.cursor = position;
    this.broadcastCursor(clientId, position);
  }
}

```

**Key considerations:**

- OT vs CRDT trade-offs
- Conflict resolution strategies
- Cursor presence and awareness
- Version history and undo
- Offline support and sync

**Follow-up:** What are the trade-offs between OT and CRDTs?

---

**Q23: How do you handle WebSocket connections during deployment?**

**Answer:**

Use **graceful shutdown** with connection draining:

**Code Example:**

```typescript
class GracefulShutdown {
  private isShuttingDown = false;

  constructor(private server: Server) {
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
  }

  async shutdown(): Promise<void> {
    if (this.isShuttingDown) return;
    this.isShuttingDown = true;

    console.log('Starting graceful shutdown...');

    // 1. Stop accepting new connections
    this.server.close(() => {
      console.log('Server closed');
    });

    // 2. Notify clients of impending shutdown
    this.server.emit('server-shutdown', {
      message: 'Server restarting, please reconnect',
      reconnectAfter: 5000,
    });

    // 3. Wait for in-flight messages
    await this.drainConnections(30000); // 30 second timeout

    // 4. Close all connections
    this.server.sockets.sockets.forEach((socket) => {
      socket.disconnect(true);
    });

    process.exit(0);
  }

  private drainConnections(timeout: number): Promise<void> {
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        console.log('Drain timeout reached');
        resolve();
      }, timeout);

      const checkInterval = setInterval(() => {
        if (this.server.engine.clientsCount === 0) {
          clearInterval(checkInterval);
          clearTimeout(timer);
          resolve();
        }
      }, 1000);
    });
  }
}

```

**Follow-up:** How do you handle session migration between servers?

---

**Q24: How do you monitor WebSocket connections in production?**

**Answer:**

Track key metrics with Prometheus/Grafana:

**Code Example:**

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

class WebSocketMetrics {
  private connections = new Gauge({
    name: 'websocket_connections_total',
    help: 'Total WebSocket connections',
    labelNames: ['namespace'],
  });

  private messages = new Counter({
    name: 'websocket_messages_total',
    help: 'Total WebSocket messages',
    labelNames: ['event', 'direction'],
  });

  private latency = new Histogram({
    name: 'websocket_latency_seconds',
    help: 'WebSocket message latency',
    labelNames: ['event'],
    buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1],
  });

  setupMonitoring(io: Server): void {
    io.on('connection', (socket) => {
      this.connections.inc();

      socket.on('disconnect', () => {
        this.connections.dec();
      });

      socket.onAny((event, ...args) => {
        this.messages.inc({ event, direction: 'inbound' });
      });

      const originalEmit = socket.emit.bind(socket);
      socket.emit = (event, ...args) => {
        this.messages.inc({ event, direction: 'outbound' });
        return originalEmit(event, ...args);
      };
    });
  }
}

```

**Key metrics to monitor:**

- Connection count (gauge)
- Message rate (counter)
- Message latency (histogram)
- Error rate (counter)
- Buffer usage (gauge)

**Follow-up:** How do you set up alerting for WebSocket issues?

---

**Q25: How do you handle WebSocket in microservices?**

**Answer:**

Use **API Gateway** pattern with WebSocket routing:

**Code Example:**

```typescript
// API Gateway WebSocket handling
class WebSocketGateway {
  private services = new Map<string, ServiceClient>();

  constructor() {
    this.services.set('chat', new ServiceClient('chat-service'));
    this.services.set('notifications', new ServiceClient('notification-service'));
  }

  handleConnection(socket: Socket): void {
    socket.onAny((event, ...args) => {
      const [service, action] = event.split(':');
      const client = this.services.get(service);

      if (client) {
        client.send(action, args[0], socket.id);
      }
    });
  }
}

// Service client with message broker
class ServiceClient {
  private producer: Producer;

  async send(action: string, data: unknown, clientId: string): Promise<void> {
    await this.producer.send({
      topic: this.serviceName,
      messages: [{
        key: clientId,
        value: JSON.stringify({ action, data, clientId }),
      }],
    });
  }

  async subscribe(handler: (message: Message) => Promise<void>): Promise<void> {
    const consumer = this.kafka.consumer({ groupId: this.serviceName });
    await consumer.subscribe({ topic: this.serviceName });
    await consumer.run({ eachMessage: handler });
  }
}

```

**Key considerations:**

- API Gateway for connection management
- Message broker for cross-service communication
- Service discovery for routing
- Distributed tracing for debugging

**Follow-up:** How do you handle state in stateless microservices?

---

**Q26: How do you implement WebSocket message persistence?**

**Answer:**

Use **event sourcing** with durable storage:

**Code Example:**

```typescript
class PersistentMessageStore {
  private kafka: Kafka;
  private cassandra: Client;

  async persistMessage(message: Message): Promise<void> {
    // 1. Write to Kafka for durability
    await this.kafka.produce('messages', {
      key: message.id,
      value: JSON.stringify(message),
    });

    // 2. Write to Cassandra for queries
    await this.cassandra.execute(
      `INSERT INTO messages (id, room_id, user_id, content, created_at)
       VALUES (?, ?, ?, ?, ?)`,
      [message.id, message.roomId, message.userId, message.content, message.createdAt]
    );
  }

  async getMessages(roomId: string, before?: string, limit = 50): Promise<Message[]> {
    let query = 'SELECT * FROM messages WHERE room_id = ?';
    const params: any[] = [roomId];

    if (before) {
      query += ' AND created_at < ?';
      params.push(before);
    }

    query += ' ORDER BY created_at DESC LIMIT ?';
    params.push(limit);

    const result = await this.cassandra.execute(query, params);
    return result.rows;
  }

  async replayMessages(roomId: string, fromVersion: number): Promise<Message[]> {
    // Replay from event store
    const events = await this.eventStore.getEvents(roomId, fromVersion);
    return events.map(this.eventToMessage);
  }
}

```

**Follow-up:** How do you handle message ordering during replay?

---

**Q27: How do you optimize WebSocket performance?**

**Answer:**

Multiple optimization strategies:

**Code Example:**

```typescript
// 1. Message compression
const wss = new WebSocketServer({
  perMessageDeflate: {
    zlibDeflateOptions: { level: 3 },
    threshold: 1024, // Only compress messages > 1KB
  },
});

// 2. Binary protocol instead of JSON
function encodeMessage(data: unknown): Buffer {
  const packed = msgpack.encode(data);
  return packed;
}

function decodeMessage(buffer: Buffer): unknown {
  return msgpack.decode(buffer);
}

// 3. Message batching
class MessageBatcher {
  private buffer: unknown[] = [];
  private flushInterval = 100; // ms

  add(message: unknown): void {
    this.buffer.push(message);
  }

  startFlushing(ws: WebSocket): void {
    setInterval(() => {
      if (this.buffer.length > 0) {
        ws.send(encodeMessage(this.buffer));
        this.buffer = [];
      }
    }, this.flushInterval);
  }
}

// 4. Connection pooling for server-to-server
class ConnectionPool {
  private connections: WebSocket[] = [];
  private currentIndex = 0;

  getConnection(): WebSocket {
    const conn = this.connections[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % this.connections.length;
    return conn;
  }
}

```

**Follow-up:** How do you measure WebSocket performance?

---

**Q28: How do you handle WebSocket in a serverless environment?**

**Answer:**

Use **WebSocket API** with Lambda or similar:

**Code Example:**

```typescript
// AWS WebSocket API Gateway + Lambda
exports.connectHandler = async (event) => {
  const connectionId = event.requestContext.connectionId;

  // Store connection
  await dynamodb.put({
    TableName: 'Connections',
    Item: {
      connectionId,
      userId: event.queryStringParameters?.userId,
      connectedAt: Date.now(),
    },
  });

  return { statusCode: 200 };
};

exports.messageHandler = async (event) => {
  const connectionId = event.requestContext.connectionId;
  const body = JSON.parse(event.body);

  // Get all connections for the room
  const connections = await dynamodb.query({
    TableName: 'Connections',
    IndexName: 'RoomIndex',
    KeyConditionExpression: 'roomId = :roomId',
    ExpressionAttributeValues: { ':roomId': body.roomId },
  });

  // Send to all connections
  const apiGateway = new ApiGatewayManagementApi({
    endpoint: event.requestContext.domainName + '/' + event.requestContext.stage,
  });

  const promises = connections.Items.map((conn) =>
    apiGateway.postToConnection({
      ConnectionId: conn.connectionId,
      Data: JSON.stringify(body),
    }).promise()
  );

  await Promise.all(promises);

  return { statusCode: 200 };
};

```

**Key considerations:**

- Cold start latency
- Connection state management
- Cost at scale
- Message ordering

**Follow-up:** How do you handle connection state in serverless?

---

**Q29: How do you implement WebSocket with GraphQL subscriptions?**

**Answer:**

Use **graphql-ws** protocol:

**Code Example:**

```typescript
// Server
import { useServer } from 'graphql-ws/lib/use/ws';
import { WebSocketServer } from 'ws';

const wsServer = new WebSocketServer({
  path: '/graphql',
  port: 4000,
});

const serverCleanup = useServer(
  {
    schema,
    context: async (ctx) => {
      const token = ctx.connectionParams?.authorization;
      const user = await verifyToken(token);
      return { user };
    },
  },
  wsServer
);

// Client
import { createClient } from 'graphql-ws';

const client = createClient({
  url: 'ws://localhost:4000/graphql',
  connectionParams: {
    authorization: token,
  },
});

client.subscribe(
  {
    query: `
      subscription OnMessageAdded($roomId: ID!) {
        messageAdded(roomId: $roomId) {
          id
          content
          user {
            name
          }
        }
      }
    `,
    variables: { roomId: '123' },
  },
  {
    next: ({ data }) => {
      console.log('New message:', data.messageAdded);
    },
    error: (err) => console.error(err),
    complete: () => console.log('Subscription complete'),
  }
);

```

**Follow-up:** How do you handle subscription filtering?

---

**Q30: How do you handle WebSocket in a multi-region deployment?**

**Answer:**

Use **geo-routing** with regional WebSocket servers:

**Code Example:**

```typescript
class MultiRegionWebSocket {
  private regions = new Map<string, RegionalServer>();
  private redis: Redis;

  constructor() {
    this.regions.set('us-east', new RegionalServer('us-east'));
    this.regions.set('eu-west', new RegionalServer('eu-west'));
    this.regions.set('ap-south', new RegionalServer('ap-south'));
  }

  async routeClient(client: Socket): Promise<RegionalServer> {
    const clientRegion = await this.detectRegion(client.handshake.address);
    return this.regions.get(clientRegion) || this.regions.get('us-east')!;
  }

  async broadcast(message: unknown): Promise<void> {
    // Publish to all regions
    const promises = Array.from(this.regions.values()).map((region) =>
      region.broadcast(message)
    );
    await Promise.all(promises);
  }

  async sendToUser(userId: string, message: unknown): Promise<void> {
    // Find user's region
    const userRegion = await this.redis.get(`user:${userId}:region`);
    if (userRegion) {
      await this.regions.get(userRegion)?.sendToUser(userId, message);
    }
  }

  private async detectRegion(ip: string): Promise<string> {
    // Use GeoIP or similar
    const geo = await geoip.lookup(ip);
    return this.mapCountryToRegion(geo?.country);
  }
}

// Regional server with Redis replication
class RegionalServer {
  private wss: WebSocketServer;
  private redis: Redis;

  constructor(private region: string) {
    this.redis = new Redis(`redis-${region}.example.com`);
    this.setupPubSub();
  }

  private setupPubSub(): void {
    // Subscribe to cross-region messages
    this.redis.subscribe('global:broadcast');
    this.redis.on('message', (channel, message) => {
      this.localBroadcast(JSON.parse(message));
    });
  }

  async broadcast(message: unknown): Promise<void> {
    // Local broadcast
    this.localBroadcast(message);

    // Publish to other regions
    await this.redis.publish('global:broadcast', JSON.stringify(message));
  }
}

```

**Key considerations:**

- Latency-based routing
- Data residency requirements
- Cross-region replication
- Failover between regions

**Follow-up:** How do you handle data consistency across regions?

---

## Summary

### Key Takeaways

1. **WebSockets** provide full-duplex communication for real-time applications

2. **Socket.io** simplifies WebSockets with automatic fallback and features

3. **SSE** is ideal for server-to-client streaming

4. **Scaling** requires Redis Pub/Sub, message brokers, and consistent hashing

5. **Security** requires authentication, rate limiting, and input validation

6. **Monitoring** is essential for production systems

### Interview Tips

- Start with the basics and build up
- Use concrete examples and code snippets
- Discuss trade-offs and alternatives
- Consider scalability and edge cases
- Mention real-world experiences

### Common Follow-up Questions

1. How would you scale this to X million users?

2. What are the trade-offs of this approach?

3. How would you handle failure scenarios?

4. What monitoring would you implement?

5. How would you test this system?

## References & Learn More

- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Socket.io Documentation](https://socket.io/docs/)
- [NestJS WebSockets](https://docs.nestjs.com/websockets)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [System Design Interview](https://www.amazon.com/System-Design-Interview-insiders-Second/dpB08CMF2PY)
- [Real-World System Design](https://github.com/karanpratapsingh/system-design)
