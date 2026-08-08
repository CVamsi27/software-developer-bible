---
section: Serverless & Edge
category: DevOps
tags: [interview-questions, practice]
---

# Serverless & Edge Interview Questions

> 30+ curated questions on serverless and edge computing, from fundamentals to FAANG-style system design.

## Definition

This guide covers the questions a senior full-stack engineer should be able to answer on serverless, FaaS, edge runtimes, cold starts, event-driven patterns, and production trade-offs. Grouped by difficulty.

## Why It Matters (TL;DR)

- **Technical interviews** — serverless and edge are core modern cloud paradigms
- **System design** — interviewers ask when to reach for Lambda vs containers
- **Cost optimization** — serverless economics drive real production decisions
- **Scalability** — auto-scaling is the most-tested benefit

## Answer Framework

```text
ANSWER STRUCTURE:
  1. Definition        (1-2 sentences — what it is)
  2. How it works      (2-3 sentences — mechanism, lifecycle)
  3. Use cases         (when to reach for it)
  4. Trade-offs        (cost, latency, lock-in, complexity)
  5. Real example      (production scenario you've shipped)
```

## Beginner

**Q1: What is serverless computing?**

A: A cloud model where the provider manages servers and dynamically allocates compute on demand. Developers deploy functions, scale is automatic (including to zero), and you pay per request plus GB-seconds of execution time.

**Q2: What are the benefits of serverless?**

A: No server management, automatic scaling to/from zero, pay-per-use pricing, faster time-to-market, built-in high availability, and reduced operational burden.

**Q3: What is AWS Lambda?**

A: AWS's FaaS compute service that runs your code in response to triggers (API Gateway, S3, SQS, EventBridge, DynamoDB Streams) without provisioning or managing servers. Supports Node.js, Python, Go, Java, .NET, Ruby, custom runtimes.

**Q4: What is a cold start?**

A: The latency incurred when Lambda initializes a new execution environment — downloads the code, starts the runtime, runs the `init` phase. First request after idle is the cold one; subsequent requests reuse the warm container. Varies by runtime: Node.js 100-300ms, Java 1-3s. Mitigations: hoisted clients, smaller packages, SnapStart, Provisioned Concurrency.

**Q5: What are edge functions?**

A: Serverless functions that run at CDN Points of Presence (Cloudflare Workers, Vercel Edge, Lambda@Edge), close to users. V8 isolate-based runtimes give sub-5ms cold starts but have limited CPU time (10ms-30s), memory (128-256MB), and no Node.js APIs.

**Q6: What is the difference between API Gateway HTTP API and REST API?**

A: HTTP API is simpler, ~70% cheaper, lower latency, with fewer features (JWT auth, OIDC, throttling, CORS only). REST API has more features (request/response transformations, request validation, API keys, usage plans, AWS WAF integration). Default to HTTP API for new projects unless you need REST-only features.

## Intermediate

**Q7: How do you reduce cold start latency?**

A: (1) Hoist AWS SDK / DB clients outside the handler — they're reused on warm starts. (2) Keep deployment packages small (esbuild / SAM `NodejsFunction`). (3) Use Provisioned Concurrency for predictable p99. (4) SnapStart (Java/Python) snapshots the initialized environment. (5) Avoid VPC unless required; use VPC endpoints / RDS Proxy when you must.

**Q8: How do you handle errors in serverless functions?**

A: (1) Try/catch + structured logs in the handler. (2) For async invocations (S3, SNS, EventBridge), configure a Dead Letter Queue (SQS or SNS). (3) Use Lambda Destinations for async failures (more powerful than DLQ — captures the event payload). (4) Idempotency: dedupe by event ID on retry. (5) Set CloudWatch alarms on Errors, Throttles, and DLQ age.

**Q9: What is the maximum execution time for Lambda?**

A: 15 minutes per invocation. For longer workflows, use Step Functions (up to 1 year) or break into smaller chained functions. Long polling on SQS can extend visibility; for genuinely long tasks use Fargate or EC2.

**Q10: What is a Lambda layer?**

A: A zip archive containing libraries, custom runtimes, or dependencies that can be shared across multiple functions. Layers are extracted to `/opt` in the execution environment. 5 layers max per function, 250MB unzipped total (with the function). Use layers to share common SDK versions or in-house libraries without bloating every function's deployment package.

**Q11: What is the difference between SQS and SNS?**

A: SQS is point-to-point (one consumer per message), buffered, polling-based, with at-least-once delivery. SNS is pub/sub (fan-out to N subscribers), push-based, near-real-time, with no message retention. They compose: SNS fan-outs to multiple SQS queues, each with its own consumer group.

