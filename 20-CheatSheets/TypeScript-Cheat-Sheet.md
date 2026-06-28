# TypeScript Cheat Sheet

## Quick Reference Table

| Concept | Key Point | Code/Example |
|---------|-----------|--------------|
| Interface vs Type | Interface: extendable, declaration merging, supports `implements`. Type: union, intersection, mapped, conditional | `interface A { x: number }` / `type B = { x: number }` |
| Union Types | `A \| B` — value can be A or B | `type ID = string \| number` |
| Intersection Types | `A & B` — value must satisfy both A and B | `type Combined = A & B` |
| Literal Types | Restrict to specific values | `type Direction = 'up' \| 'down' \| 'left' \| 'right'` |
| Type Narrowing | Narrow union types through control flow | `if (typeof x === 'string')` narrows to `string` |
| `never` | Impossible state; function that never returns | `function throwError(msg: string): never { throw new Error(msg); }` |
| `unknown` | Type-safe `any`; must narrow before use | `const val: unknown = getData(); if (typeof val === 'string') ...` |
| `void` | Function returns nothing | `function log(msg: string): void { console.log(msg); }` |
| `asserts` | Type assertion as a function return type | `function isString(x: unknown): asserts x is string { ... }` |
| Generics | Type parameters for reusable types | `function identity<T>(x: T): T { return x; }` |
| Generic Constraints | `extends` to bound generic types | `function pluck<T, K extends keyof T>(obj: T, key: K): T[K]` |
| Conditional Types | `T extends U ? X : Y` — type-level if/else | `type IsString<T> = T extends string ? true : false` |
| `infer` | Extract types within conditional types | `type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never` |
| `keyof` | Union of keys of a type | `type Keys = keyof { a: 1, b: 2 }` → `'a' \| 'b'` |
| `typeof` | Get the TypeScript type of a value | `const obj = { x: 1 }; type T = typeof obj` → `{ x: number }` |
| `in` operator | Narrow by checking property existence | `'name' in obj` narrows to type with `name` |
| Mapped Types | Transform properties of a type | `type ReadOnly<T> = { readonly [K in keyof T]: T[K] }` |
| Template Literal Types | String manipulation at type level | `type Event = \`on\${Capitalize<'click'>}\`` → `'onClick'` |
| `satisfies` | Validate type without widening | `const config = { port: 3000 } satisfies Record<string, number>` |
| Declaration Merging | Interface + same-name interface = merged | `interface Window { custom: string }` extends built-in |
| `declare` | Tell TS something exists at runtime | `declare const gtag: (...args: any[]) => void;` |
| Utility — `Partial<T>` | All properties optional | `Partial<User>` = `{ name?: string; age?: number }` |
| Utility — `Required<T>` | All properties required | `Required<Partial<User>>` |
| Utility — `Pick<T, K>` | Subset of properties | `Pick<User, 'name' \| 'age'>` |
| Utility — `Omit<T, K>` | All except specified properties | `Omit<User, 'password'>` |
| Utility — `Record<K, V>` | Object with keys K and values V | `Record<string, number>` = `{ [key: string]: number }` |
| Utility — `Readonly<T>` | All properties readonly | `Readonly<User>` |
| Utility — `ReturnType<T>` | Extract function return type | `ReturnType<typeof fn>` |
| Utility — `Parameters<T>` | Extract function parameter types | `Parameters<typeof fn>` |
| Utility — `Extract<T, U>` | Extract from T that extends U | `Extract<'a' \| 'b' \| 'c', 'a' \| 'd'>` → `'a'` |
| Utility — `Exclude<T, U>` | Exclude from T that extends U | `Exclude<'a' \| 'b' \| 'c', 'a'>` → `'b' \| 'c'` |
| Utility — `NonNullable<T>` | Remove null and undefined | `NonNullable<string \| null>` → `string` |
| Utility — `Awaited<T>` | Unwrap Promise type | `Awaited<Promise<string>>` → `string` |
| Utility — `InstanceType<T>` | Get instance type from class constructor | `InstanceType<typeof MyClass>` |
| Decorators (Stage 3) | Class/method/field/accessor decorators | `@logged class Foo {}` |
| Decorator Metadata | `reflect-metadata` for design-time type info | `@Injectable() class Service {}` |
| Strict Mode | `strict: true` enables all strict checks | `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes` |
| Enums | Numeric (auto-increment) or string enums | `enum Status { Active = 'ACTIVE' }` |
| Namespaces | Group related types (avoid in modern TS) | `namespace Models { export interface User {} }` |
| Module Augmentation | Extend existing module types | `declare module 'express' { interface Request { user: User } }` |
| Type Guards | Custom functions that narrow types | `function isUser(x: any): x is User { return x?.id !== undefined; }` |
| Assertion Functions | `asserts x is Type` for runtime checks | `function assertDefined<T>(x: T): asserts x is NonNullable<T>` |
| Branded Types | Prevent type confusion | `type UserId = string & { __brand: 'UserId' }` |
| Const Assertions | `as const` — literal types, readonly | `const arr = [1, 2] as const` → `readonly [1, 2]` |
| Variadic Tuples | Spread types in function signatures | `function merge<T extends any[]>(...args: T): T` |

