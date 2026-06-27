# Rate Limiting

## Definition

Rate limiting is a technique used to control the number of requests a client can make to an API within a specified time period. It protects APIs from abuse, ensures fair usage, prevents resource exhaustion, and maintains service availability for all users.

## Why Do We Need It?

Without rate limiting:

1. **Service degradation** - Overwhelmed servers become slow or unresponsive
2. **Resource exhaustion** - Database, memory, CPU depleted
3. **Unfair usage** - One client monopolizes resources
4. **Cost overruns** - Unexpected infrastructure costs
5. **Security vulnerabilities** - DDoS attacks, brute force attempts

## How It Works

### Rate Limiting Algorithms

```
Rate Limiting Algorithms
════════════════════════

1. Fixed Window
   Time: [----10:00----11:00----]
   Limit: 100 requests per hour
   Count: ████░░░░░░ 40/100

2. Sliding Window
   Time: [----10:00----11:00----]
   Limit: 100 requests per hour
   Sliding: ████░░░░░░ 40 in last hour

3. Token Bucket
   Bucket: 10 tokens
   Refill: 1 token/second
   Requests: Consume tokens

4. Leaky Bucket
   Bucket: 10 tokens
   Leak: 1 token/second
   Requests: Queue if full
```

### Fixed Window Algorithm

```
Fixed Window
════════════

Time Window: 1 hour (10:00 - 11:00)
Limit: 100 requests

10:00:00  Request 1   Count: 1   ✓
10:15:00  Request 2   Count: 2   ✓
10:30:00  Request 50  Count: 50  ✓
10:45:00  Request 100 Count: 100 ✓
10:59:00  Request 101 Count: 101 ✗ Rate limited
11:00:00  Window resets
11:01:00  Request 1   Count: 1   ✓
```

```typescript
// Fixed window implementation
class FixedWindowRateLimiter {
  private windows: Map<string, { count: number; resetTime: number }> = new Map();
  
  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}
  
  isAllowed(key: string): { allowed: boolean; remaining: number; resetTime: number } {
    const now = Date.now();
    const window = this.windows.get(key);
    
    if (!window || now > window.resetTime) {
      // New window
      this.windows.set(key, {
        count: 1,
        resetTime: now + this.windowMs
      });
      return { allowed: true, remaining: this.maxRequests - 1, resetTime: now + this.windowMs };
    }
    
    if (window.count >= this.maxRequests) {
      // Rate limited
      return { allowed: false, remaining: 0, resetTime: window.resetTime };
    }
    
    // Increment count
    window.count++;
    return { allowed: true, remaining: this.maxRequests - window.count, resetTime: window.resetTime };
  }
}

// Express middleware
function fixedWindowLimiter(maxRequests: number, windowMs: number) {
  const limiter = new FixedWindowRateLimiter(maxRequests, windowMs);
  
  return (req, res, next) => {
    const key = req.ip || req.connection.remoteAddress;
    const result = limiter.isAllowed(key);
    
    res.set({
      'X-RateLimit-Limit': maxRequests.toString(),
      'X-RateLimit-Remaining': result.remaining.toString(),
      'X-RateLimit-Reset': Math.ceil(result.resetTime / 1000).toString()
    });
    
    if (!result.allowed) {
      res.set('Retry-After', Math.ceil((result.resetTime - Date.now()) / 1000).toString());
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    next();
  };
}

// Usage
app.use('/api', fixedWindowLimiter(100, 60 * 60 * 1000)); // 100 requests per hour
```

### Sliding Window Algorithm

```
Sliding Window
══════════════

Time: 10:30 (looking back 1 hour)

Requests in window:
10:05 ✓
10:15 ✓
10:20 ✓
10:25 ✓
10:30 ✓

Total: 5 requests in last hour
Limit: 100 requests per hour
Result: ✓ Allowed (95 remaining)

Advantages over fixed window:
- No boundary burst issues
- More accurate counting
- Smoother rate limiting
```

