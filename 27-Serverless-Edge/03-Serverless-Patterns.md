---
section: Serverless & Edge
category: DevOps
tags: [concept, reference]
---

# Serverless Patterns

> Serverless patterns are reusable architectural designs for building serverless applications that address common challenges like API design, event processing, data streaming, and workflow orchestration.

## Definition

Serverless patterns are proven architectural templates — combinations of triggers, functions, queues, and managed services — that solve recurring problems like fan-out, async processing, orchestration, and event-driven decoupling. They reduce bespoke integration work and let teams ship faster with battle-tested designs.

## Why It Matters (TL;DR)

- **Proven solutions** — battle-tested approaches to common problems
- **Best practices baked in** — patterns account for failure modes, retries, and idempotency
- **Reduced complexity** — fewer bespoke integration decisions
- **Faster development** — ready-to-implement reference designs
- **Cost optimization** — patterns respect serverless economics (per-request, GB-second)

## Pattern Taxonomy

```text
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
│  │  • SQS + Lambda (point-to-point)                            │   │
│  │  • SNS + Lambda (pub/sub)                                   │   │
│  │  • EventBridge (event bus + rules)                          │   │
│  │  • DynamoDB Streams + Lambda (CDC)                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Orchestration Patterns                         │   │
│  │  • Step Functions                                           │   │
│  │  • Saga Pattern (compensating transactions)                  │   │
│  │  • Choreography vs Orchestration                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Data Patterns                              │   │
│  │  • CQRS (Command Query Responsibility Segregation)          │   │
│  │  • Event Sourcing                                           │   │
│  │  • Data Lake (S3 + Athena)                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. API Gateway + Lambda (SAM Template)

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "${AWS::StackName}-users"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH

  CreateUserFn:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/users.create
      Runtime: nodejs20.x
      Environment:
        Variables:
          TABLE_NAME: !Ref UsersTable
      Events:
        CreateApi:
          Type: HttpApi
          Properties:
            Path: /users
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
```

```typescript
// src/handlers/users.ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand, GetCommand } from '@aws-sdk/lib-dynamodb';

const docClient = DynamoDBDocumentClient.from(new DynamoDBClient({}));
const TABLE_NAME = process.env.TABLE_NAME!;

export const create = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  const body = JSON.parse(event.body ?? '{}');
  const item = { id: crypto.randomUUID(), ...body, createdAt: new Date().toISOString() };
  await docClient.send(new PutCommand({ TableName: TABLE_NAME, Item: item }));
  return { statusCode: 201, body: JSON.stringify(item) };
};

export const get = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  const result = await docClient.send(
    new GetCommand({ TableName: TABLE_NAME, Key: { id: event.pathParameters?.id } })
  );
  return { statusCode: result.Item ? 200 : 404, body: JSON.stringify(result.Item ?? { error: 'Not found' }) };
};
```

### 2. SQS + Lambda (Async Processing with Batch Failure Reporting)

```typescript
// producer.ts
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';

const sqs = new SQSClient({});

export async function enqueueOrder(order: Order) {
  await sqs.send(new SendMessageCommand({
    QueueUrl: process.env.QUEUE_URL!,
    MessageBody: JSON.stringify(order),
    MessageDeduplicationId: order.id,
    MessageGroupId: order.id,
  }));
}

// consumer.ts — partial batch failure handling
import { SQSEvent, SQSBatchResponse } from 'aws-lambda';

export const handler = async (event: SQSEvent): Promise<SQSBatchResponse> => {
  const batchItemFailures: { itemIdentifier: string }[] = [];
  for (const record of event.Records) {
    try {
      await processOrder(JSON.parse(record.body));
    } catch (err) {
      console.error('Failed:', record.messageId, err);
      batchItemFailures.push({ itemIdentifier: record.messageId });
    }
  }
  return { batchItemFailures }; // failed messages re-appear, successful ones don't
};
```

### 3. EventBridge (Cross-Service Event Bus)

