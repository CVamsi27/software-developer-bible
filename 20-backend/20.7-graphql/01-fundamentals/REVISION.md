<!-- section: GraphQL | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-GraphQL-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# GraphQL — Fundamentals Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## GraphQL Overview

Source: [GraphQL Overview](20.7.1.01-graphql-overview.md)

**Q:** What core constraint explains why the server cannot predict every client's needs. governs graphql overview?

**A:** REST endpoints fix the shape at design time — mobile needs 3 fields, web needs 30; someone over-fetches. GraphQL moves shape-declaration into the request: the client asks exactly, the server resolves exactly.

**Q:** What core constraint explains why the schema is the contract, queries are validated against it. governs graphql overview?

**A:** One typed schema (SDL) from which validation, introspection, tooling, and docs derive — the single-source-of-truth principle  with introspection as the killer feature.

**Q:** What core constraint explains why the costs are the famous ones, and they're structural governs graphql overview?

**A:** N+1 resolution (nested fields → nested resolvers — the dataloader is the answer, not an optimization), query-depth abuse (needs cost limits), and HTTP caching that no longer works (POST everything). Each is REST's cached-free wins being paid back explicitly.

## Schema Design

Source: [Schema Design](20.7.1.02-schema-design.md)

**Q:** What core constraint explains why types model the domain, not the database. governs schema design?

**A:** The moment `UserTable` appears in the schema, the internal model is frozen into the public contract . The schema is the consumer's view; the DB can refactor freely behind resolvers.

**Q:** What core constraint explains why nullability is the schema's honesty axis. governs schema design?

**A:** `String!` vs `String` is a promise to every client about error handling — defaulting everything nullable pushes error handling to clients; over-strict non-null turns data blips into whole-field failures. Nullability is designed per-field, not defaulted globally.

**Q:** What core constraint explains why interfaces/unions model polymorphism governs schema design?

**A:** (`Node` interface, `SearchResult` union) — the schema's answer to "one query, many shapes," and the reason GraphQL APIs age better than fixed-resource REST when the domain has genuine type variety.

## Queries & Mutations

Source: [Queries & Mutations](20.7.1.03-queries-mutations.md)

**Q:** What core constraint explains why queries may run in parallel; mutations must serialize. governs queries & mutations?

**A:** The spec enforces it because reads are independent but writes have order-of-operations hazards — the same read/write asymmetry as CQRS , encoded in the protocol.

**Q:** What core constraint explains why variables exist because string-interpolated queries are injection-shaped. governs queries & mutations?

**A:** Parameterized queries  with typed variables = reusable, cacheable, safe operations — persisted queries are this taken to production (whitelisting, smaller requests).

**Q:** What core constraint explains why errors are partial by design governs queries & mutations?

**A:** errors + partial data can coexist in one response (per-field nullability), because one failed resolver shouldn't void the whole query — a fundamentally different error model than HTTP's all-or-nothing response.

## Summary

Use these prompts after the reading pass to recall the fundamentals mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
