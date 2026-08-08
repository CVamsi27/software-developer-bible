---
section: Database
category: Backend
tags: [concept]
---

# SQL vs NoSQL — Choosing the Right Database

> **TL;DR:** SQL and NoSQL are not opposites — they are different tools for different access patterns. Reach for a relational DB (PostgreSQL, MySQL) when you need ACID transactions, joins, and ad-hoc queries; reach for a document store (MongoDB, Firestore) when reads are key-based and the shape is fluid; reach for a wide-column store (DynamoDB, Cassandra) when you need predictable single-digit-ms latency at planet scale. The senior test is the right way to think about the tradeoff, not a tribal allegiance.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

**SQL** (relational) databases store data in tables with a fixed schema, enforce ACID transactions, support joins, and use SQL as the query language. **NoSQL** is an umbrella term for non-relational stores: **document** (MongoDB, CouchDB), **key-value** (Redis, DynamoDB), **wide-column** (Cassandra, HBase), **graph** (Neo4j, Neptune), and **search** (Elasticsearch, OpenSearch). The senior design choice is "what is the dominant access pattern?" — and that drives both the data model and the consistency model.

## Why Do We Need It?

1. **Workload fit** — A 10TB document store for OLTP joins is a mismatch; a relational store for high-cardinality time-series is a mismatch.
2. **Consistency requirements** — Banking needs ACID; a like-counter can tolerate eventual consistency.
3. **Scale ceiling** — Some NoSQL stores (Cassandra, DynamoDB) scale horizontally to millions of writes/sec; vertical scaling of a single Postgres has a ceiling.
4. **Latency predictability** — A single-digit-ms p99 SLA on a real workload is more easily met by DynamoDB than by a generic RDBMS.
5. **Schema flexibility** — A document store lets you evolve the shape without a migration; a relational store makes the schema a contract.
6. **Operational cost** — A managed NoSQL (DynamoDB, Firestore) removes a lot of DB ops; a self-hosted Postgres is cheap at small scale, expensive at large.
7. **Polyglot persistence** — Most senior systems use more than one store: Postgres for the source of truth, Redis for cache, Elasticsearch for search.

## How It Works

### The CAP Triangle

```text
                       Consistency
                          /\
                         /  \
                        /    \
                       /      \
                      /  Pick  \
                     /   any    \
                    /    two     \
                   /              \
            Availability ────────── Partition tolerance
            (you always get a response) (the network WILL drop msgs)
```

In practice, partition tolerance is mandatory (the network always fails), so the real choice is **CP** (consistent, may refuse writes on partition — Postgres, MongoDB with `w:majority`) vs **AP** (available, may diverge — DynamoDB, Cassandra).

### Consistency Models

| Model | What it means | Example |
|-------|----------------|---------|
| Strong | All reads see the latest write | Postgres serializable |
| Read-your-writes | After your write, your reads see it | Postgres read-after-write in same connection |
| Causal | Reads see writes that happened-before | Some NoSQL stores with vector clocks |
| Eventual | Reads eventually see the write (ms to seconds) | DynamoDB, Cassandra |

## Code Examples

### PostgreSQL (Relational)

```sql
-- Strong schema, ACID, joins
CREATE TABLE orders (
  id          UUID PRIMARY KEY,
  customer_id UUID NOT NULL REFERENCES customers(id),
  total       NUMERIC(10, 2) NOT NULL,
  status      TEXT NOT NULL CHECK (status IN ('pending', 'paid', 'shipped')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT c.name, SUM(o.total) AS lifetime_value
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.status = 'paid'
GROUP BY c.id
ORDER BY lifetime_value DESC
LIMIT 100;
```

### MongoDB (Document)

```typescript
// Flexible schema per document, no joins, denormalized reads
const order = await db.collection('orders').insertOne({
  _id: new ObjectId(),
  customerId: 'cus_01',
  items: [
    { sku: 'sku-1', qty: 2, price: 9.99 },
    { sku: 'sku-2', qty: 1, price: 19.99 },
  ],
  total: 39.97,
  status: 'pending',
  createdAt: new Date(),
});

// Read the whole order in one query — no join
const order = await db.collection('orders').findOne({ _id });
```