```typescript
import { EventBridgeClient, PutEventsCommand } from '@aws-sdk/client-eventbridge';
import { EventBridgeEvent } from 'aws-lambda';

const eb = new EventBridgeClient({});

export async function publishOrderEvent(order: Order) {
  await eb.send(new PutEventsCommand({
    Entries: [{
      Source: 'my-app.orders',
      DetailType: 'OrderCreated',
      Detail: JSON.stringify(order),
      EventBusName: 'default',
    }],
  }));
}

export const handler = async (event: EventBridgeEvent<'OrderCreated', Order>) => {
  switch (event['detail-type']) {
    case 'OrderCreated':   return handleCreated(event.detail);
    case 'OrderUpdated':   return handleUpdated(event.detail);
    case 'OrderCancelled': return handleCancelled(event.detail);
  }
};
```

### 4. Step Functions (Workflow Orchestration)

```json
{
  "Comment": "Order Processing Workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:validate-order",
      "Next": "ProcessPayment",
      "Catch": [{ "ErrorEquals": ["States.ALL"], "Next": "OrderFailed" }]
    },
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:process-payment",
      "Next": "UpdateInventory",
      "Catch": [{ "ErrorEquals": ["PaymentFailed"], "Next": "RefundPayment" }]
    },
    "UpdateInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:update-inventory",
      "Next": "SendConfirmation"
    },
    "SendConfirmation": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:send-confirmation",
      "End": true
    },
    "RefundPayment": { "Type": "Task", "Resource": "...", "Next": "OrderFailed" },
    "OrderFailed":   { "Type": "Fail", "Cause": "Order processing failed" }
  }
}
```

### 5. Saga Pattern (Compensating Transactions)

```typescript
// Saga orchestrator — runs compensating actions in reverse on failure
interface SagaStep {
  name: string;
  execute: (ctx: SagaContext) => Promise<void>;
  compensate: (ctx: SagaContext) => Promise<void>;
}

class OrderSaga {
  constructor(private steps: SagaStep[]) {}

  async execute(order: Order): Promise<SagaResult> {
    const ctx: SagaContext = { order, completed: [] };
    try {
      for (const step of this.steps) {
        await step.execute(ctx);
        ctx.completed.push(step);
      }
      return { success: true };
    } catch (err) {
      // Compensate in reverse order
      for (const step of [...ctx.completed].reverse()) {
        await step.compensate(ctx).catch(console.error);
      }
      return { success: false, error: err as Error };
    }
  }
}

// Usage
const saga = new OrderSaga([
  { name: 'Reserve',  execute: reserveInventory, compensate: releaseInventory },
  { name: 'Charge',   execute: chargePayment,    compensate: refundPayment },
  { name: 'Ship',     execute: shipOrder,        compensate: cancelShipment },
]);
await saga.execute(order);
```

### 6. CQRS (Command Query Responsibility Segregation)

```typescript
// Write side — command
export async function createOrder(cmd: CreateOrderCommand) {
  const order = { id: crypto.randomUUID(), ...cmd, status: 'created', createdAt: new Date().toISOString() };
  await saveToWriteStore(order);
  await publishEvent({ type: 'OrderCreated', payload: order });
  return order;
}

// Read side — query (denormalized view, eventually consistent)
export async function listOrdersByUser(userId: string): Promise<OrderView[]> {
  return getOrdersFromReadStore(userId); // read-optimized schema
}
// A separate consumer projects OrderCreated → read store
```

### 7. Fan-Out / Fan-In (S3 to Parallel Lambdas)

```text
Pattern: 1 trigger → N parallel workers → 1 aggregator
┌──────────────────────────────────────────────────────────────────┐
│  S3 Event → SNS Topic → Lambda (chunker) → SQS                  │
│                                          ↓                       │
│                              ┌───────────┼───────────┐           │
│                              ▼           ▼           ▼           │
│                          Lambda x100 (parallel workers)          │
│                              │           │           │           │
│                              └───────────┼───────────┘           │
│                                          ▼                       │
│                              Lambda (aggregator) → DynamoDB     │
└──────────────────────────────────────────────────────────────────┘
```

## Real-World Use Cases

### 1. E-Commerce Order Pipeline

