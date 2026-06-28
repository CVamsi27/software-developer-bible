# Logging

## Definition

Logging is the practice of recording discrete events that occur during software execution. Logs provide a chronological record of what happened in a system, serving as the foundation of observability. They capture context about requests, errors, state changes, and business events in a format that humans and machines can parse.

A **log entry** is a timestamped, immutable record of a single event. When collected, aggregated, and indexed, logs become a powerful tool for debugging, auditing, security analysis, and understanding system behavior over time.

## Why Do We Need It?

Without logging, diagnosing production issues is like driving blindfolded. Logging provides:

1. **Debugging**: Trace execution flow to find root causes of bugs

2. **Audit trail**: Record who did what and when for compliance (GDPR, SOC2, HIPAA)

3. **Business intelligence**: Track user actions, conversions, and feature usage

4. **Security**: Detect anomalies, unauthorized access, and attack patterns

5. **Performance analysis**: Identify slow operations and bottlenecks

6. **Post-mortems**: Reconstruct events after incidents

## How It Works

Logs flow from application code through a pipeline of collection, transport, aggregation, storage, and analysis.

```text
┌─────────────────────────────────────────────────────────────────┐
│                     LOGGING PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ App Code │───▶│  Logger  │───▶│Transport │───▶│ Collector│ │
│  │ (emit)   │    │ (format) │    │ (ship)   │    │ (aggreg.)│ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                            │    │
│                                                            ▼    │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────┐  │
│  │ Analysis │◀───│  Search  │◀───│     Storage / Index      │  │
│  │Dashboard │    │ (query)  │    │  (Elasticsearch/ Loki)   │  │
│  └──────────┘    └──────────┘    └──────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  LOG LEVEL SEVERITY (least → most severe)                   │
  ├─────────────────────────────────────────────────────────────┤
  │  DEBUG  ▓░░░░░░░░░  Verbose, dev-time diagnostics          │
  │  INFO   ▓▓░░░░░░░░  Normal operations, milestones          │
  │  WARN   ▓▓▓▓░░░░░░  Potential issues, degraded but working │
  │  ERROR  ▓▓▓▓▓▓░░░░  Failures requiring attention           │
  │  FATAL  ▓▓▓▓▓▓▓▓▓▓  System cannot recover, process dies   │
  └─────────────────────────────────────────────────────────────┘

```

## Structured vs Unstructured Logging

```text
┌─────────────────────────────────────────────────────────────┐
│  UNSTRUCTURED (hard to query)                               │
├─────────────────────────────────────────────────────────────┤
│  2024-01-15 10:30:45 INFO User 12345 logged in from IP     │
│  2024-01-15 10:30:46 ERROR Failed to connect to DB          │
│  Problem: Parsing regex is fragile, field order matters     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  STRUCTURED / JSON (easy to query)                          │
├─────────────────────────────────────────────────────────────┤
│  {                                                          │
│    "timestamp": "2024-01-15T10:30:45.123Z",                │
│    "level": "info",                                         │
│    "message": "User logged in",                             │
│    "userId": "12345",                                       │
│    "ip": "192.168.1.100",                                   │
│    "service": "auth-service",                               │
│    "requestId": "req-abc-123"                               │
│  }                                                          │
│  Benefit: Queryable by any field, machine-parseable         │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Logger Setup with Winston

```typescript
import winston from "winston";

// Custom log format with structured JSON
const jsonFormat = winston.format.combine(
  winston.format.timestamp({ format: "YYYY-MM-DDTHH:mm:ss.SSSZ" }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// Pretty-print for development
const prettyFormat = winston.format.combine(
  winston.format.timestamp({ format: "HH:mm:ss.SSS" }),
  winston.format.colorize(),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : "";
    return `${timestamp} ${level}: ${message} ${metaStr}`;
  })
);

const isProduction = process.env.NODE_ENV === "production";

