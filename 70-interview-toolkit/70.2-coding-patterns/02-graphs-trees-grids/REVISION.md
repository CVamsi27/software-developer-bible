<!-- section: Coding Patterns | category: Reference | tags: revision, practi | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Graphs, Trees & Grids — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## DFS & BFS

Source: [DFS & BFS](70.2.2.01-dfs-bfs.md)

**Q:** Why mark an unweighted BFS node when enqueuing it?

**A:** BFS explores an unweighted graph one distance level at a time. The first time it reaches a node, it has found a shortest path by number of edges. Mark the node when adding it to the queue so other neighbors do not add it again. This rule alone is not sufficient when edges have different weights.

## Shortest Paths: Dijkstra & Bellman-Ford

Source: [Shortest Paths: Dijkstra & Bellman-Ford](70.2.2.02-shortest-paths-dijkstra-bellman-ford.md)

**Q:** Why does Dijkstra require non-negative edge weights when finalizing a distance?

**A:** Dijkstra selects the unfinished node with the smallest known distance. With non-negative edges, reaching it later through a farther node cannot make the path shorter. A negative edge could reduce that later path, so the selected distance would no longer be safe to treat as final.

## Union-Find

Source: [Union-Find](70.2.2.03-union-find.md)

**Q:** What do path compression and union by size change about Union-Find?

**A:** Path compression makes visited nodes point closer to their group representative. Union by size attaches the smaller tree under the larger one, limiting depth. Together, they make a sequence of find and union operations almost constant time per operation on average. Union-Find tracks connected groups; it does not return paths or directly support removing edges.

## Topological Sort

Source: [Topological Sort](70.2.2.04-topological-sort.md)

**Q:** What does it mean if Kahn's topological sort cannot process every vertex?

**A:** Kahn's algorithm repeatedly processes vertices with no remaining prerequisites. If it stops while vertices remain, the graph contains a cycle. Some remaining vertices may depend on that cycle without belonging to it. The unfinished result does not identify the exact cycle edges.

## Trie

Source: [Trie](70.2.2.05-trie.md)

**Q:** Why keep a terminal marker separate from a Trie node's existence?

**A:** A path can be a prefix of another stored word without itself being a stored word. Exact search and prefix search answer different questions.

## Matrix Traversal & Simulation

Source: [Matrix Traversal & Simulation](70.2.2.06-matrix-traversal-simulation.md)

**Q:** What must a matrix simulation make explicit before mutation?

**A:** State the valid row and column limits, the order of visits, and how you mark visited cells. Also ask whether a later step needs an original value that you are about to overwrite. A marker stored in the matrix must be distinguishable from every valid input value.

## Summary

Choose the state before the traversal: visited status for reachability, tentative distance for weighted paths, component representative for merges, or remaining prerequisites for dependency order.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
