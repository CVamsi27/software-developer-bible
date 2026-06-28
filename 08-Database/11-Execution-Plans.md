# Execution Plans

## Definition

An execution plan is PostgreSQL's strategy for executing a SQL query. It shows how the database will retrieve and process data, including which indexes to use, how to join tables, and the estimated cost of each operation. Understanding execution plans is essential for query optimization and performance tuning.

## Why Do We Need It?

- **Query Optimization**: Understand why a query is slow
- **Index Selection**: Verify which indexes are used
- **Cost Estimation**: Compare different query approaches
- **Performance Tuning**: Identify bottlenecks
- **Debugging**: Diagnose query performance issues

## How It Works

### EXPLAIN Output

```text
┌─────────────────────────────────────────────────────────────┐
│                    EXPLAIN Output Structure                   │
│                                                             │
│  Seq Scan on users  (cost=0.00..1234.00 rows=1000 width=56)│
│    Filter: (email = 'test@example.com'::text)              │
│    Rows Removed by Filter: 999                             │
│                                                             │
│  Cost:                                                      │
│  • Start-up cost (0.00): Cost before first row             │
│  • Total cost (1234.00): Estimated total cost               │
│  • Rows (1000): Estimated number of rows                   │
│  • Width (56): Average row width in bytes                   │
│                                                             │
│  Planning Time: 0.123 ms                                   │
│  Execution Time: 12.456 ms                                 │
└─────────────────────────────────────────────────────────────┘
```

### Scan Types

```text
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Scan Types                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Sequential Scan (Seq Scan)                         │   │
│  │  • Reads entire table                               │   │
│  │  • Used when no index is available or beneficial    │   │
│  │  • O(n) complexity                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Index Scan                                         │   │
│  │  • Uses index to find rows                          │   │
│  │  • Then fetches from heap (table)                   │   │
│  │  • O(log n) complexity                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Index Only Scan                                    │   │
│  │  • Data read entirely from index                    │   │
│  │  • No heap access needed                            │   │
│  │  • Fastest scan type                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Bitmap Index Scan                                  │   │
│  │  • Uses multiple indexes                            │   │
│  │  • Creates bitmap of row locations                  │   │
│  │  • Good for multiple OR conditions                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Join Algorithms

```text
┌─────────────────────────────────────────────────────────────┐
│                    Join Algorithms                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Nested Loop                                        │   │
│  │                                                     │   │
│  │  for each row in outer:                             │   │
│  │    for each row in inner:                           │   │
│  │      if match: output row                           │   │
│  │                                                     │   │
│  │  Good for: Small tables, indexed lookups            │   │
│  │  Bad for: Large tables without indexes              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Hash Join                                          │   │
│  │                                                     │   │
│  │  Phase 1: Build hash table on smaller table         │   │
│  │  Phase 2: Probe hash table with larger table        │   │
│  │                                                     │   │
│  │  Good for: Large tables, equi-joins                 │   │
│  │  Bad for: Non-equi joins, memory constraints        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Merge Join                                         │   │
│  │                                                     │   │
│  │  Phase 1: Sort both tables on join key              │   │
│  │  Phase 2: Merge sorted streams                      │   │
│  │                                                     │   │
│  │  Good for: Pre-sorted data, large tables            │   │
│  │  Bad for: Unsorted data (sort overhead)             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic EXPLAIN

```sql
-- Simple EXPLAIN (no execution)
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN ANALYZE (executes query)
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with BUFFERS (shows I/O)
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with all options
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE email = 'test@example.com';
```

### Understanding Output

```sql
-- Sequential Scan example
EXPLAIN ANALYZE SELECT * FROM users;
-- Seq Scan on users  (cost=0.00..1234.00 rows=1000 width=56)
--   (actual time=0.012..12.345 rows=1000 loops=1)
-- Planning Time: 0.089 ms
-- Execution Time: 12.456 ms

-- Index Scan example
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;
-- Index Scan using users_pkey on users  (cost=0.29..8.31 rows=1 width=56)
--   (actual time=0.025..0.026 rows=1 loops=1)
-- Planning Time: 0.123 ms
-- Execution Time: 0.089 ms

-- Hash Join example
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.name;
-- HashAggregate  (cost=1234.00..1235.00 rows=100 width=48)
--   (actual time=12.345..12.346 rows=100 loops=1)
--   ->  Hash Join  (cost=12.34..1234.00 rows=10000 width=52)
--         (actual time=0.123..12.234 rows=10000 loops=1)
--           ->  Seq Scan on users u  (cost=0.00..1234.00 rows=1000 width=44)
--                 (actual time=0.012..12.123 rows=1000 loops=1)
--           ->  Hash  (cost=12.34..12.34 rows=1000 width=12)
--                 (actual time=0.089..0.090 rows=1000 loops=1)
-- Planning Time: 0.156 ms
-- Execution Time: 12.567 ms
```

### Index Usage Analysis

