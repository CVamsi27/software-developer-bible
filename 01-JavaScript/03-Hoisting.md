---
section: JavaScript
category: Core
tags: [concept]
---

# Hoisting

## Definition

**Hoisting** is JavaScript's behavior of moving declarations to the top of their containing scope during the creation phase of the execution context. This means variables and functions can be used before they are declared in the code. However, only the declarations are hoisted, not the initializations.

## Why Do We Need It?

- **Function Declarations**: Allow functions to be used before they're defined
- **Code Organization**: Enables flexible code structure
- **Understanding JavaScript**: Critical for avoiding bugs and answering interview questions
- **Variable Behavior**: Explains why `var` variables are `undefined` before declaration
- **Debugging**: Helps understand unexpected variable behavior

## How It Works

### Hoisting Mechanism

```text
┌─────────────────────────────────────────────────────────────┐
│                    HOISTING MECHANISM                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  BEFORE HOISTING (What you write):                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  console.log(x);  // What happens here?            │    │
│  │  var x = 10;                                       │    │
│  │                                                      │    │
│  │  greet();  // What happens here?                    │    │
│  │  function greet() {                                │    │
│  │    console.log("Hello!");                           │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  AFTER HOISTING (What JS engine sees):                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  // Variable declaration hoisted                   │    │
│  │  var x;  // No value yet!                          │    │
│  │                                                      │    │
│  │  // Function declaration hoisted (with body)       │    │
│  │  function greet() {                                │    │
│  │    console.log("Hello!");                           │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  console.log(x);  // undefined                     │    │
│  │  x = 10;  // Assignment happens here               │    │
│  │                                                      │    │
│  │  greet();  // Works! Function is fully hoisted     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### What Gets Hoisted

```text
┌─────────────────────────────────────────────────────────────┐
│                    WHAT GETS HOISTED?                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ HOISTED:                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • var declarations → initialized to undefined     │    │
│  │  • function declarations → fully hoisted           │    │
│  │  • function expressions → var hoisted, not init    │    │
│  │  • arrow functions → var hoisted, not init         │    │
│  │  • class declarations → TDZ (like let/const)       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ❌ NOT HOISTED:                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • let declarations → TDZ                          │    │
│  │  • const declarations → TDZ                        │    │
│  │  • class declarations → TDZ                        │    │
│  │  • import statements → TDZ                         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  TDZ = Temporal Dead Zone (cannot access before declaration)│
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### var vs let/const Hoisting

```text
┌─────────────────────────────────────────────────────────────┐
│                 var vs let/const HOISTING                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  var HOISTING:                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  console.log(x);  // undefined                     │    │
│  │  var x = 5;                                       │    │
│  │                                                      │    │
│  │  // What happens internally:                       │    │
│  │  var x;  // Hoisted to top (undefined)            │    │
│  │  console.log(x);  // undefined                     │    │
│  │  x = 5;  // Assignment stays in place             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  let/const HOISTING:                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  console.log(y);  // ReferenceError!              │    │
│  │  let y = 10;                                       │    │
│  │                                                      │    │
│  │  // What happens internally:                       │    │
│  │  // y is hoisted but NOT initialized              │    │
│  │  // y is in "Temporal Dead Zone"                   │    │
│  │  console.log(y);  // ReferenceError               │    │
│  │  let y = 10;  // Initialization happens here      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Function Hoisting

```text
┌─────────────────────────────────────────────────────────────┐
│                    FUNCTION HOISTING                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FUNCTION DECLARATION:                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  greet();  // Works! "Hello!"                      │    │
│  │                                                      │    │
│  │  function greet() {                                │    │
│  │    console.log("Hello!");                           │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  // Entire function is hoisted                     │    │
│  │  // Can be used before declaration                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  FUNCTION EXPRESSION:                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  greet();  // TypeError: greet is not a function   │    │
│  │                                                      │    │
│  │  const greet = function() {                        │    │
│  │    console.log("Hello!");                           │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  // Only 'var/let/const' is hoisted, not init     │    │
│  │  // greet is undefined until assignment            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ARROW FUNCTION:                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  greet();  // TypeError: greet is not a function   │    │
│  │                                                      │    │
│  │  const greet = () => {                             │    │
│  │    console.log("Hello!");                           │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  // Same as function expression - only var hoisted │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Temporal Dead Zone (TDZ)

```text
┌─────────────────────────────────────────────────────────────┐
│                    TEMPORAL DEAD ZONE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIMELINE:                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  ─────────────────────────────────────────────────  │    │
│  │  |  TDZ  |        LIVE ZONE        |               │    │
│  │  ─────────────────────────────────────────────────  │    │
│  │                                                      │    │
│  │  |←─ Scope starts ─→|←─ Declaration ─→|←─ Use ─→|  │    │
│  │                     |                 |             │    │
│  │                     |   let x = 5;   |  x = 10;   │    │
│  │                     |                 |             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  CODE EXAMPLE:                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  {                                                   │    │
│  │    // TDZ starts here                              │    │
│  │    console.log(a);  // ReferenceError              │    │
│  │    console.log(b);  // ReferenceError              │    │
│  │                                                      │    │
│  │    let a = 10;  // TDZ ends here                   │    │
│  │    const b = 20;  // TDZ ends here                 │    │
│  │                                                      │    │
│  │    console.log(a);  // 10                           │    │
│  │    console.log(b);  // 20                           │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  WHY TDZ EXISTS:                                             │
│  • Prevents accidental use before initialization           │
│  • Makes code behavior more predictable                    │
│  • Enables better error messages                           │
│  • Supports block scoping properly                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic var Hoisting

```typescript
// var hoisting
console.log(name);  // undefined
var name = "Alice";
console.log(name);  // "Alice"

// What JS engine sees:
// var name;
// console.log(name);  // undefined
// name = "Alice";
// console.log(name);  // "Alice"

```

### let/const TDZ

```typescript
// let/const TDZ
try {
  console.log(age);  // ReferenceError: Cannot access 'age' before initialization
} catch (e) {
  console.log(e.message);
}

let age = 25;
console.log(age);  // 25

// const behaves the same
try {
  console.log(COLOR);  // ReferenceError
} catch (e) {
  console.log(e.message);
}

const COLOR = "red";
console.log(COLOR);  // "red"

```

### Function Declaration vs Expression

```typescript
// Function declaration - fully hoisted
add(2, 3);  // 5

function add(a: number, b: number): number {
  return a + b;
}

// Function expression - only var hoisted
try {
  multiply(2, 3);  // TypeError: multiply is not a function
} catch (e) {
  console.log(e.message);
}

const multiply = function(a: number, b: number): number {
  return a * b;
};

// Arrow function - same as expression
try {
  divide(6, 2);  // TypeError: divide is not a function
} catch (e) {
  console.log(e.message);
}

const divide = (a: number, b: number): number => a / b;

```

### Class Hoisting

```typescript
// Classes are NOT fully hoisted (TDZ like let/const)
try {
  const instance = new MyClass();  // ReferenceError
} catch (e) {
  console.log(e.message);
}

class MyClass {
  constructor() {
    this.value = 42;
  }
}

// This works (class expression)
const instance = new MyClassExpression();
console.log(instance.value);  // 42

const MyClassExpression = class {
  constructor() {
    this.value = 42;
  }
};

```

### Hoisting in Loops

```typescript
// var in loops - common bug
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);  // 3, 3, 3
}

// let in loops - works as expected
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);  // 0, 1, 2
}

