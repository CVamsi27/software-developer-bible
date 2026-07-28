---
section: React
category: Frontend
tags: [concept]
---

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

---

## See Also
- [Animation](../30-Animation/)
- [Form Handling](../29-Form-Handling/)
- [JavaScript](../01-JavaScript/)
- [Next.js](../04-NextJS/)
- [Testing](../16-Testing/)

## References & Learn More

- [React Docs: useState](https://react.dev/reference/react/useState)
- [React useState Hook Guide](https://www.freecodecamp.org/news/usestate-hook-explained/)
- [How useState Works Under the Hood](https://dmitripavlutin.com/usestate-react-hook/)
