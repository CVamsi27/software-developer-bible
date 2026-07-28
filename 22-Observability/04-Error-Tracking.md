# Error Tracking

[![Category: DevOps](https://img.shields.io/badge/category-DevOps-ff7f00)](.)

izing, and alerting on application errors across all environments. Unlike logging (which records events), error tracking focuses specifically on exceptions, crashes, and failures — grouping them by stack trace and root cause to help teams fix the most impactful issues first.

An **error tracking system** ingests error reports, deduplicates them via fingerprinting, enriches them with context (user, device, release), and provides workflows for resolution.

## Why Do We Need It?

1. **Visibility**: Errors in production often go unnoticed without centralized tracking

2. **Prioritization**: Group thousands of individual errors into actionable unique issues

3. **Context**: Attach user info, breadcrumbs, device data, and release version to errors

4. **Workflow**: Assign, track, and resolve errors with team accountability

5. **Prevention**: Identify regressions introduced by new deploys

6. **Performance impact**: Errors degrade user experience and waste resources

## How It Works

```text
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR TRACKING PIPELINE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ App Code │───▶│  SDK     │───▶│Transport │───▶│ Ingest   │ │
│  │ (throw)  │    │(capture) │    │ (queue)  │    │ (process)│ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                            │    │
│                                                            ▼    │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────────┐  │
│  │ Alerts   │◀───│ Dashboard│◀───│   Fingerprint & Group    │  │
│  │ (Slack,  │    │(issues)  │    │   (stack trace hash)     │  │
│  │  PagerD) │    └──────────┘    └──────────────────────────┘  │
│  └──────────┘                                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ERROR GROUPING                                          │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Stack trace:                                           │   │
│  │    TypeError: Cannot read property 'id' of undefined    │   │
│  │      at processOrder (orders.ts:45)                     │   │
│  │      at handleRequest (server.ts:120)                   │   │
│  │                                                         │   │
│  │  Fingerprint = hash of:                                 │   │
│  │    - Exception type + message                           │   │
│  │    - Stack trace (filename + line number)               │   │
│  │    - Exception code (if applicable)                     │   │
│  │                                                         │   │
│  │  Same fingerprint → Same issue, even if triggered by    │   │
│  │  different users or at different times                  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

```

### Error Severity Levels

```text
┌─────────────────────────────────────────────────────────────────┐
│  ERROR SEVERITY                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔴 FATAL     App crashes, process dies, data loss risk        │
│               → Immediate page, all hands on deck              │
│                                                                  │
│  🔴 ERROR     Unhandled exception, feature broken              │
│               → High priority, fix within hours                │
│                                                                  │
│  🟡 WARNING   Caught exception, degraded experience            │
│               → Medium priority, fix in current sprint         │
│                                                                  │
│  🟢 INFO      Non-exception error (validation failure)         │
│               → Track for trends, fix opportunistically        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

## Code Examples

### Sentry Integration (Node.js)

```typescript
import * as Sentry from "@sentry/node";
import { nodeProfilingIntegration } from "@sentry/profiling-node";
import express from "express";

// Initialize Sentry BEFORE any other imports
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || "development",
  release: process.env.APP_VERSION || "1.0.0",

  // Sampling
  tracesSampleRate: process.env.NODE_ENV === "production" ? 0.2 : 1.0,
  profilesSampleRate: 0.1,

  // Integrations
  integrations: [
    nodeProfilingIntegration(),
    new Sentry.Integrations.Http({ tracing: true }),
    new Sentry.Integrations.Express({ app }),
    new Sentry.Integrations.Postgres(),
  ],

  // Filtering
  beforeSend(event, hint) {
    // Don't send in development
    if (process.env.NODE_ENV === "development") {
      console.error("Sentry event (dev):", event.exception?.values);
      return null;
    }

    // Filter out known non-errors
    if (hint?.originalException instanceof Sentry.Baggage) {
      return null;
    }

    // Sanitize sensitive data
    if (event.request?.data) {
      delete event.request.data.password;
      delete event.request.data.creditCard;
      delete event.request.data.ssn;
    }

    return event;
  },

  // Ignore specific errors
  ignoreErrors: [
    "ECONNRESET",
    "ECONNREFUSED",
    "Socket closed unexpectedly",
    /^ResizeObserver loop/,
    /^Network request failed/,
  ],

  // Custom tags
  initialScope: {
    tags: {
      service: "order-service",
      team: "platform",
    },
  },

  // Attach source maps in production
  attachStacktrace: true,
});

const app = express();

// Sentry request handler (must be first middleware)
app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// Your routes here
app.use(express.json());

app.post("/api/orders", async (req, res) => {
  const transaction = Sentry.startTransaction({
    name: "processOrder",
    op: "order.process",
  });

  try {
    Sentry.configureScope((scope) => {
      scope.setTransactionName("POST /api/orders");
      scope.setUser({ id: req.body.userId });
      scope.setTag("order.type", req.body.type);
    });

    const order = await processOrder(req.body);
    res.json(order);
  } catch (err) {
    Sentry.captureException(err, {
      extra: {
        orderData: req.body,
        requestId: req.requestId,
      },
    });
    res.status(500).json({ error: "Internal server error" });
  } finally {
    transaction.end();
  }
});

