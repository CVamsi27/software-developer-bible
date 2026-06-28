# URL Shortener System Design

## Requirements
### Functional Requirements
- Given a long URL, generate a short URL
- Given a short URL, redirect to original URL
- Users can create custom aliases for short URLs
- URLs can have expiration dates
- Track click analytics (count, timestamp, location, device)
- Support both authenticated and unauthenticated users
- API for URL creation, retrieval, and analytics

### Non-Functional Requirements
- High availability (99.99% uptime)
- Low latency redirect (< 10ms)
- Short URLs should not be predictable
- System should handle 100M URLs created per day
- 1B redirects per day at peak
- URL mappings should persist indefinitely (unless expired)
- Analytics data retained for 1 year minimum

## Capacity Estimation
```
Storage Estimates:
- 100M new URLs/day = ~1.16K URLs/second
- 1B redirects/day = ~11.6K requests/second
- Each URL record: ~500 bytes
- 100M URLs/day × 365 days × 5 years = ~182.5B URLs
- Storage: 182.5B × 500 bytes = ~91.25 TB

Bandwidth Estimates:
- Write: 1.16K × 500 bytes = ~580 KB/s
- Read: 11.6K × 500 bytes = ~5.8 MB/s (assuming 10:1 read/write ratio)

Cache Estimates:
- 20% of daily traffic = 200M requests/day
- Cache size: 200M × 500 bytes = ~100 GB
- Use Redis cluster with multiple shards
```

## API Design
```yaml
POST /api/v1/urls
  Request:
    {
      "long_url": "https://example.com/very/long/path?with=params",
      "custom_alias": "my-link",          // optional
      "expiration_date": "2025-12-31",    // optional
      "user_id": "usr_123"                // optional
    }
  Response:
    {
      "short_url": "https://short.ly/abc123",
      "long_url": "https://example.com/very/long/path?with=params",
      "created_at": "2025-01-15T10:30:00Z",
      "expires_at": "2025-12-31T23:59:59Z"
    }

GET /{short_code}
  Response: 301/302 redirect to original URL

GET /api/v1/urls/{short_code}/analytics
  Response:
    {
      "short_code": "abc123",
      "total_clicks": 15234,
      "clicks_by_day": [...],
      "clicks_by_country": {...},
      "clicks_by_device": {...}
    }

DELETE /api/v1/urls/{short_code}
  Response: 204 No Content
```

## Database Design
### Schema
```sql
-- Core URL table
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    user_id BIGINT REFERENCES users(id),
    custom_alias VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    click_count BIGINT DEFAULT 0
);

CREATE INDEX idx_urls_short_code ON urls(short_code);
CREATE INDEX idx_urls_user_id ON urls(user_id);
CREATE INDEX idx_urls_expires_at ON urls(expires_at);

-- Click analytics table (partitioned by month)
CREATE TABLE click_analytics (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(10) NOT NULL,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    country VARCHAR(2),
    device_type VARCHAR(20),
    browser VARCHAR(50),
    referer TEXT
) PARTITION BY RANGE (clicked_at);

-- Create monthly partitions
CREATE TABLE click_analytics_2025_01 PARTITION OF click_analytics
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- User table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE
);
```

### ER Diagram (ASCII)
```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users     │     │      urls       │     │ click_analytics │
├─────────────┤     ├─────────────────┤     ├─────────────────┤
│ id (PK)     │◄────│ user_id (FK)    │     │ id (PK)         │
│ email       │     │ id (PK)         │◄────│ short_code (FK) │
│ name        │     │ short_code (UK) │     │ clicked_at      │
│ api_key     │     │ long_url        │     │ ip_address      │
│ created_at  │     │ custom_alias    │     │ country         │
│ is_verified │     │ created_at      │     │ device_type     │
└─────────────┘     │ expires_at      │     │ browser         │
                    │ is_active       │     │ referer         │
                    │ click_count     │     └─────────────────┘
                    └─────────────────┘
```

## Architecture
### ASCII Architecture Diagram
```
                          ┌──────────────┐
                          │   Clients    │
                          │  (Browser,   │
                          │   Mobile)    │
                          └──────┬───────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │ Load Balancer│
                         │  (Nginx/ALB) │
                         └──────┬───────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ App Node │   │ App Node │   │ App Node │
        │    1     │   │    2     │   │    N     │
        └────┬─────┘   └────┬─────┘   └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │    Redis     │  │  PostgreSQL  │  │   Kafka      │
   │   Cluster    │  │   Cluster    │  │  Cluster     │
   │  (Cache)     │  │  (Primary)   │  │ (Analytics)  │
   └──────────────┘  └──────────────┘  └──────────────┘
                           │
                           ▼
                   ┌──────────────┐
                   │  Analytics   │
                   │   Workers    │
                   └──────────────┘
```

