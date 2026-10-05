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

**Q:** Why does finding a row without a suitable index require inspecting many rows?

**A:** To answer "where is customer 42?" without structure, the engine must look at every row. Any sub-linear lookup demands *precomputed order* — which is all an index is: a sorted (or hashed) copy of one column's values, with pointers back.

**Q:** What write and storage costs does adding an index introduce?

**A:** A table with N indexes pays N index maintenance costs per insert/update. So indexes are not free wins — they're a portfolio chosen from *observed query patterns*, and unused ones are pure tax.

**Q:** Why does column order matter in a composite B-tree index?

**A:** A B-tree on `(a, b)` is usually most useful when the query constrains `a`; a query on `b` alone often cannot use it efficiently. PostgreSQL may use skip scans for some data distributions, so check the plan and statistics.

## SQL Joins

Source: [SQL Joins](20.4.2.02-joins.md)

**Q:** When can a nested-loop join be an appropriate plan?

**A:** — n×m comparisons. Correct but quadratic; only wins when one side is tiny (or an index turns the inner lookup into O(1)) — which is exactly when the planner picks it.

**Q:** How does sorted input help a merge join find matching rows?

**A:** Sort-merge join sorts both sides once (n log n), then merges in one pass — the win when data is already ordered or output needs ordering anyway.

**Q:** How does a hash join use memory to find matches?

**A:** Build a hash table on the smaller side, probe with the larger — O(n+m) when memory holds the build side. Memory is its binding constraint, which is why huge joins spill and degrade.

## Execution Plans & Query Optimization

Source: [Execution Plans & Query Optimization](20.4.2.03-execution-plans.md)

**Q:** What does the execution plan add beyond the SQL query text?

**A:** That "how" — the plan — is where all performance lives, so reading plans is not optional expertise. The plan is a tree of physical operators (seq scan, index scan, hash join) with row estimates at every node.

**Q:** How can incorrect row-count estimates lead to a poor execution plan?

**A:** The planner is a cost model over estimated row counts; when estimates diverge from actuals (stale stats, type mismatches, correlated predicates), the chosen plan is optimizing the wrong world. `ANALYZE` and `EXPLAIN ANALYZE` (estimates vs actuals side by side) exist precisely to expose this.

**Q:** How should you trace a slow plan from its inputs to its result?

**A:** The innermost nodes produce rows; each level combines. The senior scan: find the biggest cost node, check its estimate-vs-actual gap, then ask what input shape it received — because the fix is almost always upstream (index, stats, or query reshape).

## PostgreSQL Window Functions

Source: [PostgreSQL Window Functions](20.4.2.04-window-functions.md)

**Q:** When does a window function solve a problem that GROUP BY cannot?

**A:** GROUP BY destroys rows to make one output row per group; but "share of total per row" needs every row *kept* and a computation over its peers. Window functions are that: a partition-wise computation exposed alongside each row.

**Q:** What do PARTITION BY, ORDER BY, and the frame clause each control?

**A:** PARTITION BY defines the peer group, ORDER BY sequences within it, the frame clause bounds which rows contribute (running vs moving). Every window need decomposes into these three choices — memorizing functions is unnecessary once the grammar is held.

**Q:** Why must a query use an outer filter to select rows by a window-function result?

**A:** — which is why you can't filter windows in WHERE and why the subquery-with-window-outer-filter pattern exists.

## PostgreSQL JSONB

Source: [PostgreSQL JSONB](20.4.2.05-jsonb.md)

**Q:** When is JSONB useful for data whose fields vary between records?

**A:** Product attributes, integration payloads, ML feature vectors — forcing them into 40 nullable columns creates sparse-table misery; storing them as opaque text loses queryability. JSONB is the compromise: parsed, indexable hierarchy *inside* a relational row.

**Q:** What write, indexing, and estimation costs come with JSONB?

**A:** Parsed structure per value costs writes; internal keys aren't first-class columns, so the planner estimates poorly on JSONB predicates and GIN indexes trade size for lookup. The discipline: relational columns for what you query and join on *in bulk*, JSONB for what you occasionally reach into.

**Q:** Where should validation happen when data is stored in JSONB?

**A:** — validation moves to CHECK constraints and app-layer schema (zod) — it just changes *where* the schema lives.

## Summary

Use these prompts after the reading pass to recall the querying and optimization mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.

## Join grain and unmatched rows

Source: [Learning chapter](20.4.2.02-joins.md)

**Q:** Why does COUNT(*) over a left join report one row for a patient with no appointment?

**A:** The outer join supplies a NULL-extended placeholder row. COUNT of a non-null appointment identifier counts actual matches and gives zero.

**Q:** When should EXISTS replace a join plus DISTINCT?

**A:** When the required result is each entity with at least one match rather than matching pairs. EXISTS states that presence contract without introducing pair fan-out.

**Q:** What does LEFT LATERAL add to a top-one-per-patient query?

**A:** The subquery can reference each patient, and LEFT preserves patients whose subquery produces no rows. Add a deterministic tie-breaker to the chronological ordering.
