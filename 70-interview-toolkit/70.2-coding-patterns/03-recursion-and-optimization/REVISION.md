<!-- section: Coding Patterns | category: Reference | tags: revision, practice| general-importance: important| general-importance: important | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Recursion & Optimization — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Backtracking

Source: [Backtracking](70.2.3.01-backtracking.md)

**Q:** Why undo a choice before exploring the next branch?

**A:** Branches share the working state. Without restoration, a sibling sees choices from an earlier branch and enumeration becomes incomplete or incorrect.

**Q:** When does pruning preserve correctness?

**A:** When the excluded branch cannot contain any valid/better answer under the problem constraints. A speed heuristic without that proof can discard the solution.

## Dynamic Programming

Source: [Dynamic Programming](70.2.3.02-dynamic-programming.md)

**Q:** What makes a memoization key sufficient?

**A:** It contains all facts that determine future subproblem outcomes. Omitting remaining capacity, position, or other relevant state can merge different problems incorrectly.

**Q:** Why does loop direction distinguish 0/1 from unbounded knapsack in one dimension?

**A:** Descending capacity prevents the current item from being reused in the same iteration; ascending capacity allows reuse. The recurrence's dependency meaning determines the order.

## Bit Manipulation

Source: [Bit Manipulation](70.2.3.03-bit-manipulation.md)

**Q:** Why can JavaScript bitwise operations surprise code handling large integers?

**A:** Number bitwise operations use 32-bit integer representations, so shifts and masks can truncate or sign values. Use explicit 32-bit contracts or BigInt for wider exact operations.

## Summary

Separate branch-local state from memoized subproblem state. Confirm that a pruning rule is safe and that numeric operations fit the chosen representation.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