**Q12: What is Lambda concurrency and how do you control it?**

A: Concurrency = number of execution environments running simultaneously. Default account limit: 1,000 per region (soft). Reserved concurrency caps a function (protects downstream from runaway invocations). Provisioned Concurrency pre-warms environments (eliminates cold starts at higher cost). Bursty traffic can request a quota increase.

## Senior

**Q13: How do you handle long-running processes in serverless?**

A: (1) Break into smaller chained functions via SQS / SNS / Step Functions. (2) Step Functions for orchestrated workflows (15min per state, 1 year total). (3) SQS long polling for up to 12 hours buffered processing. (4) Fargate or EC2 for genuinely long tasks. (5) Use S3 + Lambda for batch jobs.

**Q14: How do you implement connection pooling in Lambda?**

A: Don't manage connections in the handler — they'll leak on cold start and exhaust the DB. Instead: (1) Use RDS Proxy or Aurora Serverless v2 to multiplex connections. (2) Hoist a single client to module scope; the warm container reuses it. (3) Set the client's connection timeout to less than the function timeout. (4) For DynamoDB, the SDK manages connections internally.

**Q15: What is the impact of VPC on Lambda?**

A: ENI (Elastic Network Interface) attach adds 1-2 seconds to cold start. Reduces available memory by ~80MB. Avoid VPC unless you need to access VPC resources (RDS, ElastiCache, internal services). When you must: use VPC endpoints to avoid NAT, RDS Proxy for connection management, and keep the function warm with Provisioned Concurrency.

**Q16: How do you test serverless functions locally?**

A: AWS SAM CLI (`sam local invoke`, `sam local start-api`) — runs Lambda in a Docker container that emulates the AWS environment. Serverless Framework (`serverless offline`). LocalStack for full AWS emulation (S3, SQS, DynamoDB). For pure unit tests, just call the handler function directly — pass a mock `APIGatewayProxyEvent`.

**Q17: What is Lambda@Edge vs CloudFront Functions vs Cloudflare Workers?**

A: Lambda@Edge runs in CloudFront PoPs, supports Node.js/Python, up to 5s (viewer) / 30s (origin) execution. CloudFront Functions runs in CloudFront, uses V8 isolates, sub-ms cold start, 1MB memory, 128KB response. Cloudflare Workers run in Cloudflare's 300+ PoPs, V8 isolates, sub-5ms cold start, 128MB, 10ms-30s CPU. Pick: CloudFront Functions for header rewrites (cheapest, fastest), Workers for global auth / A/B, Lambda@Edge for compute-heavy edge logic.

**Q18: How do you handle authentication at the edge?**

A: Verify JWTs using Web Crypto API (Web Standard — works in V8 isolates). Sub-50ms latency. Use KV or Edge Config for token blacklists. For session-based: read the session cookie and call the auth service (or check a signed JWT cookie). Cloudflare Access and Vercel Authentication provide turnkey solutions. Always validate the JWT signature, expiration, audience, and issuer.

**Q19: How do you implement idempotency in Lambda?**

A: Use the event ID (SQS MessageId, Kinesis sequence number, EventBridge event ID) as the idempotency key. Persist it in DynamoDB with a TTL (e.g., 24h) and check before processing — if the key exists, skip. For writes, use `PutItem` with `ConditionExpression: 'attribute_not_exists(idempotencyKey)'`. AWS Lambda Powertools (`@aws-lambda-powertools/idempotency`) provides a drop-in implementation.

**Q20: How do you migrate from a monolith to serverless?**

A: Strangler Fig pattern. (1) Identify seams — read-only endpoints are safest to migrate first. (2) Put API Gateway / ALB in front, route specific paths to new Lambda. (3) For state: extract shared state to DynamoDB / Aurora. (4) Use EventBridge / SNS for cross-service events. (5) Migrate one bounded context at a time. (6) Keep the monolith as fallback until the new service is battle-tested. (7) Use feature flags to toggle traffic.

**Q21: What is Lambda SnapStart and when do you use it?**

A: SnapStart (GA for Java, Python) snapshots the initialized execution environment (after `init` phase) and uses the snapshot for new cold starts, eliminating most cold-start latency (up to 10x for Java). Trade-offs: no filesystem writes (use `/tmp` for read-only after init), no unique dynamic state per invocation. Use for: latency-sensitive APIs, AI inference cold paths. Skip for: workloads with stateful init, very large heaps.

**Q22: How do you debug serverless in production?**

