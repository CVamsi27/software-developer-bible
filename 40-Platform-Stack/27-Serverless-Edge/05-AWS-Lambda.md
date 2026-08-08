---
section: Serverless & Edge
category: DevOps
tags: [concept, reference]
---

# AWS Lambda

> **AWS Lambda** is Amazon's Function-as-a-Service (FaaS) platform that runs code in response to events without provisioning servers. It supports multiple runtimes (Node.js, Python, Java, Go) and integrates with 200+ AWS services as event sources.

## Definition

AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources. You upload code as a Lambda function and the service handles everything required to run and scale it with high availability.

## Why Do We Need It?

| Problem | Solution |
|---------|----------|
| Provisioning and patching servers | Fully managed runtime — no servers to operate |
| Capacity planning for variable traffic | Auto-scaling from 0 to thousands of concurrent executions |
| Paying for idle capacity | Pay-per-request and per-GB-second pricing |
| Glue code between AWS services | Native event-source mappings (S3, SQS, DynamoDB Streams, EventBridge) |
| Global request latency | Lambda@Edge runs code at CloudFront edge locations |

## How It Works

```text
┌──────────────────────────────────────────────────────────────────┐
│                    LAMBDA EXECUTION MODEL                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │  Cold    │ ──▶│  Init    │ ──▶│  Invoke  │ ──▶│ Shutdown │   │
│  │  Start   │    │  Phase   │    │  Phase   │    │ (idle)   │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│                                                                  │
│  Cold Start: Download code, start runtime, run init code        │
│  Init Phase: Run static initialization (outside handler)        │
│  Invoke Phase: Execute handler function                         │
│  Shutdown:   After idle timeout (default 3 min)                 │
└──────────────────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Detail |
|---------|--------|
| **Event Sources** | API Gateway, S3, SQS, DynamoDB Streams, SNS, EventBridge, CloudWatch, Kinesis |
| **Cold Start** | ~200ms–1s delay on first invocation after idle (Node.js); Java/Python can be slower |
| **Timeout** | Max 15 minutes per invocation |
| **Memory** | 128MB – 10,240MB (CPU scales linearly with memory) |
| **Concurrency** | 1,000 (default) per region, can be raised via support ticket |
| **Lambda@Edge** | Runs at CloudFront edge PoPs for low-latency request/response modification |
| **SnapStart** | Snapshots initialized function (Java, Python) to remove cold-start latency |
| **Provisioned Concurrency** | Pre-warmed execution environments — predictable latency at higher cost |

## Code Examples

### 1. TypeScript Handler (API Gateway Proxy)

```typescript
// handler.ts
import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

// Initialize outside handler — reused across invocations (warm starts)
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

export const handler = async (
  event: APIGatewayProxyEvent
): Promise<APIGatewayProxyResult> => {
  const { httpMethod, path } = event;

  if (httpMethod === 'GET' && path === '/users') {
    const result = await docClient.send(
      new GetCommand({
        TableName: process.env.TABLE_NAME!,
        Key: { id: event.pathParameters?.id },
      })
    );

    return {
      statusCode: result.Item ? 200 : 404,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(result.Item ?? { error: 'Not found' }),
    };
  }

  return { statusCode: 405, body: 'Method Not Allowed' };
};
```

### 2. Stream Handler (DynamoDB Streams)

```typescript
import { DynamoDBStreamEvent, DynamoDBStreamHandler } from 'aws-lambda';
import { unmarshall } from '@aws-sdk/util-dynamodb';

export const handler: DynamoDBStreamHandler = async (
  event: DynamoDBStreamEvent
) => {
  for (const record of event.Records) {
    const newImage = record.dynamodb?.NewImage;
    if (newImage && record.eventName === 'INSERT') {
      const item = unmarshall(newImage as Record<string, unknown>);
      await processNewItem(item);
    }
  }
};

async function processNewItem(item: Record<string, unknown>): Promise<void> {
  // Update search index, fan out notifications, etc.
}
```

### 3. S3 Event Handler (Image Processing)

```typescript
import { S3Event, S3Handler } from 'aws-lambda';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({});

export const handler: S3Handler = async (event: S3Event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '));

    const obj = await s3Client.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
    const body = await obj.Body!.transformToString();

    // Resize, OCR, virus scan, etc.
    await processFile(key, body);
  }
};
```

### 4. Provisioned Concurrency (CDK / IaC)

```typescript
// CDK example — keeps N execution environments warm
import { Function, Runtime, Code } from 'aws-cdk-lib/aws-lambda';
import { Version, Alias } from 'aws-cdk-lib/aws-lambda';

const fn = new Function(this, 'MyFn', {
  runtime: Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: Code.fromAsset('lambda'),
});

const version = fn.currentVersion;
const alias = new Alias(this, 'LiveAlias', {
  aliasName: 'live',
  version,
  provisionedConcurrentExecutions: 5,
});
```

### 5. Lambda Layer (Shared Dependencies)

```bash
# Build a layer
mkdir -p layer/nodejs
cd layer/nodejs && npm init -y && npm install lodash
cd .. && zip -r layer.zip nodejs

