# Modules

## Definition

**Modules** are reusable pieces of code that encapsulate functionality and can be imported/exported between files. They provide code organization, encapsulation, and dependency management in JavaScript applications.

## Why Do We Need It?

- **Code Organization**: Split code into logical files
- **Encapsulation**: Hide implementation details
- **Reusability**: Share code across files
- **Dependency Management**: Explicit imports/exports
- **Namespace**: Avoid global scope pollution

## How It Works

### CommonJS vs ES Modules

```
┌─────────────────────────────────────────────────────────────┐
│              COMMONJS vs ES MODULES                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  COMMONJS (Node.js):                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  // Export                                           │    │
│  │  module.exports = {                                  │    │
│  │    name: 'Alice',                                   │    │
│  │    greet() { return 'Hello'; }                      │    │
│  │  };                                                 │    │
│  │                                                      │    │
│  │  // Import                                           │    │
│  │  const user = require('./user');                    │    │
│  │  console.log(user.name);                            │    │
│  │                                                      │    │
│  │  • Synchronous loading                              │    │
│  │  • Runtime resolution                               │    │
│  │  • Node.js default                                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ES MODULES (Modern):                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  // Export                                           │    │
│  │  export const name = 'Alice';                       │    │
│  │  export function greet() { return 'Hello'; }       │    │
│  │                                                      │    │
│  │  // Import                                           │    │
│  │  import { name, greet } from './user.js';          │    │
│  │  import user from './user.js';  // Default          │    │
│  │  import * as user from './user.js';  // Namespace   │    │
│  │                                                      │    │
│  │  • Asynchronous loading                             │    │
│  │  • Static analysis                                  │    │
│  │  • Browser & Node.js                                │    │
│  │  • Tree shaking support                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  COMPARISON:                                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  Feature        │ CommonJS    │ ES Modules          │    │
│  │  ───────────────┼─────────────┼─────────────────── │    │
│  │  Syntax         │ require()   │ import/export       │    │
│  │  Loading        │ Synchronous │ Asynchronous        │    │
│  │  Resolution     │ Runtime     │ Static              │    │
│  │  Tree Shaking   │ No          │ Yes                 │    │
│  │  Browser Support│ No          │ Yes                 │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Module Loading

```
┌─────────────────────────────────────────────────────────────┐
│                    MODULE LOADING                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ES MODULE LOADING:                                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  1. Parse: Find all import statements              │    │
│  │  2. Resolve: Find module files                      │    │
│  │  3. Fetch: Download module code                     │    │
│  │  4. Parse: Parse module code                        │    │
│  │  5. Link: Connect exports to imports               │    │
│  │  6. Evaluate: Execute module code                   │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  DEPENDENCY GRAPH:                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                      │    │
│  │  app.js                                             │    │
│  │    ├── user.js                                      │    │
│  │    │   └── utils.js                                │    │
│  │    ├── post.js                                      │    │
│  │    │   └── user.js                                  │    │
│  │    └── comment.js                                   │    │
│  │        └── user.js                                  │    │
│  │                                                      │    │
│  │  user.js is loaded once, shared by all             │    │
│  │                                                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### ES Module Basics

```typescript
// math.ts - Export
export const PI = 3.14159;

export function add(a: number, b: number): number {
  return a + b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

export default class Calculator {
  result = 0;

  add(n: number) {
    this.result += n;
    return this;
  }

  getResult() {
    return this.result;
  }
}
```

```typescript
// app.ts - Import
import Calculator, { PI, add, multiply } from './math';

console.log(PI);  // 3.14159
console.log(add(2, 3));  // 5

const calc = new Calculator();
calc.add(5).add(10);
console.log(calc.getResult());  // 15
```

### Named vs Default Exports

```typescript
// utils.ts
export const formatDate = (date: Date) => date.toISOString();
export const parseJSON = (str: string) => JSON.parse(str);

// Default export
export default function greet(name: string) {
  return `Hello, ${name}`;
}
```

```typescript
// app.ts
// Named imports
import { formatDate, parseJSON } from './utils';

// Default import
import greet from './utils';

// Rename imports
import { formatDate as format } from './utils';

// Namespace import
import * as utils from './utils';
console.log(utils.formatDate(new Date()));
```

### Dynamic Imports

```typescript
// Lazy load module
async function loadModule() {
  const module = await import('./heavy-module');
  module.doSomething();
}

// Conditional import
if (condition) {
  const module = await import('./optional-module');
  module.doSomething();
}

// With webpack
const module = await import(
  /* webpackChunkName: "heavy" */
  './heavy-module'
);
```

### Re-exports

```typescript
// index.ts - barrel file
export { User } from './user';
export { Post } from './post';
export { Comment } from './comment';

// Or rename
export { User as UserModel } from './user';
```

### CommonJS (Node.js)

