# Scope

## Definition

**Scope** in JavaScript determines the accessibility and lifetime of variables and functions. It defines where variables are declared and where they can be accessed. JavaScript has three main types of scope: global scope, function scope, and block scope.

## Why Do We Need It?

- **Variable Accessibility**: Controls where variables can be accessed
- **Namespace Management**: Prevents naming conflicts
- **Memory Management**: Variables are destroyed when their scope ends
- **Code Organization**: Helps organize code into logical units
- **Encapsulation**: Creates private variables and functions

## How It Works

### Types of Scope

```text
┌─────────────────────────────────────────────────────────────┐
│                    TYPES OF SCOPE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. GLOBAL SCOPE                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  // Variables declared outside any function/block   │    │
│  │  var globalVar = 'I am global';                    │    │
│  │  let globalLet = 'Also global';                    │    │
│  │  const GLOBAL_CONST = 'Constant';                  │    │
│  │                                                      │    │
│  │  function example() {                              │    │
│  │    // Can access global variables                  │    │
│  │    console.log(globalVar);  // Works               │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  2. FUNCTION SCOPE                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function example() {                              │    │
│  │    var functionVar = 'I am function-scoped';       │    │
│  │    let functionLet = 'Also function-scoped';       │    │
│  │    const FUNCTION_CONST = 'Constant';              │    │
│  │                                                      │    │
│  │    // Variables only accessible inside function    │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  console.log(functionVar);  // ReferenceError!     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  3. BLOCK SCOPE                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  if (true) {                                       │    │
│  │    let blockLet = 'I am block-scoped';             │    │
│  │    const BLOCK_CONST = 'Constant';                 │    │
│  │    var notBlockScoped = 'I am function-scoped';    │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  console.log(blockLet);       // ReferenceError!   │    │
│  │  console.log(notBlockScoped); // Works! (var)      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Scope Chain

```text
┌─────────────────────────────────────────────────────────────┐
│                      SCOPE CHAIN                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  function outer() {                                         │
│    const outerVar = 'outer';                               │
│    function middle() {                                      │
│      const middleVar = 'middle';                            │
│      function inner() {                                     │
│        const innerVar = 'inner';                            │
│        console.log(outerVar);  // Accesses outer scope     │
│        console.log(middleVar); // Accesses middle scope    │
│        console.log(innerVar);  // Accesses own scope       │
│      }                                                      │
│      inner();                                               │
│    }                                                        │
│    middle();                                                │
│  }                                                          │
│  outer();                                                   │
│                                                              │
│  SCOPE CHAIN VISUALIZATION:                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Global Scope                                        │    │
│  │  └── outer() Scope                                  │    │
│  │        └── middle() Scope                           │    │
│  │              └── inner() Scope                      │    │
│  │                                                      │    │
│  │  inner() can access:                                │    │
│  │  • innerVar (own scope)                             │    │
│  │  • middleVar (parent scope)                         │    │
│  │  • outerVar (grandparent scope)                     │    │
│  │  • global variables                                 │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Lexical Scope

