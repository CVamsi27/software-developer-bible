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

```
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

```
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

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is async/await in JavaScript?**

A: Async/await is syntactic sugar over Promises that makes asynchronous code look and feel synchronous. `async` functions return Promises, and `await` pauses execution until a Promise settles.

**Q2: What does the `async` keyword do?**

A: The `async` keyword:
1. Makes the function always return a Promise
2. Allows using `await` inside the function
3. Makes the function's return value automatically wrapped in a Promise

**Q3: What does the `await` keyword do?**

A: The `await` keyword:
1. Pauses execution until a Promise settles
2. Returns the resolved value
3. Throws if the Promise is rejected
4. Can only be used inside `async` functions

**Q4: How do you handle errors with async/await?**

A: Use try/catch blocks:
```typescript
async function riskyOperation() {
  try {
    const result = await doSomething();
    return result;
  } catch (error) {
    handleError(error);
  }
}
```

**Q5: Can you use await outside of async functions?**

A: No, `await` can only be used inside `async` functions or at the top level of ES modules.

### Intermediate (5-10 questions)

**Q6: What is the difference between sequential and parallel async operations?**

A:
- **Sequential**: Each operation waits for the previous one to complete
- **Parallel**: Operations run simultaneously

```typescript
// Sequential
const a = await fetchA();
const b = await fetchB();

// Parallel
const [a, b] = await Promise.all([fetchA(), fetchB()]);
```

**Q7: How do you make multiple independent API calls in parallel?**

A: Use `Promise.all`:
```typescript
async function loadDashboard() {
  const [user, posts, notifications] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchNotifications()
  ]);
  return { user, posts, notifications };
}
```

**Q8: What is an async generator function?**

A: An async generator function uses `async function*` and `yield` to produce values asynchronously:
```typescript
async function* asyncGenerator() {
  let i = 0;
  while (true) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    yield i++;
  }
}
```

**Q9: How do you iterate over an async generator?**

A: Use `for await...of`:
```typescript
for await (const value of asyncGenerator()) {
  console.log(value);
  if (value > 5) break;
}
```

**Q10: What is the relationship between async/await and Promises?**

A: Async/await is syntactic sugar over Promises. `async` functions always return Promises, and `await` is equivalent to `.then()` but with better readability.

### Senior (10-15 questions)

**Q11: Explain the execution model of async/await.**

A:
1. `async` function runs synchronously until first `await`
2. At `await`, function is suspended and returns a Promise
3. Execution returns to the caller
4. When the awaited Promise settles, function resumes
5. Function continues until next `await` or completion

**Q12: How does async/await interact with the event loop?**

A: `await` yields control back to the event loop. Microtasks (Promise callbacks) run between synchronous code and the next macrotask. Async functions are resumed via microtasks.

**Q13: What are the performance implications of async/await?**

A:
- Sequential awaits can be slower than parallel Promises
- Each `await` creates a new Promise (memory overhead)
- Async functions have slightly more overhead than regular functions

**Q14: How do you implement cancellation with async/await?**

A:
```typescript
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

**Q15: How do you handle async operations in React?**

A:
1. `useEffect` with async functions
2. State variables for loading/error
3. Cleanup functions for cancellation
4. Custom hooks for reusable logic

### FAANG-style (5-10 questions)

**Q16: Design an async task scheduler with concurrency control.**

A:
```typescript
class AsyncTaskScheduler {
  private queue: (() => Promise<any>)[] = [];
  private running = 0;
  private maxConcurrent: number;

  constructor(maxConcurrent: number = 5) {
    this.maxConcurrent = maxConcurrent;
  }

  async add<T>(task: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          this.running++;
          resolve(await task());
        } catch (error) {
          reject(error);
        } finally {
          this.running--;
          this.processQueue();
        }
      });

      this.processQueue();
    });
  }

  private processQueue() {
    while (this.running < this.maxConcurrent && this.queue.length > 0) {
      const task = this.queue.shift()!;
      task();
    }
  }
}
```

**Q17: How would you implement async/await without using async/await?**

A:
```typescript
function asyncToGenerator<T>(fn: (...args: any[]) => Promise<T>) {
  return function(...args: any[]) {
    return new Promise((resolve, reject) => {
      const gen = fn.apply(this, args);

      function step(key: string, arg?: any) {
        let result: any;
        try {
          result = gen[key](arg);
        } catch (error) {
          return reject(error);
        }

        const { value, done } = result;

        if (done) {
          return resolve(value);
        }

        Promise.resolve(value).then(
          (val) => step('next', val),
          (err) => step('throw', err)
        );
      }

      step('next');
    });
  };
}
```

**Q18: Analyze the memory implications of async/await.**

A:
- Each `await` creates a new Promise
- Suspended functions retain local variables
- Long chains can accumulate memory
- Solution: Use `Promise.all` for parallel, batch processing

**Q19: How do you debug async/await code?**

A:
1. Chrome DevTools: Async stack traces
2. Add logging at key points
3. Use `console.trace()` to see call stack
4. Breakpoints work across `await` boundaries
5. Use `Promise.allSettled()` to see all results

**Q20: What are the security implications of async/await?**

A:
1. **Timing attacks**: Measure async operation time
2. **Resource exhaustion**: Create too many concurrent operations
3. **Information leakage**: Async errors can expose internals
4. **Mitigation**: Rate limiting, input validation, error handling

### Follow-ups (5-10 questions)

**Q21: Can you give an example of an async/await bug in production?**

A: Common bug: Missing error handling
```typescript
// Bug: Unhandled rejection
async function fetchData() {
  const response = await fetch('/api/data');
  return await response.json();
}
// If fetch fails, unhandled rejection

// Fix: Add error handling
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch data:', error);
    throw error;
  }
}
```

**Q22: How do you handle async operations in Redux?**

A:
```typescript
// Redux thunk
const fetchUser = (id: string) => async (dispatch: Dispatch) => {
  dispatch({ type: 'FETCH_USER_START' });

  try {
    const user = await fetchUserApi(id);
    dispatch({ type: 'FETCH_USER_SUCCESS', payload: user });
  } catch (error) {
    dispatch({ type: 'FETCH_USER_FAILURE', error });
  }
};
```

**Q23: What is the relationship between async/await and generators?**

A: Async/await is syntactic sugar over generators. Generators yield values, while async functions yield Promises. Browsers transpile async/await to generator code for compatibility.

**Q24: How do different frameworks handle async operations?**

A:
- **React**: useEffect, useState, custom hooks
- **Vue**: Composition API with async setup
- **Angular**: HttpClient, async pipe
- **Svelte**: onMount, reactive statements

**Q25: What are best practices for working with async/await?**

A:
1. Always handle errors with try/catch
2. Use Promise.all for parallel operations
3. Avoid unnecessary sequential awaits
4. Use TypeScript for type safety
5. Implement cancellation patterns
6. Monitor unhandled rejections
7. Use async generators for streaming data
8. Test async code thoroughly

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

```
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

## References & Learn More

- [MDN: async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [MDN: await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)
- [JavaScript.info: Async/Await](https://javascript.info/async-await)
- [V8 Blog: Top-level await](https://v8.dev/features/top-level-await)
- [FreeCodeCamp: Async/Await Explained](https://www.freecodecamp.org/news/learn-async-await-in-20-minutes/)
