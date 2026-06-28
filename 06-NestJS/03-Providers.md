# Providers

## Definition

**Providers** in NestJS are fundamental building blocks that handle business logic, data access, and utility functions. They are classes decorated with `@Injectable()` that can be injected as dependencies into other providers, controllers, or other components. Providers are the "brains" of the application — they process data, interact with databases, call external APIs, and implement business rules.

NestJS manages providers through its powerful **Dependency Injection (DI)** system, which handles instantiation, lifetime management, and dependency resolution automatically.

## Why Do We Need It?

1. **Separation of Concerns**: Providers encapsulate business logic separate from HTTP handling.

2. **Reusability**: Services can be reused across multiple controllers and modules.

3. **Testability**: Providers can be easily mocked and tested in isolation.

4. **Dependency Injection**: Automatic dependency management through the DI container.

5. **Lifecycle Management**: NestJS manages provider instantiation, scoping, and cleanup.

6. **Modular Architecture**: Providers are organized within modules with clear boundaries.

## How It Works

Providers are registered in a module's `providers` array. NestJS's DI container instantiates them (typically as singletons) and resolves their dependencies through constructor injection.

### Provider Lifecycle

```text
┌─────────────────────────────────────────────────────────┐
│                    Module Loading                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Collect providers from @Module() decorator          │
│                         │                               │
│                         ▼                               │
│  2. Resolve dependency graph                            │
│                         │                               │
│                         ▼                               │
│  3. Instantiate providers (lazy or eager)               │
│                         │                               │
│                         ▼                               │
│  4. Inject dependencies through constructors            │
│                         │                               │
│                         ▼                               │
│  5. Provider ready for use                              │
│                                                         │
└─────────────────────────────────────────────────────────┘

```

### Provider Types

```text
┌─────────────────────────────────────────────────────┐
│                  Provider Types                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │  Injectable  │  │   Factory   │  │   Value     ││
│  │  (Class)    │  │   Provider  │  │   Provider  ││
│  │             │  │             │  │             ││
│  │ @Injectable │  │ useFactory  │  │ useValue    ││
│  │ class Svc   │  │ () => new S │  │ const val   ││
│  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                     │
│  ┌─────────────┐  ┌─────────────┐                  │
│  │   Existing  │  │  Alias      │                  │
│  │   Provider  │  │  Provider   │                  │
│  │             │  │             │                  │
│  │ useExisting │  │ useAlias    │                  │
│  │ token       │  │ token       │                  │
│  └─────────────┘  └─────────────┘                  │
└─────────────────────────────────────────────────────┘

```

## Code Examples

### Injectable Service

```typescript
// user.service.ts
import { Injectable, NotFoundException, Logger } from '@nestjs/common';
import { UserRepository } from './user.repository';
import { CreateUserDto } from './dto/create-user.dto';
import { User } from './entities/user.entity';

@Injectable()
export class UserService {
  private readonly logger = new Logger(UserService.name);

  constructor(
    private readonly userRepository: UserRepository,
    private readonly cacheService: CacheService,
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async findAll(): Promise<User[]> {
    const cacheKey = 'users:all';
    const cached = await this.cacheService.get<User[]>(cacheKey);
    if (cached) return cached;

    const users = await this.userRepository.findAll();
    await this.cacheService.set(cacheKey, users, 300);
    return users;
  }

  async findOne(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }

  async create(dto: CreateUserDto): Promise<User> {
    const user = await this.userRepository.create(dto);
    this.eventEmitter.emit('user.created', user);
    this.logger.log(`User created: ${user.id}`);
    return user;
  }

  async update(id: string, dto: UpdateUserDto): Promise<User> {
    await this.findOne(id); // Ensure exists
    const user = await this.userRepository.update(id, dto);
    await this.cacheService.del('users:all');
    this.eventEmitter.emit('user.updated', user);
    return user;
  }

  async remove(id: string): Promise<void> {
    await this.findOne(id);
    await this.userRepository.delete(id);
    await this.cacheService.del('users:all');
    this.eventEmitter.emit('user.deleted', { id });
  }
}

```

### Repository Provider

```typescript
// user.repository.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';

@Injectable()
export class UserRepository {
  constructor(
    @InjectRepository(User)
    private readonly repository: Repository<User>,
  ) {}

  async findAll(): Promise<User[]> {
    return this.repository.find({
      relations: ['profile', 'roles'],
    });
  }

  async findById(id: string): Promise<User | null> {
    return this.repository.findOne({
      where: { id },
      relations: ['profile', 'roles'],
    });
  }

  async create(data: Partial<User>): Promise<User> {
    const user = this.repository.create(data);
    return this.repository.save(user);
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    await this.repository.update(id, data);
    return this.findById(id);
  }

  async delete(id: string): Promise<void> {
    await this.repository.delete(id);
  }
}

```

