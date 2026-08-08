---
section: Form Handling
category: Frontend
tags: [concept, guide]
---

# Server Actions & Modern Form Patterns

> Server Actions (Next.js, Remix) blur the line between client and server by letting you submit forms directly to server functions. This file covers Server Actions, `useActionState`, `useFormStatus`, and progressive enhancement — the modern full-stack form pattern.

## Definition

A **Server Action** is an async function that runs on the server and is called from a client component (or directly from a form) via a special prop. They enable **progressive enhancement** — forms work without JavaScript, get progressively better with it. They pair with `useActionState` (formerly `useFormState`) and `useFormStatus` for pending UI.

## Why It Matters (TL;DR)

- **Progressive enhancement** — forms work without JS, get better with it
- **Less boilerplate** — no API route, no fetch, no client-side state for the action
- **Type-safe** — Server Action's args are typed end-to-end (Next.js 15+)
- **Revalidation** — automatic revalidation of the page after the action runs
- **Interview topic** — modern full-stack form pattern

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    SERVER ACTION FLOW                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Server (RSC + Action):                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  'use server'                                               │   │
│  │  export async function createUser(formData: FormData) { … }  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│                              │ form action={createUser}            │
│                              │                                      │
│  Client (Form):                                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  <form action={createUser}>                                  │   │
│  │    <input name="email" />                                    │   │
│  │    <button type="submit">Submit</button>                     │   │
│  │  </form>                                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  • Without JS: form submits to server, server runs action,         │
│    returns new HTML (full page reload)                              │
│  • With JS: Next.js intercepts, runs action, returns result,      │
│    updates only the affected components (revalidation)             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Plain Server Action (No JS Required)

```typescript
// app/actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const schema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContact(formData: FormData) {
  const parsed = schema.safeParse({
    email: formData.get('email'),
    message: formData.get('message'),
  });

  if (!parsed.success) {
    return { ok: false, errors: parsed.error.flatten().fieldErrors };
  }

  await db.message.create({ data: parsed.data });
  revalidatePath('/contact');
  return { ok: true };
}
```

```typescript
// app/contact/page.tsx
import { submitContact } from '../actions';

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" required />
      <label htmlFor="message">Message</label>
      <textarea id="message" name="message" required minLength={10} />
      <button type="submit">Send</button>
    </form>
  );
}
```

### 2. With `useActionState` (Pending + Errors)

```typescript
'use client';

import { useActionState } from 'react';
import { submitContact } from './actions';

type State = { ok: boolean; errors?: Record<string, string[]> } | null;

export function ContactForm() {
  const [state, formAction, isPending] = useActionState<State, FormData>(
    async (_prev, formData) => submitContact(formData),
    null
  );

  return (
    <form action={formAction}>
      <input name="email" type="email" required />
      {state?.errors?.email && <span role="alert">{state.errors.email[0]}</span>}

      <textarea name="message" required minLength={10} />
      {state?.errors?.message && <span role="alert">{state.errors.message[0]}</span>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Sending…' : 'Send'}
      </button>

      {state?.ok && <p>Message sent!</p>}
    </form>
  );
}
```

### 3. `useFormStatus` for Submit Button

```typescript
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting…' : 'Submit'}
    </button>
  );
}

export function MyForm() {
  return (
    <form action={submitContact}>
      {/* fields */}
      <SubmitButton />
    </form>
  );
}
```

### 4. Bound Args (Server Action with Parameters)

```typescript
'use server';

export async function updateUser(userId: string, formData: FormData) {
  // ...
}

// In a client component — bind the id
const updateUserBound = updateUser.bind(null, user.id);

<form action={updateUserBound}>
  <input name="name" defaultValue={user.name} />
  <button>Save</button>
</form>
```

### 5. Server Action with Zod + RHF (Hybrid)

```typescript
// actions.ts
'use server';

import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function signup(formData: FormData) {
  const parsed = schema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  });
  if (!parsed.success) return { error: parsed.error.flatten() };
  await db.user.create({ data: parsed.data });
  return { success: true };
}
```

```typescript
// SignupForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { signup } from './actions';

const schema = z.object({ email: z.string().email(), password: z.string().min(8) });
type FormData = z.infer<typeof schema>;

export function SignupForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: FormData) => {
    const fd = new FormData();
    fd.append('email', data.email);
    fd.append('password', data.password);
    const result = await signup(fd);
    if (result.error) console.error(result.error);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}
      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}
      <button type="submit" disabled={isSubmitting}>Sign up</button>
    </form>
  );
}
```

### 6. Optimistic UI with `useOptimistic` (React 19)

```typescript
'use client';

import { useOptimistic } from 'react';
import { sendMessage } from './actions';

type Message = { id: string; text: string; pending?: boolean };

export function MessageForm({ messages }: { messages: Message[] }) {
  const [optimistic, addOptimistic] = useOptimistic(
    messages,
    (state, newMsg: Message) => [...state, newMsg]
  );

  async function action(formData: FormData) {
    const text = formData.get('text') as string;
    addOptimistic({ id: crypto.randomUUID(), text, pending: true });
    await sendMessage(text);
  }

  return (
    <>
      <form action={action}>
        <input name="text" required />
        <button>Send</button>
      </form>
      <ul>
        {optimistic.map((m) => (
          <li key={m.id} style={{ opacity: m.pending ? 0.5 : 1 }}>
            {m.text}
          </li>
        ))}
      </ul>
    </>
  );
}
```

