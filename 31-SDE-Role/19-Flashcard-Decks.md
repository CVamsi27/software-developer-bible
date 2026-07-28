---
section: SDE Role
category: Interview
tags: [flashcards]
---

# 🃏 Interactive Flashcard Decks

> **Ready-to-import flashcards for Anki and Quizlet**
>
> Use these for daily active recall practice. Each card tests one key concept.

---

## 📥 How to Import

### Anki Import

```text

1. Copy the Anki-formatted cards below
2. Open Anki → File → Import
3. Paste into a text file with tab separation
4. Import as "Text File"
5. Study daily using Anki's spaced repetition

```

### Quizlet Import

```text

1. Copy the Quizlet-formatted cards below
2. Go to Quizlet.com → Create → Import
3. Paste the cards (term | definition format)
4. Save as a study set
5. Use Quizlet's Learn mode for spaced repetition

```

---

## 📚 Deck 1: Arrays & Strings (30 Cards)

### Anki Format (Front → Back)

```text

Two Pointers: When to use?	When array is sorted OR when finding pairs/triplets with specific condition
Sliding Window: When to use?	When finding subarray/substring of fixed or variable size
Prefix Sum: When to use?	When need range sum queries efficiently
Kadane's Algorithm: Purpose?	Find maximum subarray sum in O(n) time
Dutch National Flag: When to use?	When sorting array with 3 distinct values (0s, 1s, 2s)
Merge Intervals: Algorithm?	Sort by start time, merge overlapping intervals
Two Sum Pattern?	Map<num, index>, check complement (target - num)
Container With Most Water: Approach?	Two pointers from ends, move shorter pointer inward
3Sum: Approach?	Sort array, fix one element, two pointers on rest
Product of Array Except Self?	Left pass for prefix products, right pass for suffix products
Trapping Rain Water: Optimal approach?	Two pointers tracking left_max and right_max
Longest Substring Without Repeating?	Sliding window + HashSet, shrink when duplicate found
Minimum Window Substring?	Expand until valid, shrink to minimize, track with frequency map
Valid Palindrome?	Two pointers from ends, skip non-alphanumeric
Merge Sorted Arrays?	Start from end, compare and place larger element
Sort Colors (Dutch Flag)?	Three pointers: low, mid, high; swap based on value
Subarray Sum Equals K?	Prefix sum + HashMap, count prefix sums
Maximum Subarray (Kadane)?	Track current_sum, reset to 0 if negative, update max
Group Anagrams?	Sorted string as HashMap key
Product of Array Except Self?	Left prefix products × Right suffix products
Two Pointers: Time Complexity?	O(n) time, O(1) space
Sliding Window: Time Complexity?	O(n) time, O(k) space where k is window size
Prefix Sum: Time Complexity?	O(n) build, O(1) query
Kadane's Algorithm: Time Complexity?	O(n) time, O(1) space
Merge Intervals: Time Complexity?	O(n log n) due to sorting
Two Sum: Time Complexity?	O(n) time, O(n) space
Container With Most Water: Time Complexity?	O(n) time, O(1) space
3Sum: Time Complexity?	O(n²) time, O(1) space
Longest Substring: Time Complexity?	O(n) time, O(min(n, m)) space where m is charset
Valid Parentheses: Pattern?	Stack: push opening, pop closing, check match

```

### Quizlet Format (Term | Definition)

```text

Two Pointers: When to use? | When array is sorted OR when finding pairs/triplets with specific condition
Sliding Window: When to use? | When finding subarray/substring of fixed or variable size
Prefix Sum: When to use? | When need range sum queries efficiently
Kadane's Algorithm: Purpose? | Find maximum subarray sum in O(n) time
Dutch National Flag: When to use? | When sorting array with 3 distinct values (0s, 1s, 2s)
Merge Intervals: Algorithm? | Sort by start time, merge overlapping intervals
Two Sum Pattern? | Map<num, index>, check complement (target - num)
Container With Most Water: Approach? | Two pointers from ends, move shorter pointer inward
3Sum: Approach? | Sort array, fix one element, two pointers on rest
Product of Array Except Self? | Left pass for prefix products, right pass for suffix products
Trapping Rain Water: Optimal approach? | Two pointers tracking left_max and right_max
Longest Substring Without Repeating? | Sliding window + HashSet, shrink when duplicate found
Minimum Window Substring? | Expand until valid, shrink to minimize, track with frequency map
Valid Palindrome? | Two pointers from ends, skip non-alphanumeric
Merge Sorted Arrays? | Start from end, compare and place larger element
Sort Colors (Dutch Flag)? | Three pointers: low, mid, high; swap based on value
Subarray Sum Equals K? | Prefix sum + HashMap, count prefix sums
Maximum Subarray (Kadane)? | Track current_sum, reset to 0 if negative, update max
Group Anagrams? | Sorted string as HashMap key
Product of Array Except Self? | Left prefix products × Right suffix products
Two Pointers: Time Complexity? | O(n) time, O(1) space
Sliding Window: Time Complexity? | O(n) time, O(k) space where k is window size
Prefix Sum: Time Complexity? | O(n) build, O(1) query
Kadane's Algorithm: Time Complexity? | O(n) time, O(1) space
Merge Intervals: Time Complexity? | O(n log n) due to sorting
Two Sum: Time Complexity? | O(n) time, O(n) space
Container With Most Water: Time Complexity? | O(n) time, O(1) space
3Sum: Time Complexity? | O(n²) time, O(1) space
Longest Substring: Time Complexity? | O(n) time, O(min(n, m)) space where m is charset
Valid Parentheses: Pattern? | Stack: push opening, pop closing, check match

```

