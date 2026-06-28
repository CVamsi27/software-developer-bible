# useState

## Definition

`useState` is a React Hook that lets you add state to function components. It returns a stateful value and a function to update it. When the state updater is called, React re-renders the component with the new state value.

`useState` is the most fundamental hook in React — it's the building block for all state management in function components. It was introduced in React 16.8 to enable function components to have their own state.

## Why Do We Need It?

### The Problem

Before hooks, function components were stateless — they could only accept props and render JSX. To add state, you had to use class components:

```typescript
// Before hooks: class component for state
class Counter extends React.Component {
  state = { count: 0 };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          +1
        </button>
      </div>
    );
  }
}

```

### The Solution

`useState` brings state to function components:

```typescript
// After hooks: function component with state
const Counter = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
};

```

## How It Works

### useState Internals

```text
useState Internals:
═══════════════════════════════════════════════════════════════

When you call useState:
┌─────────────────────────────────────────────────────────────┐
│ 1. React looks up the hook's position in the fiber tree     │
│ 2. Returns the state value from the fiber's memoizedState   │
│ 3. Creates a dispatch function (setter)                     │
│ 4. Returns [state, dispatch] tuple                          │
└─────────────────────────────────────────────────────────────┘

When you call the setter:
┌─────────────────────────────────────────────────────────────┐
│ 1. React creates an Update object                           │
│ 2. Enqueues the update in the fiber's updateQueue           │
│ 3. Schedules a re-render                                    │
│ 4. During next render:                                      │
│    - React processes all queued updates                     │
│    - Computes new state                                     │
│    - Returns new state value                                │
└─────────────────────────────────────────────────────────────┘

Hook Call Order:
┌─────────────────────────────────────────────────────────────┐
│ Hooks are stored in a linked list on the fiber node         │
│ They MUST be called in the same order every render          │
│                                                             │
│ First render: useState(0) → useState('hello')               │
│              [count, setCount]  [name, setName]             │
│                                                             │
│ Second render: useState(0) → useState('hello')              │
│               [1, setCount]    ['world', setName]           │
│                                                             │
│ If you call hooks conditionally, the order breaks!          │
└─────────────────────────────────────────────────────────────┘

```

### State Batching

```text
State Batching:
═══════════════════════════════════════════════════════════════

React 18 Automatic Batching:
┌─────────────────────────────────────────────────────────────┐
│ const handleClick = () => {                                 │
│   setCount(c => c + 1);  // Update 1 (queued)              │
│   setName('John');       // Update 2 (queued)               │
│   setFlag(true);         // Update 3 (queued)               │
│ };                                                          │
│ // All three batched into ONE re-render                     │
│ // State after: { count: 1, name: 'John', flag: true }     │
└─────────────────────────────────────────────────────────────┘

Without Batching (React 17 and earlier):
┌─────────────────────────────────────────────────────────────┐
│ // In setTimeout (React 17):                                │
│ setTimeout(() => {                                          │
│   setCount(c => c + 1);  // Triggers re-render 1           │
│   setName('John');       // Triggers re-render 2           │
│   setFlag(true);         // Triggers re-render 3           │
│ }, 1000);                                                   │
│ // Three separate re-renders!                               │
└─────────────────────────────────────────────────────────────┘

flushSync: Escape Hatch
┌─────────────────────────────────────────────────────────────┐
│ import { flushSync } from 'react-dom';                      │
│                                                             │
│ const handleClick = () => {                                 │
│   flushSync(() => {                                         │
│     setCount(c => c + 1);  // Immediate re-render          │
│   });                                                       │
│   // DOM updated here                                       │
│   flushSync(() => {                                         │
│     setName('John');       // Another immediate re-render   │
│   });                                                       │
│   // DOM updated again                                      │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

```

### Functional Updates