### 7. Remix Action (The Other Flavor)

```typescript
// app/routes/contact.tsx
import { Form, useActionData, useNavigation } from '@remix-run/react';
import { json, type ActionFunctionArgs } from '@remix-run/node';

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const email = formData.get('email');
  // validate, save, return
  return json({ ok: true });
}

export default function Contact() {
  const data = useActionData<typeof action>();
  const nav = useNavigation();
  const submitting = nav.state === 'submitting';

  return (
    <Form method="post">
      <input name="email" type="email" required />
      <button type="submit" disabled={submitting}>
        {submitting ? 'Sending…' : 'Send'}
      </button>
      {data?.ok && <p>Sent!</p>}
    </Form>
  );
}
```

## Server Action Patterns

```text
PROGRESSIVE ENHANCEMENT CHECKLIST:
┌─────────────────────────────────────────────────────────────────┐
│  ✓ form action={serverAction} — works without JS                │
│  ✓ required, minLength, pattern on inputs — browser-side        │
│  ✓ Server-side Zod validation — re-validates everything         │
│  ✓ useActionState — graceful error display with JS              │
│  ✓ useFormStatus — pending button state with JS                │
│  ✓ useOptimistic — instant feedback with JS                    │
│  ✓ revalidatePath / revalidateTag — fresh data after action     │
│  ✓ redirect() inside action — post-submit navigation            │
└─────────────────────────────────────────────────────────────────┘
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trusting client validation alone | Always re-validate on the server (Zod shared in `packages/contracts`) |
| Calling `useFormStatus` outside a `<form>` | It only works inside a form that has a pending action |
| Returning complex types from actions | Stick to plain serializable objects (no class instances, dates as strings) |
| Not handling the `isPending` state | Disable the submit button to prevent double-submit |
| Mixing Server Actions and REST APIs in the same form | Pick one; mixing leads to confusion about where validation happens |
| Forgetting `revalidatePath` | The page won't update with the new data after a mutation |

## Best Practices

1. **Use `action={serverAction}` directly** — simplest pattern, works without JS
2. **Re-validate on the server with Zod** — never trust the client
3. **Return plain serializable state from actions** — `{ ok, errors }` shape
4. **Use `useFormStatus` for the submit button** — clean pending state
5. **Use `useOptimistic` for instant feedback** — list updates before server confirms
6. **Revalidate with `revalidatePath` or `revalidateTag`** — keep data fresh
7. **Place actions in a `actions.ts` file with `'use server'`** — easy to find
8. **Pair with shared Zod schema** — single source of truth client + server

## Summary

- Server Actions let you submit forms to server functions with progressive enhancement
- `useActionState` + `useFormStatus` give you pending state and error display
- `useOptimistic` enables instant UI feedback (React 19)
- Always re-validate on the server; never trust the client
- Combine with Zod for a single source of truth across the boundary

---

## Cheat Sheet

```text
SERVER ACTIONS CHEAT SHEET
═══════════════════════════════════════════════════════════════

PRIMITIVES (React 19 / Next.js 15):
  'use server'                    → mark server function
  <form action={serverAction}>    → works without JS
  useActionState                  → [state, action, isPending]
  useFormStatus                   → { pending } inside a form
  useOptimistic                   → optimistic value with rollback
  revalidatePath / revalidateTag  → refresh data after mutation

RECOMMENDED FLOW:
  1. Define 'use server' function in actions.ts
  2. Re-validate input with Zod
  3. Perform mutation (DB write / API call)
  4. revalidatePath() to refresh data
  5. Return { ok, errors } plain object

PROGRESSIVE ENHANCEMENT:
  • No JS: form POSTs, server runs action, returns new HTML
  • With JS: Next.js intercepts, runs action in-place, revalidates
  • Always works — just progressively better

INTERVIEW ANSWER:
  1. What Server Actions solve (no API route, type-safe, progressive)
  2. How useActionState + useFormStatus combine for pending UX
  3. Why server re-validation is still required
  4. Compare to REST / tRPC: when each wins
```

---

## See Also

- [Formik](03-Formik.md)
- [Next.js Server Actions](../04-NextJS/)
- [React Hook Form](01-React-Hook-Form.md)
- [REST APIs](../07-REST-API/)
- [TanStack Form](05-TanStack-Form.md)
- [Zod](02-Zod.md)


## References & Learn More

- [Next.js Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Progressive Enhancement (MDN)](https://developer.mozilla.org/en-US/docs/Glossary/Progressive_Enhancement)
- [React 19 useActionState](https://react.dev/reference/react/useActionState)
- [React 19 useOptimistic](https://react.dev/reference/react/useOptimistic)
- [Remix Forms](https://remix.run/docs/en/main/guides/forms)
