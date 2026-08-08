---
section: Form Handling
category: Frontend
tags: [concept, reference]
---

# React Hook Form

> React Hook Form is a performance-first form library for React that uses uncontrolled components and refs to minimize re-renders while providing a simple, ergonomic API for validation, dynamic fields, and form state.

## Definition

React Hook Form (RHF) is a React form library that minimizes re-renders by using uncontrolled inputs (refs) instead of state. It exposes a `useForm` hook that returns `register`, `handleSubmit`, `formState`, and other helpers, and integrates cleanly with schema validators (Zod, Yup) via resolvers.

## Why It Matters (TL;DR)

- **Performance** — uncontrolled inputs, no per-keystroke re-renders
- **Tiny bundle** — ~9 KB gzipped, zero dependencies
- **Excellent TypeScript** — generic-typed `useForm<T>` infers field types
- **Schema validation** — plug in Zod / Yup / Valibot via `@hookform/resolvers`
- **Built-in dynamic fields** — `useFieldArray` for repeated inputs

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    REACT HOOK FORM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    useForm Hook                               │   │
│  │  • register: bind input to form state via ref                │   │
│  │  • handleSubmit: validate → call onSubmit                    │   │
│  │  • formState: errors, isSubmitting, isValid, dirty, touched │   │
│  │  • control: Controller for controlled components            │   │
│  │  • watch: subscribe to field value changes                  │   │
│  │  • reset / setValue / trigger: imperative APIs               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Uncontrolled Inputs (refs)                  │   │
│  │  • Native HTML input value, no React state per keystroke   │   │
│  │  • RHF reads value on submit / on validate                  │   │
│  │  • Re-renders only on state changes that matter             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Validation Layer                            │   │
│  │  • Built-in HTML5 rules (required, min, max, pattern)        │   │
│  │  • Schema (Zod / Yup / Valibot) via resolver                │   │
│  │  • Custom async validators (e.g., username available?)     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Form with `useForm`

```typescript
import { useForm } from 'react-hook-form';

interface LoginForm {
  email: string;
  password: string;
}

function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    defaultValues: { email: '', password: '' },
  });

  const onSubmit = async (data: LoginForm) => {
    await api.login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          {...register('email', {
            required: 'Email is required',
            pattern: { value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i, message: 'Invalid email' },
          })}
        />
        {errors.email && <span role="alert">{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          {...register('password', {
            required: 'Password is required',
            minLength: { value: 8, message: 'Min 8 characters' },
          })}
        />
        {errors.password && <span role="alert">{errors.password.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in…' : 'Login'}
      </button>
    </form>
  );
}
```

### 2. Zod Schema Validation (Recommended)

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const registerSchema = z.object({
  username: z.string().min(3, 'Min 3 characters'),
  email: z.string().email(),
  password: z
    .string()
    .min(8, 'Min 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[0-9]/, 'Must contain a number'),
  confirmPassword: z.string(),
}).refine((d) => d.password === d.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

function RegisterForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    mode: 'onBlur',     // validate on blur (or 'onChange', 'onTouched', 'all')
  });

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input {...register('username')} />
      {errors.username?.message && <span>{errors.username.message}</span>}
      {/* … more fields … */}
    </form>
  );
}
```

### 3. Controller for Controlled Components (Select, Date Picker)

```typescript
import { Controller, useForm } from 'react-hook-form';
import Select from 'react-select';
import DatePicker from 'react-datepicker';

function EventForm() {
  const { control, handleSubmit, register, formState: { errors } } = useForm<{
    name: string;
    category: { value: string; label: string } | null;
    date: Date | null;
  }>({
    defaultValues: { name: '', category: null, date: null },
  });

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input {...register('name', { required: 'Required' })} />
      {errors.name && <span>Required</span>}

      <Controller
        name="category"
        control={control}
        rules={{ required: 'Pick a category' }}
        render={({ field }) => (
          <Select
            {...field}
            options={[
              { value: 'conf', label: 'Conference' },
              { value: 'meet', label: 'Meetup' },
            ]}
          />
        )}
      />

      <Controller
        name="date"
        control={control}
        render={({ field }) => (
          <DatePicker selected={field.value} onChange={field.onChange} />
        )}
      />
    </form>
  );
}
```

### 4. Dynamic Field Arrays

```typescript
import { useForm, useFieldArray } from 'react-hook-form';

