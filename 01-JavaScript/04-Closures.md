---
section: JavaScript
category: Core
tags: [concept]
---

# Closures

[![Section](https://img.shields.io/badge/section-JavaScript-blueviolet)](.)
[![Type](https://img.shields.io/badge/type-Concept-informational)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

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

---

## See Also
- [TypeScript](../02-TypeScript/)
- [Node.js](../05-NodeJS/)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- [JavaScript.info: Closures](https://javascript.info/closure)
- [Wikipedia: Closures (computer science)](https://en.wikipedia.org/wiki/Closure_(computer_programming))
- [Eloquent JavaScript: Closures](https://eloquentjavascript.net/3rd_edition/chapter5.html)
- [FreeCodeCamp: Closures](https://www.freecodecamp.org/news/lets-learn-about-closures-2d716ea1f5e1/)
