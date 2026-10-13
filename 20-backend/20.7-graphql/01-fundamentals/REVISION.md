<!-- section: GraphQL | category: Reference | tags: revision | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-GraphQL-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# GraphQL — Fundamentals Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## GraphQL Overview

Source: [GraphQL Overview](20.7.1.01-graphql-overview.md)

**Q:** How does client field selection support different response needs?

**A:** Each operation selects its requested fields within the schema. This supports different client views, while resolvers and underlying services still determine the actual work performed.

**Q:** How does schema validation constrain an executable GraphQL operation?

**A:** Validation checks names, argument types, variable use and selection structure. A valid operation still requires authorization, cost controls and correct runtime values.

**Q:** Which data-access, query-cost and caching problems remain with GraphQL?

**A:** Nested access can create N+1 calls and costly queries. HTTP caching needs a deliberate transport and representation policy; GraphQL can support GET queries, so POST-only behavior is not universal.

## Schema Design

Source: [Schema Design](20.7.1.02-schema-design.md)

**Q:** Why should a public GraphQL schema model consumer needs rather than database tables?

**A:** The schema is a public contract shaped for client use. Directly exposing tables can freeze storage structure into that contract; resolvers let the database evolve behind a stable API.

**Q:** How does field nullability change error propagation?

**A:** A failing non-null field propagates the error to a nullable ancestor, potentially the root. Choose nullability from data and failure semantics rather than marking every field nullable or non-null mechanically.

**Q:** How do interfaces and unions describe alternative result types?

**A:** Interfaces expose shared fields across implementing object types; unions expose alternatives without shared fields. Clients use type conditions to select fields on the possible concrete results.

**Q:** What does a OneOf input object (`@oneOf`) guarantee for a lookup?

**A:** Exactly one alternative must be supplied and non-null. Its SDL fields stay nullable and have no defaults so the selected alternative remains distinguishable. The directive validates input shape; the resolver still checks authorization and existence.

## Queries & Mutations

Source: [Queries & Mutations](20.7.1.03-queries-mutations.md)

**Q:** Which mutation fields does GraphQL serialize, and what does that not guarantee?

**A:** Only top-level fields of one mutation operation execute serially. Nested fields may resolve normally, separate requests can overlap and GraphQL does not supply transaction rollback.

**Q:** Why should GraphQL inputs use typed variables rather than query-text interpolation?

**A:** Variables separate typed values from document syntax and support reusable operations. Validation and resolver-level input checks remain necessary; automatic persisted-query negotiation is not an allowlist by itself.

**Q:** How can execution errors coexist with partial response data?

**A:** Execution can return data with field errors, depending on nullability propagation. Parse or validation errors occur before execution and return no partial data; a non-null failure can also null the whole execution result.

## Trace and Changed-Condition Checks

Source: [Overview](20.7.1.01-graphql-overview.md)

**Q:** Why does selecting an unknown nickname field prevent the user lookup in the example?

**A:** The parsed operation fails schema validation before execution, so the root resolver is not called. A resolver failing for a valid selected field is a different, execution-time outcome.

**Q:** Does selecting only a post title prove the database fetched only that column?

**A:** No. It constrains the response selection; the resolver or data-access plan determines what storage work occurs.

Source: [Schema design](20.7.1.02-schema-design.md)

**Q:** A user's required name fails while another root post succeeds. What remains in the response?

**A:** The nullable user becomes null, the unrelated post can remain, and the error path names the failing user/name field. Making the user root non-null can instead propagate the failure to all data.

**Q:** Why cannot SearchResult expose id directly even though both union members have one?

**A:** A union declares alternative object types without declaring shared fields. Select member fields through fragments; an interface can declare a common id contract.

**Q:** Does declaring DateTime or @auth install date validation or a permission check?

**A:** No. The scalar needs parsing/serialization behavior and the directive needs a corresponding implementation. Names and generated types alone do not enforce those contracts.

Source: [Queries and mutations](20.7.1.03-queries-mutations.md)

**Q:** Why does the counter end at five after add(2), rejected add(-1) and add(3)?

**A:** The nullable failed root field permits execution to continue. Root fields complete serially, but GraphQL does not roll back the earlier addition. Making add non-null nulls the data and stops later completion without undoing the first effect.

**Q:** Are an omitted update title, null and an empty string interchangeable?

**A:** No. They are distinct inputs. The service must define each meaning and inspect presence; a truthiness test silently conflates them.

**Q:** What delivery guarantees come from a GraphQL subscription declaration by itself?

**A:** It defines one event-producing root field and result execution for its source events. Transport, authorization changes, ordering, bounded queues and replay after reconnect need separate implementation contracts.

## Summary

Use these prompts after the reading pass to recall the fundamentals mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for GraphQL selection and execution contracts

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
