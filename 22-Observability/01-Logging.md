---
section: Observability
category: DevOps
tags: [concept]
---

# Logging

[![Section](https://img.shields.io/badge/section-Observability-ff7f00)](.)
[![Type](https://img.shields.io/badge/type-Concept-informational)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

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


## Summary

Logging is the most fundamental pillar of observability. Structured JSON logging with correlation IDs, appropriate log levels, and centralized aggregation gives teams the ability to debug production issues, audit compliance, and understand system behavior. Choose Pino for performance, Winston for features, and always redact sensitive data at the logger layer.

---

## See Also
- [Kubernetes](../14-Kubernetes/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Winston GitHub](https://github.com/winstonjs/winston)
- [Pino Documentation](https://getpino.io/)
- [OpenTelemetry Logging](https://opentelemetry.io/docs/specs/otel/logs/)
- [Structured Logging Best Practices](https://www.weave.works/blog/the-benefits-of-structured-logging/)
- [The Art of Logging](https://www.programminglogs.com/)
- [ELK Stack Documentation](https://www.elastic.co/guide/en/elastic-stack/current/index.html)
- [Grafana Loki Docs](https://grafana.com/docs/loki/)
