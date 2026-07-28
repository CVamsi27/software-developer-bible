# Distributed Transactions

[![Category: Architecture](https://img.shields.io/badge/category-Architecture-800080)](.)

oservices while maintaining data consistency. Traditional ACID transactions don't span service boundaries, so distributed patterns like the **Saga pattern** (choreography/orchestration), **Two-Phase Commit (2PC)**, and **Outbox pattern** are used.

## Why Do We Need It?

1. **Data consistency**: Maintain correctness across service boundaries
2. **Failure recovery**: Handle partial failures gracefully with compensating actions
3. **Idempotency**: Ensure retried operations don't cause duplicates
4. **Auditability**: Track all state changes across services

## Patterns Comparison

| Pattern | Consistency | Complexity | Throughput | Use Case |
|---------|:-----------:|:----------:|:----------:|----------|
| **Saga (Choreography)** | Eventual | Low | High | Simple workflows |
| **Saga (Orchestration)** | Eventual | Medium | Medium | Complex workflows |
| **2PC** | Strong | High | Low | Short-lived critical ops |
| **Outbox** | Strong | Medium | High | Reliable messaging |

## Transaction Outbox Pattern

```sql
-- Write to outbox table in same DB transaction
BEGIN;
  INSERT INTO orders (id, amount) VALUES (?, ?);
  INSERT INTO outbox (event_type, payload, created_at)
    VALUES ('order.created', '{"id": ...}', NOW());
COMMIT;

-- Relay process reads and publishes outbox events
```

## Summary

- Distributed transactions span multiple services and require coordination across independent data stores
- Two-Phase Commit (2PC) provides ACID guarantees but has blocking and scalability limitations
- Saga pattern breaks long-lived transactions into a sequence of local transactions with compensating actions
- Choreography-based sagas use event-driven coordination; orchestration-based sagas use a central coordinator
- Transactional Outbox pattern ensures reliable event publishing by storing events in the same database as business data

---

## Cheat Sheet
```text
DISTRIBUTED TRANSACTIONS CHEAT SHEET
============================================================

COMMON PATTERNS:
```
  -- Write to outbox table in same DB transaction
  BEGIN;
    INSERT INTO orders (id, amount) VALUES (?, ?);
    INSERT INTO outbox (event_type, payload, created_at)
      VALUES ('order.created', '{"id": ...}', NOW());
  COMMIT;
```

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [API Gateway](02-API-Gateway.md)
- [CQRS](13-CQRS.md)

## References & Learn More

- [Microservices.io: Saga](https://microservices.io/patterns/data/saga.html)
- [Outbox Pattern](https://microservices.io/patterns/data/transactional-outbox.html)
- [2PC Explained](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)
