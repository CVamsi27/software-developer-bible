# Client Components in Next.js

## Definition

**Client Components** are React components that render on the client side with full interactivity. They use the `'use client'` directive at the top of the file and can access React hooks, browser APIs, and event handlers. They are hydrated after the server-rendered HTML is sent to the browser.

## Why Do We Need It?

1. **Interactivity** — useState, useEffect, event handlers require client-side execution
2. **Browser APIs** — window, document, localStorage need the browser environment
3. **Third-party libraries** — Many React libraries require client-side rendering
4. **Rich UI** — Animations, drag-and-drop, real-time updates need client JS
5. **Form handling** — Complex form state management requires client-side logic

## How It Works

### Client Component Lifecycle

```text
┌─────────────────────────────────────────────────────────────────┐
│                  CLIENT COMPONENT LIFECYCLE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SERVER RENDERING                                            │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  Component executes with initial props              │    │
│     │  Renders HTML (or placeholder)                      │    │
│     │  Sends HTML + JavaScript bundle to client           │    │
│     └─────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  2. CLIENT HYDRATION                                            │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  Browser receives HTML                               │    │
│     │  Downloads JavaScript bundle                         │    │
│     │  React attaches event listeners (hydration)         │    │
│     │  Component becomes interactive                       │    │
│     └─────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  3. CLIENT INTERACTION                                          │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  User interacts with component                      │    │
│     │  State updates trigger re-renders                   │    │
│     │  Effects run (useEffect)                            │    │
│     │  UI updates in response to events                   │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Bundle Impact Comparison

```text
┌─────────────────────────────────────────────────────────────────┐
│               BUNDLE SIZE COMPARISON                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Server Component (page.tsx):                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  HTML: 2KB                                               │    │
│  │  JavaScript: 0KB                                         │    │
│  │  Total to client: 2KB                                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Client Component ('use client'):                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  HTML: 2KB                                               │    │
│  │  React runtime: 40KB gzipped                             │    │
│  │  Component code: 5KB                                     │    │
│  │  Dependencies: 20KB                                      │    │
│  │  Total to client: 67KB                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Impact: 33x larger bundle for Client Component                 │
└─────────────────────────────────────────────────────────────────┘
```

### Hydration Process

```text
Server Output:                    Client After Hydration:
┌──────────────────────┐         ┌──────────────────────┐
│ <div>                 │         │ <div>                 │
│   <h1>Count: 0</h1>   │   →     │   <h1>Count: 0</h1>   │
│   <button>Click</button>│       │   <button onClick=...>│
│ </div>                │         │ </div>                │
└──────────────────────┘         └──────────────────────┘
  Static HTML                      Interactive Component
  No event listeners               Event listeners attached
  No state                         State managed by React
```

## Code Examples

### Basic Client Component

```tsx
// components/counter.tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
      <button onClick={() => setCount(c => c - 1)}>
        Decrement
      </button>
    </div>
  )
}
```

### Client Component with Effects

```tsx
// components/clock.tsx
'use client'

import { useState, useEffect } from 'react'

export function Clock() {
  const [time, setTime] = useState<Date | null>(null)

  useEffect(() => {
    setTime(new Date())
    const interval = setInterval(() => {
      setTime(new Date())
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  if (!time) return <div>Loading clock...</div>

  return (
    <div>
      <p>Current time: {time.toLocaleTimeString()}</p>
    </div>
  )
}
```

### Client Component with localStorage

```tsx
// components/theme-toggle.tsx
'use client'

import { useState, useEffect } from 'react'

export function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const saved = localStorage.getItem('theme') as 'light' | 'dark'
    if (saved) {
      setTheme(saved)
      document.documentElement.classList.toggle('dark', saved === 'dark')
    }
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
    localStorage.setItem('theme', newTheme)
    document.documentElement.classList.toggle('dark', newTheme === 'dark')
  }

  return (
    <button onClick={toggleTheme}>
      {theme === 'light' ? '🌙 Dark' : '☀️ Light'}
    </button>
  )
}
```

### Client Component with Form Handling

```tsx
// components/contact-form.tsx
'use client'

import { useState, FormEvent } from 'react'

interface FormData {
  name: string
  email: string
  message: string
}

export function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    message: '',
  })
  const [status, setStatus] = useState<'idle' | 'submitting' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setStatus('submitting')

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!res.ok) throw new Error('Failed to send')

      setStatus('success')
      setFormData({ name: '', email: '', message: '' })
    } catch (error) {
      setStatus('error')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={formData.name}
        onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={e => setFormData(prev => ({ ...prev, email: e.target.value }))}
        required
      />
      <textarea
        placeholder="Message"
        value={formData.message}
        onChange={e => setFormData(prev => ({ ...prev, message: e.target.value }))}
        required
      />
      <button type="submit" disabled={status === 'submitting'}>
        {status === 'submitting' ? 'Sending...' : 'Send'}
      </button>
      {status === 'success' && <p>Message sent!</p>}
      {status === 'error' && <p>Failed to send. Try again.</p>}
    </form>
  )
}
```

### Client Component with Context

```tsx
// contexts/cart-context.tsx
'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

