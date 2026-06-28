# Database Interview Questions - Comprehensive Guide

## Definition

This guide contains 40 of the most commonly asked database/PostgreSQL interview questions, categorized by difficulty level. Each question includes a detailed answer to help you understand the concept and articulate it clearly in interviews.

## Why Do We Need It?

- **Interview Preparation**: Master common database questions
- **Concept Understanding**: Deep dive into key topics
- **Communication Skills**: Learn how to articulate answers clearly
- **Knowledge Gap Identification**: Find areas to improve
- **Confidence Building**: Prepare for any question

## How It Works

```text
┌─────────────────────────────────────────────────────────────┐
│                    Question Categories                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Beginner (5 questions)                             │   │
│  │  • Basic concepts and terminology                   │   │
│  │  • Simple operations and commands                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Intermediate (5 questions)                         │   │
│  │  • Design patterns and trade-offs                   │   │
│  │  • Performance considerations                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Senior (10 questions)                              │   │
│  │  • Architecture and internals                       │   │
│  │  • Complex scenarios and optimization               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FAANG-style (5 questions)                          │   │
│  │  • System design and scalability                    │   │
│  │  • Distributed systems and advanced concepts        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Follow-ups (5 questions)                           │   │
│  │  • Deep dives and edge cases                        │   │
│  │  • Real-world scenarios                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Beginner Questions (5)

### 1. What is PostgreSQL?

**Answer:**
PostgreSQL is a powerful, open-source, object-relational database management system (ORDBMS) with over 30 years of active development. It extends SQL with features like custom data types, functions, operators, and index methods.

**Key points:**
- ACID-compliant
- Supports MVCC (Multi-Version Concurrency Control)
- Extensible with custom types, functions, and extensions
- Standards-compliant SQL
- JSONB support for NoSQL capabilities
- Built-in replication and high availability

**Example:**
```sql
-- Basic PostgreSQL features
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}'
);

-- JSONB query
SELECT * FROM users WHERE metadata->>'role' = 'admin';

-- Array query
SELECT * WHERE 'premium' = ANY(tags);
```

### 2. What is a primary key and foreign key?

**Answer:**
A **primary key** is a column (or set of columns) that uniquely identifies each row in a table. It cannot contain NULL values and must be unique.

A **foreign key** is a column (or set of columns) that references a primary key in another table, establishing a relationship between the two tables.

**Example:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Primary key
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),  -- Foreign key
    total DECIMAL(10, 2)
);
```

**Why important:**
- Enforces referential integrity
- Prevents orphaned records
- Enables JOIN operations
- Documents relationships between tables

### 3. What is the difference between WHERE and HAVING?

**Answer:**
- **WHERE** filters rows before GROUP BY aggregation
- **HAVING** filters groups after GROUP BY aggregation

**Example:**
```sql
-- WHERE: filters before aggregation
SELECT user_id, COUNT(*) AS order_count
FROM orders
WHERE created_at > '2024-01-01'  -- Filter rows first
GROUP BY user_id;

-- HAVING: filters after aggregation
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 5;  -- Filter groups after
```

### 4. What is an index and why use it?

**Answer:**
An index is a data structure that improves the speed of data retrieval operations at the cost of additional storage and write overhead.

**Why use indexes:**
- Faster queries (O(log n) vs O(n))
- Enforce uniqueness
- Improve JOIN performance
- Support efficient filtering

**Example:**
```sql
-- Without index: Sequential scan
SELECT * FROM users WHERE email = 'test@example.com';

-- With index: Index scan
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'test@example.com';
```

### 5. What is a JOIN?

**Answer:**
A JOIN combines rows from two or more tables based on a related column between them.

**Types of JOINs:**
- **INNER JOIN**: Only matching rows
- **LEFT JOIN**: All from left + matching from right
- **RIGHT JOIN**: All from right + matching from left
- **FULL JOIN**: All from both tables
- **CROSS JOIN**: All combinations

**Example:**
```sql
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

## Intermediate Questions (5)

### 6. Explain normalization and its forms.

**Answer:**
Normalization is the process of organizing a database to reduce redundancy and improve integrity.

**Normal forms:**
- **1NF**: Atomic values, no repeating groups
- **2NF**: 1NF + no partial dependencies
- **3NF**: 2NF + no transitive dependencies
- **BCNF**: 3NF + every determinant is a candidate key

**Example:**
```sql
-- Unnormalized
CREATE TABLE orders_bad (
    id INT,
    customer_name TEXT,
    product1 TEXT,
    product2 TEXT
);

