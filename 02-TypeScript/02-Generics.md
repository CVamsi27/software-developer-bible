# Generics

## Definition

**Generics** are type parameters that allow you to write reusable, type-safe code that works with multiple types while preserving type information. They act as placeholders for types that are specified when the code is used.

```text
┌─────────────────────────────────────────────────────────────────┐
│                        GENERICS FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Generic Definition         Instantiation                      │
│   ┌─────────────────┐       ┌─────────────────┐               │
│   │ function first<T>│       │ first<string>    │               │
│   │   (arr: T[]): T  │  ──▶  │   (arr: string[])│               │
│   └─────────────────┘       │   returns string  │               │
│                              └─────────────────┘               │
│                                                                 │
│   T is a "type variable" — a placeholder for a real type       │
│   The actual type is determined when the function is called     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Why Do We Need It?

1. **Type safety**: Maintain type information through generic code

2. **Code reuse**: Write one function/class that works with many types

3. **API design**: Create flexible libraries and frameworks

4. **Data structures**: Implement generic collections like arrays, maps, sets

5. **React components**: Type props, state, and hooks generically

## How It Works

### Type Parameters

```typescript
// T is a type parameter — a placeholder for a real type
function identity<T>(value: T): T {
  return value;
}

// TypeScript infers T from the argument
const str = identity("hello"); // T is string
const num = identity(42);      // T is number

// Explicit type argument (rarely needed)
const explicit = identity<string>("hello");

```

### Constraints

```typescript
// Constrain T to types that have a .length property
function logLength<T extends { length: number }>(value: T): T {
  console.log(`Length: ${value.length}`);
  return value;
}

logLength("hello");        // ✅ string has .length
logLength([1, 2, 3]);      // ✅ array has .length
logLength({ length: 10 }); // ✅ object with .length

// Constrain T to be a key of an object
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30 };
getProperty(user, "name");  // ✅ returns string
getProperty(user, "age");   // ✅ returns number
getProperty(user, "email"); // ❌ Error: "email" not in keyof User

```

### Default Types

```typescript
// Default type parameter
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  message: string;
}

// Uses default (unknown)
const response1: ApiResponse = {
  data: null,
  status: 200,
  message: "OK"
};

// Specifies concrete type
interface User {
  name: string;
  email: string;
}
const response2: ApiResponse<User> = {
  data: { name: "Alice", email: "alice@example.com" },
  status: 200,
  message: "OK"
};

```

## Code Examples

### Generic Functions

```typescript
// ─── Basic Generic Function ───────────────────────────────────
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

const firstNum = first([1, 2, 3]);    // number | undefined
const firstStr = first(["a", "b"]);   // string | undefined

// ─── Multiple Type Parameters ─────────────────────────────────
function map<T, U>(arr: T[], fn: (item: T) => U): U[] {
  return arr.map(fn);
}

const doubled = map([1, 2, 3], n => n * 2);         // number[]
const lengths = map(["hello", "world"], s => s.length); // number[]

// ─── Generic with Constraint ──────────────────────────────────
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

const merged = merge({ name: "Alice" }, { age: 30 });
// { name: string; age: number }

```

### Generic Interfaces

```typescript
// ─── Generic Interface ────────────────────────────────────────
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// ─── Implementing Generic Interface ───────────────────────────
interface User {
  id: string;
  name: string;
  email: string;
}

class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    // Implementation
    return null;
  }

  async findAll(): Promise<User[]> {
    return [];
  }

  async save(user: User): Promise<User> {
    return user;
  }

  async delete(id: string): Promise<boolean> {
    return true;
  }
}

```

### Generic Classes

```typescript
// ─── Generic Stack ────────────────────────────────────────────
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  get size(): number {
    return this.items.length;
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }
}

const numberStack = new Stack<number>();
numberStack.push(1);
numberStack.push(2);
const top = numberStack.pop(); // number | undefined

const stringStack = new Stack<string>();
stringStack.push("hello");
const topStr = stringStack.pop(); // string | undefined

