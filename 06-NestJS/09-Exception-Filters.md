# Exception Filters

## Definition

**Exception Filters** in NestJS are classes that implement the `ExceptionFilter` interface. They are responsible for catching exceptions thrown during request handling and transforming them into appropriate HTTP responses. Exception filters provide a centralized way to handle errors consistently across the application.

NestJS has a built-in `ExceptionsFilter` (default exception filter) that handles `HttpException` and returns standard HTTP error responses. Custom exception filters extend this behavior for application-specific error handling.

## Why Do We Need It?

1. **Centralized Error Handling**: Handle all errors in one place.
2. **Consistent Responses**: Return uniform error response format.
3. **Error Logging**: Log errors for debugging and monitoring.
4. **Custom Error Codes**: Map application errors to HTTP status codes.
5. **Error Transformation**: Transform internal errors to user-friendly messages.
6. **Security**: Hide internal error details from clients.

## How It Works

Exception filters catch exceptions thrown by:
- Controllers
- Services
- Guards
- Interceptors
- Pipes

They receive the exception and the `ArgumentsHost` which provides access to the request/response context.

### Exception Flow

```
Request
   |
   v
+-------------------------------+
|       Controller/Service      |
|       throws exception        |
+-------------------------------+
   |
   v
+-------------------------------+
|     Exception Filter          |
|  1. Catch exception          |
|  2. Log error                |
|  3. Determine HTTP status    |
|  4. Format response          |
|  5. Send response            |
+-------------------------------+
   |
   v
Error Response (JSON)
```

### Built-in HTTP Exceptions

| Exception | Status Code | Description |
|-----------|-------------|-------------|
| `BadRequestException` | 400 | Invalid request data |
| `UnauthorizedException` | 401 | Authentication required |
| `ForbiddenException` | 403 | Insufficient permissions |
| `NotFoundException` | 404 | Resource not found |
| `MethodNotAllowedException` | 405 | HTTP method not allowed |
| `NotAcceptableException` | 406 | Not acceptable |
| `RequestTimeoutException` | 408 | Request timeout |
| `ConflictException` | 409 | Resource conflict |
| `GoneException` | 410 | Resource permanently removed |
| `PayloadTooLargeException` | 413 | Request body too large |
| `UnsupportedMediaTypeException` | 415 | Unsupported media type |
| `UnprocessableEntityException` | 422 | Validation failed |
| `TooManyRequestsException` | 429 | Rate limit exceeded |
| `InternalServerErrorException` | 500 | Server error |
| `BadGatewayException` | 502 | Bad gateway |
| `ServiceUnavailableException` | 503 | Service unavailable |
| `GatewayTimeoutException` | 504 | Gateway timeout |

## Code Examples

### Default Exception Filter

```typescript
// NestJS default behavior - no custom filter needed
import { NotFoundException } from '@nestjs/common';

@Injectable()
export class UserService {
  async findOne(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }
}
// Default filter returns:
// {
//   "statusCode": 404,
//   "message": "User with ID 123 not found",
//   "error": "Not Found"
// }
```

### Custom Exception Filter

```typescript
// http-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(HttpExceptionFilter.name);

  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      method: request.method,
      message: exception.message || 'Internal server error',
    };

    this.logger.error(
      `${request.method} ${request.url} ${status}`,
      exception.stack,
    );

    response.status(status).json(errorResponse);
  }
}
```

### Global Exception Filter

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Apply globally
  app.useGlobalFilters(new HttpExceptionFilter());

  await app.listen(3000);
}
bootstrap();

// Or via module
@Module({
  providers: [
    {
      provide: APP_FILTER,
      useClass: HttpExceptionFilter,
    },
  ],
})
export class AppModule {}
```

### Catching All Exceptions

```typescript
// all-exceptions.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Internal server error';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      message = exception.message;
    } else if (exception instanceof Error) {
      message = exception.message;
      this.logger.error(`Unhandled error: ${exception.message}`, exception.stack);
    }

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message,
    });
  }
}
```

### Validation Exception Filter

```typescript
// validation-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  BadRequestException,
} from '@nestjs/common';
import { Response } from 'express';

@Catch(BadRequestException)
export class ValidationExceptionFilter implements ExceptionFilter {
  catch(exception: BadRequestException, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse<Response>();
    const exceptionResponse = exception.getResponse();

    const errors = typeof exceptionResponse === 'object'
      ? (exceptionResponse as any).message
      : [exceptionResponse];

    response.status(400).json({
      statusCode: 400,
      message: 'Validation failed',
      errors: Array.isArray(errors) ? errors : [errors],
      timestamp: new Date().toISOString(),
    });
  }
}
```

### Database Exception Filter

```typescript
// database-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Response } from 'express';
import { QueryFailedError } from 'typeorm';

