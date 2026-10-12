<!-- section: Database | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Database — Querying And Optimization Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Database Indexes

Source: [Database Indexes](20.4.2.01-indexes.md)

**Q:** Why does finding a row without a suitable index require inspecting many rows?

**A:** Without an access path, the engine may inspect all rows to establish a match or absence. Ordered keys, component lists or block summaries precompute different ways to exclude work; not every index is a sorted copy or guarantees sublinear result retrieval.

**Q:** What write and storage costs does adding an index introduce?

**A:** Indexes store additional entries and add relevant write/WAL/maintenance work. Eligible HOT updates can avoid new ordinary index entries, partial membership matters, and physical cleanup is separate from logical deletion. Measure workload benefits/costs rather than multiplying a universal per-write tax.

**Q:** Why does column order matter in a composite B-tree index?

**A:** A B-tree on `(a, b)` is usually most useful when the query constrains `a`; a query on `b` alone may otherwise traverse many leading-key ranges. PostgreSQL 18 can repeatedly search a low-cardinality leading key and apply the later-key condition, but many distinct leading values make that work unattractive. Check version, statistics and plan.

**Q:** Why did the covering fixture report three heap fetches before vacuum and zero afterward?

**A:** Coverage allowed an Index Only Scan, but before vacuum the relevant pages needed heap visibility checks. The later all-visible bits permitted avoiding those visits. Concurrent updates can clear that state again; coverage is not a permanent no-heap guarantee.

**Q:** What changes when the paid-row query becomes an open-row query?

**A:** The partial index excludes open rows and cannot supply them. Predicate implication, query/operator compatibility and planning parameters decide eligibility; merely retaining the index does not retain its usefulness.

## SQL Joins

Source: [SQL Joins](20.4.2.02-joins.md)

**Q:** When can a nested-loop join be an appropriate plan?

**A:** It repeats inner matching for each outer row. A small/selective outer input and economical inner lookup can fit well; without such support, pair comparisons and output fan-out can dominate. A B-tree lookup is not universally constant-time.

**Q:** How does sorted input help a merge join find matching rows?

**A:** Compatible key order allows the engine to walk inputs and form matches without searching from the start for each row. Existing order can avoid an explicit sort; duplicate groups still produce every qualifying pair. Measure sort and output work.

**Q:** How does a hash join use memory to find matches?

**A:** It builds a key-organized candidate table for one input and probes from the other. Equality, skew, output multiplicity and memory/batches affect work. Spill can increase temporary I/O; this does not imply that an indexed nested loop is always better.

## Join grain and unmatched rows

Source: [Learning chapter](20.4.2.02-joins.md)

**Q:** Why does COUNT(*) over a left join report one row for a patient with no appointment?

**A:** The outer join supplies a NULL-extended placeholder row. COUNT of a non-null appointment identifier counts actual matches and gives zero.

**Q:** When should EXISTS replace a join plus DISTINCT?

**A:** When the required result is each entity with at least one match rather than matching pairs. EXISTS states that presence contract without introducing pair fan-out.

**Q:** What does LEFT LATERAL add to a top-one-per-patient query?

**A:** The subquery can reference each patient, and LEFT preserves patients whose subquery produces no rows. Add a deterministic tie-breaker to the chronological ordering.

**Q:** What changes when the booked predicate moves from LEFT JOIN ON to WHERE?

**A:** ON chooses booked matches while preserving unmatched patients. WHERE then filters the joined result and rejects the NULL-extended status, so Cy disappears. Match counts must still count a non-null appointment identifier.

## Execution Plans & Query Optimization

Source: [Execution Plans & Query Optimization](20.4.2.03-execution-plans.md)

**Q:** What does the execution plan add beyond the SQL query text?

**A:** It shows scans/operators, row-flow structure and estimates; instrumented execution adds observations. Pool wait, network transfer and client decoding remain outside executor time. Lock and I/O waits during execution count toward it; PostgreSQL 18 can separately measure server-side result serialization.

**Q:** What does `Index Searches` add to `loops` in a PostgreSQL 18 plan?

**A:** One node execution can do multiple index searches, such as for an `IN`/`ANY` condition or B-tree skip scan. Read the search count alongside loops to understand repeated access; neither value alone gives the total endpoint latency.

**Q:** How can a generic plan help diagnose parameter-sensitive behavior, and what does it leave out?

**A:** PostgreSQL 18's `EXPLAIN (GENERIC_PLAN)` shows a parameterized plan without concrete values and cannot be combined with `ANALYZE`. Compare it with a safe executed plan using representative values; the generic plan does not show observed runtime work.

**Q:** How can incorrect row-count estimates lead to a poor execution plan?

**A:** The planner is a cost model over estimated row counts; when estimates diverge from actuals (stale stats, type mismatches, correlated predicates), the chosen plan is optimizing the wrong world. `ANALYZE` and `EXPLAIN ANALYZE` (estimates vs actuals side by side) exist precisely to expose this.

