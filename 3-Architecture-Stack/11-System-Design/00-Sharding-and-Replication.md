---
section: System Design
category: Architecture
tags: [concept, distributed-systems, scaling, theory]
---

# Sharding & Replication

> **Two ways to scale a database.** Sharding splits data across nodes (horizontal partitioning). Replication copies data to multiple nodes. Most production systems use **both**. This is the foundation of every "how do you scale X" question in system design.

## TL;DR

- **Sharding** = split data across nodes by some key. Each node has a subset of the data. For write/read scale.
- **Replication** = copy data to multiple nodes. For read scale, availability, durability.
- **Sharding strategies:** hash-based, range-based, directory-based, geography-based.
- **Replication strategies:** single-leader, multi-leader, leaderless (quorum).
- **Most systems use both:** sharded + replicated within each shard.
- **In interviews: state your key, your sharding strategy, your replication strategy, and your rebalancing plan.**

---

## Why it matters

Every "how would you scale this to 1M users" question comes down to:

1. **Sharding** to handle more writes (a single node can't write fast enough)
2. **Replication** to handle more reads (a single node can't serve enough reads)
3. **Replication** for durability (don't lose data if a node dies)
4. **Replication** for availability (don't go down if a node dies)

You can't bluff this. The interviewer will ask "how do you handle 100x the load" and expect a specific answer about sharding + replication.

---

## Sharding (Partitioning)

**Sharding** = split a dataset across multiple nodes. Each node holds a **subset** of the data. A **shard key** determines which node a row goes to.

### Sharding strategies

#### 1. Hash-based sharding

```
shard_id = hash(shard_key) % num_shards
```

**Example:** `shard_id = hash(user_id) % 4`
- user 1 → shard 0
- user 2 → shard 3
- user 3 → shard 2
- user 4 → shard 1

**Pros:**
- Even distribution (if hash is good)
- Simple

**Cons:**
- Hard to do range queries ("give me all users with id 1-1000")
- Rebalancing is hard (changing `num_shards` reshuffles everything → consistent hashing solves this)
- Hot shards possible (if key distribution is skewed)

**Used by:** Cassandra, DynamoDB, Riak, most KV stores

#### 2. Range-based sharding

```
shard_0: keys 0 - 999
shard_1: keys 1000 - 1999
shard_2: keys 2000 - 2999
```

**Pros:**
- Range queries are efficient
- Easy to add shards (split a range)
- Easy to understand

**Cons:**
- Hot shards (recent data on the latest shard gets all the writes)
- Uneven distribution if keys aren't uniform

**Used by:** HBase, Bigtable, MongoDB (with shard key), Postgres (with partitioning)

#### 3. Directory-based sharding

A lookup table maps keys to shards.

```
lookup_table = {
  "user_1_1000": "shard_0",
  "user_1001_2000": "shard_1",
  ...
}
```

**Pros:**
- Flexible (can move individual users to balance)
- Can use any routing logic

**Cons:**
- Lookup table is a single point of failure / bottleneck
- Needs to be replicated and consistent

**Used by:** Older systems, some custom solutions. Not common in modern systems.

#### 4. Geography-based sharding

Shards by region: EU shard, US shard, APAC shard.

**Pros:**
- Low latency (data is in the user's region)
- Regulatory compliance (GDPR data stays in EU)

**Cons:**
- Cross-region queries are slow
- Cross-region writes are very slow
- Imbalanced if traffic isn't uniform

**Used by:** Most multi-region systems (CockroachDB, Spanner, large SaaS apps)

### Choosing a shard key

The most important decision. The shard key should:

1. **High cardinality** (lots of distinct values, to avoid hot shards)
2. **Even distribution** (no skew, e.g., don't use `country` if 80% of users are in India)
3. **Query-aligned** (most queries should hit one shard, not all)

**Common shard keys:**
- `user_id` (most common for user-centric apps)
- `tenant_id` (for B2B SaaS)
- `order_id` (for e-commerce)
- `device_id` (for IoT)
- `time` (for time-series data, e.g., logs)

**Anti-patterns:**
- `country` (low cardinality, skewed)
- `status` (low cardinality)
- `created_at` alone (hot shard for recent data)

### Rebalancing

When you add a shard, you need to redistribute data:

- **Hash-based:** changing `num_shards` reshuffles everything. **Consistent hashing** fixes this — only `1/N` of keys move.
- **Range-based:** split one range into two. Easy.
- **Directory-based:** update the lookup table.

**Consistent hashing:** the hash space is a ring. Each shard owns a range. When you add a shard, only the new shard's range moves. Used by Cassandra, DynamoDB, most modern KV stores.

---

## Replication

**Replication** = copy the same data to multiple nodes. For reads, availability, durability.

### Replication strategies

#### 1. Single-leader (primary-replica)

One node (the leader) accepts writes. Reads can hit any node. Other nodes (followers/replicas) get the writes via replication.

```
        Client
          │
          ▼
       Leader (writes)
          │
          ├──→ Follower 1 (read-only, async replication)
          ├──→ Follower 2 (read-only, async replication)
          └──→ Follower 3 (read-only, async replication)
```

**Pros:**
- Simple
- Strong consistency possible (with sync replication)
- No write conflicts

**Cons:**
- Single point of failure (if leader dies, must elect a new one)
- Replication lag = stale reads (with async)

**Used by:** Postgres, MySQL, MongoDB, most RDBMS

**Variants:**
- **Synchronous replication:** leader waits for replicas to acknowledge before responding. Strong consistency, but higher latency.
- **Asynchronous replication:** leader responds immediately, replicates in the background. Lower latency, but possible data loss if leader dies before replication.

#### 2. Multi-leader (multi-master)

Multiple nodes accept writes. They sync to each other.

```
        Client ──→ Leader 1 ──┐
                ↗              ↘
        Client ──→ Leader 2 ──→ (sync between leaders)
                ↗              ↗
        Client ──→ Leader 3 ──┘
```

**Pros:**
- High write availability
- Multi-region writes

**Cons:**
- Write conflicts (need to resolve)
- More complex
- Eventual consistency guaranteed

**Used by:** CouchDB (sort of), Cassandra (with caveats), some multi-region setups

#### 3. Leaderless (quorum)

Any node can accept reads and writes. Reads and writes use a quorum to ensure consistency.

```
N = total replicas
W = write quorum (how many must acknowledge)
R = read quorum (how many must respond)

If W + R > N, the read will see the most recent write (strong consistency)
```

**Example:** N=3, W=2, R=2
- Write must be acknowledged by 2 of 3 nodes
- Read must respond from 2 of 3 nodes
- W + R = 4 > 3, so the read will see the write

**Common configs:**
- N=3, W=2, R=2 (Quorum, strong consistency)
- N=3, W=1, R=1 (Fast, but reads might not see writes)
- N=3, W=3, R=1 (Strong writes, fast reads)

**Pros:**
- High availability (any node can serve)
- Tunable consistency per query

**Cons:**
- Eventual consistency (sloppy quorum) common
- Conflict resolution (vector clocks, last-write-wins)
- Hinted handoff for failed writes

**Used by:** Cassandra (default), DynamoDB, Riak, Voldemort

---

## Replication lag and consistency

With async replication, there's a delay between leader and followers:

```
t=0: Leader writes x=1
t=10ms: Follower 1 replicates x=1
t=50ms: Follower 2 replicates x=1
t=200ms: Follower 3 replicates x=1 (slow)
```

During this lag, reads from Follower 3 return the old value. This is the source of the "stale read" problem.

**Solutions:**
- **Read-after-write consistency:** after a write, the client reads from the leader
- **Synchronous replication:** no lag, but higher write latency
- **Quorum reads with version numbers:** read from majority, pick newest

---

## Combining sharding + replication

**Most production systems use both:**

```
Sharded + Replicated
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Shard 0    │  │  Shard 1    │  │  Shard 2    │
│  ┌───┐      │  │  ┌───┐      │  │  ┌───┐      │
│  │ L │ Repl │  │  │ L │ Repl │  │  │ L │ Repl │
│  │ F │ F    │  │  │ F │ F    │  │  │ F │ F    │
│  │ F │      │  │  │ F │      │  │  │ F │      │
│  └───┘      │  │  └───┘      │  │  └───┘      │
└─────────────┘  └─────────────┘  └─────────────┘
```

- Sharding handles write scale (each shard handles a subset of writes)
- Replication within each shard handles read scale and durability
- Sharding key determines which shard a row goes to
- Replication factor (RF) determines how many copies exist

**Example:** DynamoDB with 100 shards, RF=3 = 300 nodes total. Each shard has a leader and 2 replicas.

---

## Sharding + Replication in interviews

When you discuss a database in a system design round, name:

1. **Sharding strategy** (hash, range, geography)
2. **Shard key** (user_id, tenant_id, etc.) and why
3. **Replication strategy** (single-leader, multi-leader, leaderless)
4. **Replication factor** (RF=3 typical)
5. **Consistency model** (linearizable, eventual, etc.)
6. **Rebalancing plan** (consistent hashing, range split, directory update)

**Example:**
> "For user data, we shard by hash of user_id across 16 shards. Each shard has a leader and 2 followers (RF=3) with synchronous replication. This gives us linearizable consistency for account balance, and read-after-write for user profile. To rebalance, we use consistent hashing with virtual nodes so adding a 17th shard only moves 1/17 of the data."

That's the senior signal. Not "we use Postgres" — "we use sharded + replicated Postgres with these specific properties."

---

## Failure modes

- **Shard becomes unreachable:** with replication, reads/writes can hit replicas. If leader is down, followers can take over (with election).
- **Replica lag:** reads return stale data. Mitigated with read-your-writes routing.
- **Split brain:** two leaders think they're primary. Mitigated with consensus (only one can win).
- **Hot shard:** one shard gets disproportionate traffic. Mitigated by re-sharding the hot key.
- **Rebalancing during failure:** adding a shard while a node is down. Mitigated by careful operational planning.

---

## Specific technologies

| Tech | Sharding | Replication | Consistency |
|------|----------|-------------|-------------|
| **Postgres** | Manual (pg_partman, Citus) | Synchronous / async / logical | Strong (sync) or eventual (async) |
| **MySQL** | Manual (Vitess) | Async / semi-sync | Strong (semi-sync) or eventual (async) |
| **MongoDB** | Built-in (shard key) | Replica set | Tunable (write concern) |
| **Cassandra** | Built-in (partition key) | Leaderless (quorum) | Tunable (CL = ONE, QUORUM, ALL) |
| **DynamoDB** | Built-in (partition key) | Leaderless (quorum) | Tunable (R + W config) |
| **Spanner** | Built-in | Synchronous + TrueTime | Linearizable globally |
| **CockroachDB** | Built-in (range) | Synchronous (Raft) | Linearizable |
| **HBase** | Built-in (range) | Single-leader (HDFS) | Strong |
| **Redis Cluster** | Hash slot | Async | Eventual (by default) |
| **Elasticsearch** | Built-in (shard) | Async | Eventual (near real-time) |

---

## Related concepts

- [00-CAP-Theorem.md](00-CAP-Theorem.md) — the trade-off framework
- [00-Consistency-Models.md](00-Consistency-Models.md) — strong vs eventual vs causal
- [00-Consensus-and-Leader-Election.md](00-Consensus-and-Leader-Election.md) — how to elect a leader
- [00-Distributed-Transactions.md](00-Distributed-Transactions.md) — when you need to update multiple shards atomically

---

## TL;DR

- **Sharding** = split data across nodes (write scale). Hash, range, geography, directory.
- **Replication** = copy data to multiple nodes (read scale, durability, availability). Single-leader, multi-leader, leaderless.
- **Pick a shard key** that has high cardinality, even distribution, and is query-aligned.
- **Most systems use both** — sharded AND replicated.
- **In interviews: name the sharding strategy, shard key, replication strategy, RF, consistency model, and rebalancing plan.**

For case studies, see [01-URL-Shortener.md](01-URL-Shortener.md) (range sharding), [02-WhatsApp.md](02-WhatsApp.md) (hash sharding by user_id), [18-Instagram.md](18-Instagram.md) (sharded by user_id), [22-Distributed-Counter.md](22-Distributed-Counter.md) (hot shard mitigation).
