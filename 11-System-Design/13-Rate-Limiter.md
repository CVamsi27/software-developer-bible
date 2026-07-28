# Rate Limiter System Design

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

s, or API key
- Support multiple rate limiting algorithms (Token Bucket, Leaky Bucket, Sliding Window)
- Configurable limits per client (e.g., 100 requests/hour, 10 requests/minute)
- Block requests that exceed the limit with 429 Too Many Requests
- Return rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
- Hierarchical rate limiting (global → region → endpoint → user)
- Whitelist/blacklist specific clients
- Support burst allowance for short traffic spikes

### Non-Functional Requirements

- Extremely low latency (< 1ms added per request)
- High throughput (millions of requests per second)
- Highly available (99.999% — fail open not closed)
- Distributed across multiple data centers
- Eventually consistent across regions (sub-second sync)
- Minimal memory footprint per rate limit entry
- Support for millions of distinct rate limit keys

## Capacity Estimation

```text
Request Estimates:

- 10M API requests/second at peak
- 100M distinct rate limit keys (users/IPS)
- Each rate limit entry: ~100 bytes
- Memory: 100M × 100 bytes = ~10 GB (Redis)
- Works within a single Redis cluster

Algorithm Overhead:

- Token Bucket: 1 counter + timestamp per key = ~50 bytes
- Sliding Window: 2-3 counters + timestamps = ~100 bytes
- Sliding Window Log: O(N) where N = request count in window

Performance Targets:

- Decision time: < 0.5ms for cache hit, < 2ms for cache miss
- Redis queries per second: up to 10M reads, 1M writes
- P99 latency for rate limit check: < 1ms

```

## API Design

```yaml
# Rate Limiter is middleware, not exposed as API
# But it provides management APIs

# Check rate limit (internal service)
POST /api/v1/rate-limiter/check
  Request:
    {
      "client_id": "user_123",      # or API key, IP
      "client_type": "user",         # user, ip, api_key
      "resource": "/api/v1/tweets", # endpoint being called
      "method": "POST",
      "timestamp": "2025-01-15T10:30:00Z"
    }
  Response:
    {
      "allowed": true,
      "remaining": 95,
      "limit": 100,
      "reset_at": "2025-01-15T11:00:00Z",
      "retry_after_ms": 0
    }

# Configure rate limit rules (admin API)
POST /api/v1/rate-limiter/rules
  Request:
    {
      "client_type": "user",
      "resource": "/api/v1/tweets",
      "algorithm": "sliding_window",
      "limits": [
        {"duration": 60, "max_requests": 30},
        {"duration": 3600, "max_requests": 1000},
        {"duration": 86400, "max_requests": 10000}
      ],
      "burst_multiplier": 2.0,
      "burst_duration_seconds": 5
    }

# Get rate limit rules
GET /api/v1/rate-limiter/rules?resource=/api/v1/tweets

# Get current rate limit status for a client
GET /api/v1/rate-limiter/status?client_id=user_123

# Manually block or throttle (admin)
POST /api/v1/rate-limiter/throttle
  Request:
    {
      "client_id": "abusive_user",
      "action": "block",
      "duration_seconds": 3600
    }
```

## Database Design

Rate limiters are in-memory systems. No traditional database is used. However, for persistence and configuration:

```sql
-- Rate limit rules configuration
CREATE TABLE rate_limit_rules (
    id BIGSERIAL PRIMARY KEY,
    client_type VARCHAR(50) NOT NULL,     -- 'user', 'ip', 'api_key'
    resource_pattern VARCHAR(255) NOT NULL, -- '/api/v1/*', exact path
    http_method VARCHAR(10),              -- GET, POST, PUT, DELETE, NULL=all
    algorithm VARCHAR(50) NOT NULL DEFAULT 'sliding_window',
    window_size_seconds INT NOT NULL,     -- 60, 3600, 86400
    max_requests INT NOT NULL,
    burst_multiplier DECIMAL(3,1) DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (client_type, resource_pattern, http_method, window_size_seconds)
);

-- Rate limit overrides (for specific clients)
CREATE TABLE rate_limit_overrides (
    id BIGSERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    client_type VARCHAR(50) NOT NULL,
    max_requests INT NOT NULL,
    window_size_seconds INT NOT NULL,
    reason TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_overrides_client ON rate_limit_overrides(client_id, client_type);

-- Rate limit events (for analytics)
CREATE TABLE rate_limit_events (
    id BIGSERIAL PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    client_type VARCHAR(50) NOT NULL,
    resource VARCHAR(255) NOT NULL,
    action VARCHAR(20) NOT NULL,  -- 'allowed', 'blocked', 'throttled'
    rule_id BIGINT REFERENCES rate_limit_rules(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_rate_limit_events_client ON rate_limit_events(client_id, created_at DESC);
CREATE INDEX idx_rate_limit_events_action ON rate_limit_events(action, created_at DESC);
```

