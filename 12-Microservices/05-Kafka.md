# Apache Kafka

## Definition

Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant, and scalable data streaming. It publishes, subscribes to, stores, and processes records (messages) in real-time, making it ideal for microservices communication and data pipelines.

## Why Do We Need It?

In microservices:
- Decouple services through asynchronous communication
- Handle high-throughput data streams (millions of events/second)
- Provide durable message storage for replay and recovery
- Enable real-time data processing and analytics
- Support event-driven architectures and CQRS patterns

## How It Works

### Kafka Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      KAFKA CLUSTER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                     TOPIC: orders                        │   │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │
│   │  │ Partition 0 │  │ Partition 1 │  │ Partition 2 │    │   │
│   │  │             │  │             │  │             │    │   │
│   │  │ [0][1][2]   │  │ [0][1][2]   │  │ [0][1][2]   │    │   │
│   │  │   ↓         │  │   ↓         │  │   ↓         │    │   │
│   │  │ Leader      │  │ Leader      │  │ Leader      │    │   │
│   │  │ (Broker 1)  │  │ (Broker 2)  │  │ (Broker 3)  │    │   │
│   │  └─────────────┘  └─────────────┘  └─────────────┘    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │  Broker 1   │  │  Broker 2   │  │  Broker 3   │            │
│   │  (Leader)   │  │  (Follower) │  │  (Follower) │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### Producer-Consumer Flow

```
┌─────────────┐    ┌─────────────────────────────────────────────┐
│  Producer   │───>│                   KAFKA                     │
│  (Order     │    │  ┌─────────────┐  ┌─────────────┐          │
│   Service)  │    │  │ Partition 0 │  │ Partition 1 │          │
└─────────────┘    │  └──────┬──────┘  └──────┬──────┘          │
                   │         │                │                  │
                   │         ▼                ▼                  │
                   │  ┌─────────────┐  ┌─────────────┐          │
                   │  │ Consumer    │  │ Consumer    │          │
                   │  │ Group A     │  │ Group A     │          │
                   │  │ (Inventory) │  │ (Payment)   │          │
                   │  └─────────────┘  └─────────────┘          │
                   └─────────────────────────────────────────────┘
```

### Consumer Groups

```
Topic: orders (3 partitions)

Consumer Group A (Inventory Service):
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Partition 0 │    │ Partition 1 │    │ Partition 2 │
│      │      │    │      │      │    │      │      │
│      ▼      │    │      ▼      │    │      ▼      │
│ Consumer A1 │    │ Consumer A2 │    │ Consumer A3 │
└─────────────┘    └─────────────┘    └─────────────┘

Consumer Group B (Payment Service):
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Partition 0 │    │ Partition 1 │    │ Partition 2 │
│      │      │    │      │      │    │      │      │
│      ▼      │    │      ▼      │    │      ▼      │
│ Consumer B1 │    │ Consumer B1 │    │ Consumer B2 │
└─────────────┘    └─────────────┘    └─────────────┘

Each consumer group gets all messages independently
Within a group, each partition is consumed by only one consumer
```

## Code Examples

### TypeScript - Kafka Producer

