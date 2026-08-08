---
section: Database
category: Backend
tags: [concept]
---

# Database Indexes

> **TL;DR:** Indexes turn full table scans into bounded lookups — B-tree for range/equality, hash for equality, GIN for full-text/JSONB, GiST for geospatial. The senior test is knowing composite index column order, partial indexes, covering indexes, and the cost of indexes on writes.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

A database index is a data structure that improves the speed of data retrieval operations at the cost of additional storage and write overhead. Indexes create an ordered reference to rows in a table, allowing the database engine to find data without scanning every row (full table scan).

## Why Do We Need It?

- **Faster Queries**: Reduce lookup time from O(n) to O(log n) or O(1)
- **Enforce Uniqueness**: Unique indexes prevent duplicate values
- **Improve JOIN Performance**: Index foreign keys for faster joins
- **Support Sorting**: Pre-sorted index data avoids expensive sorts
- **Enable Efficient Filtering**: WHERE clauses benefit from indexes

## How It Works

### Index Types Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Index Types                     │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │    B-tree        │  │     Hash        │                  │
│  │  (default)       │  │                 │                  │
│  │  • Equality      │  │  • Equality     │                  │
│  │  • Range          │  │  • O(1) lookup  │                  │
│  │  • Sorting       │  │  • No ordering   │                  │
│  │  • IS NULL       │  │                 │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │     GIN          │  │     GiST        │                  │
│  │  Generalized     │  │  Generalized    │                  │
│  │  Inverted Index  │  │  Search Tree    │                  │
│  │  • Arrays        │  │  • Geometric    │                  │
│  │  • JSONB         │  │  • Full-text    │                  │
│  │  • Full-text     │  │  • Range types  │                  │
│  │  • hstore        │  │                 │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  BRIN            │  │  Partial        │                  │
│  │  Block Range     │  │  Index          │                  │
│  │  • Large tables  │  │  • Conditional  │                  │
│  │  • Correlated    │  │  • Smaller      │                  │
│  │  • Low overhead  │  │  • Faster       │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘

```

### B-tree Structure

```text
                    ┌─────────────┐
                    │   [50]      │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       ┌─────────┐    ┌─────────┐    ┌─────────┐
       │ [20][30]│    │ [55][70]│    │[80][90] │
       └────┬────┘    └────┬────┘    └────┬────┘
            │              │              │
     ┌──────┼──────┐      │        ┌─────┼─────┐
     ▼      ▼      ▼      ▼        ▼     ▼     ▼
   [leaf] [leaf] [leaf] [leaf]   [leaf] [leaf] [leaf]
   1-19  20-49  50-54  55-79   80-89  90+  NULL

Properties:
• Balanced tree (all leaves at same depth)
• Leaves are linked (range scans)
• Each node contains keys + pointers
• O(log n) for lookup, insert, delete

```

## Code Examples

### Creating Indexes

```sql
-- Basic B-tree index (default)
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- DESC index for descending sort
CREATE INDEX idx_orders_created_desc ON orders(created_at DESC);

-- NULLS FIRST/LAST
CREATE INDEX idx_users_name_nulls ON users(name NULLS FIRST);

-- Partial index (only index active users)
CREATE INDEX idx_active_users ON users(email)
WHERE is_active = true;

-- Expression/function-based index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering index (INCLUDE)
CREATE INDEX idx_orders_covering ON orders(user_id, status)
INCLUDE (total, created_at);

-- Hash index (equality only)
CREATE INDEX idx_users_email_hash ON users USING HASH (email);

-- GIN index for JSONB
CREATE INDEX idx_events_metadata ON events USING GIN (metadata);

-- GIN index for arrays
CREATE INDEX idx_products_tags ON products USING GIN (tags);

-- GiST index for full-text search
CREATE INDEX idx_posts_search ON posts USING GIN (to_tsvector('english', content));