// ─── Generic Cache ────────────────────────────────────────────
class Cache<T> {
  private store = new Map<string, { value: T; expires: number }>();

  set(key: string, value: T, ttl: number): void {
    this.store.set(key, {
      value,
      expires: Date.now() + ttl
    });
  }

  get(key: string): T | undefined {
    const item = this.store.get(key);
    if (!item || Date.now() > item.expires) {
      this.store.delete(key);
      return undefined;
    }
    return item.value;
  }

  has(key: string): boolean {
    return this.get(key) !== undefined;
  }

  delete(key: string): boolean {
    return this.store.delete(key);
  }
}

const userCache = new Cache<User>();
userCache.set("user:1", { id: "1", name: "Alice", email: "a@b.com" }, 60000);
const cachedUser = userCache.get("user:1"); // User | undefined

```

### Real-World Use Cases

```typescript
// ─── API Response Handling ────────────────────────────────────
interface ApiResponse<T> {
  data: T;
  status: number;
  timestamp: Date;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  total: number;
  page: number;
  limit: number;
}

async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  const data = await response.json();
  return {
    data: data as T,
    status: response.status,
    timestamp: new Date()
  };
}

interface User {
  id: string;
  name: string;
}

const userResponse = await fetchData<User>("/api/users/1");
// ApiResponse<User>

// ─── Event Emitter ────────────────────────────────────────────
type EventMap = {
  "user:created": { userId: string };
  "user:deleted": { userId: string };
  "order:placed": { orderId: string; amount: number };
};

class TypedEventEmitter<Events extends Record<string, unknown>> {
  private listeners = new Map<string, Set<(data: unknown) => void>>();

  on<K extends keyof Events>(
    event: K,
    callback: (data: Events[K]) => void
  ): () => void {
    if (!this.listeners.has(event as string)) {
      this.listeners.set(event as string, new Set());
    }
    this.listeners.get(event as string)!.add(callback as (data: unknown) => void);

    // Return unsubscribe function
    return () => {
      this.listeners.get(event as string)?.delete(callback as (data: unknown) => void);
    };
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.listeners.get(event as string)?.forEach(callback => callback(data));
  }
}

const emitter = new TypedEventEmitter<EventMap>();
emitter.on("user:created", (data) => {
  console.log(data.userId); // ✅ TypeScript knows data.userId exists
});
emitter.emit("user:created", { userId: "123" }); // ✅ Type-safe

```

## Common Mistakes

### 1. Overusing Generics

```typescript
// ❌ Bad: Unnecessary generic
function add<T>(a: T, b: T): T {
  return a + b; // Error: T might not have +
}

// ✅ Good: Constrain or use specific type
function add(a: number, b: number): number {
  return a + b;
}

// Or with constraint:
function add<T extends number | string>(a: T, b: T): T {
  return (a as any) + b;
}

```

### 2. Not Constraining Type Parameters

```typescript
// ❌ Bad: No constraint, runtime errors possible
function getLength<T>(value: T): number {
  return value.length; // Error: T doesn't have .length
}

// ✅ Good: Add constraint
function getLength<T extends { length: number }>(value: T): number {
  return value.length;
}

```

### 3. Using `any` in Generic Code

```typescript
// ❌ Bad: Defeats the purpose of generics
function first<T>(arr: T[]): any {
  return arr[0]; // Loses type information
}

// ✅ Good: Preserve type information
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

```

## Best Practices

```typescript
// 1. Name type parameters meaningfully
function mapArray<TInput, TOutput>(
  arr: TInput[],
  transform: (item: TInput) => TOutput
): TOutput[] {
  return arr.map(transform);
}

// 2. Use constraints to ensure type safety
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

// 3. Use default types for flexibility
interface Store<T = unknown> {
  get(key: string): T | undefined;
  set(key: string, value: T): void;
}

// 4. Prefer multiple type parameters over single
// ❌ Bad: Single type parameter for unrelated types
function combine<T>(a: T, b: T): T[] { return [a, b]; }

