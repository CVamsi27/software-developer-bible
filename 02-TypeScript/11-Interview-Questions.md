# TypeScript Interview Questions

## Definition

This comprehensive guide covers the most frequently asked TypeScript interview questions, categorized by difficulty level. Master these questions to ace your next TypeScript interview.

```text
┌─────────────────────────────────────────────────────────────────┐
│                  INTERVIEW QUESTION CATEGORIES                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┬─────────────────────────────────────────┐  │
│   │ Category     │ Questions                               │  │
│   ├──────────────┼─────────────────────────────────────────┤  │
│   │ Beginner     │ 10 questions (fundamentals)             │  │
│   │ Intermediate │ 10 questions (practical usage)          │  │
│   │ Senior       │ 10 questions (advanced patterns)        │  │
│   │ FAANG-style  │ 10 questions (system design)            │  │
│   │ Follow-ups   │ 10 questions (deep dives)               │  │
│   └──────────────┴─────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need This?

1. **Interview preparation**: Be ready for common TypeScript questions
2. **Knowledge validation**: Test your understanding of TypeScript concepts
3. **Career advancement**: Demonstrate expertise in TypeScript
4. **Code quality**: Write better TypeScript code
5. **Team leadership**: Mentor junior developers

## Beginner Questions (10)

### 1. What is TypeScript?

**Answer**: TypeScript is a statically-typed superset of JavaScript that compiles to plain JavaScript. It adds optional type annotations, interfaces, enums, and other features that help catch errors at compile time rather than runtime.

```typescript
// JavaScript
function add(a, b) {
  return a + b;
}

// TypeScript
function add(a: number, b: number): number {
  return a + b;
}
```

### 2. What are the benefits of using TypeScript?

**Answer**:
- **Type safety**: Catch errors at compile time
- **Better IDE support**: Autocomplete, refactoring, navigation
- **Self-documenting code**: Types serve as documentation
- **Easier refactoring**: TypeScript catches breaking changes
- **Scalability**: Essential for large codebases and teams

### 3. What is the difference between `any` and `unknown`?

**Answer**:
- `any`: Disables type checking, allows any operation
- `unknown`: Type-safe alternative to `any`, requires type checking before use

```typescript
// any - unsafe
let value: any = "hello";
value.toUpperCase(); // OK
value.foo.bar.baz; // OK (but runtime error)

// unknown - safe
let value: unknown = "hello";
value.toUpperCase(); // Error: Object is of type 'unknown'
if (typeof value === "string") {
  value.toUpperCase(); // OK after type check
}
```

### 4. What are type aliases and interfaces?

**Answer**:
- **Type alias (`type`)**: Creates a name for any type (primitives, unions, intersections)
- **Interface**: Defines the shape of objects, supports declaration merging

```typescript
// Type alias
type ID = string | number;
type User = { name: string; age: number };

// Interface
interface UserInterface {
  name: string;
  age: number;
}
```

### 5. What is structural typing?

**Answer**: TypeScript uses structural typing, meaning types are compatible based on their structure, not their explicit declarations.

```typescript
interface Point {
  x: number;
  y: number;
}

interface Coordinate {
  x: number;
  y: number;
}

const point: Point = { x: 1, y: 2 };
const coord: Coordinate = point; // OK - same structure
```

### 6. What are generics?

**Answer**: Generics allow you to write reusable, type-safe code that works with multiple types while preserving type information.

```typescript
function identity<T>(value: T): T {
  return value;
}

const str = identity("hello"); // T is string
const num = identity(42); // T is number
```

### 7. What are utility types?

**Answer**: Built-in TypeScript types that provide common type transformations.

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

type PartialUser = Partial<User>; // All properties optional
type ReadonlyUser = Readonly<User>; // All properties readonly
type UserName = Pick<User, "name">; // { name: string }
```

### 8. What is type narrowing?

**Answer**: The process of refining a broader type into a more specific type through control flow analysis.

```typescript
function process(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase(); // string
  } else {
    return value.toFixed(2); // number
  }
}
```

### 9. What are discriminated unions?

