# System Design Interview Questions

## Overview
This file contains 30 most asked system design interview questions with detailed answers, categorized by difficulty level. Each answer includes architecture, key components, trade-offs, and scaling considerations.

---

## Easy Level (1-10)

### 1. Design a URL Shortener

**Requirements:**
- Generate short URLs from long URLs
- Redirect short URLs to original
- Handle 100M URLs/day
- Analytics tracking

**High-Level Architecture:**
```text
Client → Load Balancer → App Server → Cache (Redis) → Database (PostgreSQL)
                                ↓
                        Analytics Service (Kafka)
```

**Key Components:**
1. **Hash Generation**: Use base62 encoding of MD5 hash
2. **Storage**: PostgreSQL with sharding by hash
3. **Caching**: Redis for hot URLs (80% hit rate)
4. **Analytics**: Async processing with Kafka

**Database Schema:**
```sql
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

**Scaling Considerations:**
- Shard by short_code using consistent hashing
- Cache top 20% URLs (covers 80% traffic)
- Use CDN for redirect caching

**Trade-offs:**
- 301 vs 302 redirect (301 for performance, 302 for analytics)
- MD5 vs SHA256 (MD5 faster, collision check needed)

---

### 2. Design a Rate Limiter

**Requirements:**
- Limit API requests per user
- Support multiple rate limiting algorithms
- Distributed across servers
- Low latency checking

**Algorithms:**

1. **Token Bucket:**
```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate

    def allow_request(self):
        if self.tokens > 0:
            self.tokens -= 1
            return True
        return False
```

2. **Sliding Window Log:**
```python
class SlidingWindowLog:
    def __init__(self, window_size, max_requests):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = []

    def allow_request(self):
        now = time.time()
        self.requests = [r for r in self.requests
                        if now - r < self.window_size]
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
```

**Redis Implementation:**
```python
def is_rate_limited(user_id, limit, window):
    key = f"rate_limit:{user_id}"

    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    results = pipe.execute()

    return results[0] > limit
```

**Scaling:**
- Redis cluster for distributed rate limiting
- Local rate limiting with periodic sync
- Circuit breaker for Redis failures

---

### 3. Design a Notification System

**Requirements:**
- Push, email, SMS notifications
- User preference management
- Delivery tracking
- Rate limiting

**Architecture:**
```text
Client → API Gateway → Notification Service → Message Queue (Kafka)
                                                    ↓
                                    ┌───────────────┼───────────────┐
                                    ↓               ↓               ↓
                              Push Service    Email Service    SMS Service
                              (FCM/APNs)      (SendGrid)      (Twilio)
```

**Key Components:**
1. **Template Engine**: Jinja2 for customizable messages
2. **Preference Service**: User channel preferences
3. **Rate Limiter**: Per-user notification limits
4. **Delivery Tracker**: Track sent/delivered/opened

**Database Schema:**
```sql
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    channel VARCHAR(20) NOT NULL,
    template VARCHAR(100),
    status VARCHAR(20) DEFAULT 'queued',
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP
);
```

**Scaling:**
- Kafka for async processing
- Database sharding by user_id
- Redis for preference caching

---

### 4. Design a Chat System

**Requirements:**
- 1:1 and group messaging
- Real-time delivery
- Message history
- Online/offline status

**Architecture:**
```text
Client ←→ WebSocket Server ←→ Message Queue ←→ Message Service
                    ↓
            Connection Manager (Redis)
                    ↓
            Message Storage (Cassandra)
```

**Key Components:**
1. **WebSocket Manager**: Handle persistent connections
2. **Message Queue**: Kafka for message ordering
3. **Storage**: Cassandra for write-heavy workload
4. **Presence Service**: Redis for online status

**Message Flow:**
1. User A sends message
2. WebSocket server receives
3. Publish to Kafka (partitioned by chat_id)
4. Consumer stores in Cassandra
5. Deliver to User B via WebSocket

**Scaling:**
- WebSocket servers: 100K connections each
- Kafka partitioning by chat_id
- Geographic sharding for global users

---

### 5. Design a Key-Value Store

**Requirements:**
- Put(key, value)
- Get(key)
- Delete(key)
- Distributed and scalable

**Architecture:**
```text
Client → Coordinator Node → Hash Ring → Storage Nodes
                    ↓
            Consistent Hashing
                    ↓
            Replication (3 copies)
