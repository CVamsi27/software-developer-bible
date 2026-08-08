---
section: REST API
category: Backend
tags: [concept]
---

# API Error Handling & Response Design

> **TL;DR:** API error design is the difference between a 2am page and a quiet on-call rotation. Use a consistent error envelope (RFC 7807 problem details or a custom JSON shape), pick the right status code, never leak stack traces, and return a stable `requestId` so support can find the log. The senior test is what your error response looks like at 3am when the database is on fire.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

API error handling is the discipline of consistently shaping the response when something goes wrong — bad client input (4xx), server failure (5xx), business rule violation (409/422), or upstream dependency failure (502/503/504). The two industry-standard envelopes are **RFC 7807 Problem Details for HTTP APIs** (`application/problem+json`) and a custom JSON shape (e.g., `{ error: { code, message, details, requestId } }`). The senior design choice is whether to standardize on RFC 7807, a custom shape, or a hybrid.

## Why Do We Need It?

1. **Client trust** — A stable error envelope is the contract clients write their retry/UX code against.
2. **Debuggability** — Every error carries a `requestId` / `traceId` so support can grep logs and find the failing request in seconds.
3. **Security** — Stack traces in production responses leak file paths, query shapes, internal class names. Errors must be sanitized.
4. **DX** — A consistent `{ code, message, field, hint }` shape lets the frontend write one error component, not 30.
5. **Observability** — Structured error logs with stable codes (`INVALID_TOKEN`, `USER_LOCKED`) make alerting and dashboards tractable.
6. **Retry safety** — Returning 503 + `Retry-After` lets well-behaved clients back off automatically; a 500 with no signal does not.
7. **Compliance** — GDPR/HIPAA-shaped error responses must not echo PII; the envelope gives you the place to enforce scrubbing.

## How It Works

```text
Exception thrown
   │
   ├── Domain exception (UserNotFoundError)
   │     │
   │     ▼
   │   Global Exception Filter
   │     ├── maps domain error → HTTP status (404)
   │     ├── builds problem document
   │     ├── adds requestId from AsyncLocalStorage
   │     ├── logs structured error
   │     └── returns sanitized body
   │
   ├── Unknown exception
   │     │
   │     ▼
   │   Catch-all filter
   │     ├── logs full stack
   │     ├── returns 500 with safe body
   │     └── alerts on-call
   │
   └── Validation error (class-validator)
         │
         ▼
       ValidationPipe → 400 with field-level errors
```

## Code Examples

### Domain Error Hierarchy

```typescript
// errors/domain.errors.ts
export class DomainError extends Error {
  constructor(public readonly code: string, message: string, public readonly httpStatus: number) {
    super(message);
    this.name = this.constructor.name;
  }
}
export class NotFoundError extends DomainError {
  constructor(resource: string, id: string) {
    super('NOT_FOUND', `${resource} ${id} not found`, 404);
  }
}
export class ConflictError extends DomainError {
  constructor(message: string) { super('CONFLICT', message, 409); }
}
export class ValidationError extends DomainError {
  constructor(public readonly fields: Record<string, string[]>) {
    super('VALIDATION_FAILED', 'Invalid input', 422);
  }
}
```

### RFC 7807 Problem Document