```typescript
// Sliding window implementation
class SlidingWindowRateLimiter {
  private requests: Map<string, number[]> = new Map();
  
  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}
  
  isAllowed(key: string): { allowed: boolean; remaining: number } {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // Get existing requests for this key
    const requestTimes = this.requests.get(key) || [];
    
    // Filter to only requests within the window
    const validRequests = requestTimes.filter(time => time > windowStart);
    
    if (validRequests.length >= this.maxRequests) {
      return { allowed: false, remaining: 0 };
    }
    
    // Add current request
    validRequests.push(now);
    this.requests.set(key, validRequests);
    
    return { allowed: true, remaining: this.maxRequests - validRequests.length };
  }
  
  // Cleanup old entries
  cleanup() {
    const now = Date.now();
    for (const [key, times] of this.requests.entries()) {
      const validTimes = times.filter(time => time > now - this.windowMs);
      if (validTimes.length === 0) {
        this.requests.delete(key);
      } else {
        this.requests.set(key, validTimes);
      }
    }
  }
}

// Express middleware
function slidingWindowLimiter(maxRequests: number, windowMs: number) {
  const limiter = new SlidingWindowRateLimiter(maxRequests, windowMs);
  
  // Cleanup every minute
  setInterval(() => limiter.cleanup(), 60000);
  
  return (req, res, next) => {
    const key = req.ip || req.connection.remoteAddress;
    const result = limiter.isAllowed(key);
    
    res.set({
      'X-RateLimit-Limit': maxRequests.toString(),
      'X-RateLimit-Remaining': result.remaining.toString()
    });
    
    if (!result.allowed) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    next();
  };
}
```

### Token Bucket Algorithm

```
Token Bucket
═════════════

Bucket Capacity: 10 tokens
Refill Rate: 1 token/second

Initial: [██████████] 10/10

Request 1: [█████████░] 9/10  ✓
Request 2: [████████░░] 8/10  ✓
Request 3: [███████░░░] 7/10  ✓
Request 4: [██████░░░░] 6/10  ✓
Request 5: [█████░░░░░] 5/10  ✓
Request 6: [████░░░░░░] 4/10  ✓
Request 7: [███░░░░░░░] 3/10  ✓
Request 8: [██░░░░░░░░] 2/10  ✓
Request 9: [█░░░░░░░░░] 1/10  ✓
Request 10: [░░░░░░░░░░] 0/10  ✓
Request 11: [░░░░░░░░░░] 0/10  ✗ Rate limited

After 5 seconds: [█████░░░░░] 5/10  (refilled 5 tokens)
```

```typescript
// Token bucket implementation
class TokenBucketRateLimiter {
  private buckets: Map<string, { tokens: number; lastRefill: number }> = new Map();
  
  constructor(
    private capacity: number,
    private refillRate: number, // tokens per second
    private refillInterval: number = 1000 // ms
  ) {}
  
  isAllowed(key: string): { allowed: boolean; tokens: number } {
    const now = Date.now();
    let bucket = this.buckets.get(key);
    
    if (!bucket) {
      bucket = { tokens: this.capacity, lastRefill: now };
      this.buckets.set(key, bucket);
    }
    
    // Refill tokens
    const timePassed = now - bucket.lastRefill;
    const tokensToAdd = Math.floor(timePassed / this.refillInterval) * this.refillRate;
    bucket.tokens = Math.min(this.capacity, bucket.tokens + tokensToAdd);
    bucket.lastRefill = now;
    
    if (bucket.tokens <= 0) {
      return { allowed: false, tokens: 0 };
    }
    
    // Consume token
    bucket.tokens--;
    return { allowed: true, tokens: bucket.tokens };
  }
}

// Express middleware
function tokenBucketLimiter(capacity: number, refillRate: number) {
  const limiter = new TokenBucketRateLimiter(capacity, refillRate);
  
  return (req, res, next) => {
    const key = req.ip || req.connection.remoteAddress;
    const result = limiter.isAllowed(key);
    
    res.set({
      'X-RateLimit-Limit': capacity.toString(),
      'X-RateLimit-Remaining': result.tokens.toString()
    });
    
    if (!result.allowed) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    next();
  };
}
```

### Sliding Window Log Algorithm

