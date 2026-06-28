# Real-Time Architecture

## Definition

Real-time architecture is a **system design approach** that enables applications to process and deliver data with minimal latency, providing immediate updates to users as events occur. It encompasses patterns, protocols, and infrastructure for building responsive, event-driven systems.

Real-time systems prioritize **low latency, high availability, and horizontal scalability** to handle thousands or millions of concurrent connections while maintaining data consistency.

## Why Do We Need It?

| Traditional Architecture | Real-Time Architecture |
|---|---|
| Request-response only | Event-driven |
| Batch processing | Stream processing |
| High latency (100ms+) | Low latency (<10ms) |
| Polling for updates | Push-based updates |
| Synchronous communication | Asynchronous communication |
| Limited scalability | Horizontally scalable |

### Real-Time Use Cases

```
Chat Applications         -> WebSocket + Pub/Sub
Live Notifications        -> SSE + Message Queue
Multiplayer Games         -> WebSocket + State Sync
Collaborative Editing     -> CRDT + Operational Transform
Financial Tickers         -> WebSocket + Redis Streams
IoT Sensor Data           -> MQTT + Kafka
Live Dashboards           -> SSE + Time Series DB
Social Media Feeds        -> SSE + Fan-out
```

## How It Works

### Architecture Patterns

```
Pattern 1: Direct Connection
+--------+     +--------+     +--------+
| Client | --> | Server | --> | Client |
+--------+     +--------+     +--------+
Simple, but does not scale

Pattern 2: Pub/Sub
+--------+     +---------+     +---------+     +--------+
| Client | --> | Pub/Sub | --> | Broker  | --> | Client |
+--------+     +---------+     +---------+     +--------+
Scalable, decoupled

Pattern 3: Event Sourcing
+--------+     +---------+     +---------+     +---------+
| Client | --> | Event   | --> | Event   | --> | Read    |
|        |     | Store   |     | Handler |     | Model   |
+--------+     +---------+     +---------+     +---------+
Audit trail, temporal queries

Pattern 4: CQRS + Event Sourcing
+--------+     +---------+     +---------+
| Client | --> | Command | --> | Event   |
|        |     | Side    |     | Store   |
+--------+     +---------+     +---------+
                          |
+--------+     +---------+     +---------+
| Client | <-- | Query   | <-- | Event   |
|        |     | Side    |     | Handler |
+--------+     +---------+     +---------+
Optimized read/write models
```

### Scaling WebSockets

```
Single Server:
Client ---
Client ---|--- WebSocket Server --- Database
Client ---
Limited to ~10,000 connections

Load Balanced:
Client ---     +-- Server 1 --+
Client ---+----|              |--- Database
Client ---     +-- Server 2 --+
                    |
Client ---     +-- Server 3 --+
Client ---+----|              |--- Redis Pub/Sub
Client ---     +-- Server 4 --+
                    |
              Cross-server communication via Redis

Geographic Distribution:
                    +-- US East --+
Client (US) -------|             |--- Origin
                    +-------------+
                         |
                    +-- US West --+
Client (US) -------|             |--- Origin
                    +-------------+
                         |
                    +-- EU West --+
Client (EU) -------|             |--- Origin
                    +-------------+
              CDN/Edge for static, WebSocket for real-time
```

## Code Examples

### Pub/Sub with Redis

```typescript
import Redis from 'ioredis';

class RedisPubSub {
  private publisher: Redis;
  private subscriber: Redis;
  private handlers = new Map<string, Set<(message: string) => void>>();

  constructor(config: { host: string; port: number }) {
    this.publisher = new Redis(config);
    this.subscriber = new Redis(config);

    this.subscriber.on('message', (channel, message) => {
      const channelHandlers = this.handlers.get(channel);
      if (channelHandlers) {
        channelHandlers.forEach((handler) => handler(message));
      }
    });
  }

  subscribe(channel: string, handler: (message: string) => void): void {
    if (!this.handlers.has(channel)) {
      this.handlers.set(channel, new Set());
      this.subscriber.subscribe(channel);
    }
    this.handlers.get(channel)!.add(handler);
  }

  unsubscribe(channel: string, handler: (message: string) => void): void {
    this.handlers.get(channel)?.delete(handler);
    if (this.handlers.get(channel)?.size === 0) {
      this.handlers.delete(channel);
      this.subscriber.unsubscribe(channel);
    }
  }

  publish(channel: string, message: string): void {
    this.publisher.publish(channel, message);
  }

  async disconnect(): Promise<void> {
    await this.publisher.quit();
    await this.subscriber.quit();
  }
}

// Usage
const pubsub = new RedisPubSub({ host: 'localhost', port: 6379 });

pubsub.subscribe('chat:general', (message) => {
  const data = JSON.parse(message);
  console.log('Received:', data);
});

pubsub.publish('chat:general', JSON.stringify({ user: 'Alice', text: 'Hello!' }));
```

