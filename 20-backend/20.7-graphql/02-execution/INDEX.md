# Execution - GraphQL

> **Study time:** ≈ 19 min of reading (3 files, ~6 min average).
> **3 files.** How the server resolves fields, uses request-scoped batching for repeated relationship reads, and connects Apollo Server's plugin model, federation and subscription transports to HTTP.

[![Files](https://img.shields.io/badge/files-3-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Execution-%23ff6b35)](../INDEX.md)

## Learning passes

1. Read [Resolvers](20.7.2.01-resolvers.md). Trace parent values, default resolution, ordered batching and a missing author's nullable boundary. Explain why the loader is request-scoped.
2. Read [Apollo Server](20.7.2.02-apollo-server.md). Run the Server 5/Express 5 fixture, then distinguish HTTP authentication from schema execution and resource authorization.
3. Use [Execution revision](REVISION.md) without looking at the answers. Return to a chapter when you cannot explain its failure boundary.
4. Continue to [Clients and production](../03-clients-and-production/INDEX.md), then the [interview bank](../04-interview-prep/20.7.4.01-interview-questions.md).

## Project comparison

The [Docita case study](../../../projects/docita/INDEX.md) describes the repository's REST and domain-service boundaries. Use it to compare where identity and business policy live; these GraphQL examples are study fixtures, not evidence of a deployed Docita GraphQL service. Describe an evaluation or implementation as your experience only when you can substantiate it.

## Navigation

[← Fundamentals](../01-fundamentals/INDEX.md) · [GraphQL index](../INDEX.md) · [Clients and production →](../03-clients-and-production/INDEX.md)
