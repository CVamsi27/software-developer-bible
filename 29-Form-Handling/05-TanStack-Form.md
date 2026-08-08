---
section: Form Handling
category: Frontend
tags: [concept, reference, tool]
---

# TanStack Form

> TanStack Form is a framework-agnostic, headless form library from the TanStack team. It ships first-class TypeScript inference, granular subscriptions, async validation, and a small bundle — the modern alternative to RHF and Formik when type-safety and dynamic schemas matter.

## Definition

TanStack Form is a headless, type-first form library that works in React, Vue, Solid, Svelte, and Lit. It uses a `useForm()` hook (or framework equivalent) that takes a generic type for field values, a validator function, and returns field-level state, validation, and submission helpers. It's the most type-safe option in 2026 and the only one with first-class framework parity.

## Why It Matters (TL;DR)

- **Framework-agnostic** — same API in React, Vue, Solid, Svelte, Lit
- **Type-first** — generic `useForm<TForm>` infers field types from your type
- **Granular subscriptions** — components only re-render for their slice of state
- **Schema validators** — Standard Schema support (Zod, Valibot, ArkType, Yup)
- **Built for dynamic forms** — array fields, conditional fields, complex deps

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                      TANSTACK FORM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              useForm<TForm, TValidator> hook                │   │
│  │  • defaultValues: initial state                             │   │
│  │  • validators: Standard Schema (Zod / Valibot / …)          │   │
│  │  • onSubmit: async submit handler                           │   │
│  │  • state.values, state.errors, state.fieldMeta              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Field-level helpers (no React Context!)        │   │
│  │  • field.state.value / meta / errors                       │   │
│  │  • field.handleChange / handleBlur                          │   │
│  │  • Subscribe via field.Subscribe (granular re-render)       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Validation Layer (Standard Schema)             │   │
│  │  • Sync validation on change / blur / submit                │   │
│  │  • Async validators (debounce, e.g., username check)        │   │
│  │  • Field-level + form-level                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## RHF vs TanStack Form

| Dimension | React Hook Form | TanStack Form |
|-----------|-----------------|---------------|
| Architecture | Uncontrolled, refs | Controlled + granular subscriptions |
| Framework | React only | React, Vue, Solid, Svelte, Lit |
| Type inference | Good (`useForm<T>`) | Excellent (Standard Schema → types) |
| Re-renders | Refs avoid most | Subscription-based, fine-grained |
| Bundle | ~9 KB | ~13 KB (core) + adapter per framework |
| Dynamic forms | `useFieldArray` | First-class `fieldOptions` API |
| Async validation | Manual debounce | Built-in debounce + cancellation |
| Schema | Resolver pattern | Standard Schema (no resolver needed) |
| Maturity | High (2019) | Newer (2024), rapidly maturing |

## Code Examples

### 1. Basic Form (React)

```typescript
import { useForm } from '@tanstack/react-form';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
});

type LoginValues = z.infer<typeof loginSchema>;

function LoginForm() {
  const form = useForm({
    defaultValues: { email: '', password: '' } as LoginValues,
    validators: { onChange: loginSchema },
    onSubmit: async ({ value }) => {
      await api.login(value);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
    >
      <form.Field
        name="email"
        children={(field) => (
          <div>
            <label htmlFor={field.name}>Email</label>
            <input
              id={field.name}
              type="email"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.errors.length > 0 && (
              <span role="alert">{String(field.state.meta.errors[0])}</span>
            )}
          </div>
        )}
      />
      {/* password similar */}
      <form.Subscribe selector={(s) => [s.canSubmit, s.isSubmitting]}>
        {([canSubmit, isSubmitting]) => (
          <button type="submit" disabled={!canSubmit}>
            {isSubmitting ? 'Logging in…' : 'Login'}
          </button>
        )}
      </form.Subscribe>
    </form>
  );
}
```

### 2. Granular Subscription (No Unnecessary Re-renders)

```typescript
// Only this component re-renders when email value or error changes
<form.Field
  name="email"
  children={(field) => {
    // useStore renders only on field.state changes
    return <EmailInput {...field} />;
  }}
/>

// Subscribe to specific state with form.Subscribe
<form.Subscribe
  selector={(state) => [state.values.email, state.errors.email]}
  children={([email, error]) => <EmailStatus value={email} error={error} />}
>
```

### 3. Async Validation with Debounce

```typescript
const form = useForm({
  defaultValues: { username: '' },
  validators: {
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: z.string().refine(async (val) => {
      const res = await fetch(`/api/check-username?u=${val}`);
      const { exists } = await res.json();
      return !exists;
    }, 'Username is taken'),
  },
  onSubmit: async ({ value }) => console.log(value),
});
```