```

**Consistent Hashing:**
```python
class ConsistentHash:
    def __init__(self, nodes):
        self.ring = {}
        self.sorted_keys = []
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        key = hash(node)
        self.ring[key] = node
        self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def get_node(self, data_key):
        h = hash(data_key)
        for key in self.sorted_keys:
            if h <= key:
                return self.ring[key]
        return self.ring[self.sorted_keys[0]]
```

**Replication:**
- 3 copies across different nodes
- Quorum reads/writes (R+W > N)
- Anti-entropy for consistency

**Scaling:**
- Add nodes to hash ring
- Automatic data rebalancing
- Read replicas for read-heavy workloads

---

### 6. Design a Web Crawler

**Requirements:**
- Crawl billions of web pages
- Politeness (respect robots.txt)
- Deduplication
- Distributed crawling

**Architecture:**
```text
Seed URLs → URL Frontier → Fetcher → Parser → Content Storage
                ↓
        Priority Queue
                ↓
        DNS Cache
```

**Key Components:**
1. **URL Frontier**: Priority queue with politeness
2. **Fetcher**: HTTP client with rate limiting
3. **Parser**: Extract links and content
4. **Deduplication**: Bloom filter for URL dedup

**Politeness:**
- Respect robots.txt
- Rate limit per domain
- User-agent identification

**Scaling:**
- Multiple crawler instances
- Distributed URL frontier
- DNS caching

---

### 7. Design a Search Autocomplete

**Requirements:**
- Fast prefix matching
- Top-K suggestions
- Real-time updates
- Personalization

**Architecture:**
```text
Client → API Gateway → Trie Service → Cache (Redis)
                    ↓
            Analytics Service
                    ↓
            Trie Storage (In-memory)
```

**Trie Implementation:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += 1

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self.get_top_k(node, 10)
```

**Scaling:**
- Shard trie by prefix
- Cache frequent queries
- Update trie periodically (not real-time)

---

### 8. Design a Web Analytics System

**Requirements:**
- Track page views, clicks
- Real-time dashboard
- Historical analysis
- Handle billions of events

**Architecture:**
```text
Client → Collector → Kafka → Stream Processing → OLAP Database
                ↓
        Batch Processing → Data Warehouse
```

**Key Components:**
1. **Collector**: Lightweight event collector
2. **Stream Processing**: Apache Flink for real-time
3. **OLAP Database**: ClickHouse for analytics
4. **Data Warehouse**: For historical analysis

**Event Schema:**
```json
{
  "event_id": "uuid",
  "user_id": "usr_123",
  "event_type": "page_view",
  "url": "/products/123",
  "timestamp": "2025-01-15T10:30:00Z",
  "properties": {...}
}
```

**Scaling:**
- Kafka for event ingestion
- Partitioning by user_id
- ClickHouse for fast aggregations

---

### 9. Design a Content Delivery Network (CDN)

**Requirements:**
- Global content distribution
- Low latency delivery
- Cache invalidation
- Handle static and dynamic content

**Architecture:**
```text
Client → DNS → Edge Server → Origin Server
            ↓
    Geographic Routing
            ↓
    Cache Hierarchy
```

**Key Components:**
1. **Edge Servers**: 10,000+ globally
2. **Origin Servers**: Regional data centers
3. **Cache**: L1 (edge), L2 (regional), L3 (origin)
4. **DNS**: Geographic routing

**Cache Strategy:**
```text
Request → Edge Cache → Regional Cache → Origin
          (10ms)        (50ms)          (100ms)
```

**Scaling:**
- Add edge servers in new regions
- Cache warming for popular content
- Purge API for invalidation

---

### 10. Design a Unique ID Generator

**Requirements:**
- Globally unique IDs
- Chronological ordering
- High availability
- No single point of failure

**Approaches:**

1. **UUID:**
```python
import uuid
id = uuid.uuid4()  # 128-bit random
```

2. **Snowflake (Twitter):**
```text
| 1 bit | 41 bits | 10 bits | 12 bits |
| sign  | timestamp| datacenter| sequence|
```

