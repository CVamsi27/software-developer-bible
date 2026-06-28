# Infer

## Definition

**`infer`** is a keyword used in conditional types to extract and name a type within a type position. It allows you to "infer" or "capture" a type from another type for reuse.

```text
┌─────────────────────────────────────────────────────────────────┐
│                      INFER KEYWORD                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   T extends (infer U) => void                                   │
│             │                                                   │
│             └── Captures the parameter type as U               │
│                                                                 │
│   Example:                                                      │
│   type GetReturnType<T> = T extends (...args: any[]) => infer R│
│                                                │                │
│                                                └── Captures R   │
│                                                                 │
│   type Fn = () => string;                                       │
│   type Result = GetReturnType<Fn>;  // R is captured as string  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Why Do We Need It?

1. **Type extraction**: Extract types from complex type structures

2. **Library design**: Create flexible type utilities

3. **Type inference**: Let TypeScript figure out types for you

4. **Code reuse**: Capture and reuse inferred types

5. **Advanced patterns**: Build sophisticated type-level programming

## How It Works

### Basic Inference

```typescript
// Extract return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type A = ReturnType<() => string>;         // string
type B = ReturnType<(x: number) => boolean>; // boolean

// Extract element type from array
type ElementType<T> = T extends (infer E)[] ? E : never;

type C = ElementType<string[]>;  // string
type D = ElementType<number[]>;  // number

```

### In Function Parameters

```typescript
// Extract first parameter type
type FirstParam<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;

type A = FirstParam<(name: string, age: number) => void>; // string

// Extract all parameter types as tuple
type Params<T> = T extends (...args: infer P) => any ? P : never;

type B = Params<(x: string, y: number, z: boolean) => void>;
// [string, number, boolean]

```

### In Return Types

```typescript
// Extract Promise inner type
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

type A = UnwrapPromise<Promise<string>>;  // string
type B = UnwrapPromise<Promise<number>>;  // number
type C = UnwrapPromise<number>;           // number (not a promise)

// Deep unwrap
type DeepUnwrap<T> = T extends Promise<infer U> ? DeepUnwrap<U> : T;

type D = DeepUnwrap<Promise<Promise<Promise<string>>>>; // string

```

### In Tuple Positions

```typescript
// Extract first element of tuple
type Head<T extends any[]> = T extends [infer H, ...any[]] ? H : never;

type A = Head<[string, number, boolean]>; // string

// Extract tail of tuple
type Tail<T extends any[]> = T extends [any, ...infer Rest] ? Rest : never;

type B = Tail<[string, number, boolean]>; // [number, boolean]

// Extract last element
type Last<T extends any[]> = T extends [...any[], infer L] ? L : never;

type C = Last<[string, number, boolean]>; // boolean

```

### Complex Inference Patterns

```typescript
// Extract property type
type PropertyType<T, K extends keyof T> = T extends { [P in K]: infer V } ? V : never;

interface User {
  name: string;
  age: number;
}

type A = PropertyType<User, "name">; // string
type B = PropertyType<User, "age">;  // number

// Extract event handler parameter
type EventPayload<T> = T extends (event: infer E) => void ? E : never;

type ClickHandler = (event: MouseEvent) => void;
type Payload = EventPayload<ClickHandler>; // MouseEvent

// Extract class instance type
type InstanceOf<T> = T extends new (...args: any[]) => infer I ? I : never;

class User {
  constructor(public name: string) {}
}

type UserInstance = InstanceOf<typeof User>; // User

```

## Code Examples

### Practical Examples

```typescript
// ─── Type-safe API response handling ──────────────────────────
type ApiResponse<T> = {
  data: T;
  status: number;
  timestamp: Date;
};

type ExtractApiResponse<T> = T extends ApiResponse<infer D> ? D : never;

const userResponse: ApiResponse<User> = {
  data: { id: "1", name: "Alice", email: "a@b.com" },
  status: 200,
  timestamp: new Date()
};

type UserData = ExtractApiResponse<typeof userResponse>; // User

// ─── Type-safe router ─────────────────────────────────────────
type RouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof RouteParams<Rest>]: string }
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

type Params1 = RouteParams<"users/:id">;           // { id: string }
type Params2 = RouteParams<"users/:id/posts/:postId">;
// { id: string; postId: string }

// ─── Extract middleware types ─────────────────────────────────
type Middleware<T> = T extends (req: infer Req, res: infer Res, next: infer Next) => any
  ? { request: Req; response: Res; next: Next }
  : never;

type ExpressMiddleware = Middleware<express.Handler>;
// { request: Request; response: Response; next: NextFunction }

```

### Advanced Patterns

```typescript
// ─── Deep pick using infer ────────────────────────────────────
type DeepPick<T, K extends string> =
  K extends `${infer Head}.${infer Rest}`
    ? Head extends keyof T
      ? { [P in Head]: DeepPick<T[Head], Rest> }
      : never
      : K extends keyof T
        ? { [P in K]: T[P] }
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
  server: {
    port: number;
  };
}

type DbConfig = DeepPick<Config, "database.host">;
// { database: { host: string } }

type Credentials = DeepPick<Config, "database.credentials.user">;
// { database: { credentials: { user: string } } }

// ─── Type-safe function composition ───────────────────────────
type ComposeResult<Fns extends ((...args: any[]) => any)[]> =
  Fns extends [(...args: infer A) => infer B, ...infer Rest]
    ? Rest extends ((arg: B) => infer C)[]
      ? (...args: A) => C
      : never
      : never;

