# RabbitMQ

## Definition

RabbitMQ is an open-source message broker that implements the Advanced Message Queuing Protocol (AMQP). It provides reliable, flexible messaging between services with features like routing, acknowledgment, dead letter queues, and multiple messaging patterns (pub/sub, work queues, request/reply).

## Why Do We Need It?

In microservices:

- Decouple services through asynchronous messaging
- Ensure reliable message delivery with acknowledgments
- Support complex routing and message filtering
- Handle message retry and dead letter scenarios
- Provide protocol flexibility (AMQP, MQTT, STOMP)

## How It Works

### RabbitMQ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                      RABBITMQ BROKER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐     ┌─────────────────────────────────────┐   │
│   │  Producer   │────>│           EXCHANGE                   │   │
│   │  (Publisher)│     │  (Direct/Topic/Fanout/Headers)      │   │
│   └─────────────┘     └─────────────────┬───────────────────┘   │
│                                         │                       │
│                                         │ Binding               │
│                                         │ Rules                 │
│                                         ▼                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                      QUEUES                              │   │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│   │  │ Queue 1 │  │ Queue 2 │  │ Queue 3 │  │ Queue 4 │   │   │
│   │  │         │  │         │  │         │  │ (DLQ)   │   │   │
│   │  └────┬────┘  └────┬────┘  └────┬────┘  └─────────┘   │   │
│   └───────┼────────────┼────────────┼───────────────────────┘   │
│           │            │            │                           │
│           ▼            ▼            ▼                           │
│   ┌─────────────┐┌─────────────┐┌─────────────┐                │
│   │  Consumer   ││  Consumer   ││  Consumer   │                │
│   │  (Subscriber)││  (Subscriber)││  (Subscriber)│                │
│   └─────────────┘└─────────────┘└─────────────┘                │
└─────────────────────────────────────────────────────────────────┘

```

### Exchange Types

```text
┌─────────────────────────────────────────────────────────────────┐
│                      EXCHANGE TYPES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  DIRECT EXCHANGE:                                               │
│  ┌─────────┐    routing-key: "order.created"                    │
│  │Producer │─────────────────────────────────────┐              │
│  └─────────┘                                     ▼              │
│                                      ┌──────────────────┐      │
│                                      │  Direct Exchange  │      │
│                                      └────────┬─────────┘      │
│                                               │                 │
│                         ┌─────────────────────┼─────────────┐  │
│                         │                     │             │  │
│                         ▼                     ▼             ▼  │
│                   ┌──────────┐          ┌──────────┐  ┌────────┐│
│                   │ Queue:   │          │ Queue:   │  │Queue:  ││
│                   │ order.*  │          │ payment.*│  │other.* ││
│                   └──────────┘          └──────────┘  └────────┘│
│                                                                 │
│  TOPIC EXCHANGE:                                                │
│  ┌─────────┐    routing-key: "order.created.us"                 │
│  │Producer │─────────────────────────────────────┐              │
│  └─────────┘                                     ▼              │
│                                      ┌──────────────────┐      │
│                                      │   Topic Exchange  │      │
│                                      └────────┬─────────┘      │
│                                               │                 │
│                         ┌─────────────────────┼─────────────┐  │
│                         │                     │             │  │
│                         ▼                     ▼             ▼  │
│                   ┌──────────┐          ┌──────────┐  ┌────────┐│
│                   │ Queue:   │          │ Queue:   │  │Queue:  ││
│                   │order.*.us│          │*.created.*│  │#       ││
│                   └──────────┘          └──────────┘  └────────┘│
│                                                                 │
│  FANOUT EXCHANGE:                                               │
│  ┌─────────┐                                                   │
│  │Producer │─────────────────────────────────────┐              │
│  └─────────┘                                     ▼              │
│                                      ┌──────────────────┐      │
│                                      │  Fanout Exchange  │      │
│                                      └────────┬─────────┘      │
│                                               │                 │
│                         ┌─────────────────────┼─────────────┐  │
│                         │                     │             │  │
│                         ▼                     ▼             ▼  │
│                   ┌──────────┐          ┌──────────┐  ┌────────┐│
│                   │ Queue 1  │          │ Queue 2  │  │Queue 3 ││
│                   └──────────┘          └──────────┘  └────────┘│
│              (All queues receive the message)                   │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### TypeScript - RabbitMQ Producer