3. **Database Auto-increment:**
```sql
CREATE SEQUENCE id_sequence;
SELECT nextval('id_sequence');
```

**Trade-offs:**
- UUID: No coordination, but not sortable
- Snowflake: Sortable, but requires clock sync
- DB: Simple, but single point of failure

**Scaling:**
- Snowflake with multiple datacenters
- Database with multiple masters
- Redis INCR for simple cases

---

## Medium Level (11-20)

### 11. Design a Ride-Sharing Service (Uber)

**Requirements:**
- Match riders with drivers
- Real-time location tracking
- ETA calculation
- Surge pricing

**Architecture:**
```text
Rider App → API Gateway → Ride Service → Matching Service
Driver App →               Location Service → Redis GEO
                         Payment Service → Payment Gateway
```

**Key Components:**
1. **Geospatial Index**: Redis GEO for nearby drivers
2. **Matching Algorithm**: Multi-factor scoring
3. **ETA Service**: Integration with mapping APIs
4. **Surge Pricing**: Dynamic pricing based on demand

**Database Schema:**
```sql
CREATE TABLE drivers (
    id BIGSERIAL PRIMARY KEY,
    location GEOGRAPHY(POINT, 4326),
    status VARCHAR(20),
    rating DECIMAL(3,2)
);

CREATE INDEX idx_drivers_location ON drivers USING GIST(location);
```

**Scaling:**
- Geohash-based sharding
- Redis for real-time location
- Kafka for event processing

---

### 12. Design a Social Media Feed (Twitter)

**Requirements:**
- Post tweets
- Follow users
- Timeline generation
- Real-time updates

**Architecture:**
```text
Client → API Gateway → Tweet Service → Fan-out Service
                              ↓
                    Timeline Service → Cache (Redis)
                              ↓
                    Timeline Storage (Cassandra)
```

**Fan-out Strategies:**

1. **Fan-out on Write (Push):**
```python
def post_tweet(user_id, tweet):
    save_tweet(tweet)
    for follower_id in get_followers(user_id):
        add_to_timeline(follower_id, tweet.id)
```

2. **Fan-out on Read (Pull):**
```python
def get_timeline(user_id):
    following = get_following(user_id)
    tweets = []
    for followee_id in following:
        tweets.extend(get_recent_tweets(followee_id))
    return sorted(tweets, key=time, reverse=True)
```

**Hybrid Approach:**
- Fan-out on write for < 10K followers
- Fan-out on read for celebrities

**Scaling:**
- Cassandra for timeline storage
- Redis for hot timelines
- Kafka for fan-out processing

---

### 13. Design a Video Streaming Service (YouTube)

**Requirements:**
- Upload videos
- Stream videos
- Recommendations
- Comments and likes

**Architecture:**
```text
Upload → Transcoding Service → CDN → Client
                ↓
        Metadata Service → Database
                ↓
        Recommendation Service → ML Pipeline
```

**Key Components:**
1. **Transcoding**: Convert to multiple qualities
2. **CDN**: Global content delivery
3. **Adaptive Streaming**: HLS/DASH protocols
4. **Recommendation Engine**: ML-based suggestions

**Transcoding Pipeline:**
```text
Upload → Message Queue → Transcoding Workers → CDN
                ↓
        Multiple Qualities (1080p, 720p, 480p, 360p)
```

**Scaling:**
- Distributed transcoding workers
- Multi-CDN for redundancy
- Adaptive bitrate streaming

---

### 14. Design a Payment System (Stripe)

**Requirements:**
- Process payments
- Idempotency
- Refunds
- Webhooks

**Architecture:**
```text
Client → API Gateway → Payment Service → Payment Processor
                ↓
        Idempotency Service (Redis)
                ↓
        Webhook Service → Merchant
```

**Key Components:**
1. **Idempotency**: Prevent duplicate charges
2. **Payment Routing**: Multiple processors
3. **Fraud Detection**: ML-based scoring
4. **Reconciliation**: Daily settlement

**Idempotency Implementation:**
```python
def process_payment(idempotency_key, payment_data):
    # Check if already processed
    existing = redis.get(f"idempotency:{idempotency_key}")
    if existing:
        return json.loads(existing)

    # Process payment
    result = charge(payment_data)

    # Store result
    redis.setex(
        f"idempotency:{idempotency_key}",
        86400,
        json.dumps(result)
    )

    return result
```