**Q:** How should you trace a slow plan from its inputs to its result?

**A:** Follow input rows through filtering, joins, sorting and output; inspect estimates against observed rows and repetition. Rows/time are generally per-loop averages and parent time/buffers include children. LIMIT may stop early, so avoid adding inclusive numbers or labeling the largest cost the measured bottleneck.

**Q:** Does a lower estimated cost prove a lower observed runtime across two different queries?

**A:** No. Cost is a planner estimate under its model, not milliseconds or an independent benchmark. Compare equivalent output, representative parameters and observed rows/loops/buffers; output shape and cache/environment can change work.

**Q:** What happens when EXPLAIN ANALYZE instruments an UPDATE inside a transaction that later rolls back?

**A:** The mutation runs and takes locks; its transactional fixture value changes before rollback. Rollback restores that value, but sequence increments or external effects are not universally undone. Use a safe environment.

## PostgreSQL Window Functions

Source: [PostgreSQL Window Functions](20.4.2.04-window-functions.md)

**Q:** When does a window function solve a problem that GROUP BY cannot?

**A:** `GROUP BY` reduces rows to one output row per group, but a per-row share needs each input row preserved alongside a partition-level total. A window function can calculate both in the same result.

**Q:** What do PARTITION BY, ORDER BY, and the frame clause each control?

**A:** Partition divides the filtered input; window ORDER BY sequences rows and defines peers through equal ordering keys; a frame bounds contributing rows for frame-sensitive functions. Ranking and lag/lead have partition/order semantics rather than treating all functions as frame aggregates. Final output ordering is separate.

**Q:** Why must a query use an outer filter to select rows by a window-function result?

**A:** WHERE decides the input before window calculations exist. Compute the value in a subquery/CTE, then filter outside. Moving a filter outside can deliberately change which rows contributed to ranking/totals; PostgreSQL 18 has no `QUALIFY` clause.

**Q:** Can `lag` skip NULL values in PostgreSQL 18?

**A:** No. PostgreSQL implements `RESPECT NULLS` behavior for `lag`, `lead`, `first_value`, `last_value` and `nth_value`; `IGNORE NULLS` is not implemented.

**Q:** Why do the two salary-80 peers both show 260 with the default running-sum frame?

**A:** The salary-only order makes them peers, and default RANGE extends through the current row's last peer. Explicit ROWS ordered by salary and ID yields 180 then260. last_value also sees its frame unless a full-partition frame is specified.

**Q:** What changes if “top two” means two distinct salary levels rather than two employees?

**A:** Deterministic row_number selects two rows; salary-only dense_rank <=2 includes every peer in the top two salary groups. Adding an ID to rank ordering removes salary-only peers and changes that meaning.

## PostgreSQL JSONB

Source: [PostgreSQL JSONB](20.4.2.05-jsonb.md)

**Q:** When is JSONB useful for data whose fields vary between records?

**A:** It keeps queryable variable attributes inside a relational row while stable identity/tenant/relationships can remain columns. Define the document shape/version and update ownership; flexible syntax does not remove business validation.

**Q:** What write, indexing, and estimation costs come with JSONB?

**A:** Document parsing/new row versions, compatible indexes, value size and whole-row contention all matter. A document GIN does not accelerate every extracted expression. Frequently queried paths can be indexed or promoted to typed columns when their stable constraints/statistics/ownership benefit.

**Q:** Where should validation happen when data is stored in JSONB?

**A:** Validate at the application boundary and enforce required invariants in the database. Cover SQL `NULL`, missing keys, JSON `null`, wrong types, ranges and schema versions; `CHECK` expressions that evaluate to SQL `NULL` pass unless the contract prevents it.

**Q:** In the JSONB fixture, how can note exist while its text extraction is SQL NULL?

**A:** note stores JSON null. Existence is true and jsonb_typeof yields the text null, while ->> yields SQLNULL. A missing key also extracts SQLNULL, so use existence/type to distinguish the states.

**Q:** Why does a stale replacement affect no row, and may `jsonb_path_ops` support a key-existence query?

**A:** The nested update advanced the version from 1 to 2, so a replacement expecting version 1 is rejected. Separately, `jsonb_path_ops` does not support `?`, `?|` or `?&`; use `jsonb_ops` or another compatible path. Whole-row concurrency and operator support are separate contracts.

**Q:** When is `JSON_TABLE` useful, and which boundary should a senior engineer make explicit?

**A:** PostgreSQL 17+ can project matching JSON values into relational rows and typed columns. Choose the row/path shape and define `ON EMPTY` and `ON ERROR` behavior so missing fields and failed conversions do not silently become accepted values.

## Summary

Use these prompts after the reading pass to recall the querying and optimization mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — revisit query shape before selecting an index or interpreting a plan

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
