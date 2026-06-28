# Database Normalization

## Definition

Normalization is the process of organizing a relational database to reduce data redundancy and improve data integrity. It involves decomposing tables into smaller, well-structured tables and defining relationships between them, following a series of normal forms (1NF, 2NF, 3NF, BCNF, etc.).

## Why Do We Need It?

- **Eliminate Data Redundancy**: Store each fact only once
- **Prevent Anomalies**: Avoid insertion, update, and deletion anomalies
- **Improve Data Integrity**: Consistent data across the database
- **Easier Maintenance**: Changes to one fact only need to happen in one place
- **Better Query Optimization**: Smaller tables can be more efficient

## How It Works

### Normal Forms Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Normalization Levels                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  UNNORMALIZED FORM (UNF)                           │   │
│  │  • Repeating groups                                 │   │
│  │  • Nested data                                      │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        ▼                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FIRST NORMAL FORM (1NF)                            │   │
│  │  • Atomic values (no repeating groups)              │   │
│  │  • Each row is unique                               │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        ▼                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SECOND NORMAL FORM (2NF)                           │   │
│  │  • Already in 1NF                                   │   │
│  │  • No partial dependencies (full functional         │   │
│  │    dependency on primary key)                       │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        ▼                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  THIRD NORMAL FORM (3NF)                            │   │
│  │  • Already in 2NF                                   │   │
│  │  • No transitive dependencies                       │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        ▼                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  BOYCE-CODD NORMAL FORM (BCNF)                      │   │
│  │  • Already in 3NF                                   │   │
│  │  • Every determinant is a candidate key             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

```

### Functional Dependencies

```text
A → B means "A determines B"
(A functionally determines B)

Example:
  student_id → student_name, major, advisor_id
  major → department_name
  advisor_id → advisor_name

Key concepts:
  • Full functional dependency: All attributes depend on the ENTIRE key
  • Partial dependency: Attribute depends on PART of a composite key
  • Transitive dependency: A → B → C (A determines C through B)

```

## Code Examples

### Unnormalized Table (UNF)

```sql
-- BAD: Unnormalized - repeating groups, redundant data
CREATE TABLE orders_unnormalized (
    order_id INTEGER,
    order_date DATE,
    customer_name TEXT,
    customer_email TEXT,
    customer_address TEXT,
    product1_name TEXT,
    product1_price DECIMAL,
    product1_qty INTEGER,
    product2_name TEXT,
    product2_price DECIMAL,
    product2_qty INTEGER,
    -- More products as columns...
    shipping_cost DECIMAL,
    tax_rate DECIMAL
);

-- Problems:
-- • Can only store fixed number of products per order
-- • If customer changes email, must update ALL their orders
-- • Hard to query: "find all orders for product X"

```

### First Normal Form (1NF)

```sql
-- 1NF: Atomic values, no repeating groups
CREATE TABLE orders_1nf (
    order_id INTEGER PRIMARY KEY,
    order_date DATE,
    customer_name TEXT,
    customer_email TEXT,
    customer_address TEXT,
    product_name TEXT,      -- Single product per row
    product_price DECIMAL,
    product_qty INTEGER,
    shipping_cost DECIMAL,
    tax_rate DECIMAL
);

-- Still has redundancy: customer info repeated for each product
-- Still has anomalies:
--   • Update: Change email → must update multiple rows
--   • Delete: Delete last product → lose customer info
--   • Insert: Can't add customer without an order

```

### Second Normal Form (2NF)

```sql
-- 2NF: Remove partial dependencies
-- Separate entities that depend on different parts of the key

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_email TEXT UNIQUE,
    customer_address TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_price DECIMAL NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    product_qty INTEGER NOT NULL,
    unit_price DECIMAL NOT NULL,  -- Price at time of order
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Still has transitive dependency:
-- order_id → customer_id → customer_name

```

### Third Normal Form (3NF)

```sql
-- 3NF: Remove transitive dependencies

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    shipping_cost DECIMAL NOT NULL,
    tax_rate DECIMAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Now:
-- • Customer info stored once
-- • Product info stored once
-- • Order links to customer via foreign key
-- • Order items link order to product

```

### BCNF (Boyce-Codd Normal Form)

```sql
-- BCNF: Every determinant is a candidate key
-- Example: Course scheduling

-- BAD (3NF but not BCNF):
CREATE TABLE course_schedule_bad (
    student_id INTEGER,
    course_id INTEGER,
    professor_id INTEGER,
    room TEXT,
    time_slot TEXT,
    PRIMARY KEY (student_id, course_id)
);

-- Dependency issue:
-- professor_id → room, time_slot (professor determines room/time)
-- But professor_id is not a candidate key!

-- BCNF: Decompose to eliminate the dependency
CREATE TABLE course_assignments (
    course_id INTEGER,
    professor_id INTEGER,
    room TEXT,
    time_slot TEXT,
    PRIMARY KEY (course_id)  -- professor_id → room, time_slot
);

