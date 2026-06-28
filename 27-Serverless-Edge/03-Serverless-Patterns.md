# Serverless Patterns

## Definition
Serverless patterns are reusable architectural designs for building serverless applications that address common challenges like API design, event processing, data streaming, and workflow orchestration.

## Why Do We Need It?
- **Proven Solutions**: Battle-tested approaches to common problems
- **Best Practices**: Established patterns for reliability and scalability
- **Reduced Complexity**: Simplified architecture decisions
- **Faster Development**: Ready-to-implement solutions
- **Cost Optimization**: Patterns designed for serverless economics

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SERVERLESS PATTERNS ECOSYSTEM                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    API Patterns                              │   │
│  │  • API Gateway + Lambda                                     │   │
│  │  • HTTP API vs REST API                                     │   │
│  │  • WebSocket API                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 Event-Driven Patterns                        │   │
│  │  • SQS + Lambda                                             │   │
│  │  • SNS + Lambda                                             │   │
│  │  • EventBridge + Lambda                                     │   │
│  │  • DynamoDB Streams + Lambda                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Orchestration Patterns                         │   │
│  │  • Step Functions                                           │   │
│  │  • Saga Pattern                                             │   │
│  │  • Choreography vs Orchestration                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Data Patterns                              │   │
│  │  • CQRS (Command Query Responsibility Segregation)          │   │
│  │  • Event Sourcing                                           │   │
│  │  • Data Lake                                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. API Gateway + Lambda Pattern

```typescript
// serverless.yml
service: my-api

provider:
  name: aws
  runtime: nodejs18.x
  region: us-east-1
  environment:
    TABLE_NAME: ${self:service}-table

functions:
  createUser:
    handler: src/handlers/users.create
    events:
      - httpApi:
          path: /users
          method: POST
  
  getUser:
    handler: src/handlers/users.get
    events:
      - httpApi:
          path: /users/{id}
          method: GET
  
  updateUser:
    handler: src/handlers/users.update
    events:
      - httpApi:
          path: /users/{id}
          method: PUT

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-table
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH
```

```typescript
// src/handlers/users.ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand, GetCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);
const TABLE_NAME = process.env.TABLE_NAME!;

export const create = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const body = JSON.parse(event.body || '{}');
  const item = {
    id: crypto.randomUUID(),
    ...body,
    createdAt: new Date().toISOString(),
  };
  
  await docClient.send(
    new PutCommand({
      TableName: TABLE_NAME,
      Item: item,
    })
  );
  
  return {
    statusCode: 201,
    body: JSON.stringify(item),
  };
};

export const get = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const { id } = event.pathParameters || {};
  
  const result = await docClient.send(
    new GetCommand({
      TableName: TABLE_NAME,
      Key: { id },
    })
  );
  
  if (!result.Item) {
    return {
      statusCode: 404,
      body: JSON.stringify({ error: 'Not found' }),
    };
  }
  
  return {
    statusCode: 200,
    body: JSON.stringify(result.Item),
  };
};
```

### 2. SQS + Lambda Pattern (Async Processing)

```typescript
// producer.ts - Send message to SQS
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';

const sqsClient = new SQSClient({});
const QUEUE_URL = process.env.QUEUE_URL!;

export async function processOrder(order: Order) {
  // Validate order
  await validateOrder(order);
  
  // Send to SQS for async processing
  await sqsClient.send(
    new SendMessageCommand({
      QueueUrl: QUEUE_URL,
      MessageBody: JSON.stringify(order),
      MessageAttributes: {
        orderType: {
          DataType: 'String',
          StringValue: order.type,
        },
      },
    })
  );
  
  return { orderId: order.id, status: 'queued' };
}

// consumer.ts - Process SQS messages
import { SQSEvent, SQSBatchResponse } from 'aws-lambda';

export const handler = async (event: SQSEvent): Promise<SQSBatchResponse> => {
  const batchItemFailures: { itemIdentifier: string }[] = [];
  
  for (const record of event.Records) {
    try {
      const order = JSON.parse(record.body);
      await processOrder(order);
    } catch (error) {
      console.error('Error processing message:', error);
      batchItemFailures.push({ itemIdentifier: record.messageId });
    }
  }
  
  return { batchItemFailures };
};

async function processOrder(order: Order) {
  // Process order: update inventory, send confirmation, etc.
  console.log('Processing order:', order.id);
}
```

