# HTTP Status Codes

## Definition

HTTP status codes are three-digit numbers returned by the server in response to a client's request. They indicate whether the request was successful, redirected, or encountered an error. Status codes are grouped into five classes based on their first digit: 1xx (informational), 2xx (success), 3xx (redirection), 4xx (client error), and 5xx (server error).

## Why Do We Need It?

Status codes provide standardized communication between client and server:

1. **Machine-readable** - Clients can programmatically handle different responses
2. **Debugging** - Developers can quickly identify issues
3. **Caching** - Browsers and proxies optimize behavior based on status
4. **Security** - Prevent information leakage with appropriate codes
5. **API contracts** - Clear expectations for success and failure scenarios

## How It Works

### Status Code Classes

```text
HTTP Status Code Classes
════════════════════════

Class   Meaning           Examples
─────────────────────────────────────
1xx     Informational     100 Continue, 101 Switching Protocols
2xx     Success           200 OK, 201 Created, 204 No Content
3xx     Redirection       301 Moved Permanently, 304 Not Modified
4xx     Client Error      400 Bad Request, 401 Unauthorized, 404 Not Found
5xx     Server Error      500 Internal Server Error, 503 Service Unavailable
```

### 1xx Informational

```text
1xx Status Codes
════════════════

100 Continue
  - Server received request headers; client should proceed
  - Used with Expect: 100-continue header

101 Switching Protocols
  - Server is switching protocols as requested by client
  - Common with WebSocket upgrades

102 Processing (WebDAV)
  - Server has received and is processing the request
  - No status available yet
```

```typescript
// 100 Continue - Express handles automatically
// Client sends Expect: 100-continue header

// 101 Switching Protocols - WebSocket upgrade
app.get('/ws', (req, res) => {
  // Express handles WebSocket upgrade automatically with ws library
});
```

### 2xx Success

```text
2xx Status Codes
════════════════

200 OK
  - Request succeeded
  - Used for GET, PUT, PATCH, DELETE responses

201 Created
  - Resource successfully created
  - Should include Location header with new resource URL

202 Accepted
  - Request accepted for processing
  - Processing not yet completed (async operations)

204 No Content
  - Request succeeded but no content to return
  - Used for DELETE responses

206 Partial Content
  - Server delivering only part of the resource
  - Used with Range header for resumable downloads
```

```typescript
// 200 OK
app.get('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  res.status(200).json({ data: user });
});

// 201 Created
app.post('/api/users', async (req, res) => {
  const user = await UserService.create(req.body);
  res.status(201)
    .header('Location', `/api/users/${user.id}`)
    .json({ data: user });
});

// 202 Accepted
app.post('/api/reports/generate', async (req, res) => {
  const job = await ReportService.startGeneration(req.body);
  res.status(202).json({
    data: job,
    _links: {
      self: `/api/reports/jobs/${job.id}`,
      status: `/api/reports/jobs/${job.id}/status`
    }
  });
});

// 204 No Content
app.delete('/api/users/:id', async (req, res) => {
  await UserService.delete(req.params.id);
  res.status(204).end();
});

// 206 Partial Content
app.get('/api/files/:id', async (req, res) => {
  const range = req.headers.range;
  if (range) {
    const { start, end } = parseRange(range);
    const file = await FileService.getPartial(req.params.id, start, end);
    res.status(206)
      .header('Content-Range', `bytes ${start}-${end}/${file.totalSize}`)
      .header('Content-Length', end - start + 1)
      .send(file.data);
  } else {
    const file = await FileService.get(req.params.id);
    res.json({ data: file });
  }
});
```

### 3xx Redirection

```text
3xx Status Codes
════════════════

301 Moved Permanently
  - Resource has permanently moved to new URL
  - Search engines update their index
  - Browser caches this redirect

302 Found (Temporary Redirect)
  - Resource temporarily at different URL
  - Original URL may be used again
  - Browser makes new request to new URL

304 Not Modified
  - Resource hasn't changed since last request
  - Used with ETag/If-None-Match for caching
  - No body in response

307 Temporary Redirect
  - Like 302 but preserves HTTP method
  - POST request stays POST after redirect

308 Permanent Redirect
  - Like 301 but preserves HTTP method
  - POST request stays POST after redirect
```

