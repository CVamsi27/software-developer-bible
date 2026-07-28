---
section: SDE Role
category: Interview
tags: [cheat-sheet, reference]
---

# 📋 SDE Interview Cheat Sheet — Last-Minute Review

[![Section](https://img.shields.io/badge/section-SDE%20Role-red)](.)
[![Type](https://img.shields.io/badge/type-Cheat%20Sheet-yellow)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

> **Print this. Read it the night before and morning of your interview.**

---

## ⚡ Phase 1: Java Fundamentals

```text

Collections: ArrayList, HashMap, HashSet, LinkedList, TreeMap, PriorityQueue
Streams:     filter(), map(), flatMap(), reduce(), collect(), sorted()
Lambdas:     (x, y) -> x + y  |  Function<T,R>  |  Predicate<T>
Optional:    of(), empty(), isPresent(), orElse(), map(), flatMap()
Concurrency: synchronized, volatile, ReentrantLock, CountDownLatch
Async:       ExecutorService.submit(), CompletableFuture.supplyAsync().thenApply()

```

**Key Patterns:** `Comparable<T>` (natural order) vs `Comparator<T>` (custom order)

---

## ⚡ Phase 2: Time & Space Complexity

| Complexity | Name | Example |
|------------|------|---------|
| O(1) | Constant | Hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Single loop |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Subsets |
| O(n!) | Factorial | Permutations |

**Rules:** Drop constants, focus on largest term, count operations that scale with input.

---

## ⚡ Phase 3: Data Structures

| Structure | Access | Search | Insert | Delete | Use Case |
|-----------|--------|--------|--------|--------|----------|
| Array | O(1) | O(n) | O(n) | O(n) | Index access |
| Linked List | O(n) | O(n) | O(1) | O(1) | Frequent insert/delete |
| HashMap | O(1) | O(1) | O(1) | O(1) | Key-value lookup |
| TreeMap | O(log n) | O(log n) | O(log n) | O(log n) | Sorted keys |
| BST | O(log n) | O(log n) | O(log n) | O(log n) | Ordered data |
| Heap | - | O(n) | O(log n) | O(log n) | Min/Max queries |
| Stack | - | O(n) | O(1) | O(1) | LIFO, undo, parens |
| Queue | - | O(n) | O(1) | O(1) | FIFO, BFS |
| Trie | O(m) | O(m) | O(m) | O(m) | Prefix search |

---

## ⚡ Phase 4: Sorting Algorithms

| Algorithm | Time (Avg) | Time (Worst) | Space | Stable? |
|-----------|------------|--------------|-------|---------|
| Bubble | O(n²) | O(n²) | O(1) | ✅ |
| Selection | O(n²) | O(n²) | O(1) | ❌ |
| Insertion | O(n²) | O(n²) | O(1) | ✅ |
| Merge | O(n log n) | O(n log n) | O(n) | ✅ |
| Quick | O(n log n) | O(n²) | O(log n) | ❌ |
| Heap | O(n log n) | O(n log n) | O(1) | ❌ |
| Counting | O(n+k) | O(n+k) | O(k) | ✅ |
| Radix | O(nk) | O(nk) | O(n+k) | ✅ |

---

## ⚡ Phase 5: Pattern Recognition

```text

HashMap     → Two sum, frequency, grouping
Two Pointers → Pair problems, sorted arrays, palindrome
Sliding Window → Substring/subarray problems
Prefix Sum  → Range sum queries
Binary Search → Sorted/rotated arrays, search on answer
Stack       → Parentheses, monotonic, evaluate expressions
BFS         → Level-order, shortest path, grid
DFS         → Path problems, connected components, backtracking
Greedy      → Interval scheduling, jump game
DP          → Overlapping subproblems, optimal substructure
Union-Find  → Connected components, dynamic connectivity
Trie        → Prefix matching, autocomplete

```

---

## ⚡ Phase 6: Dynamic Programming

**Template:**

```python
# 1. State: What are we tracking?
# 2. Choice: What decisions do we make?
# 3. Base Case: When do we stop?
# 4. Recurrence: How do subproblems relate?

# Memoization (top-down)
def dp(state):
    if state in memo: return memo[state]
    # make choices, recurse
    memo[state] = result
    return result

# Tabulation (bottom-up)
dp = [0] * (n + 1)
dp[0] = base
for i in range(1, n + 1):
    dp[i] = f(dp[i-1], dp[i-2], ...)

```

**Classic Patterns:**
| Pattern | Problem | Key Insight |
|---------|---------|-------------|
| 0/1 Knapsack | Subset Sum, Partition Equal | dp[i][w] = max(include, exclude) |
| Unbounded Knapsack | Coin Change | Can reuse items |
| LIS | Longest Increasing Subsequence | dp[i] = longest ending at i |
| LCS | Longest Common Subsequence | 2D table, match/mismatch |
| Interval | Burst Balloons | dp[i][j] = max over k |
| Grid | Unique Paths, Min Path Sum | dp[i][j] from neighbors |

---

## ⚡ Phase 7: Graph Algorithms

**BFS:** Queue, level-by-level, shortest path in unweighted graphs
**DFS:** Stack/recursion, explore all paths, cycle detection

| Algorithm | Use Case | Time |
|-----------|----------|------|
| Dijkstra | Shortest path (non-negative) | O((V+E) log V) |
| Bellman-Ford | Shortest path (negative weights) | O(VE) |
| Floyd-Warshall | All-pairs shortest path | O(V³) |
| Kruskal | MST (sort edges) | O(E log E) |
| Prim | MST (grow from vertex) | O((V+E) log V) |
| Topological Sort | DAG ordering, prerequisites | O(V+E) |
| Union-Find | Dynamic connectivity | O(α(n)) amortized |

**Cycle Detection:** Directed → DFS with states (0=unvisited, 1=visiting, 2=visited). Undirected → Union-Find or DFS with parent tracking.

---

## ⚡ Phase 8: Trees (Advanced)

```text

Traversal Orders:
  Preorder:  Root → Left → Right  (copy tree)
  Inorder:   Left → Root → Right  (BST sorted order)
  Postorder: Left → Right → Root  (delete tree)
  Level-order: BFS with queue    (level by level)

```

**Key Properties:**
- BST: Left < Root < Right
- LCA: First node where paths from root diverge
- Serialize: Preorder with null markers
- Trie: Each node = character, path = word

---

## ⚡ Phase 9: Bit Manipulation

```text

x & (x-1)    → Clear lowest set bit
x & (-x)     → Isolate lowest set bit
x ^ x = 0    → XOR self = 0
x ^ 0 = x    → XOR zero = self
1 << n        → 2^n
x >> 1        → x / 2
x & 1         → Check odd/even

```

**Common Tricks:** Single number (XOR all), power of two (`x > 0 && (x & (x-1)) == 0`), count bits, subset generation.

---

## ⚡ Phase 10: Math

```text

GCD(a, b) = GCD(b, a % b)          // Euclidean
LCM(a, b) = a / GCD(a, b) * b      // Avoid overflow
Sieve: O(n log log n) primes up to n
Fast Power: a^n = (a^(n/2))^2       // O(log n)
nCr = n! / (r! * (n-r)!)            // Combinations

```

---

## ⚡ Phase 11: OOP & SOLID

| Principle | Meaning | Example |
|-----------|---------|---------|
| **S**ingle Responsibility | One reason to change | Separate UserService, EmailService |
| **O**pen/Closed | Open for extension, closed for modification | Abstract classes, interfaces |
| **L**iskov Substitution | Subtypes must be substitutable | Animal → Dog/Cat work anywhere Animal works |
| **I**nterface Segregation | Many specific interfaces | Don't force impl of unused methods |
| **D**ependency Inversion | Depend on abstractions | Interface injection, not concrete classes |

**Composition > Inheritance** — Favor has-a over is-a when possible.

---

## ⚡ Phase 12: Design Patterns

| Pattern | Type | Use Case |
|---------|------|----------|
| Singleton | Creational | Single instance (DB, Config) |
| Factory | Creational | Object creation without exposing logic |
| Builder | Creational | Complex object construction |
| Strategy | Behavioral | Swap algorithms at runtime |
| Observer | Behavioral | Event notification, pub-sub |
| Decorator | Structural | Add behavior without modifying |
| Adapter | Structural | Interface compatibility |
| Facade | Structural | Simplify complex subsystem |
| Repository | Architectural | Data access abstraction |
| MVC | Architectural | Model-View-Controller separation |

---

## ⚡ Phase 13: Operating Systems

```text

Process vs Thread: Process = isolated memory, Thread = shared memory
Context Switch: Save/restore registers when switching tasks
Deadlock Conditions: Mutual exclusion, Hold & wait, No preemption, Circular wait
Solutions: Banker's algorithm, resource ordering, timeout

Synchronization:
  Mutex: Binary lock (only owner can unlock)
  Semaphore: Counting lock (N threads allowed)
  Monitor: High-level construct (Java synchronized)

Virtual Memory: Page table maps virtual → physical addresses
Page Replacement: LRU, FIFO, Optimal

```

---

## ⚡ Phase 14: Computer Networks

```text

OSI Model (7 layers):
  7. Application  → HTTP, DNS, FTP
  6. Presentation → SSL/TLS, encryption
  5. Session      → Checkpoints, recovery
  4. Transport    → TCP, UDP
  3. Network      → IP, routing
  2. Data Link    → MAC, Ethernet
  1. Physical     → Cables, signals

TCP vs UDP:
  TCP: Reliable, ordered, connection-oriented (3-way handshake)
  UDP: Unreliable, fast, connectionless

HTTP Methods: GET, POST, PUT, PATCH, DELETE
Status Codes: 200 OK, 201 Created, 301 Redirect, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Server Error

REST: Stateless, resource-based, standard HTTP methods

```

---

## ⚡ Phase 15: Databases

```sql
-- Indexes: B-Tree (range queries), Hash (equality)
-- Normalization: 1NF (atomic), 2NF (no partial), 3NF (no transitive)
-- ACID: Atomicity, Consistency, Isolation, Durability
-- Isolation Levels: Read Uncommitted → Read Committed → Repeatable Read → Serializable
-- Locks: Shared (read), Exclusive (write), Deadlock (wait-for graph)
-- MVCC: Multi-Version Concurrency Control, snapshot isolation

```

**Query Optimization:** EXPLAIN ANALYZE, index on WHERE/JOIN/ORDER BY columns, avoid SELECT *, limit result set.

---

## ⚡ Phase 16: NoSQL & Distributed Systems

```text

CAP Theorem: Pick 2 of Consistency, Availability, Partition Tolerance
  CP: MongoDB, HBase, Redis Cluster
  AP: Cassandra, DynamoDB, CouchDB

Types: Key-Value (Redis), Document (MongoDB), Wide-Column (Cassandra), Graph (Neo4j)

Redis Commands: GET, SET, HSET, LPUSH, SADD, EXPIRE, PUBLISH/SUBSCRIBE
MongoDB: find(), insertOne(), aggregate(), $lookup, $match, $group

```

---

## ⚡ Phase 17: System Design

**Framework:**
1. **Requirements** — Functional (what) + Non-functional (scale, latency, availability)
2. **Estimation** — QPS, storage, bandwidth
3. **High-Level Design** — Services, databases, caches, queues
4. **Deep Dive** — Specific components, algorithms, data models
5. **Bottlenecks** — Single points of failure, scaling strategies

**Key Components:**
| Component | Purpose | Examples |
|-----------|---------|---------|
| Load Balancer | Distribute traffic | NGINX, AWS ALB |
| Cache | Reduce DB load | Redis, Memcached |
| Message Queue | Async processing | Kafka, RabbitMQ |
| CDN | Static content | CloudFront, Cloudflare |
| Database | Persistent storage | PostgreSQL, MongoDB |
| Search | Full-text search | Elasticsearch |
| Object Storage | Files/media | S3, GCS |

**Scaling:** Horizontal (more machines) > Vertical (bigger machine). Sharding (split data) + Replication (copy data).

---

## ⚡ Phase 18: REST APIs

```text

Idempotency: PUT/DELETE = idempotent, POST = not idempotent
Pagination: offset-based (?page=2&limit=20) or cursor-based (?cursor=abc)
Rate Limiting: Token bucket, sliding window, fixed window
Versioning: /api/v1/users, header-based, query param
Authentication: API keys, OAuth2, JWT

```

---

## ⚡ Phase 19: Security

```text

SQL Injection: Use parameterized queries/prepared statements
XSS: Sanitize input, Content-Security-Policy header
CSRF: SameSite cookies, CSRF tokens
CORS: Access-Control-Allow-Origin header
JWT: Header.Payload.Signature, stateless auth
OAuth2: Authorization Code flow, PKCE for SPAs
HTTPS: TLS handshake, certificate chain, HSTS
Password Storage: bcrypt/argon2 + salt, never store plaintext

```

---

## ⚡ Phase 20: Concurrency

```java
// Thread Pool
ExecutorService pool = Executors.newFixedThreadPool(10);
Future<T> future = pool.submit(() -> compute());

// CompletableFuture
CompletableFuture.supplyAsync(() -> fetchData())
    .thenApply(data -> transform(data))
    .thenAccept(result -> save(result));

```

**Lock Types:** Mutex (exclusive), Semaphore (counting), ReadWriteLock (shared reads)

**Common Issues:**
| Issue | Description | Prevention |
|-------|-------------|------------|
| Race Condition | Unsynchronized shared state | synchronized, locks |
| Deadlock | Circular lock waiting | Lock ordering, timeouts |
| Starvation | Thread never gets CPU | Fair locks, priority queues |
| Livelock | Threads yielding forever | Random backoff |

---

## ⚡ Phase 21: Git

```text

git rebase main        → Linear history
git cherry-pick <sha>  → Apply specific commit
git squash commits     → Combine into one
git reset --soft HEAD~1→ Undo commit, keep changes
git revert <sha>       → Create undo commit (safe)

```

---

## ⚡ Phase 22: Linux

```bash
grep -rn "pattern" .        # Recursive search
find . -name "*.ts"         # Find files
awk '{print $1}' file       # Column extraction
sed -i 's/old/new/g' file   # In-place replace
ps aux | grep java          # Process list
curl -X POST url -d '{}'    # HTTP requests
netstat -tlnp               # Listening ports
top -bn1 | head -20         # System stats

```

---

## ⚡ Phase 23: Behavioral (STAR Method)

```text

Situation: Set the context (when, where, what)
Task:      What was your responsibility?
Action:    What did YOU do? (be specific)
Result:    What was the outcome? (metrics, impact)

```

**Key Themes:** Leadership, Conflict Resolution, Failure, Ambiguity, Customer Focus, Mentoring

---

## ⚡ Phase 24: Resume Deep Dive
- Quantify achievements (%, $, time saved)
- 1-page max, keywords for ATS
- Be ready to explain every line

## ⚡ Phase 25: Testing
- Unit (JUnit/Jest): Test individual functions
- Integration: Test service interactions
- E2E: Test full user flows
- TDD: Write tests before code

## ⚡ Phase 26: Cloud & DevOps
- Docker: Containerize apps (Dockerfile, docker-compose)
- Kubernetes: Pods, Services, Deployments
- CI/CD: GitHub Actions, Jenkins pipelines
- Azure/AWS: Compute, Storage, Networking basics

## ⚡ Phase 27: Frontend
- React: Hooks, Virtual DOM, Reconciliation
- Performance: Core Web Vitals (LCP, FID, CLS)
- SSR/SSG/ISR: Next.js rendering strategies
- Accessibility: ARIA labels, keyboard navigation

## ⚡ Phase 28: Mock Interviews
- Practice explaining thought process out loud
- Record yourself, review for fillers (um, uh)
- Use Pramp, Interviewing.io for free mocks

---

## 🎯 Interview Day Quick Reference

**Problem-Solving Flow:**
1. ✅ Understand — Ask clarifying questions
2. ✅ Examples — Work through 2-3 test cases
3. ✅ Brute Force — State the obvious solution
4. ✅ Optimize — Identify patterns, discuss trade-offs
5. ✅ Code — Write clean, readable code
6. ✅ Test — Walk through edge cases
7. ✅ Analyze — State time/space complexity

**Red Flags to Avoid:**
- ❌ Jumping straight to coding without discussing approach
- ❌ Silent thinking without communicating
- ❌ Ignoring edge cases
- ❌ Not asking clarifying questions
- ❌ Giving up too quickly on hard problems

**Green Flags:**
- ✅ Talk through your thought process
- ✅ Ask about constraints and edge cases
- ✅ Start with brute force, then optimize
- ✅ Write clean, well-structured code
- ✅ Handle follow-up questions gracefully

---

> **Good luck! You've got this. 💪**

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Phases 1-8: Java, DSA, Algorithms |
| [Core CS Fundamentals](02-Core-CS-Fundamentals.md) | Phases 9-16: CS Fundamentals, NoSQL |
| [System Design & APIs](03-System-Design-APIs-Security.md) | Phases 17-20: System Design, REST, Security |
| [DevOps & Career](04-DevOps-Behavioral-Career.md) | Phases 21-28: Git, Linux, Behavioral, Cloud |
| [Advanced Topics](05-Advanced-Topics.md) | Segment Tree, DI, Repository, MVC |
| [LeetCode Study Plan](06-LeetCode-Study-Plan.md) | 12-week intensive study plan |
| [Cheat Sheet](07-Cheat-Sheet.md) | Last-minute review for all 28 phases |
| [Microsoft Guide](08-Microsoft-Azure-Interview-Guide.md) | Microsoft Azure team-specific prep |
| [Progress Tracker](09-Progress-Tracker.md) | Track your weekly progress |
| [Mock Interview Bank](10-Mock-Interview-Question-Bank.md) | 90 questions (Coding + SD + Behavioral) |
| [Google Guide](11-Google-Interview-Guide.md) | Google-specific interview prep |
| [Amazon Guide](12-Amazon-Interview-Guide.md) | Amazon Leadership Principles prep |
| [Meta Guide](13-Meta-Interview-Guide.md) | Meta-specific interview prep |
| [Apple Guide](14-Apple-Interview-Guide.md) | Apple-specific interview prep |
---


## Summary

This cheat sheet provides a quick reference for essential interview concepts across all topics, including time complexities, common algorithms, data structure operations, and system design building blocks for rapid review.

## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)

## See Also
- [JavaScript](../01-JavaScript/)
- [TypeScript](../02-TypeScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