### 3. EventBridge Pattern (Event Bus)

```typescript
// Event publisher
import { EventBridgeClient, PutEventsCommand } from '@aws-sdk/client-eventbridge';

const eventBridgeClient = new EventBridgeClient({});

export async function publishOrderEvent(order: Order) {
  await eventBridgeClient.send(
    new PutEventsCommand({
      Entries: [
        {
          Source: 'my-app.orders',
          DetailType: 'OrderCreated',
          Detail: JSON.stringify(order),
          EventBusName: 'default',
        },
      ],
    })
  );
}

// Event consumer
import { EventBridgeEvent } from 'aws-lambda';

export const handler = async (
  event: EventBridgeEvent<'OrderCreated', Order>
) => {
  const order = event.detail;
  
  // Handle different event types
  switch (event['detail-type']) {
    case 'OrderCreated':
      await handleOrderCreated(order);
      break;
    case 'OrderUpdated':
      await handleOrderUpdated(order);
      break;
    case 'OrderCancelled':
      await handleOrderCancelled(order);
      break;
  }
};

async function handleOrderCreated(order: Order) {
  // Send confirmation email, update inventory, etc.
  console.log('Order created:', order.id);
}
```

### 4. Step Functions Pattern (Workflow Orchestration)

```typescript
// step-function-definition.asl.json
{
  "Comment": "Order Processing Workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:validate-order",
      "Next": "ProcessPayment",
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "OrderFailed"
        }
      ]
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:process-payment",
      "Next": "UpdateInventory",
      "Catch": [
        {
          "ErrorEquals": ["PaymentFailed"],
          "Next": "RefundPayment",
          "ResultPath": "$.error"
        }
      ]
    },
    "UpdateInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:update-inventory",
      "Next": "SendConfirmation"
    },
    "SendConfirmation": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:send-confirmation",
      "Next": "OrderComplete"
    },
    "OrderComplete": {
      "Type": "Succeed"
    },
    "RefundPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:refund-payment",
      "Next": "OrderFailed"
    },
    "OrderFailed": {
      "Type": "Fail",
      "Cause": "Order processing failed"
    }
  }
}
```

```typescript
// Lambda handlers for Step Functions
export const validateOrder = async (event: any) => {
  const { order } = event;
  
  if (!order.items || order.items.length === 0) {
    throw new Error('Order has no items');
  }
  
  return { order, validated: true };
};

export const processPayment = async (event: any) => {
  const { order } = event;
  
  // Process payment logic
  const paymentResult = {
    transactionId: 'txn_' + crypto.randomUUID(),
    status: 'success',
  };
  
  return { order, payment: paymentResult };
};

export const updateInventory = async (event: any) => {
  const { order } = event;
  
  // Update inventory logic
  for (const item of order.items) {
    await decreaseInventory(item.productId, item.quantity);
  }
  
  return { order, inventoryUpdated: true };
};
```

### 5. CQRS Pattern (Command Query Responsibility Segregation)

```typescript
// Command side - Write operations
export async function createOrder(command: CreateOrderCommand) {
  const order = {
    id: crypto.randomUUID(),
    ...command,
    status: 'created',
    createdAt: new Date().toISOString(),
  };
  
  // Save to write database
  await saveOrder(order);
  
  // Publish event
  await publishEvent({
    type: 'OrderCreated',
    payload: order,
  });
  
  return order;
}

// Query side - Read operations
export async function getOrder(orderId: string): Promise<OrderView> {
  // Read from read-optimized database
  const order = await getOrderFromReadStore(orderId);
  
  if (!order) {
    throw new Error('Order not found');
  }
  
  return order;
}

export async function listOrders(userId: string): Promise<OrderView[]> {
  // Read from read-optimized database with pagination
  return await getOrdersFromReadStore(userId);
}
```

### 6. Saga Pattern (Distributed Transactions)