```sql
-- Check if index is used
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';
-- Look for "Index Scan" or "Index Only Scan"

-- Check index usage statistics
SELECT
    schemaname,
    relname,
    indexrelname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'users';

-- Find missing indexes
SELECT
    relname,
    seq_scan,
    seq_tup_read,
    idx_scan,
    CASE WHEN seq_scan > 0
         THEN ROUND(seq_tup_read::float / seq_scan, 2)
         ELSE 0
    END AS avg_rows_per_seq_scan
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_tup_read DESC;
```

### Query Optimization Examples

```sql
-- BAD: Sequential scan on large table
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;
-- Seq Scan on orders  (cost=0.00..123456.00 rows=100 width=100)
--   (actual time=0.012..1234.567 rows=100 loops=1)

-- GOOD: Add index
CREATE INDEX idx_orders_user_id ON orders(user_id);
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;
-- Index Scan using idx_orders_user_id on orders  (cost=0.43..12.34 rows=100 width=100)
--   (actual time=0.025..0.123 rows=100 loops=1)

-- BAD: Function prevents index usage
EXPLAIN ANALYZE
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
-- Seq Scan on users  (cost=0.00..1234.00 rows=1000 width=56)

-- GOOD: Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
EXPLAIN ANALYZE
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';
-- Index Scan using idx_users_lower_email on users  (cost=0.43..8.31 rows=1 width=56)
```

## Real-World Use Cases

### Slow Query Analysis

```sql
-- Find slow queries
SELECT
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- Analyze slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT
    u.name,
    COUNT(o.id) AS order_count,
    SUM(o.total) AS total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2024-01-01'
GROUP BY u.name
HAVING COUNT(o.id) > 10
ORDER BY total_spent DESC
LIMIT 20;
```

### Index Optimization

```sql
-- Before: Sequential scan
EXPLAIN ANALYZE
SELECT * FROM products
WHERE category_id = 5
AND price < 100
AND is_active = true;
-- Seq Scan on products  (cost=0.00..1234.00 rows=50 width=100)
--   Filter: (category_id = 5 AND price < 100 AND is_active)

-- After: Composite index
CREATE INDEX idx_products_category_price_active
ON products(category_id, price)
WHERE is_active = true;

EXPLAIN ANALYZE
SELECT * FROM products
WHERE category_id = 5
AND price < 100
AND is_active = true;
-- Index Scan using idx_products_category_price_active on products
--   (cost=0.43..12.34 rows=50 width=100)
```

### Join Optimization

```sql
-- Before: Hash Join (memory intensive)
EXPLAIN ANALYZE
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;
-- Hash Join  (cost=12.34..1234.00 rows=10000 width=52)

-- After: Add index on join column
CREATE INDEX idx_orders_user_id ON orders(user_id);

EXPLAIN ANALYZE
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id;
-- Nested Loop  (cost=0.43..12.34 rows=10000 width=52)
--   ->  Index Scan using idx_orders_user_id on orders o
--   ->  Index Scan using users_pkey on users u
```

## Common Mistakes

### 1. Not Using EXPLAIN ANALYZE

```sql
-- BAD: Guessing why a query is slow
SELECT * FROM orders WHERE user_id = 123;

-- GOOD: Understanding the execution plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

### 2. Ignoring Cost Estimates

```sql
-- BAD: Only looking at actual time
EXPLAIN ANALYZE SELECT * FROM users;
-- Focuses on execution time, ignores cost

-- GOOD: Understanding cost estimates
EXPLAIN SELECT * FROM users;
-- Look at cost=0.00..1234.00
-- Lower cost = better plan
```

### 3. Not Checking Buffers

```sql
-- BAD: Only looking at time
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;

-- GOOD: Check I/O with BUFFERS
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;
-- Look for "Buffers: shared hit=123 read=45"
-- High read = disk I/O = slow
```

## Best Practices

```sql
-- 1. Always use EXPLAIN ANALYZE for slow queries
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...;

-- 2. Compare different query plans
-- Try different approaches and compare costs

-- 3. Check index usage
SELECT * FROM pg_stat_user_indexes WHERE relname = 'table_name';

-- 4. Monitor sequential scans
SELECT * FROM pg_stat_user_tables WHERE seq_scan > 100;

-- 5. Update statistics regularly
ANALYZE table_name;

-- 6. Use EXPLAIN before and after adding indexes
-- Verify index is actually used

-- 7. Check for sequential scans on large tables
EXPLAIN SELECT * FROM large_table WHERE ...;
-- Look for "Seq Scan" - consider adding index
```

## Performance Considerations

```sql
-- Cost model explanation
-- Cost = (CPU cost × rows) + (disk cost × pages)

-- Sequential scan cost
-- Cost = (cpu_tuple_cost × rows) + (seq_page_cost × pages)

-- Index scan cost
-- Cost = (cpu_tuple_cost × rows) + (random_page_cost × pages) + index_cost

