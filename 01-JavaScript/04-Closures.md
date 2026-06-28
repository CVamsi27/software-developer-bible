# Closures

## Definition

A **Closure** is a function that remembers and can access variables from its outer (lexical) scope, even after the outer function has finished executing and its execution context has been removed from the call stack. Closures are created every time a function is created, at function creation time.

## Why Do We Need It?

- **Data Privacy**: Encapsulate variables and expose only what's needed
- **Function Factories**: Create functions with preset configurations
- **Event Handlers**: Maintain state in callback functions
- **React Hooks**: Enable state management in functional components
- **Partial Application**: Pre-fill function arguments
- **Memoization**: Cache function results

## How It Works

### Closure Mechanism

```text
┌─────────────────────────────────────────────────────────────┐
│                    CLOSURE MECHANISM                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CODE:                                                       │
│  function outer() {                                         │
│    const outerVar = 'I am outer';                          │
│    function inner() {                                       │
│      console.log(outerVar);  // Accesses outer variable     │
│    }                                                        │
│    return inner;                                            │
│  }                                                          │
│  const closure = outer();                                   │
│  closure();  // 'I am outer'                                │
│                                                              │
│  LEXICAL ENVIRONMENT CHAIN:                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Global Execution Context                   │    │    │
│  │  │  • closure = [Function: inner]             │    │    │
│  │  │                                              │    │    │
│  │  │  ┌─────────────────────────────────────┐    │    │    │
│  │  │  │  outer() Execution Context          │    │    │    │
│  │  │  │  • outerVar = 'I am outer'         │    │    │    │
│  │  │  │                                     │    │    │    │
│  │  │  │  ┌─────────────────────────────┐    │    │    │    │
│  │  │  │  │  inner() Closure            │    │    │    │    │
│  │  │  │  │  • References outerVar ─────┼────┼────┼────┘    │
│  │  │  │  │  • Can access outer scope   │    │    │         │
│  │  │  │  └─────────────────────────────┘    │    │         │
│  │  │  │                                     │    │         │
│  │  │  └─────────────────────────────────────┘    │         │
│  │  │                                              │         │
│  │  └─────────────────────────────────────────────┘         │
│  │                                                          │
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### How Closures Capture Variables

```text
┌─────────────────────────────────────────────────────────────┐
│               HOW CLOSURES CAPTURE VARIABLES                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PRIMITIVE VALUES (Copied):                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function createCounter() {                        │    │
│  │    let count = 0;  // Primitive                     │    │
│  │    return function() {                              │    │
│  │      count++;  // Modifies own copy                │    │
│  │      return count;                                  │    │
│  │    };                                                │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const counter = createCounter();                   │    │
│  │  counter();  // 1                                   │    │
│  │  counter();  // 2                                   │    │
│  │  counter();  // 3                                   │    │
│  │                                                      │    │
│  │  // Each closure has its own 'count' variable      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  REFERENCE VALUES (Shared):                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function createArrayProcessor() {                 │    │
│  │    const array = [];  // Reference                  │    │
│  │    return {                                         │    │
│  │      add: (item) => array.push(item),              │    │
│  │      getArray: () => array                         │    │
│  │    };                                                │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  const processor = createArrayProcessor();          │    │
│  │  processor.add(1);                                  │    │
│  │  processor.add(2);                                  │    │
│  │  console.log(processor.getArray());  // [1, 2]     │    │
│  │                                                      │    │
│  │  // All closures share the same array reference     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Closure Scope Chain

```text
┌─────────────────────────────────────────────────────────────┐
│                 CLOSURE SCOPE CHAIN                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  function grandparent() {                                  │
│    const gpVar = 'grandparent';                            │
│    function parent() {                                     │
│      const pVar = 'parent';                                │
│      function child() {                                    │
│        const cVar = 'child';                               │
│        console.log(gpVar);  // Accesses grandparent scope  │
│        console.log(pVar);   // Accesses parent scope       │
│        console.log(cVar);   // Accesses own scope          │
│      }                                                      │
│      return child;                                          │
│    }                                                        │
│    return parent;                                           │
│  }                                                          │
│                                                              │
│  SCOPE CHAIN:                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  child() → parent() → grandparent() → Global       │    │
│  │                                                      │    │
│  │  child closure can access:                          │    │
│  │  • cVar (own scope)                                 │    │
│  │  • pVar (parent scope)                              │    │
│  │  • gpVar (grandparent scope)                        │    │
│  │  • global variables                                 │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Closure

```typescript
function createGreeter(greeting: string) {
  return function(name: string) {
    return `${greeting}, ${name}!`;
  };
}

const hello = createGreeter("Hello");
const goodbye = createGreeter("Goodbye");

console.log(hello("Alice"));    // "Hello, Alice!"
console.log(goodbye("Alice"));  // "Goodbye, Alice!"

// Each closure has its own 'greeting' variable

```

### Data Privacy (Module Pattern)

```typescript
function createBankAccount(initialBalance: number) {
  let balance = initialBalance;  // Private variable

  return {
    deposit(amount: number) {
      if (amount > 0) {
        balance += amount;
        return `Deposited $${amount}. Balance: $${balance}`;
      }
      return "Invalid amount";
    },

    withdraw(amount: number) {
      if (amount > 0 && amount <= balance) {
        balance -= amount;
        return `Withdrew $${amount}. Balance: $${balance}`;
      }
      return "Insufficient funds";
    },

    getBalance() {
      return balance;
    }
  };
}

const account = createBankAccount(1000);
console.log(account.deposit(500));    // "Deposited $500. Balance: $1500"
console.log(account.withdraw(200));   // "Withdrew $200. Balance: $1300"
console.log(account.getBalance());    // 1300
// console.log(account.balance);     // undefined (private!)

```

### Event Handler Closure

```typescript
function setupButton(buttonId: string, message: string) {
  const button = document.getElementById(buttonId);

  // Closure captures 'message'
  button?.addEventListener('click', () => {
    alert(message);  // message is accessible
  });
}

setupButton('btn1', 'Hello!');
setupButton('btn2', 'Goodbye!');

```

### Loop Closure Problem

```typescript
// Problem: All callbacks share same 'i'
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3
}

