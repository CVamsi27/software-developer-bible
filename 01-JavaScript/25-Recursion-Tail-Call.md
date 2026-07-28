---
section: JavaScript
category: Core
tags: [concept]
---

# Recursion & Tail Call Optimization

Recursion is a programming technique where a function calls itself to solve a problem by breaking it into smaller, identical sub-problems. Tail Call Optimization (TCO) is a compiler technique that optimizes recursive functions to prevent stack overflow.

## Definition

**Recursion** occurs when a function calls itself (directly or indirectly) to solve a problem. Every recursive solution has two essential parts:

- **Base case**: The condition under which the function stops recursing
- **Recursive case**: The call to the function itself with modified arguments

**Tail Call** is a function call that appears as the final action of a containing function — i.e., the called function's return value is immediately returned without further computation.

**Tail Call Optimization (TCO)** is an optimization where the compiler reuses the current stack frame for a tail call instead of creating a new one, preventing stack growth. This is also called Proper Tail Calls (PTC) in ECMAScript.

## Why Do We Need It?

- **Elegant solutions**: Some problems (tree traversal, divide-and-conquer) are naturally recursive
- **Readable code**: Recursive solutions often mirror the problem's mathematical definition
- **No state management**: Recursion eliminates explicit stack data structures
- **Memory efficiency (with TCO)**: Tail-recursive functions can run in constant stack space
- **Functional programming**: Recursion replaces loops in pure functional languages

## How It Works

### Call Stack in Recursion

Each recursive call pushes a new frame onto the call stack:

```
factorial(5):
  push factorial(5)     → stack: [factorial(5)]
    push factorial(4)   → stack: [factorial(5), factorial(4)]
      push factorial(3) → stack: [factorial(5), factorial(4), factorial(3)]
        ...
      pop factorial(3)  → returns 6
    pop factorial(4)    → returns 24
  pop factorial(5)      → returns 120
```

Without TCO, deep recursion causes **stack overflow**. With TCO, the stack frame is reused.

### Tail Call vs Non-Tail Call

**Non-tail (stack-growing):**
```javascript
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1); // Must multiply AFTER recursive call returns
}
```
The multiplication `n * ...` keeps the current frame alive until the recursive call returns.

**Tail-recursive (TCO-friendly):**
```javascript
function factorial(n, acc = 1) {
  if (n <= 1) return acc;
  return factorial(n - 1, n * acc); // Nothing left to do after call
}
```
The function returns the result of the recursive call directly. The engine can discard the current frame.

## Code Examples (JavaScript)

### Basic Recursion

```javascript
// Factorial
function factorial(n) {
  if (n <= 1) return 1;       // Base case
  return n * factorial(n - 1); // Recursive case
}

factorial(5); // 120

// Fibonacci
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

fibonacci(7); // 13

// Power (exponentiation)
function power(base, exp) {
  if (exp === 0) return 1;
  return base * power(base, exp - 1);
}

power(2, 10); // 1024
```

### Tail-Recursive Versions

```javascript
// Tail-recursive factorial
function factorialTail(n, acc = 1) {
  if (n <= 1) return acc;
  return factorialTail(n - 1, n * acc);
  // ← Nothing happens after this call; engine can TCO
}

factorialTail(5);    // 120
factorialTail(1000); // Safe even with large input (with TCO)

// Tail-recursive fibonacci
function fibonacciTail(n, a = 0, b = 1) {
  if (n === 0) return a;
  if (n === 1) return b;
  return fibonacciTail(n - 1, b, a + b);
}

fibonacciTail(50); // 12586269025

// Tail-recursive sum
function sumTail(n, acc = 0) {
  if (n === 0) return acc;
  return sumTail(n - 1, acc + n);
}

sumTail(100); // 5050

// Tail-recursive array flatten
function flattenTail(arr, acc = []) {
  if (arr.length === 0) return acc;
  const [first, ...rest] = arr;
  if (Array.isArray(first)) {
    return flattenTail(first.concat(rest), acc);
  }
  return flattenTail(rest, acc.concat(first));
}

flattenTail([1, [2, [3, 4]], 5]); // [1, 2, 3, 4, 5]
```

### Common Recursive Patterns

```javascript
// Array traversal (instead of loops)
function traverse(arr, i = 0) {
  if (i >= arr.length) return;
  console.log(arr[i]);
  traverse(arr, i + 1);
}

// Tree traversal
function traverseTree(node) {
  if (!node) return;
  console.log(node.value);
  node.children.forEach(traverseTree);
}

// Linked list reversal
function reverseList(node, prev = null) {
  if (!node) return prev;
  const next = node.next;
  node.next = prev;
  return reverseList(next, node);
}

// Divide and conquer: binary search
function binarySearch(arr, target, left = 0, right = arr.length - 1) {
  if (left > right) return -1;
  const mid = Math.floor((left + right) / 2);
  if (arr[mid] === target) return mid;
  if (arr[mid] > target) return binarySearch(arr, target, left, mid - 1);
  return binarySearch(arr, target, mid + 1, right);
}

// Mutual recursion: even/odd
function isEven(n) {
  if (n === 0) return true;
  return isOdd(n - 1);
}
function isOdd(n) {
  if (n === 0) return false;
  return isEven(n - 1);
}

isEven(42); // true
isOdd(42);  // false
```

### Recursion with Trampolining (TCO Fallback)

When TCO is not available (Safari is the only JS engine with full TCO), use trampolining:

```javascript
function trampoline(fn) {
  return function(...args) {
    let result = fn(...args);
    while (typeof result === 'function') {
      result = result();
    }
    return result;
  };
}

// Thunk-based recursion
function factorialThunk(n, acc = 1) {
  if (n <= 1) return acc;
  return () => factorialThunk(n - 1, n * acc);
  // Returns a thunk instead of making a direct recursive call
}

const safeFactorial = trampoline(factorialThunk);
safeFactorial(100000); // Works without stack overflow!
```

### Memoized Recursion

```javascript
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

// Without memoization: O(2^n)
const fibSlow = (n) => n <= 1 ? n : fibSlow(n - 1) + fibSlow(n - 2);

// With memoization: O(n)
const fibFast = memoize((n) => n <= 1 ? n : fibFast(n - 1) + fibFast(n - 2));

fibFast(100); // 354224848179262000000 (fast)
```

## Real-World Case Studies

### Recursive React Component (Tree View)

```typescript
function TreeNode({ node }) {
  return (
    <li>
      {node.label}
      {node.children && (
        <ul>
          {node.children.map(child => (
            <TreeNode key={child.id} node={child} />
          ))}
        </ul>
      )}
    </li>
  );
}
```

### Recursive Directory Tree

```javascript
const fs = require('fs');
const path = require('path');

function printTree(dir, prefix = '') {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  entries.forEach((entry, i) => {
    const isLast = i === entries.length - 1;
    console.log(`${prefix}${isLast ? '└── ' : '├── '}${entry.name}`);
    if (entry.isDirectory()) {
      printTree(
        path.join(dir, entry.name),
        `${prefix}${isLast ? '    ' : '│   '}`
      );
    }
  });
}
```

### Recursive JSON Schema Validation

```javascript
function validateSchema(data, schema) {
  if (schema.type === 'string') return typeof data === 'string';
  if (schema.type === 'number') return typeof data === 'number';

  if (schema.type === 'object') {
    if (typeof data !== 'object' || data === null) return false;
    return Object.entries(schema.properties).every(([key, propSchema]) =>
      key in data ? validateSchema(data[key], propSchema) : !schema.required?.includes(key)
    );
  }

  if (schema.type === 'array') {
    if (!Array.isArray(data)) return false;
    return data.every(item => validateSchema(item, schema.items));
  }

  return false;
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing or incorrect base case | Always identify the smallest input that should return immediately |
| Forgetting to return the recursive call | `return recursiveCall(...)` — missing `return` causes `undefined` |
| Stack overflow on large inputs | Use tail recursion with TCO, trampolining, or convert to iteration |
| Exponential time complexity (e.g., naive Fibonacci) | Add memoization or convert to iterative approach |
| Mutating shared state across recursive calls | Pass state as arguments; avoid closures that capture mutable variables |

## Best Practices

1. **Always define a base case first** — ensure it's reachable for all valid inputs
2. **Prefer tail recursion** when the problem allows it — enables TCO
3. **Use memoization** for recursive functions with overlapping subproblems
4. **Add a depth limit** for production code to prevent runaway recursion
5. **Convert to iteration** when recursion depth could exceed ~10,000 (depends on engine)
6. **Use trampolining** as a fallback when TCO is unavailable

## Performance & TCO Support

| Engine | TCO Support | Notes |
|--------|:-----------:|-------|
| Safari (JavaScriptCore) | ✅ Full | Only engine with proper TCO |
| V8 (Chrome, Node.js) | ❌ | Removed in 2017; use trampolining |
| SpiderMonkey (Firefox) | ❌ | Removed; consider it unsupported |
| Hermes (React Native) | ❌ | No support |

For production code, **do not rely on TCO**. Use trampolining or iteration for deep recursion.

## Summary

Recursion provides elegant solutions for naturally recursive problems like tree traversal, divide-and-conquer, and combinatorial search. Tail Call Optimization eliminates stack growth for tail-recursive functions, but limited engine support means fallback strategies like trampolining are often necessary. Mastering recursion — including base case design, tail recursion, memoization, and trampolining — is essential for writing clean, efficient algorithms.

## Cheat Sheet

```javascript
// Structure
function recursive(input) {
  if (/* base case */) return /* result */;
  return recursive(/* smaller input */);
}

// Tail-recursive template
function tailRecursive(input, acc = /* initial */) {
  if (/* base case */) return acc;
  return tailRecursive(/* smaller input */, /* updated acc */);
}

// Trampoline wrapper
function trampoline(fn) {
  return (...args) => {
    let r = fn(...args);
    while (typeof r === 'function') r = r();
    return r;
  };
}

// Memoization helper
const memoizedRecursive = memoize(
  (n) => n <= 1 ? n : memoizedRecursive(n - 1) + memoizedRecursive(n - 2)
);
```

---

### See Also

- [Call Stack](02-Call-Stack.md) — how recursion uses the stack
- [Closures](04-Closures.md) — how recursive closures capture scope
- [Memoization](22-Memoization.md) — optimization technique for recursion
- [Generators](23-Generators.md) — iterative alternative to recursion
- [Dynamic Programming](../19-Coding-Patterns/06-Dynamic-Programming.md) — recursion with overlapping subproblems

## References & Learn More

- [MDN: Recursion](https://developer.mozilla.org/en-US/docs/Glossary/Recursion)
- [ECMAScript Tail Call Proposal](https://github.com/tc39/proposal-ptc-syntax)
- [V8 Blog: TCO Removal](https://v8.dev/blog/modern-javascript#proper-tail-calls)
- [JavaScript Info: Recursion](https://web.archive.org/web/20240701000000/https://javascript.info/call-stack)
