# HTTP Methods

## Definition

HTTP methods (also called HTTP verbs) define the action to be performed on a resource. Each method has specific semantics regarding safety, idempotency, and whether it allows a request body. Understanding these properties is crucial for designing correct and predictable REST APIs.

## Why Do We Need It?

HTTP methods provide a standardized way to interact with resources:

1. **Predictability** - Developers know what each method does
2. **Cacheability** - Browsers and proxies can optimize based on method
3. **Security** - Safe methods don't modify server state
4. **Reliability** - Idempotent methods can be safely retried
5. **Tooling** - HTTP clients can optimize behavior per method

## How It Works

### Method Properties

```
HTTP Method Properties
══════════════════════

Method    Safe    Idempotent    Has Body    Cacheable
──────────────────────────────────────────────────────
GET       Yes     Yes           No          Yes
HEAD      Yes     Yes           No          Yes
OPTIONS   Yes     Yes           Optional    No
POST      No      No            Yes         Conditional
PUT       No      Yes           Yes         No
PATCH     No      Yes*          Yes         No
DELETE    No      Yes           Optional    No

* PATCH is idempotent when the patch document itself is idempotent
```

### Detailed Method Specifications

#### GET - Retrieve Resource

```
GET Request Flow
════════════════

Client                          Server
  │                               │
  │  GET /api/users/123           │
  │  Accept: application/json     │
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  Content-Type: application/json│
  │  Cache-Control: max-age=3600  │
  │  ETag: "abc123"              │
  │  { "data": { ... } }         │
  │◄──────────────────────────────│
```

```typescript
// GET - Safe and Idempotent
// No side effects, can be cached, can be retried safely

app.get('/api/users', async (req, res) => {
  const { page = 1, limit = 10, sort = 'createdAt' } = req.query;
  const users = await UserService.findAll({ page, limit, sort });
  const total = await UserService.count();
  
  res.json({
    data: users,
    pagination: { page, limit, total }
  });
});

app.get('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json({ data: user });
});
```

#### POST - Create Resource

```
POST Request Flow
═════════════════

Client                          Server
  │                               │
  │  POST /api/users              │
  │  Content-Type: application/json│
  │  Body: { name, email }        │
  │──────────────────────────────►│
  │                               │
  │  201 Created                  │
  │  Location: /api/users/123     │
  │  { "data": { "id": "123" } } │
  │◄──────────────────────────────│
```

```typescript
// POST - Not Safe, Not Idempotent
// Creates new resources, generates unique IDs

app.post('/api/users', async (req, res) => {
  const { name, email } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required' });
  }
  
  const existingUser = await UserService.findByEmail(email);
  if (existingUser) {
    return res.status(409).json({ error: 'Email already exists' });
  }
  
  const user = await UserService.create({ name, email });
  
  res.status(201)
    .header('Location', `/api/users/${user.id}`)
    .json({ data: user });
});

// POST is not idempotent - each request creates a new resource
app.post('/api/orders', async (req, res) => {
  const order = await OrderService.create(req.body);
  res.status(201).json({ data: order });
});
```

#### PUT - Replace Resource

```
PUT Request Flow
════════════════

Client                          Server
  │                               │
  │  PUT /api/users/123           │
  │  Content-Type: application/json│
  │  Body: { name, email }        │
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  { "data": { "id": "123" } } │
  │◄──────────────────────────────│
```

```typescript
// PUT - Not Safe, Idempotent
// Replaces entire resource, same request = same result

app.put('/api/users/:id', async (req, res) => {
  const { name, email } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required' });
  }
  
  const existingUser = await UserService.findById(req.params.id);
  if (!existingUser) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  const updatedUser = await UserService.replace(req.params.id, { name, email });
  res.json({ data: updatedUser });
});

// PUT is idempotent - calling multiple times produces same result
// First call: creates/updates user
// Second call: same result (user already has those values)
```

#### PATCH - Partial Update

```
PATCH Request Flow
══════════════════

Client                          Server
  │                               │
  │  PATCH /api/users/123         │
  │  Content-Type: application/json│
  │  Body: { email: "new@..." }   │
  │──────────────────────────────►│
  │                               │
  │  200 OK                       │
  │  { "data": { "id": "123" } } │
  │◄──────────────────────────────│
```