// Solution 1: Use let (block scope)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 0, 1, 2
}

// Solution 2: IIFE
for (var i = 0; i < 3; i++) {
  (function(index) {
    setTimeout(() => console.log(index), 100);  // 0, 1, 2
  })(i);
}

// Solution 3: setTimeout third argument
for (var i = 0; i < 3; i++) {
  setTimeout((index) => console.log(index), 100, i);  // 0, 1, 2
}

```

### Function Factory

```typescript
function createMultiplier(multiplier: number) {
  return function(number: number) {
    return number * multiplier;
  };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);
const tenTimes = createMultiplier(10);

console.log(double(5));    // 10
console.log(triple(5));    // 15
console.log(tenTimes(5));  // 50

```

### Memoization with Closures

```typescript
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map<string, ReturnType<T>>();

  return function(...args: Parameters<T>): ReturnType<T> {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  } as T;
}

const expensiveCalculation = memoize((n: number): number => {
  console.log('Computing...');
  return n * n;
});

console.log(expensiveCalculation(4));  // Computing... 16
console.log(expensiveCalculation(4));  // 16 (cached, no computation)

```

### React Hook Closure

```typescript
import { useState, useEffect } from 'react';

function useCounter(initialValue: number = 0) {
  const [count, setCount] = useState(initialValue);

  // Closure captures 'count' and 'setCount'
  const increment = () => setCount(c => c + 1);
  const decrement = () => setCount(c => c - 1);
  const reset = () => setCount(initialValue);

  return { count, increment, decrement, reset };
}

