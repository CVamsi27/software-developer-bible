# Patterns & Interview Prep — React

> **Study time:** ≈ 35 min of reading (4 files, ~9 min average).
> **4 files.** Learn where React ownership differs from DOM placement, then coordinate reusable parts through a clear shared-state contract before interview practice.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Patterns_and_Interview-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Portals](10.3.5.01-portals.md) | `createPortal`, React vs. native bubbling, outside-click ref guards, `inert`, `<dialog>` and Popover API, and SSR safety | Important | Specialized | 7 min |
| 02 | [Compound Components](10.3.5.02-compound-components.md) | Context composition, `asChild` Slot merging, generic factories, controllable state, form fields, and ARIA contracts | Important | Specialized | 11 min |
| 03 | [Interview Questions](10.3.5.03-interview-questions.md) | 47 curated mechanism, React 19.2–19.3, trade-off, and system design questions | Important | Specialized | 14 min |

---

## Read order

1. **Separate placement from logical ownership.** Read Portals; trace context, React events, and native DOM paths across the destination.
2. **Coordinate flexible parts through one owner.** Read Compound Components; identify the selection owner, unmount and reset policy, and accessible relationships.
3. **Recall before timed answers.** Complete [revision](REVISION.md), then the interview bank. Add a concrete trace and a changed-condition boundary to each answer.

---

## Navigation

[← Back to React](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
