# WebSockets Overview

## Definition

WebSockets provide a **full-duplex, bidirectional communication protocol** over a single TCP connection. Unlike HTTP's request-response model, WebSockets allow both client and server to send messages independently at any time without the overhead of repeated HTTP handshakes.

A WebSocket connection starts as an HTTP request and then **upgrades** to a persistent TCP connection using the `Upgrade` header, enabling real-time data exchange with minimal latency.

## Why Do We Need It?

| Problem with HTTP | WebSocket Solution |
|---|---|
| Request-response only | Bidirectional communication |
| High latency (new connection per request) | Single persistent connection |
| Headers sent with every request | Minimal frame overhead (~2-14 bytes) |
| No server push capability | Server can push messages anytime |
| Polling wastes bandwidth | Event-driven, push-based |

### HTTP Long Polling vs WebSockets

```
HTTP Long Polling:                    WebSockets:
Client     Server                     Client     Server
  |----req---->|                        |          |
  |     (wait) |                        |   TCP    |
  |<---resp----|                        | Upgrade  |
  |----req---->|                        |==CONNECTED|
  |     (wait) |                        |          |
  |<---resp----|                        | <--msg-- |
  |----req---->|                        | --msg--> |
                                      | --msg--> |
                                      | <--msg-- |
```

## How It Works

### The WebSocket Handshake

The WebSocket protocol begins with an HTTP/1.1 upgrade request:

```
1. Client sends HTTP Upgrade request:
   GET /chat HTTP/1.1
   Host: server.example.com
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
   Sec-WebSocket-Version: 13

2. Server responds with 101 Switching Protocols:
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

3. TCP connection established, full-duplex communication begins
```

### Frame Structure

```
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
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

### Connection Lifecycle

```
+----------+     +----------+     +----------+     +----------+
| CONNECTING| --> |   OPEN   | --> | CLOSING  | --> |  CLOSED  |
+----------+     +----------+     +----------+     +----------+
     |                |                |                |
     |  Handshake     |  Messages      |  Close frame   |  Connection
     |  in progress   |  can flow      |  sent          |  terminated
     |                |  both ways     |                |
```

### State Transitions

```typescript
const ws = new WebSocket('wss://echo.websocket.org');

ws.readyState;
// WebSocket.CONNECTING (0) - Handshake in progress
// WebSocket.OPEN (1)       - Connection established
// WebSocket.CLOSING (2)    - Close handshake initiated
// WebSocket.CLOSED (3)     - Connection fully closed
```

## Code Examples

### Basic WebSocket Client

```typescript
class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(url: string): void {
    this.ws = new WebSocket(url);

    this.ws.onopen = (event) => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.onConnected?.(event);
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.onMessage?.(data);
    };

    this.ws.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} ${event.reason}`);
      this.attemptReconnect(url);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private attemptReconnect(url: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(url), delay);
    }
  }

  send(data: Record<string, unknown>): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close(): void {
    this.ws?.close(1000, 'Client closing');
  }
}
```

### Basic WebSocket Server (Node.js)

```typescript
import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

interface Client {
  id: string;
  ws: WebSocket;
  isAlive: boolean;
}

const clients = new Map<string, Client>();

wss.on('connection', (ws: WebSocket, req) => {
  const clientId = crypto.randomUUID();
  const client: Client = { id: clientId, ws, isAlive: true };
  clients.set(clientId, client);

  console.log(`Client ${clientId} connected. Total: ${clients.size}`);

  ws.on('pong', () => {
    client.isAlive = true;
  });

  ws.on('message', (data: Buffer) => {
    const message = JSON.parse(data.toString());
    handleMessage(clientId, message);
  });

  ws.on('close', () => {
    clients.delete(clientId);
    console.log(`Client ${clientId} disconnected. Total: ${clients.size}`);
  });
});

function handleMessage(senderId: string, message: { type: string; payload: unknown }): void {
  switch (message.type) {
    case 'broadcast':
      broadcast(senderId, message.payload);
      break;
    case 'direct':
      sendToClient(message.payload as string, { from: senderId, data: message.payload });
      break;
  }
}

function broadcast(senderId: string, data: unknown): void {
  clients.forEach((client) => {
    if (client.id !== senderId && client.ws.readyState === WebSocket.OPEN) {
      client.ws.send(JSON.stringify({ type: 'broadcast', data }));
    }
  });
}

function sendToClient(clientId: string, data: unknown): void {
  const client = clients.get(clientId);
  if (client?.ws.readyState === WebSocket.OPEN) {
    client.ws.send(JSON.stringify(data));
  }
}

// Heartbeat mechanism
const heartbeat = setInterval(() => {
  clients.forEach((client) => {
    if (!client.isAlive) {
      client.ws.terminate();
      clients.delete(client.id);
      return;
    }
    client.isAlive = false;
    client.ws.ping();
  });
}, 30000);

wss.on('close', () => clearInterval(heartbeat));
```

