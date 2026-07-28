[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

# Lexical Environment

## Definition

A **Lexical Environment** is a specification type defined by the ECMAScript standard that associates a scope (the set of variable bindings) with a specific location in source code. It consists of an **Environment Record** (which stores the actual variable and function bindings) and an optional reference to an **outer lexical environment** (which enables the scope chain). Every time a function is called, a new lexical environment is created.

Think of it as the engine's internal data structure that maps identifiers to their values within a specific scope, along with the ability to look up identifiers in parent scopes.

## Why Do We Need It?

1. **Scope Management**: Determines which variables are accessible at any point in code execution

2. **Closure Implementation**: Lexical environments are the engine-level implementation behind closures

3. **Identifier Resolution**: Provides the mechanism for resolving variable names to their values

4. **Nested Scope Chain**: Enables inner functions to access variables from outer functions

5. **Specification Correctness**: Understanding lexical environments helps predict JavaScript behavior accurately

## How It Works

### Structure of a Lexical Environment

```text
Lexical Environment
├── Environment Record
│   ├── Declarative Environment Record (let, const, functions)
│   │   ├── Creates bindings for let/const/function declarations
│   │   └── Used by function scopes and block scopes
│   └── Object Environment Record (var, global)
│       ├── Creates bindings on a binding object (e.g., global object)
│       └── Used by global scope and with statements
│
└── Outer Environment Reference ([[OuterEnv]])
    └── Points to the enclosing lexical environment (scope chain)
```

### Lexical Environment Creation

```text
Function call creates a new Lexical Environment:

function outer(a) {
    ┌─────────────────────────────────────────┐
    │  Lexical Environment (outer call)        │
    │  Environment Record:                     │
    │    a → 10         (parameter)           │
    │    b → undefined  (var, hoisted)        │
    │    c → <uninit>   (let, TDZ)            │
    │  Outer: global environment               │
    └─────────────────────────────────────────┘

    return function inner(b) {
        ┌─────────────────────────────────────────┐
        │  Lexical Environment (inner call)        │
        │  Environment Record:                     │
        │    b → 20    (parameter)                │
        │  Outer: outer's lexical environment      │
        └─────────────────────────────────────────┘
    };
}
```

### Scope Chain Resolution

```typescript
const globalVar = 'global';

function outer() {
  const outerVar = 'outer';

  function inner() {
    const innerVar = 'inner';
    console.log(innerVar);  // Found in own environment
    console.log(outerVar);  // Found in outer's environment
    console.log(globalVar); // Found in global environment
  }

  inner();
}

// Resolution Path for inner():
// inner's env → outer's env → global env
```

### Block-Level Lexical Environments

```typescript
// Blocks create new lexical environments for let/const
let x = 1;

{
  // New lexical environment (block scope)
  let x = 2;       // Different variable than outer x
  const y = 3;     // Block-scoped
  var z = 4;       // NOT block-scoped — goes to function/global env
  console.log(x);  // 2
}

console.log(x);  // 1 (outer x unchanged)
console.log(z);  // 4 (var escapes the block)
// console.log(y); // ReferenceError — y is block-scoped
```

### Function Declaration Hoisting

```typescript
// Function declarations are hoisted to the top of their lexical environment
console.log(greet('Alice')); // "Hello, Alice!" — works due to hoisting

function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Let/const are hoisted but in TDZ
// console.log(tdzVar); // ReferenceError: Cannot access before initialization
let tdzVar = 'TDZ example';
```

### Environment Records in Detail

```text
┌─────────────────────────────────────────────────────────────┐
│              ENVIRONMENT RECORD TYPES                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DECLARATIVE ENVIRONMENT RECORD                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Stores bindings for function declarations          │    │
│  │ • Stores bindings for let, const declarations        │    │
│  │ • Stores function parameters                         │    │
│  │ • Used by: function scopes, block scopes, module     │    │
│  │ • Example: function foo() { let x = 1; }             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  OBJECT ENVIRONMENT RECORD                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Stores bindings on a binding object               │    │
│  │ • Each property access goes through [[Get]] on obj   │    │
│  │ • Used by: global environment, `with` statement      │    │
│  │ • Example: globalThis.x = 1                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  GLOBAL ENVIRONMENT                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Uses Object Environment Record                    │    │
│  │ • Binding object is the global object (window/global)│    │
│  │ • Also has a Declarative Environment Record         │    │
│  │ • [[OuterEnv]] = null (it's the root)               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Lexical Environment and Closure

```typescript
function createCounter() {
  // Lexical environment for createCounter()
  let count = 0;   // Binding in declarative environment record

  return function increment() {
    // Lexical environment for increment()
    // [[OuterEnv]] → createCounter's environment
    count++;        // Resolved via scope chain
    return count;
  };
}

const counter = createCounter();
console.log(counter());  // 1
console.log(counter());  // 2

// The createCounter's lexical environment is NOT garbage collected
// because increment's [[OuterEnv]] still references it
```

### Loop and Lexical Environment (var vs let)

```typescript
// var: ONE lexical environment for the entire function
const funcsVar: (() => void)[] = [];

for (var i = 0; i < 3; i++) {
  // All iterations share the same lexical environment
  funcsVar.push(() => console.log(i));
}

funcsVar.forEach(f => f()); // 3, 3, 3 — all reference the same 'i'

// let: NEW lexical environment per iteration
const funcsLet: (() => void)[] = [];

for (let i = 0; i < 3; i++) {
  // Each iteration gets its OWN lexical environment
  // with a new binding for 'i'
  funcsLet.push(() => console.log(i));
}

funcsLet.forEach(f => f()); // 0, 1, 2 — each closure captures its own 'i'

// Under the hood, this is equivalent to:
for (let i = 0; i < 3; i++) {
  let _i = i;  // Implicit per-iteration binding
  funcsLet.push(() => console.log(_i));
}
```

### Lexical Environment in Try/Catch

```typescript
// Each catch clause creates its own lexical environment
try {
  throw new Error('Oops');
} catch (err) {
  // err is block-scoped to this catch environment
  const message = err.message;
  console.log(message);
}

// console.log(err); // ReferenceError — err is out of scope

// ES2019: Optional catch binding (no environment variable needed)
try {
  JSON.parse('invalid');
} catch {
  // No err binding created — no lexical environment overhead
  console.log('Parse failed');
}
```

### Module Lexical Environment

```typescript
// module.ts — each module has its own lexical environment
export const exportedVar = 'visible outside';
const privateVar = 'module-scoped only'; // Not visible outside module

// The module's lexical environment is the top-level scope
// Its [[OuterEnv]] = global environment

export function getPrivateVar(): string {
  return privateVar; // Resolved via module's environment
}
```

### Debugging Lexical Environments

```typescript
function debugScope() {
  const a = 1;
  let b = 2;

  function inner() {
    const c = 3;

    // Set breakpoint here and inspect in DevTools
    // You can see the Scope panel showing:
    // - Local: { c: 3 }
    // - Closure (debugScope): { a: 1, b: 2 }
    // - Global: { ... }
    console.log(a + b + c);
  }

  return inner;
}

const fn = debugScope();
fn();
```

## Real-World Use Cases

### 1. Module Pattern with Private State

```typescript
// Each module instance has its own lexical environment
function createModule() {
  // Private state — only accessible within this environment
  const privateState = new Map<string, unknown>();

  return {
    set(key: string, value: unknown): void {
      privateState.set(key, value);
    },
    get(key: string): unknown {
      return privateState.get(key);
    },
    has(key: string): boolean {
      return privateState.has(key);
    },
  };
}

const moduleA = createModule();
moduleA.set('token', 'abc123');
// privateState is NOT accessible here — only via the returned methods
```

### 2. Event Handler with Correct Scope

```typescript
function setupButton(buttonId: string, message: string) {
  const button = document.getElementById(buttonId);

  button?.addEventListener('click', function() {
    // This function's [[OuterEnv]] captures:
    // - buttonId from setupButton's environment
    // - message from setupButton's environment
    console.log(`Button ${buttonId} clicked: ${message}`);
  });
}

// Each call creates a separate lexical environment
setupButton('btn1', 'First');
setupButton('btn2', 'Second');
```

### 3. Memoization via Closures

```typescript
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  // Cache lives in the lexical environment
  const cache = new Map<string, ReturnType<T>>();

  return function(this: any, ...args: Parameters<T>) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      return cache.get(key)!;
    }

    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  } as T;
}