```typescript
import amqplib, { Connection, Channel, ChannelModel } from 'amqplib';

interface ProducerConfig {
  url: string;
  prefetchCount?: number;
  reconnectInterval?: number;
}

class RabbitMQProducer {
  private connection: ChannelModel | null = null;
  private channel: Channel | null = null;
  private config: ProducerConfig;

  constructor(config: ProducerConfig) {
    this.config = {
      reconnectInterval: 5000,
      ...config,
    };
  }

  async connect(): Promise<void> {
    try {
      this.connection = await amqplib.connect(this.config.url);
      this.channel = await this.connection.createChannel();

      this.connection.on('error', (err) => {
        console.error('RabbitMQ connection error:', err);
        this.reconnect();
      });

      this.connection.on('close', () => {
        console.warn('RabbitMQ connection closed, reconnecting...');
        this.reconnect();
      });

      console.log('RabbitMQ producer connected');
    } catch (error) {
      console.error('Failed to connect to RabbitMQ:', error);
      await this.reconnect();
    }
  }

  async disconnect(): Promise<void> {
    if (this.channel) {
      await this.channel.close();
    }
    if (this.connection) {
      await this.connection.close();
    }
    console.log('RabbitMQ producer disconnected');
  }

  async publish<T>(
    exchange: string,
    routingKey: string,
    message: T,
    options?: {
      persistent?: boolean;
      expiration?: string;
      priority?: number;
    }
  ): Promise<boolean> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    const messageBuffer = Buffer.from(JSON.stringify(message));
    const messageOptions: any = {
      persistent: options?.persistent ?? true,
      timestamp: Date.now(),
      contentType: 'application/json',
      correlationId: this.generateCorrelationId(),
    };

    if (options?.expiration) {
      messageOptions.expiration = options.expiration;
    }

    if (options?.priority) {
      messageOptions.priority = options.priority;
    }

    const result = this.channel.publish(
      exchange,
      routingKey,
      messageBuffer,
      messageOptions
    );

    console.log(`Message published to ${exchange}/${routingKey}`);
    return result;
  }

  async sendToQueue<T>(
    queue: string,
    message: T,
    options?: { persistent?: boolean }
  ): Promise<boolean> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    const messageBuffer = Buffer.from(JSON.stringify(message));
    const result = this.channel.sendToQueue(
      queue,
      messageBuffer,
      {
        persistent: options?.persistent ?? true,
        timestamp: Date.now(),
        contentType: 'application/json',
      }
    );

    console.log(`Message sent to queue: ${queue}`);
    return result;
  }

  async assertExchange(
    exchange: string,
    type: 'direct' | 'topic' | 'fanout' | 'headers',
    options?: { durable?: boolean; autoDelete?: boolean }
  ): Promise<void> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    await this.channel.assertExchange(exchange, type, {
      durable: options?.durable ?? true,
      autoDelete: options?.autoDelete ?? false,
    });

    console.log(`Exchange asserted: ${exchange} (${type})`);
  }

  async assertQueue(
    queue: string,
    options?: {
      durable?: boolean;
      exclusive?: boolean;
      deadLetterExchange?: string;
      messageTtl?: number;
    }
  ): Promise<void> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    await this.channel.assertQueue(queue, {
      durable: options?.durable ?? true,
      exclusive: options?.exclusive ?? false,
      deadLetterExchange: options?.deadLetterExchange,
      arguments: options?.messageTtl
        ? { 'x-message-ttl': options.messageTtl }
        : undefined,
    });

    console.log(`Queue asserted: ${queue}`);
  }

  async bindQueue(
    queue: string,
    exchange: string,
    routingKey: string
  ): Promise<void> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    await this.channel.bindQueue(queue, exchange, routingKey);
    console.log(`Queue ${queue} bound to ${exchange} with key ${routingKey}`);
  }

  private async reconnect(): Promise<void> {
    console.log(
      `Reconnecting in ${this.config.reconnectInterval}ms...`
    );
    setTimeout(() => this.connect(), this.config.reconnectInterval);
  }

  private generateCorrelationId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

```