### Factory Provider

```typescript
// logger.factory.ts
import { LoggerService, Logger } from '@nestjs/common';

export function createLoggerService(context: string): LoggerService {
  return new Logger(context);
}

// module registration
@Module({
  providers: [
    {
      provide: 'APP_LOGGER',
      useFactory: () => createLoggerService('App'),
    },
    {
      provide: 'DB_LOGGER',
      useFactory: (config: ConfigService) => {
        const level = config.get('LOG_LEVEL');
        return new DatabaseLogger(level);
      },
      inject: [ConfigService],
    },
  ],
})
export class AppModule {}

```

### Value Provider

```typescript
// constants.ts
export const APP_CONFIG = 'APP_CONFIG';
export const DATABASE_OPTIONS = 'DATABASE_OPTIONS';
export const SMTP_CONFIG = 'SMTP_CONFIG';

// module.ts
@Module({
  providers: [
    {
      provide: APP_CONFIG,
      useValue: {
        name: 'MyApp',
        version: '1.0.0',
        environment: process.env.NODE_ENV,
      },
    },
    {
      provide: DATABASE_OPTIONS,
      useValue: {
        type: 'postgres',
        host: 'localhost',
        port: 5432,
        database: 'mydb',
      },
    },
  ],
})
export class AppModule {}

```

### Existing Provider (Alias)

```typescript
@Module({
  providers: [
    UserService,
    {
      provide: 'UserRepoAlias',
      useExisting: UserService, // Alias to existing provider
    },
  ],
})
export class UserModule {}

```

### Provider Scope

```typescript
import { Injectable, Scope } from '@nestjs/common';

// Default scope: Singleton (one instance per module)
@Injectable()
export class SingletonService {}

// Transient scope: New instance per consumer
@Injectable({ scope: Scope.TRANSIENT })
export class TransientService {}

// Request scope: New instance per HTTP request
@Injectable({ scope: Scope.REQUEST })
export class RequestContextService {
  constructor(private readonly request: Request) {}
}

```

### Custom Provider Tokens

```typescript
// Using injection tokens
export const PAYMENT_SERVICE = 'PAYMENT_SERVICE';

@Module({
  providers: [
    {
      provide: PAYMENT_SERVICE,
      useClass: process.env.NODE_ENV === 'production'
        ? StripePaymentService
        : MockPaymentService,
    },
  ],
})
export class PaymentModule {}

// Usage in another service
@Injectable()
export class OrderService {
  constructor(
    @Inject(PAYMENT_SERVICE)
    private readonly paymentService: PaymentServiceInterface,
  ) {}
}

```

### Async Provider

```typescript
@Module({
  providers: [
    {
      provide: 'ASYNC_CONFIG',
      useFactory: async (configService: ConfigService) => {
        // Async initialization
        const config = await configService.loadConfig();
        return config;
      },
      inject: [ConfigService],
    },
  ],
})
export class AppModule {}

```

### Entity Provider

```typescript
// Using TypeORM entities as providers
@Module({
  imports: [
    TypeOrmModule.forFeature([
      User,
      Order,
      Product,
    ]),
  ],
})
export class FeatureModule {}

// Or custom entity provider
@Module({
  providers: [
    {
      provide: 'USER_ENTITY',
      useValue: User,
    },
  ],
})
export class EntityModule {}

```

## Real-World Use Cases

### 1. Service Layer Pattern

```typescript
// Product service with multiple dependencies
@Injectable()
export class ProductService {
  constructor(
    private readonly productRepository: ProductRepository,
    private readonly inventoryService: InventoryService,
    private readonly pricingService: PricingService,
    private readonly cacheService: CacheService,
    private readonly eventEmitter: EventEmitter2,
    private readonly logger: Logger,
  ) {}

  async getProducts(filters: ProductFilter): Promise<PaginatedResult<Product>> {
    const cacheKey = `products:${JSON.stringify(filters)}`;
    const cached = await this.cacheService.get<PaginatedResult<Product>>(cacheKey);
    if (cached) return cached;

    const products = await this.productRepository.findByFilters(filters);
    const enriched = await this.enrichProducts(products);
    await this.cacheService.set(cacheKey, enriched, 600);
    return enriched;
  }

  private async enrichProducts(products: Product[]): Promise<Product[]> {
    return Promise.all(
      products.map(async (product) => {
        const stock = await this.inventoryService.getStock(product.id);
        const price = await this.pricingService.calculatePrice(product);
        return { ...product, stock, price };
      }),
    );
  }
}

```

### 2. Strategy Pattern with Providers