-- GiST index for geometric data
CREATE INDEX idx_locations_coords ON locations USING GiST (coordinates);

-- BRIN index for large, naturally ordered tables
CREATE INDEX idx_logs_created ON logs USING BRIN (created_at);

```

### Index-Only Scans

```sql
-- Covering index: includes extra columns in the index
CREATE INDEX idx_orders_covering ON orders(user_id, status)
INCLUDE (total, created_at, shipping_address);

-- Query can be answered entirely from the index
SELECT status, total, created_at
FROM orders
WHERE user_id = 123;

-- Without covering index: must go to heap (table)
-- With covering index: index-only scan (faster)

-- Check if index-only scan is used
EXPLAIN SELECT status, total FROM orders WHERE user_id = 123;
-- Look for "Index Only Scan" in output

```

### EXPLAIN ANALYZE

```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN ANALYZE (actually runs the query)
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 10;

-- EXPLAIN with BUFFERS (shows I/O)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;

-- Understanding the output:
-- Seq Scan: Full table scan (bad for large tables)
-- Index Scan: Using index to find rows
-- Index Only Scan: Data read from index only
-- Nested Loop: Join algorithm
-- Hash Join: Join algorithm
-- Sort: In-memory or disk sort

```

### Index Maintenance

```sql
-- Check index usage statistics
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan AS times_used,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelid NOT IN (
    SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
);

-- Rebuild an index
REINDEX INDEX idx_users_email;
REINDEX TABLE users;

-- Check index bloat
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS size
FROM pg_indexes
WHERE tablename = 'users';

```

## Real-World Use Cases

### E-commerce Query Optimization

```sql
-- Products page with filtering and sorting
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER,
    price DECIMAL(10, 2),
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Indexes for common queries
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = true;
CREATE INDEX idx_products_category_price ON products(category_id, price);
CREATE INDEX idx_products_created ON products(created_at DESC);

-- This query uses the composite index
SELECT * FROM products
WHERE category_id = 5
AND is_active = true
ORDER BY price
LIMIT 20;

-- Search query uses GIN for text search
CREATE INDEX idx_products_name_search ON products
USING GIN (to_tsvector('english', name));

```

### User Authentication

```sql
-- Login query optimization
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMPTZ
);

-- Critical index for login
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Session lookup
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);

```

### Time-series Data

```sql
-- Events table with time-series data
CREATE TABLE events (
    id BIGSERIAL,
    event_type TEXT NOT NULL,
    user_id INTEGER,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- BRIN index for naturally ordered data
CREATE INDEX idx_events_created ON events USING BRIN (created_at);

-- Composite index for common queries
CREATE INDEX idx_events_type_user ON events(event_type, user_id, created_at DESC);

-- Query: Get recent events for a user
SELECT * FROM events
WHERE event_type = 'page_view'
AND user_id = 123
AND created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 100;

```

## Common Mistakes

### 1. Over-Indexing

```sql
-- BAD: Too many indexes
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_address ON users(address);
CREATE INDEX idx_users_city ON users(city);
CREATE INDEX idx_users_state ON users(state);
CREATE INDEX idx_users_zip ON users(zip);
CREATE INDEX idx_users_created ON users(created_at);
-- Each index slows down INSERT/UPDATE/DELETE

-- GOOD: Index only what's queried
CREATE UNIQUE INDEX idx_users_email ON users(email);  -- Login
CREATE INDEX idx_users_name ON users(name);           -- Search

```

### 2. Not Indexing Foreign Keys

```sql
-- BAD: Foreign key without index
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id)  -- No index!
);

-- JOINs and CASCADE deletes are slow
SELECT * FROM orders o JOIN users u ON o.user_id = u.id;

-- GOOD
CREATE INDEX idx_orders_user_id ON orders(user_id);

```

### 3. Wrong Index Type

```sql
-- BAD: Hash index for range queries
CREATE INDEX idx_users_created_hash ON users USING HASH (created_at);
-- Can't do: WHERE created_at > '2024-01-01'