const logger = winston.createLogger({
  level: isProduction ? "info" : "debug",
  format: isProduction ? jsonFormat : prettyFormat,
  defaultMeta: {
    service: process.env.SERVICE_NAME || "api-gateway",
    environment: process.env.NODE_ENV || "development",
    version: process.env.APP_VERSION || "unknown",
  },
  transports: [
    new winston.transports.Console(),
    ...(isProduction
      ? [
          new winston.transports.File({
            filename: "logs/error.log",
            level: "error",
            maxsize: 10 * 1024 * 1024, // 10MB
            maxFiles: 5,
          }),
          new winston.transports.File({
            filename: "logs/combined.log",
            maxsize: 50 * 1024 * 1024, // 50MB
            maxFiles: 10,
          }),
        ]
      : []),
  ],
  exceptionHandlers: [
    new winston.transports.File({ filename: "logs/exceptions.log" }),
  ],
  rejectionHandlers: [
    new winston.transports.File({ filename: "logs/rejections.log" }),
  ],
});

export default logger;

```

### Fast Structured Logger with Pino

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  serializers: {
    err: pino.stdSerializers.err,
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
  },
  // Redact sensitive fields
  redact: {
    paths: ["req.headers.authorization", "password", "token", "ssn", "creditCard"],
    censor: "[REDACTED]",
  },
});

// Child loggers inherit parent context
const requestLogger = logger.child({ requestId: "req-123" });
const userLogger = requestLogger.child({ userId: "user-456" });

export { logger, requestLogger, userLogger };

```

### Request Context Logging Middleware

```typescript
import { Request, Response, NextFunction } from "express";
import { v4 as uuidv4 } from "uuid";
import { requestLogger } from "./logger";

// Augment Express Request type
declare global {
  namespace Express {
    interface Request {
      requestId: string;
      startTime: number;
    }
  }
}

export function requestLoggingMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const requestId = (req.headers["x-request-id"] as string) || uuidv4();
  req.requestId = requestId;
  req.startTime = Date.now();

  // Log incoming request
  requestLogger.info(
    {
      requestId,
      method: req.method,
      url: req.originalUrl,
      query: req.query,
      ip: req.ip,
      userAgent: req.get("user-agent"),
      contentLength: req.get("content-length"),
    },
    "Request received"
  );

  // Capture original json method to log response
  const originalJson = res.json.bind(res);
  res.json = function (body: any) {
    const duration = Date.now() - req.startTime;

    const logLevel = res.statusCode >= 500 ? "error" : res.statusCode >= 400 ? "warn" : "info";

    requestLogger[logLevel](
      {
        requestId,
        method: req.method,
        url: req.originalUrl,
        statusCode: res.statusCode,
        duration,
        contentLength: res.get("content-length"),
      },
      "Request completed"
    );

    return originalJson(body);
  };

  // Log unhandled errors
  res.on("error", (err) => {
    requestLogger.error(
      { requestId, err },
      "Response error"
    );
  });

  next();
}

```

### Contextual Logging Patterns

```typescript
import logger from "./logger";

// Pattern: Enrich logs with business context at each step
async function processOrder(orderId: string, userId: string) {
  const log = logger.child({ orderId, userId, operation: "processOrder" });

  log.info("Order processing started");

  try {
    // Step 1: Validate
    log.info("Validating order");
    const order = await validateOrder(orderId);
    log.debug({ order }, "Order validated");

    // Step 2: Check inventory
    log.info("Checking inventory");
    const available = await checkInventory(order.items);
    if (!available) {
      log.warn({ items: order.items }, "Insufficient inventory");
      throw new InventoryError("Items out of stock");
    }
    log.debug("Inventory confirmed");

    // Step 3: Process payment
    log.info("Processing payment");
    const payment = await chargePayment(userId, order.total);
    log.info({ paymentId: payment.id, amount: order.total }, "Payment successful");

    // Step 4: Ship
    log.info("Creating shipment");
    const shipment = await createShipment(order);
    log.info({ trackingNumber: shipment.tracking }, "Shipment created");

    log.info("Order processing completed");
    return { orderId, shipment: shipment.tracking };
  } catch (err) {
    log.error({ err, orderId }, "Order processing failed");
    throw err;
  }
}

```

