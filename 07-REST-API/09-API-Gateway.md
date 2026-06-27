# API Gateway

## Definition

An API Gateway is a server that acts as a single entry point for all client requests to a backend system. It handles routing, authentication, rate limiting, load balancing, request/response transformation, and other cross-cutting concerns, simplifying client interactions with microservices.

## Why Do We Need It?

Without an API Gateway:

1. **Complex client logic** - Clients must know all service endpoints
2. **Cross-cutting concerns** - Auth, rate limiting repeated in each service
3. **Service discovery** - Clients need to know service locations
4. **Protocol translation** - Different services may use different protocols
5. **Security exposure** - Internal services directly exposed to clients

## How It Works

### API Gateway Architecture

```
API Gateway Architecture
════════════════════════

Client          API Gateway              Microservices
  │                 │                         │
  │  GET /api/users │                         │
  │────────────────►│                         │
  │                 │  Route to User Service  │
  │                 │────────────────────────►│
  │                 │                         │
  │                 │  200 OK                 │
  │                 │◄────────────────────────│
  │                 │                         │
  │  200 OK         │                         │
  │◄────────────────│                         │
  │                 │                         │
  │  POST /api/orders                        │
  │────────────────►│                         │
  │                 │  Route to Order Service │
  │                 │────────────────────────►│
  │                 │                         │
  │  201 Created    │                         │
  │◄────────────────│                         │
```

### Gateway Components

```
API Gateway Components
══════════════════════

┌─────────────────────────────────────────────────────┐
│                    API Gateway                       │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Routing   │  │    Auth     │  │   Rate      │ │
│  │   Engine    │  │   Module    │  │  Limiting   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Request   │  │   Load      │  │   Circuit   │ │
│  │ Transformer │  │  Balancer   │  │   Breaker   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Response  │  │   Logging   │  │   Caching   │ │
│  │ Transformer │  │   & Metrics │  │   Layer     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Routing

```typescript
// Express-based API Gateway
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

// Route to User Service
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  changeOrigin: true,
  pathRewrite: { '^/api/users': '/users' }
}));

// Route to Order Service
app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  changeOrigin: true,
  pathRewrite: { '^/api/orders': '/orders' }
}));

// Route to Product Service
app.use('/api/products', createProxyMiddleware({
  target: 'http://product-service:3003',
  changeOrigin: true,
  pathRewrite: { '^/api/products': '/products' }
}));

// Dynamic routing based on configuration
const routes = {
  '/api/users': 'http://user-service:3001',
  '/api/orders': 'http://order-service:3002',
  '/api/products': 'http://product-service:3003'
};