---

## 📚 Deck 2: Trees (30 Cards)

### Anki Format

```text

Preorder Traversal: Order?	Root → Left → Right
Inorder Traversal: Order?	Left → Root → Right (BST = sorted)
Postorder Traversal: Order?	Left → Right → Root
Level Order Traversal: Algorithm?	BFS with Queue, process level by level
DFS (Recursive): Template?	Base case → Process → Recurse left → Recurse right
BFS (Template): Key structure?	Queue, track level size, process each level
BST Property?	Left < Root < Right
Validate BST: Approach?	Inorder traversal should be strictly increasing
LCA (Binary Tree): Algorithm?	Return node if found in left OR right subtree
LCA (BST): Optimization?	Leverage BST property: go left if both < root, right if both > root
Diameter: What to track?	Max path through each node (left_depth + right_depth)
Path Sum: Approach?	Subtract node.val from remaining sum, check at leaf
Serialize Binary Tree?	Preorder with null markers, rebuild using same order
Binary Search Tree Iterator?	Inorder traversal with stack, O(h) space
Maximum Path Sum: Key insight?	Global max tracks best path, return path through current node
Tree Height: Recursive formula?	1 + max(height(left), height(right))
Symmetric Tree?	Compare left subtree with mirrored right subtree
Invert Binary Tree?	Swap children recursively
Binary Tree from Preorder + Inorder?	First preorder = root, find in inorder for left/right subtrees
Balanced Binary Tree?	Height difference ≤ 1 for every node
DFS: Time Complexity?	O(n) time, O(h) space where h is height
BFS: Time Complexity?	O(n) time, O(w) space where w is max width
BST Search: Time Complexity?	O(log n) average, O(n) worst
BST Insert: Time Complexity?	O(log n) average, O(n) worst
Validate BST: Inorder Approach?	Inorder traversal should be strictly increasing
Level Order: Queue Operations?	poll() to process, offer() to add children
Path Sum III: Prefix Sum on Tree?	Run prefix sum from root, check if (current - target) exists
Serialize: delimiter?	Comma-separated values with "null" for empty nodes
Tree Traversal: When Preorder?	When need to process root before children (copy tree)
Tree Traversal: When Inorder?	When need sorted order (BST) or specific processing order

```

### Quizlet Format

```text

Preorder Traversal: Order? | Root → Left → Right
Inorder Traversal: Order? | Left → Root → Right (BST = sorted)
Postorder Traversal: Order? | Left → Right → Root
Level Order Traversal: Algorithm? | BFS with Queue, process level by level
DFS (Recursive): Template? | Base case → Process → Recurse left → Recurse right
BFS (Template): Key structure? | Queue, track level size, process each level
BST Property? | Left < Root < Right
Validate BST: Approach? | Inorder traversal should be strictly increasing
LCA (Binary Tree): Algorithm? | Return node if found in left OR right subtree
LCA (BST): Optimization? | Leverage BST property: go left if both < root, right if both > root
Diameter: What to track? | Max path through each node (left_depth + right_depth)
Path Sum: Approach? | Subtract node.val from remaining sum, check at leaf
Serialize Binary Tree? | Preorder with null markers, rebuild using same order
Binary Search Tree Iterator? | Inorder traversal with stack, O(h) space
Maximum Path Sum: Key insight? | Global max tracks best path, return path through current node
Tree Height: Recursive formula? | 1 + max(height(left), height(right))
Symmetric Tree? | Compare left subtree with mirrored right subtree
Invert Binary Tree? | Swap children recursively
Binary Tree from Preorder + Inorder? | First preorder = root, find in inorder for left/right subtrees
Balanced Binary Tree? | Height difference ≤ 1 for every node
DFS: Time Complexity? | O(n) time, O(h) space where h is height
BFS: Time Complexity? | O(n) time, O(w) space where w is max width
BST Search: Time Complexity? | O(log n) average, O(n) worst
BST Insert: Time Complexity? | O(log n) average, O(n) worst
Validate BST: Inorder Approach? | Inorder traversal should be strictly increasing
Level Order: Queue Operations? | poll() to process, offer() to add children
Path Sum III: Prefix Sum on Tree? | Run prefix sum from root, check if (current - target) exists
Serialize: delimiter? | Comma-separated values with "null" for empty nodes
Tree Traversal: When Preorder? | When need to process root before children (copy tree)
Tree Traversal: When Inorder? | When need sorted order (BST) or specific processing order

```

