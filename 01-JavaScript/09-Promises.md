# Promises

## Definition

A **Promise** is an object representing the eventual completion or failure of an asynchronous operation. It's a container for a future value that allows you to chain asynchronous operations and handle their results or errors in a clean, readable way.

## Why Do We Need It?

- **Async Operations**: Handle asynchronous code elegantly
- **Error Handling**: Centralized error handling with `.catch()`
- **Chaining**: Chain multiple async operations
- **Composition**: Combine multiple promises with `Promise.all`, `Promise.race`
- **Avoid Callback Hell**: Replace nested callbacks with flat chains

## How It Works

### Promise States

```text
┌─────────────────────────────────────────────────────────────┐
│                    PROMISE STATES                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │                    PENDING                          │    │
│  │                   (initial)                         │    │
│  │                      │                              │    │
│  │          ┌───────────┴───────────┐                  │    │
│  │          ▼                       ▼                  │    │
│  │    ┌──────────┐           ┌──────────┐             │    │
│  │    │FULFILLED │           │ REJECTED │             │    │
│  │    │(success) │           │ (error)  │             │    │
│  │    └──────────┘           └──────────┘             │    │
│  │          │                       │                  │    │
│  │          └───────────┬───────────┘                  │    │
│  │                      ▼                              │    │
│  │                  SETTLED                            │    │
│  │              (final state)                         │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  STATE TRANSITIONS:                                          │
│  • pending → fulfilled (with value)                        │
│  • pending → rejected (with reason/error)                  │
│  • Once settled, state cannot change                       │
│  • Once settled, value/reason cannot change                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Promise Execution Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                 PROMISE EXECUTION FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  const promise = new Promise((resolve, reject) => {        │
│    // Executor function                                     │
│    // Runs immediately when promise is created             │
│                                                              │
│    if (success) {                                           │
│      resolve(value);  // → pending to fulfilled            │
│    } else {                                                  │
│      reject(error);   // → pending to rejected             │
│    }                                                         │
│  });                                                        │
│                                                              │
│  promise                                                     │
│    .then(value => {                                        │
│      // Handles fulfilled state                            │
│      return nextValue;  // Returns new promise             │
│    })                                                       │
│    .catch(error => {                                        │
│      // Handles rejected state                             │
│      return recoveryValue;                                 │
│    })                                                       │
│    .finally(() => {                                         │
│      // Runs regardless of state                           │
│      cleanup();                                             │
│    });                                                      │
│                                                              │
│  FLOW DIAGRAM:                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  new Promise(executor)                              │    │
│  │       │                                              │    │
│  │       ▼                                              │    │
│  │  Executor runs immediately                          │    │
│  │       │                                              │    │
│  │       ├──→ resolve(value) ──→ .then(value)         │    │
│  │       │                                              │    │
│  │       └──→ reject(error) ──→ .catch(error)         │    │
│  │                                                      │    │
│  │  .then() returns new promise (chainable)           │    │
│  │  .catch() returns new promise (chainable)          │    │
│  │  .finally() returns new promise (chainable)        │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Promise

```typescript
// Creating a promise
function fetchUser(id: number): Promise<{ id: number; name: string }> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: `User ${id}` });
      } else {
        reject(new Error('Invalid ID'));
      }
    }, 1000);
  });
}

// Using the promise
fetchUser(1)
  .then(user => console.log(user))  // { id: 1, name: 'User 1' }
  .catch(error => console.error(error))
  .finally(() => console.log('Done'));
```

### Promise Chaining

```typescript
function fetchData(url: string): Promise<any> {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve({ data: `Data from ${url}` });
    }, 1000);
  });
}

function processData(data: any): Promise<any> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ processed: true, ...data });
    }, 500);
  });
}

// Chaining
fetchData('https://api.example.com')
  .then(response => processData(response.data))
  .then(result => console.log(result))
  .catch(error => console.error(error));

// Each .then() returns a new promise
// If you return a promise, it's awaited
// If you return a value, it's wrapped in a resolved promise
```

### Error Handling

```typescript
function riskyOperation(): Promise<string> {
  return new Promise((resolve, reject) => {
    const success = Math.random() > 0.5;
    if (success) {
      resolve('Success!');
    } else {
      reject(new Error('Operation failed'));
    }
  });
}