**Scaling:**
- Database sharding by merchant
- Redis for idempotency
- Kafka for async processing

---

### 15. Design a Ticket Booking System

**Requirements:**
- Browse events
- Select seats
- Reserve temporarily
- Process payment

**Architecture:**
```text
Client → API Gateway → Booking Service → Seat Service
                ↓
        Reservation Service (Redis)
                ↓
        Payment Service → Payment Gateway
```

**Key Components:**
1. **Seat Locking**: Redis with TTL
2. **Reservation**: Temporary holds (10 minutes)
3. **Payment**: Idempotent processing
4. **QR Code**: Ticket generation

**Seat Locking:**
```python
def reserve_seat(event_id, seat_id, user_id):
    lock_key = f"seat:{event_id}:{seat_id}"

    # Atomic reserve with TTL
    acquired = redis.set(lock_key, user_id, nx=True, ex=600)

    if acquired:
        return {"status": "reserved", "expires_in": 600}
    else:
        return {"status": "unavailable"}
```

**Scaling:**
- Redis for seat locking
- Database sharding by event
- Queue for flash sales

---

### 16. Design a Search Engine

**Requirements:**
- Full-text search
- Rank results
- Handle billions of documents
- Fast response time

**Architecture:**
```text
Client → API Gateway → Query Parser → Index Service
                              ↓
                    Ranking Service → Results
                              ↓
                    Index Storage (Elasticsearch)
```

**Key Components:**
1. **Indexer**: Build inverted index
2. **Ranker**: TF-IDF, BM25, PageRank
3. **Query Parser**: Parse and expand queries
4. **Index Storage**: Elasticsearch cluster

**Inverted Index:**
```python
# Document: "the cat sat on the mat"
inverted_index = {
    "the": [doc1, doc2],
    "cat": [doc1],
    "sat": [doc1],
    "on": [doc1],
    "mat": [doc1]
}
```

**Scaling:**
- Elasticsearch sharding
- Replicas for read scaling
- Caching frequent queries

---

### 17. Design a Distributed Cache

**Requirements:**
- High performance
- Distributed across nodes
- Cache eviction policies
- Consistency

**Architecture:**
```text
Client → Cache Client → Hash Ring → Cache Nodes
                    ↓
            Replication
                    ↓
            Eviction Policy
```

**Eviction Policies:**
1. **LRU**: Least Recently Used
2. **LFU**: Least Frequently Used
3. **TTL**: Time to Live

**Consistent Hashing:**
```python
class DistributedCache:
    def __init__(self, nodes):
        self.ring = ConsistentHash(nodes)
        self.replication_factor = 3

    def get(self, key):
        node = self.ring.get_node(key)
        return node.get(key)

    def set(self, key, value):
        primary = self.ring.get_node(key)
        primary.set(key, value)

        # Replicate
        for i in range(self.replication_factor):
            replica = self.ring.get_node(f"{key}:{i}")
            replica.set(key, value)
```

**Scaling:**
- Add nodes to hash ring
- Automatic data migration
- Read replicas

---

### 18. Design a Task Scheduler (Cron)

**Requirements:**
- Schedule tasks
- Distributed execution
- Retry logic
- Monitoring

**Architecture:**
```text
Client → API Gateway → Scheduler Service → Task Queue
                                    ↓
                    Worker Pool → Task Execution
                                    ↓
                    Result Storage → Monitoring
```

**Key Components:**
1. **Scheduler**: Cron-like scheduling
2. **Task Queue**: Redis or Kafka
3. **Worker Pool**: Distributed workers
4. **Monitoring**: Track task status

**Task Schema:**
```json
{
  "task_id": "task_123",
  "type": "email",
  "payload": {...},
  "schedule": "0 9 * * *",
  "retries": 3,
  "status": "pending"
}
```

**Scaling:**
- Multiple scheduler instances
- Worker auto-scaling
- Task sharding by type

---

### 19. Design a File Storage System (Dropbox)

**Requirements:**
- Upload/download files
- Sync across devices
- Versioning
- Sharing

