# Dependency Injection

## Definition

**Dependency Injection (DI)** is a design pattern where an object receives its dependencies from an external source rather than creating them itself. NestJS has a built-in **IoC (Inversion of Control) container** that manages the entire dependency graph of an application — creating, resolving, and injecting dependencies automatically.

In NestJS, DI works through constructor injection: you declare dependencies as constructor parameters, and the framework resolves and injects them at runtime.

## Why Do We Need It?

1. **Loose Coupling**: Components depend on abstractions, not concrete implementations.
2. **Testability**: Easy to mock dependencies for unit testing.
3. **Maintainability**: Dependencies are explicitly declared and managed centrally.
4. **Reusability**: Services can be used in different contexts with different implementations.
5. **Lifecycle Management**: The container manages instantiation, scoping, and cleanup.
6. **Configuration**: Different configurations for different environments through DI.

## How It Works

NestJS's DI container works in several phases:

1. **Collection**: Gather all providers from modules
2. **Resolution**: Build a dependency graph
3. **Instantiation**: Create instances in topological order
4. **Injection**: Inject dependencies through constructors
5. **Caching**: Cache instances for singleton scope

### DI Resolution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DI Resolution Flow                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Collect all providers from all modules                  │
│     ┌─────────────────────────────────────────────────────┐ │
│     │ ModuleA: [ServiceA, RepoA]                          │ │
│     │ ModuleB: [ServiceB, RepoB]                          │ │
│     │ ModuleC: [ServiceC, RepoC]                          │ │
│     └─────────────────────────────────────────────────────┘ │
│                         │                                   │
│                         ▼                                   │
│  2. Build dependency graph                                  │
│     ┌─────────────────────────────────────────────────────┐ │
│     │ ServiceA ──▶ RepoA                                  │ │
│     │ ServiceB ──▶ ServiceA, RepoB                        │ │
│     │ ServiceC ──▶ ServiceA, ServiceB, RepoC              │ │
│     └─────────────────────────────────────────────────────┘ │
│                         │                                   │
│                         ▼                                   │
│  3. Resolve in topological order (leaf nodes first)         │
│     RepoA, RepoB, RepoC ──▶ ServiceA ──▶ ServiceB ──▶ SC  │
│                         │                                   │
│                         ▼                                   │
│  4. Instantiate and cache (singleton)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Constructor Injection

```
┌──────────────────────────────────────────────────────┐
│                 Constructor Injection                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  @Injectable()                                       │
│  class OrderService {                                │
│    constructor(                                      │
│      private userRepo: UserRepository,  ◀──注入      │
│      private paymentSvc: PaymentService, ◀──注入     │
│      private cache: CacheService,         ◀──注入    │
│    ) {}                                              │
│  }                                                   │
│                                                      │
│  NestJS Container:                                   │
│  ┌────────────────────────────────────────────────┐  │
│  │ 1. Create UserRepository instance              │  │
│  │ 2. Create PaymentService instance              │  │
│  │ 3. Create CacheService instance                │  │
│  │ 4. Create OrderService with all three injected │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Constructor Injection

```typescript
// user.service.ts
import { Injectable } from '@nestjs/common';
import { UserRepository } from './user.repository';
import { CacheService } from '../cache/cache.service';

@Injectable()
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly cacheService: CacheService,
  ) {}

  async findAll() {
    const cached = await this.cacheService.get('users');
    if (cached) return cached;

    const users = await this.userRepository.findAll();
    await this.cacheService.set('users', users, 300);
    return users;
  }
}
```

### Injection Tokens

```typescript
// Using string tokens
export const PAYMENT_SERVICE = 'PAYMENT_SERVICE';
export const EMAIL_SERVICE = 'EMAIL_SERVICE';

// provider.ts
import { Injectable } from '@nestjs/common';

export interface PaymentService {
  charge(amount: number): Promise<boolean>;
}

@Injectable()
export class StripePaymentService implements PaymentService {
  async charge(amount: number): Promise<boolean> {
    // Stripe implementation
    return true;
  }
}