// Sentry error handler (must be last middleware)
app.use(Sentry.Handlers.errorHandler());

export { app };

```

### Custom Error Boundary with Context

```typescript
import * as Sentry from "@sentry/node";
import { Request, Response, NextFunction } from "express";

// Custom error classes with Sentry context
class AppError extends Error {
  public statusCode: number;
  public isOperational: boolean;
  public errorCode: string;

  constructor(
    message: string,
    statusCode: number,
    errorCode: string,
    isOperational = true
  ) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    this.errorCode = errorCode;
    Object.setPrototypeOf(this, new.target.prototype);
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  public fields: Record<string, string>;

  constructor(message: string, fields: Record<string, string>) {
    super(message, 400, "VALIDATION_ERROR");
    this.fields = fields;
  }
}

class PaymentError extends AppError {
  public paymentId: string;
  public provider: string;

  constructor(message: string, paymentId: string, provider: string) {
    super(message, 402, "PAYMENT_FAILED");
    this.paymentId = paymentId;
    this.provider = provider;
  }
}

// Global error handler
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
) {
  // Operational errors (expected)
  if (err instanceof AppError && err.isOperational) {
    Sentry.withScope((scope) => {
      scope.setLevel("warning");
      scope.setTag("error.code", err.errorCode);
      scope.setContext("error_details", {
        statusCode: err.statusCode,
        errorCode: err.errorCode,
        ...(err instanceof ValidationError ? { fields: err.fields } : {}),
        ...(err instanceof PaymentError
          ? { paymentId: err.paymentId, provider: err.provider }
          : {}),
      });
      Sentry.captureException(err);
    });

    return res.status(err.statusCode).json({
      error: {
        code: err.errorCode,
        message: err.message,
        ...(err instanceof ValidationError ? { fields: err.fields } : {}),
      },
    });
  }

  // Unexpected errors (bugs)
  Sentry.withScope((scope) => {
    scope.setLevel("error");
    scope.setTag("error.type", "unexpected");
    scope.setContext("request", {
      method: req.method,
      url: req.originalUrl,
      query: req.query,
      body: sanitizeBody(req.body),
      userId: (req as any).userId,
      requestId: req.requestId,
    });
    scope.setExtras({
      headers: req.headers,
      ip: req.ip,
    });
    Sentry.captureException(err);
  });

  console.error("Unexpected error:", err);

  res.status(500).json({
    error: {
      code: "INTERNAL_ERROR",
      message:
        process.env.NODE_ENV === "production"
          ? "An unexpected error occurred"
          : err.message,
    },
  });
}

function sanitizeBody(body: any): any {
  if (!body) return body;
  const sanitized = { ...body };
  const sensitiveFields = ["password", "token", "creditCard", "ssn", "cvv"];
  for (const field of sensitiveFields) {
    if (sanitized[field]) sanitized[field] = "[REDACTED]";
  }
  return sanitized;
}

export { AppError, ValidationError, PaymentError, errorHandler };

```

### Frontend Error Tracking (React)

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.REACT_APP_VERSION,
  integrations: [
    new BrowserTracing({
      tracingOrigins: ["api.example.com"],
      beforeNavigate: (context) => {
        // Sanitize URLs to remove PII
        return {
          ...context,
          name: window.location.pathname.replace(/\/\d+/g, "/:id"),
        };
      },
    }),
  ],
  tracesSampleRate: 0.2,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  beforeSend(event) {
    // Filter out non-actionable errors
    if (event.exception?.values?.[0]?.type === "ChunkLoadError") {
      return null;
    }
    return event;
  },
});

// React Error Boundary
import { ErrorBoundary } from "@sentry/react";

function App() {
  return (
    <ErrorBoundary
      fallback={<ErrorPage />}
      onError={(error, errorInfo) => {
        console.error("React Error:", error, errorInfo);
      }}
    >
      <Router>
        <Routes>...</Routes>
      </Router>
    </ErrorBoundary>
  );
}

// Replay integration for debugging
Sentry.addGlobalEventProcessor((event, hint) => {
  if (hint?.originalException) {
    Sentry.setContext("browser", {
      url: window.location.href,
      userAgent: navigator.userAgent,
    });
  }
  return event;
});

```

### Error Tracking with Source Maps

```bash
# Build with source maps enabled
npx tsc --sourceMap
# or
npx webpack --mode production --devtool source-map

# Upload source maps to Sentry
npx @sentry/cli releases files "$RELEASE" upload-sourcemaps ./dist \
  --url-prefix "~/dist" \
  --validate

# Mark release as deployed
npx @sentry/cli releases deploys "$RELEASE" new \
  --environment production

# Verify source maps are correct
npx @sentry/cli releases files "$RELEASE" list

```

