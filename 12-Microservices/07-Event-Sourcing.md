---
section: Microservices
category: Architecture
tags: [concept]
---

# Event Sourcing

## TL;DR

Persist all state changes as an immutable sequence of events; rebuild current state by replaying them, often paired with CQRS.

**Why it matters:** Tests event store design, snapshotting, projection rebuilds, and the trade-offs (audit trail + time travel vs schema evolution headaches).

## Definition

Event Sourcing is a design pattern where state changes are stored as an immutable sequence of events. Instead of storing current state, you store all events that led to that state. The current state is derived by replaying events. Events are facts that happened in the system and cannot be modified or deleted.

## Why Do We Need It?

In microservices:

- Complete audit trail of all changes
- Temporal queries - see state at any point in time
- Debugging and root cause analysis
- Event-driven architecture integration
- CQRS implementation
- Replay and recovery capabilities

## How It Works

### Traditional vs Event Sourcing

```text
TRADITIONAL STATE STORAGE:
┌─────────────────────────────────────────────────────────┐
│                    DATABASE                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Orders Table:                                         │
│   ┌─────────┬──────────┬────────┬─────────┐            │
│   │ OrderID │ Status   │ Amount │ Updated │            │
│   ├─────────┼──────────┼────────┼─────────┤            │
│   │ ord-123 │ Shipped  │ $100   │ 2024-01 │            │
│   └─────────┴──────────┴────────┴─────────┘            │
│                                                         │
│   Only current state is stored                          │
└─────────────────────────────────────────────────────────┘

EVENT SOURCING:
┌─────────────────────────────────────────────────────────┐
│                    EVENT STORE                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Events:                                               │
│   ┌─────┬─────────────────┬─────────────────────────┐  │
│   │ Seq │ Event Type      │ Data                    │  │
│   ├─────┼─────────────────┼─────────────────────────┤  │
│   │ 1   │ OrderCreated    │ {id: ord-123, ...}      │  │
│   │ 2   │ ItemAdded       │ {item: "book", ...}     │  │
│   │ 3   │ PaymentReceived │ {amount: 100, ...}      │  │
│   │ 4   │ OrderShipped    │ {tracking: "123456"}    │  │
│   └─────┴─────────────────┴─────────────────────────┘  │
│                                                         │
│   All events are stored, current state is derived       │
└─────────────────────────────────────────────────────────┘

```

### Event Store Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                  EVENT SOURCING ARCHITECTURE             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐     ┌─────────────────────────────┐  │
│   │  Command    │────>│        AGGREGATE             │  │
│   │  (Intent)   │     │  (Business Logic)            │  │
│   └─────────────┘     └─────────────┬───────────────┘  │
│                                     │                   │
│                                     │ Emits             │
│                                     │ Events            │
│                                     ▼                   │
│                         ┌─────────────────────────────┐ │
│                         │       EVENT STORE            │ │
│                         │  ┌───────────────────────┐  │ │
│                         │  │ Event 1: Created      │  │ │
│                         │  │ Event 2: ItemAdded    │  │ │
│                         │  │ Event 3: Shipped      │  │ │
│                         │  └───────────────────────┘  │ │
│                         └─────────────┬───────────────┘ │
│                                       │                 │
│                                       │ Projects        │
│                                       ▼                 │
│                         ┌─────────────────────────────┐ │
│                         │     PROJECTION               │ │
│                         │  (Read Model)                │ │
│                         │  ┌───────────────────────┐  │ │
│                         │  │ Order View:           │  │ │
│                         │  │ Status: Shipped       │  │ │
│                         │  │ Amount: $100          │  │ │
│                         │  └───────────────────────┘  │ │
│                         └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

```

## Code Examples

### TypeScript - Event Store

```typescript
interface Event {
  id: string;
  aggregateId: string;
  aggregateType: string;
  type: string;
  data: Record<string, any>;
  metadata: {
    timestamp: Date;
    version: number;
    correlationId?: string;
    causationId?: string;
  };
}

class EventStore {
  private events: Event[] = [];
  private snapshots: Map<string, any> = new Map();

  async append(event: Omit<Event, 'id' | 'metadata'>): Promise<Event> {
    const fullEvent: Event = {
      ...event,
      id: this.generateEventId(),
      metadata: {
        timestamp: new Date(),
        version: this.getNextVersion(event.aggregateId),
      },
    };

    this.events.push(fullEvent);
    console.log(`Event appended: ${fullEvent.type} for ${fullEvent.aggregateId}`);

    return fullEvent;
  }

