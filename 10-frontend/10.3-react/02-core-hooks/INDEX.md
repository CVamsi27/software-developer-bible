# Core Hooks — React

> **Study time:** ≈ 2 h 19 m of reading (5 files, ~28 min average).
> **5 files.** The five essential hooks — useState, useEffect, useMemo/useCallback, useRef, Context — used in 95% of React code.

[![Files](https://img.shields.io/badge/files-5-blue)](#files)
[![Category](https://img.shields.io/badge/category-Core_Hooks-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [useState](10.3.2.01-usestate.md) | State initialization, batching, functional updates, lazy init | 26 min |
| 02 | [useEffect](10.3.2.02-useeffect.md) | Dependencies, cleanup, effect timing, strict mode, race conditions | 30 min |
| 03 | [useMemo / useCallback](10.3.2.03-usememo-usecallback.md) | Memoization, dependency tracking, when to use (and when not to) | 24 min |
| 04 | [useRef](10.3.2.04-useref.md) | DOM refs, mutable refs, forwardRef, callback refs, useImperativeHandle | 27 min |
| 05 | [Context API](10.3.2.05-context-api.md) | createContext, Provider, useContext, performance pitfalls, splitting context | 32 min |

---

## Read order

useState → useEffect → useMemo / useCallback → useRef → Context API.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category        | Docita evidence                                                                                       |                                          |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| useState & functional updates | `packages/hooks/src/use-toggle.ts` - `setState(prev => !prev)` tuple-return hook                      |                                          |
| useEffect sync & cleanup      | `packages/hooks/src/use-local-storage.ts` - state synced both ways with `localStorage` inside effects |                                          |
| useRef for DOM/mutable values | `packages/hooks/src/use-click-outside.ts` - ref containment check against outside pointer events      |                                          |
| Context API                   | `apps/app/src/lib/auth/auth-context-inner.ts` - `createContext<AuthContextType \                      | undefined>` split from its provider file |

---

## Navigation

[← Back to React](../INDEX.md)
