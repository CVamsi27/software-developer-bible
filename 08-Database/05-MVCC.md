# MVCC (Multi-Version Concurrency Control)

## Definition

MVCC (Multi-Version Concurrency Control) is a database concurrency control technique that maintains multiple versions of data objects. Each transaction sees a consistent snapshot of the database at a particular point in time, without blocking other transactions from reading or writing. This allows readers and writers to operate concurrently without conflicting.

## Why Do We Need It?

- **Non-blocking Reads**: Readers don't block writers, writers don't block readers
- **Consistent Snapshots**: Each transaction sees a consistent view of data
- **High Concurrency**: Multiple transactions can execute simultaneously
- **No Read Locks Needed**: Readers never acquire locks
- **Snapshot Isolation**: Transactions see data as of transaction start time

## How It Works

### MVCC Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MVCC Overview                             │
│                                                             │
│  Transaction T1 (starts at xid 100)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Reads see committed data as of xid 100             │   │
│  │  Own writes are visible immediately                 │   │
│  │  Other uncommitted writes are invisible             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Transaction T2 (starts at xid 101)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Reads see committed data as of xid 101             │   │
│  │  Own writes are visible immediately                 │   │
│  │  Other uncommitted writes are invisible             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Both can read/write without blocking each other!           │
└─────────────────────────────────────────────────────────────┘
```

### Tuple Visibility Rules

```
┌─────────────────────────────────────────────────────────────┐
│                    Tuple Visibility Rules                     │
│                                                             │
│  For a tuple with xmin (creating xid) and xmax (deleting xid):│
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  VISIBLE if:                                         │   │
│  │  • xmin is committed AND                             │   │
│  │  • xmax is not committed OR not set                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  INVISIBLE if:                                       │   │
│  │  • xmin is not committed (created by active txn)     │   │
│  │  • xmax is committed (deleted by committed txn)      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ABORTED if:                                         │   │
│  │  • xmin is aborted (creating txn rolled back)        │   │
│  │  • xmax is aborted (deleting txn rolled back)        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Transaction ID Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Transaction ID Lifecycle                   │
│                                                             │
│  xid 100 (T1)    xid 101 (T2)    xid 102 (T3)            │
│      │               │               │                      │
│      ▼               ▼               ▼                      │
│  ┌───────┐      ┌───────┐      ┌───────┐                   │
│  │ BEGIN │      │ BEGIN │      │ BEGIN │                   │
│  └───┬───┘      └───┬───┘      └───┬───┘                   │
│      │              │              │                        │
│      ▼              ▼              ▼                        │
│  ┌───────┐      ┌───────┐      ┌───────┐                   │
│  │ COMMIT│      │ COMMIT│      │ROLLBACK│                   │
│  └───┬───┘      └───┬───┘      └───┬───┘                   │
│      │              │              │                        │
│      ▼              ▼              ▼                        │
│  ┌───────┐      ┌───────┐      ┌───────┐                   │
│  │xid 100│      │xid 101│      │ xid   │                   │
│  │committed│     │committed│    │ aborted│                   │
│  └───────┘      └───────┘      └───────┘                   │
│                                                             │
│  xmin: Transaction ID that created the tuple                │
│  xmax: Transaction ID that deleted/updated the tuple        │
│       (0 if not deleted)                                    │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### MVCC in Action

```sql
-- Session 1: Transaction T1 (xid 100)
BEGIN;
UPDATE accounts SET balance = 500 WHERE id = 1;
-- Tuple now has xmin=100, xmax=0

-- Session 2: Transaction T2 (xid 101)
BEGIN;
-- Can still read old version (xmin=99, committed)
SELECT balance FROM accounts WHERE id = 1;
-- Returns 100 (old value)

-- Session 1 commits
COMMIT;

-- Session 2: Still sees old version
SELECT balance FROM accounts WHERE id = 1;
-- Returns 100 (snapshot isolation)

-- Session 2 commits (now sees new data)
COMMIT;
SELECT balance FROM accounts WHERE id = 1;
-- Returns 500
```