-- GOOD: B-tree for range queries
CREATE INDEX idx_users_created ON users(created_at);

```

### 4. Ignoring Index Selectivity

```sql
-- BAD: Index on low-selectivity column
CREATE INDEX idx_users_gender ON users(gender);
-- Only 2-3 values; index barely helps

-- GOOD: Index on high-selectivity columns
CREATE INDEX idx_users_email ON users(email);  -- Nearly unique

```

## Best Practices

```sql
-- 1. Index columns used in WHERE, JOIN, ORDER BY
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at);

-- 2. Use composite indexes wisely (column order matters)
-- For: WHERE user_id = ? AND status = ?
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- NOT: orders(status, user_id)

-- 3. Use partial indexes for filtered queries
CREATE INDEX idx_active_orders ON orders(user_id)
WHERE status = 'active';

-- 4. Monitor index usage
SELECT * FROM pg_stat_user_indexes
WHERE idx_scan = 0;  -- Unused indexes

-- 5. Use EXPLAIN ANALYZE before creating indexes
EXPLAIN ANALYZE SELECT ...;

-- 6. Consider covering indexes for read-heavy queries
CREATE INDEX idx_covering ON orders(user_id)
INCLUDE (status, total, created_at);

-- 7. Don't index small tables
-- Sequential scan is faster for small tables

-- 8. Rebuild bloated indexes
REINDEX INDEX CONCURRENTLY idx_users_email;

```

## Performance Considerations

```sql
-- Index size impact
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS size
FROM pg_indexes
WHERE tablename = 'orders';

-- Write performance impact
-- Each index adds overhead to INSERT/UPDATE/DELETE
-- Monitor with:
SELECT
    schemaname,
    relname,
    n_tup_ins AS inserts,
    n_tup_upd AS updates,
    n_tup_del AS deletes
FROM pg_stat_user_tables
WHERE relname = 'orders';

-- Index-only scan benefit
-- Without covering index: Index Scan → Heap Fetch
-- With covering index: Index Only Scan (no heap access)

-- Partial index benefit
-- Smaller index = faster scans = less storage
CREATE INDEX idx_active ON users(email) WHERE is_active = true;
-- Only indexes active users (maybe 20% of total)

```

## Summary

Indexes are essential for query performance but come with write overhead. B-tree is the default and most versatile type. Use composite indexes with proper column ordering. Partial and covering indexes optimize specific queries. Always use EXPLAIN ANALYZE to verify index usage. Monitor index health and remove unused indexes.

## Cheat Sheet
```sql
-- Create indexes
CREATE INDEX idx_name ON table(column);
CREATE UNIQUE INDEX idx_name ON table(column);
CREATE INDEX idx_name ON table(col1, col2);  -- Composite
CREATE INDEX idx_name ON table(col) WHERE condition;  -- Partial
CREATE INDEX idx_name ON table USING GIN (jsonb_col);
CREATE INDEX idx_name ON table(col) INCLUDE (extra_col);

-- Monitor
SELECT * FROM pg_stat_user_indexes;
SELECT * FROM pg_stat_user_tables;

-- Maintenance
REINDEX INDEX idx_name;
REINDEX TABLE table_name;
ANALYZE table_name;

-- EXPLAIN
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

```

---

## See Also
- [Performance Monitoring](../26-Performance-Monitoring/)
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [PostgreSQL Indexing Documentation](https://www.postgresql.org/docs/current/indexes.html)
- [Use The Index, Luke - SQL Indexing and Tuning](https://use-the-index-luke.com/)
- [PostgreSQL Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
- [How PostgreSQL Chooses Indexes - Cybertec](https://www.cybertec-postgresql.com/en/postgresql-indexing-choosing-the-right-index/)
- [PostgreSQL Performance Tuning - Percona](https://www.percona.com/blog/)