-- 3NF
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id)
);

CREATE TABLE order_items (
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT
);
```

### 7. What is the difference between DELETE and TRUNCATE?

**Answer:**
| Feature | DELETE | TRUNCATE |
|---------|--------|----------|
| Type | DML | DDL |
| WHERE clause | Yes | No |
| Rollback | Yes | No (in most cases) |
| Triggers | Fires | Does not fire |
| Speed | Slower | Faster |
| Reset counter | No | Yes (resets IDENTITY) |

**Example:**
```sql
-- DELETE: Removes specific rows, logs each delete
DELETE FROM users WHERE id = 1;

-- TRUNCATE: Removes all rows, resets counters
TRUNCATE TABLE users;
```

### 8. What is the difference between INNER JOIN and LEFT JOIN?

**Answer:**
- **INNER JOIN**: Returns only rows with matches in both tables
- **LEFT JOIN**: Returns all rows from left table + matching from right (NULLs if no match)

**Example:**
```sql
-- INNER JOIN: Only users with orders
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: All users, including those without orders
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- Users without orders have NULL in o.total
```

### 9. What is a transaction?

**Answer:**
A transaction is a logical unit of work that maintains ACID properties:
- **Atomicity**: All or nothing
- **Consistency**: Valid state transitions
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data persists

**Example:**
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### 10. What is an execution plan?

**Answer:**
An execution plan shows how PostgreSQL will execute a query, including:
- Scan types (Seq Scan, Index Scan)
- Join algorithms (Nested Loop, Hash Join)
- Cost estimates
- Estimated rows

**Example:**
```sql
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';
-- Shows which index is used, estimated vs actual rows
```

## Senior Questions (10)

### 11. Explain MVCC and how PostgreSQL implements it.

**Answer:**
MVCC (Multi-Version Concurrency Control) maintains multiple versions of data objects. Each transaction sees a consistent snapshot without blocking others.

**PostgreSQL implementation:**
- Each row has `xmin` (creating xid) and `xmax` (deleting xid)
- Old versions kept until VACUUM
- Readers don't block writers
- Writers don't block readers

**Example:**
```sql
-- Check tuple versions
SELECT ctid, xmin, xmax, * FROM users WHERE id = 1;

-- xmin: transaction that created the row
-- xmax: transaction that deleted/updated the row (0 if not deleted)
```

### 12. What is WAL and why is it important?

**Answer:**
WAL (Write-Ahead Logging) ensures durability by writing changes to a log before applying them to the data files.

**Importance:**
- Enables crash recovery
- Supports point-in-time recovery
- Enables streaming replication
- Improves write performance (sequential vs random I/O)

**Example:**
```sql
-- WAL location
SHOW wal_level;
SHOW archive_mode;
SHOW archive_command;
```

### 13. How does PostgreSQL handle concurrent updates?

**Answer:**
PostgreSQL uses MVCC with last-commit-wins semantics:
1. Transaction reads snapshot
2. Transaction modifies data
3. At commit, PostgreSQL checks for conflicts
4. If conflict: serialization error (Serializable) or last commit wins (Read Committed)

**Example:**
```sql
-- Read Committed: last commit wins
-- Session 1: UPDATE accounts SET balance = 200 WHERE id = 1;
-- Session 2: UPDATE accounts SET balance = 300 WHERE id = 1;
-- Result: 300 (Session 2 wins)

-- Serializable: raises error
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Similar scenario raises serialization_failure
```

### 14. What is a GIN index?

**Answer:**
GIN (Generalized Inverted Index) is for composite values like arrays, JSONB, and full-text search.

**Use cases:**
- JSONB containment queries
- Array element queries
- Full-text search
- hstore key-value queries

**Example:**
```sql
-- GIN for JSONB
CREATE INDEX idx_metadata ON events USING GIN (metadata);
SELECT * FROM events WHERE metadata @> '{"type": "signup"}';

-- GIN for arrays
CREATE INDEX idx_tags ON products USING GIN (tags);
SELECT * WHERE 'premium' = ANY(tags);
```

### 15. What is the difference between logical and physical replication?

**Answer:**
| Feature | Logical | Physical |
|---------|---------|----------|
| Level | Row-level | Block-level |
| Selectivity | Can replicate specific tables | Whole database |
| Data types | All | Same major version |
| Write target | Can write to replica | Read-only |
| Use case | Reporting, data integration | HA, read scaling |

**Example:**
```sql
-- Logical replication setup
CREATE PUBLICATION my_pub FOR TABLE users, orders;
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=... dbname=...'
  PUBLICATION my_pub;