```text
┌─────────────────────────────────────────────────────────────┐
│                     LEXICAL SCOPE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Lexical scope means scope is determined by where code     │
│  is written (defined), not where it's called.              │
│                                                              │
│  function outer() {                                         │
│    const message = 'Hello';                                │
│    function inner() {                                       │
│      console.log(message);  // Lexically scoped            │
│    }                                                        │
│    return inner;                                            │
│  }                                                          │
│                                                              │
│  const innerFunc = outer();                                 │
│  innerFunc();  // 'Hello' - even though outer() is done   │
│                                                              │
│  This works because of closures - inner() retains access   │
│  to outer's scope even after outer() returns.              │
│                                                              │
│  LEXICAL vs DYNAMIC SCOPING:                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  JavaScript: Lexical scoping                       │    │
│  │  • Scope determined at definition time              │    │
│  │  • Based on code structure                          │    │
│  │                                                      │    │
│  │  Some languages: Dynamic scoping                    │    │
│  │  • Scope determined at call time                    │    │
│  │  • Based on call stack                              │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### var vs let/const Scope

```text
┌─────────────────────────────────────────────────────────────┐
│                var vs let/const SCOPE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  var: FUNCTION SCOPED                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function example() {                              │    │
│  │    if (true) {                                     │    │
│  │      var x = 10;  // Function-scoped              │    │
│  │    }                                                │    │
│  │    console.log(x);  // 10 (still accessible!)     │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  let/const: BLOCK SCOPED                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function example() {                              │    │
│  │    if (true) {                                     │    │
│  │      let y = 20;  // Block-scoped                 │    │
│  │      const z = 30;  // Block-scoped               │    │
│  │    }                                                │    │
│  │    console.log(y);  // ReferenceError!            │    │
│  │    console.log(z);  // ReferenceError!            │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  SCOPE DIFFERENCE:                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  for (var i = 0; i < 3; i++) {                    │    │
│  │    // i is function-scoped (var)                   │    │
│  │  }                                                  │    │
│  │  console.log(i);  // 3 (accessible!)              │    │
│  │                                                      │    │
│  │  for (let j = 0; j < 3; j++) {                    │    │
│  │    // j is block-scoped (let)                      │    │
│  │  }                                                  │    │
│  │  console.log(j);  // ReferenceError!              │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Global Scope

```typescript
// Global scope
const globalConst = 'I am global';
let globalLet = 'Also global';
var globalVar = 'I am global too';

function checkScope() {
  console.log(globalConst);  // Accessible
  console.log(globalLet);    // Accessible
  console.log(globalVar);    // Accessible
}

checkScope();
console.log(globalConst);  // Accessible everywhere
```

### Function Scope

```typescript
function outerFunction() {
  const outerVar = 'I am outer';

  function innerFunction() {
    const innerVar = 'I am inner';
    console.log(outerVar);  // Accessible (parent scope)
    console.log(innerVar);  // Accessible (own scope)
  }

  innerFunction();
  console.log(innerVar);  // ReferenceError! Not accessible
}

outerFunction();
console.log(outerVar);  // ReferenceError! Not accessible
```

### Block Scope

```typescript
function blockScopeExample() {
  if (true) {
    let blockLet = 'I am block-scoped';
    const BLOCK_CONST = 'Also block-scoped';
    var notBlockScoped = 'I am function-scoped';

    console.log(blockLet);       // Accessible
    console.log(BLOCK_CONST);    // Accessible
    console.log(notBlockScoped); // Accessible
  }

  console.log(blockLet);       // ReferenceError!
  console.log(BLOCK_CONST);    // ReferenceError!
  console.log(notBlockScoped); // Accessible (var is function-scoped)
}

blockScopeExample();
```

### Loop Scope

```typescript
// var in loops - shared scope
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3
}

// let in loops - block scope
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);  // 0, 1, 2
}

// Why? var i is hoisted to function/global scope
// All callbacks share the same i variable
// By the time setTimeout runs, i is already 3
```

### Nested Functions

```typescript
function level1() {
  const a = 1;

  function level2() {
    const b = 2;

    function level3() {
      const c = 3;

      console.log(a);  // Access level1's scope
      console.log(b);  // Access level2's scope
      console.log(c);  // Access own scope
    }

    level3();
  }

  level2();
}

level1();
```

### Scope with Closures

```typescript
function createCounter() {
  let count = 0;  // Encapsulated variable

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

### Block Scope in Switch Statements

```typescript
function switchExample(value: string) {
  switch (value) {
    case 'a': {
      let result = 'Option A';
      console.log(result);  // Accessible
      break;
    }
    case 'b': {
      let result = 'Option B';  // Different 'result' than case 'a'
      console.log(result);  // Accessible
      break;
    }
  }

  // result is not accessible here
}
```

### IIFE (Immediately Invoked Function Expression)

```typescript
// IIFE creates its own scope
(function() {
  const privateVar = 'I am private';
  console.log(privateVar);  // Accessible
})();

