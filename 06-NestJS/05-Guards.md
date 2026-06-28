# Guards

## Definition

**Guards** in NestJS are classes that implement the `CanActivate` interface. They are responsible for determining whether a request should be handled by the route handler or rejected. Guards execute after middleware but before interceptors and pipes, making them ideal for authorization, authentication, and access control logic.

Guards have access to the execution context, which provides information about the current request, including the handler, class, and args.

## Why Do We Need It?

1. **Authorization**: Control access to routes based on user roles or permissions.
2. **Authentication**: Verify user identity before processing requests.
3. **Access Control**: Implement fine-grained permission systems.
4. **Route Protection**: Protect sensitive endpoints from unauthorized access.
5. **Rate Limiting**: Prevent abuse by limiting request frequency.
6. **Feature Flags**: Enable/disable routes based on feature flags.
7. **Input Validation**: Validate request context before processing.

## How It Works

Guards implement the `CanActivate` interface, which has a single method: `canActivate(context: ExecutionContext)`. This method returns:
- `true` if the request is allowed
- `false` if the request is rejected (throws ForbiddenException)
- A Promise or Observable that resolves to a boolean

### Guard Execution Flow

```text
┌──────────────────────────────────────────────────────────┐
│                  Request Lifecycle                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Client Request                                          │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────┐                                        │
│  │  Middleware   │  (e.g., Logger, CORS)                 │
│  └──────┬───────┘                                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │    Guard     │  ★ Authorization check here            │
│  │  canActivate │  Returns true/false                    │
│  └──────┬───────┘                                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Interceptor  │  (before/after handler)                │
│  └──────┬───────┘                                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │    Pipe      │  (validation, transformation)          │
│  └──────┬───────┘                                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │  Controller  │  (route handler)                       │
│  │   Handler    │                                        │
│  └──────────────┘                                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Guard Application Levels

```text
┌─────────────────────────────────────────────────────────┐
│                  Guard Application Levels                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Global Guard:                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │ app.useGlobalGuards(new AuthGuard());               ││
│  │ Applies to ALL routes in the application            ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
│  Controller-level Guard:                                │
│  ┌─────────────────────────────────────────────────────┐│
│  │ @UseGuards(AuthGuard)                               ││
│  │ @Controller('users')                                ││
│  │ export class UserController {}                      ││
│  │ Applies to ALL routes in the controller             ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
│  Method-level Guard:                                    │
│  ┌─────────────────────────────────────────────────────┐│
│  │ @UseGuards(RolesGuard)                              ││
│  │ @Delete(':id')                                      ││
│  │ remove(@Param('id') id: string) {}                  ││
│  │ Applies only to this route                          ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
│  Custom Decorator Guard:                                │
│  ┌─────────────────────────────────────────────────────┐│
│  │ @Roles('admin')                                     ││
│  │ @Delete(':id')                                      ││
│  │ remove(@Param('id') id: string) {}                  ││
│  │ Guard receives metadata from decorator              ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Code Examples

### Basic Auth Guard

```typescript
// auth.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { Reflector } from '@nestjs/core';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(
    private readonly jwtService: JwtService,
    private readonly reflector: Reflector,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);

    if (!token) {
      throw new UnauthorizedException();
    }

    try {
      const payload = this.jwtService.verify(token);
      request.user = payload;
      return true;
    } catch {
      throw new UnauthorizedException();
    }
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
```

### Role-Based Guard

```typescript
// roles.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { Role } from '../enums/role.enum';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles) {
      return true; // No roles required
    }

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
```

### Custom Decorator for Roles

```typescript
// roles.decorator.ts
import { SetMetadata } from '@nestjs/common';
import { Role } from '../enums/role.enum';

export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);

// Usage in controller
import { Roles } from '../decorators/roles.decorator';
import { Role } from '../enums/role.enum';

@Controller('users')
@UseGuards(AuthGuard, RolesGuard)
export class UserController {
  @Get()
  findAll() {
    return this.userService.findAll(); // Accessible to all authenticated users
  }

  @Roles(Role.ADMIN)
  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.userService.remove(id); // Only admins
  }

  @Roles(Role.ADMIN, Role.MODERATOR)
  @Put(':id')
  update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
    return this.userService.update(id, dto); // Admins and moderators
  }
}
```

