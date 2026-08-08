---
section: Serverless & Edge
category: DevOps
tags: [concept, overview]
---

# Serverless Overview

> Serverless computing is a cloud execution model where the cloud provider dynamically manages the allocation and provisioning of servers. Developers write and deploy code without worrying about the underlying infrastructure, paying only for actual compute time consumed.

## Definition

Serverless is a cloud execution model in which the provider dynamically allocates compute resources on demand, billed per request and per GB-second. Developers deploy units of business logic (functions) and never touch servers, scaling, or capacity planning.

## Why It Matters (TL;DR)

- **No server management** — no patching, scaling, or capacity planning
- **Auto-scaling**, including to zero
- **Pay only for execution time**, not idle resources
- **Faster development** — focus on code, not infrastructure
- **High availability and fault tolerance** built in

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    SERVERLESS ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐  │
│  │   Request   │ ──▶ │    API      │ ──▶ │   Function          │  │
│  │   (HTTP)    │     │   Gateway   │     │   (Lambda/Function) │  │
│  └─────────────┘     └─────────────┘     └──────────┬──────────┘  │
│                                                      │              │
│                                                      ▼              │
│                                            ┌─────────────────────┐  │
│                                            │   Cloud Services    │  │
│                                            │   • DynamoDB        │  │
│                                            │   • S3              │  │
│                                            │   • SQS             │  │
│                                            └─────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Provider Responsibilities                 │   │
│  │  • Server provisioning    • Auto-scaling                    │   │
│  │  • OS patching            • Load balancing                  │   │
│  │  • Runtime management     • High availability               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Developer Responsibilities                │   │
│  │  • Write function code    • Define triggers                 │   │
│  │  • Configure permissions  • Set resource limits             │   │
│  │  • Monitor and debug      • Handle errors                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## FaaS vs Containers vs Traditional Servers

| Dimension | Serverless (FaaS) | Containers | Traditional VM/Bare-metal |
|-----------|-------------------|------------|---------------------------|
| Provisioning | None | Image + orchestrator | OS + runtime + app |
| Cold start | 100ms–2s (V8: <5ms) | Seconds (image pull) | None |
| Billing | Per request + GB-s | Per CPU/memory allocated | Per hour/month reserved |
| Max execution | 15 min (Lambda) | Unlimited | Unlimited |
| Scaling model | Automatic, to zero | Horizontal via orchestrator | Manual, capacity planning |
| Best for | Spiky/unpredictable traffic | Long-running services, stateful | Legacy, custom hardware, full control |
| Cost at low load | Lowest | Mid | Highest (idle) |
| Vendor lock-in | High | Medium (portable images) | Low |

## Code Examples

### 1. AWS Lambda Handler (API Gateway Proxy)

```typescript
// handler.ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

interface User {
  id: string;
  name: string;
  email: string;
}

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const { httpMethod, path, body } = event;
  const requestBody = body ? JSON.parse(body) : null;

  if (httpMethod === 'GET' && path === '/users') {
    const users = await getUsers();
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(users),
    };
  }

  if (httpMethod === 'POST' && path === '/users') {
    const newUser = await createUser(requestBody);
    return { statusCode: 201, body: JSON.stringify(newUser) };
  }

  return { statusCode: 404, body: JSON.stringify({ error: 'Not found' }) };
};
```

### 2. Cold Start Optimization (Hoist Clients)

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

// Hoisted — reused on warm starts; cold start only pays this once
const docClient = DynamoDBDocumentClient.from(new DynamoDBClient({}));

export const handler = async (event: APIGatewayProxyEvent) => {
  const result = await docClient.send(
    new GetCommand({
      TableName: 'Users',
      Key: { id: event.pathParameters?.id },
    })
  );
  return { statusCode: 200, body: JSON.stringify(result.Item ?? null) };
};
```

### 3. Vercel Serverless Function (Node Runtime)

```typescript
// api/users.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  switch (req.method) {
    case 'GET':
      return res.status(200).json(await fetchUsers(req.query));
    case 'POST':
      return res.status(201).json(await createUser(req.body));
    case 'DELETE':
      await deleteUser(req.query.id as string);
      return res.status(204).end();
    default:
      return res.status(405).json({ error: 'Method not allowed' });
  }
}
```

### 4. Event-Driven: DynamoDB Stream → Lambda

```typescript
import { DynamoDBStreamEvent, DynamoDBStreamHandler } from 'aws-lambda';
import { unmarshall } from '@aws-sdk/util-dynamodb';

export const handler: DynamoDBStreamHandler = async (event: DynamoDBStreamEvent) => {
  for (const record of event.Records) {
    if (record.eventName === 'INSERT' && record.dynamodb?.NewImage) {
      await processNewItem(unmarshall(record.dynamodb.NewImage as Record<string, unknown>));
    }
  }
};
```

### 5. S3 Event → Image Processing

```typescript
import { S3Event, S3Handler } from 'aws-lambda';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';
import { Readable } from 'stream';

const s3 = new S3Client({});

