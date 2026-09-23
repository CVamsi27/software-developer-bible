# Linear Structures

> **Study time:** ≈ 1 h 42 m of reading (7 files, ~15 min average).
> **7 files.** Array-, string-, and list-based patterns: sliding window, two pointers, binary search, linked list manipulation, intervals, greedy/prefix sums, and string search — the highest-frequency pattern family in interviews.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The 7 patterns

| # | File | When to recognize | Read time |
| --: | ------ | ------------------- | ----------: |
| 01 | [Sliding Window](70.2.1.01-sliding-window.md) | "Longest/shortest subarray/substring" with a contiguity constraint | 12 min |
| 02 | [Two Pointers](70.2.1.02-two-pointers.md) | "Sorted array, find pair/triplet", in-place partitioning | 14 min |
| 03 | [Binary Search](70.2.1.03-binary-search.md) | "Find first/last position", search on answer space, rotated arrays | 14 min |
| 04 | [Linked List Manipulation Patterns](70.2.1.04-linked-list-manipulation-patterns.md) | "Reverse/reorder list, reverse m..n, cycle entry, O(1)-space pointer surgery" | 17 min |
| 05 | [Intervals](70.2.1.05-intervals.md) | "Merge intervals, meeting rooms, overlapping ranges" | 14 min |
| 06 | [Greedy & Prefix Sum](70.2.1.06-greedy-prefix-sum.md) | "Jump game, partition, range sum queries" | 15 min |
| 07 | [String Search — KMP & Rabin-Karp](70.2.1.07-string-search-kmp-rabin-karp.md) | "Find substring, pattern matching, rolling hash" | 16 min |

---

## Recognition drill

```text
"Longest substring without repeating chars" → Sliding Window
"Two sum in sorted array"                   → Two Pointers
"Find first/last position"                  → Binary Search
"Reverse list between positions m-n"        → Linked List Manipulation
"Meeting rooms"                             → Intervals
"Jump game / range sum"                     → Greedy & Prefix Sum
"Repeated DNA sequences"                    → Rabin-Karp
```

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