```typescript
// filters/problem-details.filter.ts
import { ArgumentsHost, Catch, ExceptionFilter, HttpException } from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class ProblemDetailsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const res = ctx.getResponse<Response>();
    const req = ctx.getRequest<Request>();
    const requestId = (req as any).id;   // from request-id middleware

    let status = 500;
    let title = 'Internal Server Error';
    let type = 'about:blank';
    let detail: string | undefined;
    let code = 'INTERNAL_ERROR';
    const errors: Record<string, string[]> | undefined = undefined;

    if (exception instanceof DomainError) {
      status = exception.httpStatus;
      title = exception.code;
      type = `https://api.example.com/errors/${exception.code.toLowerCase()}`;
      detail = exception.message;
      code = exception.code;
      if (exception instanceof ValidationError) (errors as any) = exception.fields;
    } else if (exception instanceof HttpException) {
      status = exception.getStatus();
      title = exception.name;
      detail = exception.message;
    } else {
      // Log full stack server-side
      console.error('[UNHANDLED]', exception, { requestId });
    }

    res.status(status).type('application/problem+json').send({
      type, title, status, detail, instance: req.originalUrl, code, errors, requestId,
    });
  }
}
```

### Custom JSON Envelope (the Stripe / Twilio shape)

```typescript
// filters/api-error.filter.ts
interface ApiErrorBody {
  error: {
    code: string;
    message: string;
    field?: string;
    details?: unknown;
    requestId: string;
  };
}

