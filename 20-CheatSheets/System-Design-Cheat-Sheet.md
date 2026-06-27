# System Design Cheat Sheet

## Quick Reference Table

| Concept | Key Point | Code/Example |
|---------|-----------|--------------|
| Load Balancer | Distributes traffic across servers; L4 (TCP) or L7 (HTTP) | NGINX, HAProxy, AWS ALB/NLB |
| Round Robin | Equal distribution; no consideration of server load | Simple but ignores server health |
| Least Connections | Route to server with fewest active connections | Better for uneven request durations |
| IP Hash | Sticky sessions based on client IP | Session persistence without shared state |
| Horizontal Scaling | Add more machines; stateless servers scale horizontally | Scale out: 2 servers → 20 servers |
| Vertical Scaling | Bigger machine; limited by hardware ceiling | Scale up: 8GB RAM → 64GB RAM |
| Database Sharding | Split data across databases by key (user ID, region) | Shard by `user_id % 4` → 4 databases |
| Read Replicas | Copy database for read traffic; leader-follower pattern | Writes → leader, reads → followers |
| Caching | Store frequently accessed data in fast storage | Redis, Memcached, CDN edge cache |
| CDN | Content Delivery Network; cache static assets at edge | CloudFlare, AWS CloudFront, Fastly |
| Cache-Aside | App checks cache, misses → DB → stores in cache | Most common; app controls cache invalidation |
| Write-Through | Write to cache and DB simultaneously | Consistent but adds write latency |
| Write-Behind | Write to cache, async flush to DB | Fast writes but risk of data loss |
| Cache Invalidation | Remove/update cache when data changes; hard problem | TTL, versioning, event-driven invalidation |
| Cache Stampede | Many requests hit DB when cache expires | Locking, probabilistic early refresh, stale-while-revalidate |
| Message Queue | Decouple producers/consumers; async processing | RabbitMQ, Kafka, SQS, Redis Streams |
| Pub/Sub | Broadcast to all subscribers; fan-out pattern | Redis Pub/Sub, Kafka Topics, SNS |
| Event Sourcing | Store events, not state; rebuild state from events | Audit trail, temporal queries, CQRS |
| CQRS | Command Query Responsibility Segregation; separate read/write models | Write: normalized DB. Read: denormalized/projection. |
| API Gateway | Single entry point; routing, auth, rate limiting, aggregation | Kong, AWS API Gateway, Traefik |
| Service Mesh | Infrastructure for service-to-service communication | Istio, Linkerd — sidecar proxy pattern |
| Circuit Breaker | Stop calling failing service; half-open after timeout | Prevents cascading failures; opossum, Polly |
| Retry with Backoff | Exponential backoff + jitter for transient failures | `delay = min(base * 2^attempt + jitter, maxDelay)` |
| Idempotency | Same request = same result; use idempotency keys | `X-Idempotency-Key: <uuid>` for POST |
| Consistency | Every read returns the most recent write | Strong: linearizability. Eventual: lag possible |
| Availability | System is operational and responsive | Trade-off: strong consistency may reduce availability |
| CAP Theorem | Can only have 2 of 3: Consistency, Availability, Partition tolerance | Always have P; choose CP or AP |
| PACELC | If Partition: choose A or C. Else: choose L (latency) or C (consistency) | More nuanced than CAP |
| Rate Limiting | Control request rate; sliding window, token bucket, leaky bucket | Per-IP (public), per-user (authenticated) |
| Docker | Container packaging; image layers, Dockerfile, docker-compose | `docker build -t app . && docker run -p 3000:3000 app` |
| Docker Multi-Stage | Separate build and runtime stages; smaller images | `FROM node:20 AS builder` ... `FROM node:20-slim` |
| Kubernetes (K8s) | Container orchestration; pods, services, deployments, ingress | Declarative infrastructure as code |
| K8s Pod | Smallest deployable unit; one or more containers sharing network | `apiVersion: v1, kind: Pod` |
| K8s Deployment | Manages ReplicaSets; rolling updates, rollbacks | `spec.replicas: 3, strategy: RollingUpdate` |
| K8s Service | Stable network endpoint for pods; ClusterIP, NodePort, LoadBalancer | `type: ClusterIP` for internal, `LoadBalancer` for external |
| K8s Ingress | HTTP routing; path-based and host-based routing | NGINX Ingress, Traefik, AWS ALB Controller |
| K8s ConfigMap/Secret | Externalized configuration; ConfigMap for non-sensitive, Secret for sensitive | Mounted as env vars or volumes |
| K8s HPA | Horizontal Pod Autoscaler; scale based on CPU/memory/custom metrics | `minReplicas: 2, maxReplicas: 10, targetCPU: 70` |
| K8s Health Probes | Liveness (restart if failed), Readiness (remove from LB if not ready), Startup | `httpGet`, `tcpSocket`, `exec` |
| Message Queue Patterns | Point-to-point, pub/sub, competing consumers, dead letter queue | DLQ for failed messages |
| Kafka | Distributed event streaming; topics, partitions, consumer groups | High throughput, ordered within partition, durable |
| Redis | In-memory data structure; strings, hashes, lists, sets, sorted sets, streams | `SET key value EX 3600` |
| Redis Patterns | Cache, session store, rate limiter (sliding window), pub/sub, leader election | `INCR` for counters, `SETNX` for locks |
| SQL vs NoSQL | SQL: structured, ACID, joins. NoSQL: flexible, horizontal scale, eventual consistency | Choose based on data model and access patterns |
| Database Scaling | Vertical → Read replicas → Sharding → CQRS → Event sourcing | Progressive complexity |
| Back-of-Envelope | Estimations: QPS, storage, bandwidth, latency | 1M DAU × 10 req/day = ~120 QPS |
| Monitoring | Metrics (Prometheus), Logs (ELK), Traces (Jaeger/Zipkin) | Three pillars of observability |
| SLO/SLA/SLI | SLI: metric. SLO: target. SLA: contract with penalties | `99.9% availability` = ~43 min downtime/month |
| Blue-Green Deploy | Two identical environments; switch traffic instantly | Zero-downtime deploy; instant rollback |
| Canary Deploy | Roll out to small percentage first; monitor; increase gradually | 1% → 5% → 25% → 100% |
| Feature Flags | Toggle features without deploy; gradual rollout, A/B testing | LaunchDarkly, Unleash, custom |
| Chaos Engineering | Inject failures to test resilience | Netflix Simian Army, Chaos Monkey |