### 4. Dynamic Field Arrays

```typescript
<form.Field
  name="items"
  mode="array"
  children={(field) => (
    <div>
      {field.state.value.map((_, i) => (
        <form.Field
          key={i}
          name={`items[${i}].name`}
          children={(sub) => (
            <input
              value={sub.state.value}
              onChange={(e) => sub.handleChange(e.target.value)}
            />
          )}
        />
      ))}
      <button type="button" onClick={() => field.pushValue({ name: '', qty: 1, price: 0 })}>
        Add
      </button>
    </div>
  )}
/>
```

### 5. Framework-Agnostic Usage (Vue)

```typescript
// In a Vue component — same `useForm` API
import { useForm } from '@tanstack/vue-form';

const form = useForm({
  defaultValues: { email: '' },
  onSubmit: async ({ value }) => console.log(value),
});
```

## When to Choose TanStack Form

| Use TanStack Form | Stick with RHF |
|-------------------|----------------|
| Multi-framework team (React + Vue + Solid) | React-only project |
| Need maximum type-safety from schemas | RHF is "good enough" on types |
| Building a UI kit / design system | Single-app form library needs |
| Standard Schema support is required | Yup / Zod via resolver is fine |
| Complex dynamic forms (form builder) | Mostly static forms |
| Want to invest in a 2026+ library | Prefer the most-mature option |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mixing controlled `<input value={...}>` without `onChange` | Use `field.state.value` + `field.handleChange(e.target.value)` together |
| Calling `form.handleSubmit()` outside form onSubmit | Always call from `onSubmit` after `preventDefault()` |
| Not subscribing to submit state | Use `form.Subscribe` to read `canSubmit` and `isSubmitting` |
| Assuming RHF patterns apply | TanStack Form is subscription-based, not ref-based |

## Best Practices

1. **Pair with Standard Schema** (Zod / Valibot) — no resolver needed
2. **Use `field.Subscribe` for granular updates** — better than watching the whole form
3. **Validate per lifecycle** — `onChange`, `onBlur`, `onSubmit`, or async
4. **Debounce async validators** — `onChangeAsyncDebounceMs: 500`
5. **Adopt for UI libraries** — framework-agnostic = single investment
6. **Wrap in a custom `<Form>` component** — encapsulates the boilerplate

## Summary

- TanStack Form is the framework-agnostic, type-first form library for 2026
- First-class React, Vue, Solid, Svelte, Lit support — same API across all
- Granular subscriptions beat context-based re-renders for performance
- Standard Schema support (no resolver) — Zod, Valibot, ArkType, Yup
- Best for: multi-framework teams, UI libraries, dynamic forms

---

## Cheat Sheet

```text
TANSTACK FORM CHEAT SHEET
═══════════════════════════════════════════════════════════════

CORE API:
  useForm({
    defaultValues,
    validators: { onChange, onBlur, onSubmit, onChangeAsync, onBlurAsync, onSubmitAsync },
    onSubmit: async ({ value }) => { ... },
  })

  form.Field name="..." children={(field) => ...}
  form.Subscribe selector={...} children={...}

FIELD HELPERS:
  field.state.value          // current value
  field.state.meta           // { errors, isTouched, isDirty, … }
  field.handleChange(value)
  field.handleBlur()
  field.setValue(value)
  field.validate()

VALIDATION TIMING:
  onChange    sync
  onBlur      sync
  onSubmit    sync
  onChangeAsync  +  onChangeAsyncDebounceMs: 500
  onBlurAsync    +  onBlurAsyncDebounceMs
  onSubmitAsync

WHEN TO USE:
  • Multi-framework team      ✓
  • UI library                ✓
  • Maximum type inference    ✓
  • Complex dynamic forms     ✓
  • React-only, simple forms  → RHF is fine
```

---

## See Also

- [Design Patterns](../10-Design-Patterns/)
- [Formik](03-Formik.md)
- [React](../03-React/)
- [React Hook Form](01-React-Hook-Form.md)
- [Server Actions & Form Patterns](06-Server-Actions-and-Form-Patterns.md)
- [TypeScript](../02-TypeScript/)
- [Zod](02-Zod.md)


## References & Learn More

- [Standard Schema](https://github.com/standard-schema/standard-schema)
- [TanStack Form Documentation](https://tanstack.com/form)
- [TanStack Form GitHub](https://github.com/TanStack/form)
- [TanStack Form vs RHF](https://tanstack.com/form/latest/docs/comparison)