@Catch()
export class ApiErrorFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const req = host.switchToHttp().getRequest();
    const res = host.switchToHttp().getResponse();

    const requestId = (req as any).id;
    let status = 500;
    let body: ApiErrorBody = {
      error: { code: 'INTERNAL_ERROR', message: 'Something went wrong', requestId },
    };

    if (exception instanceof DomainError) {
      status = exception.httpStatus;
      body = { error: { code: exception.code, message: exception.message, requestId } };
    } else if (exception instanceof HttpException) {
      status = exception.getStatus();
      const resp = exception.getResponse() as any;
      body = { error: { code: status.toString(), message: resp.message ?? exception.message, requestId } };
    } else {
      console.error('[UNHANDLED]', exception, { requestId });
    }

    res.status(status).json(body);
  }
}
```

### Register Globally and Per-Controller

```typescript
// main.ts
app.useGlobalFilters(new ApiErrorFilter());   // or use APP_FILTER provider
app.use(requestIdMiddleware);                 // sets req.id for the filter
```

### ValidationPipe with Field-Level Errors

```typescript
// main.ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
    exceptionFactory: (errors) => {
      const fields: Record<string, string[]> = {};
      for (const e of errors) {
        fields[e.property] = Object.values(e.constraints ?? {});
      }
      return new ValidationError(fields);
    },
  }),
);
```

### Retry-After for 503 / 429

```typescript
@Get('heavy')
async heavy(@Res({ passthrough: true }) res: Response) {
  if (this.queue.isOverloaded()) {
    res.setHeader('Retry-After', '5');
    throw new HttpException('Overloaded', HttpStatus.SERVICE_UNAVAILABLE);
  }
  return this.svc.run();
}
```

## Real-World Use Cases

1. **Public API** — RFC 7807 + a docs page per `type` URL (`/errors/not-found`) gives clients a reference for every error code.
2. **Internal microservices** — A simple `{ code, message, requestId }` envelope is enough; everyone agrees on the shape.
3. **Mobile apps** — Stable error codes power localized error messages; a `field` array drives inline form errors.
4. **Idempotency on retries** — Return a 409 with `idempotencyKey` echo so a retried POST after success doesn't double-charge.
5. **Rate-limit responses** — 429 with `Retry-After` and `X-RateLimit-Remaining` so well-behaved clients back off.
6. **Multi-tenant** — Tenant-scoped error codes (`{tenant}.USER_LOCKED`) keep dashboards per-tenant.
7. **On-call alerts** — Distinct stable codes (`DB_DOWN`, `STRIPE_5XX`) make Prometheus rules and PagerDuty routing trivial.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Returning 200 with `{ ok: false, error: ... }` | Always use the right HTTP status code |
| Stack trace in the response body | Log server-side, return a safe body |
| Different envelope shapes per endpoint | One global filter, one shape |
| No `requestId` / `traceId` | Always include one — it is your lifeline in incident response |
| `message: "User not found"` with no code | Add a stable `code` (`USER_NOT_FOUND`) for client logic |
| Catching all and returning 500 silently | Log with context, alert on the rate of 500s |
| 500 for validation errors | 400 for malformed JSON, 422 for business validation |
| Echoing PII in error messages | Strip emails, IDs, names from error details |
| Returning HTML error pages from a JSON API | `Content-Type: application/problem+json` (or your envelope) |
| Retrying on non-idempotent 5xx without an `idempotencyKey` | Return 409 for already-processed; only retry safe verbs |

## Best Practices

1. **One global filter** — Per-endpoint exception handling is a maintenance disaster; one filter maps everything.
2. **Stable error codes** — `USER_NOT_FOUND`, `INVALID_TOKEN`, `RATE_LIMITED` — clients switch on these, not on `message`.
3. **Always include `requestId`** — Tie the response to the log line; it is your incident-response superpower.
4. **Right status code** — 400 (malformed), 401 (no auth), 403 (forbidden), 404 (not found), 409 (conflict), 422 (validation), 429 (rate-limited), 5xx (server).
5. **Sanitize production responses** — No stack traces, no internal class names, no PII; log the full thing server-side.
6. **`Retry-After` for transient failures** — 503 / 504 / 429 with a seconds hint; clients back off automatically.
7. **Document errors in OpenAPI** — `@ApiResponse({ status: 4xx, type: ErrorDto })` for every realistic client error.
8. **Idempotency keys for write retries** — `POST /orders` with `Idempotency-Key: <uuid>`; 409 if the same key was used.
9. **Localized messages optional** — Return `code` + `message`; let the client map `code` to a translated string.
10. **Alert on 5xx rate** — A spike in `INTERNAL_ERROR` is a page; a spike in `NOT_FOUND` is not.

## Performance Considerations

- A global filter adds microseconds per request — negligible.
- Validation error responses can be large (one entry per field); keep the body shape compact for mobile.
- Logging the full error on every 4xx is expensive; sample 4xx, log all 5xx.
- Stack-trace capture in Node.js is expensive; only capture for unhandled 5xx.

## Summary

- Pick one error envelope (RFC 7807 or a custom shape) and enforce it via a single global filter.
- Always include a stable `code`, a human `message`, and a `requestId` / `traceId`.
- Right status code, sanitized body, full-stack log server-side.
- Document every realistic error in OpenAPI; clients write retry/UX code against the envelope.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| RFC 7807 | `application/problem+json` standard for HTTP API errors |
| Custom envelope | `{ error: { code, message, field?, requestId } }` (Stripe, Twilio) |
| `requestId` / `traceId` | Per-request correlation id in body + log + `X-Request-Id` header |
| 400 vs 422 | 400 = malformed JSON; 422 = valid JSON but fails business validation |
| 409 Conflict | Idempotency conflict, duplicate resource, version mismatch |
| 429 + `Retry-After` | Rate limit with a backoff hint in seconds |
| 503 + `Retry-After` | Transient upstream failure; let well-behaved clients retry |
| Domain errors | Custom error classes mapped to status by the global filter |
| `exceptionFactory` | ValidationPipe hook to build a structured 422 body |
| `Idempotency-Key` | Header on write requests to dedupe retries |

---

## See Also
- [Microservices](../12-Microservices/) (consistent envelopes across services)
- [NestJS](../06-NestJS/) (ExceptionFilter in NestJS)
- [Security](../09-Security/) (don't leak info via error messages)
- [System Design](../11-System-Design/) (error envelopes in API contracts)

## References & Learn More

- [RFC 7807 — Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
- [RFC 9457 — Problem Details for HTTP APIs (obsoletes 7807)](https://datatracker.ietf.org/doc/html/rfc9457)
- [Stripe API Errors](https://stripe.com/docs/api/errors)
- [Twilio API Errors](https://www.twilio.com/docs/api/errors)
- [Google API Design Guide — Errors](https://cloud.google.com/apis/design/errors)
- [Microsoft REST API Guidelines — Errors](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#errors)
