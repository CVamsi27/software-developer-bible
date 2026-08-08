---
section: NestJS
category: Backend
tags: [concept]
---

# NestJS Dependency Injection

> **TL;DR:** DI in NestJS is a constructor-injection IoC container that resolves a graph of providers at boot. Master scopes (DEFAULT / REQUEST / TRANSIENT), custom tokens, and `forwardRef` to handle real-world circular dependency cases.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

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

```text
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

```text
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

---

## See Also
- [Design Patterns](../10-Design-Patterns/)
- [Microservices](../12-Microservices/)
- [Node.js](../05-NodeJS/)
- [REST APIs](../07-REST-API/)

## References & Learn More

- [NestJS Dependency Injection Official Docs](https://docs.nestjs.com/fundamentals/custom-providers)
- [NestJS IoC Container](https://docs.nestjs.com/fundamentals/dependency-injection)
- [NestJS Provider Scopes](https://docs.nestjs.com/fundamentals/injection-scopes)
- [NestJS Circular Dependencies](https://docs.nestjs.com/fundamentals/circular-dependency)
