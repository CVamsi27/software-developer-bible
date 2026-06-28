# Chain of Responsibility Pattern

## Definition

The Chain of Responsibility pattern is a behavioral design pattern that allows passing requests along a chain of handlers. Each handler decides either to process the request or to pass it to the next handler in the chain.

The pattern is particularly useful for processing pipelines, middleware chains, and when you want to give multiple objects a chance to handle a request without coupling the sender to specific receivers.

## Why Do We Need It?

Without the Chain of Responsibility pattern, request handling leads to:

1. **Tight coupling**: Sender depends on specific handlers
2. **Complex conditionals**: Large if/else chains for routing
3. **Difficult maintenance**: Adding new handlers requires modifying existing code
4. **Code duplication**: Common handling logic repeated

## How It Works

The Chain of Responsibility pattern works by:

1. Defining a handler interface with a method to handle requests
2. Each handler has a reference to the next handler in the chain
3. When a handler receives a request, it either handles it or passes it along
4. The chain continues until a handler processes the request or the end is reached

```
┌─────────────────────────────────────────────────┐
│         Chain of Responsibility Pattern         │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │◄── Sends request              │
│  └──────────────┘                               │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Handler Interface                │   │
│  │    + handle(request): void               │   │
│  │    + setNext(handler): Handler           │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│         ▼                                       │
│  ┌──────┐   ┌──────┐   ┌──────┐              │
│  │Handler│──▶│Handler│──▶│Handler│             │
│  │  1    │   │  2    │   │  3    │              │
│  └──────┘   └──────┘   └──────┘              │
│                                                  │
│  Request passes through chain until handled       │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Basic Chain of Responsibility

```typescript
// Handler interface
abstract class Handler {
  private nextHandler: Handler | null = null;

  setNext(handler: Handler): Handler {
    this.nextHandler = handler;
    return handler;
  }

  handle(request: any): any {
    if (this.nextHandler) {
      return this.nextHandler.handle(request);
    }

    return null;
  }
}

// Concrete handlers
class AuthHandler extends Handler {
  handle(request: any): any {
    console.log('AuthHandler: Checking authentication...');

    if (!request.token) {
      console.log('AuthHandler: No token provided');
      return { error: 'Unauthorized', status: 401 };
    }

    console.log('AuthHandler: Token validated');
    return super.handle(request);
  }
}

class ValidationHandler extends Handler {
  handle(request: any): any {
    console.log('ValidationHandler: Validating request...');

    if (!request.body || Object.keys(request.body).length === 0) {
      console.log('ValidationHandler: Invalid request body');
      return { error: 'Bad Request', status: 400 };
    }

    console.log('ValidationHandler: Request valid');
    return super.handle(request);
  }
}

class RateLimitHandler extends Handler {
  private requests: Map<string, number[]> = new Map();
  private limit: number;
  private windowMs: number;

  constructor(limit: number = 100, windowMs: number = 60000) {
    super();
    this.limit = limit;
    this.windowMs = windowMs;
  }

  handle(request: any): any {
    console.log('RateLimitHandler: Checking rate limit...');

    const ip = request.ip || 'unknown';
    const now = Date.now();

    const requests = this.requests.get(ip) || [];
    const recentRequests = requests.filter(time => now - time < this.windowMs);

    if (recentRequests.length >= this.limit) {
      console.log('RateLimitHandler: Rate limit exceeded');
      return { error: 'Too Many Requests', status: 429 };
    }

    recentRequests.push(now);
    this.requests.set(ip, recentRequests);

    console.log('RateLimitHandler: Rate limit OK');
    return super.handle(request);
  }
}

class FinalHandler extends Handler {
  handle(request: any): any {
    console.log('FinalHandler: Processing request...');
    return { success: true, data: 'Response data', status: 200 };
  }
}

// Client code
function processRequest(request: any): any {
  const auth = new AuthHandler();
  const validation = new ValidationHandler();
  const rateLimit = new RateLimitHandler();
  const final = new FinalHandler();

  auth.setNext(validation).setNext(rateLimit).setNext(final);

  return auth.handle(request);
}

