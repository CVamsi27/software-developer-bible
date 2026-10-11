# Memory & Data — JavaScript

> **Study time:** ≈ 2 h 42 m of reading (10 files, ~16 min average).
> **10 files.** Value vs reference semantics, choosing the right collection, hash table internals, copying strategies, equality & coercion rules, debounce/throttle rate limiting, and how garbage collection actually frees memory.

[![Files](https://img.shields.io/badge/files-10-blue)](#files)
[![Category](https://img.shields.io/badge/category-Memory_and_Data-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |  |  |
| --   : | ------ | -------- | --- | --- | ----------: |  |  |
| 01 | [Pass by Value](10.1.4.01-pass-by-value.md) | Primitive vs reference, value/reference semantics, mutation gotchas | Essential | Foundational | 6 min |  | 6 min |
| 02 | [Map, Set, WeakMap, WeakSet](10.1.4.02-map-set-weakmap-weakset.md) | Keyed collections, weak references, memory-efficient lookups, when to use what | Essential | Foundational | 15 min |  | 17 min |
| 03 | [Shallow vs Deep Copy](10.1.4.03-shallow-vs-deep-copy.md) | Spread, `Object.assign`, `structuredClone`, JSON methods, pitfalls | Essential | Foundational | 14 min |  | 16 min |
| 04 | [Debounce](10.1.4.04-debounce.md) | Implementation, leading/trailing edge, real-world use cases (search input, resize) | Essential | Foundational | 22 min |  | 16 min |
| 05 | [Throttle](10.1.4.05-throttle.md) | Implementation, vs debounce, animation frame throttling, scroll handlers | Essential | Foundational | 21 min |  | 17 min |
| 06 | [Memory Leaks](10.1.4.06-memory-leaks.md) | Retaining paths, timer/listener ownership, bounded caches, diagnosis | Essential | Foundational | 21 min |  | 17 min |
| 07 | [Garbage Collection](10.1.4.07-garbage-collection.md) | Mark-and-sweep, generational collection, V8 Orinoco, WeakRef, FinalizationRegistry | Essential | Foundational | 21 min |  | 21 min |
| 08 | [Hash Tables & HashMaps](10.1.4.08-hash-tables-internals.md) | Collision resolution, load factor, rehashing, V8 internals, Robin Hood, interview patterns | Important | Specialized | 27 min |  | 31 min |
| 09 | [Equality & Coercion](10.1.4.09-equality-and-coercion.md) | Conversion rules, truthiness, defaults, Object.is, numeric boundaries | Essential | Foundational | 9 min |  | 11 min |

---

## Read order

Start with **Pass by Value** to separate binding reassignment from shared-object mutation. Then **Shallow vs Deep Copy** explains which identities a copy separates. Read **Equality & Coercion** before **Map/Set/WeakMap/WeakSet**, so key identity and SameValueZero have a meaning; **Hash Tables** then derives collision handling behind a possible collection implementation.

Read **Debounce** before **Throttle** to compare waiting for quiet with preserving execution spacing. Their pending callbacks introduce lifetime ownership. **Memory Leaks** follows that ownership into retaining paths, and **Garbage Collection** explains why unreachable data can be reclaimed while unwanted reachable data cannot. Finish with revision before returning to interview practice.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - healthcare-platform codebase (NestJS API + React/Astro apps, TypeScript monorepo; source paths alone do not establish deployment status). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Map as an ordered collection | `apps/api/src/shared/common/utils/lru-cache.ts` - `Map` insertion order drives LRU eviction with TTL expiry |
| WeakMap for cycle-safe data | `packages/utils/src/monitoring/phi-scrubber.ts` - deep PHI redaction that survives circular references |
| Hash table as core primitive | `apps/api/src/shared/common/utils/lru-cache.ts` - Map key lookup and recency order support this cache; inspect workload/version before assuming a complexity bound |
| Debounce implementation | `packages/hooks/src/use-debounce.ts` - trailing-edge debounce built on refs and a subscriber set |
| Cleanup to avoid leaks | `packages/hooks/src/use-click-outside.ts` - removes document listeners on unmount/deps change |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
