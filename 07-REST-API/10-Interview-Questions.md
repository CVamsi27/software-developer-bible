# REST API Interview Questions

## Definition

This comprehensive guide covers the most frequently asked REST API interview questions, organized by difficulty level. Each question includes detailed answers, code examples, and follow-up questions to help you prepare for senior full-stack developer interviews.

## Why Do We Need It?

REST API design is a critical skill for full-stack developers. Interviewers test:

1. **Fundamental knowledge** - HTTP methods, status codes, resource design
2. **Architecture decisions** - Versioning, pagination, authentication
3. **Security awareness** - CORS, rate limiting, input validation
4. **Scalability thinking** - Caching, load balancing, microservices
5. **Real-world experience** - Common pitfalls, best practices, tradeoffs

## How It Works

### Interview Format

```
REST API Interview Structure
════════════════════════════

1. Conceptual Questions (10-15 min)
   - What is REST?
   - Explain HTTP methods
   - Status codes usage

2. Design Questions (20-30 min)
   - Design a URL shortener API
   - Design a social media feed
   - Design a payment system

3. Implementation Questions (15-20 min)
   - Code a rate limiter
   - Implement pagination
   - Design authentication

4. Architecture Questions (15-20 min)
   - Microservices API design
   - API gateway patterns
   - Caching strategies

5. Tradeoff Questions (10-15 min)
   - REST vs GraphQL
   - Pagination strategies
   - Authentication methods
```

## Code Examples

### Question 1: What is REST?

**Answer:**

REST (Representational State Transfer) is an architectural style for designing networked applications. It uses standard HTTP methods and resource-based URLs.

**Key constraints:**
1. **Client-Server** - Separation of concerns
2. **Stateless** - No server-side session
3. **Cacheable** - Responses can be cached
4. **Uniform Interface** - Consistent resource identification
5. **Layered System** - Client can't tell if connected directly to server
6. **Code on Demand** - Optional executable code

```typescript
// Example RESTful API
app.get('/api/users', async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

app.post('/api/users', async (req, res) => {
  const user = await UserService.create(req.body);
  res.status(201).json({ data: user });
});
```

### Question 2: What is the difference between PUT and PATCH?

**Answer:**

| Aspect | PUT | PATCH |
|--------|-----|-------|
| Purpose | Replace entire resource | Partial update |
| Body | Complete resource | Only changed fields |
| Idempotent | Yes | Can be |
| Response | 200 OK | 200 OK |
| Location header | Optional | No |

```typescript
// PUT - Replace entire user
app.put('/api/users/:id', async (req, res) => {
  const { name, email, phone, address } = req.body;
  // All fields required
  const user = await UserService.replace(req.params.id, {
    name, email, phone, address
  });
  res.json({ data: user });
});

// PATCH - Update specific fields
app.patch('/api/users/:id', async (req, res) => {
  const user = await UserService.update(req.params.id, req.body);
  // Only provided fields updated
  res.json({ data: user });
});
```

### Question 3: Design a URL Shortener API

**Answer:**

```
URL Shortener API Design
════════════════════════

Endpoints:
  POST   /api/shorten         - Create short URL
  GET    /:shortCode          - Redirect to original URL
  GET    /api/urls/:shortCode - Get URL stats
  DELETE /api/urls/:shortCode - Delete short URL

Data Model:
  {
    id: string,
    shortCode: string,
    originalUrl: string,
    createdAt: Date,
    clicks: number,
    userId: string
  }

Rate Limits:
  - 10 URLs per minute for free tier
  - 100 URLs per minute for pro tier

Caching:
  - Cache redirect mappings in Redis
  - TTL: 24 hours
```

