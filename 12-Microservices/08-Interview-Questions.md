# Microservices Interview Questions

## Definition

This comprehensive guide covers 30+ most frequently asked microservices interview questions, categorized by difficulty level. Each question includes detailed answers, code examples, and follow-up questions to help you ace your senior full-stack developer interview.

## Why Do We Need It?

Microservices architecture is widely adopted in modern software development. Understanding these concepts is essential for senior developer roles at top tech companies. These questions test your understanding of distributed systems, system design, and architectural patterns.

## How It Works

### Question Categories

```text
┌─────────────────────────────────────────────────────────────────┐
│              MICROSERVICES INTERVIEW QUESTIONS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BEGINNER (5-10)                                               │
│  └── Foundational concepts, definitions, basic understanding   │
│                                                                 │
│  INTERMEDIATE (5-10)                                           │
│  └── Implementation details, trade-offs, patterns              │
│                                                                 │
│  SENIOR (10-15)                                                │
│  └── System design, architecture decisions, complex scenarios   │
│                                                                 │
│  FAANG-STYLE (5-10)                                            │
│  └── Large-scale systems, real-world problems, optimization    │
│                                                                 │
│  FOLLOW-UPS (5-10)                                             │
│  └── Deep dives, edge cases, advanced topics                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Beginner Questions

#### Q1: What is microservices architecture?

**Answer:**
Microservices architecture is an architectural style that structures an application as a collection of loosely coupled, independently deployable services. Each service is self-contained, implements a specific business capability, and communicates with other services through well-defined APIs.

```text
MONOLITHIC ARCHITECTURE:
┌─────────────────────────────────────────┐
│              APPLICATION                │
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │  User   │ │ Product │ │  Order  │  │
│  │ Module  │ │ Module  │ │ Module  │  │
│  └────┬────┘ └────┬────┘ └────┬────┘  │
│       │           │           │        │
│       └───────────┼───────────┘        │
│                   │                    │
│            ┌──────┴──────┐             │
│            │  Database   │             │
│            └─────────────┘             │
└─────────────────────────────────────────┘

MICROSERVICES ARCHITECTURE:
┌──────────┐  ┌──────────┐  ┌──────────┐
│  User    │  │ Product  │  │  Order   │
│ Service  │  │ Service  │  │ Service  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ User DB │  │Product  │  │ Order   │
│         │  │  DB     │  │  DB     │
└─────────┘  └─────────┘  └─────────┘

```

**Follow-up:** What are the benefits and drawbacks?

#### Q2: How do microservices communicate?

**Answer:**
Microservices communicate through two primary patterns:

1. **Synchronous Communication** (HTTP/REST, gRPC)

   - Request/response model
   - Direct service-to-service calls
   - Examples: REST API calls, gRPC streams

2. **Asynchronous Communication** (Message Queues, Events)

   - Event-driven architecture
   - Decoupled services
   - Examples: Kafka, RabbitMQ, AWS SQS

```typescript
// Synchronous Communication (REST)
class UserServiceClient {
  async getUser(userId: string): Promise<User> {
    const response = await fetch(`http://user-service/users/${userId}`);
    return response.json();
  }
}

// Asynchronous Communication (Event-driven)
class OrderService {
  async createOrder(order: Order): Promise<void> {
    // Save order
    await this.orderRepository.save(order);

    // Publish event (async, non-blocking)
    await this.eventBus.publish('order.created', {
      orderId: order.id,
      userId: order.userId,
      items: order.items,
    });
  }
}

```

#### Q3: What is service discovery?

**Answer:**
Service discovery is a mechanism that allows services to find and communicate with each other dynamically. Instead of hardcoding network locations, services register with a discovery server and look up other services through it.

```typescript
// Client-side discovery
class ServiceDiscoveryClient {
  constructor(private registry: ServiceRegistry) {}

  async getService(serviceName: string): Promise<ServiceInstance> {
    const instances = await this.registry.getInstances(serviceName);

    // Load balancing (round-robin, random, weighted)
    return this.selectInstance(instances);
  }

  private selectInstance(instances: ServiceInstance[]): ServiceInstance {
    // Round-robin selection
    return instances[Math.floor(Math.random() * instances.length)];
  }
}

```

#### Q4: What is an API Gateway?

**Answer:**
An API Gateway is a server that acts as a single entry point for all client requests. It handles cross-cutting concerns like routing, authentication, rate limiting, and request transformation.

```typescript
// API Gateway pattern
const gateway = express();

// Authentication middleware
gateway.use('/api', authenticate);

