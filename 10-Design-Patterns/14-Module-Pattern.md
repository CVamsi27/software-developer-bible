---
section: Design Patterns
category: Architecture
tags: [concept]
---

# Module Pattern

> **TL;DR:** The Module pattern encapsulates private state behind a public API — the foundation of clean code in any language. In ES modules it is the default (each file is a module with its own scope); historically it was IIFE / revealing module in pre-ES6 code. The senior test is using modules deliberately for encapsulation, namespacing, and tree-shaking — not just because every file is a module.
>
> **Why it matters:** This is an Architecture interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

The **Module pattern** groups related code (state + behavior) behind a defined public interface, hiding internal implementation details. In modern JavaScript/TypeScript, **ES modules** (`import` / `export`) are the native form — each `.mjs` / `.ts` file is a module with its own scope, and only the named exports are visible to importers. The historical variants are the **IIFE module** (Immediately Invoked Function Expression) and the **Revealing Module** pattern, both designed to produce privacy before ES2015. The senior design choice is using modules to enforce a clear public API and prevent accidental coupling.

## Why Do We Need It?

1. **Encapsulation** — Private state stays private; only the exported surface is part of the contract.
2. **Namespacing** — Avoid global scope pollution; multiple modules can use the same internal name without collision.
3. **Tree-shaking** — Modern bundlers (Webpack, Vite, esbuild) drop unused exports; the module pattern makes that work.
4. **Testability** — A module with a small public surface is easy to mock; private internals stay untouched.
5. **Lazy evaluation** — Top-level code in a module runs once, on first import; side effects are bounded.
6. **Dependency clarity** — `import` statements make dependencies explicit; the file is self-documenting.
7. **Refactor safety** — A module's internals can change freely; consumers only depend on the public API.

## How It Works

### Modern ES Module

```text
shapes/circle.ts
   ├── private: PI, computeArea()
   ├── exported: area(r), circumference(r)
   │
   ▼
shapes/index.ts (barrel — re-exports)
   ├── re-exports: area, circumference
   │
   ▼
main.ts
   └── import { area } from './shapes'
```

### Module Resolution

```text
import { foo } from './module'         // relative path
import { foo } from '@/lib/module'     // path alias (tsconfig / bundler)
import { foo } from 'lodash/foo'        // package
import { foo } from 'lodash'            // package main
```

### Tree-Shaking

```text
Full module exports: { a, b, c, d }
   │
   ▼
Consumer imports: { a }
   │
   ▼
Bundler output: only `a` is included; `b`, `c`, `d` are tree-shaken out
```

## Code Examples

### Modern ES Module (TypeScript)

```typescript
// shapes/circle.ts
const PI = 3.14159;                                   // private — not exported

function computeArea(r: number): number {             // private
  return PI * r * r;
}

export function area(r: number): number {             // public
  return computeArea(r);
}

export function circumference(r: number): number {    // public
  return 2 * PI * r;
}
```

```typescript
// shapes/index.ts — barrel re-export
export { area, circumference } from './circle';
export { perimeter as rectPerimeter, area as rectArea } from './rectangle';
```

```typescript
// consumer
import { area } from './shapes';
const a = area(5);            // public API
// PI is not accessible here — private to the module
```

### IIFE Module (Pre-ES6; still seen in legacy code)

```typescript
// shapes/circle.iife.ts
const Circle = (function () {
  const PI = 3.14159;            // truly private
  function computeArea(r: number) {
    return PI * r * r;
  }
  return {
    area(r: number) { return computeArea(r); },
    circumference(r: number) { return 2 * PI * r; },
  };
})();

// usage
Circle.area(5);                  // public
// PI is not accessible — IIFE captured it
```

### Revealing Module Pattern

```typescript
// utils/cache.ts
const Cache = (function () {
  const store = new Map<string, unknown>();          // private
  const hits = { count: 0 };                          // private

  function get<T>(key: string): T | undefined {
    if (store.has(key)) hits.count++;
    return store.get(key) as T | undefined;
  }

  function set(key: string, value: unknown) {
    store.set(key, value);
  }

  function stats() {                                  // public read-only view
    return { size: store.size, hits: hits.count };
  }

  return { get, set, stats };                          // public API
})();
```

### Namespace Imports vs Named Imports

```typescript
// Named imports — tree-shakable, more explicit
import { readFile } from 'fs/promises';

// Namespace import — pulls in everything
import * as fs from 'fs/promises';   // harder to tree-shake
```

### Side-Effect Module (Singleton at First Import)

```typescript
// logger/index.ts
let configured = false;

export function configure(opts: { level: string }) {
  if (configured) return;
  // one-time setup at first import
  process.env.LOG_LEVEL = opts.level;
  configured = true;
}

export function log(msg: string) { ... }
```

```typescript
// consumer
import { configure, log } from './logger';
configure({ level: 'info' });   // safe to call once
log('ready');
```

