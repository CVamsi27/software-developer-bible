# Saga Pattern

## Definition

Saga Pattern is a design pattern for managing distributed transactions across multiple microservices. Instead of using a single ACID transaction, sagas break the transaction into a sequence of local transactions, each publishing events that trigger the next step. If any step fails, compensating transactions are executed to undo previous work.

## Why Do We Need It?

In microservices:

- Traditional distributed transactions (2PC) are complex and slow
- Services own their data, can't share database transactions
- Need eventual consistency across services
- Long-running business processes span multiple services
- Must handle failures gracefully without data corruption

## How It Works

### Choreography-Based Saga

```text
┌─────────────┐    OrderCreated    ┌─────────────┐
│   Order     │───────────────────>│  Inventory  │
│   Service   │                    │  Service    │
└─────────────┘                    └──────┬──────┘
                                          │
                                   InventoryReserved
                                          │
                                          ▼
┌─────────────┐    PaymentProcessed ┌─────────────┐
│  Shipping   │<───────────────────│  Payment    │
│  Service    │                    │  Service    │
└─────────────┘                    └─────────────┘

Event Flow:

1. Order Service publishes OrderCreated

2. Inventory Service reserves stock, publishes InventoryReserved

3. Payment Service processes payment, publishes PaymentProcessed

4. Shipping Service prepares shipment

Failure Flow:

1. Payment fails → Publishes PaymentFailed

2. Inventory Service receives PaymentFailed → Releases stock

3. Order Service receives PaymentFailed → Cancels order

```

### Orchestration-Based Saga

```text
                    ┌─────────────────┐
                    │   Saga          │
                    │   Orchestrator  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Order     │       │  Inventory  │       │  Payment    │
│   Service   │       │  Service    │       │  Service    │
└─────────────┘       └─────────────┘       └─────────────┘

Flow:

1. Orchestrator sends CreateOrder to Order Service

2. Orchestrator sends ReserveInventory to Inventory Service

3. Orchestrator sends ProcessPayment to Payment Service

4. If success: Send ShipOrder to Shipping Service

5. If failure: Execute compensating transactions

```

## Code Examples

### TypeScript - Saga Orchestrator

```typescript
enum SagaStepStatus {
  PENDING = 'PENDING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  COMPENSATED = 'COMPENSATED',
}

interface SagaStep<T> {
  name: string;
  execute: (context: T) => Promise<void>;
  compensate: (context: T) => Promise<void>;
  status: SagaStepStatus;
}

interface SagaConfig {
  maxRetries: number;
  retryDelay: number;
  timeout: number;
}

class SagaOrchestrator<T> {
  private steps: SagaStep<T>[] = [];
  private config: SagaConfig;

  constructor(config: Partial<SagaConfig> = {}) {
    this.config = {
      maxRetries: config.maxRetries || 3,
      retryDelay: config.retryDelay || 1000,
      timeout: config.timeout || 30000,
    };
  }

  addStep(
    name: string,
    execute: (context: T) => Promise<void>,
    compensate: (context: T) => Promise<void>
  ): this {
    this.steps.push({
      name,
      execute,
      compensate,
      status: SagaStepStatus.PENDING,
    });
    return this;
  }

  async execute(context: T): Promise<{ success: boolean; error?: string }> {
    const completedSteps: SagaStep<T>[] = [];

    for (const step of this.steps) {
      try {
        await this.executeWithRetry(step, context);
        step.status = SagaStepStatus.COMPLETED;
        completedSteps.push(step);
        console.log(`Step ${step.name} completed`);
      } catch (error) {
        console.error(`Step ${step.name} failed:`, error);
        step.status = SagaStepStatus.FAILED;

        // Compensate completed steps in reverse order
        await this.compensate(completedSteps.reverse(), context);
        return {
          success: false,
          error: `Failed at step ${step.name}: ${error}`
        };
      }
    }

    return { success: true };
  }

  private async executeWithRetry(step: SagaStep<T>, context: T): Promise<void> {
    let lastError: Error | null = null;

    for (let attempt = 1; attempt <= this.config.maxRetries; attempt++) {
      try {
        await Promise.race([
          step.execute(context),
          this.timeoutPromise(),
        ]);
        return;
      } catch (error) {
        lastError = error as Error;
        console.warn(
          `Step ${step.name} attempt ${attempt} failed, retrying...`
        );

        if (attempt < this.config.maxRetries) {
          await this.delay(this.config.retryDelay * attempt);
        }
      }
    }

    throw lastError;
  }

  private async compensate(steps: SagaStep<T>[], context: T): Promise<void> {
    for (const step of steps) {
      try {
        await step.compensate(context);
        step.status = SagaStepStatus.COMPENSATED;
        console.log(`Compensated step ${step.name}`);
      } catch (error) {
        console.error(`Failed to compensate step ${step.name}:`, error);
        // In production: alert, manual intervention, dead letter queue
      }
    }
  }

  private timeoutPromise(): Promise<never> {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Step timeout')), this.config.timeout);
    });
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

```