// Rate limiting
gateway.use('/api', rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

// Route to services
gateway.use('/api/users', createProxyMiddleware({ target: 'http://user-service:3001' }));
gateway.use('/api/products', createProxyMiddleware({ target: 'http://product-service:3002' }));
gateway.use('/api/orders', createProxyMiddleware({ target: 'http://order-service:3003' }));

```

#### Q5: What is the difference between synchronous and asynchronous communication?

**Answer:**

| Aspect | Synchronous | Asynchronous |
|--------|-------------|--------------|
| Coupling | Tight | Loose |
| Timeout | Immediate | Deferred |
| Throughput | Lower | Higher |
| Complexity | Simpler | More complex |
| Use Case | Real-time queries | Event processing |

```typescript
// Synchronous: Direct call, waits for response
const user = await httpClient.get('/users/123');

// Asynchronous: Fire and forget, process later
await messageQueue.publish('user-events', { type: 'USER_CREATED', data: user });

```

### Intermediate Questions

#### Q6: What is the Saga pattern?

**Answer:**
The Saga pattern manages distributed transactions across multiple services. Instead of a single ACID transaction, sagas use a sequence of local transactions with compensating transactions for rollback.

```typescript
class OrderSaga {
  async execute(order: Order): Promise<void> {
    try {
      // Step 1: Create order
      await this.orderService.create(order);

      // Step 2: Reserve inventory
      await this.inventoryService.reserve(order.items);

      // Step 3: Process payment
      await this.paymentService.charge(order.userId, order.total);

      // Step 4: Confirm order
      await this.orderService.confirm(order.id);

    } catch (error) {
      // Compensate: Undo previous steps
      await this.compensate(order);
    }
  }

  private async compensate(order: Order): Promise<void> {
    await this.paymentService.refund(order.userId, order.total);
    await this.inventoryService.release(order.items);
    await this.orderService.cancel(order.id);
  }
}

```

#### Q7: What is the Circuit Breaker pattern?

**Answer:**
Circuit Breaker prevents cascade failures by stopping requests to failing services. It has three states: CLOSED (normal), OPEN (failing), and HALF-OPEN (testing recovery).

```typescript
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime = 0;

  async call<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > 30000) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= 5) {
      this.state = 'OPEN';
    }
  }
}

```

#### Q8: What is event sourcing?

**Answer:**
Event Sourcing stores all changes as a sequence of events. Instead of storing current state, you store events that led to that state. Current state is derived by replaying events.

```typescript
// Event Store
class EventStore {
  private events: Event[] = [];

  append(event: Event): void {
    this.events.push(event);
  }

  getEvents(aggregateId: string): Event[] {
    return this.events.filter(e => e.aggregateId === aggregateId);
  }

  // Rebuild state from events
  getState(aggregateId: string): any {
    return this.getEvents(aggregateId).reduce(
      (state, event) => this.applyEvent(state, event),
      {}
    );
  }
}

// Example events
const events = [
  { type: 'OrderCreated', data: { id: '123', userId: 'user1' } },
  { type: 'ItemAdded', data: { productId: 'prod1', quantity: 2 } },
  { type: 'PaymentReceived', data: { amount: 100 } },
  { type: 'OrderShipped', data: { trackingNumber: '123456' } },
];

```

#### Q9: What is CQRS?

**Answer:**
Command Query Responsibility Segregation (CQRS) separates read and write operations into different models. Write model handles commands, read model handles queries, optimized independently.

```typescript
// Command Side (Write)
class OrderCommandHandler {
  async createOrder(command: CreateOrderCommand): Promise<void> {
    // Validate, apply business rules
    const order = Order.create(command);
    await this.orderRepository.save(order);

    // Publish event for read model
    await this.eventBus.publish('OrderCreated', order);
  }
}

// Query Side (Read)
class OrderQueryHandler {
  async getOrder(orderId: string): Promise<OrderView> {
    // Optimized read from projection
    return this.orderViewRepository.findById(orderId);
  }
}

```

#### Q10: How do you handle distributed transactions?

**Answer:**
Distributed transactions are handled through:

1. **Saga Pattern** - Compensating transactions

2. **Eventual Consistency** - Accept temporary inconsistency

3. **Two-Phase Commit (2PC)** - Distributed locks (rarely used)

4. **Outbox Pattern** - Reliable event publishing

```typescript
// Outbox Pattern
class OrderService {
  async createOrder(order: Order): Promise<void> {
    await this.database.transaction(async (trx) => {
      // Save order
      await trx('orders').insert(order);

      // Save event to outbox (same transaction)
      await trx('outbox').insert({
        aggregateId: order.id,
        eventType: 'OrderCreated',
        payload: JSON.stringify(order),
      });
    });

    // Separate process publishes events from outbox
  }
}

```

### Senior Questions

#### Q11: How would you design a microservices system for an e-commerce platform?

**Answer:**

```text
┌─────────────────────────────────────────────────────────────────┐
│                  E-COMMERCE MICROSERVICES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │   API       │    │   User      │    │   Product   │        │
│   │   Gateway   │────│   Service   │    │   Service   │        │
│   └─────────────┘    └─────────────┘    └─────────────┘        │
│          │                  │                  │                 │
│          │                  │                  │                 │
│   ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐        │
│   │   Order     │   │  Inventory  │   │   Search    │        │
│   │   Service   │   │   Service   │   │   Service   │        │
│   └─────────────┘   └─────────────┘   └─────────────┘        │
│          │                  │                  │                 │
│          │                  │                  │                 │
│   ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐        │
│   │  Payment    │   │  Shipping   │   │  Analytics  │        │
│   │  Service    │   │  Service    │   │  Service    │        │
│   └─────────────┘   └─────────────┘   └─────────────┘        │
│                                                                 │
│   MESSAGE BROKER (Kafka/RabbitMQ)                              │
│   └── Event-driven communication between services              │
└─────────────────────────────────────────────────────────────────┘

```

**Key decisions:**

- API Gateway for client simplification
- Event-driven communication for loose coupling
- Database per service for independence
- Saga pattern for distributed transactions
- CQRS for read/write optimization

#### Q12: How do you handle service failures in microservices?

**Answer:**
Multi-layered approach:

```typescript
// 1. Circuit Breaker
const circuitBreaker = new CircuitBreaker({
  failureThreshold: 5,
  timeout: 30000,
});