// Why? var i is hoisted to function/global scope
// All callbacks share the same i variable
// By the time setTimeout runs, i is already 3

```

### Nested Function Hoisting

```typescript
function outer() {
  console.log(inner());  // Works! Function is hoisted

  function inner() {
    return "Hello from inner";
  }

  // But this wouldn't work:
  // console.log(inner2());  // TypeError
  // const inner2 = () => "Hello";
}

outer();

```

### Conditional Function Declaration

```typescript
// Function declarations are hoisted regardless of condition
if (true) {
  function sayHello() {
    return "Hello";
  }
} else {
  function sayHello() {
    return "Goodbye";
  }
}

console.log(sayHello());  // "Hello" (last declaration wins)

// This is why function expressions are safer
let sayGoodbye: () => string;

if (true) {
  sayGoodbye = () => "Hello";
} else {
  sayGoodbye = () => "Goodbye";
}

console.log(sayGoodbye());  // "Hello" (as expected)

```

## Real-World Use Cases

### 1. Utility Functions

```typescript
// Hoisting allows organizing code logically
function calculateArea(width: number, height: number): number {
  return multiply(width, height);  // Can use multiply before declaration
}

function calculatePerimeter(width: number, height: number): number {
  return add(add(width, width), add(height, height));
}

// Helper functions defined below (but hoisted)
function multiply(a: number, b: number): number {
  return a * b;
}

function add(a: number, b: number): number {
  return a + b;
}

```

### 2. Module Pattern

```typescript
// Hoisting enables the module pattern
const Module = (function() {
  // Private variables (not hoisted)
  let privateVar = "private";

  // Public API
  return {
    getVar: function() {
      return privateVar;
    },
    setVar: function(value: string) {
      privateVar = value;
    }
  };
})();

// Can't access privateVar directly
console.log(Module.getVar());  // "private"

```

### 3. React Component Hoisting

```typescript
// Component declarations are hoisted
function App() {
  return <ChildComponent />;
}

// Child can be used before declaration
function ChildComponent() {
  return <div>Hello</div>;
}

```

### 4. TypeScript Interface Hoisting

```typescript
// Interfaces are fully hoisted
interface User {
  name: string;
  age: number;
}

// Can use interface before declaration
function createUser(user: User): User {
  return user;
}

```

## Common Mistakes

### 1. Using var Before Declaration

```typescript
// Mistake: Expecting undefined
console.log(x);  // undefined (not ReferenceError!)
var x = 10;

// This can cause confusing bugs
function example() {
  console.log(x);  // undefined
  if (true) {
    var x = 20;  // Hoisted to function scope
  }
  console.log(x);  // 20
}

