---
section: JavaScript
category: Core
tags: [concept]
---

# Async/Await

## Definition

**Async/Await** is syntactic sugar over Promises that makes asynchronous code look and feel synchronous. An `async` function always returns a Promise, and `await` pauses execution until a Promise settles, making asynchronous code more readable and maintainable.

## Why Do We Need It?

- **Readability**: Asynchronous code looks like synchronous code
- **Error Handling**: Use familiar try/catch blocks
- **Debugging**: Easier to step through asynchronous code
- **Maintenance**: Flatter code structure, easier to understand
- **Modern JavaScript**: Standard way to handle async operations

## How It Works

### Async/Await Basics

```text
┌─────────────────────────────────────────────────────────────┐
│                  ASYNC/AWAIT BASICS                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ASYNC FUNCTION:                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  async function fetchData() {                       │    │
│  │    return 'Hello';  // Automatically wrapped        │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  // Always returns a Promise                       │    │
│  │  fetchData().then(console.log);  // 'Hello'        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  AWAIT EXPRESSION:                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  async function fetchData() {                       │    │
│  │    const response = await fetch('/api/data');       │    │
│  │    const data = await response.json();              │    │
│  │    return data;                                     │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  // await pauses execution until Promise settles   │    │
│  │  // Returns the resolved value                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  EXECUTION FLOW:                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  async function example() {                        │    │
│  │    console.log('1');  // Runs synchronously        │    │
│  │    await Promise.resolve();                        │    │
│  │    console.log('2');  // Runs after await          │    │
│  │  }                                                  │    │
│  │                                                      │    │
│  │  console.log('Start');                             │    │
│  │  example();                                        │    │
│  │  console.log('End');                               │    │
│  │                                                      │    │
│  │  // Output: Start, 1, End, 2                      │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

### Async/Await vs Promises

```text
┌─────────────────────────────────────────────────────────────┐
│              ASYNC/AWAIT vs PROMISES                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PROMISE CHAIN:                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  function fetchData() {                            │    │
│  │    return fetch('/api/data')                       │    │
│  │      .then(response => response.json())            │    │
│  │      .then(data => processData(data))              │    │
│  │      .then(processed => saveData(processed))       │    │
│  │      .catch(error => handleError(error));          │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ASYNC/AWAIT:                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  async function fetchData() {                       │    │
│  │    try {                                            │    │
│  │      const response = await fetch('/api/data');    │    │
│  │      const data = await response.json();           │    │
│  │      const processed = await processData(data);    │    │
│  │      await saveData(processed);                    │    │
│  │      return processed;                             │    │
│  │    } catch (error) {                               │    │
│  │      handleError(error);                           │    │
│  │    }                                                │    │
│  │  }                                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  COMPARISON:                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Feature      │ Promise Chain │ Async/Await        │    │
│  │  ─────────────┼───────────────┼───────────────────  │    │
│  │  Readability  │ Good          │ Better              │    │
│  │  Error Handle │ .catch()      │ try/catch           │    │
│  │  Debugging    │ Harder        │ Easier              │    │
│  │  Debugging    │ Harder        │ Easier              │    │
│  │  Control Flow │ Complex       │ Simple              │    │
│  │  Composition  │ Promise.all   │ Parallel awaits     │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Basic Async/Await

```typescript
async function getUser(id: number): Promise<{ id: number; name: string }> {
  const response = await fetch(`/api/users/${id}`);
  const user = await response.json();
  return user;
}

// Usage
async function main() {
  try {
    const user = await getUser(1);
    console.log(user);
  } catch (error) {
    console.error(error);
  }
}

```

### Sequential Operations

```typescript
async function processData() {
  const data = await fetchData();           // Wait for data
  const processed = await processRawData(data);  // Wait for processing
  const saved = await saveToDatabase(processed);  // Wait for save
  return saved;
}

```

### Parallel Operations

```typescript
async function loadDashboard() {
  // Sequential (slower)
  // const user = await fetchUser();
  // const posts = await fetchPosts();
  // const notifications = await fetchNotifications();

  // Parallel (faster)
  const [user, posts, notifications] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchNotifications()
  ]);

  return { user, posts, notifications };
}

```

### Error Handling

```typescript
async function riskyOperation() {
  try {
    const result = await fetch('/api/risky');
    if (!result.ok) {
      throw new Error(`HTTP error! status: ${result.status}`);
    }
    return await result.json();
  } catch (error) {
    // Handle error
    console.error('Operation failed:', error);
    throw error;  // Re-throw if needed
  } finally {
    // Cleanup regardless of success/failure
    console.log('Operation completed');
  }
}

```

### Async Iteration

```typescript
async function processItems(items: any[]) {
  for (const item of items) {
    await processItem(item);  // Sequential processing
  }
}

async function processItemsParallel(items: any[]) {
  await Promise.all(items.map(item => processItem(item)));  // Parallel
}

// Async generators
async function* asyncGenerator() {
  let i = 0;
  while (true) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    yield i++;
  }
}

async function useAsyncGenerator() {
  for await (const value of asyncGenerator()) {
    console.log(value);
    if (value > 5) break;
  }
}

```

### Real-World Patterns

```typescript
// Retry pattern
async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  delay: number = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) {
        throw error;
      }
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Max attempts reached');
}

// Timeout pattern
async function withTimeout<T>(
  promise: Promise<T>,
  ms: number
): Promise<T> {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Timeout')), ms);
  });

  return Promise.race([promise, timeout]);
}

// Cancellation pattern
function createCancellable<T>(promise: Promise<T>) {
  let cancelled = false;

  const wrappedPromise = new Promise<T>((resolve, reject) => {
    promise
      .then(value => {
        if (!cancelled) resolve(value);
      })
      .catch(error => {
        if (!cancelled) reject(error);
      });
  });

  return {
    promise: wrappedPromise,
    cancel: () => { cancelled = true; }
  };
}

```

## Real-World Use Cases

### 1. API Calls

```typescript
async function fetchUserData(userId: string) {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

async function updateUserProfile(userId: string, data: Partial<User>) {
  const response = await fetch(`/api/users/${userId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

```

### 2. File Operations (Node.js)

```typescript
import { readFile, writeFile } from 'fs/promises';

async function processFile(inputPath: string, outputPath: string) {
  const data = await readFile(inputPath, 'utf-8');
  const processed = processData(data);
  await writeFile(outputPath, processed, 'utf-8');
}

async function readMultipleFiles(paths: string[]) {
  const contents = await Promise.all(
    paths.map(path => readFile(path, 'utf-8'))
  );
  return contents;
}

```

### 3. Database Operations

```typescript
async function createOrder(userId: string, items: OrderItem[]) {
  const user = await db.users.findById(userId);

  if (!user) {
    throw new Error('User not found');
  }

  const order = await db.orders.create({
    userId,
    items,
    total: calculateTotal(items)
  });

  await db.inventory.decrementStock(items);
  await sendConfirmationEmail(user.email, order);

  return order;
}

```

### 4. React Component

```typescript
import { useState, useEffect } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchUser() {
      try {
        const data = await fetchUserData(userId);
        setUser(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  return <div>{user?.name}</div>;
}

```

### 5. Middleware Pattern

```typescript
type Middleware = (ctx: Context, next: () => Promise<void>) => Promise<void>;

async function compose(middlewares: Middleware[], ctx: Context) {
  async function dispatch(index: number): Promise<void> {
    if (index >= middlewares.length) return;

    const middleware = middlewares[index];
    await middleware(ctx, () => dispatch(index + 1));
  }

  await dispatch(0);
}

// Usage
const authMiddleware: Middleware = async (ctx, next) => {
  const token = ctx.request.headers.authorization;

  if (!token) {
    throw new Error('Unauthorized');
  }

  ctx.user = verifyToken(token);
  await next();
};

```

## Common Mistakes

### 1. Not Awaiting Promises

```typescript
// Bad: Not awaiting
async function getData() {
  const promise = fetch('/api/data');  // Missing await!
  const data = promise.json();  // Error: promise is Promise
  return data;
}

// Good: Proper await
async function getData() {
  const response = await fetch('/api/data');
  const data = await response.json();
  return data;
}

```

### 2. Unnecessary Sequential Operations

```typescript
// Bad: Sequential when parallel is better
async function loadDashboard() {
  const user = await fetchUser();  // Wait...
  const posts = await fetchPosts();  // Wait...
  const notifications = await fetchNotifications();  // Wait...
  return { user, posts, notifications };
}

// Good: Parallel operations
async function loadDashboard() {
  const [user, posts, notifications] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchNotifications()
  ]);
  return { user, posts, notifications };
}

```

### 3. Missing Error Handling

```typescript
// Bad: No error handling
async function riskyOperation() {
  const response = await fetch('/api/risky');
  return await response.json();
}

// Good: Proper error handling
async function riskyOperation() {
  try {
    const response = await fetch('/api/risky');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Operation failed:', error);
    throw error;
  }
}

```

### 4. Async in Loops

```typescript
// Bad: Sequential processing
async function processItems(items: any[]) {
  for (const item of items) {
    await processItem(item);  // Waits for each item
  }
}

// Good: Parallel processing
async function processItems(items: any[]) {
  await Promise.all(items.map(item => processItem(item)));
}

// Or batched processing
async function processItemsBatched(items: any[]) {
  const batchSize = 10;
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    await Promise.all(batch.map(item => processItem(item)));
  }
}

```

## Best Practices

### 1. Use async/await for Clarity

```typescript
// Good: Clear async/await
async function processData() {
  const data = await fetchData();
  const processed = await processRawData(data);
  await saveToDatabase(processed);
  return processed;
}

```

### 2. Always Handle Errors

```typescript
// Good: Proper error handling
async function riskyOperation() {
  try {
    return await doSomethingRisky();
  } catch (error) {
    handleError(error);
    throw error;
  }
}

```

### 3. Use Promise.all for Parallel Operations

```typescript
// Good: Parallel when independent
async function loadMultipleResources() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ]);

  return { users, posts, comments };
}