// 2. Retry with Backoff
const retry = new Retry({
  maxRetries: 3,
  backoff: 'exponential',
});

// 3. Fallback
async function getUserWithFallback(userId: string): Promise<User> {
  try {
    return await circuitBreaker.execute(() =>
      retry.execute(() => userService.getUser(userId))
    );
  } catch (error) {
    // Fallback to cached data or default
    return cache.get(`user:${userId}`) || defaultUser;
  }
}

// 4. Bulkheading
const userPool = new Pool({ max: 10 });
const orderPool = new Pool({ max: 20 });
// Isolate failures to specific services

```

#### Q13: How do you implement distributed tracing?

**Answer:**
Using OpenTelemetry for distributed tracing:

```typescript
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';

// Initialize tracer
const provider = new NodeTracerProvider();
const exporter = new JaegerExporter();
provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register();

// Instrument HTTP calls
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
new HttpInstrumentation().instrument();

// Custom spans
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

async function processOrder(orderId: string): Promise<void> {
  const span = tracer.startSpan('processOrder');
  try {
    span.setAttribute('order.id', orderId);

    // Your business logic
    await validateOrder(orderId);
    await processPayment(orderId);

    span.setStatus({ code: SpanStatusCode.OK });
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    throw error;
  } finally {
    span.end();
  }
}

```

#### Q14: How do you ensure data consistency across services?

**Answer:**
Strategies for data consistency:

```typescript
// 1. Eventual Consistency with Events
class OrderService {
  async createOrder(order: Order): Promise<void> {
    // Save locally
    await this.orderRepository.save(order);

    // Publish event (async)
    await this.eventBus.publish('OrderCreated', {
      orderId: order.id,
      userId: order.userId,
    });
  }
}

// 2. Saga Pattern for Strong Consistency
class OrderSaga {
  async execute(order: Order): Promise<void> {
    await this.orderService.create(order);
    await this.inventoryService.reserve(order.items);
    await this.paymentService.charge(order.userId, order.total);
  }

  async compensate(order: Order): Promise<void> {
    await this.paymentService.refund(order.userId, order.total);
    await this.inventoryService.release(order.items);
    await this.orderService.cancel(order.id);
  }
}

// 3. Outbox Pattern for Reliable Events
class OrderService {
  async createOrder(order: Order): Promise<void> {
    await this.database.transaction(async (trx) => {
      await trx('orders').insert(order);
      await trx('outbox').insert({
        aggregateId: order.id,
        eventType: 'OrderCreated',
        payload: JSON.stringify(order),
      });
    });
  }
}

```

#### Q15: How do you handle database per service pattern?

**Answer:**

```typescript
// Each service has its own database
// No direct database access across services

// User Service
class UserService {
  constructor(private userDatabase: Database) {}

  async getUser(userId: string): Promise<User> {
    return this.userDatabase.query('SELECT * FROM users WHERE id = ?', [userId]);
  }
}

// Order Service (cannot access User database)
class OrderService {
  constructor(
    private orderDatabase: Database,
    private userClient: UserServiceClient  // HTTP/gRPC client
  ) {}

  async createOrder(order: Order): Promise<void> {
    // Must call User Service to get user data
    const user = await this.userClient.getUser(order.userId);

    // Save order with user reference (not user data)
    await this.orderDatabase.query(
      'INSERT INTO orders (id, user_id, total) VALUES (?, ?, ?)',
      [order.id, user.id, order.total]
    );
  }
}

// API Composition for queries spanning services
class OrderQueryService {
  async getOrderDetails(orderId: string): Promise<any> {
    const order = await this.orderClient.getOrder(orderId);
    const user = await this.userClient.getUser(order.userId);
    const products = await this.productClient.getProducts(order.itemIds);

    return { ...order, user, products };
  }
}

```

### FAANG-Style Questions

#### Q16: Design a URL shortener like bit.ly

**Answer:**

```text
┌─────────────────────────────────────────────────────────────────┐
│                    URL SHORTENER DESIGN                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Client ──> API Gateway ──> URL Service ──> Database            │
│              │                    │                              │
│              │                    ├──> Cache (Redis)             │
│              │                    │                              │
│              └──> Analytics Service                             │
│                                                                 │
│   Key Components:                                               │
│   • URL Encoding: Base62 (a-z, A-Z, 0-9)                       │
│   • Storage: Database with short_url, long_url, created_at      │
│   • Cache: Redis for hot URLs                                    │
│   • Analytics: Track clicks, referrers                          │
└─────────────────────────────────────────────────────────────────┘

```

```typescript
// URL Service
class UrlService {
  async createShortUrl(longUrl: string): Promise<string> {
    // Generate unique short code
    const shortCode = this.generateShortCode();

    // Store in database
    await this.database.query(
      'INSERT INTO urls (short_code, long_url, created_at) VALUES (?, ?, ?)',
      [shortCode, longUrl, new Date()]
    );

    // Cache for fast lookup
    await this.cache.set(`url:${shortCode}`, longUrl, 'EX', 86400);

    return `https://short.ly/${shortCode}`;
  }