// ✅ Good: Separate type parameters
function combine<A, B>(a: A, b: B): [A, B] { return [a, b]; }

// 5. Use generic constraints with keyof for property access
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

```

## Performance Considerations

- **Type erasure**: Generics are erased at runtime — no performance cost
- **Compilation**: Complex generics can slow down compilation
- **Instantiation**: Each generic instantiation creates a new type
- **Union types**: Generic constraints with unions can cause type explosion
- **Conditional types**: Deep conditional generics can cause slow type checking

## Interview Questions

### Beginner

1. **What are generics in TypeScript?**

   - Type parameters that allow writing reusable, type-safe code

2. **How do you define a generic function?**

   ```typescript
   function identity<T>(value: T): T { return value; }

```

3. **What is the purpose of generic constraints?**

   - To limit what types a generic parameter can accept

4. **Can you have multiple type parameters?**

   - Yes: `<T, U, V>` etc.

5. **What is the default type parameter?**

   - A fallback type when no type is specified: `<T = unknown>`

### Intermediate

6. **When would you use generic constraints with keyof?**

   - When accessing properties dynamically on a generic type

7. **How do generics differ from `any`?**

   - Generics preserve type information; `any` loses it

8. **Can you use generics with interfaces?**

   - Yes: `interface Box<T> { value: T; }`

9. **How do you constrain a generic to be a function?**

   ```typescript
   function call<T extends (...args: any[]) => any>(fn: T): ReturnType<T> {
     return fn();
   }

```

10. **What is type inference in generics?**

    - TypeScript automatically determining the type parameter from usage

### Senior

11. **Design a generic curry function**

    ```typescript
    type Curry<Args extends any[], Return> =
      Args extends [infer First, ...infer Rest]
        ? (arg: First) => Curry<Rest, Return>
        : Return;

    function curry<Args extends any[], Return>(
      fn: (...args: Args) => Return
    ): Curry<Args, Return> {
      // Implementation
    }

```

12. **Implement a type-safe event emitter**

    - Map event names to payload types using generics

13. **How do you handle generic type inference in complex scenarios?**

    - Use explicit type arguments when inference fails

14. **Explain variance in generic types**

    - Covariance, contravariance, invariance in generic positions

### FAANG-style

15. **Implement a generic immutable data structure**

    - Design a persistent list or tree with generic types

16. **Build a type-safe query builder**

    - Use generics to infer result types from query definitions

17. **Create a generic validation framework**

    - Type-safe validators that infer output types

### Follow-ups

18. **How do generics interact with union types?**

    - Generic constraints can use unions; generic parameters can be unions

19. **Can you have generic type aliases?**

    - Yes: `type Box<T> = { value: T; }`

20. **How do generics work with async/await?**

    - Generic functions can return promises: `function fetch<T>(): Promise<T>`

## Summary

Generics are essential for writing reusable, type-safe TypeScript code. They allow you to create flexible functions, classes, and interfaces that work with multiple types while preserving type information. Use constraints to ensure type safety, and leverage TypeScript's type inference to minimize explicit type annotations.

## Cheat Sheet

```typescript
// Basic generic function
function identity<T>(value: T): T { return value; }

// Generic with constraint
function first<T extends { length: number }>(arr: T): T[0] { return arr[0]; }

// Generic interface
interface Box<T> { value: T; }

// Generic class
class Stack<T> { /* ... */ }

// Multiple type parameters
function map<T, U>(arr: T[], fn: (item: T) => U): U[] { return arr.map(fn); }

// Default type
interface Response<T = unknown> { data: T; }

// Generic with keyof
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> { /* ... */ }

// Generic constraint with extends
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

```

## References & Learn More

- [TypeScript Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [TypeScript Generics Tutorial](https://www.typescriptlang.org/docs/handbook/2/generics.html#generic-constraints)
- [Generic Types in TypeScript](https://www.digitalocean.com/community/tutorials/typescript-generics)
