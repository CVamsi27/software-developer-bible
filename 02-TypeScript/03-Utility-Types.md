# Utility Types

## Definition

**Utility types** are built-in TypeScript types that provide common type transformations. They allow you to manipulate and transform types without writing complex type logic from scratch.

```
┌─────────────────────────────────────────────────────────────────┐
│                    UTILITY TYPES CHEAT SHEET                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Partial<T>      - All properties optional                     │
│   Required<T>     - All properties required                     │
│   Readonly<T>     - All properties readonly                     │
│   Pick<T, K>      - Extract subset of properties                │
│   Omit<T, K>      - Remove subset of properties                 │
│   Record<K, T>    - Object with keys K and values T             │
│   Exclude<T, U>   - Remove types from union                     │
│   Extract<T, U>   - Extract types from union                    │
│   NonNullable<T>  - Remove null and undefined                   │
│   Parameters<T>   - Extract function parameter types            │
│   ReturnType<T>   - Extract function return type                │
│   InstanceType<T> - Extract class instance type                 │
│   Awaited<T>      - Unwrap Promise type                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **DRY principle**: Avoid repeating type transformations
2. **Type safety**: Perform complex type operations safely
3. **Code generation**: Create derived types from existing ones
4. **API design**: Transform types for DTOs, responses, etc.
5. **React patterns**: Type components, hooks, and state

## How It Works

### Partial<T>

```typescript
// Makes all properties optional
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

type PartialUser = Partial<User>;
// {
//   id?: string;
//   name?: string;
//   email?: string;
//   age?: number;
// }

// Real-world: Update function
function updateUser(id: string, updates: Partial<User>): Promise<User> {
  // Can update any subset of fields
  return Promise.resolve({ id, name: "Alice", email: "a@b.com", age: 30 });
}

updateUser("1", { name: "Bob" });           // ✅ Only update name
updateUser("1", { email: "new@b.com" });    // ✅ Only update email
updateUser("1", { name: "Bob", age: 25 });  // ✅ Update multiple
```

### Required<T>

```typescript
// Makes all properties required
interface Config {
  host?: string;
  port?: number;
  debug?: boolean;
}

type RequiredConfig = Required<Config>;
// {
//   host: string;
//   port: number;
//   debug: boolean;
// }

// Real-world: Ensure all options are provided
function createServer(config: RequiredConfig): Server {
  // config.host is guaranteed to be string
  return new Server(config.host, config.port, config.debug);
}
```

### Readonly<T>

```typescript
// Makes all properties readonly
interface Point {
  x: number;
  y: number;
}

type ReadonlyPoint = Readonly<Point>;
// {
//   readonly x: number;
//   readonly y: number;
// }

const point: ReadonlyPoint = { x: 1, y: 2 };
point.x = 3; // ❌ Error: Cannot assign to 'x' because it is a read-only property

// Real-world: Immutable state
function useState<T>(initial: T): [Readonly<T>, (new: T) => void] {
  let state = initial;
  const setState = (newState: T) => { state = newState; };
  return [state, setState];
}
```

### Pick<T, K>

```typescript
// Extracts a subset of properties
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

type UserPreview = Pick<User, "id" | "name" | "email">;
// {
//   id: string;
//   name: string;
//   email: string;
// }

// Real-world: API response with limited fields
function getUserPreview(id: string): Promise<UserPreview> {
  return fetch(`/api/users/${id}?fields=id,name,email`);
}
```

### Omit<T, K>

```typescript
// Removes a subset of properties
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

type CreateUserDTO = Omit<User, "id" | "createdAt">;
// {
//   name: string;
//   email: string;
//   password: string;
// }

// Real-world: Create entity without auto-generated fields
function createUser(data: CreateUserDTO): Promise<User> {
  return fetch("/api/users", {
    method: "POST",
    body: JSON.stringify({
      ...data,
      id: generateId(),
      createdAt: new Date()
    })
  });
}
```

### Record<K, T>

```typescript
// Creates an object type with keys K and values T
type Fruit = "apple" | "banana" | "orange";
type FruitCount = Record<Fruit, number>;
// {
//   apple: number;
//   banana: number;
//   orange: number;
// }

const inventory: FruitCount = {
  apple: 10,
  banana: 5,
  orange: 8
};

// Real-world: Lookup tables
type UserRoles = Record<string, "admin" | "user" | "guest">;
const roles: UserRoles = {
  "user1": "admin",
  "user2": "user",
  "user3": "guest"
};

// With nested objects
type StatusMessages = Record<
  "success" | "error" | "warning",
  { message: string; code: number }
