# Coding Patterns — Index

> **21 files across 4 categories.** Essential coding patterns for technical interviews from sliding window and two pointers to dynamic programming, advanced data structures (monotonic stack, segment tree, bit manipulation), and streaming algorithms (reservoir sampling).

[![Files](https://img.shields.io/badge/files-21-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why coding patterns:** Most LeetCode problems reduce to one of ~15-20 patterns. If you can name the pattern in 30 seconds, the rest is implementation. The 12 core patterns cover ~80% of interview problems. The 6 advanced patterns handle the harder FAANG questions.

---

## The 4 Categories

| Category | Files | Coverage |
| ----------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------ |
| [01 — Linear Structures](01-linear-structures/INDEX.md) | 7 | Sliding window, two pointers, binary search, linked list manipulation, intervals, greedy/prefix sum, string search |
| [02 — Graphs, Trees & Grids](02-graphs-trees-grids/INDEX.md) | 6 | DFS/BFS, shortest paths (Dijkstra/Bellman-Ford), union find, topological sort, trie, matrix traversal/simulation |
| [03 — Recursion & Optimization](03-recursion-and-optimization/INDEX.md) | 3 | Backtracking, dynamic programming, bit manipulation |
| [04 — Heaps, Stacks & Selection](04-heaps-stacks-selection/INDEX.md) | 5 | Heap, monotonic stack, stack/queue designs, segment tree, quickselect/reservoir sampling |

---

## Core Patterns (the 12 that cover ~80% of problems)

Master these first.

| # | Pattern | Category | When to recognize | Read time |
| --: | --------- | ---------- | ------------------- | ----------: |
| 01 | [Sliding Window](01-linear-structures/70.2.1.01-sliding-window.md) | Linear | "Longest/shortest subarray/substring" | 30 min |
| 02 | [Two Pointers](01-linear-structures/70.2.1.02-two-pointers.md) | Linear | "Sorted array, find pair/triplet" | 30 min |
| 03 | [Binary Search](01-linear-structures/70.2.1.03-binary-search.md) | Linear | "Find first/last position", rotated array | 30 min |
| 04 | [DFS & BFS](02-graphs-trees-grids/70.2.2.01-dfs-bfs.md) | Graphs | "Tree/graph traversal", shortest path, components | 45 min |
| 05 | [Backtracking](03-recursion-and-optimization/70.2.3.01-backtracking.md) | Recursion | "Generate all permutations/combinations/subsets" | 30 min |
| 06 | [Dynamic Programming](03-recursion-and-optimization/70.2.3.02-dynamic-programming.md) | Recursion | "Count ways, min/max cost, LCS" | 60 min |
| 07 | [Heap](04-heaps-stacks-selection/70.2.4.01-heap.md) | Selection | "Top K, K-way merge, median of stream" | 25 min |
| 08 | [Trie](02-graphs-trees-grids/70.2.2.05-trie.md) | Graphs | "Prefix search, autocomplete, word dictionary" | 20 min |
| 09 | [Union Find](02-graphs-trees-grids/70.2.2.03-union-find.md) | Graphs | "Connected components, redundant connections" | 25 min |
| 10 | [Topological Sort](02-graphs-trees-grids/70.2.2.04-topological-sort.md) | Graphs | "Dependency resolution, course schedule" | 20 min |
| 11 | [Intervals](01-linear-structures/70.2.1.05-intervals.md) | Linear | "Merge intervals, meeting rooms, overlapping" | 20 min |
| 12 | [Greedy & Prefix Sum](01-linear-structures/70.2.1.06-greedy-prefix-sum.md) | Linear | "Jump game, partition, range sum queries" | 30 min |

---

## Advanced Patterns

For staff/principal FAANG questions.

| # | Pattern | Category | When to recognize | Read time |
| --: | --------- | ---------- | ------------------- | ----------: |
| 13 | [Monotonic Stack](04-heaps-stacks-selection/70.2.4.02-monotonic-stack.md) | Heaps/Stacks | "Next greater/smaller element, histogram" | 30 min |
| 14 | [Segment Tree & BIT](04-heaps-stacks-selection/70.2.4.04-segment-tree.md) | Heaps/Stacks | "Range query + point update" | 45 min |
| 15 | [Bit Manipulation](03-recursion-and-optimization/70.2.3.03-bit-manipulation.md) | Recursion | "XOR, bitmask, subset enumeration, popcount" | 25 min |
| 16 | [String Search — KMP & Rabin-Karp](01-linear-structures/70.2.1.07-string-search-kmp-rabin-karp.md) | Linear | "Find substring, pattern matching" | 30 min |
| 17 | [Quick Select & Reservoir Sampling](04-heaps-stacks-selection/70.2.4.05-quick-select-reservoir-sampling.md) | Heaps/Stacks | "K-th largest, sample from stream" | 25 min |
| 18 | [Stack & Queue Patterns](04-heaps-stacks-selection/70.2.4.03-stack-queue-patterns.md) | Heaps/Stacks | "LRU cache, sliding window max, min stack" | 30 min |
| 19 | [Linked List Manipulation Patterns](01-linear-structures/70.2.1.04-linked-list-manipulation-patterns.md) | Linear | "Reverse/reorder list, cycle entry, O(1)-space surgery" | 35 min |
| 20 | [Shortest Paths — Dijkstra & Bellman-Ford](02-graphs-trees-grids/70.2.2.02-shortest-paths-dijkstra-bellman-ford.md) | Graphs | "Weighted shortest path, K stops, negative edges/arbitrage" | 40 min |
| 21 | [Matrix Traversal & Simulation](02-graphs-trees-grids/70.2.2.06-matrix-traversal-simulation.md) | Graphs | "Spiral order, rotate in place, set zeroes O(1), diagonals" | 30 min |

---

## Pattern recognition drill (the first 30 seconds of any problem)

```text
"Longest substring without repeating chars" → Sliding Window
"Two sum in sorted array" → Two Pointers
"Find first/last position" → Binary Search
"Number of islands" → DFS/BFS
"Permutations" → Backtracking
"Coin change" → Dynamic Programming
"Top K frequent" → Heap
"Word search" → Trie / Backtracking
"Redundant connection" → Union Find
"Course schedule" → Topological Sort
"Merge intervals" → Intervals
"Jump game" → Greedy
"Reverse list between positions m-n" → Linked List Manipulation
"Cheapest flights within K stops" → Shortest Paths (Bellman-Ford)
"Spiral order / rotate matrix in place" → Matrix Traversal & Simulation
```

---

## Suggested Study Order

### Path A — Abroad Full-Stack (1-2 days)
Focus on **6 patterns**: Sliding Window, Two Pointers, DFS/BFS, Heap, Binary Search, Backtracking. Do 5-8 problems per pattern.

### Path B — Indian SDE / FAANG (1-2 weeks)
**All 12 core patterns**, then **all 9 advanced patterns**. 10-15 problems per pattern. Practice timed (45 min per medium).

### Path C — Interview tomorrow
- Re-read the cheat sheet for the 3-4 most-tested patterns
- Do 1-2 warm-up problems
- Memorize the recognition keywords (above)

---

## Common interview topics

- "Given X, recognize the pattern in 30 seconds."
- "Implement X in 30 minutes with O(...) time/space."
- "What if the input is now a stream?"
- "What if memory is constrained?"

---

## Cross-References

- [JavaScript](../../10-frontend/10.1-javascript/INDEX.md) — implement patterns in JS
- [System Design](../../30-architecture/30.2-system-design/INDEX.md) — patterns at scale
- [SDE Role](../../81-lanes-indian-sde-faang/INDEX.md) — the Indian SDE/FAANG lane (heavy on this)
- [Cheat Sheets](../70.3-cheatsheets/INDEX.md) — quick reference

---

## Navigation

← Previous: [Behavioral](../70.1-behavioral/INDEX.md) · [ Back to Index](../INDEX.md) · Next: [CheatSheets →](../70.3-cheatsheets/INDEX.md)
