---
section: Microservices
category: Architecture
tags: [concept]
---

# CQRS (Command Query Responsibility Segregation)

## Definition

**CQRS (Command Query Responsibility Segregation)** is an architectural pattern that separates read operations (queries) from write operations (commands) into distinct models, services, and often databases. Instead of a single model that handles both reads and writes, CQRS uses separate **command models** for mutations (create, update, delete) and **query models** for reads (select, list, search). This separation allows each side to be optimized independently for its specific workload.

## Why Do We Need It?

1. **Performance optimization** — Read and write workloads have different scaling requirements
2. **Security** — Queries and commands often need different authentication/authorization
3. **Complexity management** — Separate domain logic (commands) from presentation logic (queries)
4. **Scalability** — Independently scale read replicas vs write primaries
5. **Flexibility** — Optimize each model for its use case (denormalized reads, normalized writes)

## How It Works

### Architecture Overview

```text
CQRS Architecture:
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│                    CQRS ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Client                    Command Side         Query Side       │
│  ┌────────────────┐       ┌────────────────┐   ┌──────────────┐ │
│  │  User Interface │       │  Command Model │   │ Query Model  │ │
│  │                 │       │                │   │              │ │
│  │  ┌──────────┐  │       │  ┌──────────┐  │   │ ┌──────────┐ │ │
│  │  │  Create   │──┼──────┼─>│  Command  │  │   │ │  Query   │ │ │
│  │  │  Order    │  │       │  │  Handler  │  │   │ │  Handler │ │ │
│  │  └──────────┘  │       │  └─────┬────┘  │   │ └────┬─────┘ │ │
│  │                │       │        │        │   │      │       │ │
│  │  ┌──────────┐  │       │        ▼        │   │      ▼       │ │
│  │  │  Get      │──┼──────┼──     ...       │   │  ┌────────┐ │ │
│  │  │  Orders   │  │       │                │   │  │ SELECT  │ │ │
│  │  └──────────┘  │       │  ┌──────────┐  │   │  └────────┘ │ │
│  └────────────────┘       │  │  Domain   │  │   └──────────────┘ │
│                           │  │  Events   │──┼────────────────>  │
│                           │  └──────────┘  │                    │
│                           └────────────────┘                    │
│                                     │                           │
│                                     ▼                           │
│                           ┌─────────────────────────────────┐   │
│                           │        Event Store / Bus          │   │
│                           │  Events: OrderCreated, etc.      │   │
│                           └─────────────────────────────────┘   │
│                                     │                           │
│                                     ▼                           │
│                           ┌─────────────────────────────────┐   │
│                           │      Read Model Projection        │   │
│                           │  ┌───────────────────────────┐  │   │
│                           │  │  Write DB  │   Read DB    │  │   │
│                           │  │ (Normalized)│ (Denormalized) │  │   │
│                           │  └───────────────────────────┘  │   │
│                           └─────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

### Command vs Query

```text
Command Side (Writes):
═══════════════════════════════════════════════════════════════

├── Purpose: Execute business operations
├── Verb: POST, PUT, PATCH, DELETE
├── Returns: Status (success/failure), no data
├── Model: Domain-driven, normalized
├── Validation: Business rules, invariants
├── Events: May emit domain events
└── Example: PlaceOrder, UpdateCustomer, DeleteProduct

Query Side (Reads):
═══════════════════════════════════════════════════════════════

├── Purpose: Retrieve data for presentation
├── Verb: GET
├── Returns: DTOs, ViewModels
├── Model: UI-optimized, denormalized
├── Validation: None (or minimal projection)
├── Events: Subscribes to events to update projections
└── Example: GetOrderById, SearchProducts, GetCustomerHistory

```

## Code Examples

### 1. Basic CQRS — Commands

```typescript
// ─── Command Models ──────────────────────────────────────────

interface Command {
  type: string;
  timestamp: Date;
}

interface CreateOrderCommand extends Command {
  type: 'CreateOrder';
  customerId: string;
  items: OrderItem[];
  shippingAddress: Address;
}

interface UpdateOrderStatusCommand extends Command {
  type: 'UpdateOrderStatus';
  orderId: string;
  status: OrderStatus;
  reason?: string;
}

interface CancelOrderCommand extends Command {
  type: 'CancelOrder';
  orderId: string;
  reason: string;
}

// ─── Command Handler ─────────────────────────────────────────

