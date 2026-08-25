# Recursion & Optimization

> **3 files.** The exhaustive-search-to-optimal pipeline: backtracking to enumerate, dynamic programming to remember, bit manipulation to compress state.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The 3 patterns

| # | File | When to recognize | Read time |
|--:|------|-------------------|----------:|
| 01 | [Backtracking](70.2.3.01-backtracking.md) | "Generate all permutations/combinations/subsets", N-Queens, Sudoku | 30 min |
| 02 | [Dynamic Programming](70.2.3.02-dynamic-programming.md) | "Count ways, min/max cost, longest common subsequence, knapsack" | 60 min |
| 03 | [Bit Manipulation](70.2.3.03-bit-manipulation.md) | "XOR tricks, bitmask subset enumeration, popcount, single number" | 25 min |

---

## The relationship

```text
Brute force recursion          → correct, exponential
   + prune dead branches       → backtracking
   + memoize overlapping calls → dynamic programming (top-down)
   + tabulate bottom-up        → DP (bottom-up), O(1) extra per state
   + states fit in a word      → bitmask DP / bit manipulation
```

Interview trap: "Why is memoized recursion still exponential here?" — overlapping subproblems are necessary but not sufficient; distinguish them from distinct states.

---

## Cross-References

- [Graphs, Trees & Grids](../02-graphs-trees-grids/INDEX.md) — backtracking = DFS over choice space with undo.
- [Heaps, Stacks & Selection](../04-heaps-stacks-selection/INDEX.md) — greedy-with-structure alternatives to DP.

---

## Navigation

[← Graphs, Trees & Grids](../02-graphs-trees-grids/INDEX.md) · [↑ Coding Patterns Home](../INDEX.md) · [Next: Heaps, Stacks & Selection →](../04-heaps-stacks-selection/INDEX.md)