### TypeScript - Order Saga Implementation

```typescript
interface OrderContext {
  orderId: string;
  userId: string;
  items: Array<{ productId: string; quantity: number; price: number }>;
  totalAmount: number;
  paymentId?: string;
  inventoryReservationId?: string;
}

class OrderSaga {
  private saga: SagaOrchestrator<OrderContext>;

  constructor(
    private orderService: OrderService,
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
    private shippingService: ShippingService
  ) {
    this.saga = new SagaOrchestrator<OrderContext>({ maxRetries: 3 });
    this.setupSteps();
  }

  private setupSteps(): void {
    this.saga
      .addStep(
        'CreateOrder',
        async (ctx) => {
          const order = await this.orderService.create({
            id: ctx.orderId,
            userId: ctx.userId,
            items: ctx.items,
            totalAmount: ctx.totalAmount,
            status: 'PENDING',
          });
          ctx.orderId = order.id;
        },
        async (ctx) => {
          await this.orderService.cancel(ctx.orderId);
        }
      )
      .addStep(
        'ReserveInventory',
        async (ctx) => {
          const reservation = await this.inventoryService.reserve({
            orderId: ctx.orderId,
            items: ctx.items,
          });
          ctx.inventoryReservationId = reservation.id;
        },
        async (ctx) => {
          if (ctx.inventoryReservationId) {
            await this.inventoryService.release(ctx.inventoryReservationId);
          }
        }
      )
      .addStep(
        'ProcessPayment',
        async (ctx) => {
          const payment = await this.paymentService.charge({
            orderId: ctx.orderId,
            userId: ctx.userId,
            amount: ctx.totalAmount,
          });
          ctx.paymentId = payment.id;
        },
        async (ctx) => {
          if (ctx.paymentId) {
            await this.paymentService.refund(ctx.paymentId);
          }
        }
      )
      .addStep(
        'ConfirmOrder',
        async (ctx) => {
          await this.orderService.confirm(ctx.orderId);
        },
        async (ctx) => {
          await this.orderService.cancel(ctx.orderId);
        }
      )
      .addStep(
        'InitiateShipping',
        async (ctx) => {
          await this.shippingService.initiate({
            orderId: ctx.orderId,
            items: ctx.items,
          });
        },
        async (ctx) => {
          await this.shippingService.cancel(ctx.orderId);
        }
      );
  }

  async placeOrder(context: OrderContext): Promise<{ success: boolean; orderId?: string; error?: string }> {
    const result = await this.saga.execute(context);

    if (result.success) {
      return { success: true, orderId: context.orderId };
    }

    return { success: false, error: result.error };
  }
}

// Service interfaces (simplified)
interface OrderService {
  create(order: any): Promise<any>;
  confirm(orderId: string): Promise<void>;
  cancel(orderId: string): Promise<void>;
}

interface InventoryService {
  reserve(data: any): Promise<any>;
  release(reservationId: string): Promise<void>;
}

interface PaymentService {
  charge(data: any): Promise<any>;
  refund(paymentId: string): Promise<void>;
}

interface ShippingService {
  initiate(data: any): Promise<void>;
  cancel(orderId: string): Promise<void>;
}

```

### TypeScript - Choreography-Based Saga