**Architecture:**
```text
Client → API Gateway → File Service → Object Storage (S3)
                ↓
        Sync Service → WebSocket
                ↓
        Metadata Service → Database
```

**Key Components:**
1. **Chunking**: Split files into blocks
2. **Deduplication**: Content-based addressing
3. **Sync**: Delta sync for efficiency
4. **Versioning**: Full copy per version

**Chunking:**
```python
def chunk_file(file_data, chunk_size=4*1024*1024):
    chunks = []
    for i in range(0, len(file_data), chunk_size):
        chunk = file_data[i:i+chunk_size]
        chunk_hash = hashlib.sha256(chunk).hexdigest()
        chunks.append({"hash": chunk_hash, "data": chunk})
    return chunks
```

**Scaling:**
- Object storage for file content
- Database sharding for metadata
- CDN for frequent downloads

---

### 20. Design a Metrics Monitoring System

**Requirements:**
- Collect metrics
- Store time-series data
- Query and visualize
- Alerting

**Architecture:**
```text
Agents → Collector → Time-Series DB → Query Engine → Dashboard
                ↓
        Alert Manager → Notifications
```

**Key Components:**
1. **Agents**: Collect metrics from services
2. **Collector**: Aggregate metrics
3. **Time-Series DB**: InfluxDB or Prometheus
4. **Alert Manager**: Threshold-based alerts

**Metrics Schema:**
```json
{
  "metric": "cpu_usage",
  "tags": {"host": "server1", "region": "us-east"},
  "value": 75.5,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Scaling:**
- sharding by metric name
- Aggregation for long-term storage
- Caching for dashboards

---

## Hard Level (21-30)

### 21. Design a Distributed Transaction System

**Requirements:**
- ACID properties
- Distributed across services
- Fault tolerance
- High availability

**Patterns:**

1. **Two-Phase Commit (2PC):**
```text
Coordinator → Prepare (Phase 1) → Participants
            → Commit (Phase 2) → Participants
```

2. **Saga Pattern:**
```text
Order Service → Payment Service → Inventory Service
     ↓              ↓                  ↓
   Compensate   Compensate         Compensate
```

3. **Event Sourcing:**
```python
class EventStore:
    def append(self, event):
        self.events.append(event)

    def get_events(self, aggregate_id):
        return [e for e in self.events
                if e.aggregate_id == aggregate_id]
```

**Trade-offs:**
- 2PC: Strong consistency, but blocking
- Saga: Eventual consistency, but complex
- Event Sourcing: Audit trail, but complex queries

**Scaling:**
- Database per service
- Event-driven communication
- CQRS for read optimization

---

### 22. Design a Real-time Analytics System

**Requirements:**
- Process millions of events/second
- Real-time aggregations
- Low latency queries
- Historical analysis

**Architecture:**
```text
Producers → Kafka → Stream Processing → OLAP Database
                        ↓
                Window Aggregations
                        ↓
                Materialized Views
```

**Key Components:**
1. **Stream Processing**: Apache Flink
2. **OLAP Database**: ClickHouse
3. **Window Functions**: Tumbling, Sliding, Session
4. **Materialized Views**: Pre-computed aggregations

**Stream Processing:**
```sql
SELECT
    window_start,
    COUNT(*) as event_count,
    AVG(value) as avg_value
FROM TABLE(
    TUMBLE(TABLE events, DESCRIPTOR(event_time), INTERVAL '1' MINUTE)
)
GROUP BY window_start;
```

**Scaling:**
- Kafka partitioning
- Flink parallelism
- ClickHouse sharding

---

### 23. Design a Multi-Region Database

**Requirements:**
- Global distribution
- Low latency reads
- Conflict resolution
- High availability

**Architecture:**
```text
Region 1 ←→ Global Load Balancer ←→ Region 2
    ↓                                   ↓
Primary DB ←→ Replication ←→ Read Replicas
```

**Consistency Models:**

1. **Strong Consistency:**
```python
def write(data):
    # Write to all regions
    for region in regions:
        region.write(data)
    # Wait for acknowledgment
    wait_for_quorum()
```

2. **Eventual Consistency:**
```python
def write(data):
    # Write to local region
    local_region.write(data)
    # Async replication
    async_replicate(data)