```typescript
// 301 Moved Permanently
app.get('/old-path', (req, res) => {
  res.redirect(301, '/new-path');
});

// 302 Found
app.get('/temp-path', (req, res) => {
  res.redirect(302, '/other-path');
});

// 304 Not Modified
app.get('/api/products', async (req, res) => {
  const products = await ProductService.findAll();
  const etag = generateETag(products);

  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }

  res.set({ 'ETag': etag, 'Cache-Control': 'public, max-age=3600' });
  res.json({ data: products });
});

// 307 Temporary Redirect
app.post('/api/users', (req, res) => {
  res.redirect(307, '/api/v2/users');
});
```

### 4xx Client Errors

```text
4xx Status Codes
════════════════

400 Bad Request
  - Malformed request syntax
  - Invalid JSON, missing required fields

401 Unauthorized
  - Authentication required
  - Missing or invalid credentials

403 Forbidden
  - Authenticated but insufficient permissions
  - Server refuses to authorize

404 Not Found
  - Resource doesn't exist
  - Endpoint doesn't exist

405 Method Not Allowed
  - HTTP method not supported for this resource
  - Include Allow header with supported methods

408 Request Timeout
  - Server timed out waiting for request
  - Client took too long to send request

409 Conflict
  - Request conflicts with current state
  - Duplicate resource, version conflict

410 Gone
  - Resource permanently removed
  - Unlike 404, this is intentional and permanent

413 Payload Too Large
  - Request body exceeds server limits
  - Reduce request size

415 Unsupported Media Type
  - Content-Type header not supported
  - Check request format

422 Unprocessable Entity
  - Request well-formed but semantically invalid
  - Validation errors

429 Too Many Requests
  - Rate limit exceeded
  - Check Retry-After header
```

```typescript
// 400 Bad Request
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({
      error: 'Bad Request',
      message: 'Missing required fields',
      details: {
        ...(!name && { name: 'Required' }),
        ...(!email && { email: 'Required' })
      }
    });
  }
});

// 401 Unauthorized
app.get('/api/profile', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  try {
    const user = verifyToken(token);
    req.user = user;
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
});

// 403 Forbidden
app.delete('/api/users/:id', authenticate, (req, res) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Insufficient permissions' });
  }
});

// 404 Not Found
app.get('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
});

// 405 Method Not Allowed
app.all('/api/users/:id', (req, res) => {
  res.status(405)
    .set({ 'Allow': 'GET, PUT, PATCH, DELETE' })
    .json({ error: 'Method not allowed' });
});

// 409 Conflict
app.post('/api/users', async (req, res) => {
  const existing = await UserService.findByEmail(req.body.email);
  if (existing) {
    return res.status(409).json({ error: 'Email already exists' });
  }
});

// 422 Unprocessable Entity
app.post('/api/users', (req, res) => {
  const errors = validateUser(req.body);
  if (errors.length > 0) {
    return res.status(422).json({ error: 'Validation failed', details: errors });
  }
});

// 429 Too Many Requests
app.use('/api', rateLimiter({
  windowMs: 15 * 60 * 1000,
  max: 100,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: 60
    });
    res.set('Retry-After', '60');
  }
}));
```

### 5xx Server Errors

```text
5xx Status Codes
════════════════

500 Internal Server Error
  - Generic server error
  - Unexpected condition encountered
  - Don't expose internal details

501 Not Implemented
  - Server doesn't support the functionality
  - Feature not yet implemented

502 Bad Gateway
  - Invalid response from upstream server
  - Gateway/proxy received bad response

503 Service Unavailable
  - Server temporarily unable to handle request
  - Maintenance, overload, or dependency down
  - Include Retry-After header

504 Gateway Timeout
  - Upstream server didn't respond in time
  - Gateway timeout waiting for response
```

