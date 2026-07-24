---

# Appendix: Additional Topics

> This appendix covers topics from the original outline that are essential for interview preparation but may not have been covered in detail in the main sections.

---

# Segment Tree (Basic)

> **When to Use:** Range queries (sum, min, max) and range updates on arrays.

## Concept

```
Segment Tree: Binary tree where each node represents a range of the array
- Leaf nodes: individual elements
- Internal nodes: result of combining children (sum, min, max)
- Height: O(log n)
- Space: O(4n) or O(2n)

Use Cases:
- Range sum query: sum(arr[l..r])
- Range min/max query: min(arr[l..r])
- Range update: add value to all elements in [l..r]
```

## Implementation

```java
class SegmentTree {
    private int[] tree;
    private int n;
    
    SegmentTree(int[] arr) {
        n = arr.length;
        tree = new int[4 * n];
        build(arr, 1, 0, n - 1);
    }
    
    void build(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = tree[2 * node] + tree[2 * node + 1]; // sum
        }
    }
    
    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
        } else {
            int mid = (start + end) / 2;
            if (idx <= mid) update(2 * node, start, mid, idx, val);
            else update(2 * node + 1, mid + 1, end, idx, val);
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }
    }
    
    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0; // outside range
        if (l <= start && end <= r) return tree[node]; // fully inside
        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r) + 
               query(2 * node + 1, mid + 1, end, l, r);
    }
}
```

## Problems