const expensiveFn = memoize((n: number) => {
  console.log('Computing...');
  return n * 2;
});

expensiveFn(5); // Computing... → 10
expensiveFn(5); // Cache hit → 10 (no "Computing..." log)
```

## Common Mistakes

### 1. Confusing Lexical Scope with Dynamic Scope

```typescript
// ❌ WRONG: Expecting dynamic scope (how 'this' works)
const obj = {
  name: 'My Object',
  getName: () => {
    // Arrow function captures lexical 'this', not caller's 'this'
    return this.name; // 'this' is lexical (from surrounding scope)
  }
};

// ✅ CORRECT: Understanding lexical vs dynamic
const obj2 = {
  name: 'My Object',
  getName() {
    // Regular function: 'this' is dynamic (depends on caller)
    return this.name;
  }
};

console.log(obj.getName());   // undefined (lexical this)
console.log(obj2.getName());  // "My Object" (dynamic this)
```

### 2. Assuming Block Scope for `var`

```typescript
// ❌ BAD: var ignores block lexical environments
if (true) {
  var leaked = 'I escape!';
  let scoped = 'I stay here';
}
console.log(leaked);  // "I escape!" — var ignores block scope
// console.log(scoped); // ReferenceError

// ✅ GOOD: Use let/const for block scoping
if (true) {
  let safe = 'Block scoped';
  const alsoSafe = 'Also block scoped';
}
```

### 3. Forgetting Each Call Creates a New Environment

```typescript
// ❌ BAD: Assuming shared state
function makeCounter() {
  let count = 0; // New environment each call
  return () => ++count;
}