```typescript
// Sliding window log - stores timestamps
class SlidingWindowLogRateLimiter {
  private logs: Map<string, number[]> = new Map();
  
  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}
  
  isAllowed(key: string): { allowed: boolean; remaining: number; retryAfter?: number } {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // Get and filter logs
    const logs = (this.logs.get(key) || []).filter(t => t > windowStart);
    
    if (logs.length >= this.maxRequests) {
      const oldestInWindow = logs[0];
      const retryAfter = oldestInWindow + this.windowMs - now;
      return { allowed: false, remaining: 0, retryAfter };
    }
    
    logs.push(now);
    this.logs.set(key, logs);
    
    return { allowed: true, remaining: this.maxRequests - logs.length };
  }
}
```

## Code Examples

### Complete Rate Limiting System

```typescript
import express, { Request, Response, NextFunction } from 'express';
import Redis from 'ioredis';

// Redis-based distributed rate limiter
class RedisRateLimiter {
  private redis: Redis;
  
  constructor(redis: Redis) {
    this.redis = redis;
  }
  
  // Sliding window with Redis
  async isAllowed(
    key: string,
    maxRequests: number,
    windowMs: number
  ): Promise<{ allowed: boolean; remaining: number; resetTime: number }> {
    const now = Date.now();
    const windowStart = now - windowMs;
    const redisKey = `ratelimit:${key}`;
    
    const pipeline = this.redis.pipeline();
    
    // Remove old entries
    pipeline.zremrangebyscore(redisKey, 0, windowStart);
    
    // Add current request
    pipeline.zadd(redisKey, now.toString(), `${now}-${Math.random()}`);
    
    // Count requests in window
    pipeline.zcard(redisKey);
    
    // Set expiry
    pipeline.expire(redisKey, Math.ceil(windowMs / 1000));
    
    const results = await pipeline.exec();
    const count = results[2][1] as number;
    
    // Calculate reset time
    const resetTime = now + windowMs;
    
    if (count > maxRequests) {
      return { allowed: false, remaining: 0, resetTime };
    }
    
    return { allowed: true, remaining: maxRequests - count, resetTime };
  }
  
  // Token bucket with Redis
  async isAllowedTokenBucket(
    key: string,
    capacity: number,
    refillRate: number
  ): Promise<{ allowed: boolean; tokens: number }> {
    const now = Date.now();
    const bucketKey = `bucket:${key}`;
    
    const bucket = await this.redis.hgetall(bucketKey);
    
    let tokens = bucket.tokens ? parseFloat(bucket.tokens) : capacity;
    let lastRefill = bucket.lastRefill ? parseInt(bucket.lastRefill) : now;
    
    // Refill tokens
    const timePassed = now - lastRefill;
    const tokensToAdd = (timePassed / 1000) * refillRate;
    tokens = Math.min(capacity, tokens + tokensToAdd);
    
    if (tokens < 1) {
      return { allowed: false, tokens: Math.floor(tokens) };
    }
    
    // Consume token
    tokens -= 1;
    
    // Update Redis
    await this.redis.hset(bucketKey, {
      tokens: tokens.toString(),
      lastRefill: now.toString()
    });
    await this.redis.expire(bucketKey, Math.ceil(capacity / refillRate) * 2);
    
    return { allowed: true, tokens: Math.floor(tokens) };
  }
}

// Rate limiting middleware factory
function rateLimiter(options: {
  windowMs: number;
  max: number;
  keyGenerator?: (req: Request) => string;
  handler?: (req: Request, res: Response) => void;
  skip?: (req: Request) => boolean;
  message?: string;
}) {
  const {
    windowMs,
    max,
    keyGenerator = (req) => req.ip || 'unknown',
    handler,
    skip = () => false,
    message = 'Too many requests'
  } = options;
  
  const redis = new Redis(process.env.REDIS_URL);
  const limiter = new RedisRateLimiter(redis);
  
  return async (req: Request, res: Response, next: NextFunction) => {
    if (skip(req)) {
      return next();
    }
    
    const key = keyGenerator(req);
    
    try {
      const result = await limiter.isAllowed(key, max, windowMs);
      
      // Set rate limit headers
      res.set({
        'X-RateLimit-Limit': max.toString(),
        'X-RateLimit-Remaining': Math.max(0, result.remaining).toString(),
        'X-RateLimit-Reset': Math.ceil(result.resetTime / 1000).toString()
      });
      
      if (!result.allowed) {
        const retryAfter = Math.ceil((result.resetTime - Date.now()) / 1000);
        res.set('Retry-After', retryAfter.toString());
        
        if (handler) {
          return handler(req, res);
        }
        
        return res.status(429).json({
          error: message,
          retryAfter
        });
      }
      
      next();
    } catch (err) {
      // If rate limiting fails, allow request (fail open)
      console.error('Rate limiting error:', err);
      next();
    }
  };
}

// Usage examples
app.use('/api',
  rateLimiter({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // 100 requests per 15 minutes
    keyGenerator: (req) => req.ip
  })
);

// Different limits for different endpoints
app.use('/api/auth',
  rateLimiter({
    windowMs: 15 * 60 * 1000,
    max: 10, // 10 login attempts per 15 minutes
    keyGenerator: (req) => req.ip,
    message: 'Too many login attempts'
  })
);

app.use('/api/search',
  rateLimiter({
    windowMs: 60 * 1000, // 1 minute
    max: 30, // 30 searches per minute
    keyGenerator: (req) => req.user?.id || req.ip,
    skip: (req) => req.user?.role === 'admin'
  })
);
```