## Key Components

### Hash Generation Service
```python
import hashlib
import base64

class HashGenerator:
    def __init__(self):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.base = len(self.alphabet)

    def generate_hash(self, long_url: str) -> str:
        # Use MD5 for speed, take first 7 characters
        hash_hex = hashlib.md5(long_url.encode()).hexdigest()
        hash_int = int(hash_hex[:12], 16)

        # Convert to base62
        short_code = []
        while hash_int > 0 and len(short_code) < 7:
            hash_int, remainder = divmod(hash_int, self.base)
            short_code.append(self.alphabet[remainder])

        return ''.join(reversed(short_code))

    def generate_with_collision_check(self, long_url: str, db) -> str:
        max_attempts = 10
        for _ in range(max_attempts):
            short_code = self.generate_hash(long_url)
            if not db.check_exists(short_code):
                return short_code
            # Add random salt for collision
            long_url += str(uuid.uuid4())

        raise Exception("Could not generate unique short code")
```

### Rate Limiter
```python
from redis import Redis
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def is_allowed(self, user_id: str, limit: int = 100,
                   window: int = 3600) -> bool:
        key = f"rate_limit:{user_id}"

        current = self.redis.get(key)
        if current and int(current) >= limit:
            return False

        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        pipe.execute()

        return True
```

## Caching Strategy (Redis)

### Cache Architecture
```python
class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 86400  # 24 hours

    async def get_url(self, short_code: str) -> Optional[str]:
        # L1: In-memory LRU cache (per instance)
        cached = self.local_cache.get(short_code)
        if cached:
            return cached

        # L2: Redis distributed cache
        long_url = await self.redis.get(f"url:{short_code}")
        if long_url:
            self.local_cache.set(short_code, long_url, ttl=300)
            return long_url

        # L3: Database
        long_url = await self.db.get_url(short_code)
        if long_url:
            await self.redis.setex(
                f"url:{short_code}",
                self.default_ttl,
                long_url
            )
            self.local_cache.set(short_code, long_url, ttl=300)
            return long_url

        return None
```

### Cache Invalidation Strategy
- Write-through for new URL creation
- TTL-based expiration aligned with URL expiration
- Cache-aside pattern for reads
- Background refresh for hot keys
- Event-driven invalidation via Kafka for analytics updates

## Message Queue (Kafka)

### Topics and Consumers
```
Topics:
├── url.created       (new URL creation events)
├── url.clicked       (click events for analytics)
├── url.expired       (URL expiration events)
└── analytics.process (processed analytics data)

Consumers:
├── analytics-worker   → processes click events
├── cache-warmer       → pre-populates cache for hot URLs
└── cleanup-worker     → removes expired URLs
```

### Click Event Processing
```python
class ClickEventProcessor:
    def __init__(self, kafka_consumer, db, cache):
        self.consumer = kafka_consumer
        self.db = db
        self.cache = cache

    async def process_click(self, event: dict):
        # Store in analytics table (async, non-blocking)
        await self.db.insert_click_analytics(
            short_code=event['short_code'],
            ip_address=event['ip'],
            user_agent=event['user_agent'],
            country=event['country']
        )

        # Update click count in cache
        await self.cache.incr(f"clicks:{event['short_code']}")

        # Batch write to analytics database every 1000 events
        if self.batch_counter >= 1000:
            await self.flush_analytics_batch()
```

## Scaling Strategy

### Horizontal Scaling
```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
│  (Round-robin with health checks, sticky sessions off)  │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   App Pool   │   │   App Pool   │   │   App Pool   │
│   (5-20)     │   │   (5-20)     │   │   (5-20)     │
└──────────────┘   └──────────────┘   └──────────────┘
```

### Database Sharding
```python
class ShardRouter:
    def __init__(self, shards: List[str]):
        self.shards = shards

    def get_shard(self, short_code: str) -> str:
        # Consistent hashing for shard routing
        hash_val = mmh3.hash(short_code)
        shard_index = hash_val % len(self.shards)
        return self.shards[shard_index]

    def get_db(self, short_code: str):
        shard = self.get_shard(short_code)
        return self.connections[shard]
```

### Read Replicas
- Primary handles all writes
- 3-5 read replicas per shard for read-heavy traffic
- Async replication with < 100ms lag
- Read replicas can be scaled independently

## Failure Handling

### Circuit Breaker Pattern
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = 'CLOSED'
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if self.should_reset():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError()

        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise
```

### Failure Scenarios
| Failure | Mitigation |
|---------|------------|
| Redis down | Fall back to database, serve stale cache |
| Primary DB down | Promote read replica to primary |
| Kafka down | Buffer clicks locally, retry when available |
| CDN failure | Serve directly from origin |
| DNS failure | Use IP fallback, client-side retry |

### Graceful Degradation
- If analytics service down, clicks still work (fire-and-forget)
- If rate limiter down, allow all requests (fail open)
- If custom alias service down, generate random code instead
- Return cached responses during database maintenance

## Monitoring

### Key Metrics (Prometheus + Grafana)
```yaml
Business Metrics:
  - urls_created_per_second
  - redirects_per_second
  - click_rate_by_country

System Metrics:
  - request_latency_p50/p95/p99
  - error_rate_4xx_5xx
  - cache_hit_ratio
  - database_connection_pool_usage
  - kafka_consumer_lag

Infrastructure Metrics:
  - cpu_usage_per_instance
  - memory_usage_per_instance
  - network_io
  - disk_io
```

### Alerting Rules
```yaml
alerts:
  - name: High Latency
    condition: p99_latency > 50ms for 5 minutes
    severity: warning

  - name: Cache Hit Ratio Low
    condition: cache_hit_ratio < 80% for 10 minutes
    severity: warning

  - name: Database Connection Pool Exhausted
    condition: active_connections > 90% of max
    severity: critical

  - name: High Error Rate
    condition: error_5xx_rate > 1% for 5 minutes
    severity: critical
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Hash Algorithm | MD5 (fast, collisions possible) | SHA256 (slow, no collisions) | MD5 with collision check |
| Storage | SQL (ACID, joins) | NoSQL (scale, flexibility) | PostgreSQL with partitioning |
| Caching | Redis (fast, complex) | Memcached (simple, limited) | Redis (rich data structures) |
| Redirect Type | 301 (permanent, cached) | 302 (temporary, always check) | 302 (respect expiration) |
| Analytics | Synchronous | Async (Kafka) | Async (non-blocking) |

## Interview Questions

### Design Questions
1. **How would you handle 100M URLs created daily?**
   - Use consistent hashing for database sharding
   - Partition analytics tables by time
   - Use Redis cluster for caching
   - Batch analytics writes with Kafka

2. **How do you ensure short URLs are not predictable?**
   - Use base62 encoding of random hashes
   - Add user-specific salt to hash generation
   - Limit custom alias attempts
   - Rate limit URL creation

3. **How would you implement custom aliases?**
   - Separate table for custom aliases with unique constraint
   - Validate uniqueness before assignment
   - Reserve certain prefixes for system use
   - Allow users to reclaim unused aliases after expiry

### Scaling Questions
4. **How do you scale to 1B redirects per day?**
   - CDN for static redirects
   - Redis cluster with 100+ nodes
   - Read replicas across regions
   - Connection pooling and keep-alive

5. **How do you handle hot keys (viral URLs)?**
   - Multi-level caching (in-memory + Redis)
   - Cache warming for predicted hot URLs
   - Replicate hot keys across cache nodes
   - Local cache with TTL refresh

### Trade-off Questions
6. **301 vs 302 redirects?**
   - 301: Browser caches, reduces server load, but can't track clicks
   - 302: Always hits server, enables analytics, respects expiration
   - Choose based on requirements (analytics vs performance)

7. **SQL vs NoSQL for storage?**
   - SQL: ACID compliance, complex queries, joins
   - NoSQL: Better horizontal scaling, simpler schema
   - Choose PostgreSQL with partitioning for this use case

### Senior-level Questions
8. **How do you prevent abuse of the URL shortener?**
   - Rate limiting per user/IP
   - URL reputation checking before creation
   - Block known malicious domains
   - Limit redirects per short URL

9. **How would you implement geo-redirects?**
   - Store multiple destination URLs per short code
   - Use GeoIP to determine user location
   - Cache geo-redirect mappings
   - A/B test different destinations

10. **How do you handle URL expiration?**
    - Soft delete with scheduled cleanup job
    - Check expiration on read (add to cache TTL)
    - Kafka topic for expiration events
    - Grace period before permanent deletion

## Summary

The URL Shortener system design covers:
- **Scalability**: Sharded databases, Redis caching, CDN
- **Performance**: Sub-10ms redirects, multi-level caching
- **Reliability**: Circuit breakers, graceful degradation
- **Analytics**: Async event processing, partitioned storage
- **Security**: Rate limiting, abuse prevention, HTTPS

Key takeaways:
1. Use consistent hashing for shard routing
2. Implement multi-level caching (L1 in-memory, L2 Redis)
3. Process analytics asynchronously with Kafka
4. Handle failures gracefully with circuit breakers
5. Monitor everything with proper alerting

This design can handle 1B+ daily redirects while maintaining sub-10ms latency and 99.99% availability.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
