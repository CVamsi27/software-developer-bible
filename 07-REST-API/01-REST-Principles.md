---
section: REST APIs
category: Backend
tags: [concept]
---

# REST Principles

## Definition

REST (Representational State Transfer) is an architectural style for designing networked applications, introduced by Roy Fielding in his 2000 doctoral dissertation. It provides a set of constraints and principles that emphasize scalability, simplicity, modifiability, and visibility.

REST is not a protocol or standard—it's an architectural pattern that leverages existing HTTP/HTTPS protocols to build web services that are:

- **Scalable** - Handles large volumes of requests efficiently
- **Modifiable** - Easy to change and evolve over time
- **Visible** - Clear, transparent communication
- **Reliable** - Fault-tolerant and consistent
- **Portable** - Works across platforms and devices

## Why Do We Need It?

Before REST, web services relied on complex protocols like SOAP requiring heavy XML payloads, complex WSDL contracts, specialized tooling, and tight coupling between client and server.

REST emerged as a simpler alternative that:

1. **Reduces complexity** - Uses standard HTTP methods and status codes

2. **Improves performance** - Lightweight JSON payloads instead of verbose XML

3. **Enhances scalability** - Stateless design enables horizontal scaling

4. **Increases interoperability** - Works with any client that speaks HTTP

5. **Simplifies development** - Intuitive resource-based URL design

## How It Works

### The Six REST Constraints

REST is defined by six architectural constraints that must be applied together.

#### 1. Client-Server Architecture

The client and server are separate concerns that communicate over a network, allowing independent development, different technology stacks, and scalability of each tier independently.

```text
Client-Server Architecture
══════════════════════════

┌─────────────┐          ┌─────────────┐
│   Client     │          │   Server     │
│  (Browser,   │  HTTP/   │  (API,       │
│   Mobile)    │  HTTPS   │   Database)  │
│             │ ◄──────► │             │
└─────────────┘          └─────────────┘
       │                        │
   User Interface          Business Logic
   Presentation            Data Storage
   Client-Side Logic       Server-Side Logic

```

```typescript
// Server-side (Express.js)
app.get('/api/users/:id', async (req, res) => {
  const user = await UserService.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json({
    data: user,
    links: {
      self: `/api/users/${user.id}`,
      posts: `/api/users/${user.id}/posts`
    }
  });
});

// Client-side
async function getUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const result = await response.json();
  return result.data;
}

```

#### 2. Stateless

Each request from client to server must contain all information needed to understand and process the request. The server does not store client context between requests.

```text
Stateless Communication
═══════════════════════

Request 1: GET /api/orders
Headers: { Authorization: "Bearer abc123" }
──────────────────────────────────────────► Server processes request
                                           Returns all orders
                                           No state stored

Request 2: GET /api/orders/456
Headers: { Authorization: "Bearer abc123" }
──────────────────────────────────────────► Server processes request
                                           Returns order 456
                                           No state stored

```

```typescript
// Each request is self-contained with JWT token
interface JWTClaims {
  sub: string;           // User ID
  role: string;          // User role
  permissions: string[]; // User permissions
  exp: number;           // Expiration time
}

app.post('/api/orders', authenticate, async (req, res) => {
  // User info comes from JWT token, not server session
  const userId = req.user.sub;
  const order = await OrderService.create({
    userId,
    items: req.body.items,
    shippingAddress: req.body.shippingAddress
  });
  res.status(201).json({ data: order });
});

```

#### 3. Cacheable

Responses must explicitly state whether they can be cached. If cacheable, the client may reuse the response data for equivalent future requests.

```text
Cacheable Response Flow
═══════════════════════

Client                        Server
  │  GET /api/products          │
  │  If-None-Match: "abc123"   │
  │────────────────────────────►│
  │  304 Not Modified           │
  │  (Use cached version)       │
  │◄────────────────────────────│
  │                             │
  │  GET /api/products          │
  │────────────────────────────►│
  │  200 OK                     │
  │  Cache-Control: max-age=3600│
  │  ETag: "def456"            │
  │◄────────────────────────────│

```

```typescript
app.get('/api/products', async (req, res) => {
  const products = await ProductService.findAll();
  res.set({
    'Cache-Control': 'public, max-age=3600',
    'ETag': generateETag(products)
  });
  res.json({ data: products });
});

app.get('/api/orders', authenticate, async (req, res) => {
  const orders = await OrderService.findByUserId(req.user.sub);
  const etag = generateETag(orders);
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }
  res.set({ 'Cache-Control': 'private, no-cache', 'ETag': etag });
  res.json({ data: orders });
});

```

#### 4. Uniform Interface

REST defines a uniform interface with four sub-constraints:

**a) Identification of Resources** - Each resource identified by unique URI

```text
Resource Identification via URIs
═══════════════════════════════

✅ Good: /api/users/123
✅ Good: /api/users/123/posts/789
❌ Bad:  /api/getUser?id=123
❌ Bad:  /api/user/123/delete

```

**b) Manipulation Through Representations**