### WebSocket Server with Redis Scaling

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { createServer } from 'http';
import Redis from 'ioredis';

class ScalableWebSocketServer {
  private wss: WebSocketServer;
  private clients = new Map<string, WebSocket>();
  private redis: Redis;
  private pubsub: Redis;
  private nodeId: string;

  constructor(port: number) {
    this.nodeId = crypto.randomUUID();
    this.redis = new Redis();
    this.pubsub = new Redis();

    const server = createServer();
    this.wss = new WebSocketServer({ server });

    this.setupWebSocket();
    this.setupRedisPubSub();

    server.listen(port);
  }

  private setupWebSocket(): void {
    this.wss.on('connection', (ws) => {
      const clientId = crypto.randomUUID();
      this.clients.set(clientId, ws);

      this.redis.hset('clients', clientId, JSON.stringify({
        nodeId: this.nodeId,
        connectedAt: Date.now(),
      }));

      ws.on('message', (data) => {
        this.handleMessage(clientId, data.toString());
      });

      ws.on('close', () => {
        this.clients.delete(clientId);
        this.redis.hdel('clients', clientId);
      });
    });
  }

  private setupRedisPubSub(): void {
    this.pubsub.subscribe('broadcast', 'user:', 'room:');

    this.pubsub.on('message', (channel, message) => {
      const data = JSON.parse(message);

      if (channel === 'broadcast') {
        this.broadcast(data);
      } else if (channel.startsWith('user:')) {
        const userId = channel.split(':')[1];
        this.sendToUser(userId, data);
      } else if (channel.startsWith('room:')) {
        const roomId = channel.split(':')[1];
        this.sendToRoom(roomId, data);
      }
    });
  }

  private handleMessage(clientId: string, data: string): void {
    const message = JSON.parse(data);

    switch (message.type) {
      case 'broadcast':
        this.redis.publish('broadcast', JSON.stringify(message));
        break;
      case 'user':
        this.redis.publish(`user:${message.userId}`, JSON.stringify(message));
        break;
      case 'room':
        this.redis.publish(`room:${message.roomId}`, JSON.stringify(message));
        break;
    }
  }

  private broadcast(data: unknown): void {
    this.clients.forEach((ws) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
      }
    });
  }

  private sendToUser(userId: string, data: unknown): void {
    const ws = this.clients.get(userId);
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data));
    }
  }

  private sendToRoom(roomId: string, data: unknown): void {
    this.redis.smembers(`room:${roomId}`).then((members) => {
      members.forEach((memberId) => {
        this.sendToUser(memberId, data);
      });
    });
  }
}
```

### Message Queue with Kafka

```typescript
import { Kafka, Producer, Consumer, EachMessagePayload } from 'kafkajs';

class KafkaMessageQueue {
  private kafka: Kafka;
  private producer: Producer;
  private consumers = new Map<string, Consumer>();

  constructor(config: { clientId: string; brokers: string[] }) {
    this.kafka = new Kafka({
      clientId: config.clientId,
      brokers: config.brokers,
    });
    this.producer = this.kafka.producer();
  }

  async connect(): Promise<void> {
    await this.producer.connect();
  }

  async produce(topic: string, message: unknown): Promise<void> {
    await this.producer.send({
      topic,
      messages: [
        {
          key: crypto.randomUUID(),
          value: JSON.stringify(message),
          timestamp: Date.now().toString(),
        },
      ],
    });
  }

  async consume(
    topic: string,
    groupId: string,
    handler: (message: EachMessagePayload) => Promise<void>
  ): Promise<void> {
    const consumer = this.kafka.consumer({ groupId });
    await consumer.connect();
    await consumer.subscribe({ topic, fromBeginning: false });

    await consumer.run({ eachMessage: handler });

    this.consumers.set(`${topic}:${groupId}`, consumer);
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
    for (const consumer of this.consumers.values()) {
      await consumer.disconnect();
    }
  }
}

// Usage
const kafka = new KafkaMessageQueue({
  clientId: 'my-app',
  brokers: ['localhost:9092'],
});

