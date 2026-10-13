# Form Handling — Index

> **Study time:** ≈ 1 h 4 m of reading (8 files, ~8 min average).
> **8 files** — Form handling in React from React Hook Form and Zod to Formik, TanStack Form, Server Actions, autosave/draft recovery, and interview questions.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Forms coordinate editable values, feedback, submission and recovery. Senior interviews test how these states cross browser, server and persistence boundaries.

---

## Topic Categories

| Category | Files | Why it matters |
| --------------------------------------------- | ----: | --------------------------------------------------------------------- |
| [Validation](#validation) | 1 | Zod 4 runtime parsing and TypeScript input/output types |
| [Form Libraries](#form-libraries) | 3 | Compare field ownership, subscriptions and existing integrations |
| [Server-Side Patterns](#server-side-patterns) | 1 | Server Functions, Server Actions, progressive enhancement |
| [Draft Persistence](#draft-persistence) | 1 | Autosave, localStorage/IndexedDB, dirty guards, conflict resolution |
| [Interview Prep](#interview-prep) | 1 | 30+ form-specific questions |

---

## Validation

Zod parses runtime values and can derive TypeScript types from its schemas.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 02 | [Zod](10.5.02-zod.md) | Schemas, `z.infer`, transforms, refines, API boundary validation, env validation, error formatting | Essential | Important | 10 min |

`z.infer<typeof schema>` describes parsed output; `z.input<typeof schema>` describes accepted input when transforms or coercion change its type. Parsing does not establish authorization.

---

## Form Libraries

Three main form libraries — pick the right one for the job.

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 01 | [React Hook Form](10.5.01-react-hook-form.md) | Native registration, controlled widgets, Zod resolver, `useFieldArray`, `FormProvider` | Existing integrations or forms that benefit from native field registration | Essential | Important | 11 min |
| 03 | [Formik](10.5.03-formik.md) | Controlled fields, context and validation integration | Existing Formik forms or requirements suited to controlled state | Optional | Specialized | 8 min |
| 04 | [TanStack Form](10.5.04-tanstack-form.md) | Typed fields, granular subscriptions, framework adapters, Standard Schema | Forms that need selected subscriptions or a non-React adapter | Optional | Specialized | 9 min |

Compare the existing integration, native or controlled widgets, required subscriptions and normalized output. Prototype a representative form and measure it before choosing or migrating; no library name establishes a universal performance or maintenance conclusion.

---

## Server-Side Patterns

Modern Next.js form patterns with Server Actions.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Server Actions & Form Patterns](10.5.05-server-actions-and-form-patterns.md) | `useActionState`, `useFormStatus`, `useOptimistic`, progressive enhancement, file uploads | Important | Specialized | 8 min |

---

## Draft Persistence

Long-form resilience: recover persisted input and handle storage failures.

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 06 | [Autosave & Draft Recovery](10.5.06-autosave-draft-recovery.md) | Debounced autosave, localStorage vs IndexedDB, multi-step resume, dirty-state guards (`beforeunload` + route blockers), versioned draft migrations, server-vs-local conflict resolution | Important | Important | 9 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 07 | [Interview Questions](10.5.07-interview-questions.md) | 30+ curated questions covering all form libraries and patterns | Essential | Important | 7 min |

---

## Study Order

1. Read [Zod](10.5.02-zod.md) to distinguish received input from parsed output.
2. Work through [React Hook Form](10.5.01-react-hook-form.md): register a native field, adapt a controlled widget and retain input after a rejected save.
3. Compare [Formik](10.5.03-formik.md) and [TanStack Form](10.5.04-tanstack-form.md) by tracing who owns values and which views subscribe to changes.
4. Trace a server rejection, bounded file upload and no-JavaScript submission in [Server Actions](10.5.05-server-actions-and-form-patterns.md).
5. Walk a failed save, reload and revision conflict in [Autosave & Draft Recovery](10.5.06-autosave-draft-recovery.md).
6. Close the chapters, answer the [revision questions](REVISION.md), then use the separate [interview drill](10.5.07-interview-questions.md).

---

## Reading Path and Completion Check

Build one form, submit invalid and valid values, simulate a server rejection, then restore a draft after reload. Be able to state what each layer validates, what it persists and which operation enforces authorization or conflict handling.

## Cross-References

- [Accessibility](../../50-quality/50.2-accessibility/INDEX.md) — accessible form patterns
- [Next.js](../10.4-next.js/INDEX.md) — Server Actions, form components
- [React](../10.3-react/INDEX.md) — useState/useReducer for form state
- [TypeScript](../10.2-typescript/INDEX.md) — `z.infer` for type-safe schemas

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| React Hook Form primitives | `packages/ui/src/components/form/form-primitives.tsx` - FormField/FormLabel/FormControl/FormMessage kit over RHF context |
| Zod resolver integration | `apps/app/src/features/patients/components/forms/dialogs/EditPatientDialog.tsx` - `resolver: zodResolver(updatePatientRequestSchema)` |
| Typed field paths | `packages/ui/src/lib/rhf-path.ts` - guarded escape hatch for RHF's conditional `Path<T>` names |
| Debounced form input | `packages/ui/src/components/form/debounced-search-input.tsx` - local state + debounced `onChange` for search fields |
| Autosave & draft recovery | `apps/app/src/features/setup/components/onboarding/forms/use-onboarding-draft.ts` - localStorage draft persistence, resume-step resolution, multi-step restore |

_No Server Actions / Formik / TanStack Form implementations in docita yet._

---

## Navigation

[← Previous: Next.js](../10.4-next.js/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Animation →](../10.6-animation/INDEX.md)