```typescript
interface UserRepresentation {
  id: string;
  name: string;
  email: string;
  _links: {
    self: string;
    posts: string;
    followers: string;
  };
}

app.post('/api/users', async (req, res) => {
  const user = await UserService.create(req.body);
  const representation: UserRepresentation = {
    id: user.id,
    name: user.name,
    email: user.email,
    _links: {
      self: `/api/users/${user.id}`,
      posts: `/api/users/${user.id}/posts`,
      followers: `/api/users/${user.id}/followers`
    }
  };
  res.status(201).json(representation);
});

```

**c) Self-Descriptive Messages** - Each request/response contains enough information to be understood.

**d) HATEOAS (Hypermedia as the Engine of Application State)**

```typescript
app.get('/api/orders/:id', authenticate, async (req, res) => {
  const order = await OrderService.findById(req.params.id);
  const response = {
    id: order.id,
    status: order.status,
    total: order.total,
    _links: {
      self: `/api/orders/${order.id}`,
      ...(order.status === 'pending' && { cancel: `/api/orders/${order.id}/cancel` }),
      ...(order.status === 'pending' && { pay: `/api/orders/${order.id}/pay` }),
      ...(['shipped', 'processing'].includes(order.status) && { track: `/api/orders/${order.id}/track` })
    }
  };
  res.json(response);
});

```

#### 5. Layered System

A client cannot tell whether it is connected directly to the end server or to an intermediary (load balancer, proxy, cache).

```text
Layered System Architecture
═══════════════════════════

┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Client  │────►│  Load   │────►│   API   │────►│Database │
│         │     │ Balancer│     │ Gateway │     │         │
└─────────┘     └─────────┘     └─────────┘     └─────────┘

```

#### 6. Code on Demand (Optional)

REST allows servers to extend client functionality by transferring executable code. This is the only optional constraint.

### HTTP Methods

```text
HTTP Methods and Their Purposes
═══════════════════════════════

Method    Purpose              Idempotent  Safe    Has Body
─────────────────────────────────────────────────────────────
GET       Retrieve resource    Yes         Yes     No
POST      Create resource      No          No      Yes
PUT       Replace resource     Yes         No      Yes
PATCH     Partial update       Yes*        No      Yes
DELETE    Delete resource      Yes         No      Optional
HEAD      Get metadata only    Yes         Yes     No
OPTIONS   Get allowed methods  Yes         Yes     No

```

## Code Examples

### Complete RESTful API Implementation

```typescript
import express, { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}

interface ApiResponse<T> {
  data: T | null;
  error?: string;
  message?: string;
  _links?: Record<string, string>;
}

const users: Map<string, User> = new Map();

const router = express.Router();

router.get('/', async (req: Request, res: Response) => {
  const { page = '1', limit = '10', sort = 'createdAt' } = req.query;
  const pageNum = parseInt(page as string);
  const limitNum = parseInt(limit as string);
  let userList = Array.from(users.values());
  userList.sort((a, b) => {
    const aVal = a[sort as keyof User];
    const bVal = b[sort as keyof User];
    return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
  });
  const startIndex = (pageNum - 1) * limitNum;
  const paginatedUsers = userList.slice(startIndex, startIndex + limitNum);
  res.json({
    data: paginatedUsers,
    _links: {
      self: `/api/users?page=${pageNum}&limit=${limitNum}`,
      next: userList.length > startIndex + limitNum ? `/api/users?page=${pageNum + 1}&limit=${limitNum}` : '',
      prev: pageNum > 1 ? `/api/users?page=${pageNum - 1}&limit=${limitNum}` : ''
    }
  });
});

router.get('/:id', async (req: Request, res: Response) => {
  const user = users.get(req.params.id);
  if (!user) return res.status(404).json({ data: null, error: 'Not Found' });
  res.json({ data: user, _links: { self: `/api/users/${user.id}` } });
});

router.post('/', async (req: Request, res: Response) => {
  const { name, email } = req.body;
  if (!name || !email) return res.status(400).json({ data: null, error: 'Bad Request' });
  const existingUser = Array.from(users.values()).find(u => u.email === email);
  if (existingUser) return res.status(409).json({ data: null, error: 'Conflict' });
  const newUser: User = { id: uuidv4(), name, email, createdAt: new Date(), updatedAt: new Date() };
  users.set(newUser.id, newUser);
  res.status(201).header('Location', `/api/users/${newUser.id}`).json({ data: newUser });
});

router.put('/:id', async (req: Request, res: Response) => {
  const existingUser = users.get(req.params.id);
  if (!existingUser) return res.status(404).json({ data: null, error: 'Not Found' });
  const updatedUser: User = { ...existingUser, ...req.body, id: existingUser.id, updatedAt: new Date() };
  users.set(req.params.id, updatedUser);
  res.json({ data: updatedUser });
});

router.delete('/:id', async (req: Request, res: Response) => {
  if (!users.has(req.params.id)) return res.status(404).json({ data: null, error: 'Not Found' });
  users.delete(req.params.id);
  res.status(204).end();
});

app.use('/api/users', router);

```