  async getLongUrl(shortCode: string): Promise<string> {
    // Check cache first
    const cached = await this.cache.get(`url:${shortCode}`);
    if (cached) return cached;

    // Fallback to database
    const result = await this.database.query(
      'SELECT long_url FROM urls WHERE short_code = ?',
      [shortCode]
    );

    if (result.length === 0) {
      throw new NotFoundError('URL not found');
    }

    const longUrl = result[0].long_url;
    await this.cache.set(`url:${shortCode}`, longUrl, 'EX', 86400);

    return longUrl;
  }

  private generateShortCode(): string {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 7; i++) {
      code += chars[Math.floor(Math.random() * chars.length)];
    }
    return code;
  }
}

```

#### Q17: Design a real-time chat application

**Answer:**

```typescript
// WebSocket Gateway
class ChatGateway {
  private clients: Map<string, WebSocket> = new Map();

  handleConnection(socket: WebSocket, userId: string): void {
    this.clients.set(userId, socket);

    socket.on('message', async (data) => {
      const message = JSON.parse(data);

      // Save message to database
      await this.messageService.save(message);

      // Broadcast to room
      this.broadcastToRoom(message.roomId, {
        type: 'MESSAGE',
        data: message,
      });

      // Publish to message broker for other services
      await this.eventBus.publish('chat.message', message);
    });

    socket.on('close', () => {
      this.clients.delete(userId);
    });
  }

  broadcastToRoom(roomId: string, message: any): void {
    // Get room members
    const members = this.roomService.getMembers(roomId);

    members.forEach(memberId => {
      const client = this.clients.get(memberId);
      if (client) {
        client.send(JSON.stringify(message));
      }
    });
  }
}

// Message Service
class MessageService {
  async save(message: Message): Promise<void> {
    await this.database.query(
      'INSERT INTO messages (id, room_id, user_id, content, created_at) VALUES (?, ?, ?, ?, ?)',
      [message.id, message.roomId, message.userId, message.content, new Date()]
    );
  }

  async getMessages(roomId: string, limit: number = 50): Promise<Message[]> {
    return this.database.query(
      'SELECT * FROM messages WHERE room_id = ? ORDER BY created_at DESC LIMIT ?',
      [roomId, limit]
    );
  }
}

```

#### Q18: Design a notification system

**Answer:**

```typescript
// Notification Service
class NotificationService {
  async send(notification: Notification): Promise<void> {
    // Save notification
    await this.notificationRepository.save(notification);

    // Route to appropriate channel
    switch (notification.channel) {
      case 'email':
        await this.emailService.send(notification);
        break;
      case 'sms':
        await this.smsService.send(notification);
        break;
      case 'push':
        await this.pushService.send(notification);
        break;
      case 'in-app':
        await this.inAppService.send(notification);
        break;
    }

    // Track delivery
    await this.trackingService.track(notification);
  }
}

// Email Service
class EmailService {
  async send(notification: Notification): Promise<void> {
    const template = await this.templateService.getTemplate(notification.type);
    const html = template.render(notification.data);

    await this.emailProvider.send({
      to: notification.recipient,
      subject: template.subject,
      html,
    });
  }
}

// Push Service
class PushService {
  async send(notification: Notification): Promise<void> {
    const deviceTokens = await this.deviceService.getTokens(notification.recipient);

    await Promise.all(deviceTokens.map(token =>
      this.pushProvider.send({
        token,
        title: notification.title,
        body: notification.body,
        data: notification.data,
      })
    ));
  }
}

```

#### Q19: Design a rate limiting system

**Answer:**

```typescript
// Rate Limiter using Token Bucket algorithm
class RateLimiter {
  private buckets: Map<string, { tokens: number; lastRefill: number }> = new Map();

  constructor(
    private maxTokens: number,
    private refillRate: number, // tokens per second
  ) {}

  async isAllowed(key: string): Promise<boolean> {
    const now = Date.now();
    let bucket = this.buckets.get(key);

    if (!bucket) {
      bucket = { tokens: this.maxTokens, lastRefill: now };
      this.buckets.set(key, bucket);
    }

    // Refill tokens
    const timePassed = (now - bucket.lastRefill) / 1000;
    bucket.tokens = Math.min(this.maxTokens, bucket.tokens + timePassed * this.refillRate);
    bucket.lastRefill = now;

    // Check if request is allowed
    if (bucket.tokens >= 1) {
      bucket.tokens--;
      return true;
    }

    return false;
  }
}

// Redis-based distributed rate limiter
class DistributedRateLimiter {
  async isAllowed(key: string, limit: number, windowMs: number): Promise<boolean> {
    const now = Date.now();
    const windowStart = now - windowMs;

    const pipeline = this.redis.pipeline();
    pipeline.zremrangebyscore(key, 0, windowStart); // Remove old entries
    pipeline.zadd(key, now, `${now}-${Math.random()}`); // Add current request
    pipeline.zcard(key); // Count requests in window
    pipeline.expire(key, windowMs / 1000); // Set TTL

    const results = await pipeline.exec();
    const requestCount = results[2][1] as number;

    return requestCount <= limit;
  }
}

```

#### Q20: Design a distributed caching system

**Answer:**

```typescript
// Distributed Cache with Consistent Hashing
class DistributedCache {
  private nodes: CacheNode[] = [];
  private ring: ConsistentHashRing;

  constructor(nodeAddresses: string[]) {
    this.ring = new ConsistentHashRing();

    nodeAddresses.forEach(address => {
      const node = new CacheNode(address);
      this.nodes.push(node);
      this.ring.addNode(node);
    });
  }