**Answer**: A union of types with a common discriminant property, enabling type-safe pattern matching.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
  }
}
```

### 10. What is the `never` type?

**Answer**: A type that represents values that never occur. Used for functions that never return or exhaustive checking.

```typescript
function throwError(message: string): never {
  throw new Error(message);
}

// Exhaustive checking
function process(shape: Shape): number {
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

## Intermediate Questions (10)

### 11. How do you type a function that returns a Promise?

**Answer**:

```typescript
// Explicit return type
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// Using ReturnType
type UserReturn = ReturnType<typeof fetchUser>; // Promise<User>
```

### 12. What is the difference between `extends` and `&`?

**Answer**:
- `extends`: Interface inheritance, can override properties
- `&`: Intersection type, creates a type with all properties

```typescript
// extends
interface Animal {
  name: string;
}
interface Dog extends Animal {
  breed: string;
}

// &
type Animal = { name: string };
type Dog = Animal & { breed: string };
```

### 13. How do you type event handlers?

**Answer**:

```typescript
// React event handlers
function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
  console.log(event.clientX, event.clientY);
}

// DOM event handlers
function handleInput(event: Event) {
  const target = event.target as HTMLInputElement;
  console.log(target.value);
}
```

### 14. What are mapped types?

**Answer**: Types that transform existing types by iterating over their keys.

```typescript
type Optional<T> = {
  [K in keyof T]?: T[K];
};

type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};
```

### 15. What are conditional types?

**Answer**: Types that select types based on conditions.

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>; // true
type B = IsString<number>; // false
```

### 16. How do you type a generic React component?

**Answer**:

```typescript
interface Props<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: Props<T>) {
  return <div>{items.map(renderItem)}</div>;
}

// Usage
<List
  items={["a", "b", "c"]}
  renderItem={(item) => <span>{item}</span>}
/>
```

### 17. What is the `infer` keyword?

**Answer**: Used in conditional types to extract and name a type.

```typescript
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

type Fn = () => string;
type Result = ReturnType<Fn>; // string
```

### 18. How do you type a REST API response?

**Answer**:

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  total: number;
  page: number;
  limit: number;
}

type UserResponse = ApiResponse<User>;
type UserListResponse = PaginatedResponse<User>;
```

### 19. What are type guards?

**Answer**: Functions that return a type predicate, narrowing the type.

```typescript
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function process(value: unknown) {
  if (isString(value)) {
    value.toUpperCase(); // OK after type guard
  }
}
```

### 20. How do you type a reducer?

**Answer**:

```typescript
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
```

## Senior Questions (10)

### 21. How do you implement a type-safe event emitter?

**Answer**:

```typescript
type EventMap = {
  "user:created": { userId: string };
  "user:deleted": { userId: string };
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
```

### 22. Design a type-safe state management solution

**Answer**:

```typescript
type ActionMap = {
  "user/create": { name: string; email: string };
  "user/delete": { userId: string };
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

function reducer<S, A extends Action<keyof ActionMap>>(
  state: S,
  action: A
): S {
  switch (action.type) {
    case "user/create":
      // TypeScript knows action.payload has name and email
      return state;
    default:
      return state;
  }
}
```

### 23. How do you create a type-safe router?

**Answer**:

```typescript
type RouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof RouteParams<Rest>]: string }
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

function createRoute<T extends string>(route: T): { path: T; params: RouteParams<T> } {
  return { path: route } as any;
}

const userRoute = createRoute("/users/:id");
// { path: "/users/:id"; params: { id: string } }
```

### 24. Implement a type-safe curry function

**Answer**:

```typescript
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
```

### 25. How do you type a deep object path?

**Answer**:

```typescript
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
  };
}

type HostType = DeepPropertyAccess<Config, "database.host">; // string
```

### 26. Design a type-safe form validation system

**Answer**:

```typescript
type ValidationRule<T> = {
  [K in keyof T]?: {
    required?: boolean;
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    custom?: (value: T[K]) => string | null;
  };
};

type ValidationErrors<T> = {
  [K in keyof T]?: string[];
};

function validate<T extends Record<string, any>>(
  data: T,
  rules: ValidationRule<T>
): ValidationErrors<T> {
  const errors = {} as ValidationErrors<T>;

  for (const key in rules) {
    const value = data[key];
    const rule = rules[key];
    const fieldErrors: string[] = [];

    if (rule?.required && (value === undefined || value === null)) {
      fieldErrors.push(`${key} is required`);
    }

    if (rule?.custom) {
      const error = rule.custom(value);
      if (error) fieldErrors.push(error);
    }

    if (fieldErrors.length > 0) {
      errors[key] = fieldErrors;
    }
  }

  return errors;
}
```

