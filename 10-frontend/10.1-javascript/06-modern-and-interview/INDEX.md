# Modern JS & Interview Prep — JavaScript

> **Study time:** ≈ 1 h 20 m of reading (6 files, ~13 min average).
> **6 files.** The newest language features (ES2023+/ES2024), offloading CPU-heavy work to Web Workers, DOM events & delegation, cross-tab communication, and the 50+ question self-test bank.

[![Files](https://img.shields.io/badge/files-6-blue)](#files)
[![Category](https://img.shields.io/badge/category-Modern_JS_Interview-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-wip-yellow)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------    : |
| 01 | [ES2024+ Features](10.1.6.01-es2024-features.md) | `?.`/`??` syntax foundations (ES2020), `structuredClone`, `toSorted`, `Object.groupBy`, `Promise.withResolvers`, iterator helpers, Set methods (ES2025) | Important | Specialized | 16 min |
| 02 | [Web Workers](10.1.6.02-web-workers.md) | Dedicated/Shared workers, OffscreenCanvas, Comlink, React hooks for workers | Important | Important | 11 min |
| 03 | [DOM Events & Delegation](10.1.6.03-dom-events-delegation.md) | Capture/bubble phases, target vs currentTarget, delegation patterns, passive listeners, CustomEvent, React synthetic events | Essential | Foundational | 17 min |
| 04 | [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md) | BroadcastChannel, storage events, SharedWorker vs postMessage, non-atomic storage races and Web Locks, sync logout, IndexedDB payloads, service-worker messaging | Important | Specialized | 19 min |
| 05 | [Interview Questions](10.1.6.05-interview-questions.md) | 55+ curated questions with answers | Essential | Foundational | 11 min |

---

## Read order

First compare syntax/host API availability and value-copy behavior. Then study who owns worker state and how replies return, followed by the event path that lets a parent route child actions. Cross-tab communication builds on these message/owner concepts to compare notifications, stored recovery and locks. Complete [revision](REVISION.md) after the four learning chapters, then use the interview bank to explain one trace and one changed condition per answer.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| DOM events & listeners | `packages/hooks/src/use-keyboard-shortcuts.ts` - document-level keydown handling with `preventDefault`/`stopPropagation` and cleanup |
| Event target & delegation guards | `packages/hooks/src/keyboard-shortcut-match.ts` - pure predicate composition incl. typing-target suppression |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
