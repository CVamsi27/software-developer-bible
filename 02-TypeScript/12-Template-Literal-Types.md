# Template Literal Types

[![Category: Core](https://img.shields.io/badge/category-Core-blueviolet)](.)

## Definition

**Template literal types** are TypeScript types built using string literal types with template literal syntax (backticks). They allow you to manipulate strings at the type level — concatenating, splitting, and transforming literal types into new literal types. Introduced in TypeScript 4.1, they enable type-safe string operations, CSS property typing, event name systems, and sophisticated type transformations through `infer` and recursive conditional types.

## Why Do We Need It?

1. **Type-safe string operations** — Enforce string format constraints at compile time
2. **Pattern matching** — Extract and transform parts of string types
3. **API design** — Create type-safe event emitters, routers, and i18n systems
4. **CSS-in-JS** — Type-safe CSS property and value generation
5. **Automatic type derivation** — Derive complex types from simple string patterns

## How It Works

### Basic Syntax

```text
Template Literal Type Syntax:
═══════════════════════════════════════════════════════════════

type EventName = `on${Capitalize<string>}`;
// Generates: "onChange" | "onClick" | "onSubmit" etc.

┌─────────────────────────────────────────────────────────────┐
│ Type-Level String Interpolation:                             │
│                                                              │
│   type Greeting<T extends string> = `Hello, ${T}!`          │
│   type A = Greeting<"World">   // "Hello, World!"           │
│   type B = Greeting<"Alice">   // "Hello, Alice!"           │
│                                                              │
│ Key Points:                                                  │
│ ├── Works with string literal types                          │
│ ├── µnion types distribute (cartesian product)              │
│ ├── Supports infer for extraction                            │
│ ├── Built-in string transformers: Capitalize, Uncapitalize   │
│ ├── Uppercase, Lowercase                                      │
│ └── Can be recursive                                          │
└─────────────────────────────────────────────────────────────┘

```

### String Transformers

```typescript
// Built-in string manipulation types
type UppercaseEvent = Uppercase<'click'>;     // "CLICK"
type LowercaseEvent = Lowercase<'CLICK'>;     // "click"
type Capitalized = Capitalize<'user'>;        // "User"
type Uncapitalized = Uncapitalize<'User'>;    // "user"

// Applied in template literals
type EventHandler<T extends string> = `on${Capitalize<T>}`;
type ClickHandler = EventHandler<'click'>;    // "onClick"
type SubmitHandler = EventHandler<'submit'>;  // "onSubmit"

// Union distribution
type Events = 'click' | 'focus' | 'blur';
type Handlers = `on${Capitalize<Events>}`;
// "onClick" | "onFocus" | "onBlur"
```

### Union Distribution in Template Literals

```typescript
// Template literals distribute over unions (cartesian product)
type Horizontal = 'left' | 'center' | 'right';
type Vertical = 'top' | 'middle' | 'bottom';

type Position = `${Vertical}-${Horizontal}`;
// "top-left" | "top-center" | "top-right" |
// "middle-left" | "middle-center" | "middle-right" |
// "bottom-left" | "bottom-center" | "bottom-right"

// With string transformers
type CSSClass = `align-${Vertical}-${Horizontal}`;
// "align-top-left" | "align-top-center" | ...
```

### Inference with Template Literals

```typescript
// Extract parts of a string using infer
type ExtractRoute<T extends string> =
  T extends `${infer Method} /${infer Path}`
    ? { method: Method; path: `/${Path}` }
    : never;

type Route1 = ExtractRoute<'GET /users'>;
// { method: "GET"; path: "/users" }

type Route2 = ExtractRoute<'POST /api/v2/products'>;
// { method: "POST"; path: "/api/v2/products" }

// Extract IDs from patterns
type ExtractUserId<T extends string> =
  T extends `/users/${infer Id}`
    ? Id
    : never;

type UserId1 = ExtractUserId<'/users/abc123'>;  // "abc123"
type UserId2 = ExtractUserId<'/users/42'>;       // "42"

// Multiple inference positions
type ParsePattern<T extends string> =
  T extends `${infer Resource}:${infer Action}`
    ? { resource: Resource; action: Action }
    : never;

type Parsed = ParsePattern<'user:create'>;
// { resource: "user"; action: "create" }
```

## Code Examples

### 1. Type-Safe Event Emitter

```typescript
type EventMap = {
  'user:created': { userId: string; timestamp: number };
  'user:updated': { userId: string; changes: string[] };
  'user:deleted': { userId: string; reason: string };
  'order:placed': { orderId: string; amount: number };
  'order:shipped': { orderId: string; trackingNumber: string };
};

// Derive event names from the map
type EventName = keyof EventMap;
// "user:created" | "user:updated" | "user:deleted" | "order:placed" | "order:shipped"

// Derive handler names
type HandlerName<T extends EventName> =
  T extends `${infer Resource}:${infer Action}`
    ? `on${Capitalize<Resource>}${Capitalize<Action>}`
    : never;

type UserCreatedHandler = HandlerName<'user:created'>;
// "onUserCreated"

// Full event emitter type
class TypedEventEmitter {
  on<E extends EventName>(
    event: E,
    handler: (payload: EventMap[E]) => void
  ): void { /* ... */ }

  emit<E extends EventName>(event: E, payload: EventMap[E]): void { /* ... */ }
}

const emitter = new TypedEventEmitter();
emitter.on('user:created', ({ userId, timestamp }) => {
  // Both properties are fully typed
  console.log(userId, timestamp);
});
// emitter.on('invalid:event', () => {}); // ❌ Type error!
```

### 2. Type-Safe CSS Properties

```typescript
// CSS property types
type CSSUnit = 'px' | 'rem' | 'em' | '%' | 'vw' | 'vh' | 'pt';
type CSSValue = `${number}${CSSUnit}`;

type Width = CSSValue;  // "10px" | "2rem" | "50%" | ...
type Margin = `${CSSValue} ${CSSValue}`;  // "10px 20px"
type Padding = `${CSSValue} ${CSSValue} ${CSSValue} ${CSSValue}`;

// Type-safe CSS-in-JS
interface CSSProperties {
  width?: CSSValue;
  height?: CSSValue;
  margin?: CSSValue | Margin;
  padding?: CSSValue | Padding;
  fontSize?: CSSValue;
  gap?: CSSValue;
  borderRadius?: CSSValue;
}

const styles: CSSProperties = {
  width: '100px',      // ✅ Valid
  height: '50%',       // ✅ Valid
  // width: 'abc',     // ❌ Type error!
  // height: '10',     // ❌ Missing unit
  margin: '10px 20px', // ✅ Valid
  padding: '10px 15px 10px 15px', // ✅ Valid
};
```

### 3. Type-Safe Route Builder

```typescript
// Route definitions
type RoutePatterns = {
  'users': `/users`;
  'user-detail': `/users/${string}`;
  'user-posts': `/users/${string}/posts`;
  'user-post-detail': `/users/${string}/posts/${string}`;
  'products': `/products`;
  'product-detail': `/products/${string}`;
};

// Route params extractor
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractParams<`/${Rest}`>]: string }
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

type UserParams = ExtractParams<'/users/:id'>;
// { id: string }

type PostParams = ExtractParams<'/users/:userId/posts/:postId'>;
// { userId: string; postId: string }

// Type-safe route builder
function buildPath<T extends RoutePatterns[keyof RoutePatterns]>(
  pattern: T,
  params: ExtractParams<T>
): string {
  let path = pattern as string;
  for (const [key, value] of Object.entries(params)) {
    path = path.replace(`:${key}`, value as string);
  }
  return path;
}

const path1 = buildPath('/users/:id', { id: '42' });
// Result: "/users/42"
const path2 = buildPath('/users/:userId/posts/:postId', {
  userId: 'abc',
  postId: '123',
});
// Result: "/users/abc/posts/123"
```

### 4. CSS Class Name Builder

```typescript
// Utility classes
type Spacing = '0' | '1' | '2' | '4' | '8' | '16' | '32';
type Direction = 't' | 'b' | 'l' | 'r' | 'x' | 'y' | '';
type Breakpoint = '' | 'sm:' | 'md:' | 'lg:' | 'xl:';

// Generate margin/padding classes
type SpacingClass<Prefix extends string> =
  `${Breakpoint}${Prefix}${Direction}-${Spacing}`;

type MarginClass = SpacingClass<'m'>;
// "m-0" | "m-1" | ... | "mt-0" | "mb-8" | "sm:mx-4" | ...

type PaddingClass = SpacingClass<'p'>;
// "p-0" | "p-1" | ... | "pt-16" | "md:px-2" | ...

// Color classes
type Color = 'red' | 'blue' | 'green' | 'gray' | 'indigo';
type Shade = '50' | '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900';
type ColorClass = `text-${Color}-${Shade}` | `bg-${Color}-${Shade}` | `border-${Color}-${Shade}`;
// "text-red-500" | "bg-blue-200" | "border-green-600" | ...

// Combined utility type
type TailwindClass = SpacingClass<'m'> | SpacingClass<'p'> | ColorClass;

function cn(...classes: TailwindClass[]): string {
  return classes.join(' ');
}

cn('m-4', 'p-2', 'text-red-500');       // ✅ Valid
// cn('invalid-class');                   // ❌ Type error
```

### 5. String Transformations

```typescript
// SnakeCase to CamelCase
type SnakeToCamel<S extends string> =
  S extends `${infer T}_${infer U}`
    ? `${T}${Capitalize<SnakeToCamel<U>>}`
    : S;

type CamelCase1 = SnakeToCamel<'user_name'>;
// "userName"
type CamelCase2 = SnakeToCamel<'first_last_name'>;
// "firstName"
type CamelCase3 = SnakeToCamel<'user_profile_data'>;
// "userProfileData"

// CamelCase to KebabCase
type CamelToKebab<S extends string> =
  S extends `${infer T}${infer U}`
    ? T extends Uppercase<T>
      ? `-${Lowercase<T>}${CamelToKebab<U>}`
      : `${T}${CamelToKebab<U>}`
    : S;

type Kebab1 = CamelToKebab<'backgroundColor'>;
// "background-color"
type Kebab2 = CamelToKebab<'fontSize'>;
// "font-size"
type Kebab3 = CamelToKebab<'borderRadius'>;
// "border-radius"

// SnakeCase to KebabCase
type SnakeToKebab<S extends string> =
  S extends `${infer T}_${infer U}`
    ? `${T}-${SnakeToKebab<U>}`
    : S;

type Kebab4 = SnakeToKebab<'user_profile'>;
// "user-profile"

// Type-safe object key converter
type ConvertKeys<T, Converter extends (s: string) => string> = {
  [K in keyof T as Converter<string & K>]: T[K];
};

interface ApiResponse {
  user_name: string;
  user_email: string;
  created_at: Date;
}

type FrontendResponse = ConvertKeys<ApiResponse, SnakeToCamel>;
// {
//   userName: string;
//   userEmail: string;
//   createdAt: Date;
// }
```

### 6. Deep Path Extraction

```typescript
// Type-safe object path access
type PathImpl<T, K extends keyof T> =
  K extends string
    ? T[K] extends Record<string, any>
      ? `${K}.${PathImpl<T[K], keyof T[K]> & string}`
      : K
    : never;

type Path<T> = PathImpl<T, keyof T> & string;

interface NestedConfig {
  database: {
    host: string;
    port: number;
    credentials: {
      user: string;
      password: string;
    };
  };
  cache: {
    ttl: number;
    redis: {
      host: string;
      port: number;
    };
  };
}

type ConfigPaths = Path<NestedConfig>;
// "database.host" | "database.port" | "database.credentials.user"
// | "database.credentials.password" | "cache.tti" | "cache.redis.host"
// | "cache.redis.port"

// Get nested value type from path
type GetValue<T, P extends string> =
  P extends `${infer Key}.${infer Rest}`
    ? Key extends keyof T
      ? GetValue<T[Key], Rest>
      : never
    : P extends keyof T
      ? T[P]
      : never;

type HostType = GetValue<NestedConfig, 'database.host'>;
// string
type PortType = GetValue<NestedConfig, 'database.port'>;
// number
type PasswordType = GetValue<NestedConfig, 'database.credentials.password'>;
// string
```

### 7. Type-Safe i18n / Localization

```typescript
type Locale = 'en' | 'es' | 'fr' | 'de';

type TranslationKeys = {
  'welcome': `welcome.${Locale}`;
  'goodbye': `goodbye.${Locale}`;
  'error.not_found': `error.not_found.${Locale}`;
  'error.server': `error.server.${Locale}`;
};

type TranslationKey = TranslationKeys[keyof TranslationKeys];
// "welcome.en" | "welcome.es" | ... | "error.server.de"

// Type-safe translation function
function t(key: TranslationKey, params?: Record<string, string>): string {
  // Implementation
  return key;
}

t('welcome.en');             // ✅ Valid
t('error.not_found.fr');     // ✅ Valid
// t('invalid.key');         // ❌ Type error!

// Parameterized translations
type ParamTranslation<T extends string> =
  T extends `${infer Key}.${Locale}` ? Key : never;

type WelcomeKey = ParamTranslation<'welcome.en'>;
// "welcome"

// With parameters
type TFunc = {
  <K extends TranslationKey>(key: K): string;
  <K extends TranslationKey, P extends Record<string, string>>(
    key: K,
    params: P
  ): string;
};

const translate: TFunc = (key: string, params?: Record<string, string>) => {
  let value = getTranslation(key); // Fetch from dictionary
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      value = value.replace(`{{${k}}}`, v);
    });
  }
  return value;
};

const greeting = translate('welcome.en', { name: 'Alice' });
```

### 8. Join and Split Types

```typescript
// Join array of strings
type Join<T extends string[], Separator extends string = ','> =
  T extends [infer F, ...infer R]
    ? F extends string
      ? R extends string[]
        ? R['length'] extends 0
          ? F
          : `${F}${Separator}${Join<R, Separator>}`
        : never
      : never
    : '';

type Joined1 = Join<['a', 'b', 'c']>;
// "a,b,c"
type Joined2 = Join<['a', 'b', 'c'], '-'>;
// "a-b-c"
type Joined3 = Join<['hello'], '.'>;
// "hello"

// Split string into tuple
type Split<S extends string, D extends string = ','> =
  string extends S ? string[] :
  S extends '' ? [] :
  S extends `${infer T}${D}${infer U}`
    ? [T, ...Split<U, D>]
    : [S];

type Split1 = Split<'a,b,c'>;
// ["a", "b", "c"]
type Split2 = Split<'hello world', ' '>;
// ["hello", "world"]
type Split3 = Split<'user:42:active', ':'>;
// ["user", "42", "active"]
```

### 9. Object Key Prefixed Types

```typescript
// Add prefix to all keys
type PrefixedKeys<T, Prefix extends string> = {
  [K in keyof T as `${Prefix}${string & Capitalize<K & string>}`]: T[K];
};

interface User {
  name: string;
  email: string;
  age: number;
}

type PrefixedUser = PrefixedKeys<User, 'user'>;
// {
//   userName: string;
//   userEmail: string;
//   userAge: number;
// }

// Add suffix to all keys
type SuffixedKeys<T, Suffix extends string> = {
  [K in keyof T as `${string & K}${Suffix}`]: T[K];
};

type ApiUser = SuffixedKeys<User, '_api'>;
// {
//   name_api: string;
//   email_api: string;
//   age_api: number;
// }

// Remove prefix from keys
type RemovePrefix<T, Prefix extends string> = {
  [K in keyof T as K extends `${Prefix}${infer Rest}`
    ? Uncapitalize<Rest>
    : K
  ]: T[K];
};

type RawUser = RemovePrefix<PrefixedUser, 'User'>;
// Reverts back to: { name: string; email: string; age: number }
```

### 10. Recursive String Utility Types

```typescript
// Trim whitespace
type TrimLeft<S extends string> =
  S extends `${' ' | '\n' | '\t'}${infer Rest}`
    ? TrimLeft<Rest>
    : S;

type TrimRight<S extends string> =
  S extends `${infer Rest}${' ' | '\n' | '\t'}`
    ? TrimRight<Rest>
    : S;

type Trim<S extends string> = TrimLeft<TrimRight<S>>;

type Trimmed1 = Trim<'  hello  '>;   // "hello"
type Trimmed2 = Trim<'\n\t world \n'>; // "world"

// Repeat string N times (using array accumulator for type-level length tracking)
type Repeat<S extends string, N extends number, Acc extends never[] = []> =
  Acc['length'] extends N ? '' : `${S}${Repeat<S, N, [...Acc, never]>}`;

type Dashes = Repeat<'-', 5>;     // "-----"
type Dots = Repeat<'.', 3>;      // "..."

// Replace all occurrences
type ReplaceAll<S extends string, From extends string, To extends string> =
  S extends `${infer Head}${From}${infer Tail}`
    ? `${Head}${To}${ReplaceAll<Tail, From, To>}`
    : S;

type Replaced1 = ReplaceAll<'a-b-c-d', '-', '_'>;
// "a_b_c_d"
type Replaced2 = ReplaceAll<'user@example.com', '@', '[at]'>;
// "user[at]example.com"
```

## Real-World Use Cases

### MongoDB/Prisma Query Builder

```typescript
// Type-safe field selection
type SelectFields<T> = {
  [K in keyof T as K extends string ? K : never]?: boolean;
};

// Combined with template literals for nested selects
type DeepSelect<T, Prefix extends string = ''> = {
  [K in keyof T & string as `${Prefix}${K}`]?:
    T[K] extends Record<string, any>
      ? DeepSelect<T[K], `${Prefix}${K}.`>
      : boolean;
};
```

### API Client Generator

```typescript
// Type-safe API endpoints
type ApiVersion = 'v1' | 'v2';
type ApiResource = 'users' | 'posts' | 'comments' | 'products';
type ApiAction = 'list' | 'get' | 'create' | 'update' | 'delete';

type ApiEndpoint = `/api/${ApiVersion}/${ApiResource}`;
type ApiResourceEndpoint<T extends ApiResource> = `/api/v1/${T}`;
type ApiActionEndpoint<T extends ApiResource, A extends ApiAction> =
  A extends 'list' ? `/api/v1/${T}` :
  A extends 'get' ? `/api/v1/${T}/:id` :
  A extends 'create' ? `/api/v1/${T}` :
  A extends 'update' ? `/api/v1/${T}/:id` :
  A extends 'delete' ? `/api/v1/${T}/:id` :
  never;
```

## Common Mistakes

### 1. Recursive Type Instantiation Limits

```typescript
// ❌ BAD: Deep recursion hits TypeScript's instantiation limit
type DeepReplace<T extends string> =
  T extends `${infer A}${infer B}${infer C}${infer D}${infer Rest}`
    ? `${A}${DeepReplace<Rest>}` // Too deep!
    : T;

// ✅ GOOD: Limit recursion depth with bailout conditions
type SafeReplace<T extends string, Depth extends number = 10> =
  Depth extends 0 ? T :
  T extends `${infer A}${infer Rest}`
    ? `${A}${SafeReplace<Rest, SubtractOne<Depth>>}`
    : T;

// Helper: Decrement a number type (limited to small values)
type SubtractOne<N extends number> =
  N extends 10 ? 9 : N extends 9 ? 8 : N extends 8 ? 7 :
  N extends 7 ? 6 : N extends 6 ? 5 : N extends 5 ? 4 :
  N extends 4 ? 3 : N extends 3 ? 2 : N extends 2 ? 1 : 0;
```

### 2. Type Instantiation Explosion

```typescript
// ❌ BAD: Generates ALL combinations → Slow compilation
type Colors = 'red' | 'green' | 'blue';
type Sizes = 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
type States = 'hover' | 'active' | 'focus' | 'disabled';

// 3 × 6 × 4 = 72 combinations (manageable)
type AllClasses = `${Colors}-${Sizes}-${States}`;

// ❌ BAD: 3 × 6 × 4 × 100 (if more unions combined)
// Use sparingly with large unions

// ✅ GOOD: Limit union combinations
type ColorSize = `${Colors}-${Sizes}`; // Only 18 combinations
```

### 3. Forgetting Union Distribution

```typescript
// ❌ BAD: Doesn't distribute as expected
type WrapString<T> = T extends string ? `~${T}~` : T;
type Result = WrapString<'a' | 'b'>;
// "~a~" | "~b~" ✅ (actually distributes correctly in template literals)

// ✅ GOOD: Template literals automatically distribute
type Wrapped = `~${'a' | 'b'}~`;
// "~a~" | "~b~"
```

## Best Practices

```typescript
// 1. Use template literal types for API/event patterns
type EventNames = `on${Capitalize<string>}`;

// 2. Combine with infer for extraction
type ExtractId<T extends string> =
  T extends `/users/${infer Id}` ? Id : never;

// 3. Use recursive types cautiously
type Repeat<T extends string, N extends number, Acc extends never[] = []> =
  Acc['length'] extends N ? '' : `${T}${Repeat<T, N, [...Acc, never]>}`;

// 4. Limit union sizes to avoid type explosion
type SmallUnion = 'a' | 'b' | 'c';
type Combined = `prefix-${SmallUnion}`; // 3 combinations ✅

// 5. Leverage built-in string transformers
// Capitalize, Uncapitalize, Uppercase, Lowercase

// 6. Document complex template literal types
/**
 * Converts snake_case string to camelCase at the type level
 * @example SnakeToCamel<'user_name'> → "userName"
 */
type SnakeToCamel<S extends string> = /* ... */;
```

## Performance Considerations

```text
Template Literal Type Performance:
═══════════════════════════════════════════════════════════════

Small Unions (< 10):
├── Compilation: Instant
└── IDE performance: Excellent

Medium Unions (10-50):
├── Compilation: Fast (< 100ms)
└── IDE performance: Good

Large Unions (50-500):
├── Compilation: Moderate (100-500ms)
└── IDE performance: Noticeable lag

Very Large Unions (500+):
├── Compilation: Slow (> 1s)
├── IDE performance: Poor
└── Consider limiting combinations

Recursive Types:
├── Depth limit: ~50 levels (configurable)
├── Each recursion creates type instantiations
├── Use bailout conditions for safety
└── Monitor with --diagnostics flag

```

## Summary

Template literal types enable powerful string manipulation at the TypeScript type level. They are essential for type-safe event emitters, CSS-in-JS, API route builders, and string transformation utilities. Combine them with `infer`, recursive conditional types, and mapped types for sophisticated type systems.

## Cheat Sheet

```typescript
// Basic syntax
type Greeting = `Hello, ${string}!`;

// String transformers
type Upper = Uppercase<'hello'>;           // "HELLO"
type Lower = Lowercase<'HELLO'>;           // "hello"
type Capital = Capitalize<'hello'>;        // "Hello"
type Uncapital = Uncapitalize<'Hello'>;    // "hello"

// Union distribution
type Colored = `text-${'red' | 'blue'}-500`;
// "text-red-500" | "text-blue-500"

// Inference
type ExtractId<T> = T extends `/users/${infer Id}` ? Id : never;

// Snake to Camel
type SnakeToCamel<S> =
  S extends `${infer T}_${infer U}`
    ? `${T}${Capitalize<SnakeToCamel<U>>}`
    : S;

// Camel to Kebab
type CamelToKebab<S> =
  S extends `${infer T}${infer U}`
    ? T extends Uppercase<T>
      ? `-${Lowercase<T>}${CamelToKebab<U>}`
      : `${T}${CamelToKebab<U>}`
    : S;

// Key transformation
type Prefixed<T, P extends string> = {
  [K in keyof T as `${P}${Capitalize<string & K>}`]: T[K];
};

// Join & Split
type Join<T extends string[], D extends string> = /* ... */;
type Split<S extends string, D extends string> = /* ... */;

// Replace
type ReplaceAll<S, F extends string, T extends string> =
  S extends `${infer H}${F}${infer Tail}`
    ? `${H}${T}${ReplaceAll<Tail, F, T>}`
    : S;
```

---

## See Also
- [Advanced Generics](10-Advanced-Generics.md)
- [Branded Types](13-Branded-Types.md)
- [Conditional Types](04-Conditional-Types.md)
- [Declaration Files](14-Declaration-Files.md)
- [Infer](05-Infer.md)
- [JavaScript](../01-JavaScript/)
- [keyof / typeof](06-Keyof-typeof.md)
- [Mapped Types](07-Mapped-Types.md)
- [NestJS](../06-NestJS/)
- [React](../03-React/)

## References & Learn More

- [TypeScript Handbook: Template Literal Types](https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html)
- [TypeScript 4.1 Release Notes](https://devblogs.microsoft.com/typescript/announcing-typescript-4-1/#template-literal-types)
- [TypeScript Deep Dive: Template Literal Types](https://basarat.gitbook.io/typescript/type-system/template-literal-types)
- [Type Challenges: Template Literal Type Exercises](https://github.com/type-challenges/type-challenges)