// ─── Extract union members matching pattern ───────────────────
type ExtractByType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never;
}[keyof T];

interface Mixed {
  name: string;
  age: number;
  active: boolean;
  email: string;
}

type StringKeys = ExtractByType<Mixed, string>; // "name" | "email"
type NumberKeys = ExtractByType<Mixed, number>; // "age"

```

## Common Mistakes

### 1. Forgetting Inference Position

```typescript
// ❌ Wrong: infer not in the right position
type Bad<T> = T extends infer U ? U : never;
// This just returns T, doesn't capture anything specific

// ✅ Correct: infer in specific position
type Good<T> = T extends Promise<infer U> ? U : never;
// Captures the Promise's inner type

```

### 2. Not Handling the False Branch

```typescript
// ❌ Bad: Returns unknown for non-matching types
type ExtractString<T> = T extends string ? infer S : unknown;

// ✅ Good: Return a sensible default
type ExtractString<T> = T extends string ? T : never;

```

### 3. Overcomplicating Inference

```typescript
// ❌ Bad: Too many nested inferences
type Complex<T> =
  T extends Promise<infer U>
    ? U extends Array<infer V>
      ? V extends Promise<infer W>
        ? W
        : V
      : U
    : T;

// ✅ Better: Use helper types
type Unwrap<T> = T extends Promise<infer U> ? Unwrap<U> : T;
type Flatten<T> = T extends Array<infer E> ? Flatten<E> : T;
type Result = Flatten<Unwrap<T>>;

```

## Best Practices

```typescript
// 1. Name inferred types meaningfully
type GetPayload<T> = T extends (event: infer EventPayload) => void
  ? EventPayload
  : never;

// 2. Use infer for type-safe wrappers
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

// 3. Combine with conditional types for powerful extractions
type ElementType<T> = T extends readonly (infer E)[] ? E : T;

// 4. Use infer in mapped types for transformations
type PromiseProps<T> = {
  [K in keyof T]: T[K] extends Promise<infer U> ? U : T[K];
};

// 5. Document complex infer patterns
/**

 - Extracts the first element of a tuple type.
 - Returns `never` if T is not a tuple.
 */
type Head<T extends readonly any[]> = T extends readonly [infer H, ...any[]] ? H : never;

```

## Performance Considerations

- **Compilation**: Each infer creates a new type instantiation
- **Depth**: Deeply nested infer can slow compilation
- **Caching**: TypeScript caches infer results
- **Distribution**: Infer interacts with distribution in conditional types
- **Recursion**: Recursive infer can cause infinite type recursion

## Interview Questions

### Beginner

1. **What does `infer` do?**

   - Extracts and names a type within a conditional type

2. **How do you extract a function's return type?**

   ```typescript
   type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

```

3. **Can you have multiple `infer` in one conditional?**

   - Yes, but only one per position

4. **What happens if infer doesn't match?**

   - The conditional type evaluates to the false branch

5. **How do you extract Promise inner type?**

   ```typescript
   type Unwrap<T> = T extends Promise<infer U> ? U : T;

```

### Intermediate

6. **Write a type that extracts first array element**

   ```typescript
   type First<T extends any[]> = T extends [infer F, ...any[]] ? F : never;

```

7. **How do you extract all function parameters?**

   ```typescript
   type Params<T> = T extends (...args: infer P) => any ? P : never;

```

8. **Can infer be used outside conditional types?**

   - No, it's only valid in the `extends` clause

9. **How do you handle nested promises?**

   - Use recursive conditional types with infer

10. **What is the difference between infer and extends?**

    - `extends` checks assignability; `infer` captures a type

### Senior

11. **Design a type that extracts all event handler types**

    - Use infer to capture event parameters

12. **How do you create a type-safe deep clone function?**

    - Use infer to preserve type information through cloning

13. **Implement a type-safe curry function using infer**

    - Capture argument types and return type

14. **How do you handle function overloads with infer?**

    - Use infer with conditional types to match signatures

### FAANG-style

15. **Build a type-safe ORM query builder**

    - Use infer to extract model types from queries

16. **Create a type-safe middleware chain**

    - Use infer to propagate types through middleware

17. **Implement a type-safe state machine**

    - Use infer to capture state and event types

### Follow-ups

18. **How does infer interact with union types?**

    - Infer distributes over unions automatically

19. **Can you use infer in mapped types?**

    - No, infer is only valid in conditional type extends clauses

20. **How do you debug infer issues?**

    - Create intermediate type aliases and use IDE hover

## Summary

The `infer` keyword is essential for extracting types from complex type structures. It enables powerful type-level programming and is crucial for building type-safe libraries and frameworks. Master infer to unlock advanced TypeScript patterns.

## Cheat Sheet

```typescript
// Basic infer
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Extract Promise type
type Unwrap<T> = T extends Promise<infer U> ? U : T;

// Extract array element
type Element<T> = T extends (infer E)[] ? E : never;

// Extract first tuple element
type Head<T> = T extends [infer H, ...any[]] ? H : never;

// Extract function parameters
type Params<T> = T extends (...args: infer P) => any ? P : never;

// Extract property type
type PropType<T, K> = T extends { [P in K]: infer V } ? V : never;

// Deep unwrap
type DeepUnwrap<T> = T extends Promise<infer U> ? DeepUnwrap<U> : T;

```

## References & Learn More

- [TypeScript Handbook: infer](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html#inferring-within-conditional-types)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/type-system/conditional-types)
- [TypeScript infer keyword explained](https://dev.to/nicolo-ribaudo/using-infer-in-typescript-3c90)
