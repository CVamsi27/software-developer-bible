# Mapped Types

## Definition

**Mapped types** are types that transform existing types by iterating over their keys using `[K in keyof T]` syntax. They allow you to create new types by mapping over every property in a type.

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAPPED TYPE SYNTAX                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   {                                                              │
│     [K in keyof T]: NewType                                     │
│     │     │      │                                              │
│     │     │      └── Type for each property                     │
│     │     └────────── Iterate over all keys of T               │
│     └──────────────── Key variable                             │
│   }                                                              │
│                                                                 │
│   Example:                                                      │
│   type Optional<T> = {                                          │
│     [K in keyof T]?: T[K]                                       │
│   };                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **Type transformation**: Create derived types from existing ones
2. **Bulk operations**: Apply changes to all properties at once
3. **Type safety**: Maintain type information through transformations
4. **Code reuse**: Build utility types from mapped types
5. **Library design**: Create flexible, type-safe APIs

## How It Works

### Basic Syntax

```typescript
// Make all properties optional
type Optional<T> = {
  [K in keyof T]?: T[K];
};

interface User {
  name: string;
  age: number;
  email: string;
}

type OptionalUser = Optional<User>;
// {
//   name?: string;
//   age?: number;
//   email?: string;
// }

// Make all properties required
type Required<T> = {
  [K in keyof T]-?: T[K];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};
```

### Iteration Syntax

```typescript
// Basic iteration
type Stringify<T> = {
  [K in keyof T]: string;
};

interface User {
  name: string;
  age: number;
}

type StringUser = Stringify<User>;
// {
//   name: string;
//   age: string;
// }

// With constraints
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};

type UserPreview = Pick<User, "name" | "email">;
// {
//   name: string;
//   email: string;
// }
```

### Key Remapping with `as`

```typescript
// Transform keys
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User {
  name: string;
  age: number;
}

type UserGetters = Getters<User>;
// {
//   getName: () => string;
//   getAge: () => number;
}

// Filter keys
type NonFunctionKeys<T> = {
  [K in keyof T as T[K] extends Function ? never : K]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  greet: () => void;
}

type DataOnly = NonFunctionKeys<Mixed>;
// {
//   name: string;
//   age: number;
// }

// Rename keys
type Renamed<T> = {
  [K in keyof T as `${string & K}Key`]: T[K];
};
```

### Adding Modifiers

```typescript
// Remove readonly
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

// Remove optional
type Concrete<T> = {
  [K in keyof T]-?: T[K];
};

// Make all properties optional and nullable
type Weak<T> = {
  [K in keyof T]?: T[K] | null;
};

interface User {
  name: string;
  age: number;
}

type WeakUser = Weak<User>;
// {
//   name?: string | null;
//   age?: number | null;
// }
```

## Code Examples

### Practical Examples

```typescript
// ─── Type-safe object manipulation ────────────────────────────
function mapValues<T, U>(
  obj: T,
  fn: (value: T[keyof T], key: keyof T) => U
): { [K in keyof T]: U } {
  const result = {} as { [K in keyof T]: U };
  for (const key in obj) {
    result[key] = fn(obj[key], key);
  }
  return result;
}

const user = { name: "Alice", age: 30, email: "a@b.com" };
const lengths = mapValues(user, (value) =>
  typeof value === "string" ? value.length : value
);
// { name: number; age: number; email: number }

// ─── Type-safe API response transformation ────────────────────
type ApiResponse<T> = {
  [K in keyof T]: {
    data: T[K];
    status: number;
    timestamp: Date;
  };
};

interface UserData {
  user: User;
  posts: Post[];
  comments: Comment[];
}

type UserResponses = ApiResponse<UserData>;
// {
//   user: { data: User; status: number; timestamp: Date };
//   posts: { data: Post[]; status: number; timestamp: Date };
//   comments: { data: Comment[]; status: number; timestamp: Date };
// }

// ─── Type-safe form state ─────────────────────────────────────
type FormState<T> = {
  [K in keyof T]: {
    value: T[K];
    error: string | null;
    touched: boolean;
    dirty: boolean;
  };
};

interface LoginForm {
  email: string;
  password: string;
  rememberMe: boolean;
}

type LoginFormState = FormState<LoginForm>;
// {
//   email: { value: string; error: string | null; touched: boolean; dirty: boolean };
//   password: { value: string; error: string | null; touched: boolean; dirty: boolean };
//   rememberMe: { value: boolean; error: string | null; touched: boolean; dirty: boolean };
// }

function createFormState<T extends Record<string, any>>(defaults: T): FormState<T> {
  const state = {} as FormState<T>;
  for (const key in defaults) {
    state[key] = {
      value: defaults[key],
      error: null,
      touched: false,
      dirty: false
    };
  }
  return state;
}

const form = createFormState({
  email: "",
  password: "",
  rememberMe: false
});
```

