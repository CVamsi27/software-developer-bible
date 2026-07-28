# Distributed Tracing

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

est as it travels through multiple services in a distributed system. Each unit of work is recorded as a **span**, and all spans from a single request form a **trace**. Tracing answers the question: *"Where did time go for this request?"*

A **trace** is a directed acyclic graph (DAG) of spans representing the causal relationships between operations. A **span** is a named, timed operation with metadata (attributes), events, and a parent-child relationship to other spans.

## Why Do We Need It?

In a monolith, a stack trace tells you what happened. In microservices, a single user request may touch 5-20 services. Without tracing:

1. You can't see which service is slow

2. You can't correlate errors across service boundaries

3. Debugging requires grep across dozens of log streams

4. You don't know the full call graph for a request

Tracing provides:

- **End-to-end latency** breakdown per service
- **Dependency mapping** (which services call which)
- **Error attribution** (which service failed and why)
- **Performance optimization** (find the critical path)

## How It Works

```text
┌─────────────────────────────────────────────────────────────────┐
│                     TRACE STRUCTURE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Request: GET /api/orders/123                              │
│                                                                 │
│  Trace ID: abc-123-def-456                                      │
│                                                                 │
│  ┌─── api-gateway ──────────────────────────────────────────┐  │
│  │  Span ID: s1   Duration: 350ms                           │  │
│  │                                                           │  │
│  │  ┌─── auth-service ──────┐  ┌─── order-service ───────┐  │  │
│  │  │  Span ID: s2          │  │  Span ID: s3             │  │  │
│  │  │  Duration: 20ms       │  │  Duration: 300ms         │  │  │
│  │  │                       │  │                           │  │  │
│  │  │  ┌─── Redis ──────┐  │  │  ┌─── Postgres ──────┐  │  │  │
│  │  │  │  s4  5ms       │  │  │  │  s5  50ms          │  │  │  │
│  │  │  └────────────────┘  │  │  └────────────────────┘  │  │  │
│  │  └──────────────────────┘  │  ┌─── payment-svc ─────┐  │  │  │
│  │                             │  │  Span ID: s6         │  │  │  │
│  │                             │  │  Duration: 200ms     │  │  │  │
│  │                             │  │  ┌─── Stripe API ─┐  │  │  │  │
│  │                             │  │  │  s7  180ms     │  │  │  │  │
│  │                             │  │  └────────────────┘  │  │  │  │
│  │                             │  └──────────────────────┘  │  │  │
│  │                             └────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Critical path: api-gateway → order-service → payment → Stripe  │
│  Total trace duration: 350ms                                    │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  CONTEXT PROPAGATION                                         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                              │
  │  Service A ──HTTP Header──▶ Service B ──HTTP Header──▶ C    │
  │                                                              │
  │  Headers carry:                                              │
  │    traceparent: 00-abc123-span456-01                         │
  │    tracestate: vendor1=value1                                │
  │                                                              │
  │  Standard: W3C Trace Context (traceparent + tracestate)     │
  └─────────────────────────────────────────────────────────────┘

```

## Code Examples

### OpenTelemetry Setup (Node.js)

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-http";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";
import { Resource } from "@opentelemetry/resources";
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from "@opentelemetry/semantic-conventions";
import { diag, DiagConsoleLogger, DiagLogLevel } from "@opentelemetry/api";

// Enable OpenTelemetry diagnostics for debugging
diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);

const resource = new Resource({
  [ATTR_SERVICE_NAME]: process.env.SERVICE_NAME || "order-service",
  [ATTR_SERVICE_VERSION]: process.env.APP_VERSION || "1.0.0",
  "deployment.environment": process.env.NODE_ENV || "development",
});

const traceExporter = new OTLPTraceExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4318/v1/traces",
});

const metricExporter = new OTLPMetricExporter({
  url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://localhost:4318/v1/metrics",
});

const metricReader = new PeriodicExportingMetricReader({
  exporter: metricExporter,
  exportIntervalMillis: 15_000,
});

const sdk = new NodeSDK({
  resource,
  traceExporter,
  metricReader,
  instrumentations: [
    getNodeAutoInstrumentations({
      // Customize instrumentation
      "@opentelemetry/instrumentation-http": {
        enabled: true,
        requestHook: (span, request) => {
          span.setAttribute("http.request_id", (request as any).headers?.["x-request-id"] || "");
        },
      },
      "@opentelemetry/instrumentation-express": { enabled: true },
      "@opentelemetry/instrumentation-pg": { enabled: true },
      "@opentelemetry/instrumentation-redis": { enabled: true },
      "@opentelemetry/instrumentation-fetch": { enabled: true },
    }),
  ],
});

// Graceful shutdown
process.on("SIGTERM", () => {
  sdk.shutdown()
    .then(() => console.log("OpenTelemetry shut down"))
    .catch((err) => console.error("OpenTelemetry shutdown error", err));
});