## Top 10 Things to Remember

1. **Interface vs Type**: Use `interface` for object shapes that may be extended or merged. Use `type` for unions, intersections, mapped types, and anything beyond simple objects.

2. **`unknown` over `any`**: `unknown` forces narrowing before use. `any` disables type checking entirely. Never use `any` in library code.

3. **Generics are type-level functions**: They accept types and return types. `extends` constraints narrow what's accepted. Default types: `<T = unknown>`.

4. **Conditional types distribute over unions**: `T extends string ? X : Y` applied to `string | number` produces `X | Y`, not a single result. Wrap in `[]` to prevent distribution.

5. **`infer` extracts types**: Used inside conditional types to extract parts of complex types. `ReturnType`, `Parameters`, and `Parameters` all use `infer`.

6. **Type narrowing is compile-time only**: TypeScript uses control flow analysis. `typeof`, `instanceof`, `in`, custom type guards, and discriminated unions all narrow types.

7. **`satisfies` validates without widening**: `const x = { a: 1 } satisfies Record<string, number>` keeps `x` typed as `{ a: number }` instead of `Record<string, number>`.

8. **Strict mode is non-negotiable**: Always enable `strict: true` in `tsconfig.json`. It enables `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, etc.

9. **Discriminated unions are the pattern**: Use a `type` or `kind` field to create exhaustive, type-safe state machines and API responses.

10. **TypeScript erases types at compile time**: No runtime overhead. `interface` doesn't exist at runtime. `enum` is the exception — it generates real JS.

## Common Patterns

### Discriminated Union (State Machine)

```ts
type RequestState<T> =

  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function render<T>(state: RequestState<T>) {
  switch (state.status) {
    case 'idle': return 'Not started';
    case 'loading': return 'Loading...';
    case 'success': return state.data;      // narrowed to { data: T }
    case 'error': return state.error.message; // narrowed to { error: Error }
  }
}

```

### Builder Pattern with Generics

```ts
class QueryBuilder<T extends Record<string, unknown>> {
  private filters: Partial<T> = {};

  where<K extends keyof T>(key: K, value: T[K]): this {
    this.filters[key] = value;
    return this;
  }

  build(): Partial<T> {
    return { ...this.filters };
  }
}

```

### Type-Safe Event Emitter

```ts
type EventMap = {
  'user:login': { userId: string; timestamp: number };
  'user:logout': { userId: string };
};

class TypedEmitter<T extends Record<string, unknown>> {
  private handlers = new Map<string, Function[]>();

  on<K extends keyof T>(event: K, handler: (payload: T[K]) => void): void {
    const list = this.handlers.get(event as string) || [];
    list.push(handler);
    this.handlers.set(event as string, list);
  }

  emit<K extends keyof T>(event: K, payload: T[K]): void {
    this.handlers.get(event as string)?.forEach(h => h(payload));
  }
}

```

### Branded Types (Preventing Type Confusion)

```ts
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

function createUserId(id: string): UserId { return id as UserId; }
function getOrder(userId: UserId, orderId: OrderId) { ... }

// getOrder(orderId, userId) → compile error! Prevents swapping arguments.

```

### Exhaustive Check

```ts
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

type Color = 'red' | 'green' | 'blue';
function getColor(c: Color): string {
  switch (c) {
    case 'red': return '#ff0000';
    case 'green': return '#00ff00';
    case 'blue': return '#0000ff';
    default: return assertNever(c); // compile error if case missing
  }
}

```

### Recursive Types

```ts
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? DeepReadonly<T[K]>
    : T[K];
};

type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue };

```

### Type-Safe API Response

```ts
type ApiResponse<T> =

  | { ok: true; data: T; status: number }
  | { ok: false; error: string; status: number };

async function fetchTyped<T>(url: string): Promise<ApiResponse<T>> {
  const res = await fetch(url);
  if (!res.ok) return { ok: false, error: await res.text(), status: res.status };
  return { ok: true, data: await res.json(), status: res.status };
}

```

### Decorator Pattern (Stage 3)

```ts
function logged(originalMethod: any, context: ClassMethodDecoratorContext) {
  return function(this: any, ...args: any[]) {
    console.log(`Calling ${String(context.name)} with`, args);
    const result = originalMethod.call(this, ...args);
    console.log(`${String(context.name)} returned`, result);
    return result;
  };
}

class Calculator {
  @logged
  add(a: number, b: number) { return a + b; }
}

