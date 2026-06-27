# PostgreSQL

## Definition

PostgreSQL is a powerful, open-source, object-relational database management system (ORDBMS) with over 30 years of active development. It extends SQL with features like custom data types, functions, operators, and index methods. PostgreSQL is ACID-compliant, supports MVCC (Multi-Version Concurrency Control), and is known for its reliability, feature robustness, and performance.

## Why Do We Need It?

- **ACID Compliance**: Ensures data integrity even during failures
- **MVCC**: Allows concurrent reads without blocking writes
- **Extensibility**: Custom types, functions, operators, and extensions
- **Standards Compliance**: Most SQL-standard compliant database
- **JSONB Support**: First-class NoSQL capabilities within a relational database
- **Replication**: Built-in streaming and logical replication
- **Community**: Active open-source community with regular releases

## How It Works

### Architecture

PostgreSQL uses a client-server model with multiple processes:

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                    │
│              (Node.js, Python, Go, etc.)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │ TCP/IP Connection
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Postmaster Process                        │
│                   (Main Daemon)                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Forks     │  │  Authentication│  │  Connection     │   │
│  │  Backend    │  │    (md5/scram)│  │   Pooling       │   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │ Fork
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend Process (per connection)           │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Parser    │  │  Optimizer   │  │   Executor      │   │
│  │  (SQL→Tree) │  │  (Tree→Plan) │  │  (Plan→Rows)   │   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared Memory                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Shared Buffers│ │  WAL Buffers │  │  Lock Table     │   │
│  └─────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Background Workers                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  WAL     │  │  Check-  │  │  Autovacuum│ │  BG      │  │
│  │  Writer  │  │  pointer │  │  Launcher │  │  Writer  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Process Memory                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              work_mem (per operation)                │   │
│  │    (Sorting, Hashing, Index building)               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          maintenance_work_mem                       │   │
│  │    (VACUUM, CREATE INDEX, ALTER TABLE)              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared Memory                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          shared_buffers (default: 128MB)            │   │
│  │    (Cache for table and index data)                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          WAL buffers (default: 16MB)                │   │
│  │    (Write-Ahead Log cache)                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Lock table                                  │   │
│  │    (Track all locks)                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Write-Ahead Logging (WAL)

```
┌─────────────────────────────────────────────────────────────┐
│                    WAL Process Flow                          │
│                                                             │
│  Transaction Start                                          │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                            │
│  │ Write Change │──► WAL Buffer (in-memory)                │
│  │  to WAL Log  │                                           │
│  └─────────────┘                                            │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐    fsync                                   │
│  │ WAL Segment │──► Disk (WAL files in pg_wal/)            │
│  │   (16MB)    │                                            │
│  └─────────────┘                                            │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────┐                                            │
│  │  Checkpoint │──► Write dirty pages to data files         │
│  └─────────────┘                                            │
│                                                             │
│  Recovery: Replay WAL from last checkpoint                   │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Data Types

```sql
-- Core data types
CREATE TABLE data_types_demo (
    -- Numeric
    id SERIAL PRIMARY KEY,
    small_num SMALLINT,
    regular_num INTEGER,
    big_num BIGINT,
    decimal_num DECIMAL(10, 2),
    real_num REAL,
    double_num DOUBLE PRECISION,

    -- String
    name VARCHAR(255),
    fixed CHAR(10),
    unlimited TEXT,

    -- Date/Time
    created_at TIMESTAMP WITH TIME ZONE,
    date_only DATE,
    time_only TIME,
    interval INTERVAL,

    -- Boolean
    is_active BOOLEAN DEFAULT true,

    -- Binary
    file_data BYTEA,

    -- UUID
    uuid_col UUID DEFAULT gen_random_uuid()
);
```

### JSONB Operations

```sql
-- Creating a table with JSONB
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Inserting JSONB data
INSERT INTO events (metadata) VALUES
('{
    "type": "user_signup",
    "source": "web",
    "properties": {
        "user_id": 123,
        "plan": "premium",
        "referrer": "google.com"
    },
    "tags": ["marketing", "acquisition"]
}');