```typescript
// URL Shortener Implementation
import { nanoid } from 'nanoid';

app.post('/api/shorten', authenticate, rateLimiter({ max: 10, windowMs: 60000 }), async (req, res) => {
  const { url, customCode } = req.body;
  
  // Validate URL
  if (!isValidUrl(url)) {
    return res.status(400).json({ error: 'Invalid URL' });
  }
  
  // Check if URL already exists
  const existing = await UrlService.findByOriginal(url, req.user.id);
  if (existing) {
    return res.json({ data: existing });
  }
  
  // Generate or validate custom code
  const shortCode = customCode || nanoid(7);
  
  if (customCode) {
    const exists = await UrlService.findByCode(customCode);
    if (exists) {
      return res.status(409).json({ error: 'Short code already exists' });
    }
  }
  
  // Create short URL
  const shortUrl = await UrlService.create({
    shortCode,
    originalUrl: url,
    userId: req.user.id
  });
  
  // Cache in Redis
  await redis.setex(`url:${shortCode}`, 86400, url);
  
  res.status(201).json({
    data: {
      shortCode,
      shortUrl: `${process.env.BASE_URL}/${shortCode}`,
      originalUrl: url
    }
  });
});

// Redirect endpoint
app.get('/:shortCode', async (req, res) => {
  const { shortCode } = req.params;
  
  // Check cache first
  let originalUrl = await redis.get(`url:${shortCode}`);
  
  if (!originalUrl) {
    // Cache miss, fetch from database
    const url = await UrlService.findByCode(shortCode);
    if (!url) {
      return res.status(404).json({ error: 'Short URL not found' });
    }
    originalUrl = url.originalUrl;
    
    // Cache for next time
    await redis.setex(`url:${shortCode}`, 86400, originalUrl);
  }
  
  // Track click asynchronously
  UrlService.trackClick(shortCode, {
    ip: req.ip,
    userAgent: req.headers['user-agent'],
    referer: req.headers['referer']
  });
  
  // Redirect
  res.redirect(301, originalUrl);
});
```

### Question 4: How do you implement pagination?

**Answer:**

```
Pagination Strategies
═════════════════════

1. Offset-Based (Traditional)
   GET /api/users?page=3&limit=10
   - Simple, supports random access
   - Inefficient for large offsets

2. Cursor-Based (Recommended)
   GET /api/users?cursor=abc123&limit=10
   - Efficient for large datasets
   - Stable under concurrent changes

3. Keyset-Based
   GET /api/users?createdAfter=2024-01-01&limit=10
   - Good for time-series data
   - Natural ordering
```

```typescript
// Cursor-based pagination
app.get('/api/users', async (req, res) => {
  const { cursor, limit = '10' } = req.query;
  const limitNum = Math.min(100, parseInt(limit as string));
  
  let whereClause = {};
  if (cursor) {
    const decoded = JSON.parse(Buffer.from(cursor, 'base64').toString());
    whereClause = { id: { $gt: decoded.id } };
  }
  
  const users = await UserService.findAll({
    where: whereClause,
    limit: limitNum + 1,
    order: [['id', 'ASC']]
  });
  
  const hasMore = users.length > limitNum;
  const data = hasMore ? users.slice(0, limitNum) : users;
  const nextCursor = hasMore
    ? Buffer.from(JSON.stringify({ id: data[data.length - 1].id })).toString('base64')
    : null;
  
  res.json({
    data,
    pagination: { hasMore, nextCursor }
  });
});
```

### Question 5: Explain CORS and why it matters

**Answer:**

CORS (Cross-Origin Resource Sharing) is a security mechanism that restricts web pages from making requests to a different origin.

```
CORS Flow
═════════

Browser                    Server
  │  OPTIONS /api/data       │
  │  Origin: https://app.com │
  │─────────────────────────►│
  │                          │
  │  204 No Content          │
  │  Access-Control-Allow-   │
  │  Origin: https://app.com │
  │◄─────────────────────────│
  │                          │
  │  POST /api/data          │
  │  Origin: https://app.com │
  │─────────────────────────►│
```

```typescript
// CORS configuration
app.use(cors({
  origin: 'https://app.com',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400
}));
```

### Question 6: How do you implement rate limiting?

**Answer:**

```typescript
// Token bucket algorithm
class TokenBucket {
  private tokens: number;
  private lastRefill: number;
  
  constructor(
    private capacity: number,
    private refillRate: number
  ) {
    this.tokens = capacity;
    this.lastRefill = Date.now();
  }
  
  consume(): boolean {
    this.refill();
    if (this.tokens >= 1) {
      this.tokens--;
      return true;
    }
    return false;
  }
  
  private refill() {
    const now = Date.now();
    const elapsed = now - this.lastRefill;
    const tokensToAdd = (elapsed / 1000) * this.refillRate;
    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }
}

// Rate limiter middleware
function rateLimiter(maxRequests: number, windowMs: number) {
  const buckets = new Map<string, TokenBucket>();
  
  return (req, res, next) => {
    const key = req.user?.id || req.ip;
    let bucket = buckets.get(key);
    
    if (!bucket) {
      bucket = new TokenBucket(maxRequests, maxRequests / (windowMs / 1000));
      buckets.set(key, bucket);
    }
    
    if (!bucket.consume()) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    next();
  };
}
```