# Reference in CloudFormation/SAM
# Properties:
#   Layers:
#     - !Ref MySharedLayer
```

## Real-World Use Cases

1. **REST/GraphQL API backend** — API Gateway + Lambda + DynamoDB. Auto-scales, pay-per-request.
2. **Image/video processing pipeline** — S3 event → Lambda (transcode, thumbnail) → S3.
3. **Change-data-capture (CDC)** — DynamoDB Streams / Kinesis → Lambda → downstream (search index, audit log, materialized view).
4. **Scheduled jobs** — EventBridge cron rule → Lambda. Replaces cron servers for ops tasks.
5. **Webhook handlers** — API Gateway → Lambda. Stripe, GitHub, Slack webhooks scale instantly.
6. **Slack/Discord bots** — API Gateway + Lambda + DynamoDB. Cold-start cost is offset by low per-message compute.
7. **Event-driven glue** — SQS/SNS fan-out for order processing, notifications, and audit trails.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Initializing AWS SDK clients inside the handler | Hoist clients to module scope; reused on warm starts |
| No DLQ on async / stream invocations | Configure SQS or SNS dead-letter queue; alert on age |
| Treating state as persistent across invocations | Use DynamoDB, ElastiCache, or Lambda Destinations; in-memory state is unreliable |
| Long-running workflow in a single function | Use Step Functions or break into chained Lambdas; respect the 15-min timeout |
| Cold starts surprising p99 | Use SnapStart (Java/Python), Provisioned Concurrency, or smaller deployment packages |
| Forgetting idempotency | SQS / Streams can deliver the same event twice — design handlers to be idempotent (e.g., by event ID) |

## Best Practices

1. **Keep packages small** — Use esbuild, webpack, or SAM `NodejsFunction` with `esbuild` bundling. Smaller ZIPs = faster cold starts.
2. **Right-size memory** — More memory = more CPU. Tune with [AWS Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning).
3. **Use environment variables for config** — Never bake secrets into code. Reference Secrets Manager / SSM Parameter Store via extension.
4. **Structured JSON logging** — Emit JSON to CloudWatch; wire to OpenSearch or a third-party (Datadog, Lumigo) for searchability.
5. **Idempotency tokens** — For writes triggered by retried events, use the event ID or a deterministic hash as the idempotency key.
6. **Use destinations for failures** — Lambda Destinations (SQS/SNS/EventBridge) for async failures — better than DLQ for observability.
7. **X-Ray tracing** — Enable Active Tracing to debug latency across API Gateway → Lambda → DynamoDB.

## Performance Considerations

```text
COLD START OPTIMIZATION:
┌──────────────────────────────────────────────────────────────────┐
│  Runtime cost:    Node.js < Go < Python < .NET < Java             │
│  Package size:    Smaller = faster init (target < 5 MB)          │
│  VPC access:      ENI attach adds 1-2s to cold start             │
│  Memory:          Linear CPU scaling — test 512-3008 MB           │
│  SnapStart:       10x faster for Java; up to 2x for Python       │
│  Provisioned:     Removes cold start entirely ($$)                │
└──────────────────────────────────────────────────────────────────┘

CONCURRENCY MODEL:
  - Account soft limit: 1,000 concurrent executions (per region)
  - Reserved concurrency: caps a function (protects downstream)
  - Provisioned concurrency: pre-warms environments
  - Burst concurrency: 500-3000 instant (region-dependent)
```

## Summary

- AWS Lambda is a serverless compute service that runs code in response to events without provisioning servers
- Event sources include API Gateway, S3, DynamoDB Streams, SQS, SNS, EventBridge, and CloudWatch
- Cold starts impact latency — mitigated by SnapStart, Provisioned Concurrency, smaller packages, and client hoisting
- Lambda@Edge runs functions at CloudFront edge PoPs for low-latency request/response modification
- Best practices: stateless design, environment-variable config, idempotent handlers, DLQs, structured logs, X-Ray tracing

---

## Cheat Sheet

```text
AWS LAMBDA CHEAT SHEET
═══════════════════════════════════════════════════════════════

LIMITS:
  • Memory:      128 MB – 10,240 MB
  • Timeout:     Max 15 minutes
  • Payload:     6 MB (sync), 256 KB (async)
  • Concurrency: 1,000 default (per region, soft limit)

COLD START MITIGATIONS:
  • Hoist clients outside handler
  • Use SnapStart (Java/Python)
  • Provisioned Concurrency
  • Smaller deployment packages
  • Avoid VPC unless required (or use VPC endpoint / RDS Proxy)

EVENT SOURCES:
  • Sync:  API Gateway, ALB, CloudFront (Lambda@Edge)
  • Async: S3, SNS, EventBridge, S3
  • Stream: Kinesis, DynamoDB Streams, SQS (event source mapping)

INTERVIEW TIPS:
  - Explain the cold start → warm reuse lifecycle
  - Discuss when Lambda beats containers (and vice versa)
  - Bring up connection pooling via RDS Proxy
  - Mention idempotency for at-least-once event sources
```

---

## See Also

- [Edge Functions](02-Edge-Functions.md)
- [Observability](../22-Observability/)
- [Serverless Overview](01-Serverless-Overview.md)
- [Serverless Patterns](03-Serverless-Patterns.md)
- [Vercel Deployments](06-Vercel-Deployments.md)


## References & Learn More

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda Destinations](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html#invocation-async-destinations)
- [Lambda Power Tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)
- [Lambda@Edge](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions.html)
- [SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)