// Usage
console.log('Valid request:');
const result1 = processRequest({
  token: 'valid_token',
  body: { name: 'John' },
  ip: '127.0.0.1'
});
console.log('Result:', result1);

console.log('\nMissing token:');
const result2 = processRequest({
  body: { name: 'John' },
  ip: '127.0.0.1'
});
console.log('Result:', result2);
```

### Express-style Middleware

```typescript
// Types
interface Request {
  url: string;
  method: string;
  headers: Record<string, string>;
  body: any;
  user?: any;
  startTime?: number;
}

interface Response {
  status: number;
  body: any;
  headers: Record<string, string>;
}

type NextFunction = () => Promise<void>;
type Middleware = (req: Request, res: Response, next: NextFunction) => Promise<void>;

// Middleware chain
class MiddlewareChain {
  private middlewares: Middleware[] = [];
  private finalHandler: (req: Request, res: Response) => Promise<Response>;

  constructor(finalHandler: (req: Request, res: Response) => Promise<Response>) {
    this.finalHandler = finalHandler;
  }

  use(middleware: Middleware): this {
    this.middlewares.push(middleware);
    return this;
  }

  async execute(req: Request, res: Response): Promise<Response> {
    let index = 0;

    const next = async (): Promise<void> => {
      if (index < this.middlewares.length) {
        const middleware = this.middlewares[index++];
        await middleware(req, res, next);
      } else {
        await this.finalHandler(req, res);
      }
    };

    await next();
    return res;
  }
}

// Concrete middlewares
const loggingMiddleware: Middleware = async (req, res, next) => {
  req.startTime = Date.now();
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  await next();
  const duration = Date.now() - (req.startTime || 0);
  console.log(`Response: ${res.status} (${duration}ms)`);
};

const authMiddleware: Middleware = async (req, res, next) => {
  const token = req.headers['Authorization'];

  if (!token) {
    res.status = 401;
    res.body = { error: 'Unauthorized' };
    return;
  }

  // Simulate token validation
  req.user = { id: '1', name: 'John' };
  await next();
};

const corsMiddleware: Middleware = async (req, res, next) => {
  res.headers['Access-Control-Allow-Origin'] = '*';
  res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE';
  res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';
  await next();
};

const bodyParserMiddleware: Middleware = async (req, res, next) => {
  if (req.method === 'POST' && req.body) {
    console.log('Parsing request body...');
  }
  await next();
};

// Usage
const chain = new MiddlewareChain(async (req, res) => {
  res.status = 200;
  res.body = { message: 'Hello World' };
  return res;
});

chain
  .use(corsMiddleware)
  .use(loggingMiddleware)
  .use(bodyParserMiddleware)
  .use(authMiddleware);

const response = await chain.execute(
  {
    url: '/api/users',
    method: 'POST',
    headers: { 'Authorization': 'Bearer token123', 'Content-Type': 'application/json' },
    body: { name: 'John' }
  },
  { status: 0, body: null, headers: {} }
);

console.log('Response:', response);
```

### Discount Calculator Chain

```typescript
// Handler interface
interface DiscountHandler {
  setNext(handler: DiscountHandler): DiscountHandler;
  calculate(amount: number, context: any): number;
}

// Base handler
abstract class BaseDiscountHandler implements DiscountHandler {
  private nextHandler: DiscountHandler | null = null;

  setNext(handler: DiscountHandler): DiscountHandler {
    this.nextHandler = handler;
    return handler;
  }

  calculate(amount: number, context: any): number {
    let discount = this.applyDiscount(amount, context);

    if (this.nextHandler) {
      const remainingDiscount = this.nextHandler.calculate(amount - discount, context);
      discount += remainingDiscount;
    }

    return discount;
  }

  protected abstract applyDiscount(amount: number, context: any): number;
}

