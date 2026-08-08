---
section: NestJS
category: Backend
tags: [concept]
---

# NestJS Interceptors

> **TL;DR:** Interceptors wrap handler execution with `tap` semantics — they can transform the result, bind extra logic, transform exceptions, or completely override control flow. They are the right place for cross-cutting concerns like logging, caching, timing, and response mapping.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

**Interceptors** in NestJS are classes that implement the `NestInterceptor` interface. They have the ability to bind extra logic before/after route handler execution, transform responses, handle errors, and extend function behavior using RxJS Observable streams.

## Why Do We Need It?

1. **Logging**: Log request/response details for monitoring.

2. **Caching**: Cache responses to improve performance.

3. **Transformation**: Transform response data (e.g., wrap in envelope).

4. **Timeout**: Add timeout logic to prevent slow operations.

5. **Error Handling**: Catch and transform errors.

6. **Metrics**: Collect performance metrics.

7. **Response Mapping**: Map or filter response data.

## How It Works

Interceptors implement `intercept(context, next)` receiving an `ExecutionContext` and `CallHandler`. The `CallHandler.handle()` returns an Observable that can be piped through RxJS operators.

```text
Request

   |

   v
+-------------------------------+

|       Interceptor (Before)    |
|  - Log, Cache, Transform      |

+-------------------------------+

   |

   v
+-------------------------------+

|     next.handle() Observable  |
|  +-------------------------+  |
|  |     Route Handler       |  |
|  +-------------------------+  |

+-------------------------------+

   |

   v
+-------------------------------+

|       Interceptor (After)     |
|  - map(), tap(), catchError() |

+-------------------------------+

   |

   v
Response

```

### Common RxJS Operators

| Operator | Purpose |
|----------|---------|
| `map()` | Transform response data |
| `tap()` | Side effects (logging, metrics) |
| `catchError()` | Handle errors |
| `timeout()` | Add timeout |
| `of()` | Return cached/synthetic value |
| `throwError()` | Throw custom error |
| `switchMap()` | Switch to new observable |
| `mergeMap()` | Merge multiple observables |

## Code Examples

### Logging Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, Logger } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger('HTTP');

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const now = Date.now();

    return next.handle().pipe(
      tap(() => {
        const elapsed = Date.now() - now;
        this.logger.log(`${method} ${url} - ${elapsed}ms`);
      }),
    );
  }
}

```

### Response Transformation Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Response<T> {
  data: T;
  timestamp: string;
  path: string;
}

@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
    const request = context.switchToHttp().getRequest();
    return next.handle().pipe(
      map((data) => ({
        data,
        timestamp: new Date().toISOString(),
        path: request.url,
      })),
    );
  }
}

```

### Caching Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class CacheInterceptor implements NestInterceptor {
  private cache = new Map<string, { data: any; expiry: number }>();

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    if (request.method !== 'GET') return next.handle();

    const key = `${request.method}:${request.url}`;
    const cached = this.cache.get(key);
    if (cached && cached.expiry > Date.now()) return of(cached.data);

    return next.handle().pipe(
      tap((data) => {
        this.cache.set(key, { data, expiry: Date.now() + 5000 });
      }),
    );
  }
}

```

### Timeout Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, RequestTimeoutException } from '@nestjs/common';
import { Observable, throwError } from 'rxjs';
import { timeout, catchError } from 'rxjs/operators';

@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      timeout(5000),
      catchError((err) => {
        if (err.name === 'TimeoutError') return throwError(() => new RequestTimeoutException());
        return throwError(() => err);
      }),
    );
  }
}

```

### Error Handling Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, HttpException, HttpStatus, Logger } from '@nestjs/common';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable()
export class ErrorHandlingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(ErrorHandlingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      catchError((error) => {
        this.logger.error(error.message, error.stack);
        if (error instanceof HttpException) return throwError(() => error);
        return throwError(() => new HttpException('Internal server error', HttpStatus.INTERNAL_SERVER_ERROR));
      }),
    );
  }
}

```

### Metrics Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class MetricsInterceptor implements NestInterceptor {
  constructor(private readonly metricsService: MetricsService) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const startTime = Date.now();

    return next.handle().pipe(
      tap({
        next: () => this.metricsService.recordRequest(method, url, Date.now() - startTime, 'success'),
        error: () => this.metricsService.recordRequest(method, url, Date.now() - startTime, 'error'),
      }),
    );
  }
}

```

### Serialization Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { plainToInstance } from 'class-transformer';

export function Serialize(dto: any) {
  return (target: any, key?: string, descriptor?: any) => {
    Reflect.defineMetadata('serialize:dto', dto, target, key ?? target);
    return descriptor;
  };
}

@Injectable()
export class SerializeInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const handler = context.getHandler();
    const dto = Reflect.getMetadata('serialize:dto', handler);
    if (!dto) return next.handle();
    return next.handle().pipe(map((data) => plainToInstance(dto, data, { excludeExtraneousValues: true })));
  }
}