```

### Template Literal Type Builder

```ts
type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Endpoint = '/users' | '/posts' | '/comments';
type Route = `${HTTPMethod} ${Endpoint}`;
// = "GET /users" | "GET /posts" | ... (12 combinations)

type CSSProperty = `margin-${'top' | 'bottom' | 'left' | 'right'}`;

```

### Type-Safe localStorage

```ts
interface StorageSchema {
  'auth-token': string;
  'user-preferences': { theme: 'light' | 'dark' };
  'last-visited': number;
}

function getStorage<K extends keyof StorageSchema>(key: K): StorageSchema[K] | null {
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : null;
}

function setStorage<K extends keyof StorageSchema>(key: K, value: StorageSchema[K]): void {
  localStorage.setItem(key, JSON.stringify(value));
}

```

## Red Flags (Things NOT to Say)

- **"I use `any` when I'm not sure"** — Shows lack of discipline. Use `unknown` and narrow, or fix the type.
- **"TypeScript adds runtime overhead"** — Types are erased at compile time. Zero runtime cost (except enums and decorators).
- **"Interfaces and types are the same"** — They differ in declaration merging, extends vs intersection, and support for unions/mapped types.
- **"I don't use generics because they're confusing"** — Shows you don't understand reusable type-safe APIs. Generics are essential.
- **"I disable `strict` mode for convenience"** — Undermines the entire point of TypeScript. `strict: true` is non-negotiable.
- **"I cast with `as any` to make it work"** — This is a hack, not a solution. Fix the types properly.
- **"Enums are great, I use them everywhere"** — String literal unions are usually better (tree-shakeable, simpler, no runtime code).
- **"TypeScript catches all bugs"** — It catches type errors at compile time. Runtime errors, logic bugs, and async issues still exist.
- **"I use `!` (non-null assertion) to suppress errors"** — This is lying to the compiler. Fix the nullability properly.
- **"I don't need type guards, I just use `as`"** — `as` is an assertion, not a check. Type guards actually validate at runtime.

## Green Flags (Things TO Say)

- **"I prefer `unknown` over `any` and narrow with type guards."** — Shows type safety discipline.
- **"Discriminated unions make state management exhaustive and type-safe."** — Core pattern for robust code.
- **"I use `satisfies` to validate without losing literal types."** — Shows knowledge of modern TS features.
- **"Branded types prevent swapping arguments of the same underlying type."** — Advanced type safety pattern.
- **"I enable `strict: true` and treat the compiler as a design tool."** — Shows mature TS mindset.
- **"I prefer `interface` for public APIs (extendable, merges) and `type` for internal types (unions, mapped)."** — Nuanced understanding.
- **"Conditional types with `infer` let me extract types from complex structures."** — Advanced metaprogramming.
- **"I use mapped types to transform types programmatically instead of duplicating."** — DRY at the type level.
- **"Template literal types enable type-safe string patterns."** — Modern TS power feature.
- **"I use `as const` assertions for literal types and readonly arrays."** — Precise typing.

## 5-Minute Pre-Interview Review

- **Interface vs Type**: Interface = extend, merge, implement. Type = union, intersection, mapped, conditional. Interface for objects, type for everything else.
- **Generics**: `<T>` is a type parameter. `extends T` constrains it. Default: `<T = unknown>`. Used in functions, classes, types, interfaces.
- **Utility Types**: `Partial<T>` (all optional), `Required<T>` (all required), `Pick<T,K>` (subset), `Omit<T,K>` (exclude), `Record<K,V>` (key-value map).
- **Conditional Types**: `T extends U ? X : Y`. Distributes over unions. `infer R` extracts types. `Exclude<T,U>` = `T extends U ? never : T`.
- **Type Narrowing**: `typeof`, `instanceof`, `in`, custom type guards (`x is Type`), discriminated unions, truthiness checks, equality checks.
- **`never` vs `void`**: `never` = impossible state or function that never returns (throws/infinite). `void` = function returns nothing (undefined).
- **`unknown` vs `any`**: `unknown` is type-safe (must narrow). `any` disables checking (escape hatch). Prefer `unknown`.
- **Strict Mode**: `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `noImplicitThis`, `alwaysStrict`. Enable all.
- **Enums**: `enum E { A, B }` generates JS. `const enum` inlines values. Prefer literal unions for most cases.
- **Decorators (Stage 3)**: `@decorator` on class, method, field, accessor. Use `context` parameter for metadata. Replace `experimentalDecorators`.
- **Template Literals**: `` `on${Capitalize<K>}` `` generates type-safe string patterns. Combine with unions for API routes, event names.
- **`satisfies`**: Validates expression matches type without widening. `const x = { a: 1 } satisfies Record<string, number>` keeps `{ a: number }`.

---

## References & Learn More

- [Cheat Sheet Collection](https://github.com/detailyang/awesome-cheatsheet)
- [DevHints](https://devhints.io/)
- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