---

## 📚 Deck 3: Graphs (30 Cards)

### Anki Format

```text

DFS (Graph): Algorithm?	Recursive or stack, mark visited
BFS (Graph): Algorithm?	Queue, mark visited when enqueuing
Topological Sort: When to use?	When need linear ordering of DAG (prerequisites, build order)
Kahn's Algorithm?	BFS-based topological sort using in-degree
DFS Cycle Detection (Directed)?	Track: unvisited → visiting → visited, cycle if revisit "visiting"
DFS Cycle Detection (Undirected)?	Track parent, cycle if neighbor visited and not parent
Union-Find: Purpose?	Track connected components, detect cycles
Union-Find: Optimizations?	Path compression + union by rank
Dijkstra: When to use?	Shortest path with non-negative weights
Bellman-Ford: When to use?	Shortest path with negative weights, detect negative cycles
Floyd-Warshall: When to use?	All-pairs shortest path
MST (Prim): Algorithm?	Greedy: always add cheapest edge from MST to non-MST
MST (Kruskal): Algorithm?	Sort edges, add if no cycle (use Union-Find)
Bipartite Graph: Check?	2-coloring with BFS/DFS, conflict = not bipartite
Strongly Connected Components?	Kosaraju's or Tarjan's algorithm
Graph Representation: Adjacency List?	Map<Integer, List<Integer>> or List<List<Integer>>
Graph Representation: Adjacency Matrix?	int[][] graph, O(V²) space
BFS Shortest Path (Unweighted)?	BFS naturally finds shortest path
Weighted Shortest Path?	Dijkstra (non-negative) or Bellman-Ford (negative)
Cycle in Directed Graph?	DFS with 3 states or Kahn's (in-degree)
Cycle in Undirected Graph?	DFS with parent tracking or Union-Find
Connected Components?	DFS/BFS from each unvisited node, or Union-Find
Bipartite: 2-coloring?	Assign alternating colors, conflict = not bipartite
Dijkstra: Data Structure?	Min-heap priority queue
Bellman-Ford: Time Complexity?	O(V × E)
Dijkstra: Time Complexity?	O((V + E) log V) with min-heap
Topological Sort: Time Complexity?	O(V + E)
BFS: Time Complexity?	O(V + E)
DFS: Time Complexity?	O(V + E)
Union-Find: Time Complexity?	O(α(n)) amortized (nearly constant)
Kruskal's: Time Complexity?	O(E log E)

```

### Quizlet Format

```text

DFS (Graph): Algorithm? | Recursive or stack, mark visited
BFS (Graph): Algorithm? | Queue, mark visited when enqueuing
Topological Sort: When to use? | When need linear ordering of DAG (prerequisites, build order)
Kahn's Algorithm? | BFS-based topological sort using in-degree
DFS Cycle Detection (Directed)? | Track: unvisited → visiting → visited, cycle if revisit "visiting"
DFS Cycle Detection (Undirected)? | Track parent, cycle if neighbor visited and not parent
Union-Find: Purpose? | Track connected components, detect cycles
Union-Find: Optimizations? | Path compression + union by rank
Dijkstra: When to use? | Shortest path with non-negative weights
Bellman-Ford: When to use? | Shortest path with negative weights, detect negative cycles
Floyd-Warshall: When to use? | All-pairs shortest path
MST (Prim): Algorithm? | Greedy: always add cheapest edge from MST to non-MST
MST (Kruskal): Algorithm? | Sort edges, add if no cycle (use Union-Find)
Bipartite Graph: Check? | 2-coloring with BFS/DFS, conflict = not bipartite
Strongly Connected Components? | Kosaraju's or Tarjan's algorithm
Graph Representation: Adjacency List? | Map<Integer, List<Integer>> or List<List<Integer>>
Graph Representation: Adjacency Matrix? | int[][] graph, O(V²) space
BFS Shortest Path (Unweighted)? | BFS naturally finds shortest path
Weighted Shortest Path? | Dijkstra (non-negative) or Bellman-Ford (negative)
Cycle in Directed Graph? | DFS with 3 states or Kahn's (in-degree)
Cycle in Undirected Graph? | DFS with parent tracking or Union-Find
Connected Components? | DFS/BFS from each unvisited node, or Union-Find
Bipartite: 2-coloring? | Assign alternating colors, conflict = not bipartite
Dijkstra: Data Structure? | Min-heap priority queue
Bellman-Ford: Time Complexity? | O(V × E)
Dijkstra: Time Complexity? | O((V + E) log V) with min-heap
Topological Sort: Time Complexity? | O(V + E)
BFS: Time Complexity? | O(V + E)
DFS: Time Complexity? | O(V + E)
Union-Find: Time Complexity? | O(α(n)) amortized (nearly constant)
Kruskal's: Time Complexity? | O(E log E)

```