A: (1) Structured JSON logs to CloudWatch; use CloudWatch Logs Insights to query. (2) Enable X-Ray Active Tracing for distributed traces across API Gateway → Lambda → DynamoDB. (3) Lambda Insights for runtime metrics. (4) Custom metrics via EMF (Embedded Metric Format). (5) Third-party: Datadog Lambda, Lumigo, Thundra for deeper observability. (6) Replay production events locally with `sam remote invoke` or by re-publishing to SQS.

## FAANG-style

**Q23: Design a serverless architecture for a real-time chat application.**

A:
- API Gateway (REST) for auth, user/profile CRUD → Lambda → DynamoDB
- API Gateway WebSocket API for real-time: $connect, $disconnect, $default routes
- Connection storage: DynamoDB table keyed by `connectionId` with TTL
- Message broadcast: SNS topic → fan-out to all connected Lambda consumers via $default route (or ElastiCache pub/sub)
- Persistence: messages → DynamoDB + S3 (larger payloads)
- Presence: DynamoDB with TTL on heartbeat records
- Edge layer: CloudFront for static assets, Lambda@Edge for auth
- Considerations: connection management at scale (10K+ per instance), message ordering (use sequence numbers per room), offline support (SQS for queued messages), cost (API Gateway WebSocket ~$1/M messages)

**Q24: How would you implement CI/CD for a serverless application?**

A:
- Source: GitHub / GitLab
- Build: SAM / Serverless Framework / CDK in CI
- Test: `sam local invoke` for unit tests, integration tests against a deploy-to-staging
- Stages: dev → staging → production, with manual approval gate
- Deployment strategies: SAM safe deployments (canary via CodeDeploy), Vercel preview deployments, CloudFormation changeset
- Drift detection: scheduled `sam drift detect`
- Secrets: SSM Parameter Store / Secrets Manager, never in code
- Rollback: keep last N versions in Lambda aliases; CodeDeploy auto-rollback on alarm

**Q25: Explain serverless at scale — what breaks first?**

A:
- Cold starts: first traffic spike after idle. Fix: Provisioned Concurrency, warmer pings (anti-pattern), or accept the cost.
- Concurrent execution limits: account-level 1,000 default. Fix: quota increase, reserved concurrency for critical paths.
- Throttling on downstream: Lambda invocations > DB connection pool. Fix: RDS Proxy, throttling, or circuit breaker.
- Cost: 100M invocations/month adds up. Fix: right-size memory, batch with SQS, cache at the edge.
- Observability: CloudWatch becomes expensive. Fix: structured logs, sampled X-Ray, third-party.
- Cold start on package size: 50MB zip = 1s cold start. Fix: tree-shake, split into focused functions, use layers for shared deps.

**Q26: How do you handle a 100x traffic spike in a serverless system?**

A: (1) Lambda auto-scales to concurrency limit; raise the limit preemptively. (2) Front the API with CloudFront / Cloudflare for caching and DDoS protection. (3) Move auth to the edge (Cloudflare Workers / Lambda@Edge) so unauthenticated traffic doesn't hit origin. (4) Use Provisioned Concurrency for the auth-and-routing tier. (5) SQS for backpressure on async workloads. (6) Cache hot reads in ElastiCache / DAX. (7) Multi-region failover if the spike is regional.

**Q27: Design a serverless data pipeline for analytics.**

A:
- Ingestion: API Gateway → Kinesis Data Streams (or Kinesis Data Firehose for direct-to-S3)
- Transformation: Lambda consumers normalize, enrich, partition
- Storage: S3 (Parquet, partitioned by date/event_type) for the data lake
- Cataloging: Glue Crawler populates Glue Data Catalog
- Querying: Athena (serverless SQL) for ad-hoc; Redshift Serverless for warehouse queries
- Orchestration: Step Functions for the multi-step ETL with retries
- Visualization: QuickSight or Apache Superset
- Cost optimization: S3 Intelligent-Tiering, Parquet + partition pruning, Athena per-query cost ($5/TB scanned)

## Follow-ups

**Q28: How do you handle secrets in serverless?**

A: AWS Secrets Manager or SSM Parameter Store with automatic rotation. Reference via environment variables (Secrets Manager supports this natively with the cached value) or fetch in init phase. Never hardcode. Use IAM execution role for least-privilege access. Consider Lambda extensions for shared secret caching.

**Q29: What is the impact of serverless on database design?**

A: (1) Connection pooling is critical (RDS Proxy). (2) Prefer connectionless databases (DynamoDB, DocumentDB) for FaaS. (3) Use single-digit-millisecond DBs (DynamoDB, ElastiCache) to keep function execution short. (4) Use read replicas for read-heavy APIs. (5) Consider Aurora Serverless v2 for variable workloads.