  async get(key: string): Promise<any> {
    const node = this.ring.getNode(key);
    return node.get(key);
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    const node = this.ring.getNode(key);
    await node.set(key, value, ttl);

    // Replicate to nearby nodes
    const replicaNodes = this.ring.getReplicaNodes(key, 2);
    await Promise.all(replicaNodes.map(n => n.set(key, value, ttl)));
  }

  async delete(key: string): Promise<void> {
    const node = this.ring.getNode(key);
    await node.delete(key);

    const replicaNodes = this.ring.getReplicaNodes(key, 2);
    await Promise.all(replicaNodes.map(n => n.delete(key)));
  }
}

// Cache-aside pattern
class ProductService {
  constructor(
    private cache: DistributedCache,
    private database: Database,
  ) {}

  async getProduct(productId: string): Promise<Product> {
    // Check cache first
    const cached = await this.cache.get(`product:${productId}`);
    if (cached) return cached;

    // Fetch from database
    const product = await this.database.query(
      'SELECT * FROM products WHERE id = ?',
      [productId]
    );

    // Cache for future requests
    await this.cache.set(`product:${productId}`, product, 3600);

    return product;
  }

  async updateProduct(productId: string, updates: Partial<Product>): Promise<void> {
    // Update database
    await this.database.query(
      'UPDATE products SET ? WHERE id = ?',
      [updates, productId]
    );

    // Invalidate cache
    await this.cache.delete(`product:${productId}`);
  }
}

```

### Follow-up Questions

#### Q21: How do you handle database migrations in microservices?

**Answer:**

```typescript
// Database migration strategy
class MigrationService {
  async migrate(serviceName: string): Promise<void> {
    const database = this.databaseFactory.create(serviceName);

    // Run migrations in order
    const migrations = await this.getMigrations(serviceName);

    for (const migration of migrations) {
      console.log(`Running migration: ${migration.name}`);

      await database.transaction(async (trx) => {
        await trx.raw(migration.up);
        await trx('migrations').insert({
          name: migration.name,
          executed_at: new Date(),
        });
      });
    }
  }

  async rollback(serviceName: string, steps: number = 1): Promise<void> {
    const database = this.databaseFactory.create(serviceName);

    const executed = await database.query(
      'SELECT * FROM migrations ORDER BY executed_at DESC LIMIT ?',
      [steps]
    );

    for (const migration of executed.reverse()) {
      const migrationFile = await this.getMigration(migration.name);

      await database.transaction(async (trx) => {
        await trx.raw(migrationFile.down);
        await trx('migrations').where('name', migration.name).delete();
      });
    }
  }
}

```

#### Q22: How do you handle service versioning?

**Answer:**

```typescript
// API Versioning strategies

// 1. URL Path Versioning
app.use('/api/v1/users', userRouterV1);
app.use('/api/v2/users', userRouterV2);

// 2. Header Versioning
app.use('/api/users', (req, res, next) => {
  const version = req.headers['api-version'] || '1';
  if (version === '2') {
    return userRouterV2(req, res, next);
  }
  return userRouterV1(req, res, next);
});

// 3. Query Parameter Versioning
app.use('/api/users', (req, res, next) => {
  const version = req.query.version || '1';
  // Route based on version
});

// Backward compatibility
class UserServiceV2 extends UserServiceV1 {
  async getUser(userId: string): Promise<UserV2> {
    const user = await super.getUser(userId);

    // Transform to new format
    return {
      id: user.id,
      name: user.name,
      email: user.email,
      // New fields
      preferences: user.preferences || {},
      metadata: {},
    };
  }
}

```

#### Q23: How do you monitor microservices?

**Answer:**

```typescript
// Metrics collection
class MetricsCollector {
  private prometheus: PrometheusClient;

  constructor() {
    this.prometheus = new PrometheusClient();

    // Custom metrics
    this.requestDuration = this.prometheus.histogram({
      name: 'http_request_duration_seconds',
      help: 'Duration of HTTP requests',
      labelNames: ['method', 'route', 'status_code'],
    });

    this.activeConnections = this.prometheus.gauge({
      name: 'active_connections',
      help: 'Number of active connections',
    });
  }

  async trackRequest(req: Request, res: Response, next: NextFunction): Promise<void> {
    const start = Date.now();

    res.on('finish', () => {
      const duration = (Date.now() - start) / 1000;

      this.requestDuration.observe(
        {
          method: req.method,
          route: req.route?.path || 'unknown',
          status_code: res.statusCode,
        },
        duration
      );
    });

    next();
  }
}

// Health check endpoints
app.get('/health', (req, res) => {
  const health = {
    status: 'healthy',
    checks: {
      database: this.database.isConnected(),
      cache: this.cache.isConnected(),
      messageQueue: this.messageQueue.isConnected(),
    },
    uptime: process.uptime(),
  };

  const isHealthy = Object.values(health.checks).every(v => v === true);
  res.status(isHealthy ? 200 : 503).json(health);
});

// Distributed tracing
app.use(tracingMiddleware);

// Logging
app.use(loggingMiddleware);

```

#### Q24: How do you handle secrets management?

**Answer:**

```typescript
// Secrets management with AWS Secrets Manager
class SecretsManager {
  private secretsCache: Map<string, { value: string; expires: number }> = new Map();

