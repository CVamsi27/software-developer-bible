# Database Joins

## Definition

A JOIN is a SQL operation that combines rows from two or more tables based on a related column between them. Joins allow you to query data from multiple tables in a single result set, enabling relationships between entities to be traversed efficiently.

## Why Do We Need It?

- **Combine Related Data**: Query data from multiple tables in one result
- **Maintain Normalization**: Store data once, reference via foreign keys
- **Avoid Data Duplication**: Don't duplicate data across tables
- **Complex Queries**: Enable sophisticated data retrieval patterns
- **Performance**: Efficiently combine data without application-level loops

## How It Works

### Join Types Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    SQL Join Types                            │
│                                                             │
│  Table A          Table B                                   │
│  ┌─────┐         ┌─────┐                                   │
│  │  1  │         │  a  │                                   │
│  │  2  │         │  b  │                                   │
│  │  3  │         │  c  │                                   │
│  └─────┘         └─────┘                                   │
│                                                             │
│  INNER JOIN: Only matching rows                             │
│  ┌─────────────┐                                           │
│  │ A.id = B.id │                                           │
│  │   1 = a     │                                           │
│  │   2 = b     │                                           │
│  └─────────────┘                                           │
│                                                             │
│  LEFT JOIN: All from A + matching from B                    │
│  ┌──────────────────────────────┐                          │
│  │ 1=a, 2=b, 3=NULL            │                          │
│  └──────────────────────────────┘                          │
│                                                             │
│  RIGHT JOIN: All from B + matching from A                   │
│  ┌──────────────────────────────┐                          │
│  │ 1=a, 2=b, NULL=c            │                          │
│  └──────────────────────────────┘                          │
│                                                             │
│  FULL JOIN: All from both                                   │
│  ┌──────────────────────────────┐                          │
│  │ 1=a, 2=b, 3=NULL, NULL=c    │                          │
│  └──────────────────────────────┘                          │
│                                                             │
│  CROSS JOIN: All combinations                               │
│  ┌──────────────────────────────┐                          │
│  │ 1=a, 1=b, 1=c, 2=a, 2=b...  │                          │
│  └──────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### Join Algorithms

```text
┌─────────────────────────────────────────────────────────────┐
│                    Join Algorithms                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Nested Loop Join                                    │   │
│  │  For each row in A, scan B for matches               │   │
│  │  Good for: Small tables, indexed lookups              │   │
│  │  Complexity: O(n * m)                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Hash Join                                           │   │
│  │  Build hash table on smaller table, probe with larger│   │
│  │  Good for: Equi-joins, large unsorted tables         │   │
│  │  Complexity: O(n + m)                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Merge Join                                          │   │
│  │  Sort both tables, merge sorted streams              │   │
│  │  Good for: Pre-sorted data, large tables             │   │
│  │  Complexity: O(n + m) with sort overhead             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### INNER JOIN

```sql
-- Basic INNER JOIN
SELECT
    u.id,
    u.name,
    o.id AS order_id,
    o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- With conditions
SELECT
    u.name,
    o.total,
    o.created_at
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2024-01-01'
AND o.total > 100;

-- Multiple JOINs
SELECT
    u.name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id;
```

### LEFT JOIN

```sql
-- All users, including those without orders
SELECT
    u.name,
    COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Find users without orders
SELECT
    u.name,
    u.email
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;

-- Latest order for each user
SELECT
    u.name,
    o.id AS latest_order_id,
    o.created_at
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
AND o.created_at = (
    SELECT MAX(created_at)
    FROM orders
    WHERE user_id = u.id
);
```

### RIGHT JOIN

```sql
-- All products, including those never ordered
SELECT
    p.name,
    COUNT(oi.order_id) AS times_ordered
FROM order_items oi
RIGHT JOIN products p ON oi.product_id = p.id
GROUP BY p.id, p.name;

-- Equivalent with LEFT JOIN (more common)
SELECT
    p.name,
    COUNT(oi.order_id) AS times_ordered
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name;
```

### FULL JOIN

```sql
-- All users and all orders, matching where possible
SELECT
    u.name,
    o.id AS order_id,
    o.total
FROM users u
FULL JOIN orders o ON u.id = o.user_id;

-- Find unmatched records on both sides
SELECT
    u.name,
    o.id AS order_id
FROM users u
FULL JOIN orders o ON u.id = o.user_id
WHERE u.id IS NULL OR o.id IS NULL;
```

### CROSS JOIN

```sql
-- Cartesian product (all combinations)
SELECT
    s.name AS size,
    c.name AS color
FROM sizes s
CROSS JOIN colors c;

-- Generate date series
SELECT
    d.date,
    h.hour
FROM generate_series('2024-01-01'::date, '2024-01-31'::date, '1 day') AS d(date)
CROSS JOIN generate_series(0, 23) AS h(hour);

-- Product variants
SELECT
    p.name,
    s.size,
    c.color