```text
Functional Updates:
═══════════════════════════════════════════════════════════════

Problem with Direct State:
┌─────────────────────────────────────────────────────────────┐
│ const handleClick = () => {                                 │
│   setCount(count + 1);  // Uses stale `count`              │
│   setCount(count + 1);  // Still uses stale `count`        │
│   // Result: count incremented by 1, not 2!                 │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

Solution: Functional Update
┌─────────────────────────────────────────────────────────────┐
│ const handleClick = () => {                                 │
│   setCount(c => c + 1);  // Uses latest state              │
│   setCount(c => c + 1);  // Uses latest state              │
│   // Result: count incremented by 2!                        │
│ };                                                          │
└─────────────────────────────────────────────────────────────┘

When to Use Functional Updates:
├── Updating based on previous state
├── Multiple state updates in same handler
├── State updates in async callbacks
└── State updates that depend on current state

```

### Lazy Initialization

```text
Lazy Initialization:
═══════════════════════════════════════════════════════════════

Problem: Expensive Initial State
┌─────────────────────────────────────────────────────────────┐
│ const [state, setState] = useState(expensiveComputation()); │
│ // expensiveComputation() runs on EVERY render!             │
│ // Even though initial state is only used on first render   │
└─────────────────────────────────────────────────────────────┘

Solution: Lazy Initialization
┌─────────────────────────────────────────────────────────────┐
│ const [state, setState] = useState(() => {                  │
│   return expensiveComputation(); // Only runs once!         │
│ });                                                         │
│ // Function is only called on initial render                │
└─────────────────────────────────────────────────────────────┘

When to Use:
├── Expensive computations (parsing, parsing JSON)
├── Reading from localStorage
├── Complex initial state calculations
└── Any operation that should only run once

```

## Code Examples

### Basic useState

```typescript
import React, { useState } from 'react';

const Counter = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(count - 1)}>-1</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
};

```

### Multiple State Variables

```typescript
const UserForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState(0);

  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <input
        type="number"
        value={age}
        onChange={e => setAge(Number(e.target.value))}
      />
    </form>
  );
};

// Alternative: Single state object
const UserFormObject = () => {
  const [user, setUser] = useState({
    name: '',
    email: '',
    age: 0,
  });

  const updateField = (field: string, value: any) => {
    setUser(prev => ({ ...prev, [field]: value }));
  };

  return (
    <form>
      <input value={user.name} onChange={e => updateField('name', e.target.value)} />
      <input value={user.email} onChange={e => updateField('email', e.target.value)} />
      <input
        type="number"
        value={user.age}
        onChange={e => updateField('age', Number(e.target.value))}
      />
    </form>
  );
};

```

### Functional Updates

```typescript
const Counter = () => {
  const [count, setCount] = useState(0);

  const incrementThree = () => {
    // ❌ BAD: All use stale count
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
    // Result: count = 1 (not 3!)

    // ✅ GOOD: Functional updates use latest state
    setCount(c => c + 1);
    setCount(c => c + 1);
    setCount(c => c + 1);
    // Result: count = 3
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={incrementThree}>+3</button>
    </div>
  );
};

```

### Lazy Initialization

```typescript
const ExpensiveComponent = () => {
  // ❌ BAD: Runs on every render
  const [state, setState] = useState(JSON.parse(largeJSON));

  // ✅ GOOD: Only runs once
  const [state, setState] = useState(() => JSON.parse(largeJSON));

  // Example: Reading from localStorage
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 'light';
  });

  return <div className={theme}>...</div>;
};

```

### Complex State Updates

```typescript
const TodoApp = () => {
  const [todos, setTodos] = useState<Todo[]>([]);

  const addTodo = (text: string) => {
    setTodos(prev => [
      ...prev,
      { id: Date.now(), text, completed: false },
    ]);
  };

  const toggleTodo = (id: number) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const deleteTodo = (id: number) => {
    setTodos(prev => prev.filter(todo => todo.id !== id));
  };

  return (
    <div>
      <TodoInput onAdd={addTodo} />
      <TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </div>
  );
};

```

### State with Previous Value

```typescript
const Counter = () => {
  const [count, setCount] = useState(0);

  const increment = () => {
    setCount(prev => prev + 1); // Always uses latest state
  };

  const decrement = () => {
    setCount(prev => prev - 1);
  };

  const incrementByAmount = (amount: number) => {
    setCount(prev => prev + amount);
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
      <button onClick={() => incrementByAmount(5)}>+5</button>
    </div>
  );
};

```