Object.entries(routes).forEach(([path, target]) => {
  app.use(path, createProxyMiddleware({
    target,
    changeOrigin: true
  }));
});
```

### Authentication Middleware

```typescript
// Gateway authentication
const gatewayAuth = async (req, res, next) => {
  const token = extractToken(req);
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  try {
    const payload = await verifyToken(token);
    req.user = payload;
    
    // Add user info to headers for downstream services
    req.headers['x-user-id'] = payload.sub;
    req.headers['x-user-role'] = payload.role;
    req.headers['x-user-email'] = payload.email;
    
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

app.use('/api', gatewayAuth);
```

### Rate Limiting

```typescript
// Gateway-level rate limiting
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

const redisClient = new Redis();

const gatewayRateLimit = rateLimit({
  store: new RedisStore({
    sendCommand: (...args) => redisClient.call(...args)
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.user?.id || req.ip,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Rate limit exceeded',
      retryAfter: Math.ceil(req.rateLimit.resetTime / 1000)
    });
  }
});

app.use('/api', gatewayRateLimit);
```

### Load Balancing

```typescript
// Round-robin load balancing
class LoadBalancer {
  private services: Map<string, string[]> = new Map();
  private currentIndex: Map<string, number> = new Map();
  
  constructor() {
    this.services.set('user-service', [
      'http://user-1:3001',
      'http://user-2:3001',
      'http://user-3:3001'
    ]);
    this.services.set('order-service', [
      'http://order-1:3002',
      'http://order-2:3002'
    ]);
  }
  
  getNext(serviceName: string): string {
    const instances = this.services.get(serviceName);
    if (!instances || instances.length === 0) {
      throw new Error(`No instances for ${serviceName}`);
    }
    
    const index = this.currentIndex.get(serviceName) || 0;
    const nextIndex = (index + 1) % instances.length;
    this.currentIndex.set(serviceName, nextIndex);
    
    return instances[index];
  }
}

// Health-check based load balancing
class HealthAwareLoadBalancer extends LoadBalancer {
  private healthStatus: Map<string, boolean> = new Map();
  
  async checkHealth(serviceName: string): Promise<void> {
    const instances = this.services.get(serviceName) || [];
    
    for (const instance of instances) {
      try {
        await fetch(`${instance}/health`, { timeout: 5000 });
        this.healthStatus.set(instance, true);
      } catch {
        this.healthStatus.set(instance, false);
      }
    }
  }
  
  getHealthyInstance(serviceName: string): string {
    const instances = this.services.get(serviceName) || [];
    const healthy = instances.filter(i => this.healthStatus.get(i) !== false);
    
    if (healthy.length === 0) {
      throw new Error(`No healthy instances for ${serviceName}`);
    }
    
    const index = this.currentIndex.get(serviceName) || 0;
    const nextIndex = (index + 1) % healthy.length;
    this.currentIndex.set(serviceName, nextIndex);
    
    return healthy[index];
  }
}
```

### Request Transformation

```typescript
// Transform request before forwarding
const requestTransformer = (req, res, next) => {
  // Add gateway headers
  req.headers['x-gateway-timestamp'] = Date.now().toString();
  req.headers['x-request-id'] = generateRequestId();
  
  // Transform request body
  if (req.body) {
    req.body = transformRequestBody(req.body);
  }
  
  // Remove sensitive headers
  delete req.headers['x-internal-token'];
  
  next();
};

function transformRequestBody(body: any): any {
  // Remove sensitive fields
  const { password, internalId, ...safeBody } = body;
  
  // Add metadata
  return {
    ...safeBody,
    _metadata: {
      source: 'gateway',
      timestamp: new Date().toISOString()
    }
  };
}
```

### Response Transformation

```typescript
// Transform response before sending to client
const responseTransformer = (req, res, next) => {
  const originalJson = res.json.bind(res);
  
  res.json = (body) => {
    // Transform response
    const transformed = transformResponseBody(body, req);
    return originalJson(transformed);
  };
  
  next();
};

function transformResponseBody(body: any, req: express.Request): any {
  // Add pagination links
  if (body.pagination) {
    body._links = generatePaginationLinks(body.pagination, req);
  }
  
  // Remove internal fields
  if (body.data && Array.isArray(body.data)) {
    body.data = body.data.map(item => {
      const { __v, _id, ...safeItem } = item;
      return safeItem;
    });
  }
  
  // Add metadata
  body._meta = {
    requestId: req.headers['x-request-id'],
    timestamp: new Date().toISOString()
  };
  
  return body;
}
```

### Circuit Breaker

```typescript
import CircuitBreaker from 'opossum';

// Circuit breaker for each service
const breakers = new Map<string, CircuitBreaker>();

function createCircuitBreaker(serviceName: string, target: string) {
  const breaker = new CircuitBreaker(
    async (req) => {
      const response = await fetch(`${target}${req.path}`, {
        method: req.method,
        headers: req.headers,
        body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined
      });
      return response;
    },
    {
      timeout: 5000,
      errorThresholdPercentage: 50,
      resetTimeout: 30000
    }
  );
  
  breaker.on('open', () => {
    console.log(`Circuit breaker OPEN for ${serviceName}`);
  });
  
  breaker.on('halfOpen', () => {
    console.log(`Circuit breaker HALF-OPEN for ${serviceName}`);
  });
  
  breaker.on('close', () => {
    console.log(`Circuit breaker CLOSED for ${serviceName}`);
  });
  
  breakers.set(serviceName, breaker);
  return breaker;
}

// Usage
const userBreaker = createCircuitBreaker('user-service', 'http://user-service:3001');

app.use('/api/users', async (req, res) => {
  try {
    const response = await userBreaker.fire(req);
    res.status(response.status).json(await response.json());
  } catch (err) {
    if (err.name === 'CircuitOpenError') {
      return res.status(503).json({ error: 'Service temporarily unavailable' });
    }
    throw err;
  }
});
```

## Code Examples

### Complete API Gateway

```typescript
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import rateLimit from 'express-rate-limit';
import CircuitBreaker from 'opossum';
import Redis from 'ioredis';

const app = express();
const redis = new Redis(process.env.REDIS_URL);

// Request ID middleware
app.use((req, res, next) => {
  req.headers['x-request-id'] = req.headers['x-request-id'] || generateRequestId();
  res.set('X-Request-Id', req.headers['x-request-id']);
  next();
});

// Logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log({
      requestId: req.headers['x-request-id'],
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration,
      ip: req.ip,
      userAgent: req.headers['user-agent']
    });
  });
  
  next();
});