## Real-World Use Cases

### 1. E-commerce Platform

```typescript
app.get('/api/products', ...);                    // List products
app.get('/api/products/:id', ...);                // Get product details
app.post('/api/products', ...);                   // Create product (admin)
app.get('/api/cart', authenticate, ...);          // Get user's cart
app.post('/api/cart/items', authenticate, ...);   // Add item to cart
app.post('/api/orders', authenticate, ...);       // Place order
app.get('/api/orders', authenticate, ...);        // List user's orders

```

### 2. Social Media API

```typescript
app.get('/api/users/:id', ...);                   // Get user profile
app.post('/api/posts', authenticate, ...);        // Create post
app.get('/api/feed', authenticate, ...);          // Get personalized feed
app.post('/api/posts/:id/comments', authenticate, ...); // Add comment
app.post('/api/posts/:id/like', authenticate, ...);    // Like post

```

### 3. Banking API

```typescript
app.get('/api/accounts', authenticate, ...);      // List accounts
app.get('/api/accounts/:id/transactions', authenticate, ...); // List transactions
app.post('/api/transfers', authenticate, ...);    // Create transfer

```

## Common Mistakes

### 1. Using Verbs Instead of Nouns

```typescript
// ❌ Bad
app.get('/api/getUsers', ...);
app.post('/api/createUser', ...);

// ✅ Good
app.get('/api/users', ...);
app.post('/api/users', ...);

```

### 2. Breaking Stateless Constraint

```typescript
// ❌ Bad: Storing session state on server
app.post('/api/login', (req, res) => {
  req.session.userId = user.id;
});

// ✅ Good: Stateless with JWT
app.post('/api/login', (req, res) => {
  const token = generateJWT({ userId: user.id });
  res.json({ data: { token } });
});

```

### 3. Ignoring Cacheability

```typescript
// ❌ Bad: No cache headers
res.json({ data: products });

// ✅ Good: Proper cache headers
res.set({ 'Cache-Control': 'public, max-age=3600', 'ETag': generateETag(products) });
res.json({ data: products });

```

### 4. Not Using Hypermedia (HATEOAS)

```typescript
// ❌ Bad: No links
res.json({ data: user });

// ✅ Good: Response with links
res.json({ data: user, _links: { self: `/api/users/${user.id}`, posts: `/api/users/${user.id}/posts` } });

```

### 5. Incorrect HTTP Status Codes

```typescript
// ❌ Bad: Always returning 200
res.json({ data: user });

// ✅ Good: Appropriate status codes
res.status(201).json({ data: user });
res.status(400).json({ error: 'Invalid input' });
res.status(404).json({ error: 'Not found' });

```

## Best Practices

1. **Use plural nouns** - `/api/users` not `/api/user`

2. **Use HTTP methods correctly** - GET for read, POST for create, PUT for update, DELETE for remove

3. **Return proper status codes** - 200, 201, 204, 400, 401, 403, 404, 500

4. **Implement pagination** - Use query params for page/limit

5. **Use consistent response format** - Standardize data/error structure

6. **Version your API** - `/api/v1/users`

7. **Support filtering and sorting** - Query parameters

8. **Handle errors gracefully** - Consistent error responses

9. **Document your API** - OpenAPI/Swagger
10. **Use HTTPS** - Always encrypt in transit

## Performance Considerations

- Implement caching headers (ETag, Cache-Control)
- Use pagination for large datasets
- Enable gzip compression
- Use CDN for static assets
- Implement database query optimization
- Use connection pooling
- Consider GraphQL for complex data requirements


## Summary

REST is a powerful architectural style that leverages HTTP's existing features to create scalable, maintainable web services. Understanding its six constraints—client-server, stateless, cacheable, uniform interface, layered system, and code on demand—is essential for designing robust APIs. Following best practices like proper URI design, correct HTTP methods, appropriate status codes, and consistent response formats ensures your API is intuitive and maintainable.

## Cheat Sheet
| Concept | Details |
|---------|---------|
| **Resources** | Nouns in URIs (`/api/users`) |
| **HTTP Methods** | GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove) |
| **Status Codes** | 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Server Error) |
| **Idempotency** | GET, PUT, DELETE are idempotent; POST is not |
| **Statelessness** | No server-side session; use JWT tokens |
| **Caching** | ETag, Cache-Control, Last-Modified headers |
| **HATEOAS** | Include links in responses for discoverability |
| **Versioning** | URL path (`/v1/users`) or headers |
| **Pagination** | Use page/limit query parameters |
| **Consistency** | Uniform interface, self-descriptive messages |

---

## See Also
- [NestJS](../06-NestJS/)
- [Security](../09-Security/)
- [System Design](../11-System-Design/)
- [Microservices](../12-Microservices/)

## References & Learn More

- [REST - Wikipedia](https://en.wikipedia.org/wiki/Representational_state_transfer)
- [Roy Fielding's Original REST Dissertation](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md)
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)
- [RESTful API Design - Best Practices](https://restfulapi.net/)
