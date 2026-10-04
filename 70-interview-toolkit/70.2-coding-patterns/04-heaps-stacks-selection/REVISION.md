<!-- section: Coding Patterns | category: Reference | tags: revision, practi | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Heaps, Stacks & Selection — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Heap

Source: [Heap](70.2.4.01-heap.md)

**Q:** What does a heap guarantee without fully sorting its storage?

**A:** A min-heap keeps each parent no larger than its children, so the root contains a smallest value. A max-heap reverses the comparison. The remaining storage is not fully sorted. Inserting or removing the root repairs only the affected path through the tree.

## Monotonic Stack

Source: [Monotonic Stack](70.2.4.02-monotonic-stack.md)

**Q:** Why can each item enter and leave a monotonic stack only once?

**A:** In a one-pass monotonic-stack algorithm, an item is pushed once. When it is popped, the algorithm has resolved its answer or proved it cannot help later, so it is never pushed again. Across n items, there are at most n pushes and n pops. An inner while loop therefore does not make the total work quadratic.

## Stack & Queue Patterns

Source: [Stack & Queue Patterns](70.2.4.03-stack-queue-patterns.md)

**Q:** Why can Array.shift invalidate a claimed linear queue algorithm?

**A:** Removing the front of a dense array can move/reindex later elements. Use a head index, ring buffer, or real deque when the proof needs constant-time front removal.

## Segment Tree & Binary Indexed Tree (BIT)

Source: [Segment Tree & Binary Indexed Tree (BIT)](70.2.4.04-segment-tree.md)

**Q:** Why does replacing an array value in a sum Fenwick tree require the difference from its old value?

**A:** A sum Fenwick tree adds a change to the stored totals; it does not directly assign a new array value. Keep the old value and add new minus old to the tree. Then save the new value in the array.

## Quick Select & Reservoir Sampling

Source: [Quick Select & Reservoir Sampling](70.2.4.05-quick-select-reservoir-sampling.md)

**Q:** Why must selection account for every value equal to its pivot?

**A:** A three-way partition groups values below, equal to, and above the pivot. If the target position falls in the equal group, the answer is the pivot. To search the higher group with a relative position, subtract the sizes of both earlier groups. Ignoring duplicate counts can select the wrong position or repeatedly revisit many equal values.

**Q:** Why does reservoir sampling require more than proving each item has probability k/n?

**A:** Giving each item the same chance to appear is not enough: the items might still be selected in biased combinations. A uniform sample gives every possible group of k items the same probability. Reservoir sampling preserves that rule as items arrive by choosing whether to admit the new item and, if admitted, which stored position to replace uniformly.

## Summary

Distinguish order at the root, monotone candidate order, and partial partition order. For range updates, specify whether the operation adds a delta or replaces a value.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