### 27. How do you create a type-safe middleware chain?

**Answer**:

```typescript
type Middleware<T> = (req: T, next: () => void) => void;

function createMiddlewareChain<T>(
  middlewares: Middleware<T>[]
): (req: T) => void {
  return (req: T) => {
    let index = 0;

    function next(): void {
      if (index < middlewares.length) {
        const middleware = middlewares[index++];
        middleware(req, next);
      }
    }

    next();
  };
}
```

### 28. Implement a type-safe query builder

**Answer**:

```typescript
interface DatabaseSchema {
  users: { id: string; name: string; email: string };
  posts: { id: string; title: string; authorId: string };
}

type Table = keyof DatabaseSchema;
type Column<T extends Table> = keyof DatabaseSchema[T];

class QueryBuilder<T extends Table> {
  private selectedColumns: Column<T>[] = [];

  select(...columns: Column<T>[]): this {
    this.selectedColumns = columns;
    return this;
  }

  where(condition: string): this {
    return this;
  }

  build(): string {
    return `SELECT ${this.selectedColumns.join(", ")} FROM ${this.table}`;
  }

  constructor(private table: T) {}
}

const query = new QueryBuilder("users")
  .select("id", "name")
  .where("id = '1'");
```

### 29. How do you type a plugin system?

**Answer**:

```typescript
interface Plugin<T> {
  name: string;
  install: (app: T) => void;
}

class App {
  private plugins: Plugin<App>[] = [];

  use(plugin: Plugin<App>): void {
    this.plugins.push(plugin);
    plugin.install(this);
  }
}

const loggerPlugin: Plugin<App> = {
  name: "logger",
  install: (app) => {
    console.log("Logger installed");
  }
};
```

### 30. Design a type-safe configuration system

**Answer**:

```typescript
type ConfigSchema = {
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
    ssl: boolean;
  };
};

type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

function createConfig(defaults: ConfigSchema): DeepPartial<ConfigSchema> {
  return defaults;
}

const config = createConfig({
  database: {
    host: "localhost",
    port: 5432,
    credentials: {
      user: "admin",
      password: "secret"
    }
  },
  server: {
    port: 3000,
    ssl: false
  }
});
```

## FAANG-style Questions (10)

### 31. Design a type-safe API client

**Answer**:

```typescript
interface ApiEndpoints {
  "/users": {
    GET: { response: User[] };
    POST: { body: CreateUserDTO; response: User };
  };
  "/users/:id": {
    GET: { response: User };
    PUT: { body: UpdateUserDTO; response: User };
    DELETE: { response: void };
  };
}

type Method = "GET" | "POST" | "PUT" | "DELETE";

class ApiClient {
  async request<
    Path extends keyof ApiEndpoints,
    M extends keyof ApiEndpoints[Path]
  >(
    path: Path,
    method: M,
    options?: { body?: any }
  ): Promise<any> {
    const response = await fetch(path, {
      method: method as string,
      body: options?.body ? JSON.stringify(options.body) : undefined,
      headers: { "Content-Type": "application/json" }
    });
    return response.json();
  }
}

const api = new ApiClient();
const users = await api.request("/users", "GET");
```

### 32. Implement a type-safe state machine

**Answer**:

```typescript
type StateMap = {
  idle: { events: { FETCH: "loading" } };
  loading: { events: { SUCCESS: "success"; ERROR: "error" } };
  success: { events: { RESET: "idle" } };
  error: { events: { RETRY: "loading"; RESET: "idle" } };
};

type State = keyof StateMap;
type Event<S extends State> = keyof StateMap[S]["events"];

class StateMachine<S extends State> {
  constructor(private state: S) {}

  transition<E extends Event<S>>(event: E): StateMap[S]["events"][E] {
    return this.state as any;
  }
}

const machine = new StateMachine<"idle">("idle");
const next = machine.transition("FETCH"); // "loading"
```