```typescript
export const STORAGE_STRATEGY = 'STORAGE_STRATEGY';

@Module({
  providers: [
    {
      provide: STORAGE_STRATEGY,
      useFactory: (config: ConfigService) => {
        const provider = config.get('STORAGE_PROVIDER');
        switch (provider) {
          case 's3':
            return new S3StorageService();
          case 'gcs':
            return new GCSStorageService();
          case 'local':
            return new LocalStorageService();
          default:
            throw new Error(`Unknown storage provider: ${provider}`);
        }
      },
      inject: [ConfigService],
    },
  ],
})
export class StorageModule {}

```

### 3. Interceptor-Style Provider

```typescript
@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map(data => ({
        success: true,
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}

```

### 4. Custom Decorator with Provider

```typescript
export const CURRENT_USER_KEY = 'CURRENT_USER';

export const CurrentUser = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  },
);

// Usage
@Get('profile')
getProfile(@CurrentUser('id') userId: string) {
  return this.userService.getProfile(userId);
}

```

## Common Mistakes

### 1. Not Using @Injectable()

```typescript
// ❌ BAD: Missing @Injectable() decorator
export class UserService {
  constructor(private readonly repo: UserRepository) {}
}

// ✅ GOOD: Always use @Injectable()
@Injectable()
export class UserService {
  constructor(private readonly repo: UserRepository) {}
}

```

### 2. Circular Dependency

```typescript
// ❌ BAD: Circular dependency
@Injectable()
export class UserService {
  constructor(private readonly orderService: OrderService) {}
}

@Injectable()
export class OrderService {
  constructor(private readonly userService: UserService) {}
}

// ✅ GOOD: Use forwardRef or restructure
@Injectable()
export class UserService {
  constructor(
    @Inject(forwardRef(() => OrderService))
    private readonly orderService: OrderService,
  ) {}
}

```

### 3. Not Handling Provider Scope

```typescript
// ❌ BAD: Request-scoped provider used as singleton
@Injectable({ scope: Scope.REQUEST })
export class UserService {
  constructor(private readonly request: Request) {} // Won't work as singleton
}

// ✅ GOOD: Match scope to usage
@Injectable() // Default singleton scope
export class UserService {
  constructor(private readonly userRepo: UserRepository) {}
}

@Injectable({ scope: Scope.REQUEST })
export class RequestContextService {
  constructor(private readonly request: Request) {} // Correct usage
}

```

### 4. Creating Instances Manually

```typescript
// ❌ BAD: Creating instances instead of using DI
@Injectable()
export class UserService {
  private readonly mailService = new MailService(); // Manual creation
}

// ✅ GOOD: Inject dependencies through constructor
@Injectable()
export class UserService {
  constructor(private readonly mailService: MailService) {}
}

```

### 5. Over-Injecting Dependencies

```typescript
// ❌ BAD: Too many dependencies (sign of SRP violation)
@Injectable()
export class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly orderRepo: OrderRepository,
    private readonly productRepo: ProductRepository,
    private readonly paymentService: PaymentService,
    private readonly emailService: EmailService,
    private readonly cacheService: CacheService,
    private readonly queueService: QueueService,
    private readonly analyticsService: AnalyticsService,
  ) {}
}

// ✅ GOOD: Split into focused services
@Injectable()
export class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly cacheService: CacheService,
  ) {}
}

```

## Best Practices

1. **Single Responsibility**: Each provider should have one clear purpose.

2. **Constructor Injection**: Always use constructor injection for dependencies.

3. **Interface Segregation**: Use interfaces for provider contracts.

4. **Provider Scope**: Choose appropriate scope (default, transient, request).

5. **Factory Providers**: Use factories for complex initialization logic.

6. **Custom Tokens**: Use injection tokens for flexible provider binding.

7. **Error Handling**: Handle errors within providers, not in controllers.

8. **Logging**: Include logging in providers for debugging.

9. **Async Providers**: Use async factories for async initialization.
10. **Testing**: Mock providers in tests using `Test.createTestingModule()`.

## Performance Considerations

1. **Singleton Scope**: Default scope is singleton — one instance per module.

2. **Transient Scope**: Creates new instances — use sparingly for performance.

3. **Request Scope**: New instance per request — adds overhead for each request.

4. **Lazy Loading**: Providers can be lazy-loaded to reduce startup time.

5. **Provider Caching**: Cache frequently accessed provider data.

6. **Connection Pooling**: Reuse database connections through singleton repositories.

## Interview Questions

### Beginner

**Q1: What is a provider in NestJS?**
A provider is a class decorated with `@Injectable()` that handles business logic, data access, or utility functions. Providers are managed by NestJS's DI container.

**Q2: What is the difference between a provider and a controller?**
Providers handle business logic and data access. Controllers handle HTTP requests and responses. Controllers typically delegate to providers.