  async getSecret(secretName: string): Promise<string> {
    // Check cache
    const cached = this.secretsCache.get(secretName);
    if (cached && Date.now() < cached.expires) {
      return cached.value;
    }

    // Fetch from Secrets Manager
    const secret = await this.awsSecretsManager.getSecretValue({
      SecretId: secretName,
    }).promise();

    // Cache for 1 hour
    this.secretsCache.set(secretName, {
      value: secret.SecretString,
      expires: Date.now() + 3600000,
    });

    return secret.SecretString;
  }

  async getDatabaseCredentials(): Promise<DatabaseCredentials> {
    const secret = await this.getSecret('prod/database/credentials');
    return JSON.parse(secret);
  }
}

// Environment variables for non-sensitive config
const config = {
  port: parseInt(process.env.PORT || '3000'),
  nodeEnv: process.env.NODE_ENV || 'development',
  logLevel: process.env.LOG_LEVEL || 'info',
};

// Never commit secrets to code
// Use .env files locally (add to .gitignore)
// Use secrets manager in production

```

#### Q25: How do you handle blue-green deployments?

**Answer:**

```typescript
// Blue-Green deployment with Kubernetes
const deployment = {
  apiVersion: 'apps/v1',
  kind: 'Deployment',
  metadata: {
    name: 'user-service',
  },
  spec: {
    replicas: 3,
    selector: {
      matchLabels: {
        app: 'user-service',
        version: 'green',
      },
    },
    template: {
      metadata: {
        labels: {
          app: 'user-service',
          version: 'green',
        },
      },
      spec: {
        containers: [
          {
            name: 'user-service',
            image: 'user-service:2.0.0',
            ports: [{ containerPort: 3000 }],
          },
        ],
      },
    },
  },
};

// Service switching
const service = {
  apiVersion: 'v1',
  kind: 'Service',
  metadata: {
    name: 'user-service',
  },
  spec: {
    selector: {
      app: 'user-service',
      version: 'green', // Switch from 'blue' to 'green'
    },
    ports: [
      {
        port: 80,
        targetPort: 3000,
      },
    ],
  },
};

// Rollback strategy
async function rollback(): Promise<void> {
  // Switch service back to blue version
  await kubernetes.updateService('user-service', {
    selector: { version: 'blue' },
  });

  // Scale down green
  await kubernetes.scaleDeployment('user-service-green', 0);

  // Scale up blue
  await kubernetes.scaleDeployment('user-service-blue', 3);
}

```

#### Q26: How do you handle circuit breaker in async systems?

**Answer:**

```typescript
// Async Circuit Breaker with Message Queue
class AsyncCircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime = 0;

  async publishWithCircuitBreaker(
    topic: string,
    message: any,
    fallback?: (msg: any) => Promise<any>
  ): Promise<void> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > 30000) {
        this.state = 'HALF_OPEN';
      } else {
        // Circuit is open, use fallback
        if (fallback) {
          await fallback(message);
        } else {
          throw new Error('Circuit breaker is OPEN');
        }
        return;
      }
    }

    try {
      await this.messageQueue.publish(topic, message);
      this.onSuccess();
    } catch (error) {
      this.onFailure();

      if (fallback) {
        await fallback(message);
      } else {
        // Send to dead letter queue
        await this.messageQueue.publish('dlq', {
          originalTopic: topic,
          message,
          error: error.message,
        });
      }
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= 5) {
      this.state = 'OPEN';
    }
  }
}

```

#### Q27: How do you handle idempotency in distributed systems?

**Answer:**

```typescript
// Idempotency Key pattern
class IdempotentService {
  async processPayment(payment: Payment): Promise<PaymentResult> {
    const idempotencyKey = payment.idempotencyKey ||
      `${payment.userId}-${payment.amount}-${Date.now()}`;

    // Check if already processed
    const existing = await this.idempotencyStore.get(idempotencyKey);
    if (existing) {
      return existing;
    }

    // Process payment
    const result = await this.paymentGateway.charge(payment);

    // Store result with TTL
    await this.idempotencyStore.set(idempotencyKey, result, 86400);

    return result;
  }
}

// Database idempotency
class IdempotentOrderService {
  async createOrder(order: Order): Promise<Order> {
    return this.database.transaction(async (trx) => {
      // Check for existing order with same idempotency key
      const existing = await trx('orders')
        .where('idempotency_key', order.idempotencyKey)
        .first();

      if (existing) {
        return existing;
      }

      // Create order
      const [id] = await trx('orders').insert({
        ...order,
        idempotency_key: order.idempotencyKey,
      });

      return { ...order, id };
    });
  }
}

// HTTP Idempotency Headers
app.post('/api/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];

  // Check cache
  const cached = await redis.get(`idempotent:${idempotencyKey}`);
  if (cached) {
    return res.json(JSON.parse(cached));
  }

  // Process
  const result = await paymentService.process(req.body);

  // Cache result
  await redis.set(`idempotent:${idempotencyKey}`, JSON.stringify(result), 'EX', 86400);

  res.json(result);
});

```

#### Q28: How do you handle distributed locking?

**Answer:**

```typescript
// Redis-based distributed lock
class DistributedLock {
  private redis: RedisClient;

  async acquire(lockName: string, ttl: number = 10000): Promise<string | null> {
    const lockValue = `${Date.now()}-${Math.random()}`;

    const acquired = await this.redis.set(
      `lock:${lockName}`,
      lockValue,
      'NX',
      'PX',
      ttl
    );

    return acquired ? lockValue : null;
  }

