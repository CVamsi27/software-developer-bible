# Advanced Generics

## Definition

**Advanced generics** encompass complex generic patterns that go beyond basic type parameters. They include higher-kinded types simulation, variadic generics, conditional generic types, and sophisticated constraint patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│                  ADVANCED GENERIC PATTERNS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┬───────────────────────────────────────┐  │
│   │ Pattern         │ Description                           │  │
│   ├─────────────────┼───────────────────────────────────────┤  │
│   │ HKT Simulation  │ Higher-Kinded Types workaround        │  │
│   │ Variadic        │ Variable-length type parameters       │  │
│   │ Conditional     │ Type-level conditionals in generics   │  │
│   │ Constraints     │ Complex keyof/infer constraints       │  │
│   │ Recursive       │ Self-referencing generic types        │  │
│   │ Mapped          │ Generic mapped types                  │  │
│   └─────────────────┴───────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **Type-level programming**: Express complex type relationships
2. **Library design**: Create flexible, type-safe APIs
3. **Advanced patterns**: Implement sophisticated abstractions
4. **Type inference**: Guide TypeScript's type inference
5. **Code reuse**: Build reusable type utilities

## How It Works

### Higher-Kinded Types Simulation

```typescript
// TypeScript doesn't have native HKTs, but we can simulate them

// ─── Basic HKT Pattern ────────────────────────────────────────
interface HKT {
  _type: unknown;
}

interface ArrayHKT extends HKT {
  _type: unknown[];
}

interface PromiseHKT extends HKT {
  _type: Promise<unknown>;
}

// Map function for HKTs
type MapHKT<F extends HKT, T, U> = F extends ArrayHKT
  ? T[]
  : F extends PromiseHKT
    ? Promise<T>
    : never;

// ─── Practical HKT Example ────────────────────────────────────
interface Functor<F> {
  map: <A, B>(fa: F<A>, f: (a: A) => B) => F<B>;
}

// Array functor
const arrayFunctor: Functor<Array> = {
  map: (fa, f) => fa.map(f)
};

// Promise functor (simplified)
const promiseFunctor: Functor<Promise> = {
  map: (fa, f) => fa.then(f)
};
```

### Generic Constraints with keyof

```typescript
// ─── Deep Property Access ─────────────────────────────────────
type DeepPropertyAccess<T, Path extends string> =
  Path extends `${infer Head}.${infer Rest}`
    ? Head extends keyof T
      ? DeepPropertyAccess<T[Head], Rest>
      : never
    : Path extends keyof T
      ? T[Path]
      : never;

interface Config {
  database: {
    host: string;
    port: number;
    credentials: {
      user: string;
      password: string;
    };
  };
}

type HostType = DeepPropertyAccess<Config, "database.host">; // string
type UserType = DeepPropertyAccess<Config, "database.credentials.user">; // string

// ─── Type-safe property setter ────────────────────────────────
type SetProperty<
  T,
  Path extends string,
  Value
> = Path extends `${infer Head}.${infer Rest}`
  ? Head extends keyof T
    ? { [K in keyof T]: K extends Head ? SetProperty<T[K], Rest, Value> : T[K] }
    : T
  : Path extends keyof T
    ? { [K in keyof T]: K extends Path ? Value : T[K] }
    : T;
```

### Conditional Generic Types

```typescript
// ─── Conditional return type ──────────────────────────────────
type ApiResponse<T> = T extends "user"
  ? { name: string; email: string }
  : T extends "post"
    ? { title: string; content: string }
    : never;

function fetchData<T extends "user" | "post">(type: T): Promise<ApiResponse<T>> {
  return fetch(`/api/${type}`).then(r => r.json());
}

const user = await fetchData("user"); // { name: string; email: string }

// ─── Conditional generic constraints ──────────────────────────
function process<T>(value: T): T extends string ? number : boolean {
  if (typeof value === "string") {
    return value.length as any;
  }
  return (value !== null) as any;
}
```

### Variadic Generics

```typescript
// ─── Variable-length type parameters ──────────────────────────
type Tuple<T extends any[]> = [...T];

type Result = Tuple<[string, number, boolean]>;
// [string, number, boolean]

// ─── Curry function with variadic generics ────────────────────
type Curry<Args extends any[], Return> =
  Args extends [infer First, ...infer Rest]
    ? Rest extends []
      ? (arg: First) => Return
      : (arg: First) => Curry<Rest, Return>
    : Return;

function curry<Args extends any[], Return>(
  fn: (...args: Args) => Return
): Curry<Args, Return> {
  const arity = fn.length;

  if (arity === 1) {
    return fn as any;
  }

  return (arg: any) =>
    curry((...args: any[]) => fn(arg, ...args)) as any;
}

const add = curry((a: number, b: number, c: number) => a + b + c);
add(1)(2)(3); // 6

// ─── Pipe function ────────────────────────────────────────────
type PipeResult<Functions extends ((arg: any) => any)[]> =
  Functions extends [(arg: infer A) => infer B, ...infer Rest]
    ? Rest extends ((arg: B) => any)[]
      ? PipeResult<Rest> extends (arg: A) => infer C
        ? (arg: A) => C
        : never
      : (arg: A) => B
    : never;

function pipe<Functions extends ((arg: any) => any)[]>(
  ...fns: Functions
): PipeResult<Functions> {
  return (arg: any) =>
    fns.reduce((acc, fn) => fn(acc), arg) as any;
}

const process = pipe(
  (x: number) => x + 1,
  (x: number) => x * 2,
  (x: number) => x.toString()
);
// (arg: number) => string
```

