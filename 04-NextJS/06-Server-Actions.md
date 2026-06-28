# Server Actions in Next.js

## Definition

**Server Actions** are asynchronous functions that run on the server and can be called from Client Components or Server Components. They use the `'use server'` directive and enable form handling, data mutations, and progressive enhancement without creating API routes.

## Why Do We Need It?

1. **No API routes needed** — Simplifies data mutations
2. **Progressive enhancement** — Forms work without JavaScript
3. **Type safety** — End-to-end TypeScript types
4. **Security** — Server-side execution, no exposed endpoints
5. **Caching integration** — Automatic revalidation with `revalidatePath`/`revalidateTag`

## How It Works

### Server Actions Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                    SERVER ACTIONS FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Client Component (Browser)                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  <form action={createPost}>                              │   │
│  │    <input name="title" />                                │   │
│  │    <textarea name="content" />                           │   │
│  │    <button type="submit">Submit</button>                 │   │
│  │  </form>                                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  HTTP Request (POST)                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  POST /action/createPost                                 │   │
│  │  Body: { title: "...", content: "..." }                  │   │
│  │  Headers: Next-Action: <action-id>                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  Server Action Execution                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  'use server'                                            │   │
│  │  async function createPost(formData) {                   │   │
│  │    const title = formData.get('title')                   │   │
│  │    const content = formData.get('content')               │   │
│  │    await db.post.create({ data: { title, content } })   │   │
│  │    revalidatePath('/posts')                              │   │
│  │  }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  Response                                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Revalidate /posts page                                  │   │
│  │  Return success/error to client                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Server Actions vs API Routes

```text
┌─────────────────────────────────────────────────────────────────┐
│                  SERVER ACTIONS vs API ROUTES                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Server Actions:                                                │
│  ├─ Type-safe (end-to-end)                                      │
│  ├─ Automatic revalidation                                      │
│  ├─ Progressive enhancement                                     │
│  ├─ Built-in error handling                                     │
│  ├─ No exposed endpoint                                         │
│  └─ Simpler setup                                               │
│                                                                 │
│  API Routes:                                                    │
│  ├─ Full HTTP control                                           │
│  ├─ External API access                                         │
│  ├─ Webhook handling                                            │
│  ├─ File uploads                                                │
│  ├─ Custom response formats                                     │
│  └─ More flexible                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Server Action

```tsx
// app/actions/post.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { db } from '@/lib/database'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  if (!title || !content) {
    throw new Error('Title and content are required')
  }

  await db.post.create({
    data: { title, content },
  })

  revalidatePath('/posts')
  redirect('/posts')
}
```

### Using Server Action in Form

```tsx
// app/posts/new/page.tsx
import { createPost } from '../actions/post'

export default function NewPostPage() {
  return (
    <div>
      <h1>Create New Post</h1>
      <form action={createPost}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            name="title"
            required
          />
        </div>
        <div>
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            name="content"
            required
          />
        </div>
        <button type="submit">Create Post</button>
      </form>
    </div>
  )
}
```

### Server Action with Validation

```tsx
// app/actions/user.ts
'use server'

import { z } from 'zod'
import { revalidatePath } from 'next/cache'

const userSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().min(18).max(120),
})

interface ActionState {
  errors?: Record<string, string[]>
  success?: boolean
}

export async function createUser(
  prevState: ActionState,
  formData: FormData
): Promise<ActionState> {
  const rawData = {
    name: formData.get('name') as string,
    email: formData.get('email') as string,
    age: Number(formData.get('age')),
  }

  const validated = userSchema.safeParse(rawData)

  if (!validated.success) {
    return {
      errors: validated.error.flatten().fieldErrors,
    }
  }

  await db.user.create({
    data: validated.data,
  })

  revalidatePath('/users')
  return { success: true }
}
```

### Using useFormState Hook

```tsx
// app/users/new/page.tsx
'use client'

import { useFormState } from 'react-dom'
import { createUser } from '../actions/user'

