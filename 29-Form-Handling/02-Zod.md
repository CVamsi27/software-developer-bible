---
section: Form Handling
category: Frontend
tags: [concept, reference]
---

# Zod

> Zod is a TypeScript-first schema declaration and validation library. It provides a concise, expressive syntax for defining data schemas, validating data at runtime, and inferring TypeScript types automatically.

## Definition

Zod is a runtime validator and static type generator. You declare a schema (the shape of valid data) and Zod provides: (1) `.parse()` to validate untrusted input, (2) `z.infer<typeof Schema>` to get a TypeScript type that matches the schema. One source of truth for both runtime and compile-time safety.

## Why It Matters (TL;DR)

- **Type safety** — `z.infer` produces a TypeScript type from the schema
- **Runtime validation** — validate API responses, form input, env vars
- **Composable** — schemas compose with `.merge`, `.extend`, `.pick`, `.omit`, `.partial`
- **Great errors** — structured `ZodError` with paths and codes
- **Transforms** — `.transform()` to normalize data on parse

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         ZOD ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Schema Definition                         │   │
│  │  • Define shape of valid data                                │   │
│  │  • Specify validation rules (min, max, regex, refine)       │   │
│  │  • Set default values (z.optional().default(...))           │   │
│  │  • Transformations (z.string().transform(toLowerCase))      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Validation Engine                         │   │
│  │  • Parse input data                                          │   │
│  │  • Apply rules in order, short-circuit on first failure     │   │
│  │  • Generate detailed, structured errors                     │   │
│  │  • Return typed result                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│         ┌────────────────────┼────────────────────┐                │
│         ▼                    ▼                    ▼                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  │  .safeParse │    │   .parse    │    │  z.infer<…> │            │
│  │  returns    │    │  throws on  │    │  TS type    │            │
│  │  Result     │    │  error      │    │  from schema│            │
│  └─────────────┘    └─────────────┘    └─────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Schemas

```typescript
import { z } from 'zod';

// Primitives
const name = z.string();
const age = z.number().int().positive();
const isActive = z.boolean();

// String validators
const email = z.string().email();
const url = z.string().url();
const uuid = z.string().uuid();
const slug = z.string().regex(/^[a-z0-9-]+$/);

// Object schema
const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(['admin', 'user', 'guest']).default('user'),
  createdAt: z.date(),
});

// Type inference — single source of truth
type User = z.infer<typeof userSchema>;
// → { id: string; name: string; email: string; age?: number; role: 'admin' | 'user' | 'guest'; createdAt: Date }
```

### 2. Complex Compositions

```typescript
// Nested objects
const addressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string().length(2),
  zip: z.string().regex(/^\d{5}(-\d{4})?$/),
  country: z.string().default('US'),
});

// Arrays with constraints
const tagsSchema = z.array(z.string().min(1)).min(1).max(10);

// Tuples
const coordSchema = z.tuple([z.number(), z.number()]);

// Discriminated unions (great for API responses)
const eventSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('keypress'), key: z.string() }),
  z.object({ type: z.literal('scroll'), offset: z.number() }),
]);

// Records
const metadataSchema = z.record(z.string(), z.union([z.string(), z.number()]));
```

### 3. Transforms and Preprocess

```typescript
// Transform: normalize on parse
const formSchema = z.object({
  email: z.string().transform((v) => v.toLowerCase().trim()),
  age: z.string().transform((v) => parseInt(v, 10)),
  birthday: z.string().transform((v) => new Date(v)),
});

// Preprocess: accept multiple input shapes
const numberFromAnything = z.preprocess(
  (v) => (typeof v === 'string' ? parseFloat(v) : v),
  z.number()
);

// Coercion (built-in shortcut)
const numberFromForm = z.coerce.number();   // string → number
```

### 4. Cross-Field Validation with `superRefine`

```typescript
const passwordSchema = z
  .object({
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'Passwords do not match',
        path: ['confirmPassword'],
      });
    }
  });

// Alternative: .refine (single-condition, single-path)
const sameAs = z
  .object({ password: z.string(), confirm: z.string() })
  .refine((d) => d.password === d.confirm, {
    message: 'Passwords do not match',
    path: ['confirm'],
  });
```

### 5. React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: 'onBlur',
  });

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <input type="email" {...register('email')} />
      {errors.email?.message && <span>{errors.email.message}</span>}
      <input type="password" {...register('password')} />
      {errors.password?.message && <span>{errors.password.message}</span>}
      <button type="submit">Login</button>
    </form>
  );
}
```

### 6. API Boundary Validation (tRPC / Server Actions / REST)

```typescript
// Server-side: validate untrusted input
export async function POST(request: Request) {
  const body = await request.json();
  const parsed = CreateUserSchema.safeParse(body);

  if (!parsed.success) {
    return Response.json({ errors: parsed.error.flatten() }, { status: 400 });
  }

  // parsed.data is fully typed
  const user = await db.user.create({ data: parsed.data });
  return Response.json(user);
}

// Client-side: validate API response
const userResponseSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  createdAt: z.string().datetime(),
});

export async function fetchUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  const data = userResponseSchema.parse(await res.json());
  return data;  // typed as User
}
```

### 7. Environment Variable Validation

```typescript
// env.ts — run on app start, fail fast
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  PORT: z.coerce.number().int().positive().default(3000),
});

export const env = envSchema.parse(process.env);
```

## Real-World Use Cases

### Form Validation Pipeline

```text
Client Form:
  • Zod schema defines the valid shape
  • React Hook Form uses zodResolver to validate
  • TypeScript infers form data type from `z.infer<typeof schema>`
  • On submit, the data is guaranteed to match the schema

