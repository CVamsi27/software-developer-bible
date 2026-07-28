# 📋 Quick Reference Cards

[![Category: Interview](https://img.shields.io/badge/category-Interview-1f7a8a)](.)

sk. Review before mock interviews.

---

## 🃏 Card 1: Arrays & Strings

```text

┌─────────────────────────────────────────────────────────────────┐
│  ARRAYS & STRINGS — Quick Reference                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PATTERNS:                                                      │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ Two Pointers    │ Opposite ends, same direction        │    │
│  │ Sliding Window  │ Fixed/variable size window           │    │
│  │ Prefix Sum      │ Running sum for range queries        │    │
│  │ Kadane's        │ Max subarray sum                     │    │
│  │ Dutch Flag      │ 3-way partition (sort colors)        │    │
│  │ Merge Intervals │ Sort by start, merge overlaps        │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  TEMPLATES:                                                     │
│                                                                 │
│  // Two Pointers                                                │
│  int left = 0, right = n - 1;                                  │
│  while (left < right) {                                        │
│      if (condition) left++;                                    │
│      else right--;                                             │
│  }                                                              │
│                                                                 │
│  // Sliding Window                                              │
│  int left = 0;                                                  │
│  for (int right = 0; right < n; right++) {                     │
│      // add arr[right] to window                               │
│      while (window_invalid) {                                  │
│          // remove arr[left] from window                       │
│          left++;                                               │
│      }                                                          │
│      // update answer                                          │
│  }                                                              │
│                                                                 │
│  // Prefix Sum                                                  │
│  int[] prefix = new int[n+1];                                  │
│  for (int i = 0; i < n; i++)                                   │
│      prefix[i+1] = prefix[i] + arr[i];                        │
│  // range sum [l, r] = prefix[r+1] - prefix[l]                │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Two Sum (#1)          • 3Sum (#15)                          │
│  • Container Water (#11) • Trapping Rain (#42)                 │
│  • Merge Intervals (#56) • Product Array (#238)                │
│  • Max Subarray (#53)    • Sort Colors (#75)                   │
│                                                                 │
│  COMPLEXITY CHEAT:                                              │
│  • Access: O(1)  • Search: O(n)  • Insert: O(n)               │
│  • Delete: O(n)  • Space: O(1) for in-place                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 2: Trees

```text

┌─────────────────────────────────────────────────────────────────┐
│  TREES — Quick Reference                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TRAVERSALS:                                                    │
│  ┌──────────────┬───────────────────────────────────────┐      │
│  │ Preorder     │ Root → Left → Right (copy tree)       │      │
│  │ Inorder      │ Left → Root → Right (BST sorted)      │      │
│  │ Postorder    │ Left → Right → Root (delete tree)     │      │
│  │ Level Order  │ BFS with queue (level by level)       │      │
│  └──────────────┴───────────────────────────────────────┘      │
│                                                                 │
│  TEMPLATES:                                                     │
│                                                                 │
│  // DFS (Recursive)                                             │
│  void dfs(TreeNode node) {                                     │
│      if (node == null) return;                                 │
│      // process node (preorder)                                │
│      dfs(node.left);                                           │
│      // process node (inorder)                                 │
│      dfs(node.right);                                          │
│      // process node (postorder)                               │
│  }                                                              │
│                                                                 │
│  // BFS (Level Order)                                           │
│  Queue<TreeNode> queue = new LinkedList<>();                   │
│  queue.offer(root);                                             │
│  while (!queue.isEmpty()) {                                     │
│      int size = queue.size();                                  │
│      for (int i = 0; i < size; i++) {                          │
│          TreeNode node = queue.poll();                         │
│          // process node                                       │
│          if (node.left != null) queue.offer(node.left);        │
│          if (node.right != null) queue.offer(node.right);      │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  // BST Validation                                              │
│  boolean validate(TreeNode node, long min, long max) {         │
│      if (node == null) return true;                            │
│      if (node.val <= min || node.val >= max) return false;     │
│      return validate(node.left, min, node.val)                 │
│          && validate(node.right, node.val, max);               │
│  }                                                              │
│                                                                 │
│  KEY PATTERNS:                                                  │
│  • LCA: Return node if found in left OR right subtree         │
│  • Diameter: Track max path through each node                  │
│  • Path Sum: Subtract node.val from remaining sum              │
│  • Serialization: Preorder with null markers                   │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Max Depth (#104)     • LCA (#236)                          │
│  • Validate BST (#98)   • Level Order (#102)                   │
│  • Serialize (#297)     • Path Sum (#437)                      │
│  • Diameter (#543)      • BST Iterator (#173)                  │
│                                                                 │
│  BST PROPERTY: Left < Root < Right                             │
│  Inorder traversal of BST = Sorted array                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 3: Graphs

```text

┌─────────────────────────────────────────────────────────────────┐
│  GRAPHS — Quick Reference                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  REPRESENTATIONS:                                               │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ Adjacency List  │ Map<Integer, List<Integer>>          │    │
│  │ Adjacency Matrix│ int[][] graph                        │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  TEMPLATES:                                                     │
│                                                                 │
│  // DFS (Recursive)                                             │
│  Set<Integer> visited = new HashSet<>();                       │
│  void dfs(int node, Map<Integer, List<Integer>> graph) {       │
│      if (visited.contains(node)) return;                       │
│      visited.add(node);                                        │
│      for (int neighbor : graph.get(node)) {                    │
│          dfs(neighbor, graph);                                 │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  // BFS (Shortest Path)                                         │
│  Queue<Integer> queue = new LinkedList<>();                    │
│  Map<Integer, Integer> distance = new HashMap<>();             │
│  queue.offer(start);                                            │
│  distance.put(start, 0);                                       │
│  while (!queue.isEmpty()) {                                     │
│      int node = queue.poll();                                  │
│      for (int neighbor : graph.get(node)) {                    │
│          if (!distance.containsKey(neighbor)) {                │
│              distance.put(neighbor, distance.get(node) + 1);   │
│              queue.offer(neighbor);                            │
│          }                                                      │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  // Topological Sort (Kahn's Algorithm)                         │
│  int[] inDegree = new int[n];                                  │
│  Queue<Integer> queue = new LinkedList<>();                    │
│  for (int i = 0; i < n; i++)                                   │
│      if (inDegree[i] == 0) queue.offer(i);                    │
│  List<Integer> order = new ArrayList<>();                      │
│  while (!queue.isEmpty()) {                                     │
│      int node = queue.poll();                                  │
│      order.add(node);                                          │
│      for (int neighbor : graph.get(node)) {                    │
│          if (--inDegree[neighbor] == 0)                        │
│              queue.offer(neighbor);                            │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  KEY ALGORITHMS:                                                │
│  • Dijkstra: Shortest path (non-negative weights)              │
│  • Bellman-Ford: Shortest path (negative weights)              │
│  • Union-Find: Connected components                            │
│  • Topological Sort: DAG ordering                              │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Number of Islands (#200) • Course Schedule (#207)           │
│  • Clone Graph (#133)       • Pacific Atlantic (#417)          │
│  • Network Delay (#743)     • Redundant Connection (#684)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 4: Dynamic Programming

```text

┌─────────────────────────────────────────────────────────────────┐
│  DYNAMIC PROGRAMMING — Quick Reference                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  3 STEPS TO SOLVE:                                              │
│  1. Define State: What are we tracking?                        │
│  2. Recurrence: How do subproblems relate?                     │
│  3. Base Case: When do we stop?                                │
│                                                                 │
│  TEMPLATES:                                                     │
│                                                                 │
│  // Memoization (Top-Down)                                      │
│  Map<Integer, Integer> memo = new HashMap<>();                 │
│  int dp(int n) {                                                │
│      if (n <= 1) return n;  // base case                       │
│      if (memo.containsKey(n)) return memo.get(n);              │
│      int result = dp(n-1) + dp(n-2);  // recurrence           │
│      memo.put(n, result);                                      │
│      return result;                                            │
│  }                                                              │
│                                                                 │
│  // Tabulation (Bottom-Up)                                      │
│  int[] dp = new int[n+1];                                      │
│  dp[0] = 0; dp[1] = 1;  // base cases                         │
│  for (int i = 2; i <= n; i++)                                   │
│      dp[i] = dp[i-1] + dp[i-2];  // recurrence                │
│  return dp[n];                                                  │
│                                                                 │
│  PATTERNS:                                                      │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ 0/1 Knapsack    │ dp[i][w] = max(include, exclude)    │    │
│  │ Unbounded       │ Can reuse items                       │    │
│  │ LIS             │ dp[i] = longest ending at i          │    │
│  │ LCS             │ 2D table, match/mismatch             │    │
│  │ Grid DP         │ dp[i][j] from neighbors              │    │
│  │ Interval        │ dp[i][j] = max over k                │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Climbing Stairs (#70)   • Coin Change (#322)               │
│  • LIS (#300)              • LCS (#1143)                       │
│  • Edit Distance (#72)     • Burst Balloons (#312)             │
│  • Unique Paths (#62)      • Word Break (#139)                 │
│                                                                 │
│  SPACE OPTIMIZATION:                                            │
│  If dp[i] only depends on dp[i-1] and dp[i-2],                │
│  use two variables instead of array!                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 5: System Design

```text

┌─────────────────────────────────────────────────────────────────┐
│  SYSTEM DESIGN — Quick Reference                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  5-STEP FRAMEWORK:                                              │
│  1. Requirements (5 min)  → Functional + Non-functional        │
│  2. Estimation (5 min)    → QPS, Storage, Bandwidth            │
│  3. High-Level (15 min)   → Services, DBs, Caches, Queues     │
│  4. Deep Dive (20 min)    → Specific components                │
│  5. Wrap-up (5 min)       → Trade-offs, monitoring             │
│                                                                 │
│  KEY COMPONENTS:                                                │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ Load Balancer   │ NGINX, AWS ALB, Azure LB             │    │
│  │ Cache           │ Redis, Memcached                      │    │
│  │ Message Queue   │ Kafka, RabbitMQ, SQS                  │    │
│  │ CDN             │ CloudFront, Cloudflare                │    │
│  │ Database        │ PostgreSQL, MongoDB, DynamoDB         │    │
│  │ Search          │ Elasticsearch                         │    │
│  │ Object Storage  │ S3, Azure Blob, GCS                   │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  SCALING:                                                       │
│  • Horizontal: More machines (preferred)                       │
│  • Vertical: Bigger machine (limited)                          │
│  • Sharding: Split data across databases                       │
│  • Replication: Copy data for redundancy                       │
│                                                                 │
│  DATABASE CHOICES:                                              │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ SQL (RDBMS)     │ ACID, joins, structured data         │    │
│  │ NoSQL (Document)│ Flexible schema, horizontal scale    │    │
│  │ Key-Value       │ Fast lookups, caching                │    │
│  │ Wide-Column     │ Time-series, analytics               │    │
│  │ Graph           │ Relationships, social networks       │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  COMMON PATTERNS:                                               │
│  • CQRS: Separate read/write models                            │
│  • Event Sourcing: Store events, not state                     │
│  • Circuit Breaker: Prevent cascade failures                   │
│  • Saga: Distributed transactions                              │
│                                                                 │
│  COMMON QUESTIONS:                                              │
│  • URL Shortener, Rate Limiter, Chat System                    │
│  • News Feed, Notification System, Search                      │
│  • YouTube, Netflix, Uber, WhatsApp                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 6: Linked Lists & Stacks

```text

┌─────────────────────────────────────────────────────────────────┐
│  LINKED LISTS & STACKS — Quick Reference                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LINKED LIST TEMPLATES:                                         │
│                                                                 │
│  // Reverse Linked List                                         │
│  ListNode prev = null;                                          │
│  ListNode curr = head;                                          │
│  while (curr != null) {                                         │
│      ListNode next = curr.next;                                │
│      curr.next = prev;                                          │
│      prev = curr;                                               │
│      curr = next;                                               │
│  }                                                              │
│  return prev;                                                   │
│                                                                 │
│  // Detect Cycle (Floyd's)                                      │
│  ListNode slow = head, fast = head;                            │
│  while (fast != null && fast.next != null) {                   │
│      slow = slow.next;                                          │
│      fast = fast.next.next;                                    │
│      if (slow == fast) return true;  // cycle found            │
│  }                                                              │
│  return false;                                                  │
│                                                                 │
│  // Dummy Node Technique                                        │
│  ListNode dummy = new ListNode(0);                             │
│  ListNode tail = dummy;                                         │
│  // ... process nodes, attach to tail.next                     │
│  return dummy.next;                                             │
│                                                                 │
│  STACK PATTERNS:                                                │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ Valid Parens    │ Match opening/closing                 │    │
│  │ Monotonic Stack │ Next greater/lesser element           │    │
│  │ Evaluation      │ Postfix/Infix evaluation              │    │
│  │ DFS             │ Stack代替 recursion                    │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  MONOTONIC STACK:                                               │
│  Stack<Integer> stack = new Stack<>();                         │
│  for (int i = 0; i < n; i++) {                                  │
│      while (!stack.isEmpty() && arr[i] > arr[stack.peek()]) {  │
│          int idx = stack.pop();                                │
│          result[idx] = arr[i];  // next greater               │
│      }                                                          │
│      stack.push(i);                                             │
│  }                                                              │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Reverse List (#206)    • Merge Lists (#21)                 │
│  • LRU Cache (#146)       • Valid Parens (#20)                 │
│  • Min Stack (#155)       • Daily Temp (#739)                  │
│  • Largest Rectangle (#84)• Trapping Rain (#42)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 7: Hash Maps & Heaps

```text

┌─────────────────────────────────────────────────────────────────┐
│  HASH MAPS & HEAPS — Quick Reference                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  HASH MAP PATTERNS:                                             │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ Two Sum         │ Map<num, index>, check complement    │    │
│  │ Frequency       │ Map<num, count>                      │    │
│  │ Grouping        │ Map<key, list>                       │    │
│  │ Anagram         │ Map<sorted_string, list>             │    │
│  │ Subarray Sum    │ Map<prefix_sum, count>               │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  HEAP PATTERNS:                                                 │
│  ┌─────────────────┬──────────────────────────────────────┐    │
│  │ Top K           │ Min heap of size K                    │    │
│  │ Median          │ Max heap (lower) + Min heap (upper)  │    │
│  │ Merge K         │ Min heap of K lists                   │    │
│  │ Streaming       │ Heap for running statistics           │    │
│  └─────────────────┴──────────────────────────────────────┘    │
│                                                                 │
│  JAVA HEAP:                                                     │
│  // Min Heap                                                    │
│  PriorityQueue<Integer> minHeap = new PriorityQueue<>();       │
│  // Max Heap                                                    │
│  PriorityQueue<Integer> maxHeap = new PriorityQueue<>(         │
│      Collections.reverseOrder());                              │
│                                                                 │
│  TOP K TEMPLATE:                                                │
│  PriorityQueue<Integer> heap = new PriorityQueue<>();          │
│  for (int num : nums) {                                         │
│      heap.offer(num);                                           │
│      if (heap.size() > k) heap.poll();                        │
│  }                                                              │
│                                                                 │
│  LRU CACHE:                                                     │
│  HashMap<Integer, Node> map;                                   │
│  doubly-linked list for order;                                  │
│  get: O(1) - move to front                                     │
│  put: O(1) - add to front, evict from back if full             │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Two Sum (#1)          • Group Anagrams (#49)                │
│  • Top K (#347)          • LRU Cache (#146)                    │
│  • Subarray Sum (#560)   • Kth Largest (#215)                  │
│  • Merge K Lists (#23)   • Find Median (#295)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 🃏 Card 8: Binary Search & Sorting

```text

┌─────────────────────────────────────────────────────────────────┐
│  BINARY SEARCH & SORTING — Quick Reference                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BINARY SEARCH TEMPLATE:                                        │
│  int left = 0, right = n - 1;                                  │
│  while (left <= right) {                                        │
│      int mid = left + (right - left) / 2;                      │
│      if (arr[mid] == target) return mid;                       │
│      else if (arr[mid] < target) left = mid + 1;              │
│      else right = mid - 1;                                     │
│  }                                                              │
│  return left;  // insertion point                              │
│                                                                 │
│  SEARCH ON ANSWER:                                              │
│  int left = min_possible, right = max_possible;                │
│  while (left < right) {                                         │
│      int mid = left + (right - left) / 2;                      │
│      if (canSolve(mid)) right = mid;  // minimize             │
│      else left = mid + 1;                                      │
│  }                                                              │
│  return left;                                                   │
│                                                                 │
│  ROTATED ARRAY:                                                 │
│  while (left <= right) {                                        │
│      int mid = left + (right - left) / 2;                      │
│      if (arr[mid] == target) return mid;                       │
│      if (arr[left] <= arr[mid]) {  // left sorted             │
│          if (target >= arr[left] && target < arr[mid])         │
│              right = mid - 1;                                  │
│          else left = mid + 1;                                  │
│      } else {  // right sorted                                 │
│          if (target > arr[mid] && target <= arr[right])        │
│              left = mid + 1;                                   │
│          else right = mid - 1;                                 │
│      }                                                          │
│  }                                                              │
│                                                                 │
│  SORTING COMPLEXITY:                                            │
│  ┌──────────────┬───────────┬───────────┬────────┐            │
│  │ Algorithm    │ Best      │ Average   │ Worst  │            │
│  ├──────────────┼───────────┼───────────┼────────┤            │
│  │ Bubble       │ O(n)      │ O(n²)     │ O(n²) │            │
│  │ Insertion    │ O(n)      │ O(n²)     │ O(n²) │            │
│  │ Merge        │ O(nlogn)  │ O(nlogn)  │ O(nlogn)│          │
│  │ Quick        │ O(nlogn)  │ O(nlogn)  │ O(n²) │            │
│  │ Heap         │ O(nlogn)  │ O(nlogn)  │ O(nlogn)│          │
│  └──────────────┴───────────┴───────────┴────────┘            │
│                                                                 │
│  KEY PROBLEMS:                                                  │
│  • Binary Search (#704) • Rotated Array (#33)                  │
│  • Koko Bananas (#875)  • Split Array (#410)                   │
│  • Median Arrays (#4)   • Search Matrix (#74)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

---

## 📖 How to Use These Cards

### Before Mock Interviews
1. Review the relevant card for the topics you'll practice
2. Skim the templates and patterns
3. Recall 2-3 key problems for each pattern

### During Coding Interviews
1. Identify the pattern (Two Pointers? DP? Graph?)
2. Recall the template from the card
3. Adapt the template to the specific problem

### Daily Review
1. Pick one card per day
2. Cover the templates and try to recall from memory
3. Check your recall against the card

### Printing Tips
- Print each card on a single page
- Laminate for durability
- Keep on your desk or in a study folder
- Review during breaks

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Full coverage of all patterns |
| [Cheat Sheet](07-Cheat-Sheet.md) | Quick reference for all 28 phases |
| [LeetCode Study Plan](06-LeetCode-Study-Plan.md) | 12-week study schedule |
| [Mock Interview Bank](09-Mock-Interview-Question-Bank.md) | 90 practice questions |
| [Progress Tracker](08-Progress-Tracker.md) | Track your readiness |
---

## Summary

These quick reference cards provide single-page summaries of essential interview topics, including arrays, trees, graphs, dynamic programming, system design, and data structure cheat sheets for rapid review.

## See Also
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
- [JavaScript](../01-JavaScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [TypeScript](../02-TypeScript/)

---

## Cheat Sheet
```text
📋 QUICK REFERENCE CARDS CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)
