# GraphQL — Index

> **Study time:** ≈ 1 h 31 m of reading (12 files, ~8 min average).
> **12 files** — GraphQL fundamentals from schema design and queries/mutations/subscriptions to resolvers, Apollo Server, Apollo Client, codegen schema safety in CI, performance, security, and interview questions.

[![Files](https://img.shields.io/badge/files-12-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-API-%23ff6b35)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Study GraphQL when the role involves client-selected API composition, graph execution or an existing GraphQL service. Learn its contract and execution costs before choosing a server/client library; compare it with REST using the application's actual access patterns.

## Learning passes

| Pass | Reading | What you should be able to explain |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Contract | [Fundamentals](01-fundamentals/INDEX.md) | Select fields, trace nullability, design inputs and paginate a stable relationship. |
| Execution | [Resolvers and Apollo Server](02-execution/INDEX.md) | Resolve a field tree with scoped policy, ordered batching and an explicit HTTP/context boundary. |
| Consumers and operations | [Clients and production](03-clients-and-production/INDEX.md) | Separate entity/list updates, bound request-specific work and validate generated contract artifacts. |
| Revision | [Fundamentals](01-fundamentals/REVISION.md), [execution](02-execution/REVISION.md), [clients/production](03-clients-and-production/REVISION.md) | Recall mechanisms and their limitations without borrowing the chapter's wording. |
| Interview practice | [Interview preparation](04-interview-prep/INDEX.md) | Adapt all 50 authored prompts to the role and defend a concrete decision with its failure boundary. |

For a back-end role, emphasize authorization paths, storage fan-out, admission and dependency failure. For a front-end role, also trace normalized identity, partial/optimistic data and logout/tenant transitions. For senior architecture work, explain schema ownership, supported-client compatibility and what federation does to cost and trust.

## Project comparison

The [Docita case study](../../projects/docita/INDEX.md) provides source-backed REST/domain design examples. These GraphQL fixtures teach analogous boundaries but do not establish a deployed GraphQL implementation. A Prisma storage schema and an API DTO schema are separate contracts unless an explicit generator connects them; relation loading does not by itself prove N+1 is absent. Keep project evidence and proposed GraphQL designs distinct.

## Cross-References

- [REST APIs](../20.3-rest-apis/INDEX.md) — compare resource/representation contracts and HTTP behavior.
- [React](../../10-frontend/10.3-react/INDEX.md) — UI identity and state transitions.
- [NestJS](../20.2-nestjs/INDEX.md) — transport and domain boundaries.
- [System design](../../30-architecture/30.2-system-design/INDEX.md) — consistency, dependency cost and service ownership.

## Navigation

[← Microservices](../20.6-microservices/INDEX.md) · [Main index](../../INDEX.md) · [Design patterns →](../../30-architecture/30.1-design-patterns/INDEX.md)