class CreateOrderHandler {
  constructor(
    private orderRepository: OrderRepository,
    private eventBus: EventBus,
    private inventoryService: InventoryService,
  ) {}

  async handle(command: CreateOrderCommand): Promise<CommandResult> {
    // 1. Validate business rules
    await this.validateInventory(command.items);

    // 2. Create domain entity
    const order = Order.create({
      customerId: command.customerId,
      items: command.items,
      shippingAddress: command.shippingAddress,
    });

    // 3. Persist to write database
    await this.orderRepository.save(order);

    // 4. Emit domain event
    await this.eventBus.publish(new OrderCreatedEvent({
      orderId: order.id,
      customerId: command.customerId,
      items: command.items,
      total: order.total,
      timestamp: new Date(),
    }));

    return { success: true, orderId: order.id };
  }

  private async validateInventory(items: OrderItem[]): Promise<void> {
    for (const item of items) {
      const available = await this.inventoryService.checkStock(item.productId);
      if (available < item.quantity) {
        throw new Error(`Insufficient inventory for ${item.productId}`);
      }
    }
  }
}
```

### 2. Basic CQRS — Queries

```typescript
// ─── Query Models ────────────────────────────────────────────

interface Query {
  type: string;
}

interface GetOrderByIdQuery extends Query {
  type: 'GetOrderById';
  orderId: string;
}

interface SearchOrdersQuery extends Query {
  type: 'SearchOrders';
  customerId?: string;
  status?: OrderStatus;
  fromDate?: Date;
  toDate?: Date;
  page: number;
  limit: number;
}

interface GetDashboardStatsQuery extends Query {
  type: 'GetDashboardStats';
  merchantId: string;
  period: 'daily' | 'weekly' | 'monthly';
}

// ─── Query Handler ───────────────────────────────────────────

class OrderQueryHandler {
  constructor(private readDb: ReadDatabase) {}

  async handle(query: GetOrderByIdQuery): Promise<OrderView | null> {
    // Read from denormalized read database
    return this.readDb.orders.findOne({
      where: { id: query.orderId },
      select: {
        id: true,
        customerName: true,
        items: true,
        total: true,
        status: true,
        trackingUrl: true,
        estimatedDelivery: true,
      },
    });
  }

  async handleSearch(query: SearchOrdersQuery): Promise<PaginatedResult<OrderSummary>> {
    const { customerId, status, fromDate, toDate, page, limit } = query;

    const where: any = {};
    if (customerId) where.customerId = customerId;
    if (status) where.status = status;
    if (fromDate || toDate) {
      where.createdAt = {};
      if (fromDate) where.createdAt.gte = fromDate;
      if (toDate) where.createdAt.lte = toDate;
    }

    const [items, total] = await Promise.all([
      this.readDb.orderSummaries.findMany({
        where,
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.readDb.orderSummaries.count({ where }),
    ]);

    return { items, total, page, limit, totalPages: Math.ceil(total / limit) };
  }
}
```

### 3. Event Sourcing + CQRS Integration

```typescript
// ─── Domain Events ───────────────────────────────────────────

interface DomainEvent {
  type: string;
  aggregateId: string;
  timestamp: Date;
  data: Record<string, any>;
}

class OrderCreatedEvent implements DomainEvent {
  readonly type = 'OrderCreated';
  readonly timestamp = new Date();

  constructor(
    public readonly aggregateId: string,
    public readonly data: {
      customerId: string;
      items: OrderItem[];
      total: number;
      shippingAddress: Address;
    },
  ) {}
}

class OrderShippedEvent implements DomainEvent {
  readonly type = 'OrderShipped';
  readonly timestamp = new Date();

  constructor(
    public readonly aggregateId: string,
    public readonly data: {
      trackingNumber: string;
      carrier: string;
      estimatedDelivery: Date;
    },
  ) {}
}

// ─── Event Store ─────────────────────────────────────────────

class EventStore {
  private events: DomainEvent[] = [];

  async append(event: DomainEvent): Promise<void> {
    this.events.push(event);
    // In production: write to dedicated event store (e.g., EventStoreDB, Kafka)
  }

  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    return this.events.filter(e => e.aggregateId === aggregateId);
  }
}

// ─── Read Model Projector ────────────────────────────────────

class OrderReadModelProjector {
  constructor(private readDb: ReadDatabase) {}