**Q3: How do you make a provider available to other modules?**
Export the provider in the module's `exports` array, then import that module in the consuming module.

**Q4: What is the default scope of a provider?**
Singleton — one instance per module that provides it.

**Q5: How do you inject a provider into a controller?**
Declare it as a constructor parameter with the appropriate type.

### Intermediate

**Q6: What is the difference between `useClass`, `useFactory`, `useValue`, and `useExisting`?**

- `useClass`: Instantiate a class as the provider
- `useFactory`: Use a factory function to create the provider
- `useValue`: Use a static value as the provider
- `useExisting`: Alias to an existing provider

**Q7: What is transient scope and when would you use it?**
Transient scope creates a new instance for each consumer that injects it. Use when each consumer needs its own isolated instance (e.g., counters, accumulators).

**Q8: How do you use custom injection tokens?**
Define a token (string or Symbol), register the provider with that token, and use `@Inject(token)` to inject it.

**Q9: What is `ModuleRef` and how do you use it?**
`ModuleRef` provides access to the DI container at runtime. Use it to dynamically resolve providers outside the normal DI flow.

**Q10: How do you handle async provider initialization?**
Use `useFactory` with an async function and specify `inject` for dependencies.

### Senior

**Q11: How would you implement a plugin architecture using providers?**
Use dynamic modules with factory providers. Each plugin provides a token and implementation class. Register plugins dynamically.

**Q12: How do you test providers with complex dependencies?**
Use `Test.createTestingModule()` with `overrideProvider()` to mock dependencies. Isolate the provider under test.

**Q13: Explain provider lifetime management in NestJS.**
Providers are instantiated when their module loads (default) or lazily on first injection. Singleton providers persist for the app lifetime. Request-scoped providers are created per request and destroyed after.

**Q14: How do you implement provider-level caching?**
Inject a cache service and cache results at the provider level. Use cache keys based on method parameters.

**Q15: How would you handle provider cleanup on application shutdown?**
Implement `OnModuleDestroy` or `OnApplicationShutdown` lifecycle hooks.

### FAANG-Style

**Q16: Design a provider system for a multi-tenant application.**
Use dynamic module pattern with `forRoot()` for each tenant. Create tenant-specific providers using factory pattern with tenant context.

**Q17: How would you implement a circuit breaker pattern in a provider?**
Create a wrapper provider that tracks failures and opens the circuit after threshold. Use observables for async fallback.

**Q18: Design a provider for distributed tracing.**
Inject trace context from requests, propagate through all providers, export to Jaeger/Zipkin. Use async hooks for context propagation.

**Q19: How would you implement provider versioning?**
Use injection tokens with version strings. Register versioned providers and inject specific versions based on API version.

**Q20: Design a provider system for feature flags.**
Create a FeatureFlagService that loads flags from a config service. Inject it into providers that need feature-gated behavior.

### Follow-ups

**Q21: How do you handle provider dependency resolution order?**
NestJS resolves dependencies topologically. Use `forwardRef()` for circular dependencies.

**Q22: What happens if a provider throws during initialization?**
The application fails to start. Handle errors in factory providers or use async initialization with error handling.

**Q23: How do you scope providers to specific routes?**
Use request-scoped providers with request context, or create route-specific providers with custom decorators.

**Q24: How do you share providers between modules without making them global?**
Export the provider from one module and import that module in the consuming module.

**Q25: How do you handle provider configuration from environment variables?**
Use ConfigService injected into providers, or use factory providers that read from process.env.

## Summary

Providers are NestJS's core building blocks that implement business logic, data access, and utility functions. They leverage dependency injection for automatic instantiation and dependency resolution. Understanding provider types (class, factory, value, existing), scopes (singleton, transient, request), and patterns is essential for building well-architected NestJS applications.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `@Injectable()` | Marks a class as a provider |
| `providers` array | Register providers in a module |
| Singleton scope | Default: one instance per module |
| `Scope.TRANSIENT` | New instance per consumer |
| `Scope.REQUEST` | New instance per request |
| `useClass` | Provide a class |
| `useFactory` | Provide using a factory function |
| `useValue` | Provide a static value |
| `useExisting` | Alias to existing provider |
| `@Inject(token)` | Inject using custom token |
| `ModuleRef` | Runtime DI container access |
| `forwardRef()` | Resolve circular dependencies |

## References & Learn More

- [NestJS Providers Official Docs](https://docs.nestjs.com/providers)
- [NestJS Dependency Injection](https://docs.nestjs.com/fundamentals/custom-providers)
- [NestJS Lifecycle Events](https://docs.nestjs.com/fundamentals/lifecycle-events)
- [NestJS Testing](https://docs.nestjs.com/fundamentals/testing)