// Concrete handlers
class VIPDiscount extends BaseDiscountHandler {
  protected applyDiscount(amount: number, context: any): number {
    if (context.isVIP) {
      console.log('VIP Discount: 20%');
      return amount * 0.2;
    }
    return 0;
  }
}

class SeasonalDiscount extends BaseDiscountHandler {
  protected applyDiscount(amount: number, context: any): number {
    if (context.isSeasonalSale) {
      console.log('Seasonal Discount: 15%');
      return amount * 0.15;
    }
    return 0;
  }
}

class CouponDiscount extends BaseDiscountHandler {
  protected applyDiscount(amount: number, context: any): number {
    if (context.couponCode) {
      const discounts: Record<string, number> = {
        'SAVE10': 0.1,
        'SAVE20': 0.2,
        'FLAT50': 50
      };

      const discountRate = discounts[context.couponCode] || 0;
      console.log(`Coupon Discount: ${discountRate * 100}%`);
      return amount * discountRate;
    }
    return 0;
  }
}

class FirstTimeBuyerDiscount extends BaseDiscountHandler {
  protected applyDiscount(amount: number, context: any): number {
    if (context.isFirstTimeBuyer) {
      console.log('First Time Buyer Discount: 10%');
      return amount * 0.1;
    }
    return 0;
  }
}

// Client code
function calculateDiscount(amount: number, context: any): number {
  const vip = new VIPDiscount();
  const seasonal = new SeasonalDiscount();
  const coupon = new CouponDiscount();
  const firstTime = new FirstTimeBuyerDiscount();

  vip.setNext(seasonal).setNext(coupon).setNext(firstTime);

  return vip.calculate(amount, context);
}

// Usage
const amount = 100;
const context = {
  isVIP: true,
  isSeasonalSale: true,
  couponCode: 'SAVE10',
  isFirstTimeBuyer: false
};

const discount = calculateDiscount(amount, context);
console.log(`\nTotal discount: $${discount}`);
console.log(`Final price: $${amount - discount}`);
```

### Validation Chain

```typescript
// Handler interface
interface ValidationHandler {
  setNext(handler: ValidationHandler): ValidationHandler;
  validate(data: any): { isValid: boolean; errors: string[] };
}

// Base handler
abstract class BaseValidationHandler implements ValidationHandler {
  private nextHandler: ValidationHandler | null = null;

  setNext(handler: ValidationHandler): ValidationHandler {
    this.nextHandler = handler;
    return handler;
  }

  validate(data: any): { isValid: boolean; errors: string[] } {
    const result = this.validateData(data);

    if (this.nextHandler) {
      const nextResult = this.nextHandler.validate(data);
      return {
        isValid: result.isValid && nextResult.isValid,
        errors: [...result.errors, ...nextResult.errors]
      };
    }

    return result;
  }

  protected abstract validateData(data: any): { isValid: boolean; errors: string[] };
}

// Concrete handlers
class RequiredFieldsValidation extends BaseValidationHandler {
  private requiredFields: string[];

  constructor(requiredFields: string[]) {
    super();
    this.requiredFields = requiredFields;
  }

  protected validateData(data: any): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    for (const field of this.requiredFields) {
      if (!data[field]) {
        errors.push(`${field} is required`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }
}

class EmailValidation extends BaseValidationHandler {
  protected validateData(data: any): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (data.email && !emailRegex.test(data.email)) {
      errors.push('Invalid email format');
    }

    return { isValid: errors.length === 0, errors };
  }
}

class PasswordValidation extends BaseValidationHandler {
  private minLength: number;

  constructor(minLength: number = 8) {
    super();
    this.minLength = minLength;
  }

  protected validateData(data: any): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (data.password) {
      if (data.password.length < this.minLength) {
        errors.push(`Password must be at least ${this.minLength} characters`);
      }

      if (!/[A-Z]/.test(data.password)) {
        errors.push('Password must contain at least one uppercase letter');
      }

      if (!/[0-9]/.test(data.password)) {
        errors.push('Password must contain at least one number');
      }
    }