```typescript
// 500 Internal Server Error
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'production' ? 'Something went wrong' : err.message
  });
});

// 502 Bad Gateway
app.get('/api/external', async (req, res) => {
  try {
    const data = await externalService.fetch();
    res.json({ data });
  } catch (err) {
    if (err.code === 'ECONNREFUSED') {
      return res.status(502).json({ error: 'Bad Gateway: External service unavailable' });
    }
    throw err;
  }
});

// 503 Service Unavailable
app.get('/api/status', async (req, res) => {
  const isHealthy = await checkHealth();
  if (!isHealthy) {
    res.set('Retry-After', '300');
    return res.status(503).json({ error: 'Service Unavailable', retryAfter: 300 });
  }
  res.json({ status: 'healthy' });
});

// 504 Gateway Timeout
app.get('/api/data', async (req, res) => {
  try {
    const data = await Promise.race([
      fetchFromService(),
      new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 30000))
    ]);
    res.json({ data });
  } catch (err) {
    if (err.message === 'timeout') {
      return res.status(504).json({ error: 'Gateway Timeout' });
    }
    throw err;
  }
});
```

## Code Examples

### Complete Status Code Handler

```typescript
import express, { Request, Response, NextFunction } from 'express';

// Custom error classes
class AppError extends Error {
  constructor(public statusCode: number, message: string, public details?: any) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(404, id ? `${resource} with ID ${id} not found` : `${resource} not found`);
  }
}

class ValidationError extends AppError {
  constructor(details: any) {
    super(422, 'Validation failed', details);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(401, message);
  }
}

class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(403, message);
  }
}

class ConflictError extends AppError {
  constructor(message: string) {
    super(409, message);
  }
}

// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(err.details && { details: err.details })
    });
  }

  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'production' ? 'Something went wrong' : err.message
  });
});

// Route handlers with proper status codes
app.get('/api/users', async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

app.get('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) throw new NotFoundError('User', req.params.id);
  res.json({ data: user });
});

app.post('/api/users', async (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    throw new ValidationError({ name: !name ? 'Required' : undefined, email: !email ? 'Required' : undefined });
  }

  const existing = await UserService.findByEmail(email);
  if (existing) throw new ConflictError('Email already exists');

  const user = await UserService.create({ name, email });
  res.status(201).header('Location', `/api/users/${user.id}`).json({ data: user });
});

app.put('/api/users/:id', authenticate, async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) throw new NotFoundError('User', req.params.id);

  const updated = await UserService.replace(req.params.id, req.body);
  res.json({ data: updated });
});

app.delete('/api/users/:id', authenticate, async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) throw new NotFoundError('User', req.params.id);

  await UserService.delete(req.params.id);
  res.status(204).end();
});
```

## Real-World Use Cases

### 1. Authentication Flow

```typescript
// Login
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }

  const user = await UserService.findByEmail(email);
  if (!user || !await bcrypt.compare(password, user.password)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateJWT(user);
  res.json({ data: { token, user: { id: user.id, email: user.email } } });
});

// Protected route
app.get('/api/profile', authenticate, async (req, res) => {
  const user = await UserService.findById(req.user.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ data: user });
});
```

### 2. File Operations

