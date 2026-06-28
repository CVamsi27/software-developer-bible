# NestJS Modules

## Definition

A **Module** in NestJS is a class decorated with `@Module()` that organizes closely related set of capabilities. Modules are the fundamental building blocks of a NestJS application's architecture, providing a way to encapsulate providers (services, repositories, etc.) and manage their scope, dependencies, and exposure to other parts of the application.

Every NestJS application has at least one module — the **root module** (`AppModule`) — which serves as the entry point for the framework's dependency injection system and determines which components are available for injection across the entire application.

## Why Do We Need It?

1. **Encapsulation**: Modules group related functionality together, keeping code organized and maintainable.

2. **Dependency Management**: They define clear boundaries for dependency injection, controlling which providers are available in which contexts.

3. **Reusability**: Feature modules can be easily imported into other modules, promoting code reuse.

4. **Scalability**: As applications grow, modules provide a clear structure for adding new features without impacting existing code.

5. **Testing**: Well-defined module boundaries make unit and integration testing straightforward.

6. **Lazy Loading**: Modules can be loaded on demand, improving application startup time.

7. **Clear Architecture**: Enforces a modular architecture that aligns with SOLID principles.

## How It Works

NestJS modules work through a decorator-based system. The `@Module()` decorator accepts a metadata object that defines:

- `providers`: Array of providers (services, repositories, etc.) to be instantiated and available within this module
- `controllers`: Array of controllers that handle incoming requests
- `imports`: Array of modules whose exported providers are needed in this module
- `exports`: Array of providers that should be made available to other modules that import this module

### Module Resolution Flow

```text
┌─────────────────────────────────────────────────┐
│                  Root Module                     │
│              (AppModule)                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────┐│
│  │  UserModule  │  │ OrderModule  │  │AuthModule││
│  │             │  │             │  │         ││
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │┌───────┐││
│  │ │UsersCtrl│ │  │ │OrderCtrl│ │  ││AuthCtrl│││
│  │ └────┬────┘ │  │ └────┬────┘ │  │└───┬───┘││
│  │      │      │  │      │      │  │    │    ││
│  │ ┌────▼────┐ │  │ ┌────▼────┐ │  │┌───▼───┐││
│  │ │UserSvc  │ │  │ │OrderSvc │ │  ││AuthSvc │││
│  │ └────┬────┘ │  │ └────┬────┘ │  │└───┬───┘││
│  │      │      │  │      │      │  │    │    ││
│  │ ┌────▼────┐ │  │ ┌────▼────┐ │  │┌───▼───┐││
│  │ │UserRepo │ │  │ │OrderRepo│ │  ││JWT     │││
│  │ └─────────┘ │  │ └─────────┘ │  │└───────┘││
│  └─────────────┘  └─────────────┘  └─────────┘│
│                                                 │
│  Imports: [UserModule, AuthModule]               │
│  Exports: [OrderModule]                         │
└─────────────────────────────────────────────────┘

```

### Module Dependency Graph

```text
                    ┌──────────────┐
                    │  AppModule   │
                    │  (Root)      │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
     ┌──────────┐   ┌──────────┐   ┌──────────┐
     │UserModule│   │OrderMod  │   │AuthModule│
     └────┬─────┘   └────┬─────┘   └────┬─────┘
          │              │              │
          ▼              ▼              ▼
   ┌────────────┐ ┌────────────┐ ┌────────────┐
   │ Database   │ │ Payment    │ │ JWT        │
   │ Module     │ │ Module     │ │ Module     │
   └────────────┘ └────────────┘ └────────────┘

```

## Code Examples

### Basic Module Structure

```typescript
// user.module.ts
import { Module } from '@nestjs/common';
import { UserController } from './user.controller';
import { UserService } from './user.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([User]),
  ],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService], // Export so other modules can use UserService
})
export class UserModule {}

```

### Root Module

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { UserModule } from './user/user.module';
import { OrderModule } from './order/order.module';
import { AuthModule } from './auth/auth.module';
import { DatabaseModule } from './database/database.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    DatabaseModule,
    AuthModule,
    UserModule,
    OrderModule,
  ],
})
export class AppModule {}