```

### 2. Assuming let/const Are Hoisted Like var

```typescript
// Mistake: Expecting undefined for let/const
try {
  console.log(y);  // ReferenceError, not undefined!
  let y = 20;
} catch (e) {
  console.log("Correct behavior: TDZ");
}

```

### 3. Function Expression Hoisting

```typescript
// Mistake: Using function expression before assignment
try {
  const result = greet();  // TypeError!
  console.log(result);
} catch (e) {
  console.log("TypeError: greet is not a function");
}

const greet = () => "Hello";

// Fix: Use function declaration
function greetFixed() {
  return "Hello";
}
const result = greetFixed();  // Works!

```

### 4. Class Hoisting

```typescript
// Mistake: Using class before declaration
try {
  const obj = new MyClass();  // ReferenceError!
} catch (e) {
  console.log("ReferenceError: Cannot access 'MyClass' before initialization");
}

class MyClass {
  constructor() {}
}

```

## Best Practices

### 1. Use const by Default

```typescript
// Good: const prevents reassignment
const API_URL = "https://api.example.com";
const MAX_RETRIES = 3;

// Only use let when you need to reassign
let counter = 0;
counter++;

// Avoid var entirely
// var is function-scoped, leads to confusing bugs

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

### 3. Use Function Declarations for hoisting

```typescript
// Good: Function declarations are fully hoisted
function processItem(item: any) {
  return transform(item);  // Can use transform before declaration
}

function transform(item: any) {
  return { ...item, processed: true };
}

// Function expressions should be used when needed conditionally
const processItemExpr = condition
  ? (item: any) => item.value
  : (item: any) => item.name;

```

### 4. Avoid Conditional Function Declarations

```typescript
// Bad: Conditional function declarations are unreliable
if (condition) {
  function doSomething() {
    return "A";
  }
} else {
  function doSomething() {
    return "B";
  }
}

// Good: Use function expressions
const doSomething = condition
  ? () => "A"
  : () => "B";

```

## Performance Considerations

### Memory Allocation

```typescript
// var is hoisted to function scope
function example() {
  // var x is allocated for entire function
  // even if only used in one branch
  if (true) {
    var x = 10;  // Allocated at function start
  }
  console.log(x);  // 10
}

// let/const are block-scoped
function exampleOptimized() {
  if (true) {
    const y = 10;  // Allocated only in this block
    console.log(y);  // 10
  }
  // y is not accessible here, memory can be freed
}

```

### Function Declaration Optimization

```typescript
// Function declarations are hoisted and created once
function expensiveOperation() {
  // This function object is created during creation phase
  // and reused for all calls
  return Math.random();
}

// Function expressions create new function object each time
const expensiveOperationExpr = function() {
  return Math.random();
};

```


## Summary

Hoisting is a fundamental JavaScript concept:

1. **What**: Declarations are moved to the top of their scope

2. **var**: Hoisted and initialized to `undefined`

3. **let/const**: Hoisted but not initialized (TDZ)

4. **Functions**: Declarations fully hoisted, expressions not

5. **Classes**: Not hoisted (TDZ like let/const)

6. **TDZ**: Prevents access before initialization

7. **Best practices**: Use const/let, avoid var, declare at top

Understanding hoisting is crucial for writing bug-free JavaScript and answering interview questions confidently.

## Cheat Sheet
```text
HOISTING CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHAT GETS HOISTED:
• var declarations → undefined
• let/const declarations → TDZ (uninitialized)
• function declarations → fully hoisted
• function expressions → only var hoisted
• class declarations → TDZ

VAR HOISTING:
console.log(x);  // undefined
var x = 5;

LET/CONST TDZ:
console.log(y);  // ReferenceError!
let y = 10;

FUNCTION DECLARATION:
greet();  // Works!
function greet() { return "Hello"; }

FUNCTION EXPRESSION:
greet();  // TypeError!
const greet = () => "Hello";

TEMPORAL DEAD ZONE:
• Period between hoisting and initialization
• let/const are in TDZ before declaration
• Accessing throws ReferenceError
• Exists from scope start to declaration

BEST PRACTICES:
• Use const by default
• Use let when needed
• Avoid var entirely
• Declare at top of scope
• Use function declarations for hoisting
• Avoid conditional function declarations

COMMON BUGS:
• var in loops (shared scope)
• Function expressions before assignment
• let/const TDZ access
• Class hoisting

DEBUGGING:
• console.trace() for execution flow
• Chrome DevTools breakpoints
• Linter rules for detection
• Step through code line by line

```

---

## See Also
- [TypeScript](../02-TypeScript/)
- [Node.js](../05-NodeJS/)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- [MDN: Hoisting](https://developer.mozilla.org/en-US/docs/Glossary/Hoisting)
- [JavaScript.info: Hoisting](https://javascript.info/closure)
- [BitBucket Blog: JavaScript Hoisting](https://blog.bitsrc.io/understanding-hoisting-in-javascript-1e74a48f4a96)
- [FreeCodeCamp: JavaScript Hoisting](https://www.freecodecamp.org/news/understanding-hoisting-in-javascript-1e74a48f4a96/)
