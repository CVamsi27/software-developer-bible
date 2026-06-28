# API Gateway

## Definition

An API Gateway is a server that acts as a single entry point for all client requests in a microservices architecture. It handles cross-cutting concerns like routing, authentication, rate limiting, and request transformation before forwarding requests to appropriate backend services.

## Why Do We Need It?

In microservices:
- Clients need simple, unified API instead of complex service mesh
- Cross-cutting concerns should be centralized, not duplicated
- Security enforcement at edge protects internal services
- Protocol translation between clients and services
- Request aggregation reduces client-server round trips

## How It Works

```
┌─────────────┐
│   Mobile    │────┐
│   Client    │    │
└─────────────┘    │
                   ▼
┌─────────────┐  ┌─────────────────────────────────────────┐
│   Web       │──│              API GATEWAY                 │
│   Client    │  │                                         │
└─────────────┘  │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
                 │  │ Rate    │ │ Auth    │ │ Request │   │
┌─────────────┐  │  │ Limiter │ │ Handler │ │ Trans.  │   │
│   IoT       │──│  └─────────┘ └─────────┘ └─────────┘   │
│   Device    │  │         │                               │
└─────────────┘  │         ▼                               │
                 │  ┌─────────────────┐                    │
                 │  │    Router       │                    │
                 │  └─────────────────┘                    │
                 └──────────────┬──────────────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
   ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
   │  User       │       │  Product    │       │  Order      │
   │  Service    │       │  Service    │       │  Service    │
   └─────────────┘       └─────────────┘       └─────────────┘
```

## Code Examples

### TypeScript - Basic API Gateway

```typescript
import express, { Request, Response, NextFunction } from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import rateLimit from 'express-rate-limit';
import jwt from 'jsonwebtoken';

const app = express();

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests',
});

app.use(limiter);

// Authentication middleware
const authenticate = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Service routes
const serviceRoutes: Record<string, string> = {
  '/api/users': 'http://user-service:3001',
  '/api/products': 'http://product-service:3002',
  '/api/orders': 'http://order-service:3003',
};

// Apply proxy routes
Object.entries(serviceRoutes).forEach(([path, target]) => {
  app.use(path, authenticate, createProxyMiddleware({
    target,
    changeOrigin: true,
    pathRewrite: { [`^${path}`]: '' },
    onError: (err, req, res) => {
      console.error('Proxy error:', err);
      (res as Response).status(502).json({ error: 'Service unavailable' });
    },
  }));
});

app.listen(3000, () => {
  console.log('API Gateway running on port 3000');
});
```

### TypeScript - Advanced Gateway with Request Transformation

