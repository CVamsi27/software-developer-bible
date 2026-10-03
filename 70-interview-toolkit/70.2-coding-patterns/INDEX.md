# Coding Patterns — Index

> **Study time:** ≈ 5 h of reading (27 files, ~11 min average).
> **27 files across 5 categories.** Essential coding patterns for technical interviews from sliding window and two pointers to dynamic programming, advanced data structures (monotonic stack, segment tree, bit manipulation), number theory & combinatorics, and streaming algorithms (reservoir sampling).

[![Files](https://img.shields.io/badge/files-27-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

A pattern is a candidate explanation, not a guarantee. “Contiguous subarray” suggests a window only when the validity rule supports safe expansion/shrinking; negative values can change that choice. Learn the invariant and input contract alongside the keyword.

## Read in Three Passes

1. **Move through the data:** start with [linear structures](01-linear-structures/INDEX.md), then [graphs and grids](02-graphs-trees-grids/INDEX.md). For each example, draw what remains unprocessed after one step.
2. **Decide what state must survive:** read [recursion and optimization](03-recursion-and-optimization/INDEX.md). Compare enumeration, repeated subproblems, and compressed state before choosing an algorithm.
3. **Handle changing priorities and arithmetic bounds:** read [heaps and selection](04-heaps-stacks-selection/INDEX.md), then [number theory](05-math-and-number-theory/INDEX.md). Identify the operation that dominates cost and the intermediate value that can overflow.

Finish each category with its separate revision companion. On a return visit, open the category whose mechanism you could not explain; you do not need to reread every chapter.
---

## The 5 Categories

| Category | Files | Coverage |
| ----------------------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------ |
| [01 — Linear Structures](01-linear-structures/INDEX.md) | 7 | Sliding window, two pointers, binary search, linked list manipulation, intervals, greedy/prefix sum, string search |
| [02 — Graphs, Trees & Grids](02-graphs-trees-grids/INDEX.md) | 6 | DFS/BFS, shortest paths (Dijkstra/Bellman-Ford), union find, topological sort, trie, matrix traversal/simulation |
| [03 — Recursion & Optimization](03-recursion-and-optimization/INDEX.md) | 3 | Backtracking, dynamic programming, bit manipulation |
| [04 — Heaps, Stacks & Selection](04-heaps-stacks-selection/INDEX.md) | 5 | Heap, monotonic stack, stack/queue designs, segment tree, quickselect/reservoir sampling |
| [05 — Math & Number Theory](05-math-and-number-theory/INDEX.md) | 1 | Number theory & combinatorics (primes, GCD/LCM, modular arithmetic, probability) |

---

## Start with Common Problem Shapes

Use these links after choosing a category pass above. The signals narrow the candidates; the constraints settle the choice.

| # | Pattern | Category | When to recognize | Role priority | General importance | Read time |
| --: | --------- | ---------- | ------------------- | --- | --- | ----------: |
| 01 | [Sliding Window](01-linear-structures/70.2.1.01-sliding-window.md) | Linear | "Longest/shortest subarray/substring" | Essential | 11 min | 11 min |
| 02 | [Two Pointers](01-linear-structures/70.2.1.02-two-pointers.md) | Linear | "Sorted array, find pair/triplet" | Essential | 13 min | 12 min |
| 03 | [Binary Search](01-linear-structures/70.2.1.03-binary-search.md) | Linear | "Find first/last position", rotated array | Essential | 11 min | 11 min |
| 04 | [DFS & BFS](02-graphs-trees-grids/70.2.2.01-dfs-bfs.md) | Graphs | "Tree/graph traversal", shortest path, components | Essential | 16 min | 16 min |
| 05 | [Backtracking](03-recursion-and-optimization/70.2.3.01-backtracking.md) | Recursion | "Generate all permutations/combinations/subsets" | Essential | 13 min | 13 min |
| 06 | [Dynamic Programming](03-recursion-and-optimization/70.2.3.02-dynamic-programming.md) | Recursion | "Count ways, min/max cost, LCS" | Essential | 11 min | 11 min |
| 07 | [Heap](04-heaps-stacks-selection/70.2.4.01-heap.md) | Selection | "Top K, K-way merge, median of stream" | Essential | 12 min | 12 min |
| 08 | [Trie](02-graphs-trees-grids/70.2.2.05-trie.md) | Graphs | "Prefix search, autocomplete, word dictionary" | Essential | 15 min | 15 min |
| 09 | [Union Find](02-graphs-trees-grids/70.2.2.03-union-find.md) | Graphs | "Connected components, redundant connections" | Optional | 15 min | 15 min |
| 10 | [Topological Sort](02-graphs-trees-grids/70.2.2.04-topological-sort.md) | Graphs | "Dependency resolution, course schedule" | Essential | 13 min | 13 min |
| 11 | [Intervals](01-linear-structures/70.2.1.05-intervals.md) | Linear | "Merge intervals, meeting rooms, overlapping" | Essential | 11 min | 11 min |
| 12 | [Greedy & Prefix Sum](01-linear-structures/70.2.1.06-greedy-prefix-sum.md) | Linear | "Jump game, partition, range sum queries" | Essential | 12 min | 12 min |

---

## Extend the Toolkit

Use these when a simpler scan, traversal, or recurrence cannot meet the stated operations and bounds.

| # | Pattern | Category | When to recognize | Role priority | General importance | Read time |
| --: | --------- | ---------- | ------------------- | --- | --- | ----------: |
| 13 | [Monotonic Stack](04-heaps-stacks-selection/70.2.4.02-monotonic-stack.md) | Heaps/Stacks | "Next greater/smaller element, histogram" | Essential | 12 min | 12 min |
| 14 | [Segment Tree & BIT](04-heaps-stacks-selection/70.2.4.04-segment-tree.md) | Heaps/Stacks | "Range query + point update" | Optional | 16 min | 16 min |
| 15 | [Bit Manipulation](03-recursion-and-optimization/70.2.3.03-bit-manipulation.md) | Recursion | "XOR, bitmask, subset enumeration, popcount" | Optional | 14 min | 14 min |
| 16 | [String Search — KMP & Rabin-Karp](01-linear-structures/70.2.1.07-string-search-kmp-rabin-karp.md) | Linear | "Find substring, pattern matching" | Optional | 15 min | 15 min |
| 17 | [Quick Select & Reservoir Sampling](04-heaps-stacks-selection/70.2.4.05-quick-select-reservoir-sampling.md) | Heaps/Stacks | "K-th largest, sample from stream" | Essential | 15 min | 15 min |
| 18 | [Stack & Queue Patterns](04-heaps-stacks-selection/70.2.4.03-stack-queue-patterns.md) | Heaps/Stacks | "LRU cache, sliding window max, min stack" | Essential | 16 min | 16 min |
| 19 | [Linked List Manipulation Patterns](01-linear-structures/70.2.1.04-linked-list-manipulation-patterns.md) | Linear | "Reverse/reorder list, cycle entry, O(1)-space surgery" | Essential | 14 min | 14 min |
| 20 | [Shortest Paths — Dijkstra & Bellman-Ford](02-graphs-trees-grids/70.2.2.02-shortest-paths-dijkstra-bellman-ford.md) | Graphs | "Weighted shortest path, K stops, negative edges/arbitrage" | Optional | 14 min | 14 min |
| 21 | [Matrix Traversal & Simulation](02-graphs-trees-grids/70.2.2.06-matrix-traversal-simulation.md) | Graphs | "Spiral order, rotate in place, set zeroes O(1), diagonals" | Essential | 13 min | 13 min |

---

## Choose a Practice Route

For an upcoming full-stack interview, prioritize the structures the employer actually describes and practice explaining contracts and edge cases. For a broader coding loop, complete the category passes and compare two plausible approaches for each problem. With little time left, use the section companions to find one or two specific gaps and rehearse those mechanisms.

## Finish the Categories

- [Linear structures revision](01-linear-structures/REVISION.md)
- [Graphs, trees and grids revision](02-graphs-trees-grids/REVISION.md)
- [Recursion and optimization revision](03-recursion-and-optimization/REVISION.md)
- [Heaps, stacks and selection revision](04-heaps-stacks-selection/REVISION.md)
- [Math and number theory revision](05-math-and-number-theory/REVISION.md)

## Cross-References

- [JavaScript](../../10-frontend/10.1-javascript/INDEX.md) — implement patterns in JS
- [System Design](../../30-architecture/30.2-system-design/INDEX.md) — patterns at scale
- [SDE Role](../../81-lanes-indian-sde-faang/INDEX.md) — the Indian SDE/FAANG lane (heavy on this)
- [Cheat Sheets](../70.3-cheatsheets/INDEX.md) — quick reference

---

## Navigation

← Previous: [Behavioral](../70.1-behavioral/INDEX.md) · [ Back to Index](../INDEX.md) · Next: [Cheat Sheets →](../70.3-cheatsheets/INDEX.md)