### Log Sampling and Rate Limiting

```typescript
import pino from "pino";

// Prevent log flooding from high-traffic endpoints
const rateLimitedLogger = (function () {
  const counts = new Map<string, number>();
  const windowMs = 60_000;

  setInterval(() => counts.clear(), windowMs);

  return {
    log: (key: string, level: string, msg: string, meta?: object) => {
      const count = (counts.get(key) || 0) + 1;
      counts.set(key, count);

      // Only log first occurrence and then every 100th
      if (count === 1 || count % 100 === 0) {
        logger[level as keyof typeof logger](
          { ...meta, suppressedCount: count - 1 },
          `${msg} (${count} total in ${windowMs / 1000}s)`
        );
      }
    },
  };
})();

// Usage in high-traffic handler
app.get("/api/products", (req, res) => {
  rateLimitedLogger.log("listProducts", "info", "Products listed", {
    query: req.query,
  });
  // ... handler logic
});

```

### Log Rotation and Lifecycle

```typescript
import winston from "winston";
import "winston-daily-rotate-file";

const dailyRotateTransport = new winston.transports.DailyRotateFile({
  filename: "logs/application-%DATE%.log",
  datePattern: "YYYY-MM-DD",
  zippedArchive: true,
  maxSize: "20m",
  maxFiles: "30d", // Keep 30 days
  frequency: "24h",
});

dailyRotateTransport.on("rotate", (oldFilename, newFilename) => {
  logger.info("Log file rotated", { oldFilename, newFilename });
});

const rotatedLogger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [dailyRotateTransport],
});

export default rotatedLogger;

```

## Real-World Use Cases

1. **Request tracing**: Every API call gets a `requestId` logged at entry/exit with duration

2. **Security auditing**: Login attempts, permission changes, data access logged for compliance

3. **Business events**: User signups, purchases, feature activations tracked for analytics

4. **Error forensics**: Full stack traces and request context captured for debugging

5. **Performance monitoring**: Slow queries logged when execution time exceeds threshold

6. **Feature flags**: Log which variant a user sees for A/B test analysis

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Logging PII/passwords | Compliance violations (GDPR, CCPA) | Redact sensitive fields |
| Console.log in production | No structure, no levels, no rotation | Use structured logger (Pino/Winston) |
| Logging inside loops | Log floods, performance degradation | Batch logs or log at summary level |
| No request context | Can't correlate logs to requests | Add requestId to all logs |
| Inconsistent field names | Hard to query across services | Define a shared log schema |
| Ignoring log level | Debug logs pollute production | Set level per environment |
| Blocking I/O for logs | Logger blocks request thread | Use async transports |

## Best Practices

1. **Use structured JSON logs** — machine-parseable, queryable by field

2. **Include correlation IDs** — propagate `requestId`/`traceId` across all services

3. **Log at boundaries** — entry/exit of service, DB call, external API call

4. **Use appropriate levels** — `debug` for dev, `info` for operations, `error` for failures

5. **Redact sensitive data** — mask PII, tokens, passwords before writing

6. **Set log levels per environment** — `debug` in dev, `info` in prod

7. **Monitor log volume** — alert on sudden spikes that could indicate issues or abuse

8. **Use child loggers** — inherit context (`userId`, `requestId`) without repeating it

9. **Include actionable context** — what happened, what was being attempted, what should happen next
10. **Centralize aggregation** — ship logs to ELK, Loki, or Datadog for searching

## Performance Considerations

