# Patterns & Interview Prep — React

> **Study time:** ≈ 1 h 5 m of reading (4 files, ~16 min average).
> **4 files.** Reusable component composition patterns — portals and compound components — plus the 60+ question interview bank.

[![Files](https://img.shields.io/badge/files-4-blue)](#files)
[![Category](https://img.shields.io/badge/category-Patterns_and_Interview-orange)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Portals](10.3.5.01-portals.md) | createPortal, event bubbling, modals, tooltips, overflow escape, SSR safety | Important | Specialized | 23 min |
| 02 | [Compound Components](10.3.5.02-compound-components.md) | Context-based pattern, tabs, accordion, select, form fields, generics | Important | Specialized | 26 min |
| 03 | [Interview Questions](10.3.5.03-interview-questions.md) | 60+ curated questions with answers | Important | Specialized | 14 min |

---

## Read order

Portals → Compound Components → Interview Questions.

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Portals | `packages/ui/src/components/overlay/dialog.tsx` - `DialogPrimitive.Portal` wrapper rendering dialogs outside the DOM tree |
| Compound components | `packages/ui/src/components/form/form-primitives.tsx` - FormField/FormLabel/FormControl/FormMessage kit backed by context in `packages/ui/src/components/form/form.tsx` |

---

## Navigation

[← Back to React](../INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