### Recursive Generic Types

```typescript
// ─── Deep readonly ────────────────────────────────────────────
type DeepReadonly<T> =
  T extends (infer U)[]
    ? ReadonlyArray<DeepReadonly<U>>
    : T extends Map<infer K, infer V>
      ? Map<DeepReadonly<K>, DeepReadonly<V>>
      : T extends Set<infer U>
        ? Set<DeepReadonly<U>>
        : T extends object
          ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
          : T;

// ─── Deep partial ─────────────────────────────────────────────
type DeepPartial<T> =
  T extends (infer U)[]
    ? DeepPartial<U>[]
    : T extends Map<infer K, infer V>
      ? Map<K, DeepPartial<V>>
      : T extends Set<infer U>
        ? Set<DeepPartial<U>>
        : T extends object
          ? { [K in keyof T]?: DeepPartial<T[K]> }
          : T;

// ─── Flatten nested arrays ────────────────────────────────────
type DeepFlatten<T> =
  T extends (infer U)[]
    ? DeepFlatten<U>
    : T;

type Nested = number[][][];
type Flat = DeepFlatten<Nested>; // number
```

### Generic Utility Types Deep Dive

```typescript
// ─── Type-safe Object.keys ────────────────────────────────────
function typedKeys<T extends object>(obj: T): (keyof T)[] {
  return Object.keys(obj) as (keyof T)[];
}

const user = { name: "Alice", age: 30, email: "a@b.com" };
const keys = typedKeys(user); // ("name" | "age" | "email")[]

// ─── Type-safe Object.entries ─────────────────────────────────
function typedEntries<T extends object>(
  obj: T
): [keyof T, T[keyof T]][] {
  return Object.entries(obj) as [keyof T, T[keyof T]][];
}

// ─── Type-safe Object.fromEntries ─────────────────────────────
function typedFromEntries<K extends string, V>(
  entries: [K, V][]
): { [P in K]: V } {
  return Object.fromEntries(entries) as { [P in K]: V };
}

// ─── Type-safe array grouping ─────────────────────────────────
function groupBy<T, K extends string>(
  arr: T[],
  keyFn: (item: T) => K
): Record<K, T[]> {
  return arr.reduce((acc, item) => {
    const key = keyFn(item);
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(item);
    return acc;
  }, {} as Record<K, T[]>);
}

const users = [
  { name: "Alice", role: "admin" },
  { name: "Bob", role: "user" },
  { name: "Charlie", role: "admin" }
];

const grouped = groupBy(users, (u) => u.role);
// { admin: User[]; user: User[] }
```

## Code Examples

### Real-World Use Cases

```typescript
// ─── Type-safe event emitter ──────────────────────────────────
type EventMap = {
  "user:created": { userId: string };
  "user:deleted": { userId: string };
  "order:placed": { orderId: string; amount: number };
};

class TypedEventEmitter<Events extends Record<string, any>> {
  private listeners = new Map<string, Set<Function>>();

  on<K extends keyof Events>(
    event: K,
    listener: (payload: Events[K]) => void
  ): () => void {
    if (!this.listeners.has(event as string)) {
      this.listeners.set(event as string, new Set());
    }
    this.listeners.get(event as string)!.add(listener);

    return () => {
      this.listeners.get(event as string)?.delete(listener);
    };
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.listeners.get(event as string)?.forEach((fn) =>
      (fn as (payload: Events[K]) => void)(payload)
    );
  }
}

const emitter = new TypedEventEmitter<EventMap>();
emitter.on("user:created", (data) => {
  console.log(data.userId); // ✅ TypeScript knows data.userId exists
});

// ─── Type-safe Redux-like store ───────────────────────────────
type ActionMap = {
  "user/create": { name: string; email: string };
  "user/delete": { userId: string };
  "post/create": { title: string; content: string };
};

type Action<T extends keyof ActionMap> = {
  type: T;
  payload: ActionMap[T];
};

function createAction<T extends keyof ActionMap>(
  type: T,
  payload: ActionMap[T]
): Action<T> {
  return { type, payload };
}

const createAction_userCreate = createAction("user/create", {
  name: "Alice",
  email: "alice@example.com"
});

// ─── Type-safe query builder ──────────────────────────────────
interface DatabaseSchema {
  users: {
    id: string;
    name: string;
    email: string;
    age: number;
  };
  posts: {
    id: string;
    title: string;
    content: string;
    authorId: string;
  };
}

type Table = keyof DatabaseSchema;
type Column<T extends Table> = keyof DatabaseSchema[T];

function select<T extends Table>(
  table: T,
  columns: Column<T>[]
): void {
  console.log(`SELECT ${columns.join(", ")} FROM ${table}`);
}

select("users", ["id", "name"]); // ✅
select("posts", ["id", "title"]); // ✅
select("users", ["id", "title"]); // ❌ Error: "title" not in users
```

