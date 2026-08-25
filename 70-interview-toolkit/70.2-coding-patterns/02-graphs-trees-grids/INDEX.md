# Graphs, Trees & Grids

> **4 files** (slots 02 and 06 reserved). Traversal and connectivity: DFS/BFS, union-find, topological sort, and tries — plus the grid-as-graph trick that unlocks most matrix problems.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The 4 patterns

| # | File | When to recognize | Read time |
|--:|------|-------------------|----------:|
| 01 | [DFS & BFS](70.2.2.01-dfs-bfs.md) | "Tree/graph traversal", connected components, level-order, shortest unweighted path | 45 min |
| 03 | [Union Find](70.2.2.03-union-find.md) | "Connected components online", redundant connections, accounts merge | 25 min |
| 04 | [Topological Sort](70.2.2.04-topological-sort.md) | "Dependency resolution, course schedule, build order" | 20 min |
| 05 | [Trie](70.2.2.05-trie.md) | "Prefix search, autocomplete, word dictionary" | 20 min |

---

## Planned additions

- **70.2.2.02 — Shortest Paths: Dijkstra & Bellman-Ford** *(upcoming)*: weighted shortest paths, when each applies, negative edges.
- **70.2.2.06 — Matrix Traversal & Simulation** *(upcoming)*: grid BFS/DFS idioms, spiral/rotation simulation, direction vectors.

Slots reserved; not yet written.

---

## Choosing between them

```text
Explore everything?              → DFS/BFS
Dynamic connectivity queries?    → Union Find
Ordering under dependencies?     → Topological Sort (Kahn's or DFS-based)
Many prefix lookups?             → Trie
Weighted shortest path?          → Dijkstra (planned 70.2.2.02)
Matrix as implicit graph?        → BFS/DFS with direction vectors
```

---

## Cross-References

- [Linear Structures](../01-linear-structures/INDEX.md) — binary search on sorted adjacency; intervals for scheduling variants.
- [Recursion & Optimization](../03-recursion-and-optimization/INDEX.md) — backtracking is DFS + undo.

---

## Navigation

[← Linear Structures](../01-linear-structures/INDEX.md) · [↑ Coding Patterns Home](../INDEX.md) · [Next: Recursion & Optimization →](../03-recursion-and-optimization/INDEX.md)
