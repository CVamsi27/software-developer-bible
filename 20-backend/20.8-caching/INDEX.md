# Caching — Index

> **Study time:** ≈ 48 min of reading (5 files, ~10 min average).
> **5 files** — cache contracts, invalidation, Redis data structures, operational patterns and interview practice.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why caching:** Caching can reduce response time and origin work when reads repeat and the cache costs less than recomputation. Measure latency, origin load, hit rate and miss cost; then define freshness, invalidation and outage behavior before picking a pattern.

---

## Topic Categories

| Category | File | Why it matters | Role priority | General importance |
| ------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------- | ------------------ |
| Patterns & Strategy | [Caching Deep Dive](20.8.01-caching-deep-dive.md) | Cache-aside and read-through, write policies, invalidation and stampede control | Essential | Important |
| Redis Fundamentals | [Redis Fundamentals](20.8.02-redis-fundamentals.md) | Command execution, data structures, persistence, replication, Cluster slots, and basic patterns | Essential | Important |
| Advanced Redis | [Advanced Redis Patterns](20.8.03-advanced-redis-patterns.md) | Leases, Lua scripting, Streams — the senior-level toolkit | Essential | Important |

---

## Compare the Contracts

| Read/write profile | Pattern | Why |
| ------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| Read-heavy, stale-tolerant | Cache-aside + TTL + jitter | Useful when the stated stale-read and fallback policy holds |
| Read-heavy, needs fresh writes | Write-through | Successful writes warm reads; partial failures and ordering remain |
| Write-heavy analytics | Write-behind (batch flush) | Throughput ↑; risk window on crash |
| Hot key / thundering herd | Lock single-flight + early refresh | Stampede defense |
| Cross-instance coordination | Database invariant first; lease only where overlap is safe | Expiry and failover can permit overlapping holders |

---

## Pattern Selection

```text
Need to cache data?
│
├─ Read-heavy, eventual consistency OK? ──→ Cache-aside + TTL (default)
│
├─ Read must reflect writes immediately? ──→ authoritative reads or source-coordinated versions
│
├─ Writes are huge, reads are rare? ──→ Write-behind (consistency risk)
│
├─ Cache miss stampede risk? ──→ Single-flight + early refresh
│
├─ Multi-instance mutex? ──→ DB invariant or lease + resource-enforced fencing
│
└─ Just count / dedupe / queue? ──→ Specialized data structures (JSON, Time Series, probabilistic types, Streams)
```

---

## File Index

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 1 | [Caching Deep Dive](20.8.01-caching-deep-dive.md) | Cache hierarchy, cache-aside and read-through, write policies, invalidation, stampede prevention, multi-tenant caching | Essential | Important | 11 min |
| 2 | [Redis Fundamentals](20.8.02-redis-fundamentals.md) | Command path and latency, data structures, persistence versus replication, Cluster slots, and core patterns | Essential | Important | 16 min |
| 3 | [Advanced Redis Patterns](20.8.03-advanced-redis-patterns.md) | Lease assumptions, Lua rate limiting, Pub/Sub delivery, Redis Streams, scripting boundaries | Essential | Important | 10 min |
| 4 | [Interview Questions](20.8.04-interview-questions.md) | 25 senior Q&A: invalidation design, stampede physics, data-structure tradeoffs, hit-ratio forensics, persistence decisions | Essential | Important | 8 min |

---

## Suggested Study Order

1. **Caching Deep Dive** — must know, the patterns
2. **Redis Fundamentals** — the most common caching store
3. **Advanced Redis** — use leases, Lua, and Streams only after naming their failure boundary
4. **Revision** — use the [separate chapter review](REVISION.md) to diagnose gaps; return to its source chapter
5. **Interview Questions** — practice concise answers after the mechanisms are clear

---

## Cross-References

- [HTTP Caching](../20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md) — cache headers (Cache-Control, ETag)
- [System Design — Caching theory](../../30-architecture/30.2-system-design/01-theory/30.2.1.05-caching-patterns.md) — caching in system design
- [Database — Performance tuning](../20.4-database/01-postgresql-foundations/20.4.1.05-postgresql-performance.md) — DB-level caching

---

## Navigation

[← Previous: GraphQL](../20.7-graphql/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Real-Time stack →](../../60-realtime/60.1-websockets/INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) pointers are places to inspect current behavior and tests before citing project evidence:

| Topic | Docita evidence |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Global cache module | `apps/api/src/cache/cache.module.ts` - @nestjs/cache-manager registered globally: TTL 300s, max 500 entries |
| Tag-based invalidation | `apps/api/src/shared/modules/services/tagged-cache.service.ts` - tag→key maps identify groups for invalidation; verify concurrency guarantees in the implementation |
| LRU primitive | `apps/api/src/shared/common/utils/lru-cache.ts` - capacity+TTL in-process LRU for read-heavy lookups |
| Response caching | `apps/api/src/shared/common/interceptors/cache.interceptor.ts` - hashed-key GET caching through CACHE_MANAGER |
| Short-TTL flag cache | `apps/api/src/shared/modules/feature-flags/feature-flags.service.ts` - 30s resolved-flag TTLs bound staleness |

Verify the current cache backend and deployment configuration. These pointers alone do not establish Redis use, present TTL values or production correctness.
