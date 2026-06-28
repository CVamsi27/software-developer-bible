# Server-Sent Events (SSE)

## Definition

Server-Sent Events (SSE) is a **standardized technology** that allows servers to push data to clients over HTTP in real-time. Unlike WebSockets, SSE provides **unidirectional communication** from server to client, making it ideal for scenarios where the client only needs to receive updates (news feeds, live scores, notifications).

SSE uses the `EventSource` API on the client and standard HTTP on the server, providing automatic reconnection, event IDs, and last-event-id tracking.

## Why Do We Need It?

| Feature | SSE | WebSockets |
|---|---|---|
| Direction | Server → Client only | Bidirectional |
| Protocol | HTTP | WebSocket (separate protocol) |
| Reconnection | Automatic | Manual implementation |
| Event IDs | Built-in support | Manual implementation |
| Data Format | Text (UTF-8) | Text or Binary |
| Browser Support | All modern browsers | All modern browsers |
| Proxy/Firewall | Works with HTTP | May be blocked |
| Complexity | Simple | More complex |
| Scalability | HTTP infrastructure | Custom infrastructure |

### When to Choose SSE

```text
Use SSE when:                    Use WebSockets when:

- Server pushes updates          - Bidirectional communication needed
- No client → server messages    - Client sends frequent messages
- Simple implementation needed   - Binary data transfer required
- HTTP infrastructure available  - Low-latency critical
- Auto-reconnection needed       - Custom protocol needed
- Event sourcing useful          - Full-duplex required

```

## How It Works

### SSE Protocol

```text
Client                              Server

  |                                    |
  |  GET /events HTTP/1.1              |
  |  Accept: text/event-stream         |
  |----------------------------------->|
  |                                    |
  |  HTTP/1.1 200 OK                   |
  |  Content-Type: text/event-stream   |
  |  Cache-Control: no-cache           |
  |  Connection: keep-alive            |
  |  Transfer-Encoding: chunked        |
  |<-----------------------------------|
  |                                    |
  |  data: {"type":"update"}\n\n       |
  |<-----------------------------------|
  |                                    |
  |  id: 12345\n                       |
  |  event: message\n                  |
  |  data: Hello World\n\n             |
  |<-----------------------------------|
  |                                    |
  |  retry: 5000\n                     |
  |  data: Reconnect in 5s\n\n         |
  |<-----------------------------------|

```

### Message Format

```text
Single-line message:
data: Hello World\n\n

Multi-line message:
data: Line 1\n
data: Line 2\n
data: Line 3\n\n

With event type:
event: user-connected\n
data: {"userId": 123}\n\n

With event ID:
id: 42\n
data: Important update\n\n

With retry interval:
retry: 3000\n
data: Will retry in 3 seconds\n\n

Comments (ignored by client):
: This is a comment\n
: Keep-alive ping\n\n

```

### Connection Lifecycle

```text
+-----------+     +-----------+     +-----------+     +-----------+

| CONNECTING| --> |   OPEN    | --> | CONNECTING| --> |   OPEN    |

+-----------+     +-----------+     +-----------+     +-----------+

      |                |                 |                 |

      | HTTP Request   | Receive data    | Auto-reconnect  | Resume
      | sent           | from server     | on disconnect   | from last
      |                |                 |                 | event ID

```

## Code Examples

### Basic SSE Client

```typescript
class SSEClient {
  private eventSource: EventSource | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private lastEventId: string | null = null;

  connect(url: string): void {
    const separator = url.includes('?') ? '&' : '?';
    const urlWithId = this.lastEventId
      ? `${url}${separator}lastEventId=${this.lastEventId}`
      : url;

    this.eventSource = new EventSource(urlWithId);

    this.eventSource.onopen = () => {
      console.log('SSE connection opened');
      this.reconnectAttempts = 0;
    };

    this.eventSource.onmessage = (event) => {
      console.log('Received message:', event.data);
      this.handleMessage(event);
    };

    this.eventSource.addEventListener('custom-event', (event) => {
      console.log('Custom event:', event.data);
      this.handleCustomEvent(event);
    });

    this.eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      this.handleError(error);
    };
  }

  private handleMessage(event: MessageEvent): void {
    this.lastEventId = event.lastEventId;
    // Process message
  }

  private handleCustomEvent(event: MessageEvent): void {
    this.lastEventId = event.lastEventId;
    // Process custom event
  }

  private handleError(error: Event): void {
    this.reconnectAttempts++;
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.eventSource?.close();
    }
  }

  disconnect(): void {
    this.eventSource?.close();
    this.eventSource = null;
  }
}

```