  async release(lockName: string, lockValue: string): Promise<boolean> {
    // Lua script for atomic release
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;

    const result = await this.redis.eval(
      script,
      1,
      `lock:${lockName}`,
      lockValue
    );

    return result === 1;
  }

  async withLock<T>(
    lockName: string,
    fn: () => Promise<T>,
    ttl: number = 10000
  ): Promise<T> {
    const lockValue = await this.acquire(lockName, ttl);

    if (!lockValue) {
      throw new Error(`Failed to acquire lock: ${lockName}`);
    }

    try {
      return await fn();
    } finally {
      await this.release(lockName, lockValue);
    }
  }
}

// Usage
const lock = new DistributedLock();

async function transferFunds(from: string, to: string, amount: number) {
  await lock.withLock(`transfer:${from}:${to}`, async () => {
    // Critical section - only one transfer at a time
    const balance = await accountService.getBalance(from);
    if (balance < amount) {
      throw new Error('Insufficient funds');
    }

    await accountService.debit(from, amount);
    await accountService.credit(to, amount);
  });
}

```

#### Q29: How do you handle service mesh?

**Answer:**

```yaml
# Istio Service Mesh Configuration
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:

  - user-service
  http:

  - route:
    - destination:
        host: user-service
        subset: v1
      weight: 90

    - destination:
        host: user-service
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  subsets:

  - name: v1
    labels:
      version: v1

  - name: v2
    labels:
      version: v2
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s

```

```typescript
// Service Mesh benefits in code
// 1. Automatic Load Balancing
// 2. Circuit Breaking (built-in)
// 3. Retries and Timeouts
// 4. Distributed Tracing
// 5. mTLS (mutual TLS)

// Your code focuses on business logic
class UserService {
  async getUser(userId: string): Promise<User> {
    // Service mesh handles:
    // - Load balancing to user-service instances
    // - Circuit breaking if service is down
    // - Retries on failure
    // - Distributed tracing headers
    // - mTLS encryption

    return this.userRepository.findById(userId);
  }
}

```

#### Q30: How do you handle event-driven architecture at scale?

**Answer:**

```typescript
// Event-driven architecture with Kafka
class EventDrivenArchitecture {
  private kafka: Kafka;
  private producer: Producer;
  private consumers: Map<string, Consumer> = new Map();

  async initialize(): Promise<void> {
    this.kafka = new Kafka({
      clientId: 'order-service',
      brokers: ['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092'],
    });

    this.producer = this.kafka.producer({
      idempotent: true,
      transactionalId: 'order-service-producer',
    });

    await this.producer.connect();
  }

  async publishEvent<T>(topic: string, event: T): Promise<void> {
    await this.producer.send({
      topic,
      messages: [
        {
          key: (event as any).id,
          value: JSON.stringify(event),
          timestamp: Date.now().toString(),
        },
      ],
    });
  }

  async subscribe(
    topic: string,
    groupId: string,
    handler: (event: any) => Promise<void>
  ): Promise<void> {
    const consumer = this.kafka.consumer({ groupId });
    await consumer.connect();
    await consumer.subscribe({ topics: [topic] });

    await consumer.run({
      eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value!.toString());
        await handler(event);
      },
    });

    this.consumers.set(`${topic}-${groupId}`, consumer);
  }
}

// Event Sourcing with CQRS
class EventSourcedOrderService {
  async createOrder(command: CreateOrderCommand): Promise<void> {
    // Create aggregate
    const order = OrderAggregate.create(command);

    // Save events
    await this.eventStore.saveEvents(order.id, order.getUncommittedEvents());

    // Update read model (async)
    await this.eventBus.publish('OrderCreated', {
      orderId: order.id,
      ...command,
    });
  }

  async getOrder(orderId: string): Promise<OrderView> {
    // Read from projection (optimized for reads)
    return this.orderProjection.get(orderId);
  }
}

