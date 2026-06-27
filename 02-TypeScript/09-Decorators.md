# Decorators

## Definition

**Decorators** are a stage 3 ECMAScript feature (and TypeScript experimental feature) that provide a way to add annotations and metadata to classes, methods, properties, and parameters. They enable metaprogramming and aspect-oriented programming patterns.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECORATOR TYPES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   @ClassDecorator                                                │
│   class MyClass {                                                │
│     @PropertyDecorator                                           │
│     myProperty: string;                                         │
│                                                                 │
│     @MethodDecorator                                             │
│     myMethod(@ParameterDecorator arg: string): void {}          │
│   }                                                              │
│                                                                 │
│   ┌──────────────────┬─────────────────────────────────────┐   │
│   │ Decorator Type   │ Applies To                          │   │
│   ├──────────────────┼─────────────────────────────────────┤   │
│   │ Class            │ Class declaration                   │   │
│   │ Method           │ Class method                        │   │
│   │ Property         │ Class property                      │   │
│   │ Parameter        │ Method/function parameter           │   │
│   └──────────────────┴─────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

1. **Metaprogramming**: Add behavior to classes and methods
2. **Code reuse**: Implement cross-cutting concerns (logging, validation)
3. **Declarative syntax**: Express intent through annotations
4. **Framework support**: Used by Angular, NestJS, TypeORM, etc.
5. **Aspect-oriented programming**: Separate concerns from business logic

## How It Works

### Experimental Decorators (TypeScript legacy)

```typescript
// Enable in tsconfig.json:
// { "experimentalDecorators": true }

// ─── Class Decorator ──────────────────────────────────────────
function Sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@Sealed
class Greeter {
  greeting: string;
  constructor(message: string) {
    this.greeting = message;
  }
  greet() {
    return "Hello, " + this.greeting;
  }
}

// ─── Method Decorator ─────────────────────────────────────────
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with`, args);
    const result = originalMethod.apply(this, args);
    console.log(`Result:`, result);
    return result;
  };
}

class Calculator {
  @Log
  add(a: number, b: number): number {
    return a + b;
  }
}

// ─── Property Decorator ───────────────────────────────────────
function Required(
  target: any,
  propertyKey: string
) {
  let value: any;

  const getter = () => value;
  const setter = (newVal: any) => {
    if (newVal === undefined || newVal === null) {
      throw new Error(`Cannot set ${propertyKey} to undefined or null`);
    }
    value = newVal;
  };

  Object.defineProperty(target, propertyKey, {
    get: getter,
    set: setter
  });
}

class User {
  @Required
  name!: string;
}

// ─── Parameter Decorator ──────────────────────────────────────
function Validate(
  target: any,
  propertyKey: string,
  parameterIndex: number
) {
  const existingRequiredParameters: number[] =
    Reflect.getOwnMetadata("required", target, propertyKey) || [];
  existingRequiredParameters.push(parameterIndex);
  Reflect.defineMetadata(
    "required",
    existingRequiredParameters,
    target,
    propertyKey
  );
}

class UserService {
  createUser(@Validate name: string, @Validate email: string): void {
    // Implementation
  }
}
```

### Stage 3 Decorators (TC39 proposal)

```typescript
// Stage 3 decorators have a different API

// ─── Class Decorator ──────────────────────────────────────────
function sealed(originalClass: new (...args: any[]) => any, context: ClassDecoratorContext) {
  Object.seal(originalClass);
  Object.seal(originalClass.prototype);
  return originalClass;
}

@sealed
class Greeter {
  greeting: string;
  constructor(message: string) {
    this.greeting = message;
  }
  greet() {
    return "Hello, " + this.greeting;
  }
}

// ─── Method Decorator ─────────────────────────────────────────
function log(originalMethod: any, context: ClassMethodDecoratorContext) {
  const methodName = String(context.name);

  return function (this: any, ...args: any[]) {
    console.log(`Calling ${methodName} with`, args);
    const result = originalMethod.call(this, ...args);
    console.log(`Result:`, result);
    return result;
  };
}

class Calculator {
  @log
  add(a: number, b: number): number {
    return a + b;
  }
}