console.log(privateVar);  // ReferenceError!

// Arrow function IIFE
(() => {
  const privateVar = 'I am private';
  console.log(privateVar);  // Accessible
})();
```

## Real-World Use Cases

### 1. Module Pattern

```typescript
const Calculator = (function() {
  // Private variables
  let result = 0;

  // Private function
  function validateNumber(num: number): boolean {
    return !isNaN(num) && isFinite(num);
  }

  // Public API
  return {
    add(num: number) {
      if (validateNumber(num)) result += num;
      return this;
    },
    subtract(num: number) {
      if (validateNumber(num)) result -= num;
      return this;
    },
    getResult() {
      return result;
    },
    reset() {
      result = 0;
      return this;
    }
  };
})();

Calculator.add(5).subtract(2).getResult();  // 3
// result is not accessible directly
```

### 2. Event Handler Scope

```typescript
function setupForm() {
  const form = document.getElementById('myForm');
  const errors: string[] = [];

  form?.addEventListener('submit', (e) => {
    e.preventDefault();

    // Closure captures 'errors' array
    if (validateForm()) {
      submitForm();
    } else {
      showError(errors);
    }
  });

  function validateForm(): boolean {
    // Can access 'errors' from outer scope
    errors.length = 0;
    // ... validation logic
    return errors.length === 0;
  }

  function submitForm() {
    // Can access 'errors' from outer scope
    console.log('Submitting...');
  }
}
```

### 3. React Component Scope

```typescript
import { useState, useEffect } from 'react';

function UserProfile({ userId }: { userId: string }) {
  // Component scope
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Closure captures 'userId', 'setUser', 'setLoading'
    async function fetchUser() {
      try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, [userId]);  // Re-run when userId changes

  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
}
```

### 4. Configuration Pattern

```typescript
function createConfig(environment: string) {
  // Encapsulated configuration
  const configs = {
    development: { apiUrl: 'http://localhost:3000', debug: true },
    production: { apiUrl: 'https://api.example.com', debug: false },
    test: { apiUrl: 'http://test-api:3000', debug: true }
  };

  const config = configs[environment as keyof typeof configs];

  return {
    getApiUrl: () => config.apiUrl,
    isDebug: () => config.debug,
    getEnvironment: () => environment
  };
}

const envConfig = createConfig('development');
console.log(envConfig.getApiUrl());  // 'http://localhost:3000'
// configs is not accessible directly
```

## Common Mistakes

### 1. var in Loops

```typescript
// Bad: All callbacks share same 'var' variable
for (var i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100);  // 5, 5, 5, 5, 5
}

// Good: Use 'let' for block scoping
for (let i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100);  // 0, 1, 2, 3, 4
}
```

### 2. Accidental Global Variables

```typescript
function accidentalGlobal() {
  // Without var/let/const, creates global variable
  accidentalGlobalVar = 'I am global!';

  // With strict mode, throws ReferenceError
}

// Always use var, let, or const
function intentionalLocal() {
  const localVar = 'I am local';
  let localLet = 'I am also local';
  var localVar2 = 'I am function-scoped';
}
```

### 3. Shadowing Issues

```typescript
const x = 10;

function example() {
  const x = 20;  // Shadows outer x
  console.log(x);  // 20, not 10

  if (true) {
    const x = 30;  // Shadows both outer x's
    console.log(x);  // 30
  }

  console.log(x);  // 20 (back to function scope)
}

example();
console.log(x);  // 10 (global scope)
```

### 4. Hoisting Confusion

```typescript
// var is hoisted to function scope
function hoistingExample() {
  console.log(x);  // undefined (hoisted)
  var x = 10;
  console.log(x);  // 10
}

