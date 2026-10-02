# Heaps, Stacks & Selection

> **Study time:** ≈ 1 h 13 m of reading (6 files, ~12 min average).
> **6 files.** Order-of-access structures and their interview patterns: heaps for top-K and streams, monotonic stacks for next-greater-element, classic stack/queue designs, segment trees for range queries, and quickselect/reservoir sampling for selection under constraints.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Interview-red)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Reading Passes

Read the heap for changing priorities, then the monotonic stack for candidates whose answers become final during a scan. Use the stack/queue chapter for ordering and cache designs. Finish with mutable range aggregates and selection/sampling, where the key question changes from arrival order to query operations or sample guarantees.

## The 5 patterns

| # | File | When to recognize | Read time |
| --: | ------ | ------------------- | ----------: |
| 01 | [Heap](70.2.4.01-heap.md) | "Top K, K-way merge, median of stream, scheduling" | 12 min |
| 02 | [Monotonic Stack](70.2.4.02-monotonic-stack.md) | "Next greater/smaller element, largest rectangle in histogram, daily temperatures" | 12 min |
| 03 | [Stack & Queue Patterns](70.2.4.03-stack-queue-patterns.md) | "LRU cache, sliding window max (deque), min stack, valid parentheses" | 16 min |
| 04 | [Segment Tree](70.2.4.04-segment-tree.md) | "Range sum/min/max query with point updates" | 16 min |
| 05 | [Quick Select & Reservoir Sampling](70.2.4.05-quick-select-reservoir-sampling.md) | "K-th largest without sorting, random sample from a stream" | 15 min |

---

## Choosing quickly

```text
K largest/smallest, streaming?    → Heap
Next/previous greater element?    → Monotonic Stack
O(1) access structure design?     → Stack/Queue Patterns
Many range queries + updates?     → Segment Tree
K-th finite-array element?       → Quick Select
Unknown length, uniform sample?   → Reservoir Sampling
```

---

## Cross-References

- [Recursion & Optimization](../03-recursion-and-optimization/INDEX.md) — DP vs heap-greedy trade-offs.
- [Linear Structures](../01-linear-structures/INDEX.md) — sliding window max pairs the deque with window logic.

---

## Navigation

[← Recursion & Optimization](../03-recursion-and-optimization/INDEX.md) · [↑ Coding Patterns Home](../INDEX.md)

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
