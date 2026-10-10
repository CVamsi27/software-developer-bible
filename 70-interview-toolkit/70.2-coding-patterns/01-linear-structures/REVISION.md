<!-- section: Coding Patterns | category: Reference | tags: revision, practice | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Coding%20Patterns-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Linear Structures — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## Sliding Window

Source: [Sliding Window](70.2.1.01-sliding-window.md)

**Q:** What property permits moving a window's left boundary without revisiting discarded starts?

**A:** You need a reason why a discarded start cannot lead to an answer later. For example, in a minimum-length window with positive numbers, extending the right side cannot decrease the sum, so the left side can move forward when the target is reached. With negative numbers, that reasoning fails. Also check that adding and removing an element updates the window state efficiently.

## Two Pointers

Source: [Two Pointers](70.2.1.02-two-pointers.md)

**Q:** What justifies discarding an endpoint in sorted two-sum?

**A:** If the smallest candidate plus the right endpoint is too large, every larger left value with that right endpoint is also too large; the symmetric argument discards left for a too-small sum.

## Binary Search

Source: [Binary Search](70.2.1.03-binary-search.md)

**Q:** How does a lower-bound search differ from stopping on equality?

**A:** A lower-bound search finds the first position whose value is at least the target. Finding an equal value is not enough: an earlier equal value may exist, so keep searching to the left. The result may be an insertion position rather than a match; check that it is inside the array and holds the target.

## Linked List Manipulation Patterns

Source: [Linked List Manipulation Patterns](70.2.1.04-linked-list-manipulation-patterns.md)

**Q:** Why save next before reversing a linked-list pointer?

**A:** Reversing a node changes its next pointer to point backward. Save the original next node first, or you lose the link to the remaining list. Then move to the saved node and repeat.

## Intervals

Source: [Intervals](70.2.1.05-intervals.md)

**Q:** Why can sorting intervals by start simplify merging?

**A:** Sorting by start puts possible overlaps together. Keep the furthest end reached by the current merged interval. When the next start no longer overlaps, save that interval and begin another. Decide whether touching endpoints count as an overlap: [1, 3] and [3, 5] overlap as closed intervals, while [1, 3) and [3, 5) do not.

## Greedy & Prefix Sum

Source: [Greedy & Prefix Sum](70.2.1.06-greedy-prefix-sum.md)

**Q:** Why does a prefix-sum hash map handle negative values where a simple sum window may fail?

**A:** A prefix sum is the total from the beginning up to a position. Subtracting an earlier prefix sum from the current one gives the sum between them. To find a target sum, look for earlier totals equal to current minus target. This works with negative numbers because it does not assume that extending a window increases its sum.

## String Search — KMP & Rabin-Karp

Source: [String Search — KMP & Rabin-Karp](70.2.1.07-string-search-kmp-rabin-karp.md)

**Q:** What information lets KMP avoid comparing an already matched prefix again?

**A:** For the characters matched so far, the LPS table records the longest beginning part that also matches an ending part, excluding the whole matched string. After a mismatch, that overlap tells KMP how much of the match it can keep. It need not compare those characters again.

## Check the Changed Conditions

### Sliding Window

Source: [Sliding Window](70.2.1.01-sliding-window.md)

**Q:** Why does a historical maximum character count work for the replacement-window length, but not prove that the current window is a valid answer substring?

**A:** The stored maximum may exceed the frequency in the current window after its left side advances. It bounds the length search using a frequency reached earlier; reconstructing an actual substring requires checking its current frequencies. The chapter returns a length, not the current window as a witness.

### Two Pointers

Source: [Two Pointers](70.2.1.02-two-pointers.md)

**Q:** What makes the same pointer movement unsafe on unsorted two-sum input?

**A:** A sum that is too large no longer proves that every larger left index gives a larger value. Sorting first changes the index mapping and may mutate the input; use a value-to-index map if original positions must be returned.

### Binary Search

Source: [Binary Search](70.2.1.03-binary-search.md)

**Q:** Why keep mid when finding a rotated minimum, and what changes with duplicate values?

**A:** Mid itself may be the minimum, so the right boundary becomes mid rather than mid minus one. Equal mid and right values do not identify the sorted side; a duplicates-aware search may need to remove one endpoint and take linear time.

### Linked Lists

Source: [Linked Lists](70.2.1.04-linked-list-manipulation-patterns.md)

**Q:** What should a palindrome check leave behind if callers retain the list?

**A:** Restore the reversed second half before returning, including after a mismatch. Verify the original node identities and successor links, not only the Boolean result. Otherwise a read-like operation silently changes subsequent traversals.

### Intervals

Source: [Intervals](70.2.1.05-intervals.md)

**Q:** Can a meeting ending at 10 and another starting at 10 use one room?

**A:** Yes under half-open meeting ranges: the room becomes free before the next meeting starts. Closed ranges would overlap at 10. Endpoint rules determine both the comparison and how simultaneous start/end events are ordered.

### Greedy and Prefix Sums

Source: [Greedy and Prefix Sums](70.2.1.06-greedy-prefix-sum.md)

**Q:** Why count matching earlier prefix sums before inserting the current prefix when the target is zero?

**A:** Inserting first would let the current prefix match itself, counting an empty subarray. Seed the map with the empty prefix once, count earlier occurrences, then insert the current total. Multiple earlier equal totals represent different nonempty subarrays.

### String Search

Source: [String Search](70.2.1.07-string-search-kmp-rabin-karp.md)

**Q:** What prevents a rolling-hash collision from becoming a false substring match?

**A:** Compare the candidate characters after their hashes agree. Equal hashes filter candidates; they do not prove equality. Many candidates or deliberate collisions can increase verification work, so the bound includes character comparisons rather than promising unconditional linear time.

## Summary

For each window or search, explain why moving a boundary cannot discard the answer. For intervals, state whether endpoints are included. For strings and lists, keep the information needed to continue after moving a pointer.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
