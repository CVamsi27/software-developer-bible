# Form Handling — Index

> **7 files** — Form handling in React from React Hook Form and Zod to Formik, TanStack Form, Server Actions, autosave/draft recovery, and interview questions.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why forms matter:** Every product has forms. Sign-up, login, settings, checkout, search. Senior interviews test form state management, validation, accessibility, and progressive enhancement. Form libraries (React Hook Form, TanStack Form) and validation (Zod) are now standard tooling.

---

## Topic Categories

| Category                                      | Files | Why it matters                                                        |
| --------------------------------------------- | ----: | --------------------------------------------------------------------- |
| [Form Libraries](#form-libraries)             | 3     | React Hook Form, Formik, TanStack Form — pick the right one           |
| [Validation](#validation)                     | 1     | Zod — the standard for runtime + type-safe validation                 |
| [Server-Side Patterns](#server-side-patterns) | 1     | Server Actions, progressive enhancement, modern Next.js form patterns |
| [Draft Persistence](#draft-persistence)       | 1     | Autosave, localStorage/IndexedDB, dirty guards, conflict resolution   |
| [Interview Prep](#interview-prep)             | 1     | 30+ form-specific Qs                                                  |

---

## Form Libraries

Three main form libraries — pick the right one for the job.

| #   | File                                          | Topics                                                                         | When to use                                                     | Read time   |
| --: | ------                                        | --------                                                                       | -------------                                                   | ----------: |
| 01  | [React Hook Form](10.5.01-react-hook-form.md) | Uncontrolled inputs, `register`, Zod resolver, `useFieldArray`, `FormProvider` | Default choice for React 18+ forms                              | 30 min      |
| 03  | [Formik](10.5.03-formik.md)                   | Controlled-component + context, Yup-first, maintenance mode in 2026            | Legacy codebases; new projects should use RHF                   | 20 min      |
| 04  | [TanStack Form](10.5.04-tanstack-form.md)     | Framework-agnostic, type-first, granular subscriptions, Standard Schema        | New projects needing framework-agnostic or fine-grained control | 25 min      |

**Decision:**

```text
Building a new React form?
├── Yes, standard React 18+ app → React Hook Form (RHF)
├── Yes, need framework-agnostic or fine-grained reactivity → TanStack Form
└── No, maintaining legacy → Formik (don't start new projects with it)
```

---

## Validation

Zod is the standard for runtime validation with TypeScript inference.

| #   | File                  | Topics                                                                                             | Read time   |
| --: | ------                | --------                                                                                           | ----------: |
| 02  | [Zod](10.5.02-zod.md) | Schemas, `z.infer`, transforms, refines, API boundary validation, env validation, error formatting | 30 min      |

**The killer feature:** `z.infer<typeof Schema>` gives you the TypeScript type from your Zod schema. One source of truth for both runtime validation and compile-time types.

---

## Server-Side Patterns

Modern Next.js form patterns with Server Actions.

| #   | File                                                                          | Topics                                                                                    | Read time   |
| --: | ------                                                                        | --------                                                                                  | ----------: |
| 05  | [Server Actions & Form Patterns](10.5.05-server-actions-and-form-patterns.md) | `useActionState`, `useFormStatus`, `useOptimistic`, progressive enhancement, file uploads | 30 min      |

---

## Draft Persistence

Long-form resilience: never lose user input again.

| #   | File                                                            | Topics                                                                                                                                                                                  | Read time   |
| --: | ------                                                          | --------                                                                                                                                                                                | ----------: |
| 06  | [Autosave & Draft Recovery](10.5.06-autosave-draft-recovery.md) | Debounced autosave, localStorage vs IndexedDB, multi-step resume, dirty-state guards (`beforeunload` + route blockers), versioned draft migrations, server-vs-local conflict resolution | 30 min      |

---

## Interview Prep

| #   | File                                                  | Topics                                                         | Read time   |
| --: | ------                                                | --------                                                       | ----------: |
| 07  | [Interview Questions](10.5.07-interview-questions.md) | 30+ curated questions covering all form libraries and patterns | 2 hrs       |

---

## Suggested Study Order

1. **React Hook Form** (30 min) — the default
2. **Zod** (30 min) — the validator
3. **Server Actions** (30 min) — modern Next.js
4. **Autosave & Draft Recovery** (30 min) — production polish for long forms
5. **TanStack Form** (25 min) — alternative if needed
6. **Formik** (skim, 10 min) — for legacy
7. **Interview Questions** (2 hrs)

---

## The Modern Form Stack

```typescript
// 1. Define the schema (Zod)
const signupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// 2. Infer the type
type SignupInput = z.infer<typeof signupSchema>;

// 3. Use it in React Hook Form
const { register, handleSubmit, formState: { errors } } = useForm<SignupInput>({
  resolver: zodResolver(signupSchema),
});

// 4. Submit to a Next.js Server Action
async function onSubmit(data: SignupInput) {
  await signupAction(data);
}
```

This is the standard pattern for modern full-stack forms.

---

## Cross-References

- [Accessibility](../../50-quality/50.2-accessibility/INDEX.md) — accessible form patterns
- [Next.js](../10.4-next.js/INDEX.md) — Server Actions, form components
- [React](../10.3-react/INDEX.md) — useState/useReducer for form state
- [TypeScript](../10.2-typescript/INDEX.md) — `z.infer` for type-safe schemas

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category     | Docita evidence                                                                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| React Hook Form primitives | `packages/ui/src/components/form/form-primitives.tsx` - FormField/FormLabel/FormControl/FormMessage kit over RHF context                                       |
| Zod resolver integration   | `apps/app/src/features/patients/components/forms/dialogs/EditPatientDialog.tsx` - `resolver: zodResolver(updatePatientRequestSchema)`                          |
| Typed field paths          | `packages/ui/src/lib/rhf-path.ts` - guarded escape hatch for RHF's conditional `Path<T>` names                                                                 |
| Debounced form input       | `packages/ui/src/components/form/debounced-search-input.tsx` - local state + debounced `onChange` for search fields                                            |
| Autosave & draft recovery  | `apps/app/src/features/setup/components/onboarding/forms/use-onboarding-draft.ts` - localStorage draft persistence, resume-step resolution, multi-step restore |

_No Server Actions / Formik / TanStack Form implementations in docita yet._

---

## Navigation

[← Previous: Next.js](../10.4-next.js/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Animation →](../10.6-animation/INDEX.md)