### Tiered Rate Limiting

```typescript
// Different rate limits for different user tiers
class TieredRateLimiter {
  private tiers = {
    free: { requests: 100, windowMs: 60 * 60 * 1000 }, // 100/hour
    pro: { requests: 1000, windowMs: 60 * 60 * 1000 }, // 1000/hour
    enterprise: { requests: 10000, windowMs: 60 * 60 * 1000 } // 10000/hour
  };
  
  async isAllowed(userId: string, tier: string): Promise<{ allowed: boolean; remaining: number }> {
    const tierConfig = this.tiers[tier] || this.tiers.free;
    const key = `ratelimit:${tier}:${userId}`;
    
    const result = await this.redisRateLimiter.isAllowed(
      key,
      tierConfig.requests,
      tierConfig.windowMs
    );
    
    return result;
  }
}

// Middleware
function tieredRateLimiter(req: Request, res: Response, next: NextFunction) {
  const userTier = req.user?.tier || 'free';
  const limiter = new TieredRateLimiter();
  
  limiter.isAllowed(req.user.id, userTier)
    .then(result => {
      res.set({
        'X-RateLimit-Limit': limiter.tiers[userTier].requests.toString(),
        'X-RateLimit-Remaining': result.remaining.toString(),
        'X-RateLimit-Tier': userTier
      });
      
      if (!result.allowed) {
        return res.status(429).json({
          error: 'Rate limit exceeded',
          tier: userTier,
          upgradeUrl: '/pricing'
        });
      }
      
      next();
    });
}
```

### Rate Limit Headers

```typescript
// Standard rate limit response headers
app.use('/api', (req, res, next) => {
  // After rate limiting is applied, these headers are set:
  // X-RateLimit-Limit: Maximum requests per window
  // X-RateLimit-Remaining: Remaining requests in window
  // X-RateLimit-Reset: Unix timestamp when window resets
  // Retry-After: Seconds to wait (only on 429)
  
  next();
});

// Example response on 429
res.status(429).json({
  error: 'Rate limit exceeded',
  message: 'You have exceeded the rate limit. Please wait before making another request.',
  retryAfter: 60,
  documentation: 'https://api.example.com/docs/rate-limiting'
});
```

## Real-World Use Cases

### 1. Public API Rate Limiting

```typescript
// Different limits for different API endpoints
const rateLimits = {
  '/api/public/data': { max: 1000, windowMs: 60 * 60 * 1000 }, // 1000/hour
  '/api/public/search': { max: 100, windowMs: 60 * 1000 }, // 100/minute
  '/api/public/export': { max: 10, windowMs: 24 * 60 * 60 * 1000 } // 10/day
};

Object.entries(rateLimits).forEach(([path, config]) => {
  app.use(path, rateLimiter(config));
});
```

### 2. User-Specific Rate Limiting