### TypeScript - RabbitMQ Consumer

```typescript
import amqplib, { Connection, Channel, ChannelModel, ConsumeMessage } from 'amqplib';

interface ConsumerConfig {
  url: string;
  queue: string;
  prefetchCount?: number;
  noAck?: boolean;
}

class RabbitMQConsumer {
  private connection: ChannelModel | null = null;
  private channel: Channel | null = null;
  private config: ConsumerConfig;
  private isProcessing: boolean = false;

  constructor(config: ConsumerConfig) {
    this.config = {
      prefetchCount: 10,
      noAck: false,
      ...config,
    };
  }

  async connect(): Promise<void> {
    try {
      this.connection = await amqplib.connect(this.config.url);
      this.channel = await this.connection.createChannel();

      await this.channel.prefetch(this.config.prefetchCount);

      this.connection.on('error', (err) => {
        console.error('RabbitMQ connection error:', err);
      });

      this.connection.on('close', () => {
        console.warn('RabbitMQ connection closed');
      });

      console.log('RabbitMQ consumer connected');
    } catch (error) {
      console.error('Failed to connect to RabbitMQ:', error);
      throw error;
    }
  }

  async consume(
    handler: (message: any) => Promise<void>
  ): Promise<void> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    await this.channel.assertQueue(this.config.queue, { durable: true });

    console.log(`Consuming from queue: ${this.config.queue}`);

    await this.channel.consume(
      this.config.queue,
      async (msg: ConsumeMessage | null) => {
        if (!msg) {
          console.warn('Consumer cancelled by server');
          return;
        }

        this.isProcessing = true;

        try {
          const content = JSON.parse(msg.content.toString());
          const metadata = {
            exchange: msg.fields.exchange,
            routingKey: msg.fields.routingKey,
            redelivered: msg.properties.redelivered,
            correlationId: msg.properties.correlationId,
            timestamp: msg.properties.timestamp,
          };

          console.log('Processing message:', {
            queue: this.config.queue,
            correlationId: metadata.correlationId,
          });

          await handler({ content, metadata, raw: msg });

          if (!this.config.noAck) {
            this.channel!.ack(msg);
          }

          console.log('Message processed successfully');
        } catch (error) {
          console.error('Error processing message:', error);

          if (!this.config.noAck) {
            // Reject and requeue (or send to DLQ)
            this.channel!.nack(msg, false, false);
          }
        } finally {
          this.isProcessing = false;
        }
      },
      {
        noAck: this.config.noAck,
      }
    );
  }

  async consumeWithRetry(
    handler: (message: any) => Promise<void>,
    maxRetries: number = 3
  ): Promise<void> {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }

    await this.channel.assertQueue(this.config.queue, { durable: true });

    await this.channel.consume(
      this.config.queue,
      async (msg: ConsumeMessage | null) => {
        if (!msg) return;

        try {
          const content = JSON.parse(msg.content.toString());
          const retryCount = msg.properties.headers?.['x-retry-count'] || 0;

          await handler({ content, retryCount, raw: msg });

          this.channel!.ack(msg);
        } catch (error) {
          const retryCount = msg.properties.headers?.['x-retry-count'] || 0;

          if (retryCount < maxRetries) {
            // Requeue with incremented retry count
            const retryMessage = {
              ...msg.properties.headers,
              'x-retry-count': retryCount + 1,
            };

            this.channel!.nack(msg, false, false);
            console.log(
              `Message requeued (attempt ${retryCount + 1}/${maxRetries})`
            );
          } else {
            // Send to dead letter queue
            this.channel!.nack(msg, false, false);
            console.log('Message sent to DLQ after max retries');
          }
        }
      }
    );
  }

  async disconnect(): Promise<void> {
    if (this.channel) {
      await this.channel.close();
    }
    if (this.connection) {
      await this.connection.close();
    }
    console.log('RabbitMQ consumer disconnected');
  }

  isBusy(): boolean {
    return this.isProcessing;
  }
}

```