### Permission-Based Guard

```typescript
// permissions.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { Permission } from '../enums/permission.enum';

export const PERMISSIONS_KEY = 'permissions';
export const Permissions = (...permissions: Permission[]) =>
  SetMetadata(PERMISSIONS_KEY, permissions);

@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPermissions = this.reflector.getAllAndOverride<Permission[]>(
      PERMISSIONS_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (!requiredPermissions) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    return requiredPermissions.every((permission) =>
      user.permissions?.includes(permission),
    );
  }
}
```

### API Key Guard

```typescript
// api-key.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(private configService: ConfigService) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];

    if (!apiKey) {
      throw new UnauthorizedException('API key required');
    }

    const validApiKey = this.configService.get('API_KEY');
    if (apiKey !== validApiKey) {
      throw new UnauthorizedException('Invalid API key');
    }

    return true;
  }
}
```

### Rate Limiting Guard

```typescript
// rate-limit.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';

export const RATE_LIMIT_KEY = 'rate_limit';
export const RateLimit = (points: number, duration: number) =>
  SetMetadata(RATE_LIMIT_KEY, { points, duration });

@Injectable()
export class RateLimitGuard implements CanActivate {
  private readonly rateLimitMap = new Map<string, { count: number; resetTime: number }>();

  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const rateLimit = this.reflector.getAllAndOverride<{ points: number; duration: number }>(
      RATE_LIMIT_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (!rateLimit) return true;

    const request = context.switchToHttp().getRequest();
    const key = `${request.ip}:${context.getHandler().name}`;
    const now = Date.now();

    const current = this.rateLimitMap.get(key);

    if (!current || now > current.resetTime) {
      this.rateLimitMap.set(key, { count: 1, resetTime: now + rateLimit.duration * 1000 });
      return true;
    }

    if (current.count >= rateLimit.points) {
      throw new HttpException('Rate limit exceeded', HttpStatus.TOO_MANY_REQUESTS);
    }

    current.count++;
    return true;
  }
}
```

### Scope Guard

```typescript
// scope.guard.ts
import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

export const SCOPE_KEY = 'scope';
export const Scope = (scope: string) => SetMetadata(SCOPE_KEY, scope);

@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScope = this.reflector.getAllAndOverride<string>(SCOPE_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredScope) return true;

    const request = context.switchToHttp().getRequest();
    const userScopes = request.user?.scopes || [];

    if (!userScopes.includes(requiredScope)) {
      throw new ForbiddenException(`Missing scope: ${requiredScope}`);
    }

    return true;
  }
}
```

### Global Guard

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { AuthGuard } from './auth/auth.guard';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Apply globally
  app.useGlobalGuards(new AuthGuard());

  await app.listen(3000);
}
bootstrap();

// Or via module
@Module({
  providers: [
    {
      provide: APP_GUARD,
      useClass: AuthGuard,
    },
  ],
})
export class AppModule {}
```

## Real-World Use Cases

### 1. JWT Authentication Guard

```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(
    private reflector: Reflector,
    private jwtService: JwtService,
  ) {
    super();
  }

  canActivate(context: ExecutionContext) {
    const isPublic = this.reflector.getAllAndOverride<boolean>('isPublic', [
      context.getHandler(),
      context.getClass(),
    ]);

    if (isPublic) return true;

    return super.canActivate(context);
  }

  handleRequest(err: any, user: any, info: any) {
    if (err || !user) {
      throw err || new UnauthorizedException();
    }
    return user;
  }
}
```

### 2. Subscription Tier Guard

```typescript
@Injectable()
export class SubscriptionGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private subscriptionService: SubscriptionService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const requiredTier = this.reflector.getAllAndOverride<SubscriptionTier>(
      'subscription_tier',
      [context.getHandler(), context.getClass()],
    );

    if (!requiredTier) return true;

    const request = context.switchToHttp().getRequest();
    const userTier = await this.subscriptionService.getUserTier(request.user.id);

    const tierLevels: Record<SubscriptionTier, number> = {
      free: 0,
      basic: 1,
      pro: 2,
      enterprise: 3,
    };

    return tierLevels[userTier] >= tierLevels[requiredTier];
  }
}
```

### 3. Feature Flag Guard

```typescript
@Injectable()
export class FeatureFlagGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private featureFlagService: FeatureFlagService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const featureKey = this.reflector.getAllAndOverride<string>('feature', [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!featureKey) return true;

    const request = context.switchToHttp().getRequest();
    return this.featureFlagService.isEnabled(featureKey, {
      userId: request.user?.id,
      tenantId: request.headers['x-tenant-id'],
    });
  }
}

