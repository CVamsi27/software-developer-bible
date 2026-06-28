# State Management

## Definition

State management in React refers to how application state (data that changes over time) is stored, updated, and shared across components. It ranges from local component state (`useState`) to global state management solutions (Redux, Zustand, Jotai) and server state management (React Query/TanStack Query).

## Why Do We Need It?

### The Problem

As applications grow, state becomes complex:

1. **Shared state**: Multiple components need the same data

2. **Derived state**: Data computed from other state

3. **Async state**: Data from APIs with loading/error states

4. **Persistent state**: Data that persists across page reloads

5. **Server state**: Data synchronized with a backend

### State Categories

```text
State Categories:
═══════════════════════════════════════════════════════════════

1. Local State (useState)
   ├── Component-specific data
   ├── Form inputs
   ├── UI state (open/closed, active tab)
   └── Temporary data

2. Lifted State (useState + props)
   ├── Shared between siblings
   ├── Parent-child communication
   └── Common ancestors

3. Global State (Context, Redux, Zustand)
   ├── App-wide data (theme, auth, language)
   ├── Deeply nested components
   └── Cross-cutting concerns

4. Server State (React Query, SWR)
   ├── API data
   ├── Caching
   ├── Background refetching
   └── Optimistic updates

5. URL State
   ├── Current route
   ├── Query parameters
   └── Filters, pagination

```

## How It Works

### Local State vs Global State

```text
Local State vs Global State:
═══════════════════════════════════════════════════════════════

Local State (useState):
┌─────────────────────────────────────────────────────────────┐
│ Component A                                                 │
│ ├── [count, setCount] = useState(0)                        │
│ └── count is ONLY available in Component A                  │
│                                                             │
│ Component B                                                 │
│ └── Cannot access count!                                    │
└─────────────────────────────────────────────────────────────┘

Global State (Context/Redux):
┌─────────────────────────────────────────────────────────────┐
│ Store/Context                                                │
│ └── [user, setUser] = { user: {...}, setUser: ... }       │
│                                                             │
│ Component A                                                 │
│ └── const user = useContext(AuthContext) // Can access!     │
│                                                             │
│ Component B                                                 │
│ └── const user = useContext(AuthContext) // Can access!     │
└─────────────────────────────────────────────────────────────┘

```

### Context vs Redux vs Zustand

```text
Comparison:
═══════════════════════════════════════════════════════════════

Context API:
├── Built into React
├── Simple to use
├── Good for: themes, auth, language
├── Limitations: performance, devtools
└── No middleware, no time-travel

Redux:
├── Third-party library
├── Complex but powerful
├── Good for: complex state logic
├── Features: middleware, devtools, time-travel
└── Steep learning curve

Zustand:
├── Third-party library (lightweight)
├── Simple API
├── Good for: medium complexity
├── Features: middleware, devtools
└── Minimal boilerplate

Jotai:
├── Third-party library (atomic)
├── Bottom-up approach
├── Good for: granular state
├── Features: async, devtools
└── Minimal boilerplate

```

### Server State vs Client State

```text
Server State vs Client State:
═══════════════════════════════════════════════════════════════

Client State (useState, Redux):
┌─────────────────────────────────────────────────────────────┐
│ Data owned by the client                                    │
│ ├── Form inputs                                            │
│ ├── UI state (modals, tabs)                                │
│ ├── User preferences                                        │
│ └── Shopping cart                                           │
│                                                             │
│ Updates: Direct, synchronous                                │
│ Persistence: localStorage, sessionStorage                  │
└─────────────────────────────────────────────────────────────┘

Server State (React Query):
┌─────────────────────────────────────────────────────────────┐
│ Data owned by the server                                    │
│ ├── User data from API                                     │
│ ├── Products from database                                 │
│ ├── Orders from backend                                     │
│ └── Any API response                                       │
│                                                             │
│ Updates: Async, with loading/error states                   │
│ Persistence: Server database                               │
│ Features: Caching, background refetching, retry            │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Local State with useState

```typescript
const Counter = () => {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
    </div>
  );
};

```

### Lifted State

```typescript
const Parent = () => {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <Child count={count} onIncrement={() => setCount(c => c + 1)} />
    </div>
  );
};

const Child = ({ count, onIncrement }: { count: number; onIncrement: () => void }) => (
  <button onClick={onIncrement}>Count: {count}</button>
);

```

### Context API

```typescript
const ThemeContext = createContext<'light' | 'dark'>('light');