// module.ts
@Module({
  providers: [
    {
      provide: PAYMENT_SERVICE,
      useClass: StripePaymentService,
    },
  ],
})
export class PaymentModule {}

// Usage
@Injectable()
export class OrderService {
  constructor(
    @Inject(PAYMENT_SERVICE)
    private readonly paymentService: PaymentService,
  ) {}
}
```

### Symbol Injection Tokens

```typescript
// tokens.ts
export const LOGGER_TOKEN = Symbol('Logger');
export const CACHE_TOKEN = Symbol('Cache');

// module.ts
@Module({
  providers: [
    {
      provide: LOGGER_TOKEN,
      useClass: WinstonLoggerService,
    },
    {
      provide: CACHE_TOKEN,
      useClass: RedisCacheService,
    },
  ],
})
export class CoreModule {}

// Usage
@Injectable()
export class AppService {
  constructor(
    @Inject(LOGGER_TOKEN)
    private readonly logger: LoggerService,
    @Inject(CACHE_TOKEN)
    private readonly cache: CacheService,
  ) {}
}
```

### Interface Injection

```typescript
// interfaces/user-service.interface.ts
export interface IUserService {
  findAll(): Promise<User[]>;
  findOne(id: string): Promise<User>;
  create(dto: CreateUserDto): Promise<User>;
}

// concrete implementation
@Injectable()
export class UserService implements IUserService {
  async findAll(): Promise<User[]> {
    return this.userRepository.findAll();
  }
  // ...
}

// module.ts
@Module({
  providers: [
    {
      provide: 'IUserService',
      useClass: UserService,
    },
  ],
})
export class UserModule {}

// Usage with interface token
@Injectable()
export class UserController {
  constructor(
    @Inject('IUserService')
    private readonly userService: IUserService,
  ) {}
}
```

### Provider Override in Tests

```typescript
// user.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from './user.service';
import { UserRepository } from './user.repository';

