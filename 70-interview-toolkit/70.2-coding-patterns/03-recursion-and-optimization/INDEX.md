# Recursion & Optimization

> **Study time:** ≈ 40 min of reading (4 files, ~10 min average).
> **4 files.** The exhaustive-search-to-optimal pipeline: backtracking to enumerate, dynamic programming to remember, bit manipulation to compress state.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Reading Passes

Enumerate choices with backtracking first, watching which state must be restored for a sibling branch. Then read DP and identify repeated states that can be reused. Finish with bit representation only after deciding what the state means; fitting it into a word does not make an exponential state space small.

## The 3 patterns

| # | File | When to recognize | Role priority | General importance | Read time |
| --: | ------ | ------------------- | --- | --- | ----------: |
| 01 | [Backtracking](70.2.3.01-backtracking.md) | "Generate all permutations/combinations/subsets", N-Queens, Sudoku | Essential | Important | 13 min |
| 02 | [Dynamic Programming](70.2.3.02-dynamic-programming.md) | "Count ways, min/max cost, longest common subsequence, knapsack" | Essential | Important | 11 min |
| 03 | [Bit Manipulation](70.2.3.03-bit-manipulation.md) | "XOR tricks, bitmask subset enumeration, popcount, single number" | Optional | Specialized | 13 min |

---

## The relationship

```text
Brute force recursion          → correct, exponential
   + prune dead branches       → backtracking
   + memoize overlapping calls → dynamic programming (top-down)
   + tabulate bottom-up        → DP (bottom-up), evaluated in dependency order
   + states fit in a word      → compact representation; state count still matters
```

Memoization reuses repeated states; runtime still depends on the number of distinct states and transitions. Test that distinction in the separate revision companion.

---

## Cross-References

- [Graphs, Trees & Grids](../02-graphs-trees-grids/INDEX.md) — backtracking = DFS over choice space with undo.
- [Heaps, Stacks & Selection](../04-heaps-stacks-selection/INDEX.md) — greedy-with-structure alternatives to DP.

---

## Navigation

[← Graphs, Trees & Grids](../02-graphs-trees-grids/INDEX.md) · [↑ Coding Patterns Home](../INDEX.md) · [Next: Heaps, Stacks & Selection →](../04-heaps-stacks-selection/INDEX.md)

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