// ─── Field Decorator ──────────────────────────────────────────
function bound(originalMethod: any, context: ClassFieldDecoratorContext) {
  const methodName = String(context.name);

  return function (this: any, ...args: any[]) {
    const result = originalMethod.call(this, ...args);
    return result;
  };
}
```

## Code Examples

### Practical Examples

```typescript
// ─── Validation Decorators ────────────────────────────────────
function Min(length: number) {
  return function (target: any, propertyKey: string) {
    let value: string;

    const getter = () => value;
    const setter = (newVal: string) => {
      if (newVal.length < length) {
        throw new Error(
          `${propertyKey} must be at least ${length} characters`
        );
      }
      value = newVal;
    };

    Object.defineProperty(target, propertyKey, {
      get: getter,
      set: setter
    });
  };
}

class Form {
  @Min(3)
  username!: string;

  @Min(8)
  password!: string;
}

// ─── Caching Decorator ────────────────────────────────────────
function Cache(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  const cache = new Map<string, any>();

  descriptor.value = function (...args: any[]) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      console.log(`Cache hit for ${propertyKey}`);
      return cache.get(key);
    }

    const result = originalMethod.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

class DataService {
  @Cache
  getUser(id: string): Promise<User> {
    console.log(`Fetching user ${id}`);
    return fetch(`/api/users/${id}`).then(r => r.json());
  }
}

// ─── Retry Decorator ──────────────────────────────────────────
function Retry(maxRetries: number = 3) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      let lastError: Error;

      for (let i = 0; i <= maxRetries; i++) {
        try {
          return await originalMethod.apply(this, args);
        } catch (error) {
          lastError = error as Error;
          console.log(`Retry ${i + 1}/${maxRetries} failed`);
          if (i < maxRetries) {
            await new Promise(resolve =>
              setTimeout(resolve, 1000 * (i + 1))
            );
          }
        }
      }

      throw lastError!;
    };
  };
}

class ApiClient {
  @Retry(3)
  async fetchData(url: string): Promise<any> {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Request failed");
    return response.json();
  }
}
```

### Advanced Patterns

```typescript
// ─── Dependency Injection ─────────────────────────────────────
const dependencies = new Map<string, any>();

function Injectable(constructor: Function) {
  dependencies.set(constructor.name, new constructor());
}

function Inject(dependency: string) {
  return function (target: any, propertyKey: string, parameterIndex: number) {
    const existingDependencies: string[] =
      Reflect.getOwnMetadata("dependencies", target, propertyKey) || [];
    existingDependencies[parameterIndex] = dependency;
    Reflect.defineMetadata("dependencies", existingDependencies, target, propertyKey);
  };
}

@Injectable
class DatabaseService {
  query(sql: string): any[] {
    return [];
  }
}

class UserService {
  constructor(
    @Inject("DatabaseService") private db: DatabaseService
  ) {}