## Architecture
### ASCII Architecture Diagram

```text
┌──────────────────────────────────────────────────────────────────┐
│                        API Clients                               │
│                 (Mobile Apps, Web, Services)                      │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   API Gateway / LB    │
                    │   (Entry point)       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Rate Limiter        │
                    │   Middleware          │
                    │   (Global Decision)   │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
           ┌──────────────────┐  ┌──────────────────┐
           │     Allowed      │  │     Blocked       │
           │                  │  │                   │
           ▼                  │  ▼                   │
    ┌──────────────┐          │  ┌─────────────────┐ │
    │  App Server  │          │  │ Return 429      │ │
    └──────────────┘          │  │ Response        │ │
                              │  └─────────────────┘ │
                              └──────────────────────┘

Rate Limiter Internal Architecture:
┌─────────────────────────────────────────────────────────────┐
│                   Rate Limiter Cluster                       │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Rule       │  │  Algorithm  │  │  Decision   │          │
│  │  Cache      │─▶│  Engine     │─▶│  Response   │          │
│  └─────────────┘  └──────┬──────┘  └─────────────┘          │
│                          │                                   │
│                          ▼                                   │
│  ┌──────────────────────────────────────────┐                │
│  │           Redis Cluster                   │                │
│  │  ┌──────┐ ┌──────┐ ┌──────┐             │                │
│  │  │Shard1│ │Shard2│ │Shard3│  ...         │                │
│  │  └──────┘ └──────┘ └──────┘             │                │
│  └──────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### Rate Limiting Algorithms

```python
import time
from abc import ABC, abstractmethod
from redis import Redis
from threading import Lock

class RateLimitAlgorithm(ABC):
    @abstractmethod
    def is_allowed(self, key: str, max_requests: int,
                   window_seconds: int) -> tuple[bool, dict]:
        """Returns (allowed, response_headers)."""
        pass