## Top 10 Things to Remember

1. **Start with requirements**: Functional (what it does) and non-functional (scale, latency, availability, consistency). Ask clarifying questions before designing.

2. **Back-of-envelope estimation**: 1M DAU × 10 req/day = ~120 QPS. 1KB per request × 120 = 120KB/s. Storage: 1M × 10 × 365 × 1KB = ~3.6TB/year.

3. **CAP theorem is a trade-off, not a choice**: Always have Partition tolerance. Choose between Consistency (CP: Zookeeper, HBase) and Availability (AP: Cassandra, DynamoDB). Most systems are AP with eventual consistency.

4. **Caching is the #1 performance tool**: Cache-aside is the default pattern. Use CDN for static assets, Redis for dynamic data, browser cache for repeated visits. Cache invalidation is the hard part.

5. **Stateless services scale horizontally**: Put state in databases or distributed caches. Any server can handle any request. This enables auto-scaling and rolling deployments.

6. **Message queues decouple and buffer**: Producer doesn't wait for consumer. Handles traffic spikes. Enables async processing, retry logic, and dead letter queues for failed messages.

7. **Database read replicas scale reads, sharding scales writes**: Read replicas for read-heavy workloads (most apps). Sharding when a single node can't handle write volume. Shard by access pattern (user ID, region).