describe('UserService', () => {
  let service: UserService;
  let mockUserRepository: Partial<UserRepository>;

  beforeEach(async () => {
    mockUserRepository = {
      findAll: jest.fn().mockResolvedValue([]),
      findById: jest.fn().mockResolvedValue(null),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: UserRepository,
          useValue: mockUserRepository,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  it('should return empty array', async () => {
    const result = await service.findAll();
    expect(result).toEqual([]);
    expect(mockUserRepository.findAll).toHaveBeenCalled();
  });
});
```

### Dynamic Provider Resolution

```typescript
// Using ModuleRef for dynamic resolution
import { ModuleRef } from '@nestjs/core';

@Injectable()
export class NotificationService {
  constructor(private readonly moduleRef: ModuleRef) {}

  async sendNotification(type: string, data: any) {
    // Dynamically resolve provider based on type
    const handler = this.moduleRef.get<NotificationHandler>(
      `${type}NotificationHandler`,
    );
    return handler.send(data);
  }
}
```

### Forward Reference for Circular Dependencies

```typescript
// module-a.module.ts
@Module({
  imports: [forwardRef(() => ModuleB)],
})
export class ModuleA {}

// module-b.module.ts
@Module({
  imports: [forwardRef(() => ModuleA)],
})
export class ModuleB {}

// service-a.service.ts
@Injectable()
export class ServiceA {
  constructor(
    @Inject(forwardRef(() => ServiceB))
    private serviceB: ServiceB,
  ) {}
}

// service-b.service.ts
@Injectable()
export class ServiceB {
  constructor(
    @Inject(forwardRef(() => ServiceA))
    private serviceA: ServiceA,
  ) {}
}
```

### Custom Provider Patterns

```typescript
// Factory with dependencies
@Module({
  providers: [
    {
      provide: 'HTTP_CLIENT',
      useFactory: (config: ConfigService, logger: LoggerService) => {
        const client = axios.create({
          baseURL: config.get('API_URL'),
          timeout: 5000,
        });

        client.interceptors.request.use((config) => {
          logger.log(`Request: ${config.method} ${config.url}`);
          return config;
        });

        return client;
      },
      inject: [ConfigService, LoggerService],
    },
  ],
})
export class HttpModule {}
```

### Scoped Providers

```typescript
// Request-scoped provider
@Injectable({ scope: Scope.REQUEST })
export class RequestContext {
  constructor(private readonly request: Request) {}

  get userId(): string {
    return this.request.user?.id;
  }

  get tenantId(): string {
    return this.request.headers['x-tenant-id'];
  }
}

// Transient-scoped provider
@Injectable({ scope: Scope.TRANSIENT })
export class Counter {
  private count = 0;

  increment(): number {
    return ++this.count;
  }

  getCount(): number {
    return this.count;
  }
}

// Usage: each consumer gets its own Counter
@Injectable()
export class ServiceA {
  constructor(private readonly counter: Counter) {} // Own counter
}

@Injectable()
export class ServiceB {
  constructor(private readonly counter: Counter) {} // Different counter
}
```

## Real-World Use Cases

### 1. Multi-Strategy Payment System

```typescript
export const PAYMENT_STRATEGY = 'PAYMENT_STRATEGY';

@Module({
  providers: [
    {
      provide: PAYMENT_STRATEGY,
      useFactory: (config: ConfigService) => {
        const strategies: Record<string, PaymentStrategy> = {
          stripe: new StripePaymentStrategy(config.get('STRIPE_KEY')),
          paypal: new PayPalPaymentStrategy(config.get('PAYPAL_KEY')),
          crypto: new CryptoPaymentStrategy(config.get('CRYPTO_WALLET')),
        };
        return strategies[config.get('PAYMENT_PROVIDER')];
      },
      inject: [ConfigService],
    },
  ],
})
export class PaymentModule {}
```

### 2. Database Connection Pool

```typescript
@Module({})
export class DatabaseModule {
  static forRoot(options: DatabaseOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        {
          provide: 'DATABASE_CONNECTION',
          useFactory: async (config: ConfigService) => {
            const pool = await createPool({
              host: options.host || config.get('DB_HOST'),
              port: options.port || config.get('DB_PORT'),
              database: options.database || config.get('DB_NAME'),
              connectionLimit: 10,
            });
            return pool;
          },
          inject: [ConfigService],
        },
      ],
      exports: ['DATABASE_CONNECTION'],
    };
  }
}
```

### 3. Event-Driven Architecture

```typescript
// Event emitter as injection token
export const EVENT_EMITTER = 'EVENT_EMITTER';

@Module({
  providers: [
    {
      provide: EVENT_EMITTER,
      useFactory: () => {
        return new EventEmitter2({
          wildcard: true,
          delimiter: '.',
          maxListeners: 100,
        });
      },
    },
  ],
})
export class EventModule {}

// Usage
@Injectable()
export class UserService {
  constructor(
    @Inject(EVENT_EMITTER)
    private readonly emitter: EventEmitter2,
  ) {}

  async create(dto: CreateUserDto) {
    const user = await this.userRepo.create(dto);
    this.emitter.emit('user.created', user);
    return user;
  }
}
```

## Common Mistakes

### 1. Not Using Constructor Injection

```typescript
// ❌ BAD: Creating dependencies manually
@Injectable()
export class UserService {
  private repo = new UserRepository(); // No DI!
}

// ✅ GOOD: Use constructor injection
@Injectable()
export class UserService {
  constructor(private readonly repo: UserRepository) {}
}
```

### 2. Circular Dependencies Without Resolution

```typescript
// ❌ BAD: Unresolved circular dependency
@Injectable()
export class ServiceA {
  constructor(private serviceB: ServiceB) {} // Error at runtime
}

// ✅ GOOD: Use forwardRef
@Injectable()
export class ServiceA {
  constructor(
    @Inject(forwardRef(() => ServiceB))
    private serviceB: ServiceB,
  ) {}
}
```

### 3. Injecting Request-Scoped Providers into Singletons

```typescript
// ❌ BAD: Singleton depends on request-scoped
@Injectable() // Singleton
export class UserService {
  constructor(
    private context: RequestContext, // REQUEST scope - ERROR!
  ) {}
}

// ✅ GOOD: Use module-scoped provider or pass context explicitly
@Injectable()
export class UserService {
  findAll(request: Request) { // Pass context explicitly
    const userId = request.user.id;
    // ...
  }
}
```

### 4. Overusing @Inject()

```typescript
// ❌ BAD: Using @Inject when type is available
@Injectable()
export class UserService {
  constructor(
    @Inject(UserRepository) // Unnecessary
    private repo: UserRepository,
  ) {}
}

// ✅ GOOD: Only use @Inject when needed (tokens, interfaces)
@Injectable()
export class UserService {
  constructor(
    private repo: UserRepository, // Type injection
    @Inject(PAYMENT_SERVICE) // Token injection
    private payment: PaymentService,
  ) {}
}
```

### 5. Not Handling Provider Errors

```typescript
// ❌ BAD: No error handling in factory
{
  provide: 'CONFIG',
  useFactory: () => {
    return JSON.parse(fs.readFileSync('config.json', 'utf8'));
    // What if file doesn't exist?
  },
}

// ✅ GOOD: Handle errors in factory
{
  provide: 'CONFIG',
  useFactory: () => {
    try {
      return JSON.parse(fs.readFileSync('config.json', 'utf8'));
    } catch (error) {
      throw new Error(`Failed to load config: ${error.message}`);
    }
  },
}
```

## Best Practices

1. **Constructor Injection**: Always use constructor injection for dependencies.
2. **Interface Tokens**: Use interfaces/tokens for flexible provider binding.
3. **Minimal Dependencies**: Keep provider dependencies minimal.
4. **Forward Reference**: Use `forwardRef()` to resolve circular dependencies.
5. **Provider Scope**: Choose appropriate scope for each provider.
6. **Factory Providers**: Use factories for complex initialization.
7. **Error Handling**: Handle errors in factory providers.
8. **Testing**: Override providers in tests for isolation.
9. **Documentation**: Document complex provider configurations.
10. **Lifecycle Hooks**: Implement cleanup in `OnModuleDestroy`.

## Performance Considerations

1. **Singleton Caching**: Singletons are cached — instantiate only once.
2. **Transient Overhead**: Transient providers create new instances per injection.
3. **Request Scope**: Request-scoped providers add overhead per request.
4. **Lazy Resolution**: Providers can be resolved lazily on first use.
5. **Circular Resolution**: Circular dependencies add resolution overhead.
6. **Factory Execution**: Factory providers run at module initialization.

## Interview Questions

### Beginner

**Q1: What is dependency injection in NestJS?**
DI is a pattern where NestJS's IoC container manages and injects dependencies into components through constructor parameters.

**Q2: What is the IoC container?**
The IoC container is NestJS's dependency injection container that manages provider instantiation, dependency resolution, and lifecycle.

**Q3: What is constructor injection?**
Declaring dependencies as constructor parameters. NestJS resolves and injects them when creating the class instance.

**Q4: What is a singleton provider?**
A provider with default scope — one instance per module that provides it.

**Q5: How do you inject a provider into a controller?**
Declare the provider type as a constructor parameter.

### Intermediate

**Q6: What are injection tokens?**
Tokens (strings, Symbols, or classes) used to identify providers when the type alone isn't sufficient (interfaces, multiple implementations).

**Q7: How do you resolve circular dependencies?**
Use `forwardRef()` to defer resolution, or restructure code to remove the circular dependency.

**Q8: What is the difference between `useClass` and `useFactory`?**
- `useClass`: Instantiates a class as the provider
- `useFactory`: Uses a function to create the provider (more flexible)

**Q9: How do you override a provider in tests?**
Use `Test.createTestingModule()` with `overrideProvider()` to replace providers with mocks.

**Q10: What is request-scoped dependency injection?**
Creates a new instance of the provider for each HTTP request, allowing request-specific data to be stored.

### Senior

**Q11: Explain how NestJS resolves the dependency graph.**
NestJS performs topological sort on the dependency graph, instantiating leaf dependencies first, then working up to the root. It handles circular dependencies with forwardRef.

**Q12: How do you implement a provider with async initialization?**
Use `useFactory` with an async function, or implement `OnModuleInit` lifecycle hook.

**Q13: How would you design a DI system from scratch?**
Implement a container with registration, resolution, scoping, and lifecycle management. Use graph algorithms for dependency resolution.

**Q14: What are the performance implications of DI?**
- Startup time: Graph resolution and instantiation
- Memory: Singleton caching vs transient overhead
- Request latency: Request-scoped provider creation

**Q15: How do you handle DI in distributed systems?**
Use service meshes (Istio), shared libraries, or microservice-specific DI patterns.

### FAANG-Style

**Q16: Design a DI container from scratch.**
Implement container with `register()`, `resolve()`, `inject()`, lifecycle hooks, and graph resolution.

```typescript
class Container {
  private providers = new Map<Token, Provider>();
  private instances = new Map<Token, any>();

  register<T>(token: Token, provider: Provider<T>) { ... }
  resolve<T>(token: Token): T { ... }
  inject<T>(token: Token): T { ... }
}
```

**Q17: How would you implement request context propagation?**
Use async hooks or continuation-local storage to propagate request context through the DI container.

**Q18: Design a multi-tenant DI system.**
Use dynamic modules with tenant-specific providers. Create isolated DI containers per tenant.

**Q19: How would you implement DI for microservices?**
Use shared libraries with local DI, or centralized service discovery with remote provider resolution.

**Q20: How would you optimize DI performance?**
- Lazy instantiation
- Provider pooling
- Dependency caching
- Graph optimization

### Follow-ups

**Q21: What is the order of dependency resolution?**
Topological order — dependencies are resolved before dependents. Leaf nodes first.

**Q22: How do you handle optional dependencies?**
Use `@Optional()` decorator to make dependencies optional.

**Q23: What happens if a dependency fails to resolve?**
The application throws an error and fails to start.

**Q24: How do you implement provider scopes at runtime?**
Use `ModuleRef` to resolve providers with different scopes dynamically.

**Q25: How do you debug DI issues?**
Enable debug logging with `nest start --debug`, use `ModuleRef` to inspect providers.

## Summary

Dependency Injection is NestJS's core mechanism for managing component dependencies. The IoC container handles instantiation, resolution, and lifecycle management automatically. Understanding DI patterns — constructor injection, injection tokens, provider scopes, and circular dependency resolution — is essential for building scalable, testable NestJS applications.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| Constructor Injection | Declare dependencies as constructor params |
| IoC Container | Manages provider instantiation and resolution |
| Injection Token | String/Symbol/class to identify providers |
| `@Inject(token)` | Inject using custom token |
| `forwardRef()` | Resolve circular dependencies |
| Singleton Scope | Default: one instance per module |
| Transient Scope | New instance per consumer |
| Request Scope | New instance per request |
| `useClass` | Provide a class |
| `useFactory` | Provide using factory function |
| `useValue` | Provide a static value |
| `useExisting` | Alias to existing provider |
| `ModuleRef` | Runtime DI container access |
| `overrideProvider()` | Replace providers in tests |

## References & Learn More

- [NestJS Dependency Injection Official Docs](https://docs.nestjs.com/fundamentals/custom-providers)
- [NestJS IoC Container](https://docs.nestjs.com/fundamentals/dependency-injection)
- [NestJS Provider Scopes](https://docs.nestjs.com/fundamentals/injection-scopes)
- [NestJS Circular Dependencies](https://docs.nestjs.com/fundamentals/circular-dependency)
