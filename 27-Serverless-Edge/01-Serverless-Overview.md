# Serverless Overview

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

 provider dynamically manages the allocation and provisioning of servers. Developers write and deploy code without worrying about the underlying infrastructure, paying only for actual compute time consumed.

## Why Do We Need It?

- **No Server Management**: No patching, updating, or maintaining servers
- **Auto-Scaling**: Automatically scales with demand, including to zero
- **Cost Efficiency**: Pay only for execution time, not idle resources
- **Faster Development**: Focus on code, not infrastructure
- **High Availability**: Built-in redundancy and fault tolerance

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

## AWS Lambda

### Lambda Execution Model

```text
Lambda Function Lifecycle:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Cold    │ ──▶ │  Init    │ ──▶ │  Invoke  │ ──▶ │ Shutdown │ │
│  │  Start   │    │  Phase   │    │  Phase   │    │ (if idle)│ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                 │
│  Cold Start: Download code, start runtime, run init code       │
│  Init Phase: Run static initialization (outside handler)       │
│  Invoke Phase: Execute handler function                        │
│  Shutdown: After idle timeout (default 3 min)                  │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Basic AWS Lambda Function

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

  // Parse request
  const requestBody = body ? JSON.parse(body) : null;

  // Route handling
  if (httpMethod === 'GET' && path === '/users') {
    const users = await getUsers();
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(users),
    };
  }

  if (httpMethod === 'POST' && path === '/users') {
    const newUser = await createUser(requestBody);
    return {
      statusCode: 201,
      body: JSON.stringify(newUser),
    };
  }

  return {
    statusCode: 404,
    body: JSON.stringify({ error: 'Not found' }),
  };
};

async function getUsers(): Promise<User[]> {
  // Fetch from database
  return [
    { id: '1', name: 'John Doe', email: 'john@example.com' },
  ];
}

async function createUser(data: Partial<User>): Promise<User> {
  // Create in database
  return {
    id: '2',
    name: data.name || '',
    email: data.email || '',
  };
}

```

### 2. Vercel Serverless Function

```typescript
// api/users.ts
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
  const { method, query, body } = req;

  switch (method) {
    case 'GET':
      const users = await fetchUsers(query);
      return res.status(200).json(users);

    case 'POST':
      const newUser = await createUser(body);
      return res.status(201).json(newUser);

    case 'PUT':
      const updated = await updateUser(query.id as string, body);
      return res.status(200).json(updated);

    case 'DELETE':
      await deleteUser(query.id as string);
      return res.status(204).end();

    default:
      return res.status(405).json({ error: 'Method not allowed' });
  }
}

async function fetchUsers(query: Record<string, string>) {
  // Implementation
  return [];
}

async function createUser(data: any) {
  // Implementation
  return { id: '1', ...data };
}

async function updateUser(id: string, data: any) {
  // Implementation
  return { id, ...data };
}

async function deleteUser(id: string) {
  // Implementation
}

```

### 3. Cold Start Optimization

```typescript
// Optimized Lambda function
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand } from '@aws-sdk/lib-dynamodb';

// Initialize outside handler (reused across invocations)
const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

export const handler = async (event: APIGatewayProxyEvent) => {
  const { id } = event.pathParameters || {};

  // Use initialized client
  const result = await docClient.send(
    new GetCommand({
      TableName: 'Users',
      Key: { id },
    })
  );

  return {
    statusCode: 200,
    body: JSON.stringify(result.Item),
  };
};

```

### 4. Serverless with DynamoDB Streams

```typescript
// Process DynamoDB stream events
import { DynamoDBStreamEvent, DynamoDBStreamHandler } from 'aws-lambda';
import { unmarshall } from '@aws-sdk/util-dynamodb';

export const handler: DynamoDBStreamHandler = async (
  event: DynamoDBStreamEvent
) => {
  for (const record of event.Records) {
    if (record.eventName === 'INSERT') {
      const newImage = record.dynamodb?.NewImage;
      if (newImage) {
        const item = unmarshall(newImage as any);
        await processNewItem(item);
      }
    }

    if (record.eventName === 'MODIFY') {
      const oldImage = record.dynamodb?.OldImage;
      const newImage = record.dynamodb?.NewImage;
      if (oldImage && newImage) {
        const oldItem = unmarshall(oldImage as any);
        const newItem = unmarshall(newImage as any);
        await processUpdatedItem(oldItem, newItem);
      }
    }
  }
};

async function processNewItem(item: Record<string, any>) {
  console.log('New item:', item);
  // Send notification, update search index, etc.
}

async function processUpdatedItem(
  oldItem: Record<string, any>,
  newItem: Record<string, any>
) {
  console.log('Item updated:', { old: oldItem, new: newItem });
  // Update related data, trigger workflows, etc.
}

```

