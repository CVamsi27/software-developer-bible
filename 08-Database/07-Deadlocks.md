# Database Deadlocks

## Definition

A deadlock is a situation where two or more transactions are blocked forever, each waiting for the other to release a lock. In PostgreSQL, deadlocks are detected automatically and resolved by aborting one of the transactions (the victim).

## Why Do We Need It?

- **Data Integrity**: Prevents lost updates from race conditions
- **Concurrent Access**: Multiple transactions can safely modify data
- **Automatic Detection**: PostgreSQL detects and resolves deadlocks
- **Application Reliability**: Proper handling prevents silent failures
- **Performance**: Understanding deadlocks prevents performance issues

## How It Works

### Deadlock Conditions

```text
┌─────────────────────────────────────────────────────────────┐
│                    Deadlock Conditions (Coffman)             │
│                                                             │
│  1. Mutual Exclusion                                        │
│     • Resources cannot be shared                             │
│     • Only one transaction can hold a lock at a time         │
│                                                             │
│  2. Hold and Wait                                           │
│     • Transaction holds a lock while waiting for another     │
│     • Doesn't release held locks                            │
│                                                             │
│  3. No Preemption                                           │
│     • Locks cannot be forcibly taken away                    │
│     • Only released voluntarily by holding transaction       │
│                                                             │
│  4. Circular Wait                                           │
│     • T1 waits for T2, T2 waits for T1                      │
│     • Chain of transactions waiting for each other           │
└─────────────────────────────────────────────────────────────┘
```

### Deadlock Example

```text
┌─────────────────────────────────────────────────────────────┐
│                    Deadlock Scenario                         │
│                                                             │
│  Timeline:                                                  │
│                                                             │
│  T1: BEGIN;                                                │
│  T1: UPDATE accounts SET balance = 100 WHERE id = 1;       │
│      → Locks row 1                                         │
│                                                             │
│  T2: BEGIN;                                                │
│  T2: UPDATE accounts SET balance = 200 WHERE id = 2;       │
│      → Locks row 2                                         │
│                                                             │
│  T1: UPDATE accounts SET balance = 300 WHERE id = 2;       │
│      → Waits for T2 to release row 2                       │
│                                                             │
│  T2: UPDATE accounts SET balance = 400 WHERE id = 1;       │
│      → Waits for T1 to release row 1                       │
│                                                             │
│  DEADLOCK! T1 and T2 are stuck forever.                    │
│                                                             │
│  PostgreSQL detects this and aborts T2 (victim).            │
│  ERROR: deadlock detected                                   │
└─────────────────────────────────────────────────────────────┘
```

### Lock Modes

```text
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Lock Modes                     │
│                                                             │
│  Mode              │ Shared │ Exclusive │ Description       │
│  ─────────────────┼───────┼──────────┼────────────────────│
│  ACCESS SHARE      │   ✓    │     ✓     │ SELECT            │
│  ROW SHARE         │   ✓    │     ✓     │ SELECT FOR UPDATE │
│  ROW EXCLUSIVE     │   ✓    │     ✓     │ INSERT/UPDATE/DEL │
│  SHARE UPDATE EXCL │   ✓    │     ✓     │ VACUUM, ANALYZE   │
│  SHARE             │   ✓    │     ✗     │ CREATE INDEX      │
│  SHARE ROW EXCLUSIVE│  ✓    │     ✗     │ ALTER TABLE       │
│  EXCLUSIVE         │   ✗    │     ✗     │ REFRESH MATERIALIZED│
│  ACCESS EXCLUSIVE  │   ✗    │     ✗     │ DROP, ALTER, LOCK │
└─────────────────────────────────────────────────────────────┘

• Compatible with itself (Shared modes)
• Blocks conflicting modes
```

## Code Examples

### Creating a Deadlock

```sql
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- T1 locks row 1

-- Session 2
BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE id = 2;
-- T2 locks row 2

-- Session 1
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- T1 waits for T2 to release row 2

-- Session 2
UPDATE accounts SET balance = balance + 200 WHERE id = 1;
-- T2 waits for T1 to release row 1
-- DEADLOCK! PostgreSQL aborts one transaction
```