  async getEvents(aggregateId: string): Promise<Event[]> {
    return this.events
      .filter(e => e.aggregateId === aggregateId)
      .sort((a, b) => a.metadata.version - b.metadata.version);
  }

  async getEventsByType(eventType: string): Promise<Event[]> {
    return this.events
      .filter(e => e.type === eventType)
      .sort((a, b) => a.metadata.timestamp.getTime() - b.metadata.timestamp.getTime());
  }

  async getEventsFromTimestamp(from: Date): Promise<Event[]> {
    return this.events
      .filter(e => e.metadata.timestamp >= from)
      .sort((a, b) => a.metadata.timestamp.getTime() - b.metadata.timestamp.getTime());
  }

  async getEventsFromVersion(
    aggregateId: string,
    fromVersion: number
  ): Promise<Event[]> {
    return this.events
      .filter(
        e =>
          e.aggregateId === aggregateId &&
          e.metadata.version > fromVersion
      )
      .sort((a, b) => a.metadata.version - b.metadata.version);
  }

  async saveSnapshot(aggregateId: string, state: any): Promise<void> {
    this.snapshots.set(aggregateId, {
      state,
      timestamp: new Date(),
      version: this.getNextVersion(aggregateId) - 1,
    });
    console.log(`Snapshot saved for ${aggregateId}`);
  }

  async getSnapshot(aggregateId: string): Promise<any | null> {
    const snapshot = this.snapshots.get(aggregateId);
    return snapshot?.state || null;
  }

  private generateEventId(): string {
    return `evt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private getNextVersion(aggregateId: string): number {
    const events = this.events.filter(e => e.aggregateId === aggregateId);
    if (events.length === 0) return 1;
    return Math.max(...events.map(e => e.metadata.version)) + 1;
  }
}

```

### TypeScript - Aggregate with Event Sourcing

```typescript
abstract class AggregateRoot {
  protected id: string;
  protected version: number = 0;
  private uncommittedEvents: Event[] = [];

  constructor(id: string) {
    this.id = id;
  }

  protected apply(event: Omit<Event, 'id' | 'metadata'>): void {
    const fullEvent: Event = {
      ...event,
      id: `evt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      metadata: {
        timestamp: new Date(),
        version: this.version + 1,
      },
    };

    this.applyEvent(fullEvent);
    this.uncommittedEvents.push(fullEvent);
  }

  protected abstract applyEvent(event: Event): void;

  getUncommittedEvents(): Event[] {
    return [...this.uncommittedEvents];
  }

  clearUncommittedEvents(): void {
    this.uncommittedEvents = [];
  }

  getVersion(): number {
    return this.version;
  }

  getId(): string {
    return this.id;
  }
}

// Order Aggregate
interface OrderState {
  id: string;
  userId: string;
  items: Array<{ productId: string; quantity: number; price: number }>;
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';
  totalAmount: number;
  createdAt: Date;
  updatedAt: Date;
}

class OrderAggregate extends AggregateRoot {
  private state: OrderState | null = null;

  constructor(id: string) {
    super(id);
  }