```typescript
import { Kafka, Producer, ProducerRecord, RecordMetadata } from 'kafkajs';

interface OrderEvent {
  orderId: string;
  userId: string;
  items: Array<{ productId: string; quantity: number; price: number }>;
  totalAmount: number;
  timestamp: Date;
}

class KafkaProducer {
  private producer: Producer;
  private kafka: Kafka;

  constructor(clientId: string, brokers: string[]) {
    this.kafka = new Kafka({
      clientId,
      brokers,
      retry: {
        initialRetryTime: 100,
        retries: 8,
      },
    });
    this.producer = this.kafka.producer({
      maxInFlightRequests: 5,
      idempotent: true,
      transactionalId: `${clientId}-transactional`,
    });
  }

  async connect(): Promise<void> {
    await this.producer.connect();
    console.log('Kafka producer connected');
  }

  async disconnect(): Promise<void> {
    await this.producer.disconnect();
    console.log('Kafka producer disconnected');
  }

  async produce<T>(
    topic: string,
    message: T,
    key?: string
  ): Promise<RecordMetadata[]> {
    const record: ProducerRecord = {
      topic,
      messages: [
        {
          key: key || JSON.stringify({ topic, timestamp: Date.now() }),
          value: JSON.stringify(message),
          timestamp: Date.now().toString(),
          headers: {
            'content-type': 'application/json',
            'correlation-id': this.generateCorrelationId(),
          },
        },
      ],
    };

    return this.producer.send(record);
  }

  async produceBatch<T>(
    topic: string,
    messages: T[],
    getKey?: (msg: T) => string
  ): Promise<RecordMetadata[]> {
    const record: ProducerRecord = {
      topic,
      messages: messages.map(msg => ({
        key: getKey ? getKey(msg) : JSON.stringify({ timestamp: Date.now() }),
        value: JSON.stringify(msg),
        timestamp: Date.now().toString(),
        headers: {
          'content-type': 'application/json',
        },
      })),
    };

    return this.producer.send(record);
  }

  private generateCorrelationId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Usage
const producer = new KafkaProducer('order-service', ['localhost:9092']);
await producer.connect();

const orderEvent: OrderEvent = {
  orderId: 'order-123',
  userId: 'user-456',
  items: [
    { productId: 'prod-1', quantity: 2, price: 29.99 },
    { productId: 'prod-2', quantity: 1, price: 49.99 },
  ],
  totalAmount: 109.97,
  timestamp: new Date(),
};

await producer.produce('order-events', orderEvent, orderEvent.orderId);
```

### TypeScript - Kafka Consumer

```typescript
import {
  Kafka,
  Consumer,
  EachMessagePayload,
  KafkaMessage,
  ConsumerRunOpts,
} from 'kafkajs';

interface ConsumerConfig {
  groupId: string;
  topics: string[];
  fromBeginning?: boolean;
  sessionTimeout?: number;
}

class KafkaConsumer {
  private consumer: Consumer;
  private kafka: Kafka;
  private handlers: Map<string, (message: KafkaMessage) => Promise<void>> = new Map();

  constructor(clientId: string, brokers: string[]) {
    this.kafka = new Kafka({
      clientId,
      brokers,
      retry: {
        initialRetryTime: 100,
        retries: 8,
      },
    });
    this.consumer = this.kafka.consumer({
      groupId: `default-group`,
      sessionTimeout: 30000,
      heartbeat: 3000,
    });
  }

  async connect(config: ConsumerConfig): Promise<void> {
    this.consumer = this.kafka.consumer({
      groupId: config.groupId,
      sessionTimeout: config.sessionTimeout || 30000,
    });

    await this.consumer.connect();
    console.log('Kafka consumer connected');

    await this.consumer.subscribe({
      topics: config.topics,
      fromBeginning: config.fromBeginning || false,
    });

    await this.consumer.run({
      eachMessage: async (payload: EachMessagePayload) => {
        await this.handleMessage(payload);
      },
    });
  }

  async disconnect(): Promise<void> {
    await this.consumer.disconnect();
    console.log('Kafka consumer disconnected');
  }

  onMessage(
    topic: string,
    handler: (message: KafkaMessage) => Promise<void>
  ): void {
    this.handlers.set(topic, handler);
  }

  private async handleMessage(payload: EachMessagePayload): Promise<void> {
    const { topic, partition, message } = payload;
    const handler = this.handlers.get(topic);

    if (!handler) {
      console.warn(`No handler for topic: ${topic}`);
      return;
    }

    try {
      console.log(`Processing message from ${topic}[${partition}]`, {
        offset: message.offset,
        key: message.key?.toString(),
      });

      await handler(message);

      console.log(`Successfully processed message from ${topic}[${partition}]`);
    } catch (error) {
      console.error(`Error processing message from ${topic}[${partition}]:`, error);
      throw error;
    }
  }
}

// Usage
const consumer = new KafkaConsumer('inventory-service', ['localhost:9092']);

consumer.onMessage('order-events', async (message) => {
  const order = JSON.parse(message.value!.toString());
  console.log('Received order:', order);

  // Process order - reserve inventory
  await reserveInventory(order);
});

await consumer.connect({
  groupId: 'inventory-service-group',
  topics: ['order-events'],
  fromBeginning: false,
});
```

