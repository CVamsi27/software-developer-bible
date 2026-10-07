<!-- section: Caching | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Caching-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-orange)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
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

## Advanced Redis Patterns

Source: [Advanced Redis Patterns](20.8.03-advanced-redis-patterns.md).

**Q:** A refill rate is specified in tokens per second but elapsed time is in milliseconds. What conversion belongs at the boundary?

**A:** Divide the rate by 1000, or divide elapsed milliseconds by 1000. Mixing them without conversion refills roughly 1000 times too fast.

**Q:** Why can a Streams consumer reading `>` miss work left by a crashed worker?

**A:** `>` retrieves never-delivered entries. Already-delivered entries remain in the pending-entry list and need explicit recovery/reclaim; processing must tolerate an old worker resuming.

**Q:** Does XACK delete the event, and does a successful XADD prove it survives failover?

**A:** XACK clears pending-delivery bookkeeping; retention controls stored entries. Persistence, asynchronous replication, eviction, and recovery settings decide whether an appended event survives a failure.

## Next Step

Return to the [reading flow](INDEX.md), then use the interview bank to explain one trade-off in under a minute.

## Summary

Explain the failure boundary before naming the technique. Return to the source chapter when an answer omits the race, recovery path, or durability assumption.

## See Also

- [Stack reading flow](INDEX.md) — return to the mechanism that needs another pass.

## References & Learn More

The source chapters linked above contain the technical references for these review answers.
