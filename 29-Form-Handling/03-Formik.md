---
section: Form Handling
category: Frontend
tags: [concept, reference]
---

# Formik

> Formik is a long-standing React form library that uses controlled components and renders its own context to manage form state, validation, and submission. While RHF has surpassed it in popularity, Formik remains in production at many companies and is worth understanding for interview contexts.

## Definition

Formik is a React form library that ships three primitives: a `<Formik>` component (or `useFormik` hook), `<Field>` and `<ErrorMessage>`. It uses React context to expose `values`, `errors`, `touched`, `handleChange`, `handleBlur`, and `handleSubmit` to child components. The library is in maintenance mode as of 2024 — RHF is the modern alternative.

## Why It Matters (TL;DR)

- **Mature API** — battle-tested, used in production for years
- **Render-prop and hook** — both `<Formik>` and `useFormik()` styles
- **Yup integration** — built-in `validationSchema` prop (Zod works via adapter)
- **Field-level control** — `<Field as="textarea">` for non-input elements
- **Interview context** — many existing codebases still use Formik

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        FORMIK ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    <Formik> Component / useFormik Hook       │   │
│  │  • values: current form values                              │   │
│  │  • errors: validation errors                                 │   │
│  │  • touched: which fields have been blurred                  │   │
│  │  • handleChange / handleBlur / handleSubmit                 │   │
│  │  • isSubmitting: in-flight submission                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Controlled-Component Approach                   │   │
│  │  • <Field> wraps inputs with value/onChange/onBlur           │   │
│  │  • Re-renders on every change (slower than RHF)            │   │
│  │  • shouldComponentUpdate mitigations in <Field>              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Validation Layer                            │   │
│  │  • Yup schema (default — validationSchema prop)             │   │
│  │  • Custom validate functions (validate prop)                 │   │
│  │  • Field-level (Field's validate prop) or form-level        │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Formik Component (Render Prop Style)

```typescript
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const loginSchema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(8, 'Min 8 characters').required('Required'),
});

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={loginSchema}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          await api.login(values);
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <Form>
          <label htmlFor="email">Email</label>
          <Field id="email" name="email" type="email" />
          <ErrorMessage name="email" component="div" className="error" />

          <label htmlFor="password">Password</label>
          <Field id="password" name="password" type="password" />
          <ErrorMessage name="password" component="div" className="error" />

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Logging in…' : 'Login'}
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

### 2. useFormik Hook Style

```typescript
import { useFormik } from 'formik';
import * as Yup from 'yup';

const schema = Yup.object({
  username: Yup.string().min(3).required(),
  email: Yup.string().email().required(),
  password: Yup.string().min(8).required(),
  confirm: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Please confirm'),
});

function RegisterForm() {
  const formik = useFormik({
    initialValues: { username: '', email: '', password: '', confirm: '' },
    validationSchema: schema,
    onSubmit: (values) => console.log(values),
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <input
        name="username"
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        value={formik.values.username}
      />
      {formik.touched.username && formik.errors.username && (
        <div className="error">{formik.errors.username}</div>
      )}
      {/* … more fields … */}
      <button type="submit" disabled={formik.isSubmitting}>Register</button>
    </form>
  );
}
```

### 3. Custom Field Component (useField)

```typescript
import { useField, type FieldProps } from 'formik';

interface CustomInputProps extends FieldProps {
  label: string;
  type?: string;
}

function CustomInput({ label, type = 'text', ...props }: CustomInputProps) {
  const [field, meta] = useField(props);
  const hasError = meta.touched && meta.error;
  return (
    <div className="form-group">
      <label htmlFor={field.name}>{label}</label>
      <input
        {...field}
        id={field.name}
        type={type}
        className={hasError ? 'input-error' : ''}
        aria-invalid={hasError ? 'true' : 'false'}
      />
      {hasError && <div className="error">{meta.error}</div>}
    </div>
  );
}

// Usage
<Formik initialValues={{ name: '', email: '' }} onSubmit={…}>
  <Form>
    <CustomInput label="Name" name="name" />
    <CustomInput label="Email" name="email" type="email" />
    <button type="submit">Send</button>
  </Form>
</Formik>
```

### 4. FieldArray for Dynamic Fields

```typescript
import { Formik, Form, Field, FieldArray } from 'formik';

interface OrderItem { name: string; qty: number; price: number; }

function OrderForm() {
  const initialValues = {
    customer: '',
    items: [{ name: '', qty: 1, price: 0 }] as OrderItem[],
  };

  return (
    <Formik initialValues={initialValues} onSubmit={console.log}>
      {({ values }) => (
        <Form>
          <Field name="customer" placeholder="Customer" />

          <FieldArray name="items">
            {({ push, remove }) => (
              <div>
                {values.items.map((item, index) => (
                  <div key={index}>
                    <Field name={`items.${index}.name`} placeholder="Item" />
                    <Field name={`items.${index}.qty`} type="number" />
                    <Field name={`items.${index}.price`} type="number" />
                    <button type="button" onClick={() => remove(index)}>×</button>
                  </div>
                ))}
                <button type="button" onClick={() => push({ name: '', qty: 1, price: 0 })}>
                  Add item
                </button>
              </div>
            )}
          </FieldArray>

          <strong>
            Total: ${values.items.reduce((s, i) => s + i.qty * i.price, 0).toFixed(2)}
          </strong>
          <button type="submit">Place order</button>
        </Form>
      )}
    </Formik>
  );
}
```

### 5. Zod Instead of Yup (Modern Adapters)

```typescript
import { Formik } from 'formik';
import { z } from 'zod';
import { toFormikValidationSchema } from 'zod-formik-adapter';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

<Formik
  initialValues={{ email: '', password: '' }}
  validationSchema={toFormikValidationSchema(schema)}
  onSubmit={console.log}
>
  {/* … */}
</Formik>
```

### 6. Custom Validation Function

```typescript
<Formik
  initialValues={{ email: '', password: '' }}
  validate={(values) => {
    const errors: Record<string, string> = {};
    if (!values.email) errors.email = 'Required';
    else if (!/^[^@]+@[^@]+\.[^@]+$/.test(values.email)) errors.email = 'Invalid';
    if (values.password.length < 8) errors.password = 'Min 8';
    return errors;
  }}
  onSubmit={console.log}
>
  {/* … */}
</Formik>
```

### 7. Multi-Step Form

```typescript
function MultiStepForm() {
  const [step, setStep] = useState(1);

  const step1Schema = Yup.object({ name: Yup.string().required(), email: Yup.string().email().required() });
  const step2Schema = Yup.object({ address: Yup.string().required(), city: Yup.string().required() });

  return (
    <Formik
      initialValues={{ name: '', email: '', address: '', city: '' }}
      validationSchema={step === 1 ? step1Schema : step2Schema}
      onSubmit={(values, { setSubmitting }) => {
        if (step < 3) {
          setStep(step + 1);
        } else {
          console.log('submitting', values);
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <Form>
          {step === 1 && <Step1 />}
          {step === 2 && <Step2 />}
          {step === 3 && <Step3 />}
          {step > 1 && <button type="button" onClick={() => setStep(step - 1)}>Back</button>}
          <button type="submit" disabled={isSubmitting}>
            {step === 3 ? 'Submit' : 'Next'}
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

## Formik vs React Hook Form

| Dimension | Formik | React Hook Form |
|-----------|--------|-----------------|
| Year introduced | 2017 | 2019 |
| Architecture | Controlled components, context | Uncontrolled, ref-based |
| Re-renders | Every change re-renders the form | Refs read on demand — minimal re-renders |
| Bundle size | ~13 KB gzipped | ~9 KB gzipped |
| TypeScript | Decent (improved in v2) | Excellent (generic `useForm<T>`) |
| Schema validators | Yup (default), Zod via adapter | Zod / Yup / Valibot via resolver |
| Status (2026) | Maintenance mode | Actively developed |
| Best for | Existing codebases, transition | New projects |
| Performance (large forms) | Slower | Faster |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not checking `touched` before showing errors | Show errors only after blur / first submit — `{formik.touched.email && formik.errors.email && …}` |
| Over-validating on every keystroke | Use `validateOnBlur` and `validateOnChange` props carefully; default is fine for most |
| Forgetting to reset after submit | Use `resetForm()` in onSubmit's finally block |
| Using uncontrolled `<input>` inside Formik | Use `<Field>` or `useField` to keep the form in sync |
| No loading state on submit | Disable button with `disabled={isSubmitting}` |

## Best Practices

1. **Use `validationSchema` (Yup)** — declarative, clean, reusable
2. **Always check `touched` before showing errors** — avoid showing errors before user interaction
3. **Wrap submission with `setSubmitting`** — properly track loading state
4. **Use `<Field as="textarea">`** for text areas; `as="select"` for selects
5. **Build custom inputs with `useField`** — type-safe, encapsulated
6. **Migrate to RHF for new projects** — Formik is in maintenance
7. **Add `noValidate` to `<form>`** — disable native validation, use Formik's

## Summary

- Formik is a mature React form library using controlled components + context
- Status (2026): maintenance mode — RHF is the default for new projects
- Three primitives: `<Formik>`, `<Field>`, `<ErrorMessage>` (or `useFormik` + `useField`)
- Pairs naturally with Yup; Zod via `zod-formik-adapter`
- Best for: legacy codebases, controlled-component pattern preference

---

## Cheat Sheet

```text
FORMIK CHEAT SHEET
═══════════════════════════════════════════════════════════════

CORE API:
  <Formik initialValues={…} validationSchema={…} onSubmit={…}>
  useFormik({ initialValues, validationSchema, onSubmit })
  <Form>, <Field>, <ErrorMessage>, <FieldArray>
  useField(props)                 // custom field

PROPS:
  initialValues      object
  validationSchema   Yup / Zod schema
  validate           function
  onSubmit           (values, formikHelpers) => void
  enableReinitialize  boolean
  validateOnMount    boolean

RENDER PROPS:
  values, errors, touched, isSubmitting
  handleChange, handleBlur, handleSubmit
  setFieldValue, setFieldTouched, setFieldError
  resetForm, validateForm

INTERVIEW ANSWER:
  1. Controlled-component + context architecture
  2. Renders on every change (slower than RHF)
  3. Pairs with Yup; Zod via adapter
  4. Why most teams migrated to RHF
```

---

## See Also

- [Design Patterns](../10-Design-Patterns/)
- [React](../03-React/)
- [React Hook Form](01-React-Hook-Form.md)
- [Server Actions & Form Patterns](06-Server-Actions-and-Form-Patterns.md)
- [TanStack Form](05-TanStack-Form.md)
- [TypeScript](../02-TypeScript/)
- [Zod](02-Zod.md)


## References & Learn More

- [Formik Documentation](https://formik.org/)
- [Formik GitHub](https://github.com/jaredpalmer/formik)
- [Formik vs React Hook Form](https://blog.logrocket.com/react-hook-form-vs-formik-comparison/)
- [Yup Documentation](https://github.com/jquense/yup)
- [zod-formik-adapter](https://github.com/robertLichtnow/zod-formik-adapter)