// Error handling patterns
riskyOperation()
  .then(
    result => console.log(result),
    error => console.error('Error:', error)  // Handle in .then()
  )
  .catch(error => console.error('Catch:', error))  // Or use .catch()
  .finally(() => console.log('Cleanup'));

// Re-throwing errors
riskyOperation()
  .then(result => {
    if (result === 'Success!') {
      return result;
    }
    throw new Error('Unexpected result');  // Goes to .catch()
  })
  .catch(error => {
    console.error(error);
    return 'Default value';  // Recovery
  });
```

### Promise.all

```typescript
const promise1 = fetch('/api/user');
const promise2 = fetch('/api/posts');
const promise3 = fetch('/api/comments');

// Wait for all promises to resolve
Promise.all([promise1, promise2, promise3])
  .then(([user, posts, comments]) => {
    console.log('All data loaded');
  })
  .catch(error => {
    console.error('One promise failed:', error);
  });

// If any promise rejects, Promise.all rejects immediately
```

### Promise.allSettled

```typescript
const promise1 = Promise.resolve('Success');
const promise2 = Promise.reject('Error');
const promise3 = Promise.resolve('Another success');

// Wait for all promises to settle (fulfilled or rejected)
Promise.allSettled([promise1, promise2, promise3])
  .then(results => {
    results.forEach(result => {
      if (result.status === 'fulfilled') {
        console.log('Value:', result.value);
      } else {
        console.log('Reason:', result.reason);
      }
    });
  });

// Results:
// { status: 'fulfilled', value: 'Success' }
// { status: 'rejected', reason: 'Error' }
// { status: 'fulfilled', value: 'Another success' }
```

### Promise.any

```typescript
const promise1 = new Promise((_, reject) =>
  setTimeout(() => reject('Error 1'), 1000)
);
const promise2 = new Promise(resolve =>
  setTimeout(() => resolve('Success 2'), 2000)
);
const promise3 = new Promise(resolve =>
  setTimeout(() => resolve('Success 3'), 1500)
);

// Resolves with first successful promise
Promise.any([promise1, promise2, promise3])
  .then(value => {
    console.log('First success:', value);  // 'Success 3'
  })
  .catch(error => {
    // Only rejects if ALL promises reject
    console.error('All failed:', error);
  });
```

### Promise.race

```typescript
const promise1 = new Promise(resolve =>
  setTimeout(() => resolve('First'), 1000)
);
const promise2 = new Promise(resolve =>
  setTimeout(() => resolve('Second'), 2000)
);