await kafka.connect();

await kafka.produce('chat-messages', {
  userId: 'user123',
  text: 'Hello!',
  timestamp: Date.now(),
});

await kafka.consume('chat-messages', 'chat-group', async ({ message }) => {
  const data = JSON.parse(message.value!.toString());
  console.log('Received:', data);
});
```

### Event Sourcing

```typescript
interface Event {
  id: string;
  type: string;
  aggregateId: string;
  data: unknown;
  metadata: {
    userId: string;
    timestamp: number;
    version: number;
  };
}

class EventStore {
  private events: Event[] = [];
  private snapshots = new Map<string, { version: number; state: unknown }>();

  async append(event: Event): Promise<void> {
    this.events.push(event);

    const aggregateEvents = this.events.filter(
      (e) => e.aggregateId === event.aggregateId
    );
    if (aggregateEvents.length % 100 === 0) {
      await this.createSnapshot(event.aggregateId);
    }
  }

  async getEvents(aggregateId: string, afterVersion?: number): Promise<Event[]> {
    return this.events.filter(
      (e) =>
        e.aggregateId === aggregateId &&
        (!afterVersion || e.metadata.version > afterVersion)
    );
  }

  async getState(aggregateId: string): Promise<unknown> {
    const snapshot = this.snapshots.get(aggregateId);
    const afterVersion = snapshot?.version || 0;
    const events = await this.getEvents(aggregateId, afterVersion);

    let state = snapshot?.state || {};
    for (const event of events) {
      state = this.applyEvent(state, event);
    }
    return state;
  }

  private async createSnapshot(aggregateId: string): Promise<void> {
    const state = await this.getState(aggregateId);
    const version = this.events.filter(
      (e) => e.aggregateId === aggregateId
    ).length;
    this.snapshots.set(aggregateId, { version, state });
  }

  private applyEvent(state: unknown, event: Event): unknown {
    switch (event.type) {
      case 'UserCreated':
        return { ...state, id: event.data.id, name: event.data.name };
      case 'UserUpdated':
        return { ...state, ...event.data };
      default:
        return state;
    }
  }
}
```

### CQRS Pattern

```typescript
// Command Side
class CommandHandler {
  constructor(private eventStore: EventStore) {}

  async createUser(command: { id: string; name: string; email: string; userId: string }): Promise<void> {
    const event: Event = {
      id: crypto.randomUUID(),
      type: 'UserCreated',
      aggregateId: command.id,
      data: {
        id: command.id,
        name: command.name,
        email: command.email,
      },
      metadata: {
        userId: command.userId,
        timestamp: Date.now(),
        version: 1,
      },
    };

    await this.eventStore.append(event);
  }

  async updateUser(command: { id: string; changes: Record<string, unknown>; userId: string }): Promise<void> {
    const currentState = await this.eventStore.getState(command.id) as { version: number };
    const newVersion = currentState.version + 1;

    const event: Event = {
      id: crypto.randomUUID(),
      type: 'UserUpdated',
      aggregateId: command.id,
      data: command.changes,
      metadata: {
        userId: command.userId,
        timestamp: Date.now(),
        version: newVersion,
      },
    };

    await this.eventStore.append(event);
  }
}

// Query Side
class QueryHandler {
  private readModel = new Map<string, Record<string, unknown>>();

  constructor(private eventStore: EventStore) {
    this.buildReadModel();
  }

  private async buildReadModel(): Promise<void> {
    // Rebuild read model from events
  }

  async getUser(id: string): Promise<Record<string, unknown> | null> {
    return this.readModel.get(id) || null;
  }

  async searchUsers(query: string): Promise<Record<string, unknown>[]> {
    return Array.from(this.readModel.values()).filter(
      (user) =>
        (user.name as string)?.toLowerCase().includes(query.toLowerCase()) ||
        (user.email as string)?.toLowerCase().includes(query.toLowerCase())
    );
  }
}
```

### Redis Streams for Real-Time

```typescript
import Redis from 'ioredis';

class RedisStreamConsumer {
  private redis: Redis;
  private consumerGroup: string;
  private consumerId: string;

  constructor(config: { host: string; port: number }) {
    this.redis = new Redis(config);
    this.consumerGroup = 'my-group';
    this.consumerId = `consumer-${crypto.randomUUID()}`;
  }

  async createGroup(stream: string): Promise<void> {
    try {
      await this.redis.xgroup('CREATE', stream, this.consumerGroup, '0', 'MKSTREAM');
    } catch (error) {
      // Group already exists
    }
  }