### 33. Design a type-safe ORM

**Answer**:

```typescript
interface Model {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

interface User extends Model {
  name: string;
  email: string;
}

class Repository<T extends Model> {
  async findById(id: string): Promise<T | null> {
    return null;
  }

  async findMany(where: Partial<T>): Promise<T[]> {
    return [];
  }

  async create(data: Omit<T, "id" | "createdAt" | "updatedAt">): Promise<T> {
    return data as T;
  }
}

const userRepo = new Repository<User>();
const user = await userRepo.findById("1");
```

### 34. Implement a type-safe middleware system

**Answer**:

```typescript
type Context = {
  req: Request;
  res: Response;
  state: Record<string, any>;
};

type Middleware = (ctx: Context, next: () => Promise<void>) => Promise<void>;

function createRouter() {
  const middlewares: Middleware[] = [];

  return {
    use(middleware: Middleware) {
      middlewares.push(middleware);
      return this;
    },

    async handle(ctx: Context) {
      let index = 0;

      async function next(): Promise<void> {
        if (index < middlewares.length) {
          const middleware = middlewares[index++];
          await middleware(ctx, next);
        }
      }

      await next();
    }
  };
}
```

### 35. Design a type-safe validation library

**Answer**:

```typescript
type Validator<T> = {
  [K in keyof T]?: (value: any) => string | null;
};

type ValidationErrors<T> = {
  [K in keyof T]?: string[];
};

function validate<T extends Record<string, any>>(
  data: T,
  validators: Validator<T>
): { valid: boolean; errors: ValidationErrors<T> } {
  const errors: ValidationErrors<T> = {};
  let valid = true;

  for (const key in validators) {
    const validator = validators[key];
    if (validator) {
      const error = validator(data[key]);
      if (error) {
        errors[key] = [error];
        valid = false;
      }
    }
  }

  return { valid, errors };
}
```

### 36. Implement a type-safe event system

**Answer**:

```typescript
type EventMap = {
  "user:created": { userId: string };
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
```

### 37. Design a type-safe dependency injection container

**Answer**:

```typescript
type Constructor<T = {}> = new (...args: any[]) => T;

class Container {
  private services = new Map<string, any>();

  register<T>(name: string, constructor: Constructor<T>): void {
    this.services.set(name, new constructor());
  }

  resolve<T>(name: string): T {
    return this.services.get(name) as T;
  }
}

class DatabaseService {
  query(sql: string): any[] {
    return [];
  }
}

const container = new Container();
container.register("database", DatabaseService);
const db = container.resolve<DatabaseService>("database");
```

### 38. Implement a type-safe plugin system

**Answer**:

```typescript
interface Plugin<T> {
  name: string;
  version: string;
  install: (app: T) => void;
}

class App {
  private plugins: Plugin<App>[] = [];

  use(plugin: Plugin<App>): void {
    this.plugins.push(plugin);
    plugin.install(this);
  }

  getPlugin(name: string): Plugin<App> | undefined {
    return this.plugins.find((p) => p.name === name);
  }
}

const loggerPlugin: Plugin<App> = {
  name: "logger",
  version: "1.0.0",
  install: (app) => {
    console.log("Logger plugin installed");
  }
};
```

### 39. Design a type-safe configuration system

**Answer**:

```typescript
type ConfigSchema = {
  database: {
    host: string;
    port: number;
  };
  server: {
    port: number;
  };
};

type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

class ConfigManager<T extends Record<string, any>> {
  private config: T;

  constructor(defaults: T) {
    this.config = defaults;
  }

  get<K extends keyof T>(key: K): T[K] {
    return this.config[key];
  }

  set<K extends keyof T>(key: K, value: T[K]): void {
    this.config[key] = value;
  }

  merge(overrides: DeepPartial<T>): void {
    this.config = { ...this.config, ...overrides } as T;
  }
}
```

### 40. Implement a type-safe query builder

**Answer**:

```typescript
interface DatabaseSchema {
  users: { id: string; name: string; email: string };
  posts: { id: string; title: string; authorId: string };
}

type Table = keyof DatabaseSchema;
type Column<T extends Table> = keyof DatabaseSchema[T];

class QueryBuilder<T extends Table> {
  private selectedColumns: Column<T>[] = [];
  private whereCondition: string = "";

  constructor(private table: T) {}

  select(...columns: Column<T>[]): this {
    this.selectedColumns = columns;
    return this;
  }

  where(condition: string): this {
    this.whereCondition = condition;
    return this;
  }

  build(): string {
    const columns = this.selectedColumns.join(", ");
    let query = `SELECT ${columns} FROM ${this.table}`;
    if (this.whereCondition) {
      query += ` WHERE ${this.whereCondition}`;
    }
    return query;
  }
}

const query = new QueryBuilder("users")
  .select("id", "name")
  .where("id = '1'")
  .build();
```

## Follow-up Questions (10)

### 41. How does TypeScript handle module resolution?

**Answer**: TypeScript uses module resolution algorithms to find type declarations. It supports:
- Node module resolution
- Classic module resolution
- Path mapping
-baseUrl configuration

### 42. What are declaration files (.d.ts)?

**Answer**: Files that contain type declarations for JavaScript libraries. They provide type information without implementation.

```typescript
// types/lodash.d.ts
declare module "lodash" {
  export function chunk<T>(array: T[], size: number): T[][];
}
```

### 43. How do you handle circular dependencies?

**Answer**:
- Use interfaces instead of type aliases
- Limit circular references
- Use dependency injection
- Break circular dependencies with barrel files

### 44. What are ambient declarations?

**Answer**: Declarations that describe the shape of existing JavaScript code without providing implementation.

```typescript
declare global {
  interface Window {
    myCustomProperty: string;
  }
}
```

### 45. How do you optimize TypeScript compilation?

**Answer**:
- Use project references for large codebases
- Enable incremental compilation
- Use `skipLibCheck` for faster compilation
- Configure `include` and `exclude` properly

### 46. What are template literal types?

**Answer**: Types that use template literal syntax to create string types.

```typescript
type EventName = "click" | "scroll";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onScroll"
```

### 47. How do you type a WebSocket connection?

**Answer**:

```typescript
interface WebSocketMessage {
  type: string;
  payload: any;
}

class TypedWebSocket {
  constructor(private ws: WebSocket) {}

  send<T extends WebSocketMessage>(message: T): void {
    this.ws.send(JSON.stringify(message));
  }

  on<T extends WebSocketMessage>(
    callback: (message: T) => void
  ): void {
    this.ws.onmessage = (event) => {
      callback(JSON.parse(event.data));
    };
  }
}
```

### 48. What are type assertions?

**Answer**: A way to tell TypeScript about a more specific type.

```typescript
const element = document.getElementById("app") as HTMLDivElement;
const value = someUnknown as string;
```

### 49. How do you handle async/await with TypeScript?

**Answer**:

```typescript
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

// Usage
const user = await fetchData<User>("/api/users/1");
```

### 50. What are the best practices for TypeScript in production?

**Answer**:
- Enable strict mode
- Use explicit return types for public APIs
- Avoid `any` — use `unknown` instead
- Use discriminated unions for complex types
- Write comprehensive tests
- Use ESLint with TypeScript rules
- Document complex types with JSDoc

## Summary

This comprehensive guide covers TypeScript interview questions from beginner to FAANG-level. Master these concepts and patterns to demonstrate your expertise in TypeScript and ace your next interview.

## Cheat Sheet

```typescript
// Type safety
let value: unknown; // Prefer over any

// Generics
function identity<T>(value: T): T { return value; }

// Utility types
type Partial<T> = { [K in keyof T]?: T[K] };

// Conditional types
type IsString<T> = T extends string ? true : false;

// Mapped types
type Readonly<T> = { readonly [K in keyof T]: T[K] };

// Type narrowing
if (typeof x === "string") { /* x is string */ }

// Discriminated unions
type Result<T> = { success: true; data: T } | { success: false; error: string };

// Exhaustive checking
function process(x: Shape): number {
  switch (x.kind) {
    case "circle": return Math.PI * x.radius ** 2;
    case "rectangle": return x.width * x.height;
    default: const _: never = x; return _;
  }
}
```

## References & Learn More

- [TypeScript Interview Questions](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Total TypeScript](https://totaltypescript.com/)