### Inspecting Tuple Versions

```sql
-- See tuple versioning information
SELECT
    ctid,           -- Physical location (page, offset)
    xmin,           -- Creating transaction ID
    xmax,           -- Deleting transaction ID (0 if not deleted)
    id,
    name,
    balance
FROM accounts
WHERE id = 1;

-- ctid  | xmin | xmax | id | name   | balance
-- -------+------+------+----+--------+--------
-- (0,1)  |  100 |    0 |  1 | Alice  |    500

-- Check transaction status
SELECT
    txid_current(),           -- Current transaction ID
    txid_status(100),         -- Status of transaction 100
    txid_status(101);         -- Status of transaction 101

-- txid_current | txid_status | txid_status
-- -------------+-------------+------------
--          102 |    committed|   aborted
```

### Vacuum and Dead Tuples

```sql
-- Dead tuples accumulate over time
SELECT
    relname,
    n_live_tup,     -- Live tuples
    n_dead_tup,     -- Dead tuples (old versions)
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE relname = 'accounts';

-- Manual vacuum
VACUUM accounts;           -- Reclaims space, keeps data visible
VACUUM FULL accounts;      -- Reclaims space, locks table
VACUUM ANALYZE accounts;   -- Vacuum + update statistics

-- Autovacuum settings
SHOW autovacuum;
SHOW autovacuum_vacuum_threshold;
SHOW autovacuum_vacuum_scale_factor;
```

### Transaction ID Wraparound

```sql
-- Check current transaction ID
SELECT txid_current();

-- Check age of datfrozenxid
SELECT
    datname,
    age(datfrozenxid) AS xid_age,
    2^31 - age(datfrozenxid) AS transactions_until_wraparound
FROM pg_database
WHERE datname = current_database();

-- Freeze old tuples to prevent wraparound
-- Autovacuum handles this automatically
-- Manual freeze
VACUUM FREEZE accounts;

-- Monitor wraparound risk
SELECT
    relname,
    age(relfrozenxid) AS xid_age,
    pg_size_pretty(pg_relation_size(oid)) AS size
FROM pg_class
WHERE relkind = 'r'
ORDER BY xid_age DESC;
```

### Prisma with MVCC

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Transaction sees consistent snapshot
async function transferMoney(fromId: number, toId: number, amount: number) {
  return prisma.$transaction(async (tx) => {
    // Both reads see the same snapshot
    const from = await tx.account.findUnique({ where: { id: fromId } });
    const to = await tx.account.findUnique({ where: { id: toId } });

    // MVCC ensures no dirty reads
    if (!from || !to || from.balance < amount) {
      throw new Error('Insufficient funds');
    }

    await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });

    return { success: true };
  });
}
```

## Real-World Use Cases

### High-Concurrency E-commerce

```sql
-- Product inventory with MVCC
-- Multiple users can read stock simultaneously
BEGIN;

-- Lock product row for update
SELECT stock FROM products WHERE id = 1 FOR UPDATE;

-- Check stock
IF (SELECT stock FROM products WHERE id = 1) > 0 THEN
    UPDATE products SET stock = stock - 1 WHERE id = 1;
    INSERT INTO orders (product_id, user_id) VALUES (1, 123);
END IF;

COMMIT;

-- Other users can still READ the product (non-blocking)
-- But can't UPDATE until this transaction commits
```

### Reporting Queries

```sql
-- Long-running report without blocking writes
BEGIN;

-- This query sees consistent snapshot even as writes happen
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS orders,
    SUM(total) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1;

-- Writes to orders table continue without blocking
COMMIT;
```

### Audit Trail

```sql
-- Track all changes with MVCC
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    record_id INTEGER,
    operation TEXT,
    old_data JSONB,
    new_data JSONB,
    changed_by INTEGER,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    xid INTEGER DEFAULT txid_current()
);