### TypeScript - Exactly-Once Delivery

```typescript
import { Kafka, Producer, Consumer, EachMessagePayload } from 'kafkajs';

class ExactlyOnceProcessor {
  private producer: Producer;
  private consumer: Consumer;
  private processedMessages: Map<string, boolean> = new Map();

  constructor(private kafka: Kafka) {
    this.producer = kafka.producer({
      idempotent: true,
      transactionalId: 'exactly-once-processor',
    });

    this.consumer = kafka.consumer({
      groupId: 'exactly-once-group',
    });
  }

  async start(): Promise<void> {
    await this.producer.connect();
    await this.consumer.connect();

    await this.consumer.subscribe({
      topics: ['input-topic'],
      fromBeginning: false,
    });

    await this.consumer.run({
      eachMessage: async (payload: EachMessagePayload) => {
        await this.processWithExactlyOnce(payload);
      },
    });
  }

  private async processWithExactlyOnce(
    payload: EachMessagePayload
  ): Promise<void> {
    const { topic, partition, message } = payload;
    const messageId = `${topic}-${partition}-${message.offset}`;

    // Check if already processed (idempotency check)
    if (this.processedMessages.has(messageId)) {
      console.log(`Message ${messageId} already processed, skipping`);
      return;
    }

    // Start transaction
    const transaction = await this.producer.transaction();

    try {
      // Process the message
      const data = JSON.parse(message.value!.toString());
      const result = await this.processData(data);

      // Send result to output topic within transaction
      await transaction.send({
        topic: 'output-topic',
        messages: [
          {
            key: message.key,
            value: JSON.stringify(result),
            headers: {
              'source-offset': message.offset?.toString(),
              'source-partition': partition.toString(),
            },
          },
        ],
      });

      // Commit transaction
      await transaction.commit();

      // Mark as processed
      this.processedMessages.set(messageId, true);

      console.log(`Successfully processed message ${messageId}`);
    } catch (error) {
      // Abort transaction on failure
      await transaction.abort();
      throw error;
    }
  }

  private async processData(data: any): Promise<any> {
    // Your processing logic here
    return {
      ...data,
      processedAt: new Date(),
      status: 'processed',
    };
  }
}
```

### TypeScript - Kafka Streams

```typescript
import { Kafka, StreamType, KStream, KTable } from 'kafkajs';

class KafkaStreamProcessor {
  private kafka: Kafka;
  private streams: Map<string, any> = new Map();

  constructor(clientId: string, brokers: string[]) {
    this.kafka = new Kafka({
      clientId,
      brokers,
    });
  }

  async createStreamProcessor(): Promise<void> {
    // In production, use kafkajs-streams or similar library
    // This is a simplified example of stream processing logic

    const consumer = this.kafka.consumer({
      groupId: 'stream-processor-group',
    });

    const producer = this.kafka.producer();

    await consumer.connect();
    await producer.connect();

    await consumer.subscribe({
      topics: ['input-stream'],
      fromBeginning: false,
    });

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const data = JSON.parse(message.value!.toString());

        // Stream transformation logic
        const transformed = await this.transform(data);

        // Send to output stream
        await producer.send({
          topic: 'output-stream',
          messages: [
            {
              key: message.key,
              value: JSON.stringify(transformed),
            },
          ],
        });
      },
    });
  }

  private async transform(data: any): Promise<any> {
    // Example transformations:
    // - Filter
    // - Map
    // - Aggregate
    // - Join
    // - Window

    return {
      ...data,
      transformed: true,
      transformedAt: new Date(),
    };
  }

  async createKTable(
    topic: string,
    storeName: string
  ): Promise<Map<string, any>> {
    const table = new Map<string, any>();

    const consumer = this.kafka.consumer({
      groupId: `${storeName}-table-group`,
    });

    await consumer.connect();
    await consumer.subscribe({ topics: [topic], fromBeginning: true });

    await consumer.run({
      eachMessage: async ({ message }) => {
        const key = message.key?.toString();
        const value = message.value ? JSON.parse(message.value.toString()) : null;

        if (value) {
          table.set(key!, value);
        } else {
          table.delete(key!);
        }
      },
    });

    return table;
  }
}
```

