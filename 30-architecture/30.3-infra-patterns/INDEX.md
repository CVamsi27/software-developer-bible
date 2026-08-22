# Infrastructure Patterns

> **Database scaling, resilience patterns, deployment strategies, data pipelines** — production-grade infrastructure for senior engineers.

| File | Topics |
|------|--------|
| [30.3.01-database-scaling.md](30.3.01-database-scaling.md) | PostgreSQL partitioning (range, hash, list), replication (streaming, logical), connection pooling (PgBouncer), query optimization, index strategies |
| [30.3.02-resilience-patterns.md](30.3.02-resilience-patterns.md) | Circuit breaker, bulkhead isolation, retry with exponential backoff, idempotency keys, timeout patterns, health checks |
| [30.3.03-leader-election-consensus.md](30.3.03-leader-election-consensus.md) | Raft algorithm, Paxos, database-based leader election, Redis-based leader election, distributed locks (Redlock), fencing tokens |
| [30.3.04-technical-debt.md](30.3.04-technical-debt.md) | Debt types and prioritization, strangler fig pattern, branch by abstraction, test coverage strategy, ADRs |
| [30.3.05-zero-downtime-deployments.md](30.3.05-zero-downtime-deployments.md) | Rolling, blue-green, canary deployments, feature flags, expand-contract migrations, rollback strategies |
| [30.3.06-data-pipelines.md](30.3.06-data-pipelines.md) | Batch ETL, stream processing, data lake architecture (bronze/silver/gold), data quality, backfill strategies |
| [30.3.07-cdn-architecture.md](30.3.07-cdn-architecture.md) | CDN caching strategies, cache invalidation, edge computing (Cloudflare Workers, Vercel Edge), healthcare PHI considerations |
| [30.3.08-event-sourcing-cqrs.md](30.3.08-event-sourcing-cqrs.md) | Event sourcing, CQRS, event store, projections, snapshots, replay, Docita appointment timeline |
| [30.3.09-saga-pattern.md](30.3.09-saga-pattern.md) | Choreography vs orchestration sagas, compensating transactions, state machines, distributed transactions |
| [30.3.10-api-gateway-patterns.md](30.3.10-api-gateway-patterns.md) | Gateway roles, rate limiting, auth, routing, BFF, aggregation, circuit breaking |
| [30.3.11-health-checks-graceful-shutdown.md](30.3.11-health-checks-graceful-shutdown.md) | Liveness vs readiness probes, drain connections, in-flight request handling, Kubernetes integration |
| [30.3.12-distributed-transactions.md](30.3.12-distributed-transactions.md) | 2PC, 3PC, Saga, TCC, outbox pattern, eventual consistency vs strong consistency |

---

**Study order:**
1. Database scaling (partitioning, replication, connection pooling)
2. Resilience patterns (circuit breaker, retry, idempotency)
3. Zero-downtime deployments (blue-green, canary, feature flags)
4. Leader election and consensus (Raft, distributed locks)
5. Data pipelines (batch + stream processing)
6. Event sourcing and CQRS
7. Saga pattern for distributed transactions
8. API gateway patterns
9. Health checks and graceful shutdown
10. Distributed transactions (2PC, Saga, TCC)
11. Technical debt management
