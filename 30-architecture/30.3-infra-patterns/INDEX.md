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

---

**Study order:**
1. Database scaling (partitioning, replication, connection pooling)
2. Resilience patterns (circuit breaker, retry, idempotency)
3. Zero-downtime deployments (blue-green, canary, feature flags)
4. Leader election and consensus (Raft, distributed locks)
5. Data pipelines (batch + stream processing)
6. Technical debt management