interface CartContextType {
  items: CartItem[]
  addItem: (item: Omit<CartItem, 'quantity'>) => void
  removeItem: (id: string) => void
  total: number
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([])

  const addItem = (item: Omit<CartItem, 'quantity'>) => {
    setItems(prev => {
      const existing = prev.find(i => i.id === item.id)
      if (existing) {
        return prev.map(i =>
          i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
        )
      }
      return [...prev, { ...item, quantity: 1 }]
    })
  }

  const removeItem = (id: string) => {
    setItems(prev => prev.filter(i => i.id !== id))
  }

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0)

  return (
    <CartContext.Provider value={{ items, addItem, removeItem, total }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (!context) throw new Error('useCart must be used within CartProvider')
  return context
}
```

### Client Component with Third-Party Libraries

```tsx
// components/date-picker.tsx
'use client'

import { useState } from 'react'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'

export function EventDatePicker() {
  const [startDate, setStartDate] = useState<Date | null>(null)

  return (
    <div>
      <label>Select Event Date</label>
      <DatePicker
        selected={startDate}
        onChange={(date) => setStartDate(date)}
        minDate={new Date()}
        placeholderText="Select a date"
      />
      {startDate && (
        <p>Selected: {startDate.toLocaleDateString()}</p>
      )}
    </div>
  )
}
```

### Client Component with Animations

```tsx
// components/animated-card.tsx
'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export function AnimatedCard() {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <motion.div
      layout
      className="card"
      onClick={() => setIsExpanded(!isExpanded)}
    >
      <AnimatePresence mode="wait">
        {isExpanded ? (
          <motion.div
            key="expanded"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <h3>Expanded Content</h3>
            <p>Detailed information here...</p>
          </motion.div>
        ) : (
          <motion.div
            key="collapsed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <h3>Click to expand</h3>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
```

### Client Component with WebSocket

```tsx
// components/live-chat.tsx
'use client'

import { useState, useEffect, useRef } from 'react'

interface Message {
  id: string
  text: string
  sender: string
  timestamp: Date
}

export function LiveChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    wsRef.current = new WebSocket('wss://chat.example.com')

    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data)
      setMessages(prev => [...prev, message])
    }

    return () => {
      wsRef.current?.close()
    }
  }, [])

  const sendMessage = () => {
    if (!input.trim() || !wsRef.current) return

    wsRef.current.send(JSON.stringify({
      text: input,
      sender: 'User',
      timestamp: new Date(),
    }))

    setInput('')
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className="message">
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <div className="input">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
}
```

### Composing Server and Client Components

```tsx
// app/products/page.tsx — Server Component
import { ProductFilters } from './product-filters' // Client
import { ProductGrid } from './product-grid' // Server
import { db } from '@/lib/database'

export default async function ProductsPage() {
  const products = await db.product.findMany()
  const categories = await db.category.findMany()

  return (
    <div>
      <h1>Products</h1>
      {/* Client Component for filters */}
      <ProductFilters categories={categories} />
      {/* Server Component for product list */}
      <ProductGrid products={products} />
    </div>
  )
}
```

```tsx
// app/products/product-filters.tsx — Client Component
'use client'

import { useState } from 'react'

interface Category {
  id: string
  name: string
}

export function ProductFilters({ categories }: { categories: Category[] }) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 1000])

  return (
    <div className="filters">
      <select
        value={selectedCategory || ''}
        onChange={e => setSelectedCategory(e.target.value || null)}
      >
        <option value="">All Categories</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.id}>{cat.name}</option>
        ))}
      </select>

      <input
        type="range"
        min={0}
        max={1000}
        value={priceRange[1]}
        onChange={e => setPriceRange([priceRange[0], Number(e.target.value)])}
      />
      <span>${priceRange[1]}</span>
    </div>
  )
}
```

```tsx
// app/products/product-grid.tsx — Server Component
import { AddToCartButton } from './add-to-cart-button' // Client

