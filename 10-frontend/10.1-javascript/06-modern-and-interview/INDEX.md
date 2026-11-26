# Modern JS & Interview Prep — JavaScript

> **Study time:** ≈ 1 h 3 m of reading (7 files, ~9 min average).
> **7 files.** Selected ECMAScript 2022–2026 features and separate host APIs, Web Workers, DOM events, cross-tab coordination, regular expressions, and a 76-question interview bank.

[![Files](https://img.shields.io/badge/files-7-blue)](#chapters)
[![Category](https://img.shields.io/badge/category-Modern_JS_Interview-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Chapters

The Files badge counts these 6 chapters plus the revision companion.

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Recent ECMAScript Features](10.1.6.01-es2024-features.md) | Selected ES2022–2026 built-ins, `Iterator.concat`, `JSON.rawJSON`, `Uint8Array.fromBase64`, and host boundaries | Important | Specialized | 8 min |
| 02 | [Web Workers](10.1.6.02-web-workers.md) | Dedicated, shared, and service workers; `ArrayBuffer` transfer, `SharedArrayBuffer` COOP/COEP, and cancellation | Important | Important | 8 min |
| 03 | [DOM Events & Delegation](10.1.6.03-dom-events-delegation.md) | Event path, Shadow DOM `composed: true`, delegation, propagation, passive listeners, and cleanup | Essential | Foundational | 6 min |
| 04 | [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md) | `BroadcastChannel`, stored recovery, shared owners, Web Locks, and safe cross-tab session updates | Important | Specialized | 7 min |
| 05 | [Regular Expressions and Text Matching](10.1.6.06-regexp-and-text.md) | Character classes, `g`/`u`/`v`/`d` flags, capture indices, ReDoS backtracking risk, and log redaction | Essential | Important | 9 min |
| 06 | [Interview Questions](10.1.6.05-interview-questions.md) | 76 curated questions with answers and changed-condition checks | Essential | Foundational | 17 min |

---

## Read order

First compare syntax and host API availability alongside value-copy behavior. Then study who owns worker state and how replies return, followed by the event path that lets a parent route child actions. Cross-tab communication builds on these message and owner concepts to compare notifications, stored recovery, and locks. Regular expressions close the learning sequence with pattern structure, stateful matching, and backtracking risk. Complete [revision](REVISION.md) after the five learning chapters, then use the interview bank to explain one trace and one changed condition per answer.

---

## Docita Anchor

Examples in [Docita](https://github.com/CVamsi27/docita), a healthcare-platform repository with a NestJS API and React and Astro apps in a TypeScript monorepo. Study the chapter, then locate the implementation:

| Topic in this category | Docita evidence |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| DOM events & listeners | `packages/hooks/src/use-keyboard-shortcuts.ts` - document-level keydown handling with `preventDefault`, `stopPropagation`, and cleanup |
| Event target & delegation guards | `packages/hooks/src/keyboard-shortcut-match.ts` - pure predicate composition incl. typing-target suppression |

---

## Navigation

[← Back to JavaScript](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
