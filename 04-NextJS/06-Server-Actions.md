# Server Actions in Next.js

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

er and can be called from Client Components or Server Components. They use the `'use server'` directive and enable form handling, data mutations, and progressive enhancement without creating API routes.

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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

```typescript
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

---

## See Also
- [Authentication](13-Authentication.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [Serverless & Edge](../27-Serverless-Edge/)

## References & Learn More

- [Next.js Docs: Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Server Actions Guide](https://nextjs.org/blog/next-14#server-actions)
- [Progressive Enhancement with Server Actions](https://react.dev/reference/rsc/use-server)