### DynamoDB (Key-Value / Wide-Column)

```typescript
// Single-digit-ms latency, horizontal scale, pay per RCU/WCU
import { DynamoDBClient, PutItemCommand, GetItemCommand } from '@aws-sdk/client-dynamodb';

const client = new DynamoDBClient({ region: 'us-east-1' });

await client.send(new PutItemCommand({
  TableName: 'Orders',
  Item: {
    PK: { S: 'USER#cus_01' },         // partition key
    SK: { S: 'ORDER#2025-01-15#ord_1' }, // sort key
    total: { N: '39.97' },
    status: { S: 'pending' },
  },
}));

const { Item } = await client.send(new GetItemCommand({
  TableName: 'Orders',
  Key: { PK: { S: 'USER#cus_01' }, SK: { S: 'ORDER#2025-01-15#ord_1' } },
}));
```

### Redis (Key-Value / Cache)

```typescript
// Sub-millisecond reads, ephemeral, in-memory
await redis.set('user:42', JSON.stringify(user), 'EX', 300);
const cached = await redis.get('user:42');
```

### Elasticsearch (Search)

```typescript
// Full-text search, fuzzy match, aggregations
const results = await es.search({
  index: 'products',
  query: { match: { name: { query: 'red shoes', fuzziness: 'AUTO' } } },
  aggs: { by_brand: { terms: { field: 'brand' } } },
});
```

### Neo4j (Graph)

```cypher
// Relationships are first-class; social / fraud / recommendation
MATCH (u:User { id: 42 })-[:FRIEND_OF]->(friend)-[:PURCHASED]->(p:Product)
RETURN p.name, COUNT(*) AS frequency
ORDER BY frequency DESC
LIMIT 10;
```

## Real-World Use Cases

1. **E-commerce order pipeline** — Postgres for orders & payments (ACID), Redis for cart & session, Elasticsearch for product search, S3 for assets.
2. **Social feed** — Cassandra/DynamoDB for the feed (write-heavy, time-ordered), Postgres for the user profile (relational), Neo4j for "people you may know" (graph).
3. **IoT telemetry** — TimescaleDB (Postgres extension) or InfluxDB for time-series; Postgres for device registry.
4. **Real-time analytics** — ClickHouse or BigQuery for OLAP, Postgres for the source of truth, Kafka as the transport.
5. **Multi-tenant SaaS** — Postgres per tenant (or per-shard) for the source of truth; Redis for rate limit and session; Elasticsearch for tenant search.
6. **Catalog / CMS** — MongoDB or Postgres JSONB when the shape is fluid per document; a normalized table when every record has the same fields.
7. **Audit log** — Append-only Postgres or S3 + Athena; never your primary store.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "NoSQL is faster than SQL" | Both can be fast; NoSQL avoids joins, but you pay in denormalization |
| Storing everything in one document to avoid joins | Documents grow, become unindexable, hot-spot in the write path |
| Skipping indexes because "the DB is fast" | NoSQL stores also need index design; a missing index is a seq scan |
| Using MongoDB for money | Use Postgres / a relational store; floats in MongoDB are floats |
| DynamoDB single-partition hot key | Design the partition key for high cardinality; sharding is the first concern |
| Treating eventual consistency as "anything goes" | Document staleness windows; never silently relax them for a financial path |
| Polyglot without a contract | Define the source of truth; every other store is a derived view that can be rebuilt |
| Picking a graph DB "just in case" | Use Postgres for the first 10M relationships; only graduate when the joins are too slow |

## Best Practices