**Q30: How do you handle rate limiting in serverless?**

A: (1) API Gateway throttling (10K RPS default burst, 5K RPS sustained). (2) Usage plans with API keys for per-customer limits. (3) Token bucket in DynamoDB or ElastiCache (Redis) for custom logic. (4) Cloudflare / CloudFront rate limiting rules at the edge. (5) Lambda reserved concurrency as a coarse-grained rate limit.

**Q31: What are the cost considerations for serverless?**

A: (1) Per-request + per-GB-second — easy to underestimate GB-seconds when functions are slow. (2) Provisioned Concurrency is always-on cost. (3) Data transfer out to internet is the biggest surprise. (4) CloudWatch costs scale with log volume — log only what you need. (5) Step Functions state transitions are billed per transition. (6) Compare with container alternatives (Fargate) for high-RPS steady workloads.

**Q32: How do you secure serverless applications?**

A: (1) Least-privilege IAM execution role per function. (2) VPC for sensitive resources. (3) Encrypt environment variables with KMS. (4) Use Secrets Manager for credentials. (5) API Gateway authorization (Cognito, Lambda authorizer, IAM). (6) AWS WAF for SQL injection / XSS. (7) Scan packages for vulnerabilities (`npm audit`, Snyk). (8) Lambda code signing for supply-chain integrity.

## Key Concepts to Master

| Concept | Key Points |
|---------|------------|
| Cold Starts | What causes them, runtime cost, how to minimize (SnapStart, PC, hoisted clients) |
| Concurrency | Account limits, reserved, provisioned, burst behavior |
| State Management | External stores (DynamoDB, ElastiCache); never rely on in-memory |
| Error Handling | Retries with exponential backoff, DLQ, Lambda Destinations, idempotency |
| Cost Optimization | Right-sizing memory, batching, provisioned concurrency trade-off |
| Security | IAM execution role, secrets, VPC, KMS, WAF, code signing |
| Observability | Structured logs, X-Ray, CloudWatch metrics, EMF, third-party tools |
| Edge vs Serverless | When to use which — latency, CPU budget, API support |

## Common Follow-up Questions

- "How would you implement this in production?"
- "What are the cost implications at 1M / 100M / 1B requests/month?"
- "How do you handle failures?"
- "What are the alternatives — why not containers?"
- "How do you test this?"
- "How would you migrate an existing monolith to this?"

## Summary

- Serverless and edge computing are core modern paradigms for scalable, cost-effective applications
- Master cold start mechanics, concurrency limits, and event-driven patterns
- Know the trade-offs: per-request cost, vendor lock-in, observability challenges
- Be ready to design: real-time chat, data pipelines, CI/CD, cost-optimized APIs

---

## Cheat Sheet

```text
SERVERLESS & EDGE INTERVIEW CHEAT SHEET
═══════════════════════════════════════════════════════════════

ANSWER FRAMEWORK:
  1. Definition
  2. How it works (lifecycle, triggers)
  3. Use cases (when to reach for it)
  4. Trade-offs (cost, latency, lock-in)
  5. Real production example

KEY NUMBERS:
  • Lambda timeout:    15 min
  • Lambda memory:     128 MB – 10,240 MB
  • Lambda package:    50 MB (zipped) / 250 MB (unzipped)
  • Concurrency:       1,000 default per region
  • Cold start:        100ms-2s (Node.js ~200ms)
  • Edge CPU limit:    10ms-30s
  • Edge memory:       128-256 MB

INTERVIEW WINNERS:
  - Bring up SnapStart, Provisioned Concurrency, Lambda Destinations
  - Distinguish CloudFront Functions, Lambda@Edge, Cloudflare Workers
  - Mention idempotency for at-least-once event sources
  - Reference real production examples with concrete numbers
```

---

## See Also

- [AWS Lambda](05-AWS-Lambda.md)
- [Edge Functions](02-Edge-Functions.md)
- [Microservices](../12-Microservices/)
- [Observability](../22-Observability/)
- [Serverless Overview](01-Serverless-Overview.md)
- [Serverless Patterns](03-Serverless-Patterns.md)
- [Vercel Deployments](06-Vercel-Deployments.md)


## References & Learn More

- [Awesome Serverless](https://github.com/anaibol/awesome-serverless)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Cloudflare Workers](https://developers.cloudflare.com/workers/)
- [Lambda Powertools](https://docs.powertools.aws.dev/lambda/python/latest/)
- [Serverless Best Practices (AWS)](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Serverless Framework](https://www.serverless.com/)
- [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions)