---

## 📚 Deck 4: Dynamic Programming (30 Cards)

### Anki Format

```text

DP Core Idea?	Solve overlapping subproblems, store results
Memoization?	Top-down: recursive + cache (HashMap/Array)
Tabulation?	Bottom-up: iterative, fill table from base cases
State Definition?	What does dp[i] or dp[i][j] represent?
Recurrence Relation?	How does current state relate to previous states?
Base Case?	When do we stop? Usually dp[0] or dp[1]
Space Optimization?	If dp[i] only uses dp[i-1] and dp[i-2], use two variables
0/1 Knapsack Recurrence?	dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])
Unbounded Knapsack?	Like 0/1 but can reuse items: dp[i] = max(include, exclude)
LIS Recurrence?	dp[i] = 1 + max(dp[j]) for all j < i where arr[j] < arr[i]
LCS Recurrence?	dp[i][j] = dp[i-1][j-1]+1 if match, else max(dp[i-1][j], dp[i][j-1])
Coin Change Recurrence?	dp[amount] = min(dp[amount], dp[amount-coin]+1)
Edit Distance Recurrence?	dp[i][j] = min(insert, delete, replace)
Grid DP: Unique Paths?	dp[i][j] = dp[i-1][j] + dp[i][j-1]
Interval DP: Burst Balloons?	dp[i][j] = max(dp[i][k-1] + dp[k+1][j] + nums[i]*nums[k]*nums[j])
Fibonacci: Optimal?	Two variables instead of array: O(1) space
House Robber: Recurrence?	dp[i] = max(dp[i-1], dp[i-2] + nums[i])
Climbing Stairs: Same as?	Fibonacci: dp[i] = dp[i-1] + dp[i-2]
Word Break: Approach?	dp[i] = true if any word matches ending at i
Decode Ways: Recurrence?	dp[i] = dp[i-1] (if valid) + dp[i-2] (if valid 2-digit)
Maximum Product Subarray?	Track both min and max at each position
Longest Palindromic Substring?	Expand around center OR 2D DP
DP Time Complexity?	O(n × m) for 2D, O(n) for 1D, O(n²) for interval
DP Space Complexity?	O(n × m) for 2D, O(1) optimized, O(n) for 1D
When to use DP?	1. Optimal substructure 2. Overlapping subproblems
When NOT to use DP?	No optimal substructure OR no overlapping subproblems
Top-Down vs Bottom-Up?	Top-down: easier to write, Bottom-up: better space
Knapsack: When to use?	When need to maximize value with constraint (weight, capacity)
LIS: O(n²) vs O(n log n)?	Binary search optimization: patience sorting
DP: Common mistakes?	Wrong base case, wrong order of filling, missing cases

```

### Quizlet Format

