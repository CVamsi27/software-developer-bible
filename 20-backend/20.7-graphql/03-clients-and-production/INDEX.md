# Clients & Production - GraphQL

> **Study time:** ≈ 28 min of reading (4 files, ~7 min average).
> **4 files.** The client side (normalized cache, optimistic UI), production defenses (query depth limits, complexity analysis, persisted queries, field-level auth), and schema-driven codegen with CI safety gates.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Clients%20%26%20Production-%23ff6b35)](../INDEX.md)

## Learning passes

1. Read [Apollo Client](20.7.3.01-apollo-client.md). Trace one normalized entity, an optimistic rollback and a list membership change. Distinguish entity updates from pagination and private-cache lifetime.
2. Read [Performance and security](20.7.3.02-performance-security.md). Explain APQ versus a trusted allowlist, then reject a valid but oversized page and trace resource authorization.
3. Read [Code generation and schema safety](20.7.3.03-codegen-schema-safety-ci.md). Generate the actual client-preset output, compile its consumer and identify what still needs runtime validation.
4. Use [Client and production revision](REVISION.md) before the [interview bank](../04-interview-prep/20.7.4.01-interview-questions.md). Back-end roles can emphasize admission and compatibility; front-end roles should also explain cache/identity transitions.

## Project comparison

Compare the [Docita case study](../../../projects/docita/INDEX.md) with these GraphQL boundaries: tenant policy, response freshness and contract generation matter in either API style. A REST implementation is not proof of Apollo caching, GraphQL query controls or a GraphQL codegen pipeline. Use source-backed project claims separately from proposed GraphQL designs.

## Navigation

[← Execution](../02-execution/INDEX.md) · [GraphQL index](../INDEX.md) · [Interview practice →](../04-interview-prep/INDEX.md)