-- Trigger to log changes
CREATE OR REPLACE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, operation, old_data, new_data)
    VALUES (
        TG_TABLE_NAME,
        CASE WHEN TG_OP = 'DELETE' THEN OLD.id ELSE NEW.id END,
        TG_OP,
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) ELSE NULL END
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
```

## Common Mistakes

### 1. Not Understanding Snapshot Isolation

```sql
-- Session 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;
-- Returns 100

-- Session 2
BEGIN;
UPDATE accounts SET balance = 200 WHERE id = 1;
COMMIT;

-- Session 1: Still sees 100 (snapshot isolation)
SELECT balance FROM accounts WHERE id = 1;
-- Returns 100, not 200!

COMMIT;  -- Must commit to see new data
```

### 2. Ignoring Dead Tuples

```sql
-- BAD: Not vacuuming
-- Dead tuples accumulate, table bloats, queries slow down

-- GOOD: Monitor and vacuum
SELECT
    relname,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup::float / GREATEST(n_live_tup, 1) * 100, 2) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000;

VACUUM ANALYZE large_table;
```

### 3. Long Transactions Prevent Vacuum

```sql
-- BAD: Transaction open for hours
BEGIN;
SELECT * FROM large_table;  -- Takes 1 hour
-- Meanwhile, dead tuples can't be vacuumed
COMMIT;

-- GOOD: Keep transactions short
BEGIN;
-- Do work quickly
COMMIT;
```

## Best Practices

```sql
-- 1. Keep transactions short
-- Long transactions prevent vacuum and cause bloat

-- 2. Monitor dead tuples
SELECT
    relname,
    n_dead_tup,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000;

-- 3. Configure autovacuum appropriately
ALTER TABLE large_table SET (
    autovacuum_vacuum_scale_factor = 0.01,
    autovacuum_analyze_scale_factor = 0.005
);

-- 4. Use VACUUM ANALYZE after bulk operations
VACUUM ANALYZE table_name;

-- 5. Monitor transaction ID age
SELECT
    datname,
    age(datfrozenxid) AS xid_age
FROM pg_database;

-- 6. Avoid long-running transactions in production
-- Set statement_timeout
SET statement_timeout = '30s';

-- 7. Use appropriate isolation levels
-- Read Committed for most cases
-- Serializable for financial transactions
```

## Performance Considerations

```sql
-- MVCC overhead
-- Each UPDATE creates a new tuple version
-- Old versions must be vacuumed

-- Table bloat from dead tuples
SELECT
    relname,
    pg_size_pretty(pg_relation_size(oid)) AS table_size,
    pg_size_pretty(pg_total_relation_size(oid)) AS total_size
FROM pg_class
WHERE relname = 'accounts';

-- Vacuum performance
-- VACUUM (without FULL) is non-blocking
-- VACUUM FULL locks the table