// Authentication middleware
const authenticate = async (req, res, next) => {
  const publicPaths = ['/api/health', '/api/auth/login', '/api/auth/register'];
  
  if (publicPaths.some(p => req.path.startsWith(p))) {
    return next();
  }
  
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  try {
    const payload = await verifyToken(token);
    req.user = payload;
    req.headers['x-user-id'] = payload.sub;
    req.headers['x-user-role'] = payload.role;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

app.use(authenticate);

// Rate limiting
const limiter = rateLimit({
  store: new RedisStore({ sendCommand: (...args) => redis.call(...args) }),
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip
});

app.use('/api', limiter);

// Service configuration
const services = {
  users: {
    target: 'http://user-service:3001',
    pathRewrite: { '^/api/users': '/users' },
    circuitBreaker: { timeout: 5000, errorThreshold: 50 }
  },
  orders: {
    target: 'http://order-service:3002',
    pathRewrite: { '^/api/orders': '/orders' },
    circuitBreaker: { timeout: 5000, errorThreshold: 50 }
  },
  products: {
    target: 'http://product-service:3003',
    pathRewrite: { '^/api/products': '/products' },
    circuitBreaker: { timeout: 5000, errorThreshold: 50 }
  }
};

// Create circuit breakers
const breakers = new Map();
Object.entries(services).forEach(([name, config]) => {
  const breaker = new CircuitBreaker(
    async (req) => {
      const proxy = createProxyMiddleware({
        target: config.target,
        changeOrigin: true,
        pathRewrite: config.pathRewrite
      });
      return new Promise((resolve, reject) => {
        proxy(req, { json: () => resolve(req) }, (err) => {
          if (err) reject(err);
          else resolve(req);
        });
      });
    },
    config.circuitBreaker
  );
  breakers.set(name, breaker);
});

// Proxy routes
app.use('/api/users', createProxyMiddleware({
  target: services.users.target,
  changeOrigin: true,
  pathRewrite: services.users.pathRewrite,
  onProxyReq: (proxyReq, req) => {
    proxyReq.setHeader('X-Request-Id', req.headers['x-request-id']);
    proxyReq.setHeader('X-User-Id', req.headers['x-user-id'] || '');
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(502).json({ error: 'Bad Gateway' });
  }
}));

app.use('/api/orders', createProxyMiddleware({
  target: services.orders.target,
  changeOrigin: true,
  pathRewrite: services.orders.pathRewrite
}));

app.use('/api/products', createProxyMiddleware({
  target: services.products.target,
  changeOrigin: true,
  pathRewrite: services.products.pathRewrite
}));

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Gateway error:', err);
  res.status(500).json({ error: 'Internal Gateway Error' });
});