### Binary Data Transfer

```typescript
// Client: Sending binary data
function sendBinaryData(ws: WebSocket): void {
  // Send ArrayBuffer
  const buffer = new ArrayBuffer(32);
  const view = new Uint8Array(buffer);
  for (let i = 0; i < 32; i++) {
    view[i] = i;
  }
  ws.send(buffer);

  // Send Blob
  const blob = new Blob(['Hello, Binary World!'], { type: 'text/plain' });
  ws.send(blob);

  // Send typed array
  const typedArray = new Float32Array([1.1, 2.2, 3.3, 4.4]);
  ws.send(typedArray.buffer);
}

// Server: Handling binary data
wss.on('connection', (ws) => {
  ws.on('message', (data, isBinary) => {
    if (isBinary) {
      // Handle as Buffer
      const buffer = Buffer.from(data);
      console.log('Received binary:', buffer.length, 'bytes');

      // Parse as needed
      const view = new Uint8Array(buffer);
      console.log('First byte:', view[0]);
    } else {
      // Handle as string
      const message = JSON.parse(data.toString());
      console.log('Received text:', message);
    }
  });
});
```

### Heartbeat Implementation

```typescript
class HeartbeatWebSocket {
  private ws: WebSocket;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private heartbeatTimeout: NodeJS.Timeout | null = null;
  private readonly HEARTBEAT_INTERVAL = 30000;
  private readonly HEARTBEAT_TIMEOUT = 10000;

  constructor(url: string) {
    this.ws = new WebSocket(url);
    this.setupConnection();
  }

  private setupConnection(): void {
    this.ws.onopen = () => {
      this.startHeartbeat();
    };

    this.ws.onmessage = (event) => {
      if (event.data === 'pong') {
        this.onPong();
      }
    };

    this.ws.onclose = () => {
      this.stopHeartbeat();
    };
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send('ping');
        this.heartbeatTimeout = setTimeout(() => {
          console.log('Heartbeat timeout, closing connection');
          this.ws.close();
        }, this.HEARTBEAT_TIMEOUT);
      }
    }, this.HEARTBEAT_INTERVAL);
  }

  private onPong(): void {
    if (this.heartbeatTimeout) {
      clearTimeout(this.heartbeatTimeout);
      this.heartbeatTimeout = null;
    }
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) clearInterval(this.heartbeatInterval);
    if (this.heartbeatTimeout) clearTimeout(this.heartbeatTimeout);
  }
}
```

## Real-World Use Cases

### 1. Chat Applications

```typescript
// Real-time chat with message history
class ChatService {
  private rooms = new Map<string, Set<string>>();

  handleMessage(clientId: string, message: ChatMessage): void {
    switch (message.type) {
      case 'join':
        this.joinRoom(clientId, message.roomId);
        break;
      case 'leave':
        this.leaveRoom(clientId, message.roomId);
        break;
      case 'message':
        this.broadcastToRoom(message.roomId, {
          type: 'message',
          from: clientId,
          content: message.content,
          timestamp: Date.now(),
        });
        break;
    }
  }

  private joinRoom(clientId: string, roomId: string): void {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new Set());
    }
    this.rooms.get(roomId)!.add(clientId);
  }

  private broadcastToRoom(roomId: string, message: object): void {
    this.rooms.get(roomId)?.forEach((clientId) => {
      sendToClient(clientId, message);
    });
  }
}
```