@Catch(QueryFailedError)
export class DatabaseExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(DatabaseExceptionFilter.name);

  catch(exception: QueryFailedError, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse<Response>();
    const detail = exception.driverError as any;

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Database error';

    if (detail.code === '23505') {
      status = HttpStatus.CONFLICT;
      message = 'Unique constraint violation';
    } else if (detail.code === '23503') {
      status = HttpStatus.BAD_REQUEST;
      message = 'Foreign key constraint violation';
    }

    this.logger.error(`Database error: ${detail.message}`, exception.stack);

    response.status(status).json({
      statusCode: status,
      message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### GraphQL Exception Filter

```typescript
// graphql-exception.filter.ts
import { Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { GqlExecutionContext, GraphQLException } from '@nestjs/graphql';
import { GraphQLError } from 'graphql';

@Catch(HttpException)
export class GraphQLExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const gqlHost = GqlExecutionContext.create(host);
    const status = exception.getStatus();

    throw new GraphQLError(exception.message, {
      extensions: {
        code: this.mapStatusToCode(status),
        status,
      },
    });
  }

  private mapStatusToCode(status: number): string {
    const map: Record<number, string> = {
      400: 'BAD_USER_INPUT',
      401: 'UNAUTHENTICATED',
      403: 'FORBIDDEN',
      404: 'NOT_FOUND',
      409: 'CONFLICT',
    };
    return map[status] || 'INTERNAL_SERVER_ERROR';
  }
}
```

### Custom Application Exception

```typescript
// app.exception.ts
import { HttpException, HttpStatus } from '@nestjs/common';

export class InsufficientFundsException extends HttpException {
  constructor(required: number, available: number) {
    super(
      {
        statusCode: HttpStatus.BAD_REQUEST,
        message: 'Insufficient funds',
        error: {
          required,
          available,
          deficit: required - available,
        },
      },
      HttpStatus.BAD_REQUEST,
    );
  }
}

// Usage in service
@Injectable()
export class PaymentService {
  async processPayment(amount: number, userId: string): Promise<any> {
    const balance = await this.getBalance(userId);
    if (balance < amount) {
      throw new InsufficientFundsException(amount, balance);
    }
    // Process payment
  }
}
```

## Real-World Use Cases

### 1. Production Error Handler

```typescript
@Catch()
export class ProductionExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger('Production');

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = 500;
    let message = 'Internal server error';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const res = exception.getResponse();
      message = typeof res === 'string' ? res : (res as any).message;
    }

    // Log to monitoring service
    this.logger.error({
      status,
      message: exception instanceof Error ? exception.message : message,
      stack: exception instanceof Error ? exception.stack : undefined,
      path: request.url,
      method: request.method,
    });

    // Don't expose internal details in production
    response.status(status).json({
      statusCode: status,
      message: status === 500 ? 'Internal server error' : message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### 2. Error Response Envelope

```typescript
@Catch()
export class ErrorEnvelopeFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const response = host.switchToHttp().getResponse<Response>();

    let status = 500;
    let message = 'Internal server error';
    let details: any = null;

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const res = exception.getResponse();
      message = typeof res === 'string' ? res : (res as any).message;
      details = typeof res === 'object' ? (res as any).error : null;
    }

    response.status(status).json({
      success: false,
      error: {
        statusCode: status,
        message,
        details,
        timestamp: new Date().toISOString(),
      },
    });
  }
}
```

## Common Mistakes

### 1. Not Catching Specific Exceptions

```typescript
// BAD: Catches everything, loses specificity
@Catch()
export class BadFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // Treats all exceptions the same
  }
}

// GOOD: Catch specific exceptions
@Catch(HttpException)
export class GoodFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const status = exception.getStatus();
    // Handle HTTP exceptions specifically
  }
}
```

### 2. Exposing Internal Errors

```typescript
// BAD: Exposes internal details
response.status(500).json({
  error: exception.stack, // Exposes stack trace!
});

// GOOD: Hide internal details
response.status(500).json({
  message: 'Internal server error',
  // Don't include stack trace in production
});
```

### 3. Not Logging Errors

```typescript
// BAD: Silent failure
catch(exception: unknown, host: ArgumentsHost) {
  response.status(500).json({ message: 'Error' });
}

// GOOD: Always log errors
catch(exception: unknown, host: ArgumentsHost) {
  this.logger.error(exception);
  response.status(500).json({ message: 'Error' });
}
```

### 4. Wrong Filter Application

```typescript
// BAD: Controller-level filter for specific route
@UseFilters(HttpExceptionFilter) // Only applies to this controller
@Controller('users')
export class UserController {}

