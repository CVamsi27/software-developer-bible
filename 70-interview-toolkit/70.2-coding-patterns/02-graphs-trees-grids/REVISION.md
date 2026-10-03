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

**A:** Its first discovery has shortest edge distance; marking then prevents multiple parents from repeatedly queueing the same node. Weighted algorithms need a different settlement rule.

## Shortest Paths: Dijkstra & Bellman-Ford

Source: [Shortest Paths: Dijkstra & Bellman-Ford](70.2.2.02-shortest-paths-dijkstra-bellman-ford.md)

**Q:** Why does non-negative weight matter to Dijkstra's settlement proof?

**A:** Once the minimum candidate is chosen, any remaining path cannot improve it through a negative detour. Negative edges invalidate that greedy proof even if a reprocessing variant sometimes finds the answer.

## Union-Find

Source: [Union-Find](70.2.2.03-union-find.md)

**Q:** What do path compression and union by size change about Union-Find?

**A:** They shorten future parent walks and prevent avoidable deep trees, giving amortized near-constant operations. They do not provide arbitrary graph paths or edge deletions.

## Topological Sort

Source: [Topological Sort](70.2.2.04-topological-sort.md)

**Q:** What does an incomplete Kahn traversal establish?

**A:** If fewer vertices are emitted than exist, remaining vertices are blocked by a cycle under the dependency graph model. It does not necessarily identify every cycle's exact edges.

## Trie

Source: [Trie](70.2.2.05-trie.md)

**Q:** Why keep a terminal marker separate from a Trie node's existence?

**A:** A path can be a prefix of another stored word without itself being a stored word. Exact search and prefix search answer different questions.

## Matrix Traversal & Simulation

Source: [Matrix Traversal & Simulation](70.2.2.06-matrix-traversal-simulation.md)

**Q:** What must a matrix simulation make explicit before mutation?

**A:** Bounds, traversal order, visited/state encoding, and which original values future steps still need. In-place markers are safe only when they cannot collide with legitimate input state.

## Summary

Choose the state before the traversal: visited status for reachability, tentative distance for weighted paths, component representative for merges, or remaining prerequisites for dependency order.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
