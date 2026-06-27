# Conditional Types

## Definition

**Conditional types** are TypeScript types that select types based on conditions, similar to the ternary operator (`? :`) in JavaScript. They enable creating types that depend on type relationships.

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONDITIONAL TYPE SYNTAX                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   T extends U ? X : Y                                          │
│   │       │   │                                                │
│   │       │   └── Type if condition is true                    │
│   │       └────── Condition (is T assignable to U?)            │
│   └────────────── Type being checked                           │
│                                                                 │
│   Example:                                                      │
│   type IsString<T> = T extends string ? "yes" : "no";          │
│   type A = IsString<string>;  // "yes"                          │
│   type B = IsString<number>;  // "no"                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **Type computation**: Create types based on other types
2. **Type narrowing**: Filter types based on conditions
3. **Library design**: Create flexible, type-safe APIs
4. **Runtime to compile-time**: Map runtime logic to type system
5. **Complex transformations**: Build sophisticated type utilities

## How It Works

### Basic Syntax

```typescript
// Simple conditional type
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;  // true
type B = IsString<number>;  // false
type C = IsString<"hello">; // true (string literal extends string)
```

### Distributing Over Unions

```typescript
// Conditional types distribute over unions automatically
type ToArray<T> = T extends any ? T[] : never;

type StrArr = ToArray<string | number>;
// string[] | number[] (distributed)

// To prevent distribution, wrap in tuple
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type Result = ToArrayNonDist<string | number>;
// (string | number)[]
```

### Nested Conditionals

```typescript
// Multiple conditions
type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  T extends boolean ? "boolean" :
  T extends undefined ? "undefined" :
  T extends Function ? "function" :
  "object";

type A = TypeName<string>;    // "string"
type B = TypeName<() => void>; // "function"
type C = TypeName<string[]>;   // "object"
```

### The `infer` Keyword

```typescript
// Extract type using infer
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : any;

type Fn = () => string;
type Result = ReturnType<Fn>; // string

// More complex inference
type UnpackPromise<T> = T extends Promise<infer U> ? U : T;

type A = UnpackPromise<Promise<string>>;  // string
type B = UnpackPromise<number>;           // number
```

## Code Examples

### Practical Examples

```typescript
// ─── Type-safe event handling ─────────────────────────────────
type EventMap = {
  click: { x: number; y: number };
  scroll: { top: number };
  keypress: { key: string };
};

type EventHandler<T extends keyof EventMap> =
  (event: EventMap[T]) => void;

const handleClick: EventHandler<"click"> = (event) => {
  console.log(event.x, event.y); // ✅ TypeScript knows event has x, y
};

// ─── Conditional API response ─────────────────────────────────
type ApiResponse<T> =
  T extends "user" ? { name: string; email: string } :
  T extends "post" ? { title: string; content: string } :
  T extends "comment" ? { text: string; author: string } :
  never;

function fetchData<T extends "user" | "post" | "comment">(type: T): Promise<ApiResponse<T>> {
  return fetch(`/api/${type}`).then(r => r.json());
}

const user = await fetchData("user");
// { name: string; email: string }

// ─── Deep Readonly ────────────────────────────────────────────
type DeepReadonly<T> =
  T extends (infer U)[] ? ReadonlyArray<DeepReadonly<U>> :
  T extends object ? { readonly [K in keyof T]: DeepReadonly<T[K]> } :
  T;

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

type ReadonlyConfig = DeepReadonly<Config>;
// All nested properties are readonly

// ─── Extract function arguments ───────────────────────────────
type FirstArg<T> = T extends (first: infer F, ...rest: any[]) => any ? F : never;

type A = FirstArg<(name: string, age: number) => void>; // string
type B = FirstArg<() => void>; // never (no arguments)

// ─── Flatten arrays recursively ───────────────────────────────
type DeepFlatten<T> = T extends (infer U)[] ? DeepFlatten<U> : T;

type Nested = number[][][];
type Flat = DeepFlatten<Nested>; // number
```

### Complex Patterns

```typescript
// ─── Type-safe switch statement ────────────────────────────────
type Match<T, U> = T extends U ? T : U;

function processValue<T extends string | number>(value: T): Match<T, string> {
  if (typeof value === "string") {
    return value.toUpperCase() as Match<T, string>;
  }
  return String(value) as Match<T, string>;
}

// ─── Conditional mapped type ──────────────────────────────────
type NullableKeys<T> = {
  [K in keyof T]: null extends T[K] ? K : undefined extends T[K] ? K : never
}[keyof T];

interface User {
  name: string;
  email: string;
  phone: string | null;
  address?: string;
}

type OptionalAndNullableKeys = NullableKeys<User>;
// "phone" | "address"

// ─── Type-safe discriminated union helper ─────────────────────
type Discriminate<U, K extends string, V> =
  U extends { [P in K]: V } ? U : never;

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

type Circle = Discriminate<Shape, "kind", "circle">;
// { kind: "circle"; radius: number }

type Rectangle = Discriminate<Shape, "kind", "rectangle">;
// { kind: "rectangle"; width: number; height: number }
```

## Common Mistakes

### 1. Forgetting Distribution