const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const value = useMemo(() => ({ theme, setTheme }), [theme]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

const useTheme = () => useContext(ThemeContext);

```

### Zustand

```typescript
import { create } from 'zustand';

interface TodoStore {
  todos: Todo[];
  addTodo: (text: string) => void;
  toggleTodo: (id: string) => void;
  deleteTodo: (id: string) => void;
}

const useTodoStore = create<TodoStore>((set) => ({
  todos: [],
  addTodo: (text) => set((state) => ({
    todos: [...state.todos, { id: crypto.randomUUID(), text, completed: false }],
  })),
  toggleTodo: (id) => set((state) => ({
    todos: state.todos.map((t) => t.id === id ? { ...t, completed: !t.completed } : t),
  })),
  deleteTodo: (id) => set((state) => ({
    todos: state.todos.filter((t) => t.id !== id),
  })),
}));

// Usage
const TodoList = () => {
  const todos = useTodoStore((state) => state.todos);
  const addTodo = useTodoStore((state) => state.addTodo);
  return <div>{/* ... */}</div>;
};

```

### Redux Toolkit

```typescript
import { createSlice, configureStore } from '@reduxjs/toolkit';

const todosSlice = createSlice({
  name: 'todos',
  initialState: [] as Todo[],
  reducers: {
    addTodo: (state, action) => {
      state.push({ id: crypto.randomUUID(), text: action.payload, completed: false });
    },
    toggleTodo: (state, action) => {
      const todo = state.find((t) => t.id === action.payload);
      if (todo) todo.completed = !todo.completed;
    },
  },
});

const store = configureStore({ reducer: { todos: todosSlice.reducer } });

```

### React Query (TanStack Query)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const useUsers = () => useQuery({
  queryKey: ['users'],
  queryFn: () => fetch('/api/users').then((res) => res.json()),
});

const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (newUser: CreateUserDTO) =>
      fetch('/api/users', { method: 'POST', body: JSON.stringify(newUser) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
};

```

### Optimistic Updates

```typescript
const useToggleTodo = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => fetch(`/api/todos/${id}/toggle`, { method: 'PATCH' }),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previous = queryClient.getQueryData(['todos']);
      queryClient.setQueryData(['todos'], (old: Todo[]) =>
        old.map((t) => t.id === id ? { ...t, completed: !t.completed } : t)
      );
      return { previous };
    },
    onError: (err, id, context) => {
      queryClient.setQueryData(['todos'], context.previous);
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  });
};

```

## Common Mistakes

1. **Putting everything in global state**: Use local state when possible

2. **Not normalizing state**: Keep state flat for efficient updates

3. **Using Context for complex state**: Use Redux/Zustand for complex logic

4. **Not handling loading/error states**: Always handle async states

5. **Over-fetching**: Use caching with React Query

## Best Practices

1. **Start with local state**: Use useState for component-specific data

2. **Lift state when needed**: Move state to common ancestor for siblings

3. **Use Context for global data**: Theme, auth, language

4. **Use Redux/Zustand for complex state**: Multiple updates, middleware

5. **Use React Query for server state**: Caching, background refetching

6. **Normalize state**: Flat structures for efficient updates

7. **Colocate state**: Keep state near where it's used

## Interview Questions

### Beginner (5-10)

**Q1: What are the different types of state in React?**
A: Local state (useState), lifted state (props), global state (Context/Redux), server state (React Query).

**Q2: When should you use useState vs useReducer?**
A: useState for simple state; useReducer for complex state with multiple sub-values.

**Q3: What is prop drilling?**
A: Passing props through intermediate components that don't use them. Solved by Context.

**Q4: What is Context API?**
A: React's built-in solution for sharing data across the component tree without prop drilling.

**Q5: What is Redux?**
A: A third-party state management library with a single store, actions, and reducers.

**Q6: What is Zustand?**
A: A lightweight state management library with a simple API and minimal boilerplate.

**Q7: What is server state?**
A: Data fetched from an API/server that needs caching, refetching, and error handling.

**Q8: What is React Query?**
A: A library for managing server state with caching, background refetching, and optimistic updates.

**Q9: When should you use global state?**
A: When data is needed by many components at different nesting levels.

**Q10: What is state normalization?**
A: Flattening nested state into a flat structure with IDs for efficient updates.

### Intermediate (5-10)

**Q11: Compare Context vs Redux.**
A: Context is simple, built-in, good for themes/auth. Redux is complex, has devtools/middleware, good for complex state logic.

**Q12: What is the difference between client state and server state?**
A: Client state is owned by the client (form inputs, UI). Server state is owned by the server (API data).

**Q13: How do you handle async state?**
A: Use React Query for server state; useState + useEffect for client async state.

**Q14: What is optimistic update?**
A: Updating UI immediately before server confirmation, then rolling back on error.

**Q15: How do you share state between siblings?**
A: Lift state to common parent, or use Context/Redux.

**Q16: What is the difference between Redux and Zustand?**
A: Redux is complex with boilerplate. Zustand is simple with minimal API.

**Q17: How do you handle forms in React?**
A: Controlled components with useState, or form libraries like React Hook Form.

**Q18: What is derived state?**
A: Data computed from other state during render, not stored separately.

**Q19: How do you persist state?**
A: localStorage, sessionStorage, or server-side persistence.

**Q20: What is the difference between useReducer and Redux?**
A: useReducer is for local state; Redux is for global state with devtools/middleware.

### Senior (10-15)

**Q21: Design a state management strategy for a large app.**
A: Local state for components, Context for global data, Redux/Zustand for complex state, React Query for server state.

**Q22: How do you optimize context performance?**
A: Memoize value, split contexts by concern, use useTransition for non-urgent updates.

**Q23: What is the relationship between state management and architecture?**
A: State management affects component structure, data flow, and testability.

**Q24: How do you test state management?**
A: Unit tests for reducers, integration tests for components, E2E tests for user flows.

**Q25: What are the trade-offs between state management solutions?**
A: Complexity vs simplicity, performance vs features, boilerplate vs flexibility.

**Q26: How do you handle state in micro-frontends?**
A: Independent state per micro-frontend, shared state via events or context.

**Q27: What is the impact of state management on performance?**
A: Unnecessary re-renders, memory usage, update frequency.

**Q28: How do you debug state issues?**
A: React DevTools, Redux DevTools, console logging, profiling.

**Q29: What is the relationship between state and React DevTools?**
A: React DevTools shows component state and allows editing for debugging.

**Q30: How do you handle state migration?**
A: Incremental migration, adapter pattern, feature flags.

### FAANG-style (5-10)

**Q31: Design a state management system for a real-time app.**
A: WebSockets for real-time data, Zustand for local state, optimistic updates.

**Q32: How would you implement state synchronization across tabs?**
A: localStorage events, BroadcastChannel, or WebSocket.

**Q33: Analyze the performance implications of different state solutions.**
A: Context causes all consumers to re-render; Redux has selector optimization; Zustand has selective subscriptions.

**Q34: How would you design a state management system for offline-first apps?**
A: Local storage, sync queue, conflict resolution, background sync.

**Q35: Design a state management testing strategy.**
A: Unit tests for reducers, integration tests for hooks, E2E tests for flows.

**Q36: How do you handle state in server-rendered apps?**
A: Hydration, server state, client state separation.

**Q37: What is the relationship between state management and security?**
A: Sensitive data should not be stored in client state; use server-side sessions.

**Q38: How do you handle state in concurrent rendering?**
A: Transitions, deferred values, selective subscriptions.

**Q39: What is the impact of React Compiler on state management?**
A: Automatic memoization reduces need for manual optimization.

**Q40: Design a state management system for a collaborative app.**
A: CRDT, operational transformation, conflict resolution, real-time sync.

### Follow-ups (5-10)

**Q41: How would you explain state management to a junior developer?**
A: State is data that changes over time. Local state is for one component; global state is for many components.

**Q42: What are the edge cases in state management?**
A: Race conditions, stale closures, memory leaks, serialization.

**Q43: How does state management interact with testing?**
A: Isolated state is easier to test; global state needs mocking.

**Q44: What is the relationship between state and performance?**
A: Unnecessary state updates cause re-renders; memoization prevents them.

**Q45: How do you handle state in legacy apps?**
A: Incremental migration, wrapper components, adapter pattern.

## Summary

State management ranges from local useState to global Redux/Zustand and server state React Query. Choose based on complexity: local state for component data, Context for global data, Redux/Zustand for complex logic, React Query for server data.

## Cheat Sheet

```text
State Management Options:
├── useState: Simple local state
├── useReducer: Complex local state
├── Context: Global simple state (theme, auth)
├── Redux: Complex global state (middleware, devtools)
├── Zustand: Simple global state (minimal API)
├── Jotai: Atomic state (granular updates)
├── React Query: Server state (caching, refetching)
└── URL state: Query params, route

When to Use:
├── useState: Component-specific data
├── Context: Shared global data
├── Redux/Zustand: Complex state logic
├── React Query: API data
└── URL: Filters, pagination, navigation

Best Practices:
├── Start with local state
├── Lift state when needed
├── Use Context for global data
├── Use Redux for complex logic
├── Use React Query for server state
├── Normalize state
└── Colocate state

```

## References & Learn More

- [React Docs: Managing State](https://react.dev/learn/managing-state)
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Redux Toolkit Docs](https://redux-toolkit.js.org/)
- [Jotai GitHub](https://github.com/pmndrs/jotai)