  async produce(stream: string, data: Record<string, string>): Promise<string> {
    const entries: string[] = [];
    for (const [key, value] of Object.entries(data)) {
      entries.push(key, value);
    }
    return await this.redis.xadd(stream, '*', ...entries);
  }

  async consume(
    stream: string,
    handler: (id: string, data: Record<string, string>) => Promise<void>
  ): Promise<void> {
    while (true) {
      try {
        const results = await this.redis.xreadgroup(
          'GROUP',
          this.consumerGroup,
          this.consumerId,
          'COUNT',
          10,
          'BLOCK',
          5000,
          'STREAMS',
          stream,
          '>'
        );

        if (!results) continue;

        for (const [, messages] of results) {
          for (const [id, fields] of messages) {
            const data: Record<string, string> = {};
            for (let i = 0; i < fields.length; i += 2) {
              data[fields[i]] = fields[i + 1];
            }
            await handler(id, data);
            await this.redis.xack(stream, this.consumerGroup, id);
          }
        }
      } catch (error) {
        console.error('Consumer error:', error);
        await this.delay(1000);
      }
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
```

## Real-World Use Cases

### 1. Chat Application Architecture

```typescript
// Multi-server chat with Redis Pub/Sub
class ChatArchitecture {
  private redis: Redis;
  private wss: WebSocketServer;

  constructor() {
    this.redis = new Redis();
    this.setupWebSocket();
    this.setupPubSub();
  }

  private setupWebSocket(): void {
    this.wss.on('connection', (socket) => {
      socket.on('join-room', (roomId) => {
        socket.join(roomId);
        this.redis.sadd(`room:${roomId}`, socket.id);
      });

      socket.on('message', (data) => {
        // Publish to Redis for cross-server delivery
        this.redis.publish('chat:message', JSON.stringify({
          roomId: data.roomId,
          message: data.message,
          userId: socket.handshake.auth.userId,
        }));
      });
    });
  }

  private setupPubSub(): void {
    const subscriber = new Redis();
    subscriber.subscribe('chat:message');

    subscriber.on('message', (channel, message) => {
      if (channel === 'chat:message') {
        const data = JSON.parse(message);
        this.wss.to(data.roomId).emit('new-message', data);
      }
    });
  }
}
```

### 2. Live Notification System

```typescript
// Fan-out notification system
class NotificationSystem {
  private redis: Redis;
  private userSubscriptions = new Map<string, Set<string>>();

  constructor() {
    this.redis = new Redis();
  }

  async subscribe(userId: string, topics: string[]): Promise<void> {
    for (const topic of topics) {
      await this.redis.sadd(`topic:${topic}`, userId);
      if (!this.userSubscriptions.has(userId)) {
        this.userSubscriptions.set(userId, new Set());
      }
      this.userSubscriptions.get(userId)!.add(topic);
    }
  }

  async publish(topic: string, notification: unknown): Promise<void> {
    const subscribers = await this.redis.smembers(`topic:${topic}`);
    for (const userId of subscribers) {
      await this.redis.lpush(`notifications:${userId}`, JSON.stringify(notification));
      await this.redis.publish(`user:${userId}`, JSON.stringify(notification));
    }
  }
}
```

### 3. Real-Time Analytics Dashboard

```typescript
// Real-time metrics streaming
class AnalyticsDashboard {
  private redis: Redis;
  private metricsBuffer = new Map<string, number[]>();

  constructor() {
    this.redis = new Redis();
    this.startAggregation();
  }

  async recordMetric(name: string, value: number): Promise<void> {
    await this.redis.xadd('metrics:stream', '*', 'name', name, 'value', value.toString());
  }

  private startAggregation(): void {
    setInterval(async () => {
      const metrics = await this.getLatestMetrics();
      this.redis.publish('analytics:update', JSON.stringify(metrics));
    }, 1000);
  }

  private async getLatestMetrics(): Promise<Record<string, number>> {
    const result = await this.redis.xrevrange('metrics:stream', '+', '-', 'COUNT', 100);
    const metrics: Record<string, number> = {};

    for (const [, fields] of result) {
      const name = fields[1];
      const value = parseFloat(fields[3]);
      metrics[name] = (metrics[name] || 0) + value;
    }

    return metrics;
  }
}
```

## Common Mistakes

### 1. Not Using Message Queues for Scale

```typescript
// ❌ Bad: Direct database writes in real-time handlers
socket.on('message', async (data) => {
  await db.messages.insert(data); // Blocks, doesn't scale
  io.to(data.roomId).emit('new-message', data);
});

// ✅ Good: Use message queue for durability
socket.on('message', async (data) => {
  await messageQueue.publish('chat:message', data); // Non-blocking
  io.to(data.roomId).emit('new-message', data);
});
```

### 2. Not Handling Message Ordering

```typescript
// ❌ Bad: No ordering guarantee
socket.on('update', (data) => {
  redis.publish('updates', JSON.stringify(data));
});

// ✅ Good: Use sequence numbers
let sequence = 0;
socket.on('update', (data) => {
  redis.publish('updates', JSON.stringify({
    ...data,
    sequence: ++sequence,
    timestamp: Date.now(),
  }));
});
```

### 3. Not Implementing Dead Letter Queues

```typescript
// ❌ Bad: Messages lost on failure
consumer.consume('orders', async (message) => {
  await processOrder(message); // If fails, message is lost
  await consumer.ack(message);
});

// ✅ Good: Dead letter queue for failed messages
consumer.consume('orders', async (message) => {
  try {
    await processOrder(message);
    await consumer.ack(message);
  } catch (error) {
    await deadLetterQueue.publish('orders:failed', {
      original: message,
      error: error.message,
      timestamp: Date.now(),
    });
    await consumer.ack(message);
  }
});
```

## Best Practices

### 1. Use Event Sourcing for Audit Trails

```typescript
// Every state change is recorded as an event
class AuditableService {
  constructor(private eventStore: EventStore) {}

  async changeState(aggregateId: string, newState: unknown, userId: string): Promise<void> {
    const event: Event = {
      id: crypto.randomUUID(),
      type: 'StateChanged',
      aggregateId,
      data: newState,
      metadata: {
        userId,
        timestamp: Date.now(),
        version: await this.getNextVersion(aggregateId),
      },
    };

    await this.eventStore.append(event);
  }
}
```

### 2. Implement Circuit Breakers

```typescript
// Prevent cascade failures
class CircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure(): void {
    this.failures++;
    this.lastFailure = Date.now();
    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}
```

### 3. Use Consistent Hashing for Distribution

```typescript
import { createHash } from 'crypto';

class ConsistentHash<T> {
  private ring = new Map<number, T>();
  private sortedKeys: number[] = [];
  private virtualNodes = 150;

  addNode(node: T): void {
    for (let i = 0; i < this.virtualNodes; i++) {
      const hash = this.hash(`${node}:${i}`);
      this.ring.set(hash, node);
      this.sortedKeys.push(hash);
    }
    this.sortedKeys.sort((a, b) => a - b);
  }

  getNode(key: string): T {
    const hash = this.hash(key);
    const index = this.sortedKeys.findIndex((k) => k >= hash);
    const nodeIndex = index === -1 ? 0 : index;
    return this.ring.get(this.sortedKeys[nodeIndex])!;
  }

  private hash(key: string): number {
    return createHash('md5').update(key).digest('hex').slice(0, 8);
  }
}
```

## Performance Considerations

### Throughput Comparison

```
Message Broker Throughput (messages/sec):
- Redis Pub/Sub: 100,000-500,000
- Kafka: 100,000-2,000,000
- RabbitMQ: 20,000-50,000
- NATS: 100,000-1,000,000
```

### Latency Comparison

```
End-to-End Latency:
- Redis Pub/Sub: 1-5ms
- Kafka: 5-15ms
- RabbitMQ: 1-10ms
- NATS: 1-5ms
```

### Memory Usage

```
Per Connection Memory:
- WebSocket: 0.5-2 KB
- SSE: 1-2 KB
- HTTP Long Polling: 2-8 KB
```

## Interview Questions

### Beginner (5)

1. **What is pub/sub and why use it?**
   - Publish-subscribe pattern for decoupled communication
   - Producers don't know about consumers
   - Enables horizontal scaling
   - Message brokers handle routing

2. **What is event sourcing?**
   - Store state changes as events
   - Rebuild state by replaying events
   - Provides complete audit trail
   - Enables temporal queries

3. **What is CQRS?**
   - Command Query Responsibility Segregation
   - Separate read and write models
   - Optimize each model independently
   - Often combined with event sourcing

4. **How do you scale WebSockets?**
   - Use Redis Pub/Sub for cross-server communication
   - Implement sticky sessions
   - Use message brokers for durability
   - Consider geographic distribution

5. **What is a message broker?**
   - Middleware for async communication
   - Decouples producers and consumers
   - Provides message persistence
   - Handles routing and delivery

### Intermediate (5-8)

6. **How do you handle message ordering?**
   - Use sequence numbers
   - Implement vector clocks
   - Use single-partition topics
   - Consider CRDTs for conflicts

7. **What is backpressure?**
   - Consumer can't keep up with producer
   - Monitor queue depths
   - Implement flow control
   - Use bounded queues

8. **How do you handle failures?**
   - Dead letter queues
   - Retry with exponential backoff
   - Circuit breakers
   - Idempotent operations

9. **What is message durability?**
   - Persist messages to disk
   - Replicate across nodes
   - Acknowledgment-based delivery
   - Recovery after crashes

10. **How do you monitor real-time systems?**
    - Track message rates
    - Monitor queue depths
    - Alert on latency spikes
    - Dashboard for visibility

### Senior (8-12)

11. **Design a chat system for 10M users**
    - Connection management with consistent hashing
    - Message fanout via Redis Pub/Sub
    - Presence service with heartbeat
    - Message storage with Cassandra
    - CDN for media delivery

12. **How do you handle exactly-once delivery?**
    - Idempotent operations
    - Deduplication at consumer
    - Transactional outbox pattern
    - Consider trade-offs (at-least-once vs exactly-once)

13. **How do you implement event replay?**
    - Event store with versioning
    - Snapshot and replay
    -投影 rebuild
    - Time-travel debugging

14. **How do you handle distributed transactions?**
    - Saga pattern
    - Two-phase commit
    - Event sourcing
    - Consider eventual consistency

15. **How do you optimize for high throughput?**
    - Batch processing
    - Message compression
    - Partitioning strategies
    - Connection pooling

### FAANG-style (5-8)

16. **Design a real-time collaboration system**
    - CRDT or OT for conflict resolution
    - Cursor presence and awareness
    - Version history and undo
    - Offline support and sync
    - Scaling to millions of users

17. **Design a live auction platform**
    - Real-time bidding with WebSocket
    - Timer management and extensions
    - Fraud detection
    - Winner notification
    - Payment integration

18. **Design a multiplayer game backend**
    - Deterministic game loop
    - State synchronization
    - Client-side prediction
    - Lag compensation
    - Anti-cheat measures

19. **Design a live monitoring dashboard**
    - Real-time metrics streaming
    - Data aggregation and filtering
    - Alert management
    - Historical data viewing
    - Export and sharing

20. **Design a stock trading platform**
    - Real-time price updates
    - Order matching engine
    - Risk management
    - Regulatory compliance
    - High availability

### Follow-ups (5-8)

21. **How do you test real-time systems?**
    - Load testing with tools like Artillery
    - Chaos engineering for failures
    - Integration tests with mock brokers
    - Monitoring and alerting

22. **How do you handle real-time data in microservices?**
    - Event-driven architecture
    - API gateway for WebSocket routing
    - Service discovery
    - Distributed tracing

23. **What are common pitfalls?**
    - Not handling backpressure
    - Missing dead letter queues
    - No circuit breakers
    - Ignoring message ordering
    - Not testing failure scenarios

24. **How do you secure real-time systems?**
    - Authentication and authorization
    - Rate limiting
    - Input validation
    - Encryption in transit
    - Audit logging

25. **How do you migrate to real-time architecture?**
    - Start with notifications
    - Add WebSocket for chat
    - Implement event sourcing
    - Gradually replace polling

## Summary

Real-time architecture encompasses:

- **Pub/Sub Pattern**: Decoupled, scalable communication
- **Event Sourcing**: Complete audit trail, temporal queries
- **CQRS**: Optimized read/write models
- **Message Brokers**: Kafka, Redis, RabbitMQ for durability
- **Scaling**: Consistent hashing, Redis Pub/Sub, geographic distribution

Key considerations:
- Choose the right pattern for your use case
- Handle failures gracefully with dead letter queues
- Monitor everything (latency, throughput, errors)
- Test thoroughly (load, chaos, integration)
- Scale horizontally with Redis and message brokers

## References & Learn More

- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Building Microservices](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/)
- [Real-Time Web Application Architecture](https://martinfowler.com/articles/2022-real-time-web-architecture.html)
- [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS](https://martinfowler.com/bliki/CQRS.html)
- [The Log: What every software engineer should know](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)