-- Transaction ID wraparound
-- PostgreSQL uses 32-bit transaction IDs
-- Must freeze old tuples before wraparound
-- Autovacuum handles this automatically
```

## Interview Questions

### Beginner (5)

1. **What is MVCC?**
   Multi-Version Concurrency Control; maintains multiple versions of data for concurrent access.

2. **What is a snapshot in MVCC?**
   A consistent view of data at a particular point in time.

3. **What is a dead tuple?**
   An old version of a row that's no longer visible to any transaction.

4. **What is vacuum?**
   Process that reclaims space from dead tuples.

5. **What is transaction ID (xid)?**
   Unique identifier for each transaction; used for visibility checks.

### Intermediate (5)

6. **What is xmin and xmax?**
   xmin: creating transaction ID; xmax: deleting/updating transaction ID.

7. **How does PostgreSQL handle concurrent updates?**
   Last commit wins or serialization error (depending on isolation level).

8. **What is transaction ID wraparound?**
   When xid counter wraps around; prevented by freezing old tuples.

9. **What is the difference between VACUUM and VACUUM FULL?**
   VACUUM: non-blocking, reclaims space; VACUUM FULL: blocking, compacts table.

10. **What is autovacuum?**
    Automatic vacuum process; runs based on thresholds.

### Senior (10)

11. **Explain tuple visibility rules.**
    xmin committed + xmax not committed = visible.

12. **What is the visibility map?**
    Tracks which pages are all-visible; speeds up vacuum and queries.

13. **How does MVCC affect index scans?**
    Indexes point to all versions; must check visibility for each.

14. **What is the difference between hot updates and regular updates?**
    HOT: update doesn't change key columns; avoids index update.

15. **What is the transaction ID freeze threshold?**
    When xid age reaches 200M; autovacuum freezes old tuples.

16. **How do you monitor MVCC health?**
    pg_stat_user_tables (dead tuples), pg_database (xid age).

17. **What is the impact of long transactions on MVCC?**
    Prevent vacuum, cause bloat, increase xid age.

18. **What is a serialization failure?**
    Conflict detected in Serializable isolation; must retry transaction.

19. **How does PostgreSQL detect visibility?**
    Checks xmin/xmax commit status in pg_xact.

20. **What is the difference between read committed and repeatable read in MVCC?**
    Read committed: new snapshot per statement; repeatable read: snapshot per transaction.

### FAANG-style (5)

21. **Design a system to handle 1 million concurrent transactions.**
    Connection pooling, read replicas, partitioning, proper vacuum tuning.

22. **How do you handle MVCC in a distributed database?**
    Hybrid logical clocks, vector clocks, CRDTs.

23. **Explain the write amplification problem in MVCC.**
    Each update creates new version + index updates + WAL.

24. **How do you optimize for read-heavy workloads with MVCC?**
    Read replicas, materialized views, covering indexes.

25. **Design a garbage collection system for old versions.**
    Background vacuum, incremental vacuum, priority-based cleanup.

### Follow-ups (5)

26. **What is the difference between physical and logical replication?**
    Physical: block-level; Logical: row-level with xid tracking.

27. **How do you handle transaction ID exhaustion?**
    Monitoring, autovacuum tuning, emergency freeze.

28. **What is the impact of MVCC on storage?**
    Multiple versions = more storage; vacuum reclaims space.

29. **How do you debug visibility issues?**
    pg_visibility extension, xmin/xmax inspection.

30. **What is the relationship between MVCC and isolation levels?**
    MVCC provides snapshot isolation; higher levels add conflict detection.

## Summary

MVCC enables high concurrency by maintaining multiple versions of data. Each transaction sees a consistent snapshot without blocking others. Understanding xmin/xmax, vacuum, and transaction ID lifecycle is crucial. Keep transactions short to prevent bloat. Monitor dead tuples and xid age regularly.

## Cheat Sheet

```sql
-- Inspect tuple versions
SELECT ctid, xmin, xmax, * FROM table WHERE id = 1;

-- Check transaction status
SELECT txid_current();
SELECT txid_status(xid);

-- Monitor dead tuples
SELECT relname, n_dead_tup FROM pg_stat_user_tables;

-- Monitor xid age
SELECT datname, age(datfrozenxid) FROM pg_database;

-- Vacuum
VACUUM table_name;
VACUUM ANALYZE table_name;
VACUUM FULL table_name;  -- Locks table!

-- Autovacuum settings
SHOW autovacuum;
ALTER TABLE table SET (autovacuum_vacuum_scale_factor = 0.01);
```

## References & Learn More

- [PostgreSQL MVCC Documentation](https://www.postgresql.org/docs/current/mvcc.html)
- [PostgreSQL MVCC Explained - EnterpriseDB](https://www.enterprisedb.com/blog/postgresql-vacuuming-part-1-vacuum-essentials)
- [Understanding MVCC in PostgreSQL - Cybertec](https://www.cybertec-postgresql.com/en/postgresql-multiversion-concurrency-control/)
- [PostgreSQL VACUUM and ANALYZE - PostgreSQL Wiki](https://wiki.postgresql.org/wiki/VACUUM)
- [How MVCC Works - Amazon Aurora Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Aurora PostgreSQL Aurora Repairs.html)