// GOOD: Global filter for all routes
app.useGlobalFilters(new HttpExceptionFilter());
```

## Best Practices

1. **Global Filters**: Use global filters for consistent error handling.
2. **Specific Filters**: Create specific filters for different error types.
3. **Always Log**: Log all errors for debugging and monitoring.
4. **Hide Details**: Don't expose internal error details in production.
5. **Consistent Format**: Return uniform error response format.
6. **Error Codes**: Use meaningful error codes for client-side handling.
7. **Testing**: Test filters with different exception types.

## Performance Considerations

1. **Filter Execution**: Filters run only when exceptions are thrown.
2. **Logging Overhead**: Async logging doesn't block request processing.
3. **Error Serialization**: Keep error response objects small.
4. **Monitoring**: Send errors to monitoring services asynchronously.

## Interview Questions

### Beginner

**Q1: What is an exception filter in NestJS?**
A class implementing `ExceptionFilter` that catches exceptions and transforms them into HTTP responses.

**Q2: What is the default exception filter?**
NestJS has a built-in filter that catches `HttpException` and returns standard error responses.

**Q3: How do you apply a filter globally?**
Use `app.useGlobalFilters()` or `APP_FILTER` token.

**Q4: What is `ArgumentsHost`?**
Provides access to request/response context and handler information.

**Q5: How do you catch all exceptions?**
Use `@Catch()` without parameters to catch all exceptions.

### Intermediate

**Q6: How do you create a custom exception filter?**
Implement `ExceptionFilter`, use `@Catch()` decorator, handle exception in `catch()` method.

**Q7: What is the difference between `@Catch(HttpException)` and `@Catch()`?**
- `@Catch(HttpException)`: Only catches HttpException
- `@Catch()`: Catches all exceptions

**Q8: How do you access the request object in a filter?**
Use `host.switchToHttp().getRequest()`.

**Q9: How do you return different error formats?**
Implement different filters for different contexts (REST, GraphQL, WebSocket).

**Q10: How do you handle validation errors?**
Catch `BadRequestException` and extract validation error details.

### Senior

**Q11: Design a comprehensive error handling strategy.**
Layer 1: Input validation (pipes) -> Layer 2: Business errors (service) -> Layer 3: System errors (filters).

**Q12: How would you implement error monitoring?**
Send errors to Sentry/DataDog asynchronously, include correlation IDs.

**Q13: Design error handling for microservices.**
Centralized API gateway filter, service-specific filters, propagate error context.

**Q14: How would you implement error retry logic?**
Use interceptors with exponential backoff, not filters.

**Q15: Design error handling for WebSocket connections.**
Create WebSocket exception filter that sends error messages through socket.

### FAANG-Style

**Q16: Design a distributed error tracking system.**
Correlate errors across services, centralize in error tracking service, alert on patterns.

**Q17: How would you implement error rate limiting?**
Track error rates per endpoint, trigger alerts when threshold exceeded.

**Q18: Design error handling for serverless functions.**
Transform errors to Lambda-compatible format, handle cold start errors.

**Q19: How would you implement error-based circuit breaking?**
Track errors per service, open circuit when error rate exceeds threshold.

**Q20: Design a self-healing error system.**
Detect error patterns, automatically restart unhealthy services, rollback deployments.

### Follow-ups

**Q21: Can filters access route handler metadata?**
Yes, through `host.getHandler()` and `host.getClass()`.

**Q22: How do you test exception filters?**
Mock `ArgumentsHost`, create exception, verify response format.

**Q23: What is the order of filter execution?**
Method-level -> Controller-level -> Global.

**Q24: Can filters be async?**
Yes, filters can be async.

**Q25: How do you handle errors in WebSocket gateways?**
Create `WsExceptionFilter` using `WsException` and `WsArgumentsHost`.

## Summary

Exception Filters are NestJS's centralized error handling mechanism. They catch exceptions thrown during request processing and transform them into appropriate HTTP responses. Built-in filters handle basic cases, while custom filters provide application-specific error handling with logging, monitoring, and consistent error response formats.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `ExceptionFilter` | Interface filters implement |
| `catch()` | Method handling exceptions |
| `@Catch()` | Decorator to specify exception types |
| `ArgumentsHost` | Access request/response context |
| `HttpException` | Base HTTP exception class |
| `APP_FILTER` | Register global filter |
| `@UseFilters()` | Apply filter to controller/method |
| `BadRequestException` | 400 - Invalid request |
| `UnauthorizedException` | 401 - Auth required |
| `ForbiddenException` | 403 - Forbidden |
| `NotFoundException` | 404 - Not found |
| `ConflictException` | 409 - Conflict |
| `InternalServerErrorException` | 500 - Server error |

## References & Learn More

- [NestJS Exception Filters Official Docs](https://docs.nestjs.com/exception-filters)
- [NestJS Built-in HTTP Exceptions](https://docs.nestjs.com/exception-filters#built-in-http-exceptions)
- [HTTP Status Codes Reference](https://httpstatuses.com/)
- [Exception Filters: Custom Implementation](https://docs.nestjs.com/exception-filters#exception-filters)
