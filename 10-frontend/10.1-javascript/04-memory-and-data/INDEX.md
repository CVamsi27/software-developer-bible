# Memory & Data — JavaScript

> **Study time:** ≈ 1 h 5 m of reading (10 files, ~6 min average).
> **10 files.** Follow values and object identity into collection choice and copying, then learn how timers, retaining paths, hash tables, equality rules, and garbage collection shape real JavaScript systems.

[![Files](https://img.shields.io/badge/files-10-blue)](#files)
[![Category](https://img.shields.io/badge/category-Memory_and_Data-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Pass by Value](10.1.4.01-pass-by-value.md) | Primitive vs reference, value/reference semantics, mutation gotchas | Essential | Foundational | 7 min |
| 02 | [Map, Set, WeakMap, WeakSet](10.1.4.02-map-set-weakmap-weakset.md) | Key identity and order, weak metadata, conversion, bounded eviction | Essential | Foundational | 9 min |
| 03 | [Shallow vs Deep Copy](10.1.4.03-shallow-vs-deep-copy.md) | Reference graphs, structured cloning, transfer, JSON boundary, path copying | Essential | Foundational | 6 min |
| 04 | [Debounce](10.1.4.04-debounce.md) | Quiet-time scheduling, edge policies, cancellation, stale async results | Essential | Foundational | 6 min |
| 05 | [Throttle](10.1.4.05-throttle.md) | Periodic scheduling, edge policies, cancellation, concurrency boundaries | Essential | Foundational | 6 min |
| 06 | [Memory Leaks](10.1.4.06-memory-leaks.md) | Retaining paths, cleanup ownership, bounded caches, heap diagnosis | Essential | Foundational | 5 min |
| 07 | [Garbage Collection](10.1.4.07-garbage-collection.md) | Tracing, generations, scheduling, weak references, process memory | Essential | Foundational | 4 min |
| 08 | [Hash Tables and Hash Maps](10.1.4.08-hash-tables-internals.md) | Hash lookup, collisions, growth costs, JavaScript collection guarantees | Important | Specialized | 7 min |
| 09 | [Equality & Coercion](10.1.4.09-equality-and-coercion.md) | Conversion rules, truthiness, defaults, Object.is, numeric boundaries | Essential | Foundational | 5 min |

---

## Read order

Follow the numbered chapters. **Pass by Value** establishes the difference between rebinding and mutating shared identity; **Map/Set** applies identity to keys and ownership; **Shallow vs Deep Copy** then shows which references a copy separates. **Debounce** and **Throttle** compare waiting for quiet with admitting periodic work. Their pending callbacks lead into cleanup ownership in **Memory Leaks**, then reachability in **Garbage Collection**. Finish with **Hash Tables** for the collision and growth costs behind lookup, and **Equality & Coercion** for the distinct comparison algorithms. Use the revision companion to connect these topics before interview practice.

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
