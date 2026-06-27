# Execution Context

## Definition

An **Execution Context** is the environment in which JavaScript code is evaluated and executed. It contains all the necessary information for the JS engine to run a specific piece of code, including variable declarations, function declarations, scope chain, and the `this` binding.

Think of it as a container that holds everything the JavaScript engine needs to execute a specific block of code.

## Why Do We Need It?

- **Code Organization**: Provides a structured environment for code execution
- **Scope Management**: Determines variable accessibility and lifetime
- **Variable Lifecycle**: Manages when variables are created, used, and destroyed
- **Understanding JavaScript**: Critical for understanding closures, hoisting, and scope
- **Debugging**: Helps trace code execution and understand errors

## How It Works

### Types of Execution Contexts

```
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTION CONTEXT TYPES                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Global Execution Context (GEC)                          │
│     - Created when JS program starts                        │
│     - Creates global object (window in browser)             │
│     - Sets 'this' to global object                          │
│     - Only one per program                                   │
│                                                              │
│  2. Function Execution Context (FEC)                        │
│     - Created when function is called                       │
│     - Each function has its own context                     │
│     - Multiple can exist simultaneously                     │
│                                                              │
│  3. Eval Execution Context (EEC)                            │
│     - Created when code is executed inside eval()           │
│     - Avoid using eval() - security risks                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Creation Phase vs Execution Phase

```
┌─────────────────────────────────────────────────────────────┐
│              EXECUTION CONTEXT LIFECYCLE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PHASE 1: CREATION PHASE                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Scan for function declarations                    │    │
│  │ • Allocate memory for variables                     │    │
│  │ • Set var variables to undefined                    │    │
│  │ • Set let/const variables to uninitialized          │    │
│  │ • Create lexical environment                        │    │
│  │ • Create variable environment                       │    │
│  │ • Determine 'this' binding                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│  PHASE 2: EXECUTION PHASE                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Execute code line by line                         │    │
│  │ • Assign values to variables                        │    │
│  │ • Execute function bodies                           │    │
│  │ • Push/pop function contexts onto call stack        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Execution Context Stack (Call Stack)

```
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTION CONTEXT STACK                      │
│                    (LIFO - Last In, First Out)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Code:                                                       │
│  var global = 'I am global';                                │
│  function first() {                                         │
│      var first = 'I am first';                              │
│      second();                                               │
│  }                                                          │
│  function second() {                                        │
│      var second = 'I am second';                            │
│  }                                                          │
│  first();                                                   │
│                                                              │
│  STACK VISUALIZATION:                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │    ┌─────────────────────┐                          │    │
│  │    │  2nd FEC            │ ← Top (current)         │    │
│  │    │  (second function)  │                          │    │
│  │    └─────────────────────┘                          │    │
│  │    ┌─────────────────────┐                          │    │
│  │    │  1st FEC            │                          │    │
│  │    │  (first function)   │                          │    │
│  │    └─────────────────────┘                          │    │
│  │    ┌─────────────────────┐                          │    │
│  │    │  GEC                │ ← Bottom (always here)  │    │
│  │    │  (Global Context)   │                          │    │
│  │    └─────────────────────┘                          │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  After second() returns:                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │    ┌─────────────────────┐                          │    │
│  │    │  1st FEC            │ ← Top (current)         │    │
│  │    │  (first function)   │                          │    │
│  │    └─────────────────────┘                          │    │
│  │    ┌─────────────────────┐                          │    │
│  │    │  GEC                │ ← Bottom                │    │
│  │    └─────────────────────┘                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Execution Context Components

```
┌─────────────────────────────────────────────────────────────┐
│            EXECUTION CONTEXT STRUCTURE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Execution Context                      │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │         Lexical Environment                 │    │    │
│  │  │  • References to outer environment          │    │    │
│  │  │  • Block scope variables (let/const)        │    │    │
│  │  │  • Controls variable visibility            │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │         Variable Environment               │    │    │
│  │  │  • Stores var declarations                 │    │    │
│  │  │  • Function declarations                   │    │    │
│  │  │  • Function arguments                      │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │              This Binding                  │    │    │
│  │  │  • References to 'this' value              │    │    │
│  │  │  • Global context: window/global           │    │    │
│  │  │  • Function context: caller-dependent      │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Execution Context

