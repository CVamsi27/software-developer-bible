# MAQ — Category Revision

Read [the experience reconstruction](01-product-engineering.md) first. Technical answers below describe mechanisms; personal examples must come from your actual work.

## Workflow Ownership

Source: [Workflow and service boundaries](01-product-engineering.md#bullet-1-explain-one-recruitment-or-internal-workflow).

**Q:** How do I explain my MAQ work without disclosing client details?

**A:** Describe the user, operation, constraints, personal responsibility and sanitized technical change. Separate the team's scope from the files or decisions you owned. Confidentiality does not require invented scale or outcomes.

**Q:** Why does TypeScript not replace request validation?

**A:** Static types do not validate arbitrary runtime input. Parse input at trusted boundaries and enforce authorization and business invariants separately.

**Q:** When is a shared service pattern a useful abstraction?

**A:** When it centralizes a stable behavior or invariant for actual consumers. If consumers need conflicting behavior, parameterization or separate implementations may be clearer than one overly generic helper.

**Q:** What would substantiate the old 25% faster-delivery claim?

**A:** A defined lead/cycle-time or effort measure, comparable periods and tasks, sample size and a defensible attribution. No such records were supplied, so the current resume describes the engineering work without that percentage.

## API and Database Performance

Source: [Bottleneck investigation](01-product-engineering.md#bullet-2-show-how-you-diagnosed-an-api-bottleneck).

**Q:** In the 50-row practice list, why does running all status requests in parallel not remove N+1?

**A:** It changes scheduling but leaves the per-row query pattern: 51 calls still compete for connections and database work. A scoped batch or suitable join changes the access pattern. Verify result cardinality and authorization as well as query count.

**Q:** If batching takes the query count from 51 to two, can I quote a corresponding endpoint speedup?

**A:** No. Those counts belong to the stated practice scenario. End-to-end speed depends on query cost, pool waiting, network and other work. Measure comparable requests and errors before reporting a latency change.

**Q:** How would I distinguish a slow query from a slow endpoint?

**A:** Trace request stages, query counts/timings, external calls and application processing. A fast database query does not exclude serialization, connection waiting or downstream latency.

**Q:** Why can batching fix N+1 and still introduce a problem?

**A:** It reduces repeated round trips but can fetch too much data, create an expensive join or consume more memory. Verify the needed fields, cardinality, plans and endpoint behavior.

**Q:** How do I justify an index rather than listing indexing as an optimization?

**A:** Connect it to predicates and ordering in an actual query plan. Evaluate selectivity, rows scanned, sort work and the cost to writes/storage under representative data.

**Q:** When would cursor pagination be preferable to offset pagination?

**A:** When large/deep lists and changing data make offset cost or page drift problematic. Define a stable order and tie-breaker; cursors still need scope and filter compatibility.

**Q:** What is a cache-correctness failure in an authorized list endpoint?

**A:** A key omitting tenant, user permission or relevant filters can return another scope's result. Even correctly scoped keys need invalidation and an acceptable freshness policy.

**Q:** How should I answer “Was the 30% latency improvement p95?”

**A:** Do not select a statistic from memory of a percentage alone. The original statistic and records were not supplied; the current resume omits the figure. Explain the actual profiling work you remember, or discuss a newly executed benchmark with its own scope.

## React Components and User Behavior

Source: [Reusable interfaces](01-product-engineering.md#bullet-3-explain-reuse-without-hiding-product-behavior).

**Q:** Which rules belong in a reusable field, and which belong in the workflow?

**A:** Label/error associations, focus and interaction states can be shared field behavior. Approval permissions and business transitions belong in the workflow and server. A generic field must not become the only enforcement point for a product rule.

**Q:** Why separate local form state and cached server state?

**A:** Editing intent and validation belong to the interaction; fetched records have identity, freshness and synchronization concerns. Mirroring everything into local state can create stale copies and conflicting updates.

**Q:** How do I prevent an older search response from replacing a newer one?

**A:** Use correctly keyed requests and cancellation or an explicit current-request guard. Verify the UI with responses arriving out of order; do not assume debounce alone controls completion order.

**Q:** Does memoizing every component guarantee faster rendering?

**A:** No. Compare costs and actual render behavior; unstable inputs, cheap renders and memoization overhead can eliminate the benefit. Measure a specific interaction before choosing an optimization.

**Q:** What can I demonstrate for the keyboard/screen-reader bullet?

**A:** A real component's semantic elements, labels, focus order, error association and status announcements, then keyboard and assistive-technology checks. Identify which work you performed versus a separate practice implementation.

## Delivery and Collaboration

Source: [Release checks and mentoring](01-product-engineering.md#bullet-4-describe-delivery-and-mentoring-with-one-example-each).

**Q:** Why is high coverage insufficient evidence of release quality?

**A:** Executed lines can lack meaningful assertions and integration coverage. Describe a fault an assertion catches, what is mocked and the failures that require another test layer.

**Q:** What makes a migration unsafe even when unit tests pass?

**A:** Old and new application versions may use the schema concurrently, locks/backfills may affect traffic and data may not satisfy a new constraint. Verify compatibility and rollout/recovery with representative data.

**Q:** How do I explain mentoring without claiming a made-up productivity increase?

**A:** Use a real review or pairing example: the problem, reasoning offered, the teammate's decision and an outcome you observed. Keep team results and your influence distinct.

**Q:** What should I do if I understand a technique but cannot remember using it at MAQ?

**A:** Explain it as technical knowledge or a practice exercise. Narrow the resume wording if it implies personal implementation you cannot substantiate.

## Summary

Answer the mechanism clearly, then support personal experience with a real example. Do not fill gaps with invented measurements or incidents.

## See Also

- [MAQ learning index](INDEX.md) — reconstruction and practice order.