```typescript
interface GatewayConfig {
  routes: RouteConfig[];
  rateLimit: RateLimitConfig;
  auth: AuthConfig;
}

interface RouteConfig {
  path: string;
  target: string;
  methods: string[];
  rateLimit?: { windowMs: number; max: number };
  cache?: { ttl: number; key?: string };
  transforms?: RequestTransform[];
}

interface RateLimitConfig {
  windowMs: number;
  max: number;
  skipSuccessfulRequests?: boolean;
}

interface AuthConfig {
  jwtSecret: string;
  excludePaths: string[];
}

interface RequestTransform {
  type: 'add-header' | 'remove-header' | 'rewrite-path' | 'add-body-field';
  config: Record<string, string>;
}

class AdvancedAPIGateway {
  private app: express.Application;
  private config: GatewayConfig;
  private cache: Map<string, { data: unknown; expiry: number }> = new Map();

  constructor(config: GatewayConfig) {
    this.app = express();
    this.config = config;
    this.setupMiddleware();
    this.setupRoutes();
  }

  private setupMiddleware(): void {
    this.app.use(express.json());
    this.app.use(this.rateLimitMiddleware());
    this.app.use(this.authMiddleware());
    this.app.use(this.loggingMiddleware());
  }

  private rateLimitMiddleware() {
    const requests = new Map<string, { count: number; resetTime: number }>();

    return (req: Request, res: Response, next: NextFunction) => {
      const key = req.ip || 'unknown';
      const now = Date.now();
      const windowMs = this.config.rateLimit.windowMs;

      let record = requests.get(key);
      if (!record || now > record.resetTime) {
        record = { count: 0, resetTime: now + windowMs };
        requests.set(key, record);
      }

      record.count++;

      if (record.count > this.config.rateLimit.max) {
        return res.status(429).json({ error: 'Rate limit exceeded' });
      }

      res.setHeader('X-RateLimit-Remaining',
        this.config.rateLimit.max - record.count);
      next();
    };
  }

  private authMiddleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      if (this.config.auth.excludePaths.some(p => req.path.startsWith(p))) {
        return next();
      }

      const token = req.headers.authorization?.split(' ')[1];
      if (!token) {
        return res.status(401).json({ error: 'Authentication required' });
      }

      try {
        const decoded = jwt.verify(token, this.config.auth.jwtSecret);
        (req as any).user = decoded;
        next();
      } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
      }
    };
  }

  private loggingMiddleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const start = Date.now();

      res.on('finish', () => {
        const duration = Date.now() - start;
        console.log({
          timestamp: new Date().toISOString(),
          method: req.method,
          path: req.path,
          statusCode: res.statusCode,
          duration: `${duration}ms`,
          ip: req.ip,
          userAgent: req.headers['user-agent'],
        });
      });

      next();
    };
  }

  private setupRoutes(): void {
    this.config.routes.forEach(route => {
      const router = express.Router();

      // Apply route-specific rate limiting
      if (route.rateLimit) {
        router.use(this.createRouteRateLimit(route.rateLimit));
      }

      // Apply caching if configured
      if (route.cache) {
        router.use(this.createCacheMiddleware(route.cache));
      }

      // Apply request transforms
      if (route.transforms) {
        route.transforms.forEach(transform => {
          router.use(this.createTransformMiddleware(transform));
        });
      }

      // Proxy to target service
      router.all('*', createProxyMiddleware({
        target: route.target,
        changeOrigin: true,
        onError: (err, req, res) => {
          console.error(`Proxy error for ${route.path}:`, err);
          (res as Response).status(502).json({ error: 'Service unavailable' });
        },
      }));

      this.app.use(route.path, router);
    });
  }

  private createRouteRateLimit(config: { windowMs: number; max: number }) {
    const requests = new Map<string, { count: number; resetTime: number }>();

    return (req: Request, res: Response, next: NextFunction) => {
      const key = `${req.ip}-${req.path}`;
      const now = Date.now();

      let record = requests.get(key);
      if (!record || now > record.resetTime) {
        record = { count: 0, resetTime: now + config.windowMs };
        requests.set(key, record);
      }

      record.count++;

      if (record.count > config.max) {
        return res.status(429).json({ error: 'Route rate limit exceeded' });
      }

      next();
    };
  }

  private createCacheMiddleware(config: { ttl: number; key?: string }) {
    return (req: Request, res: Response, next: NextFunction) => {
      if (req.method !== 'GET') {
        return next();
      }

      const cacheKey = config.key
        ? `${req.path}-${config.key}`
        : `${req.path}-${JSON.stringify(req.query)}`;

      const cached = this.cache.get(cacheKey);
      if (cached && Date.now() < cached.expiry) {
        return res.json(cached.data);
      }

      // Override res.json to cache response
      const originalJson = res.json.bind(res);
      res.json = (data: unknown) => {
        this.cache.set(cacheKey, { data, expiry: Date.now() + config.ttl });
        return originalJson(data);
      };

      next();
    };
  }

  private createTransformMiddleware(transform: RequestTransform) {
    return (req: Request, res: Response, next: NextFunction) => {
      switch (transform.type) {
        case 'add-header':
          Object.entries(transform.config).forEach(([key, value]) => {
            req.headers[key.toLowerCase()] = value;
          });
          break;
        case 'remove-header':
          Object.keys(transform.config).forEach(key => {
            delete req.headers[key.toLowerCase()];
          });
          break;
        case 'rewrite-path':
          req.url = req.url.replace(
            new RegExp(transform.config.pattern),
            transform.config.replacement
          );
          break;
        case 'add-body-field':
          if (req.body && typeof req.body === 'object') {
            Object.entries(transform.config).forEach(([key, value]) => {
              req.body[key] = value;
            });
          }
          break;
      }
      next();
    };
  }

  start(port: number): void {
    this.app.listen(port, () => {
      console.log(`API Gateway started on port ${port}`);
    });
  }
}
```

### TypeScript - Circuit Breaker Integration