class TokenBucket(RateLimitAlgorithm):
    """Token Bucket algorithm - allows bursts up to bucket size."""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def is_allowed(self, key: str, max_requests: int,
                   window_seconds: int) -> tuple[bool, dict]:
        """Token bucket with refill rate = max_requests / window_seconds."""
        now = time.time()
        bucket_key = f"token_bucket:{key}"
        refill_rate = max_requests / window_seconds  # tokens per second

        # Lua script for atomic check-and-update
        script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local max_tokens = tonumber(ARGV[2])
        local refill_rate = tonumber(ARGV[3])

        local bucket = redis.call('hmget', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1])
        local last_refill = tonumber(bucket[2])

        if tokens == nil then
            tokens = max_tokens
            last_refill = now
        end

        -- Refill tokens based on time elapsed
        local elapsed = now - last_refill
        local new_tokens = math.min(max_tokens, tokens + elapsed * refill_rate)

        if new_tokens >= 1 then
            redis.call('hmset', key,
                'tokens', new_tokens - 1,
                'last_refill', now
            )
            redis.call('expire', key, math.ceil(window_seconds * 2))
            return {1, new_tokens - 1, max_tokens, now + window_seconds}
        else
            redis.call('hmset', key,
                'tokens', new_tokens,
                'last_refill', now
            )
            redis.call('expire', key, math.ceil(window_seconds * 2))
            return {0, 0, max_tokens, now + window_seconds}
        end
        """

        result = self.redis.eval(
            script, 1, bucket_key,
            now, max_requests, refill_rate
        )

        allowed = result[0] == 1
        return allowed, {
            'X-RateLimit-Limit': result[2],
            'X-RateLimit-Remaining': int(result[1]),
            'X-RateLimit-Reset': int(result[3])
        }

class SlidingWindowCounter(RateLimitAlgorithm):
    """Sliding Window Counter - smooths edges between windows."""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def is_allowed(self, key: str, max_requests: int,
                   window_seconds: int) -> tuple[bool, dict]:
        now = time.time()
        window_key = f"sliding_window:{key}:{window_seconds}"
        current_window = int(now / window_seconds)
        previous_window = current_window - 1

        script = """
        local key = KEYS[1]
        local current_window = tonumber(ARGV[1])
        local previous_window = tonumber(ARGV[2])
        local max_requests = tonumber(ARGV[3])
        local now = tonumber(ARGV[4])
        local window_seconds = tonumber(ARGV[5])

        -- Current window counter
        local current_key = key .. ':' .. current_window
        local current_count = tonumber(redis.call('get', current_key) or 0)

        -- Previous window counter
        local previous_key = key .. ':' .. previous_window
        local previous_count = tonumber(redis.call('get', previous_key) or 0)

        -- Calculate weighted count
        local window_position = (now % window_seconds) / window_seconds
        local weighted_count = previous_count * (1 - window_position) + current_count

        if weighted_count < max_requests then
            redis.call('incr', current_key)
            redis.call('expire', current_key, window_seconds * 2)
            local remaining = max_requests - math.floor(weighted_count) - 1
            return {1, remaining, max_requests, current_window * window_seconds + window_seconds}
        else
            local reset_at = current_window * window_seconds + window_seconds
            return {0, 0, max_requests, reset_at}
        end
        """

        result = self.redis.eval(
            script, 1, window_key,
            current_window, previous_window, max_requests, now, window_seconds
        )

        allowed = result[0] == 1
        return allowed, {
            'X-RateLimit-Limit': result[2],
            'X-RateLimit-Remaining': int(result[1]),
            'X-RateLimit-Reset': int(result[3])
        }

class SlidingWindowLog(RateLimitAlgorithm):
    """Sliding Window Log - most accurate, higher memory usage."""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def is_allowed(self, key: str, max_requests: int,
                   window_seconds: int) -> tuple[bool, dict]:
        now = time.time()
        log_key = f"sliding_log:{key}:{window_seconds}"
        window_start = now - window_seconds

        script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window_start = tonumber(ARGV[2])
        local max_requests = tonumber(ARGV[3])
        local window_seconds = tonumber(ARGV[4])

        -- Remove expired entries
        redis.call('zremrangebyscore', key, 0, window_start)

        -- Count current requests
        local current_count = redis.call('zcard', key)

        if current_count < max_requests then
            -- Add current request timestamp
            redis.call('zadd', key, now, now)
            redis.call('expire', key, window_seconds * 2)
            local remaining = max_requests - current_count - 1
            return {1, remaining, max_requests, now + window_seconds}
        else
            local oldest = redis.call('zrange', key, 0, 0, 'withscores')
            local reset_at = tonumber(oldest[2]) + window_seconds
            return {0, 0, max_requests, reset_at}
        end
        """

        result = self.redis.eval(
            script, 1, log_key,
            now, window_start, max_requests, window_seconds
        )

        allowed = result[0] == 1
        return allowed, {
            'X-RateLimit-Limit': result[2],
            'X-RateLimit-Remaining': int(result[1]),
            'X-RateLimit-Reset': int(result[3])
        }