```typescript
// Saga orchestrator
interface SagaStep {
  name: string;
  execute: (context: SagaContext) => Promise<void>;
  compensate: (context: SagaContext) => Promise<void>;
}

class OrderSaga {
  private steps: SagaStep[] = [
    {
      name: 'ReserveInventory',
      execute: async (ctx) => {
        ctx.inventoryReservation = await reserveInventory(ctx.order);
      },
      compensate: async (ctx) => {
        await releaseInventory(ctx.inventoryReservation);
      },
    },
    {
      name: 'ProcessPayment',
      execute: async (ctx) => {
        ctx.payment = await processPayment(ctx.order);
      },
      compensate: async (ctx) => {
        await refundPayment(ctx.payment);
      },
    },
    {
      name: 'ShipOrder',
      execute: async (ctx) => {
        ctx.shipment = await shipOrder(ctx.order);
      },
      compensate: async (ctx) => {
        await cancelShipment(ctx.shipment);
      },
    },
  ];
  
  async execute(order: Order): Promise<SagaResult> {
    const context: SagaContext = { order, completedSteps: [] };
    
    try {
      for (const step of this.steps) {
        await step.execute(context);
        context.completedSteps.push(step.name);
      }
      
      return { success: true, context };
    } catch (error) {
      // Compensate in reverse order
      for (const stepName of context.completedSteps.reverse()) {
        const step = this.steps.find((s) => s.name === stepName);
        if (step) {
          await step.compensate(context);
        }
      }
      
      return { success: false, error: error as Error };
    }
  }
}
```

## Real-World Use Cases

### E-Commerce Order Processing
```
Order Flow:
┌─────────────────────────────────────────────────────────────────┐
│  Order Placed → SQS → Lambda (Validate) → Lambda (Payment)    │
│                              │                                   │
│                              ▼                                   │
│                     Lambda (Inventory) → Lambda (Ship)          │
│                              │                                   │
│                              ▼                                   │
│                     Lambda (Email) → Order Complete              │
└─────────────────────────────────────────────────────────────────┘
```

### Real-time Data Processing
```
Data Pipeline:
┌─────────────────────────────────────────────────────────────────┐
│  Kinesis → Lambda (Transform) → DynamoDB → Lambda (Aggregate)  │
│                                        │                        │
│                                        ▼                        │
│                               S3 (Data Lake)                    │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

1. **Not handling failures**: Missing retry logic and dead letter queues
2. **Over-orchestration**: Using Step Functions for simple workflows
3. **Ignoring idempotency**: Not handling duplicate events
4. **Tight coupling**: Functions too dependent on each other
5. **Missing monitoring**: No visibility into async processes

## Best Practices

1. **Design for failure**: Implement retries, dead letter queues, circuit breakers
2. **Keep functions small**: Single responsibility principle
3. **Use idempotency**: Handle duplicate events gracefully
4. **Monitor everything**: Track all async operations
5. **Document patterns**: Create reusable pattern libraries

## Performance Considerations

```
Pattern Selection Guide:
┌─────────────────────────────────────────────────────────────────┐
│  Simple API:              API Gateway + Lambda                   │
│  Async Processing:        SQS + Lambda                          │
│  Event-Driven:            EventBridge + Lambda                  │
│  Complex Workflow:        Step Functions                        │
│  Real-time:               WebSocket API + DynamoDB              │
│  Data Streaming:          Kinesis + Lambda                      │
└─────────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)
1. **What is the API Gateway + Lambda pattern?**
   - Answer: A pattern where API Gateway handles HTTP requests and triggers Lambda functions for processing.

2. **What is SQS used for in serverless?**
   - Answer: Decoupling services, async processing, buffering requests, and handling traffic spikes.

3. **What is EventBridge?**
   - Answer: AWS's serverless event bus that connects applications with events from AWS services, SaaS apps, and custom applications.

4. **What is a dead letter queue?**
   - Answer: A queue that receives messages that failed processing after maximum retries, enabling later investigation.

5. **What is idempotency?**
   - Answer: The property where executing an operation multiple times produces the same result as executing it once.

### Intermediate (5)
6. **When should you use Step Functions vs simple Lambda chaining?**
   - Answer: Use Step Functions for complex workflows with branching, parallel execution, or human approval. Use Lambda chaining for simple sequential operations.

7. **How do you handle errors in SQS + Lambda?**
   - Answer: Use partial batch failures, dead letter queues, exponential backoff retry, and visibility timeout.