>;
```

### Exclude<T, U>

```typescript
// Removes types from a union
type Status = "active" | "inactive" | "pending" | "deleted";
type ActiveStatus = Exclude<Status, "deleted" | "pending">;
// "active" | "inactive"

// Real-world: Filter options
type AllSortFields = "name" | "email" | "createdAt" | "password";
type SafeSortFields = Exclude<AllSortFields, "password">;
// "name" | "email" | "createdAt"

function sortBy(field: SafeSortFields): void {
  // Can't sort by password
}
```

### Extract<T, U>

```typescript
// Extracts types from a union
type Status = "active" | "inactive" | "pending" | "deleted";
type ActiveStatus = Extract<Status, "active" | "inactive">;
// "active" | "inactive"

// Real-world: Filter event types
type Event = "click" | "scroll" | "resize" | "load";
type MouseEvents = Extract<Event, "click" | "scroll">;
// "click" | "scroll"
```

### NonNullable<T>

```typescript
// Removes null and undefined from a type
type MaybeString = string | null | undefined;
type DefinitelyString = NonNullable<MaybeString>;
// string

// Real-world: After null checks
function processValue(value: string | null): string {
  if (value === null) {
    throw new Error("Value is null");
  }
  // value is string (NonNullable applied by control flow)
  return value.toUpperCase();
}
```

### Parameters<T>

```typescript
// Extracts function parameter types as a tuple
function createUser(name: string, age: number, email: string): User {
  return { id: "1", name, age, email, createdAt: new Date() };
}

type CreateUserParams = Parameters<typeof createUser>;
// [string, number, string]

// Real-world: Type-safe function wrappers
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

### ReturnType<T>

```typescript
// Extracts function return type
function getUser(id: string): Promise<User> {
  return fetch(`/api/users/${id}`).then(r => r.json());
}

type GetUserReturn = ReturnType<typeof getUser>;
// Promise<User>

// Real-world: Type inference from functions
function createInitialState() {
  return {
    items: [] as string[],
    loading: false,
    error: null as string | null
  };
}

type State = ReturnType<typeof createInitialState>;
// { items: string[]; loading: boolean; error: string | null }
```

### InstanceType<T>

```typescript
// Extracts instance type from a class
class User {
  constructor(
    public name: string,
    public email: string
  ) {}
}

type UserInstance = InstanceType<typeof User>;
// User

// Real-world: Dependency injection
function createUserService(UserModel: new (...args: any[]) => User): UserInstance {
  return new UserModel("default", "default@example.com");
}
```

### Awaited<T>

```typescript
// Unwraps Promise type (recursive)
type A = Awaited<Promise<string>>;           // string
type B = Awaited<Promise<Promise<number>>>;  // number
type C = Awaited<string | Promise<number>>;  // string | number

// Real-world: Async function return types
async function fetchData(): Promise<Promise<string>> {
  return Promise.resolve("data");
}

type DataType = Awaited<ReturnType<typeof fetchData>>;
// string
```

## Code Examples

### Comprehensive Transformation Example

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  role: "admin" | "user" | "guest";
  createdAt: Date;
}

// Different views of the same entity
type UserPublic = Omit<User, "password">;
type CreateUserDTO = Omit<User, "id" | "createdAt">;
type UpdateUserDTO = Partial<CreateUserDTO>;
type UserPreview = Pick<User, "id" | "name" | "email">;
type UserRoles = Record<User["id"], User["role"]>;

// API response types
type ApiResponse<T> = {
  data: T;
  status: number;
  message: string;
};

type UserResponse = ApiResponse<User>;
type UserListResponse = ApiResponse<User[]>;

// Function types
type GetUserById = (id: string) => Promise<User | null>;
type GetUserParams = Parameters<GetUserById>;  // [string]
type GetUserReturn = ReturnType<GetUserById>;  // Promise<User | null>
```

### React Patterns

```typescript
// Component props
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

// Make all props except 'label' optional
type ButtonPropsPartial = Omit<ButtonProps, "label"> & Partial<Pick<ButtonProps, "label">>;

// Hook return type
function useUser(id: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUser(id).then(setUser).finally(() => setLoading(false));
  }, [id]);

  return { user, loading, error };
}

type UseUserReturn = ReturnType<typeof useUser>;
// { user: User | null; loading: boolean; error: string | null }
```

## Common Mistakes

### 1. Overusing Partial

```typescript
// ❌ Bad: Partial makes everything optional, losing type safety
function updateUser(user: Partial<User>) {
  // user.id might be undefined!
  return db.update(user.id, user);
}

