<!-- section: Coding Patterns | category: Reference | tags: revision, practi | role-priority: essential | general-importance: important -->
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

**A:** The next branch often reuses the same list or board. Undo the previous choice so it starts from the correct state. Otherwise it inherits an earlier branch's choices and can miss answers or produce invalid ones.

**Q:** When does pruning preserve correctness?

**A:** Pruning skips a branch. It is safe when you can show that the branch contains no valid answer, or no answer better than the best already found. A guess that a branch is unlikely to help is not that proof and may discard the solution.

## Dynamic Programming

Source: [Dynamic Programming](70.2.3.02-dynamic-programming.md)

**Q:** What makes a memoization key sufficient?

**A:** The key must include everything that can change the answer to the remaining problem. For knapsack, that might include the current item and remaining capacity. Leaving one out can make two different situations share a cached answer incorrectly.

**Q:** Why does loop direction distinguish 0/1 from unbounded knapsack in one dimension?

**A:** In 0/1 knapsack, each item can be used once. Updating capacities from high to low reads results from before that item was added. Updating low to high can read a result already updated with the current item, allowing it to be used again; that suits unbounded knapsack. Follow which earlier result each update reads.

## Bit Manipulation

Source: [Bit Manipulation](70.2.3.03-bit-manipulation.md)

**Q:** Why can JavaScript bitwise operations surprise code handling large integers?

**A:** Bitwise operations on Number values convert them to 32-bit integers. Larger values can lose upper bits, and signed results can become negative. Use them when the input fits the intended 32-bit representation. For wider exact integer bit operations, use BigInt and check that the required operator supports it.

## Summary

Separate branch-local state from memoized subproblem state. Confirm that a pruning rule is safe and that numeric operations fit the chosen representation.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
