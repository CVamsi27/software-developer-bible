---
section: JavaScript
category: Core
tags: [concept]
---

# Error Handling

## Definition

**Error handling** is the process of anticipating, detecting, and responding to exceptional conditions that occur during program execution. In JavaScript, errors are represented by `Error` objects and can be caught and managed using `try/catch/finally` blocks, propagated via the call stack, or handled asynchronously through Promise rejection handlers. Proper error handling distinguishes robust, production-ready code from fragile scripts.

## Why Do We Need It?

1. **Graceful Degradation**: Prevents complete application crashes when unexpected conditions occur

2. **User Experience**: Provides meaningful feedback instead of silent failures or cryptic errors

3. **Debugging**: Structured error objects contain stack traces for diagnosing issues

4. **Data Integrity**: Prevents corrupt state by handling failures in transactions

5. **Security**: Prevents sensitive information leakage through unhandled exceptions

6. **Observability**: Structured errors enable monitoring and alerting in production

## How It Works

### Error Propagation

```text
CALL STACK ERROR PROPAGATION:

function a() {
  throw new Error('Failed in a');
}

function b() { a(); }
function c() { b(); }

try {
  c();
} catch (err) {
  // Error propagates: a → b → c → catch
  console.log(err.message); // "Failed in a"
  console.log(err.stack);   // Full stack trace
}

┌─────────────────────────────────────────┐
│  Call Stack when error is thrown:       │
│                                         │
│  a()  ← error thrown here              │
│  b()  ← stack unwinds through here     │
│  c()  ← stack unwinds through here     │
│  try/catch  ← caught here              │
└─────────────────────────────────────────┘
```

### The Error Object

```typescript
// Built-in error types
new Error('message');           // Generic error
new SyntaxError('message');     // Syntax parsing error
new TypeError('message');       // Wrong type encountered
new ReferenceError('message');  // Invalid reference
new RangeError('message');      // Value out of range
new URIError('message');        // URI handling error
new EvalError('message');       // eval() error (rare)

// Error object properties
const err = new Error('Something went wrong');
console.log(err.message);   // "Something went wrong"
console.log(err.name);      // "Error"
console.log(err.stack);     // Stack trace (non-standard but widely supported)
console.log(err.cause);     // Optional chained error (ES2022)
```

## Code Examples

### Basic try/catch/finally

```typescript
function parseJSON(jsonString: string): unknown {
  try {
    const result = JSON.parse(jsonString);
    return result;
  } catch (error) {
    // Handle the error
    console.error('Failed to parse JSON:', error);
    return null;
  } finally {
    // Always executes, even if catch re-throws
    console.log('Parse attempt completed');
  }
}

console.log(parseJSON('{"name": "Alice"}')); // { name: 'Alice' }
console.log(parseJSON('invalid json'));       // null (no crash)
```

### Custom Error Classes

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    options?: ErrorOptions
  ) {
    super(message, options);
    this.name = 'AppError';
  }
}

class ValidationError extends AppError {
  constructor(
    message: string,
    public readonly field: string
  ) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id '${id}' not found`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

// Usage
function findUser(id: string): never {
  throw new NotFoundError('User', id);
}

try {
  findUser('invalid-id');
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log(`404: ${error.message}`); // 404: User with id 'invalid-id' not found
  } else if (error instanceof ValidationError) {
    console.log(`400: ${error.message}`);
  } else if (error instanceof AppError) {
    console.log(`${error.statusCode}: ${error.message}`);
  }
}
```

### Error Handling with Type Narrowing

```typescript
function handleError(error: unknown): string {
  // Unknown type forces proper narrowing
  if (error instanceof Error) {
    return `Error: ${error.message}`;
  }

  if (typeof error === 'string') {
    return `String error: ${error}`;
  }

  if (typeof error === 'object' && error !== null && 'message' in error) {
    return `Object error: ${(error as { message: string }).message}`;
  }

  return `Unknown error: ${String(error)}`;
}

// Usage
try {
  throw { code: 500, message: 'Server fault' };
} catch (error) {
  console.log(handleError(error)); // "Object error: Server fault"
}
```

### Async Error Handling

```typescript
// async/await with try/catch
async function fetchUserData(userId: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${userId}`);

    if (!response.ok) {
      throw new AppError(
        `HTTP ${response.status}: ${response.statusText}`,
        'HTTP_ERROR',
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    // Handle network errors and HTTP errors
    if (error instanceof TypeError) {
      // Network error (fetch only rejects on network failures)
      throw new AppError('Network request failed', 'NETWORK_ERROR', 503);
    }
    throw error; // Re-throw HTTP errors
  }
}

// Promise-based error handling
function fetchWithTimeout(url: string, timeout = 5000): Promise<Response> {
  return Promise.race([
    fetch(url),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new AppError('Request timeout', 'TIMEOUT', 408)), timeout)
    ),
  ]);
}
```

### Error Boundary Pattern (try/catch at Boundaries)

```typescript
// At system boundaries — always catch errors
class ApiService {
  async get<T>(path: string): Promise<Result<T>> {
    try {
      const response = await fetch(path);
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return {
        success: false,
        error: error instanceof AppError
          ? error
          : new AppError('Unexpected API error', 'UNKNOWN'),
      };
    }
  }
}

// Result type pattern (Rust-inspired)
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: AppError };

// Usage — no try/catch needed at call site!
const result = await apiService.get<User[]>('/api/users');

if (result.success) {
  console.log(result.data.length, 'users found');
} else {
  console.error('Failed:', result.error.message);
}
```

### Global Error Handlers

```typescript
// Browser: Unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
  event.preventDefault(); // Prevent default console warning
});