### Basic SSE Server (Express)

```typescript
import express from 'express';
import { Request, Response } from 'express';

const app = express();

interface SSEClient {
  id: string;
  res: Response;
  lastEventId: number;
}

const clients = new Map<string, SSEClient>();

app.get('/events', (req: Request, res: Response) => {
  const clientId = crypto.randomUUID();

  // Set SSE headers
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no'); // Disable nginx buffering

  // Disable compression for SSE
  res.setHeader('Content-Encoding', 'identity');

  // Handle client reconnect with last event ID
  const lastEventId = parseInt(req.headers['last-event-id'] as string) || 0;

  // Register client
  const client: SSEClient = {
    id,
    res,
    lastEventId,
  };
  clients.set(id, client);

  console.log(`Client ${clientId} connected. Total: ${clients.size}`);

  // Send initial connection message
  res.write(`id: ${Date.now()}\n`);
  res.write(`event: connected\n`);
  res.write(`data: ${JSON.stringify({ clientId, serverTime: Date.now() })}\n\n`);

  // Send missed events if reconnecting
  if (lastEventId > 0) {
    sendMissedEvents(client, lastEventId);
  }

  // Handle client disconnect
  req.on('close', () => {
    clients.delete(clientId);
    console.log(`Client ${clientId} disconnected. Total: ${clients.size}`);
  });
});

function sendMissedEvents(client: SSEClient, fromId: number): void {
  const missedEvents = getEventsAfterId(fromId);
  missedEvents.forEach((event) => {
    sendEventToClient(client, event);
  });
}

function sendEventToClient(client: SSEClient, event: Event): void {
  client.res.write(`id: ${event.id}\n`);
  client.res.write(`event: ${event.type}\n`);
  client.res.write(`data: ${JSON.stringify(event.data)}\n\n`);
}

function broadcastEvent(event: Event): void {
  clients.forEach((client) => {
    // Only send events newer than client's last event
    if (event.id > client.lastEventId) {
      sendEventToClient(client, event);
    }
  });
}

// Keepalive ping every 30 seconds
setInterval(() => {
  clients.forEach((client) => {
    client.res.write(`: ping\n\n`);
  });
}, 30000);

app.listen(3000);

```

### TypeScript SSE Client with Events

```typescript
interface SSEEvent {
  id: string;
  type: string;
  data: unknown;
  timestamp: number;
}

class TypedSSEClient<T extends Record<string, unknown>> {
  private eventSource: EventSource | null = null;
  private handlers = new Map<string, Set<(data: T[keyof T]) => void>>();
  private reconnectTimer: NodeJS.Timeout | null = null;
  private lastEventId: number = 0;

  constructor(private url: string) {}

  connect(): void {
    this.eventSource = new EventSource(this.url);

    this.eventSource.onopen = () => {
      this.emit('_open', undefined as T[keyof T]);
    };

    this.eventSource.onmessage = (event) => {
      this.lastEventId = parseInt(event.lastEventId) || this.lastEventId;
      const data = JSON.parse(event.data) as T[keyof T];
      this.emit('message', data);
    };

    this.eventSource.onerror = (error) => {
      this.emit('_error', error as unknown as T[keyof T]);
      this.scheduleReconnect();
    };
  }

  on<K extends keyof T>(event: K, handler: (data: T[K]) => void): () => void {
    if (!this.handlers.has(event as string)) {
      this.handlers.set(event as string, new Set());
    }
    this.handlers.get(event as string)!.add(handler as (data: T[keyof T]) => void);

    // Return unsubscribe function
    return () => {
      this.handlers.get(event as string)?.delete(handler as (data: T[keyof T]) => void);
    };
  }

  private emit(event: string, data: T[keyof T]): void {
    this.handlers.get(event)?.forEach((handler) => {
      try {
        handler(data);
      } catch (error) {
        console.error(`Error in SSE handler for ${event}:`, error);
      }
    });
  }

  private scheduleReconnect(): void {
    if (this.reconnectTimer) return;

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, delay);
  }

  private get reconnectAttempts(): number {
    return this.lastEventId > 0 ? 0 : 0; // Track separately in real impl
  }

  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }
    this.eventSource?.close();
  }
}

// Usage
type ServerEvents = {
  'user-connected': { userId: string; timestamp: number };
  'user-disconnected': { userId: string; timestamp: number };
  'message': { content: string; sender: string; timestamp: number };
  'notification': { title: string; body: string; type: string };
};

const client = new TypedSSEClient<ServerEvents>('http://localhost:3000/events');

client.on('message', (data) => {
  console.log('New message:', data.content);
});

client.on('notification', (data) => {
  console.log('Notification:', data.title);
});

client.on('user-connected', (data) => {
  console.log('User joined:', data.userId);
});

client.connect();

```