## Real-World Use Cases

### 1. Form State Management

```typescript
const ContactForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.message) newErrors.message = 'Message is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    try {
      await submitForm(formData);
      setFormData({ name: '', email: '', message: '' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={formData.name}
        onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
      />
      {errors.name && <span>{errors.name}</span>}
      {/* ... other fields */}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
};

```

### 2. Toggle State

```typescript
const Modal = () => {
  const [isOpen, setIsOpen] = useState(false);

  const openModal = () => setIsOpen(true);
  const closeModal = () => setIsOpen(false);
  const toggleModal = () => setIsOpen(prev => !prev);

  return (
    <>
      <button onClick={toggleModal}>Toggle Modal</button>
      {isOpen && (
        <div className="modal">
          <h2>Modal Title</h2>
          <p>Modal content</p>
          <button onClick={closeModal}>Close</button>
        </div>
      )}
    </>
  );
};

```

### 3. Array State

```typescript
const TagInput = () => {
  const [tags, setTags] = useState<string[]>([]);
  const [inputValue, setInputValue] = useState('');

  const addTag = () => {
    if (inputValue && !tags.includes(inputValue)) {
      setTags(prev => [...prev, inputValue]);
      setInputValue('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(prev => prev.filter(tag => tag !== tagToRemove));
  };

  return (
    <div>
      <div className="tags">
        {tags.map(tag => (
          <span key={tag} className="tag">
            {tag}
            <button onClick={() => removeTag(tag)}>×</button>
          </span>
        ))}
      </div>
      <input
        value={inputValue}
        onChange={e => setInputValue(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && addTag()}
      />
      <button onClick={addTag}>Add</button>
    </div>
  );
};

```

### 4. Dependent State

```typescript
const MultiStepForm = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    personal: { name: '', email: '' },
    address: { street: '', city: '', zip: '' },
    payment: { card: '', expiry: '' },
  });

  const nextStep = () => setStep(prev => Math.min(prev + 1, 3));
  const prevStep = () => setStep(prev => Math.max(prev - 1, 1));

  const updatePersonal = (data: Partial<typeof formData.personal>) => {
    setFormData(prev => ({
      ...prev,
      personal: { ...prev.personal, ...data },
    }));
  };

  return (
    <div>
      <StepIndicator currentStep={step} totalSteps={3} />
      {step === 1 && (
        <PersonalInfo
          data={formData.personal}
          onChange={updatePersonal}
          onNext={nextStep}
        />
      )}
      {step === 2 && (
        <Address
          data={formData.address}
          onChange={data => setFormData(prev => ({ ...prev, address: data }))}
          onNext={nextStep}
          onBack={prevStep}
        />
      )}
      {step === 3 && (
        <Payment
          data={formData.payment}
          onChange={data => setFormData(prev => ({ ...prev, payment: data }))}
          onBack={prevStep}
          onSubmit={() => submitForm(formData)}
        />
      )}
    </div>
  );
};

```

## Common Mistakes

### 1. Stale State in Closures

```typescript
// ❌ BAD: Stale state in event handler
const Counter = () => {
  const [count, setCount] = useState(0);

  const incrementThree = () => {
    setCount(count + 1); // count is 0
    setCount(count + 1); // count is still 0
    setCount(count + 1); // count is still 0
    // Result: count = 1, not 3!
  };

  return <button onClick={incrementThree}>+3</button>;
};

// ✅ GOOD: Functional updates
const Counter = () => {
  const [count, setCount] = useState(0);

  const incrementThree = () => {
    setCount(c => c + 1);
    setCount(c => c + 1);
    setCount(c => c + 1);
    // Result: count = 3
  };

  return <button onClick={incrementThree}>+3</button>;
};

```

### 2. Mutating State Directly

