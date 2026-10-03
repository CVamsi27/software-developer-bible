<!-- section: Database | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Database — Querying And Optimization Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Database Indexes

Source: [Database Indexes](20.4.2.01-indexes.md)

**Q:** What core constraint explains why unordered data requires o(n) search. governs database indexes?

**A:** To answer "where is customer 42?" without structure, the engine must look at every row. Any sub-linear lookup demands *precomputed order* — which is all an index is: a sorted (or hashed) copy of one column's values, with pointers back.

**Q:** What core constraint explains why the trade is unavoidable: every index taxes every write. governs database indexes?

**A:** A table with N indexes pays N index maintenance costs per insert/update. So indexes are not free wins — they're a portfolio chosen from *observed query patterns*, and unused ones are pure tax.

**Q:** What core constraint explains why order matters in composite indexes governs database indexes?

**A:** (leftmost prefix rule) because a B-tree is sorted lexicographically — an index on `(a, b)` serves `WHERE a` and `WHERE a AND b` but not `WHERE b` alone. This one fact explains most "why isn't my index used" mysteries.

## SQL Joins

Source: [SQL Joins](20.4.2.02-joins.md)

**Q:** What core constraint explains why nested loop is the naive baseline governs sql joins?

**A:** — n×m comparisons. Correct but quadratic; only wins when one side is tiny (or an index turns the inner lookup into O(1)) — which is exactly when the planner picks it.

**Q:** What core constraint explains why sorting creates matchable neighborhoods. governs sql joins?

**A:** Sort-merge join sorts both sides once (n log n), then merges in one pass — the win when data is already ordered or output needs ordering anyway.

**Q:** What core constraint explains why hashing creates direct addressing. governs sql joins?

**A:** Build a hash table on the smaller side, probe with the larger — O(n+m) when memory holds the build side. Memory is its binding constraint, which is why huge joins spill and degrade.

## Execution Plans & Query Optimization

Source: [Execution Plans & Query Optimization](20.4.2.03-execution-plans.md)

**Q:** What core constraint explains why you state *what*, the engine chooses *how*. governs execution plans & query optimization?

**A:** That "how" — the plan — is where all performance lives, so reading plans is not optional expertise. The plan is a tree of physical operators (seq scan, index scan, hash join) with row estimates at every node.

**Q:** What core constraint explains why estimates drive everything. governs execution plans & query optimization?

**A:** The planner is a cost model over estimated row counts; when estimates diverge from actuals (stale stats, type mismatches, correlated predicates), the chosen plan is optimizing the wrong world. `ANALYZE` and `EXPLAIN ANALYZE` (estimates vs actuals side by side) exist precisely to expose this.

**Q:** What core constraint explains why read plans bottom-up for cost, top-down for shape. governs execution plans & query optimization?

**A:** The innermost nodes produce rows; each level combines. The senior scan: find the biggest cost node, check its estimate-vs-actual gap, then ask what input shape it received — because the fix is almost always upstream (index, stats, or query reshape).

## PostgreSQL Window Functions

Source: [PostgreSQL Window Functions](20.4.2.04-window-functions.md)

**Q:** What core constraint explains why aggregate-without-collapsing requires a new kind of function. governs postgresql window functions?

**A:** GROUP BY destroys rows to make one output row per group; but "share of total per row" needs every row *kept* and a computation over its peers. Window functions are that: a partition-wise computation exposed alongside each row.

**Q:** What core constraint explains why partition + order + frame = the whole grammar. governs postgresql window functions?

**A:** PARTITION BY defines the peer group, ORDER BY sequences within it, the frame clause bounds which rows contribute (running vs moving). Every window need decomposes into these three choices — memorizing functions is unnecessary once the grammar is held.

**Q:** What core constraint explains why they execute after joins/where/having, before order by governs postgresql window functions?

**A:** — which is why you can't filter windows in WHERE and why the subquery-with-window-outer-filter pattern exists.

## PostgreSQL JSONB

Source: [PostgreSQL JSONB](20.4.2.05-jsonb.md)

**Q:** What core constraint explains why some data has no fixed shape worth a table. governs postgresql jsonb?

**A:** Product attributes, integration payloads, ML feature vectors — forcing them into 40 nullable columns creates sparse-table misery; storing them as opaque text loses queryability. JSONB is the compromise: parsed, indexable hierarchy *inside* a relational row.

**Q:** What core constraint explains why the trade is write cost and statistics. governs postgresql jsonb?

**A:** Parsed structure per value costs writes; internal keys aren't first-class columns, so the planner estimates poorly on JSONB predicates and GIN indexes trade size for lookup. The discipline: relational columns for what you query and join on *in bulk*, JSONB for what you occasionally reach into.

**Q:** What core constraint explains why it is not an excuse to skip schema design governs postgresql jsonb?

**A:** — validation moves to CHECK constraints and app-layer schema (zod) — it just changes *where* the schema lives.

## Summary

Use these prompts after the reading pass to recall the querying and optimization mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
