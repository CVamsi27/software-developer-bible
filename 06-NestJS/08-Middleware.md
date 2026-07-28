---
section: NestJS
category: Backend
tags: [concept]
---

# Middleware

[![Section](https://img.shields.io/badge/section-NestJS-success)](.)
[![Type](https://img.shields.io/badge/type-Concept-informational)](.)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](.)

## Definition

**Middleware** in NestJS is a function that has access to the request, response, and next function in the application's request-response cycle. Middleware executes before route handlers and can execute any code, end the request-response cycle, modify the request/response objects, or call the next middleware function in the stack.

NestJS middleware is similar to Express middleware and can be implemented as a function or a class implementing the `NestMiddleware` interface.

## Why Do We Need It?

1. **Cross-Cutting Concerns**: Handle logging, CORS, authentication, compression.

2. **Request Processing**: Modify request/response before reaching controllers.

3. **Third-Party Integration**: Integrate Express/Fastify middleware.

4. **Modularity**: Organize middleware in a modular fashion.

5. **Flexibility**: Apply middleware to specific routes or globally.

## How It Works

Middleware runs in the order they are registered, before guards, interceptors, pipes, and controllers. Each middleware calls `next()` to pass control to the next middleware.

```text
Request

   |

   v
+-------------------------------+

|       Middleware 1            |
|  (Logger, CORS)              |

+-------------------------------+

   | next()
   v
+-------------------------------+

|       Middleware 2            |
|  (Auth, Rate Limit)          |

+-------------------------------+

   | next()
   v
+-------------------------------+

|          Guard                |

+-------------------------------+

   |

   v
+-------------------------------+

|       Interceptor             |

+-------------------------------+

   |

   v
+-------------------------------+

|           Pipe                |

+-------------------------------+

   |

   v
+-------------------------------+

|       Controller              |

+-------------------------------+

   |

   v
Response

```

### Middleware Consumer

The `MiddlewareConsumer` provides methods to configure middleware:

- `apply()`: Apply middleware
- `exclude()`: Exclude specific routes
- `forRoutes()`: Specify routes

## Code Examples

### Class-Based Middleware

```typescript
// logger.middleware.ts
import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  private readonly logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction): void {
    const { method, originalUrl } = req;
    const start = Date.now();

    res.on('finish', () => {
      const { statusCode } = res;
      const elapsed = Date.now() - start;
      this.logger.log(`${method} ${originalUrl} ${statusCode} ${elapsed}ms`);
    });

    next();
  }
}

```

### Function-Based Middleware

```typescript
// cors.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function corsMiddleware(req: Request, res: Response, next: NextFunction) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }

  next();
}

```

### Module Configuration

```typescript
// app.module.ts
import { Module, NestModule, MiddlewareConsumer } from '@nestjs/common';
import { LoggerMiddleware } from './common/middleware/logger.middleware';
import { CorsMiddleware } from './common/middleware/cors.middleware';
import { UserController } from './user/user.controller';

@Module({
  imports: [UserModule, OrderModule],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    // Apply logger to all routes
    consumer
      .apply(LoggerMiddleware)
      .forRoutes('*');

    // Apply CORS to specific routes
    consumer
      .apply(CorsMiddleware)
      .forRoutes(UserController);

    // Apply middleware excluding certain routes
    consumer
      .apply(AuthMiddleware)
      .exclude(
        { path: 'auth/login', method: RequestMethod.POST },
        { path: 'auth/register', method: RequestMethod.POST },
      )
      .forRoutes('*');
  }
}

```

### Auth Middleware

```typescript
// auth.middleware.ts
import { Injectable, NestMiddleware, UnauthorizedException } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthMiddleware implements NestMiddleware {
  constructor(private readonly jwtService: JwtService) {}

  use(req: Request, res: Response, next: NextFunction): void {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      throw new UnauthorizedException('No token provided');
    }

    try {
      const payload = this.jwtService.verify(token);
      req.user = payload;
      next();
    } catch (error) {
      throw new UnauthorizedException('Invalid token');
    }
  }
}

```

### Rate Limiting Middleware

```typescript
// rate-limit.middleware.ts
import { Injectable, NestMiddleware, HttpException, HttpStatus } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class RateLimitMiddleware implements NestMiddleware {
  private readonly requests = new Map<string, { count: number; resetTime: number }>();
  private readonly maxRequests = 100;
  private readonly windowMs = 60 * 1000; // 1 minute

  use(req: Request, res: Response, next: NextFunction): void {
    const key = req.ip;
    const now = Date.now();
    const record = this.requests.get(key);

    if (!record || now > record.resetTime) {
      this.requests.set(key, { count: 1, resetTime: now + this.windowMs });
      return next();
    }

    if (record.count >= this.maxRequests) {
      throw new HttpException('Rate limit exceeded', HttpStatus.TOO_MANY_REQUESTS);
    }

    record.count++;
    next();
  }
}

```

### Body Parser Middleware

```typescript
// body-parser.middleware.ts
import { Injectable, NestMiddleware, BadRequestException } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class BodyParserMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    if (req.headers['content-type']?.includes('application/json')) {
      let body = '';
      req.on('data', (chunk) => { body += chunk; });
      req.on('end', () => {
        try {
          req.body = JSON.parse(body);
          next();
        } catch {
          throw new BadRequestException('Invalid JSON');
        }
      });
    } else {
      next();
    }
  }
}

```

### Request ID Middleware

```typescript
// request-id.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { v4 as uuid } from 'uuid';

@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    const requestId = req.headers['x-request-id'] as string || uuid();
    req.requestId = requestId;
    res.setHeader('X-Request-Id', requestId);
    next();
  }
}

```

### Multiple Middleware

```typescript
// app.module.ts
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(RequestIdMiddleware, LoggerMiddleware, CorsMiddleware)
      .forRoutes('*');
  }
}

```

### Conditional Middleware

```typescript
// conditional.middleware.ts
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class ConditionalMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    if (req.headers['x-internal-request']) {
      // Skip auth for internal requests
      return next();
    }

    // Apply auth logic
    this.authenticate(req, res, next);
  }

  private authenticate(req: Request, res: Response, next: NextFunction) {
    // Auth logic here
    next();
  }
}

```

## Real-World Use Cases

### 1. Global Logging Middleware

```typescript
@Injectable()
export class GlobalLoggerMiddleware implements NestMiddleware {
  private readonly logger = new Logger('Global');

  use(req: Request, res: Response, next: NextFunction): void {
    const correlationId = uuid();
    req.correlationId = correlationId;
    res.setHeader('X-Correlation-Id', correlationId);

    this.logger.log(`[${correlationId}] ${req.method} ${req.url}`);

    res.on('finish', () => {
      this.logger.log(`[${correlationId}] ${res.statusCode}`);
    });

    next();
  }
}

```

### 2. Request Sanitization Middleware

```typescript
@Injectable()
export class SanitizeMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    if (req.body) {
      req.body = this.sanitize(req.body);
    }
    next();
  }

  private sanitize(obj: any): any {
    if (typeof obj === 'string') {
      return obj.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    }
    if (typeof obj === 'object' && obj !== null) {
      for (const key of Object.keys(obj)) {
        obj[key] = this.sanitize(obj[key]);
      }
    }
    return obj;
  }
}

```

### 3. Tenant Resolution Middleware

```typescript
@Injectable()
export class TenantMiddleware implements NestMiddleware {
  constructor(private readonly tenantService: TenantService) {}

  async use(req: Request, res: Response, next: NextFunction): Promise<void> {
    const tenantId = req.headers['x-tenant-id'] as string;
    if (!tenantId) throw new BadRequestException('Tenant ID required');

    const tenant = await this.tenantService.findById(tenantId);
    if (!tenant) throw new NotFoundException('Tenant not found');

    req.tenant = tenant;
    next();
  }
}

```

## Common Mistakes

### 1. Not Calling next()

```typescript
// BAD: Forgot to call next()
use(req: Request, res: Response, next: NextFunction): void {
  console.log(req.url);
  // Request hangs forever
}

// GOOD
use(req: Request, res: Response, next: NextFunction): void {
  console.log(req.url);
  next();
}

```

### 2. Heavy Operations in Middleware

```typescript
// BAD: Synchronous heavy operation
use(req: Request, res: Response, next: NextFunction): void {
  const data = heavyComputation(); // Blocks event loop
  next();
}

// GOOD: Async processing
async use(req: Request, res: Response, next: NextFunction): Promise<void> {
  req.data = await heavyAsyncOperation();
  next();
}

```

### 3. Modifying Response After Send

```typescript
// BAD
use(req: Request, res: Response, next: NextFunction): void {
  next();
  res.setHeader('X-Custom', 'value'); // Too late!
}

// GOOD
use(req: Request, res: Response, next: NextFunction): void {
  res.setHeader('X-Custom', 'value');
  next();
}

```

## Best Practices

1. **Single Responsibility**: Each middleware handles one concern.

2. **Always Call next()**: Ensure middleware doesn't hang requests.

3. **Error Handling**: Use try-catch and call next(error) for errors.

4. **Keep Fast**: Middleware runs on every matching request.

5. **Use NestMiddleware**: Class-based middleware for DI support.

6. **Exclude Routes**: Use `exclude()` for routes that don't need middleware.

7. **Order Matters**: Apply middleware in the correct order.

## Performance Considerations

1. **Execution Order**: Middleware runs on every matching request.

2. **Async Overhead**: Async middleware adds latency per request.

3. **Memory**: In-memory stores (rate limiting) can grow unbounded.

4. **Conditional Execution**: Skip unnecessary middleware based on route.

5. **Caching**: Cache middleware results when possible.


## Summary

Middleware in NestJS provides a way to execute logic before route handlers, similar to Express middleware. They handle cross-cutting concerns like logging, authentication, and CORS. NestJS middleware can be class-based (with DI support) or function-based, and are configured through the `MiddlewareConsumer`.

## Cheat Sheet
| Concept | Description |
|---------|-------------|
| `NestMiddleware` | Interface for class-based middleware |
| `use()` | Method that processes request/response |
| `next()` | Call to pass to next middleware |
| `MiddlewareConsumer` | Configures middleware in modules |
| `apply()` | Apply middleware |
| `exclude()` | Exclude routes from middleware |
| `forRoutes()` | Specify target routes |
| `forRoutes('*')` | Apply to all routes |
| `RequestMethod.GET` | Filter by HTTP method |

---

## See Also
- [Node.js](../05-NodeJS/)
- [REST APIs](../07-REST-API/)
- [Microservices](../12-Microservices/)
- [Design Patterns](../10-Design-Patterns/)

## References & Learn More

- [NestJS Middleware Official Docs](https://docs.nestjs.com/middleware)
- [NestJS Express Middleware](https://docs.nestjs.com/techniques/middleware)
- [NestJS Fastify Middleware](https://docs.nestjs.com/techniques/fastify)
- [Express.js Middleware](https://expressjs.com/en/guide/using-middleware.html)
