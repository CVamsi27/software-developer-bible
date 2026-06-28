# Database Transactions

## Definition

A transaction is a logical unit of work that contains one or more SQL statements. Transactions ensure that all operations within them are completed successfully (committed) or none of them take effect (rolled back), maintaining database consistency even in the face of errors or failures.

## Why Do We Need It?

- **Data Consistency**: Ensure partial operations don't corrupt data
- **Atomicity**: All-or-nothing execution
- **Concurrency Control**: Multiple users can work simultaneously
- **Error Recovery**: Roll back on failure
- **ACID Compliance**: Industry standard for reliable transactions

## How It Works

### Transaction Lifecycle

```text
┌─────────────────────────────────────────────────────────────┐
│                    Transaction Lifecycle                      │
│                                                             │
│  ┌─────────────┐                                            │
│  │    BEGIN     │  Start transaction                        │
│  └──────┬──────┘                                            │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │ SQL Statements│  Execute queries                         │
│  │  (reads &   │                                            │
│  │   writes)   │                                            │
│  └──────┬──────┘                                            │
│         │                                                   │
│    ┌────┴────┐                                              │
│    │         │                                              │
│    ▼         ▼                                              │
│  ┌─────┐  ┌──────────┐                                     │
│  │ OK  │  │  ERROR   │                                     │
│  └──┬──┘  └─────┬────┘                                     │
│     │           │                                           │
│     ▼           ▼                                           │
│  ┌─────┐  ┌──────────┐                                     │
│  │COMMIT│  │ ROLLBACK │                                     │
│  └──┬──┘  └─────┬────┘                                     │
│     │           │                                           │
│     ▼           ▼                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                Transaction Complete                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

```

### Isolation Levels

```text
┌─────────────────────────────────────────────────────────────┐
│                    Isolation Levels                          │
│                                                             │
│  Level              │ Dirty Read │ Non-Repeatable │ Phantom │
│                     │            │ Read           │ Read    │
│  ──────────────────┼───────────┼───────────────┼─────────│
│  Read Uncommitted  │   Yes      │     Yes        │  Yes    │
│  Read Committed    │   No       │     Yes        │  Yes    │
│  Repeatable Read   │   No       │     No         │  Yes    │
│  Serializable      │   No       │     No         │  No     │
└─────────────────────────────────────────────────────────────┘

Dirty Read: Reading uncommitted data from another transaction
Non-Repeatable Read: Same query returns different results within transaction
Phantom Read: New rows appear between reads in a transaction

```

## Code Examples

### Basic Transaction

```sql
-- Simple transaction: Transfer money between accounts
BEGIN;

UPDATE accounts SET balance = balance - 100.00 WHERE id = 1;
UPDATE accounts SET balance = balance + 100.00 WHERE id = 2;

-- Verify the transfer
SELECT balance FROM accounts WHERE id IN (1, 2);

COMMIT;  -- Or ROLLBACK if something went wrong

```

### Transaction with Error Handling

```sql
-- PL/pgSQL with exception handling
DO $$
DECLARE
    v_from_balance DECIMAL;
BEGIN
    -- Check sufficient funds
    SELECT balance INTO v_from_balance
    FROM accounts WHERE id = 1
    FOR UPDATE;  -- Lock the row

    IF v_from_balance < 100 THEN
        RAISE EXCEPTION 'Insufficient funds: %', v_from_balance;
    END IF;

    -- Perform transfer
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;

    -- If we get here, commit is automatic in DO block
EXCEPTION WHEN OTHERS THEN
    -- Rollback is automatic on exception
    RAISE NOTICE 'Transaction rolled back: %', SQLERRM;
END;
$$;

```

### Savepoints

```sql
-- Partial rollback with savepoints
BEGIN;

INSERT INTO orders (user_id, total) VALUES (1, 50.00) RETURNING id;

SAVEPOINT order_created;

INSERT INTO order_items (order_id, product_id, quantity)
VALUES (currval('orders_id_seq'), 1, 2);

-- Something went wrong with items, but keep the order
ROLLBACK TO SAVEPOINT order_created;

-- Order exists, but items were rolled back
COMMIT;

```

### Isolation Level Examples

```sql
-- Read Uncommitted (allows dirty reads)
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- May see uncommitted data
COMMIT;

-- Read Committed (PostgreSQL default)
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Sees committed snapshot
-- Another transaction commits a change
SELECT balance FROM accounts WHERE id = 1;  -- May see different value
COMMIT;

-- Repeatable Read
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Snapshot taken
-- Another transaction commits a change
SELECT balance FROM accounts WHERE id = 1;  -- Same value (snapshot)
COMMIT;

-- Serializable
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- All queries see a consistent snapshot
-- Conflicts cause serialization failure
SELECT * FROM accounts WHERE id IN (1, 2);
COMMIT;

```

### Advisory Locks

```sql
-- Advisory locks (application-level)
BEGIN;
SELECT pg_advisory_lock(12345);  -- Lock with key 12345
-- Do work...
SELECT pg_advisory_unlock(12345);
COMMIT;

-- Try-lock (non-blocking)
SELECT pg_try_advisory_lock(12345);
-- Returns true if lock acquired, false if not

```

