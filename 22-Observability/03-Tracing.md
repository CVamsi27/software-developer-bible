# Distributed Tracing

## Definition

Distributed tracing is a method of tracking the flow of a request as it travels through multiple services in a distributed system. Each unit of work is recorded as a **span**, and all spans from a single request form a **trace**. Tracing answers the question: *"Where did time go for this request?"*

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

## Interview Questions

### Beginner

1. **What is the difference between a trace and a span?**
   - A trace is the full request lifecycle across services. A span is a single unit of work within that trace. Spans are nested and form a tree.

2. **Why is distributed tracing important in microservices?**
   - A single request may touch 10+ services. Without tracing, you can't see which service is slow, which failed, or how they're connected.

3. **What is context propagation?**
   - Passing trace context (traceId, spanId) between services via HTTP headers so spans from the same request are linked into one trace.

4. **What is OpenTelemetry?**
   - A vendor-neutral open standard for collecting traces, metrics, and logs. It provides SDKs, APIs, and a collector for instrumentation.

5. **What is span sampling?**
   - Deciding which traces to record vs discard. Without sampling, high-traffic systems would generate unmanageable amounts of trace data.

### Intermediate

6. **Explain the difference between head-based and tail-based sampling.**
   - Head-based: decision made at trace start (SDK decides to sample or not). Tail-based: decision made after trace completes (collector evaluates full trace). Tail-based is better for keeping error/slow traces.

7. **How do you correlate traces with logs?**
   - Inject `traceId` and `spanId` into every log entry using a logger formatter that reads the active span context. Link traces to logs in your observability platform.

8. **What are semantic conventions in OpenTelemetry?**
   - Standardized attribute names for common operations (`http.method`, `db.system`, `rpc.service`) ensuring consistent, queryable traces across services.

9. **How does W3C Trace Context work?**
   - Two headers: `traceparent` (version-traceId-spanId-traceFlags) and `tracestate` (vendor-specific data). Every service in the chain reads/writes these headers.

10. **What is a span event?**
    - A timestamped annotation within a span (e.g., "retry attempt", "cache miss"). Less structured than child spans, useful for point-in-time observations.

### Senior

11. **Design a tracing architecture for 50 microservices.**
    - Deploy OTel SDK in each service (auto-instrumentation + custom spans). Deploy OTel Collector as DaemonSet per node. Use tail-based sampling in collector (keep errors, slow, 1% success). Export to Jaeger/Tempo. Build service dependency graph from trace data.

12. **Your traces show correct latency but users complain about slowness. What's missing?**
    - Client-side tracing (Real User Monitoring / RUM). The trace only covers server-side. Network latency, client rendering, and DNS are invisible. Add frontend performance monitoring.

13. **How do you handle tracing across async boundaries (queues, events)?**
    - Use messaging semantic conventions (`messaging.system`, `messaging.destination`). Propagate trace context in message attributes. On consumer side, extract context from message to link producer and consumer spans.

14. **Explain the critical path in a trace and how to find it.**
    - The critical path is the sequence of spans that determines total trace duration. It's the longest chain of dependent spans. Find it by walking from root span, always choosing the child with the latest end time.

15. **How would you implement trace-based alerting?**
    - Alert on P99 end-to-end latency (histogram from traces). Alert on error rate per service from span status codes. Alert on dependency failures (external API latency). Use trace data to enrich metric alerts with context.

### FAANG-style

16. **If you could add one instrumentation to your system, what would it be?**
    - HTTP server middleware that creates a span for every incoming request, propagates context, and records status code and duration. This gives you end-to-end latency, error rates, and dependency mapping for free.

17. **How do you prevent trace context from being lost in your system?**
    - Ensure all HTTP libraries use OTel instrumentation (auto-instrumentation covers most). Use context propagation middleware for message queues. Audit service mesh (Istio/Linkerd) for context passing. Add integration tests that verify trace continuity.

18. **Your trace shows a 5-second gap with no child spans. What happened?**
    - The service is doing synchronous blocking work not instrumented (file I/O, CPU computation, external API without instrumentation). Check for uninstrumented libraries, blocking event loop operations, or manual span creation missing.

19. **How would you trace serverless functions?**
    - Use OTel SDK with Lambda layer. Propagate context via SQS/SNS message attributes. Use X-Ray daemon or OTel Collector as Lambda extension. Instrument handler entry/exit.

20. **Explain trace merging in a service mesh.**
    - Service mesh (Istio, Linkerd) adds its own spans to traces. This can create duplicate spans or break context if not configured correctly. Ensure mesh uses W3C Trace Context and doesn't override application-level trace context.

### Follow-ups

21. **How do you handle tracing in batch processing?**
    - Create one trace per batch job, with spans per item processed. Use `BATCH` span kind. Propagate context within the batch but not across batches.

22. **What's the storage cost of tracing vs logging?**
    - Tracing generates less data than logging per request but requires structured storage. A typical trace with 10 spans is ~2KB. At 1000 req/s with 10% sampling = ~200MB/day.

23. **How do you trace GraphQL queries?**
    - Instrument the GraphQL resolver layer. Create spans per resolver. Use query name as span attribute. Track field-level latency to find slow resolvers.

24. **When would you NOT use OpenTelemetry?**
    - When you're already deeply invested in a vendor-specific solution (Datadog APM, AWS X-Ray) and the migration cost outweighs benefits. Even then, OTel can be used alongside.

25. **How do you test tracing instrumentation?**
    - Use in-memory exporters to capture spans in tests. Assert that expected spans are created with correct attributes. Use OTel SDK's `InMemorySpanExporter` for integration tests.

## Summary

Distributed tracing is essential for understanding request flow in microservices. OpenTelemetry provides the vendor-neutral standard for instrumentation. Focus on propagating context at every service boundary, sampling intelligently, and correlating traces with logs for complete observability.

## References & Learn More

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Zipkin Documentation](https://zipkin.io/pages/references.html)
- [Grafana Tempo](https://grafana.com/docs/tempo/)
- [Distributed Tracing in Practice](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)
- [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/otel/)