```typescript
// ❌ BAD: Mutating state directly
const TodoApp = () => {
  const [todos, setTodos] = useState<Todo[]>([]);

  const addTodo = (text: string) => {
    todos.push({ id: Date.now(), text, completed: false }); // Mutation!
    setTodos(todos); // React won't re-render (same reference)
  };

  return <TodoInput onAdd={addTodo} />;
};

// ✅ GOOD: Create new array
const TodoApp = () => {
  const [todos, setTodos] = useState<Todo[]>([]);

  const addTodo = (text: string) => {
    setTodos(prev => [
      ...prev,
      { id: Date.now(), text, completed: false },
    ]);
  };

  return <TodoInput onAdd={addTodo} />;
};

```

### 3. Setting State During Render

```typescript
// ❌ BAD: Setting state during render (infinite loop)
const Counter = () => {
  const [count, setCount] = useState(0);

  setCount(count + 1); // Infinite loop!

  return <div>{count}</div>;
};

// ✅ GOOD: Conditional state update during render
const Counter = () => {
  const [count, setCount] = useState(0);
  const [doubleCount, setDoubleCount] = useState(0);

  // Acceptable: conditional update that terminates
  if (count % 2 === 0 && doubleCount !== count * 2) {
    setDoubleCount(count * 2);
  }

  return (
    <div>
      <p>Count: {count}</p>
      <p>Double: {doubleCount}</p>
    </div>
  );
};

```

### 4. Using Object/Array State Without Spread

```typescript
// ❌ BAD: Not spreading state
const UserForm = () => {
  const [user, setUser] = useState({ name: '', email: '' });

  const updateName = () => {
    setUser({ name: 'John' }); // email is lost!
  };

  return <button onClick={updateName}>Set Name</button>;
};

// ✅ GOOD: Spread existing state
const UserForm = () => {
  const [user, setUser] = useState({ name: '', email: '' });

  const updateName = () => {
    setUser(prev => ({ ...prev, name: 'John' })); // email preserved
  };

  return <button onClick={updateName}>Set Name</button>;
};

```

## Best Practices

1. **Use functional updates when setting state based on previous state**: `setState(prev => newValue)`.

2. **Use lazy initialization for expensive initial state**: `useState(() => expensiveComputation())`.

3. **Keep state minimal**: Only store what you need in state.

4. **Use multiple state variables for unrelated state**: Don't combine unrelated values into one object.

5. **Don't mutate state directly**: Always create new objects/arrays.

6. **Use state colocation**: Keep state as close to where it's used as possible.

7. **Avoid setting state during render**: It causes unnecessary re-renders.

## Performance Considerations

### useState Performance

| Aspect | Impact | Mitigation |
|--------|--------|------------|
| State updates | Trigger re-renders | Batch updates |
| Object state | New reference on update | Use `useReducer` for complex state |
| Array state | New array on update | Spread operator or `useReducer` |
| Lazy initialization | One-time cost | Use function initializer |

### When to Use useState vs useReducer

| Use Case | useState | useReducer |
|----------|----------|------------|
| Simple state | ✅ | ❌ |
| Complex state | ❌ | ✅ |
| Multiple related values | ❌ | ✅ |
| Complex update logic | ❌ | ✅ |
| Testing | ✅ | ✅ |

## Interview Questions

### Beginner (5-10)

**Q1: What is useState?**
A: `useState` is a React Hook that adds state to function components. It returns a stateful value and a setter function. When the setter is called, React re-renders the component with the new state.

**Q2: How do you initialize state with useState?**
A: `const [count, setCount] = useState(0)`. The argument to `useState` is the initial state value.

**Q3: Can you update state directly?**
A: No. Always use the setter function: `setCount(5)`. Direct state mutation (`count = 5`) won't trigger re-renders.

**Q4: What is lazy initialization in useState?**
A: Lazy initialization lets you pass a function to `useState` that only runs on the first render: `useState(() => expensiveComputation())`. This prevents expensive computations on every render.

**Q5: What is state batching?**
A: React batches multiple state updates into a single re-render. For example, calling `setCount` and `setName` in the same handler only causes one re-render.

**Q6: What are functional updates?**
A: Functional updates let you update state based on the previous state: `setCount(prev => prev + 1)`. This is important when setting state multiple times in the same handler.

**Q7: Can useState be conditional?**
A: No. Hooks must be called in the same order every render. Calling hooks conditionally breaks the hook order and causes errors.

