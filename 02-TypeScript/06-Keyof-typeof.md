# Keyof & Typeof

## Definition

- **`keyof`**: A type operator that extracts the keys of an object type as a union of string literal types
- **`typeof`**: A type operator that extracts the type of a value/expression

```
┌─────────────────────────────────────────────────────────────────┐
│                   KEYOF vs TYPEOF                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   keyof T                        typeof value                   │
│   │                              │                              │
│   └── Extracts keys as union    └── Extracts type of value     │
│                                                                 │
│   interface User {               const user = {                 │
│     name: string;                 name: "Alice",                │
│     age: number;                  age: 30                       │
│   }                             };                              │
│                                                                 │
│   type Keys = keyof User;        type User = typeof user;       │
│   // "name" | "age"              // { name: string; age: number }│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **Type safety**: Safely reference object keys and values
2. **Code reuse**: Create types from existing values
3. **Mapped types**: Use keys to iterate over object properties
4. **Type inference**: Let TypeScript infer types from runtime values
5. **Refactoring**: Automatically update types when values change

## How It Works

### keyof

```typescript
// Extract keys as union
interface User {
  name: string;
  age: number;
  email: string;
}

type UserKeys = keyof User;
// "name" | "age" | "email"

// Use in generic functions
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { name: "Alice", age: 30, email: "a@b.com" };
const name = getProperty(user, "name");  // string
const age = getProperty(user, "age");    // number
```

### typeof

```typescript
// Extract type of a value
const config = {
  host: "localhost",
  port: 3000,
  debug: true
};

type Config = typeof config;
// {
//   host: string;
//   port: number;
//   debug: boolean;
// }

// Use with class instances
class User {
  constructor(
    public name: string,
    public email: string
  ) {}
}

const user = new User("Alice", "a@b.com");
type UserType = typeof user; // User

// Use with functions
function createUser(name: string) {
  return { name, createdAt: new Date() };
}

type CreateUserReturn = ReturnType<typeof createUser>;
// { name: string; createdAt: Date }
```

### keyof in Mapped Types

```typescript
// Create type with all properties set to a specific type
type Record<K extends keyof any, T> = {
  [P in K]: T;
};

interface User {
  name: string;
  age: number;
  email: string;
}

// All properties as booleans
type UserFlags = Record<keyof User, boolean>;
// {
//   name: boolean;
//   age: boolean;
//   email: boolean;
// }

// All properties as optional
type PartialUser = {
  [K in keyof User]?: User[K];
};
```

### Key Remapping with `as`

```typescript
// Transform keys using `as`
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
type NullableKeys<T> = {
  [K in keyof T as null extends T[K] ? K : never]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  phone: string | null;
}

type Nullable = NullableKeys<Mixed>;
// { phone: string | null }
```

### typeof with keyof

```typescript
// Combine typeof and keyof for type-safe property access
const routes = {
  home: "/",
  about: "/about",
  contact: "/contact"
} as const;

type Route = keyof typeof routes;
// "home" | "about" | "contact"

function navigate(route: Route): void {
  window.location.href = routes[route];
}

navigate("home");    // ✅
navigate("about");   // ✅
navigate("missing"); // ❌ Error
```

## Code Examples

### Practical Patterns

```typescript
// ─── Type-safe object manipulation ────────────────────────────
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

const user = { name: "Alice", age: 30, email: "a@b.com" };
const preview = pick(user, ["name", "email"]);
// { name: string; email: string }

// ─── Type-safe event emitter ──────────────────────────────────
class TypedEmitter<Events extends Record<string, any>> {
  private listeners = new Map<string, Function[]>();

  on<K extends keyof Events>(
    event: K,
    listener: (payload: Events[K]) => void
  ): void {
    if (!this.listeners.has(event as string)) {
      this.listeners.set(event as string, []);
    }
    this.listeners.get(event as string)!.push(listener);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.listeners.get(event as string)?.forEach(fn => fn(payload));
  }
}

interface AppEvents {
  "user:created": { userId: string };
  "user:deleted": { userId: string };
  "order:placed": { orderId: string; amount: number };
}

const emitter = new TypedEmitter<AppEvents>();
emitter.on("user:created", (data) => {
  console.log(data.userId); // ✅ TypeScript knows data.userId exists
});
emitter.emit("user:created", { userId: "123" }); // ✅ Type-safe

// ─── Type-safe configuration ──────────────────────────────────
const defaultConfig = {
  host: "localhost",
  port: 3000,
  debug: false,
  logLevel: "info"
} as const;

type ConfigKey = keyof typeof defaultConfig;
type ConfigValue = typeof defaultConfig[ConfigKey];

function getConfig(key: ConfigKey): ConfigValue {
  return defaultConfig[key];
}

const host = getConfig("host");     // string
const port = getConfig("port");     // number
```

### Advanced Patterns

```typescript
// ─── Type-safe property accessor ──────────────────────────────
type PropertyAccessor<T> = {
  [K in keyof T]: {
    get: () => T[K];
    set: (value: T[K]) => void;
  };
};

function createAccessor<T extends object>(obj: T): PropertyAccessor<T> {
  const result = {} as PropertyAccessor<T>;
  for (const key of Object.keys(obj) as (keyof T)[]) {
    result[key] = {
      get: () => obj[key],
      set: (value) => { (obj as any)[key] = value; }
    };
  }
  return result;
}

// ─── Type-safe enum-like objects ──────────────────────────────
const Status = {
  Active: "ACTIVE",
  Inactive: "INACTIVE",
  Pending: "PENDING"
} as const;

type StatusValue = typeof Status[keyof typeof Status];
// "ACTIVE" | "INACTIVE" | "PENDING"

