# CQRS (Command Query Responsibility Segregation)

## Definition

**CQRS (Command Query Responsibility Segregation)** is an architectural pattern that separates read and write operations into different models. **Commands** change state (create, update, delete) and **Queries** return data without modifying state. In NestJS, CQRS is implemented through the `@nestjs/cqrs` library, which provides decorators, buses, and handlers for commands, queries, and events.

## Why Do We Need It?

1. **Separation of Concerns**: Read and write models have different optimization strategies.
2. **Scalability**: Reads and writes can be scaled independently.
3. **Performance**: Optimized read models (projections) for queries, normalized write models for commands.
4. **Flexibility**: Different data stores for reads (Elasticsearch) and writes (PostgreSQL).
5. **Event Sourcing**: Natural fit for event-driven architectures.
6. **Testability**: Commands and queries can be tested independently.
7. **Complex Domains**: Simplifies complex business logic by separating concerns.

## How It Works

CQRS separates the application into two sides:
- **Command Side**: Handles state mutations (write operations)
- **Query Side**: Handles data retrieval (read operations)

```text
┌─────────────────────────────────────────────────────────────┐
│                    CQRS Architecture                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │   Client     │         │   Client     │                   │
│  └──────┬──────┘         └──────┬──────┘                   │
│         │ Command               │ Query                     │
│         ▼                       ▼                           │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │   Command   │         │    Query    │                   │
│  │   Bus       │         │    Bus      │                   │
│  └──────┬──────┘         └──────┬──────┘                   │
│         │                       │                           │
│         ▼                       ▼                           │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │   Command   │         │    Query    │                   │
│  │  Handler    │         │   Handler   │                   │
│  └──────┬──────┘         └──────┬──────┘                   │
│         │                       │                           │
│         ▼                       ▼                           │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │   Write     │         │    Read     │                   │
│  │   Model     │         │    Model    │                   │
│  │ (Database)  │         │ (Cache/ES)  │                   │
│  └──────┬──────┘         └─────────────┘                   │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Event Bus / Event Store                 │   │
│  │  (Projects write model to read model)               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### CQRS Flow

```text
Command Flow:
Client -> Command -> CommandBus -> CommandHandler -> WriteModel -> Event -> ReadModel

Query Flow:
Client -> Query -> QueryBus -> QueryHandler -> ReadModel -> Response
```

## Code Examples

### Command

```typescript
// create-user.command.ts
export class CreateUserCommand {
  constructor(
    public readonly name: string,
    public readonly email: string,
    public readonly password: string,
  ) {}
}
```

### Command Handler

```typescript
// create-user.handler.ts
import { ICommandHandler, CommandHandler } from '@nestjs/cqrs';
import { CreateUserCommand } from './create-user.command';
import { UserRepository } from '../repositories/user.repository';
import { User } from '../entities/user.entity';
import { hash } from 'bcrypt';

@CommandHandler(CreateUserCommand)
export class CreateUserHandler implements ICommandHandler<CreateUserCommand> {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly eventBus: EventBus,
  ) {}

  async execute(command: CreateUserCommand): Promise<User> {
    const hashedPassword = await hash(command.password, 10);

    const user = await this.userRepository.create({
      name: command.name,
      email: command.email,
      password: hashedPassword,
    });

    // Publish event for read model projection
    this.eventBus.publish(new UserCreatedEvent(user));

    return user;
  }
}
```

### Query

```typescript
// get-user.query.ts
export class GetUserQuery {
  constructor(public readonly id: string) {}
}

export class GetUsersQuery {
  constructor(
    public readonly page: number,
    public readonly limit: number,
  ) {}
}
```

### Query Handler

```typescript
// get-user.handler.ts
import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { GetUserQuery } from './get-user.query';
import { UserReadRepository } from '../repositories/user-read.repository';

@QueryHandler(GetUserQuery)
export class GetUserHandler implements IQueryHandler<GetUserQuery> {
  constructor(
    private readonly userReadRepository: UserReadRepository,
  ) {}

  async execute(query: GetUserQuery): Promise<UserDto> {
    return this.userReadRepository.findById(query.id);
  }
}

@QueryHandler(GetUsersQuery)
export class GetUsersHandler implements IQueryHandler<GetUsersQuery> {
  constructor(
    private readonly userReadRepository: UserReadRepository,
  ) {}

