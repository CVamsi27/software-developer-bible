# Error Tracking

## Definition

Error tracking is the practice of capturing, grouping, prioritizing, and alerting on application errors across all environments. Unlike logging (which records events), error tracking focuses specifically on exceptions, crashes, and failures — grouping them by stack trace and root cause to help teams fix the most impactful issues first.

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

## Interview Questions

### Beginner

1. **What is the difference between error tracking and logging?**
   - Logging records all events (info, warn, error). Error tracking specifically captures, groups, and manages exceptions with context, deduplication, and workflow features.

2. **What is a source map and why do you need it with error tracking?**
   - Source maps translate minified production code back to original source. Without them, stack traces in error tracking show unreadable minified code.

3. **What are breadcrumbs in error tracking?**
   - A chronological trail of user actions and system events leading up to an error. They help reproduce the conditions that caused the error.

4. **What is error fingerprinting?**
   - Generating a unique hash from the error type, message, and stack trace to group identical errors into single issues, even when triggered by different users.

5. **Why should you upload source maps in CI/CD?**
   - To ensure every production deployment has accurate stack traces. Manual uploads are error-prone and get forgotten.

### Intermediate

6. **How does Sentry group errors?**
   - By exception type + message + stack trace (filename + line). Same code path throwing the same error = same issue. Custom fingerprints can override grouping.

7. **What is the difference between `beforeSend` and `ignoreErrors`?**
   - `ignoreErrors` drops events matching patterns before they're processed. `beforeSend` gives you full event access to filter, modify, or drop events programmatically.

8. **How do you handle errors in async/await code with Sentry?**
   - Wrap async operations in try/catch. Use `Sentry.withScope()` to attach context. Ensure the Sentry Express error handler is after all routes.

9. **What is error regression and how do you detect it?**
   - When a previously resolved error re-appears. Sentry marks it as "Regressed" and re-opens the issue. Requires marking issues as resolved (manually or automatically).

10. **How do you set up alerts for new errors without alerting on all errors?**
    - Configure Sentry alerts for "New Issue" events only. Set up separate alerts for "Regression" events. Use issue states (unresolved/resolved) to filter.

### Senior

11. **Design an error tracking strategy for a monorepo with 10 services.**
    - One Sentry organization, separate projects per service. Shared SDK configuration. Source maps uploaded per service in CI. Unified Slack channel for critical errors. Weekly error budget review. Error ownership via CODEOWNERS.

12. **Your error tracking shows 10,000 errors/day but the app seems fine. What's happening?**
    - Likely non-critical errors (validation failures logged as errors, network retries, client-side errors). Review error grouping, adjust severity, filter non-actionable errors. Consider if some should be warnings.

13. **How do you track errors across microservices?**
    - Propagate `traceId` through all services. When an error occurs in any service, the trace context links to the original request. Use distributed tracing (OpenTelemetry) alongside error tracking.

14. **How would you handle PII in error reports?**
    - Sanitize in `beforeSend` callback. Use Sentry's `sendDefaultPii: false`. Strip sensitive fields from request bodies. Never log passwords, tokens, or PII in error context.

15. **Design an error budget system. How do you combine error tracking with SLOs?**
    - Define SLI (success rate from error tracking). Calculate error budget (1 - SLO = allowed error rate). Track actual error rate vs budget. Alert when budget is being consumed too fast. Stop deployments when budget is exhausted.

### FAANG-style

16. **If you could only add ONE thing to improve error visibility, what would it be?**
    - Automatic error grouping with source maps. Most teams have errors but can't prioritize because they see minified stack traces. Source maps + grouping turns noise into actionable issues.

17. **How would you build a custom error tracking system? What are the trade-offs vs Sentry?**
    - Build: error ingestion API, fingerprinting engine, storage (Elasticsearch), dashboard, alerting. Trade-offs: Sentry handles millions of events, has mature SDKs, and years of edge cases. Custom gives you full control over data retention and costs.

18. **Your error rate spiked 500% after a deploy. Walk through your response.**
    - Check Sentry for new/regressed issues. Identify the problematic commit. Rollback if severity is high. Check error type (5xx = server error, 4xx = client issue). Check if it's a specific endpoint or user segment. Fix forward if easy, rollback if complex.

19. **How do you handle errors in Web Workers / Service Workers?**
    - Use Sentry's browser worker plugin. Capture errors via `self.onerror` and `self.onunhandledrejection`. Ensure source maps are uploaded for worker bundles. Workers have limited context — attach available metadata manually.

20. **Explain the relationship between error tracking, monitoring, and tracing.**
    - Error tracking captures *what* went wrong (exceptions). Monitoring captures *how* the system is performing (metrics). Tracing captures *where* in the request path the failure occurred (spans). Together they give complete observability.

### Follow-ups

21. **How do you track client-side JavaScript errors?**
    - Use Sentry React/Vue/Angular SDK. Initialize in entry point. Set up `ErrorBoundary` components. Use `BrowserTracing` for performance. Upload source maps for minified bundles.

22. **What's the difference between handled and unhandled errors?**
    - Unhandled: crashes, uncaught exceptions — most critical. Handled: caught exceptions, rejected promises — lower severity but still valuable for tracking patterns.

23. **How do you test error tracking in development?**
    - Use Sentry's development mode (`environment: "development"`). Test `beforeSend` filtering. Verify source maps work locally. Use `Sentry.captureException()` in test endpoints.

24. **How do you handle errors in serverless (Lambda)?**
    - Use `@sentry/serverless`. Wrap handler with `Sentry.AWSLambda.wrapHandler()`. Ensure source maps are uploaded. Monitor Cold Start errors separately.

25. **When would you NOT use Sentry?**
    - Strict data residency requirements (Sentry Cloud may not be available in all regions). Self-hosted Sentry solves this. Very low error volume (manual logging suffices). Regulatory constraints on third-party tools.

## Summary

Error tracking transforms raw exceptions into actionable, grouped issues with context, ownership, and workflow. Sentry is the industry standard, but the principles apply to any tool: capture errors with context, group intelligently, upload source maps, track releases, and review trends regularly.

## References & Learn More

- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry Node SDK](https://docs.sentry.io/platforms/node/)
- [Sentry React SDK](https://docs.sentry.io/platforms/javascript/react/)
- [Sentry CLI](https://docs.sentry.io/product/cli/)
- [Source Maps Explained](https://www.html5rocks.com/en/tutorials/developertools/sourcemaps/)
- [Error Handling Best Practices](https://github.com/nicktraz/error-handling-best-practices)
- [Sentry Release Management](https://docs.sentry.io/product/releases/)