```typescript
// utils.js (CommonJS)
const PI = 3.14159;

function add(a, b) {
  return a + b;
}

module.exports = { PI, add };

// Or
exports.PI = PI;
exports.add = add;
```

```typescript
// app.js (CommonJS)
const { PI, add } = require('./utils');
// Or
const utils = require('./utils');
console.log(utils.PI);
```

## Real-World Use Cases

### 1. React Components

```typescript
// Button.tsx
export interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
}

export function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {children}
    </button>
  );
}
```

```typescript
// App.tsx
import { Button } from './Button';

function App() {
  return (
    <Button onClick={() => console.log('clicked')}>
      Click me
    </Button>
  );
}
```

### 2. Utility Library

```typescript
// utils/index.ts
export { formatDate, parseDate } from './date';
export { debounce, throttle } from './timing';
export { deepClone, isEqual } from './objects';
```

```typescript
// utils/date.ts
export function formatDate(date: Date): string {
  return date.toLocaleDateString();
}

export function parseDate(str: string): Date {
  return new Date(str);
}
```

### 3. API Client

```typescript
// api/client.ts
export class ApiClient {
  constructor(private baseUrl: string) {}

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`);
    return response.json();
  }
}

export const api = new ApiClient('https://api.example.com');
```

```typescript
// api/users.ts
import { api } from './client';

export interface User {
  id: string;
  name: string;
}

export async function getUsers(): Promise<User[]> {
  return api.get<User[]>('/users');
}
```

### 4. Configuration

```typescript
// config/index.ts
const config = {
  development: {
    apiUrl: 'http://localhost:3000',
    debug: true
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false
  }
};

const env = process.env.NODE_ENV || 'development';
export default config[env as keyof typeof config];
```

## Common Mistakes

### 1. Circular Dependencies

```typescript
// a.ts
import { b } from './b';
export const a = 'a';

// b.ts
import { a } from './a';  // Circular!
export const b = 'b';

// Solution: Restructure code, use dependency injection
```

### 2. Default vs Named Exports

```typescript
// Bad: Inconsistent exports
export default function foo() {}
export function bar() {}

// Good: Consistent pattern
// Either all default or all named
export function foo() {}
export function bar() {}
```

### 3. Import Side Effects

```typescript
// Bad: Importing for side effects
import './polyfill';
import './styles.css';

// Good: Use side-effect imports explicitly
import './polyfill';  // Document that this is for side effects
```

### 4. Missing File Extensions

```typescript
// Bad: Missing extension
import { foo } from './utils';

// Good: Explicit extension (ESM)
import { foo } from './utils.js';
```

## Best Practices

### 1. Use Named Exports

```typescript
// Good: Named exports are clearer
export function formatDate(date: Date) {}
export function parseDate(str: string) {}

// Import with clear names
import { formatDate, parseDate } from './utils';
```

### 2. Create Barrel Files

```typescript
// utils/index.ts
export * from './date';
export * from './timing';
export * from './objects';
```

### 3. Lazy Load When Possible

```typescript
// Dynamic import for code splitting
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### 4. Use TypeScript for Type Safety

```typescript
// types.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

// user.ts
import { User } from './types';
export function getUser(id: string): Promise<User> {}
```

## Performance Considerations

### Code Splitting

```typescript
// Route-based splitting
const Home = React.lazy(() => import('./pages/Home'));
const About = React.lazy(() => import('./pages/About'));

// Component-based splitting
const HeavyChart = React.lazy(() => import('./components/HeavyChart'));
```

### Tree Shaking

```typescript
// Good: Named exports for tree shaking
export function add(a: number, b: number) { return a + b; }
export function multiply(a: number, b: number) { return a * b; }

// Import only what's needed
import { add } from './math';
// multiply is not included in bundle

// Bad: Default export with everything
export default { add, multiply };
// Both are included even if only add is used
```

### Module Bundling