-- Guidelines
-- Lower cost = better plan
-- Compare plans: which approach has lower total cost?
-- Consider: actual time vs estimated time

-- Statistics impact
-- Outdated statistics = wrong cost estimates = bad plans
ANALYZE table_name;

-- Memory impact
-- work_mem affects hash join and sort operations
SET work_mem = '256MB';  -- Increase for complex queries
```

## Interview Questions

### Beginner (5)

1. **What is EXPLAIN?**
   Shows PostgreSQL's execution plan for a query.

2. **What is the difference between EXPLAIN and EXPLAIN ANALYZE?**
   EXPLAIN: shows plan only; EXPLAIN ANALYZE: executes and shows actual results.

3. **What is a sequential scan?**
   Reading entire table; used when no index is beneficial.

4. **What is an index scan?**
   Using index to find rows; faster than sequential scan.

5. **What does "cost" mean in EXPLAIN output?**
   Estimated cost of operation; lower is better.

### Intermediate (5)

6. **What is the difference between Index Scan and Index Only Scan?**
   Index Scan: uses index then heap; Index Only Scan: data from index only.

7. **What is a Hash Join?**
   Builds hash table on smaller table, probes with larger table.

8. **What is the difference between Nested Loop and Hash Join?**
   Nested Loop: O(n*m); Hash Join: O(n+m).

9. **What is "Buffers" in EXPLAIN output?**
   Shows I/O operations; shared hit = memory, shared read = disk.

10. **What is the difference between cost and actual time?**
    Cost: estimated; Actual: measured during execution.

### Senior (10)

11. **How does PostgreSQL choose between join algorithms?**
    Based on table sizes, statistics, available indexes, memory.

12. **What is the impact of statistics on execution plans?**
    Outdated statistics = wrong cost estimates = bad plans.

13. **What is the difference between cost and actual time?**
    Cost: model-based estimate; Actual: measured during execution.

14. **How do you optimize a query with multiple OR conditions?**
    Use Bitmap Index Scan; consider UNION ALL.

15. **What is the difference between Seq Scan and Index Scan?**
    Seq Scan: reads entire table; Index Scan: uses index for lookup.

16. **How do you handle parallel query execution?**
    PostgreSQL can parallelize Seq Scan, Hash Join, etc.

17. **What is the impact of work_mem on query performance?**
    Affects hash join and sort operations; increase for complex queries.

18. **How do you debug a slow query?**
    EXPLAIN ANALYZE, check buffers, verify indexes, update statistics.

19. **What is the difference between planning and execution time?**
    Planning: generating plan; Execution: running query.

20. **How do you compare different query approaches?**
    Run EXPLAIN ANALYZE for each; compare cost and actual time.

### FAANG-style (5)

21. **How would you optimize a query on a billion-row table?**
    Partitioning, materialized views, approximate queries, proper indexes.

22. **Design a query performance monitoring system.**
    pg_stat_statements, pgBadger, custom dashboards.

23. **How do you handle query optimization in a distributed database?**
    Distributed query planning, data locality, partition pruning.

24. **Design a system for automatic index recommendation.**
    Query analysis, workload capture, index suggestion engine.

25. **How do you optimize for both reads and writes?**
    Read replicas, write-optimized indexes, materialized views.

### Follow-ups (5)

26. **What is the difference between EXPLAIN and EXPLAIN ANALYZE?**
    EXPLAIN: estimated plan; EXPLAIN ANALYZE: actual execution with timing.

27. **How do you handle parallel execution in EXPLAIN?**
    Look for "Parallel" in output; workers = number of parallel processes.

28. **What is the difference between planning and execution time?**
    Planning: generating plan; Execution: running query.

29. **How do you optimize a query with many JOINs?**
    Join order, indexes on join columns, filter early.

30. **What is the impact of data distribution on execution plans?**
    Skewed data can cause bad plans; ANALYZE helps statistics.

## Summary

EXPLAIN ANALYZE is essential for query optimization. Understand scan types (Seq Scan, Index Scan, Index Only Scan), join algorithms (Nested Loop, Hash Join, Merge Join), and cost estimates. Always check buffers for I/O impact. Update statistics regularly and verify index usage.

## Cheat Sheet

```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM users WHERE id = 1;

-- With actual execution
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;

-- With I/O information
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE id = 1;

-- All options
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT * FROM users WHERE id = 1;

-- Check index usage
SELECT * FROM pg_stat_user_indexes WHERE relname = 'users';

-- Update statistics
ANALYZE users;
```

## References & Learn More

- [PostgreSQL EXPLAIN Documentation](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL Performance Analysis - Explain Plans](https://www.postgresql.org/docs/current/using-explain.html)
- [Understanding PostgreSQL Execution Plans - Cybertec](https://www.cybertec-postgresql.com/en/postgresql-execution-plans/)
- [EXPLAIN ANALYZE - PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Using_EXPLAIN)
- [Query Performance Tuning - Percona](https://www.percona.com/blog/)