### Prisma Transactions

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Interactive transaction
async function transferMoney(fromId: number, toId: number, amount: number) {
  return prisma.$transaction(async (tx) => {
    const fromAccount = await tx.account.findUnique({
      where: { id: fromId },
    });

    if (!fromAccount || fromAccount.balance < amount) {
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

// Batch transaction (atomic)
async function createOrderWithItems(
  userId: number,
  items: Array<{ productId: number; quantity: number; price: number }>
) {
  return prisma.$transaction([
    prisma.order.create({
      data: {
        userId,
        total: items.reduce((sum, item) => sum + item.price * item.quantity, 0),
        items: {
          create: items.map((item) => ({
            productId: item.productId,
            quantity: item.quantity,
            unitPrice: item.price,
          })),
        },
      },
    }),
  ]);
}

```

## Real-World Use Cases

### Bank Transfer

```sql
-- Safe bank transfer with proper locking
BEGIN;

-- Lock both accounts to prevent race conditions
SELECT * FROM accounts WHERE id IN (1, 2) FOR UPDATE;

-- Check balances
DO $$
DECLARE
    v_from_balance DECIMAL;
BEGIN
    SELECT balance INTO v_from_balance FROM accounts WHERE id = 1;

    IF v_from_balance < 100 THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
END $$;

-- Perform transfer
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Log the transfer
INSERT INTO transfers (from_id, to_id, amount, created_at)
VALUES (1, 2, 100, NOW());

COMMIT;

```

### Inventory Management

```sql
-- Prevent overselling with row-level locking
BEGIN;

-- Lock the product row
SELECT stock FROM products WHERE id = 1 FOR UPDATE;

-- Check stock
DO $$
BEGIN
    IF (SELECT stock FROM products WHERE id = 1) < 1 THEN
        RAISE EXCEPTION 'Out of stock';
    END IF;
END $$;

-- Decrease stock
UPDATE products SET stock = stock - 1 WHERE id = 1;

-- Create order
INSERT INTO orders (product_id, user_id, quantity)
VALUES (1, 123, 1);

COMMIT;

```

### User Registration with Duplicate Check

```sql
-- Prevent duplicate registrations
BEGIN;

-- Check if email exists
IF EXISTS (SELECT 1 FROM users WHERE email = 'new@example.com') THEN
    RAISE EXCEPTION 'Email already registered';
END IF;

-- Create user
INSERT INTO users (email, name, password_hash)
VALUES ('new@example.com', 'John', 'hashed_password');

-- Create profile
INSERT INTO profiles (user_id, bio)
VALUES (currval('users_id_seq'), '');

COMMIT;

```

## Common Mistakes

### 1. Long-Running Transactions

```sql
-- BAD: Transaction holds locks for too long
BEGIN;
SELECT * FROM large_table;  -- Takes 30 seconds
-- ... user goes to lunch ...
UPDATE other_table SET ...;
COMMIT;  -- Locks held for hours!

-- GOOD: Short transactions
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;  -- Release locks immediately

```

### 2. Not Using FOR UPDATE

```sql
-- BAD: Race condition without locking
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Read balance
-- Another transaction updates the same row
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Based on stale data
COMMIT;

-- GOOD: Lock before reading
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;  -- Lock row
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

```

### 3. Implicit Commit

```sql
-- BAD: DDL causes implicit commit
BEGIN;
INSERT INTO orders (...) VALUES (...);
CREATE TABLE new_table (...);  -- Implicit COMMIT!
-- If next statement fails, order is already committed
INSERT INTO order_items (...) VALUES (...);

-- GOOD: Separate DDL from transactions
-- Run DDL outside of transaction blocks

```

## Best Practices

```sql
-- 1. Keep transactions short
BEGIN;
-- Minimal work
COMMIT;

-- 2. Use appropriate isolation levels
-- Read Committed for most cases
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Serializable for financial transactions
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 3. Use FOR UPDATE for read-modify-write patterns
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- 4. Handle deadlocks gracefully
-- Retry logic in application code
-- Set lock_timeout to avoid long waits
SET lock_timeout = '5s';

-- 5. Use savepoints for complex operations
BEGIN;
INSERT INTO orders (...) VALUES (...);
SAVEPOINT items_insert;
INSERT INTO order_items (...) VALUES (...);
-- If items fail, we can retry without losing the order
COMMIT;

-- 6. Monitor long-running transactions
SELECT
    pid,
    state,
    query_start,
    now() - query_start AS duration,
    query
FROM pg_stat_activity
WHERE state != 'idle'
AND query_start < now() - interval '5 minutes';

```

## Performance Considerations

```sql
-- Transaction overhead
-- Each transaction has overhead: BEGIN, COMMIT, WAL writes
-- Batch operations in single transaction when possible

-- BAD: Many small transactions
INSERT INTO logs (message) VALUES ('log1');
-- Auto-commit
INSERT INTO logs (message) VALUES ('log2');
-- Auto-commit
-- ... repeat 10000 times

-- GOOD: Single transaction
BEGIN;
INSERT INTO logs (message)
SELECT 'log' || generate_series(1, 10000);
COMMIT;

-- Lock duration impact
-- Long transactions hold locks longer
-- Use lock_timeout to prevent indefinite waits
SET lock_timeout = '10s';

-- WAL impact
-- Each transaction generates WAL
-- Frequent commits = more WAL = more I/O

```

## Interview Questions

### Beginner (5)

1. **What is a transaction?**
   A logical unit of work; all-or-nothing execution.

2. **What does ACID stand for?**
   Atomicity, Consistency, Isolation, Durability.

3. **What is the difference between COMMIT and ROLLBACK?**
   COMMIT saves changes; ROLLBACK discards them.

4. **What is the default isolation level in PostgreSQL?**
   Read Committed.

5. **What is a savepoint?**
   A point within a transaction to which you can partially roll back.

### Intermediate (5)

6. **What is a dirty read?**
   Reading uncommitted data from another transaction.

7. **What is the difference between Read Committed and Repeatable Read?**
   Read Committed sees latest committed data; Repeatable Read uses snapshot.

8. **What is a phantom read?**
   New rows appear between reads in a transaction.

9. **What is FOR UPDATE?**
   Locks selected rows until transaction completes.

10. **What are advisory locks?**
    Application-level locks; not tied to table rows.

### Senior (10)

11. **Explain MVCC in PostgreSQL.**
    Multi-Version Concurrency Control; each transaction sees a snapshot.

12. **What is serialization failure?**
    Conflict detected in Serializable isolation; must retry.

13. **How does PostgreSQL handle deadlocks?**
    Detects circular wait; rolls back one transaction.

14. **What is the difference between implicit and explicit transactions?**
    Implicit: auto-commit per statement; Explicit: BEGIN/COMMIT block.

15. **What is a two-phase commit?**
    Protocol for distributed transactions; prepare then commit.

16. **How do you handle transaction timeouts?**
    SET statement_timeout; application-level timeout logic.

17. **What is transaction logging (WAL)?**
    Write-Ahead Log; ensures durability and enables recovery.

18. **What is the difference between READ COMMITTED and READ UNCOMMITTED?**
    READ UNCOMMITTED allows dirty reads; READ COMMITTED doesn't.

19. **How do you implement retry logic for failed transactions?**
    Application-level retry with exponential backoff.

20. **What is the impact of long transactions on performance?**
    Holds locks, prevents vacuum, bloats tables.

### FAANG-style (5)

21. **Design a distributed transaction system.**
    Saga pattern, event sourcing, eventual consistency.

22. **How do you handle transactions across microservices?**
    Saga pattern, two-phase commit, event-driven architecture.

23. **Explain the CAP theorem in context of transactions.**
    PostgreSQL is CP; favors consistency over availability.

24. **How do you achieve exactly-once processing?**
    Idempotency, deduplication, transactional outbox pattern.

25. **Design a real-time bidding system with transactions.**
    Serializable isolation, optimistic locking, row-level locking.

### Follow-ups (5)

26. **What is the difference between optimistic and pessimistic locking?**
    Optimistic: check version at commit; Pessimistic: lock rows upfront.

27. **How do you handle deadlocks in application code?**
    Retry logic, consistent lock ordering, lock timeout.

28. **What is the impact of isolation level on performance?**
    Higher isolation = more overhead; Serializable is slowest.

29. **How do you debug transaction issues?**
    pg_stat_activity, lock monitoring, log_min_duration_statement.

30. **What is the difference between statement-level and transaction-level rollback?**
    SAVEPOINT allows partial rollback; ROLLBACK discards entire transaction.

## Summary

Transactions ensure data consistency through ACID properties. PostgreSQL defaults to Read Committed isolation. Use FOR UPDATE for read-modify-write patterns. Keep transactions short to minimize lock duration. Handle deadlocks and serialization failures with retry logic. Understand MVCC for proper concurrency control.

## Cheat Sheet

```sql
-- Basic transaction
BEGIN;
-- statements
COMMIT;  -- or ROLLBACK

-- Isolation levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Locking
SELECT * FROM table WHERE id = 1 FOR UPDATE;
SELECT * FROM table WHERE id = 1 FOR SHARE;

-- Savepoints
SAVEPOINT sp1;
ROLLBACK TO SAVEPOINT sp1;
RELEASE SAVEPOINT sp1;

-- Advisory locks
SELECT pg_advisory_lock(key);
SELECT pg_try_advisory_lock(key);
SELECT pg_advisory_unlock(key);

-- Monitoring
SELECT * FROM pg_stat_activity WHERE state = 'active';

```

## References & Learn More

- [PostgreSQL Transaction Isolation Documentation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL Locking Documentation](https://www.postgresql.org/docs/current/locking-indexes.html)
- [ACID Transactions Explained - PostgreSQL](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [Understanding Transaction Isolation Levels - Baeldung](https://www.baeldung.com/transaction-isolation-levels)
- [Two-Phase Commit Protocol - Wikipedia](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)