FROM products p
CROSS JOIN sizes s
CROSS JOIN colors c;
```

### LATERAL JOIN

```sql
-- LATERAL allows subquery to reference preceding columns
-- Get top 3 orders per user
SELECT
    u.name,
    top_orders.*
FROM users u
CROSS JOIN LATERAL (
    SELECT
        o.id,
        o.total,
        o.created_at
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY o.created_at DESC
    LIMIT 3
) AS top_orders;

-- Get nearest locations for each user
SELECT
    u.name,
    nearest.*
FROM users u
CROSS JOIN LATERAL (
    SELECT
        l.name AS location_name,
        l.coordinates <-> u.coordinates AS distance
    FROM locations l
    ORDER BY u.coordinates <-> l.coordinates
    LIMIT 5
) AS nearest;
```

### Self Join

```sql
-- Find employees and their managers
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Find pairs of employees in same department
SELECT
    e1.name AS employee1,
    e2.name AS employee2,
    e1.department
FROM employees e1
INNER JOIN employees e2
    ON e1.department = e2.department
    AND e1.id < e2.id;
```

### Subqueries vs Joins

```sql
-- Subquery approach
SELECT *
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
    WHERE total > 100
);

-- Join approach (often faster)
SELECT DISTINCT u.*
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;

-- Correlated subquery
SELECT
    u.name,
    (SELECT COUNT(*) FROM orders WHERE user_id = u.id) AS order_count
FROM users u;

-- Join approach
SELECT
    u.name,
    COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

## Real-World Use Cases

### E-commerce Dashboard

```sql
-- Sales dashboard with multiple joins
SELECT
    DATE_TRUNC('day', o.created_at) AS sale_date,
    c.name AS category,
    p.name AS product,
    u.name AS customer,
    oi.quantity,
    oi.unit_price,
    o.total AS order_total
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
INNER JOIN categories c ON p.category_id = c.id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY o.created_at DESC;
```

### User Activity Report

```sql
-- User activity with latest action
SELECT
    u.name,
    u.email,
    la.action,
    la.created_at AS last_action
FROM users u
LEFT JOIN LATERAL (
    SELECT action, created_at
    FROM user_actions
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) la ON true
WHERE u.is_active = true;
```

### Inventory Check

```sql
-- Products with stock and sales data
SELECT
    p.name,
    p.stock AS current_stock,
    COALESCE(SUM(oi.quantity), 0) AS total_sold,
    p.stock - COALESCE(SUM(oi.quantity), 0) AS remaining
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id
AND o.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.id, p.name, p.stock;
```

## Common Mistakes

### 1. Missing Join Conditions (Cartesian Product)

```sql
-- BAD: Missing ON clause
SELECT u.name, o.total
FROM users u, orders o;
-- Returns every combination (n * m rows)

-- GOOD: Explicit join condition
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### 2. Using WHERE Instead of ON

```sql
-- BAD: Filter in WHERE (may lose rows in LEFT JOIN)
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.user_id IS NOT NULL;  -- Converts LEFT JOIN to INNER JOIN

-- GOOD: Filter in ON for LEFT JOIN
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
AND o.created_at > '2024-01-01';  -- Preserves LEFT JOIN
```

### 3. Not Using Table Aliases

```sql
-- BAD: Ambiguous column names
SELECT id, name, total
FROM users
JOIN orders ON users.id = orders.user_id;

-- GOOD: Clear aliases
SELECT u.id, u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

## Best Practices

```sql
-- 1. Always specify join type explicitly
-- BAD
SELECT * FROM users, orders WHERE users.id = orders.user_id;

-- GOOD
SELECT * FROM users u INNER JOIN orders o ON u.id = o.user_id;

-- 2. Use table aliases for readability
SELECT
    u.name,
    o.total,
    p.name AS product
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id;

-- 3. Index join columns
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- 4. Use EXPLAIN ANALYZE to check join performance
EXPLAIN ANALYZE
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 5. Prefer INNER JOIN over WHERE with comma joins
-- BAD
SELECT * FROM users u, orders o WHERE u.id = o.user_id;

-- GOOD
SELECT * FROM users u INNER JOIN orders o ON u.id = o.user_id;
```

## Performance Considerations

```sql
-- Join order matters for performance
-- PostgreSQL optimizer usually picks good order
-- But you can influence with hints (not recommended)

-- Check join algorithm used
EXPLAIN ANALYZE
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Look for:
-- Nested Loop: Good for small, indexed joins
-- Hash Join: Good for large, unsorted joins
-- Merge Join: Good for pre-sorted data

-- Filter early to reduce join size
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2024-01-01'  -- Filter before join
AND u.is_active = true;

-- Use covering indexes
CREATE INDEX idx_orders_covering ON orders(user_id)
INCLUDE (total, created_at);
```

## Interview Questions

### Beginner (5)

1. **What is a JOIN?**
   Combines rows from two or more tables based on related columns.

2. **What is the difference between INNER JOIN and LEFT JOIN?**
   INNER: only matching rows; LEFT: all from left table + matching from right.