```

### Rate Limiter Middleware

```python
class RateLimiterMiddleware:
    def __init__(self, redis_client, rule_cache):
        self.redis = redis_client
        self.rule_cache = rule_cache
        self.algorithms = {
            'token_bucket': TokenBucket(redis_client),
            'sliding_window': SlidingWindowCounter(redis_client),
            'sliding_window_log': SlidingWindowLog(redis_client),
        }
        self.local_ratelimit_cache = {}
        self.cache_ttl = 0.5  # 500ms local cache for hot keys

    async def check_rate_limit(self, request: dict) -> dict:
        """Check all applicable rate limits for a request."""
        client_id = self.extract_client_id(request)
        resource = request['resource']
        method = request['method']

        # Get applicable rules
        rules = await self.get_applicable_rules(
            client_id['type'], resource, method
        )

        # Check each rule hierarchically
        for rule in rules:
            algorithm = self.algorithms[rule['algorithm']]
            rate_limit_key = f"{client_id['type']}:{client_id['id']}:{rule['id']}"

            # Check local cache first (for hot keys)
            cached = self.check_local_cache(rate_limit_key)
            if cached is not None:
                if not cached['allowed']:
                    return self.build_blocked_response(cached['headers'])
                continue  # Allowed, check next rule

            allowed, headers = algorithm.is_allowed(
                rate_limit_key,
                rule['max_requests'],
                rule['window_size_seconds']
            )

            # Update local cache
            self.update_local_cache(rate_limit_key, {
                'allowed': allowed,
                'headers': headers
            })

            if not allowed:
                # Log rate limit event
                await self.log_rate_limit_event(client_id, resource, rule)

                return self.build_blocked_response(headers)

        return self.build_allowed_response()

    def extract_client_id(self, request: dict) -> dict:
        """Extract client identifier from request."""
        if 'api_key' in request:
            return {'type': 'api_key', 'id': request['api_key']}
        elif 'user_id' in request:
            return {'type': 'user', 'id': request['user_id']}
        else:
            return {'type': 'ip', 'id': request.get('ip', 'unknown')}

    async def get_applicable_rules(self, client_type: str,
                                    resource: str,
                                    method: str) -> list:
        """Get all applicable rate limit rules, ordered by priority."""
        rules = await self.rule_cache.get_rules(client_type)
        applicable = []

        for rule in rules:
            if self.rule_matches(rule, resource, method):
                applicable.append(rule)

        # Sort by specificity (most specific first)
        return sorted(applicable, key=lambda r: -r.get('priority', 0))

    def rule_matches(self, rule: dict, resource: str,
                     method: str) -> bool:
        """Check if a rule matches the request."""
        import fnmatch

        # Check HTTP method
        if rule.get('http_method') and rule['http_method'] != method:
            return False

        # Check resource pattern (support wildcards)
        return fnmatch.fnmatch(resource, rule['resource_pattern'])

    def check_local_cache(self, key: str):
        """Check in-memory cache for hot keys (sub-millisecond)."""
        entry = self.local_ratelimit_cache.get(key)
        if entry and time.time() < entry['expires_at']:
            return entry
        return None

    def update_local_cache(self, key: str, value: dict):
        """Update local cache with short TTL."""
        self.local_ratelimit_cache[key] = {
            **value,
            'expires_at': time.time() + self.cache_ttl
        }

    def build_blocked_response(self, headers: dict) -> dict:
        return {
            'allowed': False,
            'status_code': 429,
            'headers': {
                'Retry-After': str(headers.get('X-RateLimit-Reset', 60)),
                **headers
            },
            'body': {
                'error': 'rate_limit_exceeded',
                'message': 'Too many requests. Please try again later.'
            }
        }

    def build_allowed_response(self) -> dict:
        return {
            'allowed': True,
            'status_code': 200,
            'headers': {}
        }

    async def log_rate_limit_event(self, client_id: dict,
                                    resource: str, rule: dict):
        """Log rate limit events for analytics."""
        # Use async logging to avoid blocking
        await self.async_logger.log({
            'client_id': client_id['id'],
            'client_type': client_id['type'],
            'resource': resource,
            'rule_id': rule['id'],
            'action': 'blocked',
            'timestamp': time.time()
        })
```

### Distributed Rate Limiter with Consistent Hashing

```python
import hashlib

class DistributedRateLimiter:
    """Rate limiter that uses consistent hashing for Redis shard routing."""

    def __init__(self, redis_nodes: list):
        self.ring = ConsistentHashRing(redis_nodes, replicas=150)
        self.local_cache = LocalRateLimitCache()

    def check_request(self, client_id: str, max_requests: int,
                      window_seconds: int) -> tuple[bool, dict]:
        # Get the Redis node responsible for this client
        redis_node = self.ring.get_node(client_id)

        # Check local cache (fast path)
        local_result = self.local_cache.get(f"{client_id}:{max_requests}")
        if local_result and local_result['reset_at'] > time.time():
            return local_result['allowed'], local_result['headers']

        # Check with Redis (slower path)
        algorithm = SlidingWindowCounter(redis_node)
        allowed, headers = algorithm.is_allowed(
            f"global:{client_id}",
            max_requests,
            window_seconds
        )

        # Update local cache
        self.local_cache.set(
            f"{client_id}:{max_requests}",
            {'allowed': allowed, 'headers': headers,
             'reset_at': headers.get('X-RateLimit-Reset', 0)},
            ttl=0.1  # 100ms local cache
        )

        return allowed, headers


