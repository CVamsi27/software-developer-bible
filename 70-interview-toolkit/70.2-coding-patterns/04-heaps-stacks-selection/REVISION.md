<!-- section: Coding Patterns | category: Reference | tags: revision, practice -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Heaps, Stacks & Selection — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Heap

Source: [Heap](70.2.4.01-heap.md)

**Q:** What does a heap guarantee without fully sorting its storage?

**A:** The parent/child ordering makes the extreme element available at the root. Other positions are not globally sorted; push/pop repair only affected paths.

## Monotonic Stack

Source: [Monotonic Stack](70.2.4.02-monotonic-stack.md)

**Q:** Why can each item enter and leave a monotonic stack only once?

**A:** Popping permanently disqualifies that item for future candidates under the invariant. Across the traversal, total pushes plus pops are linear even inside a while loop.

## Stack & Queue Patterns

Source: [Stack & Queue Patterns](70.2.4.03-stack-queue-patterns.md)

**Q:** Why can Array.shift invalidate a claimed linear queue algorithm?

**A:** Removing the front of a dense array can move/reindex later elements. Use a head index, ring buffer, or real deque when the proof needs constant-time front removal.

## Segment Tree & Binary Indexed Tree (BIT)

Source: [Segment Tree & Binary Indexed Tree (BIT)](70.2.4.04-segment-tree.md)

**Q:** Why does assigning a new value through a Fenwick tree require a delta?

**A:** Fenwick updates add contributions. Store the old array value, compute new minus old, update with that delta, then replace the stored value.

## Quick Select & Reservoir Sampling

Source: [Quick Select & Reservoir Sampling](70.2.4.05-quick-select-reservoir-sampling.md)

**Q:** Why must selection account for every value equal to its pivot?

**A:** A three-way partition produces less-than, equal-to, and greater-than groups. A target rank inside the equal group is already resolved; when continuing to the right, subtract both preceding groups. Treating all equal values as one pivot can miscount ranks or repeatedly process a large duplicate group.

**Q:** Why does reservoir sampling require more than proving each item has probability k/n?

**A:** Equal marginal inclusion probabilities do not alone imply a uniform sample of k-element subsets. The reservoir update preserves the uniform-subset invariant as each new item arrives; this also explains why selected positions, rather than arbitrary replacement bias, matter.

## Summary

Distinguish order at the root, monotone candidate order, and partial partition order. For range updates, specify whether the operation adds a delta or replaces a value.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