**Q8: What is the difference between state and props?**
A: State is internal to a component and can be changed. Props are passed from parent to child and are read-only.

**Q9: When does useState cause a re-render?**
A: When you call the setter function with a new value. If you set state to the same value (for primitives), React skips the re-render.

**Q10: Can you use useState with objects?**
A: Yes. Use the spread operator to update: `setUser(prev => ({ ...prev, name: 'John' }))`.

### Intermediate (5-10)

**Q11: Explain how useState works internally.**
A: `useState` stores state in the fiber node's `memoizedState` property. On each render, it returns the current state from the fiber. When the setter is called, it creates an Update object, enqueues it in the fiber's updateQueue, and schedules a re-render.

**Q12: What is the difference between state and refs?**
A: State triggers re-renders when changed; refs don't. State is for data that should be displayed; refs are for mutable values that don't affect rendering (DOM access, timers, etc.).

**Q13: How does React handle state updates in event handlers?**
A: React batches state updates in event handlers. Multiple updates are queued and applied together in a single re-render. This is called automatic batching (React 18).

**Q14: What is the `flushSync` API?**
A: `flushSync` forces React to synchronously flush pending state updates. Use it when you need immediate DOM updates after state change (e.g., measuring DOM after state change).

**Q15: How do you reset state?**
A: Use a `key` prop to reset state: `<Component key={resetKey} />`. When the key changes, React unmounts the old component and mounts a new one with fresh state.

**Q16: What is the difference between `useState` and `useReducer`?**
A: `useState` is for simple state. `useReducer` is for complex state with multiple sub-values or complex update logic. Both use the same underlying mechanism.

**Q17: How do you handle derived state?**
A: Compute derived state during render, not in `useEffect`:

```typescript
const filtered = useMemo(() => items.filter(...), [items, query]);

```

**Q18: What is the performance impact of state updates?**
A: State updates trigger re-renders. Multiple updates batched together cause one re-render. State updates to the same value (primitives) skip re-renders.

**Q19: How do you share state between components?**
A: Lift state up to the nearest common ancestor and pass it down via props, or use Context API for deeply nested components.

**Q20: What are the common patterns for state management?**
A:

- Local state: `useState` for component-specific state
- Lifted state: State moved to parent component
- Context: State shared across component tree
- External stores: Redux, Zustand, etc.

### Senior (10-15)

**Q21: Explain the complete state update lifecycle.**
A:

1. Setter function called

2. React creates an Update object

3. Update enqueued in fiber's updateQueue

4. React schedules a re-render

5. During next render:

   - React processes all queued updates
   - Computes new state for each update
   - Returns new state value
   - Component re-renders with new state

**Q22: How does state batching work in React 18?**
A: React 18 uses automatic batching via the `scheduleCallback` function. All state updates (in event handlers, setTimeout, promises) are batched into a single re-render. This is implemented via the `flushSync` escape hatch.

**Q23: What is the "state closure" problem?**
A: State closures occur when a callback captures stale state. For example, a `setTimeout` that references `count` will use the value at the time the timeout was set, not the current value. Solution: functional updates or refs.

**Q24: How does state work with React Suspense?**
A: Suspense can suspend state updates during concurrent rendering. When a component suspends, React pauses rendering and shows the fallback. State updates are queued and applied when the component resumes.

**Q25: What is the difference between `useState` and `useRef` for mutable values?**
A: `useState` triggers re-renders; `useRef` doesn't. Use `useState` for data that should be displayed. Use `useRef` for DOM access, timers, and values that don't affect rendering.

**Q26: How do you handle complex state updates?**
A: Use `useReducer` for complex state with multiple sub-values or complex update logic. It provides a `dispatch` function and a `reducer` that handles state transitions.

**Q27: What is the "state hoisting" pattern?**
A: State hoisting moves state to the nearest common ancestor. Child components receive state and callbacks via props. This is the standard way to share state between siblings.

**Q28: How does state interact with React.memo?**
A: `React.memo` wraps components to skip re-renders when props haven't changed. State updates still trigger re-renders of the component itself, but memoized children won't re-render unless their props change.