### SSE with Node.js (No Framework)

```typescript
import http from 'http';
import { URL } from 'url';

interface Client {
  id: string;
  res: http.ServerResponse;
  lastEventId: number;
}

const clients = new Map<string, Client>();

const server = http.createServer((req, res) => {
  const url = new URL(req.url!, `http://${req.headers.host}`);

  if (url.pathname === '/events') {
    // Handle SSE connection
    const clientId = crypto.randomUUID();
    const lastEventId = parseInt(req.headers['last-event-id'] as string) || 0;

    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    });

    const client: Client = { id: clientId, res, lastEventId };
    clients.set(clientId, client);

    // Send initial message
    res.write(`id: ${Date.now()}\n`);
    res.write(`event: connected\n`);
    res.write(`data: {"clientId":"${clientId}"}\n\n`);

    req.on('close', () => {
      clients.delete(clientId);
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

function broadcast(event: string, data: unknown, id?: number): void {
  const eventId = id || Date.now();
  const message = `id: ${eventId}\nevent: ${event}\ndata: ${JSON.stringify(data)}\n\n`;

  clients.forEach((client) => {
    if (!client.res.destroyed) {
      client.res.write(message);
    }
  });
}

// Example: Send temperature update
setInterval(() => {
  broadcast('temperature', {
    value: Math.random() * 100,
    unit: 'celsius',
    timestamp: Date.now(),
  });
}, 5000);

server.listen(3000);

```

### SSE with Authentication

```typescript
import express from 'express';
import jwt from 'jsonwebtoken';

const app = express();

// Authentication middleware
app.use('/events', (req, res, next) => {
  const token = req.query.token as string;

  if (!token) {
    return res.status(401).json({ error: 'Token required' });
  }

  try {
    const user = jwt.verify(token, process.env.JWT_SECRET!) as { userId: string };
    (req as any).userId = user.userId;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
});

app.get('/events', (req, res) => {
  const userId = (req as any).userId;
  const clientId = crypto.randomUUID();

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Send welcome message
  res.write(`id: ${Date.now()}\n`);
  res.write(`event: welcome\n`);
  res.write(`data: ${JSON.stringify({ userId, clientId })}\n\n`);

  // Store client for user-specific events
  const client = { id: clientId, res, userId };
  userClients.set(userId, client);

  req.on('close', () => {
    userClients.delete(userId);
  });
});

// Send event to specific user
function sendToUser(userId: string, event: string, data: unknown): void {
  const client = userClients.get(userId);
  if (client && !client.res.destroyed) {
    client.res.write(`id: ${Date.now()}\n`);
    client.res.write(`event: ${event}\n`);
    client.res.write(`data: ${JSON.stringify(data)}\n\n`);
  }
}

```

## Real-World Use Cases

### 1. Live News Feed

```typescript
class NewsFeedService {
  private subscriptions = new Map<string, Set<string>>(); // category -> clientIds
  private clients = new Map<string, { res: Response; categories: Set<string> }>();

  subscribe(clientId: string, res: Response, categories: string[]): void {
    this.clients.set(clientId, { res, categories: new Set(categories) });

    categories.forEach((category) => {
      if (!this.subscriptions.has(category)) {
        this.subscriptions.set(category, new Set());
      }
      this.subscriptions.get(category)!.add(clientId);
    });

    // Send initial recent articles
    this.sendRecentArticles(clientId, categories);
  }

  publishArticle(article: Article): void {
    const subscribers = this.subscriptions.get(article.category);
    if (!subscribers) return;

    subscribers.forEach((clientId) => {
      const client = this.clients.get(clientId);
      if (client && !client.res.destroyed) {
        client.res.write(`id: ${article.id}\n`);
        client.res.write(`event: article\n`);
        client.res.write(`data: ${JSON.stringify(article)}\n\n`);
      }
    });
  }

  private async sendRecentArticles(clientId: string, categories: string[]): Promise<void> {
    const client = this.clients.get(clientId);
    if (!client) return;

    const articles = await getRecentArticles(categories, 10);
    articles.forEach((article) => {
      client.res.write(`id: ${article.id}\n`);
      client.res.write(`event: article\n`);
      client.res.write(`data: ${JSON.stringify(article)}\n\n`);
    });
  }
}

```

### 2. Live Sports Scores

```typescript
class SportsScoreService {
  private gameSubscriptions = new Map<string, Set<string>>(); // gameId -> clientIds
  private clientGames = new Map<string, Set<string>>(); // clientId -> gameIds

  subscribeToGame(clientId: string, res: Response, gameId: string): void {
    if (!this.gameSubscriptions.has(gameId)) {
      this.gameSubscriptions.set(gameId, new Set());
    }
    this.gameSubscriptions.get(gameId)!.add(clientId);

    if (!this.clientGames.has(clientId)) {
      this.clientGames.set(clientId, new Set());
    }
    this.clientGames.get(clientId)!.add(gameId);

    // Send current score
    this.sendCurrentScore(clientId, res, gameId);
  }

  updateScore(gameId: string, score: GameScore): void {
    const subscribers = this.gameSubscriptions.get(gameId);
    if (!subscribers) return;

    subscribers.forEach((clientId) => {
      const client = this.getClient(clientId);
      if (client && !client.res.destroyed) {
        client.res.write(`id: ${score.id}\n`);
        client.res.write(`event: score-update\n`);
        client.res.write(`data: ${JSON.stringify({ gameId, ...score })}\n\n`);
      }
    });
  }

  private async sendCurrentScore(clientId: string, res: Response, gameId: string): Promise<void> {
    const score = await getCurrentScore(gameId);
    res.write(`id: ${score.id}\n`);
    res.write(`event: current-score\n`);
    res.write(`data: ${JSON.stringify({ gameId, ...score })}\n\n`);
  }
}

```

### 3. Live Dashboard Metrics

```typescript
class DashboardMetricsService {
  private dashboards = new Map<string, { res: Response; metrics: string[] }>();

  subscribe(clientId: string, res: Response, metrics: string[]): void {
    this.dashboards.set(clientId, { res, metrics });

    // Start sending metrics
    this.startMetricStream(clientId);
  }

  private startMetricStream(clientId: string): void {
    const dashboard = this.dashboards.get(clientId);
    if (!dashboard) return;

    const interval = setInterval(async () => {
      if (dashboard.res.destroyed) {
        clearInterval(interval);
        return;
      }

      const metrics = await this.getMetrics(dashboard.metrics);
      dashboard.res.write(`id: ${Date.now()}\n`);
      dashboard.res.write(`event: metrics\n`);
      dashboard.res.write(`data: ${JSON.stringify(metrics)}\n\n`);
    }, 1000); // Send every second
  }

  private async getMetrics(metrics: string[]): Promise<Record<string, number>> {
    const result: Record<string, number> = {};
    for (const metric of metrics) {
      result[metric] = await getMetricValue(metric);
    }
    return result;
  }
}

```

### 4. Chat Application (SSE + Fetch)

```typescript
// Client: SSE for receiving, Fetch for sending
class ChatClient {
  private eventSource: EventSource;
  private messageHandler: (message: ChatMessage) => void;

  constructor(private baseUrl: string, private authToken: string) {
    this.eventSource = new EventSource(`${baseUrl}/events?token=${authToken}`);
    this.setupEventListeners();
  }

  private setupEventListeners(): void {
    this.eventSource.addEventListener('message', (event) => {
      const message = JSON.parse(event.data) as ChatMessage;
      this.messageHandler(message);
    });

    this.eventSource.addEventListener('typing', (event) => {
      const data = JSON.parse(event.data) as { userId: string; isTyping: boolean };
      this.handleTypingIndicator(data);
    });
  }

  async sendMessage(content: string, roomId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.authToken}`,
      },
      body: JSON.stringify({ content, roomId }),
    });

    if (!response.ok) {
      throw new Error('Failed to send message');
    }
  }

  onMessage(handler: (message: ChatMessage) => void): void {
    this.messageHandler = handler;
  }

  disconnect(): void {
    this.eventSource.close();
  }
}

```

## Common Mistakes

### 1. Not Setting Correct Headers

```typescript
// ❌ Bad: Missing headers
res.writeHead(200, { 'Content-Type': 'text/event-stream' });

// ✅ Good: Complete headers
res.writeHead(200, {
  'Content-Type': 'text/event-stream',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'X-Accel-Buffering': 'no', // For nginx
  'Content-Encoding': 'identity', // Disable compression
});

```

### 2. Not Handling Client Disconnects

```typescript
// ❌ Bad: No cleanup
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');

  // Send data forever
  setInterval(() => {
    res.write(`data: ${JSON.stringify(getData())}\n\n`);
  }, 1000);
});

// ✅ Good: Cleanup on disconnect
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');

  const clientId = registerClient(res);

  const interval = setInterval(() => {
    if (!res.destroyed) {
      res.write(`data: ${JSON.stringify(getData())}\n\n`);
    }
  }, 1000);

  req.on('close', () => {
    clearInterval(interval);
    unregisterClient(clientId);
  });
});

```

### 3. Not Using Event IDs

```typescript
// ❌ Bad: No event IDs
res.write(`data: ${JSON.stringify(data)}\n\n`);

// ✅ Good: Include event IDs for reconnection
res.write(`id: ${event.id}\n`);
res.write(`data: ${JSON.stringify(event.data)}\n\n`);

```

### 4. Not Handling Reconnection

```typescript
// ❌ Bad: No reconnection handling
const eventSource = new EventSource('/events');
eventSource.onmessage = (event) => {
  processEvent(event);
};

// ✅ Good: Handle reconnection with last event ID
const eventSource = new EventSource('/events');
let lastEventId = '';

eventSource.onmessage = (event) => {
  lastEventId = event.lastEventId;
  processEvent(event);
};

eventSource.onerror = () => {
  console.log('Reconnecting...');
  // EventSource auto-reconnects, but we can track state
};

```

### 5. Sending Binary Data

```typescript
// ❌ Bad: Trying to send binary
res.write(binaryData); // Will fail

// ✅ Good: Convert to base64 or use WebSockets
const base64 = binaryData.toString('base64');
res.write(`data: ${base64}\n\n`);
// Or use WebSockets for binary data

```

## Best Practices

### 1. Keepalive/Heartbeat

```typescript
// Send keepalive every 30 seconds to prevent proxy timeouts
setInterval(() => {
  clients.forEach((client) => {
    if (!client.res.destroyed) {
      // Comments are ignored by EventSource
      client.res.write(': heartbeat\n\n');
    }
  });
}, 30000);

```

### 2. Event ID Management

```typescript
// Use sequential IDs for proper reconnection
let eventCounter = 0;

function sendEvent(client: Client, event: string, data: unknown): void {
  const eventId = ++eventCounter;
  client.res.write(`id: ${eventId}\n`);
  client.res.write(`event: ${event}\n`);
  client.res.write(`data: ${JSON.stringify(data)}\n\n`);
}

// Store recent events for missed event delivery
const recentEvents = new Map<number, Event>();

function storeEvent(id: number, event: Event): void {
  recentEvents.set(id, event);
  // Keep only last 1000 events
  if (recentEvents.size > 1000) {
    const oldest = Math.min(...recentEvents.keys());
    recentEvents.delete(oldest);
  }
}

function getEventsAfterId(lastId: number): Event[] {
  const events: Event[] = [];
  recentEvents.forEach((event, id) => {
    if (id > lastId) events.push(event);
  });
  return events.sort((a, b) => a.id - b.id);
}

```

### 3. Compression

```typescript
import { createGzip } from 'zlib';

// Enable gzip compression for large payloads
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Content-Encoding', 'gzip');

  const gzip = createGzip();
  gzip.pipe(res);

  const sendEvent = (data: unknown) => {
    const message = `data: ${JSON.stringify(data)}\n\n`;
    gzip.write(message);
  };

  // Use sendEvent instead of res.write
});

```

### 4. Connection Pooling

```typescript
class SSEConnectionPool {
  private maxConnectionsPerClient = 3;
  private clientConnections = new Map<string, number>();

  canAcceptConnection(clientId: string): boolean {
    const count = this.clientConnections.get(clientId) || 0;
    return count < this.maxConnectionsPerClient;
  }

  addConnection(clientId: string): void {
    const count = this.clientConnections.get(clientId) || 0;
    this.clientConnections.set(clientId, count + 1);
  }

  removeConnection(clientId: string): void {
    const count = this.clientConnections.get(clientId) || 0;
    if (count <= 1) {
      this.clientConnections.delete(clientId);
    } else {
      this.clientConnections.set(clientId, count - 1);
    }
  }
}

```

### 5. Error Handling

```typescript
// Server-side error handling
app.get('/events', async (req, res) => {
  try {
    res.setHeader('Content-Type', 'text/event-stream');

    const client = registerClient(res);

    // Send initial connection
    res.write(`event: connected\n`);
    res.write(`data: ${JSON.stringify({ clientId: client.id })}\n\n`);

    // Stream data with error handling
    await streamData(client, res);
  } catch (error) {
    console.error('SSE error:', error);

    // Send error event before closing
    if (!res.destroyed) {
      res.write(`event: error\n`);
      res.write(`data: ${JSON.stringify({ message: 'Stream error' })}\n\n`);
      res.end();
    }
  }
});

```

## Performance Considerations

### Memory Usage

```text
SSE vs WebSockets Memory:

- SSE: ~1-2 KB per connection (HTTP overhead)
- WebSockets: ~0.5-1 KB per connection

10,000 connections:

- SSE: ~10-20 MB
- WebSockets: ~5-10 MB

```

### Throughput

```text
Message Rate:

- SSE: 10,000-50,000 messages/second
- WebSockets: 50,000-500,000 messages/second

SSE is sufficient for most server-push scenarios

```

### Latency

```text
Latency Comparison:

- HTTP Polling: 100-500ms
- SSE: 10-50ms
- WebSockets: 1-10ms

SSE provides good latency for server-push use cases

```

## Interview Questions

### Beginner (5)

1. **What are Server-Sent Events (SSE)?**

   - Standard for server-to-client streaming over HTTP
   - Uses EventSource API on client
   - Provides automatic reconnection
   - Unidirectional (server → client)

2. **How does SSE differ from WebSockets?**

   - SSE is unidirectional; WebSockets are bidirectional
   - SSE uses HTTP; WebSockets use separate protocol
   - SSE has automatic reconnection; WebSockets require manual
   - SSE is simpler to implement

3. **What is the EventSource API?**

   - Browser API for receiving SSE
   - Handles connection management
   - Provides automatic reconnection
   - Supports event types and IDs

4. **When should you use SSE vs WebSockets?**

   - SSE: Server push, notifications, live feeds
   - WebSockets: Chat, gaming, collaboration
   - SSE: When bidirectional not needed
   - WebSockets: When low latency critical

5. **How do SSE handle reconnection?**

   - Automatic reconnection on disconnect
   - Uses last-event-id header
   - Server can set retry interval
   - Client tracks received events

### Intermediate (5-8)

6. **How do you implement SSE with authentication?**

   - Pass token in query string or header
   - Validate token on connection
   - Associate client with user
   - Clean up on disconnect

7. **How do you handle multiple event types in SSE?**

   - Use event field in message
   - Listen for specific events on client
   - Default to 'message' event if not specified
   - Type events for better organization

8. **How do you scale SSE across multiple servers?**

   - Use Redis for pub/sub
   - Implement sticky sessions
   - Share client state
   - Load balance connections

9. **How do you handle large payloads in SSE?**

   - Implement pagination
   - Use compression
   - Send data in chunks
   - Monitor bandwidth usage

10. **How do you test SSE implementations?**

    - Unit test event formatting
    - Integration test connection handling
    - Load test with multiple clients
    - Test reconnection behavior

### Senior (8-12)

11. **Design a real-time notification system with SSE**

    - User subscription management
    - Event routing and filtering
    - Persistence for offline users
    - Delivery guarantees
    - Analytics and monitoring

12. **How do you handle SSE in microservices?**

    - API gateway for connection management
    - Event bus for cross-service communication
    - Centralized subscription service
    - Service discovery for scaling

13. **How do you implement SSE with message queues?**

    - Queue messages for reliability
    - Fan-out to multiple subscribers
    - Handle queue backpressure
    - Dead letter queues for failed messages

14. **How do you monitor SSE connections in production?**

    - Track connection counts
    - Monitor message rates
    - Alert on error rates
    - Dashboard for real-time visibility

15. **How do you handle SSE during deployments?**

    - Graceful connection draining
    - Version negotiation
    - Session migration
    - Rollback strategies

### FAANG-style (5-8)

16. **Design a live feed system (Twitter-like)**

    - Real-time updates for followed users
    - Timeline generation and caching
    - Fan-out on write vs fan-out on read
    - Media handling and CDN integration
    - Rate limiting and abuse prevention

17. **Design a live sports score system**

    - Real-time score updates
    - Game state management
    - Historical data and playback
    - Push notifications for score changes
    - Analytics and statistics

18. **Design a live collaboration tool**

    - Real-time cursor tracking
    - Operation transformation
    - Conflict resolution
    - Version history
    - Offline support

19. **Design a live auction platform**

    - Real-time bidding
    - Timer management
    - Bid validation and fraud detection
    - Winner notification
    - Payment integration

20. **Design a live monitoring dashboard**

    - Real-time metrics streaming
    - Data aggregation and filtering
    - Alert management
    - Historical data viewing
    - Export and sharing

### Follow-ups (5-8)

21. **How do you handle SSE in load-balanced environments?**

    - Sticky sessions
    - Redis for state sharing
    - Consistent hashing
    - Health checks

22. **How do you secure SSE endpoints?**

    - HTTPS only
    - Token validation
    - Rate limiting
    - Input validation

23. **How do you handle SSE with CDNs?**

    - Cache-Control headers
    - Streaming support
    - Edge computing
    - Origin shielding

24. **How do you debug SSE issues?**

    - Browser dev tools
    - Server logs
    - Network monitoring
    - Client state inspection

25. **What are SSE alternatives?**

    - WebSockets
    - HTTP/2 Server Push
    - gRPC streaming
    - MQTT

## Summary

SSE is ideal for server-to-client streaming with:

- **Simple implementation**: Standard HTTP, EventSource API
- **Automatic reconnection**: Built-in retry with event IDs
- **Good compatibility**: Works through proxies and firewalls
- **Lower complexity**: No protocol upgrade needed
- **Event sourcing**: Natural fit for event-driven architectures

Key considerations:

- Use when bidirectional not needed
- Implement proper event IDs for reconnection
- Handle client disconnects gracefully
- Scale with Redis pub/sub
- Monitor connection metrics

## References & Learn More

- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
- [HTML5 SSE Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [SSE vs WebSockets](https://blog.dreamfactory.com/websockets-vs-server-sent-events/)
- [Node.js SSE Implementation](https://nodejs.org/en/docs/guides/getting-started-guide/)