// let/const are hoisted but in TDZ
function tdzExample() {
  try {
    console.log(y);  // ReferenceError!
  } catch (e) {
    console.log('TDZ error');
  }
  let y = 20;
}
```

## Best Practices

### 1. Use const by Default

```typescript
// Good: const prevents reassignment
const API_URL = 'https://api.example.com';
const MAX_RETRIES = 3;

// Only use let when you need to reassign
let counter = 0;
counter++;

// Avoid var entirely
```

### 2. Declare Variables at Top of Scope

```typescript
function processData(data: any[]) {
  // Declare variables at top
  let result: any[] = [];
  let index: number;
  let item: any;

  // Then use them
  for (index = 0; index < data.length; index++) {
    item = data[index];
    if (item.isValid) {
      result.push(item);
    }
  }

  return result;
}
```

### 3. Use Block Scope for Loops

```typescript
// Good: let provides block scoping
for (let i = 0; i < items.length; i++) {
  const item = items[i];
  // item is scoped to this iteration
  processItem(item);
}

// Bad: var shares scope
for (var i = 0; i < items.length; i++) {
  var item = items[i];  // Shared across iterations
}
```

### 4. Avoid Global Variables

```typescript
// Bad: Global variable
globalCounter = 0;

// Good: Module pattern
const Counter = (function() {
  let count = 0;

  return {
    increment: () => ++count,
    getCount: () => count
  };
})();
```

## Performance Considerations

### Memory Management

```typescript
// Scope affects variable lifetime
function example() {
  // These variables live for the entire function
  const largeArray = new Array(1000000).fill(0);

  if (condition) {
    // This variable only lives in this block
    const smallValue = 42;
    console.log(smallValue);
  }
  // smallValue is destroyed here

  // largeArray is destroyed when function returns
}
```

### Scope Chain Lookup

```typescript
// Deeply nested scopes can impact performance
function level1() {
  const a = 1;

  function level2() {
    const b = 2;

    function level3() {
      const c = 3;

      function level4() {
        const d = 4;

        // Each lookup traverses the scope chain
        console.log(a + b + c + d);
      }

      level4();
    }

    level3();
  }

  level2();
}

// Better: Pass values as parameters
function level1Optimized() {
  const a = 1;
  level2(a);
}

function level2Optimized(a: number) {
  const b = 2;
  level3(a, b);
}

function level3Optimized(a: number, b: number) {
  const c = 3;
  level4(a, b, c);
}

function level4Optimized(a: number, b: number, c: number) {
  const d = 4;
  console.log(a + b + c + d);
}
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is scope in JavaScript?**

A: Scope determines where variables and functions are accessible in your code. It defines the lifetime and visibility of variables.

**Q2: What are the different types of scope in JavaScript?**

A: There are three main types:
1. **Global scope**: Accessible everywhere
2. **Function scope**: Accessible only within the function
3. **Block scope**: Accessible only within the block (for `let`/`const`)

**Q3: What is the difference between var, let, and const?**

A:
- `var`: Function-scoped, can be reassigned, hoisted
- `let`: Block-scoped, can be reassigned, TDZ
- `const`: Block-scoped, cannot be reassigned, TDZ

**Q4: What is lexical scope?**

A: Lexical scope means scope is determined by where code is written (defined), not where it's called. JavaScript uses lexical scoping.

**Q5: What is the scope chain?**

A: The scope chain is the hierarchy of scopes that JavaScript uses to resolve variable names. It goes from the current scope outward to the global scope.

### Intermediate (5-10 questions)

**Q6: Why does `var` have function scope instead of block scope?**

A: This is a historical design decision from before ES6. `var` was designed to be function-scoped for simplicity, but this caused many bugs. ES6 introduced `let` and `const` with block scoping to fix these issues.

**Q7: How does the scope chain work with closures?**