  static create(id: string, userId: string, items: any[]): OrderAggregate {
    const order = new OrderAggregate(id);
    order.apply({
      aggregateId: id,
      aggregateType: 'Order',
      type: 'OrderCreated',
      data: {
        userId,
        items,
        status: 'pending',
        totalAmount: items.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        ),
      },
    });
    return order;
  }

  addItem(productId: string, quantity: number, price: number): void {
    if (this.state?.status !== 'pending') {
      throw new Error('Can only add items to pending orders');
    }

    this.apply({
      aggregateId: this.id,
      aggregateType: 'Order',
      type: 'ItemAdded',
      data: { productId, quantity, price },
    });
  }

  confirm(): void {
    if (this.state?.status !== 'pending') {
      throw new Error('Can only confirm pending orders');
    }

    this.apply({
      aggregateId: this.id,
      aggregateType: 'Order',
      type: 'OrderConfirmed',
      data: {},
    });
  }

  ship(trackingNumber: string): void {
    if (this.state?.status !== 'confirmed') {
      throw new Error('Can only ship confirmed orders');
    }

    this.apply({
      aggregateId: this.id,
      aggregateType: 'Order',
      type: 'OrderShipped',
      data: { trackingNumber },
    });
  }

  cancel(reason: string): void {
    if (this.state?.status === 'shipped' || this.state?.status === 'delivered') {
      throw new Error('Cannot cancel shipped or delivered orders');
    }

    this.apply({
      aggregateId: this.id,
      aggregateType: 'Order',
      type: 'OrderCancelled',
      data: { reason },
    });
  }

  getState(): OrderState | null {
    return this.state ? { ...this.state } : null;
  }

  protected applyEvent(event: Event): void {
    this.version = event.metadata.version;

    switch (event.type) {
      case 'OrderCreated':
        this.state = {
          id: event.aggregateId,
          userId: event.data.userId,
          items: event.data.items,
          status: 'pending',
          totalAmount: event.data.totalAmount,
          createdAt: event.metadata.timestamp,
          updatedAt: event.metadata.timestamp,
        };
        break;

      case 'ItemAdded':
        this.state!.items.push({
          productId: event.data.productId,
          quantity: event.data.quantity,
          price: event.data.price,
        });
        this.state!.totalAmount += event.data.price * event.data.quantity;
        this.state!.updatedAt = event.metadata.timestamp;
        break;

      case 'OrderConfirmed':
        this.state!.status = 'confirmed';
        this.state!.updatedAt = event.metadata.timestamp;
        break;

      case 'OrderShipped':
        this.state!.status = 'shipped';
        this.state!.updatedAt = event.metadata.timestamp;
        break;

      case 'OrderCancelled':
        this.state!.status = 'cancelled';
        this.state!.updatedAt = event.metadata.timestamp;
        break;
    }
  }

  static rehydrate(id: string, events: Event[]): OrderAggregate {
    const order = new OrderAggregate(id);
    events.forEach(event => order.applyEvent(event));
    return order;
  }
}

```

### TypeScript - Projections

```typescript
interface Projection {
  name: string;
  version: number;
}

class ProjectionManager {
  private projections: Map<string, ProjectionHandler> = new Map();
  private eventStore: EventStore;

  constructor(eventStore: EventStore) {
    this.eventStore = eventStore;
  }

  register(name: string, handler: ProjectionHandler): void {
    this.projections.set(name, handler);
  }

  async rebuild(projectionName?: string): Promise<void> {
    const events = await this.eventStore.getEventsFromTimestamp(new Date(0));

    for (const [name, handler] of this.projections) {
      if (projectionName && name !== projectionName) continue;

      console.log(`Rebuilding projection: ${name}`);
      await handler.rebuild(events);
    }
  }

  async project(event: Event): Promise<void> {
    for (const [name, handler] of this.projections) {
      await handler.project(event);
    }
  }
}

interface ProjectionHandler {
  project(event: Event): Promise<void>;
  rebuild(events: Event[]): Promise<void>;
}

class OrderSummaryProjection implements ProjectionHandler {
  private orderSummaries: Map<string, any> = new Map();

  async project(event: Event): Promise<void> {
    if (event.aggregateType !== 'Order') return;

    let summary = this.orderSummaries.get(event.aggregateId) || {
      id: event.aggregateId,
      status: 'pending',
      itemCount: 0,
      totalAmount: 0,
      lastUpdated: null,
    };

    switch (event.type) {
      case 'OrderCreated':
        summary.userId = event.data.userId;
        summary.status = event.data.status;
        summary.totalAmount = event.data.totalAmount;
        summary.itemCount = event.data.items.length;
        break;

      case 'ItemAdded':
        summary.itemCount++;
        summary.totalAmount += event.data.price * event.data.quantity;
        break;

      case 'OrderConfirmed':
        summary.status = 'confirmed';
        break;

      case 'OrderShipped':
        summary.status = 'shipped';
        summary.trackingNumber = event.data.trackingNumber;
        break;

      case 'OrderCancelled':
        summary.status = 'cancelled';
        break;
    }

    summary.lastUpdated = event.metadata.timestamp;
    this.orderSummaries.set(event.aggregateId, summary);
  }

  async rebuild(events: Event[]): Promise<void> {
    this.orderSummaries.clear();
    for (const event of events) {
      await this.project(event);
    }
  }

  getOrderSummary(orderId: string): any {
    return this.orderSummaries.get(orderId);
  }

  getAllOrderSummaries(): any[] {
    return Array.from(this.orderSummaries.values());
  }
}

