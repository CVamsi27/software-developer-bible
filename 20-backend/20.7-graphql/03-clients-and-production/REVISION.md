<!-- section: GraphQL | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-GraphQL-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# GraphQL — Clients And Production Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Apollo Client

Source: [Apollo Client](20.7.3.01-apollo-client.md)

**Q:** What core constraint explains why a normalized cache (by id) turns query responses into a graph store. governs apollo client?

**A:** Same entity from two queries = one cache entry, auto-updated on refetch — the client-side analog of identity maps . This is what makes GraphQL clients feel magical and also what makes cache bugs subtle.

**Q:** What core constraint explains why cache semantics need explicit design governs apollo client?

**A:** field policies (merge functions for pagination), garbage collection, and invalidation-by-refetch — because the cache is the UI's source of truth, staleness rules are product decisions .

**Q:** What core constraint explains why the fetching layer composes governs apollo client?

**A:** optimistic updates (write the expected result now, reconcile later — the same pattern as optimistic locking , applied to UI), subscriptions for live data, error policies per query. The client is a state manager whose source is a schema.

## Performance & Security

Source: [Performance & Security](20.7.3.02-performance-security.md)

**Q:** What core constraint explains why query complexity must be bounded because the client writes the query. governs performance & security?

**A:** Depth limits, cost analysis, and max-aliases stop the `fragment explosion` / deeply-nested DoS — REST never had this problem because the server fixed the shape. The fix is pricing queries like rate limiting  prices requests.

**Q:** What core constraint explains why introspection is a feature in dev, a map for attackers in prod governs performance & security?

**A:** — disable it in production; same for verbose errors . Persisted queries (whitelist) make both moot: only known queries execute.

**Q:** What core constraint explains why authz is per-field, not per-endpoint. governs performance & security?

**A:** One query touches many resolvers — each must authorize , or the client composes its way past an endpoint-level check. Field-level authZ is GraphQL's version of "every request is untrusted input plus a claim" .

## GraphQL Code Generator — Schema Safety & CI

Source: [GraphQL Code Generator — Schema Safety & CI](20.7.3.03-codegen-schema-safety-ci.md)

**Q:** What core constraint explains why the schema is the type system; codegen projects it into your language. governs graphql code generator — schema safety & ci?

**A:** TypeScript types from SDL mean a renamed field breaks the build, not production — the same fail-fast-at-contract as generated API clients , applied bidirectionally (client ops → typed hooks too).

**Q:** What core constraint explains why operations are validated at build time governs graphql code generator — schema safety & ci?

**A:** against the schema (graphql-inspector-style diffs) — breaking changes are detected in CI by diffing schemas, before any client ships. The contract's evolution becomes a mechanical check.

**Q:** What core constraint explains why the discipline: schema-first with generated types, or code-first with generated sdl — but *one* source of truth governs graphql code generator — schema safety & ci?

**A:** . Two hand-maintained representations of the contract always diverge; the tooling's whole job is making divergence impossible.

## Summary

Use these prompts after the reading pass to recall the clients and production mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