A: Closures retain access to their lexical environment (scope chain) even after the outer function returns. This allows inner functions to access outer variables.

**Q8: What is variable shadowing?**

A: Variable shadowing occurs when a variable in an inner scope has the same name as a variable in an outer scope. The inner variable "shadows" the outer one.

**Q9: How do you access global variables inside a function?**

A: You can access global variables directly from any scope. However, it's better to pass them as parameters for clarity and testability.

**Q10: What is the difference between scope and context?**

A:
- **Scope**: Where variables are accessible (determined by code structure)
- **Context**: What `this` refers to (determined by how functions are called)

### Senior (10-15 questions)

**Q11: How does scope relate to memory management?**

A: Variables are destroyed when their scope ends (garbage collected). Understanding scope helps predict variable lifetimes and prevent memory leaks.

**Q12: What are the performance implications of deep scope chains?**

A: Deeply nested scopes require more lookups to resolve variables. This can impact performance in tight loops or frequently called functions.

**Q13: How do different JavaScript engines optimize scope resolution?**

A: Engines use techniques like:
- Inline caching for property access
- Hidden classes for object shapes
- JIT compilation to optimize scope lookups
- Deoptimization when scope assumptions are violated

**Q14: How does scope work with `eval()`?**

A: `eval()` executes code in the current scope, which can modify variables in that scope. This is why `eval()` is dangerous and discouraged.

**Q15: What is the relationship between scope and hoisting?**

A: Hoisting moves declarations to the top of their scope. `var` is hoisted to function scope, while `let`/`const` are hoisted to block scope but remain in TDZ.

### FAANG-style (5-10 questions)

**Q16: Design a scope-aware variable resolver.**

A:
```typescript
class ScopeResolver {
  private scopes: Map<string, Map<string, any>> = new Map();
  private parentScope: ScopeResolver | null = null;

  constructor(parent?: ScopeResolver) {
    this.parentScope = parent || null;
  }

  declare(name: string, value: any): void {
    const currentScope = this.getCurrentScope();
    currentScope.set(name, value);
  }

  resolve(name: string): any {
    const currentScope = this.getCurrentScope();
    if (currentScope.has(name)) {
      return currentScope.get(name);
    }

    if (this.parentScope) {
      return this.parentScope.resolve(name);
    }

    throw new Error(`Variable '${name}' not defined`);
  }

  private getCurrentScope(): Map<string, any> {
    // Implementation depends on use case
    return new Map();
  }
}
```

**Q17: How would you implement block scoping for `var` in transpilers?**

A:
```typescript
// Original code
function example() {
  if (true) {
    var x = 10;
  }
  console.log(x);
}

// Transpiled to block scoping
function example() {
  var x;  // Declare at function scope
  if (true) {
    x = 10;  // Assign in block
  }
  console.log(x);
}
```

**Q18: Analyze the memory implications of different scoping strategies.**

A:
- **Global scope**: Longest lifetime, highest memory impact
- **Function scope**: Medium lifetime, moderate memory impact
- **Block scope**: Shortest lifetime, lowest memory impact

Optimization: Use block scoping to minimize variable lifetimes.

**Q19: How do you handle scope in a REPL environment?**

A:
```typescript
class REPL {
  private globalScope = new Map<string, any>();
  private currentScope = this.globalScope;

  execute(code: string): any {
    // Parse code
    // Create new scope for execution
    // Evaluate in current scope
    // Return result
  }

  getScope(): Map<string, any> {
    return new Map(this.currentScope);
  }
}
```

**Q20: What are the security implications of scope in JavaScript?**

A:
1. **Global scope pollution**: Can be exploited for attacks
2. **eval()**: Can inject code into current scope
3. **with statement**: Deprecated due to scope ambiguity
4. **Prototype pollution**: Can affect all objects in scope

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a scope-related bug in production?**