### 2. Live Stock Ticker

```typescript
// Real-time financial data streaming
class StockTicker {
  private subscriptions = new Map<string, Set<string>>();

  subscribe(clientId: string, symbols: string[]): void {
    symbols.forEach((symbol) => {
      if (!this.subscriptions.has(symbol)) {
        this.subscriptions.set(symbol, new Set());
      }
      this.subscriptions.get(symbol)!.add(clientId);
    });
  }

  // Called when stock price changes
  onPriceUpdate(symbol: string, price: number): void {
    this.subscriptions.get(symbol)?.forEach((clientId) => {
      sendToClient(clientId, {
        type: 'price_update',
        symbol,
        price,
        timestamp: Date.now(),
      });
    });
  }
}
```

### 3. Collaborative Editing

```typescript
// Operational Transform for real-time collaboration
class CollaborativeEditor {
  private documents = new Map<string, DocumentState>();
  private clients = new Map<string, string>(); // clientId -> documentId

  handleOperation(clientId: string, operation: Operation): void {
    const docId = this.clients.get(clientId);
    if (!docId) return;

    const doc = this.documents.get(docId);
    if (!doc) return;

    // Transform operation against pending operations
    const transformedOp = this.transformOperation(operation, doc.pendingOps);

    // Apply to document
    this.applyOperation(doc, transformedOp);

    // Store in pending operations
    doc.pendingOps.push(transformedOp);

    // Broadcast to other clients
    this.broadcastToDocument(docId, clientId, transformedOp);
  }

  private transformOperation(op: Operation, pendingOps: Operation[]): Operation {
    return pendingOps.reduce(
      (transformedOp, pendingOp) => Operation.transform(transformedOp, pendingOp),
      op
    );
  }
}
```

### 4. Multiplayer Games

```typescript
// Game state synchronization
class GameServer {
  private gameRooms = new Map<string, GameState>();
  private tickRate = 20; // 20 ticks per second

  startGameLoop(roomId: string): void {
    setInterval(() => {
      const state = this.gameRooms.get(roomId);
      if (!state) return;

      // Update game logic
      this.updatePhysics(state);
      this.checkCollisions(state);
      this.updateScores(state);

      // Broadcast state to all players
      this.broadcastGameState(roomId, state);
    }, 1000 / this.tickRate);
  }

  private broadcastGameState(roomId: string, state: GameState): void {
    const clients = this.getRoomClients(roomId);
    clients.forEach((client) => {
      // Send only relevant state to each client (visibility culling)
      const relevantState = this.getRelevantState(state, client.position);
      sendToClient(client.id, {
        type: 'game_state',
        ...relevantState,
      });
    });
  }
}
```

### 5. Live Notifications

```typescript
// Push notification system
class NotificationService {
  private userSockets = new Map<string, Set<string>>(); // userId -> socketIds

  sendNotification(userId: string, notification: Notification): void {
    const sockets = this.userSockets.get(userId);
    if (sockets && sockets.size > 0) {
      // Send via WebSocket
      sockets.forEach((socketId) => {
        sendToClient(socketId, {
          type: 'notification',
          ...notification,
        });
      });
    } else {
      // Fallback to push notification
      this.sendPushNotification(userId, notification);
    }
  }
}
```

## Common Mistakes

### 1. Not Handling Reconnection

```typescript
// ❌ Bad: No reconnection logic
ws.onclose = () => {
  console.log('Connection closed');
};

// ✅ Good: Exponential backoff reconnection
class ReconnectingWebSocket {
  private reconnectAttempts = 0;
  private maxAttempts = 5;

  private handleClose(): void {
    if (this.reconnectAttempts < this.maxAttempts) {
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      this.reconnectAttempts++;
      setTimeout(() => this.reconnect(), delay);
    }
  }
}
```

### 2. No Message Validation