```typescript
// Upload with various status codes
app.post('/api/files', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file provided' });
  }

  if (req.file.size > 10 * 1024 * 1024) {
    return res.status(413).json({ error: 'File too large (max 10MB)' });
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  if (!allowedTypes.includes(req.file.mimetype)) {
    return res.status(415).json({ error: 'Unsupported file type' });
  }

  const file = await FileService.create(req.file);
  res.status(201).json({ data: file });
});

// Download with range support
app.get('/api/files/:id', async (req, res) => {
  const file = await FileService.findById(req.params.id);
  if (!file) {
    return res.status(404).json({ error: 'File not found' });
  }

  if (req.headers.range) {
    const range = parseRange(req.headers.range, file.size);
    const stream = await FileService.getStream(file.id, range);

    res.status(206)
      .set({
        'Content-Range': `bytes ${range.start}-${range.end}/${file.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': range.end - range.start + 1,
        'Content-Type': file.mimeType
      });
    stream.pipe(res);
  } else {
    res.set({
      'Content-Length': file.size,
      'Content-Type': file.mimeType,
      'Accept-Ranges': 'bytes'
    });
    const stream = await FileService.getStream(file.id);
    stream.pipe(res);
  }
});
```

### 3. Payment Processing

```typescript
app.post('/api/payments', authenticate, async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];

  if (!idempotencyKey) {
    return res.status(400).json({ error: 'Idempotency-Key header required' });
  }

  const existing = await PaymentService.findByIdempotencyKey(idempotencyKey);
  if (existing) {
    return res.json({ data: existing });
  }

  try {
    const payment = await PaymentService.create({
      userId: req.user.id,
      ...req.body,
      idempotencyKey
    });
    res.status(201).json({ data: payment });
  } catch (err) {
    if (err.code === 'card_declined') {
      return res.status(402).json({ error: 'Payment failed', details: err.message });
    }
    throw err;
  }
});
```

## Common Mistakes

### 1. Always Returning 200

```typescript
// ❌ Bad
app.post('/api/users', async (req, res) => {
  try {
    const user = await UserService.create(req.body);
    res.json({ data: user });  // Should be 201
  } catch (err) {
    res.json({ error: err.message });  // Should be 4xx or 5xx
  }
});

// ✅ Good
app.post('/api/users', async (req, res) => {
  try {
    const user = await UserService.create(req.body);
    res.status(201).json({ data: user });
  } catch (ValidationError) {
    res.status(422).json({ error: 'Validation failed' });
  } catch (ConflictError) {
    res.status(409).json({ error: 'Email exists' });
  }
});
```

### 2. Exposing Internal Errors

```typescript
// ❌ Bad
res.status(500).json({ error: err.message, stack: err.stack });

// ✅ Good
res.status(500).json({
  error: 'Internal Server Error',
  message: process.env.NODE_ENV === 'production' ? 'Something went wrong' : err.message
});
```

### 3. Wrong Error for Authentication vs Authorization

```typescript
// ❌ Bad: Using 403 for unauthenticated
if (!req.user) {
  return res.status(403).json({ error: 'Not authenticated' });
}

// ✅ Good: 401 for unauthenticated, 403 for unauthorized
if (!req.user) {
  return res.status(401).json({ error: 'Authentication required' });
}
if (req.user.role !== 'admin') {
  return res.status(403).json({ error: 'Insufficient permissions' });
}
```

### 4. Missing Location Header for 201

```typescript
// ❌ Bad
res.status(201).json({ data: user });

// ✅ Good
res.status(201).header('Location', `/api/users/${user.id}`).json({ data: user });
```

### 5. Not Including Retry-After for 429/503

```typescript
// ❌ Bad
res.status(429).json({ error: 'Rate limited' });