-- Querying JSONB
SELECT
    metadata->>'type' AS event_type,
    metadata->'properties'->>'user_id' AS user_id,
    metadata->'tags'->0 AS first_tag
FROM events
WHERE metadata->>'type' = 'user_signup';

-- JSONB indexing
CREATE INDEX idx_events_metadata ON events USING GIN (metadata);
CREATE INDEX idx_events_type ON events ((metadata->>'type'));

-- JSONB aggregation
SELECT
    metadata->>'type' AS event_type,
    COUNT(*) AS event_count
FROM events
GROUP BY metadata->>'type';

-- Updating JSONB
UPDATE events
SET metadata = jsonb_set(
    metadata,
    '{properties,plan}',
    '"enterprise"'
)
WHERE id = 1;
```

### Array Types

```sql
-- Arrays in PostgreSQL
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    tags TEXT[],
    scores INTEGER[] DEFAULT '{}'
);

-- Insert with arrays
INSERT INTO products (name, tags, scores)
VALUES (
    'Laptop',
    ARRAY['electronics', 'computers', 'portable'],
    ARRAY[85, 90, 78]
);

-- Array operations
SELECT name FROM products WHERE 'electronics' = ANY(tags);
SELECT name FROM products WHERE tags @> ARRAY['computers'];
SELECT name FROM products WHERE array_length(tags, 1) > 2;

-- Unnesting arrays
SELECT name, unnest(tags) AS tag FROM products;

-- Array aggregation
SELECT
    array_agg(DISTINCT tag) AS all_tags
FROM products, unnest(tags) AS tag;
```

### Common Table Expressions (CTEs)

```sql
-- Recursive CTE for hierarchical data
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT
        id,
        name,
        manager_id,
        1 AS level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees with managers
    SELECT
        e.id,
        e.name,
        e.manager_id,
        oc.level + 1,
        oc.path || ' → ' || e.name
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;

-- CTE for complex aggregation
WITH monthly_sales AS (
    SELECT
        date_trunc('month', created_at) AS month,
        product_id,
        SUM(amount) AS total_sales
    FROM orders
    GROUP BY 1, 2
),
ranked_products AS (
    SELECT
        month,
        product_id,
        total_sales,
        RANK() OVER (PARTITION BY month ORDER BY total_sales DESC) AS rank
    FROM monthly_sales
)
SELECT * FROM ranked_products WHERE rank <= 5;
```

### Window Functions

```sql
-- Window functions for analytics
SELECT
    department,
    employee_name,
    salary,
    -- Row number within department
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS dept_rank,
    -- Running total
    SUM(salary) OVER (
        PARTITION BY department
        ORDER BY salary DESC
        ROWS UNBOUNDED PRECEDING
    ) AS running_total,
    -- Percentage of department total
    ROUND(
        salary * 100.0 / SUM(salary) OVER (PARTITION BY department),
        2
    ) AS pct_of_dept,
    -- Lag/Lead for comparison
    LAG(salary) OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS prev_salary,
    LEAD(salary) OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS next_salary
FROM employees;
```

### Prisma Schema for PostgreSQL

```prisma
// schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch", "postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [uuid_ossp, pgcrypto]
}

model User {
  id        String   @id @default(uuid()) @db.Uuid
  email     String   @unique
  name      String?
  posts     Post[]
  metadata  Json?    @default("{}")
  tags      String[] @default([])
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
}

model Post {
  id        String   @id @default(uuid()) @db.Uuid
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String   @map("author_id") @db.Uuid
  tags      String[] @default([])
  metadata  Json?    @default("{}")

  @@index([authorId])
  @@index([published, createdAt])
  @@map("posts")
}
```

## Real-World Use Cases

### E-commerce Product Catalog

```sql
-- Flexible product attributes using JSONB
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    attributes JSONB NOT NULL DEFAULT '{}',
    search_vector TSVECTOR,

    -- GIN index for full-text search on attributes
    CONSTRAINT valid_attributes CHECK (jsonb_typeof(attributes) = 'object')
);

CREATE INDEX idx_products_attrs ON products USING GIN (attributes);
CREATE INDEX idx_products_search ON products USING GIN (search_vector);