```

### 4. Avoid async in Loops

```typescript
// Good: Batch processing
async function processLargeArray(items: any[]) {
  const batchSize = 100;

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    await Promise.all(batch.map(processItem));

    // Yield between batches
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

```

## Performance Considerations

### Sequential vs Parallel

```typescript
// Sequential: Total time = sum of all times
async function sequential() {
  const a = await fetchA();  // 1 second
  const b = await fetchB();  // 1 second
  const c = await fetchC();  // 1 second
  return { a, b, c };  // Total: 3 seconds
}

// Parallel: Total time = max time
async function parallel() {
  const [a, b, c] = await Promise.all([
    fetchA(),  // 1 second
    fetchB(),  // 1 second
    fetchC()   // 1 second
  ]);
  return { a, b, c };  // Total: 1 second
}

```

### Memory Usage

```typescript
// Bad: Creating many promises at once
async function processAll(items: any[]) {
  const promises = items.map(item => processItem(item));
  return await Promise.all(promises);  // All promises in memory
}

// Good: Process in batches
async function processBatched(items: any[]) {
  const batchSize = 100;
  const results = [];

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map(item => processItem(item))
    );
    results.push(...batchResults);
  }

  return results;
}

```

### Error Recovery

```typescript
// Good: Graceful degradation
async function fetchWithFallback() {
  try {
    return await fetchPrimary();
  } catch (error) {
    console.warn('Primary failed, trying fallback:', error);
    try {
      return await fetchFallback();
    } catch (fallbackError) {
      console.error('Fallback also failed:', fallbackError);
      return getDefaultData();
    }
  }
}