export const handler: S3Handler = async (event: S3Event) => {
  for (const record of event.Records) {
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '));
    const obj = await s3.send(
      new GetObjectCommand({ Bucket: record.s3.bucket.name, Key: key })
    );
    const chunks: Buffer[] = [];
    for await (const chunk of obj.Body as Readable) chunks.push(Buffer.from(chunk));
    await processFile(key, Buffer.concat(chunks));
  }
};
```

## Real-World Use Cases

### 1. REST API for a Mobile App

```text
Use Case: RESTful API for mobile app
┌─────────────────────────────────────────────────────────────────┐
│  Client → API Gateway → Lambda → DynamoDB                       │
│                                                                 │
│  Benefits:                                                      │
│  • Auto-scaling for traffic spikes                              │
│  • Pay per request                                              │
│  • No server management                                         │
│  • Built-in authentication (Cognito)                            │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Real-Time Data Pipeline

```text
Use Case: Real-time data transformation
┌─────────────────────────────────────────────────────────────────┐
│  S3 Upload → Lambda (transform) → Redshift                     │
│                                                                 │
│  Benefits:                                                      │
│  • Event-driven processing                                      │
│  • Automatic parallelism                                        │
│  • Cost-effective for sporadic workloads                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Webhook Receivers

```text
Use Case: GitHub webhook → Slack notification
┌─────────────────────────────────────────────────────────────────┐
│  GitHub → API Gateway → Lambda → SNS → Slack                   │
│                                                                 │
│  Why serverless:                                                │
│  • Webhooks are bursty (idle most of the day)                   │
│  • Auto-scales during deploy events / incidents                 │
│  • Pay nothing for the 99% of time nothing is happening         │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Initializing clients inside the handler | Hoist AWS SDK / DB clients to module scope |
| Treating state as persistent across invocations | Use DynamoDB / ElastiCache; in-memory state is unreliable |
| Long-running work in a single function | Use Step Functions or chain multiple Lambdas; respect 15-min timeout |
| Cold start surprising p99 | Use Provisioned Concurrency, SnapStart (Java), smaller packages |
| Missing DLQ on async / stream invocations | Configure SQS/SNS DLQ; alert on queue age |
| No idempotency for at-least-once event sources | Use event ID as idempotency key in DB write |

## Best Practices

1. **Minimize cold starts** — small packages, hoisted clients, avoid VPC unless required
2. **Right-size memory** — more memory = more CPU; tune with Lambda Power Tuning
3. **Use Provisioned Concurrency** for latency-sensitive APIs
4. **Implement error handling** — DLQs, retries, Lambda Destinations for observability
5. **Monitor and alert** — track cold starts, duration, error rates, throttles
6. **Design for failure** — circuit breakers, timeouts, fallbacks
7. **Single-responsibility functions** — one trigger, one purpose; compose with Step Functions

## Performance Considerations

```text
Cold Start Optimization:
┌─────────────────────────────────────────────────────────────────┐
│  Impact on Cold Start:                                          │
│  • Runtime choice: Node.js < Go < Python < Java < .NET          │
│  • Package size: Smaller = faster                               │
│  • VPC configuration: Adds 1-2 seconds (use VPC endpoint instead)│
│  • Memory allocation: More memory = faster init                 │
│                                                                 │
│  Optimization Strategies:                                       │
│  • Use Lambda@Edge / Cloudflare Workers for global deployment   │
│  • Implement connection pooling (RDS Proxy for relational DBs)  │
│  • Lazy load heavy dependencies                                 │
│  • Use SnapStart (Java, Python) — 10x faster cold starts        │
│  • Provisioned Concurrency for predictable p99                   │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- Serverless is a cloud execution model where the provider manages servers and the developer ships functions
- FaaS differs from containers and traditional servers in provisioning, billing, and scaling model
- Cold starts (100ms–2s) are the main performance concern; mitigations include hoisted clients, SnapStart, Provisioned Concurrency, and smaller packages
- Serverless shines for spiky traffic, event-driven workloads, and short-lived tasks
- Always design for failure: DLQs, retries, idempotency, and observability are non-negotiable

---

## Cheat Sheet

```text
SERVERLESS OVERVIEW CHEAT SHEET
═══════════════════════════════════════════════════════════════

EXECUTION MODELS:
  • FaaS         — pay per request, auto-scaling, 15-min max
  • Containers   — always-on, portable, custom runtimes
  • Traditional  — full control, idle cost, manual scaling

COLD START MITIGATIONS:
  • Hoist clients outside handler
  • Smaller deployment packages (esbuild / SAM NodejsFunction)
  • Provisioned Concurrency
  • SnapStart (Java / Python)
  • Avoid VPC unless required; use VPC endpoint

INTERVIEW ANSWER FRAMEWORK:
  1. Definition (1-2 sentences)
  2. How it works (event sources, lifecycle)
  3. Use cases (when to reach for it)
  4. Trade-offs (cost, cold start, lock-in)
  5. Real production example
```

---

## See Also

- [AWS Lambda](05-AWS-Lambda.md)
- [Docker](../13-Docker/)
- [Edge Functions](02-Edge-Functions.md)
- [Next.js](../04-NextJS/)
- [Observability](../22-Observability/)
- [Serverless Patterns](03-Serverless-Patterns.md)
- [Vercel Deployments](06-Vercel-Deployments.md)


## References & Learn More

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)
- [Serverless Best Practices (AWS)](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Serverless Framework](https://www.serverless.com/)
- [The Twelve-Factor App](https://12factor.net/)
- [Vercel Serverless Functions](https://vercel.com/docs/functions)