## Real-World Use Cases

### 1. Netflix
- Real-time video streaming events
- User activity tracking
- Recommendation engine data pipeline
- Log aggregation and monitoring

### 2. LinkedIn
- Activity feeds and notifications
- Real-time analytics
- Data integration between services
- Metrics collection

### 3. Uber
- Real-time ride tracking
- Pricing calculations
- Driver matching
- Trip event processing

### 4. E-Commerce
- Order processing pipeline
- Inventory updates
- Real-time pricing
- Customer behavior tracking

## Common Mistakes

1. **Not partitioning properly** - Leads to hot partitions
2. **Ignoring consumer lag** - Messages pile up
3. **Wrong key selection** - Poor distribution across partitions
4. **No dead letter queue** - Failed messages lost
5. **Not handling rebalancing** - Consumer crashes cause issues
6. **Missing idempotency** - Duplicate message processing
7. **Wrong replication factor** - Data loss risk
8. **Not monitoring** - No visibility into pipeline health

## Best Practices

1. **Design partitions carefully** - Based on throughput and ordering needs
2. **Use consumer groups** - For parallel processing and scalability
3. **Implement idempotent consumers** - Handle duplicate messages
4. **Monitor consumer lag** - Alert on growing lag
5. **Use appropriate serializers** - Avro, Protobuf for schema evolution
6. **Configure retention properly** - Balance storage and replay needs
7. **Handle rebalancing gracefully** - Pause processing during rebalance
8. **Use dead letter queues** - For failed message handling

## Performance Considerations

- **Batch size**: Increase for higher throughput
- **Compression**: Use gzip, snappy, or lz4
- **Replication factor**: 3 for production
- **Partition count**: Based on consumer parallelism needs
- **Consumer fetch size**: Balance latency vs throughput

## Interview Questions

### Beginner (5-10)

1. **What is Apache Kafka?**
   - Distributed event streaming platform for high-throughput data pipelines.

2. **What is a Kafka topic?**
   - Logical channel for publishing and subscribing to messages.

3. **What is a Kafka partition?**
   - Topic subdivision for parallel processing and ordering guarantees.

4. **What is a Kafka consumer group?**
   - Group of consumers that jointly consume a topic, each partition consumed by one consumer.

5. **What is a Kafka producer?**
   - Application that publishes messages to Kafka topics.

6. **What is a Kafka consumer?**
   - Application that subscribes to and processes messages from topics.

7. **What is message offset?**
   - Unique identifier for each message within a partition.

8. **What is consumer lag?**
   - Difference between latest message and consumer's current position.

### Intermediate (5-10)

9. **What is exactly-once delivery?**
   - Guarantee that each message is processed exactly once, no duplicates.

10. **What is a dead letter queue?**
    - Queue for messages that can't be processed after retries.

11. **How does Kafka achieve fault tolerance?**
    - Replication across brokers, leader election, ISR.

12. **What is a Kafka broker?**
    - Server that stores data and serves client requests.

13. **What is ISR in Kafka?**
    - In-Sync Replicas - replicas that are fully caught up with leader.

14. **How do you handle Kafka rebalancing?**
    - Pause processing, commit offsets, handle partition reassignment.

15. **What is Kafka Connect?**
    - Framework for integrating Kafka with external systems.

16. **What is Kafka Streams?**
    - Client library for building stream processing applications.

### Senior (10-15)

