# Graphs, Trees & Grids

> **6 files.** Traversal, connectivity, weighted paths, and grid simulation: DFS/BFS, Dijkstra/Bellman-Ford, union-find, topological sort, tries, and the matrix-index patterns that unlock most grid problems.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The 6 patterns

| # | File | When to recognize | Read time |
|--:|------|-------------------|----------:|
| 01 | [DFS & BFS](70.2.2.01-dfs-bfs.md) | "Tree/graph traversal", connected components, level-order, shortest unweighted path | 45 min |
| 02 | [Shortest Paths — Dijkstra & Bellman-Ford](70.2.2.02-shortest-paths-dijkstra-bellman-ford.md) | Weighted shortest path, "cheapest with K stops", negative edges/arbitrage, 0-1 weights | 40 min |
| 03 | [Union Find](70.2.2.03-union-find.md) | "Connected components online", redundant connections, accounts merge | 25 min |
| 04 | [Topological Sort](70.2.2.04-topological-sort.md) | "Dependency resolution, course schedule, build order" | 20 min |
| 05 | [Trie](70.2.2.05-trie.md) | "Prefix search, autocomplete, word dictionary" | 20 min |
| 06 | [Matrix Traversal & Simulation](70.2.2.06-matrix-traversal-simulation.md) | Spiral order, rotate in place, set zeroes O(1), diagonal traversal, direction vectors | 30 min |

---

## Choosing between them

```text
Explore everything?              → DFS/BFS
Dynamic connectivity queries?    → Union Find
Ordering under dependencies?     → Topological Sort (Kahn's or DFS-based)
Many prefix lookups?             → Trie
Weighted shortest path (w >= 0)? → Dijkstra + binary heap
Negative edges / K-stop limits?  → Bellman-Ford (+ cycle detection)
Matrix as implicit graph?        → BFS/DFS with direction vectors
Spiral/rotate/zero-fill?         → Boundary shrinking / transpose+reverse / marker tricks
```

---

## Cross-References

- [Linear Structures](../01-linear-structures/INDEX.md) — binary search on sorted adjacency; intervals for scheduling variants.
- [Recursion & Optimization](../03-recursion-and-optimization/INDEX.md) — backtracking is DFS + undo.

---

## Navigation

[← Linear Structures](../01-linear-structures/INDEX.md) · [↑ Coding Patterns Home](../INDEX.md) · [Next: Recursion & Optimization →](../03-recursion-and-optimization/INDEX.md)