**Q29: What is the performance impact of state on large component trees?**
A: State updates trigger re-renders of the component and all its descendants (unless memoized). For large trees, this can be expensive. Mitigate with `React.memo`, state colocation, and context splitting.

**Q30: How do you test stateful components?**
A: Use React Testing Library:

```typescript
test('increments counter', () => {
  render(<Counter />);
  fireEvent.click(screen.getByText('+1'));
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

```

### FAANG-style (5-10)

**Q31: Design a state management system for a large-scale application.**
A:

1. **Local state**: `useState` for component-specific state

2. **Lifted state**: State moved to common ancestors

3. **Context**: State shared across component tree

4. **External stores**: Redux/Zustand for global state

5. **Server state**: React Query/TanStack Query

6. **State normalization**: Flatten nested state

7. **State colocation**: Keep state near usage

**Q32: How would you debug a state-related issue?**
A:

1. **React DevTools**: Inspect state values

2. **Why did this render**: Enable in React DevTools

3. **Console logging**: Log state changes

4. **React.Profiler**: Measure render performance

5. **Chrome DevTools**: Record interactions

**Q33: Analyze the performance implications of state design.**
A:

- **Granular state**: More state variables = more re-renders
- **Object state**: New reference on update = unnecessary re-renders
- **Derived state**: Computing in render vs useEffect
- **State colocation**: Moving state closer reduces re-renders

**Q34: How would you implement state persistence?**
A:

```typescript
const usePersistedState = (key: string, initialValue: any) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(state));
  }, [key, state]);

  return [state, setState];
};

```

**Q35: Design a state management system for offline-first apps.**
A:

1. **Local storage**: Persist state locally

2. **Sync queue**: Queue changes for sync

3. **Conflict resolution**: CRDT or last-write-wins

4. **Optimistic updates**: Show changes immediately

5. **Background sync**: Sync when online

**Q36: How would you implement state time-travel debugging?**
A:

1. **State history**: Store all state snapshots

2. **Time-travel controls**: Navigate to past states

3. **Action replay**: Replay user actions

4. **State diffing**: Show what changed between states

5. **DevTools integration**: Visualize state changes

**Q37: Analyze the memory implications of state.**
A:

- **Per state variable**: ~100 bytes
- **Object state**: Additional memory for properties
- **Array state**: Additional memory for elements
- **State history**: Memory for previous states
- **Optimization**: Use `useReducer` for complex state

**Q38: How would you implement state synchronization across tabs?**
A:

```typescript
const useCrossTabState = (key: string, initialValue: any) => {
  const [state, setState] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key) {
        setState(JSON.parse(e.newValue!));
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [key]);

  const setPersistedState = (value: any) => {
    setState(value);
    localStorage.setItem(key, JSON.stringify(value));
  };

  return [state, setPersistedState];
};

```

**Q39: How does state interact with React Server Components?**
A: Server Components can't use state. They're rendered on the server and serialized. Client Components hydrate with normal state. Server and client state are separate.

**Q40: Design a state management system for real-time collaborative apps.**
A:

1. **CRDT**: Conflict-free replicated data types

2. **Operational transformation**: Transform operations

3. **State merging**: Merge concurrent changes

4. **Conflict resolution**: Handle conflicting edits

5. **Optimistic updates**: Show changes immediately

### Follow-ups (5-10)

**Q41: How would you explain useState to a junior developer?**
A: "`useState` is like a variable that React watches. When you change it, React re-renders the component with the new value. You get the current value and a function to change it: `const [count, setCount] = useState(0)`."

**Q42: What are the edge cases in state management?**
A:

- Stale closures in async callbacks
- State updates after unmount
- Conditional hook calls
- State serialization/deserialization
- Concurrent state updates

**Q43: How does state handle the "derived state" pattern?**
A: Derived state should be computed during render, not stored in state:

```typescript
const [items, setItems] = useState([]);
const [query, setQuery] = useState('');
const filtered = useMemo(() => items.filter(...), [items, query]);

```

**Q44: What is the relationship between state and React DevTools?**
A: React DevTools shows component state, allows editing, and tracks why components re-render. It's essential for debugging state-related issues.