// ✅ Good: Separate required and optional fields
function updateUser(id: string, updates: Omit<Partial<User>, "id">) {
  return db.update(id, updates);
}
```

### 2. Mixing Utility Types Unnecessarily

```typescript
// ❌ Bad: Complex nested utility types
type Complex = Partial<Omit<Required<User>, "password">>;

// ✅ Better: Create explicit type
type UserUpdate = {
  name?: string;
  email?: string;
  role?: User["role"];
};
```

### 3. Forgetting Utility Types Exist

```typescript
// ❌ Bad: Manual type transformation
type UserWithoutPassword = {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user" | "guest";
  createdAt: Date;
};

// ✅ Good: Use utility type
type UserWithoutPassword = Omit<User, "password">;
```

## Best Practices

```typescript
// 1. Use descriptive type names
type CreateUserDTO = Omit<User, "id" | "createdAt">;
type UserPublicProfile = Pick<User, "id" | "name" | "email">;

// 2. Combine utility types logically
type UpdateUserDTO = Partial<Omit<User, "id" | "createdAt">>;

// 3. Use Record for lookup tables
type UserMap = Record<string, User>;

// 4. Use Extract/Exclude for filtering unions
type SafeSortFields = Exclude<SortField, "password" | "email">;

// 5. Use Parameters/ReturnType for function types
type Handler = (...args: Parameters<typeof originalHandler>) => void;
```

## Performance Considerations

- **Compilation**: Utility types are resolved at compile time
- **Memory**: No runtime overhead — types are erased
- **Complexity**: Deeply nested utility types can slow compilation
- **IDE**: Complex utility types may affect IDE performance
- **Tree shaking**: No impact on bundle size

## Interview Questions

### Beginner

1. **What is Partial<T>?**
   - Makes all properties of T optional

2. **What is the difference between Pick and Omit?**
   - Pick extracts specified properties; Omit removes them

3. **How do you make all properties required?**
   - Use `Required<T>`

4. **What does Record<K, V> create?**
   - An object type with keys K and values V

5. **How do you extract function parameter types?**
   - Use `Parameters<T>`

### Intermediate

6. **When would you use Exclude vs Extract?**
   - Exclude removes types from a union; Extract keeps only matching types

7. **How do you create a type with all readonly properties?**
   - Use `Readonly<T>`

8. **What does NonNullable<T> do?**
   - Removes null and undefined from a type

9. **How do you get the return type of an async function?**
   - Use `ReturnType<T>` which gives `Promise<T>`, or `Awaited<ReturnType<T>>` to unwrap

10. **Can you chain utility types?**
    - Yes: `Partial<Omit<User, "id">>`

### Senior

11. **Design a type system for a CRUD API using utility types**
    - Entity, CreateDTO, UpdateDTO, Response types

12. **How would you implement a type-safe deep partial?**
    - Use recursive mapped types with Partial

13. **Explain the relationship between Pick and Omit**
    - `Omit<T, K>` is equivalent to `Pick<T, Exclude<keyof T, K>>`

14. **How do you type a function that transforms an object?**
    - Use mapped types with conditional types

### FAANG-style

15. **Build a type-safe form validation system**
    - Use Partial for optional fields, Record for error maps

16. **Implement a type-safe state management solution**
    - Use utility types for state, actions, and reducers

17. **Create a type-safe API client**
    - Use ReturnType, Parameters for method signatures

### Follow-ups

18. **How do utility types interact with generics?**
    - Utility types can be used inside generic constraints

19. **Can you create custom utility types?**
    - Yes: Use mapped types, conditional types, and infer

20. **How do you debug complex utility types?**
    - Use IDE hover, or create intermediate type aliases

## Summary

Utility types are essential tools for type transformation in TypeScript. Master them to write cleaner, more maintainable code. They're especially useful for creating DTOs, API responses, and React component props.

## Cheat Sheet

```typescript
// Object transformations
Partial<T>     // All optional
Required<T>    // All required
Readonly<T>    // All readonly
Pick<T, K>     // Extract K from T
Omit<T, K>     // Remove K from T
Record<K, V>   // { [key: K]: V }

// Union transformations
Exclude<T, U>  // Remove U from T
Extract<T, U>  // Keep only U from T
NonNullable<T> // Remove null | undefined

// Function transformations
Parameters<T>    // Function parameter types
ReturnType<T>    // Function return type
InstanceType<T>  // Class instance type

// Promise unwrapping
Awaited<T>       // Unwrap Promise recursively
```

## References & Learn More

- [TypeScript Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [TypeScript Built-in Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
- [TypeScript Cheat Sheet](https://www.typescriptlang.org/cheatsheets)