// Usage
function Counter() {
  const { count, increment, decrement, reset } = useCounter(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}

```

### Private Class Fields (Closure Pattern)

```typescript
function createPerson(name: string, age: number) {
  // Private variables
  let _name = name;
  let _age = age;

  return {
    get name() { return _name; },
    set name(value: string) {
      if (value.length > 0) _name = value;
    },
    get age() { return _age; },
    set age(value: number) {
      if (value > 0 && value < 150) _age = value;
    },
    greet() {
      return `Hi, I'm ${_name}, ${_age} years old`;
    }
  };
}

const person = createPerson("Alice", 30);
console.log(person.name);  // "Alice"
person.name = "Bob";
console.log(person.name);  // "Bob"
// Direct access not possible

```

## Real-World Use Cases

### 1. React State Management

```typescript
import { useState, useCallback } from 'react';

function useTodoList() {
  const [todos, setTodos] = useState<string[]>([]);

  // Closures capture 'todos' and 'setTodos'
  const addTodo = useCallback((todo: string) => {
    setTodos(prev => [...prev, todo]);
  }, []);

  const removeTodo = useCallback((index: number) => {
    setTodos(prev => prev.filter((_, i) => i !== index));
  }, []);

  const clearTodos = useCallback(() => {
    setTodos([]);
  }, []);

  return { todos, addTodo, removeTodo, clearTodos };
}

```

### 2. Debounce/Throttle Implementation

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;

  return function(...args: Parameters<T>) {
    // Closure captures 'timeout' and 'func'
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

const handleSearch = debounce((query: string) => {
  console.log(`Searching: ${query}`);
}, 300);

```

### 3. Event Listener Management

```typescript
function createEventManager() {
  const listeners = new Map<string, Function[]>();

  return {
    on(event: string, callback: Function) {
      if (!listeners.has(event)) {
        listeners.set(event, []);
      }
      listeners.get(event)!.push(callback);

      // Return unsubscribe function (closure)
      return () => {
        const callbacks = listeners.get(event);
        if (callbacks) {
          const index = callbacks.indexOf(callback);
          if (index > -1) {
            callbacks.splice(index, 1);
          }
        }
      };
    },

    emit(event: string, ...args: any[]) {
      const callbacks = listeners.get(event);
      if (callbacks) {
        callbacks.forEach(cb => cb(...args));
      }
    }
  };
}

const events = createEventManager();
const unsubscribe = events.on('data', (data: any) => console.log(data));
events.emit('data', { value: 42 });
unsubscribe();  // Remove listener

```

### 4. Configuration Pattern

```typescript
function createApiConfig(baseUrl: string) {
  const config = {
    baseUrl,
    timeout: 5000,
    retries: 3
  };

  return {
    get: (endpoint: string) => fetch(`${config.baseUrl}${endpoint}`),
    post: (endpoint: string, data: any) =>
      fetch(`${config.baseUrl}${endpoint}`, {
        method: 'POST',
        body: JSON.stringify(data)
      }),
    setTimeout: (ms: number) => {
      config.timeout = ms;
      return this;  // For chaining
    }
  };
}

const api = createApiConfig('https://api.example.com');
api.get('/users');  // Uses captured baseUrl

```

### 5. Iterator Pattern

```typescript
function createRangeIterator(start: number, end: number) {
  let current = start;

  return {
    next() {
      if (current <= end) {
        return { value: current++, done: false };
      }
      return { done: true };
    },
    [Symbol.iterator]() {
      return this;
    }
  };
}

const iterator = createRangeIterator(1, 5);
console.log(iterator.next());  // { value: 1, done: false }
console.log(iterator.next());  // { value: 2, done: false }
// ... until done

```

## Common Mistakes

### 1. Loop Closure Problem

```typescript
// BAD: All callbacks share same variable
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3
}

// GOOD: Use let or IIFE
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 0, 1, 2
}

```

### 2. Accidentally Capturing Large Objects

```typescript
// BAD: Captures entire large object
function processData() {
  const largeData = new Array(1000000).fill(0);

  return function() {
    // Closure captures 'largeData' even if not used
    return "Done";
  };
}

// GOOD: Only capture what you need
function processDataOptimized() {
  const largeData = new Array(1000000).fill(0);
  const summary = { length: largeData.length };

  return function() {
    return summary.length;  // Only captures summary
  };
}

```

### 3. Forgetting to Clean Up Closures

```typescript
// BAD: Memory leak - closure keeps reference
function createHandler() {
  const hugeData = new Array(1000000).fill(0);

  return function handler() {
    console.log(hugeData.length);
    // hugeData is kept alive even after handler is done
  };
}

// GOOD: Release reference when done
function createHandlerOptimized() {
  let hugeData: number[] | null = new Array(1000000).fill(0);

  return function handler() {
    console.log(hugeData!.length);
    hugeData = null;  // Release reference
  };
}

```

### 4. Arrow Function `this` in Closures

```typescript
// BAD: Arrow function inherits 'this' from outer scope
const obj = {
  name: 'Alice',
  greet: () => {
    // 'this' is window, not obj
    console.log(this.name);
  }
};

// GOOD: Use regular function for methods
const obj2 = {
  name: 'Alice',
  greet() {
    console.log(this.name);
  }
};

```

## Best Practices

### 1. Limit Closure Scope

```typescript
// Bad: Captures entire object
function bad() {
  const hugeObject = { data: new Array(1000000), name: 'test' };
  return function() {
    return hugeObject.name;  // Captures entire object
  };
}

// Good: Only capture needed values
function good() {
  const hugeObject = { data: new Array(1000000), name: 'test' };
  const { name } = hugeObject;  // Destructure
  return function() {
    return name;  // Only captures name
  };
}

```

### 2. Use WeakMap for Private Data

```typescript
const privateData = new WeakMap();

class Person {
  constructor(name: string) {
    privateData.set(this, { name });
  }

  getName() {
    return privateData.get(this)?.name;
  }
}

```

### 3. Clean Up Event Listeners

```typescript
function setupEventListener() {
  const handler = () => console.log('clicked');
  document.addEventListener('click', handler);

  // Return cleanup function
  return () => {
    document.removeEventListener('click', handler);
  };
}

const cleanup = setupEventListener();
// Later: cleanup();

```

### 4. Use Closure for Configuration

```typescript
function createConfig(defaults: Record<string, any>) {
  return function configure(overrides: Record<string, any>) {
    return { ...defaults, ...overrides };
  };
}

const createAppConfig = createConfig({
  theme: 'light',
  language: 'en'
});

const config = createAppConfig({ theme: 'dark' });
// { theme: 'dark', language: 'en' }

```

## Performance Considerations

### Memory Usage

```typescript
// Each closure retains a reference to its lexical environment
function createClosures() {
  const largeArray = new Array(1000000).fill(0);

  // Bad: Creates 1000 closures, each holding reference
  const closures = [];
  for (let i = 0; i < 1000; i++) {
    closures.push(() => {
      console.log(i);  // Each closure captures 'i'
    });
  }

  return closures;
}

// Better: Minimize what each closure captures
function createClosuresOptimized() {
  const largeArray = new Array(1000000).fill(0);

  // Only capture what's needed
  const closures = [];
  for (let i = 0; i < 1000; i++) {
    const value = i;  // Capture specific value
    closures.push(() => {
      console.log(value);
    });
  }

  return closures;
}

```

### Garbage Collection

```typescript
// Closures prevent garbage collection of their lexical environment
function createClosure() {
  let data = new Array(1000000).fill(0);

  return function() {
    // Even if we don't use 'data', it's kept alive
    return "Done";
  };
}

// To allow GC, explicitly release reference
function createClosureWithCleanup() {
  let data: number[] | null = new Array(1000000).fill(0);

  return function() {
    const result = data?.length;
    data = null;  // Allow GC
    return result;
  };
}

```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is a closure in JavaScript?**

A: A closure is a function that remembers and can access variables from its outer (lexical) scope, even after the outer function has finished executing. Closures are created every time a function is created.

**Q2: How are closures created?**

A: Closures are created when a function is defined inside another function and the inner function is returned or referenced outside. The inner function retains access to the outer function's variables.

**Q3: What is the use of closures?**

A: Common uses include:

- Data privacy (encapsulation)
- Function factories
- Event handlers
- Maintaining state in callbacks
- React hooks
- Memoization

**Q4: Do all functions create closures?**

A: Yes, all functions create closures at creation time. However, the closure is only useful if the function is used outside its original scope.

**Q5: What is the scope chain in closures?**

A: Closures have access to their own scope, the outer function's scope, and the global scope. This chain is called the scope chain or lexical environment chain.

### Intermediate (5-10 questions)

**Q6: Explain the loop closure problem and how to solve it.**

A: The problem occurs when using `var` in loops - all callbacks share the same variable. Solutions:

1. Use `let` instead of `var` (block scoping)

2. Use IIFE to create new scope for each iteration

3. Use `setTimeout` third argument to pass the value

**Q7: How do closures affect memory management?**

A: Closures retain references to their lexical environment, preventing garbage collection. If a closure captures a large object, that object stays in memory as long as the closure exists.

**Q8: What is the difference between closure and scope?**

A:

- **Scope**: Defines variable accessibility (where variables are visible)
- **Closure**: The combination of a function and its lexical environment that it remembers

All closures have scope, but not all scope creates closures.

**Q9: How do closures work with `this`?**

A: Arrow functions inherit `this` from their enclosing scope (lexical this). Regular functions have their own `this` based on how they're called. This can cause confusion in closures.

**Q10: Can closures be used for data encapsulation?**

A: Yes, closures are commonly used for data privacy. By returning functions that access private variables, you can expose only the methods you want, keeping the data hidden.

### Senior (10-15 questions)

**Q11: Explain how closures relate to the lexical environment.**

A: Each execution context has a lexical environment that contains its variables and a reference to the outer lexical environment. When a closure is created, it retains a reference to its lexical environment, allowing access to outer variables even after the outer function returns.

**Q12: How do closures interact with garbage collection?**

A: Closures prevent garbage collection of their lexical environment. The garbage collector cannot free memory referenced by closures. This can lead to memory leaks if closures capture large objects unnecessarily.

**Q13: What is the memory footprint of closures?**

A: Each closure retains a reference to its entire lexical environment chain. The footprint includes:

- All variables in the closure's scope
- All variables in outer scopes (if referenced)
- The function itself
- Any objects referenced by these variables

**Q14: How do you optimize closure memory usage?**

A:

1. Only capture variables you actually use

2. Destructure objects to capture only needed properties

3. Set references to null when done

4. Use WeakMap for private data

5. Avoid creating closures in loops unnecessarily

**Q15: What is the relationship between closures and functional programming?**

A: Closures enable functional programming concepts:

- **Higher-order functions**: Functions that return functions
- **Partial application**: Pre-filling function arguments
- **Currying**: Converting functions to accept one argument at a time
- **Composition**: Combining functions
- **Immutability**: Maintaining state without mutation

### FAANG-style (5-10 questions)

**Q16: Design a state management system using closures.**

A:

```typescript
function createStore<T>(initialState: T) {
  let state = initialState;
  const listeners = new Set<() => void>();

  return {
    getState: () => state,
    setState: (newState: T | ((prev: T) => T)) => {
      state = typeof newState === 'function'
        ? (newState as (prev: T) => T)(state)
        : newState;
      listeners.forEach(listener => listener());
    },
    subscribe: (listener: () => void) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    }
  };
}

const store = createStore({ count: 0 });
const unsubscribe = store.subscribe(() => {
  console.log('State changed:', store.getState());
});
store.setState({ count: 1 });  // Logs state change
unsubscribe();

```

**Q17: How would you implement a pub/sub system with closures?**

A:

```typescript
function createPubSub() {
  const subscribers = new Map<string, Set<Function>>();

  return {
    subscribe(event: string, callback: Function) {
      if (!subscribers.has(event)) {
        subscribers.set(event, new Set());
      }
      subscribers.get(event)!.add(callback);

      return () => subscribers.get(event)?.delete(callback);
    },

    publish(event: string, ...args: any[]) {
      subscribers.get(event)?.forEach(callback => {
        callback(...args);
      });
    },

    unsubscribe(event: string, callback?: Function) {
      if (callback) {
        subscribers.get(event)?.delete(callback);
      } else {
        subscribers.delete(event);
      }
    }
  };
}

```

**Q18: Analyze the performance implications of closures in a React application.**

A:

1. **Memory**: Closures in hooks can prevent garbage collection

2. **Re-renders**: New closures on each render cause unnecessary re-renders

3. **Solution**: Use `useCallback` and `useMemo` to memoize closures

4. **Cleanup**: Always clean up event listeners and subscriptions

5. **Profiling**: Use React DevTools to identify closure-related performance issues

**Q19: How do closures affect testability?**

A:

1. **Isolation**: Closures provide natural isolation for unit testing

2. **Dependency injection**: Can mock dependencies through closure parameters

3. **State management**: Easy to test state changes

4. **Challenges**: Private state can be harder to verify

5. **Solution**: Expose test-specific methods or use dependency injection

**Q20: What are the security implications of closures?**

A:

1. **Data leakage**: Closures can expose private data if not careful

2. **Prototype pollution**: Can affect all instances

3. **XSS**: Closures in event handlers can be exploited

4. **Mitigation**: Use strict mode, validate inputs, sanitize data

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a closure-related memory leak?**

A:

```typescript
// Memory leak: Closure keeps reference to DOM element
function createLeakyHandler() {
  const element = document.getElementById('button');

  element?.addEventListener('click', () => {
    // Closure keeps 'element' alive even after removal
    console.log('clicked');
  });

  // Element is never garbage collected
}

// Fix: Remove event listener when done
function createCleanHandler() {
  const element = document.getElementById('button');
  const handler = () => console.log('clicked');

  element?.addEventListener('click', handler);

  return () => {
    element?.removeEventListener('click', handler);
  };
}

```

**Q22: How do you debug closure-related issues?**

A:

1. **Chrome DevTools**: Inspect closure scopes in debugger

2. **Console.log**: Log captured variables

3. **WeakRef**: Track closure references

4. **Memory snapshots**: Compare heap snapshots

5. **Performance profiling**: Identify closure-related performance issues

**Q23: What is the relationship between closures and modules?**

A: Modules use closures to encapsulate private state. The module pattern returns an object with methods that close over private variables, exposing only the public API.

**Q24: How do closures work in different JavaScript environments?**

A:

- **Browser**: Standard closure behavior
- **Node.js**: Same behavior, but with module system
- **Web Workers**: Separate global scope, but closures work the same
- **Service Workers**: Closures can persist across requests

**Q25: What are best practices for using closures in large applications?**

A:

1. Document closure behavior in complex functions

2. Use TypeScript to track variable types

3. Limit closure scope to what's needed

4. Clean up event listeners and subscriptions

5. Use WeakMap for private data

6. Profile memory usage regularly

7. Avoid creating closures in hot paths

8. Use dependency injection for testability

## Summary

Closures are a powerful JavaScript feature:

1. **Definition**: Functions that remember their lexical environment

2. **Creation**: Created when functions are defined

3. **Use cases**: Data privacy, event handlers, React hooks, memoization

4. **Memory**: Can prevent garbage collection if not managed

5. **Performance**: Minimize captured variables

6. **Debugging**: Use DevTools to inspect closure scopes

7. **Best practices**: Clean up, limit scope, use WeakMap

Understanding closures is essential for writing efficient, maintainable JavaScript and answering advanced interview questions.

## Cheat Sheet

```text
CLOSURES CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHAT IS A CLOSURE?
• Function + its lexical environment
• Remembers outer variables
• Created at function creation time

USE CASES:
• Data privacy (module pattern)
• Event handlers
• React hooks
• Memoization
• Function factories
• Configuration

SCOPE CHAIN:
• Own scope → Parent scope → Global scope
• Access variables up the chain
• Lexical scoping (where defined, not called)

MEMORY IMPLICATIONS:
• Closures retain references to outer variables
• Prevents garbage collection
• Can cause memory leaks if not managed

COMMON PATTERNS:
// Data privacy
function createCounter() {
  let count = 0;
  return {
    increment: () => ++count,
    getCount: () => count
  };
}

// Event handler
function setupHandler(element, callback) {
  element.addEventListener('click', callback);
}

// Memoization
function memoize(fn) {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    return cache.has(key) ? cache.get(key) : cache.set(key, fn(...args)).get(key);
  };
}

BEST PRACTICES:
• Limit closure scope
• Clean up event listeners
• Use WeakMap for private data
• Avoid capturing large objects
• Profile memory usage

DEBUGGING:
• Chrome DevTools: Inspect closure scopes
• console.log: Log captured variables
• Memory snapshots: Track references
• Performance profiling: Identify issues

COMMON MISTAKES:
• Loop closure problem (var in loops)
• Capturing large objects unnecessarily
• Not cleaning up event listeners
• Arrow function 'this' confusion

INTERVIEW TIPS:
• Explain lexical environment
• Discuss memory implications
• Show practical examples
• Mention performance considerations
• Talk about debugging techniques

```

## References & Learn More

- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- [JavaScript.info: Closures](https://javascript.info/closure)
- [Wikipedia: Closures (computer science)](https://en.wikipedia.org/wiki/Closure_(computer_programming))
- [Eloquent JavaScript: Closures](https://eloquentjavascript.net/3rd_edition/chapter5.html)
- [FreeCodeCamp: Closures](https://www.freecodecamp.org/news/lets-learn-about-closures-2d716ea1f5e1/)