### Question 7: Design authentication for a REST API

**Answer:**

```
JWT Authentication Flow
═══════════════════════

Client                    Server
  │  POST /api/auth/login  │
  │  { email, password }   │
  │───────────────────────►│
  │                        │
  │  200 OK                │
  │  { token, refreshToken }│
  │◄───────────────────────│
  │                        │
  │  GET /api/users        │
  │  Authorization: Bearer │
  │  eyJhbG...             │
  │───────────────────────►│
  │                        │
  │  200 OK                │
  │  { data: [...] }      │
  │◄───────────────────────│
```

```typescript
// JWT implementation
import jwt from 'jsonwebtoken';

const generateToken = (user) => {
  return jwt.sign(
    { sub: user.id, email: user.email, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
};

const authenticate = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Usage
app.get('/api/users', authenticate, async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});
```

### Question 8: What is HATEOAS and why is it important?

**Answer:**

HATEOAS (Hypermedia as the Engine of Application State) means responses include links that guide the client on available actions.

```typescript
// Without HATEOAS
res.json({
  id: 123,
  name: 'Order #123',
  status: 'pending'
});

// With HATEOAS
res.json({
  id: 123,
  name: 'Order #123',
  status: 'pending',
  _links: {
    self: '/api/orders/123',
    cancel: '/api/orders/123/cancel',
    pay: '/api/orders/123/pay',
    items: '/api/orders/123/items'
  }
});
```

Benefits:
1. **Discoverability** - Client can discover available actions
2. **Loose coupling** - Client doesn't need to hardcode URLs
3. **Evolvability** - Server can change URLs without breaking client

### Question 9: How do you handle API versioning?

**Answer:**

```
Versioning Strategies
═════════════════════

1. URL Path (Recommended)
   GET /api/v1/users
   GET /api/v2/users

2. Query Parameter
   GET /api/users?version=1

3. Header
   GET /api/users
   Accept: application/vnd.api.v1+json
```

```typescript
// URL-based versioning
const v1Router = express.Router();
const v2Router = express.Router();

// V1: Basic response
v1Router.get('/users', async (req, res) => {
  const users = await UserService.findAll();
  res.json({ data: users });
});

// V2: With pagination metadata
v2Router.get('/users', async (req, res) => {
  const { page, limit } = req.query;
  const users = await UserService.findAll({ page, limit });
  const total = await UserService.count();
  
  res.json({
    data: users,
    pagination: { page, limit, total }
  });
});

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

### Question 10: Design a REST API for a social media feed

**Answer:**

```
Social Media Feed API
═════════════════════

Endpoints:
  GET    /api/feed              - Get personalized feed
  GET    /api/posts             - List all posts
  POST   /api/posts             - Create post
  GET    /api/posts/:id         - Get post details
  DELETE /api/posts/:id         - Delete post
  POST   /api/posts/:id/like    - Like post
  POST   /api/posts/:id/comment - Add comment

Features:
  - Infinite scroll (cursor pagination)
  - Real-time updates (WebSocket)
  - Feed ranking algorithm
  - Media upload support
```

```typescript
// Feed endpoint with cursor pagination
app.get('/api/feed', authenticate, async (req, res) => {
  const { cursor, limit = '20' } = req.query;
  
  const feed = await FeedService.getPersonalized(req.user.id, {
    cursor,
    limit: parseInt(limit as string)
  });
  
  res.json({
    data: feed,
    pagination: {
      hasMore: feed.length === parseInt(limit as string),
      nextCursor: feed.length === parseInt(limit as string)
        ? feed[feed.length - 1].id
        : null
    }
  });
});