```typescript
// PATCH - Not Safe, Can be Idempotent
// Updates specific fields only

app.patch('/api/users/:id', async (req, res) => {
  const existingUser = await UserService.findById(req.params.id);
  if (!existingUser) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  // Only update provided fields
  const allowedFields = ['name', 'email', 'profile'];
  const updates: Partial<User> = {};
  
  for (const field of allowedFields) {
    if (req.body[field] !== undefined) {
      updates[field] = req.body[field];
    }
  }
  
  const updatedUser = await UserService.update(req.params.id, updates);
  res.json({ data: updatedUser });
});

// PATCH with JSON Patch (RFC 6902)
app.patch('/api/users/:id', async (req, res) => {
  if (req.headers['content-type'] === 'application/json-patch+json') {
    const user = await UserService.findById(req.params.id);
    const patchedUser = applyJsonPatch(user, req.body);
    await UserService.update(req.params.id, patchedUser);
    return res.json({ data: patchedUser });
  }
  // Regular partial update
  const updatedUser = await UserService.update(req.params.id, req.body);
  res.json({ data: updatedUser });
});
```

#### DELETE - Remove Resource

```
DELETE Request Flow
═══════════════════

Client                          Server
  │                               │
  │  DELETE /api/users/123        │
  │──────────────────────────────►│
  │                               │
  │  204 No Content               │
  │◄──────────────────────────────│
```

```typescript
// DELETE - Not Safe, Idempotent
// Removes resource, can be retried safely

app.delete('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  await UserService.delete(req.params.id);
  res.status(204).end();
});

// DELETE is idempotent - calling multiple times:
// First call: deletes user, returns 204
// Second call: user not found, returns 404 (but no state change)
```

#### HEAD - Get Metadata Only

```typescript
// HEAD - Safe, Idempotent
// Same as GET but returns only headers (no body)

app.head('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) {
    return res.status(404).end();
  }
  
  res.set({
    'Content-Type': 'application/json',
    'X-User-Exists': 'true',
    'X-User-Name': user.name
  });
  res.status(200).end();
});
```

#### OPTIONS - Get Allowed Methods

```typescript
// OPTIONS - Safe, Idempotent
// Returns allowed methods for a resource (used in CORS preflight)

app.options('/api/users', (req, res) => {
  res.set({
    'Allow': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.status(200).end();
});

app.options('/api/users/:id', (req, res) => {
  res.set({
    'Allow': 'GET, PUT, PATCH, DELETE, OPTIONS',
    'Access-Control-Allow-Methods': 'GET, PUT, PATCH, DELETE, OPTIONS'
  });
  res.status(200).end();
});
```

### Idempotency Deep Dive

```
Idempotency Examples
════════════════════

GET /api/users/123
  Request 1: Returns user 123
  Request 2: Returns same user 123
  Request 3: Returns same user 123
  Result: ✅ Idempotent (same result each time)

POST /api/users
  Request 1: Creates user, returns 201
  Request 2: Creates ANOTHER user, returns 201
  Request 3: Creates ANOTHER user, returns 201
  Result: ❌ Not Idempotent (different result each time)

PUT /api/users/123
  Request 1: Updates user, returns 200
  Request 2: Same update, returns 200 (no change)
  Request 3: Same update, returns 200 (no change)
  Result: ✅ Idempotent (same final state)

DELETE /api/users/123
  Request 1: Deletes user, returns 204
  Request 2: User already deleted, returns 404
  Request 3: User already deleted, returns 404
  Result: ✅ Idempotent (same final state - user deleted)
```

## Code Examples

### Complete Method Router