  async handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
    // Project to denormalized read model
    await this.readDb.orderViews.create({
      data: {
        id: event.aggregateId,
        customerId: event.data.customerId,
        items: JSON.stringify(event.data.items),
        total: event.data.total,
        shippingAddress: JSON.stringify(event.data.shippingAddress),
        status: 'created',
        createdAt: event.timestamp,
        updatedAt: event.timestamp,
      },
    });

    // Update dashboard stats
    await this.readDb.dailyStats.upsert({
      where: { date: getDateKey(event.timestamp) },
      create: { ordersCount: 1, revenue: event.data.total },
      update: { ordersCount: { increment: 1 }, revenue: { increment: event.data.total } },
    });
  }

  async handleOrderShipped(event: OrderShippedEvent): Promise<void> {
    await this.readDb.orderViews.update({
      where: { id: event.aggregateId },
      data: {
        status: 'shipped',
        trackingUrl: `https://track.example.com/${event.data.trackingNumber}`,
        estimatedDelivery: event.data.estimatedDelivery,
        updatedAt: event.timestamp,
      },
    });
  }
}
```

### 4. CQRS with Separate Databases

```typescript
// ─── Write Model (Normalized) ───────────────────────────────

// Write database entities (normalized, constrained)
// PostgreSQL with ACID transactions

interface WriteOrder {
  id: string;
  customerId: string;
  status: OrderStatus;
  createdAt: Date;
  updatedAt: Date;
  // Items stored in separate table
}

interface WriteOrderItem {
  id: string;
  orderId: string;
  productId: string;
  quantity: number;
  unitPrice: number;
}

// ─── Read Model (Denormalized) ──────────────────────────────

// Read database (could be MongoDB, Elasticsearch, Redis, or PG view)
// Optimized for queries, may duplicate data

interface ReadOrderView {
  id: string;
  orderNumber: string;
  customerId: string;
  customerName: string;
  customerEmail: string;
  items: Array<{
    productId: string;
    productName: string;
    imageUrl: string;
    quantity: number;
    unitPrice: number;
    totalPrice: number;
  }>;
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
  status: OrderStatus;
  trackingUrl: string | null;
  estimatedDelivery: Date | null;
  shippingAddress: {
    street: string;
    city: string;
    state: string;
    zip: string;
  };
  createdAt: Date;
  updatedAt: Date;
}

// ─── Data Synchronizer ──────────────────────────────────────

class OrderDataSynchronizer {
  constructor(
    private writeDb: WriteDatabase,
    private readDb: ReadDatabase,
  ) {}

  async syncOrder(orderId: string): Promise<void> {
    // Fetch normalized write data
    const order = await this.writeDb.orders.findUnique({
      where: { id: orderId },
      include: { items: true, customer: true },
    });

    if (!order) return;

    // Transform to denormalized read model
    const readModel: ReadOrderView = {
      id: order.id,
      orderNumber: `ORD-${order.createdAt.getTime()}`,
      customerId: order.customerId,
      customerName: order.customer.name,
      customerEmail: order.customer.email,
      items: order.items.map(item => ({
        productId: item.productId,
        productName: item.product.name,
        imageUrl: item.product.imageUrl,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        totalPrice: item.quantity * item.unitPrice,
      })),
      subtotal: order.items.reduce((s, i) => s + i.quantity * i.unitPrice, 0),
      tax: order.tax,
      shipping: order.shipping,
      total: order.total,
      status: order.status,
      trackingUrl: order.trackingUrl,
      estimatedDelivery: order.estimatedDelivery,
      shippingAddress: order.shippingAddress as any,
      createdAt: order.createdAt,
      updatedAt: order.updatedAt,
    };

    // Upsert into read database
    await this.readDb.orderViews.upsert({
      where: { id: orderId },
      create: readModel,
      update: readModel,
    });
  }
}
```

### 5. CQRS Mediator Pattern

```typescript
// ─── Mediator ────────────────────────────────────────────────

class Mediator {
  private commandHandlers = new Map<string, CommandHandler>();
  private queryHandlers = new Map<string, QueryHandler>();

  registerCommand<T extends Command>(type: string, handler: CommandHandler<T>): void {
    this.commandHandlers.set(type, handler);
  }

  registerQuery<T extends Query>(type: string, handler: QueryHandler<T>): void {
    this.queryHandlers.set(type, handler);
  }

  async send<T extends Command>(command: T): Promise<CommandResult> {
    const handler = this.commandHandlers.get(command.type);
    if (!handler) throw new Error(`No handler for command: ${command.type}`);
    return handler.handle(command);
  }