// Resolves/rejects with first settled promise
Promise.race([promise1, promise2])
  .then(value => {
    console.log('Winner:', value);  // 'First'
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Practical Examples

```typescript
// Timeout pattern
function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Timeout')), ms);
  });

  return Promise.race([promise, timeout]);
}

// Usage
withTimeout(fetch('/api/data'), 5000)
  .then(response => response.json())
  .catch(error => {
    if (error.message === 'Timeout') {
      console.log('Request timed out');
    }
  });

// Retry pattern
function retry<T>(fn: () => Promise<T>, maxAttempts: number): Promise<T> {
  return fn().catch(error => {
    if (maxAttempts <= 1) {
      throw error;
    }
    return retry(fn, maxAttempts - 1);
  });
}

// Usage
retry(() => fetch('/api/data'), 3)
  .then(response => response.json())
  .catch(error => console.error('All attempts failed'));
```

## Real-World Use Cases

### 1. API Calls

```typescript
async function fetchUserData(userId: string) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

### 2. Parallel Operations

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

### 3. Sequential Operations

```typescript
async function processData() {
  const data = await fetchData();
  const processed = await processRawData(data);
  const saved = await saveToDatabase(processed);
  return saved;
}
```

### 4. Error Recovery

```typescript
async function fetchWithFallback() {
  try {
    return await fetchPrimary();
  } catch (error) {
    console.warn('Primary failed, trying fallback:', error);
    return await fetchFallback();
  }
}
```

### 5. Caching

```typescript
const cache = new Map<string, Promise<any>>();

async function cachedFetch(url: string) {
  if (cache.has(url)) {
    return cache.get(url);
  }

  const promise = fetch(url).then(r => r.json());
  cache.set(url, promise);

  return promise;
}
```

## Common Mistakes

### 1. Not Returning Promises

```typescript
// Bad: Not returning in .then()
fetchUser()
  .then(user => {
    fetchPosts(user.id);  // Not returned!
  })
  .then(posts => {
    // posts is undefined
  });

// Good: Return the promise
fetchUser()
  .then(user => {
    return fetchPosts(user.id);  // Returned!
  })
  .then(posts => {
    // posts is defined
  });
```

### 2. Forgetting .catch()

```typescript
// Bad: No error handling
fetchUser()
  .then(user => console.log(user));
// If promise rejects, unhandled rejection

// Good: Always handle errors
fetchUser()
  .then(user => console.log(user))
  .catch(error => console.error(error));
```

### 3. Creating Promises Unnecessarily

```typescript
// Bad: Wrapping existing promise
function getUser(id: number) {
  return new Promise((resolve, reject) => {
    fetch(`/api/users/${id}`)
      .then(response => resolve(response.json()))
      .catch(error => reject(error));
  });
}

// Good: Return promise directly
function getUser(id: number) {
  return fetch(`/api/users/${id}`).then(r => r.json());
}
```

### 4. Mixing async/await with .then()

```typescript
// Bad: Mixing styles
async function getData() {
  const user = await fetchUser().then(u => u);
  return user;
}

// Good: Use one style consistently
async function getData() {
  const user = await fetchUser();
  return user;
}
```

## Best Practices

### 1. Always Handle Errors

```typescript
// Use .catch() or try/catch with async/await
promise
  .then(result => processResult(result))
  .catch(error => handleError(error));

// Or
async function process() {
  try {
    const result = await promise;
    processResult(result);
  } catch (error) {
    handleError(error);
  }
}
```

### 2. Return Promises

```typescript
// Always return in .then()
promise
  .then(result => {
    return processResult(result);  // Return new promise
  })
  .then(processed => {
    console.log(processed);
  });
```

### 3. Use Promise Utilities

```typescript
// Promise.all for parallel
const results = await Promise.all([p1, p2, p3]);

// Promise.allSettled for all results
const results = await Promise.allSettled([p1, p2, p3]);

// Promise.race for timeout
const result = await Promise.race([promise, timeout]);

// Promise.any for first success
const result = await Promise.any([p1, p2, p3]);
```

### 4. Avoid Nested Promises

```typescript
// Bad: Nested
getUser().then(user => {
  getPosts(user.id).then(posts => {
    console.log(posts);
  });
});

// Good: Chained
getUser()
  .then(user => getPosts(user.id))
  .then(posts => console.log(posts));
```

## Performance Considerations

### Parallel vs Sequential

```typescript
// Sequential (slower)
async function sequential() {
  const a = await fetchA();
  const b = await fetchB();
  const c = await fetchC();
  return { a, b, c };
}

// Parallel (faster)
async function parallel() {
  const [a, b, c] = await Promise.all([
    fetchA(),
    fetchB(),
    fetchC()
  ]);
  return { a, b, c };
}
```

### Memory Usage

```typescript
// Bad: Creating many promises
function createManyPromises() {
  const promises = [];
  for (let i = 0; i < 1000000; i++) {
    promises.push(new Promise(resolve => resolve(i)));
  }
  return Promise.all(promises);
}

// Better: Process in batches
async function processBatched() {
  const results = [];
  for (let i = 0; i < 1000000; i += 1000) {
    const batch = [];
    for (let j = i; j < Math.min(i + 1000, 1000000); j++) {
      batch.push(Promise.resolve(j));
    }
    const batchResults = await Promise.all(batch);
    results.push(...batchResults);

    // Yield between batches
    await new Promise(resolve => setTimeout(resolve, 0));
  }
  return results;
}
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is a Promise in JavaScript?**

A: A Promise is an object representing the eventual completion or failure of an asynchronous operation. It's a container for a future value that allows you to chain asynchronous operations.

**Q2: What are the three states of a Promise?**

A:
- **Pending**: Initial state, neither fulfilled nor rejected
- **Fulfilled**: Operation completed successfully
- **Rejected**: Operation failed

**Q3: What is the difference between `.then()` and `.catch()`?**

A:
- `.then()`: Handles fulfilled state, receives the resolved value
- `.catch()`: Handles rejected state, receives the error/reason

**Q4: What is Promise chaining?**

A: Promise chaining is linking multiple `.then()` handlers together. Each `.then()` returns a new promise, allowing you to chain operations sequentially.

**Q5: How do you create a Promise?**

A: Use the `Promise` constructor:
```typescript
const promise = new Promise((resolve, reject) => {
  // Async operation
  if (success) {
    resolve(value);
  } else {
    reject(error);
  }
});
```

### Intermediate (5-10 questions)

**Q6: What is the difference between `Promise.all`, `Promise.allSettled`, `Promise.race`, and `Promise.any`?**

A:
- `Promise.all`: Resolves when all resolve, rejects if any rejects
- `Promise.allSettled`: Resolves when all settle (fulfilled or rejected)
- `Promise.race`: Resolves/rejects with first settled promise
- `Promise.any`: Resolves with first fulfilled, rejects if all reject

**Q7: What is microtask in relation to Promises?**

A: Promise callbacks (`.then`, `.catch`, `.finally`) are microtasks. They run after the current synchronous code completes but before macrotasks (setTimeout, I/O).

**Q8: What happens if you don't handle a rejected Promise?**

A: It results in an "unhandled promise rejection" warning. In modern browsers and Node.js, this can cause the program to terminate.

**Q9: What is `finally()` used for?**

A: `finally()` runs regardless of whether the promise is fulfilled or rejected. It's useful for cleanup operations that should always execute.

**Q10: How do you convert a callback-based function to a Promise?**

A: Use the `Promise` constructor:
```typescript
function promisify(callbackFn) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      callbackFn(...args, (error, result) => {
        if (error) reject(error);
        else resolve(result);
      });
    });
  };
}
```

### Senior (10-15 questions)

**Q11: Explain the Promise resolution procedure.**

A: When a promise is resolved:
1. If value is a thenable, adopt its state
2. If value is a promise, queue `.then()` handlers
3. If value is a plain value, wrap in resolved promise
4. Settle the promise with the value

**Q12: What is promise unwrapping?**

A: Promise unwrapping is when a `.then()` handler returns a promise, and the next `.then()` waits for that promise to settle before executing.

**Q13: What is the difference between returning a value and returning a Promise in `.then()`?**

A:
- Returning a value: Wraps it in a resolved promise
- Returning a promise: The next `.then()` waits for it to settle

**Q14: How do you implement a custom Promise.all?**

A:
```typescript
function customPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;

    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(value => {
          results[index] = value;
          completed++;
          if (completed === promises.length) {
            resolve(results);
          }
        })
        .catch(reject);
    });
  });
}
```

**Q15: What are the performance implications of Promise.all vs sequential awaits?**

A:
- `Promise.all`: Runs in parallel, faster for independent operations
- Sequential awaits: Runs one after another, slower but simpler
- Use `Promise.all` when operations don't depend on each other

### FAANG-style (5-10 questions)

**Q16: Design a Promise-based task scheduler.**

A:
```typescript
class TaskScheduler {
  private queue: (() => Promise<any>)[] = [];
  private running = 0;
  private maxConcurrent: number;

  constructor(maxConcurrent: number = 5) {
    this.maxConcurrent = maxConcurrent;
  }

  async add(task: () => Promise<any>): Promise<any> {
    while (this.running >= this.maxConcurrent) {
      await new Promise(resolve => setTimeout(resolve, 10));
    }

    this.running++;
    try {
      return await task();
    } finally {
      this.running--;
      this.processQueue();
    }
  }

  private processQueue() {
    if (this.queue.length > 0 && this.running < this.maxConcurrent) {
      const task = this.queue.shift()!;
      this.add(task);
    }
  }
}
```

**Q17: How would you implement Promise.retry with exponential backoff?**

A:
```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxAttempts) {
        throw error;
      }

      const delay = baseDelay * Math.pow(2, attempt - 1);
      const jitter = delay * 0.1 * Math.random();

      await new Promise(resolve =>
        setTimeout(resolve, delay + jitter)
      );
    }
  }

  throw new Error('Max attempts reached');
}
```

**Q18: Analyze the memory implications of Promise chains.**

A:
- Each `.then()` creates a new promise
- Old promises are garbage collected when no longer referenced
- Long chains can use significant memory
- Solution: Use async/await for flatter code

**Q19: How do you debug Promise chains?**

A:
1. Add `.then()` with logging
2. Use `console.trace()` in `.catch()`
3. Chrome DevTools: Async stack traces
4. Use `Promise.allSettled()` to see all results
5. Implement custom promise wrappers with logging

**Q20: What are the security implications of Promises?**

A:
1. **Timing attacks**: Measure promise resolution time
2. **Resource exhaustion**: Create too many promises
3. **Information leakage**: Promise values can be intercepted
4. **Mitigation**: Limit concurrent promises, validate inputs

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a Promise-related bug in production?**

A: Common bug: Unhandled rejection
```typescript
// Bug: Missing .catch()
fetchUser()
  .then(user => fetchPosts(user.id))
  .then(posts => renderPosts(posts));
// If fetchUser rejects, unhandled rejection

// Fix: Always add .catch()
fetchUser()
  .then(user => fetchPosts(user.id))
  .then(posts => renderPosts(posts))
  .catch(error => showError(error));
```

**Q22: How do you handle Promise cancellation?**

A:
```typescript
function cancellablePromise<T>(promise: Promise<T>): [Promise<T>, () => void] {
  let cancelled = false;
  let cancel: () => void;

  const wrappedPromise = new Promise<T>((resolve, reject) => {
    cancel = () => {
      cancelled = true;
      reject(new Error('Cancelled'));
    };

    promise
      .then(value => {
        if (!cancelled) resolve(value);
      })
      .catch(error => {
        if (!cancelled) reject(error);
      });
  });

  return [wrappedPromise, cancel];
}
```

**Q23: What is the relationship between Promises and async/await?**

A: async/await is syntactic sugar over Promises. `async` functions always return Promises, and `await` pauses execution until a Promise settles.

**Q24: How do different frameworks handle Promises?**

A:
- **React**: useEffect with async functions, state management
- **Vue**: Composition API with async setup
- **Angular**: HttpClient returns Observables (can convert to Promises)
- **Svelte**: onMount with async functions

**Q25: What are best practices for working with Promises?**

A:
1. Always handle errors with `.catch()` or try/catch
2. Return values in `.then()` handlers
3. Use `Promise.all` for parallel operations
4. Avoid creating Promises unnecessarily
5. Use async/await for cleaner code
6. Implement proper cancellation patterns
7. Monitor unhandled rejections
8. Use TypeScript for type safety

## Summary

Promises are essential for async JavaScript:

1. **Three states**: Pending, fulfilled, rejected
2. **Chaining**: Link multiple async operations
3. **Error handling**: Centralized with `.catch()`
4. **Composition**: `Promise.all`, `Promise.race`, etc.
5. **Microtasks**: Run after sync code, before macrotasks
6. **Best practices**: Handle errors, return promises, use utilities
7. **Performance**: Prefer parallel when possible

Understanding Promises is crucial for writing clean, maintainable asynchronous JavaScript.

## Cheat Sheet

```text
PROMISES CHEAT SHEET
═══════════════════════════════════════════════════════════════

STATES:
• Pending → Fulfilled (with value)
• Pending → Rejected (with reason)
• Once settled, cannot change

CREATING:
new Promise((resolve, reject) => {
  // Async operation
  resolve(value);  // or reject(error)
});

CHARNING:
promise
  .then(value => nextValue)
  .catch(error => recovery)
  .finally(() => cleanup);

UTILITIES:
• Promise.all([p1, p2, p3]) - All must resolve
• Promise.allSettled([p1, p2, p3]) - Wait for all
• Promise.race([p1, p2, p3]) - First to settle
• Promise.any([p1, p2, p3]) - First to resolve

ERROR HANDLING:
• Always add .catch() or try/catch
• Unhandled rejections crash programs
• Use .finally() for cleanup

MICROTASKS:
• Promise callbacks are microtasks
• Run after sync code
• Before macrotasks (setTimeout)
• Can block rendering

PERFORMANCE:
• Promise.all for parallel
• Sequential awaits for dependent operations
• Avoid unnecessary promise creation

BEST PRACTICES:
• Always handle errors
• Return promises in .then()
• Use async/await for readability
• Implement cancellation patterns
• Monitor unhandled rejections

COMMON MISTAKES:
• Not returning in .then()
• Forgetting .catch()
• Wrapping existing promises
• Mixing async/await with .then()

DEBUGGING:
• .then() with logging
• console.trace() in .catch()
• Chrome DevTools async traces
• Promise.allSettled() for all results
```

## References & Learn More

- [MDN: Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [JavaScript.info: Promises](https://javascript.info/promise-basics)
- [JavaScript.info: Promises Chaining](https://javascript.info/promise-chaining)
- [JavaScript.info: Promises API Reference](https://javascript.info/promise-api)
- [Dassum.io: Master JavaScript Promises](https://dassum.io/master-javascript-promises/)