interface OrderForm {
  customer: string;
  items: { name: string; qty: number; price: number }[];
}

function OrderForm() {
  const { register, control, handleSubmit, watch, formState: { errors } } = useForm<OrderForm>({
    defaultValues: { customer: '', items: [{ name: '', qty: 1, price: 0 }] },
  });

  const { fields, append, remove } = useFieldArray({ control, name: 'items' });
  const items = watch('items');
  const total = items.reduce((sum, i) => sum + i.qty * i.price, 0);

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input {...register('customer', { required: true })} />

      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`items.${index}.name`, { required: true })} placeholder="Item" />
          <input type="number" {...register(`items.${index}.qty`, { valueAsNumber: true, min: 1 })} />
          <input type="number" {...register(`items.${index}.price`, { valueAsNumber: true, min: 0 })} />
          <button type="button" onClick={() => remove(index)}>×</button>
        </div>
      ))}

      <button type="button" onClick={() => append({ name: '', qty: 1, price: 0 })}>
        Add item
      </button>
      <strong>Total: ${total.toFixed(2)}</strong>
      <button type="submit">Place order</button>
    </form>
  );
}
```

### 5. Async Validation (Username Available Check)

```typescript
function UsernameForm() {
  const { register, handleSubmit, formState: { errors, isValidating } } = useForm<{ username: string }>({
    mode: 'onChange',
  });

  const checkUsername = async (value: string) => {
    const res = await fetch(`/api/check-username?username=${value}`);
    const { exists } = await res.json();
    return exists ? 'Username is taken' : true;
  };

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input {...register('username', {
        required: 'Required',
        minLength: { value: 3, message: 'Min 3' },
        validate: checkUsername,
      })} />
      {isValidating && <span>Checking…</span>}
      {errors.username && <span>{errors.username.message}</span>}
      <button type="submit">Save</button>
    </form>
  );
}
```

### 6. Multi-Step Form (FormProvider)

```typescript
import { FormProvider, useForm } from 'react-hook-form';

function MultiStepForm() {
  const methods = useForm({ mode: 'onChange' });
  const [step, setStep] = useState(1);

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(console.log)}>
        {step === 1 && <Step1 />}
        {step === 2 && <Step2 />}
        {step === 3 && <Step3 />}

        {step > 1 && <button type="button" onClick={() => setStep(step - 1)}>Back</button>}
        <button type="submit">{step === 3 ? 'Submit' : 'Next'}</button>
      </form>
    </FormProvider>
  );
}

// Step components use useFormContext() to access methods
function Step1() {
  const { register, formState: { errors } } = useFormContext();
  return <input {...register('name', { required: true })} />;
}
```

## Real-World Use Cases

### Multi-Step Onboarding

```text
Onboarding flow with cross-step state:
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Account (email, password)                              │
│  Step 2: Profile (name, avatar)                                 │
│  Step 3: Preferences (notifications, theme)                     │
│                                                                 │
│  FormProvider keeps all step values in one form context.        │
│  Validate each step with `trigger(['name', 'email'])` before    │
│  advancing. Submit on final step.                                │
└─────────────────────────────────────────────────────────────────┘
```

### Dynamic Invoice Items

```text
Invoice editor with line items:
┌─────────────────────────────────────────────────────────────────┐
│  Customer info + useFieldArray for invoice items                │
│                                                                 │
│  Each row: { description, qty, price, tax }                     │
│  Add / remove / reorder rows                                    │
│  Compute total via watch() + reduce                             │
│  Submit sends the full invoice payload                          │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `Controller` for native `<input>` | Use `register` — it's faster (no re-render) |
| Forgetting `defaultValues` | Without them, uncontrolled inputs start as `undefined` and `watch()` breaks |
| Watching the whole form on every change | Watch specific fields: `watch('email')` not `watch()` |
| No `mode` set | Default `mode: 'onSubmit'` — show errors only after submit. Use `mode: 'onBlur'` for friendlier UX |
| Mixing controlled and uncontrolled | Pick one style per field. Use `Controller` only for third-party controlled components |
| Not memoizing the submit handler | Wrap `onSubmit` in `useCallback` if it has dependencies, otherwise `handleSubmit` will re-fire unnecessarily |