```

### TypeScript - CQRS with Event Sourcing

```typescript
// Command Side
class OrderCommandHandler {
  private eventStore: EventStore;
  private repository: OrderRepository;

  constructor(eventStore: EventStore) {
    this.eventStore = eventStore;
    this.repository = new OrderRepository(eventStore);
  }

  async createOrder(command: {
    orderId: string;
    userId: string;
    items: any[];
  }): Promise<void> {
    const order = OrderAggregate.create(
      command.orderId,
      command.userId,
      command.items
    );

    await this.repository.save(order);
  }

  async addItem(command: {
    orderId: string;
    productId: string;
    quantity: number;
    price: number;
  }): Promise<void> {
    const order = await this.repository.load(command.orderId);
    order.addItem(command.productId, command.quantity, command.price);
    await this.repository.save(order);
  }

  async confirmOrder(command: { orderId: string }): Promise<void> {
    const order = await this.repository.load(command.orderId);
    order.confirm();
    await this.repository.save(order);
  }

  async shipOrder(command: {
    orderId: string;
    trackingNumber: string;
  }): Promise<void> {
    const order = await this.repository.load(command.orderId);
    order.ship(command.trackingNumber);
    await this.repository.save(order);
  }

  async cancelOrder(command: {
    orderId: string;
    reason: string;
  }): Promise<void> {
    const order = await this.repository.load(command.orderId);
    order.cancel(command.reason);
    await this.repository.save(order);
  }
}

class OrderRepository {
  private eventStore: EventStore;

  constructor(eventStore: EventStore) {
    this.eventStore = eventStore;
  }

  async save(order: OrderAggregate): Promise<void> {
    const events = order.getUncommittedEvents();
    for (const event of events) {
      await this.eventStore.append(event);
    }
    order.clearUncommittedEvents();
  }

  async load(id: string): Promise<OrderAggregate> {
    const events = await this.eventStore.getEvents(id);
    if (events.length === 0) {
      throw new Error(`Order not found: ${id}`);
    }
    return OrderAggregate.rehydrate(id, events);
  }
}

// Query Side
class OrderQueryHandler {
  private projection: OrderSummaryProjection;

  constructor(projection: OrderSummaryProjection) {
    this.projection = projection;
  }

  async getOrder(orderId: string): Promise<any> {
    return this.projection.getOrderSummary(orderId);
  }

  async getAllOrders(): Promise<any[]> {
    return this.projection.getAllOrderSummaries();
  }

  async getOrdersByStatus(status: string): Promise<any[]> {
    return this.projection
      .getAllOrderSummaries()
      .filter(order => order.status === status);
  }

  async getOrdersByUser(userId: string): Promise<any[]> {
    return this.projection
      .getAllOrderSummaries()
      .filter(order => order.userId === userId);
  }
}

```

### TypeScript - Temporal Queries

```typescript
class TemporalQueryService {
  private eventStore: EventStore;

  constructor(eventStore: EventStore) {
    this.eventStore = eventStore;
  }

  async getStateAtTime(
    aggregateId: string,
    timestamp: Date
  ): Promise<any> {
    const events = await this.eventStore.getEvents(aggregateId);
    const filteredEvents = events.filter(
      e => e.metadata.timestamp <= timestamp
    );

    return this.reconstructState(filteredEvents);
  }

  async getStateAtVersion(
    aggregateId: string,
    version: number
  ): Promise<any> {
    const events = await this.eventStore.getEvents(aggregateId);
    const filteredEvents = events.filter(
      e => e.metadata.version <= version
    );

    return this.reconstructState(filteredEvents);
  }

  async getAggregateHistory(aggregateId: string): Promise<Event[]> {
    return this.eventStore.getEvents(aggregateId);
  }

  async getEventsInTimeRange(
    from: Date,
    to: Date
  ): Promise<Event[]> {
    const events = await this.eventStore.getEventsFromTimestamp(from);
    return events.filter(e => e.metadata.timestamp <= to);
  }

  private reconstructState(events: Event[]): any {
    let state: any = {};

    for (const event of events) {
      state = this.applyEvent(state, event);
    }

    return state;
  }