8. **Docker containers package, Kubernetes orchestrates**: Containers ensure consistency across environments. K8s manages deployment, scaling, self-healing, and service discovery. Don't run K8s if you have 3 services — use ECS or simple Docker Compose.

9. **Circuit breakers prevent cascading failures**: When a service is down, stop calling it. Use half-open state to test recovery. This prevents a single failure from bringing down the entire system.

10. **Observability has three pillars**: Metrics (what's happening), Logs (why), Traces (where). You can't fix what you can't see. Always instrument before you need it.

## Common Patterns

### Cache-Aside (Lazy Loading)
```
1. Check cache for key
2. Cache HIT → return cached value
3. Cache MISS → query database
4. Store result in cache with TTL
5. Return result
```
```python
def get_user(user_id):
    # Check cache
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # Cache miss - query DB
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    if user:
        redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

### Sliding Window Rate Limiter (Redis)
```python
def is_rate_limited(user_id, limit=100, window=60):
    key = f"rate:{user_id}:{int(time.time()) // window}"
    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    current = pipe.execute()[0]
    return current > limit
```

### Circuit Breaker (State Machine)
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = 'CLOSED'
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise
```

### Event Sourcing
```python
class EventStore:
    def __init__(self):
        self.events = []

    def append(self, aggregate_id, event_type, data):
        self.events.append({
            'aggregate_id': aggregate_id,
            'event_type': event_type,
            'data': data,
            'timestamp': datetime.utcnow(),
            'version': len(self.events) + 1,
        })

    def get_events(self, aggregate_id):
        return [e for e in self.events if e['aggregate_id'] == aggregate_id]

    def rebuild_state(self, aggregate_id):
        events = self.get_events(aggregate_id)
        state = {}
        for event in events:
            state = self.apply_event(state, event)
        return state

    def apply_event(self, state, event):
        if event['event_type'] == 'UserCreated':
            return {'id': event['data']['id'], 'name': event['data']['name']}
        if event['event_type'] == 'UserEmailChanged':
            return {**state, 'email': event['data']['email']}
        return state
```

### Idempotent API Endpoint
```typescript
async function createOrder(req: Request) {
  const idempotencyKey = req.headers['x-idempotency-key'];

  // Check if already processed
  const existing = await redis.get(`idempotent:${idempotencyKey}`);
  if (existing) {
    return JSON.parse(existing); // Return cached response
  }

  // Process
  const order = await db.order.create({ data: req.body });

  // Cache response
  const response = { id: order.id, status: 'created' };
  await redis.setex(`idempotent:${idempotencyKey}`, 86400, JSON.stringify(response));

  return response;
}
```

### Distributed Lock (Redis)
```python
def acquire_lock(lock_name, timeout=10):
    identifier = str(uuid.uuid4())
    lock_key = f"lock:{lock_name}"

    # Set if not exists (atomic)
    if redis.set(lock_key, identifier, nx=True, ex=timeout):
        return identifier
    return None

def release_lock(lock_name, identifier):
    lock_key = f"lock:{lock_name}"
    # Only release if we own it (Lua script for atomicity)
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return redis.eval(script, 1, lock_key, identifier)
```

### K8s Deployment + Service + HPA
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
      - name: api
        image: myapp:1.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: ClusterIP
  selector:
    app: api-server
  ports:
  - port: 80
    targetPort: 3000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Docker Multi-Stage Build
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

USER nextjs
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Kafka Consumer Group
```python
from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(
    'orders',
    group_id='order-processing',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    max_poll_records=100,
)

for message in consumer:
    try:
        process_order(message.value)
        consumer.commit()
    except Exception as e:
        # Send to dead letter topic
        producer.send('orders-dlq', value=message.value)
        consumer.commit()  # Skip failed message
```

## Red Flags (Things NOT to Say)

- **"Just use a single database"** — Doesn't address scale. Always discuss trade-offs and when you'd add replicas, caching, or sharding.
- **"We need microservices for everything"** — Start monolith, extract when needed. Microservices add complexity (network, data consistency, deployment).
- **"SQL is always better than NoSQL"** — Depends on data model and access patterns. SQL for relational data, NoSQL for document/columnar/scaling needs.
- **"I'd use Kubernetes for a 3-service application"** — Overkill. Use Docker Compose, ECS, or simple VMs first. K8s complexity is justified at scale.
- **"Caching solves all performance problems"** — Caching adds complexity (invalidation, consistency, cold starts). Profile first, cache what matters.
- **"We'll handle it with more servers"** — Horizontal scaling doesn't fix bad algorithms. O(n²) with 100 servers is still slow.
- **"I'd use REST for everything"** — Consider gRPC for internal services, GraphQL for complex client needs, WebSocket for real-time.
- **"We need strong consistency everywhere"** — Most features work fine with eventual consistency. Choose consistency per use case.
- **"I'd shard the database from day one"** — Premature optimization. Start with a single optimized database, shard when you hit limits.
- **"Monitoring is for after we launch"** — Instrument from day one. You can't debug what you can't observe.

## Green Flags (Things TO Say)

- **"Let me start with requirements and constraints."** — Structured approach. Shows you think before designing.
- **"I'd estimate the scale: QPS, storage, bandwidth."** — Back-of-envelope estimation shows practical thinking.
- **"I'd use cache-aside with Redis for this hot path, with TTL-based invalidation."** — Specific pattern with reasoning.
- **"For this read-heavy workload, I'd add read replicas to the primary database."** — Matches solution to problem.
- **"I'd use a message queue to decouple these services for async processing."** — Decoupling is a core principle.
- **"Let me discuss the trade-offs between consistency and availability for this feature."** — CAP awareness.
- **"I'd start with a monolith and extract services when we have clear boundaries."** — Pragmatic architecture.
- **"I'd implement circuit breakers for external API calls to prevent cascading failures."** — Resilience patterns.
- **"I'd use blue-green or canary deployments for zero-downtime releases."** — Deployment strategy awareness.
- **"I'd set up monitoring with metrics, logs, and distributed traces from day one."** — Observability from the start.

## 5-Minute Pre-Interview Review

- **Requirements**: Functional (features), non-functional (scale, latency, availability, consistency, cost). Ask clarifying questions.
- **Estimation**: QPS = DAU × requests/day ÷ 86400. Storage = QPS × avg size × retention. Bandwidth = QPS × avg payload.
- **CAP Theorem**: Consistency + Availability + Partition tolerance — pick 2. PACELC: adds latency vs consistency trade-off when no partition.
- **Load Balancing**: Round Robin (simple), Least Connections (uneven), IP Hash (sticky), Health Checks (remove bad servers).
- **Caching**: Cache-aside (default), Write-through (consistent), Write-behind (fast writes), CDN (static assets), TTL (expiration).
- **Database Scaling**: Single DB → Read Replicas (read scale) → Sharding (write scale) → CQRS (separate read/write).
- **Message Queues**: Decouple services, buffer traffic, async processing, retry logic, dead letter queues. RabbitMQ (traditional), Kafka (streaming).
- **Docker**: Container = isolated process with own filesystem. Image = immutable template. Dockerfile = build instructions. Multi-stage = smaller images.
- **Kubernetes**: Pod = smallest unit. Deployment = manages pods. Service = stable network endpoint. Ingress = HTTP routing. HPA = auto-scaling.
- **Security**: Rate limiting, input validation, parameterized queries, CSP headers, SameSite cookies, JWT in httpOnly cookies, bcrypt for passwords.
- **Monitoring**: Metrics (Prometheus/Grafana), Logs (ELK/Loki), Traces (Jaeger/Zipkin). SLO/SLA/SLI for reliability targets.
- **Deployment**: Blue-green (instant switch), Canary (gradual rollout), Feature flags (toggle without deploy).

---

## References & Learn More
- [Cheat Sheet Collection](https://github.com/detailyang/awesome-cheatsheet)
- [DevHints](https://devhints.io/)
- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
