# Types vs Interfaces

[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

## Definition

**Type aliases (`type`)** and **interfaces (`interface`)** are TypeScript constructs that describe the shape of objects and other data structures. While they overlap significantly in functionality, they have distinct features and use cases.

- **`type`**: A type alias that can represent any TypeScript type — primitives, unions, intersections, tuples, functions, and more.
- **`interface`**: A named contract for object shapes that supports declaration merging, extension via `extends`, and is specifically designed for object-oriented patterns.

```text
┌─────────────────────────────────────────────────────────────────┐
│                     TYPE vs INTERFACE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   type User = {           interface User {                      │
│     name: string;           name: string;                       │
│     age: number;            age: number;                        │
│   }                       }                                    │
│                                                                 │
│   ✅ Primitives            ❌ Primitives                        │
│   ✅ Unions                ❌ Unions                            │
│   ✅ Intersections         ❌ Intersections (use extends)       │
│   ✅ Tuples                ❌ Tuples                            │
│   ✅ Mapped types          ❌ Mapped types                      │
│   ❌ Declaration merging   ✅ Declaration merging               │
│   ✅ Computed properties   ❌ Computed properties               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

## Why Do We Need It?

1. **Type safety**: Both enforce contracts at compile time

2. **Code documentation**: Self-documenting code with explicit shapes

3. **IDE support**: Autocomplete, refactoring, and error detection

4. **Scalability**: Essential for large codebases and team collaboration

5. **Framework integration**: React props, API responses, database models

## How It Works

### Syntax Differences

```typescript
// ─── Type Alias ───────────────────────────────────────────────
type StringOrNumber = string | number;
type Point = { x: number; y: number };
type Pair<T> = [T, T];

// ─── Interface ────────────────────────────────────────────────
interface StringOrNumberInterface {} // ❌ Cannot represent unions
interface PointInterface {
  x: number;
  y: number;
}

```

### Declaration Merging (Interface Only)

```typescript
interface Window {
  title: string;
}
interface Window {
  close(): void;
}
// Result: Window has both `title` and `close()`

// Type aliases cannot merge — second declaration causes error
type Config = { debug: boolean };
type Config = { verbose: boolean }; // ❌ Duplicate identifier

```

### Extends vs Intersection

```typescript
// ─── Interface Extends ────────────────────────────────────────
interface Animal {
  name: string;
}
interface Dog extends Animal {
  breed: string;
}

// ─── Type Intersection ────────────────────────────────────────
type Animal = { name: string };
type Dog = Animal & { breed: string };

// ─── Interface Extending Multiple Interfaces ──────────────────
interface Serializable {
  serialize(): string;
}
interface Loggable {
  log(): void;
}
interface Entity extends Serializable, Loggable {
  id: number;
}

// ─── Type Intersection (equivalent) ──────────────────────────
type Entity = Serializable & Loggable & { id: number };

```

### Nameability

```typescript
// Types can be anonymous
function greet(person: { name: string }) {} // Inline object type

// Interfaces can be anonymous too, but are typically named
function process(data: { items: number[] }) {} // Both work

// Named types are better for error messages
type User = { name: string; age: number };
interface UserInterface { name: string; age: number }

```

## Code Examples

### Structural Typing

```typescript
// TypeScript uses structural typing — both types and interfaces
// are compatible based on shape, not explicit declaration

type Point = { x: number; y: number };
interface PointInterface { x: number; y: number }

const p1: Point = { x: 1, y: 2 };
const p2: PointInterface = p1; // ✅ Compatible — same structure

// Extra properties are allowed when assigning to a variable
const p3 = { x: 1, y: 2, z: 3 };
const p4: Point = p3; // ✅ OK — extra properties allowed

// Extra properties are NOT allowed in object literals
const p5: Point = { x: 1, y: 2, z: 3 }; // ❌ Error: excess property

```

### Common Patterns

```typescript
// ─── Pattern 1: API Response Types ───────────────────────────
type ApiResponse<T> = {
  data: T;
  status: number;
  message: string;
};

interface User {
  id: number;
  name: string;
  email: string;
}

type UserResponse = ApiResponse<User>;

// ─── Pattern 2: Discriminated Unions (type only) ────────────
type Shape =

  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

// ─── Pattern 3: React Props (interface preferred) ────────────
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";
}

// ─── Pattern 4: Class Implementation (interface preferred) ───
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}

class UserRepository implements Repository<User> {
  async findById(id: string): Promise<User | null> {
    // Implementation
    return null;
  }
  async findAll(): Promise<User[]> { return []; }
  async save(user: User): Promise<User> { return user; }
  async delete(id: string): Promise<boolean> { return true; }
}

```

### Extending and Intersecting

```typescript
// ─── Interface Chain ──────────────────────────────────────────
interface BaseEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

interface TimestampedEntity extends BaseEntity {
  deletedAt?: Date;
}

interface User extends TimestampedEntity {
  name: string;
  email: string;
}

// ─── Type Chain ──────────────────────────────────────────────
type BaseEntity = {
  id: string;
  createdAt: Date;
  updatedAt: Date;
};

