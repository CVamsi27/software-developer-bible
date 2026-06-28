# Type Narrowing

## Definition

**Type narrowing** is the process of refining a broader type into a more specific type through control flow analysis, type guards, and other TypeScript mechanisms. It allows you to safely work with specific types within conditional blocks.

```text
┌─────────────────────────────────────────────────────────────────┐
│                    TYPE NARROWING                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Union Type          Narrowed Type                             │
│   ┌─────────┐        ┌─────────┐                               │
│   │ string  │        │ string  │  (after typeof check)         │
│   │ number  │   ──▶  └─────────┘                               │
│   │ boolean │                                                 │
│   └─────────┘                                                  │
│                                                                 │
│   function process(x: string | number) {                       │
│     if (typeof x === "string") {                               │
│       // x is string here                                     │
│     } else {                                                   │
│       // x is number here                                     │
│     }                                                          │
│   }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **Type safety**: Safely work with specific types in conditional blocks
2. **Code clarity**: Make type relationships explicit
3. **Error prevention**: Catch type errors at compile time
4. **API design**: Create type-safe functions and interfaces
5. **Pattern matching**: Implement complex type-based logic

## How It Works

### typeof

```typescript
// Narrow primitive types
function processValue(value: string | number | boolean): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // ✅ string methods available
  } else if (typeof value === "number") {
    return value.toFixed(2); // ✅ number methods available
  } else {
    return value ? "true" : "false"; // ✅ boolean
  }
}
```

### instanceof

```typescript
// Narrow class instances
class HttpError {
  constructor(public status: number, public message: string) {}
}

class NetworkError {
  constructor(public message: string, public code: string) {}
}

function handleError(error: HttpError | NetworkError): string {
  if (error instanceof HttpError) {
    return `HTTP ${error.status}: ${error.message}`;
  } else {
    return `Network ${error.code}: ${error.message}`;
  }
}
```

### in Operator

```typescript
// Check for property existence
interface Bird {
  fly(): void;
  layEggs(): void;
}

interface Fish {
  swim(): void;
  layEggs(): void;
}

function move(animal: Bird | Fish): void {
  if ("fly" in animal) {
    animal.fly(); // ✅ Bird
  } else {
    animal.swim(); // ✅ Fish
  }
}
```

### User-Defined Type Guards

```typescript
// Type guard function
interface Cat {
  meow(): void;
  purr(): void;
}

interface Dog {
  bark(): void;
  fetch(): void;
}

function isCat(animal: Cat | Dog): animal is Cat {
  return "meow" in animal;
}

function interact(animal: Cat | Dog): void {
  if (isCat(animal)) {
    animal.meow(); // ✅ Cat
    animal.purr(); // ✅ Cat
  } else {
    animal.bark(); // ✅ Dog
    animal.fetch(); // ✅ Dog
  }
}
```

### Discriminated Unions

```typescript
// Union with common discriminant
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
  }
}

// Exhaustive check
function assertNever(x: never): never {
  throw new Error("Unexpected value: " + x);
}

function areaExhaustive(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      return assertNever(shape); // ✅ Compile error if missing case
  }
}
```

### The never Type

```typescript
// never represents values that never occur
function throwError(message: string): never {
  throw new Error(message);
}

function infiniteLoop(): never {
  while (true) {}
}

// Use with exhaustive checking
function processShape(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    default:
      // shape is never here — all cases handled
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}
```

## Code Examples

### Practical Examples

```typescript
// ─── API Response handling ────────────────────────────────────
type ApiResponse<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: string }
  | { status: "loading" };

function handleResponse<T>(response: ApiResponse<T>): string {
  switch (response.status) {
    case "success":
      return `Data: ${JSON.stringify(response.data)}`;
    case "error":
      return `Error: ${response.error}`;
    case "loading":
      return "Loading...";
  }
}

// ─── Type-safe event handling ─────────────────────────────────
type Event =
  | { type: "click"; x: number; y: number }
  | { type: "keypress"; key: string }
  | { type: "scroll"; top: number };

function handleEvent(event: Event): void {
  switch (event.type) {
    case "click":
      console.log(`Click at (${event.x}, ${event.y})`);
      break;
    case "keypress":
      console.log(`Key pressed: ${event.key}`);
      break;
    case "scroll":
      console.log(`Scrolled to ${event.top}`);
      break;
  }
}

// ─── Type-safe parsing ────────────────────────────────────────
function parseJSON<T>(json: string): T | null {
  try {
    return JSON.parse(json) as T;
  } catch {
    return null;
  }
}

function processUser(json: string): void {
  const user = parseJSON<User>(json);
  if (user && typeof user === "object" && "name" in user) {
    console.log(user.name); // ✅ TypeScript knows user has name
  }
}
```

### Advanced Patterns

```typescript
// ─── Type-safe reducer ────────────────────────────────────────
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "RESET" };

interface State {
  count: number;
}

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "INCREMENT":
      return { count: state.count + action.amount };
    case "DECREMENT":
      return { count: state.count - action.amount };
    case "RESET":
      return { count: 0 };
  }
}

// ─── Type-safe validation ─────────────────────────────────────
interface ValidationSuccess<T> {
  valid: true;
  value: T;
}

interface ValidationFailure {
  valid: false;
  errors: string[];
}

type ValidationResult<T> = ValidationSuccess<T> | ValidationFailure;

function validate(input: unknown): ValidationResult<string> {
  if (typeof input === "string") {
    return { valid: true, value: input };
  }
  return { valid: false, errors: ["Expected string"] };
}