A: Common bug:
```typescript
// Bug: var in loop causes unexpected behavior
function processItems(items: any[]) {
  for (var i = 0; i < items.length; i++) {
    setTimeout(() => {
      console.log(items[i]);  // Undefined for all iterations!
    }, 100);
  }
}

// Fix: Use let
function processItemsFixed(items: any[]) {
  for (let i = 0; i < items.length; i++) {
    setTimeout(() => {
      console.log(items[i]);  // Correct item for each iteration
    }, 100);
  }
}
```

**Q22: How do you debug scope-related issues?**

A:
1. **Chrome DevTools**: Use Scope panel in debugger
2. **console.log**: Log variable values at different points
3. **Breakpoints**: Set breakpoints to inspect scope
4. **Linters**: Use ESLint to catch scope issues
5. **TypeScript**: Catch scope errors at compile time

**Q23: What is the relationship between scope and `this`?**

A: `this` is not part of the scope chain. It depends on how functions are called, not where they're defined. Arrow functions inherit `this` from their lexical scope.

**Q24: How do you handle scope in a single-page application?**

A:
1. Use module pattern for encapsulation
2. Avoid global variables
3. Use React/Vue component scope
4. Implement state management (Redux, Vuex)
5. Use closures for private state

**Q25: What are best practices for managing scope in large codebases?**

A:
1. Use `const` by default, `let` when needed
2. Avoid `var` entirely
3. Declare variables at top of scope
4. Use block scoping in loops
5. Avoid variable shadowing
6. Use TypeScript for type safety
7. Implement linting rules
8. Document scope behavior in complex functions

## Summary

Scope is fundamental to JavaScript:

1. **Three types**: Global, function, and block scope
2. **var vs let/const**: Function-scoped vs block-scoped
3. **Lexical scoping**: Scope determined by code structure
4. **Scope chain**: Hierarchical variable resolution
5. **Closures**: Retain access to outer scopes
6. **Memory**: Variables destroyed when scope ends
7. **Best practices**: Use const/let, avoid var, minimize scope

Understanding scope is essential for writing clean, efficient, bug-free JavaScript.

## Cheat Sheet

```text
SCOPE CHEAT SHEET
═══════════════════════════════════════════════════════════════

TYPES OF SCOPE:
• Global: Accessible everywhere
• Function: Accessible within function
• Block: Accessible within block (let/const)

VAR vs LET/CONST:
• var: Function-scoped, hoisted, reassignable
• let: Block-scoped, TDZ, reassignable
• const: Block-scoped, TDZ, not reassignable

SCOPE CHAIN:
• Current scope → Parent scope → Global scope
• Variable lookup traverses the chain
• Lexical scoping (where defined, not called)

CLOSURES:
• Retain access to outer lexical scope
• Created at function creation time
• Can cause memory leaks if not managed

COMMON BUGS:
• var in loops (shared scope)
• Variable shadowing
• Hoisting confusion
• Accidental globals

BEST PRACTICES:
• Use const by default
• Use let when needed
• Avoid var entirely
• Declare at top of scope
• Avoid shadowing
• Use block scoping

DEBUGGING:
• Chrome DevTools: Scope panel
• console.log: Log variable values
• Breakpoints: Inspect scope
• Linters: Catch scope issues

PERFORMANCE:
• Deep scope chains = more lookups
• Block scoping = shorter lifetimes
• Global scope = longest lifetime

SECURITY:
• Avoid global pollution
• Don't use eval()
• Prevent prototype pollution
```

## References & Learn More

- [MDN: Scope](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)
- [JavaScript.info: Scope & Closures](https://javascript.info/closure)
- [DigitalOcean: Understanding Scope and Closures in JavaScript](https://www.digitalocean.com/community/tutorials/understanding-scope-and-closures-in-javascript)
- [Dev.to: JavaScript Scope Explained](https://dev.to/boywithnohorns/javascript-scope-explained-1h83)