## Best Practices

1. **Pair with Zod** — single schema gives runtime validation + TypeScript types via `z.infer`
2. **Use `register` for native inputs** — only `Controller` for third-party controlled components
3. **Set `mode: 'onBlur'`** — validate as user leaves field, not on every keystroke
4. **`useFieldArray` for dynamic lists** — built-in, no manual state
5. **`FormProvider` for complex forms** — share context across sub-components
6. **Debounce async validators** — don't hit the server on every keystroke
7. **Disable submit while `isSubmitting`** — prevent double-submit

## Performance Considerations

```text
React Hook Form Performance:
┌─────────────────────────────────────────────────────────────────┐
│  Why it's fast:                                                 │
│  • Uncontrolled inputs — no per-keystroke state update         │
│  • Refs read on demand — only when needed                       │
│  • Selective subscriptions — components re-render only when    │
│    the field they watch changes                                 │
│                                                                 │
│  Bundle:                                                        │
│  • ~9 KB gzipped                                                │
│  • Zero dependencies                                            │
│  • Tree-shakeable                                               │
│                                                                 │
│  Optimization tips:                                              │
│  • Use `register` over `Controller` (avoid React re-render)    │
│  • Watch specific fields, not the whole form                   │
│  • Use `shouldUnregister: true` to clean up fields on unmount │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- React Hook Form is the de-facto form library for React in 2026 — fast, tiny, type-safe
- Use `register` for native inputs; `Controller` only for third-party controlled components
- Pair with Zod via `@hookform/resolvers/zod` for type-safe validation
- `useFieldArray` for dynamic lists; `FormProvider` for multi-step or deeply-nested forms
- Uncontrolled inputs mean no re-renders on keystroke — best-in-class performance

---

## Cheat Sheet

```text
REACT HOOK FORM CHEAT SHEET
═══════════════════════════════════════════════════════════════

CORE API:
  useForm({ defaultValues, resolver, mode })
  register('field', { required, min, max, pattern, validate })
  handleSubmit(onValid, onInvalid)
  formState: { errors, isSubmitting, isValid, dirtyFields, touchedFields }
  watch('field')              → subscribe to changes
  setValue('field', value)    → imperative set
  reset(values?)              → clear or set new defaults
  trigger(['field'])          → re-validate manually

UTILITY HOOKS:
  useFieldArray({ control, name })  → dynamic lists
  useFormContext()                  → access useForm() in child
  Controller                        → wrap controlled components

MODE OPTIONS:
  onSubmit   → validate on submit (default)
  onBlur     → validate when field loses focus (recommended UX)
  onChange   → validate on every change
  onTouched   → on first blur, then on every change
  all        → onBlur + onChange

INTERVIEW ANSWER:
  1. Why RHF (uncontrolled, no re-renders, tiny)
  2. How register() works (ref-based, native input)
  3. When Controller is needed (third-party controlled)
  4. Zod resolver for type-safe validation
```

---

## See Also

- [Design Patterns](../10-Design-Patterns/)
- [Formik](03-Formik.md)
- [React](../03-React/)
- [Server Actions & Form Patterns](06-Server-Actions-and-Form-Patterns.md)
- [TanStack Form](05-TanStack-Form.md)
- [TypeScript](../02-TypeScript/)
- [Zod](02-Zod.md)


## References & Learn More

- [React Hook Form Documentation](https://react-hook-form.com/)
- [React Hook Form GitHub](https://github.com/react-hook-form/react-hook-form)
- [RHF Performance Guide](https://react-hook-form.com/advanced-usage#PerformanceOptimization)
- [useFieldArray](https://react-hook-form.com/docs/usefieldarray)
- [Zod Resolver](https://github.com/react-hook-form/resolvers)