```typescript
// Rate limit per user
app.use('/api', rateLimiter({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => req.user?.id || req.ip,
  skip: (req) => req.user?.role === 'admin'
}));

// Different limits for different user actions
app.post('/api/messages', rateLimiter({
  windowMs: 60 * 1000,
  max: 30, // 30 messages per minute
  keyGenerator: (req) => req.user.id
}));

app.post('/api/uploads', rateLimiter({
  windowMs: 60 * 60 * 1000,
  max: 5, // 5 uploads per hour
  keyGenerator: (req) => req.user.id
}));
```

### 3. Distributed Rate Limiting

```typescript
// Redis-based distributed rate limiting
const redis = new Redis(process.env.REDIS_URL);
const limiter = new RedisRateLimiter(redis);

// Consistent rate limiting across multiple servers
app.use('/api', async (req, res, next) => {
  const key = req.ip;
  const result = await limiter.isAllowed(key, 100, 60 * 60 * 1000);
  
  if (!result.allowed) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  
  next();
});
```

### 4. API Key Based Rate Limiting

```typescript
// Rate limit by API key
app.use('/api', rateLimiter({
  windowMs: 60 * 60 * 1000,
  max: 1000,
  keyGenerator: (req) => req.headers['x-api-key'] as string || req.ip
}));

// Different limits for different API keys
const apiKeyLimits = new Map([
  ['key-free', { max: 100, windowMs: 60 * 60 * 1000 }],
  ['key-pro', { max: 1000, windowMs: 60 * 60 * 1000 }],
  ['key-enterprise', { max: 10000, windowMs: 60 * 60 * 1000 }]
]);
```

## Common Mistakes

### 1. Not Including Rate Limit Headers

```typescript
// ❌ Bad: No headers
res.status(429).json({ error: 'Rate limited' });

// ✅ Good: Include headers
res.set({
  'X-RateLimit-Limit': '100',
  'X-RateLimit-Remaining': '0',
  'X-RateLimit-Reset': '1735689600',
  'Retry-After': '60'
});
res.status(429).json({ error: 'Rate limited' });
```

### 2. Not Failing Open

```typescript
// ❌ Bad: Block on error
try {
  const allowed = await checkRateLimit(key);
  if (!allowed) return res.status(429);
  next();
} catch (err) {
  return res.status(500); // Blocks all requests if rate limiter fails
}

// ✅ Good: Fail open
try {
  const allowed = await checkRateLimit(key);
  if (!allowed) return res.status(429);
  next();
} catch (err) {
  console.error('Rate limiter error:', err);
  next(); // Allow request if rate limiter fails
}
```

### 3. Rate Limiting by Wrong Key

```typescript
// ❌ Bad: Rate limit only by IP (doesn't work for authenticated users)
keyGenerator: (req) => req.ip

// ✅ Good: Rate limit by user ID or API key
keyGenerator: (req) => req.user?.id || req.headers['x-api-key'] || req.ip
```

### 4. Not Considering Distributed Systems

```typescript
// ❌ Bad: In-memory rate limiting (doesn't work across servers)
const requests = new Map<string, number[]>();

// ✅ Good: Redis-based rate limiting
const redis = new Redis();
```

### 5. Not Providing Retry Information

```typescript
// ❌ Bad: No retry guidance
res.status(429).json({ error: 'Rate limited' });

// ✅ Good: Include retry information
res.set('Retry-After', '60');
res.status(429).json({
  error: 'Rate limited',
  retryAfter: 60,
  message: 'Please wait 60 seconds before retrying'
});
```

## Best Practices

1. **Always return rate limit headers** - X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
2. **Include Retry-After on 429** - Tell clients when to retry
3. **Fail open** - Don't block requests if rate limiter fails
4. **Use distributed storage** - Redis for multi-server setups
5. **Different limits per tier** - Free, Pro, Enterprise
6. **Different limits per endpoint** - Heavy endpoints get lower limits
7. **Consider user authentication** - Rate limit by user ID, not just IP
8. **Document rate limits** - Clear API documentation
9. **Monitor rate limiting** - Track 429 responses
10. **Provide upgrade path** - Link to pricing for higher limits

## Performance Considerations

- **Redis performance** - Use pipelining for multiple operations
- **Local caching** - Cache rate limit state locally with periodic sync
- **Approximate algorithms** - Use probabilistic data structures for high throughput
- **Connection pooling** - Reuse Redis connections
- **Async processing** - Don't block on rate limit checks