### TypeScript - Dead Letter Queue Configuration

```typescript
class DeadLetterQueueSetup {
  private producer: RabbitMQProducer;

  constructor(producer: RabbitMQProducer) {
    this.producer = producer;
  }

  async setupDLQ(
    queueName: string,
    dlxName: string = 'dlx'
  ): Promise<void> {
    const dlqName = `${queueName}.dlq`;
    const retryQueueName = `${queueName}.retry`;

    // Assert dead letter exchange
    await this.producer.assertExchange(dlxName, 'direct', {
      durable: true,
    });

    // Assert DLQ
    await this.producer.assertQueue(dlqName, {
      durable: true,
      deadLetterExchange: dlxName,
    });

    // Assert retry queue (with TTL)
    await this.producer.assertQueue(retryQueueName, {
      durable: true,
      deadLetterExchange: '',
      deadLetterRoutingKey: queueName,
      messageTtl: 30000, // 30 seconds
    });

    // Bind queues
    await this.producer.bindQueue(dlqName, dlxName, '');
    await this.producer.bindQueue(retryQueueName, dlxName, 'retry');

    console.log(`DLQ setup complete for queue: ${queueName}`);
  }

  async setupPriorityQueue(
    queueName: string,
    maxPriority: number = 10
  ): Promise<void> {
    await this.producer.assertQueue(queueName, {
      durable: true,
    });

    console.log(`Priority queue setup: ${queueName} (max priority: ${maxPriority})`);
  }

  async setupTTLQueue(
    queueName: string,
    ttlMs: number
  ): Promise<void> {
    await this.producer.assertQueue(queueName, {
      durable: true,
      messageTtl: ttlMs,
    });

    console.log(`TTL queue setup: ${queueName} (TTL: ${ttlMs}ms)`);
  }

  async setupMaxLengthQueue(
    queueName: string,
    maxLength: number
  ): Promise<void> {
    await this.producer.assertQueue(queueName, {
      durable: true,
    });

    // Note: Max length is set via queue arguments
    console.log(`Max length queue setup: ${queueName} (max: ${maxLength})`);
  }
}

```

### TypeScript - Request/Reply Pattern

```typescript
import { v4 as uuidv4 } from 'uuid';

interface RequestReplyConfig {
  replyTimeout: number;
  correlationId?: string;
}

class RabbitMQRequestReply {
  private producer: RabbitMQProducer;
  private replyQueue: string;
  private pendingRequests: Map<
    string,
    { resolve: Function; reject: Function; timer: NodeJS.Timeout }
  > = new Map();

  constructor(producer: RabbitMQProducer, replyQueue = 'amq.rabbitmq.reply-to') {
    this.producer = producer;
    this.replyQueue = replyQueue;
  }

  async initialize(): Promise<void> {
    // Set up reply consumer
    const consumer = new RabbitMQConsumer({
      url: (this.producer as any).config.url,
      queue: this.replyQueue,
      noAck: true,
    });

    await consumer.connect();
    await consumer.consume(async (message) => {
      const correlationId = message.metadata.correlationId;
      const pending = this.pendingRequests.get(correlationId);

      if (pending) {
        clearTimeout(pending.timer);
        this.pendingRequests.delete(correlationId);
        pending.resolve(message.content);
      }
    });
  }

  async request<TRequest, TResponse>(
    exchange: string,
    routingKey: string,
    request: TRequest,
    config: RequestReplyConfig = { replyTimeout: 30000 }
  ): Promise<TResponse> {
    const correlationId = config.correlationId || uuidv4();

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pendingRequests.delete(correlationId);
        reject(new Error('Request timeout'));
      }, config.replyTimeout);

      this.pendingRequests.set(correlationId, { resolve, reject, timer });

      this.producer.publish(exchange, routingKey, request, {
        persistent: true,
        replyTo: this.replyQueue,
        correlationId,
      });
    });
  }

  async reply(
    originalMessage: any,
    response: any
  ): Promise<void> {
    const correlationId = originalMessage.metadata.correlationId;
    const replyTo = originalMessage.raw.properties.replyTo;

    if (replyTo && correlationId) {
      await this.producer.sendToQueue(replyTo, response, {
        persistent: true,
      });
    }
  }
}

```

