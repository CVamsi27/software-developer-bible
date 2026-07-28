---
section: Serverless & Edge
category: DevOps
tags: [concept]
---

# AWS Lambda

## Definition

**AWS Lambda** is Amazon's Function-as-a-Service (FaaS) platform that runs code in response to events without provisioning servers. It supports multiple runtimes (Node.js, Python, Java, Go) and integrates with 200+ AWS services as event sources.

## Why Do We Need It?

1. **Zero infrastructure**: No servers to manage — auto-scales from 0 to thousands
2. **Event-driven**: Respond to S3 uploads, DynamoDB streams, API Gateway requests, SQS messages
3. **Cost**: Pay only per request and compute duration (free tier: 1M requests/month)
4. **Ecosystem**: Deep AWS integration, layers (shared dependencies), Lambda@Edge for CDN

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Event Sources** | API Gateway, S3, SQS, DynamoDB Streams, SNS, CloudWatch |
| **Cold Start** | ~200ms-1s delay on first invocation after idle |
| **Timeout** | Max 15 minutes per invocation |
| **Memory** | 128MB - 10,240MB (CPU scales with memory) |
| **Concurrency** | 1000 (default) per region, can be increased |
| **Lambda@Edge** | Run at CloudFront edge locations for low latency |

---

### See Also

- [Edge Functions](02-Edge-Functions.md)
- [Interview Questions](04-Interview-Questions.md)
- [Next.js Deployment](../04-NextJS/)
- [Serverless Overview](01-Serverless-Overview.md)
- [Serverless Patterns](03-Serverless-Patterns.md)

### References

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda@Edge](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions.html)
