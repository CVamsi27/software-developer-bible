# Microservices

## Definition

**NestJS Microservices** are lightweight, independently deployable services that communicate over the network using various transport layers. NestJS provides a microservices architecture mode with built-in support for multiple transport protocols (TCP, Redis, Kafka, RabbitMQ, NATS, gRPC, MQTT) and communication patterns (request-response, event-based).

Each microservice is a complete NestJS application with its own controllers, services, and modules, communicating through message brokers.

## Why Do We Need It?

1. **Scalability**: Scale individual services independently.
2. **Fault Isolation**: Failure in one service doesn't crash others.
3. **Technology Flexibility**: Different services can use different databases.
4. **Team Autonomy**: Teams can work on services independently.
5. **Deployment**: Deploy individual services without affecting others.
6. **Performance**: Distribute load across multiple instances.
7. **Complexity Management**: Break monolith into manageable pieces.

## How It Works

NestJS microservices communicate using transport layers. The client sends messages to a message broker, which routes them to the appropriate service handler.

```text
┌─────────────────────────────────────────────────────────────┐
│                  NestJS Microservices Architecture           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   API       │    │   API       │    │   API       │    │
│  │   Gateway   │    │   Gateway   │    │   Gateway   │    │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Message Broker                          │   │
│  │         (Redis / Kafka / RabbitMQ / NATS)           │   │
│  └──────┬──────────────┬──────────────┬───────────────┘   │
│         │              │              │                    │
│         ▼              ▼              ▼                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │
│  │   User      │ │   Order     │ │   Payment   │         │
│  │  Service    │ │  Service    │ │  Service    │         │
│  │             │ │             │ │             │         │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │         │
│  │ │  TCP    │ │ │ │  TCP    │ │ │ │  TCP    │ │         │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │         │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │         │
│  │ │Database │ │ │ │Database │ │ │ │Database │ │         │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │         │
│  └─────────────┘ └─────────────┘ └─────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Transport Layers

| Transport | Use Case | Pros | Cons |
|-----------|----------|------|------|
| TCP | Default, simple | Fast, no dependencies | No persistence |
| Redis | Common, pub/sub | Persistent, fast | Memory limitations |
| Kafka | Event streaming | High throughput, durable | Complex setup |
| RabbitMQ | Message queuing | Flexible routing, reliable | Additional infrastructure |
| NATS | Lightweight messaging | Fast, simple | Limited features |
| gRPC | High-performance RPC | Binary protocol, streaming | Complex contracts |
| MQTT | IoT messaging | Lightweight, pub/sub | Limited features |

## Code Examples

### Basic Microservice Setup

```typescript
// main.ts (microservice)
import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.TCP,
      options: {
        host: '127.0.0.1',
        port: 3001,
      },
    },
  );

  await app.listen();
}
bootstrap();
```

### Message Pattern (Request-Response)

```typescript
// user.controller.ts
import { Controller } from '@nestjs/common';
import { MessagePattern, Payload } from '@nestjs/microservices';
import { UserService } from './user.service';

@Controller()
export class UserController {
  constructor(private readonly userService: UserService) {}

  @MessagePattern({ cmd: 'get_user' })
  async getUser(@Payload() data: { id: string }) {
    return this.userService.findOne(data.id);
  }

  @MessagePattern({ cmd: 'create_user' })
  async createUser(@Payload() data: CreateUserDto) {
    return this.userService.create(data);
  }

  @MessagePattern({ cmd: 'get_users' })
  async getUsers(@Payload() data: { page: number; limit: number }) {
    return this.userService.findAll(data.page, data.limit);
  }
}
```

### Event Pattern

```typescript
// user.controller.ts
@Controller()
export class UserController {
  @EventPattern('user_created')
  async handleUserCreated(@Payload() data: UserCreatedEvent) {
    // Handle event (no response returned)
    await this.notificationService.sendWelcomeEmail(data.email);
  }

  @EventPattern('order_placed')
  async handleOrderPlaced(@Payload() data: OrderPlacedEvent) {
    await this.inventoryService.reserveStock(data.items);
  }
}
```

### Client (API Gateway)

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';

@Module({
  imports: [
    ClientsModule.register([
      {
        name: 'USER_SERVICE',
        transport: Transport.TCP,
        options: {
          host: '127.0.0.1',
          port: 3001,
        },
      },
      {
        name: 'ORDER_SERVICE',
        transport: Transport.TCP,
        options: {
          host: '127.0.0.1',
          port: 3002,
        },
      },
    ]),
  ],
})
export class AppModule {}
```