    return { isValid: errors.length === 0, errors };
  }
}

class AgeValidation extends BaseValidationHandler {
  private minAge: number;
  private maxAge: number;

  constructor(minAge: number = 18, maxAge: number = 120) {
    super();
    this.minAge = minAge;
    this.maxAge = maxAge;
  }

  protected validateData(data: any): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (data.age !== undefined) {
      if (data.age < this.minAge || data.age > this.maxAge) {
        errors.push(`Age must be between ${this.minAge} and ${this.maxAge}`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }
}

// Client code
function validateUser(data: any): { isValid: boolean; errors: string[] } {
  const required = new RequiredFieldsValidation(['name', 'email', 'password']);
  const email = new EmailValidation();
  const password = new PasswordValidation();
  const age = new AgeValidation();

  required.setNext(email).setNext(password).setNext(age);

  return required.validate(data);
}

// Usage
const validUser = {
  name: 'John',
  email: 'john@example.com',
  password: 'Password123',
  age: 25
};

const invalidUser = {
  name: 'John',
  email: 'invalid-email',
  password: 'weak',
  age: 15
};

console.log('Valid user:');
console.log(validateUser(validUser));

console.log('\nInvalid user:');
console.log(validateUser(invalidUser));
```

## Real-World Use Cases

### 1. Express.js-style Middleware

```typescript
// Real-world Express-like middleware implementation
type AppRequest = {
  url: string;
  method: string;
  headers: Record<string, string>;
  body: any;
  params: Record<string, string>;
  query: Record<string, string>;
  user?: any;
};

type AppResponse = {
  status: number;
  body: any;
  headers: Record<string, string>;
};

type AppNext = () => Promise<void>;
type AppMiddleware = (req: AppRequest, res: AppResponse, next: AppNext) => Promise<void>;

class App {
  private middlewares: AppMiddleware[] = [];
  private routes: Map<string, Map<string, AppMiddleware[]>> = new Map();

  use(middleware: AppMiddleware): this {
    this.middlewares.push(middleware);
    return this;
  }

  get(path: string, ...middlewares: AppMiddleware[]): this {
    this.addRoute('GET', path, middlewares);
    return this;
  }

  post(path: string, ...middlewares: AppMiddleware[]): this {
    this.addRoute('POST', path, middlewares);
    return this;
  }

  private addRoute(method: string, path: string, middlewares: AppMiddleware[]): void {
    if (!this.routes.has(method)) {
      this.routes.set(method, new Map());
    }
    this.routes.get(method)!.set(path, middlewares);
  }

  async handleRequest(req: AppRequest, res: AppResponse): Promise<AppResponse> {
    // Apply global middlewares
    for (const middleware of this.middlewares) {
      await this.executeMiddleware(middleware, req, res);
    }

    // Apply route-specific middlewares
    const routeMiddlewares = this.routes.get(req.method)?.get(req.url) || [];
    for (const middleware of routeMiddlewares) {
      await this.executeMiddleware(middleware, req, res);
    }

    return res;
  }

  private async executeMiddleware(middleware: AppMiddleware, req: AppRequest, res: AppResponse): Promise<void> {
    let nextCalled = false;
    const next = async () => { nextCalled = true; };

    await middleware(req, res, next);

    if (!nextCalled) {
      throw new Error('Next not called in middleware');
    }
  }
}

// Usage
const app = new App();

// Global middleware
app.use(async (req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  await next();
});

// Route middleware
app.get('/api/users',
  async (req, res, next) => {
    console.log('Auth middleware');
    req.user = { id: '1' };
    await next();
  },
  async (req, res, next) => {
    console.log('Handler');
    res.body = { users: [] };
    await next();
  }
);

const response = await app.handleRequest(
  { url: '/api/users', method: 'GET', headers: {}, body: null, params: {}, query: {} },
  { status: 200, body: null, headers: {} }
);
```

### 2. Error Handling Chain

```typescript
// Error types
class AppError extends Error {
  constructor(message: string, public statusCode: number, public code: string) {
    super(message);
  }
}

class ValidationError extends AppError {
  constructor(message: string, public field: string) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND');
  }
}

class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

// Error handler interface
interface ErrorHandler {
  setNext(handler: ErrorHandler): ErrorHandler;
  handle(error: Error): { status: number; body: any } | null;
}

// Base error handler
abstract class BaseErrorHandler implements ErrorHandler {
  private nextHandler: ErrorHandler | null = null;