```

## Summary

Async/await is the modern way to handle asynchronous JavaScript:

1. **Syntax sugar**: Makes async code look synchronous

2. **Readability**: Easier to understand and maintain

3. **Error handling**: Familiar try/catch blocks

4. **Performance**: Use Promise.all for parallel operations

5. **Best practices**: Handle errors, avoid sequential when parallel is better

6. **Debugging**: Easier than Promise chains

7. **Patterns**: Retry, timeout, cancellation

Understanding async/await is essential for modern JavaScript development.

## Cheat Sheet
```text
ASYNC/AWAIT CHEAT SHEET
═══════════════════════════════════════════════════════════════

BASICS:
async function fetchData() {
  const result = await somePromise();
  return result;
}

• async: Function returns Promise
• await: Pauses until Promise settles
• Returns resolved value or throws error

ERROR HANDLING:
async function risky() {
  try {
    const result = await doSomething();
    return result;
  } catch (error) {
    handleError(error);
  } finally {
    cleanup();
  }
}

PARALLEL OPERATIONS:
const [a, b, c] = await Promise.all([
  fetchA(),
  fetchB(),
  fetchC()
]);

SEQUENTIAL OPERATIONS:
const a = await fetchA();
const b = await fetchB(a);
const c = await fetchC(b);

ASYNC GENERATORS:
async function* gen() {
  while (true) {
    yield await fetchNext();
  }
}

for await (const value of gen()) {
  console.log(value);
}

PATTERNS:

// Retry
async function retry(fn, attempts) {
  for (let i = 0; i < attempts; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === attempts - 1) throw error;
      await delay(1000 * i);
    }
  }
}

// Timeout
async function withTimeout(promise, ms) {
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), ms)
  );
  return Promise.race([promise, timeout]);
}

BEST PRACTICES:
• Always handle errors
• Use Promise.all for parallel
• Avoid sequential when parallel is better
• Use TypeScript for type safety
• Implement cancellation patterns
• Monitor unhandled rejections

COMMON MISTAKES:
• Not awaiting promises
• Sequential when parallel is better
• Missing error handling
• Async in loops

PERFORMANCE:
• Promise.all > sequential awaits
• Batch large operations
• Yield between batches
• Use async generators for streams

DEBUGGING:
• Chrome DevTools async traces
• console.trace() in catch
• Logging at key points
• Promise.allSettled() for visibility

```

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/)
- [Node.js](../05-NodeJS/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [MDN: async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [MDN: await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)
- [JavaScript.info: Async/Await](https://javascript.info/async-await)
- [V8 Blog: Top-level await](https://v8.dev/features/top-level-await)
- [FreeCodeCamp: Async/Await Explained](https://www.freecodecamp.org/news/learn-async-await-in-20-minutes/)
