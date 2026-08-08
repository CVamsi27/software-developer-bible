---
section: TypeScript
category: Core
tags: [concept]
---

# The `satisfies` Operator

## TL;DR

The `satisfies` operator (TS 4.9+) validates that an expression matches a type **without widening** the inferred type. It's the answer to the long-standing tension between "I want to be sure this object matches the contract" and "I want autocomplete on the specific keys I wrote." Use it whenever you need both: type safety AND literal-type preservation.

## Why It Matters

Before `satisfies`, you chose between a type annotation (loses literals, gains safety) and a type assertion (keeps literals, loses safety). `satisfies` gives you both: validation AND preservation. Senior engineers use it for: configuration objects, route tables, event handlers, and any place where you want to type-check without erasing literal info that downstream code depends on.

## Definition

`satisfies` is a TypeScript operator introduced in 4.9 that checks an expression is assignable to a type, but returns the expression's original (narrower) inferred type rather than the constraint type. It sits between type assertions (`as`) and type annotations (`:`) in terms of safety.

```typescript
const config = {
  port: 3000,
  host: 'localhost',
  debug: true,
} satisfies ServerConfig;
// config.port is typed as 3000 (literal), not number
// config.host is typed as 'localhost' (literal), not string
// but TS verifies the whole object matches ServerConfig
```

## Why Do We Need It?

1. **Type validation without type widening** — Verify the shape matches a contract while keeping specific keys literal
2. **Better autocomplete** — `satisfies` keeps the narrower inferred type, so `config.host.` shows the literal-specific operations
3. **Catch typos early** — A misspelled property becomes a compile error, but valid keys still have their specific types
4. **Replace dangerous `as` casts** — `as` is unchecked; `satisfies` is checked
5. **Improve object literal ergonomics** — Especially for unions, `Record<string, X>`, and config-driven code

## How It Works

### The Problem `satisfies` Solves

```typescript
type Routes = Record<string, { path: string; auth: boolean }>;

// ❌ Annotation: types widened, lose literal info
const routes: Routes = {
  home: { path: '/', auth: false },
  admin: { path: '/admin', auth: true },
};
routes.home; // typed as { path: string; auth: boolean } — useless for autocomplete

// ❌ Assertion: keeps literals, but unchecked
const routes = {
  home: { path: '/', auth: false },
  admin: { path: '/admin', auth: true },
} as Routes;
// Works, but typos go undetected:
// routes.admni = ... — silently typed as Routes, no error

// ✅ satisfies: validates AND preserves literals
const routes = {
  home: { path: '/', auth: false },
  admin: { path: '/admin', auth: true },
} satisfies Routes;
// routes.home.path is 'string' (not '/' — autocompletion is limited to the wider type)
// But typos are caught: routes.admni — error
```

### Comparing the Three Approaches

```typescript
type Color = 'red' | 'green' | 'blue';

const obj1: Record<string, Color> = { primary: 'red' };
// obj1.primary is typed as Color — narrowed info lost

const obj2 = { primary: 'red' } as Record<string, Color>;
// obj2.primary is typed as 'red' — but no validation against the type

const obj3 = { primary: 'red' } satisfies Record<string, Color>;
// obj3.primary is typed as 'red' AND validated against the type
```

### Common Use Cases

```typescript
// ─── 1. Config validation ─────────────────────────────────────
type FeatureFlags = Record<string, boolean>;

const flags = {
  newCheckout: true,
  darkMode: false,
  betaSearch: true,
} satisfies FeatureFlags;
// Each flag keeps its literal boolean type (useful for tree-shaking)

// ─── 2. Discriminated union narrowing ─────────────────────────
type Event =
  | { type: 'click'; x: number; y: number }
  | { type: 'keypress'; key: string }
  | { type: 'resize'; width: number; height: number };

const handler: Event = { type: 'click', x: 10, y: 20 };
// Without satisfies: handler is typed as Event (the union) — narrowing is needed
// With satisfies on a wider value, you still preserve the literal 'click'

// ─── 3. Tuple validation with literal preservation ────────────
type Routes = ['home' | 'about' | 'contact', string];
const r = ['home', '/'] satisfies Routes;
// r[0] is 'home' (not 'home' | 'about' | 'contact')

// ─── 4. Object with optional vs required keys ─────────────────
type ApiResponse = {
  data?: unknown;
  error?: { code: number; message: string };
};

const res = { data: { id: 1 } } satisfies ApiResponse;
// res.data is typed as { id: number } — not unknown
// But TS checks: if you wrote res.erro, that's a typo and an error
```

## Code Examples

### Real-World: Feature Flag System

```typescript
type FlagConfig = {
  key: string;
  defaultValue: boolean;
  description: string;
};

const flags = [
  { key: 'newCheckout', defaultValue: false, description: 'New checkout flow' },
  { key: 'darkMode',    defaultValue: true,  description: 'Dark mode UI' },
] satisfies FlagConfig[];
// Each flag retains its literal `key` type — useful for type-safe lookups
type FlagKey = typeof flags[number]['key']; // 'newCheckout' | 'darkMode'

function isEnabled(key: FlagKey): boolean { /* ... */ }
isEnabled('newCheckout'); // ✅
isEnabled('typo');         // ❌ Type error
```

### Real-World: Server Route Table

```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
type RouteDefinition = {
  method: HttpMethod;
  path: string;
  handler: string; // handler name for reference
};

const routes = {
  getUser:    { method: 'GET',    path: '/users/:id',  handler: 'getUser' },
  createUser: { method: 'POST',   path: '/users',       handler: 'createUser' },
  deleteUser: { method: 'DELETE', path: '/users/:id',  handler: 'deleteUser' },
} satisfies Record<string, RouteDefinition>;

// routes.getUser.method is typed as 'GET' (literal), not HttpMethod
// TS validates every entry matches RouteDefinition
// A typo like `methods` would be caught at compile time
```