**Q45: How does state interact with React StrictMode?**
A: StrictMode double-renders in development. This can cause state to appear to reset. It's intentional — it helps detect side effects and impure render functions.

**Q46: What is the future of state management in React?**
A: React is exploring:

- Automatic memoization (React Compiler)
- Better concurrent state handling
- Server state integration
- Improved state colocation patterns

**Q47: How would you implement state validation?**
A:

```typescript
const useValidatedState = (initialValue: any, validator: Function) => {
  const [state, setState] = useState(initialValue);
  const [error, setError] = useState<string | null>(null);

  const setValidatedState = (value: any) => {
    const validationError = validator(value);
    if (validationError) {
      setError(validationError);
    } else {
      setError(null);
      setState(value);
    }
  };

  return [state, setValidatedState, error];
};

```

**Q48: How does state handle the "optimistic update" pattern?**
A: Optimistic updates show changes immediately before server confirmation:

```typescript
const handleLike = async (postId: string) => {
  setPosts(prev => prev.map(p =>
    p.id === postId ? { ...p, likes: p.likes + 1 } : p
  ));
  try {
    await api.likePost(postId);
  } catch {
    // Revert on error
    setPosts(prev => prev.map(p =>
      p.id === postId ? { ...p, likes: p.likes - 1 } : p
    ));
  }
};

```

**Q49: How would you implement state rollback?**
A:

```typescript
const useRollbackState = (initialValue: any) => {
  const [history, setHistory] = useState([initialValue]);
  const [index, setIndex] = useState(0);

  const setState = (value: any) => {
    setHistory(prev => [...prev.slice(0, index + 1), value]);
    setIndex(prev => prev + 1);
  };

  const undo = () => setIndex(prev => Math.max(0, prev - 1));
  const redo = () => setIndex(prev => Math.min(history.length - 1, prev + 1));

  return [history[index], setState, { undo, redo, canUndo: index > 0, canRedo: index < history.length - 1 }];
};

```

**Q50: How does state interact with React's concurrent features?**
A: Concurrent features affect state:

- Transitions defer state updates
- `useDeferredValue` creates lagging state
- Suspense can pause state updates
- State updates can be interrupted

## Summary

`useState` is the fundamental React Hook for adding state to function components. It provides a stateful value and a setter function. Key features include functional updates, lazy initialization, and automatic batching. Understanding `useState` is crucial for building interactive React applications.

## Cheat Sheet

```text
useState Key Points:
├── What: Hook for adding state to function components
├── Syntax: const [state, setState] = useState(initialValue)
├── Lazy: useState(() => expensiveComputation())
├── Functional: setState(prev => newValue)
├── Batching: Multiple updates → one re-render
├── Primitives: Same value → skip re-render
├── Objects: Always spread: { ...prev, ...new }

Common Patterns:
├── Simple state: useState(initialValue)
├── Object state: useState({ ... })
├── Array state: useState([])
├── Toggle: setState(prev => !prev)
├── Functional: setState(prev => prev + 1)
├── Reset: key={resetKey}
└── Lazy: useState(() => expensiveComputation())

Common Mistakes:
├── Stale state in closures (use functional updates)
├── Mutating state directly (always create new objects)
├── Setting state during render (causes infinite loop)
├── Not spreading object state (loses properties)
├── Conditional hook calls (breaks hook order)
└── Using useEffect for derived state (compute during render)

Performance:
├── Batch updates (React 18 automatic batching)
├── Functional updates for based-on-previous-state
├── Lazy initialization for expensive initial state
├── State colocation (keep state near usage)
├── React.memo to prevent child re-renders
└── useReducer for complex state logic

When to Use useState vs useReducer:
├── useState: Simple state, few sub-values
├── useReducer: Complex state, multiple sub-values, complex logic
└── Both use the same underlying mechanism

```

## References & Learn More

- [React Docs: useState](https://react.dev/reference/react/useState)
- [React useState Hook Guide](https://www.freecodecamp.org/news/usestate-hook-explained/)
- [How useState Works Under the Hood](https://dmitripavlutin.com/usestate-react-hook/)