| Problem | Difficulty | Pattern |
|---------|-----------|---------|
| [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Easy | Prefix Sum (simpler) |
| [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | Medium | Segment Tree |
| [Range Minimum Query](https://leetcode.com/problems/range-minimum-query-mutable/) | Medium | Segment Tree |
| [Maximum Area Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Hard | Segment Tree variant |

---

# Fenwick Tree / Binary Indexed Tree (Basic)

> **When to Use:** Prefix sum queries with point updates (simpler than Segment Tree).

## Concept

```
Fenwick Tree: Array-based data structure for prefix sum queries
- Space: O(n)
- Update: O(log n)
- Query: O(log n)
- Simpler to implement than Segment Tree

Key Idea: Use binary representation to determine which elements to update/query
- lowbit(x) = x & (-x): the lowest set bit
```

## Implementation

```java
class FenwickTree {
    private int[] tree;
    private int n;
    
    FenwickTree(int[] arr) {
        n = arr.length;
        tree = new int[n + 1];
        for (int i = 0; i < n; i++) {
            update(i + 1, arr[i]);
        }
    }
    
    void update(int i, int delta) {
        while (i <= n) {
            tree[i] += delta;
            i += i & (-i); // add lowbit
        }
    }
    
    int query(int i) { // prefix sum [1..i]
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= i & (-i); // subtract lowbit
        }
        return sum;
    }
    
    int rangeQuery(int l, int r) { // sum [l..r]
        return query(r) - query(l - 1);
    }
}
```

## Fenwick Tree vs Segment Tree

```
| Feature         | Fenwick Tree | Segment Tree    |
|-----------------|--------------|-----------------|
| Space           | O(n)         | O(4n)           |
| Update          | O(log n)     | O(log n)        |
| Query           | O(log n)     | O(log n)        |
| Implementation  | Simple       | Complex         |
| Range Update    | Hard         | Easy            |
| Range Query     | Prefix only | Any operation   |
```

---

# AVL Tree (Concept)

> **When to Use:** Self-balancing BST that guarantees O(log n) operations.

## Concept

```
AVL Tree: Self-balancing Binary Search Tree
- Balance Factor: height(left) - height(right) ∈ {-1, 0, 1}
- Rotations: maintain balance after insert/delete
  - Left Rotation
  - Right Rotation
  - Left-Right Rotation
  - Right-Left Rotation
- Guarantee: O(log n) for search, insert, delete
```

## Rotations

```
Left Rotation (LL case):
    y           x
   / \         / \
  x   C  →    A   y
 / \             / \
A   B           B   C

Right Rotation (RR case):
  x             y
 / \           / \
A   y    →    x   C
   / \       / \
  B   C     A   B

Left-Right Rotation (LR case):
  x         x         z
 / \       / \       / \
A   y  →  A   z  →  x   y
   / \       / \   / \ / \
  z   C     A   B A B C
 / \
B   C

Right-Left Rotation (RL case):
  x         x         z
 / \       / \       / \
y   C  →  z   C  →  x   y
/ \       / \       / \ / \
A   z     y   B     A B C
   / \   / \
  B   C A   B
```

## When to Use AVL vs Red-Black Tree

```
AVL Tree:
- Stricter balancing (height difference ≤ 1)
- Faster lookups (more balanced)
- Slower inserts/deletes (more rotations)
- Use when: read-heavy, fewer writes

Red-Black Tree (used in Java TreeMap, HashMap):
- Less strict balancing
- Fewer rotations on insert/delete
- Use when: write-heavy, balanced read/write
```

---

# Parking Lot Design

> **System Design Problem:** Design a parking lot system.

## Requirements

```
Functional:
- Multiple floors with parking spots
- Different vehicle types (car, motorcycle, truck)
- Entry/exit management
- Parking spot assignment
- Payment calculation

Non-Functional:
- Handle 1000s of vehicles
- Real-time availability
- Support multiple payment methods
```

## High-Level Design

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Entry      │────→│  Parking     │────→│  Spot           │
│   Terminal   │     │  Controller  │     │  Manager        │
└─────────────┘     └──────────────┘     └─────────────────┘
                           │                      │
                    ┌──────┴──────┐        ┌──────┴──────┐
                    │  Display    │        │  Database   │
                    │  Board      │        │  (Redis +   │
                    └─────────────┘        │  PostgreSQL) │
                                           └─────────────┘
```

## Key Classes

```java
// Vehicle
class Vehicle {
    String licensePlate;
    VehicleType type; // CAR, MOTORCYCLE, TRUCK
}

// Parking Spot
class ParkingSpot {
    int floor;
    int spotNumber;
    VehicleType type;
    Vehicle vehicle; // null if empty
    boolean isAvailable() { return vehicle == null; }
}

// Parking Lot
class ParkingLot {
    Map<Integer, List<ParkingSpot>> floors;
    Map<String, ParkingSpot> vehicleToSpot;
    
    ParkingSpot assignSpot(Vehicle vehicle) {
        // Find available spot of correct type
        for (List<ParkingSpot> floor : floors.values()) {
            for (ParkedSpot spot : floor) {
                if (spot.isAvailable() && spot.type == vehicle.type) {
                    spot.vehicle = vehicle;
                    vehicleToSpot.put(vehicle.licensePlate, spot);
                    return spot;
                }
            }
        }
        return null; // no spot available
    }
    
    double releaseSpot(String licensePlate, long exitTime) {
        ParkingSpot spot = vehicleToSpot.remove(licensePlate);
        long duration = exitTime - spot.vehicle.entryTime;
        spot.vehicle = null;
        return calculatePayment(duration, spot.type);
    }
}
```

## Database Schema

```sql
CREATE TABLE parking_spots (
    id SERIAL PRIMARY KEY,
    floor INT,
    spot_number INT,
    vehicle_type VARCHAR(20),
    is_available BOOLEAN DEFAULT true
);

CREATE TABLE parking_transactions (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(20),
    spot_id INT,
    entry_time TIMESTAMP,
    exit_time TIMESTAMP,
    payment_amount DECIMAL
);
```

---

# Distributed Cache Design

> **System Design Problem:** Design a distributed cache (like Redis cluster).

## Requirements

```
Functional:
- put(key, value, ttl)
- get(key)
- delete(key)
- Support millions of keys

Non-Functional:
- High availability
- Low latency (< 1ms)
- Horizontal scaling
- Data consistency
```

## High-Level Design

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client     │────→│  Cache       │────→│  Cache          │
│              │     │  Proxy       │     │  Servers        │
└─────────────┘     └──────────────┘     │  (Redis nodes)  │
                                          └─────────────────┘
                                                 │
                                          ┌──────┴──────┐
                                          │  Persistent  │
                                          │  Storage     │
                                          └─────────────┘
```

## Key Decisions

```
1. Partitioning: Consistent Hashing
   - Each key maps to a position on hash ring
   - Each server owns a range of positions
   - Adding/removing server only affects nearby keys

2. Replication: Leader-Follower
   - Each partition has one leader, multiple followers
   - Writes go to leader, reads from any replica
   - Async replication for performance

3. Eviction Policies:
   - LRU (Least Recently Used) — most common
   - LFU (Least Frequently Used)
   - TTL (Time To Live)
   - No eviction (throw error when full)

4. Consistency:
   - Eventual consistency for performance
   - Read-your-writes consistency option
```

## Consistent Hashing

```java
class ConsistentHash {
    private final TreeMap<Long, String> ring = new TreeMap<>();
    private final int virtualNodes = 150;
    
    void addServer(String server) {
        for (int i = 0; i < virtualNodes; i++) {
            long hash = getHash(server + "#" + i);
            ring.put(hash, server);
        }
    }
    
    void removeServer(String server) {
        for (int i = 0; i < virtualNodes; i++) {
            long hash = getHash(server + "#" + i);
            ring.remove(hash);
        }
    }
    
    String getServer(String key) {
        if (ring.isEmpty()) return null;
        long hash = getHash(key);
        Map.Entry<Long, String> entry = ring.ceilingEntry(hash);
        if (entry == null) entry = ring.firstEntry();
        return entry.getValue();
    }
}
```

---

# Cookies & Sessions

> **Computer Networks Topic:** How state is maintained in HTTP.

## Cookies

```
Cookies: Small pieces of data stored on client side
- Sent with every HTTP request to the same domain
- Set by server via Set-Cookie header
- Have expiration, domain, path, secure, httpOnly flags

Types:
- Session Cookies: deleted when browser closes
- Persistent Cookies: have expiration date
- Secure Cookies: only sent over HTTPS
- HttpOnly Cookies: not accessible via JavaScript (XSS protection)

Example:
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict; Path=/
```

## Sessions

```
Sessions: Server-side storage of user state
- Session ID stored in cookie
- Server maps session ID to user data
- More secure than storing data in cookies

Flow:
1. User logs in → server creates session
2. Server sends session ID in cookie
3. Client sends cookie with every request
4. Server looks up session data
5. Session expires after inactivity
```

## JWT vs Sessions

```
| Feature       | JWT                    | Sessions               |
|---------------|------------------------|------------------------|
| Storage       | Client-side (cookie)   | Server-side            |
| Scalability   | Stateless, easy        | Stateful, harder       |
| Revocation    | Hard (blacklist)       | Easy (delete session)  |
| Performance   | No server lookup       | Server lookup needed   |
| Size          | Larger (contains data) | Smaller (just ID)      |
```

## Security Considerations

```
Cookie Security:
✅ Use HttpOnly flag (prevents XSS)
✅ Use Secure flag (HTTPS only)
✅ Use SameSite=Strict (prevents CSRF)
✅ Set reasonable expiration
❌ Never store sensitive data in cookies

Session Security:
✅ Regenerate session ID after login
✅ Set session timeout
✅ Invalidate on logout
✅ Use secure random session IDs
❌ Never use predictable session IDs
```

---

# Parallel Streams

> **Java Concurrency Topic:** Processing collections in parallel.

## Usage

```java
// Parallel stream processing
List<Integer> numbers = IntStream.rangeClosed(1, 1000000)
    .boxed()
    .collect(Collectors.toList());

// Sequential
long start = System.currentTimeMillis();
long count = numbers.stream()
    .filter(n -> isPrime(n))
    .count();
System.out.println("Sequential: " + (System.currentTimeMillis() - start) + "ms");

// Parallel
start = System.currentTimeMillis();
count = numbers.parallelStream()
    .filter(n -> isPrime(n))
    .count();
System.out.println("Parallel: " + (System.currentTimeMillis() - start) + "ms");

// Custom thread pool
 ForkJoinPool customPool = new ForkJoinPool(4);
 customPool.submit(() -> {
     numbers.parallelStream()
         .filter(n -> isPrime(n))
         .count();
 }).get();
```

## When to Use Parallel Streams

```
USE Parallel Streams When:
✅ Large datasets (> 10,000 elements)
✅ CPU-bound operations (not I/O bound)
✅ Stateless operations (no shared mutable state)
✅ Each element processing is independent

DON'T Use Parallel Streams When:
❌ Small datasets (overhead > benefit)
❌ I/O-bound operations (use CompletableFuture instead)
❌ Operations with shared mutable state
❌ Ordered operations that depend on encounter order
❌ Operations that throw exceptions frequently
```

## Common Pitfalls

```java
// BAD: Shared mutable state
List<Integer> sharedList = new ArrayList<>();
numbers.parallelStream()
    .filter(n -> n > 100)
    .forEach(n -> sharedList.add(n)); // Race condition!

// GOOD: Use collect
List<Integer> result = numbers.parallelStream()
    .filter(n -> n > 100)
    .collect(Collectors.toList()); // Thread-safe

// BAD: Non-thread-safe operations
Map<Integer, Boolean> cache = new HashMap<>();
numbers.parallelStream()
    .forEach(n -> cache.put(n, isPrime(n))); // Race condition!

// GOOD: Use ConcurrentHashMap
Map<Integer, Boolean> safeCache = new ConcurrentHashMap<>();
numbers.parallelStream()
    .forEach(n -> safeCache.put(n, isPrime(n))); // Safe
```

## Performance Considerations

```
Overhead Factors:
- Thread creation/management
- Task splitting and joining
- Synchronization of shared resources
- Context switching

Benchmark:
- 1M elements, CPU-bound: 3-4x speedup
- 100 elements: slower due to overhead
- I/O-bound: use CompletableFuture instead

Best Practices:
- Measure before optimizing
- Use appropriate thread pool size
- Avoid side effects
- Consider work-stealing (ForkJoinPool)
```

---

# Starvation

> **Concurrency Topic:** When a thread is perpetually denied access to resources.

## What is Starvation?

```
Starvation: A thread cannot gain regular access to shared resources
- Happens when high-priority threads monopolize resources
- Low-priority threads may wait indefinitely
- Different from deadlock (threads are waiting, not blocked)

Common Causes:
1. Priority inversion
2. Greedy resource allocation
3. Inadequate locking
```

## Examples

```java
// Starvation example
class Worker implements Runnable {
    private final Lock lock;
    
    Worker(Lock lock) { this.lock = lock; }
    
    public void run() {
        while (true) {
            lock.lock();
            try {
                System.out.println(Thread.currentThread().getName() + " working");
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            } finally {
                lock.unlock();
            }
        }
    }
}

// With ReentrantLock, low-priority threads may starve
ReentrantLock lock = new ReentrantLock();
// Multiple threads competing for lock
// Some threads may never get the lock
```

## Prevention Strategies

```java
// 1. Use fair locks (FIFO ordering)
ReentrantLock fairLock = new ReentrantLock(true); // fair = true
// Ensures longest-waiting thread gets lock next

// 2. Use tryLock with timeout
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try {
        // work
    } finally {
        lock.unlock();
    }
} else {
    // handle timeout — back off and retry
}

// 3. Use read-write locks
ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
// Multiple readers allowed, single writer
// Prevents writer starvation

// 4. Avoid priority inversion
// Use synchronized (which has built-in priority inheritance)
// or explicit priority inheritance protocols

// 5. Use executors with bounded queues
ExecutorService executor = new ThreadPoolExecutor(
    4, 4, 0L, TimeUnit.MILLISECONDS,
    new LinkedBlockingQueue<>(100) // bounded queue
);
```

## Starvation vs Deadlock vs Livelock

```
| Issue      | Description                              | Threads    |
|------------|------------------------------------------|------------|
| Starvation | Thread never gets resource               | Running    |
| Deadlock   | Circular wait, all blocked               | Blocked    |
| Livelock   | Threads keep changing state, no progress | Running    |

Key Difference:
- Starvation: at least one thread makes progress
- Deadlock: NO thread makes progress
- Livelock: threads are active but not progressing
```

---

# Aggregation (OOP)

> **Object-Oriented Programming Topic:** Composition relationship.

## Aggregation vs Composition

```
Aggregation (HAS-A, weak):
- Child can exist independently of parent
- Parent and child have independent lifecycles
- Example: Department has Employees
  - Department is deleted, Employees still exist

Composition (HAS-A, strong):
- Child cannot exist without parent
- Parent controls child lifecycle
  - Example: House has Rooms
  - House is destroyed, Rooms are destroyed too
```

## Examples

```java
// Aggregation: Department has Employees
class Employee {
    String name;
    Employee(String name) { this.name = name; }
}

class Department {
    String name;
    List<Employee> employees; // aggregation — employees exist independently
    
    Department(String name) {
        this.name = name;
        this.employees = new ArrayList<>();
    }
    
    void addEmployee(Employee emp) {
        employees.add(emp);
    }
}

// When Department is destroyed, Employees still exist
Department dept = new Department("Engineering");
Employee alice = new Employee("Alice");
dept.addEmployee(alice);
dept = null; // Department garbage collected
// alice still exists!
```

```java
// Composition: House has Rooms
class Room {
    String name;
    Room(String name) { this.name = name; }
}

class House {
    String address;
    List<Room> rooms; // composition — rooms are created with house
    
    House(String address) {
        this.address = address;
        this.rooms = Arrays.asList(
            new Room("Living Room"),
            new Room("Bedroom"),
            new Room("Kitchen")
        );
    }
}

// When House is destroyed, Rooms are destroyed too
House house = new House("123 Main St");
house = null; // House and all Rooms garbage collected
```

## When to Use Which

```
Use Aggregation When:
- Child can be shared between multiple parents
- Child has independent lifecycle
- Example: Library has Books (Books can be in multiple libraries)

Use Composition When:
- Child belongs to exactly one parent
- Child lifecycle is controlled by parent
- Example: Window has WindowFrame (Frame is part of Window)
```

---

# Message Queue Design

> **System Design Problem:** Design a distributed message queue.

## Requirements

```
Functional:
- produce(topic, message)
- consume(topic, consumerGroup, callback)
- Support multiple topics and consumers
- Guarantee message delivery (at-least-once)

Non-Functional:
- High throughput (millions of messages/sec)
- Low latency (< 10ms)
- Durability (messages persist to disk)
- Horizontal scaling
```

## High-Level Design

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Producer   │────→│  Message     │────→│  Topic          │
│              │     │  Broker      │     │  (Partitioned)  │
└─────────────┘     └──────────────┘     └─────────────────┘
                                                 │
                                          ┌──────┴──────┐
                                          │  Consumer   │
                                          │  Group      │
                                          └─────────────┘
```

## Key Concepts

```
1. Topics and Partitions:
   - Topic: logical channel for messages
   - Partition: physical division of topic (enables parallelism)
   - Messages in same partition are ordered

2. Consumer Groups:
   - Group of consumers that process messages together
   - Each partition consumed by only one consumer in group
   - Enables parallel processing

3. Offsets:
   - Track which messages consumer has processed
   - Enable message replay
   - Stored in consumer group metadata

4. Durability:
   - Write-ahead log (WAL)
   - Replication across brokers
   - Configurable retention period
```

## Kafka-like Architecture

```java
// Producer
class MessageProducer {
    void produce(String topic, String key, String value) {
        // 1. Determine partition (hash(key) % numPartitions)
        // 2. Send to partition leader
        // 3. Wait for acknowledgment
    }
}

// Consumer
class MessageConsumer {
    void consume(String topic, String groupId) {
        // 1. Join consumer group
        // 2. Get assigned partitions
        // 3. Poll messages from assigned partitions
        // 4. Process messages
        // 5. Commit offset
    }
}

// Broker
class MessageBroker {
    Map<String, List<Partition>> topics;
    Map<String, ConsumerGroup> consumerGroups;
    
    void storeMessage(String topic, int partition, Message msg) {
        // 1. Append to partition log
        // 2. Replicate to followers
        // 3. Acknowledge producer
    }
}
```

## Guarantees

```
At-Most-Once: Message may be lost, never duplicated
- Consumer processes then commits offset
- If consumer crashes before commit, message reprocessed

At-Least-Once: Message may be duplicated, never lost (Kafka default)
- Consumer commits offset after processing
- If consumer crashes before commit, message reprocessed

Exactly-Once: Message processed exactly once (hard to achieve)
- Requires idempotent consumers
- Transactional messaging
```

---

# API Gateway Design

> **System Design Concept:** Single entry point for all client requests.

## What is an API Gateway?

```
API Gateway: Single entry point that routes requests to appropriate services

Responsibilities:
1. Request routing → appropriate microservice
2. Authentication/Authorization
3. Rate limiting
4. Request/Response transformation
5. Load balancing
6. Caching
7. Logging and monitoring
8. Protocol translation (HTTP → gRPC)
```

## High-Level Design

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Client     │────→│  API         │────→│  Microservices  │
│   (Web/Mobile)│    │  Gateway     │     │                 │
└─────────────┘     └──────────────┘     └─────────────────┘
                         │
                  ┌──────┴──────┐
                  │  Service    │
                  │  Discovery  │
                  │  (Eureka)   │
                  └─────────────┘
```

## API Gateway vs Direct Service Calls

```
| Feature          | API Gateway        | Direct Calls       |
|------------------|--------------------|--------------------|
| Single Entry     | Yes                | No                 |
| Cross-cutting    | Centralized        | Distributed        |
| Client Coupling  | Loose              | Tight              |
| Protocol Support | Multiple           | Service-specific   |
| Complexity       | Additional layer   | Simpler            |
```

## Common Patterns

```
1. BFF (Backend for Frontend):
   - Separate gateway per client type
   - Web gateway, Mobile gateway, IoT gateway
   - Each optimized for its client

2. API Composition:
   - Gateway aggregates multiple service calls
   - Returns unified response to client
   - Reduces client-side complexity

3. Edge Service:
   - Gateway handles authentication
   - Services focus on business logic
   - Security centralized at edge
```

---

# Microservices Communication Patterns

> **System Design Topic:** How microservices communicate.

## Synchronous Communication

```
REST (HTTP):
- Request-response model
- JSON/XML payloads
- Simple, widely supported
- Use when: CRUD operations, low coupling needed

gRPC:
- Binary protocol (Protocol Buffers)
- HTTP/2 based
- Bidirectional streaming
- Use when: High performance, service-to-service

GraphQL:
- Query language for APIs
- Client specifies exact data needed
- Single endpoint
- Use when: Flexible data requirements
```

## Asynchronous Communication

```
Message Queue (Kafka, RabbitMQ):
- Producer sends message to queue
- Consumer processes asynchronously
- Decouples services
- Use when: Event-driven, eventual consistency OK

Event Streaming (Kafka):
- Ordered, immutable log
- Multiple consumers can read same event
- Replay capability
- Use when: Event sourcing, audit trail

Pub/Sub:
- Publisher sends to topic
- Subscribers receive all messages
- Fan-out pattern
- Use when: Broadcasting, notifications
```

## Communication Pattern Selection

```
| Pattern            | Use Case                    | Consistency     |
|--------------------|-----------------------------|-----------------|
| Request-Response   | CRUD operations             | Strong          |
| Pub/Sub            | Event broadcasting          | Eventual        |
| Event Sourcing     | Audit trail, time travel    | Eventual        |
| CQRS               | Read/write optimization     | Eventual        |
| Saga               | Distributed transactions    | Eventual        |
| Circuit Breaker    | Fault tolerance             | Varies          |
```

---

# Event Sourcing (Basic)

> **System Design Pattern:** Store events instead of state.

## Concept

```
Event Sourcing: Store all changes as a sequence of events

Traditional:
- Store current state: balance = $500
- Update state: balance = $400

Event Sourcing:
- Store events: [Deposited $1000, Withdrew $500, Withdrew $100]
- Current state derived from events
- Complete history preserved

Benefits:
- Complete audit trail
- Time travel (replay to any point)
- Debugging (reproduce exact state)
- Analytics on event patterns
```

## Implementation

```java
// Event
class Event {
    String eventId;
    String aggregateId;
    String eventType;
    Map<String, Object> data;
    Instant timestamp;
}

// Aggregate
class BankAccount {
    String accountId;
    List<Event> events = new ArrayList<>();
    double balance = 0;
    
    void applyEvent(Event event) {
        switch (event.eventType) {
            case "DEPOSITED":
                balance += (double) event.data.get("amount");
                break;
            case "WITHDREW":
                balance -= (double) event.data.get("amount");
                break;
        }
        events.add(event);
    }
    
    // Rebuild state from events
    void rebuild() {
        balance = 0;
        for (Event event : events) {
            applyEvent(event);
        }
    }
    
    // Get state at specific point in time
    double getBalanceAt(Instant timestamp) {
        double bal = 0;
        for (Event event : events) {
            if (event.timestamp.isAfter(timestamp)) break;
            bal = applyEventToBalance(event, bal);
        }
        return bal;
    }
}
```

## Event Store

```
Event Store: Database for storing events

Options:
- PostgreSQL (append-only table)
- Kafka (natural event log)
- EventStoreDB (purpose-built)
- DynamoDB (with append pattern)

Schema:
CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    aggregate_id UUID,
    event_type VARCHAR(50),
    event_data JSONB,
    timestamp TIMESTAMP,
    version INT
);
```

---

# CQRS (Basic)

> **System Design Pattern:** Command Query Responsibility Segregation.

## Concept

```
CQRS: Separate read and write models

Traditional:
- Single model for reads and writes
- Same database for both

CQRS:
- Command model: handles writes (CREATE, UPDATE, DELETE)
- Query model: handles reads (SELECT)
- Can use different databases optimized for each

Benefits:
- Optimize read/write independently
- Scale reads and writes separately
- Different consistency models for reads vs writes
```

## Architecture

```
Commands (Write):
┌─────────┐    ┌─────────────┐    ┌─────────────┐
│ Client   │───→│ Command     │───→│ Write DB    │
│          │    │ Handler     │    │ (PostgreSQL)│
└─────────┘    └─────────────┘    └─────────────┘
                     │
                     ↓ (events)
              ┌─────────────┐
              │ Event Bus   │
              └─────────────┘
                     │
                     ↓
Queries (Read):
┌─────────┐    ┌─────────────┐    ┌─────────────┐
│ Client   │───→│ Query       │───→│ Read DB     │
│          │    │ Handler     │    │ (Redis/ES)  │
└─────────┘    └─────────────┘    └─────────────┘
```

## When to Use CQRS

```
USE CQRS When:
✅ Read and write patterns are very different
✅ Read and write workloads are imbalanced (100:1 reads)
✅ Different consistency requirements for reads vs writes
✅ Complex queries that are hard with standard ORM

DON'T Use CQRS When:
❌ Simple CRUD application
❌ Small team (increases complexity)
❌ Strong consistency needed for all operations
❌ Read and write patterns are similar
```

---

# Resources for Additional Topics

- 📘 **Book:** *Designing Data-Intensive Applications* by Martin Kleppmann — Event Sourcing, CQRS, Distributed Cache
- 📘 **Book:** *System Design Interview (Vol 1 & 2)* by Alex Xu — Parking Lot, Message Queue, API Gateway
- 🌐 **Website:** [AlgoVisualizer](https://algovisualizer.org/) — Segment Tree, Fenwick Tree visualization
- 🌐 **Website:** [VisuAlgo](https://visualgo.net/) — AVL Tree rotations
- 🎥 **YouTube:** [ByteByteGo](https://www.youtube.com/@ByteByteGo) — System Design concepts
- 🌐 **Website:** [Microservices.io](https://microservices.io/patterns/) — Microservices patterns

---

# Dependency Injection

> **Design Pattern:** Invert control of object creation. Dependencies are provided rather than created internally.

## Concept

```
Dependency Injection (DI): A class receives its dependencies from outside
instead of creating them itself.

Without DI (tight coupling):
class UserService {
    private UserRepository repo = new PostgresUserRepository(); // hardcoded
}

With DI (loose coupling):
class UserService {
    private final UserRepository repo;
    UserService(UserRepository repo) { this.repo = repo; } // injected
}
```

## Types of DI

```java
// 1. Constructor Injection (preferred)
class OrderService {
    private final OrderRepository orderRepo;
    private final PaymentService paymentService;
    
    OrderService(OrderRepository orderRepo, PaymentService paymentService) {
        this.orderRepo = orderRepo;
        this.paymentService = paymentService;
    }
}

// 2. Setter Injection
class OrderService {
    private OrderRepository orderRepo;
    
    void setOrderRepo(OrderRepository orderRepo) {
        this.orderRepo = orderRepo;
    }
}

// 3. Field Injection (not recommended, hard to test)
class OrderService {
    @Autowired
    private OrderRepository orderRepo;
}
```

## DI Containers

```
Spring (Java):
- @Component, @Service, @Repository — mark classes for DI
- @Autowired — inject dependencies
- @Configuration — define beans

NestJS (TypeScript):
- @Injectable() — mark class for DI
- @Inject() — inject dependencies
- Module system — organize providers
```

## Benefits

```
✅ Loose coupling — classes don't know about concrete implementations
✅ Testability — easy to inject mocks
✅ Flexibility — swap implementations without changing code
✅ Single Responsibility — classes focus on business logic
```

---

# Repository Pattern

> **Design Pattern:** Abstract data access layer. Separates business logic from persistence.

## Concept

```
Repository: Acts as an in-memory collection of domain objects
- Hides data access complexity
- Provides CRUD operations
- Enables unit testing without database
```

## Implementation

```java
// Interface
interface UserRepository {
    User findById(Long id);
    List<User> findAll();
    User save(User user);
    void delete(Long id);
    User findByEmail(String email);
}

// PostgreSQL implementation
class PostgresUserRepository implements UserRepository {
    private final JdbcTemplate jdbcTemplate;
    
    PostgresUserRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }
    
    public User findById(Long id) {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE id = ?",
            new UserRowMapper(), id
        );
    }
}

// In-memory implementation (for testing)
class InMemoryUserRepository implements UserRepository {
    private final Map<Long, User> users = new HashMap<>();
    
    public User findById(Long id) { return users.get(id); }
    public User save(User user) {
        users.put(user.getId(), user);
        return user;
    }
}
```

## Benefits

```
✅ Separation of concerns — business logic separate from data access
✅ Testability — swap real DB for in-memory in tests
✅ Flexibility — change database without changing business code
✅ Single source of truth — all data access goes through repository
```

---

# MVC (Model-View-Controller)

> **Design Pattern:** Separate application into three interconnected components.

## Concept

```
MVC: Separation of concerns in web applications

Model: Data and business logic
- Represents domain entities
- Contains business rules
- Handles data validation

View: User interface
- Displays data from Model
- Handles user input
- Templates, HTML, React components

Controller: Request handling
- Receives user input
- Interacts with Model
- Returns appropriate View
```

## Flow

```
User Request → Controller → Model → View → Response

1. User clicks button → sends HTTP request
2. Controller receives request, calls Model method
3. Model processes data, returns result
4. Controller selects View, passes data
5. View renders response to user
```

## Implementation (Spring MVC)

```java
// Model
@Entity
class User {
    @Id Long id;
    String name;
    String email;
}

@Repository
interface UserRepository extends JpaRepository<User, Long> {}

// Controller
@RestController
@RequestMapping("/users")
class UserController {
    private final UserRepository userRepository;
    
    UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userRepository.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User saved = userRepository.save(user);
        return ResponseEntity.ok(saved);
    }
}
```

## MVC vs MVVM vs MVP

```
| Pattern | View-Model Binding | Testability | Complexity |
|---------|-------------------|-------------|------------|
| MVC     | Indirect (Controller) | Good | Low |
| MVVM    | Two-way binding (Data binding) | Very Good | Medium |
| MVP     | Presenter mediates | Very Good | Medium |
```