3. **What is a Cartesian product?**
   Every combination of rows from two tables; happens with missing join condition.

4. **What is a self join?**
   Joining a table to itself; useful for hierarchical data.

5. **What is the difference between WHERE and HAVING?**
   WHERE filters rows before GROUP BY; HAVING filters groups after.

### Intermediate (5)

6. **What is a LATERAL join?**
   Allows subquery to reference columns from preceding tables.

7. **When would you use a CROSS JOIN?**
   Generating combinations (product variants, date series).

8. **What is the difference between a subquery and a JOIN?**
   Subquery returns values; JOIN combines rows. Performance varies.

9. **How do you find unmatched records?**
   LEFT JOIN with IS NULL check.

10. **What is an anti-join?**
    Finding rows in one table without matching rows in another.

### Senior (10)

11. **Explain Nested Loop, Hash Join, and Merge Join.**
    Nested Loop: O(n*m), good for small indexed joins; Hash: O(n+m), builds hash table; Merge: O(n+m), requires sorted data.

12. **How does PostgreSQL choose join algorithm?**
    Based on table sizes, statistics, available indexes, cost estimates.

13. **What is join ordering and why does it matter?**
    Order tables are joined; affects intermediate result sizes and performance.

14. **What is a hash join and when is it optimal?**
    Build hash table on smaller table; optimal for equi-joins on large tables.

15. **How do you optimize a slow JOIN?**
    Index join columns, filter early, use covering indexes, check statistics.

16. **What is a materialized view for join optimization?**
    Pre-computed join result; refresh periodically.

17. **What is the difference between SEMI JOIN and ANTI JOIN?**
    SEMI: returns rows with matches; ANTI: returns rows without matches.

18. **How do joins work with NULL values?**
    NULL != NULL; use IS NULL or COALESCE for NULL handling.

19. **What is a partition-wise join?**
    Join partitions of partitioned tables; improves parallelism.

20. **How do you handle many-to-many joins?**
    Junction/bridge table with foreign keys.

### FAANG-style (5)

21. **Design a schema for a social network with friends and posts.**
    Users, friendships (junction table), posts with proper indexes.

22. **How would you optimize a JOIN on billion-row tables?**
    Partitioning, materialized views, approximate queries.

23. **Explain the impact of joins on ACID transactions.**
    Joins see consistent snapshot; locks affect concurrent access.

24. **Design a real-time analytics system with complex joins.**
    Star schema, columnar storage, pre-aggregated views.

25. **How do you handle JOINs in distributed databases?**
    Co-locate data, shuffle joins, broadcast joins.

### Follow-ups (5)

26. **What is the difference between JOIN and UNION?**
    JOIN combines columns; UNION combines rows.

27. **How do you handle duplicate column names in JOINs?**
    Use aliases and explicit column selection.

28. **What is a natural join and why is it risky?**
    Joins on columns with same name; can produce unexpected results.

29. **What is the performance impact of JOINs on indexing?**
    Join columns need indexes; composite indexes help.

30. **How do you debug a slow JOIN?**
    EXPLAIN ANALYZE, check statistics, index join columns.

## Summary

Joins combine data from multiple tables. INNER JOIN returns only matches; LEFT/RIGHT/FULL JOIN include non-matches. LATERAL JOIN enables correlated subqueries. Always index join columns and use EXPLAIN ANALYZE to verify performance. Choose the right join type based on your data requirements.

## Cheat Sheet

```sql
-- Join types
SELECT * FROM a INNER JOIN b ON a.id = b.a_id;
SELECT * FROM a LEFT JOIN b ON a.id = b.a_id;
SELECT * FROM a RIGHT JOIN b ON a.id = b.a_id;
SELECT * FROM a FULL JOIN b ON a.id = b.a_id;
SELECT * FROM a CROSS JOIN b;
SELECT * FROM a, b WHERE a.id = b.a_id;  -- Comma join (avoid)

-- LATERAL
SELECT * FROM a CROSS JOIN LATERAL (SELECT * FROM b WHERE b.a_id = a.id) sub;

-- Anti-join
SELECT * FROM a LEFT JOIN b ON a.id = b.a_id WHERE b.a_id IS NULL;

-- Self-join
SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;
```

## References & Learn More

- [PostgreSQL JOIN Documentation](https://www.postgresql.org/docs/current/tutorial-join.html)
- [Visualizing SQL Joins - Coding Horror](https://blog.codinghorror.com/a-visual-explanation-of-sql-joins/)
- [PostgreSQL LATERAL JOIN - PostgreSQL Docs](https://www.postgresql.org/docs/current/functions-subquery.html)
- [SQL Joins Explained - GeeksforGeeks](https://www.geeksforgeeks.org/sql-join-set-1-inner-left-right-and-full-joins/)
- [Understanding JOIN Types in SQL - Mode Analytics](https://mode.com/sql-tutorial/sql-joins)