```

### Feature Module with Relationships

```typescript
// order.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { OrderController } from './order.controller';
import { OrderService } from './order.service';
import { Order } from './entities/order.entity';
import { OrderItem } from './entities/order-item.entity';
import { UserModule } from '../user/user.module';
import { PaymentModule } from '../payment/payment.module';

@Module({
  imports: [
    TypeOrmModule.forFeature([Order, OrderItem]),
    UserModule,       // Import to use exported UserService
    PaymentModule,    // Import to use exported PaymentService
  ],
  controllers: [OrderController],
  providers: [OrderService],
  exports: [OrderService],
})
export class OrderModule {}

```

### Dynamic Module

```typescript
// database.module.ts
import { Module, DynamicModule, Global } from '@nestjs/common';
import { TypeOrmModule, TypeOrmModuleOptions } from '@nestjs/typeorm';

@Global()
@Module({})
export class DatabaseModule {
  static forRoot(options: TypeOrmModuleOptions): DynamicModule {
    const module = TypeOrmModule.forRoot(options);
    return {
      module: DatabaseModule,
      imports: [module],
      exports: [module],
    };
  }

  static forFeature(entities: Function[]): DynamicModule {
    const module = TypeOrmModule.forFeature(entities);
    return {
      module: DatabaseModule,
      imports: [module],
      exports: [module],
    };
  }
}

// Usage in app.module.ts
@Module({
  imports: [
    DatabaseModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'user',
      password: 'pass',
      database: 'mydb',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: true,
    }),
  ],
})
export class AppModule {}

```

### Configurable Dynamic Module

```typescript
// mail.module.ts
import { Module, DynamicModule } from '@nestjs/common';
import { MailService } from './mail.service';
import { MAIL_OPTIONS, MailModuleOptions } from './mail.constants';

@Module({})
export class MailModule {
  static forRoot(options: MailModuleOptions): DynamicModule {
    return {
      module: MailModule,
      providers: [
        {
          provide: MAIL_OPTIONS,
          useValue: options,
        },
        MailService,
      ],
      exports: [MailService],
    };
  }

  static forRootAsync(options: {
    useFactory: (...args: any[]) => Promise<MailModuleOptions> | MailModuleOptions;
    inject?: any[];
  }): DynamicModule {
    return {
      module: MailModule,
      providers: [
        {
          provide: MAIL_OPTIONS,
          useFactory: options.useFactory,
          inject: options.inject || [],
        },
        MailService,
      ],
      exports: [MailService],
    };
  }
}

// Usage
@Module({
  imports: [
    MailModule.forRoot({
      transport: 'smtp',
      host: 'smtp.example.com',
      port: 587,
    }),
  ],
})
export class AppModule {}

```

### Shared Module Pattern

```typescript
// shared/shared.module.ts
import { Module, Global } from '@nestjs/common';
import { LoggerService } from './logger.service';
import { CacheService } from './cache.service';
import { NotificationService } from './notification.service';

const SHARED_PROVIDERS = [LoggerService, CacheService, NotificationService];

@Global()
@Module({
  providers: SHARED_PROVIDERS,
  exports: SHARED_PROVIDERS,
})
export class SharedModule {}

```

### Module with Re-export

```typescript
// core.module.ts
import { Module, Global } from '@nestjs/common';
import { ConfigModule } from './config.module';
import { DatabaseModule } from './database.module';
import { LoggerModule } from './logger.module';

@Global()
@Module({
  imports: [ConfigModule, DatabaseModule, LoggerModule],
  exports: [ConfigModule, DatabaseModule, LoggerModule],
})
export class CoreModule {}

```

### Lazy Module

```typescript
// heavy-computation.module.ts
import { Module } from '@nestjs/common';
import { HeavyComputationService } from './heavy-computation.service';

@Module({
  providers: [HeavyComputationService],
  exports: [HeavyComputationService],
})
export class HeavyComputationModule {}

// In another module, use LazyModule
import { Module } from '@nestjs/common';
import { LazyModule } from '@nestjs/core';

