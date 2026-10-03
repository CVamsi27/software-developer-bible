# Linear Structures

> **Study time:** ≈ 1 h 29 m of reading (8 files, ~11 min average).
> **8 files.** Array-, string-, and list-based patterns: sliding window, two pointers, binary search, linked list manipulation, intervals, greedy/prefix sums, and string search — a foundation for sequence-based problems.

[![Files](https://img.shields.io/badge/files-8-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Reading Passes

Start with window and pointer movement, then binary-search interval invariants. Continue into linked-list rewiring and interval endpoint conventions. Finish by contrasting greedy elimination with stored prefix state, then use KMP/rolling hashes to retain work across string alignments. Keep the same habit throughout: draw the retained state and name the input contract before tracing code.

## The 7 patterns

| # | File | When to recognize | Role priority | General importance | Read time |
| --: | ------ | ------------------- | --- | --- | ----------: |
| 01 | [Sliding Window](70.2.1.01-sliding-window.md) | "Longest/shortest subarray/substring" with a contiguity constraint | Essential | 11 min | 11 min |
| 02 | [Two Pointers](70.2.1.02-two-pointers.md) | "Sorted array, find pair/triplet", in-place partitioning | Essential | 13 min | 12 min |
| 03 | [Binary Search](70.2.1.03-binary-search.md) | "Find first/last position", search on answer space, rotated arrays | Essential | 11 min | 11 min |
| 04 | [Linked List Manipulation Patterns](70.2.1.04-linked-list-manipulation-patterns.md) | "Reverse/reorder list, reverse m..n, cycle entry, O(1)-space pointer surgery" | Essential | 14 min | 14 min |
| 05 | [Intervals](70.2.1.05-intervals.md) | "Merge intervals, meeting rooms, overlapping ranges" | Essential | 11 min | 11 min |
| 06 | [Greedy & Prefix Sum](70.2.1.06-greedy-prefix-sum.md) | "Jump game, partition, range sum queries" | Essential | 12 min | 12 min |
| 07 | [String Search — KMP & Rabin-Karp](70.2.1.07-string-search-kmp-rabin-karp.md) | "Find substring, pattern matching, rolling hash" | Optional | 15 min | 15 min |

---

## Cross-References

- [Graphs, Trees & Grids](../02-graphs-trees-grids/INDEX.md) — when data stops being linear.
- [Heaps, Stacks & Selection](../04-heaps-stacks-selection/INDEX.md) — monotonic stack generalizes two-pointers ideas.

---

## Navigation

[↑ Coding Patterns Home](../INDEX.md) · [Next: Graphs, Trees & Grids →](../02-graphs-trees-grids/INDEX.md)

---

## Docita Anchor

[Docita](https://github.com/CVamsi27/docita) is the companion production repo this bible anchors to.

| Topic | Docita evidence |
| ------------------------------------ | --------------------------------------------------------------------------------- |
| Hashing + eviction ordering hot spot | `apps/api/src/shared/common/utils/lru-cache.ts` — the closest genuine pattern use |

Honest note: docita's workload is business CRUD dominated; there are no algorithmic hot spots beyond this one utility. The patterns in this category stay interview-only material.

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