## Common Mistakes

### 1. Overcomplicating Generic Constraints

```typescript
// ❌ Bad: Too many constraints
function process<
  T extends object & { id: string } & { name: string } & { email: string }
>(value: T): T {
  return value;
}

// ✅ Good: Use interfaces for constraints
interface User {
  id: string;
  name: string;
  email: string;
}

function process<T extends User>(value: T): T {
  return value;
}
```

### 2. Not Using Default Types

```typescript
// ❌ Bad: Always requiring type argument
interface Response<T> {
  data: T;
  status: number;
}

// ✅ Good: Provide default type
interface Response<T = unknown> {
  data: T;
  status: number;
}

const response: Response = { data: null, status: 200 }; // OK
```

### 3. Recursive Types Without Base Case

```typescript
// ❌ Bad: Infinite recursion
type Infinite<T> = { value: T; next: Infinite<T> };

// ✅ Good: Base case
type LinkedList<T> = { value: T; next: LinkedList<T> } | null;
```

## Best Practices

```typescript
// 1. Use descriptive generic names
function processData<TInput, TOutput>(
  input: TInput,
  transform: (input: TInput) => TOutput
): TOutput {
  return transform(input);
}

// 2. Provide default types for flexibility
interface Store<T = unknown> {
  get(key: string): T | undefined;
  set(key: string, value: T): void;
}

// 3. Use constraints to ensure type safety
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

// 4. Document complex generic types
/**
 * Maps event names to their payload types.
 * Used for type-safe event handling.
 */
type EventMap = Record<string, unknown>;

// 5. Use generic inference when possible
function identity<T>(value: T): T {
  return value;
}

// TypeScript infers T from the argument
const result = identity("hello"); // T is inferred as string
```

## Performance Considerations

- **Compilation**: Complex generics slow compilation
- **IDE**: Deep generic chains affect IDE performance
- **Type checking**: Each generic instantiation creates a new type
- **Memory**: Large generic types consume more memory
- **Caching**: TypeScript caches generic type results

## Interview Questions

### Beginner

1. **What are advanced generics?**
   - Complex generic patterns beyond basic type parameters

2. **What is a generic constraint?**
   - A restriction on what types a generic parameter can accept

3. **How do you create a generic interface?**
   - Use `<T>` syntax: `interface Box<T> { value: T; }`

4. **Can you have multiple type parameters?**
   - Yes: `<T, U, V>` etc.

5. **What is a default type parameter?**
   - A fallback type: `<T = unknown>`

### Intermediate

6. **How do you simulate higher-kinded types?**
   - Use interfaces with `_type` property

7. **What are variadic generics?**
   - Type parameters that accept variable-length tuples

8. **How do you create a type-safe curry function?**
   - Use recursive conditional types with `infer`

9. **What is a recursive generic type?**
   - A generic type that references itself

10. **How do you constrain a generic to be a function?**
    - Use `T extends (...args: any[]) => any`

### Senior

11. **Implement a type-safe pipe function**
    - Use variadic generics and conditional types

12. **Design a type-safe ORM query builder**
    - Use generic constraints for table/column relationships

13. **How do you create a type-safe event system?**
    - Use mapped types with generic constraints

14. **What is the difference between `any` and `unknown` in generics?**
    - `unknown` preserves type safety; `any` bypasses it

### FAANG-style

15. **Build a type-safe state management solution**
    - Use advanced generics for actions, reducers, middleware

16. **Implement a type-safe API client**
    - Use generics for request/response types

17. **Create a type-safe form validation system**
    - Use generics for field types, validation rules

### Follow-ups

18. **How do generics interact with conditional types?**
    - Generic parameters can be used in conditional type checks

19. **Can you have generic type aliases?**
    - Yes: `type Box<T> = { value: T; }`

20. **How do you debug complex generic types?**
    - Create intermediate type aliases, use IDE hover

## Summary

Advanced generics enable sophisticated type-level programming in TypeScript. They're essential for building type-safe libraries, frameworks, and complex applications. Master constraints, conditional types, and variadic generics for maximum type safety.

## Cheat Sheet

```typescript
// Generic constraint
function first<T extends { length: number }>(arr: T): T[0] { return arr[0]; }

// Default type
interface Response<T = unknown> { data: T; }

// Multiple type parameters
function map<T, U>(arr: T[], fn: (item: T) => U): U[] { return arr.map(fn); }

// Recursive generic
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// Variadic generic
type Curry<Args extends any[], Return> =
  Args extends [infer First, ...infer Rest]
    ? (arg: First) => Curry<Rest, Return>
    : Return;

// Higher-kinded type simulation
interface HKT { _type: unknown; }
interface ArrayHKT extends HKT { _type: unknown[]; }
```

## References & Learn More

- [TypeScript Advanced Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)
- [Type Challenges (GitHub)](https://github.com/type-challenges/type-challenges)
- [TypeScript Playground](https://www.typescriptlang.org/play)