  private applyEvent(state: any, event: Event): any {
    switch (event.type) {
      case 'OrderCreated':
        return {
          id: event.aggregateId,
          userId: event.data.userId,
          items: event.data.items,
          status: event.data.status,
          totalAmount: event.data.totalAmount,
          createdAt: event.metadata.timestamp,
        };

      case 'ItemAdded':
        return {
          ...state,
          items: [
            ...state.items,
            {
              productId: event.data.productId,
              quantity: event.data.quantity,
              price: event.data.price,
            },
          ],
          totalAmount: state.totalAmount + event.data.price * event.data.quantity,
        };

      case 'OrderConfirmed':
        return { ...state, status: 'confirmed' };

      case 'OrderShipped':
        return {
          ...state,
          status: 'shipped',
          trackingNumber: event.data.trackingNumber,
        };

      case 'OrderCancelled':
        return { ...state, status: 'cancelled', cancelReason: event.data.reason };

      default:
        return state;
    }
  }
}

```

## Real-World Use Cases

### 1. Financial Systems

- Complete audit trail for transactions
- Regulatory compliance
- Temporal queries for reporting
- Reconciliation and debugging

### 2. E-Commerce

- Order history and tracking
- Customer behavior analysis
- Inventory management
- Returns and refunds

### 3. Healthcare

- Patient medical history
- Audit trail for compliance
- Temporal queries for diagnosis
- Research and analytics

### 4. IoT

- Device state history
- Telemetry data analysis
- Predictive maintenance
- Anomaly detection

## Common Mistakes

1. **Storing too many events** - Need event compaction/snapshots

2. **Not designing events carefully** - Events are immutable, hard to change

3. **Ignoring event versioning** - Schema evolution challenges

4. **No snapshot strategy** - Slow rebuilds

5. **Tight coupling to event structure** - Breaking changes

6. **Missing correlation IDs** - Can't trace event chains

7. **Not handling event ordering** - Critical for consistency

8. **Ignoring performance** - Event replay can be slow

## Best Practices

1. **Design events as facts** - Immutable, describe what happened

2. **Use event versioning** - For schema evolution

3. **Implement snapshots** - For performance optimization

4. **Include metadata** - Timestamp, correlation ID, causation ID

5. **Keep events small** - Store references, not full data

6. **Use idempotent handlers** - Events may be replayed

7. **Plan for event compaction** - Manage storage growth

8. **Monitor event throughput** - Performance and capacity planning

## Performance Considerations

- **Snapshots**: Periodically save state to avoid replaying all events
- **Event partitioning**: Distribute events across multiple stores
- **Parallel projection**: Build projections concurrently
- **Event compaction**: Remove old events or merge similar events
- **Indexing**: Index events for efficient querying

## Summary

Event Sourcing provides complete audit trails and temporal queries by storing immutable events. Combined with CQRS, it enables scalable read and write models. Key considerations include event design, versioning, and performance optimization.

## Cheat Sheet
```text
┌─────────────────────────────────────────────────────────┐
│                 EVENT SOURCING                          │
├─────────────────────────────────────────────────────────┤
│ CORE CONCEPTS:                                          │
│ • Event: Immutable fact that happened                   │
│ • Aggregate: Business entity emitting events            │
│ • Event Store: Persistent event storage                 │
│ • Projection: Read model built from events              │
│ • Snapshot: Saved state for performance                 │
│                                                         │
│ PATTERNS:                                               │
│ • CQRS: Separate read/write models                      │
│ • Event Replay: Rebuild state from events               │
│ • Temporal Queries: State at point in time              │
│ • Event Versioning: Schema evolution                    │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Design events as immutable facts                      │
│ • Use event versioning                                  │
│ • Implement snapshots                                   │
│ • Include metadata (timestamp, correlation ID)          │
│ • Keep events small                                     │
│ • Use idempotent handlers                               │
│ • Plan for event compaction                             │
│ • Monitor event throughput                              │
│                                                         │
│ TRADE-OFFS:                                             │
│ ✓ Complete audit trail                                  │
│ ✓ Temporal queries                                      │
│ ✓ Event-driven integration                              │
│ ✗ Complexity                                            │
│ ✗ Eventual consistency                                  │
│ ✗ Storage growth                                        │
└─────────────────────────────────────────────────────────┘

```

---

## See Also
- [CQRS](13-CQRS.md)
- [Docker](../13-Docker/)
- [Kubernetes](../14-Kubernetes/)
- [NestJS](../06-NestJS/)
- [Strangler Fig](12-Strangler-Fig.md)
- [System Design](../11-System-Design/)

## References & Learn More

- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