```json
// sentry.properties (in repo root)
defaults.org=your-org
defaults.project=your-project
cli.releases.auto=true
cli.executable.path=./node_modules/.bin/sentry-cli

```

### Release Tracking

```typescript
// Track which release introduced an error
Sentry.init({
  release: `${process.env.APP_NAME}@${process.env.APP_VERSION}`,
  // This tells Sentry: "this error started appearing in version 2.3.0"
  // Sentry will show: "First seen in 2.3.0, last seen in 2.5.0"
});

// Tag deployment
Sentry.addBreadcrumb({
  category: "deployment",
  message: `Deployed ${process.env.APP_VERSION} to ${process.env.DEPLOY_ENV}`,
  level: "info",
});

// Track regression: when a previously resolved issue re-appears
// Sentry marks it as "Regressed" automatically

```

### Breadcrumbs

```typescript
// Automatic breadcrumbs (captured by SDK)
// - Navigation events
// - DOM events (clicks)
// - Console logs
// - Network requests
// - History changes

// Manual breadcrumbs
Sentry.addBreadcrumb({
  category: "auth",
  message: "User logged in",
  level: "info",
  data: {
    userId: user.id,
    method: "oauth",
  },
});

Sentry.addBreadcrumb({
  category: "ui.click",
  message: "Clicked checkout button",
  level: "info",
  data: {
    cartTotal: cart.total,
    itemCount: cart.items.length,
  },
});

// Breadcrumb trail helps reproduce the user's journey before the error:
// 1. Navigated to /checkout
// 2. Clicked "Apply coupon"
// 3. Typed coupon code "SAVE20"
// 4. Clicked "Checkout" button
// 5. ERROR: TypeError: Cannot read property 'discount' of undefined

```

## Real-World Use Cases

1. **Regression detection**: Automatically detect when a new deploy introduces errors

2. **User impact analysis**: See how many users are affected by each error

3. **Performance monitoring**: Track error rates alongside latency and throughput

4. **A/B test monitoring**: Compare error rates between experiment variants

5. **Mobile crash tracking**: Track native crashes with device/OS context

6. **API error monitoring**: Track 4xx/5xx rates with endpoint-level grouping

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Swallowing errors silently | Bugs hide forever | Always log or track caught exceptions |
| Not uploading source maps | Production errors show minified code | Upload source maps in CI/CD pipeline |
| Too many `ignoreErrors` filters | Real errors get filtered out | Be selective; only ignore known non-issues |
| No error ownership | Errors pile up with no assignee | Assign error owners per team/service |
| Alerting on all errors | Alert fatigue | Only alert on new/regressed/high-impact errors |
| Logging PII in error context | Compliance violations | Sanitize error context before sending |

## Best Practices

1. **One error tracking service per organization** — avoid duplicate tools

2. **Upload source maps in CI/CD** — every deploy should upload maps

3. **Tag releases** — track which version introduced each error

4. **Set up error budgets** — combine with SLOs for reliability targets

5. **Use issue owners** — assign code owners to error groups for accountability

6. **Monitor error rate as a metric** — alert on spikes, not individual errors

7. **Integrate with Slack/Teams** — real-time notifications for new critical errors

8. **Use user feedback** — attach user-reported context to error reports

9. **Clean up resolved issues** — auto-resolve issues not seen in 7+ days
10. **Review error trends weekly** — identify recurring patterns to fix systemic issues

## Performance Considerations

- **SDK overhead** — Sentry SDK adds <5ms per event; negligible for most apps
- **Source map upload time** — large bundles may take 30-60s to upload; cache in CI
- **Event volume** — aggressive sampling (`tracesSampleRate: 0.1`) reduces costs
- **Before send filtering** — filter client-side to reduce network calls to Sentry
- **Queue buffering** — SDK buffers events before sending; flush on process exit

## Summary

Error tracking transforms raw exceptions into actionable, grouped issues with context, ownership, and workflow. Sentry is the industry standard, but the principles apply to any tool: capture errors with context, group intelligently, upload source maps, track releases, and review trends regularly.

---

## Cheat Sheet
```text
ERROR TRACKING CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  npx tsc --sourceMap
  npx webpack --mode production --devtool source-map
  npx @sentry/cli releases files "$RELEASE" upload-sourcemaps ./dist \
    --url-prefix "~/dist" \
    --validate
  npx @sentry/cli releases deploys "$RELEASE" new \
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [Kubernetes](../14-Kubernetes/)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry Node SDK](https://docs.sentry.io/platforms/node/)
- [Sentry React SDK](https://docs.sentry.io/platforms/javascript/react/)
- [Sentry CLI](https://docs.sentry.io/product/cli/)
- [Source Maps Explained](https://www.html5rocks.com/en/tutorials/developertools/sourcemaps/)
- [Error Handling Best Practices](https://github.com/nicktraz/node-error-handling)
- [Sentry Release Management](https://docs.sentry.io/product/releases/)