  async execute(query: GetUsersQuery): Promise<PaginatedResult<UserDto>> {
    return this.userReadRepository.findAll(query.page, query.limit);
  }
}
```

### Event

```typescript
// user-created.event.ts
export class UserCreatedEvent {
  constructor(
    public readonly userId: string,
    public readonly name: string,
    public readonly email: string,
    public readonly createdAt: Date,
  ) {}
}
```

### Event Handler

```typescript
// user-created.handler.ts
import { EventsHandler, IEventHandler } from '@nestjs/cqrs';
import { UserCreatedEvent } from './user-created.event';
import { UserReadRepository } from '../repositories/user-read.repository';

@EventsHandler(UserCreatedEvent)
export class UserCreatedHandler implements IEventHandler<UserCreatedEvent> {
  constructor(
    private readonly userReadRepository: UserReadRepository,
  ) {}

  async handle(event: UserCreatedEvent): Promise<void> {
    await this.userReadRepository.create({
      id: event.userId,
      name: event.name,
      email: event.email,
      createdAt: event.createdAt,
    });
  }
}
```

### Controller Using CQRS

```typescript
// user.controller.ts
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { CommandBus, QueryBus } from '@nestjs/cqrs';
import { CreateUserCommand } from './commands/create-user.command';
import { GetUserQuery } from './queries/get-user.query';
import { GetUsersQuery } from './queries/get-users.query';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UserController {
  constructor(
    private readonly commandBus: CommandBus,
    private readonly queryBus: QueryBus,
  ) {}

  @Post()
  async create(@Body() dto: CreateUserDto) {
    return this.commandBus.execute(
      new CreateUserCommand(dto.name, dto.email, dto.password),
    );
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.queryBus.execute(new GetUserQuery(id));
  }

  @Get()
  async findAll(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
  ) {
    return this.queryBus.execute(new GetUsersQuery(page, limit));
  }
}
```

### Module Configuration

```typescript
// user.module.ts
import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';
import { UserController } from './user.controller';
import { CreateUserHandler } from './commands/handlers/create-user.handler';
import { GetUserHandler } from './queries/handlers/get-user.handler';
import { GetUsersHandler } from './queries/handlers/get-users.handler';
import { UserCreatedHandler } from './events/handlers/user-created.handler';

const CommandHandlers = [CreateUserHandler];
const QueryHandlers = [GetUserHandler, GetUsersHandler];
const EventHandlers = [UserCreatedHandler];

@Module({
  imports: [CqrsModule],
  controllers: [UserController],
  providers: [
    ...CommandHandlers,
    ...QueryHandlers,
    ...EventHandlers,
    UserRepository,
    UserReadRepository,
  ],
})
export class UserModule {}
```

### Event Sourcing

```typescript
// aggregate-root.ts
export abstract class AggregateRoot {
  private domainEvents: DomainEvent[] = [];

  protected addEvent(event: DomainEvent): void {
    this.domainEvents.push(event);
  }

  getUncommittedEvents(): DomainEvent[] {
    return this.domainEvents;
  }

  commit(): void {
    this.domainEvents = [];
  }
}

// user.aggregate.ts
import { AggregateRoot } from './aggregate-root';
import { UserCreatedEvent } from '../events/user-created.event';
import { UserUpdatedEvent } from '../events/user-updated.event';

export class UserAggregate extends AggregateRoot {
  private id: string;
  private name: string;
  private email: string;

  static create(name: string, email: string): UserAggregate {
    const user = new UserAggregate();
    user.apply(new UserCreatedEvent(uuid(), name, email));
    return user;
  }

  update(name?: string, email?: string): void {
    if (name) this.name = name;
    if (email) this.email = email;
    this.apply(new UserUpdatedEvent(this.id, this.name, this.email));
  }

  private apply(event: DomainEvent): void {
    this.addEvent(event);
    this.applyEvent(event);
  }

  private applyEvent(event: DomainEvent): void {
    if (event instanceof UserCreatedEvent) {
      this.id = event.userId;
      this.name = event.name;
      this.email = event.email;
    }
  }
}
```

### Saga

```typescript
// order.saga.ts
import { Injectable, Logger } from '@nestjs/common';
import { Saga, ICommand, IEvent } from '@nestjs/cqrs';
import { Observable, of } from 'rxjs';
import { mergeMap } from 'rxjs/operators';
import { OrderCreatedEvent } from '../events/order-created.event';
import { ReserveInventoryCommand } from '../commands/reserve-inventory.command';
import { ProcessPaymentCommand } from '../commands/process-payment.command';
import { SendConfirmationEmailCommand } from '../commands/send-email.command';