class ConsistentHashRing:
    """Consistent hashing for distributing rate limit keys across Redis nodes."""

    def __init__(self, nodes: list, replicas: int = 150):
        self.nodes = nodes
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []

        for node in nodes:
            for i in range(replicas):
                key = self.hash(f"{node}:{i}")
                self.ring[key] = node
                self.sorted_keys.append(key)

        self.sorted_keys.sort()

    def get_node(self, key: str):
        if not self.ring:
            return None

        hash_val = self.hash(key)
        # Linear scan around the ring
        for node_key in self.sorted_keys:
            if hash_val <= node_key:
                return self.ring[node_key]

        # Wrap around
        return self.ring[self.sorted_keys[0]]

    def hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

### Rule Cache Service

```python
class RuleCache:
    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db
        self.cache_ttl = 300  # 5 minutes

    async def get_rules(self, client_type: str) -> list:
        """Get rate limit rules for a client type, cached."""
        cache_key = f"rate_limit_rules:{client_type}"

        # Try cache
        cached = self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        # Load from database
        rules = await self.db.query(
            "SELECT * FROM rate_limit_rules "
            "WHERE client_type = $1 AND is_active = TRUE "
            "ORDER BY window_size_seconds ASC",
            client_type
        )

        rules_list = [dict(r) for r in rules]

        # Cache for future
        self.redis.setex(cache_key, self.cache_ttl, json.dumps(rules_list))

        return rules_list

    async def invalidate_cache(self, client_type: str = None):
        """Invalidate rule cache when rules change."""
        if client_type:
            self.redis.delete(f"rate_limit_rules:{client_type}")
        else:
            # Invalidate all
            for key in self.redis.scan_iter("rate_limit_rules:*"):
                self.redis.delete(key)
```

## Caching Strategy (Redis)

### Multi-Layer Rate Limit Cache

```python
class RateLimitCache:
    def __init__(self, redis_client):
        self.redis = redis_client

        # In-memory LRU cache for hot keys (sub-millisecond)
        self.l1_cache = LRUCache(maxsize=100000, ttl=0.1)

    def check_rate_limit(self, key: str, max_requests: int,
                         window_seconds: int) -> tuple[bool, dict]:
        # L1: In-memory cache
        l1_key = f"{key}:{max_requests}:{window_seconds}"
        l1_result = self.l1_cache.get(l1_key)
        if l1_result is not None:
            return l1_result['allowed'], l1_result['headers']

        # L2: Redis (using Lua scripting for atomicity)
        allowed, headers = self._redis_check(
            key, max_requests, window_seconds
        )

        # Update L1 cache
        self.l1_cache.set(l1_key, {
            'allowed': allowed,
            'headers': headers
        })

        return allowed, headers
```

## Message Queue (Kafka)

### Rate Limit Event Stream

```text
Topics:
├── rate_limit.checked       (every rate limit check - sampled 1:100)
├── rate_limit.blocked       (every blocked request)
├── rate_limit.rule_updated  (rule configuration changes)
├── rate_limit.throttle      (manual throttle commands)

Consumer Groups:
├── rate-limit-analytics     (process blocked events for dashboards)
├── rate-limit-sync          (sync rules across regions)
```

## Scaling Strategy

### Redis Cluster Scaling

```text
┌─────────────────────────────────────────────────────────────┐
│                    Redis Cluster                             │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Master 1 │  │ Master 2 │  │ Master 3 │  │ Master N │    │
│  │  500MB   │  │  500MB   │  │  500MB   │  │  500MB   │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │             │           │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐    │
│  │Replica 1 │  │Replica 2 │  │Replica 3 │  │Replica N │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Horizontal Scaling

```python
class RateLimiterPool:
    """Manages pool of rate limiter instances for horizontal scaling."""

    def __init__(self, num_instances: int = 10):
        self.instances = [
            RateLimiterMiddleware(redis_pool)
            for _ in range(num_instances)
        ]
        self.router = ConsistentHashRing(
            [f"instance_{i}" for i in range(num_instances)]
        )

    def get_limiter(self, client_id: str) -> RateLimiterMiddleware:
        idx = self.router.get_node(client_id)
        return self.instances[int(idx.split('_')[1])]
