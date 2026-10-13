# Core Hooks — React

> **Study time:** ≈ 38 min of reading (6 files, ~6 min average).
> Follow state from one render snapshot to the next, synchronize external work safely, then choose which values belong in refs, memoized calculations or context.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Core_Hooks-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [useState](10.3.2.01-usestate.md) | Render snapshots, queued updates, immutable state and ownership | Essential | Foundational | 5 min |
| 02 | [useEffect](10.3.2.02-useeffect.md) | External synchronization, dependency changes and stale-result guards | Essential | Foundational | 7 min |
| 03 | [useMemo / useCallback](10.3.2.03-usememo-usecallback.md) | Measured render caches and the React Compiler boundary | Important | Important | 7 min |
| 04 | [useRef](10.3.2.04-useref.md) | Imperative handles, callback cleanup and React 19 ref props | Essential | Foundational | 6 min |
| 05 | [Context API](10.3.2.05-context-api.md) | Provider scope, value identity, consumer updates and the React 19.3 Server Component boundary | Important | Important | 8 min |

---

## Read order

1. **Own the state transition.** Read useState and explain why a setter does not change the current handler snapshot.
2. **Keep external work current.** Read useEffect and trace a changed identity through cleanup, the new request and stale-result protection.
3. **Choose how a value survives.** Read memoization, refs and Context; identify which changes should render, which handles are imperative, and which descendants subscribe. Finish with [revision](REVISION.md).

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| useState and functional updates | `packages/hooks/src/use-toggle.ts` — updater receives previous state |
| useEffect synchronization | `packages/hooks/src/use-local-storage.ts` — inspect initialization, persistence and subscription behavior separately |
| useRef for DOM values | `packages/hooks/src/use-click-outside.ts` — containment check and listener cleanup |
| Context API | `apps/app/src/lib/auth/auth-context-inner.ts` — context may contain AuthContextType or undefined; the provider and consumer establish its use |

---

## Navigation

[← Back to React](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