// Usage
@FeatureFlag('new-dashboard')
@Get('dashboard')
getDashboard() { ... }
```

## Common Mistakes

### 1. Not Throwing Proper Exceptions

```typescript
// ❌ BAD: Returning false without explanation
canActivate(context: ExecutionContext): boolean {
  return false; // No error message
}

// ✅ GOOD: Throw descriptive exception
canActivate(context: ExecutionContext): boolean {
  throw new ForbiddenException('Insufficient permissions');
}
```

### 2. Making Guards Too Complex

```typescript
// ❌ BAD: Guard doing too much
@Injectable()
export class MegaGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    // Auth check
    // Role check
    // Permission check
    // Rate limit check
    // Feature flag check
    // Logging
    // Metrics
    // All in one guard!
  }
}

// ✅ GOOD: Compose multiple focused guards
@UseGuards(AuthGuard, RolesGuard, RateLimitGuard)
@Get('admin')
adminEndpoint() {}
```

### 3. Not Using Reflector Properly

```typescript
// ❌ BAD: Hardcoding metadata access
canActivate(context: ExecutionContext): boolean {
  const handler = context.getHandler();
  const roles = Reflect.getMetadata('roles', handler);
  // ...
}

// ✅ GOOD: Use Reflector
canActivate(context: ExecutionContext): boolean {
  const roles = this.reflector.getAllAndOverride<Role[]>('roles', [
    context.getHandler(),
    context.getClass(),
  ]);
  // ...
}
```

### 4. Guards Blocking Every Request

```typescript
// ❌ BAD: Guard that blocks all requests
@Injectable()
export class BrokenGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    return false; // Always blocks!
  }
}