```

## Failure Handling

### Failure Scenarios

| Failure | Mitigation |
|---------|------------|
| Redis node down | Consistent hashing redistributes to next node |
| Redis cluster unavailable | Local in-memory rate limiting with degraded accuracy |
| Network partition | Fail open (allow requests) rather than fail closed |
| High latency | Local cache absorbs 99% of checks, only hits Redis every 100ms |
| Clock skew | Use Redis time, synchronize via NTP |

### Circuit Breaker for Redis

```python
class RedisCircuitBreaker:
    def __init__(self, fallback_limiter):
        self.failure_count = 0
        self.failure_threshold = 5
        self.reset_timeout = 10
        self.last_failure = 0
        self.state = 'CLOSED'
        self.fallback = fallback_limiter  # Local in-memory limiter

    def execute(self, check_func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure > self.reset_timeout:
                self.state = 'HALF_OPEN'
            else:
                return self.fallback(*args, **kwargs)

        try:
            result = check_func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except (RedisConnectionError, TimeoutError) as e:
            self.failure_count += 1
            self.last_failure = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            return self.fallback(*args, **kwargs)
```

## Monitoring

### Key Metrics

```yaml
Business Metrics:

  - requests_allowed_per_second
  - requests_blocked_per_second
  - block_rate_percentage
  - top_blocked_clients
  - top_blocked_endpoints

System Metrics:

  - rate_limit_check_latency_p50_p95_p99
  - redis_query_latency
  - l1_cache_hit_ratio
  - l2_cache_hit_ratio
  - active_rate_limit_keys

Infrastructure Metrics:

  - redis_memory_usage
  - redis_cpu_usage
  - number_of_rules_loaded
  - local_cache_size
```

### Alerting

```yaml
alerts:

  - name: High Rate Limit Latency
    condition: p99_latency > 5ms for 2 minutes
    severity: warning

  - name: Redis Cluster Memory High
    condition: redis_memory_usage > 80% for 5 minutes
    severity: critical

  - name: Excessive Blocks
    condition: block_rate > 30% for 5 minutes
    severity: warning (possible DDoS)

  - name: Redis Connection Failures
    condition: redis_connection_errors > 10 per minute
    severity: critical
```

## Trade-offs

| Decision | Option A | Option B | Choice |
|----------|----------|----------|--------|
| Algorithm | Token Bucket (bursty, simple) | Sliding Window (smooth, accurate) | Sliding Window Counter (balance) |
| Storage | Redis (fast, persistent) | Local memory (fastest, not shared) | Redis + local L1 cache |
| Consistency | Strong (global lock) | Eventually consistent | Eventually consistent for performance |
| Fail Mode | Fail open (allow all) | Fail closed (block all) | Fail open (better UX) |
| Routing | Consistent hashing (stable) | Round-robin (simple) | Consistent hashing |

## Summary

The Rate Limiter system design covers:

- **Multiple Algorithms**: Token Bucket, Sliding Window, Sliding Window Log
- **Distributed Architecture**: Consistent hashing across Redis cluster
- **Ultra-Low Latency**: Multi-level caching (L1 in-memory, L2 Redis)
- **Hierarchical Rules**: Global → region → endpoint → user
- **Graceful Degradation**: Local fallback when Redis is unavailable

Key takeaways:

1. Use Lua scripts in Redis for atomic rate limit checks

2. Implement L1 local cache for sub-millisecond hot-path decisions

3. Use consistent hashing for stable key-to-node mapping

4. Always fail open (allow requests) during Redis outages

5. Monitor block rates to detect abuse and DDoS attacks

This design handles 10M+ requests/second with < 1ms added latency per rate limit check.

---

---

## Cheat Sheet
```text
RATE LIMITER SYSTEM DESIGN CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  Request Estimates:
  - 10M API requests/second at peak
  - 100M distinct rate limit keys (users/IPS)
  - Each rate limit entry: ~100 bytes
  - Memory: 100M × 100 bytes = ~10 GB (Redis)
  - Works within a single Redis cluster
```
```
  Rate limiters are in-memory systems. No traditional database is used. However, for persistence and configuration:
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [REST APIs](../07-REST-API/)
- [Security](../09-Security/)

## References & Learn More

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [Redis Rate Limiting Patterns](https://redis.com/redis-best-practices/rate-limiting/)
- [Stripe Rate Limiting](https://stripe.com/docs/rate-limits)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