app.listen(8080, () => {
  console.log('API Gateway running on port 8080');
});
```

## Real-World Use Cases

### 1. Microservices Aggregation

```typescript
// Aggregate responses from multiple services
app.get('/api/dashboard', async (req, res) => {
  const [user, orders, notifications] = await Promise.all([
    fetchFromService('user-service', `/users/${req.user.id}`),
    fetchFromService('order-service', `/orders?userId=${req.user.id}`),
    fetchFromService('notification-service', `/notifications?userId=${req.user.id}`)
  ]);
  
  res.json({
    data: {
      user: user.data,
      orders: orders.data,
      notifications: notifications.data
    }
  });
});
```

### 2. Protocol Translation

```typescript
// REST to gRPC translation
app.post('/api/users', async (req, res) => {
  const grpcRequest = {
    name: req.body.name,
    email: req.body.email
  };
  
  const response = await userGrpcClient.createUser(grpcRequest);
  
  res.status(201).json({
    data: {
      id: response.id,
      name: response.name,
      email: response.email
    }
  });
});
```

### 3. Request/Response Aggregation

```typescript
// Aggregate paginated results
app.get('/api/feed', async (req, res) => {
  const { page = 1, limit = 10 } = req.query;
  
  const [posts, stories, recommendations] = await Promise.all([
    fetchFromService('post-service', `/posts?page=${page}&limit=${limit}`),
    fetchFromService('story-service', `/stories?limit=5`),
    fetchFromService('recommendation-service', `/recommendations?userId=${req.user.id}`)
  ]);
  
  res.json({
    data: {
      posts: posts.data,
      stories: stories.data,
      recommendations: recommendations.data
    }
  });
});
```

### 4. Authentication Gateway

```typescript
// Centralized authentication
app.use('/api', async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  // Token introspection
  const tokenInfo = await introspectToken(token);
  
  if (!tokenInfo.active) {
    return res.status(401).json({ error: 'Invalid token' });
  }
  
  // Add user context to request
  req.user = {
    id: tokenInfo.sub,
    email: tokenInfo.email,
    roles: tokenInfo.roles,
    permissions: tokenInfo.permissions
  };
  
  // Add headers for downstream services
  req.headers['x-user-id'] = tokenInfo.sub;
  req.headers['x-user-email'] = tokenInfo.email;
  req.headers['x-user-roles'] = tokenInfo.roles.join(',');
  
  next();
});
```

## Common Mistakes

### 1. Not Handling Service Failures

```typescript
// ❌ Bad: No circuit breaker
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001'
}));

// ✅ Good: Circuit breaker
const breaker = new CircuitBreaker(async (req) => {
  return await fetch(`http://user-service:3001${req.path}`);
}, { timeout: 5000 });

app.use('/api/users', async (req, res) => {
  try {
    const response = await breaker.fire(req);
    res.json(await response.json());
  } catch (err) {
    if (err.name === 'CircuitOpenError') {
      return res.status(503).json({ error: 'Service unavailable' });
    }
    throw err;
  }
});
```

### 2. Not Adding Request IDs

```typescript
// ❌ Bad: No request tracking
app.use('/api', createProxyMiddleware({ target: 'http://service:3001' }));

// ✅ Good: Request ID tracking
app.use((req, res, next) => {
  req.headers['x-request-id'] = generateRequestId();
  next();
});
app.use('/api', createProxyMiddleware({ target: 'http://service:3001' }));
```

### 3. Not Rate Limiting at Gateway

```typescript
// ❌ Bad: Rate limiting in each service
// user-service: rate limiter
// order-service: rate limiter
// product-service: rate limiter

// ✅ Good: Rate limiting at gateway
app.use('/api', rateLimiter({ max: 100, windowMs: 15 * 60 * 1000 }));
app.use('/api/users', createProxyMiddleware({ target: 'http://user-service:3001' }));
```

### 4. Not Handling Timeouts

```typescript
// ❌ Bad: No timeout
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001'
}));

// ✅ Good: Timeout handling
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  proxyTimeout: 5000,
  timeout: 5000
}));
```

### 5. Not Logging Errors

```typescript
// ❌ Bad: Silent failures
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  onError: (err, req, res) => {
    res.status(502).json({ error: 'Bad Gateway' });
  }
}));