```typescript
// ❌ Bad: No validation
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  processData(data); // Could crash on invalid data
};

// ✅ Good: Schema validation
import { z } from 'zod';

const MessageSchema = z.object({
  type: z.enum(['chat', 'update', 'delete']),
  payload: z.record(z.unknown()),
  timestamp: z.number(),
});

ws.onmessage = (event) => {
  try {
    const parsed = JSON.parse(event.data);
    const validated = MessageSchema.parse(parsed);
    processData(validated);
  } catch (error) {
    console.error('Invalid message:', error);
  }
};
```

### 3. Memory Leaks from Unsubscribed Listeners

```typescript
// ❌ Bad: Not cleaning up
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // This creates a closure that may never be cleaned up
  eventEmitter.on('update', () => {
    ws.send(JSON.stringify({ type: 'update', data }));
  });
};

// ✅ Good: Clean up subscriptions
class WebSocketHandler {
  private cleanup: (() => void)[] = [];

  setup(): void {
    const handler = (data: unknown) => {
      this.ws.send(JSON.stringify({ type: 'update', data }));
    };
    eventEmitter.on('update', handler);
    this.cleanup.push(() => eventEmitter.off('update', handler));
  }

  destroy(): void {
    this.cleanup.forEach((fn) => fn());
    this.ws.close();
  }
}
```

### 4. Not Handling Backpressure

```typescript
// ❌ Bad: Sending without checking buffer
function broadcast(data: unknown): void {
  clients.forEach((client) => {
    client.ws.send(JSON.stringify(data)); // Could overflow buffer
  });
}

// ✅ Good: Check buffer before sending
function broadcast(data: unknown): void {
  const message = JSON.stringify(data);
  clients.forEach((client) => {
    if (client.ws.bufferedAmount < 1024 * 1024) { // 1MB limit
      client.ws.send(message);
    } else {
      console.warn(`Client ${client.id} buffer full, dropping message`);
    }
  });
}
```

### 5. Exposing Internal Errors

```typescript
// ❌ Bad: Sending error details to client
ws.on('error', (error) => {
  ws.send(JSON.stringify({
    type: 'error',
    message: error.message,
    stack: error.stack, // Security risk!
  }));
});

// ✅ Good: Generic error messages
ws.on('error', (error) => {
  console.error('Server error:', error);
  ws.send(JSON.stringify({
    type: 'error',
    message: 'An internal error occurred',
  }));
});
```

## Best Practices

### 1. Authentication & Authorization

```typescript
// Authenticate WebSocket connections
wss.on('connection', (ws, req) => {
  const token = new URL(req.url!, `http://${req.headers.host}`).searchParams.get('token');

  if (!token) {
    ws.close(4001, 'Authentication required');
    return;
  }

  try {
    const user = verifyJWT(token);
    (ws as any).userId = user.id;
    (ws as any).userRole = user.role;
  } catch {
    ws.close(4001, 'Invalid token');
  }
});
```

### 2. Rate Limiting

```typescript
class RateLimiter {
  private limits = new Map<string, { count: number; resetAt: number }>();

  isAllowed(clientId: string, limit: number, windowMs: number): boolean {
    const now = Date.now();
    const record = this.limits.get(clientId);

    if (!record || now > record.resetAt) {
      this.limits.set(clientId, { count: 1, resetAt: now + windowMs });
      return true;
    }

    if (record.count >= limit) {
      return false;
    }

    record.count++;
    return true;
  }
}
```

### 3. Message Compression

```typescript
import { WebSocketServer } from 'ws';
import { createWebSocketStream } from 'ws';
import { createGzip, createGunzip } from 'zlib';

// Enable permessage-deflate extension
const wss = new WebSocketServer({
  port: 8080,
  perMessageDeflate: {
    zlibDeflateOptions: {
      chunkSize: 1024,
      memLevel: 7,
      level: 3,
    },
    zlibInflateOptions: {
      chunkSize: 10 * 1024,
    },
    threshold: 1024,
    concurrencyLimit: 10,
  },
});
```

### 4. Connection Pool Management

```typescript
class ConnectionPool {
  private maxConnections = 1000;
  private connections = new Map<string, WebSocket>();