### Advanced Patterns

```typescript
// ─── Deep mapped type ─────────────────────────────────────────
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// ─── Conditional mapped type ──────────────────────────────────
type NullableStrings<T> = {
  [K in keyof T]: T[K] extends string ? T[K] | null : T[K];
};

interface Config {
  host: string;
  port: number;
  debug: boolean;
}

type NullableConfig = NullableStrings<Config>;
// {
//   host: string | null;
//   port: number;
//   debug: boolean;
// }

// ─── Type-safe event emitter ──────────────────────────────────
type EventMap = {
  "user:created": { userId: string };
  "user:deleted": { userId: string };
  "order:placed": { orderId: string; amount: number };
};

type EventHandler<T> = (payload: T) => void;

type TypedEventHandlers<Events> = {
  [K in keyof Events as `${string & K}`]: EventHandler<Events[K]>;
};

type Handlers = TypedEventHandlers<EventMap>;
// {
//   "user:created": EventHandler<{ userId: string }>;
//   "user:deleted": EventHandler<{ userId: string }>;
//   "order:placed": EventHandler<{ orderId: string; amount: number }>;
// }

// ─── Type-safe router ─────────────────────────────────────────
type RouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof RouteParams<Rest>]: string }
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

type Params1 = RouteParams<"users/:id">;
// { id: string }

type Params2 = RouteParams<"users/:id/posts/:postId">;
// { id: string; postId: string }
```

### Utility Type Implementations

```typescript
// ─── Partial ──────────────────────────────────────────────────
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};

// ─── Required ─────────────────────────────────────────────────
type MyRequired<T> = {
  [K in keyof T]-?: T[K];
};

// ─── Readonly ─────────────────────────────────────────────────
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};

// ─── Pick ─────────────────────────────────────────────────────
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};

// ─── Record ───────────────────────────────────────────────────
type MyRecord<K extends keyof any, T> = {
  [P in K]: T;
};
```

## Common Mistakes

### 1. Forgetting to Use T[K]

```typescript
// ❌ Bad: All properties become string
type Bad<T> = {
  [K in keyof T]: string;
};

// ✅ Good: Preserve original types
type Good<T> = {
  [K in keyof T]: T[K];
};
```

### 2. Not Handling Nested Objects

```typescript
// ❌ Bad: Only makes top-level properties optional
type ShallowPartial<T> = {
  [K in keyof T]?: T[K];
};

interface Config {
  database: {
    host: string;
    port: number;
  };
}

type PartialConfig = ShallowPartial<Config>;
// database is still required, only host/port are optional

// ✅ Good: Deep partial
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

### 3. Overusing Mapped Types

```typescript
// ❌ Bad: Unnecessary mapped type
type StringUser = {
  [K in "name" | "age"]: string;
};

// ✅ Better: Simple object type
type StringUser = {
  name: string;
  age: string;
};
```

## Best Practices

```typescript
// 1. Use mapped types for bulk transformations
type Optional<T> = { [K in keyof T]?: T[K] };