@Module({
  imports: [
    LazyModule.register(() => import('./heavy-computation.module')),
  ],
})
export class AppModule {}

```

## Real-World Use Cases

### 1. E-Commerce Application Module Structure

```text
src/
├── app.module.ts
├── auth/
│   ├── auth.module.ts
│   ├── auth.controller.ts
│   ├── auth.service.ts
│   └── strategies/
├── users/
│   ├── users.module.ts
│   ├── users.controller.ts
│   ├── users.service.ts
│   └── entities/
├── products/
│   ├── products.module.ts
│   ├── products.controller.ts
│   ├── products.service.ts
│   └── entities/
├── orders/
│   ├── orders.module.ts
│   ├── orders.controller.ts
│   ├── orders.service.ts
│   └── entities/
├── payments/
│   ├── payments.module.ts
│   ├── payments.controller.ts
│   ├── payments.service.ts
│   └── strategies/
├── notifications/
│   ├── notifications.module.ts
│   ├── notifications.service.ts
│   └── channels/
└── shared/
    ├── shared.module.ts
    ├── logger/
    ├── interceptors/
    └── guards/

```

### 2. Microservice Module Boundaries

```typescript
// Each microservice has its own complete module
@Module({
  imports: [
    TypeOrmModule.forRoot(),
    ConfigModule.forRoot(),
  ],
  controllers: [OrderController],
  providers: [OrderService, OrderRepository],
})
export class OrderMicroserviceModule {}

```

### 3. Plugin Architecture

```typescript
// Plugin system using dynamic modules
@Module({})
export class PluginModule {
  static register(plugins: Plugin[]): DynamicModule {
    return {
      module: PluginModule,
      providers: plugins.map(plugin => ({
        provide: plugin.token,
        useClass: plugin.class,
      })),
      exports: plugins.map(plugin => plugin.token),
    };
  }
}

// Usage
@Module({
  imports: [
    PluginModule.register([
      { token: 'ANALYTICS_PLUGIN', class: AnalyticsPlugin },
      { token: 'SEO_PLUGIN', class: SeoPlugin },
    ]),
  ],
})
export class AppModule {}

```

## Common Mistakes

### 1. Circular Dependencies

```typescript
// ❌ BAD: Circular dependency
@Module({
  imports: [UserModule],
  providers: [OrderService],
})
export class OrderModule {}

@Module({
  imports: [OrderModule],
  providers: [UserService],
})
export class UserModule {}

// ✅ GOOD: Use forwardRef or restructure
@Module({
  imports: [forwardRef(() => OrderModule)],
  providers: [UserService],
})
export class UserModule {}

```

### 2. Missing Exports

```typescript
// ❌ BAD: Not exporting providers that other modules need
@Module({
  providers: [UserService],
})
export class UserModule {}

// Another module tries to inject UserService - FAILS
@Module({
  imports: [UserModule],
})
export class OrderModule {
  constructor(private userService: UserService) {} // Error!
}