```
┌─────────────────────────────────────────────────────────────┐
│                    MODULE BUNDLING                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  BEFORE (Development):                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  app.js                                             │    │
│  │  ├── user.js                                        │    │
│  │  ├── post.js                                        │    │
│  │  └── utils.js                                       │    │
│  │                                                      │    │
│  │  Multiple HTTP requests                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  AFTER (Production - Bundled):                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  bundle.js (all code combined)                     │    │
│  │                                                      │    │
│  │  Single HTTP request                               │    │
│  │  Tree shaking removes unused code                  │    │
│  │  Minification reduces file size                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  TOOLS:                                                      │
│  • Webpack                                                  │
│  • Rollup                                                   │
│  • esbuild                                                  │
│  • Vite                                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5-10 questions)

**Q1: What is a module in JavaScript?**

A: A module is a reusable piece of code that encapsulates functionality and can be imported/exported between files.

**Q2: What is the difference between CommonJS and ES Modules?**

A: CommonJS uses require() and is synchronous. ES Modules use import/export and are asynchronous with static analysis.

**Q3: What is a default export?**

A: A default export is the main export of a module, imported without curly braces: `import foo from './module'`

**Q4: What is a named export?**

A: Named exports are exported with specific names, imported with curly braces: `import { foo } from './module'`

**Q5: What is tree shaking?**

A: Tree shaking is dead code elimination that removes unused exports from the final bundle.

### Intermediate (5-10 questions)

**Q6: What is a barrel file?**

A: A barrel file re-exports all exports from a directory, allowing single imports: `export * from './utils'`

**Q7: What is dynamic import?**

A: Dynamic import() loads a module asynchronously, enabling code splitting: `const module = await import('./module')`

**Q8: What are circular dependencies?**

A: When module A depends on B and B depends on A. Can cause issues with initialization order.

**Q9: How do you avoid global scope pollution with modules?**

A: Modules have their own scope. Only exported values are accessible outside.

**Q10: What is the module loading process?**

A: Parse → Resolve → Fetch → Parse → Link → Evaluate. ES Modules are loaded asynchronously.

### Senior (10-15 questions)

**Q11: How do ES Modules differ from CommonJS at runtime?**

A: CommonJS evaluates at runtime, ES Modules are statically analyzed. ES Modules are loaded asynchronously and have live bindings.

**Q12: What is the relationship between modules and bundlers?**

A: Bundlers combine modules into single files for browser delivery. They handle dependencies, code splitting, and optimization.

**Q13: How do you handle module resolution in TypeScript?**

A: Configure tsconfig.json paths, use barrel files, or use bundler's module resolution.

**Q14: What are live bindings in ES Modules?**

A: Live bindings mean imports reflect the current value of exports. If an export changes, all imports see the change.

**Q15: How do you implement lazy loading with modules?**

A: Use dynamic import() to load modules on demand, combined with React.lazy or similar patterns.

### FAANG-style (5-10 questions)

**Q16: Design a module system from scratch.**

A: Implement module loading, dependency resolution, circular dependency detection, and caching.

**Q17: How would you implement code splitting without a bundler?**

A: Use dynamic import() and HTTP/2 server push, or implement manual chunking.

**Q18: Analyze the performance implications of different module strategies.**

A: Compare loading time, bundle size, caching behavior, and runtime performance.

**Q19: How do you debug module loading issues?**

A: Use network tab, source maps, module-specific debugging tools, and console logging.

**Q20: What are security implications of modules?**

A: Code injection, dependency vulnerabilities, prototype pollution through imports.

### Follow-ups (5-10 questions)

**Q21: Can you give an example of a module-related bug in production?**

A: Circular dependency causing undefined imports at runtime.

**Q22: How do you handle modules in a monorepo?**

A: Use workspace packages, shared barrel files, and proper dependency management.

**Q23: What is the relationship between modules and micro-frontends?**

A: Each micro-frontend is a module, loaded independently, sharing dependencies.

**Q24: How do different frameworks handle modules?**

A: React: component modules. Vue: SFC modules. Angular: NgModules.

**Q25: What are best practices for working with modules?**

A: Use named exports, create barrel files, lazy load when possible, avoid circular dependencies.

## Summary

Modules are essential for modern JavaScript:

1. **CommonJS**: require(), synchronous, Node.js
2. **ES Modules**: import/export, asynchronous, modern standard
3. **Tree shaking**: Remove unused code
4. **Code splitting**: Load code on demand
5. **Best practices**: Named exports, barrel files, avoid circular deps
6. **Performance**: Lazy loading, proper bundling
7. **TypeScript**: Type safety with modules

## Cheat Sheet

```
MODULES CHEAT SHEET
═══════════════════════════════════════════════════════════════

COMMONJS (Node.js):
const { foo } = require('./module');
module.exports = { foo };

ES MODULES (Modern):
import { foo } from './module.js';
export const foo = 'bar';

DEFAULT EXPORT:
export default function foo() {}
import foo from './module.js';

NAMED EXPORTS:
export function foo() {}
import { foo } from './module.js';

DYNAMIC IMPORT:
const module = await import('./module.js');

BARREL FILE:
export * from './utils';

TREE SHAKING:
• Use named exports
• Import only what's needed
• Bundler removes unused code

CODE SPLITTING:
const Lazy = React.lazy(() => import('./Lazy'));

COMMON ISSUES:
• Circular dependencies
• Missing file extensions
• Side effect imports

BEST PRACTICES:
• Use named exports
• Create barrel files
• Lazy load when possible
• Avoid circular dependencies
• Use TypeScript

TOOLS:
• Webpack/Rollup/esbuild
• TypeScript
• Node.js
```

## References & Learn More

- [MDN: JavaScript Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- [JavaScript.info: Modules](https://javascript.info/modules-intro)
- [Node.js: CommonJS vs ES Modules](https://nodejs.org/api/esm.html)
- [LogRocket: A Guide to JavaScript Modules](https://blog.logrocket.com/a-guide-to-javascript-modules/)
