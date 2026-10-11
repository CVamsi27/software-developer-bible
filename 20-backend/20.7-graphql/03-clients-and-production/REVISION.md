<!-- section: GraphQL | category: Reference | tags: revision | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-GraphQL-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../../docs/topic-importance.md)

# GraphQL — Clients and Production Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Apollo Client

Source: [Apollo Client](20.7.3.01-apollo-client.md)

**Q:** How does a normalized cache share an entity across operation results?

**A:** An entity identifier lets responses refer to the same normalized record. Stable key policies are essential; refetching one operation does not guarantee every list membership or aggregate updates automatically.

**Q:** Which identity, freshness and pagination rules must a client cache define?

**A:** Define entity keys, field variants, pagination merges and tolerated staleness. Cached data is a client representation, so invalidation and refetch rules must follow the product's freshness needs.

**Q:** How do cache policies and fetching state interact in a client application?

**A:** Fetch policies choose when cache or network supplies data; error and optimistic-update policies determine what the UI displays during uncertainty. An optimistic UI update is not database optimistic concurrency control.

## Performance & Security

Source: [Performance & Security](20.7.3.02-performance-security.md)

**Q:** Why must an API limit GraphQL work beyond counting HTTP requests?

**A:** One request can select many aliases and expensive nested fields. Bound meaningful cost, depth, input sizes, fan-out and execution resources; a request count alone cannot price that work.

**Q:** Why is disabling introspection insufficient to secure a schema?

**A:** Attackers can infer fields through errors or other artifacts, and known queries can still be expensive or unauthorized. Introspection policy is a separate decision from object authorization and admission; an enforced operation allowlist is stronger than hash negotiation alone.

**Q:** Why must authorization account for fields, objects and resolver paths?

**A:** A single endpoint can reach many objects through different paths. Apply the same resource and tenant policy at authoritative access boundaries, with additional field/property checks where access differs.

## GraphQL Code Generator — Schema Safety & CI

Source: [GraphQL Code Generator — Schema Safety & CI](20.7.3.03-codegen-schema-safety-ci.md)

**Q:** How does code generation project a schema into application types?

**A:** Generation derives result and variable types from the schema and selected operations. Regeneration and compilation can catch incompatibility; static types do not validate arbitrary runtime responses.

**Q:** What can build-time operation validation detect, and what remains a runtime concern?

**A:** Validation catches invalid selections, variable declarations and types against the tested schema. Runtime data, authorization and deployment version skew remain separate concerns; schema diff rules also need real consumer coverage.

**Q:** Why should a project identify one authoritative schema source?

**A:** Choose maintained SDL or code-derived schema as authoritative and regenerate other artifacts. Add consistency checks because generation can still be skipped or run against the wrong schema version.

## Cache, admission and build boundaries

Source: [Apollo Client](20.7.3.01-apollo-client.md)

**Q:** A task's project ID changed in a normalized record. Why can the old project's task list still be wrong?

**A:** Entity normalization updates the task's fields, but cannot infer filtered list membership, counts or order. Explicitly update the relevant list representation or invalidate/refetch the affected operations; test concurrent pages and optimistic rollback.

**Q:** How do network-only and no-cache differ after receiving a result?

**A:** Both fetch rather than satisfying the operation from cache. network-only writes its result into the normalized cache; no-cache does not store that operation result. Neither guarantees the server's data is fresh beyond its own contract.

Source: [Performance and security](20.7.3.02-performance-security.md)

**Q:** Why can an APQ cache contain an expensive document that no developer approved?

**A:** Automatic persisted-query negotiation normally allows a client to submit text after a hash miss. A trusted allowlist accepts only reviewed deployment artifacts. Both still need variable bounds, resource authorization and quotas for repeated requests.

**Q:** Why is depth alone a weak estimate of query work?

**A:** Aliases repeat fields at the same depth and list arguments multiply fan-out. Cost estimates must include bounded arguments and expensive dependencies, then actual concurrency, deadlines and storage limits cap resource consumption.

Source: [Code generation and schema safety](20.7.3.03-codegen-schema-safety-ci.md)

**Q:** What does mapping DateTime to string fail to prove?

**A:** It supplies a compile-time representation but does not parse or validate runtime values. Define server scalar coercion and client decoding separately, and verify that the schema artifact used by codegen matches the deployed contract.

Source: [Apollo Client](20.7.3.01-apollo-client.md) and [Apollo Server](../02-execution/20.7.2.02-apollo-server.md)

**Q:** Can one GraphQL.js major version be assumed compatible across Apollo Client and Apollo Server?

**A:** No. Apollo Client 4.3.3 accepts GraphQL.js 16 or 17, while Apollo Server 5.5.1 declares `^16.11.0`. When practical, share a compatible 16.x runtime in a combined server/client project and check peer dependencies on upgrades.

**Q:** Why can regeneration plus git diff miss a new generated file?

**A:** git diff checks tracked changes and does not include untracked output. A committed-artifact workflow must also reject unexpected untracked files or compare a clean generated directory; compilation and runtime tests remain separate checks.

## Summary

Use these prompts after the reading pass to recall the clients and production mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for normalized state and operation admission

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