// ✅ GOOD: Export the service
@Module({
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}

```

### 3. Over-Importing

```typescript
// ❌ BAD: Importing entire modules when only specific providers are needed
@Module({
  imports: [
    TypeOrmModule.forRoot([User, Order, Product, Category, ...]),
  ],
})
export class AppModule {}

// ✅ GOOD: Use forFeature in each module
@Module({
  imports: [TypeOrmModule.forFeature([User])],
})
export class UserModule {}

```

### 4. Not Using @Global Properly

```typescript
// ❌ BAD: Making everything global
@Global()
@Module({
  providers: [ServiceA, ServiceB, ServiceC, ServiceD],
  exports: [ServiceA, ServiceB, ServiceC, ServiceD],
})
export class SharedModule {}

// ✅ GOOD: Only global what truly needs to be global
@Global()
@Module({
  providers: [LoggerService, ConfigService],
  exports: [LoggerService, ConfigService],
})
export class SharedModule {}

```

### 5. Module Initialization Order Issues

```typescript
// ❌ BAD: Module depends on something not yet initialized
@Module({
  imports: [
    DatabaseModule.forRoot(config), // Config not loaded yet
  ],
})
export class AppModule {}

// ✅ GOOD: Use ConfigModule first
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    DatabaseModule.forRootAsync({
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        host: config.get('DB_HOST'),
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}

```

## Best Practices

1. **Single Responsibility**: Each module should have a single, well-defined purpose.

2. **Feature Modules**: Organize code by feature, not by type (controllers, services, etc.).

3. **Shared Module**: Create a dedicated `SharedModule` for cross-cutting concerns.

4. **Barrel Exports**: Use index.ts files to simplify imports.

5. **Lazy Loading**: Use `LazyModule` for heavy modules not needed at startup.

6. **Dynamic Modules**: Leverage dynamic modules for configurable functionality.

7. **Avoid Circular Dependencies**: Design module dependency trees as directed acyclic graphs (DAGs).

8. **Minimal Exports**: Only export what other modules actually need.

9. **Use Global Sparingly**: Reserve `@Global()` for truly universal providers.
10. **Module Testing**: Test modules in isolation with `Test.createTestingModule()`.

## Performance Considerations

1. **Module Initialization**: Modules are instantiated once during application bootstrap. Heavy initialization should be deferred.

2. **Provider Scope**: Default scope is singleton. Use `TRANSIENT` or `REQUEST` scope carefully as they create new instances per request.

3. **Tree-Shaking**: NestJS CLI tree-shakes unused imports during compilation.

4. **Lazy Loading**: Defer non-critical module imports to reduce startup time.

5. **Dynamic Module Config**: Use `forRootAsync` to load configuration asynchronously and avoid blocking.

6. **Module Caching**: NestJS caches module metadata. Restart the application if module structure changes in development.

## Interview Questions

### Beginner

**Q1: What is a NestJS module?**
A module is a class decorated with `@Module()` that groups related controllers, providers, and imports. It's the basic building block for organizing NestJS applications.

**Q2: What is the root module?**
The root module (`AppModule`) is the entry point of a NestJS application. It's the first module loaded and typically imports all other feature modules.

**Q3: What are the properties of the `@Module()` decorator?**

- `providers`: Services and repositories available within the module
- `controllers`: Request handlers
- `imports`: Other modules whose exports are needed
- `exports`: Providers available to modules that import this module

**Q4: Why do we need modules in NestJS?**
Modules provide encapsulation, dependency management, code reuse, and scalability. They enforce a modular architecture and control provider visibility.

**Q5: What happens if you don't export a provider?**
Other modules cannot inject that provider. It becomes private to the module where it's defined.

### Intermediate

**Q6: What is a dynamic module?**
A dynamic module is a module that can be configured at runtime. It's created by returning a `DynamicModule` object from a static method (e.g., `forRoot()`).

**Q7: How do you share a provider across all modules?**
Use the `@Global()` decorator on the module to make its exported providers available globally without explicit imports.

**Q8: What is the difference between `forRoot()` and `forFeature()`?**

- `forRoot()`: Initializes a module with global configuration (e.g., database connection)
- `forFeature()`: Registers specific entities/services within a feature module

**Q9: How do you handle circular dependencies?**

- Use `forwardRef()` to defer resolution
- Restructure code to remove the circular dependency
- Create a shared module or use event-based communication

**Q10: Can a module import itself?**
No, this would cause an infinite loop. NestJS detects and prevents self-imports.

### Senior

**Q11: Explain module initialization order in NestJS.**
NestJS loads modules in topological order based on imports. The root module loads first, then its direct imports, then their imports, and so on. The order is determined by dependency analysis, not the order in the imports array.

**Q12: How does NestJS handle module isolation?**
Each module has its own dependency injection scope. Providers in one module are not accessible in another unless explicitly exported and imported.

**Q13: What are the different provider scopes in NestJS?**

- `DEFAULT`: Singleton (one instance per module)
- `TRANSIENT`: New instance for each consumer that injects it
- `REQUEST`: New instance for each request

**Q14: How would you design a plugin system using NestJS modules?**
Use dynamic modules with `register()` or `forRootAsync()` methods. Each plugin provides a token and implementation class. The plugin module registers all plugins as providers with their tokens.

**Q15: What is the purpose of `ModuleRef`?**
`ModuleRef` provides access to the module's dependency injection container at runtime, allowing dynamic resolution of providers and accessing providers outside the normal DI flow.

### FAANG-Style

**Q16: Design a multi-tenant architecture using NestJS modules.**
Create a `TenantModule` that dynamically configures database connections based on tenant ID. Use middleware to extract tenant context, then use `ModuleRef` to resolve tenant-specific services.

```typescript
@Module({})
export class TenantModule {
  static forRoot(tenantId: string): DynamicModule {
    return {
      module: TenantModule,
      providers: [
        {
          provide: 'TENANT_CONFIG',
          useFactory: (configService: ConfigService) => ({
            database: configService.get(`TENANT_${tenantId}_DB`),
          }),
          inject: [ConfigService],
        },
      ],
    };
  }
}

```

**Q17: How would you implement module-level caching in a distributed system?**
Create a `CacheModule` using dynamic module pattern with Redis adapter. Use `@Global()` to make it available everywhere. Implement cache invalidation through event-driven patterns.

**Q18: Explain how you'd structure modules for a microservices architecture.**
Each microservice has its own NestJS application with isolated modules. Use `@nestjs/microservices` for transport (TCP, Redis, Kafka). Shared libraries are published as npm packages and imported as modules.

**Q19: How do you handle module testing in complex dependency graphs?**
Use `Test.createTestingModule()` with `overrideProvider()` to mock dependencies. Create isolated test modules that import only the modules under test. Use `close()` to clean up after tests.

**Q20: Describe a strategy for module lazy loading in large applications.**
Use `LazyModule` with dynamic imports. Implement route-based module loading where feature modules load only when their routes are accessed. Use webpack's dynamic imports for code splitting.

### Follow-ups

**Q21: What happens if two modules export the same provider token?**
The last imported module's provider wins. NestJS uses a "last wins" strategy for token resolution.

**Q22: How do you test a module with external dependencies?**
Use `Test.createTestingModule()` with `overrideProvider()` to replace external dependencies with mocks or stubs.

**Q23: Can you have multiple instances of the same module?**
No, NestJS ensures singleton module instances. However, dynamic modules can create different configurations of the same module class.

**Q24: How do you handle module configuration validation?**
Use Joi, Zod, or class-validator with custom validation pipes in dynamic module factories. Validate configuration before module initialization.

**Q25: What's the difference between `@Module` and `@Global`?**
`@Module` defines a module's structure. `@Global` makes the module's exported providers available globally, so importing modules don't need to explicitly import it.

## Summary

Modules are NestJS's fundamental organizational unit that encapsulate related functionality, manage dependencies, and provide clear boundaries between different parts of an application. They enable modular architecture, dependency injection, code reuse, and testability. Understanding modules — including dynamic modules, module scoping, and best practices — is essential for building scalable NestJS applications.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `@Module({})` | Decorator that defines a module |
| `providers` | Services/repositories instantiated by the module |
| `controllers` | Request handlers |
| `imports` | Modules whose exports are needed |
| `exports` | Providers available to importing modules |
| `@Global()` | Makes module exports available globally |
| `DynamicModule` | Configurable module returned from static methods |
| `forRoot()` | Static method for module initialization |
| `forFeature()` | Static method for entity/service registration |
| `forwardRef()` | Resolves circular dependencies |
| `ModuleRef` | Runtime access to DI container |
| `TRANSIENT` scope | New instance per consumer |
| `REQUEST` scope | New instance per request |
| `DEFAULT` scope | Singleton per module |

## References & Learn More

- [NestJS Modules Official Docs](https://docs.nestjs.com/modules)
- [NestJS Dynamic Modules](https://docs.nestjs.com/fundamentals/dynamic-modules)
- [NestJS Architecture Guide](https://docs.nestjs.com/recipes/cqrs)
- [NestJS Best Practices](https://docs.nestjs.com/recipes/cqrs)