8. **What is the difference between SQS and SNS?**
   - Answer: SQS is point-to-point (one consumer); SNS is pub-sub (many consumers). SQS buffers messages; SNS routes immediately.

9. **How do you implement event sourcing in serverless?**
   - Answer: Store events in DynamoDB/S3, use Lambda to project events into read models, replay events to rebuild state.

10. **What is CQRS and when should you use it?**
    - Answer: Separating read and write operations. Use when read and write patterns differ significantly or when scaling independently.

### Senior (10)
11. **Design a serverless e-commerce order processing system**
    - Answer: API Gateway + Lambda for API, SQS for async processing, Step Functions for order workflow, DynamoDB for state, EventBridge for events.

12. **How do you handle distributed transactions in serverless?**
    - Answer: Use Saga pattern with compensating transactions, or event sourcing for eventual consistency.

13. **Explain choreography vs orchestration**
    - Answer: Choreography: Services react to events independently. Orchestration: Central coordinator manages workflow. Use choreography for simple, orchestration for complex.

14. **How do you test serverless patterns?**
    - Answer: Unit test handlers, integration test with localstack/SAM Local, end-to-end test with deployed stack, use step functions local.

15. **What are the limitations of serverless patterns?**
    - Answer: Cold starts, execution time limits, vendor lock-in, debugging complexity, state management challenges.

16. **How do you monitor async serverless workflows?**
    - Answer: Use CloudWatch for logs, X-Ray for tracing, custom metrics, Step Functions visual execution history.

17. **How do you handle data consistency in event-driven architectures?**
    - Answer: Use eventual consistency, implement idempotency, use transactional outbox pattern, handle duplicate events.

18. **What is the Strangler Fig pattern in serverless migration?**
    - Answer: Gradually replacing legacy system components with serverless alternatives, routing traffic between old and new.

19. **How do you optimize serverless costs?**
    - Answer: Right-size memory, use provisioned concurrency strategically, optimize execution time, use ARM architectures.

20. **Design a serverless real-time notification system**
    - Answer: EventBridge for events, Lambda for processing, SNS for fan-out, SQS for buffering, WebSocket API for real-time delivery.

### FAANG-style (5)
21. **Design a serverless system processing 1 million events per second**
    - Answer: Kinesis for ingestion, Lambda for processing, DynamoDB for storage, auto-scaling, multi-region deployment, monitoring at scale.

22. **How would you implement a serverless microservices architecture?**
    - Answer: Event-driven communication, API Gateway per service, Lambda for compute, DynamoDB per service, EventBridge for events, Step Functions for workflows.

23. **Explain serverless at global scale**
    - Answer: Multi-region deployment, edge computing for latency, data replication, failover strategies, global consistency challenges.

24. **How do you handle serverless security at scale?**
    - Answer: IAM least privilege, VPC for isolation, secrets management, WAF for API protection, audit logging.

25. **Design a serverless data pipeline for analytics**
    - Answer: Kinesis for streaming, Lambda for ETL, S3 for data lake, Athena for querying, Glue for cataloging, QuickSight for visualization.

### Follow-ups (5)
26. **How do you handle stateful operations in serverless?**
    - Answer: Use external state stores (DynamoDB, ElastiCache), Durable Objects for edge, or Step Functions for workflow state.

27. **What is the impact of serverless on DevOps?**
    - Answer: Infrastructure as code, CI/CD for serverless, monitoring complexity, debugging challenges, new deployment strategies.

28. **How do you migrate a monolith to serverless?**
    - Answer: Strangler Fig pattern, identify serverless-suitable components, refactor incrementally, test thoroughly.

29. **What are the anti-patterns in serverless?**
    - Answer: God functions, synchronous chains, missing error handling, over-provisioning, tight coupling.

30. **How do you ensure reliability in serverless systems?**
    - Answer: Dead letter queues, retries with backoff, circuit breakers, health checks, monitoring and alerting.

## Summary

Serverless patterns provide proven solutions for common architectural challenges. Understand when to use each pattern, how to implement them correctly, and how to handle failures gracefully.

## References & Learn More

- [AWS Serverless Patterns](https://serverlessland.com/patterns)
- [Serverless Framework Patterns](https://www.serverless.com/framework/docs/)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/)
- [Event-Driven Architecture](https://aws.amazon.com/event-driven-architecture/)
- [Serverless Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