```text
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

### 2. Real-Time Data Pipeline

```text
Data Pipeline:
┌─────────────────────────────────────────────────────────────────┐
│  Kinesis → Lambda (Transform) → DynamoDB → Lambda (Aggregate)  │
│                                        │                        │
│                                        ▼                        │
│                               S3 (Data Lake)                    │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No retry / DLQ for async invocations | Configure SQS DLQ; alert on DLQ depth |
| Over-orchestrating simple workflows with Step Functions | Use direct Lambda → SQS → Lambda for 2-3 step flows |
| Ignoring idempotency for at-least-once event sources | Use event ID or deterministic key for DB writes |
| Tight coupling (Lambda A calls Lambda B synchronously) | Decouple with SQS/SNS; let failures retry independently |
| Missing observability for async flows | Use X-Ray for distributed tracing across SQS → Lambda → DynamoDB |

## Best Practices

1. **Design for failure** — retries, DLQs, circuit breakers, idempotency
2. **Single-responsibility functions** — one trigger, one purpose
3. **Idempotent handlers** — duplicate events are a guarantee, not a possibility
4. **Decouple with queues** — never chain synchronous Lambda → Lambda
5. **Orchestrate with Step Functions** for multi-step workflows with branching / humans-in-the-loop
6. **Monitor everything** — CloudWatch metrics, X-Ray traces, structured logs

## Performance Considerations

```text
Pattern Selection Guide:
┌──────────────────────────────────────────────────────────────────┐
│  Simple API:              API Gateway + Lambda                   │
│  Async Processing:        SQS + Lambda (with partial batch)     │
│  Pub/Sub fan-out:         SNS → multiple Lambdas                │
│  Event bus:               EventBridge + targets                 │
│  Complex Workflow:        Step Functions                        │
│  Real-time:               WebSocket API + DynamoDB              │
│  Data Streaming:          Kinesis → Lambda                      │
│  Fan-out / fan-in:        SNS → SQS → workers → aggregator     │
│  CDC:                     DynamoDB Streams / Kinesis → Lambda  │
└──────────────────────────────────────────────────────────────────┘
```

## Summary

- Serverless patterns are battle-tested templates for common architectures: API, event-driven, orchestration, and data
- Always decouple async work with SQS or SNS — never chain synchronous Lambda → Lambda
- Use Step Functions for multi-step workflows with retries, parallelism, and human-in-the-loop steps
- Make every handler idempotent — at-least-once delivery is a guarantee from SQS, Streams, and EventBridge
- Monitor distributed async flows with X-Ray; alert on DLQ depth

---

## Cheat Sheet

```text
SERVERLESS PATTERNS CHEAT SHEET
═══════════════════════════════════════════════════════════════

CHOOSE BY WORKFLOW SHAPE:
  • 1 trigger → 1 sync response   API Gateway + Lambda
  • 1 trigger → 1 async result   SQS + Lambda
  • 1 trigger → N consumers       SNS fan-out
  • Multi-domain events           EventBridge bus
  • Multi-step workflow           Step Functions
  • State + coordinating logic    Step Functions + Lambda
  • Real-time bidirectional       WebSocket API + DynamoDB

IDEMPOTENCY CHEAT:
  • SQS / Streams: at-least-once   → use event ID as DB key
  • SNS: at-least-once             → same
  • EventBridge: at-least-once     → use idempotency key field
  • API Gateway: at-most-once      → still design for client retries

INTERVIEW ANSWER:
  1. What problem the pattern solves
  2. Failure modes (DLQ, retries, idempotency)
  3. Cost / performance trade-off
  4. Real production example
```

---

## See Also

- [AWS Lambda](05-AWS-Lambda.md)
- [Edge Functions](02-Edge-Functions.md)
- [Microservices](../12-Microservices/)
- [Observability](../22-Observability/)
- [Serverless Overview](01-Serverless-Overview.md)
- [Vercel Deployments](06-Vercel-Deployments.md)


## References & Learn More

- [AWS Serverless Patterns](https://serverlessland.com/patterns)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/)
- [Event-Driven Architecture on AWS](https://aws.amazon.com/event-driven-architecture/)
- [Serverless Best Practices (AWS)](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Serverless Framework Patterns](https://www.serverless.com/framework/docs/)