### Path Aliases (`tsconfig.json` + bundler)

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/lib/*": ["src/lib/*"],
      "@/domain/*": ["src/domain/*"]
    }
  }
}
```

```typescript
// usage
import { User } from '@/domain/user';
```

## Real-World Use Cases

1. **Domain layer** — `domain/order.ts` exports `Order`, `place()`, `cancel()`; the internal state machine and validation stay private.
2. **Service layer** — `services/payment-service.ts` exports a small public surface; the SDK clients and retry logic are private.
3. **Utility libraries** — `lib/format-date.ts` exports `formatDate`, `parseDate`; the internal locale data is private.
4. **Barrel re-exports** — `index.ts` re-exports a curated public API; consumers never reach into sub-files.
5. **Plugin systems** — A module that exports `install(app)` and `uninstall(app)`; the framework wires it via the module's public surface.
6. **Tree-shakeable SDK** — An SDK that exports hundreds of functions, but the consumer's bundle only includes what they import.
7. **Feature flags as a module** — A single import gives you the typed `flags` object; the underlying source (LaunchDarkly, Statsig) is an internal implementation detail.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `export *` from a barrel | Re-export named symbols explicitly; `export *` defeats tree-shaking and is hard to audit |
| Re-exporting internals "just in case" | Public API is a contract; smaller is better |
| `import * as X from 'X'` when a named import works | Named imports are tree-shakable; namespace imports are not |
| Side effects in module top-level code | Side effects run on import; make them idempotent or move them into an exported function |
| Circular imports | Refactor to a shared module; or use lazy `import()` inside functions |
| Mixing default + named exports | Pick one style; mixing makes it hard to know which is canonical |
| `@ts-ignore` on a private cross-module access | If you need it private, the design is wrong — talk to the owner |
| Barrel re-exports that hide circular dependencies | Audit the import graph; barrels can mask cycles |

## Best Practices

1. **Default to ES modules** — Every `.ts` / `.mjs` file is a module; use it deliberately.
2. **Small public surface** — Only `export` what consumers need; everything else is private.
3. **Barrel `index.ts` per directory** — A curated public API; refactor internal files without touching consumers.
4. **Named exports over default** — `export function area()` is more refactor-friendly than `export default { area }`.
5. **No top-level side effects** — If you need a side effect, expose a function the consumer calls; don't surprise them on import.
6. **Path aliases for readability** — `@/lib/foo` over `../../../lib/foo`.
7. **Tree-shake your own SDK** — Use named exports, side-effect-free modules; verify the bundle.
8. **Single responsibility per file** — A module that exports 30 things is doing too much; split it.
9. **Document the public API** — A `README.md` per package; or TSDoc on every export.
10. **Lock down barrel re-exports** — `export *` is a footgun; prefer explicit `export { a, b }`.

## Performance Considerations

- ES module imports are static; bundlers can analyze and tree-shake them.
- Top-level code in a module runs once per process; expensive initialization should be lazy.
- `import()` is dynamic and returns a promise; useful for code-splitting and lazy loading.
- Circular imports are evaluated with a partial export object; if you depend on the other side, you get `undefined`.
- Bundlers can split modules into chunks; use dynamic `import()` for route-level code splitting.

## Summary

- The Module pattern encapsulates private state behind a public API.
- Modern ES modules (`import` / `export`) are the canonical form; each file is a module.
- Keep the public surface small; use barrel `index.ts` to curate it; prefer named exports.
- No top-level side effects; tree-shaking is your friend; small modules are your friend.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| ES Module | Native module system in JS/TS (ES2015+); `import` / `export` |
| IIFE Module | Pre-ES6; an immediately invoked function returning a public API |
| Revealing Module | IIFE variant; private functions revealed through a return object |
| Barrel re-export | `index.ts` re-exports a curated public API |
| Tree-shaking | Bundler drops unused exports — only works with static imports + named exports |
| `export *` | Re-export everything — defeats tree-shaking; avoid |
| Side-effect import | `import './side-effect'`; runs on first import; idempotent or risky |
| Dynamic `import()` | Lazy-load a module; returns a Promise; code-splitting |
| Path alias | `@/lib/foo` resolves to `src/lib/foo` via `tsconfig` + bundler |
| Circular import | Two modules import each other; one gets a partial export; refactor |
| Named vs default export | Prefer named; default is mutable and rename-prone |

---

## See Also
- [Coding Patterns](../19-Coding-Patterns/) (module-level organization)
- [JavaScript](../01-JavaScript/) (ES modules, CommonJS, dynamic import)
- [NestJS](../06-NestJS/) (modules as DI containers)
- [System Design](../11-System-Design/) (bounded contexts as modules)

## References & Learn More

- [MDN — JavaScript Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- [TypeScript — Modules](https://www.typescriptlang.org/docs/handbook/2/modules.html)
- [Node.js — ECMAScript Modules](https://nodejs.org/api/esm.html)
- [Addy Osmani — Writing Modular JavaScript](https://addyosmani.com/blog/writing-modular-javascript/)
- [Tree-shaking — Webpack Docs](https://webpack.js.org/guides/tree-shaking/)
- [Revealing Module Pattern](https://addyosmani.com/resources/essentialjsdesignpatterns/book/#revealingmodulepatternjavascript)
