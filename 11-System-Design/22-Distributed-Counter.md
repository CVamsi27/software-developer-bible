---
section: System Design
category: Architecture
tags: [concept]
---

# Distributed Counter / Metrics Aggregation System Design

## TL;DR

Design a system that counts events at massive scale (likes, page views, ad impressions, votes) across millions of keys, with strong-per-key consistency, sub-second freshness on dashboards, and horizontal scalability.

**Why it matters:** One of the most common senior interview questions disguised as a "simple" problem. The naive `UPDATE counter SET n = n + 1` doesn't scale past 1K QPS per key. Tests your grasp of **contention, sharding, eventual consistency, and the trade-offs between CRDTs, batching, and tiered storage**.

## Requirements

### Functional Requirements

- Increment / decrement a counter by a key (e.g., `likes:post_123`)
- Get the current value of a counter
- Sum / aggregate counters across a prefix (e.g., total likes on a user's posts)
- Time-windowed counters (e.g., "views in the last 5 minutes" for trending)
- Bulk increment (batch from an event stream)
- Idempotent operations (or at-least-once delivery handling)

### Non-Functional Requirements

- 1M+ keys, 100K QPS sustained, 1M QPS peak
- Sub-second read latency for hot counters (p99 < 100ms)
- Strong consistency per key (no lost increments on the same key)
- Eventually consistent for cross-key aggregates (5–30s lag OK)
- Durable: no counter regression after a node crash
- Multi-region with regional write affinity

## Capacity Estimation

```text
QPS:
- 1M events/sec across all counters
- Top 1% of keys absorb 50% of writes (long tail, Zipfian)
- A single hot key (viral post) can absorb 100K writes/sec

Storage:
- 1B distinct counters × 16 bytes = 16 GB raw state
- With time-windowed (60 buckets × 1B counters): 60 GB hot, 1 TB cold
- Per-counter audit log (for backfill): 1M events/sec × 100 bytes = 100 MB/s = 8.6 TB/day

```

## API Design

```yaml
# Increment
POST /v1/counters/{key}:increment
  Body: { "delta": 1, "idempotency_key": "uuid-..." }
  Response: 200 { "key": "post:123:likes", "value": 12345, "ts": "..." }

# Get
GET /v1/counters/{key}
  Response: 200 { "key": "post:123:likes", "value": 12345 }

# Bulk get
POST /v1/counters/_bulk
  Body: { "keys": ["post:123:likes", "post:456:likes", ...] }
  Response: { "counters": { "post:123:likes": 12345, ... } }

# Time-windowed
GET /v1/counters/{key}/window?bucket=1m&from=...&to=...
  Response: { "buckets": [ { "ts": "2026-07-15T10:30:00Z", "value": 4500 }, ... ] }

```

## Database Design

### Storage Tiers

| Tier | Use case | Tech | Latency |
|---|---|---|---|
| Hot (in-memory) | Most-accessed 1% of counters | Redis cluster, sorted set or hash | < 5ms |
| Warm (on-disk) | Recently-written counters | Cassandra, RocksDB (LSM tree) | < 50ms |
| Cold (historical) | Old / sparse counters | S3 + Athena / BigQuery | seconds |
| Time-series | Time-windowed buckets | ClickHouse, TimescaleDB, Druid | < 500ms |

```sql
-- Hot counter table (Redis HASH, sharded by key)
HSET counters:post:123 likes 12345 shares 89

-- Persistent store (Cassandra / sharded PostgreSQL)
CREATE TABLE counters (
    key          VARCHAR(255) PRIMARY KEY,
    value        BIGINT NOT NULL,
    updated_at   TIMESTAMPTZ NOT NULL
);

-- Time-windowed (Cassandra or ClickHouse)
CREATE TABLE counter_buckets (
    key          VARCHAR(255),
    bucket_ts    TIMESTAMP,        -- truncated to bucket size
    value        BIGINT,
    PRIMARY KEY (key, bucket_ts)
);
```

## Architecture

### ASCII Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────┐
│                DISTRIBUTED COUNTER STACK                            │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Clients / Producers                                                │
│       │                                                             │
│       ▼                                                             │
│  Ingest API (rate limit, idempotency key dedupe)                    │
│       │                                                             │
│       ├──▶ Redis (hot counters, HASH/Sorted Set, sharded)           │
│       │              │                                              │
│       │              └─▶ Async flush to Cassandra (durable)         │
│       │                                                                 │
│       ├──▶ Kafka `counter.events` (every increment)                  │
│       │              │                                              │
│       │              ├─▶ Batch flusher (1s batches to Redis/C*)    │
│       │              ├─▶ Time-series indexer (ClickHouse)           │
│       │              └─▶ Analytics / fraud detection                │
│       │                                                                 │
│       └──▶ Read path:                                              │
│              Hot key → Redis (O(1) HGET)                            │
│              Cold key → Cassandra → optional Redis cache            │
│              Windowed → ClickHouse / Druid                          │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## Key Components

### Naive Approach (and Why It Fails)

```sql
-- Single Postgres row, single writer
UPDATE counters SET value = value + 1 WHERE key = 'post:123';
-- Locks the row, serializes all writes to that key
-- At 100K writes/sec to one key, you get 100K lock-acquire cycles
-- Postgres tops out around 5K–20K QPS on hot rows
```

The hot-key contention is the **core problem** of distributed counters.

### Strategy 1: Per-Key Sharding + Aggregation

For a hot key like `post:viral:likes`, instead of one row, use **N shards** and aggregate on read:

```text
Hot key "post:viral:likes" → 16 shards:
  counters:post:viral:likes:0 = 0
  counters:post:viral:likes:1 = 0
  ...
  counters:post:viral:likes:15 = 0

Write:  INCR random shard (load-balanced)
Read:   SUM all 16 shards
```

- **Pro**: linearizes the hot key across N counters
- **Con**: reads are N× more expensive (16× for 16 shards)
- **Con**: cannot decrement atomically across shards

For mostly-increment workloads (likes, views, impressions), this is the right trade.

### Strategy 2: Local Counters + Async Flush

Each app server keeps a **local in-memory counter** (per process). Flushes to Redis/Cassandra every 1–5s:

```python
class LocalCounter:
    def __init__(self):
        self.counts = {}
        self.last_flush = time.time()

    def inc(self, key: str, delta: int = 1):
        self.counts[key] = self.counts.get(key, 0) + delta
        if time.time() - self.last_flush > 1.0:
            self.flush()

    def flush(self):
        # Send the delta to Kafka; downstream aggregator applies
        for k, v in self.counts.items():
            kafka.send('counter.events', key=k, value=v)
        self.counts.clear()
        self.last_flush = time.time()
```

- **Pro**: zero contention, no per-write IO
- **Con**: a process crash loses the unflushed delta
- **Con**: reads are eventually consistent (up to flush interval stale)

### Strategy 3: CRDT (G-Counter)

A **G-Counter** is a state-based CRDT where each node has its own slot:

```text
G-Counter for key "post:123:likes":
  Node A: 4500
  Node B: 4300
  Node C: 4200
  ─────────────
  Total:  13000   (sum across nodes)
```

- Each node increments its own slot (no contention)
- Total = sum of all slots (idempotent, commutative, associative)
- Eventually consistent: any node sees the truth once all slots are merged
- **Pro**: no locks, no central write coordination
- **Con**: read cost grows with node count
- **Con**: deletions / decrements require a separate PN-Counter structure

### Strategy 4: Tiered (Hot/Warm/Cold) with Batched Writes

The pragmatic approach for most production systems:

```text
Write path:
  1. Client sends increment
  2. Increment in Redis (sub-ms, atomic)
  3. Fire-and-forget Kafka event for durable ledger
  4. Periodic Redis → Cassandra flush (every 5s, batched)
  5. Periodic Cassandra → cold storage archival (daily)

Read path:
  1. Hot key (last 60s accessed): read from Redis
  2. Otherwise: read from Cassandra
  3. Windowed: read from ClickHouse / Druid
```

## Hot-Key Problem (Detail)

A viral post gets 100K likes/sec. A single Redis key on a single shard becomes the bottleneck.

**Solution A: Key splitting (per-shard)**

```python
import random
SHARD_COUNT = 64

def incr_hot(key: str) -> int:
    shard = random.randint(0, SHARD_COUNT - 1)
    return redis.incr(f"{key}:s{shard}")

def get_hot(key: str) -> int:
    pipe = redis.pipeline()
    for i in range(SHARD_COUNT):
        pipe.get(f"{key}:s{i}")
    return sum(int(v or 0) for v in pipe.execute())
```

**Solution B: Local pre-aggregation per server**

```python
# Each app server aggregates locally for 1s, then sends a single INCRBY
class PerServerAggregator:
    def __init__(self):
        self.local = {}
        self.last_flush = time.time()

    def inc(self, key, delta=1):
        self.local[key] = self.local.get(key, 0) + delta
        if time.time() - self.last_flush > 1.0:
            self.flush_all()

    def flush_all(self):
        with redis.pipeline() as pipe:
            for k, v in self.local.items():
                pipe.incrby(k, v)
            pipe.execute()
        self.local.clear()
        self.last_flush = time.time()
```

100K writes/sec on the wire becomes 1 INCRBY per key per second per server. With 1K app servers, that's 1K INCRBYs/sec — well within Redis capacity.

## Caching Strategy

| Cache | Stores | TTL | Invalidation |
|---|---|---|---|
| Redis | Hot counters (top 1% by QPS) | Persistent, evict cold keys | LRU + warm-up job |
| Memcached | Recently-read cold counters | 1 min | TTL |
| CDN | Aggregated dashboards | 1 min | WebSocket push on increment |

## Message Queue

Kafka topic `counter.events`:
- Each event: `{ key, delta, ts, source_node }`
- Used for: durable ledger, time-series indexer, fraud detection, analytics
- **Partition by key** for ordered processing per counter (but local pre-aggregation breaks this guarantee — accept eventual consistency)
- Retention: 7 days hot, then cold S3 archive

## Scaling Strategy

| Bottleneck | Solution |
|---|---|
| Hot key (100K writes/sec) | Local pre-aggregation + key sharding |
| Read fan-out (100K keys per dashboard) | Pre-compute and cache dashboard in Memcached |
| Redis memory | Tier out cold counters to Cassandra; only keep hot 10% in Redis |
| Idempotency on retries | Idempotency key dedupe window (5 min) in Redis SET |
| Cross-region consistency | Per-region counters; CRDT merge async between regions |
| Time-windowed queries at scale | Pre-aggregate to ClickHouse / Druid at write time |

## Failure Handling

| Failure | Mitigation |
|---|---|
| Redis node down | Redis cluster auto-failover; replicas serve reads |
| Local pre-aggregation lost on crash | Acceptable for non-critical counters; critical counters go direct to Redis |
| Cassandra write backlog | Buffer in Kafka; replay when recovered |
| Hot key shard imbalance | Re-shard by hash of `(key, time-bucket)` for time-windowed |
| Aggregator lag | Alert when dashboard read latency > 5s; degrade to stale data with banner |
| Idempotency key collision | Use `request_id` (UUIDv4) per attempt; store in Redis SET with TTL |

## Monitoring

- **QPS per tier**: Redis INCR/sec, Cassandra write/sec, Kafka throughput
- **Hot key watch**: top 100 keys by write rate (alert if any exceeds 10K/sec)
- **Local aggregator flush lag**: p99 time between local inc and Redis write
- **Dashboard freshness**: time since last successful aggregation
- **Redis memory**: used / max, eviction rate
- **Read latency**: p50/p95/p99 per tier

Alerts: any key > 50K writes/sec, Redis memory > 80%, aggregator lag > 5s, dashboard stale > 30s.

## Trade-offs

| Decision | Option A | Option B | Choice |
|---|---|---|---|
| Hot key | Single Redis key | Per-shard split | Split for > 10K QPS |
| Write path | Direct Redis | Local + batched | Batched (write throughput, eventual OK) |
| Counter type | Monotonic (G-Counter) | Monotonic + decrement (PN-Counter) | G-Counter unless decrements needed |
| Time-series | ClickHouse | Druid | ClickHouse (latency + SQL) |
| Read consistency | Strong | Eventual | Eventually consistent (5–30s) |
| Idempotency | Server-dedupe by request ID | At-most-once | At-least-once with dedupe window |
| Cross-region | Synchronous replication | CRDT merge | CRDT merge (latency vs consistency) |
| Cold storage | Keep in Cassandra forever | Archive to S3 | S3 (cost) |

## Summary

- **Hot key** is the core problem — and the right answer is **local pre-aggregation + per-shard split + tiered storage**.
- **Don't** use a single-row SQL `UPDATE` for a hot counter; it locks and serializes.
- **G-Counter CRDT** is elegant for monotonic counters in distributed settings but is overkill for most production systems.
- **Tiered** (Redis hot / Cassandra warm / ClickHouse time-series / S3 cold) is the realistic answer.
- **Reads** can be eventually consistent; **writes** need to be durable and at-least-once with idempotency.
- **Idempotency keys** + dedupe window handle the "client retried, did we double-count?" problem.

---

## See Also
- [Database](../08-Database/)
- [Microservices](../12-Microservices/)
- [Rate Limiter](13-Rate-Limiter.md) (similar token-bucket math)
- [System Design Interview Questions](16-Interview-Questions.md)
- [Twitter Feed](12-Twitter-Feed.md) (counters for like/retweet counts)

## References & Learn More

- [DynamoDB — Atomic counters](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [Cassandra Counters](https://cassandra.apache.org/doc/latest/cassandra/operating/counters.html)
- [Redis INCR pattern](https://redis.io/commands/incr/)
- [CRDTs — Shapiro et al. (INRIA)](https://hal.inria.fr/inria-00609399v1/document)
- [ClickHouse — Real-time analytics DB](https://clickhouse.com/)
- [Alex Xu — System Design Vol 2 (Metrics aggregation chapter)](https://bytebytego.com/)
- [Designing Data-Intensive Applications — Kleppmann (Ch. 5: Replication)](https://dataintensive.net/)