sdk.start();
export default sdk;

```

### Custom Spans and Attributes

```typescript
import { trace, context, SpanKind, SpanStatusCode } from "@opentelemetry/api";

const tracer = trace.getTracer("order-service", "1.0.0");

// Automatic span creation with nested operations
async function processOrder(orderId: string, userId: string) {
  return tracer.startActiveSpan(
    "processOrder",
    {
      kind: SpanKind.INTERNAL,
      attributes: {
        "order.id": orderId,
        "user.id": userId,
      },
    },
    async (span) => {
      try {
        // Step 1: Validate order
        span.addEvent("validating_order");
        const order = await validateOrder(orderId);
        span.setAttribute("order.itemCount", order.items.length);
        span.setAttribute("order.total", order.total);

        // Step 2: Check inventory (creates child span automatically via instrumentation)
        span.addEvent("checking_inventory");
        const inventoryAvailable = await checkInventory(order.items);
        span.setAttribute("inventory.available", inventoryAvailable);

        if (!inventoryAvailable) {
          span.setStatus({ code: SpanStatusCode.ERROR, message: "Inventory unavailable" });
          throw new Error("Items out of stock");
        }

        // Step 3: Process payment
        span.addEvent("processing_payment");
        const paymentResult = await processPayment(userId, order.total);
        span.setAttribute("payment.id", paymentResult.id);
        span.setAttribute("payment.method", paymentResult.method);

        // Step 4: Create shipment
        span.addEvent("creating_shipment");
        const shipment = await createShipment(order);

        span.setStatus({ code: SpanStatusCode.OK });
        return { orderId, shipment: shipment.trackingNumber };
      } catch (err) {
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: err instanceof Error ? err.message : "Unknown error",
        });
        span.recordException(err as Error);
        throw err;
      } finally {
        span.end();
      }
    }
  );
}

// Manual span for specific operation
async function callExternalAPI(url: string) {
  return tracer.startActiveSpan(
    "external-api-call",
    {
      kind: SpanKind.CLIENT,
      attributes: { "http.url": url, "http.method": "GET" },
    },
    async (span) => {
      const startTime = Date.now();
      try {
        const response = await fetch(url);
        const duration = Date.now() - startTime;

        span.setAttribute("http.status_code", response.status);
        span.setAttribute("http.response_time_ms", duration);

        if (!response.ok) {
          span.setStatus({ code: SpanStatusCode.ERROR, message: `HTTP ${response.status}` });
        }

        return await response.json();
      } catch (err) {
        span.setStatus({ code: SpanStatusCode.ERROR, message: (err as Error).message });
        span.recordException(err as Error);
        throw err;
      } finally {
        span.end();
      }
    }
  );
}

```

### Context Propagation Across Services

```typescript
import { context, propagation, trace } from "@opentelemetry/api";
import express from "express";

// Service A: Propagate context via HTTP headers
async function callServiceB(orderId: string) {
  const currentSpan = trace.getActiveSpan();
  const headers: Record<string, string> = {};

  // Inject current context into headers
  propagation.inject(context.active(), headers);

  const response = await fetch(`http://service-b/api/orders/${orderId}`, {
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  });

  return response.json();
}

// Service B: Extract context from incoming headers
const app = express();

app.use((req, res, next) => {
  // Extract context from incoming request headers
  const parentContext = propagation.extract(context.active(), req.headers);

  // All operations within this context will be linked to the parent trace
  context.with(parentContext, () => {
    next();
  });
});

app.get("/api/orders/:id", async (req, res) => {
  // This handler runs within the extracted parent context
  const span = trace.getActiveSpan(); // Already linked to parent trace
  span?.setAttribute("order.id", req.params.id);

  const order = await getOrder(req.params.id);
  res.json(order);
});

```

### Baggage (Cross-Service Context)

```typescript
import { context, propagation, baggage } from "@opentelemetry/api";

// Service A: Set baggage
const entry = baggage.createEntry("user.tier", "premium");
const currentBaggage = propagation.getBaggage(context.active()) || baggage.createBaggage();
const newBaggage = currentBaggage.setEntry("user.tier", entry);

const ctxWithBaggage = propagation.setBaggage(context.active(), newBaggage);

context.with(ctxWithBaggage, () => {
  // Service B can read this baggage
  callServiceB();
});

// Service B: Read baggage
function handleRequest(req: express.Request) {
  const incomingBaggage = propagation.getBaggage(context.active());
  const userTier = incomingBaggage?.getEntry("user.tier")?.value;

  if (userTier === "premium") {
    // Apply premium routing/logic
  }
}

```

### Trace-to-Log Correlation

```typescript
import { trace, context } from "@opentelemetry/api";
import pino from "pino";