@Injectable()
export class OrderSaga {
  private readonly logger = new Logger(OrderSaga.name);

  @Saga()
  orderCreated = (events$: Observable<IEvent>): Observable<ICommand> => {
    return events$.pipe(
      mergeMap((event) => {
        if (event instanceof OrderCreatedEvent) {
          this.logger.log(`Order created: ${event.orderId}`);
          return of(
            new ReserveInventoryCommand(event.orderId, event.items),
            new ProcessPaymentCommand(event.orderId, event.total),
            new SendConfirmationEmailCommand(event.orderId, event.customerEmail),
          );
        }
        return of();
      }),
    );
  };
}
```

## Real-World Use Cases

### 1. E-Commerce Order System

```typescript
// Command side
@CommandHandler(CreateOrderCommand)
export class CreateOrderHandler implements ICommandHandler<CreateOrderCommand> {
  async execute(command: CreateOrderCommand): Promise<Order> {
    // Validate business rules
    const order = OrderAggregate.create(command.customerId, command.items);
    await this.orderRepository.save(order);
    this.eventBus.publish(new OrderCreatedEvent(order));
    return order;
  }
}

// Query side - Optimized for reads
@QueryHandler(GetOrderSummaryQuery)
export class GetOrderSummaryHandler implements IQueryHandler<GetOrderSummaryQuery> {
  async execute(query: GetOrderSummaryQuery): Promise<OrderSummaryDto> {
    // Read from optimized read model (possibly different database)
    return this.orderReadModel.getSummary(query.orderId);
  }
}
```

### 2. Real-Time Analytics Dashboard

```typescript
// Write side: Track events
@CommandHandler(TrackPageViewCommand)
export class TrackPageViewHandler {
  async execute(command: TrackPageViewCommand): Promise<void> {
    await this.analyticsRepository.recordPageView(command);
    this.eventBus.publish(new PageViewTrackedEvent(command));
  }
}

// Read side: Aggregated data
@QueryHandler(GetDashboardQuery)
export class GetDashboardHandler {
  async execute(query: GetDashboardQuery): Promise<DashboardDto> {
    return this.analyticsReadModel.getDashboardData(query.dateRange);
  }
}
```

## Common Mistakes

### 1. Using CQRS for Simple CRUD

```typescript
// BAD: CQRS for simple CRUD adds unnecessary complexity
// When simple CRUD would suffice, don't use CQRS

// GOOD: Use CQRS when read/write models differ significantly
// Complex business rules, different read/write stores, event sourcing
```

### 2. Not Publishing Events

```typescript
// BAD: Command handler doesn't publish events
@CommandHandler(CreateUserCommand)
export class CreateUserHandler {
  async execute(command: CreateUserCommand) {
    await this.userRepository.create(command);
    // Read model never updated!
  }
}

// GOOD: Always publish events after state changes
@CommandHandler(CreateUserCommand)
export class CreateUserHandler {
  async execute(command: CreateUserCommand) {
    const user = await this.userRepository.create(command);
    this.eventBus.publish(new UserCreatedEvent(user));
    return user;
  }
}
```

### 3. Query Handlers Accessing Write Model

```typescript
// BAD: Query handler uses write repository
@QueryHandler(GetUserQuery)
export class GetUserHandler {
  async execute(query: GetUserQuery) {
    return this.writeRepository.findById(query.id); // Wrong model
  }
}

