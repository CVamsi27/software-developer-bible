# Optimistic vs Pessimistic Locking

## Definition

**Optimistic Locking** assumes conflicts are rare and checks for conflicts only at commit time, typically using a version column. **Pessimistic Locking** assumes conflicts are likely and acquires locks before modifying data, preventing other transactions from accessing the same rows until the lock is released.

## Why Do We Need It?

- **Data Integrity**: Prevent lost updates from concurrent modifications
- **Concurrency Control**: Choose strategy based on contention level
- **Performance**: Optimistic for low contention, Pessimistic for high contention
- **Application Reliability**: Prevent silent data corruption
- **Flexibility**: Different strategies for different use cases

## How It Works

### Comparison Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Locking Strategies                         │
│                                                             │
│  OPTIMISTIC LOCKING                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Read data + version number                       │   │
│  │  2. Modify data in application                       │   │
│  │  3. Update with version check                        │   │
│  │     UPDATE SET ... WHERE id = ? AND version = ?      │   │
│  │  4. If affected_rows = 0, conflict occurred          │   │
│  │  5. Retry or fail                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  PESSIMISTIC LOCKING                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Acquire lock (SELECT FOR UPDATE)                 │   │
│  │  2. Read data                                        │   │
│  │  3. Modify data                                      │   │
│  │  4. Update data                                      │   │
│  │  5. Release lock (COMMIT)                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Optimistic Locking Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    Optimistic Locking                         │
│                                                             │
│  T1: Read row (id=1, version=5, balance=100)               │
│  T2: Read row (id=1, version=5, balance=100)               │
│                                                             │
│  T1: Update WHERE id=1 AND version=5                        │
│      → Success (balance=200, version=6)                     │
│                                                             │
│  T2: Update WHERE id=1 AND version=5                        │
│      → Fails (version changed!)                             │
│      → affected_rows = 0                                    │
│      → Retry or handle conflict                             │
└─────────────────────────────────────────────────────────────┘
```

### Pessimistic Locking Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    Pessimistic Locking                       │
│                                                             │
│  T1: SELECT FOR UPDATE (locks row)                          │
│      → Gets lock                                           │
│                                                             │
│  T2: SELECT FOR UPDATE (same row)                           │
│      → Waits for T1 to release lock                        │
│                                                             │
│  T1: UPDATE, COMMIT                                        │
│      → Releases lock                                       │
│                                                             │
│  T2: Gets lock, reads updated data                         │
│      → Proceeds with correct values                        │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Optimistic Locking with Version Column

```sql
-- Schema with version column
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Read account
SELECT id, balance, version FROM accounts WHERE id = 1;
-- Returns: id=1, balance=100, version=5

-- Update with version check
UPDATE accounts
SET balance = balance - 100,
    version = version + 1,
    updated_at = NOW()
WHERE id = 1
AND version = 5;  -- Check version!

-- Check if update succeeded
-- If rows_affected = 0, conflict occurred
-- Retry or handle conflict
```

### Optimistic Locking in TypeScript

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Optimistic locking implementation
async function transferOptimistic(
  fromId: number,
  toId: number,
  amount: number,
  maxRetries = 3
) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Read both accounts with version
      const fromAccount = await prisma.account.findUnique({
        where: { id: fromId },
      });
      const toAccount = await prisma.account.findUnique({
        where: { id: toId },
      });

      if (!fromAccount || !toAccount) {
        throw new Error('Account not found');
      }

      if (fromAccount.balance < amount) {
        throw new Error('Insufficient funds');
      }

      // Update both with version check
      const [fromUpdate, toUpdate] = await Promise.all([
        prisma.account.updateMany({
          where: {
            id: fromId,
            version: fromAccount.version,  // Optimistic lock
          },
          data: {
            balance: { decrement: amount },
            version: { increment: 1 },
            updatedAt: new Date(),
          },
        }),
        prisma.account.updateMany({
          where: {
            id: toId,
            version: toAccount.version,  // Optimistic lock
          },
          data: {
            balance: { increment: amount },
            version: { increment: 1 },
            updatedAt: new Date(),
          },
        }),
      ]);

      if (fromUpdate.count === 0 || toUpdate.count === 0) {
        // Conflict detected - retry
        console.log(`Attempt ${attempt}: Conflict, retrying...`);
        continue;
      }

      return { success: true };
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }
    }
  }

  throw new Error('Max retries exceeded');
}
```