```

## Real-World Use Cases

### 1. Netflix

- 1000+ microservices
- Handles 200M+ subscribers
- Real-time streaming, recommendations
- Event-driven architecture with Kafka

### 2. Uber

- Microservices for ride matching, pricing, payments
- Real-time location tracking
- Event sourcing for trip events
- Circuit breakers for resilience

### 3. Amazon

- Hundreds of microservices
- Independent deployment
- Saga pattern for order processing
- Event-driven for inventory management

### 4. LinkedIn

- Activity feeds, messaging
- Kafka for event streaming
- CQRS for read-heavy workloads
- Distributed caching

## Common Mistakes

1. **Distributed monolith** - Services too coupled

2. **Shared databases** - Violates service independence

3. **Synchronous everything** - Creates tight coupling

4. **Ignoring failure handling** - Cascade failures

5. **Missing monitoring** - Can't debug issues

6. **Over-engineering** - Unnecessary complexity

7. **Wrong service boundaries** - Chatty services

8. **Ignoring data consistency** - Data corruption

## Best Practices

1. **Design for failure** - Assume services will fail

2. **Embrace eventual consistency** - Don't fight it

3. **Use circuit breakers** - Prevent cascade failures

4. **Implement idempotency** - Handle retries safely

5. **Monitor everything** - Metrics, logs, traces

6. **Automate deployments** - CI/CD pipelines

7. **Use API contracts** - Clear service boundaries

8. **Document architecture** - Keep docs updated

## Performance Considerations

- **Async communication** - Don't block on service calls
- **Caching** - Cache frequently accessed data
- **Connection pooling** - Reuse connections
- **Load balancing** - Distribute traffic
- **Circuit breakers** - Prevent cascade failures
- **Bulkheading** - Isolate failures
- **Monitoring** - Track performance metrics

## Interview Questions

### Beginner (5-10)

1. **What is microservices architecture?**

   - Collection of loosely coupled, independently deployable services.

2. **Why use microservices?**

   - Scalability, independent deployment, technology flexibility, team autonomy.

3. **What is service discovery?**

   - Mechanism for services to find each other dynamically.

4. **What is an API Gateway?**

   - Single entry point handling cross-cutting concerns.

5. **What is the difference between REST and gRPC?**

   - REST: HTTP/JSON, text-based
   - gRPC: HTTP/2, Protocol Buffers, binary

6. **What is containerization?**

   - Packaging applications with dependencies (Docker).

7. **What is orchestration?**

   - Managing containers at scale (Kubernetes).

8. **What is continuous integration?**

   - Automated building and testing of code changes.

### Intermediate (5-10)

9. **What is the Saga pattern?**

   - Managing distributed transactions with compensation.

10. **What is circuit breaker?**

    - Preventing cascade failures by stopping calls to failing services.

11. **What is event sourcing?**

    - Storing state changes as immutable events.

12. **What is CQRS?**

    - Separating read and write models for optimization.

13. **How do you handle service failures?**

    - Circuit breakers, retries, fallbacks, bulkheading.

14. **What is distributed tracing?**

    - Tracking requests across service boundaries.

15. **How do you ensure data consistency?**

    - Sagas, eventual consistency, outbox pattern.

16. **What is service mesh?**

    - Infrastructure layer for service-to-service communication.

### Senior (10-15)

17. **Design a microservices system for e-commerce.**

    - Service boundaries, communication patterns, data management.

18. **How do you handle database per service?**

    - API composition, event-driven synchronization.

19. **What is the outbox pattern?**

    - Reliable event publishing within transactions.

20. **How do you handle distributed transactions?**

    - Saga pattern, eventual consistency, compensation.

21. **What is event-driven architecture?**

    - Services communicate through events.

22. **How do you monitor microservices?**

    - Metrics, logs, traces, health checks.

23. **What is blue-green deployment?**

    - Zero-downtime deployment strategy.

24. **How do you handle secrets management?**

    - Secrets manager, environment variables, encryption.

25. **What is service versioning?**

    - Managing API changes without breaking clients.

### FAANG-style (5-10)

26. **Design Netflix's microservices architecture.**

    - 1000+ services, event-driven, high availability.

27. **How would you handle 1M requests/second?**

    - Caching, load balancing, async processing, optimization.

28. **Design a real-time analytics system.**

    - Stream processing, event sourcing, CQRS.

29. **How do you ensure microservices security?**

    - mTLS, API gateway, authentication, authorization.

30. **Explain microservices testing strategies.**

    - Unit, integration, contract, end-to-end testing.

### Follow-ups (5-10)

31. **How do you migrate from monolith to microservices?**

    - Strangler fig pattern, gradual extraction.

32. **What is the impact of microservices on development?**

    - Team autonomy, deployment complexity, monitoring.

33. **How do you handle microservices debugging?**

    - Distributed tracing, logging, correlation IDs.

34. **What is the future of microservices?**

    - Serverless, service mesh, AI-driven operations.

35. **How do you choose between microservices and monolith?**

    - Team size, complexity, deployment frequency.

## Summary

Microservices architecture requires understanding of distributed systems, communication patterns, and architectural decisions. Master these concepts and practice implementing them to ace your senior developer interviews.

## Cheat Sheet

```text
┌─────────────────────────────────────────────────────────────────┐
│           MICROSERVICES INTERVIEW CHEAT SHEET                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CORE CONCEPTS:                                                 │
│  • Service Independence: Database per service                   │
│  • Communication: Sync (REST/gRPC) vs Async (Events)           │
│  • Service Discovery: Dynamic service location                  │
│  • API Gateway: Single entry point                             │
│                                                                 │
│  PATTERNS:                                                      │
│  • Saga: Distributed transactions with compensation             │
│  • Circuit Breaker: Prevent cascade failures                    │
│  • Event Sourcing: Store events, derive state                   │
│  • CQRS: Separate read/write models                            │
│  • Outbox: Reliable event publishing                           │
│  • Bulkhead: Isolate failures                                  │
│                                                                 │
│  KEY TOOLS:                                                     │
│  • Docker: Containerization                                    │
│  • Kubernetes: Orchestration                                   │
│  • Kafka/RabbitMQ: Message brokers                             │
│  • Redis: Caching                                              │
│  • Jaeger/Zipkin: Distributed tracing                          │
│                                                                 │
│  BEST PRACTICES:                                                │
│  • Design for failure                                          │
│  • Embrace eventual consistency                                │
│  • Implement circuit breakers                                  │
│  • Monitor everything                                          │
│  • Automate deployments                                        │
│  • Use API contracts                                           │
│  • Document architecture                                       │
│                                                                 │
│  COMMON PITFALLS:                                               │
│  ✗ Distributed monolith                                        │
│  ✗ Shared databases                                            │
│  ✗ Synchronous everything                                      │
│  ✗ Ignoring failure handling                                   │
│  ✗ Missing monitoring                                          │
│  ✗ Over-engineering                                            │
└─────────────────────────────────────────────────────────────────┘

```

---

## References & Learn More

- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)