function isValidStatus(value: string): value is StatusValue {
  return Object.values(Status).includes(value as StatusValue);
}

// ─── Type-safe route parameters ───────────────────────────────
function createRoute<T extends string>(
  route: T
): T extends `${string}:${infer Param}`
  ? { path: T; params: Record<Param, string> }
  : { path: T; params?: never } {
  // Implementation
  return { path: route } as any;
}

const userRoute = createRoute("/users/:id");
// { path: "/users/:id"; params: { id: string } }

const homeRoute = createRoute("/home");
// { path: "/home"; params?: never }
```

## Common Mistakes

### 1. Using keyof on Non-Object Types

```typescript
// ❌ Error: keyof on non-object
type Bad = keyof string; // "toString" | "charAt" | ... (not useful)

// ✅ Correct: Use keyof on interfaces/types
interface User { name: string; age: number; }
type Keys = keyof User; // "name" | "age"
```

### 2. Not Constraining Generic Keys

```typescript
// ❌ Bad: No constraint on K
function getProp<T, K>(obj: T, key: K) {
  return obj[key]; // Error: K might not be a key of T
}

// ✅ Good: Constrain K
function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### 3. Forgetting typeof Returns the Value Type

```typescript
// ❌ Confusion: typeof returns the type of the VALUE
const str = "hello";
type T1 = typeof str; // "hello" (the literal type), not string

// ✅ To get the primitive type, use string directly
type T2 = string; // string
```

## Best Practices

```typescript
// 1. Use keyof for type-safe property access
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// 2. Use typeof to create types from runtime values
const config = { host: "localhost", port: 3000 };
type Config = typeof config;

// 3. Combine keyof and typeof for enums
const STATUS = { Active: "active", Inactive: "inactive" } as const;
type Status = typeof STATUS[keyof typeof STATUS];

// 4. Use key remapping with `as` for transformations
type PrefixKeys<T> = {
  [K in keyof T as `prefix_${string & K}`]: T[K];
};

// 5. Use mapped types with keyof for bulk transformations
type Optional<T> = {
  [K in keyof T]?: T[K];
};
```

## Performance Considerations

- **Compilation**: keyof and typeof are resolved at compile time
- **IDE**: Fast hover and autocomplete support
- **Complex types**: Deep keyof chains can slow compilation
- **Large objects**: typeof on large objects can create complex types
- **Union size**: keyof on large types creates large unions

## Interview Questions

### Beginner

1. **What does `keyof` do?**
   - Extracts the keys of an object type as a union

2. **What does `typeof` do?**
   - Extracts the type of a value/expression

3. **How do you safely access object properties?**
   - Use `K extends keyof T` constraint

4. **Can you use keyof on arrays?**
   - Yes, it returns array method names and indices

5. **How do you create a type from a const object?**
   - Use `typeof obj[keyof typeof obj]`

### Intermediate

6. **Write a type-safe getProperty function**
   ```typescript
   function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
     return obj[key];
   }
   ```

7. **How do you filter keys in a mapped type?**
   - Use key remapping with `as`: `[K in keyof T as Condition ? K : never]`

8. **What is the difference between keyof T and keyof any?**
   - keyof T extracts keys of specific type; keyof any is string | number | symbol

9. **How do you create an enum-like type from an object?**
   - Use `typeof obj[keyof typeof obj]`

10. **Can you use typeof in type annotations?**
    - Yes: `const x: typeof y = y;`

### Senior

11. **Design a type-safe property validator**
    - Use keyof and mapped types to validate object properties

12. **How do you create a type-safe event system?**
    - Use keyof for event names, typeof for payloads

13. **Implement a type-safe deep property access**
    - Use recursive keyof with template literals

14. **How do you handle dynamic property names?**
    - Use computed property names with keyof constraints

### FAANG-style

15. **Build a type-safe form builder**
    - Use keyof for field names, typeof for default values

16. **Create a type-safe API router**
    - Use typeof for route definitions, keyof for parameter extraction

17. **Implement a type-safe state management solution**
    - Use keyof for action types, typeof for payloads

### Follow-ups

18. **How do keyof and typeof interact with generics?**
    - Both work with generic types and values

19. **Can you use keyof with intersection types?**
    - Yes, keyof distributes over intersections

20. **How do you handle symbol keys with keyof?**
    - keyof includes symbol keys in the union

## Summary

`keyof` and `typeof` are fundamental TypeScript operators for type-safe property access and type inference. They enable powerful patterns like type-safe object manipulation, enum-like objects, and generic constraints. Master them to write more robust TypeScript code.

## Cheat Sheet

```typescript
// keyof: Extract object keys
interface User { name: string; age: number; }
type Keys = keyof User; // "name" | "age"

// typeof: Extract value type
const user = { name: "Alice", age: 30 };
type UserType = typeof user; // { name: string; age: number }

// Type-safe property access
function get<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }

// Enum-like objects
const STATUS = { Active: "active", Inactive: "inactive" } as const;
type Status = typeof STATUS[keyof typeof STATUS];

// Key remapping
type Prefix<T> = { [K in keyof T as `get_${string & K}`]: () => T[K] };

// typeof with keyof for const objects
const routes = { home: "/", about: "/about" } as const;
type Route = keyof typeof routes;
```

## References & Learn More

- [TypeScript Handbook: keyof](https://www.typescriptlang.org/docs/handbook/2/keyof-types.html)
- [TypeScript Handbook: typeof](https://www.typescriptlang.org/docs/handbook/2/typeof-types.html)
- [TypeScript Deep Dive: Keyof](https://basarat.gitbook.io/typescript/type-system/index-signatures)