### Preventing Deadlocks with Lock Ordering

```sql
-- BAD: Inconsistent lock order
-- T1: Lock row 1 then row 2
-- T2: Lock row 2 then row 1 → DEADLOCK

-- GOOD: Consistent lock order (always lock by ID ascending)
-- T1: Lock row 1 then row 2
-- T2: Lock row 1 then row 2 → No deadlock

BEGIN;
-- Lock rows in consistent order
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
-- Now safe to update
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### SELECT FOR UPDATE

```sql
-- Lock specific rows for update
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- Other transactions wait for this lock
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- NOWAIT: Fail immediately if locked
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;
-- If row is locked, raises exception immediately

-- SKIP LOCKED: Skip locked rows
BEGIN;
SELECT * FROM orders WHERE status = 'pending'
FOR UPDATE SKIP LOCKED
LIMIT 10;
-- Returns only unlocked rows
COMMIT;
```

### Advisory Locks

```sql
-- Application-level locks (not tied to rows)
BEGIN;
SELECT pg_advisory_lock(12345);  -- Lock key 12345
-- Do critical section...
SELECT pg_advisory_unlock(12345);
COMMIT;

-- Try-lock (non-blocking)
SELECT pg_try_advisory_lock(12345);
-- Returns true if acquired, false if not

-- Named locks
SELECT pg_advisory_lock(hashtext('my_lock'));
SELECT pg_advisory_unlock(hashtext('my_lock'));
```

### Lock Monitoring

```sql
-- Check current locks
SELECT
    l.pid,
    l.mode,
    l.granted,
    l.relation::regclass,
    l.page,
    l.tuple,
    a.query,
    a.state
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;  -- Waiting for lock

-- Check lock waits
SELECT
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query,
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON blocked.pid = bl.pid
JOIN pg_locks kl ON bl.relation = kl.relation
AND bl.page = kl.page
AND bl.tuple = kl.tuple
JOIN pg_stat_activity blocking ON kl.pid = blocking.pid
WHERE NOT bl.granted
AND kl.granted
AND blocked.pid != blocking.pid;

-- Kill a blocking session
SELECT pg_terminate_backend(pid);
```

## Real-World Use Cases

### Bank Transfer (Deadlock Prevention)

```sql
-- Safe transfer with consistent lock ordering
BEGIN;

-- Lock both accounts in ascending order
SELECT * FROM accounts WHERE id IN (from_id, to_id)
ORDER BY id FOR UPDATE;

-- Check balances
DO $$
DECLARE
    v_balance DECIMAL;
BEGIN
    SELECT balance INTO v_balance FROM accounts WHERE id = from_id;
    IF v_balance < amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
END $$;

-- Perform transfer
UPDATE accounts SET balance = balance - amount WHERE id = from_id;
UPDATE accounts SET balance = balance + amount WHERE id = to_id;

-- Log transfer
INSERT INTO transfers (from_id, to_id, amount) VALUES (from_id, to_id, amount);

COMMIT;
```

### Order Processing (Optimistic Locking)

```sql
-- Use version column instead of row locks
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status TEXT DEFAULT 'pending',
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Read order
SELECT id, status, version FROM orders WHERE id = 1;

-- Update with version check
UPDATE orders
SET status = 'processing',
    version = version + 1,
    updated_at = NOW()
WHERE id = 1
AND version = 1;  -- Check version

-- If affected_rows = 0, someone else updated it
-- Retry or handle conflict
```

### Task Queue (SKIP LOCKED)

```sql
-- Safe task processing without deadlocks
BEGIN;

-- Get next unprocessed task (skip locked ones)
SELECT * FROM tasks
WHERE status = 'pending'
ORDER BY created_at
FOR UPDATE SKIP LOCKED
LIMIT 1;

-- Process task
UPDATE tasks SET status = 'processing' WHERE id = ?;

COMMIT;

-- Multiple workers can process different tasks safely
```

## Common Mistakes

### 1. Not Handling Deadlock Errors

```typescript
// BAD: No retry logic
async function transfer(fromId: number, toId: number, amount: number) {
  await prisma.$transaction(async (tx) => {
    await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });
    await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });
  });
}