export default function NewUserPage() {
  const [state, formAction] = useFormState(createUser, {})

  return (
    <div>
      <h1>Create User</h1>
      <form action={formAction}>
        <div>
          <label htmlFor="name">Name</label>
          <input type="text" id="name" name="name" required />
          {state.errors?.name && (
            <p className="error">{state.errors.name[0]}</p>
          )}
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input type="email" id="email" name="email" required />
          {state.errors?.email && (
            <p className="error">{state.errors.email[0]}</p>
          )}
        </div>
        <div>
          <label htmlFor="age">Age</label>
          <input type="number" id="age" name="age" required />
          {state.errors?.age && (
            <p className="error">{state.errors.age[0]}</p>
          )}
        </div>
        <button type="submit">Create</button>
        {state.success && <p className="success">User created!</p>}
      </form>
    </div>
  )
}
```

### Server Action with useFormStatus

```tsx
// app/actions/subscribe.ts
'use server'

export async function subscribe(formData: FormData) {
  const email = formData.get('email') as string

  await db.subscriber.create({
    data: { email },
  })

  return { success: true }
}
```

```tsx
// components/subscribe-form.tsx
'use client'

import { useFormStatus } from 'react-dom'
import { subscribe } from '../actions/subscribe'

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Subscribing...' : 'Subscribe'}
    </button>
  )
}

export function SubscribeForm() {
  return (
    <form action={subscribe}>
      <input
        type="email"
        name="email"
        placeholder="Enter your email"
        required
      />
      <SubmitButton />
    </form>
  )
}
```

### Server Action with useTransition

```tsx
// app/actions/like.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function toggleLike(postId: string) {
  const existingLike = await db.like.findFirst({
    where: { postId, userId: currentUserId },
  })

  if (existingLike) {
    await db.like.delete({ where: { id: existingLike.id } })
  } else {
    await db.like.create({
      data: { postId, userId: currentUserId },
    })
  }

  revalidatePath('/posts')
}
```

```tsx
// components/like-button.tsx
'use client'

import { useTransition } from 'react'
import { toggleLike } from '../actions/like'

export function LikeButton({ postId, initialLiked }: {
  postId: string
  initialLiked: boolean
}) {
  const [isPending, startTransition] = useTransition()

  return (
    <button
      onClick={() => startTransition(() => toggleLike(postId))}
      disabled={isPending}
      className={initialLiked ? 'liked' : ''}
    >
      {initialLiked ? '❤️' : '🤍'}
    </button>
  )
}
```

### Server Action with Optimistic Updates

```tsx
// components/todo-list.tsx
'use client'

import { useOptimistic } from 'react'
import { addTodo } from '../actions/todo'

interface Todo {
  id: string
  text: string
  completed: boolean
}

export function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    initialTodos,
    (state, newTodo: Omit<Todo, 'id'>) => [
      ...state,
      { ...newTodo, id: 'temp-' + Date.now() },
    ]
  )

  async function handleSubmit(formData: FormData) {
    const text = formData.get('text') as string

    addOptimisticTodo({ text, completed: false })
    await addTodo(formData)
  }

  return (
    <div>
      <form action={handleSubmit}>
        <input name="text" required />
        <button type="submit">Add</button>
      </form>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} className={todo.completed ? 'done' : ''}>
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

### Server Action with Cookies

```tsx
// app/actions/preferences.ts
'use server'

import { cookies } from 'next/headers'
import { revalidatePath } from 'next/cache'

export async function updatePreferences(formData: FormData) {
  const theme = formData.get('theme') as string
  const language = formData.get('language') as string

  const cookieStore = await cookies()

  cookieStore.set('preferences', JSON.stringify({ theme, language }), {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 365, // 1 year
  })

  revalidatePath('/')
}
```

### Server Action with Error Handling

```tsx
// app/actions/upload.ts
'use server'

import { revalidatePath } from 'next/cache'

interface UploadState {
  error?: string
  success?: boolean
  fileUrl?: string
}

export async function uploadFile(
  prevState: UploadState,
  formData: FormData
): Promise<UploadState> {
  const file = formData.get('file') as File

  if (!file) {
    return { error: 'No file provided' }
  }

  if (file.size > 5 * 1024 * 1024) {
    return { error: 'File size must be less than 5MB' }
  }

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    return { error: 'File type not allowed' }
  }

  try {
    const buffer = Buffer.from(await file.arrayBuffer())
    const filename = `${Date.now()}-${file.name}`

    // Upload to storage (e.g., S3, Cloudflare R2)
    const url = await uploadToStorage(buffer, filename)

    revalidatePath('/gallery')
    return { success: true, fileUrl: url }
  } catch (error) {
    return { error: 'Upload failed. Please try again.' }
  }
}
```