type TimestampedEntity = BaseEntity & {
  deletedAt?: Date;
};

type User = TimestampedEntity & {
  name: string;
  email: string;
};

// ─── Mixed Extends and Intersection ──────────────────────────
interface HasId {
  id: string;
}

type Timestamped = {
  createdAt: Date;
  updatedAt: Date;
};

// Interface can extend a type intersection
interface User extends HasId, Timestamped {
  name: string;
}

```

## Real-World Use Cases

### Database Models

```typescript
// Interface for database entity (declaration merging with ORM)
interface BaseModel {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

interface User extends BaseModel {
  name: string;
  email: string;
  passwordHash: string;
}

// Type for creation (omit auto-generated fields)
type CreateUserDTO = Omit<User, "id" | "createdAt" | "updatedAt">;

// Type for update (all fields optional)
type UpdateUserDTO = Partial<CreateUserDTO>;

```

### Configuration

```typescript
// Type for complex configurations
type Environment = "development" | "staging" | "production";

type DatabaseConfig = {
  host: string;
  port: number;
  database: string;
  ssl: boolean;
};

type AppConfig = {
  env: Environment;
  port: number;
  database: DatabaseConfig;
};

// Interface for extending configs
interface AppConfig {
  logging: {
    level: "debug" | "info" | "warn" | "error";
    format: "json" | "text";
  };
}

```

## Common Mistakes

### 1. Using Interface When Type Is Required

```typescript
// ❌ Wrong: Interface cannot represent unions
interface Status = "active" | "inactive"; // Syntax error

// ✅ Correct
type Status = "active" | "inactive";

```

### 2. Using Type When Interface Would Be Better

```typescript
// ❌ Poor: No declaration merging, no extends
type Config = { debug: boolean };
// Later need to extend...

// ✅ Better: Interface allows merging and extension
interface Config {
  debug: boolean;
}
interface Config {
  verbose: boolean; // Merges automatically
}

```

### 3. Forgetting Structural Typing

```typescript
// This works because TypeScript uses structural typing
type Duck = { quack(): void };
type Bird = { quack(): void };

const duck: Duck = { quack: () => console.log("quack") };
const bird: Bird = duck; // ✅ No error — same structure

```

### 4. Excessive Intersections

```typescript
// ❌ Bad: Hard to read and debug
type ComplexType = A & B & C & D & E & F;

// ✅ Better: Use interfaces with extends
interface ComplexType extends A, B, C {
  // Group related properties
}

```

## Best Practices

```typescript
// 1. Use interfaces for object shapes and class contracts
interface User {
  name: string;
  email: string;
}

// 2. Use types for unions, intersections, and primitives
type ID = string | number;
type Result<T> = { success: true; data: T } | { success: false; error: string };

// 3. Use interfaces for public APIs (library authors)
// Declaration merging allows consumers to extend your types
interface RequestConfig {
  timeout: number;
}

// 4. Use types for internal implementation details
type InternalState = {
  cache: Map<string, unknown>;
  retryCount: number;
};

// 5. Be consistent within your project
// Pick one style for similar use cases and stick with it

```

## Performance Considerations

- **Compilation**: Interfaces are generally slightly faster to compile because TypeScript can cache their declarations
- **Type checking**: Both have similar performance for type checking
- **Large types**: Intersections of many types can slow down the compiler; prefer interfaces with extends
- **Circular references**: Both handle circular references, but interfaces handle them more gracefully
- **IDE experience**: Interfaces often provide better error messages and autocomplete

## Summary

| Feature | Type | Interface |
|---------|------|-----------|
| Primitives | ✅ | ❌ |
| Unions | ✅ | ❌ |
| Intersections | ✅ | ❌ (use extends) |
| Tuples | ✅ | ❌ |
| Mapped types | ✅ | ❌ |
| Declaration merging | ❌ | ✅ |
| Extends | ❌ | ✅ |
| Class implementation | ❌ | ✅ |
| Performance (large) | Slower | Faster |

## Cheat Sheet
```typescript
// Use TYPE for:
type ID = string | number;                    // Unions
type Pair<T> = [T, T];                        // Tuples
type Result<T> = { ok: true; data: T } | { ok: false; error: string }; // Discriminated unions

// Use INTERFACE for:
interface User { name: string; email: string; }  // Object shapes
interface Config extends BaseConfig {}           // Inheritance
interface Window { /* ... */ }                   // Declaration merging

// Quick comparison:
type Animal = { name: string };
interface Animal { name: string; }

// Type assertion (works with both):
const a: Animal = { name: "Cat" };
const b: typeof a = { name: "Dog" }; // Works with both type and interface

```

---

## See Also
- [JavaScript](../01-JavaScript/)
- [NestJS](../06-NestJS/)
- [React](../03-React/)

## References & Learn More

- [TypeScript: Interfaces vs Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#differences-between-type-aliases-and-interfaces)
- [MDN: TypeScript](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client_side_tooling/TypeScript)
- [TypeScript Handbook: Declaration Merging](https://www.typescriptlang.org/docs/handbook/declaration-merging.html)
- [When to Use Interfaces vs Types in TypeScript](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#interfaces-vs-type-aliases)
