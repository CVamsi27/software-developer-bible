# Currying & Function Composition

[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

Currying transforms a function with multiple arguments into a sequence of nested functions, each taking a single argument. Function composition combines multiple functions to produce a new function that applies them in sequence.

## Definition

**Currying** is the process of converting a function that takes multiple arguments into a chain of functions that each take a single argument and return the next function (or the result for the final argument).

**Partial Application** is related but distinct: it fixes a number of arguments to a function, producing a smaller-arity function. Currying always produces unary (single-argument) functions; partial application can produce functions of any arity.

**Function Composition** is combining two or more functions to produce a new function. Given `f(x)` and `g(x)`, composition `f ∘ g` means `f(g(x))`.

## Why Do We Need It?

- **Reusability**: Create specialized functions from general ones
- **Readability**: Chain transformations in a clear data-flow direction
- **Avoid repetition**: Pre-fill common arguments for specific contexts
- **Point-free style**: Write functions without explicitly naming arguments
- **Pipelines**: Model data processing as sequential transformations

## How It Works

Currying relies on closures: each nested function captures the arguments provided so far via the closure scope.

```
add(1, 2, 3)              → 6
curriedAdd(1)(2)(3)       → 6
curriedAdd(1)             → (b) => (c) => a + b + c
```

Function composition chains the output of one function as the input to the next.

```
compose(f, g)(x)          → f(g(x))
pipe(f, g)(x)             → g(f(x))   (reverse order)
```

## Code Examples (JavaScript)

### Manual Currying

```javascript
// Normal function
function add(a, b, c) {
  return a + b + c;
}

// Manually curried
function curriedAdd(a) {
  return function(b) {
    return function(c) {
      return a + b + c;
    };
  };
}

curriedAdd(1)(2)(3); // 6
```

### Currying with Arrow Functions

```javascript
const curriedAdd = (a) => (b) => (c) => a + b + c;
curriedAdd(1)(2)(3); // 6
```

### Generic Curry Function

```javascript
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function(...nextArgs) {
      return curried.apply(this, args.concat(nextArgs));
    };
  };
}

const sum = (a, b, c) => a + b + c;
const curriedSum = curry(sum);
curriedSum(1)(2)(3);  // 6
curriedSum(1, 2)(3);  // 6
curriedSum(1)(2, 3);  // 6
```

### Currying with Placeholders

```javascript
function curryWithPlaceholders(fn) {
  const _ = curryWithPlaceholders._;

  return function curried(...args) {
    const placeholders = args.filter(a => a === _);
    if (args.length >= fn.length && placeholders.length === 0) {
      return fn(...args);
    }
    return function(...nextArgs) {
      const merged = args.map(a => a === _ && nextArgs.length ? nextArgs.shift() : a);
      return curried(...merged, ...nextArgs);
    };
  };
}

curryWithPlaceholders._ = Symbol('placeholder');

const greet = (greeting, name, punctuation) =>
  `${greeting}, ${name}${punctuation}`;

const curriedGreet = curryWithPlaceholders(greet);
curriedGreet('Hello', _, '!')('World'); // "Hello, World!"
```

### Function Composition (Right-to-Left)

```javascript
function compose(...fns) {
  return function(initialValue) {
    return fns.reduceRight((acc, fn) => fn(acc), initialValue);
  };
}

const toUpper = (s) => s.toUpperCase();
const exclaim = (s) => s + '!';
const repeat = (s) => s + ' ' + s;

const shout = compose(exclaim, toUpper, repeat);
shout('hello'); // "HELLO HELLO!"
```

### Function Piping (Left-to-Right)

```javascript
function pipe(...fns) {
  return function(initialValue) {
    return fns.reduce((acc, fn) => fn(acc), initialValue);
  };
}

const process = pipe(
  (s) => s.trim(),
  (s) => s.toLowerCase(),
  (s) => s.split(' '),
  (arr) => arr.filter(w => w.length > 3)
);

process('  Hello World JavaScript  '); // ['hello', 'world', 'javascript']
```

### Real-World Examples

```javascript
// URL parameter builder with currying
const buildUrl = (base) => (path) => (params) => {
  const query = Object.entries(params)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&');
  return `${base}${path}?${query}`;
};

const apiUrl = buildUrl('https://api.example.com');
const usersUrl = apiUrl('/users');
usersUrl({ page: 1, limit: 10 });
// "https://api.example.com/users?page=1&limit=10"

// Data processing pipeline with composition
const fetchData = (url) => fetch(url).then(r => r.json());
const filterActive = (items) => items.filter(i => i.active);
const sortByName = (items) => [...items].sort((a, b) => a.name.localeCompare(b.name));
const takeFirst = (n) => (items) => items.slice(0, n);

const getTopActiveUsers = pipe(
  fetchData,
  filterActive,
  sortByName,
  takeFirst(10)
);

// Logger with partial application
const log = (level) => (message) => console.log(`[${level.toUpperCase()}] ${message}`);
const info = log('info');
const warn = log('warn');
const error = log('error');

info('System started');  // [INFO] System started
warn('Low memory');      // [WARN] Low memory
error('Crash detected'); // [ERROR] Crash detected
```

## Real-World Case Studies

### Redux Middleware (Curried Pattern)

Redux middleware uses curried triple-nested functions:

```javascript
const loggerMiddleware = (store) => (next) => (action) => {
  console.log('dispatching', action);
  const result = next(action);
  console.log('next state', store.getState());
  return result;
};
```

Each curried layer serves a purpose: `store` is provided once during setup, `next` per middleware chain, `action` per dispatch.

### Express Route Validation (Composition)

```javascript
const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body);
  return error ? res.status(400).json({ error }) : next();
};

const authorize = (role) => (req, res, next) => {
  return req.user?.role !== role
    ? res.status(403).json({ error: 'Forbidden' })
    : next();
};

// Compose middleware
const createUser = pipe(
  validate(userSchema),
  authorize('admin'),
  (req, res) => User.create(req.body)
);
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Confusing currying with partial application | Currying always produces unary functions in sequence; partial application can fix any number of args |
| Over-currying simple functions | Only curry when you need reusable intermediate functions; don't curry one-off calls |
| Incorrect argument order in composition | `compose(f, g)` applies `g` first, then `f` — read right-to-left; `pipe` goes left-to-right |
| Mutating arguments in piped functions | Each function should be pure; avoid side effects that break the pipeline |
| Creating deeply nested curried functions manually | Use a generic `curry()` helper instead of hand-writing nested arrow functions |

## Best Practices

1. **Use a generic `curry()` utility** from libraries like Lodash or Ramda instead of manual nesting
2. **Prefer `pipe` over `compose`** for readability in left-to-right languages
3. **Keep composed functions small and single-purpose** — each function should do one thing
4. **Use currying for configuration** — separate setup (one-time) from execution (repeated)
5. **Avoid over-abstracting** — currying adds indirection; only use it when it improves clarity

## Performance Considerations

- **Each curried call creates a closure** — minimal overhead for most use cases
- **Deep currying (5+ levels)** can impact readability and stack traces
- **Composition with many functions** may increase call stack depth; consider `reduce`-based pipe implementations
- **Library curry implementations** (Lodash, Ramda) handle edge cases (placeholders, arity detection) more efficiently than manual versions

## Summary

Currying transforms multi-argument functions into sequences of unary functions, enabling partial application and cleaner composition. Function composition chains functions together to build data-processing pipelines. Together, they enable a declarative, functional programming style that improves code reuse, testability, and readability.

## Cheat Sheet

| Concept | Syntax | Example |
|---------|--------|---------|
| Curried add | `(a) => (b) => (c) => a + b + c` | `add(1)(2)(3)` → `6` |
| Generic curry | `const curry = (fn) => ...` | `curry(sum)(1)(2)(3)` |
| Compose (R→L) | `compose(f, g)(x)` ≡ `f(g(x))` | `compose(toUpper, trim)(' hello ')` |
| Pipe (L→R) | `pipe(f, g)(x)` ≡ `g(f(x))` | `pipe(trim, toUpper)(' hello ')` |
| Lodash curry | `_.curry(fn)` | `_.curry(sum)(1)(2)(3)` |
| Ramda compose | `R.compose(f, g)` | `R.compose(R.toUpper, R.trim)` |

## See Also
- [Closures](04-Closures.md)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- [MDN: Currying](https://developer.mozilla.org/en-US/docs/Glossary/Currying)
- [JavaScript Functional Programming Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions#function_composition)
- [Lodash Curry Docs](https://lodash.com/docs/4.17.15#curry)
- [Ramda Composition Guide](https://ramdajs.com/docs/#compose)