### Inline Server Action

```tsx
// app/posts/page.tsx
import { revalidatePath } from 'next/cache'

export default function PostsPage() {
  async function deletePost(formData: FormData) {
    'use server'

    const postId = formData.get('postId') as string

    await db.post.delete({
      where: { id: postId },
    })

    revalidatePath('/posts')
  }

  return (
    <div>
      <h1>Posts</h1>
      {/* Server action defined inline */}
      <form action={deletePost}>
        <input type="hidden" name="postId" value="123" />
        <button type="submit">Delete</button>
      </form>
    </div>
  )
}
```

### Server Action with File Upload

```tsx
// app/actions/upload-document.ts
'use server'

import { put } from '@vercel/blob'
import { revalidatePath } from 'next/cache'

export async function uploadDocument(formData: FormData) {
  const file = formData.get('file') as File

  if (!file) {
    throw new Error('No file provided')
  }

  const blob = await put(file.name, file, {
    access: 'public',
  })

  await db.document.create({
    data: {
      name: file.name,
      url: blob.url,
      size: file.size,
    },
  })

  revalidatePath('/documents')
}
```

### Server Action with Search Params

```tsx
// app/actions/search.ts
'use server'

import { redirect } from 'next/navigation'

export async function searchProducts(formData: FormData) {
  const query = formData.get('query') as string
  const category = formData.get('category') as string

  const params = new URLSearchParams()
  if (query) params.set('q', query)
  if (category) params.set('category', category)

  redirect(`/products?${params.toString()}`)
}
```

## Real-World Use Cases

| Use Case | Server Action Benefit |
|----------|----------------------|
| Form submission | Progressive enhancement, no API needed |
| CRUD operations | Type-safe, auto revalidation |
| File uploads | Server-side processing, security |
| Search/filtering | URL updates, server-side logic |
| Authentication | Secure server-side validation |
| Newsletter signup | Simple data mutation |
| Contact forms | No exposed endpoint |
| Shopping cart | Type-safe operations |

## Common Mistakes

### 1. Not Using 'use server' Directive

```tsx
// ❌ BAD: Missing directive
export async function createPost(formData: FormData) {
  await db.post.create({ data: { title: formData.get('title') } })
  // This won't work as a Server Action!
}

// ✅ GOOD: Add directive
'use server'

export async function createPost(formData: FormData) {
  await db.post.create({ data: { title: formData.get('title') } })
}
```

### 2. Returning Non-Serializable Data

```tsx
// ❌ BAD: Returning non-serializable data
'use server'

export async function getData() {
  return {
    date: new Date(), // Date object not serializable!
    fn: () => {}, // Functions not serializable!
  }
}

// ✅ GOOD: Return serializable data
'use server'

export async function getData() {
  return {
    date: new Date().toISOString(), // String
    value: 42, // Primitive
  }
}
```

### 3. Not Handling Errors

```tsx
// ❌ BAD: No error handling
'use server'

export async function updateUser(formData: FormData) {
  await db.user.update({
    where: { id: formData.get('id') },
    data: { name: formData.get('name') },
  })
  // What if it fails?
}

// ✅ GOOD: Proper error handling
'use server'

export async function updateUser(
  prevState: any,
  formData: FormData
) {
  try {
    await db.user.update({
      where: { id: formData.get('id') },
      data: { name: formData.get('name') },
    })
    revalidatePath('/users')
    return { success: true }
  } catch (error) {
    return { error: 'Failed to update user' }
  }
}
```

### 4. Not Using Revalidation

```tsx
// ❌ BAD: No revalidation after mutation
'use server'

export async function createPost(formData: FormData) {
  await db.post.create({
    data: { title: formData.get('title') },
  })
  // Page won't show new post!
}

// ✅ GOOD: Revalidate after mutation
'use server'

export async function createPost(formData: FormData) {
  await db.post.create({
    data: { title: formData.get('title') },
  })
  revalidatePath('/posts') // Refresh /posts page
  revalidateTag('posts') // Refresh all pages with 'posts' tag
}
```