  add(clientId: string, ws: WebSocket): boolean {
    if (this.connections.size >= this.maxConnections) {
      // Evict oldest or reject
      return false;
    }
    this.connections.set(clientId, ws);
    return true;
  }

  remove(clientId: string): void {
    this.connections.delete(clientId);
  }

  getStats(): { total: number; byRegion: Map<string, number> } {
    const byRegion = new Map<string, number>();
    this.connections.forEach((ws) => {
      const region = (ws as any).region || 'unknown';
      byRegion.set(region, (byRegion.get(region) || 0) + 1);
    });
    return { total: this.connections.size, byRegion };
  }
}
```

## Performance Considerations

### Latency Comparison

| Protocol | Latency | Bandwidth | Use Case |
|---|---|---|---|
| HTTP Polling | 100-500ms | High | Simple updates |
| HTTP Long Polling | 50-200ms | Medium | Occasional updates |
| Server-Sent Events | 10-50ms | Low | Server → Client only |
| WebSockets | 1-10ms | Very Low | Bidirectional real-time |

### Memory Usage

```
Per Connection Memory Usage:
- HTTP Request: ~2-8 KB (headers)
- WebSocket: ~0.5-2 KB (connection state)

10,000 concurrent connections:
- HTTP Long Polling: ~20-80 MB
- WebSockets: ~5-20 MB
```

### Throughput Benchmarks

```
Message Rate (messages/second):
- HTTP REST: 1,000-5,000
- HTTP Long Polling: 5,000-20,000
- WebSockets: 50,000-500,000
- WebSockets (binary): 100,000-1,000,000
```

## Interview Questions

### Beginner (5)

1. **What is the difference between HTTP and WebSockets?**
   - HTTP is request-response; WebSockets are full-duplex bidirectional
   - HTTP creates new connections; WebSockets use a single persistent connection
   - HTTP has high overhead per message; WebSockets have minimal frame overhead

2. **What is the WebSocket handshake?**
   - An HTTP request with `Upgrade: websocket` header
   - Server responds with `101 Switching Protocols`
   - Connection upgrades from HTTP to WebSocket protocol

3. **What does full-duplex mean?**
   - Both client and server can send messages independently at any time
   - Like a phone call where both parties can speak simultaneously
   - Contrast with half-duplex (walkie-talkie) and simplex (radio)

4. **What is the WebSocket URL scheme?**
   - `ws://` for unencrypted (like `http://`)
   - `wss://` for encrypted (like `https://`)
   - Always use `wss://` in production

5. **How do you detect if a WebSocket connection is open?**
   - Check `ws.readyState === WebSocket.OPEN`
   - Listen for `onopen` event
   - Check `ws.readyState === 1`

### Intermediate (5-8)

6. **How do you handle WebSocket reconnection?**
   - Implement exponential backoff
   - Track reconnection attempts
   - Reset state on successful reconnection
   - Handle edge cases (server restart, network changes)

7. **What is the purpose of the `Sec-WebSocket-Key` header?**
   - Prevents caching proxies from reusing connections
   - Provides proof that the server understands WebSockets
   - Not for security (connection is not encrypted at this point)

8. **How do you handle binary data in WebSockets?**
   - Use `ws.send(arrayBuffer)` for sending
   - Check `event.data instanceof ArrayBuffer` for receiving
   - Set appropriate binary type: `ws.binaryType = 'arraybuffer'`

9. **What are WebSocket subprotocols?**
   - Negotiated during handshake via `Sec-WebSocket-Protocol`
   - Allow application-level protocol definition
   - Example: `graphql-ws` for GraphQL subscriptions

10. **How do you handle WebSocket errors?**
    - Listen for `onerror` event
    - Handle `onclose` with appropriate reconnection logic
    - Log error codes and reasons

### Senior (8-12)

11. **How would you scale WebSockets across multiple servers?**
    - Use sticky sessions or connection-based routing
    - Implement Redis Pub/Sub for cross-server communication
    - Consider message brokers (RabbitMQ, Kafka)
    - Use consistent hashing for session affinity

