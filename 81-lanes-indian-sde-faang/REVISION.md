# SDE Preparation — Category Revision

[![Role priority](https://img.shields.io/badge/role--priority-Deferred-lightgrey)](../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../docs/topic-importance.md)



Complete the learning stages in [the index](INDEX.md), then answer from memory. Check the source when your explanation omits a mechanism or boundary.

## [Core CS Fundamentals](81.02-core-cs-fundamentals.md)

**Q:** Why must a timed lock attempt release only after successful acquisition?

**A:** Timeout or interruption may leave the thread without ownership. Unlocking then raises an ownership error and can obscure the actual failure.

**Q:** How can a page fault occur without reading a page from disk?

**A:** The OS may allocate a zero-filled page, handle copy-on-write or reject an invalid access. A fault means the current mapping or permission did not complete the access.

**Q:** Why does reliable TCP transport not establish that an order was recorded?

**A:** TCP transports an ordered byte stream; the application’s commit and acknowledgment are separate events. Failure can leave the business outcome uncertain.

**Q:** What distinguishes flow control from congestion control?

**A:** Flow control limits sending according to receiver capacity. Congestion control responds to network conditions; neither fixes application processing backlog by itself.

**Q:** A consistent lock order prevents which deadlock condition?

**A:** Circular waiting, provided every participant uses the same order. It does not by itself establish fairness or prevent starvation.

## [System Design, APIs & Security](81.03-system-design-apis-security.md)

**Q:** What should you establish before selecting services for a booking system?

**A:** The user operation and invariant, such as preventing two sales of the last seat, plus relevant scope and workload. Trace the operation to choose mechanisms that enforce it.

**Q:** Why does authenticating a user not authorize access to every object?

**A:** Identity and permission are different checks. Authorization must evaluate the requested action and resource within the relevant tenant and policy context.

## [Learning and Retention](81.13-learning-guarantee-system.md)

**Q:** What does a successful recall session establish about future recall?

**A:** Performance on that attempt, not permanent mastery. Test later and with changed examples; adapt the review interval to observed recall.

## [Resume & Negotiation](81.15-resume-negotiation.md)

**Q:** Why does a high coverage percentage not establish that most future regressions will be caught?

**A:** It measures exercised code under the chosen coverage metric, not correctness assertions or future failure detection. State the measured coverage and verified behavior separately.

**Q:** Which difference can make two equal headline offers incomparable?

**A:** One may include a one-time payment, conditional bonus or illiquid equity. Compare annual recurring cash, first-year extras and equity conditions separately.

**Q:** Must you have a competing offer or reject the first offer to negotiate well?

**A:** No. A supported request can use role scope and comparable evidence; accepting suitable terms can also be reasonable. Do not fabricate alternatives or follow universal percentage rules.

## [Compensation Benchmarking](81.22-compensation-benchmarking.md)

**Q:** Why can dividing an initial equity grant by four misstate annual compensation?

**A:** Actual vesting may be uneven or conditional. Use the documented schedule, and add only the portion of each confirmed grant vesting in the compared year.

**Q:** Should an expected refresher be included as guaranteed recurring pay?

**A:** No. Separate confirmed grant schedules from scenarios involving unconfirmed refreshers or raises, and avoid counting an entire grant in several years.

**Q:** Is a bonus withholding percentage the final tax rate on that bonus?

**A:** Not necessarily. Withholding is a payment toward tax; final liability depends on applicable rules and the person’s circumstances.

## [Weekly Study Schedule](81.21-week-study-schedule.md)

**Q:** A planned five-hour task needed eight hours. How should the next week change?

**A:** Use the observed duration and repair needs to adjust allocations within the available budget. Do not preserve the old quota by assuming extra unallocated time or treating unfinished work as complete.

**Q:** Why is a changed example useful before moving to another topic?

**A:** It tests whether the repaired mechanism transfers beyond a memorized solution. The result supplies a better next action than a fixed problem count or invented readiness score.

## [Spaced Repetition](81.10-spaced-repetition-schedule.md)

**Q:** Why should a due date specify which attempt the delay is measured from?

**A:** “Review after seven days” is ambiguous without a starting date. A calendar date tied to the last relevant attempt keeps the schedule consistent and auditable.

**Q:** Does successful card recall establish competence on a whole coding task?

**A:** No. Recall of one prompt and solving a task with changed constraints test different demands. Combine cards with implementation and transfer checks.

## [Daily Study Timer](81.11-daily-study-timer.md)

**Q:** What does completing eight twenty-five-minute blocks establish?

**A:** Two hundred minutes of timed focus if all blocks were completed as recorded. It does not establish correct solutions, retention or interview readiness.

**Q:** What should you preserve when a timed session ends before the task is finished?

**A:** The current hypothesis, failing case and next action, along with actual duration and assistance. Schedule the continuation rather than recording the task as solved.

## [Advanced Topics](81.05-advanced-topics.md)

**Q:** Why does a point-update segment tree not automatically support efficient range changes?

**A:** Its update operation changes one leaf and its ancestors. Range changes need a compatible aggregate/tag design, such as suitable lazy propagation, or another specialized method.

**Q:** What does a right rotation preserve while repairing the 30 → 20 → 10 left-heavy chain?

**A:** Key order remains 10, 20, 30 while 20 becomes the local root. Rewiring and height updates restore the AVL condition in this case; the LL case needs a right rotation.

**Q:** Why is a ParkingSpot class with an isAvailable method insufficient to prevent double assignment?

**A:** Two callers can both observe availability before either changes it. An atomic enforcing operation must make competing claims mutually exclusive.

## [Progress Tracker](81.08-progress-tracker.md)

**Q:** Why should an attempt log include assistance as well as correctness?

**A:** A correct solution after a hint and an unaided solution are different observations. Recording the assistance identifies what needs a later independent check.

**Q:** What should a mock debrief produce besides an activity count or confidence score?

**A:** A specific observed gap, the evidence for it, a focused repair and a changed prompt for rechecking. Those guide the next session without pretending to establish an employer’s bar.

## [Coding Study Plan](81.06-leetcode-study-plan.md)

**Q:** What makes a changed problem useful for testing transfer?

**A:** It changes a condition the mechanism relies on, such as permitted signs, ordering or edge weights. Merely renaming variables leaves the old reasoning untested.

**Q:** Why can a sliding-window argument for positive sums fail when negative elements are allowed?

**A:** Removing an element no longer changes the sum monotonically in the needed direction. Reconsider the invariant and algorithm rather than reusing the template blindly.

**Q:** What should you record after using a hint to solve a problem?

**A:** The missing step, the assistance and the observed result, followed by a focused repair and later unaided variant. Hinted correctness is useful evidence but not the same as independent derivation.

## [Last-Minute Review](81.07-cheat-sheet.md)

**Q:** What makes a technique worth rehearsing before the interview?

**A:** You can explain its invariant, assumptions, complexity and a boundary case. Familiar syntax alone does not establish that you can use it correctly.

**Q:** Why can a variable-length sum window fail when negative values are allowed?

**A:** Removing a negative value increases the sum, so the usual monotonic shrinking rule may not hold.

**Q:** When does a linked-list deletion take constant time?

**A:** When the required node and links or predecessor are already available. Finding them can require linear traversal.

**Q:** How should a timeout change a design discussion?

**A:** Identify which effects may have completed before the timeout and how the caller can discover or safely retry the outcome.

**Q:** What should replace an unsupported improvement percentage in an experience answer?

**A:** State the observed outcome and its evidence, while identifying what was not measured.

## [Quick Reference Cards](81.12-quick-reference-cards.md)

**Q:** What information makes a compressed algorithm reminder usable?

**A:** The state meaning, invariant, assumptions and a boundary trace. An undefined condition hides the central decision.

**Q:** How does a prefix-sum card prevent endpoint confusion?

**A:** Define prefix[i] as the sum of the first i values and use a half-open range [left, right), whose sum is prefix[right] minus prefix[left].

**Q:** What does an incomplete Kahn traversal reveal?

**A:** If correctly computed indegrees yield fewer than V emitted vertices, a directed cycle prevents a topological order.

**Q:** Why is a parent-only check insufficient for BST validation?

**A:** A node must satisfy bounds inherited from every ancestor, not just its immediate parent; the duplicate policy also matters.

**Q:** Why should a saga reminder mention failed compensation?

**A:** Compensation is a separate business operation that can fail or have imperfect effects. It does not provide atomic rollback across services.

## [Flashcard Decks](81.14-flashcard-decks.md)

**Q:** Why does the number of DP dimensions not determine its running time?

**A:** Count reachable states and work per state. A two-dimensional interval table with a linear split loop can require cubic time.

**Q:** Which missing detail makes a maximum-subarray reminder fail on all-negative input?

**A:** The empty-subarray policy and initialization. If a nonempty result is required, initializing the best sum to zero incorrectly permits an empty answer.

**Q:** What must an LCA answer distinguish from returning a node found on one side?

**A:** The lowest common ancestor must contain both targets beneath it or be one target ancestral to the other. An algorithm assuming both exist needs additional presence checks when that guarantee is absent.

**Q:** What changes in undirected cycle detection when parallel edges are allowed?

**A:** Skipping every edge to the parent can hide a parallel-edge cycle. Track the traversed edge identity or account explicitly for edge multiplicity.

**Q:** Why must a prefix-frequency map on a tree be updated during backtracking?

**A:** Remove the current path’s contribution when returning so a sibling does not inherit frequencies from a different root-to-node path.

**Q:** What preserves decreasing stack order for a next-greater-value scan?

**A:** Pop unresolved smaller values when a larger incoming value resolves them, then push the incoming index. Equality handling depends on whether greater means strictly greater.

**Q:** What does a first-field match mean when reimporting Anki text notes?

**A:** Depending on the selected duplicate options and match scope, an existing note may be updated or ignored rather than added. Inspect the preview and settings before import.

## [Microsoft Azure Interviews](81.16-microsoft-azure-interview-guide.md)

**Q:** What should determine whether you rehearse in a plain-text editor?

**A:** The confirmed interview environment, rather than a universal claim based on the company name.

**Q:** Why can a message be redelivered after its business effect committed?

**A:** The worker may fail before successfully settling the broker delivery. Protect the business effect against repeat processing.

**Q:** How does Service Bus duplicate detection differ from business-effect deduplication?

**A:** It filters repeated sends with the same message identity within a configured window; it does not atomically coordinate arbitrary consumer side effects.

**Q:** Can a Cosmos DB account combine strong consistency with multiple write regions?

**A:** No. The supported configuration matters; choose the consistency contract and write topology together.

**Q:** What are the supported finite Azure blob lease durations?

**A:** Between 15 and 60 seconds. Infinite leases are also supported; neither choice automatically protects unrelated external resources.

**Q:** Why might a high-cardinality partition key still produce a hot partition?

**A:** Cardinality describes distinct values, not traffic distribution. One key can receive a disproportionate share of operations.

## [Google Interviews](81.17-google-interview-guide.md)

**Q:** Which part of a solution should you revisit when the interviewer changes the input contract?

**A:** The assumption supporting its invariant, then the implementation and complexity that depend on it.

**Q:** Why can BFS choose the wrong cheapest route in a weighted graph?

**A:** BFS minimizes the number of edges, not the sum of arbitrary edge costs. A longer route can cost less.

**Q:** Why is an LRU cache hit a write to shared state?

**A:** It updates recency. Synchronization must preserve the relationship between the lookup structure and eviction order.

**Q:** Why does a concurrent map plus a concurrent deque not prove a thread-safe LRU cache?

**A:** Individually safe operations do not make updates across the two structures atomic or preserve their combined invariant.

**Q:** Which Spanner configuration should accompany a claim of external consistency?

**A:** Default or serializable transaction isolation; current documentation distinguishes optional repeatable-read behavior.

**Q:** How should you treat a company-tagged question list?

**A:** As possible practice material, without inferring a current company-wide question probability or assessment contract.

## [Amazon Interviews](81.18-amazon-interview-guide.md)

**Q:** What makes a principle label useful in an experience answer?

**A:** It helps interpret an actual decision supported by actions and observations. The label alone supplies no evidence.

**Q:** Why should an unmeasured result remain qualitative?

**A:** An invented percentage cannot be defended. Describe what was actually observed and how it was established.

**Q:** Why should you preserve collaborators in an account of your contribution?

**A:** Distinguishing personal responsibility from shared work is more accurate than claiming every team action as your own.

**Q:** Does an SQS visibility timeout stop the previous receiver from executing?

**A:** No. A delayed receiver can resume after another receiver obtains the message, so business effects need appropriate duplicate and stale-owner protection.

**Q:** Why is DynamoDB TTL deletion insufficient to implement a timely lock expiry?

**A:** Cleanup is asynchronous and can occur days after expiration. Application ownership and expiry checks must govern the protocol.

**Q:** What is the scope of the public SDE II loop schedule cited in the guide?

**A:** The named role’s dated public guidance. Confirm the actual invitation rather than extending it to every level or route.

## [Meta Interviews](81.19-meta-interview-guide.md)

**Q:** Why should authorization be part of a feed trace rather than a later feature?

**A:** Candidate retrieval, caches and ranking must not expose posts outside the viewer’s permitted audience; current access can differ from cached eligibility.

**Q:** Does fan-out on read guarantee fresh results?

**A:** No. Source replication, caches and ranking inputs can still be stale. State the actual freshness contract.

**Q:** Which costs can make fan-out on write unattractive?

**A:** Large recipient sets amplify writes and increase propagation and invalidation work; compare that against read demand.

**Q:** Why can changing ranks complicate pagination?

**A:** Items may move between pages, producing duplicates or omissions unless the contract defines a snapshot or another explicit continuation strategy.

**Q:** Why is setting a reaction state easier to retry than incrementing a counter?

**A:** Repeating the same state-setting operation can preserve the intended effect, whereas an unconditional increment repeats the effect.

**Q:** What authorizes AI tool use in a rehearsal intended to match the interview?

**A:** The actual assessment instructions or recruiting confirmation, rather than another candidate’s reported format.

## [Apple Interviews](81.20-apple-interview-guide.md)

**Q:** What should determine the language used in interview rehearsal?

**A:** The confirmed role and assessment instructions, rather than assuming every Apple role prefers Swift.

**Q:** How do weak and ordinary unowned references differ after the target dies?

**A:** A weak reference becomes nil. An ordinary unowned reference assumes the target remains alive and traps if accessed after deallocation.

**Q:** Why does actor isolation not make a remote-call workflow atomic?

**A:** An await can suspend the method and permit other actor work. Assumptions about state may need revalidation after suspension.

**Q:** Why does the Inventory example keep its check and decrement together?

**A:** They enforce one invariant without a suspension point: an item is decremented only when available, preventing two successful reservations of one item.

**Q:** Does cancellation immediately stop all Swift task work?

**A:** No. Cancellation is cooperative; tasks must observe it and respond with appropriate termination or cleanup.

**Q:** Why can local computation still need a privacy review?

**A:** Stored data, permissions, synchronization and outbound telemetry can expose information even when the central computation runs on the device.

## [SDE Interview Preparation](81.01-complete-guide.md)

**Q:** Why is zero a wrong default maximum for a required nonempty window of all-negative sums?

**A:** It represents an empty choice rather than any valid window. Initialize from a valid window after checking the input contract.

**Q:** Does Big O specify which input case was analyzed?

**A:** No. It describes an asymptotic upper bound; separately state whether the bound is worst-case, expected, amortized or another analysis.

**Q:** Why can printing every subset require more than constant work per subset?

**A:** Materializing or printing its elements costs proportional to its size. Count the output work, not just the branch leaves.

**Q:** Why can comparator subtraction produce an incorrect ordering?

**A:** Subtraction can overflow the numeric range and reverse the intended comparison. Use an appropriate comparison operation.

**Q:** What should follow a mock interview mistake?

**A:** Identify its cause, repair the relevant mechanism and try a changed case; log the assistance required and observed behavior.

**Q:** Which evidence is stronger than a completed problem quota?

**A:** Correct reasoning and implementation on a changed contract, with explicit assumptions and less assistance.

## [Engineering Experience](81.04-devops-behavioral-career.md)

**Q:** What distinguishes intended, tested and observed behavior in an experience answer?

**A:** Intended behavior is the goal; tested behavior is what a stated check established; observed behavior is what actually occurred in the running system.

**Q:** Why does a code revert not establish full recovery?

**A:** Data migrations and external effects may already have happened. Recovery must account for those boundaries separately.

**Q:** Does every Git merge create a merge commit?

**A:** No. A merge can fast-forward when the history and options permit it.

**Q:** Why should a restart be distinguished from fixing an incident’s cause?

**A:** It can mitigate the symptom without establishing or removing the underlying cause. Explain the evidence and follow-up separately.

**Q:** Why are local hooks insufficient as the sole enforcement of required checks?

**A:** They can be absent or bypassed. Enforce required verification at the shared repository or release boundary.

**Q:** What prevents a local benchmark from becoming an unsupported business-impact claim?

**A:** State its environment, input, measurement and scope; do not infer production latency, churn or savings without separate evidence.

## [Mock Interview Question Bank](81.09-mock-interview-question-bank.md)

**Q:** What is the useful purpose of repeating the serialization and LRU tasks in this bank?

**A:** Change their contracts: reject malformed serialized data or preserve cache invariants under concurrency. Repeating the same memorized answer does not test those conditions.

**Q:** Why does a short-code hash need a storage uniqueness rule?

**A:** Different inputs can collide, and concurrent creators can choose the same code. An atomic constraint and explicit conflict policy determine which mapping becomes valid.

**Q:** A chat server stores a message and crashes before acknowledging it. What must a retry preserve?

**A:** A stable message identity and a deduplication contract at the durable and display boundaries. Acknowledgment loss must not create another business message.

**Q:** Why does selecting a nearby driver not reserve that driver?

**A:** Selection reads a candidate state; another worker can select the same driver. An atomic ownership transition must choose a single assignment.

**Q:** A payment times out after the provider accepts it. Why is blindly issuing a new charge unsafe?

**A:** The first effect may exist even though its reply was lost. Reuse the provider's operation identity where supported and look up or reconcile the outcome before treating it as a new charge.

**Q:** What should replace the invented metrics in a sample behavioral answer?

**A:** The candidate's actual actions and supported observations, with the measurement context or explicit limits. A truthful qualitative result is preferable to a copied percentage.

## Summary

A useful answer identifies the shared resource, enforcing mechanism and failure boundary. Revisit its source when those are unclear.

## See Also

- [Category reading flow](INDEX.md)
