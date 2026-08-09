<!-- section: System Design | category: Architecture | tags: concept, transactions, theory -->
[![Section](https://img.shields.io/badge/section-System%20Design-blue)](.)
[![Category](https://img.shields.io/badge/category-Architecture-800080)](.)
[![Tags](https://img.shields.io/badge/tags-concept%20%C2%B7%20transactions%20%C2%B7%20theory-lightgrey)](.)

# Distributed Transactions

> **How do you update multiple databases atomically?** This is the hardest problem in distributed systems. There are 3 textbook answers (2PC, 3PC, Saga) and 1 production answer (Saga, almost always).

## TL;DR

- **Atomicity across services/databases** = "all succeed or all fail."
- **2PC (two-phase commit)** = synchronous, blocking, slow. Rarely used in production.
- **3PC (three-phase commit)** = non-blocking, but more failure modes. Also rare.
- **Saga** = sequence of local transactions + compensating actions. Async, scalable. The default choice.
- **Pick per use case.** Money transfers + small scale: 2PC. Microservices at scale: Saga.

---

## Why it matters

Every "user does X, then Y" scenario is a distributed transaction:

- "User pays, we update inventory" — must be atomic
- "User cancels order, we refund payment" — must be atomic
- "User posts a comment, we update follower feeds" — must be atomic-ish

If you get the consistency model wrong, you get:
- Lost money (paid but no inventory)
- Lost data (refund didn't apply)
- User-visible bugs (comment count wrong)

You need to know 2PC and Saga. Most interviews will expect Saga.

---

## The Problem

In a single database, transactions are atomic (ACID). Across multiple databases or services, you don't have a single transaction manager.

```
Service A: write to DB A
Service B: write to DB B
Service C: write to DB C

If A succeeds and B fails: data is inconsistent.
```

How do you make this atomic?

---

## 2PC — Two-Phase Commit

**Pattern:**
1. **Prepare phase:** Coordinator asks all participants "can you commit?" Each locks the resource and replies YES/NO.
2. **Commit phase:** If all say YES, coordinator says "commit" to all. If any says NO, coordinator says "rollback" to all.

```
Coordinator
   │
   ├──→ A: "prepare?" → locks, replies YES
   ├──→ B: "prepare?" → locks, replies YES
   ├──→ C: "prepare?" → locks, replies YES
   │
   └──→ All: "commit" → A commits, B commits, C commits
```

**Pros:**
- Strong atomicity guarantee
- Well-understood, textbook answer

**Cons:**
- **Blocking:** if the coordinator dies after prepare, participants are stuck holding locks
- **Slow:** 2 round trips minimum
- **Coordinator is SPOF:** if it dies at the wrong time, data is stuck
- **Doesn't scale:** all participants must be available

**When to use:** Small-scale, low-latency, strong consistency required. Database-internal XA transactions. NOT for microservices.

**Examples:** XA transactions in Java EE, some RDBMS federated transactions, MySQL with InnoDB and binlog.

---

## 3PC — Three-Phase Commit

**Pattern:** Adds a "pre-commit" phase to 2PC. Designed to be non-blocking.

1. **CanCommit:** Coordinator asks "can you commit?" Participants reply YES/NO without locking.
2. **PreCommit:** If all YES, coordinator says "preCommit." Participants lock and ack.
3. **DoCommit:** Coordinator says "commit." Participants commit.

**Pros (vs 2PC):**
- Non-blocking (in theory): if coordinator dies after preCommit, participants can elect a new coordinator and commit
- Better failure handling

**Cons:**
- **Still has failure modes:** network partition can leave participants unsure
- **More round trips:** even slower
- **Not used in practice:** Saga is preferred

**When to use:** Almost never. Mentioned in interviews for completeness.

---

## Saga — The Production Answer

**Pattern:** Break a distributed transaction into a sequence of local transactions. Each local transaction has a **compensating action** that undoes it. If any step fails, run the compensations in reverse.

### Example: Order Placement

```
1. Create order (local DB)
2. Reserve inventory (local DB)
3. Charge payment (PSP API)
4. Mark order confirmed (local DB)

If step 3 fails:
  Compensate step 2: Release inventory
  Compensate step 1: Mark order as cancelled
```

### Two ways to coordinate Sagas

#### Choreography (no central coordinator)

Each service emits events. Other services listen and react.

```
Order Service: emits "order_created"
Inventory Service: listens, reserves, emits "inventory_reserved"
Payment Service: listens, charges, emits "payment_completed"
Order Service: listens, marks confirmed
```

**Pros:** Simple, no central point of failure.

**Cons:** Hard to understand the flow, hard to debug, no central view of progress.

#### Orchestration (central coordinator)

A central orchestrator tells each service what to do.

```
Saga Orchestrator: → Order Service: "create order"
                    → Inventory Service: "reserve"
                    → Payment Service: "charge"
                    → Order Service: "confirm"
```

**Pros:** Clear flow, easy to debug, can add retries, easy to see where you are.

**Cons:** Coordinator is a SPOF, adds another service to maintain.

**Examples:** Camunda, Temporal, AWS Step Functions, Apache Airflow (for batch).

**In interviews:** Say "orchestrated saga with [Temporal / Step Functions / custom orchestrator]" or "choreographed saga with Kafka events." Pick one and stick with it.

### Saga trade-offs

**Pros:**
- Async, scalable
- No long-held locks
- Each service is independent (no global coordinator)

**Cons:**
- **Not atomic in the ACID sense.** There's a window where the system is "in progress" or "compensating." External observers might see intermediate state.
- **Compensating actions are not always possible.** Some operations are irreversible (e.g., "send email" can't be unsent, though you can send a "sorry" email).
- **Complex failure modes.** Many ways to fail, each needs handling.

### When to use Saga

- Microservices that need to coordinate
- Long-running business processes (minutes to days)
- When 2PC is too slow or unavailable
- Most real-world distributed transactions

---

## Comparison

| Property | 2PC | 3PC | Saga |
|----------|-----|-----|------|
| Atomicity | Strong | Strong | Eventual (compensating) |
| Latency | High (2 round trips) | Higher (3) | Low (async) |
| Availability | Low (blocking) | Medium | High |
| Coordinator SPOF | Yes | Yes | Depends on style |
| Use case | DB-internal | Rare | Microservices |

---

## Common Saga patterns

### 1. Order + Payment + Inventory

```
1. Create order (DB: order created)
2. Reserve inventory (DB: stock decremented)
3. Charge payment (PSP API)
4. Confirm order (DB: order confirmed)

If 3 fails: compensate 2 (release), compensate 1 (mark cancelled)
```

### 2. Booking + Payment + Confirmation

```
1. Hold booking slot (DB: slot held, 10min TTL)
2. Charge payment (PSP API)
3. Confirm booking (DB: slot booked)

If 2 fails: compensate 1 (release slot)
```

### 3. Account transfer (debit + credit)

```
1. Debit account A (DB: A.balance -= X)
2. Credit account B (DB: B.balance += X)

If 2 fails: compensate 1 (A.balance += X)
```

---

## Anti-patterns

- **2PC across microservices.** It's a distributed transaction in name only — it's actually a single point of failure. Use Saga.
- **No compensating actions.** "We can just retry" — sometimes you can't.
- **Sync saga with HTTP calls.** Defeats the purpose. Use async events.
- **Saga with no observability.** "Where in the saga are we?" should be answerable in seconds.
- **Saga with no timeouts.** "What if a service is stuck for 24 hours?" — needs a timeout and compensation.
- **Saga with non-idempotent steps.** Duplicate compensation = wrong state. Always idempotent.

---

## Specific Technologies

| Tech | Use case | Type |
|------|----------|------|
| **Temporal** | Saga orchestration | Managed + open source |
| **AWS Step Functions** | Saga orchestration | Managed |
| **Camunda** | Saga orchestration (BPMN) | Open source |
| **Apache Airflow** | Batch sagas | Open source |
| **Apache Kafka** | Event-driven choreography | Open source |
| **AWS SQS + Lambda** | Simple async saga | Managed |
| **Axon Framework** (Java) | Saga + CQRS + event sourcing | Open source |

---

## When to discuss in interviews

**Always say something about transactions.** When the user action touches multiple services or databases:

- "We use a saga with choreography. Order service emits 'order_created', inventory consumes and reserves, payment consumes and charges, then order service marks confirmed. If any step fails, we run compensating actions in reverse."

**For money-critical scenarios:**

- "For the actual money transfer, we use 2PC within the bank's database — that's a single ACID transaction. But across services (bank + ledger + notification), we use saga."

---

## Related concepts

- [00-Queues-and-Async.md](00-Queues-and-Async.md) — async is the foundation
- [00-CAP-Theorem.md](00-CAP-Theorem.md) — 2PC is CP, Saga is AP (eventual)
- [00-Consistency-Models.md](00-Consistency-Models.md) — saga is eventually consistent
- [../../2-Backend-Stack/12-Microservices/03-Saga-Pattern.md](../../2-Backend-Stack/12-Microservices/03-Saga-Pattern.md) — full saga deep-dive
- [../../2-Backend-Stack/12-Microservices/11-Distributed-Transactions.md](../../2-Backend-Stack/12-Microservices/11-Distributed-Transactions.md)

---

## TL;DR

- **2PC** = strong atomicity, slow, blocking, SPOF. Don't use across microservices.
- **3PC** = non-blocking, but more failure modes. Rare.
- **Saga** = sequence of local transactions + compensating actions. Async, scalable. The default.
- **Choreography** = no central orchestrator, services talk via events.
- **Orchestration** = central orchestrator coordinates the steps.
- **In interviews: name the saga type, the compensating actions, the timeout, the idempotency strategy.**

For case studies, see [06-Payment-Gateway.md](06-Payment-Gateway.md) (saga for charge + ledger), [08-Ticket-Booking.md](08-Ticket-Booking.md) (saga for hold + charge + confirm), [11-Live-Betting.md](11-Live-Betting.md) (saga for bet placement + settlement).
