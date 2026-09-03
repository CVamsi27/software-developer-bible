# Memory & Data — JavaScript

> **8 files.** Value vs reference semantics, choosing the right collection, hash table internals, copying strategies, debounce/throttle rate limiting, and how garbage collection actually frees memory.

[![Files](https://img.shields.io/badge/files-8-blue)](#files)
[![Category](https://img.shields.io/badge/category-Memory_and_Data-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Pass by Value](10.1.4.01-pass-by-value.md) | Primitive vs reference, value/reference semantics, mutation gotchas | 15 min |
| 02 | [Map, Set, WeakMap, WeakSet](10.1.4.02-map-set-weakmap-weakset.md) | Keyed collections, weak references, memory-efficient lookups, when to use what | 20 min |
| 03 | [Shallow vs Deep Copy](10.1.4.03-shallow-vs-deep-copy.md) | Spread, `Object.assign`, `structuredClone`, JSON methods, pitfalls | 20 min |
| 04 | [Debounce](10.1.4.04-debounce.md) | Implementation, leading/trailing edge, real-world use cases (search input, resize) | 15 min |
| 05 | [Throttle](10.1.4.05-throttle.md) | Implementation, vs debounce, animation frame throttling, scroll handlers | 15 min |
| 06 | [Memory Leaks](10.1.4.06-memory-leaks.md) | Detached DOM, closures, circular references, detection, debugging | 25 min |
| 07 | [Garbage Collection](10.1.4.07-garbage-collection.md) | Mark-and-sweep, generational collection, V8 Orinoco, WeakRef, FinalizationRegistry | 25 min |
| 08 | [Hash Tables & HashMaps](10.1.4.08-hash-tables-internals.md) | Collision resolution, load factor, rehashing, V8 internals, Robin Hood, interview patterns | 40 min |

---

## Read order

Pass by Value → Shallow vs Deep Copy → Map/Set/WeakMap/WeakSet → **Hash Tables** → Debounce → Throttle → Memory Leaks → Garbage Collection.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Map as an ordered collection | `apps/api/src/shared/common/utils/lru-cache.ts` - `Map` insertion order drives LRU eviction with TTL expiry |
| WeakMap for cycle-safe data | `packages/utils/src/monitoring/phi-scrubber.ts` - deep PHI redaction that survives circular references |
| Hash table as core primitive | `apps/api/src/shared/common/utils/lru-cache.ts` - Map-based O(1) lookup underpins all caching layers |
| Debounce implementation | `packages/hooks/src/use-debounce.ts` - trailing-edge debounce built on refs and a subscriber set |
| Cleanup to avoid leaks | `packages/hooks/src/use-click-outside.ts` - removes document listeners on unmount/deps change |

---

## Navigation

[← Back to JavaScript](../INDEX.md)