```typescript
// Global Execution Context
var globalVar = 'I am global';
let globalLet = 'I am also global';
const globalConst = 'I am constant';

function outerFunction() {
  // Function Execution Context 1
  var outerVar = 'I am outer';
  
  function innerFunction() {
    // Function Execution Context 2
    var innerVar = 'I am inner';
    console.log(globalVar);  // Accesses GEC
    console.log(outerVar);   // Accesses FEC 1
    console.log(innerVar);   // Accesses FEC 2
  }
  
  innerFunction();
}

outerFunction();
```

### Variable Hoisting in Execution Context

```typescript
console.log(x);  // undefined (created in creation phase)
var x = 10;

console.log(y);  // ReferenceError (TDZ)
let y = 20;

function greet() {
  console.log(name);  // undefined
  var name = 'Alice';
  console.log(name);  // 'Alice'
}

greet();
```

### Object Method Execution Context

```typescript
const user = {
  name: 'Alice',
  greet() {
    // 'this' depends on how function is called
    console.log(`Hello, ${this.name}`);
  }
};

user.greet();  // this = user object

const greetFn = user.greet;
greetFn();  // this = undefined (strict mode) or window
```

### Nested Execution Contexts

```typescript
function outer() {
  const a = 1;
  
  function middle() {
    const b = 2;
    
    function inner() {
      const c = 3;
      console.log(a + b + c);  // 6
    }
    
    inner();
  }
  
  middle();
}

outer();

// Context stack progression:
// GEC created → outer() called → middle() called → inner() called
// inner() returns → middle() returns → outer() returns
```

### Eval Execution Context (Avoid!)

```typescript
// eval() creates its own execution context
const evalCode = 'var evalVar = 100';
eval(evalCode);
console.log(evalVar);  // 100 - pollutes current scope

// With 'this' in different contexts
function checkThis() {
  console.log(this);
}

checkThis();  // window (non-strict) or undefined (strict)

const obj = { method: checkThis };
obj.method();  // obj
```

## Real-World Use Cases

### 1. Module Pattern (Data Privacy)

```typescript
function createCounter() {
  // This creates a private execution context
  let count = 0;
  
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
}

const counter = createCounter();
counter.increment();  // 1
counter.increment();  // 2
console.log(counter.getCount());  // 2
// count is not accessible outside
```

### 2. Event Handler Context

```typescript
class ButtonHandler {
  constructor() {
    this.label = 'Click me';
    // Common mistake: losing 'this' context
    // this.handleClick = this.handleClick.bind(this);
  }
  
  handleClick() {
    console.log(this.label);
  }
}

const handler = new ButtonHandler();
// handler.handleClick();  // Would fail without bind

// Fix: bind or arrow function
const handler2 = new ButtonHandler();
handler2.handleClick = handler2.handleClick.bind(handler2);
handler2.handleClick();  // Works
```

### 3. React Component Context

```typescript
import React, { useState } from 'react';

function Counter() {
  // Each component render has its own execution context
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### 4. Closure Pattern in Loops

```typescript
// Problem: var has function scope, not block scope
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3
}

// Solution 1: let (block scope)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 0, 1, 2
}

// Solution 2: IIFE
for (var i = 0; i < 3; i++) {
  (function(index) {
    setTimeout(() => console.log(index), 100);  // 0, 1, 2
  })(i);
}
```

## Common Mistakes

### 1. Assuming `var` has Block Scope

```typescript
if (true) {
  var x = 10;
}
console.log(x);  // 10 - var is function/global scoped

if (true) {
  let y = 10;
}
console.log(y);  // ReferenceError - let is block scoped
```

### 2. Losing `this` Context

```typescript
const obj = {
  name: 'Alice',
  greet() {
    setTimeout(function() {
      console.log(this.name);  // undefined (window)
    }, 1000);
  }
};

// Fix with arrow function
const obj2 = {
  name: 'Alice',
  greet() {
    setTimeout(() => {
      console.log(this.name);  // 'Alice' (inherits 'this')
    }, 1000);
  }
};
```

### 3. Mixing `var` and `let` in Loops

```typescript
// All share same 'i' variable
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3
}