### 5. Calling Server Action from Server Component

```tsx
// ❌ BAD: Direct call in Server Component
'use server'
export async function getData() {
  return { value: 42 }
}

export default async function Page() {
  const data = await getData() // Works but not ideal
  return <div>{data.value}</div>
}

// ✅ GOOD: Use directly in Server Component
export default async function Page() {
  const data = await db.post.findMany() // Direct data fetching
  return <div>{data.length} posts</div>
}
```

## Best Practices

1. **Use 'use server' directive** — Always at the top of the file or function
2. **Return serializable data** — No functions, Dates, or Maps
3. **Handle errors gracefully** — Return error states to client
4. **Use revalidation** — Call `revalidatePath` or `revalidateTag` after mutations
5. **Validate inputs** — Use Zod or similar for server-side validation
6. **Keep actions focused** — One action per operation
7. **Use useFormState for forms** — For error handling and state management
8. **Use useFormStatus for loading** — Show pending state during submission
9. **Test server actions** — Unit test the action logic separately
10. **Document action contracts** — Define clear input/output types

## Performance Considerations

```text
Server Actions Performance:
- Execute on server (no client JS overhead)
- Automatic revalidation avoids full page reload
- Progressive enhancement works without JS
- Type safety reduces runtime errors

Optimization:
- Keep actions focused and fast
- Use parallel revalidation when possible
- Implement proper error handling
- Cache frequently accessed data
```

## Interview Questions

### Beginner (5-10)

1. **What are Server Actions?**
   Server Actions are async functions that run on the server, called from Client or Server Components. They use `'use server'` directive and enable data mutations.

2. **How do you create a Server Action?**
   Add `'use server'` at the top of a file or function. Export the function and use it in forms or event handlers.

3. **What is the difference between Server Actions and API Routes?**
   Server Actions are simpler, type-safe, and integrated with caching. API Routes offer more control over HTTP requests/responses.

4. **How do you handle form submission with Server Actions?**
   Use the `action` prop on forms with a Server Action function. Access form data via `FormData` parameter.

5. **What is progressive enhancement?**
   Forms work without JavaScript enabled. Server Actions handle form submission on the server, making the app functional even without client-side code.

6. **How do you show loading state with Server Actions?**
   Use `useFormStatus` hook to access the `pending` state during form submission.

7. **How do you handle validation in Server Actions?**
   Validate on the server using Zod or similar libraries. Return validation errors to the client via return values.

8. **What is `revalidatePath`?**
   A function that invalidates the cache for a specific path, causing it to re-render with fresh data.

### Intermediate (5-10)

9. **How do you use `useFormState` with Server Actions?**
   `useFormState` manages form state and returns `[state, action]`. The Server Action receives previous state and FormData.

10. **How do you implement optimistic updates with Server Actions?**
    Use `useOptimistic` hook to immediately update UI, then call Server Action to persist changes.

11. **How do you handle file uploads with Server Actions?**
    Use `FormData` to access files, process them on the server, and upload to storage services.

12. **What is the relationship between Server Actions and caching?**
    Server Actions can call `revalidatePath` or `revalidateTag` to invalidate cache after mutations.

13. **How do you pass custom data to Server Actions?**
    Use hidden form fields, `formData.append()`, or call Server Actions directly with custom parameters.

14. **How do you handle multiple Server Actions in one form?**
    Use separate buttons with different `formAction` props or handle logic within a single action.

15. **What are the security considerations for Server Actions?**
    Always validate inputs server-side, use CSRF protection, implement rate limiting, and never trust client data.

### Senior (10-15)

16. **Design a comprehensive form system using Server Actions.**
    Use `useFormState` for state management, `useFormStatus` for loading states, Zod for validation, and Server Actions for submission.

17. **How would you implement a multi-step form with Server Actions?**
    Use URL state for step tracking, Server Actions for data persistence between steps, and progressive enhancement for each step.

18. **Explain the Server Actions execution model.**
    Client sends POST request with action ID, server routes to the action, executes with provided data, and returns result. Automatic revalidation follows.

