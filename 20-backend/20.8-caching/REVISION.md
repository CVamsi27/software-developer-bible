<!-- section: Caching | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Caching-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-orange)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)

# Caching — Revision

Read a chapter, close it, and explain the mechanism before revealing the answer. Use the source links to repair a missing step. The [interview bank](20.8.04-interview-questions.md) is a separate spoken-answer drill.

## Caching Deep-Dive

Source: [Caching Deep-Dive](20.8.01-caching-deep-dive.md).

**Q:** A reader fetches the old row, a writer commits and deletes the cache key, then the reader caches its result. Which stale-read problem remains?

**A:** The old row can repopulate the cache after invalidation. TTL limits that entry's lifetime; stronger freshness needs a source-coordinated version/conditional fill or an authoritative read.

**Q:** Why does changing every cache key from `v1` to `v2` help a serializer deployment but not automatically make source writes consistent?

**A:** It prevents reuse of the previous serialization namespace. A source write and namespace change still have separate timing; a reader can load an old source snapshot into the new key unless the version/read contract prevents it.

**Q:** L1 installs a value from L2 with a new five-second TTL. Is that value at most five seconds old?

**A:** No. It may already have aged in L2 or come from a delayed source read. Propagate and enforce the relevant source/version freshness information, or accept the whole path's stated stale-read window.

**Q:** The cache limits its map to 100 entries. Has it bounded memory to a known number of bytes?

**A:** No. Entry sizes, retained result objects and in-flight responses vary. A count limit needs payload limits or a measured byte policy when memory is the constraint.

**Q:** Does `SCAN COUNT 100` cap a reply at 100 keys or give a snapshot for tenant invalidation?

**A:** Neither. `COUNT` is a work hint, and iteration can return duplicates while the keyspace changes. Split `UNLINK` into its own bounded batches; scan every primary in a cluster, or use a source-coordinated version when the old namespace must become unreachable atomically.

**Q:** What must the service survive when an entire hot cache is empty?

**A:** A burst of origin reads. Coalesce identical misses, cap origin concurrency, and shed/serve stale work under an explicit policy; merely adding retries amplifies the burst.

## Redis Fundamentals

Source: [Redis Fundamentals](20.8.02-redis-fundamentals.md).

**Q:** Why is `LPUSH tasks A B C` followed by `RPOP tasks` expected to return `A`?

**A:** LPUSH inserts its arguments one at a time at the head, yielding C, B, A. Removing the tail returns the earliest inserted item A.

**Q:** A worker pauses beyond a lease's TTL, then resumes. What does compare-and-delete release protect, and what does it leave unresolved?

**A:** Checking the random owner token prevents it deleting a replacement holder's lease. It does not stop the old worker's effect; a database invariant or resource-enforced fencing must reject unsafe overlap.

**Q:** Is a pipeline sufficient for a rate limiter's remove/count/add decision?

**A:** No. It reduces network round trips, while other clients may interleave. One Lua script or another explicitly atomic decision boundary must decide admission and record it.

## Redis 8 data types and the Node.js client

Source: [Redis Fundamentals](20.8.02-redis-fundamentals.md), [Redis data types](https://redis.io/docs/latest/develop/data-types/), and the [node-redis guide](https://redis.io/docs/latest/develop/clients/nodejs/).

**Q:** When does a Redis Hash fit better than a JSON document, and why is a JSON string different from Redis JSON?

**A:** A Hash stores flat string fields and supports field-level commands. A serialized JSON String is opaque to Redis commands, while Redis JSON supports structured field access and queries. Choose from the required data shape and access pattern, and confirm module/version availability.

**Q:** Which Node.js client does Redis recommend for new applications, and why should you avoid mixing examples from different clients?

**A:** Redis recommends node-redis for new projects and continues to maintain ioredis. Their command names, option objects and return types differ; pin the client version and test examples against its API.

**Q:** Why can one slow command raise latency for unrelated clients on the same Redis node?

**A:** Redis serializes command execution against that node's keyspace. I/O threads improve network work, but a large scan, expensive command, or long script can still occupy its command path. Bound work and inspect `SLOWLOG` and latency metrics.

**Q:** Does a successful primary reply prove a write survives restart and failover?

**A:** No. RDB snapshots, AOF fsync policy, asynchronous replica progress, and failover are separate durability boundaries. `WAIT` returns the actual acknowledgment count, which can fall below the requested count at timeout; even sufficient acknowledgments do not make Redis strongly consistent.

**Q:** What changes when two keys hash to different Redis Cluster slots?

**A:** They may be owned by different primaries, so a multi-key atomic operation cannot generally span them. A hash tag can place keys in one slot when the operation requires co-location, at the cost of concentrating that key family on one shard.

**Q:** What is the difference between `MOVED` and `ASK` during Cluster routing?

**A:** `MOVED` tells the client that the slot's owner has changed and it should refresh its map. `ASK` is a temporary redirect during migration for the current request; the client uses `ASKING` and should not treat the destination as the permanent owner.

## Advanced Redis Patterns

Source: [Advanced Redis Patterns](20.8.03-advanced-redis-patterns.md).

**Q:** A refill rate is specified in tokens per second but elapsed time is in milliseconds. What conversion belongs at the boundary?

**A:** Divide the rate by 1000, or divide elapsed milliseconds by 1000. Mixing them without conversion refills roughly 1000 times too fast.

**Q:** Why can a Streams consumer reading `>` miss work left by a crashed worker?

**A:** `>` retrieves never-delivered entries. Already-delivered entries remain in the pending-entry list and need explicit recovery/reclaim; processing must tolerate an old worker resuming.

**Q:** Does XACK delete the event, and does a successful XADD prove it survives failover?

**A:** XACK clears pending-delivery bookkeeping; retention controls stored entries. Persistence, asynchronous replication, eviction, and recovery settings decide whether an appended event survives a failure.

## Trace and Change One Condition

Source: [Cache-aside model](20.8.01-caching-deep-dive.md#cache-aside-with-one-complete-local-trace), [Redis lease](20.8.02-redis-fundamentals.md#expiring-session-and-owner-token-lease), and [Streams recovery](20.8.03-advanced-redis-patterns.md#4-redis-streams-with-consumer-groups).

**Q:** Two callers read one absent key before the source resolves. How many loads does the local model perform, and what changes across processes?

**A:** One local in-flight promise serves both. Another process has its own map and can also load; this model does not promise fleet-wide coalescing.

**Q:** The source rejects. Should a subsequent caller reuse that rejected promise?

**A:** No. The finally handler removes it, enabling recovery. A deadline and bounded retries still belong in the source adapter.

**Q:** A caller mutates the returned object. What does the example cache subsequently return?

**A:** The same object reference. The contract requires immutability or deliberate cloning; copying a value into a cache does not automatically isolate it.

**Q:** A lease acquisition succeeds but the response is lost. Is retrying acquisition evidence that the first attempt failed?

**A:** No. The stored lease may exist. Unique holder identity, bounded reconciliation and the protected resource's invariant handle the uncertainty.

**Q:** A stream entry is reclaimed while the original worker resumes. Does XACK arbitrate the business effect?

**A:** No. Both can perform work before acknowledgment; the authoritative effect needs an atomic deduplication or conflict guard.

## Next Step

Return to the [reading flow](INDEX.md), then use the interview bank to explain one trade-off in under a minute.

## Summary

Explain the failure boundary before naming the technique. Return to the source chapter when an answer omits the race, recovery path, or durability assumption.

## See Also

- [Stack reading flow](INDEX.md) — return to the mechanism that needs another pass.

## References & Learn More

The source chapters linked above contain the technical references for these review answers.