12. **How do you handle message ordering in distributed WebSockets?**
    - Use sequence numbers or timestamps
    - Implement vector clocks for causal ordering
    - Consider CRDTs for conflict resolution
    - Use message queues for guaranteed ordering

13. **What is backpressure and how do you handle it?**
    - Server can't process messages as fast as they arrive
    - Monitor `bufferedAmount` property
    - Implement message queuing with limits
    - Drop or defer messages when buffer is full

14. **How do you secure WebSocket connections?**
    - Always use WSS (WebSocket Secure)
    - Implement authentication (JWT, session cookies)
    - Validate all incoming messages
    - Rate limit connections and messages
    - Use CSP headers to prevent XSS

15. **How do you handle connection state in microservices?**
    - Centralized connection registry (Redis)
    - Event-driven architecture for state sync
    - Saga pattern for distributed transactions
    - Circuit breaker for fault tolerance

### FAANG-style (5-8)

16. **Design a chat system supporting 10 million concurrent users**
    - Connection management with consistent hashing
    - Message fanout using pub/sub
    - Presence service with heartbeat
    - Message storage with Cassandra/DynamoDB
    - CDN for media delivery

17. **How would you implement real-time collaboration (Google Docs style)?**
    - Operational Transform (OT) or CRDT
    - Conflict resolution strategies
    - Undo/redo with operation history
    - Cursor presence and awareness

18. **Design a multiplayer game backend**
    - Deterministic game loop
    - State synchronization (full vs delta)
    - Client-side prediction
    - Lag compensation techniques
    - Anti-cheat measures

19. **How do you handle WebSocket connections during deployment?**
    - Graceful shutdown with connection draining
    - Blue-green deployment strategy
    - Session migration between servers
    - Health checks and readiness probes

20. **Optimize WebSocket performance for high-throughput scenarios**
    - Message batching and compression
    - Binary protocol instead of JSON
    - Connection pooling and multiplexing
    - Memory-efficient data structures
    - Profiling and bottleneck identification

### Follow-ups (5-8)

21. **What happens if a WebSocket server crashes?**
    - Clients receive `onclose` event with code 1006
    - Clients should implement reconnection logic
    - Consider session persistence for recovery
    - Monitor connection drops for alerting

22. **How do you test WebSocket applications?**
    - Unit tests for message handlers
    - Integration tests with mock servers
    - Load testing with tools like Artillery
    - Chaos engineering for failure scenarios

23. **What are WebSocket alternatives and when would you use them?**
    - SSE for server-to-client only
    - HTTP/2 Server Push for static assets
    - gRPC for high-performance RPC
    - MQTT for IoT devices

24. **How do you monitor WebSocket connections in production?**
    - Track connection counts and durations
    - Monitor message rates and latency
    - Alert on error rates and disconnections
    - Dashboard for real-time visibility

25. **What are common WebSocket attack vectors and mitigations?**
    - Cross-site WebSocket hijacking (CSWSH)
    - DoS attacks via connection flooding
    - Message injection and manipulation
    - Information disclosure through errors

## Summary

WebSockets are essential for building real-time applications that require bidirectional communication. Key takeaways:

- **Protocol**: HTTP upgrade to persistent TCP connection
- **Characteristics**: Full-duplex, low latency, minimal overhead
- **Use Cases**: Chat, gaming, live data, collaboration tools
- **Challenges**: Scaling, security, reconnection, state management
- **Best Practices**: Authentication, rate limiting, compression, monitoring

Understanding WebSockets at a deep level demonstrates system design expertise and the ability to build performant, real-time applications.

## References & Learn More

- [RFC 6455 - The WebSocket Protocol](https://tools.ietf.org/html/rfc6455)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [WebSocket Protocol Specification](https://www.rfc-editor.org/rfc/rfc6455)
- [Socket.io Documentation](https://socket.io/docs/)
- [ws Library Documentation](https://github.com/websockets/ws)
- [Real-Time Web Application Architecture](https://martinfowler.com/articles/2022-real-time-web-architecture.html)