```text

DP Core Idea? | Solve overlapping subproblems, store results
Memoization? | Top-down: recursive + cache (HashMap/Array)
Tabulation? | Bottom-up: iterative, fill table from base cases
State Definition? | What does dp[i] or dp[i][j] represent?
Recurrence Relation? | How does current state relate to previous states?
Base Case? | When do we stop? Usually dp[0] or dp[1]
Space Optimization? | If dp[i] only uses dp[i-1] and dp[i-2], use two variables
0/1 Knapsack Recurrence? | dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])
Unbounded Knapsack? | Like 0/1 but can reuse items: dp[i] = max(include, exclude)
LIS Recurrence? | dp[i] = 1 + max(dp[j]) for all j < i where arr[j] < arr[i]
LCS Recurrence? | dp[i][j] = dp[i-1][j-1]+1 if match, else max(dp[i-1][j], dp[i][j-1])
Coin Change Recurrence? | dp[amount] = min(dp[amount], dp[amount-coin]+1)
Edit Distance Recurrence? | dp[i][j] = min(insert, delete, replace)
Grid DP: Unique Paths? | dp[i][j] = dp[i-1][j] + dp[i][j-1]
Interval DP: Burst Balloons? | dp[i][j] = max(dp[i][k-1] + dp[k+1][j] + nums[i]*nums[k]*nums[j])
Fibonacci: Optimal? | Two variables instead of array: O(1) space
House Robber: Recurrence? | dp[i] = max(dp[i-1], dp[i-2] + nums[i])
Climbing Stairs: Same as? | Fibonacci: dp[i] = dp[i-1] + dp[i-2]
Word Break: Approach? | dp[i] = true if any word matches ending at i
Decode Ways: Recurrence? | dp[i] = dp[i-1] (if valid) + dp[i-2] (if valid 2-digit)
Maximum Product Subarray? | Track both min and max at each position
Longest Palindromic Substring? | Expand around center OR 2D DP
DP Time Complexity? | O(n × m) for 2D, O(n) for 1D, O(n²) for interval
DP Space Complexity? | O(n × m) for 2D, O(1) optimized, O(n) for 1D
When to use DP? | 1. Optimal substructure 2. Overlapping subproblems
When NOT to use DP? | No optimal substructure OR no overlapping subproblems
Top-Down vs Bottom-Up? | Top-down: easier to write, Bottom-up: better space
Knapsack: When to use? | When need to maximize value with constraint (weight, capacity)
LIS: O(n²) vs O(n log n)? | Binary search optimization: patience sorting
DP: Common mistakes? | Wrong base case, wrong order of filling, missing cases

```

---

## 📚 Deck 5: System Design (30 Cards)

### Anki Format

```text

System Design Framework?	1. Requirements 2. Estimation 3. High-Level 4. Deep Dive 5. Wrap-up
Functional Requirements?	What the system should do (features)
Non-Functional Requirements?	Scale, latency, availability, consistency, cost
Horizontal Scaling?	Add more machines (preferred)
Vertical Scaling?	Get bigger machine (limited)
Sharding?	Split data across multiple databases
Replication?	Copy data for redundancy and read scaling
Load Balancer?	Distributes traffic across servers (NGINX, ALB)
CDN?	Caches static content closer to users
Cache?	Stores frequently accessed data in memory (Redis)
Message Queue?	Async communication between services (Kafka, SQS)
SQL vs NoSQL?	SQL: ACID, joins. NoSQL: scale, flexibility
CAP Theorem?	Consistency, Availability, Partition Tolerance - pick 2
Consistency Models?	Strong, Eventual, Causal, Read-your-writes
API Gateway?	Single entry point for all client requests
Microservices?	Independent deployable services
Monolith?	Single codebase, easier to develop initially
CQRS?	Separate read and write models
Event Sourcing?	Store events, not current state
Circuit Breaker?	Prevent cascade failures
Rate Limiting?	Limit requests per user/time period
Consistent Hashing?	Distribute data evenly across nodes
Database Indexing?	B-tree for range, hash for equality
Connection Pooling?	Reuse database connections
Health Checks?	Monitor service availability
Observability?	Logs, Metrics, Traces (three pillars)
Scalability Patterns?	Vertical, Horizontal, Sharding, Caching
Availability Target?	99.9% = 8.76 hours/year downtime
Latency Targets?	p95 < 200ms, p99 < 500ms
Cost Optimization?	Reserved instances, spot instances, right-sizing

```

### Quizlet Format

```text

System Design Framework? | 1. Requirements 2. Estimation 3. High-Level 4. Deep Dive 5. Wrap-up
Functional Requirements? | What the system should do (features)
Non-Functional Requirements? | Scale, latency, availability, consistency, cost
Horizontal Scaling? | Add more machines (preferred)
Vertical Scaling? | Get bigger machine (limited)
Sharding? | Split data across multiple databases
Replication? | Copy data for redundancy and read scaling
Load Balancer? | Distributes traffic across servers (NGINX, ALB)
CDN? | Caches static content closer to users
Cache? | Stores frequently accessed data in memory (Redis)
Message Queue? | Async communication between services (Kafka, SQS)
SQL vs NoSQL? | SQL: ACID, joins. NoSQL: scale, flexibility
CAP Theorem? | Consistency, Availability, Partition Tolerance - pick 2
Consistency Models? | Strong, Eventual, Causal, Read-your-writes
API Gateway? | Single entry point for all client requests
Microservices? | Independent deployable services
Monolith? | Single codebase, easier to develop initially
CQRS? | Separate read and write models
Event Sourcing? | Store events, not current state
Circuit Breaker? | Prevent cascade failures
Rate Limiting? | Limit requests per user/time period
Consistent Hashing? | Distribute data evenly across nodes
Database Indexing? | B-tree for range, hash for equality
Connection Pooling? | Reuse database connections
Health Checks? | Monitor service availability
Observability? | Logs, Metrics, Traces (three pillars)
Scalability Patterns? | Vertical, Horizontal, Sharding, Caching
Availability Target? | 99.9% = 8.76 hours/year downtime
Latency Targets? | p95 < 200ms, p99 < 500ms
Cost Optimization? | Reserved instances, spot instances, right-sizing

```