// ✅ Good
res.set('Retry-After', '60');
res.status(429).json({ error: 'Rate limited', retryAfter: 60 });
```

## Best Practices

1. **Use appropriate codes** - Match status code to the actual situation
2. **Be consistent** - Same error types should always return same codes
3. **Include error details** - Help clients understand what went wrong
4. **Don't expose internals** - Hide stack traces and server details in production
5. **Use 201 for creation** - Always with Location header
6. **Use 204 for deletion** - No content to return
7. **Use 401 vs 403 correctly** - 401: not authenticated, 403: not authorized
8. **Include Retry-After** - For 429 and 503 responses
9. **Document status codes** - In API documentation
10. **Handle all codes clientside** - Don't assume success

## Performance Considerations

- **304 responses** - Save bandwidth with conditional requests
- **429 responses** - Protect server from overload
- **503 responses** - Graceful degradation during maintenance
- **Caching** - 2xx responses with cache headers improve performance
- **Compression** - 200 responses benefit from gzip

## Interview Questions

### Beginner (5)

1. **What does 200 OK mean?** - Request succeeded; used for GET, PUT, PATCH, DELETE responses.

2. **When should you use 201 Created?** - When a new resource is successfully created via POST.

3. **What is the difference between 400 and 422?** - 400: Malformed request; 422: Well-formed but semantically invalid.

4. **When to use 404 vs 410?** - 404: Resource not found (may exist later); 410: Resource permanently removed.

5. **What does 500 indicate?** - Internal server error; unexpected condition on the server.

### Intermediate (5)

6. **Explain 401 vs 403** - 401: Authentication required (provide credentials); 403: Authenticated but not authorized (insufficient permissions).

7. **When to use 304 Not Modified?** - When client has cached version; save bandwidth by not sending body.

8. **What is Retry-After header?** - Tells client how long to wait before retrying; used with 429 and 503.

9. **How do you handle 502 Bad Gateway?** - Implement circuit breaker, fallback responses, retry with backoff.

10. **When to use 202 Accepted?** - For async operations; request accepted but processing not complete.

### Senior (10)

11. **Design error response format** - Consistent JSON structure with error code, message, details, request ID.

12. **How do you version error responses?** - Include API version in error response, evolve error format carefully.

13. **Handle partial failures in batch operations** - Return 207 Multi-Status with per-item results.

14. **Design rate limiting with 429** - Include rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After).

15. **Implement graceful degradation** - Return 503 with Retry-After during maintenance, serve cached responses.

16. **Handle idempotency with status codes** - Return 409 Conflict for duplicate idempotency keys.

17. **Design webhook retry logic** - Use exponential backoff, dead letter queue after max retries.

18. **Handle CORS preflight failures** - Return appropriate 4xx codes, document required headers.

19. **Implement request validation** - Return 400 for malformed, 422 for validation errors with details.

20. **Design monitoring for status codes** - Track error rates, set up alerts for 5xx spikes.

### FAANG-style (5)

21. **Design a globally distributed API error handling** - Consistent errors across regions, failover handling.

22. **Handle cascading failures** - Circuit breaker pattern, bulkhead isolation, fallback responses.

23. **Design error budget system** - Track SLO compliance, alert on error rate thresholds.

24. **Implement chaos engineering for error handling** - Test 5xx scenarios, verify graceful degradation.

25. **Design API error analytics pipeline** - Aggregate errors, pattern detection, automated alerting.

### Follow-ups (5)

26. **How do you test status code handling?** - Unit tests for each code, integration tests for error flows.

27. **What are common status code mistakes?** - Using 200 for errors, exposing internals, missing headers.

28. **How do status codes affect caching?** - 2xx cacheable, 3xx redirect caching, 4xx/5xx typically not cached.

29. **How do proxies handle status codes?** - May cache, transform, or retry based on code and headers.

30. **How do browsers handle different status codes?** - 3xx: follow redirect, 4xx: show error, 5xx: retry or error page.

## Summary

HTTP status codes are essential for communicating request outcomes between client and server. Using appropriate status codes makes APIs predictable, debuggable, and standards-compliant. Always use the correct class (2xx for success, 4xx for client errors, 5xx for server errors) and include relevant headers like Location, Retry-After, and Allow.

## Cheat Sheet

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 202 | Accepted | Async operation accepted |
| 204 | No Content | Successful DELETE |
| 301 | Moved Permanently | URL changed permanently |
| 304 | Not Modified | Cached version valid |
| 400 | Bad Request | Malformed request |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Unexpected failure |
| 502 | Bad Gateway | Upstream error |
| 503 | Service Unavailable | Temporarily down |

## References & Learn More

- [HTTP Status Codes - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [HTTP Status Code Definitions](https://httpstatuses.com/)
- [RFC 8610 - HTTP Status Code Registry](https://www.iana.org/assignments/http-status-codes/)
- [Which HTTP Status Code To Use - DigitalOcean](https://www.digitalocean.com/community/tutorials/which-http-status-code-to-use)
- [HTTP/1.1 Status Code Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)