```typescript
import express from 'express';
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();
const users = new Map<string, User>();

// GET - List all users
router.get('/', async (req, res) => {
  const { page = '1', limit = '10' } = req.query;
  const userList = Array.from(users.values());
  const start = (parseInt(page as string) - 1) * parseInt(limit as string);
  const paginatedUsers = userList.slice(start, start + parseInt(limit as string));
  
  res.json({
    data: paginatedUsers,
    pagination: {
      page: parseInt(page as string),
      limit: parseInt(limit as string),
      total: userList.length
    }
  });
});

// GET - Get user by ID
router.get('/:id', async (req, res) => {
  const user = users.get(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({ data: user });
});

// HEAD - Check if user exists
router.head('/:id', async (req, res) => {
  const user = users.get(req.params.id);
  if (!user) {
    return res.status(404).end();
  }
  res.set({ 'Content-Type': 'application/json' });
  res.status(200).end();
});

// POST - Create new user
router.post('/', async (req, res) => {
  const { name, email } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({
      error: 'Validation failed',
      details: { name: !name ? 'Required' : undefined, email: !email ? 'Required' : undefined }
    });
  }
  
  const existingUser = Array.from(users.values()).find(u => u.email === email);
  if (existingUser) {
    return res.status(409).json({ error: 'Email already exists' });
  }
  
  const newUser: User = {
    id: uuidv4(),
    name,
    email,
    createdAt: new Date(),
    updatedAt: new Date()
  };
  
  users.set(newUser.id, newUser);
  
  res.status(201)
    .header('Location', `/api/users/${newUser.id}`)
    .json({ data: newUser });
});

// PUT - Replace user (full update)
router.put('/:id', async (req, res) => {
  const { name, email } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required for PUT' });
  }
  
  const existingUser = users.get(req.params.id);
  if (!existingUser) {
    // PUT can create resource if it doesn't exist
    const newUser: User = {
      id: req.params.id,
      name,
      email,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    users.set(req.params.id, newUser);
    return res.status(201).header('Location', `/api/users/${newUser.id}`).json({ data: newUser });
  }
  
  const updatedUser: User = {
    ...existingUser,
    name,
    email,
    updatedAt: new Date()
  };
  
  users.set(req.params.id, updatedUser);
  res.json({ data: updatedUser });
});

// PATCH - Partial update
router.patch('/:id', async (req, res) => {
  const existingUser = users.get(req.params.id);
  if (!existingUser) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  const allowedFields = ['name', 'email'];
  const updates: Partial<User> = {};
  
  for (const field of allowedFields) {
    if (req.body[field] !== undefined) {
      updates[field] = req.body[field];
    }
  }
  
  const updatedUser: User = {
    ...existingUser,
    ...updates,
    id: existingUser.id,
    createdAt: existingUser.createdAt,
    updatedAt: new Date()
  };
  
  users.set(req.params.id, updatedUser);
  res.json({ data: updatedUser });
});

// DELETE - Remove user
router.delete('/:id', async (req, res) => {
  const user = users.get(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  users.delete(req.params.id);
  res.status(204).end();
});

// OPTIONS - Get allowed methods
router.options('/', (req, res) => {
  res.set({ 'Allow': 'GET, POST, OPTIONS' });
  res.status(200).end();
});

router.options('/:id', (req, res) => {
  res.set({ 'Allow': 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS' });
  res.status(200).end();
});

app.use('/api/users', router);
```

### Idempotency Key Implementation

```typescript
// For non-idempotent operations (POST), use idempotency keys
const idempotencyKeys = new Map<string, { result: any; timestamp: Date }>();

app.post('/api/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'] as string;
  
  if (!idempotencyKey) {
    return res.status(400).json({ error: 'Idempotency-Key header required' });
  }
  
  // Check if we've seen this key before
  const existingResult = idempotencyKeys.get(idempotencyKey);
  if (existingResult) {
    // Return cached response (idempotent behavior)
    return res.json(existingResult.result);
  }
  
  // Process the payment
  const payment = await PaymentService.create(req.body);
  
  // Store the result with the idempotency key
  idempotencyKeys.set(idempotencyKey, {
    result: { data: payment },
    timestamp: new Date()
  });
  
  // Clean up old keys (TTL: 24 hours)
  setTimeout(() => {
    idempotencyKeys.delete(idempotencyKey);
  }, 24 * 60 * 60 * 1000);
  
  res.status(201).json({ data: payment });
});
```

## Real-World Use Cases

### 1. E-commerce Order Processing

```typescript
// GET - View orders (safe, idempotent)
router.get('/orders', authenticate, async (req, res) => {
  const orders = await OrderService.findByUser(req.user.id);
  res.json({ data: orders });
});

// POST - Create order (not idempotent - use idempotency key)
router.post('/orders', authenticate, async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];
  const existingOrder = await OrderService.findByIdempotencyKey(idempotencyKey);
  if (existingOrder) return res.json({ data: existingOrder });
  
  const order = await OrderService.create({ userId: req.user.id, ...req.body });
  res.status(201).json({ data: order });
});

// PUT - Replace entire order (idempotent)
router.put('/orders/:id', authenticate, async (req, res) => {
  const order = await OrderService.replace(req.params.id, req.body);
  res.json({ data: order });
});

// PATCH - Update order status (idempotent)
router.patch('/orders/:id/status', authenticate, async (req, res) => {
  const order = await OrderService.updateStatus(req.params.id, req.body.status);
  res.json({ data: order });
});

// DELETE - Cancel order (idempotent)
router.delete('/orders/:id', authenticate, async (req, res) => {
  await OrderService.cancel(req.params.id);
  res.status(204).end();
});
```

### 2. File Upload/Download

