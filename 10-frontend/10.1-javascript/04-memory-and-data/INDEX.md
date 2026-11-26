# Memory & Data — JavaScript

> **Study time:** ≈ 1 h 22 m of reading (10 files, ~8 min average).
> **10 files.** Follow values and object identity into collection choice and copying, then learn how timers, retaining paths, hash tables, equality rules, and garbage collection shape real JavaScript systems.

[![Files](https://img.shields.io/badge/files-10-blue)](#chapters)
[![Category](https://img.shields.io/badge/category-Memory_and_Data-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Chapters

The Files badge counts these 9 chapters plus the revision companion.

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Pass by Value](10.1.4.01-pass-by-value.md) | Primitive vs. reference, call-by-sharing, shallow immutability (`freeze`/`seal`), and pure `toSorted` arrays | Essential | Foundational | 6 min |
| 02 | [Map, Set, WeakMap, WeakSet](10.1.4.02-map-set-weakmap-weakset.md) | Key identity, insertion order, `getOrInsert` and `getOrInsertComputed`, set methods, and weak symbol boundaries | Essential | Foundational | 7 min |
| 03 | [Shallow vs Deep Copy](10.1.4.03-shallow-vs-deep-copy.md) | Reference graphs, `structuredClone`, transferable buffers, JSON coercion limits, and path copying | Essential | Foundational | 7 min |
| 04 | [Debounce](10.1.4.04-debounce.md) | Quiet-time scheduling, leading/trailing/maxWait policies, cancellation, and React lifecycle cleanup | Essential | Foundational | 11 min |
| 05 | [Throttle](10.1.4.05-throttle.md) | Periodic scheduling, hybrid edge policies, `requestAnimationFrame` gating, cancellation, and concurrency limits | Essential | Foundational | 10 min |
| 06 | [Memory Leaks](10.1.4.06-memory-leaks.md) | Retaining paths, `{ signal }` listener cleanup, bounded caches, DevTools retainers, and `v8.writeHeapSnapshot()` | Essential | Foundational | 8 min |
| 07 | [Garbage Collection](10.1.4.07-garbage-collection.md) | Tracing, V8 spaces (`getHeapSpaceStatistics`), Orinoco, `WeakRef`, and ES2026 `using` deterministic disposal | Essential | Foundational | 7 min |
| 08 | [Hash Tables and Hash Maps](10.1.4.08-hash-tables-internals.md) | Hash lookup, probing tombstones, object integer-key hoisting vs. `Map`, V8 `OrderedHashTable`, and resize pauses | Important | Specialized | 7 min |
| 09 | [Equality & Coercion](10.1.4.09-equality-and-coercion.md) | Equality algorithms, `Symbol.toPrimitive`, `BigInt` rules, `??`, and explicit string/boolean boundary parsing | Essential | Foundational | 8 min |

---

## Read order

Follow the numbered chapters. **Pass by Value** establishes the difference between rebinding and mutating shared identity; **Map/Set** applies identity to keys and ownership; **Shallow vs Deep Copy** then shows which references a copy separates. **Debounce** and **Throttle** compare waiting for quiet with admitting periodic work. Their pending callbacks lead into cleanup ownership in **Memory Leaks**, then reachability in **Garbage Collection**. Finish with **Hash Tables** for the collision and growth costs behind lookup, and **Equality & Coercion** for the distinct comparison algorithms. Use the revision companion to connect these topics before interview practice.

---

## Docita Anchor

Real code from [Docita](https://github.com/CVamsi27/docita) - healthcare-platform codebase (NestJS API + React and Astro apps, TypeScript monorepo; source paths alone do not establish deployment status). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Map` as an ordered collection | `apps/api/src/shared/common/utils/lru-cache.ts` - `Map` insertion order drives LRU eviction with TTL expiry |
| `WeakMap` for cycle-safe data | `packages/utils/src/monitoring/phi-scrubber.ts` - deep PHI redaction that survives circular references |
| Hash table as core primitive | `apps/api/src/shared/common/utils/lru-cache.ts` - `Map` key lookup and recency order support this cache; inspect workload and version before assuming a complexity bound |
| Debounce implementation | `packages/hooks/src/use-debounce.ts` - trailing-edge debounce built on refs and a subscriber set |
| Cleanup to avoid leaks | `packages/hooks/src/use-click-outside.ts` - removes document listeners on unmount or dependency changes |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