const c1 = makeCounter();
const c2 = makeCounter();

console.log(c1()); // 1
console.log(c1()); // 2
console.log(c2()); // 1 — separate environment!
```

## Best Practices

1. **Use `let` and `const` over `var`** — they respect block-level lexical environments

2. **Prefer `const` by default** — use `let` only when reassignment is needed

3. **Be explicit about closures** — understand which variables are captured

4. **Use IIFEs for old-school module patterns** — creates a private lexical environment

5. **Avoid deep nesting** — excessive scope chain depth can impact readability

6. **Prefer passing parameters** over relying on scope chain for large functions

7. **Use arrow functions for lexical `this`** — they capture `this` from the enclosing lexical environment

## Performance Considerations

- **Environment lookup costs**: Variable resolution walks the scope chain; deeper nesting = more lookups
- **Environment lifetime**: Closures keep their outer environment alive, preventing GC
- **Environment creation**: Each function call and block creates new environments; hot paths may create many
- **Optimization**: V8 optimizes scope chain access for commonly used variables
- **Memory**: Closures that capture large scopes can cause memory pressure
- **Debugging**: Deeply nested environments are harder to debug in DevTools

## Summary

Lexical environments are the internal mechanism that implements JavaScript's scoping rules. They consist of an environment record (storing variable bindings) and a reference to an outer environment (forming the scope chain). Understanding lexical environments is essential for mastering closures, hoisting, block scoping, and the module pattern.

## Cheat Sheet

```text
LEXICAL ENVIRONMENT
═══════════════════════════════════════

STRUCTURE:
• Environment Record → stores variable/function bindings
  - Declarative: let, const, function declarations
  - Object: var, global bindings
• Outer Reference → points to parent environment (scope chain)
• null → global environment has no outer reference

SCOPE CHAIN RESOLUTION:
1. Check own environment record
2. If not found → check outer environment
3. Repeat until global environment
4. If not found → ReferenceError

CREATION:
• Global environment → program starts
• Function environment → each function call
• Block environment → blocks with let/const (if, for, while, switch)
• Module environment → each module file

LIFETIME:
• Environments are garbage collected when no longer referenced
• Closures keep their outer environment alive
• Per-iteration environments for let/const in loops

KEY FACTS:
• var → function-scoped (ignores blocks)
• let/const → block-scoped (respects blocks)
• Arrow functions → lexical 'this' (from surrounding env)
• Regular functions → dynamic 'this' (from caller)
• Each function call gets its own environment
• Modules have their own top-level environment

```

---

## See Also
- [Closures](04-Closures.md)
- [Execution Context](01-Execution-Context.md)
- [Hoisting](03-Hoisting.md)
- [Scope](05-Scope.md)

## References & Learn More

- [ECMAScript Spec: Lexical Environments](https://tc39.es/ecma262/#sec-lexical-environments)
- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- [JavaScript.info: Variable scope, closures](https://javascript.info/closure)
- [You Don't Know JS: Scope & Closures](https://github.com/getify/You-Dont-Know-JS/tree/2nd-ed/scope-closures)
