# NestJS Modules

[![Category: Backend](https://img.shields.io/badge/category-Backend-2ea44f)](.)

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

---

## See Also
- [Design Patterns](../10-Design-Patterns/)
- [Microservices](../12-Microservices/)
- [Node.js](../05-NodeJS/)
- [REST APIs](../07-REST-API/)

## References & Learn More

- [NestJS Modules Official Docs](https://docs.nestjs.com/modules)
- [NestJS Dynamic Modules](https://docs.nestjs.com/fundamentals/dynamic-modules)
- [NestJS Architecture Guide](https://docs.nestjs.com/recipes/cqrs)
- [NestJS Best Practices](https://docs.nestjs.com/recipes/cqrs)