### Pessimistic Locking with SELECT FOR UPDATE

```sql
-- Basic pessimistic locking
BEGIN;

-- Lock the row
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;

-- Now safe to modify
UPDATE accounts SET balance = balance - 100 WHERE id = 1;

COMMIT;  -- Lock released

-- Lock multiple rows in consistent order
BEGIN;
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- NOWAIT: Fail immediately if locked
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;
-- Raises exception if row is locked
COMMIT;

-- SKIP LOCKED: Skip locked rows
BEGIN;
SELECT * FROM tasks WHERE status = 'pending'
FOR UPDATE SKIP LOCKED
LIMIT 10;
-- Returns only unlocked rows
COMMIT;
```

### Pessimistic Locking in TypeScript

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Pessimistic locking with raw SQL
async function transferPessimistic(
  fromId: number,
  toId: number,
  amount: number
) {
  return prisma.$transaction(async (tx) => {
    // Lock rows in consistent order (ascending ID)
    const fromAccount = await tx.$queryRaw`
      SELECT * FROM accounts
      WHERE id = ${Math.min(fromId, toId)}
      FOR UPDATE
    `;

    const toAccount = await tx.$queryRaw`
      SELECT * FROM accounts
      WHERE id = ${Math.max(fromId, toId)}
      FOR UPDATE
    `;

    // Check balances
    const from = fromId < toId ? fromAccount[0] : toAccount[0];
    const to = fromId < toId ? toAccount[0] : fromAccount[0];

    if (from.balance < amount) {
      throw new Error('Insufficient funds');
    }

    // Perform transfer
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

### Hybrid Approach

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Hybrid: Use pessimistic for read, optimistic for write
async function hybridTransfer(
  fromId: number,
  toId: number,
  amount: number
) {
  // Step 1: Pessimistic read (lock rows)
  const [fromAccount, toAccount] = await prisma.$transaction([
    prisma.$queryRaw`
      SELECT * FROM accounts WHERE id = ${fromId} FOR UPDATE
    `,
    prisma.$queryRaw`
      SELECT * FROM accounts WHERE id = ${toId} FOR UPDATE
    `,
  ]);

  // Step 2: Check constraints
  if (fromAccount[0].balance < amount) {
    throw new Error('Insufficient funds');
  }

  // Step 3: Optimistic write (version check)
  const fromVersion = fromAccount[0].version;
  const toVersion = toAccount[0].version;

  const [fromUpdate, toUpdate] = await Promise.all([
    prisma.account.updateMany({
      where: { id: fromId, version: fromVersion },
      data: {
        balance: { decrement: amount },
        version: { increment: 1 },
      },
    }),
    prisma.account.updateMany({
      where: { id: toId, version: toVersion },
      data: {
        balance: { increment: amount },
        version: { increment: 1 },
      },
    }),
  ]);

  if (fromUpdate.count === 0 || toUpdate.count === 0) {
    throw new Error('Conflict detected');
  }
}
```

## Real-World Use Cases

### E-commerce Inventory

```sql
-- Optimistic locking for inventory
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    version INTEGER DEFAULT 1
);

-- Attempt to decrement stock
UPDATE products
SET stock = stock - 1,
    version = version + 1
WHERE id = 1
AND stock > 0
AND version = 5;  -- Optimistic lock

-- If affected_rows = 0, either out of stock or conflict
```

### User Profile Updates

```sql
-- Pessimistic locking for profile updates
BEGIN;

-- Lock user row
SELECT * FROM users WHERE id = 1 FOR UPDATE;

-- Update profile
UPDATE users
SET name = 'John Doe',
    email = 'john@example.com',
    updated_at = NOW()
WHERE id = 1;

COMMIT;
```

### Task Queue Processing

```sql
-- SKIP LOCKED for task queue
BEGIN;

-- Get next unprocessed task
SELECT * FROM tasks
WHERE status = 'pending'
ORDER BY created_at
FOR UPDATE SKIP LOCKED
LIMIT 1;

-- Process task
UPDATE tasks SET status = 'processing' WHERE id = ?;

COMMIT;
```

### Financial Transactions

```sql
-- Two-phase locking for financial data
BEGIN;

-- Lock account
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- Check balance
DO $$
BEGIN
    IF (SELECT balance FROM accounts WHERE id = 1) < 100 THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
END $$;

-- Perform transaction
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
INSERT INTO transactions (account_id, amount) VALUES (1, -100);

COMMIT;
```

## Common Mistakes

### 1. Using Optimistic Locking in High-Contention Scenarios

```sql
-- BAD: Optimistic locking with frequent conflicts
-- Many concurrent updates to same row
UPDATE accounts
SET balance = balance + 10
WHERE id = 1 AND version = 5;
-- High retry rate, poor performance

-- GOOD: Use pessimistic locking for high contention
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance + 10 WHERE id = 1;
COMMIT;
```

### 2. Not Handling Conflicts

```typescript
// BAD: No conflict handling
async function updateAccount(id: number, data: any) {
  const account = await prisma.account.findUnique({ where: { id } });
  await prisma.account.update({
    where: { id, version: account.version },
    data,
  });
  // If update fails, exception thrown without handling
}

// GOOD: Proper conflict handling
async function updateAccount(id: number, data: any, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const account = await prisma.account.findUnique({ where: { id } });
    const result = await prisma.account.updateMany({
      where: { id, version: account.version },
      data: { ...data, version: { increment: 1 } },
    });

    if (result.count > 0) {
      return { success: true };
    }

    if (attempt === maxRetries) {
      throw new Error('Max retries exceeded');
    }
  }
}
```

### 3. Lock Ordering Violations

```sql
-- BAD: Inconsistent lock order
-- T1
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;
COMMIT;

-- T2
BEGIN;
SELECT * FROM accounts WHERE id = 2 FOR UPDATE;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- DEADLOCK
COMMIT;

-- GOOD: Consistent lock order
-- Both T1 and T2
BEGIN;
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
COMMIT;
```

## Best Practices

```sql
-- 1. Choose based on contention level
-- Low contention: Optimistic locking
-- High contention: Pessimistic locking

-- 2. Always have retry logic for optimistic locking
-- Conflict is expected

-- 3. Use consistent lock ordering for pessimistic locking
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;

-- 4. Keep transactions short
BEGIN;
-- Minimal work
COMMIT;

-- 5. Use appropriate lock modes
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- Exclusive lock
SELECT * FROM accounts WHERE id = 1 FOR SHARE;   -- Shared lock

-- 6. Monitor lock contention
SELECT * FROM pg_locks WHERE NOT granted;

-- 7. Set lock timeout
SET lock_timeout = '5s';
```

## Performance Considerations

```sql
-- Optimistic locking
-- Pros: No locks held, better concurrency
-- Cons: Retry overhead, wasted work on conflicts

-- Pessimistic locking
-- Pros: No retries, guaranteed success
-- Cons: Lock contention, reduced concurrency

-- Hybrid approach
-- Use pessimistic for reads, optimistic for writes
-- Balance between consistency and performance

-- Monitoring
SELECT
    mode,
    COUNT(*) AS count,
    SUM(CASE WHEN NOT granted THEN 1 ELSE 0 END) AS waiting
FROM pg_locks
GROUP BY mode;
```

## Interview Questions

### Beginner (5)

1. **What is optimistic locking?**
   Assumes conflicts are rare; checks version at commit time.

2. **What is pessimistic locking?**
   Assumes conflicts are likely; acquires locks before modifying.

3. **When would you use optimistic locking?**
   Low contention scenarios; read-heavy workloads.

4. **When would you use pessimistic locking?**
   High contention scenarios; write-heavy workloads.

5. **What is a version column?**
   Incremented on each update; used for optimistic lock detection.

### Intermediate (5)

6. **How do you implement optimistic locking in SQL?**
   UPDATE ... WHERE id = ? AND version = ?;

7. **What is SELECT FOR UPDATE?**
   Acquires exclusive lock on selected rows.

8. **What is the difference between FOR UPDATE and FOR SHARE?**
   FOR UPDATE: exclusive lock; FOR SHARE: shared lock.

9. **What is NOWAIT?**
   Fails immediately if row is locked.

10. **What is SKIP LOCKED?**
    Skips locked rows; useful for task queues.

### Senior (10)

11. **How do you choose between optimistic and pessimistic locking?**
    Based on contention level, consistency requirements, performance needs.

12. **What is the retry strategy for optimistic locking?**
    Exponential backoff, limited retries, conflict detection.

13. **How do you handle deadlocks with pessimistic locking?**
    Consistent lock ordering, lock timeout, retry logic.

14. **What is the impact of isolation level on locking?**
    Higher isolation = more locks = more contention.

15. **How do you implement optimistic locking in Prisma?**
    Version column, updateMany with version check.

16. **What is two-phase locking (2PL)?**
    Acquire all locks before committing; ensures serializability.

17. **How do you handle long-running transactions with pessimistic locking?**
    Lock timeout, short transactions, optimistic alternative.

18. **What is lock escalation?**
    Converting row locks to table locks; PostgreSQL doesn't do this.

19. **How do you monitor lock contention?**
    pg_locks, pg_stat_activity, deadlock logs.

20. **What is the relationship between MVCC and locking?**
    MVCC reduces lock need; readers don't block writers.

### FAANG-style (5)

21. **Design a distributed locking system.**
    Redis locks, ZooKeeper, consensus protocols.

22. **How would you implement optimistic locking in a distributed system?**
    Vector clocks, version vectors, conflict resolution.

23. **Design a high-concurrency bidding system.**
    Optimistic locking, row-level locking, lock timeout.

24. **How do you handle conflicts in optimistic locking?**
    Last-writer-wins, merge strategies, user resolution.

25. **Design a task queue without deadlocks.**
    SKIP LOCKED, advisory locks, optimistic locking.

### Follow-ups (5)

26. **What is the difference between pessimistic and optimistic concurrency control?**
    Pessimistic: prevent conflicts; Optimistic: detect and resolve.

27. **How do you handle optimistic locking failures?**
    Retry with backoff, user notification, conflict resolution.

28. **What is the impact of optimistic locking on performance?**
    Better concurrency but retry overhead.

29. **How do you choose lock modes?**
    FOR UPDATE for writes, FOR SHARE for reads.

30. **What is the difference between row-level and table-level locks?**
    Row-level: fine-grained, better concurrency; Table-level: coarse, blocks more.

## Summary

Choose optimistic locking for low-contention scenarios; use pessimistic locking for high contention. Optimistic uses version columns and checks at commit time; pessimistic uses SELECT FOR UPDATE. Always implement retry logic for optimistic locking. Use consistent lock ordering to prevent deadlocks with pessimistic locking.

## Cheat Sheet

```sql
-- Optimistic locking
UPDATE table SET version = version + 1 WHERE id = ? AND version = ?;

-- Pessimistic locking
SELECT * FROM table WHERE id = ? FOR UPDATE;
SELECT * FROM table WHERE id = ? FOR UPDATE NOWAIT;
SELECT * FROM table WHERE id = ? FOR UPDATE SKIP LOCKED;
SELECT * FROM table WHERE id = ? FOR SHARE;

-- Monitor locks
SELECT * FROM pg_locks WHERE NOT granted;
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- Set timeout
SET lock_timeout = '5s';
```

## References & Learn More

- [PostgreSQL Explicit Locking Documentation](https://www.postgresql.org/docs/current/explicit-locking.html)
- [Optimistic vs Pessimistic Locking - Baeldung](https://www.baeldung.com/cs/optimistic-vs-pessimistic-locking)
- [Pessimistic vs Optimistic Concurrency Control - GeeksforGeeks](https://www.geeksforgeeks.org/pessimistic-vs-optimistic-concurrency-control/)
- [SKIP LOCKED - PostgreSQL Docs](https://www.postgresql.org/docs/current/sql-select.html)
- [SELECT FOR UPDATE - PostgreSQL Docs](https://www.postgresql.org/docs/current/sql-select.html)