## Real-World Use Cases

### 1. E-Commerce Order Processing

- Order events published to exchanges
- Inventory, payment, shipping services consume from queues
- Dead letter queues for failed processing

### 2. IoT Data Ingestion

- Devices publish telemetry data
- Multiple consumers process data differently
- Priority queues for critical alerts

### 3. Task Distribution

- Work queues for distributing tasks across workers
- Competing consumers for load balancing
- Priority queues for urgent tasks

### 4. Notification System

- Fanout exchange for broadcasting notifications
- Topic exchange for routing to specific services
- TTL queues for expiring notifications

## Common Mistakes

1. **Not acknowledging messages** - Messages redelivered indefinitely

2. **Ignoring prefetch count** - Consumer overwhelmed

3. **No dead letter queue** - Failed messages lost

4. **Wrong exchange type** - Messages not routed correctly

5. **Not handling reconnection** - Consumer crashes permanently

6. **Missing message persistence** - Messages lost on broker restart

7. **No monitoring** - Can't detect queue buildup

8. **Blocking in consumer** - Prevents processing other messages

## Best Practices

1. **Always acknowledge messages** - After successful processing

2. **Use prefetch count** - Limit unacknowledged messages per consumer

3. **Implement dead letter queues** - For failed message handling

4. **Use message persistence** - For important messages

5. **Handle reconnection** - Automatic reconnection logic

6. **Monitor queue lengths** - Alert on growing queues

7. **Use correlation IDs** - Track request/reply patterns

8. **Implement circuit breakers** - For producer/consumer failures

## Performance Considerations

- **Prefetch count**: Balance between throughput and memory usage
- **Message persistence**: Trade-off between durability and performance
- **Queue length limits**: Prevent memory exhaustion
- **Connection pooling**: Reuse connections across consumers
- **Batch publishing**: Increase throughput with batch sends

## Interview Questions

### Beginner (5-10)

1. **What is RabbitMQ?**

   - Open-source message broker implementing AMQP protocol.

2. **What is a message broker?**

   - Intermediary that receives, stores, and forwards messages between services.

3. **What is an exchange?**

   - Component that routes messages to queues based on binding rules.

4. **What are the exchange types?**

   - Direct, Topic, Fanout, Headers.

5. **What is a queue?**

   - Buffer that stores messages until consumed.

6. **What is a binding?**

   - Rule that connects exchange to queue with routing key.

7. **What is message acknowledgment?**

   - Consumer confirms successful message processing.

8. **What is a dead letter queue?**

   - Queue for messages that can't be processed or rejected.

### Intermediate (5-10)

9. **What is the difference between RabbitMQ and Kafka?**

   - RabbitMQ: Traditional broker, complex routing
   - Kafka: Distributed log, high throughput streaming

10. **How does RabbitMQ ensure message delivery?**

    - Persistence, acknowledgments, publisher confirms.

11. **What is prefetch count?**

    - Number of unacknowledged messages delivered to consumer at once.

12. **What is a consumer group?**

    - Group of consumers that jointly consume from queues.

13. **How do you handle message ordering?**

    - Single queue, single consumer, or partitioned queues.

14. **What is TTL in RabbitMQ?**

    - Time-to-live: Message expiration time.

15. **How do you monitor RabbitMQ?**

    - Management UI, plugins, metrics APIs.