---

## 📚 Deck 6: Linked Lists & Stacks (30 Cards)

### Anki Format

```text

Reverse Linked List: Approach?	Iterative: track prev, curr, next; reverse pointer
Reverse Linked List: Recursive?	Base case → recurse → reverse pointer
Detect Cycle (Floyd)?	Slow and fast pointers, cycle if they meet
Find Cycle Start?	Move slow to head, advance both one step at a time
Merge Two Sorted Lists?	Dummy node, compare and attach smaller
Remove Nth From End?	Two pointers with n gap
LRU Cache: Data Structure?	HashMap + Doubly Linked List
LRU Cache: Get Operation?	O(1) - lookup in map, move to front of list
LRU Cache: Put Operation?	O(1) - add to front, evict from back if full
Valid Parentheses?	Stack: push opening, pop closing, check match
Min Stack?	Auxiliary stack tracking minimum at each level
Monotonic Stack: When to use?	When need next greater/lesser element efficiently
Evaluate Reverse Polish Notation?	Stack: push numbers, pop two on operator
Decode String: Approach?	Two stacks: one for numbers, one for strings
Basic Calculator?	Stack for results and signs
Implement Queue using Stacks?	Two stacks, amortized O(1) enqueue
Linked List: Time Complexity?	Access: O(n), Search: O(n), Insert: O(1) at head
Stack: Time Complexity?	Push: O(1), Pop: O(1), Peek: O(1)
Linked List vs Array?	LL: O(1) insert, O(n) access. Array: O(1) access, O(n) insert
Doubly Linked List?	Node has prev and next pointers
Circular Linked List?	Last node points back to head
Fast/Slow Pointer: When to use?	Cycle detection, middle of list, palindrome check
Dummy Node: When to use?	When head might change (merge, remove)
Monotonic Decreasing Stack?	Maintain decreasing order, pop when smaller found
Monotonic Increasing Stack?	Maintain increasing order, pop when larger found
Stack Applications?	Parentheses, undo, DFS, evaluation, monotonic
Queue Applications?	BFS, scheduling, buffering, printer
Priority Queue?	Heap-based, O(log n) insert/extract
Linked List Cycle II: Algorithm?	Floyd's: find meeting point, then find cycle start
LRU Cache: Eviction Policy?	Least Recently Used - remove from back of list

```

### Quizlet Format

```text

Reverse Linked List: Approach? | Iterative: track prev, curr, next; reverse pointer
Reverse Linked List: Recursive? | Base case → recurse → reverse pointer
Detect Cycle (Floyd)? | Slow and fast pointers, cycle if they meet
Find Cycle Start? | Move slow to head, advance both one step at a time
Merge Two Sorted Lists? | Dummy node, compare and attach smaller
Remove Nth From End? | Two pointers with n gap
LRU Cache: Data Structure? | HashMap + Doubly Linked List
LRU Cache: Get Operation? | O(1) - lookup in map, move to front of list
LRU Cache: Put Operation? | O(1) - add to front, evict from back if full
Valid Parentheses? | Stack: push opening, pop closing, check match
Min Stack? | Auxiliary stack tracking minimum at each level
Monotonic Stack: When to use? | When need next greater/lesser element efficiently
Evaluate Reverse Polish Notation? | Stack: push numbers, pop two on operator
Decode String: Approach? | Two stacks: one for numbers, one for strings
Basic Calculator? | Stack for results and signs
Implement Queue using Stacks? | Two stacks, amortized O(1) enqueue
Linked List: Time Complexity? | Access: O(n), Search: O(n), Insert: O(1) at head
Stack: Time Complexity? | Push: O(1), Pop: O(1), Peek: O(1)
Linked List vs Array? | LL: O(1) insert, O(n) access. Array: O(1) access, O(n) insert
Doubly Linked List? | Node has prev and next pointers
Circular Linked List? | Last node points back to head
Fast/Slow Pointer: When to use? | Cycle detection, middle of list, palindrome check
Dummy Node: When to use? | When head might change (merge, remove)
Monotonic Decreasing Stack? | Maintain decreasing order, pop when smaller found
Monotonic Increasing Stack? | Maintain increasing order, pop when larger found
Stack Applications? | Parentheses, undo, DFS, evaluation, monotonic
Queue Applications? | BFS, scheduling, buffering, printer
Priority Queue? | Heap-based, O(log n) insert/extract
Linked List Cycle II: Algorithm? | Floyd's: find meeting point, then find cycle start
LRU Cache: Eviction Policy? | Least Recently Used - remove from back of list

```