### Client Service

```typescript
// user-client.service.ts
import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';

@Injectable()
export class UserClientService {
  constructor(
    @Inject('USER_SERVICE')
    private readonly client: ClientProxy,
  ) {}

  async getUser(id: string) {
    return this.client.send({ cmd: 'get_user' }, { id }).toPromise();
  }

  async createUser(dto: CreateUserDto) {
    return this.client.send({ cmd: 'create_user' }, dto).toPromise();
  }

  // Event (fire-and-forget)
  async userCreated(event: UserCreatedEvent) {
    this.client.emit('user_created', event);
  }
}
```

### TCP Transport

```typescript
// Microservice
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.TCP,
    options: {
      host: '0.0.0.0',
      port: 3001,
    },
  },
);

// Client
ClientsModule.register([
  {
    name: 'SERVICE',
    transport: Transport.TCP,
    options: { host: '127.0.0.1', port: 3001 },
  },
]);
```

### Redis Transport

```typescript
// Microservice
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.REDIS,
    options: {
      host: 'localhost',
      port: 6379,
    },
  },
);

// Client
ClientsModule.register([
  {
    name: 'SERVICE',
    transport: Transport.REDIS,
    options: { host: 'localhost', port: 6379 },
  },
]);
```

### Kafka Transport

```typescript
// Microservice
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.KAFKA,
    options: {
      client: {
        clientId: 'user-service',
        brokers: ['localhost:9092'],
      },
      consumer: {
        groupId: 'user-service-consumer',
      },
    },
  },
);

// Client
ClientsModule.register([
  {
    name: 'SERVICE',
    transport: Transport.KAFKA,
    options: {
      client: {
        clientId: 'api-gateway',
        brokers: ['localhost:9092'],
      },
      consumer: {
        groupId: 'api-gateway-consumer',
      },
    },
  },
]);

// Message pattern for Kafka
@MessagePattern('user-topic')
async handleUserTopic(@Payload() message: KafkaMessage) {
  console.log(message.value);
}
```

### RabbitMQ Transport

```typescript
// Microservice
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.RMQ,
    options: {
      urls: ['amqp://localhost:5672'],
      queue: 'users_queue',
      queueOptions: { durable: false },
    },
  },
);

// Client
ClientsModule.register([
  {
    name: 'SERVICE',
    transport: Transport.RMQ,
    options: {
      urls: ['amqp://localhost:5672'],
      queue: 'users_queue',
      queueOptions: { durable: false },
    },
  },
]);
```

### gRPC Transport

```typescript
// Proto file: user.proto
syntax = "proto3";
package users;
service UserService {
  rpc GetUser (GetUserRequest) returns (UserResponse);
  rpc CreateUser (CreateUserRequest) returns (UserResponse);
}
message GetUserRequest { string id = 1; }
message CreateUserRequest { string name = 1; string email = 2; }
message UserResponse { string id = 1; string name = 2; string email = 3; }

// Microservice
const app = await NestFactory.createMicroservice<MicroserviceOptions>(
  AppModule,
  {
    transport: Transport.GRPC,
    options: {
      package: 'users',
      protoPath: join(__dirname, 'user.proto'),
      url: '0.0.0.0:5000',
    },
  },
);

// Controller
@Controller()
export class UserController {
  @GrpcMethod('UserService', 'GetUser')
  getUser(data: { id: string }): UserResponse {
    return { id: data.id, name: 'John', email: 'john@example.com' };
  }
}
```

### Exception Handling in Microservices

```typescript
// Exception filter for microservices
@Catch()
export class MicroserviceExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToRpc();
    const context = ctx.getContext();

    if (exception instanceof RpcException) {
      throw exception;
    }

    throw new RpcException({
      statusCode: 500,
      message: 'Internal server error',
    });
  }
}

// Using in controller
@Controller()
@UseFilters(MicroserviceExceptionFilter)
export class UserController {
  // ...
}
```

### Health Checks

```typescript
// health.controller.ts
import { Controller, Get } from '@nestjs/common';
import {
  HealthCheck,
  HealthCheckService,
  TcpHealthIndicator,
  MemoryHealthIndicator,
} from '@nestjs/terminus';

@Controller('health')
export class HealthController {
  constructor(
    private health: HealthCheckService,
    private tcp: TcpHealthIndicator,
    private memory: MemoryHealthIndicator,
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.tcp.pingCheck('tcp-service', 'tcp://127.0.0.1:3001'),
      () => this.memory.checkRSS('memory', 300 * 1024 * 1024),
    ]);
  }
}
```

