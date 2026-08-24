# Coding Patterns — Index

> **18 files** — Essential coding patterns for technical interviews from sliding window and two pointers to dynamic programming, advanced data structures (monotonic stack, segment tree, bit manipulation), and streaming algorithms (reservoir sampling).

[![Files](https://img.shields.io/badge/files-18-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why coding patterns:** Most LeetCode problems reduce to one of ~15-20 patterns. If you can name the pattern in 30 seconds, the rest is implementation. The 12 core patterns cover ~80% of interview problems. The 6 advanced patterns handle the harder FAANG questions.

---

## Topic Categories

| Category | Files | Coverage | Difficulty |
|----------|------:|----------|------------|
| [Core Patterns](#core-patterns-01-12) | 12 | ~80% of interview problems | Easy-Medium |
| [Advanced Patterns](#advanced-patterns-13-18) | 6 | The harder FAANG questions | Hard |

---

## Core Patterns (01-12)

The 12 patterns that cover most LeetCode problems. **Master these first.**

| # | Pattern | When to recognize | Read time |
|--:|---------|-------------------|----------:|
| 01 | [Sliding Window](70.2.01-sliding-window.md) | "Longest/shortest subarray/substring" | 30 min |
| 02 | [Two Pointers](70.2.02-two-pointers.md) | "Sorted array, find pair/triplet" | 30 min |
| 03 | [Binary Search](70.2.03-binary-search.md) | "Find first/last position", search in rotated array | 30 min |
| 04 | [DFS & BFS](70.2.04-dfs-bfs.md) | "Tree/graph traversal", shortest path, connected components | 45 min |
| 05 | [Backtracking](70.2.05-backtracking.md) | "Generate all permutations/combinations/subsets" | 30 min |
| 06 | [Dynamic Programming](70.2.06-dynamic-programming.md) | "Count ways, min/max cost, longest common subsequence" | 60 min |
| 07 | [Heap](70.2.07-heap.md) | "Top K, K-way merge, median of stream" | 25 min |
| 08 | [Trie](70.2.08-trie.md) | "Prefix search, autocomplete, word dictionary" | 20 min |
| 09 | [Union Find](70.2.09-union-find.md) | "Connected components, redundant connections" | 25 min |
| 10 | [Topological Sort](70.2.10-topological-sort.md) | "Dependency resolution, course schedule" | 20 min |
| 11 | [Intervals](70.2.11-intervals.md) | "Merge intervals, meeting rooms, overlapping" | 20 min |
| 12 | [Greedy & Prefix Sum](70.2.12-greedy-prefix-sum.md) | "Jump game, partition, range sum queries" | 30 min |

**Pattern recognition drill (the first 30 seconds of any problem):**

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
```

---

## Advanced Patterns (13-18)

For staff/principal FAANG questions.

| # | Pattern | When to recognize | Read time |
|--:|---------|-------------------|----------:|
| 13 | [Monotonic Stack](70.2.13-monotonic-stack.md) | "Next greater/smaller element, largest rectangle in histogram" | 30 min |
| 14 | [Segment Tree & BIT](70.2.14-segment-tree.md) | "Range sum/min/max query, point update" | 45 min |
| 15 | [Bit Manipulation](70.2.15-bit-manipulation.md) | "XOR, bitmask, subset enumeration, popcount" | 25 min |
| 16 | [String Search — KMP & Rabin-Karp](70.2.16-string-search-kmp-rabin-karp.md) | "Find substring, pattern matching, plagiarism detection" | 30 min |
| 17 | [Quick Select & Reservoir Sampling](70.2.17-quick-select-reservoir-sampling.md) | "K-th largest, random sample from stream" | 25 min |
| 18 | [Stack & Queue Patterns](70.2.18-stack-queue-patterns.md) | "LRU cache, sliding window max, min stack" | 30 min |

---

## Suggested Study Order

### Path A — Abroad Full-Stack (1-2 days)
Focus on **6 patterns**: Sliding Window, Two Pointers, DFS/BFS, Heap, Binary Search, Backtracking. Do 5-8 problems per pattern.

### Path B — Indian SDE / FAANG (1-2 weeks)
**All 12 core patterns**, then **all 6 advanced patterns**. 10-15 problems per pattern. Practice timed (45 min per medium).

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