### 5. Serverless with S3 Events

```typescript
// Process S3 upload events
import { S3Event, S3Handler } from 'aws-lambda';
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

const s3Client = new S3Client({});

export const handler: S3Handler = async (event: S3Event) => {
  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, ' '));

    // Get the uploaded file
    const response = await s3Client.send(
      new GetObjectCommand({ Bucket: bucket, Key: key })
    );

    const content = await streamToString(response.Body);

    // Process the file
    await processFile(key, content);
  }
};

async function streamToString(stream: any): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of stream) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString('utf-8');
}

async function processFile(key: string, content: string) {
  console.log(`Processing file: ${key}`);
  // Image processing, data validation, etc.
}

```

## Real-World Use Cases

### API Backend

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

### Data Processing Pipeline

```text
Use Case: Real-time data transformation
┌─────────────────────────────────────────────────────────────────┐
│  S3 Upload → Lambda → Transform → Write to Redshift             │
│                                                                 │
│  Benefits:                                                      │
│  • Event-driven processing                                      │
│  • Automatic parallelism                                        │
│  • Cost-effective for sporadic workloads                        │
└─────────────────────────────────────────────────────────────────┘

```

## Common Mistakes

1. **Cold start latency**: Not optimizing initialization code

2. **Memory allocation**: Under-provisioning memory (also affects CPU)

3. **Timeout limits**: Not handling long-running processes

4. **Vendor lock-in**: Over-relying on provider-specific features

5. **State management**: Assuming state between invocations

## Best Practices

1. **Minimize cold starts**: Keep packages small, initialize clients outside handler

2. **Right-size memory**: More memory = more CPU = faster execution

3. **Use provisioned concurrency**: For latency-sensitive applications

4. **Implement error handling**: Dead letter queues, retry mechanisms

5. **Monitor and alert**: Track cold starts, duration, error rates

## Performance Considerations

```text
Cold Start Optimization:
┌─────────────────────────────────────────────────────────────────┐
│  Impact on Cold Start:                                          │
│  • Runtime choice: Node.js < Java < .NET                        │
│  • Package size: Smaller = faster                               │
│  • VPC configuration: Adds 1-2 seconds                          │
│  • Memory allocation: More memory = faster init                 │
│                                                                 │
│  Optimization Strategies:                                       │
│  • Use Lambda@Edge for global deployment                        │
│  • Implement connection pooling                                 │
│  • Lazy load dependencies                                       │
│  • Use SnapStart (Java)                                         │
└─────────────────────────────────────────────────────────────────┘

```

## Summary

Serverless computing provides a powerful model for building scalable, cost-effective applications without managing infrastructure. Understand Lambda's execution model, cold start optimization, and best practices for production deployments.

---

## Cheat Sheet
```text
SERVERLESS OVERVIEW CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  Lambda Function Lifecycle:
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
  │  │  Cold    │ ──▶ │  Init    │ ──▶ │  Invoke  │ ──▶ │ Shutdown │ │
  │  │  Start   │    │  Phase   │    │  Phase   │    │ (if idle)│ │
```
```
  Use Case: RESTful API for mobile app
  ┌─────────────────────────────────────────────────────────────────┐
  │  Client → API Gateway → Lambda → DynamoDB                       │
  │                                                                 │
  │  Benefits:                                                      │
  │  • Auto-scaling for traffic spikes                              │
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [Docker](../13-Docker/)
- [Next.js](../04-NextJS/)
- [Observability](../22-Observability/)

## References & Learn More

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Serverless Framework](https://www.serverless.com/)
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)
- [Vercel Serverless Functions](https://vercel.com/docs/functions)
- [Serverless Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