// Create post with media upload
app.post('/api/posts', authenticate, upload.single('media'), async (req, res) => {
  const { content } = req.body;
  const mediaUrl = req.file ? await uploadToS3(req.file) : null;
  
  const post = await PostService.create({
    userId: req.user.id,
    content,
    mediaUrl
  });
  
  // Invalidate feed cache
  await cache.invalidate(`feed:${req.user.id}`);
  
  res.status(201).json({ data: post });
});
```

## Interview Questions

### Beginner (10)

1. **What is REST?**
   REST is an architectural style for designing networked applications using standard HTTP methods and resource-based URLs.

2. **What are the HTTP methods?**
   GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove), HEAD (metadata), OPTIONS (allowed methods).

3. **What is a resource in REST?**
   A resource is any concept that can be identified and named, accessed via URIs (e.g., /api/users, /api/products).

4. **What is idempotency?**
   A property where making the same request multiple times produces the same result. GET, PUT, DELETE are idempotent.

5. **What are the main HTTP status code classes?**
   1xx (informational), 2xx (success), 3xx (redirection), 4xx (client error), 5xx (server error).

6. **What is the difference between 401 and 403?**
   401: Authentication required; 403: Authenticated but insufficient permissions.

7. **What is a URI?**
   Uniform Resource Identifier; a string that identifies a resource (e.g., /api/users/123).

8. **What is content negotiation?**
   Client and server agreeing on response format via Accept/Content-Type headers.

9. **Why use plural nouns in URIs?**
   Consistency and clarity; /api/users represents a collection of user resources.

10. **What is a stateless API?**
    An API where each request contains all information needed; server stores no client context between requests.

### Intermediate (10)

11. **Explain HATEOAS**
    Hypermedia as the Engine of Application State; responses include links for discoverability and available actions.

12. **What is API versioning?**
    Managing changes to APIs by creating multiple versions that coexist, enabling backward compatibility.

13. **What is the difference between PUT and PATCH?**
    PUT replaces the entire resource (idempotent); PATCH updates specific fields (can be idempotent).

14. **How do you implement pagination?**
    Use query parameters (page/limit) for offset-based or cursor parameter for cursor-based pagination.

15. **What is CORS?**
    Cross-Origin Resource Sharing; a security mechanism for cross-origin HTTP requests using headers.

16. **What is rate limiting?**
    Controlling the number of requests a client can make within a time period (e.g., 100 requests/hour).

17. **What is an API gateway?**
    A single entry point for all client requests, handling routing, authentication, rate limiting, and other concerns.

18. **How do you handle errors in REST APIs?**
    Use appropriate status codes (400, 401, 403, 404, 500) and consistent error response format.

19. **What is content negotiation?**
    Client and server agreeing on response format (JSON, XML) via Accept/Content-Type headers.

20. **What is the Richardson Maturity Model?**
    Levels 0-3: HTTP, Resources, HTTP Verbs, HATEOAS - describing REST API maturity.

### Senior (10)

21. **Design a URL shortener API**
    POST /api/shorten (create), GET /:code (redirect), GET /api/urls/:code (stats), rate limiting, caching.

22. **How do you version a REST API?**
    URL path (/v1/users), query parameter, header, or media type versioning; only version breaking changes.

23. **Explain cache strategies for REST APIs**
    ETag validation, Cache-Control headers, CDN caching, conditional requests (If-None-Match).

24. **How do you handle N+1 query problems?**
    Use eager loading, batch queries, DataLoader pattern, or consider GraphQL.

25. **Design a REST API for microservices**
    API gateway for routing, service discovery, circuit breakers, distributed tracing, centralized auth.

26. **How do you ensure API security?**
    Authentication (JWT, OAuth), authorization (RBAC), rate limiting, input validation, HTTPS, CORS.

27. **Explain eventual consistency in REST**
    When data is temporarily inconsistent across distributed systems; accept and handle stale reads.

28. **How do you handle file uploads?**
    multipart/form-data for small files, presigned URLs for cloud storage, chunked uploads for large files.

29. **Design a REST API for real-time features**
    WebSocket for bidirectional, SSE for server-push, polling as fallback, event-driven architecture.

30. **How do you test REST APIs?**
    Unit tests for handlers, integration tests for endpoints, contract testing, load testing, security testing.

### FAANG-style (10)

31. **Design a global rate limiting system**
    Distributed counters (Redis), regional rate limits, consistent hashing, fallback strategies.

32. **How would you migrate from v1 to v2 without breaking changes?**
    Dual support, deprecation headers, gradual migration, feature flags, backward compatibility.

33. **Design authentication for a multi-tenant SaaS**
    Tenant isolation, JWT with tenant claims, row-level security, audit logging.

34. **Design a webhook delivery system**
    Idempotency, retry with exponential backoff, dead letter queue, delivery guarantees.

35. **How do you handle API design for mobile apps?**
    Versioning, offline support, pagination optimization, compression, caching strategies.

36. **Design a payment processing API**
    Idempotency keys, PCI compliance, webhook notifications, retry logic, audit trail.

37. **How would you implement API analytics?**
    Request logging, latency tracking, error rates, usage patterns, capacity planning.

38. **Design a real-time collaboration API**
    Operational transforms, conflict resolution, WebSocket connections, presence awareness.

39. **How do you handle API design for IoT devices?**
    MQTT support, device authentication, protocol translation, edge computing.

40. **Design an API marketplace**
    Developer portal, API key management, usage metering, billing integration.

### Follow-ups (10)

41. **What are the tradeoffs between REST and GraphQL?**
    REST: Simple, cacheable, mature; GraphQL: Flexible queries, single endpoint, but complex caching.

42. **How do you handle API design for different clients?**
    Different endpoints or query parameters for web, mobile, and third-party developers.

43. **What is API-first design?**
    Designing API contract before implementation; enables parallel development and better documentation.

44. **How do you handle backward compatibility?**
    Add new fields without removing old ones, deprecate gradually, version when breaking changes needed.

45. **What is contract testing?**
    Testing API contracts between services to ensure they meet expectations without integration testing.

46. **How do you handle API design for internationalization?**
    Accept-Language header, locale-specific responses, date/time formats, currency handling.

47. **What is API governance?**
    Standards, guidelines, and processes for consistent API design across an organization.

48. **How do you handle API deprecation?**
    Sunset headers, documentation, migration guides, monitoring usage, gradual removal.

49. **What is API design-first approach?**
    OpenAPI/Swagger spec first, generate code, enable collaboration between frontend and backend.

50. **How do you handle API design for accessibility?**
    Consistent naming, descriptive errors, keyboard navigation support, screen reader compatibility.

## Best Practices

1. **Use plural nouns** - /api/users not /api/user
2. **Use HTTP methods correctly** - GET for read, POST for create, etc.
3. **Return proper status codes** - 200, 201, 204, 400, 401, 403, 404
4. **Implement pagination** - Never return unbounded results
5. **Use consistent response format** - Standardize data/error structure
6. **Version your API** - URL path versioning recommended
7. **Handle errors gracefully** - Consistent error responses
8. **Document your API** - OpenAPI/Swagger
9. **Use HTTPS** - Always encrypt in transit
10. **Rate limit** - Protect against abuse

## Performance Considerations

- **Caching** - ETag, Cache-Control, CDN
- **Compression** - gzip for responses
- **Pagination** - Avoid large payloads
- **Database optimization** - Indexes, query optimization
- **Connection pooling** - Reuse database connections

## Summary

REST API design is fundamental for full-stack development. Master HTTP methods, status codes, resource design, and common patterns. Practice designing APIs for real-world scenarios and understand tradeoffs between different approaches. Always consider security, scalability, and maintainability.

## Cheat Sheet

| Topic | Key Points |
|-------|------------|
| **REST** | Stateless, resource-based, uses HTTP methods |
| **HTTP Methods** | GET (safe, idempotent), POST (create), PUT (replace), PATCH (update), DELETE (remove) |
| **Status Codes** | 2xx success, 4xx client error, 5xx server error |
| **Versioning** | URL path (/v1/users) recommended |
| **Pagination** | Cursor-based for large datasets |
| **Authentication** | JWT for stateless, OAuth for third-party |
| **Rate Limiting** | Token bucket, sliding window algorithms |
| **CORS** | Required for cross-origin requests |
| **API Gateway** | Single entry point, handles cross-cutting concerns |
| **HATEOAS** | Include links in responses for discoverability |

## References & Learn More

- [RESTful API Design - Best Practices - Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md)
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)
- [10 Best Practices for Designing Better REST APIs - Medium](https://medium.com/@maheshmnj/best-practices-for-designing-better-rest-apis-60c8c9184f35)
- [How to Design a Good REST API - George Stocker](https://georgestockera.com/how-to-design-a-good-rest-api/)
- [API Design - Best Practices - Twilio](https://www.twilio.com/docs/usage/api)