```

### File Upload Interceptor

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { v4 as uuid } from 'uuid';
import { extname } from 'path';

export function SingleFileInterceptor(fieldName: string) {
  return UseInterceptors(
    FileInterceptor(fieldName, {
      storage: diskStorage({
        destination: './uploads',
        filename: (req, file, cb) => {
          cb(null, `${uuid()}${extname(file.originalname)}`);
        },
      }),
      limits: { fileSize: 5 * 1024 * 1024 },
      fileFilter: (req, file, cb) => {
        if (!file.mimetype.match(/\/(jpg|jpeg|png|gif)$/)) {
          return cb(new BadRequestException('Only image files allowed'), false);
        }
        cb(null, true);
      },
    }),
  );
}

```

## Real-World Use Cases

### 1. API Response Envelope

```typescript
@Injectable()
export class EnvelopeInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => ({
        success: true,
        data,
        meta: { timestamp: Date.now() },
      })),
    );
  }
}

```

### 2. Request ID Injection

```typescript
@Injectable()
export class RequestIdInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const requestId = request.headers['x-request-id'] || uuid();
    request.requestId = requestId;
    const response = context.switchToHttp().getResponse();
    response.setHeader('X-Request-Id', requestId);
    return next.handle();
  }
}

```

### 3. Response Compression

```typescript
@Injectable()
export class CompressionInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const response = context.switchToHttp().getResponse();
    response.setHeader('Content-Encoding', 'gzip');
    return next.handle().pipe(
      map((data) => gzipSync(JSON.stringify(data))),
    );
  }
}

```

## Common Mistakes

### 1. Not Returning the Observable

```typescript
// BAD
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  console.log('before');
  // Forgot to return next.handle()!
}

// GOOD
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  console.log('before');
  return next.handle();
}

```

### 2. Blocking Operations in Interceptors

```typescript
// BAD: Synchronous heavy operation
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  const data = heavyComputation(); // Blocks event loop
  return next.handle();
}

// GOOD: Async processing
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  return next.handle().pipe(
    switchMap(async (data) => {
      return await processAsync(data);
    }),
  );
}

```

### 3. Not Handling Errors

```typescript
// BAD: No error handling
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  return next.handle().pipe(
    tap((data) => this.log(data)),
  );
}

// GOOD: Handle errors
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  return next.handle().pipe(
    tap((data) => this.log(data)),
    catchError((error) => {
      this.logger.error(error);
      return throwError(() => error);
    }),
  );
}

```

## Best Practices

1. **Single Responsibility**: Each interceptor should handle one concern.

2. **Keep Fast**: Interceptors run on every request — keep them lightweight.

3. **Use RxJS Operators**: Leverage `map()`, `tap()`, `catchError()` for clean transformations.

4. **Error Handling**: Always handle errors in interceptors.

5. **Async Operations**: Use RxJS operators for async work, not blocking code.

6. **Composability**: Design interceptors to be composable and layered.

7. **Testing**: Test interceptors by mocking `CallHandler`.

## Performance Considerations

1. **Execution Time**: Interceptors run on every matching request.

2. **Memory**: Cache interceptors can grow unbounded — implement eviction.

3. **RxJS Overhead**: Observable chains have minimal overhead but can accumulate.

4. **Global vs Local**: Apply interceptors only where needed.

5. **Async Work**: Avoid heavy async operations — use message queues instead.

## Summary

Interceptors are NestJS's powerful mechanism for cross-cutting concerns that need access to both request and response. They leverage RxJS for composable transformations, enabling logging, caching, transformation, timeout, and error handling in a clean, functional style.

## Cheat Sheet
| Concept | Description |
|---------|-------------|
| `NestInterceptor` | Interface interceptors implement |
| `intercept()` | Method wrapping handler execution |
| `ExecutionContext` | Provides request/handler info |
| `CallHandler` | Represents the route handler |
| `next.handle()` | Execute handler, returns Observable |
| `map()` | Transform response data |
| `tap()` | Side effects without modification |
| `catchError()` | Handle errors in stream |
| `timeout()` | Add request timeout |
| `of()` | Return cached value |
| `throwError()` | Throw error in stream |
| `APP_INTERCEPTOR` | Register global interceptor |

---

## See Also
- [Design Patterns](../10-Design-Patterns/)
- [Microservices](../12-Microservices/)
- [Node.js](../05-NodeJS/)
- [REST APIs](../07-REST-API/)

## References & Learn More

- [NestJS Interceptors Official Docs](https://docs.nestjs.com/interceptors)
- [RxJS Operators Guide](https://rxjs.dev/guide/operators)
- [NestJS Response Mapping](https://docs.nestjs.com/interceptors#response-mapping)
- [NestJS Streams](https://docs.nestjs.com/techniques/streaming-files)