```typescript
// GET - Download file (safe, idempotent)
router.get('/files/:id/download', async (req, res) => {
  const file = await FileService.findById(req.params.id);
  if (!file) return res.status(404).json({ error: 'File not found' });
  
  res.set({
    'Content-Type': file.mimeType,
    'Content-Disposition': `attachment; filename="${file.name}"`,
    'Content-Length': file.size
  });
  
  const stream = await FileService.getStream(file.id);
  stream.pipe(res);
});

// POST - Upload file (not idempotent)
router.post('/files', authenticate, upload.single('file'), async (req, res) => {
  const file = await FileService.create({
    name: req.file.originalname,
    mimeType: req.file.mimetype,
    size: req.file.size,
    userId: req.user.id
  });
  
  res.status(201).json({ data: file });
});

// HEAD - Check file metadata (safe, idempotent)
router.head('/files/:id', async (req, res) => {
  const file = await FileService.findById(req.params.id);
  if (!file) return res.status(404).end();
  
  res.set({
    'Content-Type': file.mimeType,
    'Content-Length': file.size,
    'Last-Modified': file.updatedAt.toUTCString()
  });
  res.status(200).end();
});
```

### 3. Real-time Notifications

```typescript
// GET - Poll for notifications (safe, idempotent)
router.get('/notifications', authenticate, async (req, res) => {
  const { since } = req.query;
  const notifications = await NotificationService.findSince(req.user.id, since as string);
  
  res.json({
    data: notifications,
    _links: {
      self: `/api/notifications?since=${since || ''}`,
      markAllRead: '/api/notifications/read'
    }
  });
});

// PATCH - Mark notification as read (idempotent)
router.patch('/notifications/:id/read', authenticate, async (req, res) => {
  const notification = await NotificationService.markAsRead(req.params.id, req.user.id);
  res.json({ data: notification });
});

// POST - Send notification (not idempotent)
router.post('/notifications', authenticate, async (req, res) => {
  const notification = await NotificationService.create({
    ...req.body,
    senderId: req.user.id
  });
  res.status(201).json({ data: notification });
});
```

## Common Mistakes

### 1. Using GET for Mutations

```typescript
// ❌ Bad: Using GET to modify state
router.get('/api/users/:id/delete', async (req, res) => {
  await UserService.delete(req.params.id);
  res.json({ message: 'Deleted' });
});

// ✅ Good: Use DELETE method
router.delete('/api/users/:id', async (req, res) => {
  await UserService.delete(req.params.id);
  res.status(204).end();
});
```

### 2. Not Handling Idempotency Correctly

```typescript
// ❌ Bad: POST without idempotency handling
router.post('/api/payments', async (req, res) => {
  const payment = await PaymentService.create(req.body);
  res.status(201).json({ data: payment });
});

// ✅ Good: POST with idempotency key
router.post('/api/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];
  const existing = await PaymentService.findByIdempotencyKey(idempotencyKey);
  if (existing) return res.json({ data: existing });
  
  const payment = await PaymentService.create({ ...req.body, idempotencyKey });
  res.status(201).json({ data: payment });
});
```

### 3. Wrong Status Codes

```typescript
// ❌ Bad
router.post('/api/users', async (req, res) => {
  const user = await UserService.create(req.body);
  res.json({ data: user });  // Should be 201
});

// ✅ Good
router.post('/api/users', async (req, res) => {
  const user = await UserService.create(req.body);
  res.status(201).header('Location', `/api/users/${user.id}`).json({ data: user });
});
```

### 4. Missing Validation

```typescript
// ❌ Bad: No input validation
router.put('/api/users/:id', async (req, res) => {
  const user = await UserService.replace(req.params.id, req.body);
  res.json({ data: user });
});

// ✅ Good: Validate required fields for PUT
router.put('/api/users/:id', async (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required for PUT' });
  }
  const user = await UserService.replace(req.params.id, { name, email });
  res.json({ data: user });
});
```

## Best Practices

1. **Use GET for reads** - Never modify data with GET
2. **Use POST for creation** - New resources, non-idempotent operations
3. **Use PUT for full replacement** - All fields required, idempotent
4. **Use PATCH for partial updates** - Only changed fields, can be idempotent
5. **Use DELETE for removal** - Idempotent, safe to retry
6. **Implement idempotency keys** - For POST requests in critical systems
7. **Return proper status codes** - 200, 201, 204, 400, 404, etc.
8. **Use Location header** - For POST responses with created resources
9. **Support HEAD** - For checking resource existence without body
10. **Document allowed methods** - Use OPTIONS and Allow headers

## Performance Considerations

- **GET caching** - Leverage browser and CDN caching with proper headers
- **Conditional requests** - Use ETag and If-None-Match to avoid unnecessary data transfer
- **Bulk operations** - Consider POST for batch deletes instead of multiple DELETE requests
- **Compression** - Enable gzip for GET responses
- **Pagination** - Always paginate large collections