  async query<T extends Query, R>(query: T): Promise<R> {
    const handler = this.queryHandlers.get(query.type);
    if (!handler) throw new Error(`No handler for query: ${query.type}`);
    return handler.handle(query);
  }
}

// ─── Registration ────────────────────────────────────────────

// In your application bootstrap:
const mediator = new Mediator();

// Register command handlers
mediator.registerCommand('CreateOrder', new CreateOrderHandler(/* deps */));
mediator.registerCommand('UpdateOrderStatus', new UpdateOrderStatusHandler(/* deps */));
mediator.registerCommand('CancelOrder', new CancelOrderHandler(/* deps */));

// Register query handlers
mediator.registerQuery('GetOrderById', new OrderQueryHandler(/* deps */));
mediator.registerQuery('SearchOrders', new OrderQueryHandler(/* deps */));
mediator.registerQuery('GetDashboardStats', new DashboardQueryHandler(/* deps */));

// ─── API Layer ───────────────────────────────────────────────

async function createOrderHandler(req: Request, mediator: Mediator) {
  const command: CreateOrderCommand = {
    type: 'CreateOrder',
    customerId: req.body.customerId,
    items: req.body.items,
    shippingAddress: req.body.shippingAddress,
    timestamp: new Date(),
  };

  const result = await mediator.send(command);
  return Response.json(result, { status: 201 });
}

async function getOrderHandler(req: Request, mediator: Mediator) {
  const query: GetOrderByIdQuery = {
    type: 'GetOrderById',
    orderId: req.params.id,
  };

  const order = await mediator.query(query);
  if (!order) return Response.json({ error: 'Not found' }, { status: 404 });
  return Response.json(order);
}
```

### 6. CQRS Without Separate Databases

```typescript
// Simple CQRS — same database, different models

// ─── Write Model ─────────────────────────────────────────────

class UserWriteService {
  constructor(private db: PrismaClient) {}

  async createUser(command: { email: string; name: string }): Promise<User> {
    // Write-optimized model with full validation
    const user = await this.db.user.create({
      data: command,
    });

    await this.eventBus.publish(new UserCreatedEvent(user.id, user.email));
    return user;
  }
}

// ─── Read Model ──────────────────────────────────────────────

class UserReadService {
  constructor(private db: PrismaClient) {}

  async getUserProfile(userId: string): Promise<UserProfileDTO | null> {
    // Read-optimized query — returns exactly what the UI needs
    const user = await this.db.user.findUnique({
      where: { id: userId },
      select: {
        id: true,
        name: true,
        email: true,
        avatarUrl: true,
        _count: { select: { posts: true, followers: true, following: true } },
      },
    });

    if (!user) return null;

    return {
      id: user.id,
      displayName: user.name,
      email: user.email,
      avatar: user.avatarUrl,
      stats: {
        posts: user._count.posts,
        followers: user._count.followers,
        following: user._count.following,
      },
    };
  }

  async searchUsers(query: string, page: number): Promise<UserSearchResult> {
    // Search-optimized query
    const users = await this.db.user.findMany({
      where: {
        OR: [
          { name: { contains: query, mode: 'insensitive' } },
          { email: { contains: query, mode: 'insensitive' } },
        ],
      },
      select: { id: true, name: true, avatarUrl: true },
      skip: (page - 1) * 20,
      take: 20,
    });

    return { users, page };
  }
}
```

## Real-World Use Cases

| Scenario | Implementation | Benefit |
|----------|---------------|---------|
| **E-commerce** | Separate order write DB from product search (Elasticsearch) | Search doesn't slow order placement |
| **Banking** | Write: ACID transactions. Read: Event-sourced account history | Auditable, queryable history |
| **SaaS Dashboard** | Write: Normalized relational. Read: Pre-joined materialized views | Dashboards load instantly |
| **Social media** | Write: Post creates. Read: Feed cache | High write throughput + fast reads |
| **IoT** | Write: Sensor data ingestion. Read: Aggregated time-series | Handle millions of writes/reads |

## Common Mistakes

### 1. Over-Engineering

```typescript
// ❌ BAD: CQRS for a CRUD app with 3 pages
// Adds unnecessary complexity for simple applications