### Real-World: Color Palette with Strict Keys

```typescript
type Palette = Record<string, `#${string}`>;

const palette = {
  primary:   '#3b82f6',
  secondary: '#10b981',
  danger:    '#ef4444',
} satisfies Palette;

// palette.primary is '#3b82f6' (literal), enabling:
// - Tree-shaking of unused colors
// - Literal-based deduplication
// - IDE goto-definition to the actual hex value
// And TypeScript verifies every value matches the `#${string}` pattern
```

## Real-World Use Cases

1. **Feature flag tables** — Keep literal key types for type-safe lookups while validating the schema
2. **Route/endpoint definitions** — Validate HTTP method is one of the allowed set, keep literal for navigation
3. **i18n message catalogs** — Validate every locale key exists, keep literal key types for tree-shaking
4. **Theme/palette configs** — Validate color formats (`#${string}`) while keeping specific hex values literal
5. **Zod/Valibot-style schema output** — Validate a const matches a schema, preserve narrower types
6. **Enum-like const objects** — Validate it satisfies `Record<string, X>`, preserve literal values for exhaustive switches

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `satisfies` when you want to constrain a parameter | Use type annotation `:` for that — `satisfies` doesn't constrain the inferred type |
| Using `as` instead of `satisfies` to "cast" literals | Replace with `satisfies` — `as` is unchecked and a frequent source of runtime bugs |
| Putting `satisfies` on a value that needs to be assignable elsewhere | `satisfies` is stricter than `as`; if you need flexibility, use `as` (sparingly) |
| Confusing `satisfies T` with `T =` (constraint on generic) | Different operators: `satisfies` is for expressions, `extends`/default is for generics |
| Expecting `satisfies` to widen a too-narrow type | `satisfies` never widens — if the value is narrower than T, you must widen first (or use `as`) |
| Using `satisfies` to assert a value is `any` (defeating safety) | Don't. The whole point of `satisfies` is type-level validation |

## Best Practices

1. **Default to `satisfies` for `const` objects** — Validation + literal preservation is almost always what you want
2. **Use type annotations for function parameters and exports** — `satisfies` doesn't change assignability, so exported values still need annotations for cross-module contracts
3. **Use `satisfies` with `Record<string, X>` to validate AND keep literals** — This is the canonical use case
4. **Combine with `as const` when you want maximally narrow types** — `as const` + `satisfies T` gives you both worlds
5. **Don't replace `as` entirely** — `as` is still useful for genuinely necessary widening (e.g., parsed JSON before validation)
6. **Use `satisfies` to check discriminated unions** — Validates the `type` field is a known value while preserving literal

```typescript
// Best-practice combination
const config = {
  host: 'localhost',
  port: 3000,
} as const satisfies ServerConfig;
// Maximally narrow types, validated against the schema
```

## Performance Considerations

| Aspect | Impact |
|--------|--------|
| Compile time | Negligible — `satisfies` is a single type-check pass |
| Runtime | Zero — pure compile-time operator, no JS emitted |
| Editor performance | Slightly slower for very large `satisfies` expressions on `Record<string, X>`, but rarely a problem |
| IDE autocomplete | Improved — narrower types mean more specific completions |

**Caveat:** `satisfies` is not the same as `as const`. `as const` makes everything `readonly` and turns literals into their most specific type. `satisfies` validates a type without changing the inferred shape. They compose well:

```typescript
// Strictest: literal + readonly + validated
const config = {
  host: 'localhost',
  port: 3000,
} as const satisfies ServerConfig;
```

## Summary

The `satisfies` operator (TS 4.9+) validates an expression against a type while preserving its inferred (often literal) type. It's the right tool when you need both: type safety AND autocomplete on specific keys. Use it for config objects, route tables, enum-like const maps, and any place you previously had to choose between `:` (loses literals) and `as` (unchecked). Combine with `as const` for the strictest contracts.

## Cheat Sheet

| Operation | Validates Type | Preserves Literals | Use When |
|-----------|:--------------:|:------------------:|----------|
| `const x: T = ...` (annotation) | ✅ | ❌ Widens to T | Constraining parameters, exports |
| `const x = ... as T` (assertion) | ❌ Unchecked | ✅ | Necessary widening, JSON before validation |
| `const x = ... satisfies T` | ✅ | ✅ | Configs, route tables, enum-like maps |
| `const x = ... as const satisfies T` | ✅ | ✅ + readonly | Strictest contracts — readonly + validated + literal |

**Decision tree:**
- Need to constrain a function parameter or export? → Use annotation `: T`
- Need to widen a value you know is correct? → Use `as T` (sparingly)
- Need both: type safety AND specific key autocomplete? → Use `satisfies T`
- Need the strictest possible contract? → Use `as const satisfies T`

---

## See Also
- [Advanced Generics](10-Advanced-Generics.md)
- [Mapped Types](07-Mapped-Types.md)
- [Type Narrowing](08-Type-Narrowing.md)
- [Types vs Interfaces](01-Types-vs-Interfaces.md)
- [Utility Types](03-Utility-Types.md)

## References & Learn More

- [TypeScript 4.9 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html#the-satisfies-operator)
- [TypeScript Handbook: Type Assertions vs satisfies](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)
- [TypeScript PR #46883: The satisfies operator](https://github.com/microsoft/TypeScript/pull/46883)
- [Total TypeScript: satisfies patterns](https://www.totaltypescript.com/tutorials/the-satisfies-operator)