const logger = pino({
  formatters: {
    log(object) {
      const span = trace.getActiveSpan();
      if (span) {
        const spanContext = span.spanContext();
        return {
          ...object,
          traceId: spanContext.traceId,
          spanId: spanContext.spanId,
          traceFlags: spanContext.traceFlags,
        };
      }
      return object;
    },
  },
});

// Now every log includes trace context automatically
async function processItem(itemId: string) {
  logger.info({ itemId }, "Processing item");

  try {
    const result = await transformItem(itemId);
    logger.info({ itemId, result }, "Item processed");
    return result;
  } catch (err) {
    logger.error({ itemId, err }, "Failed to process item");
    throw err;
  }
}

```

### Sampling Strategies

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { ParentBasedSampler, TraceIdRatioBasedSampler } from "@opentelemetry/sdk-trace-base";

// Strategy 1: Sample 10% of all traces
const ratioSampler = new TraceIdRatioBasedSampler(0.1);

// Strategy 2: Always sample errors, 10% of success (ParentBased)
const parentBasedSampler = new ParentBasedSampler({
  root: new TraceIdRatioBasedSampler(0.1),
  // Always sample if parent is sampled (distributed trace consistency)
  remoteParentSampled: () => true,
  remoteParentNotSampled: () => false,
  localParentSampled: () => true,
  localParentNotSampled: () => false,
});

// Strategy 3: Tail-based sampling (at collector level, not SDK)
// Keep 100% of errors, 1% of success, 100% of slow requests
// Configured in OpenTelemetry Collector:
/*
  processors:
    tail_sampling:
      decision_wait: 10s
      policies:

        - name: errors
          type: status_code
          status_code: { status_codes: [ERROR] }

        - name: slow
          type: latency
          latency: { threshold_ms: 1000 }

        - name: normal
          type: probabilistic
          probabilistic: { sampling_percentage: 1 }
*/

```

## Real-World Use Cases

1. **Latency debugging**: Find which microservice in a 10-service chain is adding 2 seconds of latency

2. **Dependency mapping**: Automatically discover service call graphs from production traffic

3. **Error root cause**: Trace an error from the user-facing API down to the failing database query

4. **Performance optimization**: Identify the critical path and optimize the slowest span

5. **SLA monitoring**: Measure end-to-end latency percentiles for user-facing endpoints

6. **Capacity planning**: Understand which services are most called and need scaling

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Not propagating context | Traces break at service boundaries | Use W3C Trace Context headers automatically via OTel SDK |
| Creating too many spans | Trace becomes noisy, storage grows | Instrument at service boundaries and key operations only |
| No error recording | Errors invisible in traces | Use `span.recordException()` and `span.setStatus(ERROR)` |
| Ignoring sampling | 100% sampling overwhelms storage | Use head-based or tail-based sampling |
| Span attributes with PII | Privacy/compliance violations | Redact PII from span attributes |
| Not ending spans | Memory leaks, incomplete traces | Always use `startActiveSpan` with callback or try/finally |

## Best Practices

1. **Use OpenTelemetry** — vendor-neutral standard, avoid lock-in

2. **Instrument at boundaries** — service entry/exit, DB calls, external APIs

3. **Use semantic conventions** — `http.method`, `db.system`, `rpc.service` for consistency

4. **Propagate W3C Trace Context** — the standard for context propagation

5. **Tail-based sampling at the collector** — not at the SDK, for better decisions

6. **Correlate traces with logs** — inject `traceId` and `spanId` into log entries

7. **Name spans by operation** — `GET /api/orders`, `postgres.query`, not vague names

8. **Set span kind correctly** — `CLIENT`, `SERVER`, `PRODUCER`, `CONSUMER`, `INTERNAL`

9. **Keep span attributes flat** — avoid nested objects, use dot notation (`order.id`)

## Performance Considerations

- **OTel SDK overhead** — typically <1ms per span; negligible for most applications
- **Sampling reduces cost** — 100% sampling of a high-QPS service can cost thousands in storage
- **Span count per trace** — aim for <50 spans per trace for readability and storage
- **Attribute cardinality** — high-cardinality attributes (userId, requestId) increase storage; use them sparingly
- **Exporter batching** — OTel SDK batches spans before export to reduce network overhead
- **Collector as sidecar** — deploy the OTel Collector as a sidecar in Kubernetes to avoid network hops

## Summary

Distributed tracing is essential for understanding request flow in microservices. OpenTelemetry provides the vendor-neutral standard for instrumentation. Focus on propagating context at every service boundary, sampling intelligently, and correlating traces with logs for complete observability.

---

## See Also
- [Kubernetes](../14-Kubernetes/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Zipkin Documentation](https://zipkin.io/pages/references.html)
- [Grafana Tempo](https://grafana.com/docs/tempo/)
- [Distributed Tracing in Practice](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)
- [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/otel/)