interface Product {
  id: string
  name: string
  price: number
  image: string
}

export function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map(product => (
        <div key={product.id} className="border rounded-lg overflow-hidden">
          <img src={product.image} alt={product.name} />
          <div className="p-4">
            <h3>{product.name}</h3>
            <p>${product.price}</p>
            <AddToCartButton productId={product.id} />
          </div>
        </div>
      ))}
    </div>
  )
}
```

### Dynamic Client Component Loading

```tsx
// app/page.tsx
import dynamic from 'next/dynamic'

// Dynamically import heavy Client Component
const HeavyEditor = dynamic(() => import('./heavy-editor'), {
  loading: () => <div>Loading editor...</div>,
  ssr: false, // Disable SSR for purely client-side component
})

export default function Page() {
  return (
    <div>
      <h1>Document Editor</h1>
      <HeavyEditor />
    </div>
  )
}
```

## Real-World Use Cases

| Use Case | Why Client Component |
|----------|---------------------|
| Form handling | useState for form state, event handlers |
| Modals/Dialogs | useState for open/close, animations |
| Carousels | Swipe detection, animations |
| Search with autocomplete | Real-time filtering, keyboard navigation |
| Maps | Google Maps/Mapbox requires browser APIs |
| Rich text editors | Quill/TipTap need DOM manipulation |
| Real-time notifications | WebSocket/SSE connections |
| Dark mode toggle | localStorage, DOM manipulation |
| Drag and drop | Mouse/touch event handling |
| Video players | HTML5 video API |

## Common Mistakes

### 1. Overusing Client Components

```tsx
// ❌ BAD: Entire page is client component
'use client'
export default function ProductPage({ product }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton id={product.id} />
    </div>
  )
}

// ✅ GOOD: Keep page as server, isolate interactive parts
export default async function ProductPage({ params }) {
  const { id } = await params
  const product = await getProduct(id)

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton id={product.id} />
    </div>
  )
}

// Only the button needs 'use client'
'use client'
export function AddToCartButton({ id }: { id: string }) {
  const [loading, setLoading] = useState(false)

  const handleClick = async () => {
    setLoading(true)
    await addToCart(id)
    setLoading(false)
  }

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? 'Adding...' : 'Add to Cart'}
    </button>
  )
}
```

### 2. Passing Complex Objects to Client Components

```tsx
// ❌ BAD: Passing non-serializable props
'use client'
import { Date } from 'moment'

export function EventCard({ event }: { event: { date: Date } }) {
  // moment Date objects can't be serialized!
  return <div>{event.date.format('YYYY-MM-DD')}</div>
}

// ✅ GOOD: Pass serialized data
export default async function EventPage() {
  const event = await getEvent()
  return (
    <EventCard
      eventName={event.name}
      eventDate={event.date.toISOString()} // Serialize!
    />
  )
}

'use client'
export function EventCard({ eventName, eventDate }: {
  eventName: string
  eventDate: string
}) {
  return <div>{eventName} - {new Date(eventDate).toLocaleDateString()}</div>
}
```

### 3. Not Handling Hydration Mismatches

```tsx
// ❌ BAD: Server and client render different content
'use client'
export function Greeting() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // Server renders "Loading...", client renders name
  // This causes hydration mismatch!
  return <div>{mounted ? 'Hello, User!' : 'Loading...'}</div>
}

// ✅ GOOD: Use useEffect for client-only content
'use client'
import { useState, useEffect } from 'react'

export function Greeting() {
  const [greeting, setGreeting] = useState('')

  useEffect(() => {
    setGreeting('Hello, User!')
  }, [])

  return <div>{greeting || <div aria-busy="true">Loading...</div>}</div>
}
```

### 4. Fetching Data in Client Components

```tsx
// ❌ BAD: Client-side data fetching
'use client'
import { useEffect, useState } from 'react'

export function ProductList() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(data => {
        setProducts(data)
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Loading...</div>

  return products.map(p => <div key={p.id}>{p.name}</div>)
}

// ✅ GOOD: Use Server Component for data fetching
export default async function ProductList() {
  const products = await db.product.findMany()
  return products.map(p => <div key={p.id}>{p.name}</div>)
}
```

### 5. Not Using Proper Error Handling

```tsx
// ❌ BAD: No error handling
'use client'
export function DataFetcher() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData) // No error handling!
  }, [])

  return <div>{data?.value}</div>
}