// Browser: Uncaught exceptions
window.onerror = (message, source, lineno, colno, error) => {
  console.error('Global error:', { message, source, lineno, error });
  // Send to error tracking service (Sentry, etc.)
  return true; // Prevent default browser handling
};

// Node.js: Unhandled rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Node.js: Uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Perform cleanup
  // Then exit — the process is in an unknown state
  process.exit(1);
});
```

## Real-World Use Cases

### 1. Form Validation

```typescript
class FormValidationError extends AppError {
  constructor(
    message: string,
    public readonly errors: Record<string, string[]>
  ) {
    super(message, 'FORM_VALIDATION', 422);
  }
}

function validateForm(data: Record<string, unknown>): void {
  const errors: Record<string, string[]> = {};

  if (!data.email || typeof data.email !== 'string') {
    errors.email = ['Email is required'];
  } else if (!data.email.includes('@')) {
    errors.email = ['Invalid email format'];
  }

  if (!data.password || String(data.password).length < 8) {
    errors.password = ['Password must be at least 8 characters'];
  }

  if (Object.keys(errors).length > 0) {
    throw new FormValidationError('Validation failed', errors);
  }
}
```

### 2. Retry with Exponential Backoff

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: { maxRetries?: number; baseDelay?: number } = {}
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000 } = options;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;

      // Don't retry non-retryable errors
      if (error instanceof AppError && error.statusCode === 400) {
        throw error;
      }

      // Exponential backoff with jitter
      const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Unreachable');
}
```

## Common Mistakes

### 1. Catching and Swallowing

```typescript
// ❌ BAD: Silent catch — hides bugs
try {
  await processData();
} catch (error) {
  // Does nothing — bugs are hidden!
}

// ✅ GOOD: At minimum, log the error
try {
  await processData();
} catch (error) {
  console.error('processData failed:', error);
  throw error; // Or handle appropriately
}
```

### 2. Using `throw` with Non-Errors

```typescript
// ❌ BAD: Throwing non-Error objects
throw 'Something went wrong';
throw 404;
throw { message: 'Custom error' };

// ✅ GOOD: Always throw Error instances
throw new Error('Something went wrong');
throw new AppError('Not found', 'NOT_FOUND', 404);
```

### 3. Not Distinguishing Error Types

```typescript
// ❌ BAD: Generic catch for all errors
try {
  await apiCall();
} catch (error) {
  showError('Something went wrong'); // Same message for all errors
}

// ✅ GOOD: Handle different errors differently
try {
  await apiCall();
} catch (error) {
  if (error instanceof ValidationError) {
    showFieldErrors(error.errors);
  } else if (error instanceof NotFoundError) {
    showNotFound();
  } else {
    showGenericError();
  }
}
```

## Best Practices

1. **Always throw Error instances** — not strings or plain objects. Errors provide stack traces.

2. **Use custom error classes** — extend `Error` with domain-specific properties.

3. **Catch at boundaries** — catch errors at module/API boundaries, not deep inside logic.

4. **Don't swallow errors** — at minimum log them; re-throw if you can't handle them.

5. **Use the `cause` property** (ES2022) to chain related errors.

6. **Type narrowing for `unknown`** — in TypeScript, `catch(error)` gives you `unknown`; narrow it.

7. **Async error handling** — always wrap async function bodies in try/catch.

8. **Global handlers** — set up `unhandledrejection` and `onerror` for safety net.

9. **Result types** — consider using discriminated unions for expected failures.

10. **Don't over-catch** — allow errors to propagate to appropriate handlers.

## Performance Considerations

- **try/catch is cheap** — negligible overhead when no error is thrown
- **Throwing is expensive** — stack trace generation is costly; don't use exceptions for control flow
- **Error stack traces** — capture call stack at creation time; this has a cost
- **Nested try/catch** — minimal overhead, but readability suffers
- **Promise rejection handling** — .catch() is preferred over try/catch in promise chains for performance

## Summary

Error handling in JavaScript is built on `try/catch/finally` blocks with a hierarchy of built-in Error types. Key practices include extending Error for domain-specific errors, catching at system boundaries, always logging errors, and never using exceptions for normal control flow. Proper error handling transforms fragile code into robust, production-ready applications.

## Cheat Sheet

```text
ERROR HANDLING CHEAT SHEET
═══════════════════════════════════════

BASIC SYNTAX:
try {
  // Risky code
} catch (error) {
  // Handle error
} finally {
  // Always runs
}

BUILT-IN ERROR TYPES:
• Error           → Generic error
• SyntaxError     → Invalid syntax
• TypeError       → Wrong type
• ReferenceError  → Invalid reference
• RangeError      → Value out of range
• URIError        → URI functions (encodeURI, etc.)

CUSTOM ERRORS:
class MyError extends Error {
  constructor(message) {
    super(message);
    this.name = 'MyError';
  }
}

BEST PRACTICES:
• ✓ Throw Error instances, not strings
• ✓ Catch at system boundaries
  ✓ Use instanceof for type checking
• ✓ Log all caught errors
• ✓ Use error cause for chaining (ES2022)
• ✗ Don't swallow errors silently
  ✗ Don't use exceptions for control flow
• ✗ Don't expose stack traces to users

ASYNC PATTERNS:
• async/await: try/catch blocks
• Promises: .catch() handlers
• Global: unhandledrejection event
• Node: process.on('uncaughtException')

RETRY PATTERN:
withRetry(fn, { maxRetries: 3, baseDelay: 1000 });

```

---

## See Also
- [Async/Await](11-Async-Await.md)
- [Promises](10-Promises.md)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [MDN: Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error)
- [MDN: try/catch](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
- [Node.js Error Handling Best Practices](https://www.joyent.com/node-js/production/design/errors)
- [You Don't Know JS: Async & Performance](https://github.com/getify/You-Dont-Know-JS/tree/2nd-ed/async-performance)