// GOOD: Retry on deadlock
async function transfer(fromId: number, toId: number, amount: number) {
  const maxRetries = 3;
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await prisma.$transaction(async (tx) => {
        // Use consistent lock ordering
        const [from, to] = await Promise.all([
          tx.account.findUnique({ where: { id: Math.min(fromId, toId) } }),
          tx.account.findUnique({ where: { id: Math.max(fromId, toId) } }),
        ]);

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
      });
    } catch (error) {
      if (error.code === '40P01' && attempt < maxRetries) {
        continue; // Retry on deadlock
      }
      throw error;
    }
  }
}
```

### 2. Lock Ordering Violations

```sql
-- BAD: Different sessions lock in different orders
-- Session 1
BEGIN;
UPDATE accounts SET balance = 100 WHERE id = 1;  -- Lock 1
UPDATE accounts SET balance = 200 WHERE id = 2;  -- Wait for 2

-- Session 2
BEGIN;
UPDATE accounts SET balance = 300 WHERE id = 2;  -- Lock 2
UPDATE accounts SET balance = 400 WHERE id = 1;  -- Wait for 1 → DEADLOCK

-- GOOD: Always lock in same order
-- Both sessions
BEGIN;
UPDATE accounts SET balance = ... WHERE id = LEAST(1, 2);
UPDATE accounts SET balance = ... WHERE id = GREATEST(1, 2);
COMMIT;
```

### 3. Long Transactions Holding Locks

```sql
-- BAD: Transaction holds locks for too long
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- User goes to lunch...
-- ... 2 hours later ...
UPDATE accounts SET balance = 100 WHERE id = 1;
COMMIT;

-- GOOD: Short transactions
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = 100 WHERE id = 1;
COMMIT;  -- Release lock immediately
```

## Best Practices

```sql
-- 1. Use consistent lock ordering
-- Always lock rows in same order (e.g., by ID ascending)
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;

-- 2. Keep transactions short
BEGIN;
-- Minimal work
COMMIT;

-- 3. Use appropriate lock timeout
SET lock_timeout = '5s';
-- Fails if lock not acquired within 5 seconds

-- 4. Use advisory locks for application-level locking
SELECT pg_advisory_lock(hashtext('critical_section'));

-- 5. Use SKIP LOCKED for task queues
SELECT * FROM tasks WHERE status = 'pending'
FOR UPDATE SKIP LOCKED LIMIT 1;

-- 6. Monitor locks regularly
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- 7. Use optimistic locking for read-heavy workloads
UPDATE table SET version = version + 1 WHERE id = 1 AND version = 1;

-- 8. Set deadlock_timeout
SHOW deadlock_timeout;  -- Default: 1s
SET deadlock_timeout = '500ms';
```

## Performance Considerations

```sql
-- Deadlock detection overhead
-- PostgreSQL checks for deadlocks when lock wait exceeds deadlock_timeout
-- Default: 1 second

-- Lock contention monitoring
SELECT
    mode,
    COUNT(*) AS count,
    SUM(CASE WHEN NOT granted THEN 1 ELSE 0 END) AS waiting
FROM pg_locks
GROUP BY mode;

-- Impact on throughput
-- Deadlocks cause transaction restarts
-- Reduce deadlocks = better throughput