// ✅ Good: Error logging
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  onError: (err, req, res) => {
    console.error('Proxy error:', {
      requestId: req.headers['x-request-id'],
      service: 'user-service',
      error: err.message
    });
    res.status(502).json({ error: 'Bad Gateway' });
  }
}));
```

## Best Practices

1. **Centralize cross-cutting concerns** - Auth, rate limiting, logging at gateway
2. **Use circuit breakers** - Prevent cascade failures
3. **Implement request tracking** - X-Request-Id headers
4. **Add timeouts** - Prevent hanging requests
5. **Load balance** - Distribute traffic across instances
6. **Cache responses** - Reduce load on services
7. **Monitor gateway** - Track latency, error rates
8. **Document API** - OpenAPI/Swagger for gateway routes
9. **Health checks** - Monitor service health
10. **Graceful degradation** - Fallback responses when services down

## Performance Considerations

- **Connection pooling** - Reuse connections to services
- **Response caching** - Cache frequently accessed data
- **Compression** - Enable gzip for responses
- **Async processing** - Non-blocking I/O
- **Connection limits** - Prevent connection exhaustion

## Interview Questions

### Beginner (5)

1. **What is an API Gateway?** - A single entry point for all client requests, handling routing, auth, and other concerns.

2. **Why do we need an API Gateway?** - Simplifies client logic, centralizes cross-cutting concerns, improves security.

3. **What is routing in an API Gateway?** - Directing requests to appropriate backend services based on path or other criteria.

4. **What is rate limiting at the gateway?** - Controlling request rates before they reach individual services.

5. **What is request transformation?** - Modifying request headers, body, or path before forwarding to services.

### Intermediate (5)

6. **How does an API Gateway handle authentication?** - Validates tokens, adds user context to headers, forwards to services.

7. **What is a circuit breaker?** - A pattern to prevent cascade failures by stopping requests to failing services.

8. **How do you implement load balancing?** - Round-robin, least connections, or health-aware algorithms.

9. **What is response aggregation?** - Combining responses from multiple services into a single response.

10. **How do you handle service discovery?** - Use service registry (Consul, etcd) or environment variables.

### Senior (10)

11. **Design an API Gateway for microservices** - Routing, auth, rate limiting, circuit breakers, monitoring.

12. **How do you handle gateway high availability?** - Multiple instances, load balancing, health checks, failover.

13. **Design request/response transformation** - Header manipulation, body transformation, protocol translation.

14. **How do you monitor an API Gateway?** - Metrics, logging, tracing, alerting on latency and errors.

15. **Design gateway caching** - Response caching, cache invalidation, cache headers.

16. **How do you handle gateway security?** - TLS termination, WAF integration, DDoS protection.

17. **Design gateway for real-time applications** - WebSocket support, SSE handling, long polling.

18. **How do you test an API Gateway?** - Load testing, chaos engineering, integration testing.

19. **Design gateway for multi-region deployment** - Regional routing, latency-aware routing, failover.

20. **How do you version APIs at the gateway?** - Path-based versioning, header-based routing, A/B testing.

### FAANG-style (5)

21. **Design an API Gateway for Netflix-scale traffic** - Distributed gateway, edge caching, regional routing.

22. **How would you implement gateway for serverless?** - Lambda@Edge, CloudFront functions, cold start optimization.

23. **Design gateway for GraphQL federation** - Schema stitching, query planning, distributed resolvers.

24. **How do you handle gateway for gRPC services?** - gRPC-Web, protocol translation, load balancing.

25. **Design gateway for IoT devices** - MQTT support, device authentication, protocol translation.

### Follow-ups (5)

26. **What are the alternatives to API Gateway?** - Service mesh, client-side load balancing, direct service calls.

27. **How do you handle gateway deployment?** - Blue-green, canary, rolling updates, feature flags.

28. **What is the difference between API Gateway and Service Mesh?** - Gateway: edge proxy; Service Mesh: sidecar proxy for service-to-service.

29. **How do you handle gateway configuration?** - Config files, environment variables, dynamic configuration.

30. **What are the limitations of API Gateway?** - Single point of failure, latency overhead, complexity.

## Summary

An API Gateway is essential for microservices architectures. It provides a single entry point, centralizes cross-cutting concerns, and simplifies client interactions. Key features include routing, authentication, rate limiting, circuit breaking, and request transformation. Always implement monitoring, health checks, and graceful degradation.

## Cheat Sheet

| Component | Purpose | Implementation |
|-----------|---------|----------------|
| Routing | Direct requests to services | Path-based, header-based |
| Authentication | Verify identity | JWT validation, token introspection |
| Rate Limiting | Control request rates | Token bucket, sliding window |
| Load Balancing | Distribute traffic | Round-robin, least connections |
| Circuit Breaker | Prevent cascade failures | Open/closed/half-open states |
| Request Transform | Modify requests | Header injection, body transformation |
| Response Transform | Modify responses | Pagination links, field removal |
| Caching | Reduce service load | Response caching, CDN integration |
| Monitoring | Track performance | Metrics, logging, tracing |

## References & Learn More

- [API Gateway Pattern - Microsoft Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation)
- [Pattern: API Gateway / Backends for Frontends - Chris Richardson](https://microservices.io/patterns/apigateway.html)
- [Kong API Gateway](https://docs.konghq.com/)
- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [NGINX as an API Gateway](https://www.nginx.com/solutions/api-gateway/)