// Each iteration gets own 'i'
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 0, 1, 2
}
```

### 4. Arrow Functions and `this`

```typescript
const obj = {
  name: 'Alice',
  greet: () => {
    console.log(this);  // window, not obj
  }
};

obj.greet();  // Window { ... }
```

## Best Practices

1. **Use `let` and `const`** instead of `var` for block scoping
2. **Always bind methods** or use arrow functions for callbacks
3. **Avoid `eval()`** - use safer alternatives
4. **Be explicit about `this`** - use `.bind()`, arrow functions, or explicit parameters
5. **Understand scope chain** - know where variables come from
6. **Keep functions small** - easier to reason about execution contexts
7. **Use strict mode** - `'use strict'` helps catch common mistakes
8. **Avoid global variables** - they pollute the global execution context

## Performance Considerations

### Memory Management

```typescript
// Bad: Creates multiple execution contexts
function createObjects() {
  for (let i = 0; i < 1000000; i++) {
    const obj = { value: i };  // New context each iteration
  }
}

// Better: Reuse objects
function createObjects() {
  const obj = { value: 0 };
  for (let i = 0; i < 1000000; i++) {
    obj.value = i;  // Reuse same object
  }
}
```

### Stack Overflow Prevention

```typescript
// Bad: Deep recursion
function deepRecursion(n) {
  if (n === 0) return;
  deepRecursion(n - 1);
}

// Better: Iteration
function betterApproach(n) {
  while (n > 0) {
    n--;
  }
}
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is an execution context in JavaScript?**

A: An execution context is the environment where JavaScript code is evaluated and executed. It contains variable declarations, function declarations, scope chain, and the `this` binding. Think of it as a container that holds everything the JS engine needs to run a specific piece of code.

**Q2: What are the types of execution contexts?**

A: There are three types:
1. **Global Execution Context (GEC)**: Created when the program starts, one per program
2. **Function Execution Context (FEC)**: Created when a function is called, multiple can exist
3. **Eval Execution Context (EEC)**: Created when code is executed inside `eval()`

**Q3: What happens during the creation phase of an execution context?**

A: During the creation phase:
- Function declarations are scanned and stored
- Variables are allocated memory
- `var` variables are set to `undefined`
- `let`/`const` variables are set to uninitialized (TDZ)
- Lexical environment is created
- Variable environment is created
- `this` binding is determined

**Q4: What is the execution context stack?**

A: The execution context stack (also called the call stack) is a LIFO (Last In, First Out) data structure that tracks which execution contexts are currently active. When a function is called, its context is pushed onto the stack; when it returns, it's popped off.

**Q5: What is the difference between lexical environment and variable environment?**

A: 
- **Lexical Environment**: Stores block-scoped variables (`let`/`const`) and references to the outer environment
- **Variable Environment**: Stores function-scoped variables (`var`), function declarations, and function arguments

### Intermediate (5-10 questions)

**Q6: Why does `console.log(x)` return `undefined` but `console.log(y)` throws a ReferenceError?**

A:
```typescript
console.log(x);  // undefined
var x = 5;

console.log(y);  // ReferenceError
let y = 10;
```
During creation phase, `var x` is hoisted and initialized to `undefined`, while `let y` is hoisted but remains uninitialized (Temporal Dead Zone). Accessing an uninitialized variable throws a ReferenceError.

**Q7: What is the Temporal Dead Zone (TDZ)?**

A: The TDZ is the period between when a variable is hoisted and when it's initialized. During this time, the variable exists but cannot be accessed. Accessing it throws a ReferenceError. TDZ exists for `let` and `const` declarations.

**Q8: How does the `this` keyword work in different execution contexts?**

A: 
- **Global context**: `this` refers to `window` (browser) or `global` (Node.js)
- **Function context**: Depends on how the function is called (default binding)
- **Method context**: `this` refers to the object the method belongs to
- **Arrow functions**: Inherit `this` from the enclosing lexical context
- **Class constructors**: `this` refers to the newly created instance

**Q9: What happens when you call a function recursively?**

A: Each recursive call creates a new execution context and pushes it onto the call stack. If the recursion is too deep, it can cause a stack overflow error. Tail call optimization can help in some cases.

**Q10: Can you have multiple execution contexts running simultaneously?**