  getUser(id: string): any {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`);
  }
}

// ─── Event Emitter Decorator ──────────────────────────────────
function OnEvent(event: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    if (!target.constructor._eventHandlers) {
      target.constructor._eventHandlers = {};
    }

    target.constructor._eventHandlers[event] = originalMethod;
  };
}

class EventHandler {
  @OnEvent("user:created")
  handleUserCreated(payload: { userId: string }): void {
    console.log(`User ${payload.userId} created`);
  }

  @OnEvent("order:placed")
  handleOrderPlaced(payload: { orderId: string }): void {
    console.log(`Order ${payload.orderId} placed`);
  }
}

// ─── Auto-bind Decorator ──────────────────────────────────────
function AutoBind(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  return {
    configurable: true,
    get() {
      const bound = originalMethod.bind(this);
      Object.defineProperty(this, propertyKey, {
        value: bound,
        configurable: true,
        writable: true
      });
      return bound;
    }
  };
}

class Button {
  label = "Click me";

  @AutoBind
  handleClick() {
    console.log(this.label);
  }
}
```

## Common Mistakes

### 1. Not Preserving `this` Context

```typescript
// ❌ Bad: Losing `this` context
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    // `this` is lost here in some contexts
    return originalMethod(...args);
  };
}

// ✅ Good: Preserve `this` context
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    return originalMethod.apply(this, args);
  };
}
```

### 2. Forgetting to Return Descriptor

```typescript
// ❌ Bad: Not returning descriptor
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    return originalMethod.apply(this, args);
  };
  // Forgot to return descriptor!
}

// ✅ Good: Return modified descriptor
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    return originalMethod.apply(this, args);
  };

  return descriptor;
}
```

### 3. Using Wrong Decorator Signature

```typescript
// ❌ Bad: Wrong signature for stage 3 decorators
function log(originalMethod: any, context: ClassMethodDecoratorContext) {
  return originalMethod;
}

// ✅ Good: Correct signature
function log(originalMethod: any, context: ClassMethodDecoratorContext) {
  const methodName = String(context.name);

  return function (this: any, ...args: any[]) {
    console.log(`Calling ${methodName}`);
    return originalMethod.call(this, ...args);
  };
}
```

## Best Practices

```typescript
// 1. Use decorators for cross-cutting concerns
// Logging, validation, caching, etc.

// 2. Keep decorators simple and focused
// One decorator, one responsibility

// 3. Document decorator behavior
/**
 * Caches method results based on arguments.
 * @Cache
 */
function Cache(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  // Implementation
}

// 4. Consider using higher-order functions instead
// Decorators are not always the best solution

// 5. Be aware of decorator ordering
// Class decorators: bottom to top
// Method decorators: right to left
```

## Performance Considerations

- **Runtime overhead**: Decorators add runtime cost
- **Memory**: Cached decorators consume memory
- **Startup time**: Many decorators slow application startup
- **Tree shaking**: Decorators may prevent tree shaking
- **Debugging**: Decorators can make debugging harder

## Interview Questions

### Beginner

1. **What are decorators?**
   - A way to add annotations and metadata to classes and members

2. **What types of decorators exist?**
   - Class, method, property, and parameter decorators

3. **How do you enable decorators in TypeScript?**
   - Set `"experimentalDecorators": true` in tsconfig.json

4. **What is a decorator factory?**
   - A function that returns a decorator

5. **What is the difference between experimental and stage 3 decorators?**
   - Different API signatures and behavior

### Intermediate

6. **How do you create a method decorator?**
   - Receive target, propertyKey, and descriptor parameters

7. **What is a decorator factory?**
   - A function that returns a decorator function

8. **How do you preserve `this` in decorators?**
   - Use `.apply(this, args)` or arrow functions

9. **Can you stack multiple decorators?**
   - Yes, they are applied bottom to top

10. **How do you add metadata with decorators?**
    - Use Reflect.defineMetadata

### Senior

11. **Design a dependency injection system using decorators**
    - Use class and parameter decorators with Reflect metadata

12. **How do you implement a logging framework with decorators?**
    - Use method decorators to wrap original methods

13. **Create a validation system using decorators**
    - Use property decorators for field validation

14. **How do you handle async decorators?**
    - Wrap async methods and return promises

### FAANG-style

15. **Build an ORM using decorators**
    - Use decorators for entity mapping, relationships

16. **Implement a middleware system using decorators**
    - Use decorators for route handlers, middleware

17. **Create a plugin system using decorators**
    - Use decorators for plugin registration

### Follow-ups

18. **How do decorators interact with inheritance?**
    - Decorators are applied to the class, not instances

19. **Can you use decorators with interfaces?**
    - No, decorators only work with classes and members

20. **How do you test code with decorators?**
    - Mock decorator behavior, test decorated methods directly

## Summary

Decorators enable metaprogramming in TypeScript, allowing you to add behavior to classes and methods declaratively. They're essential for frameworks like Angular and NestJS. Understand both experimental and stage 3 decorator APIs.

## Cheat Sheet

```typescript
// Experimental decorator
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey}`);
    return original.apply(this, args);
  };
  return descriptor;
}

// Stage 3 decorator
function log(originalMethod: any, context: ClassMethodDecoratorContext) {
  const name = String(context.name);
  return function (this: any, ...args: any[]) {
    console.log(`Calling ${name}`);
    return originalMethod.call(this, ...args);
  };
}

// Decorator factory
function Retry(maxRetries: number) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    // Implementation
  };
}

// Class decorator
function Sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}
```

## References & Learn More

- [TypeScript Handbook: Decorators](https://www.typescriptlang.org/docs/handbook/decorators.html)
- [TC39 Decorator Proposal](https://github.com/tc39/proposal-decorators)
- [TypeScript Decorators Deep Dive](https://www.typescriptlang.org/docs/handbook/decorators.html)
