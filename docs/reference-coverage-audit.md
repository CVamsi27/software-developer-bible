# Reference Coverage Audit — Backend/System-Design Videos vs the Bible

> **Dated review record:** counts, test results and remaining-work statements below describe the recorded pass. Use the [current review progress](2026-10-25-fullstack-coverage-review.md) and [verification runbook](verification-gates.md) for present scope; chapter existence and passing scans do not establish complete reader review.

**Date:** 2026-09-16 · **Method:** each reference's topic list (video chapter markers pulled from the channel feed, where published) mapped to the chapter that teaches it. Anything without a dedicated home was treated as a gap and either written or explicitly scoped out.

**References audited**

| # | Reference | What it covers |
| - | --- | --- |
| 1 | [Let's Handle 1 Million Requests per Second](https://www.youtube.com/watch?v=W4EwfEU8CGA) | High-scale HTTP on AWS: load balancing, autoscaling, caching layers, DB read scaling, async offload, capacity thinking |
| 2 | [Backend from first principles](https://www.youtube.com/playlist?list=PLui3EUkuMTPgZcV0QhQrOcwMPcBCcd_Q1) (Sriniously, ~19 videos) | The full backend surface — HTTP, request lifecycle, data, ops — with chapter markers on the roadmap video |
| 3 | [7 Database Laws of Senior Backend Developer](https://www.youtube.com/watch?v=2snYdgNcxIg) | Choosing and designing around a database |
| 4 | [8 API Laws of Senior Backend Developer](https://www.youtube.com/watch?v=-40xErgJIBg) | REST API design: naming, methods, status, idempotency, paging, sorting, versioning, security |

## Verdict

**36 of 39 topics already had dedicated chapters.** Three were genuinely missing and are now written; one was thin and has been extended.

Coverage is judged at **chapter** level, not mention level: a topic "covered" only by passing references in other chapters was treated as a gap.

## Gaps found and closed

| Gap | Evidence it was missing | Fix |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Serialization & wire formats** | Roadmap topic (05:04 "Serialisation and deserialisation"); protobuf/MessagePack appeared only inside gRPC and design-pattern chapters, with no treatment of JSON's real limits (64-bit precision, dates, `undefined`), format choice, or schema evolution | New chapter **20.3.3.06 Serialization & Wire Formats** |
| **Transactional email & notification delivery** | Roadmap topic (20:04); a repo-wide search for `transactional email` returned **zero** matches — no chapter, no section, no code | New chapter **20.3.3.07 Transactional Email & Notification Delivery** |
| **Request context (AsyncLocalStorage)** | Roadmap topic (14:03 "Request context"); `AsyncLocalStorage` appeared only inside a Prisma multi-tenancy snippet and one interview skeleton — nothing taught the mechanism, the boundaries that lose it, or ALS vs request-scoped DI | New chapter **20.2.2.06 Request Context & AsyncLocalStorage** |
| **Filtering / sorting / field selection** | "Sorting" and "cross-resource references" are named in the API-laws list; the bible covered them only as query parameters inside the pagination chapter | New section **“Filtering, Sorting & Field Selection”** in 20.3.3.01 (allow-listing, filter-to-index mapping, sparse fieldsets, echoing applied filters) |

## Playlist topics → chapters (all 30 roadmap items)

| Roadmap topic | Chapter |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTTP protocol | [20.3.2.01 HTTP Methods](../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.01-http-methods.md), [20.3.2.02 Status Codes](../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.02-status-codes.md), [30.2.1.21 TCP/UDP Transport](../30-architecture/30.2-system-design/01-theory/30.2.1.21-tcp-udp-transport-fundamentals.md) |
| Routing | [20.2.1.02 Controllers](../20-backend/20.2-nestjs/01-core-architecture/20.2.1.02-controllers.md) (+ [10.4.1.02 App Router](../10-frontend/10.4-next.js/01-rendering-fundamentals/10.4.1.02-app-router.md) for the frontend side) |
| Serialisation / deserialisation | **NEW** [20.3.3.06](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.06-serialization-and-wire-formats.md) |
| Authentication & authorisation | [20.5.1.01 Auth Fundamentals](../20-backend/20.5-security/01-auth/20.5.1.01-auth-fundamentals.md), [20.3.4.04 Authentication](../20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.04-authentication.md) |
| Validation & transformation | [20.2.2.03 Pipes](../20-backend/20.2-nestjs/02-request-lifecycle/20.2.2.03-pipes.md) |
| Middlewares | [20.2.2.01 Middleware](../20-backend/20.2-nestjs/02-request-lifecycle/20.2.2.01-middleware.md) |
| Request context | **NEW** [20.2.2.06](../20-backend/20.2-nestjs/02-request-lifecycle/20.2.2.06-request-context-and-async-local-storage.md) |
| Handlers, controllers, services (BLL) | [20.2.1.02 Controllers](../20-backend/20.2-nestjs/01-core-architecture/20.2.1.02-controllers.md), [20.2.1.03 Providers](../20-backend/20.2-nestjs/01-core-architecture/20.2.1.03-providers.md), [20.2.1.04 DI](../20-backend/20.2-nestjs/01-core-architecture/20.2.1.04-dependency-injection.md) |
| CRUD deep-dive | [20.4.4.01 Prisma](../20-backend/20.4-database/04-orm-and-access/20.4.4.01-prisma.md), [20.4.1.02 Normalization](../20-backend/20.4-database/01-postgresql-foundations/20.4.1.02-normalization.md) |
| RESTful architecture & best practices | [20.3.1.02 REST Principles](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.02-rest-principles.md), [20.3.1.04 Maturity Model](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.04-rest-maturity-model.md) |
| Databases | [20.4.1.01 PostgreSQL](../20-backend/20.4-database/01-postgresql-foundations/20.4.1.01-postgresql.md), [20.4.1.04 NoSQL vs SQL](../20-backend/20.4-database/01-postgresql-foundations/20.4.1.04-nosql-vs-sql.md) |
| Caching | [20.8.01 Caching Deep-Dive](../20-backend/20.8-caching/20.8.01-caching-deep-dive.md), [30.2.1.05 Caching Patterns](../30-architecture/30.2-system-design/01-theory/30.2.1.05-caching-patterns.md) |
| Transactional emails | **NEW** [20.3.3.07](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.07-transactional-email-and-notifications.md) |
| Task queuing & scheduling | [20.2.4.04 Scheduling & Background Jobs](../20-backend/20.2-nestjs/04-quality-and-operations/20.2.4.04-scheduling-background-jobs.md), [30.2.1.06 Queues & Async](../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md) |
| Elasticsearch | [20.4.5.05 Search Infrastructure at Scale](../20-backend/20.4-database/05-operations-and-scaling/20.4.5.05-search-infrastructure-at-scale.md) |
| Error handling | [20.3.3.02 Error Handling Design](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.02-error-handling-design.md) |
| Config management | [20.2.4.01 Configuration & Validation](../20-backend/20.2-nestjs/04-quality-and-operations/20.2.4.01-configuration-validation.md), [20.1.3.03 Process Environment](../20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.03-process-environment.md) |
| Logging, monitoring, observability | [40.4.1.01 Logging](../40-platform/40.4-observability/01-pillars/40.4.1.01-logging.md), [40.4.1.02 Monitoring](../40-platform/40.4-observability/01-pillars/40.4.1.02-monitoring.md), [40.4.1.03 Tracing](../40-platform/40.4-observability/01-pillars/40.4.1.03-tracing.md) |
| Graceful shutdown | [20.2.4.03 Lifecycle Hooks & Graceful Shutdown](../20-backend/20.2-nestjs/04-quality-and-operations/20.2.4.03-lifecycle-hooks-graceful-shutdown.md), [30.3.1.01 Health Checks & Graceful Shutdown](../30-architecture/30.3-infra-patterns/01-liveness-lifecycle/30.3.1.01-health-checks-graceful-shutdown.md) |
| Security | [20.5 Security stack](../20-backend/20.5-security/) (auth, attacks & defence, API security) |
| Scaling & performance | [30.2.1.04 Load Balancing](../30-architecture/30.2-system-design/01-theory/30.2.1.04-load-balancing.md), [30.2.1.12 Capacity Planning](../30-architecture/30.2-system-design/01-theory/30.2.1.12-capacity-planning.md), [40.2.3.01 HPA Scaling](../40-platform/40.2-kubernetes/03-scaling/40.2.3.01-hpa-scaling.md) |
| Concurrency & parallelism | [20.1.3.01 Clustering](../20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.01-clustering.md), [20.1.3.02 Child Processes & Workers](../20-backend/20.1-node.js/03-processes-and-concurrency/20.1.3.02-child-processes-workers.md), [20.13.03 Java Concurrency](../20-backend/20.13-java/20.13.03-java-concurrency-multithreading.md) |
| Object storage & large files | [20.3.3.04 File Upload APIs](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.04-file-upload-apis.md) (multipart, presigned direct-to-S3, resumable) |
| Real-time backend systems | [60 Realtime stack](../60-realtime/) (WebSockets, SSE, WebTransport, scaling, NestJS gateways) |
| Testing & code quality | [50 Quality stack](../50-quality/) (test pyramid, frameworks, performance budgets, a11y) |
| 12-factor app | [40.9 Twelve-Factor](../40-platform/40.9-twelve-factor/) |
| OpenAPI standards | [20.3.1.05 OpenAPI & Swagger](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.05-openapi-swagger.md) |
| Webhooks | [20.3.3.05 Webhooks](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.05-webhooks.md) |
| DevOps for backend engineers | [40.3 CI/CD](../40-platform/40.3-ci-cd/), [40.1 Docker](../40-platform/40.1-docker/), [40.2 Kubernetes](../40-platform/40.2-kubernetes/) |

## "1 Million Requests per Second" → chapters

| Topic the video exercises | Chapter |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Load balancing (L4/L7, algorithms, health checks) | [30.2.1.04](../30-architecture/30.2-system-design/01-theory/30.2.1.04-load-balancing.md), [40.11.01 Nginx Internals](../40-platform/40.11-reverse-proxy/40.11.01-nginx-reverse-proxy-internals.md) |
| Horizontal scaling & autoscaling | [40.2.3.01 HPA](../40-platform/40.2-kubernetes/03-scaling/40.2.3.01-hpa-scaling.md), [40.2.3.02 Node Autoscaling](../40-platform/40.2-kubernetes/03-scaling/40.2.3.02-node-autoscaling-cluster-capacity.md) |
| Edge caching / CDN in front | [30.3.4.03 CDN Architecture](../30-architecture/30.3-infra-patterns/04-data-at-scale/30.3.4.03-cdn-architecture.md), [40.10.02 Multi-CDN Steering](../40-platform/40.10-cdn/40.10.02-multi-cdn-traffic-steering.md) |
| Application-level caching | [20.8.01 Caching Deep-Dive](../20-backend/20.8-caching/20.8.01-caching-deep-dive.md) |
| Database read scaling / sharding | [20.4.3.04 Replication](../20-backend/20.4-database/03-transactions-and-replication/20.4.3.04-database-replication.md), [30.3.4.01 Database Scaling](../30-architecture/30.3-infra-patterns/04-data-at-scale/30.3.4.01-database-scaling.md) |
| Connection pooling under load | [20.4.5.01 Connection Pooling](../20-backend/20.4-database/05-operations-and-scaling/20.4.5.01-connection-pooling.md) |
| Asynchronous offload | [30.2.1.06 Queues & Async](../30-architecture/30.2-system-design/01-theory/30.2.1.06-queues-and-async.md), [20.6.2.05 Message Brokers](../20-backend/20.6-microservices/02-communication-and-messaging/20.6.2.05-message-brokers.md) |
| Rate limiting / shedding abusive traffic | [30.2.1.08 Rate Limiting](../30-architecture/30.2-system-design/01-theory/30.2.1.08-rate-limiting.md), [20.3.4.01 Rate Limiting](../20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.01-rate-limiting.md) |
| Backpressure when consumers lag | [30.2.1.13 Backpressure](../30-architecture/30.2-system-design/01-theory/30.2.1.13-backpressure-and-flow-control.md) |
| Capacity planning (back-of-envelope) | [30.2.1.12](../30-architecture/30.2-system-design/01-theory/30.2.1.12-capacity-planning.md) + case studies in [30.2.2](../30-architecture/30.2-system-design/02-case-studies/) |
| Failure behaviour at scale | [30.2.1.10 Failure Modes](../30-architecture/30.2-system-design/01-theory/30.2.1.10-failure-modes.md), [30.3.2.01 Resilience Patterns](../30-architecture/30.3-infra-patterns/02-failure-and-recovery/30.3.2.01-resilience-patterns.md) |

## Database laws → chapters

| Law area | Chapter |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Choosing relational vs NoSQL by access pattern | [20.4.1.04 NoSQL vs SQL](../20-backend/20.4-database/01-postgresql-foundations/20.4.1.04-nosql-vs-sql.md) |
| Model first: normalization and constraints | [20.4.1.02 Normalization](../20-backend/20.4-database/01-postgresql-foundations/20.4.1.02-normalization.md) |
| Index for the queries you actually run | [20.4.2.01 Indexes](../20-backend/20.4-database/02-querying-and-optimization/20.4.2.01-indexes.md), [20.4.2.03 Execution Plans](../20-backend/20.4-database/02-querying-and-optimization/20.4.2.03-execution-plans.md) |
| Transactions and isolation realities | [20.4.3.01 Transactions](../20-backend/20.4-database/03-transactions-and-replication/20.4.3.01-transactions.md), [20.4.1.03 MVCC](../20-backend/20.4-database/01-postgresql-foundations/20.4.1.03-mvcc.md) |
| Capacity and consistency trade-offs (CAP/PACELC) | [30.2.1.01 CAP](../30-architecture/30.2-system-design/01-theory/30.2.1.01-cap-theorem.md), [30.2.1.02 Consistency Models](../30-architecture/30.2-system-design/01-theory/30.2.1.02-consistency-models.md) |
| Connection management | [20.4.5.01 Connection Pooling](../20-backend/20.4-database/05-operations-and-scaling/20.4.5.01-connection-pooling.md) |
| Growing past one node | [20.4.3.04 Replication](../20-backend/20.4-database/03-transactions-and-replication/20.4.3.04-database-replication.md), [30.2.1.03 Sharding & Replication](../30-architecture/30.2-system-design/01-theory/30.2.1.03-sharding-and-replication.md) |
| Migrations without downtime | [20.4.5.02 Migration Strategies](../20-backend/20.4-database/05-operations-and-scaling/20.4.5.02-migration-strategies.md), [30.3.5.01 Zero-Downtime Deployments](../30-architecture/30.3-infra-patterns/05-shipping-and-evolution/30.3.5.01-zero-downtime-deployments.md) |
| Backups and recovery | [20.4.5.04 Backups, PITR](../20-backend/20.4-database/05-operations-and-scaling/20.4.5.04-backups-pitr-recovery.md), [30.3.2.05 Backup Strategy](../30-architecture/30.3-infra-patterns/02-failure-and-recovery/30.3.2.05-backup-strategy-restore-drills.md) |
| Choosing a database in an interview | [70.3.04 Backend Cheat Sheet](../70-interview-toolkit/70.3-cheatsheets/70.3.04-backend-cheat-sheet.md) |

## API laws → chapters

| Law area | Chapter |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Resource naming (nouns, consistency) | [20.3.1.02 REST Principles](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.02-rest-principles.md) |
| Correct methods and idempotency | [20.3.2.01 HTTP Methods](../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.01-http-methods.md), [30.3.2.03 Idempotency Keys](../30-architecture/30.3-infra-patterns/02-failure-and-recovery/30.3.2.03-idempotency-keys.md) |
| Honest status codes | [20.3.2.02 Status Codes](../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.02-status-codes.md) |
| Error contract (problem details) | [20.3.3.02 Error Handling Design](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.02-error-handling-design.md) |
| Pagination | [20.3.3.01 Pagination](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.01-pagination.md) |
| Filtering, sorting, field selection | [20.3.3.01 — Filtering/Sorting/Field Selection section](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.01-pagination.md) |
| Versioning without breaking clients | [20.3.1.03 Versioning](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.03-versioning.md), [20.3.1.04 Maturity Model](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.04-rest-maturity-model.md) |
| Rate limiting and abuse control | [20.3.4.01 Rate Limiting](../20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.01-rate-limiting.md) |
| Auth and security on the API edge | [20.3.4.04 Authentication](../20-backend/20.3-rest-apis/04-edge-and-scale/20.3.4.04-authentication.md), [20.5.2.04 API Security](../20-backend/20.5-security/02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) |
| Documenting the contract | [20.3.1.05 OpenAPI & Swagger](../20-backend/20.3-rest-apis/01-design-and-contract/20.3.1.05-openapi-swagger.md) |
| Serialization choices behind the contract | **NEW** [20.3.3.06](../20-backend/20.3-rest-apis/03-payloads-errors-integration/20.3.3.06-serialization-and-wire-formats.md) |

## Deliberate non-goals

Recorded so the audit is not mistaken for an unfinished to-do list:

- **Provider-specific AWS walkthroughs** (exact ALB/ASG console steps in reference #1). The bible teaches the mechanism and the trade-off per topic; step-by-step console recipes for one cloud age badly and duplicate provider documentation.
- **Series intro/motivational videos** (roadmap, "walk the path", "what is a backend"). Covered narratively by [ROADMAP.md](../ROADMAP.md) and the stack INDEXes rather than as study chapters.

## Keeping this honest

The three gaps were found by testing a claim rather than trusting it: the audit treated *"the bible mentions it"* as insufficient, and required a dedicated chapter. Two of the three gaps returned roughly zero matches repo-wide (`transactional email`) or appeared only inside an unrelated chapter's code sample (`AsyncLocalStorage`) — which is exactly the state that looks like coverage in a grep and reads like a hole in an interview.
