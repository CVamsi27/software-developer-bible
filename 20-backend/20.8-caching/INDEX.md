# Caching — Index

> **Redis, cache patterns, invalidation strategies** — the biggest latency lever and the classic senior-interview topic.

[![Files](https://img.shields.io/badge/files-2-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

## Study Order

| # | File | Topics |
|---|------|--------|
| 1 | [Caching Deep Dive](20.8.01-caching-deep-dive.md) | Cache hierarchy, patterns (cache-aside, write-through, write-behind), invalidation strategies, stampede prevention, Redis data structures, multi-tenant caching |
| 2 | [Advanced Redis Patterns](20.8.06-advanced-redis-patterns.md) | Distributed locks (Redlock), Lua rate limiting, Pub/Sub, Redis Streams, scripting best practices |

## The Decision Table (memorize)

| Read/write profile | Pattern | Why |
|---|---|---|
| Read-heavy, stale-tolerant | Cache-aside + TTL + jitter | Simplest correct default |
| Read-heavy, needs fresh writes | Write-through | Cache always consistent; write latency ↑ |
| Write-heavy analytics | Write-behind (batch flush) | Throughput ↑; risk window on crash |
| Hot key / thundering herd | Lock single-flight + early refresh | Stampede defense |
| Cross-instance coordination | Redlock (with caveats) / DB lease | Correctness > availability of lock |

**Related HTTP-level caching:** [HTTP caching](../20.3-rest-apis/20.3.13-http-caching.md) · **System-design view:** [caching theory](../../30-architecture/30.2-system-design/00-theory/INDEX.md)

---

## Navigation

[← Previous: GraphQL](../20.7-graphql/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: WebSockets →](../20.9-websockets/INDEX.md)