-- Auto-update search vector
CREATE OR REPLACE FUNCTION update_product_search()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.attributes->>'description', '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_product_search
    BEFORE INSERT OR UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_product_search();
```

### Real-time Analytics with Window Functions

```sql
-- Daily active users with rolling 7-day average
WITH daily_active AS (
    SELECT
        DATE_TRUNC('day', created_at) AS day,
        COUNT(DISTINCT user_id) AS active_users
    FROM user_sessions
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY 1
)
SELECT
    day,
    active_users,
    AVG(active_users) OVER (
        ORDER BY day
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg,
    active_users - LAG(active_users, 7) OVER (ORDER BY day) AS week_over_week
FROM daily_active
ORDER BY day;
```

## Common Mistakes

### 1. Not Using EXPLAIN ANALYZE

```sql
-- Bad: Guessing why a query is slow
SELECT * FROM orders WHERE user_id = 123;

-- Good: Understanding the execution plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

### 2. Over-normalizing When Denormalization is Better

```sql
-- Bad: Too many JOINs for a read-heavy dashboard
SELECT o.id, u.name, p.name, c.name, s.status
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN statuses s ON o.status_id = s.id;

-- Better: Materialized view for dashboard
CREATE MATERIALIZED VIEW dashboard_orders AS
SELECT
    o.id,
    u.name AS user_name,
    p.name AS product_name,
    c.name AS category_name,
    s.status
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN products p ON o.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN statuses s ON o.status_id = s.id;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_orders;
```

### 3. Ignoring Connection Pooling

```typescript
// Bad: Creating new connections for each query
import { Pool } from 'pg';

async function getUser(id: number) {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  await pool.end(); // Don't do this!
  return result.rows[0];
}

// Good: Reusing a connection pool
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
});

async function getUser(id: number) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}
```

## Best Practices

```sql
-- 1. Always use parameterized queries (prevent SQL injection)
-- Bad
SELECT * FROM users WHERE email = '' OR 1=1--;

-- Good
SELECT * FROM users WHERE email = $1;

-- 2. Use appropriate data types
-- Bad: Storing dates as strings
CREATE TABLE events (
    event_date TEXT  -- '2024-01-15' - can't do date arithmetic
);

-- Good
CREATE TABLE events (
    event_date DATE  -- Can do: event_date + INTERVAL '7 days'
);

-- 3. Add meaningful constraints
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    total DECIMAL(10, 2) CHECK (total >= 0),
    status VARCHAR(20) CHECK (status IN ('pending', 'shipped', 'delivered')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Use EXPLAIN ANALYZE regularly
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM large_table WHERE some_column = 'value';

-- 5. Create indexes for frequently queried columns
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status != 'cancelled';
```

## Performance Considerations

```sql
-- 1. Batch inserts instead of single inserts
-- Bad
INSERT INTO logs (message) VALUES ('log1');
INSERT INTO logs (message) VALUES ('log2');
-- ... repeat 10000 times

-- Good: Bulk insert
INSERT INTO logs (message)
SELECT 'log' || generate_series(1, 10000);

-- 2. Use COPY for large data loads
COPY users FROM '/path/to/users.csv' WITH (FORMAT csv, HEADER true);

-- 3. Partition large tables
CREATE TABLE orders (
    id SERIAL,
    created_at TIMESTAMPTZ NOT NULL,
    total DECIMAL(10, 2)
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- 4. Monitor slow queries
SELECT
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';
```

## Interview Questions

### Beginner (5)

1. **What is PostgreSQL?**
   Open-source, ACID-compliant, object-relational database with extensibility.

2. **What is the difference between SQL and PostgreSQL?**
   SQL is a language; PostgreSQL is a database that implements SQL with extensions.

3. **What are the main data types?**
   INTEGER, TEXT, VARCHAR, BOOLEAN, TIMESTAMP, JSONB, UUID, arrays.

4. **What is a primary key?**
   A column (or set) that uniquely identifies each row; cannot be NULL.

5. **What is an index?**
   A data structure that improves query speed by allowing fast lookups.

### Intermediate (5)

6. **What is JSONB and why use it?**
   Binary JSON format with indexing support; flexible schema within relational DB.

7. **What are CTEs?**
   Common Table Expressions; temporary named result sets for complex queries.

8. **What is a materialized view?**
   A view stored as a physical table; must be refreshed manually.

9. **What is the difference between WHERE and HAVING?**
   WHERE filters rows before GROUP BY; HAVING filters groups after.

10. **What are window functions?**
    Functions that perform calculations across related rows without collapsing them.

### Senior (10)

11. **Explain PostgreSQL's MVCC implementation.**
    Uses tuple versioning (xmin/xmax); old versions kept until VACUUM.

12. **What is WAL and why is it important?**
    Write-Ahead Logging; ensures durability and enables point-in-time recovery.

13. **How does PostgreSQL handle concurrent updates?**
    MVCC with serialization; last commit wins or serialization error.

14. **What is a GIN index?**
    Generalized Inverted Index; for arrays, JSONB, full-text search.

15. **Explain connection pooling and why it's needed.**
    Reuses connections to avoid fork overhead; PgBouncer, PgPool-II.

16. **What is table partitioning?**
    Splitting large tables into smaller pieces; range, list, or hash.

17. **What is logical replication vs physical replication?**
    Logical: row-level, selective; Physical: block-level, exact copies.

18. **How do you handle schema migrations in production?**
    Use tools like Prisma Migrate, Flyway, or Alembic with zero-downtime strategies.

19. **What is the N+1 query problem and how do you solve it?**
    Multiple individual queries instead of one; solve with JOINs or eager loading.

20. **Explain query optimization techniques.**
    EXPLAIN ANALYZE, proper indexes, avoiding SELECT *, parameterized queries.

### FAANG-style (5)

21. **Design a schema for a social media feed with billions of posts.**
    Partitioning by user_id, denormalized feed table, Redis cache.

22. **How would you implement a real-time leaderboard?**
    Sorted sets in Redis, or PostgreSQL with window functions + materialized view.

23. **Explain CAP theorem in context of PostgreSQL replication.**
    PostgreSQL is CP; favors consistency over availability during network partitions.

24. **Design a multi-tenant SaaS database architecture.**
    Schema-per-tenant, row-level security, or database-per-tenant.

25. **How do you handle schema changes without downtime?**
    Expand-contract pattern, feature flags, backward-compatible migrations.

### Follow-ups (5)

26. **When would you choose MongoDB over PostgreSQL?**
    Flexible schemas, document-heavy workloads, rapid prototyping.

27. **How does PostgreSQL handle full-text search?**
    tsvector, tsquery, GIN indexes; can replace Elasticsearch for simple cases.

28. **What is the performance impact of JSONB vs structured columns?**
    JSONB has slight overhead; structured columns are faster for known queries.

29. **How do you monitor PostgreSQL in production?**
    pg_stat_statements, pgBadger, Prometheus + Grafana, pg_stat_activity.

30. **What are advisory locks in PostgreSQL?**
    Application-level locks; useful for distributed locking without table rows.

## Summary

PostgreSQL is the most feature-rich open-source relational database. Its key strengths include MVCC for concurrency, JSONB for flexibility, extensibility, and standards compliance. Understanding its architecture (process model, shared memory, WAL) is essential for performance tuning and debugging. Use appropriate indexes, connection pooling, and query optimization for production workloads.

## Cheat Sheet

```bash
# Connection
psql -h localhost -p 5432 -U username -d database

# Useful commands
\dt          # List tables
\d table     # Describe table
\di          # List indexes
\du          # List users
\l           # List databases

# Performance
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

# Backup
pg_dump -h host -U user dbname > backup.sql
pg_restore -h host -U user dbname backup.dump

# Config
SHOW shared_buffers;
SHOW work_mem;
SHOW max_connections;
```

## References & Learn More

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [PostgreSQL Wiki](https://wiki.postgresql.org/)
- [Use The Index, Luke - SQL Indexing and Tuning](https://use-the-index-luke.com/)
- [PgBouncer - PostgreSQL Connection Pooler](https://www.pgbouncer.org/)
- [PostgreSQL Performance Optimization](https://www.postgresql.org/docs/current/performance-tips.html)