CREATE TABLE student_enrollments (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id)
);

```

### Denormalization Examples

```sql
-- When and how to denormalize

-- 1. Derived columns for performance
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL NOT NULL,
    category TEXT,
    -- Denormalized for fast reads
    review_count INTEGER DEFAULT 0,
    avg_rating DECIMAL(3, 2) DEFAULT 0,
    total_sold INTEGER DEFAULT 0
);

-- Update denormalized values with triggers
CREATE OR REPLACE FUNCTION update_product_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET
        review_count = (SELECT COUNT(*) FROM reviews WHERE product_id = NEW.product_id),
        avg_rating = (SELECT AVG(rating) FROM reviews WHERE product_id = NEW.product_id)
    WHERE id = NEW.product_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Materialized views for complex queries
CREATE MATERIALIZED VIEW sales_dashboard AS
SELECT
    DATE_TRUNC('day', o.created_at) AS sale_date,
    c.name AS category,
    COUNT(*) AS order_count,
    SUM(o.total) AS revenue,
    AVG(o.total) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
GROUP BY 1, 2;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_dashboard;

-- 3. Redundant data in NoSQL-style
CREATE TABLE user_profiles (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    -- Denormalized from orders table
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0,
    last_order_date TIMESTAMPTZ
);

```

## Real-World Use Cases

### E-commerce Schema (3NF)

```sql
-- Fully normalized e-commerce schema
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id INTEGER REFERENCES categories(id)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    sku TEXT UNIQUE NOT NULL,
    stock_quantity INTEGER DEFAULT 0
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    type TEXT CHECK (type IN ('billing', 'shipping')),
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    is_default BOOLEAN DEFAULT false
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    shipping_address_id INTEGER REFERENCES addresses(id),
    billing_address_id INTEGER REFERENCES addresses(id),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

```

## Common Mistakes

### 1. Over-Normalization

```sql
-- BAD: Normalizing to the point of insanity
CREATE TABLE phone_types (
    id SERIAL PRIMARY KEY,
    type_name TEXT  -- 'mobile', 'home', 'work'
);

CREATE TABLE customer_phones (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    phone_type_id INTEGER REFERENCES phone_types(id),
    phone_number TEXT
);

-- BETTER: Simple enum for fixed values
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    phone TEXT,
    phone_type TEXT CHECK (phone_type IN ('mobile', 'home', 'work'))
);

```

### 2. Not Using Foreign Keys

```sql
-- BAD: No referential integrity
CREATE TABLE orders_bad (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,  -- No foreign key!
    product_id INTEGER    -- No foreign key!
);

-- GOOD
CREATE TABLE orders_good (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id)
);

```

### 3. Storing Derived Data Without Sync

```sql
-- BAD: Derived data gets out of sync
CREATE TABLE orders_bad (
    id SERIAL PRIMARY KEY,
    total DECIMAL 10,  -- Manually calculated, easily wrong
    item_count INTEGER -- Manually counted, easily wrong
);

-- BETTER: Calculate on the fly or use triggers
SELECT
    o.id,
    SUM(oi.quantity * oi.unit_price) AS computed_total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id;

```

## Best Practices

```sql
-- 1. Start normalized, denormalize only when needed
-- Always begin with 3NF; optimize later based on profiling

-- 2. Use constraints to enforce data integrity
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10, 2) CHECK (price > 0),
    stock INTEGER CHECK (stock >= 0)
);

-- 3. Document denormalization decisions
-- Add comments explaining WHY data is denormalized
COMMENT ON COLUMN products.review_count IS
    'Denormalized from reviews table. Updated by trigger on reviews insert.';

-- 4. Use materialized views for complex aggregations
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    date_trunc('month', created_at) AS month,
    SUM(total) AS revenue
FROM orders
GROUP BY 1;

-- 5. Profile before denormalizing
-- Check if the normalized query is actually slow
EXPLAIN ANALYZE SELECT ...;

-- 6. Keep normalization in mind for writes
-- Highly normalized = more joins for reads but faster updates
-- Denormalized = fewer joins but more update work

```

## Performance Considerations

```sql
-- Normalization trade-offs

-- 1. Normalized: More joins, less storage
-- Query: Get order with customer and product info
SELECT
    o.id,
    c.name,
    c.email,
    p.name,
    oi.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 123;

-- 2. Denormalized: Fewer joins, more storage
-- Same query on denormalized table
SELECT id, customer_name, customer_email, product_name, quantity
FROM orders_denormalized
WHERE id = 123;