17. **Design a Kafka-based order processing system.**
    - Topics for each stage, consumer groups, idempotency, monitoring.

18. **How do you handle schema evolution in Kafka?**
    - Schema Registry, Avro/Protobuf, backward/forward compatibility.

19. **Explain Kafka exactly-once semantics.**
    - Producer idempotency, transactional API, consumer offset commits.

20. **How do you monitor Kafka clusters?**
    - Consumer lag, broker metrics, partition distribution, replication.

21. **What is Kafka MirrorMaker?**
    - Tool for replicating data between Kafka clusters.

22. **How do you secure Kafka?**
    - SSL/TLS, SASL, ACLs, encryption at rest.

23. **Explain Kafka performance tuning.**
    - Batch size, compression, partition count, consumer configuration.

24. **How do you handle Kafka in microservices?**
    - Event-driven architecture, CQRS, saga pattern integration.

25. **What are Kafka best practices for production?**
    - Replication, monitoring, capacity planning, disaster recovery.

### FAANG-style (5-10)

26. **Design Netflix's Kafka infrastructure.**
    - Multi-region, mirroring, monitoring, exactly-once processing.

27. **How would you handle 1M messages/second?**
    - Partitioning strategy, consumer parallelism, batching, compression.

28. **Design a real-time analytics pipeline with Kafka.**
    - Stream processing, windowing, aggregation, materialized views.

29. **How do you handle Kafka disaster recovery?**
    - Multi-cluster setup, MirrorMaker, backup strategies.

30. **Explain Kafka in event-driven architecture.**
    - Event sourcing, CQRS, saga pattern, event schema management.

### Follow-ups (5-10)

31. **How do you migrate to Kafka from another message queue?**
    - Strangler fig pattern, dual write, gradual migration.

32. **What is the impact of Kafka on microservices?**
    - Decoupling, async processing, eventual consistency.

33. **How do you test Kafka-based systems?**
    - Embedded Kafka, integration tests, contract testing.

34. **What is the future of Kafka?**
    - Serverless Kafka, cloud-native, edge computing integration.

35. **How do you choose between Kafka and RabbitMQ?**
    - Kafka for streaming, RabbitMQ for traditional messaging.

## Summary

Apache Kafka is essential for building event-driven microservices. It provides high-throughput, fault-tolerant data streaming with exactly-once delivery semantics. Key concepts include topics, partitions, consumer groups, and offsets.

## Cheat Sheet

```
┌─────────────────────────────────────────────────────────┐
│                   APACHE KAFKA                          │
├─────────────────────────────────────────────────────────┤
│ CORE CONCEPTS:                                          │
│ • Topic: Logical message channel                        │
│ • Partition: Topic subdivision for parallelism          │
│ • Broker: Kafka server node                             │
│ • Producer: Publishes messages                          │
│ • Consumer: Subscribes to messages                      │
│ • Consumer Group: Joint consumption                     │
│ • Offset: Message position in partition                 │
│                                                         │
│ KEY FEATURES:                                           │
│ • High Throughput: Millions of messages/second          │
│ • Fault Tolerance: Replication across brokers           │
│ • Durability: Persistent message storage                │
│ • Scalability: Add brokers and partitions               │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Design partitions for throughput                      │
│ • Use consumer groups for parallelism                   │
│ • Implement idempotent consumers                        │
│ • Monitor consumer lag                                  │
│ • Use dead letter queues                                │
│ • Handle rebalancing gracefully                         │
│ • Configure replication factor 3+                       │
│                                                         │
│ TOOLS:                                                  │
│ • Kafka Connect: System integration                     │
│ • Kafka Streams: Stream processing                      │
│ • Schema Registry: Schema management                    │
│ • MirrorMaker: Cross-cluster replication                │
└─────────────────────────────────────────────────────────┘
```

---

## References & Learn More
- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka: The Definitive Guide](https://www.amazon.com/Kafka-Definitive-Complete-Enterprise-Streaming/dp/1492043087)
- [Confluent Documentation](https://docs.confluent.io/platform/current/)