19. **How do you handle complex mutations with Server Actions?**
    Use transactions, implement retry logic, handle partial failures, and provide rollback mechanisms.

20. **Design a file upload system with Server Actions.**
    Implement chunked uploads for large files, validate file types/sizes, process on server, and upload to storage services.

21. **How would you implement rate limiting for Server Actions?**
    Use middleware or action-level checks, implement IP-based tracking, and return appropriate error responses.

22. **Explain the relationship between Server Actions and React Suspense.**
    Server Actions can trigger Suspense boundaries, showing loading states while the action executes. Use `useTransition` for non-blocking updates.

23. **How do you implement real-time updates after Server Actions?**
    Combine Server Actions with WebSocket/SSE, use revalidation for polling, or implement optimistic updates with rollback.

24. **Design an error recovery system for Server Actions.**
    Implement retry logic, provide user-friendly error messages, log errors for debugging, and offer fallback options.

25. **How would you implement a workflow system with Server Actions?**
    Use a state machine approach, track workflow progress in database, implement step-by-step execution, and handle failures gracefully.

### FAANG-style (5-10)

26. **Design a distributed transaction system using Server Actions.**
    Implement saga pattern, handle compensation logic, track transaction state, and ensure data consistency across services.

27. **How would you implement a command pattern with Server Actions?**
    Define command types, serialize commands, execute on server, and handle undo/redo operations.

28. **Design a batch processing system with Server Actions.**
    Implement job queues, handle progress tracking, provide rollback capabilities, and manage resource limits.

29. **How would you implement a workflow engine using Server Actions?**
    Define workflow steps, track execution state, handle parallel branches, and implement compensation logic.

30. **Design a distributed system with Server Actions for coordination.**
    Use Server Actions for orchestration, implement circuit breakers, handle service failures, and ensure idempotency.

### Follow-ups (5-10)

31. **What are the limitations of Server Actions?**
    Server-side execution only, no streaming, limited error handling, and require form data or serializable arguments.

32. **How do Server Actions affect testing?**
    Test action logic separately, mock database calls, test error scenarios, and verify revalidation behavior.

33. **What is the future of Server Actions?**
    Better streaming support, improved error handling, more React integration, and enhanced DevTools.

34. **How do you migrate from API Routes to Server Actions?**
    Identify mutation endpoints, convert to Server Actions, update client code, and verify caching behavior.

35. **What security best practices apply to Server Actions?**
    Validate all inputs, implement CSRF protection, use authentication/authorization, and rate limit requests.

36. **How do Server Actions interact with middleware?**
    Server Actions execute after middleware, so middleware can't intercept them directly. Use middleware for request-level logic.

37. **What are alternatives to Server Actions?**
    API Routes, GraphQL mutations, tRPC, and direct database calls from Client Components.

38. **How do you monitor Server Actions in production?**
    Log action execution, track performance metrics, monitor error rates, and implement alerting.

## Summary

| Feature | Server Actions |
|---------|---------------|
| Directive | `'use server'` |
| Runs on | Server |
| Input | FormData or serializable args |
| Output | Serializable data |
| Revalidation | `revalidatePath`/`revalidateTag` |
| Forms | Progressive enhancement |
| Type safety | End-to-end TypeScript |
| Use case | Data mutations |

## Cheat Sheet

```text
'use server' directive:
- At top of file or function
- Marks as Server Action
- Enables server-side execution

Form handling:
<form action={serverAction}>
  <input name="field" />
  <button type="submit">Submit</button>
</form>

Hooks:
useFormState   → [state, action] for form state
useFormStatus  → { pending } for loading states
useTransition  → Non-blocking updates
useOptimistic  → Optimistic UI updates

Revalidation:
revalidatePath('/path')  → Invalidate specific path
revalidateTag('tag')     → Invalidate by tag

Validation:
- Use Zod for schema validation
- Validate on server
- Return errors to client
```

## References & Learn More

- [Next.js Docs: Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Server Actions Guide](https://nextjs.org/blog/next-14#server-actions)
- [Progressive Enhancement with Server Actions](https://react.dev/reference/rsc/use-server)