// ✅ GOOD: Use CQRS when:
// - Different read/write scalability requirements
// - Complex domain logic on write side
// - Multiple read representations of same data
// - Performance requirements justify the complexity
```

### 2. Inconsistent Data (Eventual Consistency)

```typescript
// ❌ BAD: Expecting immediate consistency
// Write succeeds, read fails to reflect new data

// ✅ GOOD: Design for eventual consistency
class OrderService {
  async placeOrder(command: CreateOrderCommand) {
    // Write succeeds
    const order = await this.writeDb.createOrder(command);
    await this.eventBus.publish(new OrderCreatedEvent(order));

    // But don't immediately query read model!
    // Return orderId and let client poll or get event notification
    return { orderId: order.id, message: 'Order placed (may take a moment to appear)' };
  }
}
```

### 3. Duplicating Business Logic

```typescript
// ❌ BAD: Validation in both command and query
class CreateOrderHandler {
  validate(order) { /* ... */ }
}

class OrderQueryHandler {
  validate(order) { /* ... Same validation! ... */ }
}

// ✅ GOOD: Only commands validate; queries just read
class CreateOrderHandler {
  validate(order) { /* Business rules here */ }
}

class OrderQueryHandler {
  // No validation — just read and return
  async getOrder(id: string) { return this.readDb.findOne(id); }
}
```

### 4. Complex Synchronization

```text
// ❌ BAD: Sync failures go undetected
Write DB → ??? → Read DB  (no monitoring)

// ✅ GOOD: Monitor sync health
Write DB → Event Bus → Projector → Read DB
                           ↓
                    Monitor: latency, failure rate, consistency check
```

## Best Practices

1. **Start without separate databases** — Use same DB with different query models first
2. **Eventual consistency is acceptable** — Design UI to handle write-read lag
3. **Monitor projection lag** — Track how far behind the read model is
4. **Idempotent projections** — Re-running projections should produce same result
5. **Handle projection failures** — Dead letter queues for failed events
6. **Validate on command side only** — Queries are for reading, not business rules
7. **Use DTOs for queries** — Don't expose domain models directly
8. **Consider CQRS for high-traffic features only** — Not the entire app
9. **Combine with Event Sourcing** — For complete audit trails
10. **Test consistency boundaries** — Verify read model eventually matches write

## Summary

- CQRS separates read and write operations into distinct models with different optimization strategies
- Commands handle mutations with full business validation; Queries handle data retrieval with UI-optimized models
- Can use separate databases (write: normalized, read: denormalized) or same database with different query models
- Eventual consistency between write and read models is expected and must be designed for
- Best suited for complex domains with different read/write scalability needs

## Cheat Sheet

```typescript
// Command
interface Command { type: string; timestamp: Date; }

class CreateOrderHandler {
  async handle(cmd: CreateOrderCommand): Promise<CommandResult> {
    // Validate → Execute → Persist → Emit event
  }
}

// Query
interface Query { type: string; }

class GetOrderHandler {
  async handle(query: GetOrderQuery): Promise<OrderView> {
    // Read from denormalized read DB
    return this.readDb.findOne(query.orderId);
  }
}

// Event projection
class OrderProjector {
  async handleOrderCreated(event: OrderCreatedEvent) {
    // Update denormalized read model
    await this.readDb.orders.create({ ...event.data });
  }
}

// Mediator pattern
const mediator = new Mediator();
mediator.register('CreateOrder', createHandler);
mediator.register('GetOrder', getHandler);
const result = await mediator.send(command);
const data = await mediator.query(query);
```

```text
CQRS Key Points:
├── Commands: Write operations (verbs: create, update, delete)
├── Queries: Read operations (verbs: get, search, list)
├── Separate models: Optimize each for its workload
├── Eventual consistency: Write → Projector → Read
├── Sync: Event bus, message queue, CDC
├── Benefits: Independent scaling, optimized reads, security
├── Costs: Complexity, eventual consistency, sync logic
└── When to use: Complex domains, different R/W perf needs
```

---

## See Also

- [Distributed Transactions](11-Distributed-Transactions.md)
- [Event Sourcing](07-Event-Sourcing.md)
- [gRPC](09-gRPC.md)
- [Interview Questions](08-Interview-Questions.md)
- [Kafka](05-Kafka.md)
- [RabbitMQ](06-RabbitMQ.md)
- [Service Discovery](01-Service-Discovery.md)

## References & Learn More

- [Martin Fowler: CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Microsoft: CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Greg Young: CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- [CQRS by Example](https://github.com/gregoryyoung/m-r)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
