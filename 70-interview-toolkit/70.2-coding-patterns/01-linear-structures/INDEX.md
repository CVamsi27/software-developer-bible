# Linear Structures

> **6 files** (slot 04 reserved). Array- and string-based patterns: sliding window, two pointers, binary search, intervals, greedy/prefix sums, and string search — the highest-frequency pattern family in interviews.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The 6 patterns

| # | File | When to recognize | Read time |
|--:|------|-------------------|----------:|
| 01 | [Sliding Window](70.2.1.01-sliding-window.md) | "Longest/shortest subarray/substring" with a contiguity constraint | 30 min |
| 02 | [Two Pointers](70.2.1.02-two-pointers.md) | "Sorted array, find pair/triplet", in-place partitioning | 30 min |
| 03 | [Binary Search](70.2.1.03-binary-search.md) | "Find first/last position", search on answer space, rotated arrays | 30 min |
| 05 | [Intervals](70.2.1.05-intervals.md) | "Merge intervals, meeting rooms, overlapping ranges" | 20 min |
| 06 | [Greedy & Prefix Sum](70.2.1.06-greedy-prefix-sum.md) | "Jump game, partition, range sum queries" | 30 min |
| 07 | [String Search — KMP & Rabin-Karp](70.2.1.07-string-search-kmp-rabin-karp.md) | "Find substring, pattern matching, rolling hash" | 30 min |

---

## Planned additions

- **70.2.1.04 — Linked List Manipulation Patterns** *(upcoming)*: reversal, cycle detection, merge, fast/slow pointers. Slot reserved; not yet written.

---

## Recognition drill

```text
"Longest substring without repeating chars" → Sliding Window
"Two sum in sorted array"                   → Two Pointers
"Find first/last position"                  → Binary Search
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
