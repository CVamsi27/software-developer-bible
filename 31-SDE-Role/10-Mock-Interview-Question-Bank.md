---
section: SDE Role
category: Interview
tags: [practice]
---

# 🎯 Mock Interview Question Bank

> **90 curated questions** for coding, system design, and behavioral rounds.
>
> **How to Use:** Pick 2-3 questions per mock session. Time yourself. Practice explaining your thought process out loud.

---

## 💻 Coding Questions (50)

### Easy (10 Questions)

| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 1 | Two Sum | [#1](https://leetcode.com/problems/two-sum/) | HashMap | 10 min | Use complement lookup |
| 2 | Valid Parentheses | [#20](https://leetcode.com/problems/valid-parentheses/) | Stack | 10 min | Match opening/closing |
| 3 | Merge Two Sorted Lists | [#21](https://leetcode.com/problems/merge-two-sorted-lists/) | Linked List | 10 min | Dummy node technique |
| 4 | Best Time to Buy and Sell Stock | [#121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Array | 10 min | Track min, calculate max profit |
| 5 | Valid Palindrome | [#125](https://leetcode.com/problems/valid-palindrome/) | Two Pointers | 10 min | Skip non-alphanumeric |
| 6 | Invert Binary Tree | [#226](https://leetcode.com/problems/invert-binary-tree/) | Tree | 10 min | Swap children recursively |
| 7 | Maximum Depth of Binary Tree | [#104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Tree | 10 min | 1 + max(left, right) |
| 8 | Linked List Cycle | [#141](https://leetcode.com/problems/linked-list-cycle/) | Fast/Slow Pointer | 10 min | Floyd's cycle detection |
| 9 | Climbing Stairs | [#70](https://leetcode.com/problems/climbing-stairs/) | DP | 10 min | Fibonacci variant |
| 10 | Binary Search | [#704](https://leetcode.com/problems/binary-search/) | Binary Search | 10 min | Classic template |

---

### Medium (25 Questions)

#### Arrays & Strings
| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 11 | 3Sum | [#15](https://leetcode.com/problems/3sum/) | Two Pointers | 25 min | Sort + fix one, two pointers on rest |
| 12 | Container With Most Water | [#11](https://leetcode.com/problems/container-with-most-water/) | Two Pointers | 20 min | Move shorter pointer inward |
| 13 | Product of Array Except Self | [#238](https://leetcode.com/problems/product-of-array-except-self/) | Prefix/Suffix | 20 min | Left pass, right pass |
| 14 | Maximum Subarray | [#53](https://leetcode.com/problems/maximum-subarray/) | Kadane's | 15 min | Track current sum, reset if negative |
| 15 | Merge Intervals | [#56](https://leetcode.com/problems/merge-intervals/) | Sorting | 20 min | Sort by start, merge overlapping |

#### Hash Maps & Sets
| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 16 | Group Anagrams | [#49](https://leetcode.com/problems/group-anagrams/) | HashMap | 20 min | Sorted string as key |
| 17 | Longest Consecutive Sequence | [#128](https://leetcode.com/problems/longest-consecutive-sequence/) | HashSet | 20 min | Only start counting from sequence start |
| 18 | Top K Frequent Elements | [#347](https://leetcode.com/problems/top-k-frequent-elements/) | Bucket Sort | 20 min | Frequency buckets, not heap |
| 19 | Subarray Sum Equals K | [#560](https://leetcode.com/problems/subarray-sum-equals-k/) | Prefix Sum + HashMap | 25 min | Count prefix sums |
| 20 | LRU Cache | [#146](https://leetcode.com/problems/lru-cache/) | Design | 25 min | HashMap + Doubly Linked List |

#### Linked Lists
| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 21 | Add Two Numbers | [#2](https://leetcode.com/problems/add-two-numbers/) | Linked List | 20 min | Carry propagation |
| 22 | Remove Nth Node From End | [#19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Two Pointers | 15 min | Gap of n between pointers |
| 23 | Reorder List | [#143](https://leetcode.com/problems/reorder-list/) | Split + Reverse | 25 min | Find middle, reverse second half, merge |

#### Trees
| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 24 | Binary Tree Level Order Traversal | [#102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS | 20 min | Queue with level size tracking |
| 25 | Validate BST | [#98](https://leetcode.com/problems/validate-bst/) | DFS | 20 min | Pass min/max bounds down |
| 26 | Lowest Common Ancestor | [#236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | DFS | 20 min | Return node if found in subtree |
| 27 | Construct Binary Tree from Preorder and Inorder | [#105](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | DFS | 25 min | First preorder = root, find in inorder |
| 28 | Serialize and Deserialize Binary Tree | [#297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | BFS/DFS | 30 min | Preorder with null markers |

#### Graphs
| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 29 | Number of Islands | [#200](https://leetcode.com/problems/number-of-islands/) | DFS/BFS | 20 min | Flood fill, mark visited |
| 30 | Course Schedule | [#207](https://leetcode.com/problems/course-schedule/) | Topological Sort | 25 min | Detect cycle in directed graph |
| 31 | Clone Graph | [#133](https://leetcode.com/problems/clone-graph/) | DFS + HashMap | 20 min | Map old to new nodes |
| 32 | Pacific Atlantic Water Flow | [#417](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Reverse DFS | 25 min | DFS from ocean edges inward |

#### Dynamic Programming
| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 33 | Coin Change | [#322](https://leetcode.com/problems/coin-change/) | Unbounded Knapsack | 20 min | dp[i] = min coins for amount i |
| 34 | Longest Increasing Subsequence | [#300](https://leetcode.com/problems/longest-increasing-subsequence/) | LIS | 25 min | dp[i] = longest ending at i |
| 35 | Word Break | [#139](https://leetcode.com/problems/word-break/) | DP + Dictionary | 20 min | Check all prefixes |

---

### Hard (15 Questions)

| # | Problem | LeetCode # | Pattern | Time Target | Key Insight |
|---|---------|------------|---------|-------------|-------------|
| 36 | Trapping Rain Water | [#42](https://leetcode.com/problems/trapping-rain-water/) | Two Pointers | 30 min | Track left_max, right_max |
| 37 | Merge K Sorted Lists | [#23](https://leetcode.com/problems/merge-k-sorted-lists/) | Heap | 30 min | Min heap of size k |
| 38 | Minimum Window Substring | [#76](https://leetcode.com/problems/minimum-window-substring/) | Sliding Window | 35 min | Expand until valid, shrink to minimize |
| 39 | Binary Tree Maximum Path Sum | [#124](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | DFS | 35 min | Track global max, return path through node |
| 40 | Find Median from Data Stream | [#295](https://leetcode.com/problems/find-median-from-data-stream/) | Two Heaps | 30 min | Max heap for lower half, min heap for upper |
| 41 | Word Ladder | [#127](https://leetcode.com/problems/word-ladder/) | BFS | 30 min | BFS for shortest path, neighbor pattern |
| 42 | Alien Dictionary | [#269](https://leetcode.com/problems/alien-dictionary/) | Topological Sort | 35 min | Build graph from character comparisons |
| 43 | Regular Expression Matching | [#10](https://leetcode.com/problems/regular-expression-matching/) | 2D DP | 40 min | Handle '.' and '*' cases |
| 44 | Edit Distance | [#72](https://leetcode.com/problems/edit-distance/) | 2D DP | 35 min | dp[i][j] = min operations for s1[:i], s2[:j] |
| 45 | Burst Balloons | [#312](https://leetcode.com/problems/burst-balloons/) | Interval DP | 40 min | dp[i][j] = max coins bursting i to j |
| 46 | Largest Rectangle in Histogram | [#84](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Monotonic Stack | 30 min | Track indices of increasing heights |
| 47 | Sliding Window Maximum | [#239](https://leetcode.com/problems/sliding-window-maximum/) | Monotonic Deque | 30 min | Maintain decreasing deque of indices |
| 48 | Median of Two Sorted Arrays | [#4](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Binary Search | 40 min | Binary search on partition |
| 49 | Serialize and Deserialize Binary Tree | [#297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Design | 30 min | Preorder with null markers |
| 50 | LRU Cache | [#146](https://leetcode.com/problems/lru-cache/) | Design | 25 min | HashMap + Doubly Linked List |

---

## 🏗️ System Design Questions (20)

### Beginner (5 Questions)

| # | Question | Core Concepts | Key Components | Time Limit |
|---|----------|---------------|----------------|------------|
| 1 | **Design a URL Shortener (TinyURL)** | Hashing, Base62, Redirect | API, DB, Cache, Analytics | 30 min |
| 2 | **Design a Rate Limiter** | Token Bucket, Sliding Window | Counter, Timer, Redis | 25 min |
| 3 | **Design a Key-Value Store** | Hashing, Replication | Consistent Hashing, Raft | 30 min |
| 4 | **Design a Unique ID Generator** | Snowflake, UUID | Sequence, Timestamp, Worker ID | 25 min |
| 5 | **Design a Pastebin** | CRUD, Expiration | API, Storage, CDN | 25 min |

#### Detailed Breakdown: URL Shortener

```text

Requirements:
- Shorten URLs (POST /shorten)
- Redirect to original (GET /{shortCode})
- Analytics (click tracking)
- Custom aliases (optional)

High-Level Design:
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Client  │────▶│   API   │────▶│   DB    │
└─────────┘     │  Server │     └─────────┘
                └────┬────┘
                     │
                ┌────▼────┐
                │  Cache  │
                └─────────┘

Key Decisions:
1. Hash Function: MD5/SHA256 → Base62 encoding
2. Storage: SQL (structured) or NoSQL (scale)
3. Read-heavy: Cache hot URLs in Redis
4. Analytics: Async via message queue

Complexity:
- Shorten: O(1)
- Redirect: O(1)
- Storage: O(n)

```

---

### Intermediate (10 Questions)

| # | Question | Core Concepts | Key Components | Time Limit |
|---|----------|---------------|----------------|------------|
| 6 | **Design a Chat System (WhatsApp)** | WebSocket, Message Queue | Presence, Delivery, Encryption | 45 min |
| 7 | **Design a News Feed (Twitter)** | Fan-out, Fan-in | Timeline, Cache, Fan-out Service | 45 min |
| 8 | **Design a Notification System** | Push, SMS, Email | Queue, Priority, Deduplication | 40 min |
| 9 | **Design a Search Autocomplete** | Trie, Ranking | Trie Service, Cache, Analytics | 40 min |
| 10 | **Design a Distributed Cache** | Consistent Hashing | Cache Nodes, Replication, Eviction | 45 min |
| 11 | **Design a File Storage System** | Block Storage, Dedup | Metadata, Chunks, Replication | 45 min |
| 12 | **Design a Video Streaming Service** | CDN, Transcoding | Upload, Process, Stream | 45 min |
| 13 | **Design a Proximity Service** | Geo-spatial, QuadTree | Nearby Search, Distance | 40 min |
| 14 | **Design a Ticket Booking System** | Concurrency, Inventory | Seat Map, Payment, Confirmation | 45 min |
| 15 | **Design a Web Crawler** | BFS/DFS, Politeness | URL Frontier, Parser, Storage | 40 min |

#### Detailed Breakdown: Chat System

```text

Requirements:
- 1:1 and group messaging
- Online/offline presence
- Message delivery status (sent, delivered, read)
- Push notifications
- End-to-end encryption

High-Level Design:
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Client  │◄───▶│  Chat   │◄───▶│ Message │
│ (Mobile) │     │  Server │     │  Queue  │
└─────────┘     └────┬────┘     └────┬────┘
                     │               │
                ┌────▼────┐     ┌────▼────┐
                │ Presence│     │Storage  │
                │ Service │     │Service  │
                └─────────┘     └─────────┘

Key Components:
1. WebSocket Server: Real-time bidirectional
2. Message Queue: Kafka for reliability
3. Presence Service: Redis for online status
4. Storage: Message DB + Cache

Message Flow:
1. User A sends message → Chat Server
2. Chat Server stores in DB
3. Chat Server checks if User B is online
4. If online: Push via WebSocket
5. If offline: Push notification
6. Update delivery status

Consistency:
- Message ordering: Sequence numbers
- Delivery: At-least-once with dedup
- Read receipts: Async processing

```

---

### Advanced (5 Questions)

| # | Question | Core Concepts | Key Components | Time Limit |
|---|----------|---------------|----------------|------------|
| 16 | **Design Google Maps / Uber** | Geo-spatial, Matching | Location Service, Trip Service, Pricing | 60 min |
| 17 | **Design Netflix / YouTube** | Streaming, Recommendation | CDN, Encoding, Recommendation Engine | 60 min |
| 18 | **Design a Search Engine** | Crawling, Indexing, Ranking | Crawler, Indexer, Ranking Algorithm | 60 min |
| 19 | **Design a Distributed Database** | CAP, Sharding, Replication | Partitioning, Consensus, Transactions | 60 min |
| 20 | **Design a Payment System** | Idempotency, Consistency | Payment Gateway, Ledger, Reconciliation | 60 min |

#### Detailed Breakdown: Design Uber/Maps

```text

Requirements:
- Find nearby drivers
- Match rider to driver
- Real-time location tracking
- Dynamic pricing
- Trip management

High-Level Design:
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Rider   │────▶│   API   │◀────│ Driver  │
│  App    │     │ Gateway │     │   App   │
└─────────┘     └────┬────┘     └─────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │Location │  │  Trip   │  │ Pricing │
   │ Service │  │ Service │  │ Service │
   └────┬────┘  └────┬────┘  └─────────┘
        │            │
   ┌────▼────┐  ┌────▼────┐
   │  Geo   │  │  Trip   │
   │  DB    │  │   DB    │
   └─────────┘  └─────────┘

Key Services:
1. Location Service: Stores driver locations
   - GeoHash for spatial indexing
   - Update frequency: Every 3-5 seconds

2. Matching Service:
   - Find nearby drivers (geo query)
   - Score drivers (rating, distance, ETA)
   - Assign trip

3. Pricing Service:
   - Surge pricing based on supply/demand
   - Route-based pricing

Data Storage:
- Redis: Real-time driver locations
- Cassandra: Trip history (write-heavy)
- PostgreSQL: User data, payments

Consistency:
- Location: Eventually consistent (OK)
- Trip state: Strongly consistent
- Payments: Exactly-once

```

---

## 🎭 Behavioral Questions (20)

### Leadership & Growth Mindset (5 Questions)

| # | Question | What They're Assessing | STAR Framework | Tips |
|---|----------|----------------------|----------------|------|
| 1 | Tell me about a time you made a mistake and what you learned. | Growth Mindset, ownership | Describe the mistake, what you did to fix it, what you learned | Be genuine, don't spin it as a success |
| 2 | Describe a time you received critical feedback. How did you respond? | Coachability, self-awareness | Share the feedback, your initial reaction, how you improved | Show you actively seek feedback |
| 3 | Tell me about a time you mentored someone. | Leadership, teaching ability | Describe the mentee, your approach, their growth | Focus on their success, not yours |
| 4 | How do you stay current with new technologies? | Learning agility, curiosity | Give specific examples of learning methods | Show systematic approach to learning |
| 5 | Describe a project where you had to learn something new quickly. | Adaptability, resourcefulness | What you learned, how fast, the outcome | Emphasize speed of learning |

#### Sample Answer: Growth Mindset

```text

Question: Tell me about a time you made a mistake.

Situation: "In my previous role, I deployed a database migration to production
without proper testing, which caused a 30-minute outage."

Task: "I needed to fix the issue immediately and prevent it from happening again."

Action:
1. "I immediately rolled back the migration"
2. "I set up a staging environment that mirrors production"
3. "I implemented a mandatory code review process for migrations"
4. "I created a checklist for all future deployments"

Result:
- "Zero downtime incidents in the next 6 months"
- "Team adopted the process, reducing deployment issues by 80%"
- "I personally learned to never skip testing, no matter how small the change"

Lesson: "This taught me that speed without quality creates more work. Now I
always invest time upfront to save time later."

```

---

### Conflict Resolution (5 Questions)

| # | Question | What They're Assessing | STAR Framework | Tips |
|---|----------|----------------------|----------------|------|
| 6 | Tell me about a time you disagreed with a teammate. | Conflict resolution, communication | Describe the disagreement, how you handled it, the resolution | Show you listen and find common ground |
| 7 | How do you handle disagreements with your manager? | Respect, assertiveness | Give an example where you disagreed but found resolution | Show you can push back respectfully |
| 8 | Describe a situation where you had to convince others of your idea. | Influence, persuasion | What was your idea, how did you convince them, outcome | Focus on data and benefits |
| 9 | Tell me about a time you had to work with a difficult colleague. | Patience, empathy | How you approached it, what worked, relationship now | Show empathy and understanding |
| 10 | How do you handle competing priorities from different stakeholders? | Prioritization, communication | Give an example, how you resolved it | Show you communicate and negotiate |

---

### Technical Challenges (5 Questions)

| # | Question | What They're Assessing | STAR Framework | Tips |
|---|----------|----------------------|----------------|------|
| 11 | Tell me about the most challenging technical problem you've solved. | Problem-solving, persistence | Describe the problem, your approach, the solution | Focus on your thought process |
| 12 | Describe a time you had to make a technical decision with incomplete information. | Judgment, risk assessment | What you decided, why, the outcome | Show you can make reasonable assumptions |
| 13 | Tell me about a time you had to optimize a system for performance. | Technical skills, impact | Before state, what you optimized, measurable results | Quantify the improvement |
| 14 | Describe a project where you had to balance technical debt with feature work. | Prioritization, trade-offs | How you made decisions, the outcome | Show pragmatic approach |
| 15 | Tell me about a time you had to debug a complex issue. | Debugging skills, persistence | The issue, your debugging process, resolution | Emphasize systematic approach |

---

### Customer & Impact (5 Questions)

| # | Question | What They're Assessing | STAR Framework | Tips |
|---|----------|----------------------|----------------|------|
| 16 | Tell me about a time you went above and beyond for a customer/user. | Customer obsession | What you did, why, the impact | Focus on user benefit |
| 17 | Describe a feature you built that had significant impact. | Impact, metrics | What you built, how you measured success | Use specific numbers |
| 18 | How do you prioritize between technical excellence and shipping quickly? | Pragmatism, judgment | Give an example of how you balanced both | Show you understand business needs |
| 19 | Tell me about a time you had to say no to a request. | Assertiveness, prioritization | What you said no to, why, how you communicated it | Show you protect team bandwidth |
| 20 | Why Microsoft? Why this team? | Passion, alignment | Research the team, give specific reasons | Be genuine, show you've done homework |

#### Sample Answer: Why Microsoft?

```text

Question: Why Microsoft?

Answer: "Three reasons:

1. Impact at Scale: Azure serves millions of customers globally, from startups
to enterprises. I want to work on systems that power this scale. Specifically,
the Azure Compute team's work on serverless computing fascinates me because
it's democratizing access to cloud resources.

2. Growth Mindset Culture: Microsoft's culture of learning aligns with how I
approach my career. I've read about Satya Nadella's transformation of the
company, and I want to be part of an organization that values learning over
knowing.

3. Technical Challenge: The distributed systems problems at Azure are unique —
global consistency, fault tolerance, and performance at scale. These are the
kind of problems I want to solve.

I'm particularly excited about [specific team] because [specific reason about
their product/challenges]."

```

---

## 📋 Mock Interview Format

### Coding Mock (45 minutes)

```text

Structure:
├── 0-5 min: Problem clarification
├── 5-10 min: Approach discussion (brute force → optimal)
├── 10-30 min: Implementation
├── 30-40 min: Testing and edge cases
└── 40-45 min: Complexity analysis and follow-ups

What to Practice:
- Talking through your thought process
- Asking clarifying questions
- Starting with brute force
- Writing clean, readable code
- Testing edge cases
- Analyzing time/space complexity

```

### System Design Mock (45-60 minutes)

```text

Structure:
├── 0-5 min: Requirements clarification
├── 5-10 min: Estimation (QPS, storage, bandwidth)
├── 10-25 min: High-level design
├── 25-45 min: Deep dive into components
├── 45-55 min: Bottlenecks and scaling
└── 55-60 min: Wrap-up and trade-offs

What to Practice:
- Drawing clear diagrams
- Discussing trade-offs
- Referencing specific technologies
- Handling scaling questions
- Mentioning monitoring and observability

```

### Behavioral Mock (30-45 minutes)

```text

Structure:
├── 5-10 min: Introduction and background
├── 10-35 min: STAR questions (3-5 questions)
├── 35-40 min: Your questions for interviewer
└── 40-45 min: Wrap-up

What to Practice:
- Telling stories concisely (2 min each)
- Using STAR framework
- Being specific with examples
- Showing self-awareness
- Asking thoughtful questions

```

---

## 📊 Question Difficulty Distribution

| Category | Easy | Medium | Hard | Total |
|----------|------|--------|------|-------|
| Coding | 10 | 25 | 15 | 50 |
| System Design | 5 | 10 | 5 | 20 |
| Behavioral | - | 20 | - | 20 |
| **Total** | **15** | **55** | **20** | **90** |

---

## 🎯 Recommended Mock Schedule

### Week 12: Final Mock Week

| Day | Type | Questions | Duration | Focus |
|-----|------|-----------|----------|-------|
| Mon | Coding | #11 (3Sum) + #29 (Islands) | 45 min | Arrays + Graphs |
| Tue | System Design | #6 (Chat System) | 45 min | Real-time systems |
| Wed | Behavioral | #1, #6, #11, #16, #20 | 30 min | Growth Mindset |
| Thu | Coding | #36 (Rain Water) + #40 (Median) | 45 min | Hard problems |
| Fri | Full Loop | 2 Coding + 1 SD + 1 Behavioral | 3 hours | Interview simulation |
| Sat | Weak Areas | Revisit weak spots | 2 hours | Targeted practice |
| Sun | Rest | Light review only | 1 hour | Mental preparation |

---

> **Pro Tip:** Record your mock interviews and review them. You'll catch filler words, unclear explanations, and missed optimizations that you wouldn't notice in the moment.

> **Remember:** The goal isn't to memorize solutions — it's to practice your thought process and communication. Interviewers care more about HOW you think than whether you get the optimal solution immediately.

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

This question bank provides a comprehensive collection of mock interview questions across coding, system design, and behavioral categories to simulate real interview conditions and practice your responses.

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