1. **Default to Postgres** — It is the right answer for 80% of OLTP workloads; reach for NoSQL when Postgres fails you, not before.
2. **Pick the access pattern, not the data type** — "What queries will the app run?" is the question, not "is the data structured?"
3. **Use the right tool for the right job** — Polyglot persistence (Postgres + Redis + Elasticsearch) is normal in production.
4. **Source of truth first** — Pick the system of record; everything else is a cache or a derived projection.
5. **Document the consistency model** — Every store has one; make it explicit so the rest of the team knows what to expect.
6. **Plan the data model before the migration** — A bad key design in DynamoDB is a multi-quarter rebuild.
7. **Right-size the operational surface** — Self-hosted Postgres needs a DBA; managed DynamoDB does not. Choose what your team can run.
8. **Use JSONB in Postgres, not MongoDB, when shape is fluid** — Same flexibility, same SQL, same transactions.
9. **Test with production-scale data** — A MongoDB collection that is fast at 10k docs can be unusable at 10M.
10. **Index everything that is read; don't index what is written** — Index design is read-driven; each index costs write performance.

## Performance Considerations

- **Postgres** — Single-node vertical scale; PgBouncer for connection pooling; logical sharding (Citus) when you outgrow one node.
- **MongoDB** — Sharded cluster for write scale; replica set for read scale; index design dominates query performance.
- **DynamoDB** — Single-digit-ms p99 by design; hot-partition is the only failure mode; use adaptive capacity.
- **Cassandra** — Tunable consistency (ONE, QUORUM, ALL); write-heavy by design; read-after-write is a configuration, not a default.
- **Redis** — Sub-ms when in memory; persistence (RDB / AOF) trades durability for performance.
- **Elasticsearch** — Inverted index, near-real-time; index design and shard sizing dominate; expensive on writes.

## Summary

- SQL is the default; NoSQL is a specific tool for a specific workload.
- Pick the access pattern, the consistency model, and the scale ceiling — not the brand.
- Most production systems are polyglot: Postgres (truth) + Redis (cache) + Elasticsearch (search) + S3 (assets) + a queue.
- Document the source of truth and the consistency model for every store.

## Cheat Sheet

| Store | Type | When to use | Avoid when |
|-------|------|-------------|------------|
| PostgreSQL | Relational | OLTP, joins, ACID, ad-hoc queries | You need sub-ms p99 at planet scale |
| MySQL | Relational | Similar to Postgres, mature replication | You need advanced JSONB / extensions |
| MongoDB | Document | Fluid schema per document, denormalized reads | You need cross-document transactions at scale |
| Redis | Key-value | Cache, session, pub/sub, rate limit, leaderboard | You need durability of every write |
| DynamoDB | Wide-column | Predictable single-digit-ms latency, scale | You need ad-hoc queries or joins |
| Cassandra | Wide-column | Write-heavy, multi-region active-active | You need strong consistency |
| Elasticsearch | Search | Full-text, fuzzy, aggregations | You need a source of truth (use as derived view) |
| Neo4j | Graph | Deep relationship queries (fraud, social) | You have < 10M nodes (use Postgres) |
| ClickHouse | OLAP | Analytics over billions of rows | You need single-row low-latency reads |
| S3 + Athena | Object / lake | Cheap durable storage, ad-hoc SQL | You need sub-second reads on hot data |

---

## See Also
- [Microservices](../12-Microservices/) (database per service)
- [REST APIs](../07-REST-API/) (REST over various stores)
- [System Design](../11-System-Design/) (polyglot persistence in designs)
- [Performance Monitoring](../26-Performance-Monitoring/) (query performance)

## References & Learn More

- [CMU — Introduction to Database Systems](https://15445.courses.cs.cmu.edu/)
- [Martin Kleppmann — Designing Data-Intensive Applications](https://dataintensive.net/)
- [AWS — NoSQL vs SQL](https://aws.amazon.com/nosql/sql-vs-nosql/)
- [DynamoDB — Choosing the Right Partition Key](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [MongoDB — Schema Design Patterns](https://www.mongodb.com/blog/post/building-with-patterns-a-summary)
- [CAP Theorem — Brewer's Conjecture](https://en.wikipedia.org/wiki/CAP_theorem)
- [Jepsen — Consistency Model Verification](https://jepsen.io/)