// 2. Combine with conditional types for filtering
type OptionalStrings<T> = {
  [K in keyof T]: T[K] extends string ? T[K] | undefined : T[K];
};

// 3. Use key remapping for transformations
type PrefixKeys<T> = {
  [K in keyof T as `prefix_${string & K}`]: T[K];
};

// 4. Document complex mapped types
/**
 * Makes all properties deeply readonly.
 */
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// 5. Use helper types for complex transformations
type NullableKeys<T> = {
  [K in keyof T]: null extends T[K] ? K : never
}[keyof T];
```

## Performance Considerations

- **Compilation**: Mapped types are resolved at compile time
- **Depth**: Deeply nested mapped types slow compilation
- **Size**: Large objects create complex mapped types
- **IDE**: Complex mapped types may affect IDE performance
- **Caching**: TypeScript caches mapped type results

## Interview Questions

### Beginner

1. **What is a mapped type?**
   - A type that transforms existing types by iterating over their keys

2. **How do you make all properties optional?**
   ```typescript
   type Optional<T> = { [K in keyof T]?: T[K] };
   ```

3. **What does `[K in keyof T]` mean?**
   - Iterate over all keys K in type T

4. **How do you preserve property types in a mapped type?**
   - Use `T[K]` to reference the original type

5. **What is key remapping?**
   - Using `as` to transform key names in mapped types

### Intermediate

6. **Write a type that makes all properties required**
   ```typescript
   type Required<T> = { [K in keyof T]-?: T[K] };
   ```

7. **How do you filter properties in a mapped type?**
   - Use key remapping with conditional: `[K in keyof T as Condition ? K : never]`

8. **What is the difference between `?` and `-?`?**
   - `?` adds optional modifier; `-?` removes it

9. **How do you make all properties readonly?**
   ```typescript
   type Readonly<T> = { readonly [K in keyof T]: T[K] };
   ```

10. **Can you nest mapped types?**
    - Yes: Use recursion for deep transformations

### Senior

11. **Design a type-safe form validation system**
    - Use mapped types for field states, error types

12. **How do you create a type-safe ORM query builder?**
    - Use mapped types for column selections, joins

13. **Implement a type-safe state management solution**
    - Use mapped types for state, actions, reducers

14. **How do you handle deeply nested objects?**
    - Use recursive mapped types with conditional types

### FAANG-style

15. **Build a type-safe API client**
    - Use mapped types for request/response transformations

16. **Create a type-safe configuration system**
    - Use mapped types for config validation, defaults

17. **Implement a type-safe event system**
    - Use mapped types for event handlers, payloads

### Follow-ups

18. **How do mapped types interact with generics?**
    - Generic type parameters can be used in mapped types

19. **Can you use mapped types with unions?**
    - Yes, but behavior may be unexpected

20. **How do you debug complex mapped types?**
    - Create intermediate type aliases, use IDE hover

## Summary

Mapped types are essential for type transformation in TypeScript. They enable bulk operations on object properties and are the foundation for many utility types. Master them to create flexible, type-safe code.

## Cheat Sheet

```typescript
// Basic mapped type
type Mapped<T> = { [K in keyof T]: T[K] };

// Add optional modifier
type Optional<T> = { [K in keyof T]?: T[K] };

// Add required modifier
type Required<T> = { [K in keyof T]-?: T[K] };

// Add readonly modifier
type Readonly<T> = { readonly [K in keyof T]: T[K] };

// Remove readonly modifier
type Mutable<T> = { -readonly [K in keyof T]: T[K] };

// Key remapping
type Prefix<T> = { [K in keyof T as `get_${string & K}`]: () => T[K] };

// Filter keys
type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

// Deep mapped type
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

## References & Learn More

- [TypeScript Handbook: Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
- [Key Remapping in Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html#key-remapping-via-as)
- [TypeScript Deep Dive: Mapped Types](https://basarat.gitbook.io/typescript/type-system/mapped-types)