```

**Conflict Resolution:**
- Last Writer Wins (LWW)
- Vector Clocks
- CRDTs (Conflict-free Replicated Data Types)

**Scaling:**
- Geographic sharding
- Read replicas per region
- Async cross-region replication

---

### 24. Design a Recommendation Engine

**Requirements:**
- Personalized recommendations
- Handle millions of users
- Real-time updates
- A/B testing

**Architecture:**
```text
User Activity → Event Stream → Feature Store → ML Model
                                        ↓
                    Recommendation Service → API
                                        ↓
                    A/B Testing Framework
```

**Algorithms:**

1. **Collaborative Filtering:**
```python
def collaborative_filtering(user_id, matrix):
    # Find similar users
    similar_users = find_similar_users(user_id, matrix)

    # Get their preferences
    recommendations = []
    for user in similar_users:
        recommendations.extend(get_user_preferences(user))

    return rank_recommendations(recommendations)
```

2. **Content-Based:**
```python
def content_based(user_profile, items):
    # Match user profile with item features
    scores = []
    for item in items:
        score = cosine_similarity(user_profile, item.features)
        scores.append((item, score))

    return sorted(scores, key=lambda x: x[1], reverse=True)
```

**Scaling:**
- Feature store for ML features
- Model serving with TensorFlow Serving
- A/B testing with feature flags

---

### 25. Design a Graph Database

**Requirements:**
- Store relationships
- Traverse graphs
- Shortest path
- Community detection

**Architecture:**
```text
Client → Query Parser → Graph Engine → Storage Engine
                    ↓
            Traversal Engine
                    ↓
            Storage (Adjacency List)
```

**Data Model:**
```python
class Node:
    def __init__(self, id, properties):
        self.id = id
        self.properties = properties
        self.edges = []

class Edge:
    def __init__(self, target, properties):
        self.target = target
        self.properties = properties
```

**Shortest Path (BFS):**
```python
def shortest_path(graph, start, end):
    queue = [(start, [start])]
    visited = {start}

    while queue:
        node, path = queue.pop(0)
        if node == end:
            return path

        for neighbor in graph[node].edges:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None
```

**Scaling:**
- Partition by node ID
- Replicate for read scaling
- Cache frequent traversals

---

### 26. Design a Service Mesh

**Requirements:**
- Service-to-service communication
- Load balancing
- Circuit breaking
- Observability

**Architecture:**
```text
Service A ←→ Sidecar Proxy ←→ Sidecar Proxy ←→ Service B
                    ↓
            Control Plane
                    ↓
            Configuration
```

**Key Components:**
1. **Sidecar Proxy**: Envoy proxy per service
2. **Control Plane**: Istio/Linkerd
3. **Data Plane**: Service communication
4. **Observability**: Metrics, logs, traces

**Circuit Breaker:**
```python
class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def call(self, func):
        if self.state == "OPEN":
            raise CircuitOpenError()

        try:
            result = func()
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count > 5:
                self.state = "OPEN"
            raise
```

**Scaling:**
- Multiple control plane instances
- Sidecar proxy per service
- Distributed tracing

---

### 27. Design a Multi-Tenant SaaS

**Requirements:**
- Tenant isolation
- Shared resources
- Customization
- Billing per tenant

**Isolation Models:**

1. **Separate Database:**
```text
Tenant A → Database A
Tenant B → Database B
```

2. **Shared Database, Separate Schema:**
```text
Tenant A → Schema A
Tenant B → Schema B
```

3. **Shared Database, Shared Schema:**
```text
Tenant A ─┐
          ├→ Table with tenant_id
Tenant B ─┘
```

**Row-Level Security:**
```sql
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.tenant_id'));
```

**Scaling:**
- Tenant-based sharding
- Resource quotas per tenant
- Feature flags per tenant

---

### 28. Design a Event-Driven Architecture

**Requirements:**
- Decoupled services
- Event sourcing
- CQRS
- Saga pattern

**Architecture:**
```text
Command → Command Handler → Event Store → Event Bus
                                              ↓
Query ← Read Model ← Projection ← Event Handler
```

**Event Sourcing:**
```python
class EventStore:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)
        self.publish(event)

    def get_events(self, aggregate_id):
        return [e for e in self.events
                if e.aggregate_id == aggregate_id]