function processInput(input: unknown): void {
  const result = validate(input);
  if (result.valid) {
    console.log(result.value.toUpperCase()); // ✅ string
  } else {
    console.error(result.errors); // ✅ string[]
  }
}

// ─── Type-safe optional chaining ──────────────────────────────
function getNestedValue(
  obj: Record<string, any>,
  path: string
): string | undefined {
  const keys = path.split(".");
  let current: any = obj;

  for (const key of keys) {
    if (current === null || current === undefined) {
      return undefined;
    }
    current = current[key];
  }

  return typeof current === "string" ? current : undefined;
}
```

## Common Mistakes

### 1. Forgetting Exhaustive Checking

```typescript
// ❌ Bad: Missing case, no error
function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    // Missing triangle case!
  }
}

// ✅ Good: Exhaustive check with never
function getArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    default:
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}
```

### 2. Over-narrowing

```typescript
// ❌ Bad: Over-narrowing makes code fragile
function process(value: string | number) {
  if (typeof value === "string") {
    // Narrowed to string
  } else if (typeof value === "number") {
    // Narrowed to number
  }
  // After if-else, value is still string | number
}

// ✅ Good: Use type assertion or reassign
function process(value: string | number) {
  let result: string;
  if (typeof value === "string") {
    result = value;
  } else {
    result = value.toString();
  }
  // result is string
}
```

### 3. Not Using Type Guards

```typescript
// ❌ Bad: Using `any` or type assertions
function isString(value: unknown): boolean {
  return typeof value === "string";
}

function process(value: unknown) {
  if (isString(value)) {
    (value as string).toUpperCase(); // Unsafe!
  }
}

// ✅ Good: Use type guard
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function process(value: unknown) {
  if (isString(value)) {
    value.toUpperCase(); // ✅ Safe
  }
}
```

## Best Practices

```typescript
// 1. Use discriminated unions for complex types
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// 2. Always handle all cases in switch statements
function process(result: Result<User>) {
  if (result.success) {
    console.log(result.data);
  } else {
    console.error(result.error);
  }
}

// 3. Use type guards for complex checks
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "name" in value &&
    "email" in value
  );
}

// 4. Use never for exhaustive checking
function assertNever(x: never): never {
  throw new Error("Unexpected: " + x);
}

// 5. Prefer type narrowing over type assertions
// ❌ Bad: (value as string).toUpperCase()
// ✅ Good: if (typeof value === "string") value.toUpperCase()
```

## Performance Considerations

- **Compilation**: Type narrowing is resolved at compile time
- **Runtime**: Type guards have minimal runtime cost
- **IDE**: Narrowing improves autocomplete and error detection
- **Bundle size**: No impact on bundle size
- **Debugging**: Narrowed types improve debugging experience

## Interview Questions

### Beginner

1. **What is type narrowing?**
   - Refining a broader type to a more specific type through control flow

2. **How do you narrow with typeof?**
   - Check `typeof value === "string"` to narrow to string

3. **What is a type guard?**
   - A function that returns a type predicate (`value is Type`)

4. **What is a discriminated union?**
   - A union of types with a common discriminant property

5. **What is the never type?**
   - A type that represents values that never occur

### Intermediate

6. **How do you implement exhaustive checking?**
   - Use `switch` with `never` in default case

7. **What is the difference between typeof and instanceof?**
   - typeof checks primitive types; instanceof checks class instances

8. **How do you narrow with the in operator?**
   - Check `"property" in object` to narrow to types with that property

9. **When would you use a user-defined type guard?**
   - When TypeScript can't infer narrowing from built-in checks

10. **How do you handle nullable types?**
    - Use null checks: `if (value !== null)`

### Senior

11. **Design a type-safe parser using discriminated unions**
    - Create AST nodes with discriminant properties

12. **How do you implement a type-safe state machine?**
    - Use discriminated unions for states and transitions

13. **Create a type-safe middleware chain**
    - Use type narrowing to propagate types through middleware

14. **How do you handle complex union types?**
    - Break down unions into smaller, more manageable types

### FAANG-style

15. **Build a type-safe JSON parser**
    - Use type guards to validate and narrow unknown data

16. **Implement a type-safe router**
    - Use discriminated unions for routes and parameters

17. **Create a type-safe form validation system**
    - Use type narrowing for validation results

### Follow-ups

18. **How does type narrowing interact with generics?**
    - Narrowing works within generic functions

19. **Can you narrow tuple types?**
    - Yes, using length checks and index access

20. **How do you debug type narrowing issues?**
    - Use IDE hover, add intermediate variables, or use `@ts-expect-error`

## Summary

Type narrowing is essential for writing safe TypeScript code. It allows you to work with specific types within conditional blocks and catch type errors at compile time. Master discriminated unions, type guards, and exhaustive checking for robust type-safe code.

## Cheat Sheet

```typescript
// typeof narrowing
if (typeof x === "string") { /* x is string */ }

// instanceof narrowing
if (x instanceof Error) { /* x is Error */ }

// in operator narrowing
if ("name" in x) { /* x has name property */ }

// Type guard
function isString(x: unknown): x is string {
  return typeof x === "string";
}

// Discriminated union
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

// Exhaustive check
function process(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    default: const _: never = shape; return _;
  }
}
```

## References & Learn More

- [TypeScript Handbook: Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [TypeScript Handbook: Type Guards](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html)
- [Type Narrowing in TypeScript](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates)