### Service Discovery

```typescript
// Using Consul for service discovery
@Module({
  imports: [
    ClientsModule.registerAsync([
      {
        name: 'USER_SERVICE',
        useFactory: (consulService: ConsulService) => ({
          transport: Transport.TCP,
          options: {
            host: consulService.getAddress('user-service'),
            port: consulService.getPort('user-service'),
          },
        }),
        inject: [ConsulService],
      },
    ]),
  ],
})
export class AppModule {}
```

## Real-World Use Cases

### 1. E-Commerce Microservices

```text
┌─────────────────────────────────────────────────────────────┐
│                 E-Commerce Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  API Gateway (Kong/NestJS)                                  │
│         │                                                   │
│         ├── User Service (PostgreSQL)                       │
│         ├── Product Service (MongoDB)                       │
│         ├── Order Service (PostgreSQL)                      │
│         ├── Payment Service (PostgreSQL)                    │
│         ├── Inventory Service (Redis)                       │
│         ├── Notification Service (SendGrid)                 │
│         └── Analytics Service (Elasticsearch)               │
│                                                             │
│  Communication: Kafka for events, TCP for commands          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Real-Time Chat System

```typescript
// Message service
@Controller()
export class MessageController {
  @EventPattern('new_message')
  async handleMessage(@Payload() data: NewMessageEvent) {
    await this.messageRepository.save(data);
    this.eventEmitter.emit('message_broadcast', data);
  }
}

// Presence service
@Controller()
export class PresenceController {
  @EventPattern('user_online')
  async handleUserOnline(@Payload() data: UserOnlineEvent) {
    await this.redis.set(`user:${data.userId}:status`, 'online');
  }
}
```

### 3. Event-Driven Analytics

```typescript
// Event collector service
@Controller()
export class EventCollectorController {
  @EventPattern('page_view')
  async handlePageView(@Payload() data: PageViewEvent) {
    await this.kafkaProducer.send({
      topic: 'analytics-events',
      messages: [{ value: JSON.stringify(data) }],
    });
  }
}
```

## Common Mistakes

### 1. Synchronous Communication Between Services

```typescript
// BAD: Synchronous calls create tight coupling
async createOrder(dto: CreateOrderDto) {
  const user = await this.userClient.send({ cmd: 'get_user' }, { id: dto.userId }).toPromise();
  const product = await this.productClient.send({ cmd: 'get_product' }, { id: dto.productId }).toPromise();
  // Creates dependency chain
}

// GOOD: Use events for loose coupling
async createOrder(dto: CreateOrderDto) {
  const order = await this.orderService.create(dto);
  this.eventBus.publish(new OrderCreatedEvent(order));
  // Other services react independently
}
```

### 2. Not Handling Service Failures

```typescript
// BAD: No error handling
async getUser(id: string) {
  return this.client.send({ cmd: 'get_user' }, { id }).toPromise();
}

// GOOD: Handle failures gracefully
async getUser(id: string) {
  try {
    return await this.client.send({ cmd: 'get_user' }, { id }).toPromise();
  } catch (error) {
    this.logger.error(`Failed to get user: ${error.message}`);
    throw new ServiceUnavailableException('User service unavailable');
  }
}
```

### 3. Missing Health Checks

```typescript
// BAD: No health checks
// Services can fail silently