---

## 📚 Deck 7: Hash Maps & Heaps (30 Cards)

### Anki Format

```text

HashMap: When to use?	O(1) lookup, frequency counting, grouping
Two Sum Pattern?	Map<num, index>, check complement
Frequency Count?	Map<num, count>, iterate and count
Grouping Pattern?	Map<key, list>, group by sorted/transformed key
Anagram Pattern?	Map<sorted_string, list>
Subarray Sum K?	Map<prefix_sum, count>
Top K Elements?	Min heap of size K
Merge K Sorted Lists?	Min heap of K pointers
Find Median?	Max heap (lower) + Min heap (upper)
Task Scheduling?	Greedy + heap for frequency
LRU Cache?	HashMap + Doubly Linked List
HashMap: Collision Handling?	Chaining (linked list) or open addressing
HashMap: Load Factor?	Resize when load factor > 0.75
Heap: Insert?	Add to end, bubble up (sift up)
Heap: Extract Min/Max?	Replace root with last, bubble down (sift down)
Heap: Build Heap?	O(n) using bottom-up approach
Min Heap Property?	Parent ≤ children
Max Heap Property?	Parent ≥ children
Priority Queue: Java?	PriorityQueue<Integer> minHeap = new PriorityQueue<>();
Max Heap: Java?	PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
Top K: Algorithm?	Maintain min heap of size K, offer and poll
Median: Algorithm?	Max heap for lower half, Min heap for upper half
HashMap: Time Complexity?	Average O(1), Worst O(n)
Heap: Insert Time?	O(log n)
Heap: Extract Time?	O(log n)
Heap: Peek Time?	O(1)
Heap: Build Time?	O(n)
Top K: Time Complexity?	O(n log k)
Merge K Lists: Time Complexity?	O(N log k) where N = total nodes
Median: Time Complexity?	O(log n) insert, O(1) find median

```

### Quizlet Format

```text

HashMap: When to use? | O(1) lookup, frequency counting, grouping
Two Sum Pattern? | Map<num, index>, check complement
Frequency Count? | Map<num, count>, iterate and count
Grouping Pattern? | Map<key, list>, group by sorted/transformed key
Anagram Pattern? | Map<sorted_string, list>
Subarray Sum K? | Map<prefix_sum, count>
Top K Elements? | Min heap of size K
Merge K Sorted Lists? | Min heap of K pointers
Find Median? | Max heap (lower) + Min heap (upper)
Task Scheduling? | Greedy + heap for frequency
LRU Cache? | HashMap + Doubly Linked List
HashMap: Collision Handling? | Chaining (linked list) or open addressing
HashMap: Load Factor? | Resize when load factor > 0.75
Heap: Insert? | Add to end, bubble up (sift up)
Heap: Extract Min/Max? | Replace root with last, bubble down (sift down)
Heap: Build Heap? | O(n) using bottom-up approach
Min Heap Property? | Parent ≤ children
Max Heap Property? | Parent ≥ children
Priority Queue: Java? | PriorityQueue<Integer> minHeap = new PriorityQueue<>();
Max Heap: Java? | PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
Top K: Algorithm? | Maintain min heap of size K, offer and poll
Median: Algorithm? | Max heap for lower half, Min heap for upper half
HashMap: Time Complexity? | Average O(1), Worst O(n)
Heap: Insert Time? | O(log n)
Heap: Extract Time? | O(log n)
Heap: Peek Time? | O(1)
Heap: Build Time? | O(n)
Top K: Time Complexity? | O(n log k)
Merge K Lists: Time Complexity? | O(N log k) where N = total nodes
Median: Time Complexity? | O(log n) insert, O(1) find median

```

---

## 📚 Deck 8: Binary Search & Sorting (30 Cards)

### Anki Format

