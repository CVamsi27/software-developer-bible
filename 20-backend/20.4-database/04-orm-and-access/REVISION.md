<!-- section: Database | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Database-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Database — Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Prisma ORM

Source: [Prisma ORM](20.4.4.01-prisma.md)

**Q:** What are the two separate outputs of changing a Prisma schema?

**A:** The application needs a matching generated client, while the database needs reviewed migration SQL. Generating types does not apply DDL, and deployment migration execution does not generate the application client.

**Q:** Why must these examples name Prisma6.19.0 explicitly?

**A:** The constructor/generator/pool and $transaction APIs belong to that legacy major contract. Current ORM8 documentation uses different contract/runtime and db.transaction/model APIs; mixing those APIs produces invalid examples.

**Q:** What does a generic argument on $queryRaw establish?

**A:** It tells TypeScript what shape the caller expects. It does not inspect the returned rows, convert PostgreSQL bigint to a JSON number or validate the SQL/interface contract.

**Q:** Why include a second ordering key in a timestamp-based page?

**A:** Several records may share a timestamp. The unique ID breaks ties; skip1 excludes the cursor row. Missing cursor and concurrent insert behavior still require an explicit API policy.

## Prisma Advanced

Source: [Prisma Advanced](20.4.4.02-prisma-advanced.md)

**Q:** Why can two individually atomic transfers still overspend?

**A:** At Read Committed, both can read the same earlier balance before either writes. Put the decision into a conditional update or use the appropriate locks/isolation, plus a database invariant.

**Q:** How does a duplicate outbox event prevent a second stock reservation in the example?

**A:** The stable event ID has a unique constraint. Its insertion failure aborts the transaction, rolling back that attempt's stock decrement. Returning a prior result also requires verifying ownership and matching operation parameters.

**Q:** Why pass a transaction client into a helper?

**A:** Its queries participate on the caller's transaction connection. A root-client query or separately opened transaction escapes that rollback boundary; the v6 transaction client does not expose nested $transaction.

**Q:** How does transaction-local tenant context avoid contaminating the next request?

**A:** set_config with the local flagtrue scopes the value to the transaction. Protected queries must use that same tx connection, with an enabled policy and a runtime role that does not bypass RLS.

## ORM & Query Builder Landscape

Source: [ORM & Query Builder Landscape](20.4.4.03-orm-query-builder-landscape.md)

**Q:** What makes two access-layer benchmarks comparable?

**A:** They must compute the same relational result with equivalent filtering, grouping, ordering, limits, projections and deployment constraints. Fetching whole relation graphs to aggregate in JavaScript is a different workload.

**Q:** Why can a repository interface fail to preserve atomicity during a tool swap?

**A:** A replacement may open another connection or transaction internally. The operation/result interface also needs a transaction-participation and tenant-context contract.

**Q:** What should migration review cover beyond whether a tool generated the SQL?

**A:** Assess locks, data backfill, old/new application compatibility, privileges and rollback/recovery. Automatic diff generation or applying pending history does not prove every production drift or online rollout risk is handled.

## Summary

Use these prompts after the reading pass to recall the mechanism and its limits.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide the API documentation and further reading.