// ✅ GOOD: Proper error handling
'use client'
import { useState, useEffect } from 'react'

export function DataFetcher() {
  const [data, setData] = useState(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/data')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch')
        return res.json()
      })
      .then(setData)
      .catch(err => setError(err.message))
  }, [])

  if (error) return <div>Error: {error}</div>
  if (!data) return <div>Loading...</div>

  return <div>{data.value}</div>
}
```

## Best Practices

1. **Minimize Client Components** — Keep them small and focused
2. **Isolate interactivity** — Extract interactive parts into separate Client Components
3. **Use dynamic imports** — Lazy load heavy Client Components with `next/dynamic`
4. **Handle hydration** — Ensure server and client render the same initial content
5. **Serialize props** — Only pass serializable data from Server to Client Components
6. **Use proper error boundaries** — Wrap Client Components in error boundaries
7. **Optimize re-renders** — Use memo, useMemo, useCallback when needed
8. **Avoid unnecessary effects** — Don't fetch data in useEffect if Server Component can
9. **Test both environments** — Client Components behave differently in dev/prod
10. **Monitor bundle size** — Track Client Component impact on bundle

## Performance Considerations

### Hydration Cost

```text
Hydration time = Component tree size × Complexity

Fast hydration:
- Small component trees
- Minimal state initialization
- Few effects

Slow hydration:
- Large component trees
- Complex state initialization
- Many effects
- Third-party libraries
```

### Optimization Strategies

```text
1. Code splitting:
   dynamic(() => import('./heavy-component'))

2. Memoization:
   const MemoizedComponent = React.memo(ExpensiveComponent)

3. State colocation:
   Move state to the lowest common ancestor

4. Lazy initialization:
   useState(() => computeExpensiveValue())

5. Virtualization:
   Use react-window for long lists