  setNext(handler: ErrorHandler): ErrorHandler {
    this.nextHandler = handler;
    return handler;
  }

  handle(error: Error): { status: number; body: any } | null {
    if (this.canHandle(error)) {
      return this.processError(error);
    }

    if (this.nextHandler) {
      return this.nextHandler.handle(error);
    }

    return null;
  }

  protected abstract canHandle(error: Error): boolean;
  protected abstract processError(error: Error): { status: number; body: any };
}

// Concrete error handlers
class ValidationErrorHandler extends BaseErrorHandler {
  protected canHandle(error: Error): boolean {
    return error instanceof ValidationError;
  }

  protected processError(error: Error): { status: number; body: any } {
    const validationError = error as ValidationError;
    return {
      status: 400,
      body: {
        error: 'Validation Error',
        message: validationError.message,
        field: validationError.field
      }
    };
  }
}

class NotFoundErrorHandler extends BaseErrorHandler {
  protected canHandle(error: Error): boolean {
    return error instanceof NotFoundError;
  }

  protected processError(error: Error): { status: number; body: any } {
    return {
      status: 404,
      body: {
        error: 'Not Found',
        message: error.message
      }
    };
  }
}

class UnauthorizedErrorHandler extends BaseErrorHandler {
  protected canHandle(error: Error): boolean {
    return error instanceof UnauthorizedError;
  }

  protected processError(error: Error): { status: number; body: any } {
    return {
      status: 401,
      body: {
        error: 'Unauthorized',
        message: error.message
      }
    };
  }
}

class GenericErrorHandler extends BaseErrorHandler {
  protected canHandle(error: Error): boolean {
    return true; // Catches all remaining errors
  }

  protected processError(error: Error): { status: number; body: any } {
    console.error('Unhandled error:', error);
    return {
      status: 500,
      body: {
        error: 'Internal Server Error',
        message: 'An unexpected error occurred'
      }
    };
  }
}

// Client code
function handleError(error: Error): { status: number; body: any } {
  const validation = new ValidationErrorHandler();
  const notFound = new NotFoundErrorHandler();
  const unauthorized = new UnauthorizedErrorHandler();
  const generic = new GenericErrorHandler();

  validation.setNext(notFound).setNext(unauthorized).setNext(generic);

  return validation.handle(error)!;
}

// Usage
console.log('Validation error:');
console.log(handleError(new ValidationError('Name is required', 'name')));

console.log('\nNot found error:');
console.log(handleError(new NotFoundError('User')));

console.log('\nUnknown error:');
console.log(handleError(new Error('Something went wrong')));
```

### 3. Request Processing Pipeline

```typescript
// Pipeline stages
interface PipelineStage {
  setNext(stage: PipelineStage): PipelineStage;
  process(data: any): Promise<any>;
}

// Base stage
abstract class BasePipelineStage implements PipelineStage {
  private nextStage: PipelineStage | null = null;

  setNext(stage: PipelineStage): PipelineStage {
    this.nextStage = stage;
    return stage;
  }

  async process(data: any): Promise<any> {
    const processedData = await this.processData(data);

    if (this.nextStage) {
      return this.nextStage.process(processedData);
    }

    return processedData;
  }