```

### 16. What is table partitioning?

**Answer:**
Splitting a large table into smaller, manageable pieces while maintaining a single table interface.

**Types:**
- **Range**: By date or numeric range
- **List**: By discrete values
- **Hash**: By hash of partition key

**Example:**
```sql
CREATE TABLE orders (
    id SERIAL,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

### 17. What is the N+1 query problem?

**Answer:**
Executing 1 query for the main list + N queries for each related record.

**Example:**
```typescript
// BAD: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  user.posts = await prisma.post.findMany({
    where: { authorId: user.id }
  });
}

// GOOD: Eager loading
const users = await prisma.user.findMany({
  include: { posts: true }
});
```

### 18. How do you handle schema migrations in production?

**Answer:**
Use migration tools with zero-downtime strategies:

1. **Expand phase**: Add new columns/tables
2. **Migrate phase**: Backfill data
3. **Contract phase**: Remove old columns

**Example:**
```typescript
// Prisma migration
npx prisma migrate dev --name add_user_status

// Zero-downtime strategy
-- 1. Add column with default
ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active';
-- 2. Backfill data
UPDATE users SET status = 'active' WHERE status IS NULL;
-- 3. Remove default
ALTER TABLE users ALTER COLUMN status DROP DEFAULT;
```

### 19. What is connection pooling and why is it needed?

**Answer:**
Connection pooling maintains a cache of database connections for reuse.

**Why needed:**
- Reduces connection overhead (TCP handshake, authentication)
- Limits concurrent connections
- Improves performance

**Example:**
```typescript
// Prisma connection pool
DATABASE_URL="postgresql://...?connection_limit=20&pool_timeout=10"

// PgBouncer
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### 20. What is a materialized view?

**Answer:**
A materialized view stores the result of a query physically. Must be refreshed manually.

**Use cases:**
- Complex aggregations
- Dashboard queries
- Data warehousing

**Example:**
```sql
CREATE MATERIALIZED VIEW sales_dashboard AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    SUM(total) AS revenue
FROM orders
GROUP BY 1;

-- Refresh
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_dashboard;
```

## FAANG-style Questions (5)

### 21. Design a schema for a social media platform.

**Answer:**
```sql
-- Core tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id UUID REFERENCES users(id),
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE follows (
    follower_id UUID REFERENCES users(id),
    following_id UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (follower_id, following_id)
);

CREATE TABLE likes (
    user_id UUID REFERENCES users(id),
    post_id UUID REFERENCES posts(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, post_id)
);

-- Indexes
CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_follows_follower ON follows(follower_id);
CREATE INDEX idx_follows_following ON follows(following_id);
```

### 22. How would you optimize a query on a billion-row table?

**Answer:**
1. **Partitioning**: Split by date or ID range
2. **Materialized views**: Pre-compute aggregations
3. **Proper indexes**: B-tree for range, GIN for JSONB
4. **Query optimization**: Avoid SELECT *, filter early
5. **Read replicas**: Offload read queries

**Example:**
```sql
-- Partition by date
CREATE TABLE events (
    id BIGSERIAL,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Materialized view for dashboards
CREATE MATERIALIZED VIEW daily_stats AS
SELECT
    DATE_TRUNC('day', created_at) AS day,
    COUNT(*) AS event_count
FROM events
GROUP BY 1;

-- BRIN index for naturally ordered data
CREATE INDEX idx_events_created ON events USING BRIN (created_at);
```

### 23. Design a multi-tenant SaaS schema.

**Answer:**
**Option 1: Schema-per-tenant**
```sql
CREATE SCHEMA tenant_1;
CREATE SCHEMA tenant_2;

-- Each schema has its own tables
CREATE TABLE tenant_1.users (...);
CREATE TABLE tenant_2.users (...);
```

**Option 2: Row-level security**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    name TEXT
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.tenant_id')::INTEGER);
```

**Option 3: Database-per-tenant**
- Separate database for each tenant
- Maximum isolation
- Higher operational cost

### 24. Design a real-time leaderboard.

**Answer:**
```sql
-- Option 1: PostgreSQL with window functions
CREATE TABLE scores (
    user_id INTEGER,
    score INTEGER,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_scores_score ON scores(score DESC);

-- Get top 10
SELECT
    user_id,
    score,
    RANK() OVER (ORDER BY score DESC) AS rank
FROM scores
ORDER BY score DESC
LIMIT 10;

-- Option 2: Redis sorted sets (better for real-time)
-- ZADD leaderboard 100 user:123
-- ZREVRANGE leaderboard 0 9 WITHSCORES
```

### 25. Design a distributed transaction system.

**Answer:**
```typescript
// Saga pattern
async function processOrder(orderId: string) {
  // Step 1: Reserve inventory
  await inventoryService.reserve(orderId);

  try {
    // Step 2: Process payment
    await paymentService.charge(orderId);
  } catch (error) {
    // Compensating transaction
    await inventoryService.release(orderId);
    throw error;
  }

  try {
    // Step 3: Ship order
    await shippingService.ship(orderId);
  } catch (error) {
    // Compensating transactions
    await paymentService.refund(orderId);
    await inventoryService.release(orderId);
    throw error;
  }
}
```

## Follow-up Questions (5)

### 26. When would you choose MongoDB over PostgreSQL?

**Answer:**
Choose MongoDB when:
- Schema changes frequently
- Document-heavy workloads
- Rapid prototyping
- Horizontal scaling is critical
- JSON documents are the primary data model

Choose PostgreSQL when:
- ACID compliance is required
- Complex queries and joins
- Data integrity is critical
- SQL expertise is available
- Structured data with relationships

### 27. How do you handle schema changes without downtime?

**Answer:**
1. **Expand-contract pattern**
2. **Feature flags**
3. **Backward-compatible changes**
4. **Dual writes**

**Example:**
```sql
-- 1. Add new column
ALTER TABLE users ADD COLUMN email_normalized TEXT;

-- 2. Backfill data
UPDATE users SET email_normalized = LOWER(email);

-- 3. Add trigger for new inserts
CREATE TRIGGER set_normalized_email
    BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION set_email_normalized();

-- 4. Remove old column (after migration)
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_normalized TO email;
```

### 28. What is the impact of isolation level on performance?

**Answer:**
| Isolation Level | Performance | Use Case |
|----------------|-------------|----------|
| Read Uncommitted | Best | Rarely used |
| Read Committed | Good | Default, most cases |
| Repeatable Read | Moderate | Consistent reads |
| Serializable | Slowest | Financial transactions |

Higher isolation = more locking = more overhead.

### 29. How do you monitor PostgreSQL in production?

**Answer:**
```sql
-- Slow queries
SELECT * FROM pg_stat_activity
WHERE state = 'active'
AND query_start < NOW() - INTERVAL '5 minutes';

-- Index usage
SELECT * FROM pg_stat_user_indexes;

-- Table bloat
SELECT
    relname,
    n_dead_tup,
    n_live_tup
FROM pg_stat_user_tables;

-- Connection count
SELECT COUNT(*) FROM pg_stat_activity;
```

### 30. What is the difference between optimistic and pessimistic locking?

**Answer:**
| Feature | Optimistic | Pessimistic |
|---------|-----------|-------------|
| Assumption | Conflicts rare | Conflicts likely |
| Mechanism | Version column | SELECT FOR UPDATE |
| Concurrency | High | Lower |
| Retry logic | Required | Not needed |
| Use case | Read-heavy | Write-heavy |

## Summary

Master these questions to ace your database interview. Focus on understanding concepts, not just memorizing answers. Practice explaining answers clearly and concisely.

## Cheat Sheet

```text
Key Concepts:
• ACID: Atomicity, Consistency, Isolation, Durability
• MVCC: Multi-Version Concurrency Control
• WAL: Write-Ahead Logging
• Normalization: 1NF → 2NF → 3NF → BCNF
• Index types: B-tree, Hash, GIN, GiST, BRIN

Commands:
• EXPLAIN ANALYZE: Query performance
• VACUUM: Reclaim space
• ANALYZE: Update statistics
• pg_stat_activity: Monitor queries
• pg_stat_user_indexes: Index usage

Best Practices:
• Keep transactions short
• Index foreign keys
• Use parameterized queries
• Monitor slow queries
• Update statistics regularly
```

## References & Learn More

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Database Design for Mere Mortals - Michael Hernandez](https://www.pearson.com/en-us/subject-catalog/p/database-design-for-mere-mortals/P200000003063)
- [SQL Performance Explained - Markus Winand](https://sql-performance-explained.com/)
- [PostgreSQL Indexing Best Practices - Cybertec](https://www.cybertec-postgresql.com/en/postgresql-indexing/)