## Interview Questions

### Beginner (5)

1. **What is the difference between GET and POST?** - GET retrieves data (safe, idempotent); POST creates data (not safe, not idempotent).

2. **When should you use PUT vs PATCH?** - PUT for full resource replacement; PATCH for partial updates.

3. **What makes DELETE idempotent?** - Calling DELETE multiple times produces the same result (resource is deleted or already gone).

4. **What is the purpose of HEAD method?** - Same as GET but returns only headers, useful for checking if resource exists.

5. **What status code should POST return?** - 201 Created with Location header.

### Intermediate (5)

6. **Explain idempotency and why it matters** - Idempotent operations produce same result when called multiple times; important for retry logic and fault tolerance.

7. **When would you use OPTIONS method?** - CORS preflight requests, discovering allowed methods for a resource.

8. **How do you handle concurrent PUT requests?** - Use optimistic locking with ETag/If-Match headers.

9. **What is the difference between 400 and 422 status codes?** - 400: Malformed request; 422: Request well-formed but semantically invalid.

10. **How do you implement idempotency for POST?** - Use Idempotency-Key header and store results server-side.

### Senior (10)

11. **Design an idempotent payment system** - Idempotency keys, idempotent database operations, retry-safe webhooks.

12. **How do you handle PATCH with JSON Patch?** - Implement RFC 6902 for standard patch operations.

13. **Design a bulk operations API** - POST for batch create, DELETE for batch remove, progress tracking.

14. **How do you version HTTP methods?** - Deprecation headers, method routing, backward compatibility.

15. **Implement optimistic concurrency control** - ETag headers, If-Match conditional updates.

16. **Design a retry-safe notification system** - Idempotency keys, deduplication, exactly-once semantics.

17. **How do you handle long-running PUT operations?** - Return 202 Accepted with status polling endpoint.

18. **Design a soft-delete system with DELETE** - Mark as deleted, purge after retention period.

19. **How do you handle partial failures in batch operations?** - Transaction rollback, partial success responses, error aggregation.

20. **Implement cache invalidation with methods** - ETag generation, Cache-Control headers, purge strategies.

### FAANG-style (5)

21. **Design a distributed counter with idempotent increments** - CRDT, vector clocks, conflict resolution.

22. **Design a shopping cart API with concurrent updates** - Merge strategies, version vectors, conflict detection.

23. **Design a document collaboration system** - OT/CRDT, operation transforms, conflict resolution.

24. **How would you migrate from POST to PUT without downtime?** - Dual-write, feature flags, gradual migration.

25. **Design a webhook delivery system with retries** - Idempotency, exponential backoff, dead letter queue.

### Follow-ups (5)

26. **What are the limitations of idempotency keys?** - Storage overhead, TTL management, key generation strategies.

27. **When would you NOT use idempotency?** - Logging, analytics, non-critical metrics.

28. **How do you test idempotency?** - Send same request twice, verify same response, check database state.

29. **What is exactly-once delivery?** - Guarantees message processed once despite retries; requires idempotency.

30. **How do you handle idempotency across microservices?** - Distributed idempotency stores, correlation IDs, saga patterns.

## Summary

HTTP methods are the foundation of REST API design. Each method has specific properties—safe, idempotent, cacheable—that determine how it should be used. Understanding these properties is crucial for building reliable, fault-tolerant APIs. Always use the correct method for the operation, implement idempotency for critical operations, and return appropriate status codes.

## Cheat Sheet

| Method | Safe | Idempotent | Has Body | Cacheable | Use Case |
|--------|------|------------|----------|-----------|----------|
| GET | Yes | Yes | No | Yes | Read resource |
| POST | No | No | Yes | Conditional | Create resource |
| PUT | No | Yes | Yes | No | Replace resource |
| PATCH | No | Yes* | Yes | No | Partial update |
| DELETE | No | Yes | Optional | No | Remove resource |
| HEAD | Yes | Yes | No | Yes | Get metadata |
| OPTIONS | Yes | Yes | Optional | No | Get allowed methods |

## References & Learn More

- [RFC 7231 - HTTP/1.1 Semantics and Content](https://tools.ietf.org/html/rfc7231)
- [MDN HTTP Methods Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [Idempotency in REST APIs](https://restfulapi.net/idempotent-rest-api/)
- [RFC 8297 - HTTP Status Code 103 (Early Hints)](https://tools.ietf.org/html/rfc8297)
- [Stripe Idempotency Keys](https://stripe.com/blog/idempotency)
