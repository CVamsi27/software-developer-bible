<!-- section: Coding Patterns | category: Reference | tags: revision, practi | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Linear Structures — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Sliding Window

Source: [Sliding Window](70.2.1.01-sliding-window.md)

**Q:** What property permits moving a window's left boundary without revisiting discarded starts?

**A:** The validity/optimality constraint must support monotone movement, and entering/leaving elements must update state efficiently. Arbitrary negative-sum constraints may break the usual shrinking proof.

## Two Pointers

Source: [Two Pointers](70.2.1.02-two-pointers.md)

**Q:** What justifies discarding an endpoint in sorted two-sum?

**A:** If the smallest candidate plus the right endpoint is too large, every larger left value with that right endpoint is also too large; the symmetric argument discards left for a too-small sum.

## Binary Search

Source: [Binary Search](70.2.1.03-binary-search.md)

**Q:** How does a lower-bound search differ from stopping on equality?

**A:** It preserves a search interval that can still contain an earlier match and moves the right boundary after equality. Verify the returned insertion position before treating it as a found value.

## Linked List Manipulation Patterns

Source: [Linked List Manipulation Patterns](70.2.1.04-linked-list-manipulation-patterns.md)

**Q:** Why save next before reversing a linked-list pointer?

**A:** The original forward link is lost when next is overwritten. Saving it preserves access to the unreversed suffix while the prefix is reconnected.

## Intervals

Source: [Intervals](70.2.1.05-intervals.md)

**Q:** Why can sorting intervals by start simplify merging?

**A:** Potential overlaps become adjacent in traversal. Track the merged interval's maximum end, then emit it only when a later start lies outside the chosen closed/half-open convention.

## Greedy & Prefix Sum

Source: [Greedy & Prefix Sum](70.2.1.06-greedy-prefix-sum.md)

**Q:** Why does a prefix-sum hash map handle negative values where a simple sum window may fail?

**A:** Each subarray sum is a difference of prefixes. Counting previous prefix values equal to current minus target does not depend on sums changing monotonically as endpoints move.

## String Search — KMP & Rabin-Karp

Source: [String Search — KMP & Rabin-Karp](70.2.1.07-string-search-kmp-rabin-karp.md)

**Q:** What information lets KMP avoid comparing an already matched prefix again?

**A:** The prefix-function/LPS table records the longest proper prefix that is also a suffix. It supplies the next viable matched length after a mismatch.

## Summary

Keep a boundary invariant for every window or search; state the endpoint convention for intervals. For strings and lists, preserve the suffix or prefix information needed after each movement.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