-- 3. Indexed views (PostgreSQL: use triggers + summary tables)
-- Instead of joining every time, maintain a summary
CREATE TABLE order_summaries (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    total DECIMAL(10, 2),
    item_count INTEGER,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Update with triggers on orders and order_items

```

## Interview Questions

### Beginner (5)

1. **What is normalization?**
   Organizing tables to reduce redundancy and improve integrity.

2. **What is 1NF?**
   Atomic values, no repeating groups, each row unique.

3. **What is the difference between a primary key and a foreign key?**
   Primary key uniquely identifies a row; foreign key references another table's primary key.

4. **What is data redundancy?**
   Storing the same data in multiple places; wastes space and causes anomalies.

5. **What is an anomaly?**
   Inconsistency caused by poor database design (insert, update, delete anomalies).

### Intermediate (5)

6. **Explain 2NF and give an example.**
   No partial dependencies; each non-key attribute depends on the entire primary key.

7. **What is a transitive dependency?**
   A → B → C; A determines C through B. Violates 3NF.

8. **What is BCNF?**
   Every determinant is a candidate key; stricter than 3NF.

9. **When should you denormalize?**
   Read-heavy workloads, complex aggregations, performance-critical queries.

10. **What are the trade-offs of normalization?**
    More joins (slower reads) vs. less storage and easier updates.

### Senior (10)

11. **Design a normalized schema for a blog platform.**
    Users, posts, comments, tags, categories with proper relationships.

12. **How do you handle many-to-many relationships?**
    Junction/bridge tables with foreign keys.

13. **What is an implicit join and why is it dangerous?**
    Comma-separated FROM clause; easy to accidentally create cross joins.

14. **How do you denormalize without losing integrity?**
    Triggers, materialized views, application-level sync.

15. **Explain the concept of a surrogate key vs. natural key.**
    Surrogate: artificial ID; Natural: business meaningful key.

16. **What is a composite primary key?**
    Primary key consisting of multiple columns.

17. **How does normalization affect indexing?**
    Smaller tables = smaller indexes = faster scans.

18. **What is a covering index?**
    Index that contains all columns needed for a query (no table access).

19. **How do you handle schema evolution in normalized databases?**
    Migrations, backward-compatible changes, default values.

20. **What is domain-driven design's impact on normalization?**
    Bounded contexts may justify denormalization within a context.

### FAANG-style (5)

21. **Design a schema for Instagram-like photo sharing.**
    Users, photos, likes, comments, followers with proper normalization.

22. **How would you optimize a schema for billion-row analytics?**
    Star schema, partitioning, materialized views, columnar storage.

23. **Explain the difference between OLTP and OLAP normalization.**
    OLTP: highly normalized; OLAP: denormalized (star/snowflake schema).

24. **Design a multi-tenant SaaS schema with isolation.**
    Schema-per-tenant, row-level security, or database-per-tenant.

25. **How do you handle soft deletes in normalized schemas?**
    deleted_at timestamp, unique constraints must account for soft-deleted rows.

### Follow-ups (5)

26. **What is the difference between a view and a materialized view?**
    View: virtual, always current; Materialized: stored, must be refreshed.

27. **How do you enforce referential integrity without foreign keys?**
    Application logic, triggers, or check constraints (not recommended).

28. **What is denormalization for?**
    Performance optimization by reducing joins at the cost of redundancy.

29. **What are functional dependencies?**
    Mathematical relationships: if A determines B, then for each A there's one B.

30. **How does PostgreSQL handle views?**
    Views are stored queries; updated on SELECT; no performance overhead.

## Summary

Normalization eliminates redundancy and anomalies through a series of normal forms (1NF→2NF→3NF→BCNF). Start with 3NF for most applications. Denormalize selectively for performance in read-heavy workloads. Use materialized views and triggers to maintain consistency when denormalizing. The key trade-off is between write efficiency (normalized) and read performance (denormalized).

## Cheat Sheet

```sql
-- Normal Forms Quick Reference
-- 1NF: Atomic values, no repeating groups
-- 2NF: 1NF + no partial dependencies
-- 3NF: 2NF + no transitive dependencies
-- BCNF: 3NF + every determinant is a candidate key

-- Check for dependencies
-- A → B: A determines B
-- Full dependency: depends on entire PK
-- Partial dependency: depends on part of PK (violates 2NF)
-- Transitive dependency: A → B → C (violates 3NF)

-- Denormalization techniques
-- 1. Derived columns + triggers
-- 2. Materialized views
-- 3. Summary tables
-- 4. Duplicate data with sync

```

## References & Learn More

- [Database Normalization Basics - Microsoft](https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
- [Normalization and De-normalization - GeeksforGeeks](https://www.geeksforgeeks.org/normalization-and-de-normalization/)
- [Database Normal Forms Explained - Vertabelo](https://www.vertabelo.com/blog/database-normalization-explained/)
- [1NF, 2NF, 3NF, BCNF with Examples - Simplilearn](https://www.simplilearn.com/database-normalization-article)
- [Database Design for Mere Mortals - Michael Hernandez](https://www.pearson.com/en-us/subject-catalog/p/database-design-for-mere-mortals/P200000003063)