```text

Binary Search: When to use?	Sorted array, find specific value or boundary
Binary Search Template?	left=0, right=n-1, while left<=right, mid calculation
Lower Bound?	Find first position ≥ target
Upper Bound?	Find first position > target
Search on Answer?	Binary search on possible answer range, check if feasible
Rotated Array Search?	Find which half is sorted, search accordingly
Binary Search: Time?	O(log n)
Binary Search: Space?	O(1) iterative, O(log n) recursive
Bubble Sort: Time?	O(n²) average, O(n) best
Insertion Sort: Time?	O(n²) average, O(n) best
Merge Sort: Time?	O(n log n) all cases
Quick Sort: Time?	O(n log n) average, O(n²) worst
Heap Sort: Time?	O(n log n)
Merge Sort: Space?	O(n) for temporary arrays
Quick Sort: Space?	O(log n) for recursion
When to use Merge Sort?	When need stable sort or guaranteed O(n log n)
When to use Quick Sort?	When average case matters, in-place preferred
When to use Insertion Sort?	Small arrays or nearly sorted
Binary Search on Answer: Template?	left=min, right=max, while left<right, check feasibility
Koko Eating Bananas?	Binary search on eating speed k
Capacity to Ship Packages?	Binary search on capacity
Split Array Largest Sum?	Binary search on maximum subarray sum
Find Minimum in Rotated?	Binary search, compare mid with right
Search in Rotated Array?	Binary search, identify sorted half
Matrix Search (2D)?	Row binary search OR staircase from top-right
Median Two Arrays?	Binary search on partition, ensure equal halves
Random Pick with Weight?	Prefix sum + binary search on cumulative weights
Binary Search: Common mistakes?	Off-by-one, infinite loop, wrong boundary
Binary Search: left=mid+1?	When arr[mid] < target, search right half
Binary Search: right=mid-1?	When arr[mid] > target, search left half

```

### Quizlet Format

```text

Binary Search: When to use? | Sorted array, find specific value or boundary
Binary Search Template? | left=0, right=n-1, while left<=right, mid calculation
Lower Bound? | Find first position ≥ target
Upper Bound? | Find first position > target
Search on Answer? | Binary search on possible answer range, check if feasible
Rotated Array Search? | Find which half is sorted, search accordingly
Binary Search: Time? | O(log n)
Binary Search: Space? | O(1) iterative, O(log n) recursive
Bubble Sort: Time? | O(n²) average, O(n) best
Insertion Sort: Time? | O(n²) average, O(n) best
Merge Sort: Time? | O(n log n) all cases
Quick Sort: Time? | O(n log n) average, O(n²) worst
Heap Sort: Time? | O(n log n)
Merge Sort: Space? | O(n) for temporary arrays
Quick Sort: Space? | O(log n) for recursion
When to use Merge Sort? | When need stable sort or guaranteed O(n log n)
When to use Quick Sort? | When average case matters, in-place preferred
When to use Insertion Sort? | Small arrays or nearly sorted
Binary Search on Answer: Template? | left=min, right=max, while left<right, check feasibility
Koko Eating Bananas? | Binary search on eating speed k
Capacity to Ship Packages? | Binary search on capacity
Split Array Largest Sum? | Binary search on maximum subarray sum
Find Minimum in Rotated? | Binary search, compare mid with right
Search in Rotated Array? | Binary search, identify sorted half
Matrix Search (2D)? | Row binary search OR staircase from top-right
Median Two Arrays? | Binary search on partition, ensure equal halves
Random Pick with Weight? | Prefix sum + binary search on cumulative weights
Binary Search: Common mistakes? | Off-by-one, infinite loop, wrong boundary
Binary Search: left=mid+1? | When arr[mid] < target, search right half
Binary Search: right=mid-1? | When arr[mid] > target, search left half

```

---

## 📖 How to Use These Flashcards

### Daily Routine

```text

Morning (10 min):
- Review 10-15 cards from yesterday
- Mark "Hard" cards for more frequent review

Evening (10 min):
- Review 10-15 cards from today
- Add new cards from problems solved

```

### Weekly Review

```text

Saturday (30 min):
- Review all "Hard" cards
- Test yourself on templates without looking
- Add cards for any new concepts learned

```

### Anki Settings

```text

New cards/day: 20
Reviews/day: 100
Learning steps: 1m 10m
Graduating interval: 1 day
Easy interval: 4 days

```

### Quizlet Settings

```text

Learn mode: Enable spaced repetition
Write mode: Practice writing answers
Match mode: Quick recall games
Test mode: Simulate exam conditions

```

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Quick Reference Cards](17-Quick-Reference-Cards.md) | One-page summaries for each topic |
| [Spaced Repetition Schedule](15-Spaced-Repetition-Schedule.md) | Review intervals for optimal retention |
| [Learning Guarantee System](18-Learning-Guarantee-System.md) | Active recall and mastery criteria |
| [Cheat Sheet](07-Cheat-Sheet.md) | Last-minute review for all 28 phases |
---


## Summary

These flashcard decks provide 240+ cards across 8 topics for Anki and Quizlet, covering core CS concepts, design patterns, system design, behavioral questions, and more to support active recall study.

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