-- Avoid table-level locks
-- Use row-level locks (FOR UPDATE) instead of LOCK TABLE
```

## Interview Questions

### Beginner (5)

1. **What is a deadlock?**
   Two or more transactions waiting for each other to release locks.

2. **How does PostgreSQL detect deadlocks?**
   Automatic detection via lock graph analysis.

3. **What happens when a deadlock is detected?**
   One transaction is aborted (the victim).

4. **What is FOR UPDATE?**
   Locks selected rows until transaction completes.

5. **What is lock ordering?**
   Consistent order of acquiring locks to prevent deadlocks.

### Intermediate (5)

6. **What are the four conditions for deadlock?**
   Mutual exclusion, hold and wait, no preemption, circular wait.

7. **What is the difference between pessimistic and optimistic locking?**
   Pessimistic: lock rows upfront; Optimistic: check version at commit.

8. **What is NOWAIT?**
   Fails immediately if row is locked instead of waiting.

9. **What is SKIP LOCKED?**
   Skips locked rows; useful for task queues.

10. **What is advisory locking?**
    Application-level locks; not tied to table rows.

### Senior (10)

11. **How do you prevent deadlocks in application code?**
    Consistent lock ordering, short transactions, retry logic.

12. **What is lock escalation?**
    Converting many row locks to fewer table locks; PostgreSQL doesn't do this.

13. **What is the difference between row-level and table-level locks?**
    Row-level: fine-grained, better concurrency; Table-level: coarse, blocks more.

14. **How do you monitor lock contention in production?**
    pg_locks, pg_stat_activity, deadlock logs.

15. **What is a livelock?**
    Transactions keep restarting but never complete; different from deadlock.

16. **What is lock timeout and how does it help?**
    Fails if lock not acquired within timeout; prevents indefinite waiting.

17. **What is the impact of deadlocks on performance?**
    Transaction restarts, wasted work, reduced throughput.

18. **How do you handle deadlocks in distributed systems?**
    Distributed locks, consensus protocols, retry with backoff.

19. **What is the difference between pessimistic and optimistic concurrency control?**
    Pessimistic: prevent conflicts; Optimistic: detect and resolve conflicts.

20. **What is deadlock_timeout?**
    How long to wait before checking for deadlocks; default 1 second.

### FAANG-style (5)

21. **Design a deadlock-free banking system.**
    Consistent lock ordering, two-phase locking, optimistic locking.

22. **How would you handle deadlocks in a distributed database?**
    Distributed lock manager, consensus protocols, eventual consistency.

23. **Design a high-concurrency task queue without deadlocks.**
    SKIP LOCKED, advisory locks, optimistic locking.

24. **How do you handle deadlocks in microservices?**
    Saga pattern, idempotency, retry with exponential backoff.

25. **Design a real-time bidding system with concurrency control.**
    Optimistic locking, row-level locking, lock timeout.

### Follow-ups (5)

26. **What is two-phase locking (2PL)?**
    Acquire all locks before committing; ensures serializability.

27. **What is the difference between exclusive and shared locks?**
    Exclusive: only one holder; Shared: multiple holders allowed.

28. **How do you test for deadlocks?**
    Concurrent load testing, deadlock detection tools.

29. **What is the relationship between isolation levels and deadlocks?**
    Higher isolation = more locks = more deadlock potential.

30. **How do you choose between pessimistic and optimistic locking?**
    Pessimistic: high contention; Optimistic: low contention.

## Summary

Deadlocks occur when transactions wait for each other in a circular pattern. PostgreSQL detects and resolves them automatically. Prevent deadlocks with consistent lock ordering, short transactions, and appropriate lock modes. Use optimistic locking for read-heavy workloads and SKIP LOCKED for task queues.

## Cheat Sheet

```sql
-- Lock rows
SELECT * FROM table WHERE id = 1 FOR UPDATE;
SELECT * FROM table WHERE id = 1 FOR UPDATE NOWAIT;
SELECT * FROM table WHERE id = 1 FOR UPDATE SKIP LOCKED;

-- Advisory locks
SELECT pg_advisory_lock(key);
SELECT pg_try_advisory_lock(key);
SELECT pg_advisory_unlock(key);

-- Monitor locks
SELECT * FROM pg_locks WHERE NOT granted;
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- Kill blocking session
SELECT pg_terminate_backend(pid);

-- Set timeout
SET lock_timeout = '5s';
SET deadlock_timeout = '500ms';
```

## References & Learn More

- [PostgreSQL Deadlocks Documentation](https://www.postgresql.org/docs/current/explicit-locking.html)
- [Deadlock Detection in PostgreSQL - PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Deadlock)
- [Understanding PostgreSQL Locking - Percona](https://www.percona.com/blog/)
- [How to Resolve Deadlocks - DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-the-sql-deadlock-detect-tool)
- [Two-Phase Locking (2PL) - Wikipedia](https://en.wikipedia.org/wiki/Two-phase_locking)