16. **What is publisher confirms?**

    - Broker acknowledges message receipt to publisher.

### Senior (10-15)

17. **Design a RabbitMQ-based order processing system.**

    - Exchanges, queues, DLQ, retry logic, monitoring.

18. **How do you handle RabbitMQ clustering?**

    - Erlang clustering, queue mirroring, node discovery.

19. **Explain RabbitMQ high availability.**

    - Queue mirroring, load balancing, failover.

20. **How do you secure RabbitMQ?**

    - SSL/TLS, SASL, ACLs, vhosts.

21. **What is RabbitMQ federation?**

    - Cross-datacenter message replication.

22. **How do you handle message replay?**

    - Replay from queue, event sourcing, backup queues.

23. **Explain RabbitMQ performance tuning.**

    - Prefetch, persistence, batch publishing, connection pooling.

24. **How do you handle RabbitMQ in microservices?**

    - Service decoupling, async processing, event-driven.

25. **What are RabbitMQ best practices?**

    - Idempotent consumers, DLQ, monitoring, capacity planning.

### FAANG-style (5-10)

26. **Design Netflix's messaging system with RabbitMQ.**

    - Multi-datacenter, federation, monitoring, exactly-once.

27. **How would you handle 100K messages/second?**

    - Connection pooling, batch publishing, consumer parallelism.

28. **Design a real-time notification system.**

    - Fanout exchanges, priority queues, TTL, delivery tracking.

29. **How do you handle RabbitMQ disaster recovery?**

    - Clustering, mirroring, backup strategies, failover.

30. **Explain RabbitMQ in event-driven architecture.**

    - Event sourcing, CQRS, saga pattern integration.

### Follow-ups (5-10)

31. **How do you migrate from RabbitMQ to Kafka?**

    - Strangler fig pattern, dual write, gradual migration.

32. **What is the impact of RabbitMQ on microservices?**

    - Decoupling, async processing, eventual consistency.

33. **How do you test RabbitMQ-based systems?**

    - Embedded broker, integration tests, contract testing.

34. **What is the future of RabbitMQ?**

    - Quorum queues, Khepri, cloud-native deployments.

35. **How do you choose between RabbitMQ and Kafka?**

    - RabbitMQ for complex routing, Kafka for streaming.

## Summary

RabbitMQ is a versatile message broker ideal for microservices communication. It provides flexible routing, reliable delivery, and multiple messaging patterns. Key concepts include exchanges, queues, bindings, and acknowledgments.

## Cheat Sheet

```text
┌─────────────────────────────────────────────────────────┐
│                    RABBITMQ                             │
├─────────────────────────────────────────────────────────┤
│ CORE CONCEPTS:                                          │
│ • Exchange: Routes messages to queues                   │
│ • Queue: Stores messages until consumed                 │
│ • Binding: Connection rule between exchange/queue       │
│ • Routing Key: Message routing criterion                │
│ • Acknowledgment: Consumer confirms processing          │
│                                                         │
│ EXCHANGE TYPES:                                         │
│ • Direct: Exact routing key match                       │
│ • Topic: Pattern matching (*, #)                        │
│ • Fanout: Broadcast to all queues                       │
│ • Headers: Header-based routing                         │
│                                                         │
│ MESSAGE FEATURES:                                       │
│ • Persistence: Survives broker restart                  │
│ • TTL: Message expiration                               │
│ • Priority: Message ordering                            │
│ • Dead Letter: Failed message handling                  │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Always acknowledge messages                           │
│ • Use prefetch count                                    │
│ • Implement DLQ                                         │
│ • Use message persistence                               │
│ • Handle reconnection                                   │
│ • Monitor queue lengths                                 │
│ • Use correlation IDs                                   │
└─────────────────────────────────────────────────────────┘

```

---

## References & Learn More

- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
- [RabbitMQ Documentation](https://www.rabbitmq.com/docs)
- [RabbitMQ in Depth](https://www.amazon.com/RabbitMQ-Depth-Software-Gabriel-Brenner/dp/1617292953)