// GOOD: Implement health checks
@Get('health')
@HealthCheck()
check() {
  return this.health.check([
    () => this.tcp.pingCheck('user-service', 'tcp://127.0.0.1:3001'),
  ]);
}
```

## Best Practices

1. **Service Independence**: Each service owns its data and logic.
2. **API Contracts**: Define clear contracts between services.
3. **Event-Driven**: Use events for loose coupling.
4. **Health Checks**: Implement health checks for all services.
5. **Circuit Breakers**: Implement circuit breakers for fault tolerance.
6. **Distributed Tracing**: Use correlation IDs across services.
7. **Graceful Degradation**: Services should degrade gracefully when dependencies fail.
8. **Containerization**: Use Docker/Kubernetes for deployment.

## Performance Considerations

1. **Message Broker Selection**: Choose based on throughput and durability needs.
2. **Connection Pooling**: Reuse connections to message brokers.
3. **Batch Processing**: Batch messages when possible.
4. **Async Communication**: Prefer async over sync for loose coupling.
5. **Load Balancing**: Distribute messages across service instances.

## Interview Questions

### Beginner

**Q1: What is a microservice in NestJS?**
A lightweight, independently deployable service communicating over the network using message patterns and transport layers.

**Q2: What is the difference between message patterns and event patterns?**
- Message pattern: Request-response (expects response)
- Event pattern: Fire-and-forget (no response)

**Q3: What transport layers does NestJS support?**
TCP, Redis, Kafka, RabbitMQ, NATS, gRPC, MQTT.

**Q4: How do you create a microservice in NestJS?**
Use `NestFactory.createMicroservice()` with transport options.

**Q5: How do clients communicate with microservices?**
Using `ClientProxy` with `send()` for commands and `emit()` for events.

### Intermediate

**Q6: What is the difference between TCP and Redis transport?**
- TCP: Direct connection, fast, no persistence
- Redis: Through Redis, supports pub/sub, persistent

**Q7: How do you handle errors in microservices?**
Use exception filters, implement retry logic, and circuit breakers.

**Q8: How do you implement service discovery?**
Use Consul, Eureka, or Kubernetes service discovery.

**Q9: How do you handle distributed transactions?**
Use saga pattern, eventual consistency, or two-phase commit.

**Q10: How do you test microservices?**
Use integration tests with test containers, mock external services.

### Senior

**Q11: Design a microservices architecture for a social media platform.**
Services: User, Post, Feed, Notification, Search, Analytics. Kafka for events, Redis for caching, PostgreSQL/MongoDB for storage.

**Q12: How would you implement distributed tracing?**
Use OpenTelemetry, propagate trace headers through services, export to Jaeger/Zipkin.

**Q13: Design a circuit breaker for microservices.**
Track failures, open circuit after threshold, fallback to cached/default response.

**Q14: How would you handle data consistency across services?**
Use saga pattern for distributed transactions, eventual consistency with event sourcing.

**Q15: Design a service mesh for microservices.**
Use Istio/Linkerd for service-to-service communication, load balancing, and security.

### FAANG-Style

**Q16: Design a microservices system for Netflix-scale streaming.**
Services: User, Content, Recommendation, Streaming, Billing. Kafka for events, Cassandra for storage, Redis for caching.

**Q17: How would you implement zero-downtime deployments?**
Blue-green deployments, rolling updates, canary releases with feature flags.

**Q18: Design a multi-region microservices architecture.**
Data replication, regional routing, failover mechanisms.

**Q19: How would you implement rate limiting across services?**
Centralized rate limiter at API gateway, distributed rate limiting with Redis.

**Q20: Design a microservices system for real-time gaming.**
WebSocket connections, game state synchronization, matchmaking service.

### Follow-ups

**Q21: How do you handle service versioning?**
API versioning, backward compatibility, feature flags.

**Q22: What is the CAP theorem and how does it apply?**
Consistency, Availability, Partition tolerance — choose two. Microservices typically favor availability and partition tolerance.

**Q23: How do you handle service authentication?**
Mutual TLS, JWT tokens, OAuth2 between services.

**Q24: How do you monitor microservices?**
Centralized logging (ELK), metrics (Prometheus), distributed tracing.

**Q25: When should you NOT use microservices?**
Small teams, simple domains, early-stage products, tight coupling requirements.

## Summary

NestJS Microservices provide a complete framework for building distributed systems with multiple transport layers. They enable independent scaling, deployment, and technology choices. Key concepts include message/event patterns, transport selection, service discovery, and fault tolerance. Microservices are best suited for complex domains with clear service boundaries.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `createMicroservice()` | Create a microservice application |
| `@MessagePattern()` | Handle request-response messages |
| `@EventPattern()` | Handle fire-and-forget events |
| `ClientProxy` | Client for sending messages |
| `send()` | Send request-response message |
| `emit()` | Send event (fire-and-forget) |
| `Transport.TCP` | TCP transport |
| `Transport.REDIS` | Redis transport |
| `Transport.KAFKA` | Kafka transport |
| `Transport.RMQ` | RabbitMQ transport |
| `Transport.GRPC` | gRPC transport |
| `@Payload()` | Extract message payload |
| `RpcException` | Exception for microservices |
| `ClientsModule` | Register microservice clients |

## References & Learn More

- [NestJS Microservices Official Docs](https://docs.nestjs.com/microservices/basics)
- [NestJS Transport Layers](https://docs.nestjs.com/microservices/basics#transporters)
- [NestJS Redis Microservice](https://docs.nestjs.com/microservices/redis)
- [NestJS Kafka Microservice](https://docs.nestjs.com/microservices/kafka)
- [NestJS RabbitMQ Microservice](https://docs.nestjs.com/microservices/rabbitmq)