// GOOD: Query handler uses read model
@QueryHandler(GetUserQuery)
export class GetUserHandler {
  async execute(query: GetUserQuery) {
    return this.readRepository.findById(query.id); // Correct model
  }
}
```

## Best Practices

1. **Start Simple**: Only use CQRS when read/write models differ significantly.
2. **Event-Driven**: Publish events after every state change.
3. **Read Model Optimization**: Optimize read models for query patterns.
4. **Idempotent Commands**: Make commands idempotent for retry safety.
5. **Event Store**: Use event store for audit trail and replay.
6. **Separate Databases**: Use different databases for reads and writes when beneficial.
7. **Testing**: Test commands and queries independently.

## Performance Considerations

1. **Eventual Consistency**: Read models may lag behind write models.
2. **Read Model Projections**: Can be resource-intensive.
3. **Event Store Growth**: Events accumulate — implement snapshots.
4. **Query Optimization**: Read models can be denormalized for fast reads.
5. **Scaling**: Commands and queries can scale independently.

## Interview Questions

### Beginner

**Q1: What is CQRS?**
Command Query Responsibility Segregation — separates read and write operations into different models.

**Q2: What is the difference between a command and a query?**
- Command: Changes state (create, update, delete)
- Query: Returns data without modifying state

**Q3: What is the role of the EventBus?**
Distributes events from command handlers to event handlers for projection updates.

**Q4: What is a projection in CQRS?**
A read model built from events, optimized for specific query patterns.

**Q5: When should you use CQRS?**
When read and write models differ significantly, or when you need event sourcing.

### Intermediate

**Q6: How does CQRS differ from traditional CRUD?**
Traditional CRUD uses one model for reads and writes. CQRS separates them, allowing independent optimization.

**Q7: What is event sourcing?**
Storing all state changes as a sequence of events, allowing state reconstruction.

**Q8: How do you handle eventual consistency?**
Use read-through caching, polling, or real-time notifications to sync read models.

**Q9: What is a saga in CQRS?**
A pattern for managing complex business processes that span multiple commands.

**Q10: How do you test CQRS components?**
Test command handlers, query handlers, and event handlers independently.

### Senior

**Q11: Design a CQRS system for a bank.**
Write side: Event-sourced account aggregate. Read side: Denormalized transaction history.

**Q12: How would you handle concurrent commands?**
Use optimistic locking, aggregate versioning, or pessimistic locking.

**Q13: Design event store implementation.**
Use append-only store with aggregate ID, version, event type, and payload.

**Q14: How would you implement read model rebuild?**
Replay all events from the beginning to reconstruct read models.

**Q15: Design a multi-tenant CQRS system.**
Partition events by tenant, create tenant-specific read models.

### FAANG-Style

**Q16: Design CQRS for a social media platform.**
Write side: User actions (posts, likes). Read side: News feed, notifications.

**Q17: How would you implement CQRS across microservices?**
Each service owns its events, use event bus (Kafka) for cross-service communication.

**Q18: Design CQRS for real-time analytics.**
Write side: Event stream. Read side: Pre-aggregated analytics dashboards.

**Q19: How would you handle schema evolution in events?**
Use upcasters, event versioning, or event adaptation.

**Q20: Design CQRS for a distributed system.**
Event-driven architecture, eventual consistency, saga pattern for distributed transactions.

### Follow-ups

**Q21: What are the trade-offs of CQRS?**
Increased complexity, eventual consistency, more infrastructure.

**Q22: How do you handle read model failures?**
Rebuild from events, implement read model redundancy.

**Q23: Can CQRS work with REST APIs?**
Yes, REST endpoints dispatch commands/queries through the bus.

**Q24: How do you monitor CQRS systems?**
Track command/query latency, event processing lag, read model freshness.

**Q25: What is the difference between CQRS and event sourcing?**
CQRS separates reads/writes. Event sourcing stores events. They're complementary but independent.

## Summary

CQRS separates read and write operations into different models, enabling independent optimization, scalability, and event-driven architectures. In NestJS, the `@nestjs/cqrs` library provides command/query buses, handlers, and events. CQRS is most valuable in complex domains with different read/write requirements.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| Command | Operation that changes state |
| Query | Operation that reads state |
| CommandBus | Dispatches commands to handlers |
| QueryBus | Dispatches queries to handlers |
| EventBus | Distributes events |
| CommandHandler | Handles specific commands |
| QueryHandler | Handles specific queries |
| EventHandler | Reacts to events |
| Projection | Read model built from events |
| Aggregate | Domain entity with business logic |
| Saga | Manages complex workflows |
| Event Store | Stores all state-changing events |

## References & Learn More

- [NestJS CQRS Official Docs](https://docs.nestjs.com/recipes/cqrs)
- [@nestjs/cqrs Library](https://github.com/kamilmysliwiec/nest-cqrs-example)
- [Martin Fowler - CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Event Sourcing Reference](https://microservices.io/patterns/data/event-sourcing.html)