  protected abstract processData(data: any): Promise<any>;
}

// Concrete stages
class SanitizeStage extends BasePipelineStage {
  protected async processData(data: any): Promise<any> {
    console.log('SanitizeStage: Sanitizing data...');

    // Remove HTML tags, trim strings, etc.
    const sanitized = { ...data };

    if (typeof sanitized.name === 'string') {
      sanitized.name = sanitized.name.replace(/<[^>]*>/g, '').trim();
    }

    return sanitized;
  }
}

class ValidateStage extends BasePipelineStage {
  protected async processData(data: any): Promise<any> {
    console.log('ValidateStage: Validating data...');

    if (!data.name || data.name.length < 2) {
      throw new Error('Name must be at least 2 characters');
    }

    return data;
  }
}

class TransformStage extends BasePipelineStage {
  protected async processData(data: any): Promise<any> {
    console.log('TransformStage: Transforming data...');

    return {
      ...data,
      name: data.name.toUpperCase(),
      processedAt: new Date().toISOString()
    };
  }
}

class PersistStage extends BasePipelineStage {
  protected async processData(data: any): Promise<any> {
    console.log('PersistStage: Persisting data...');

    // Simulate database save
    return {
      ...data,
      id: Math.random().toString(36).substr(2, 9),
      saved: true
    };
  }
}

// Client code
async function processData(data: any): Promise<any> {
  const sanitize = new SanitizeStage();
  const validate = new ValidateStage();
  const transform = new TransformStage();
  const persist = new PersistStage();

  sanitize.setNext(validate).setNext(transform).setNext(persist);

  return sanitize.process(data);
}

// Usage
const inputData = { name: '<script>alert("xss")</script>John' };

try {
  const result = await processData(inputData);
  console.log('\nFinal result:', result);
} catch (error) {
  console.error('Pipeline error:', error.message);
}
```

## Common Mistakes

### 1. Chain Too Long

```typescript
// ❌ BAD - Chain with too many handlers
const chain = new Handler1();
chain
  .setNext(new Handler2())
  .setNext(new Handler3())
  .setNext(new Handler4())
  .setNext(new Handler5())
  .setNext(new Handler6())
  .setNext(new Handler7());
// Hard to debug and maintain
```

### 2. Not Handling End of Chain

```typescript
// ❌ BAD - No final handler
class Handler {
  handle(request: any): any {
    if (this.nextHandler) {
      return this.nextHandler.handle(request);
    }
    // Request falls through without response
    return null;
  }
}
```

### 3. Circular Chain

```typescript
// ❌ BAD - Circular reference
const handler1 = new Handler();
const handler2 = new Handler();
handler1.setNext(handler2);
handler2.setNext(handler1); // Infinite loop
```

### 4. Handler with Too Much Logic

```typescript
// ❌ BAD - Handler doing too much
class BadHandler extends BaseHandler {
  protected handleRequest(request: any): any {
    // Also validates, transforms, and persists
    // Should be split into multiple handlers
  }
}
```

## Best Practices

### 1. Keep Handlers Focused

```typescript
// ✅ GOOD - Single responsibility
class AuthHandler extends BaseHandler {
  // Only handles authentication
}
```

### 2. Handle End of Chain

```typescript
// ✅ GOOD - Final handler
class FinalHandler extends BaseHandler {
  handle(request: any): any {
    return { status: 404, message: 'Not handled' };
  }
}
```

### 3. Use Builder Pattern

```typescript
// ✅ GOOD - Fluent interface
class ChainBuilder {
  static build(...handlers: Handler[]): Handler {
    for (let i = 0; i < handlers.length - 1; i++) {
      handlers[i].setNext(handlers[i + 1]);
    }
    return handlers[0];
  }
}
```

### 4. Make Handlers Stateless

```typescript
// ✅ GOOD - Stateless handlers
class StatelessHandler extends BaseHandler {
  protected handleRequest(request: any): any {
    // No instance variables
  }
}
```

## Performance Considerations

1. **Chain Length**: Longer chains add overhead; consider optimizing chain length.

2. **Early Termination**: Break chain early when request is handled.

3. **Parallel Processing**: Consider parallel handlers for independent operations.

4. **Caching**: Cache handler results for repeated requests.

5. **Lazy Initialization**: Initialize handlers only when needed.

## Interview Questions

### Beginner

1. **What is the Chain of Responsibility pattern?**
   - A behavioral pattern that passes requests along a chain of handlers.

2. **When would you use Chain of Responsibility?**
   - For middleware, validation, logging, and request processing pipelines.

3. **What's the difference between Chain of Responsibility and Decorator?**
   - Chain passes request along; Decorator adds behavior to same object.

4. **How do you implement Chain of Responsibility in TypeScript?**
   - Create handlers with setNext method and handle method.

5. **What are the benefits of Chain of Responsibility?**
   - Loose coupling, flexibility, and single responsibility.

### Intermediate

6. **How do you handle end of chain?**
   - Use a final handler that processes unhandled requests.

7. **Can handlers modify the request?**
   - Yes, handlers can modify request before passing it along.

8. **How do you test Chain of Responsibility?**
   - Test each handler independently, test chain composition.

9. **What's the relationship between Chain and Pipeline?**
   - Chain is a type of pipeline; pipeline can have parallel branches.

10. **How do you handle errors in chain?**
    - Use try-catch, error handlers, or error middleware.

### Senior

11. **How does Chain of Responsibility affect scalability?**
    - Chains are lightweight; handlers can be distributed.

12. **What are the SOLID violations with Chain?**
    - Usually follows SOLID; watch for handlers violating Single Responsibility.

13. **How do you handle Chain in microservices?**
    - Use chains for request processing, validation, and transformation.

14. **What are the memory implications of Chain?**
    - Chains are usually stateless; handlers consume minimal memory.

15. **How do you refactor Chain code?**
    - Extract common logic, use composition, and apply SOLID principles.

### FAANG-style

16. **Design a Chain for a distributed system.**
    - Consider network transparency, fault tolerance, and load balancing.

17. **How would you implement Chain for cloud-native applications?**
    - Consider serverless functions, middleware, and function composition.

18. **What are the implications of Chain in event-driven architectures?**
    - Use chains for event processing, routing, and transformation.

19. **How do you handle Chain in real-time systems?**
    - Consider latency, throughput, and resource management.

20. **Design a Chain that supports parallel processing.**
    - Consider parallel handlers, fork-join, and result aggregation.

### Follow-ups

21. **Can Chain of Responsibility be combined with other patterns?**
    - Yes, commonly with Decorator, Pipeline, and Middleware patterns.

22. **How do you handle Chain in testing frameworks?**
    - Use dependency injection, create test handlers, and mock implementations.

23. **What are the memory implications of Chain pattern?**
    - Chains are usually stateless; handlers consume minimal memory.

24. **How do you handle Chain in serverless environments?**
    - Consider stateless handlers, function composition, and cold starts.

25. **What's the impact of Chain on code maintainability?**
    - Improves maintainability by enabling flexible request processing.

## Summary

The Chain of Responsibility pattern is essential for processing pipelines and middleware. It enables flexible request handling, loose coupling, and single responsibility. Use it for validation, authentication, logging, and any scenario where requests need to pass through multiple handlers.

## Cheat Sheet

```
┌─────────────────────────────────────────────┐
│       CHAIN OF RESPONSIBILITY PATTERN       │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Request processing pipelines              │
│ • Middleware chains                         │
│ • Validation chains                         │
│ • Logging and monitoring                    │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple request handling                   │
│ • Chain too long                            │
│ • Performance is critical                   │
│ • Handlers with too much logic              │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Handler interface                         │
│ • Chain of handlers                         │
│ • Request passes through chain              │
│ • Handler decides to process or pass        │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Chain too long                            │
│ • Circular chains                           │
│ • Not handling end of chain                 │
│ • Handlers with too much logic              │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Decorator (adds behavior)                 │
│ • Pipeline (processing stages)              │
│ • Middleware (request processing)           │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Chain of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility)
- [Middleware Pattern](https://expressjs.com/en/guide/using-middleware.html)
