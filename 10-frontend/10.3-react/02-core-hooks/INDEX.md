# Core Hooks — React

> **Study time:** ≈ 2 h 3 m of reading (6 files, ~20 min average).
> **6 files.** The five essential hooks — useState, useEffect, useMemo/useCallback, useRef, Context — used in 95% of React code.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Core_Hooks-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [useState](10.3.2.01-usestate.md) | State initialization, batching, functional updates, lazy init | 24 min |
| 02 | [useEffect](10.3.2.02-useeffect.md) | Dependencies, cleanup, effect timing, strict mode, race conditions | 17 min |
| 03 | [useMemo / useCallback](10.3.2.03-usememo-usecallback.md) | Memoization, dependency tracking, when to use (and when not to) | 23 min |
| 04 | [useRef](10.3.2.04-useref.md) | DOM refs, mutable refs, forwardRef, callback refs, useImperativeHandle | 25 min |
| 05 | [Context API](10.3.2.05-context-api.md) | createContext, Provider, useContext, performance pitfalls, splitting context | 30 min |

---

## Read order

useState → useEffect → useMemo / useCallback → useRef → Context API.

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