```

**CQRS:**
```python
# Command side
def handle_command(command):
    aggregate = load_aggregate(command.aggregate_id)
    aggregate.handle(command)
    event_store.append(aggregate.get_uncommitted_events())

# Query side
def handle_query(query):
    return read_model.query(query)
```

**Scaling:**
- Event partitioning by aggregate
- Multiple event handlers
- Read model optimization

---

### 29. Design a Chaos Engineering Platform

**Requirements:**
- Inject failures
- Monitor impact
- Automatic recovery
- Safety controls

**Architecture:**
```text
Control Plane → Experiment Runner → Target System
                    ↓
            Monitoring → Analysis → Reports
```

**Experiments:**

1. **Network Partition:**
```python
def inject_partition(service_a, service_b):
    # Block traffic between services
    iptables.block(service_a, service_b)

    # Monitor impact
    metrics = monitor(service_a, service_b)

    # Restore
    iptables.allow(service_a, service_b)

    return analyze(metrics)
```

2. **CPU Stress:**
```python
def cpu_stress(target, duration):
    # Inject CPU load
    stress_ng.cpu(target, duration)

    # Monitor recovery
    metrics = monitor(target)

    return analyze(metrics)
```

**Safety Controls:**
- Blast radius limit
- Automatic rollback
- Time limits
- Approval workflow

**Scaling:**
- Distributed experiment execution
- Parallel experiments
- Real-time monitoring

---

### 30. Design a Global Payment Network

**Requirements:**
- Multi-currency support
- Cross-border payments
- Compliance
- High availability

**Architecture:**
```text
Payer → Payer Bank → Payment Network → Payee Bank → Payee
                    ↓
            Currency Conversion
                    ↓
            Compliance Check
                    ↓
            Settlement
```

**Key Components:**
1. **Currency Conversion**: Real-time rates
2. **Compliance**: KYC/AML checks
3. **Settlement**: Net settlement between banks
4. **Fraud Detection**: ML-based scoring

**Payment Flow:**
```text
1. Initiate payment
2. Validate payer
3. Check compliance
4. Convert currency
5. Debit payer account
6. Credit payee account
7. Settlement
```

**Scaling:**
- Regional payment hubs
- Async processing
- Database sharding by region

---

## Summary

### Difficulty Distribution:
- **Easy (1-10)**: URL Shortener, Rate Limiter, Notification System, Chat, Key-Value Store, Web Crawler, Search Autocomplete, Web Analytics, CDN, Unique ID Generator
- **Medium (11-20)**: Ride-Sharing, Social Media Feed, Video Streaming, Payment System, Ticket Booking, Search Engine, Distributed Cache, Task Scheduler, File Storage, Metrics Monitoring
- **Hard (21-30)**: Distributed Transactions, Real-time Analytics, Multi-Region Database, Recommendation Engine, Graph Database, Service Mesh, Multi-Tenant SaaS, Event-Driven Architecture, Chaos Engineering, Global Payment Network

### Key Patterns:
1. **Caching**: Redis for hot data
2. **Message Queue**: Kafka for async processing
3. **Database Sharding**: Horizontal scaling
4. **Circuit Breaker**: Fault tolerance
5. **CQRS**: Read/write optimization
6. **Event Sourcing**: Audit trail
7. **Saga Pattern**: Distributed transactions
8. **Consistent Hashing**: Load distribution

### Interview Tips:
1. **Clarify Requirements**: Ask about scale, latency, availability
2. **Start High-Level**: Draw architecture first
3. **Deep Dive**: Focus on key components
4. **Trade-offs**: Discuss pros and cons
5. **Scalability**: Address growth concerns
6. **Failure Handling**: Discuss error scenarios
7. **Monitoring**: Mention observability

This comprehensive guide covers the most common system design interview questions with detailed answers and scaling considerations.

---

## References & Learn More
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [System Design Interview by Alex Xu](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
- [GitHub - system-design-primer](https://github.com/donnemartin/system-design-primer)
- [High Scalability](http://highscalability.com/)
- [System Design Interview (ByteByteGo)](https://bytebytego.com/)