```typescript
enum EventType {
  ORDER_CREATED = 'ORDER_CREATED',
  INVENTORY_RESERVED = 'INVENTORY_RESERVED',
  INVENTORY_FAILED = 'INVENTORY_FAILED',
  PAYMENT_PROCESSED = 'PAYMENT_PROCESSED',
  PAYMENT_FAILED = 'PAYMENT_FAILED',
  ORDER_COMPLETED = 'ORDER_COMPLETED',
  ORDER_CANCELLED = 'ORDER_CANCELLED',
}

interface DomainEvent {
  type: EventType;
  payload: any;
  timestamp: Date;
  correlationId: string;
}

class EventStore {
  private events: DomainEvent[] = [];

  publish(event: DomainEvent): void {
    this.events.push(event);
    this.emit(event);
  }

  private emit(event: DomainEvent): void {
    // In production: use message broker (Kafka, RabbitMQ)
    console.log(`Event published: ${event.type}`, event.payload);
  }

  getEvents(correlationId: string): DomainEvent[] {
    return this.events.filter(e => e.correlationId === correlationId);
  }
}

class OrderEventHandler {
  constructor(private eventStore: EventStore) {
    this.subscribe();
  }

  private subscribe(): void {
    // In production: subscribe to message broker
    console.log('OrderEventHandler subscribed to events');
  }

  async handleOrderCreated(event: DomainEvent): Promise<void> {
    const { orderId, items } = event.payload;

    // Validate order
    if (!items || items.length === 0) {
      this.eventStore.publish({
        type: EventType.ORDER_CANCELLED,
        payload: { orderId, reason: 'Empty order' },
        timestamp: new Date(),
        correlationId: event.correlationId,
      });
      return;
    }

    // Request inventory reservation
    console.log(`Order ${orderId}: Requesting inventory reservation`);
    // In production: call inventory service or publish event
  }

  async handleInventoryReserved(event: DomainEvent): Promise<void> {
    const { orderId, reservationId } = event.payload;
    console.log(`Order ${orderId}: Inventory reserved, processing payment`);
    // Process payment
  }

  async handlePaymentProcessed(event: DomainEvent): Promise<void> {
    const { orderId } = event.payload;
    console.log(`Order ${orderId}: Payment processed, completing order`);

    this.eventStore.publish({
      type: EventType.ORDER_COMPLETED,
      payload: { orderId },
      timestamp: new Date(),
      correlationId: event.correlationId,
    });
  }

  async handlePaymentFailed(event: DomainEvent): Promise<void> {
    const { orderId, reason } = event.payload;
    console.log(`Order ${orderId}: Payment failed, compensating`);

    // Release inventory (compensation)
    console.log(`Order ${orderId}: Releasing inventory`);

    this.eventStore.publish({
      type: EventType.ORDER_CANCELLED,
      payload: { orderId, reason },
      timestamp: new Date(),
      correlationId: event.correlationId,
    });
  }
}

```

### TypeScript - Saga with NestJS

```typescript
// saga-step.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const SAGA_STEP_KEY = 'saga_step';
export const SagaStep = (name: string) => SetMetadata(SAGA_STEP_KEY, name);

// saga.module.ts
import { Module } from '@nestjs/common';
import { OrderSagaService } from './order-saga.service';
import { OrderModule } from '../order/order.module';
import { InventoryModule } from '../inventory/inventory.module';
import { PaymentModule } from '../payment/payment.module';

@Module({
  imports: [OrderModule, InventoryModule, PaymentModule],
  providers: [OrderSagaService],
  exports: [OrderSagaService],
})
export class SagaModule {}

// order-saga.service.ts
import { Injectable, Logger } from '@nestjs/common';
import { OrderService } from '../order/order.service';
import { InventoryService } from '../inventory/inventory.service';
import { PaymentService } from '../payment/payment.service';

@Injectable()
export class OrderSagaService {
  private readonly logger = new Logger(OrderSagaService.name);

  constructor(
    private orderService: OrderService,
    private inventoryService: InventoryService,
    private paymentService: PaymentService,
  ) {}

  async executeOrderSaga(orderData: any): Promise<any> {
    const correlationId = this.generateCorrelationId();
    this.logger.log(`Starting order saga: ${correlationId}`);

    let inventoryReservationId: string | null = null;
    let paymentId: string | null = null;
    let orderId: string | null = null;

    try {
      // Step 1: Create order
      orderId = await this.createOrder(orderData, correlationId);

      // Step 2: Reserve inventory
      inventoryReservationId = await this.reserveInventory(orderId, orderData.items);

      // Step 3: Process payment
      paymentId = await this.processPayment(orderId, orderData.totalAmount);

      // Step 4: Confirm order
      await this.confirmOrder(orderId);

      this.logger.log(`Order saga completed: ${correlationId}`);
      return { success: true, orderId };

    } catch (error) {
      this.logger.error(`Order saga failed: ${correlationId}`, error);

      // Execute compensating transactions
      await this.compensate(correlationId, {
        orderId,
        inventoryReservationId,
        paymentId,
      });

      return { success: false, error: error.message };
    }
  }

  private async createOrder(data: any, correlationId: string): Promise<string> {
    this.logger.log(`Creating order: ${correlationId}`);
    const order = await this.orderService.create({
      ...data,
      correlationId,
      status: 'PENDING',
    });
    return order.id;
  }

  private async reserveInventory(orderId: string, items: any[]): Promise<string> {
    this.logger.log(`Reserving inventory for order: ${orderId}`);
    const reservation = await this.inventoryService.reserve({
      orderId,
      items,
    });
    return reservation.id;
  }

  private async processPayment(orderId: string, amount: number): Promise<string> {
    this.logger.log(`Processing payment for order: ${orderId}`);
    const payment = await this.paymentService.charge({
      orderId,
      amount,
    });
    return payment.id;
  }

  private async confirmOrder(orderId: string): Promise<void> {
    this.logger.log(`Confirming order: ${orderId}`);
    await this.orderService.updateStatus(orderId, 'CONFIRMED');
  }

  private async compensate(correlationId: string, data: any): Promise<void> {
    this.logger.log(`Compensating order saga: ${correlationId}`);

    if (data.paymentId) {
      await this.paymentService.refund(data.paymentId);
    }

    if (data.inventoryReservationId) {
      await this.inventoryService.release(data.inventoryReservationId);
    }

    if (data.orderId) {
      await this.orderService.updateStatus(data.orderId, 'CANCELLED');
    }
  }

  private generateCorrelationId(): string {
    return `saga-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