## Interview Questions

### Beginner (5)

1. **What is rate limiting?** - Controlling the number of requests a client can make within a time period.

2. **Why do we need rate limiting?** - Prevent abuse, ensure fair usage, protect server resources.

3. **What HTTP status code indicates rate limiting?** - 429 Too Many Requests.

4. **What headers are used for rate limiting?** - X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After.

5. **What is the difference between rate limiting and throttling?** - Rate limiting: hard cap; Throttling: slows down requests.

### Intermediate (5)

6. **Explain token bucket algorithm** - Tokens added at fixed rate, requests consume tokens, allows bursts.

7. **What is the sliding window algorithm?** - Counts requests in a moving time window, more accurate than fixed window.

8. **How do you implement distributed rate limiting?** - Use Redis or similar distributed store for consistent counting.

9. **How do you rate limit authenticated vs unauthenticated users?** - Different limits based on user ID or API key.

10. **What is the Retry-After header?** - Tells client how many seconds to wait before retrying.

### Senior (10)

11. **Design a rate limiting system for a global API** - Regional rate limits, consistent counting across regions.

12. **How do you handle rate limiting in microservices?** - Centralized rate limiter or distributed with eventual consistency.

13. **Design rate limiting with multiple dimensions** - Per user, per endpoint, per IP, per API key.

14. **How do you test rate limiting?** - Load testing, verifying 429 responses, checking header accuracy.

15. **Design adaptive rate limiting** - Adjust limits based on server load, time of day, user behavior.

16. **How do you handle rate limiting for webhooks?** - Separate limits, retry queues, exponential backoff.

17. **Design rate limiting for batch operations** - Cost-based limiting, request weighting.

18. **How do you handle rate limiting during incidents?** - Graceful degradation, priority queues, emergency limits.

19. **Design rate limiting analytics** - Track usage patterns, detect abuse, capacity planning.

20. **How do you communicate rate limits to clients?** - Documentation, headers, error responses, developer portal.

### FAANG-style (5)

21. **Design a globally distributed rate limiting system** - Consistent hashing, regional counters, conflict resolution.

22. **Design rate limiting for a multi-tenant SaaS** - Tenant isolation, fair usage, burst handling.

23. **How would you implement rate limiting for GraphQL?** - Query complexity analysis, depth limiting, field-level limits.

24. **Design rate limiting with ML-based detection** - Anomaly detection, adaptive thresholds, abuse patterns.

25. **Design a rate limiting system that scales to millions of users** - Approximate algorithms, probabilistic data structures.

### Follow-ups (5)

26. **What are the tradeoffs between different algorithms?** - Fixed window: simple but bursty; Sliding window: accurate but complex.

27. **How do you handle rate limiting for long-running requests?** - Separate limits, timeout handling, progress callbacks.

28. **What is the impact of rate limiting on user experience?** - Frustration, lost revenue, but necessary for stability.

29. **How do you handle rate limiting for different HTTP methods?** - Separate limits for GET, POST, PUT, DELETE.

30. **How do you handle rate limiting in serverless architectures?** - Distributed state, cold start considerations, provider limits.

## Summary

Rate limiting is essential for API protection and fair usage. Token bucket is the most flexible algorithm, allowing bursts while maintaining average rates. Always include rate limit headers and Retry-After on 429 responses. Use distributed storage for multi-server setups and consider tiered limits for different user plans.

## Cheat Sheet

| Algorithm | Burst Handling | Accuracy | Complexity |
|-----------|---------------|----------|------------|
| Fixed Window | Poor | Medium | Low |
| Sliding Window | Good | High | Medium |
| Token Bucket | Excellent | High | Medium |
| Leaky Bucket | Poor | High | High |

## References & Learn More

- [Rate Limiting Patterns and Best Practices - Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#74-rate-limiting)
- [Token Bucket Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Token_bucket)
- [Sliding Window Rate Limiting - Cloudflare Blog](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
- [Zalando RESTful API Guidelines - Rate Limits](https://opensource.zalando.com/restful-api-guidelines/#rate-limiting)
- [Stripe Rate Limiting Strategy](https://stripe.com/blog/rate-limiters)