A: JavaScript is single-threaded, so only one execution context is active at a time. However, the call stack can have multiple contexts, and asynchronous code can queue up callbacks to run after the current context completes.

### Senior (10-15 questions)

**Q11: Explain how JavaScript processes code step by step from start to finish.**

A: 
1. **Creation Phase**: JavaScript engine scans the code, hoists declarations, and creates execution contexts
2. **Global Execution Context Created**: GEC is created with global object, `this` binding
3. **Function Calls**: When functions are called, new FECs are created and pushed onto the stack
4. **Execution Phase**: Code is executed line by line, values are assigned
5. **Function Returns**: When functions return, their FECs are popped from the stack
6. **Program End**: When all code is executed, GEC is popped and program ends

**Q12: How does the scope chain relate to execution contexts?**

A: Each execution context has a reference to its outer lexical environment (parent scope). When a variable is accessed, the JS engine first looks in the current scope, then follows the scope chain outward until it finds the variable or reaches the global scope. This chain is created during the creation phase based on where functions are defined (lexical scoping).

**Q13: What is the difference between the creation phase and execution phase?**

A: 
- **Creation Phase**: 
  - Function declarations are scanned and stored
  - Variable declarations are hoisted
  - Memory is allocated but code hasn't run yet
  - `var` = `undefined`, `let`/`const` = uninitialized
- **Execution Phase**: 
  - Code runs line by line
  - Variables are assigned values
  - Functions are called and their contexts are created

**Q14: How does strict mode affect execution contexts?**

A: Strict mode (`'use strict'`) changes several behaviors:
- `this` in functions defaults to `undefined` instead of `window`
- Prevents accidental global variable creation
- Throws errors for silent failures (e.g., read-only properties)
- Disables `eval()` from creating variables in calling scope
- Makes duplicate parameter names a syntax error

**Q15: What is the relationship between execution contexts and closures?**

A: Closures occur when a function retains access to its lexical environment even after its execution context has been popped from the call stack. The inner function holds a reference to the outer function's execution context, preventing it from being garbage collected. This is why closures can access variables from outer scopes.

### FAANG-style (5-10 questions)

**Q16: Design a system to track execution contexts in a JavaScript runtime.**

A: Key components:
1. **Context Stack Manager**: Maintains the call stack
2. **Context Factory**: Creates new execution contexts with proper bindings
3. **Scope Chain Builder**: Links contexts to their parent scopes
4. **Memory Manager**: Tracks variable allocation and cleanup
5. **Debug Interface**: Allows inspection of current contexts

```typescript
class ExecutionContextManager {
  private stack: ExecutionContext[] = [];
  
  push(context: ExecutionContext): void {
    this.stack.push(context);
  }
  
  pop(): ExecutionContext | undefined {
    return this.stack.pop();
  }
  
  peek(): ExecutionContext | undefined {
    return this.stack[this.stack.length - 1];
  }
}
```

**Q17: How would you optimize execution context creation for performance?**

A: 
1. **Minimize function creation**: Reuse function references
2. **Avoid deep nesting**: Flatten scope chains
3. **Use block scoping**: `let`/`const` over `var` for smaller scopes
4. **Lazy evaluation**: Only create contexts when needed
5. **Context pooling**: Reuse contexts for repeated function calls
6. **Avoid `eval()`**: Parse code statically when possible

**Q18: What are the implications of execution contexts for concurrent programming in JavaScript?**

A: Since JavaScript is single-threaded with an event loop:
- Only one execution context runs at a time
- Long-running contexts block the event loop
- Web Workers create separate execution contexts with message passing
- Async functions yield control back to the event loop
- Promise microtasks run between execution contexts

**Q19: How do you handle errors across multiple execution contexts?**

A: 
1. **Try-catch blocks**: Catch errors within a context
2. **Error boundaries**: React-like patterns for component trees
3. **Promise rejection handling**: `.catch()` or `unhandledrejection` event
4. **Global error handlers**: `window.onerror`, `window.onunhandledrejection`
5. **Error propagation**: Errors bubble up through the scope chain

**Q20: Explain how execution contexts work in a recursive function with tail call optimization.**