- **Pino is 5-10x faster than Winston** for high-throughput services — use Pino for latency-sensitive paths
- **Avoid synchronous logging** in request handlers — use async transports or fire-and-forget
- **Batch log shipping** rather than writing per-log over network (use a local agent like Fluentd/Filebeat)
- **Log sampling** in high-QPS services — log 100% of errors, 1-10% of success traffic
- **Set max log size** and rotation to prevent disk exhaustion
- **Lazy serialization** — only serialize objects when log level is enabled (`logger.debug({ expensive: computeExpensive() })` won't serialize if debug is disabled)

## Interview Questions

### Beginner

1. **What is the difference between `console.log` and a structured logger?**

   - `console.log` has no levels, no structure, no rotation, no redaction. A structured logger (Pino/Winston) supports JSON output, log levels, transports, and metadata enrichment.

2. **What are the standard log levels and when should you use each?**

   - `debug`: verbose dev diagnostics; `info`: normal operations; `warn`: degraded but working; `error`: failure needing attention; `fatal`: unrecoverable system failure.

3. **Why is JSON logging preferred over plain text?**

   - JSON logs are machine-parseable and queryable. You can filter by any field (userId, requestId) without fragile regex parsing.

4. **What is log aggregation and why does it matter?**

   - Aggregation collects logs from all services into a central store (Elasticsearch, Loki). It enables cross-service searching and correlation.

5. **How do you handle sensitive data in logs?**

   - Use log redaction/masking to replace PII, tokens, and passwords with `[REDACTED]` before writing. Configure this in the logger serializer.

### Intermediate

6. **Explain the concept of correlation IDs in distributed systems.**

   - A unique ID (UUID) assigned at the API gateway, propagated via headers (`X-Request-ID`) to all downstream services. Every log entry includes this ID, allowing you to reconstruct the full request flow across services.

7. **What is the difference between structured and unstructured logging? Give examples.**

   - Unstructured: `"User 123 logged in from 192.168.1.1"` — free text. Structured: `{"level":"info","userId":"123","ip":"192.168.1.1","event":"login"}` — key-value pairs queryable by field.

8. **How would you implement log rotation in a production Node.js application?**

   - Use `winston-daily-rotate-file` or Pino's `pino-roll` transport. Configure `maxSize`, `maxFiles`, and `zippedArchive` to prevent disk exhaustion while retaining sufficient history.

9. **What problems does log sampling solve?**

   - In high-QPS services, logging every request creates storage costs and performance overhead. Sampling logs 1-10% of successful traffic (while logging 100% of errors) reduces volume while maintaining visibility.

10. **Explain the logger.child() pattern and why it's useful.**

    - `child()` creates a new logger that inherits parent context (service, requestId, environment) without repeating it in every log call. Each log entry automatically includes the inherited fields.

### Senior

11. **Design a logging architecture for a microservices system with 20 services.**

    - Use structured JSON logs with correlation IDs. Deploy a log collector (Fluentd/Filebeat) on each node. Ship to a central store (Elasticsearch + Kibana or Loki + Grafana). Define a shared log schema. Implement sampling per service criticality. Set up alerts on error rate anomalies.

12. **How do you handle log ordering across multiple services?**

    - Use wall-clock timestamps with millisecond precision. Include a monotonically increasing sequence number per service. Use distributed tracing (OpenTelemetry) to correlate events. Accept that perfect ordering is impossible — focus on causal ordering via trace spans.

13. **Your logging system is creating 50GB/day. How do you reduce costs without losing visibility?**

    - Implement sampling (10% of success traffic). Reduce log verbosity (remove debug in prod). Filter low-value logs (health checks). Compress archived logs. Use tiered storage (hot/warm/cold). Shorten retention for verbose logs (7 days), keep errors longer (90 days).

14. **How do you ensure logs don't contain PII across a large codebase?**

    - Centralized redaction in the logger layer using serializers. Automated scanning of log output in CI (PII detection tools). Code review checklist for logging. Contract testing that logs match approved schema. Regular audits of log content.

15. **Explain the trade-off between synchronous and asynchronous logging.**

    - Synchronous: logs are written before returning — simple but blocks the event loop. Asynchronous: logs buffered and shipped asynchronously — higher throughput but risk of data loss on crash. Production best practice: async transports with a crash-safe buffer (Pino default).

### FAANG-style

16. **If you could only keep ONE log field for debugging, what would it be and why?**

    - `requestId` (correlation ID). It lets you trace the full lifecycle of a single request across all services. Everything else (userId, duration, error) can be added, but without correlation, debugging distributed systems is nearly impossible.

17. **How would you detect a logging regression in CI/CD?**

    - Snapshot testing: capture expected log output for key flows. CI step that runs integration tests and compares log schema against baseline. Contract tests that verify log fields match the shared schema. Monitor log volume as a metric — alert on unexpected drops (indicates broken logging) or spikes.

18. **Design a log-based alerting system. What are the pitfalls?**

    - Alert on error rate (errors/total), not raw error count. Use moving averages to avoid flapping. Implement suppression windows. Common pitfalls: alert fatigue from noisy alerts, circular alerts (alerting system logs trigger more alerts), stale queries, not accounting for deploy-induced spikes.

19. **Your logs show errors but no stack traces. How do you debug?**

    - Check if stack traces are being truncated by log transport max message size. Verify the error object is being serialized properly (`JSON.stringify(err)` returns `{}` — use `err.stack`). Add request context to narrow scope. Reproduce locally with same input. Check if the error is from a dependency that swallows stacks.

20. **Explain the "three pillars of observability" and how logging relates.**

    - Logs, metrics, and traces are the three pillars. Logs answer "what happened", metrics answer "how much/how fast", traces answer "where did time go". They complement each other: metrics detect anomalies, logs explain them, traces map the request path. A complete observability stack uses all three.

### Follow-ups

21. **When would you choose Pino over Winston?**

    - Pino for high-throughput, latency-sensitive services (10k+ req/s). Winston for feature richness (multiple transports, formats) and simpler setup. Pino's structured JSON is faster because it avoids object traversal until serialization.

22. **How do you handle logging in serverless (Lambda) environments?**

    - Use `console.log` (CloudWatch captures stdout). Structure JSON manually or use a lightweight logger. Set log level via environment variables. Consider Powertools for AWS Lambda for built-in tracing and logging.

23. **What's the relationship between logging and distributed tracing?**

    - Traces provide the request path; logs provide the events within each span. Correlate them by including `traceId` and `spanId` in log entries. OpenTelemetry's `context` can inject these automatically into your logger.

24. **How do you test logging behavior in unit tests?**

    - Use an in-memory transport or mock the logger. Assert that specific log calls were made with expected fields. Example: `expect(logger.info).toHaveBeenCalledWith(expect.objectContaining({ userId: '123' }))`.

25. **What is "log fatigue" and how do you prevent it?**

    - When teams see too many alerts/logs, they stop paying attention. Prevent by: enforcing log levels, sampling success traffic, alerting only on actionable conditions, and regularly pruning low-value logs and alerts.

## Summary

Logging is the most fundamental pillar of observability. Structured JSON logging with correlation IDs, appropriate log levels, and centralized aggregation gives teams the ability to debug production issues, audit compliance, and understand system behavior. Choose Pino for performance, Winston for features, and always redact sensitive data at the logger layer.

## References & Learn More

- [Winston GitHub](https://github.com/winstonjs/winston)
- [Pino Documentation](https://getpino.io/)
- [OpenTelemetry Logging](https://opentelemetry.io/docs/specs/otel/logs/)
- [Structured Logging Best Practices](https://www.weave.works/blog/the-benefits-of-structured-logging/)
- [The Art of Logging](https://www.programminglogs.com/)
- [ELK Stack Documentation](https://www.elastic.co/guide/en/elastic-stack/current/index.html)
- [Grafana Loki Docs](https://grafana.com/docs/loki/)