```typescript
// ❌ Unexpected distribution
type IsNever<T> = T extends never ? true : false;
type A = IsNever<never>; // never (not true!)

// ✅ Fix: Wrap in tuple to prevent distribution
type IsNever<T> = [T] extends [never] ? true : false;
type B = IsNever<never>; // true
```

### 2. Using `any` Instead of `unknown`

```typescript
// ❌ Bad: `any` bypasses type checking
type BadReturnType<T> = T extends (...args: any[]) => any ? any : never;

// ✅ Good: Preserve type information
type GoodReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

### 3. Overcomplicating Conditionals

```typescript
// ❌ Bad: Too many nested ternaries
type Complex<T> =
  T extends string ? "str" :
  T extends number ? "num" :
  T extends boolean ? "bool" :
  T extends null ? "null" :
  T extends undefined ? "undef" :
  T extends Function ? "func" :
  T extends any[] ? "arr" :
  "obj";

// ✅ Better: Use a helper type
type Primitive = "str" | "num" | "bool";
type GetType<T> = T extends string ? "str" : T extends number ? "num" : "bool";
```

## Best Practices

```typescript
// 1. Use conditional types for type-safe APIs
type EventHandler<T> = T extends keyof WindowEventMap
  ? (event: WindowEventMap[T]) => void
  : never;

// 2. Combine with mapped types for powerful transformations
type OptionalExcept<T, K extends keyof T> =
  Omit<T, K> & Partial<Pick<T, K>>;

// 3. Use `infer` to extract types
type ElementOf<T> = T extends (infer E)[] ? E : never;

// 4. Create type guards with conditional types
type IsString<T> = T extends string ? true : false;

// 5. Document complex conditional types with comments
/**
 * Extracts the resolved type of a Promise or returns the type itself.
 */
type Resolve<T> = T extends Promise<infer U> ? Resolve<U> : T;
```

## Performance Considerations

- **Distribution**: Automatic distribution over unions can cause type explosion
- **Depth**: Deeply nested conditionals slow compilation
- **Instantiation**: Each conditional creates a new type instantiation
- **Caching**: TypeScript caches conditional type results
- **Infinite recursion**: Guard against infinite type recursion

## Interview Questions

### Beginner

1. **What is a conditional type?**
   - A type that selects types based on conditions using `extends ? :`

2. **How do you check if a type is a string?**
   ```typescript
   type IsString<T> = T extends string ? true : false;
   ```

3. **What is the `infer` keyword?**
   - Used in conditional types to extract/infer types

4. **Do conditional types distribute over unions?**
   - Yes, automatically

5. **How do you prevent distribution?**
   - Wrap the checked type in a tuple: `[T] extends [any]`

### Intermediate

6. **Write a type that extracts array element type**
   ```typescript
   type ElementOf<T> = T extends (infer E)[] ? E : never;
   ```

7. **How do you create a deep readonly type?**
   - Use recursive conditional types with mapped types

8. **What is the difference between `any` and `unknown` in conditional types?**
   - `unknown` preserves type safety; `any` bypasses it

9. **How do you extract function parameter types?**
   - Use `infer` with function type pattern: `T extends (...args: infer P) => any ? P : never`

10. **Can you have async conditional types?**
    - No, conditional types are evaluated at compile time

### Senior

11. **Explain distribution in conditional types**
    - When T is a union, the conditional type distributes over each union member

12. **How do you create a type-safe equals function?**
    - Use conditional types to enforce type equality

13. **Design a type that recursively makes all properties optional**
    - Use recursive conditional types with Partial

14. **How do you handle circular type references?**
    - Use interfaces or limit recursion depth

### FAANG-style

15. **Implement a type-safe deep merge**
    - Use conditional types to merge object types recursively

16. **Create a type-safe route matcher**
    - Parse route parameters and infer types

17. **Build a type-safe query language**
    - Use conditional types to validate query syntax

### Follow-ups

18. **How do conditional types interact with generics?**
    - Generic type parameters can be used in conditional type checks

19. **Can you use conditional types in mapped types?**
    - Yes: `{ [K in keyof T]: T[K] extends string ? string : number }`

20. **How do you debug complex conditional types?**
    - Use IDE hover, create intermediate type aliases, or use `@ts-expect-error`

## Summary

Conditional types are powerful for creating computed types. They enable type-level programming and are essential for advanced TypeScript patterns. Master `infer` and distribution to unlock the full potential of TypeScript's type system.

## Cheat Sheet

```typescript
// Basic conditional type
type IsString<T> = T extends string ? true : false;

// With infer
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : any;

// Prevent distribution
type NoDistribute<T> = [T] extends [any] ? true : false;

// Nested conditionals
type TypeName<T> =
  T extends string ? "string" :
  T extends number ? "number" :
  "other";

// Deep transformation
type DeepReadonly<T> =
  T extends object ? { readonly [K in keyof T]: DeepReadonly<T[K]> } :
  T;
```

## References & Learn More

- [TypeScript Handbook: Conditional Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)
- [TypeScript Deep Dive: Conditional Types](https://basarat.gitbook.io/typescript/type-system/conditional-types)
- [Advanced TypeScript Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html#inferring-within-conditional-types)