API Request:
  • Client sends the validated data
  • Server re-validates with the same schema (shared types package)
  • 400 on validation failure with structured errors
  • 200 with the typed response

API Response:
  • Server returns data matching the response schema
  • Client validates on receive (catches contract drift)
  • Throws or returns typed data
```

### End-to-End Type Safety (tRPC + Zod)

```typescript
// Server router — input schema, output schema
import { z } from 'zod';
import { publicProcedure, router } from './trpc';

export const userRouter = router({
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .output(z.object({
      id: z.string().uuid(),
      name: z.string(),
      email: z.string().email(),
    }))
    .query(({ input, ctx }) => {
      return ctx.db.user.findUniqueOrThrow({ where: { id: input.id } });
    }),
});

// Client — fully typed, no manual DTOs
const user = await trpc.user.getById.query({ id: '...' });
//    ^? { id: string; name: string; email: string }
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Manually defining types instead of `z.infer` | Always use `z.infer<typeof Schema>` — one source of truth |
| Over-validating | Don't validate internal data; only validate at boundaries (forms, API, env) |
| Not using `.safeParse` for expected failures | Use `.safeParse` (returns result) for user input; `.parse` (throws) for trusted internal data |
| Missing `z.coerce` for query params / form data | `?page=1` arrives as a string — use `z.coerce.number()` |
| No defaults | Use `.default()` for optional fields with a sensible default; safer than `undefined` |
| Using `z.any()` | Avoid — defeats the purpose. Use `z.unknown()` and refine if needed |

## Best Practices

1. **Use `z.infer` everywhere** — no separate TS interfaces for validated data
2. **Validate at boundaries** — forms, API requests, API responses, env vars
3. **Compose schemas** — `UserSchema.pick({ email: true })` for partial validation
4. **Custom error messages** — `.email('Please enter a valid email')`
5. **Use `safeParse` for user input** — handle the result, don't catch throws
6. **Centralize shared schemas** — `packages/contracts` for cross-bundle schemas
7. **Use `.brand()` for nominal types** — `z.string().uuid().brand<'UserId'>()` for type-safe IDs

## Performance Considerations

```text
Zod Performance:
┌─────────────────────────────────────────────────────────────────┐
│  Fast Validation:                                                │
│  • Optimized engine — short-circuit on first error              │
│  • No reflection or codegen                                       │
│  • Minimal allocations                                           │
│                                                                 │
│  Bundle Size:                                                    │
│  • ~14 KB gzipped (full)                                         │
│  • ~3 KB for z.coerce / z.lazy modules                          │
│  • Tree-shakeable — only import what you use                     │
│                                                                 │
│  Validation Cost:                                                │
│  • Object with 10 fields: ~50µs typical                         │
│  • Array of 100 items: ~500µs typical                           │
│  • Negligible for typical API/form payloads                      │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- Zod is the de-facto TypeScript validation library — one schema = runtime validator + TypeScript type
- Compose with `.merge`, `.extend`, `.pick`, `.partial`, `.refine`, `.superRefine`
- Use `z.infer<typeof Schema>` to derive TS types — no manual interfaces
- Validate at boundaries: forms, API requests, API responses, environment variables
- `safeParse` for user input (returns result); `parse` for trusted internal data (throws)

---

## Cheat Sheet

```text
ZOD CHEAT SHEET
═══════════════════════════════════════════════════════════════

CORE API:
  z.string() / z.number() / z.boolean() / z.date()
  z.string().min(n).max(n).email().url().uuid().regex(rx)
  z.number().int().positive().min(0).max(100)
  z.array(item).min(1).max(10)
  z.object({ field: z.string() })
  z.enum(['a', 'b', 'c'])
  z.union([a, b])
  z.discriminatedUnion('type', [a, b])    // tagged union
  z.literal('exact')                       // exact value
  z.tuple([a, b])
  z.record(key, value)                     // Record<K, V>
  z.coerce.number()                        // string → number

TRANSFORM:
  z.string().transform(v => v.toLowerCase())
  z.preprocess(v => parseInt(v), z.number())

INFERENCE:
  type T = z.infer<typeof Schema>          // type from schema
  type Input = z.input<typeof Schema>      // pre-transform input
  type Output = z.output<typeof Schema>    // post-transform output

VALIDATION:
  Schema.parse(data)        // throws on error
  Schema.safeParse(data)    // returns { success, data | error }

INTERVIEW ANSWER:
  1. Single source of truth (schema = type + validator)
  2. Validate at boundaries (form, API, env)
  3. Composable with refine / superRefine
  4. Pairs with RHF via zodResolver
```

---

## See Also

- [Design Patterns](../10-Design-Patterns/)
- [Formik](03-Formik.md)
- [React](../03-React/)
- [React Hook Form](01-React-Hook-Form.md)
- [Server Actions & Form Patterns](06-Server-Actions-and-Form-Patterns.md)
- [TanStack Form](05-TanStack-Form.md)
- [TypeScript](../02-TypeScript/)


## References & Learn More

- [React Hook Form Resolvers](https://github.com/react-hook-form/resolvers)
- [tRPC + Zod](https://trpc.io/docs/)
- [Zod Documentation](https://zod.dev/)
- [Zod GitHub](https://github.com/colinhacks/zod)
- [Zod Mini (smaller bundle)](https://zod.dev/packages/mini)
