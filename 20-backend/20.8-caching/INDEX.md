# Caching — Index

> **Study time:** ≈ 49 min of reading (5 files, ~10 min average).
> **5 files** — Redis, cache patterns, invalidation strategies — the biggest latency lever and the classic senior-interview topic.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why caching:** A 10 ms request at 1000 requests/s implies about 10 concurrent requests by Little's law, not 10 CPU seconds/s. Caching can reduce origin work and response latency; measure both rather than equating elapsed time with CPU consumption. The difference between a junior and senior engineer is often the ability to identify what to cache, how to invalidate it, and how to prevent stampedes.

---

## Topic Categories

| Category | File | Why it matters | Role priority | General importance |
| ------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------- | ------------- | ------------------ |
| Patterns & Strategy | [Caching Deep Dive](20.8.01-caching-deep-dive.md) | When to use what — the 6 patterns, invalidation, stampede prevention | Essential | Important |
| Redis Fundamentals | [Redis Fundamentals](20.8.02-redis-fundamentals.md) | Data structures, basic patterns, pub/sub | Essential | Important |
| Advanced Redis | [Advanced Redis Patterns](20.8.03-advanced-redis-patterns.md) | Redlock, Lua scripting, Streams — the senior-level toolkit | Essential | Important |

---

## The Decision Table (memorize this)

| Read/write profile | Pattern | Why |
| ------------------------------ | ---------------------------------- | ------------------------------------------------------------------ |
| Read-heavy, stale-tolerant | Cache-aside + TTL + jitter | Simplest correct default |
| Read-heavy, needs fresh writes | Write-through | Successful writes warm reads; partial failures and ordering remain |
| Write-heavy analytics | Write-behind (batch flush) | Throughput ↑; risk window on crash |
| Hot key / thundering herd | Lock single-flight + early refresh | Stampede defense |
| Cross-instance coordination | Redlock (with caveats) / DB lease | Correctness > availability of lock |

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
└─ Just count / dedupe / queue? ──→ Specialized data structures (HLL, Bloom, Streams)
```

---

## File Index

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 1 | [Caching Deep Dive](20.8.01-caching-deep-dive.md) | Cache hierarchy, patterns (cache-aside, write-through, write-behind), invalidation strategies, stampede prevention, multi-tenant caching | Essential | Important | 10 min |
| 2 | [Redis Fundamentals](20.8.02-redis-fundamentals.md) | Data structures (strings, hashes, lists, sets, sorted sets, streams), caching patterns with Redis, rate limiting, distributed locks, pub/sub | Essential | Important | 17 min |
| 3 | [Advanced Redis Patterns](20.8.03-advanced-redis-patterns.md) | Redlock, Lua rate limiting, Pub/Sub deep-dive, Redis Streams, scripting best practices | Essential | Important | 8 min |
| 4 | [Interview Questions](20.8.04-interview-questions.md) | 25 senior Q&A: invalidation design, stampede physics, data-structure tradeoffs, hit-ratio forensics, persistence decisions | Essential | Important | 12 min |

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

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Global cache module | `apps/api/src/cache/cache.module.ts` - @nestjs/cache-manager registered globally: TTL 300s, max 500 entries |
| Tag-based invalidation | `apps/api/src/shared/modules/services/tagged-cache.service.ts` - tag→key maps identify groups for invalidation; verify concurrency guarantees in the implementation |
| LRU primitive | `apps/api/src/shared/common/utils/lru-cache.ts` - capacity+TTL in-process LRU for read-heavy lookups |
| Response caching | `apps/api/src/shared/common/interceptors/cache.interceptor.ts` - hashed-key GET caching through CACHE_MANAGER |
| Short-TTL flag cache | `apps/api/src/shared/modules/feature-flags/feature-flags.service.ts` - 30s resolved-flag TTLs bound staleness |

The backend store is in-memory today (`CACHE_BACKEND=memory`; CI guard `scripts/checks/check-cache-redis-required.mjs` pins the future Redis swap), so Redlock/Lua/Streams chapters: _no direct docita implementation yet._