// ✅ GOOD: Guard with proper logic
@Injectable()
export class ProperGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    return request.user !== undefined;
  }
}
```

## Best Practices

1. **Single Responsibility**: Each guard should handle one concern (auth, roles, rate limiting).
2. **Composable**: Design guards to be composable and layered.
3. **Use Reflector**: Always use Reflector for metadata access.
4. **Throw Exceptions**: Throw descriptive exceptions instead of returning false.
5. **Fast Execution**: Guards should be fast — avoid heavy operations.
6. **Caching**: Cache permission/role checks when possible.
7. **Testing**: Test guards in isolation with mocked context.
8. **Documentation**: Document guard requirements with custom decorators.

## Performance Considerations

1. **Execution Time**: Guards run on every matching request — keep them fast.
2. **Caching**: Cache role/permission lookups to avoid repeated database queries.
3. **Async Guards**: Use async guards sparingly — they add latency.
4. **Early Return**: Return early when possible to avoid unnecessary checks.
5. **Guard Ordering**: Order guards by likelihood of rejection (cheapest first).

## Interview Questions

### Beginner

**Q1: What is a guard in NestJS?**
A guard is a class implementing `CanActivate` that determines whether a request should be handled. It's used for authorization and access control.

**Q2: When do guards execute in the request lifecycle?**
After middleware, before interceptors and pipes.

**Q3: What does `canActivate` return?**
A boolean (or Promise/Observable resolving to boolean) — `true` to allow, `false` or throw exception to reject.

**Q4: How do you apply a guard to a controller?**
Use `@UseGuards(AuthGuard)` decorator on the controller class.

**Q5: What is the Reflector used for in guards?**
To access metadata set by decorators (e.g., roles, permissions).

### Intermediate

**Q6: How do you create a role-based access control system?**
Define roles in an enum, create a `@Roles()` decorator using `SetMetadata`, and implement a `RolesGuard` that reads the metadata.

**Q7: How do you make some routes public (skip auth)?**
Use `@Public()` decorator and check for it in the guard to bypass authentication.

**Q8: What is the difference between `APP_GUARD` and `@UseGuards()`?**
- `APP_GUARD`: Applies guard globally via module provider
- `@UseGuards()`: Applies guard to specific controller/method

**Q9: How do you test a guard?**
Create a mock `ExecutionContext`, set up the reflector with metadata, and verify `canActivate` returns the expected value.

**Q10: Can guards be async?**
Yes, `canActivate` can return a Promise or Observable.

### Senior

**Q11: Design a multi-tenant authorization system.**
Use guards with tenant context extracted from request headers. Implement tenant-specific permission databases and caching layers.

**Q12: How would you implement ABAC (Attribute-Based Access Control)?**
Create a guard that evaluates policies based on user attributes, resource attributes, and environment conditions.

**Q13: How do you handle guard performance in high-traffic systems?**
Cache permission checks in Redis, implement guard result memoization, and use async guards with connection pooling.

**Q14: How would you implement distributed rate limiting?**
Use Redis with sliding window algorithm, implementing the guard logic with Redis transactions.

**Q15: Design a guard system for microservices.**
Implement guards at the API gateway level, propagate auth context through service mesh, and use JWT claims for authorization.

### FAANG-Style

**Q16: Design a zero-trust security model with guards.**
Every request must be authenticated and authorized. Implement guards at every level: gateway, service, and database.

**Q17: How would you implement real-time permission updates?**
Use WebSockets or Server-Sent Events to push permission changes. Guards check a local cache with TTL.

**Q18: Design a guard for GraphQL resolvers.**
Implement `GqlExecutionContext.create()` to extract GraphQL context, then apply the same authorization logic.

**Q19: How would you audit guard decisions?**
Log guard decisions to an audit service asynchronously. Include user, resource, action, and decision.

**Q20: Design a guard system supporting dynamic permissions.**
Store permissions in a database, cache in Redis, and implement a guard that checks against the cached permissions.

### Follow-ups

**Q21: How do you handle guard errors gracefully?**
Catch exceptions in guards and throw appropriate HTTP exceptions with meaningful messages.

**Q22: Can guards access the database?**
Yes, but it adds latency. Cache database lookups when possible.

**Q23: How do you order multiple guards?**
Guards execute in the order they're defined. Use `APP_GUARD` for global, `@UseGuards()` for specific.

**Q24: How do you mock guards in tests?**
Override the guard provider in the test module with a mock that always returns true.

**Q25: What's the difference between guards and middleware?**
Middleware runs first and handles cross-cutting concerns. Guards are specifically for authorization and access control.

## Summary

Guards are NestJS's authorization mechanism that determines whether requests should be allowed or rejected. They implement the `CanActivate` interface and have access to the execution context for making authorization decisions. Guards work with decorators and Reflector for metadata-driven authorization patterns.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `CanActivate` | Interface guards implement |
| `canActivate()` | Method that returns boolean |
| `ExecutionContext` | Provides request/handler info |
| `Reflector` | Access decorator metadata |
| `@UseGuards()` | Apply guard to controller/method |
| `APP_GUARD` | Apply guard globally |
| `@SetMetadata()` | Attach metadata for guards |
| `@Roles()` | Custom decorator for roles |
| `@Public()` | Mark route as public |
| `ForbiddenException` | Throw for unauthorized access |
| `UnauthorizedException` | Throw for unauthenticated requests |

## References & Learn More

- [NestJS Guards Official Docs](https://docs.nestjs.com/guards)
- [NestJS Authorization](https://docs.nestjs.com/security/authorization)
- [NestJS Authentication](https://docs.nestjs.com/security/authentication)
- [NestJS Custom Decorators](https://docs.nestjs.com/custom-decorators)