A: With TCO, if the last action is a function call, the current context can be reused instead of creating a new one. This prevents stack overflow for deep recursion. However, TCO is not widely supported in JavaScript engines and has limitations (e.g., no access to the call stack after optimization).

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a real-world bug caused by execution context misunderstanding?**

A: Common bug: Losing `this` in callbacks
```typescript
class User {
  constructor(private name: string) {}
  
  getName() {
    return this.name;
  }
  
  // Bug: 'this' is lost in callback
  delayedGreet() {
    setTimeout(function() {
      console.log(`Hello, ${this.name}`);  // undefined
    }, 1000);
  }
  
  // Fix: Arrow function
  delayedGreetFixed() {
    setTimeout(() => {
      console.log(`Hello, ${this.name}`);  // Works
    }, 1000);
  }
}
```

**Q22: How do execution contexts differ between browser and Node.js environments?**

A: 
- **Global Object**: `window` vs `global`
- **Module System**: CommonJS vs ES Modules
- **Event Loop**: Browser vs Node.js phases
- **Web APIs**: Available in browser, not in Node.js
- **Process**: Node.js has `process` object, browser doesn't

**Q23: What is the relationship between execution contexts and memory management?**

A: Each execution context holds references to variables. When a context is popped, its variables become eligible for garbage collection unless referenced elsewhere (closures). Understanding context lifetimes helps prevent memory leaks.

**Q24: How do you debug execution context issues in production?**

A: 
1. **Source maps**: Map minified code to original
2. **Error tracking**: Sentry, LogRocket for runtime errors
3. **Performance monitoring**: Track long-running contexts
4. **Heap snapshots**: Analyze memory usage
5. **Stack traces**: Understand execution flow
6. **Console logging**: Strategic `console.log` for debugging

**Q25: What are the security implications of execution contexts?**

A: 
1. **XSS**: Malicious code can access execution contexts
2. **Prototype pollution**: Can affect all contexts
3. **CORS**: Restricts cross-origin context access
4. **Content Security Policy**: Limits script execution
5. **Sandboxing**: Web Workers provide isolated contexts

## Summary

Execution contexts are fundamental to understanding how JavaScript works. Key takeaways:

1. **Three types**: Global, Function, and Eval execution contexts
2. **Two phases**: Creation phase (hoisting, memory allocation) and Execution phase (code runs)
3. **Stack-based**: Call stack manages context execution (LIFO)
4. **Scope chain**: Lexical environments create variable access chains
5. **`this` binding**: Depends on how functions are called
6. **Closures**: Functions can retain access to outer execution contexts
7. **Performance**: Understanding contexts helps optimize memory and prevent stack overflow

Understanding execution contexts is crucial for writing efficient, bug-free JavaScript and answering interview questions confidently.

## Cheat Sheet

```
EXECUTION CONTEXT CHEAT SHEET
═══════════════════════════════════════════════════════════════

TYPES:
• Global Execution Context (GEC) - one per program
• Function Execution Context (FEC) - one per function call
• Eval Execution Context (EEC) - avoid using

CREATION PHASE:
• Hoist function declarations
• Initialize var = undefined
• Let/const = uninitialized (TDZ)
• Create lexical environment
• Create variable environment
• Set 'this' binding

EXECUTION PHASE:
• Execute code line by line
• Assign values to variables
• Call functions (push to stack)
• Return from functions (pop from stack)

STACK (LIFO):
• New context → push to top
• Function returns → pop from top
• Only top context is active
• Stack overflow = too many contexts

THIS BINDING:
• Global: window/global
• Function: caller-dependent
• Method: object itself
• Arrow: inherits from parent
• Class: new instance

COMMON BUGS:
• var in loops (shared scope)
• Lost 'this' in callbacks
• TDZ access (let/const)
• Stack overflow (deep recursion)

BEST PRACTICES:
• Use let/const over var
• Bind methods or use arrows
• Avoid eval()
• Keep functions small
• Be explicit about 'this'
```

## References & Learn More

- [MDN: Execution Context](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_context)
- [JavaScript.info: Execution Context](https://javascript.info/execution-context)
- [V8 Blog: How V8 Optimizes JavaScript](https://v8.dev/blog)
- [Jake Archibald: Tasks, microtasks, queues and schedules](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/)