```typescript
import CircuitBreaker from 'opossum';

class GatewayWithCircuitBreaker {
  private breakers: Map<string, CircuitBreaker> = new Map();

  constructor(private routes: Record<string, string>) {
    this.initializeBreakers();
  }

  private initializeBreakers(): void {
    Object.entries(this.routes).forEach(([path, target]) => {
      const breaker = new CircuitBreaker(
        async (req: express.Request) => {
          const response = await fetch(`${target}${req.url}`, {
            method: req.method,
            headers: req.headers as Record<string, string>,
            body: req.method !== 'GET' ? JSON.stringify(req.body) : undefined,
          });
          return response.json();
        },
        {
          timeout: 5000,
          errorThresholdPercentage: 50,
          resetTimeout: 30000,
        }
      );

      breaker.on('open', () => {
        console.log(`Circuit breaker OPEN for ${path}`);
      });

      breaker.on('halfOpen', () => {
        console.log(`Circuit breaker HALF-OPEN for ${path}`);
      });

      breaker.on('close', () => {
        console.log(`Circuit breaker CLOSED for ${path}`);
      });

      this.breakers.set(path, breaker);
    });
  }

  async handleRequest(
    req: express.Request,
    res: express.Response
  ): Promise<void> {
    const route = Object.keys(this.routes).find(path =>
      req.path.startsWith(path)
    );

    if (!route) {
      res.status(404).json({ error: 'Route not found' });
      return;
    }

    const breaker = this.breakers.get(route);
    if (!breaker) {
      res.status(500).json({ error: 'Circuit breaker not configured' });
      return;
    }

    try {
      const result = await breaker.fire(req);
      res.json(result);
    } catch (error) {
      if (breaker.open) {
        res.status(503).json({
          error: 'Service temporarily unavailable',
          retryAfter: 30,
        });
      } else {
        res.status(500).json({ error: 'Internal server error' });
      }
    }
  }
}
```

## Real-World Use Cases

### 1. Netflix API Gateway (Zuul)
- Routes millions of requests per second
- Dynamic routing based on request headers
- Canary deployments and A/B testing

### 2. E-Commerce Platform
- Unified checkout API aggregating inventory, pricing, payment
- Rate limiting per user tier
- Request transformation for mobile vs web clients

### 3. Banking API
- Strong authentication and authorization
- Request/response logging for compliance
- Protocol translation (REST to gRPC)

## Common Mistakes

1. **Gateway as business logic** - Keep it thin, only cross-cutting concerns
2. **No caching** - Overwhelming backend services
3. **Single point of failure** - Deploy multiple instances
4. **Ignoring timeout** - Long-running requests blocking resources
5. **Not monitoring** - Missing visibility into traffic patterns
6. **Hardcoded routes** - Use configuration or service discovery
7. **Missing rate limiting** - Vulnerable to abuse
8. **No request validation** - Passing invalid data to services

## Best Practices

1. **Keep gateway thin** - Business logic belongs in services
2. **Implement circuit breakers** - Prevent cascade failures
3. **Use caching** - Reduce load on backend services
4. **Monitor everything** - Latency, error rates, throughput
5. **Version your APIs** - Support multiple API versions
6. **Implement request validation** - Reject bad requests early
7. **Use async processing** - For long-running operations
8. **Deploy redundantly** - Avoid single point of failure

## Performance Considerations

- **Connection pooling** - Reuse connections to backend services
- **Response compression** - gzip/brotli for large payloads
- **Request batching** - Combine multiple requests when possible
- **CDN integration** - Cache static responses at edge
- **Load balancing** - Distribute across gateway instances

## Interview Questions

### Beginner (5-10)

1. **What is an API Gateway?**
   - Single entry point for all client requests, handling cross-cutting concerns.

2. **Why use an API Gateway?**
   - Centralizes auth, rate limiting, routing; simplifies client interaction.

3. **What are common API Gateway features?**
   - Routing, authentication, rate limiting, caching, request transformation.

4. **How does API Gateway differ from load balancer?**
   - Gateway handles application logic; load balancer distributes traffic.

5. **What is request transformation?**
   - Modifying request/response format between client and service.

6. **How does rate limiting work?**
   - Tracks requests per client/IP and blocks excess requests.

7. **What is backend for frontend (BFF)?**
   - Separate API Gateway for each client type (web, mobile, etc.).

8. **Name popular API Gateway solutions.**
   - Kong, AWS API Gateway, Azure API Management, Zuul.

### Intermediate (5-10)

9. **How do you implement authentication in API Gateway?**
   - JWT validation, OAuth2, API keys at gateway level.

10. **What is circuit breaker pattern in gateway?**
    - Prevents cascade failures by stopping requests to failing services.

11. **How do you handle long-running requests?**
    - Async processing, webhooks, or polling pattern.

