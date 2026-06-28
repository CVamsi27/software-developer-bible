# Serverless/Edge Interview Questions

## Definition
This comprehensive guide covers 25+ interview questions on serverless and edge computing, from fundamentals to advanced system design.

## Why Do We Need It?
- **Technical Interviews**: Serverless and edge are modern cloud paradigms
- **System Design**: Understanding serverless architecture is crucial
- **Cost Optimization**: Serverless economics are interview favorites
- **Scalability**: Serverless auto-scaling is a key advantage

## How It Works

```text
Interview Question Categories:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Fundamentals│  │   Patterns  │  │      System Design      │ │
│  │             │  │             │  │                         │ │
│  │ • Concepts  │  │ • API       │  │ • E-commerce            │ │
│  │ • Benefits  │  │ • Event     │  │ • Real-time             │ │
│  │ • Trade-offs│  │ • Workflow  │  │ • Data Pipeline         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Common Interview Answer Patterns

```typescript
// Pattern 1: Concept → Use Case → Trade-offs
function answerPattern(concept: string): string {
  return `
    1. Concept: What ${concept} is
    2. Use Case: When to use it
    3. Implementation: How it works
    4. Trade-offs: Benefits and limitations
  `;
}

// Pattern 2: Problem → Solution → Architecture
function architecturePattern(problem: string): string {
  return `
    1. Problem: ${problem}
    2. Solution: Serverless/Edge approach
    3. Architecture: Components and flow
    4. Considerations: Cost, performance, reliability
  `;
}
```

## Interview Questions

### Beginner (5)

**Q1: What is serverless computing?**
- **Answer**: A cloud model where providers manage servers; developers deploy code without infrastructure concerns, paying only for execution time.

**Q2: What are the benefits of serverless?**
- **Answer**: No server management, auto-scaling, pay-per-use, faster development, built-in availability, reduced operational costs.

**Q3: What is AWS Lambda?**
- **Answer**: AWS's serverless compute service that runs code in response to events without provisioning or managing servers.

**Q4: What is a cold start?**
- **Answer**: The initialization time when a serverless function is invoked for the first time or after being idle, including downloading code and starting the runtime.

**Q5: What are edge functions?**
- **Answer**: Serverless functions that run at CDN edge locations, close to users, reducing latency for dynamic content processing.

### Intermediate (5)

**Q6: How do you reduce cold start latency?**
- **Answer**: Keep packages small, initialize clients outside handler, use provisioned concurrency, choose faster runtimes, minimize VPC configuration.

**Q7: What is the difference between API Gateway HTTP API and REST API?**
- **Answer**: HTTP API is simpler, cheaper, and faster with fewer features. REST API has more features like request validation, caching, and API keys.

**Q8: How do you handle errors in serverless functions?**
- **Answer**: Implement try-catch, use dead letter queues for async invocations, set up CloudWatch alarms, implement retry logic.

**Q9: What is the maximum execution time for Lambda?**
- **Answer**: 15 minutes. For longer processes, use Step Functions or break into smaller tasks.

**Q10: What is a Lambda layer?**
- **Answer**: A package of libraries and dependencies that can be shared across multiple functions, reducing deployment package size.

### Senior (10)

**Q11: How do you handle long-running processes in serverless?**
- **Answer**: Break into smaller functions, use Step Functions for orchestration, implement async processing with SQS/SNS, or use Fargate for truly long-running tasks.

**Q12: Explain Lambda concurrency limits**
- **Answer**: Default 1000 concurrent executions per region. Can request increase. Use reserved concurrency for critical functions, provisioned concurrency for latency-sensitive.

**Q13: How do you implement connection pooling in Lambda?**
- **Answer**: Initialize database connections outside the handler to reuse across invocations. Use RDS Proxy for database connection management.

**Q14: What is the difference between SQS and SNS?**
- **Answer**: SQS is point-to-point (one consumer); SNS is pub-sub (many consumers). SQS buffers messages; SNS routes immediately.

**Q15: How do you handle state in serverless?**
- **Answer**: Use external stores like DynamoDB, ElastiCache, or S3. Don't rely on in-memory state between invocations.

**Q16: What is the impact of VPC on Lambda?**
- **Answer**: VPC configuration adds cold start latency (1-2 seconds) but provides access to VPC resources like RDS.

**Q17: How do you test serverless functions locally?**
- **Answer**: Use SAM Local, Serverless Offline, or LocalStack for local testing and debugging.

**Q18: What is Lambda@Edge?**
- **Answer**: Lambda functions that run at CloudFront edge locations, enabling low-latency processing close to users.

**Q19: How do you handle authentication at the edge?**
- **Answer**: Verify JWTs at the edge, use KV for token blacklists, implement refresh token rotation, use Cloudflare Access.

**Q20: What are the limitations of edge functions?**
- **Answer**: CPU time limits (10ms-30s), memory limits (128MB), limited Node.js API support, stateless execution, vendor lock-in.

### FAANG-style (5)

**Q21: Design a serverless architecture for a real-time chat application**
- **Answer**:
  - API Gateway + Lambda for API
  - WebSocket API for real-time
  - DynamoDB for storage
  - ElastiCache for session management
  - SNS for notifications
  - Consider: Connection management, message ordering, offline support

**Q22: How would you implement CI/CD for serverless?**
- **Answer**:
  - Use GitHub Actions/GitLab CI
  - SAM/Serverless Framework for deployment
  - Automated testing with SAM Local
  - Implement canary deployments
  - Use CloudFormation for infrastructure as code

**Q23: Explain serverless at scale**
- **Answer**:
  - Handle cold starts with provisioned concurrency
  - Implement circuit breakers
  - Use multiple regions for availability
  - Optimize cost with right-sizing
  - Monitor with CloudWatch and X-Ray

**Q24: How do you debug serverless in production?**
- **Answer**:
  - Use X-Ray for distributed tracing
  - CloudWatch Logs Insights for log analysis
  - Implement structured logging
  - Use custom metrics
  - Enable Lambda Insights

**Q25: Design a serverless data pipeline for analytics**
- **Answer**:
  - Kinesis for streaming ingestion
  - Lambda for ETL processing
  - S3 for data lake storage
  - Athena for querying
  - Glue for data cataloging
  - QuickSight for visualization

### Follow-ups (5)

**Q26: How do you handle secrets in serverless?**
- **Answer**: Use AWS Secrets Manager or Parameter Store, avoid hardcoding, rotate secrets regularly, use IAM roles for service access.

**Q27: What is the impact of serverless on database design?**
- **Answer**: Consider connection pooling, use serverless-friendly databases (DynamoDB, Aurora Serverless), optimize for Lambda's execution model.

**Q28: How do you handle rate limiting in serverless?**
- **Answer**: Use API Gateway throttling, implement token bucket in DynamoDB, use WAF for additional protection, implement per-user limits.

**Q29: What are the cost considerations for serverless?**
- **Answer**: Pay per request and duration, consider provisioned concurrency costs, monitor for cost optimization opportunities, compare with container alternatives.

**Q30: How do you migrate from server to serverless?**
- **Answer**:
  - Start with new features
  - Refactor stateless components first
  - Use strangler fig pattern
  - Implement comprehensive testing
  - Monitor performance and costs

## Best Practices for Interview Answers

### Structure Your Answer
```text
1. Definition (1-2 sentences)
2. How it works (2-3 sentences)
3. Use cases (when to use)
4. Trade-offs (benefits vs limitations)
5. Code example (if applicable)
```

### Key Concepts to Master

| Concept | Key Points |
|---------|------------|
| Cold Starts | What causes them, how to minimize |
| Concurrency | Limits, provisioned vs on-demand |
| State Management | External stores, Durable Objects |
| Error Handling | Retries, DLQ, circuit breakers |
| Cost Optimization | Right-sizing, provisioned concurrency |
| Security | IAM, secrets management, VPC |
| Monitoring | CloudWatch, X-Ray, custom metrics |

### Common Follow-up Questions
- "How would you implement this in production?"
- "What are the cost implications?"
- "How do you handle failures?"
- "What are the alternatives?"
- "How do you test this?"

## Summary

Serverless and edge computing are modern cloud paradigms that enable building scalable, cost-effective applications. Master the concepts, patterns, and trade-offs to excel in interviews.

## References & Learn More

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Serverless Framework](https://www.serverless.com/)
- [Cloudflare Workers](https://developers.cloudflare.com/workers/)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Serverless Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