```

## Real-World Use Cases

### 1. E-Commerce Order Processing

- Create order → Reserve inventory → Process payment → Ship order
- Compensation: Refund payment → Release inventory → Cancel order

### 2. Travel Booking

- Book flight → Book hotel → Book car → Process payment
- Compensation: Cancel car → Cancel hotel → Cancel flight → Refund

### 3. Banking Transfer

- Debit account A → Credit account B → Update ledger
- Compensation: Reverse debit → Reverse credit → Revert ledger

### 4. Insurance Claim

- Validate claim → Assess damage → Process payment → Update records
- Compensation: Reverse payment → Revert assessment → Cancel claim

## Common Mistakes

1. **Not designing compensation properly** - Every step needs undo capability

2. **Ignoring idempotency** - Steps may retry, must be safe to execute multiple times

3. **Missing correlation IDs** - Can't track saga progress

4. **Not handling timeout** - Steps may hang indefinitely

5. **Business logic in orchestrator** - Keep orchestrator thin

6. **Ignoring event ordering** - Events may arrive out of order

7. **Not logging saga progress** - Debugging becomes impossible

8. **Synchronous only** - Should support async processing

## Best Practices

1. **Design compensating transactions first** - Before implementing forward path

2. **Make all steps idempotent** - Safe to retry without side effects

3. **Use correlation IDs** - Track entire saga lifecycle

4. **Implement timeouts** - Prevent hung sagas

5. **Log everything** - Essential for debugging distributed systems

6. **Keep orchestrator thin** - Only coordinate, no business logic

7. **Use dead letter queues** - For failed compensation

8. **Monitor saga metrics** - Success rate, duration, failure points

## Performance Considerations

- **Async processing** - Don't block waiting for steps
- **Parallel execution** - Independent steps can run concurrently
- **Eventual consistency** - Accept delayed consistency for better performance
- **Caching** - Cache frequently accessed data
- **Connection pooling** - Reuse connections to services

## Interview Questions

### Beginner (5-10)

1. **What is the Saga pattern?**

   - Pattern for managing distributed transactions using local transactions and compensation.

2. **Why use Sagas instead of 2PC?**

   - Better performance, scalability, and availability; 2PC is blocking and slow.

3. **What is a compensating transaction?**

   - Undo operation that reverses the effect of a completed step.

4. **What's the difference between choreography and orchestration?**

   - Choreography: Services publish/subscribe to events
   - Orchestration: Central coordinator manages flow

5. **What is a saga orchestrator?**

   - Central service that coordinates the execution of saga steps.

6. **Why are correlation IDs important?**

   - Track and correlate all events/transactions in a saga.

7. **What happens when a saga step fails?**

   - Compensating transactions execute in reverse order.

8. **What is eventual consistency?**

   - System will become consistent over time, not immediately.

### Intermediate (5-10)

9. **How do you handle idempotency in sagas?**

   - Use unique operation IDs, check if operation already performed.

10. **What is a dead letter queue?**

    - Queue for messages that can't be processed, for later investigation.

11. **How do you handle timeouts in sagas?**

    - Set timeout for each step, trigger compensation on timeout.

12. **What is event sourcing in saga context?**

    - Store all state changes as events, can replay to reconstruct state.

13. **How do you handle concurrent sagas?**

    - Use optimistic locking, conflict detection, or serialization.

14. **What is a saga log?**

    - Persistent record of all saga events for recovery and auditing.

15. **How do you test sagas?**

    - Unit test each step, integration test full flow, chaos testing.

16. **What metrics should you monitor?**

    - Saga completion rate, step failure rate, compensation frequency.

### Senior (10-15)

17. **Design a saga orchestrator from scratch.**

    - State machine, event handling, compensation logic, monitoring.

18. **How do you handle saga failures that can't be compensated?**

    - Manual intervention, alerting, dead letter queues, reconciliation.

19. **What is the relationship between sagas and CQRS?**

    - Sagas for write side, CQRS for read side, events connect them.

20. **How do you implement saga persistence?**

    - Database, event store, or distributed cache for saga state.

21. **Explain saga evolution patterns.**

    - Start with choreography, move to orchestration as complexity grows.

22. **How do you handle cross-organizational sagas?**

    - API contracts, event standards, distributed tracing.

23. **What is the role of message brokers in sagas?**

    - Asynchronous communication, event persistence, guaranteed delivery.

24. **How do you handle network partitions in sagas?**

    - Timeout, retry, circuit breaker, eventual consistency.

25. **Explain saga monitoring and observability.**

    - Distributed tracing, logging, metrics, alerting.

### FAANG-style (5-10)

26. **Design Netflix's order saga.**

    - Choreography-based, event-driven, multiple services, high throughput.

27. **How would you handle 100K sagas per second?**

    - Sharding, partitioning, async processing, eventual consistency.

28. **Design a saga system for global e-commerce.**

    - Multi-region, currency conversion, tax calculation, compliance.

29. **How do you ensure exactly-once processing in sagas?**

    - Idempotent operations, deduplication, transactional outbox.

30. **Explain saga patterns in event-driven architecture.**

    - Event choreography, event sourcing, CQRS integration.

### Follow-ups (5-10)

31. **How do you migrate from 2PC to sagas?**

    - Strangler fig pattern, gradual extraction, dual write.

32. **What are the limitations of sagas?**

    - Eventual consistency, complex compensation, no isolation.

33. **How do you handle saga debugging?**

    - Correlation IDs, distributed tracing, saga visualization.

34. **What is the future of saga patterns?**

    - Serverless sagas, AI-driven compensation, workflow engines.

35. **How do you choose between choreography and orchestration?**

    - Choreography for simple flows, orchestration for complex business logic.

## Summary

Saga Pattern enables distributed transactions in microservices using local transactions and compensation. Choose choreography for simple, decoupled flows or orchestration for complex business logic. Key considerations include idempotency, compensation design, and monitoring.

## Cheat Sheet

```text
┌─────────────────────────────────────────────────────────┐
│                   SAGA PATTERN                          │
├─────────────────────────────────────────────────────────┤
│ TYPES:                                                  │
│ • Choreography: Event-driven, decentralized             │
│ • Orchestration: Central coordinator                    │
│                                                         │
│ KEY CONCEPTS:                                           │
│ • Local Transaction: Single service operation           │
│ • Compensation: Undo previous operations                │
│ • Correlation ID: Track saga across services            │
│ • Saga Log: Persistent record of events                 │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Design compensation first                             │
│ • Make all steps idempotent                             │
│ • Use correlation IDs                                   │
│ • Implement timeouts                                    │
│ • Log everything                                        │
│ • Monitor saga metrics                                  │
│                                                         │
│ PATTERNS:                                               │
│ • Event Sourcing: Store state changes as events         │
│ • CQRS: Separate read/write sides                       │
│ • Dead Letter Queue: Handle failed events               │
│ • Transactional Outbox: Reliable event publishing       │
└─────────────────────────────────────────────────────────┘

```

---

## References & Learn More

- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)