12. **What is request/response caching?**
    - Caching responses to reduce backend load and latency.

13. **How do you implement API versioning?**
    - URL path (/v1/), header, or query parameter versioning.

14. **What is canary deployment?**
    - Routing small percentage of traffic to new version for testing.

15. **How do you handle service discovery with gateway?**
    - Gateway queries service registry for dynamic routing.

16. **What metrics should you monitor?**
    - Request rate, error rate, latency, throughput, circuit breaker state.

### Senior (10-15)

17. **Design a highly available API Gateway.**
    - Multiple instances, health checks, failover, no single point of failure.

18. **How do you prevent gateway from becoming bottleneck?**
    - Caching, async processing, horizontal scaling, efficient routing.

19. **Explain gateway pattern in microservices.**
    - Edge service handling cross-cutting concerns, protocol translation.

20. **How do you handle gateway during deployments?**
    - Blue/green deployments, traffic shifting, rollback mechanisms.

21. **What is API composition pattern?**
    - Gateway aggregates data from multiple services into single response.

22. **How do you implement request validation?**
    - JSON Schema validation, OpenAPI specifications, middleware validation.

23. **Explain distributed tracing in gateway context.**
    - Propagate trace IDs through gateway to all backend services.

24. **How do you handle multi-region gateway?**
    - Regional gateways, global load balancing, DNS-based routing.

25. **What security considerations exist for gateway?**
    - DDoS protection, WAF integration, input sanitization, HTTPS.

### FAANG-style (5-10)

26. **Design Netflix's Zuul gateway.**
    - Dynamic routing, filters, canary deployments, failure recovery.

27. **How would you handle 1M requests/second?**
    - Horizontal scaling, caching, connection pooling, async processing.

28. **Design gateway for GraphQL federation.**
    - Schema stitching, query planning, distributed resolvers.

29. **How do you implement gateway for gRPC services?**
    - gRPC-JSON transcoding, protocol translation, load balancing.

30. **Explain gateway in service mesh architecture.**
    - Gateway handles north-south traffic; service mesh handles east-west.

### Follow-ups (5-10)

31. **How do you migrate from monolith gateway to microservices?**
    - Strangler fig pattern, gradual route extraction.

32. **What is the impact of gateway on latency?**
    - Additional hop, but benefits outweigh costs with proper optimization.

33. **How do you test API Gateway?**
    - Integration tests, load testing, chaos engineering.

34. **How do you handle gateway for WebSocket connections?**
    - Persistent connections, sticky sessions, message routing.

35. **What is the future of API Gateway?**
    - Serverless gateways, edge computing, AI-driven routing.

## Summary

API Gateway is essential for microservices architecture, providing a unified entry point with centralized cross-cutting concerns. Key features include routing, authentication, rate limiting, and request transformation. Proper implementation ensures security, performance, and maintainability.

## Cheat Sheet

```
┌─────────────────────────────────────────────────────────┐
│                    API GATEWAY                          │
├─────────────────────────────────────────────────────────┤
│ ENTRY POINT: Single interface for all clients           │
│                                                         │
│ KEY FEATURES:                                           │
│ • Routing: Direct requests to appropriate services      │
│ • Authentication: Verify client identity                │
│ • Rate Limiting: Prevent abuse                          │
│ • Caching: Reduce backend load                          │
│ • Request Transformation: Format conversion             │
│ • Load Balancing: Distribute traffic                    │
│                                                         │
│ PATTERNS:                                               │
│ • BFF: Backend for Frontend (per client type)           │
│ • Circuit Breaker: Prevent cascade failures             │
│ • API Composition: Aggregate multiple services          │
│                                                         │
│ BEST PRACTICES:                                         │
│ • Keep gateway thin (no business logic)                 │
│ • Deploy redundantly                                    │
│ • Monitor latency and errors                            │
│ • Use caching aggressively                              │
│ • Implement circuit breakers                            │
│ • Version your APIs                                     │
└─────────────────────────────────────────────────────────┘
```

---

## References & Learn More
- [Microservices Patterns by Chris Richardson](https://www.amazon.com/Microservices-Patterns-designing-Chris-Richardson/dp/1617294543)
- [Building Microservices by Sam Newman](https://www.amazon.com/Building-Microservices-designing-Systems/dp/1491950358)
- [Microservices.io](https://microservices.io/)
- [Martin Fowler - Microservices](https://martinfowler.com/microservices/)
- [Domain-Driven Design by Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)