```

## Interview Questions

### Beginner (5-10)

1. **What is a Client Component?**
   A Client Component renders on the client with full interactivity. It uses `'use client'` directive and can access React hooks and browser APIs.

2. **How do you create a Client Component?**
   Add `'use client'` at the top of the file. This tells Next.js to render it on the client.

3. **Why can't all components be Client Components?**
   Client Components send JavaScript to the browser. Too many increase bundle size and slow down initial load. Server Components reduce client JS.

4. **What is hydration?**
   Hydration is when React attaches event listeners to server-rendered HTML, making it interactive. The HTML is displayed first, then JavaScript makes it work.

5. **Can Server Components import Client Components?**
   Yes! Server Components can import and render Client Components. But Client Components can't import Server Components.

6. **What happens if you forget `'use client'`?**
   You'll get an error when using hooks or event handlers. Next.js will tell you to add the directive.

7. **How do Client Components affect performance?**
   They increase bundle size, require hydration, and add to JavaScript execution time. Keep them minimal.

8. **What is the `'use client'` directive?**
   A directive at the top of a file that marks it as a Client Component. It's a boundary between server and client rendering.

### Intermediate (5-10)

9. **How do you optimize Client Component performance?**
   Use `next/dynamic` for lazy loading, `React.memo` for preventing unnecessary re-renders, and state colocation to minimize re-renders.

10. **How do you handle hydration mismatches?**
    Ensure server and client render the same initial content. Use `useEffect` for client-only content. Avoid `Math.random()` or `Date.now()` in render.

11. **What is the relationship between Client Components and Suspense?**
    Client Components can be wrapped in Suspense boundaries. The server renders the fallback, then streams the Client Component when ready.

12. **How do you pass Server Component data to Client Components?**
    Pass serializable props from Server to Client Components. Never pass functions, Date objects, or Maps.

13. **When should you use `next/dynamic` with `ssr: false`?**
    For purely client-side components that don't need server rendering (e.g., charts, maps, editors).

14. **How do Client Components interact with the App Router?**
    They can use `useRouter()`, `usePathname()`, `useSearchParams()` for navigation and URL access.

15. **What is the impact of Client Components on Core Web Vitals?**
    They increase FCP/LCP due to hydration, can cause CLS during hydration, and affect TTI. Server Components improve all metrics.

### Senior (10-15)

16. **Design a component architecture that minimizes Client Component usage.**
    Use Server Components for data fetching and static content, isolate interactive elements as Client Components, and use composition patterns to minimize client JS.

17. **How would you implement optimistic updates with Client Components?**
    Use local state for immediate UI updates, Server Actions for mutations, and revalidation to sync with Server Components.

18. **Explain the hydration process in detail.**
    1. Server renders HTML
    2. Client downloads JS bundle
    3. React creates virtual DOM from HTML
    4. React compares with server HTML
    5. React attaches event listeners
    6. Component becomes interactive

19. **How do you debug hydration mismatches?**
    Use React DevTools, enable strict mode, check for `useEffect` timing, and avoid client-only values in initial render.

20. **Design a state management architecture for a large app with many Client Components.**
    Use React Context for shared state, URL state for navigation state, Server Components for data fetching, and Client Components for UI state.

21. **How would you implement a virtualized list with Client Components?**
    Use react-window or react-virtualized, implement infinite scrolling with IntersectionObserver, and lazy load items as needed.

22. **Explain the relationship between Client Components and React Server Actions.**
    Client Components can call Server Actions, which are async functions that run on the server. This enables mutations without API routes.

23. **How do you handle form validation with Client Components?**
    Use controlled forms with useState, implement client-side validation for UX, and server-side validation for security. Use libraries like Zod.

24. **Design a real-time notification system with Client Components.**
    Use WebSocket/SSE for real-time updates, React Context for notification state, and toast components for display. Handle reconnection logic.

25. **How would you optimize a page with 50+ Client Components?**
    Use React.memo aggressively, implement virtualization for lists, code-split heavy components, and use Web Workers for expensive computations.

### FAANG-style (5-10)

26. **Design a micro-frontend architecture with Client Components.**
    Use Module Federation, each micro-frontend as independent Client Components, shared React runtime, and composition in a shell application.

27. **How would you implement server-driven UI with Client Components?**
    Server sends component configuration, Client Components render based on config, and use JSON schema for component definitions.

28. **Design a system for tracking Client Component performance.**
    Implement performance marks, track hydration time, monitor re-render frequency, and use Real User Monitoring (RUM).

29. **How would you implement progressive enhancement with Client Components?**
    Server renders semantic HTML, Client Components enhance with interactivity, and use `useEffect` for progressive enhancement.

30. **Design a Client Component caching strategy.**
    Use React Query for server state, SWR for revalidation, local storage for persistence, and IndexedDB for offline support.

### Follow-ups (5-10)

31. **What are the alternatives to Client Components?**
    Server Components, Server Actions, Route Handlers, and edge functions. Each serves different purposes.

32. **How do Client Components affect SEO?**
    Client-rendered content is not indexed by all crawlers. Use Server Components for SEO-critical content.

33. **What is the future of Client Components?**
    Better hydration, smaller bundles, improved streaming, and deeper integration with React features.

34. **How do you test Client Components?**
    Use `@testing-library/react`, mock hooks, test user interactions, and use MSW for API mocking.

35. **What is the relationship between Client Components and Service Workers?**
    Service Workers can cache Client Component bundles, enable offline support, and pre-cache routes.

36. **How do you handle internationalization with Client Components?**
    Use React Context for locale, next-intl for translations, and Server Components for initial locale detection.

37. **What are the security implications of Client Components?**
    Client-side code is visible to users. Never expose secrets, implement CSRF protection, and validate all user input.

38. **How do you monitor Client Component errors?**
    Use Error Boundaries, Sentry for error tracking, and console.error for development debugging.

## Summary

| Aspect | Client Component |
|--------|-----------------|
| Directive | `'use client'` |
| Renders | Client (after hydration) |
| Hooks | Yes (useState, useEffect, etc.) |
| Browser APIs | Yes |
| Event handlers | Yes |
| Bundle impact | Full component JS |
| Use case | Interactivity |
| Default | No (opt-in) |

## Cheat Sheet

```text
'use client' directive:
- Marks component as Client Component
- Must be at top of file
- Required for hooks/event handlers

When to use:
- useState/useEffect
- Event handlers (onClick, onChange)
- Browser APIs (window, document)
- Third-party client libraries
- Form handling
- Animations

When NOT to use:
- Data fetching
- Static content
- Server-side logic
- Simple display components

Optimization:
- next/dynamic for lazy loading
- React.memo for re-render prevention
- State colocation
- Code splitting
```

## References & Learn More

- [Next.js: Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- [Next.js: Server and Client Components](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns)
- [use client Directive](https://react.dev/reference/react/use-client)
