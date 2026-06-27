# Decorator Pattern

## Definition

The Decorator pattern is a structural design pattern that allows you to attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors. It provides an alternative to subclassing for extending functionality.

The pattern is particularly useful when you need to add responsibilities to objects dynamically, when extending functionality through subclassing is impractical, or when you want to combine multiple behaviors.

## Why Do We Need It?

Without the Decorator pattern, extending object behavior leads to:

1. **Class explosion**: Many subclasses for each combination of behaviors
2. **Rigid hierarchy**: Static inheritance makes changes difficult
3. **Code duplication**: Common behaviors repeated across subclasses
4. **Violation of Open/Closed Principle**: Modifying existing classes for new behavior

## How It Works

The Decorator pattern works by:

1. Defining a common interface for components and decorators
2. Creating concrete components that implement the base behavior
3. Creating decorators that wrap components and add behavior
4. Decorators delegate to the wrapped component and add their behavior

```
┌─────────────────────────────────────────────────┐
│              Decorator Pattern                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │         Component Interface              │   │
│  │    + operation(): string                 │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┐                                 │
│    ▼         ▼                                 │
│ ┌──────┐ ┌──────────────┐                     │
│ │Comp  │ │   Decorator   │                     │
│ │      │ │ + operation() │                     │
│ └──────┘ │ - wrapped: Component │              │
│          └──────────────┘                     │
│                │                               │
│                ▼                               │
│  ┌──────────────────────────────────────────┐  │
│  │         Concrete Decorators              │  │
│  │    + operation(): string                 │  │
│  │    - wrapped: Component                  │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Basic Decorator Pattern

```typescript
// Component interface
interface DataSource {
  writeData(data: string): void;
  readData(): string;
}

// Concrete component
class FileDataSource implements DataSource {
  private filename: string;
  private data: string = '';
  
  constructor(filename: string) {
    this.filename = filename;
  }
  
  writeData(data: string): void {
    console.log(`Writing data to file: ${this.filename}`);
    this.data = data;
  }
  
  readData(): string {
    console.log(`Reading data from file: ${this.filename}`);
    return this.data;
  }
}

// Base decorator
abstract class DataSourceDecorator implements DataSource {
  protected wrapped: DataSource;
  
  constructor(source: DataSource) {
    this.wrapped = source;
  }
  
  writeData(data: string): void {
    this.wrapped.writeData(data);
  }
  
  readData(): string {
    return this.wrapped.readData();
  }
}

// Concrete decorators
class EncryptionDecorator extends DataSourceDecorator {
  writeData(data: string): void {
    const encrypted = this.encrypt(data);
    console.log('Encrypting data...');
    super.writeData(encrypted);
  }
  
  readData(): string {
    const data = super.readData();
    console.log('Decrypting data...');
    return this.decrypt(data);
  }
  
  private encrypt(data: string): string {
    // Simple encryption simulation
    return Buffer.from(data).toString('base64');
  }
  
  private decrypt(data: string): string {
    // Simple decryption simulation
    return Buffer.from(data, 'base64').toString();
  }
}

class CompressionDecorator extends DataSourceDecorator {
  writeData(data: string): void {
    const compressed = this.compress(data);
    console.log('Compressing data...');
    super.writeData(compressed);
  }
  
  readData(): string {
    const data = super.readData();
    console.log('Decompressing data...');
    return this.decompress(data);
  }
  
  private compress(data: string): string {
    // Simple compression simulation
    return `[compressed]${data}[/compressed]`;
  }
  
  private decompress(data: string): string {
    // Simple decompression simulation
    return data.replace(/\[compressed\]|\[\/compressed\]/g, '');
  }
}

// Client code
function processFile(source: DataSource): void {
  source.writeData('Important data');
  const data = source.readData();
  console.log(`Processed data: ${data}`);
}

// Usage
console.log('Simple file:');
const simpleFile = new FileDataSource('data.txt');
processFile(simpleFile);

console.log('\nEncrypted file:');
const encryptedFile = new EncryptionDecorator(new FileDataSource('data.txt'));
processFile(encryptedFile);

console.log('\nCompressed file:');
const compressedFile = new CompressionDecorator(new FileDataSource('data.txt'));
processFile(compressedFile);

console.log('\nEncrypted and compressed file:');
const decoratedFile = new CompressionDecorator(
  new EncryptionDecorator(new FileDataSource('data.txt'))
);
processFile(decoratedFile);
```

### HTTP Middleware Decorator

```typescript
// Component interface
interface RequestHandler {
  handle(request: Request): Promise<Response>;
}

interface Request {
  url: string;
  method: string;
  headers: Record<string, string>;
  body: any;
  user?: any;
}

interface Response {
  status: number;
  body: any;
  headers: Record<string, string>;
}

// Concrete component
class BasicHandler implements RequestHandler {
  async handle(request: Request): Promise<Response> {
    console.log('Handling request...');
    return { status: 200, body: { message: 'OK' }, headers: {} };
  }
}

// Base decorator
abstract class HandlerDecorator implements RequestHandler {
  protected wrapped: RequestHandler;
  
  constructor(handler: RequestHandler) {
    this.wrapped = handler;
  }
  
  async handle(request: Request): Promise<Response> {
    return this.wrapped.handle(request);
  }
}

// Concrete decorators
class LoggingHandler extends HandlerDecorator {
  async handle(request: Request): Promise<Response> {
    console.log(`[${new Date().toISOString()}] ${request.method} ${request.url}`);
    const start = Date.now();
    
    const response = await super.handle(request);
    
    const duration = Date.now() - start;
    console.log(`Response: ${response.status} (${duration}ms)`);
    
    return response;
  }
}

class AuthenticationHandler extends HandlerDecorator {
  async handle(request: Request): Promise<Response> {
    const token = request.headers['Authorization'];
    
    if (!token) {
      return { status: 401, body: { error: 'Unauthorized' }, headers: {} };
    }
    
    // Simulate token validation
    request.user = { id: '1', name: 'John' };
    
    return super.handle(request);
  }
}

class RateLimitHandler extends HandlerDecorator {
  private requests: Map<string, number[]> = new Map();
  private limit: number;
  private windowMs: number;
  
  constructor(handler: RequestHandler, limit: number = 100, windowMs: number = 60000) {
    super(handler);
    this.limit = limit;
    this.windowMs = windowMs;
  }
  
  async handle(request: Request): Promise<Response> {
    const ip = request.headers['X-Forwarded-For'] || 'unknown';
    const now = Date.now();
    
    const requests = this.requests.get(ip) || [];
    const recentRequests = requests.filter(time => now - time < this.windowMs);
    
    if (recentRequests.length >= this.limit) {
      return { status: 429, body: { error: 'Too Many Requests' }, headers: {} };
    }
    
    recentRequests.push(now);
    this.requests.set(ip, recentRequests);
    
    return super.handle(request);
  }
}

class CORSHandler extends HandlerDecorator {
  async handle(request: Request): Promise<Response> {
    const response = await super.handle(request);
    
    response.headers['Access-Control-Allow-Origin'] = '*';
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE';
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';
    
    return response;
  }
}

// Client code
class Server {
  private handler: RequestHandler;
  
  constructor() {
    // Build middleware chain
    this.handler = new CORSHandler(
      new RateLimitHandler(
        new AuthenticationHandler(
          new LoggingHandler(
            new BasicHandler()
          )
        )
      )
    );
  }
  
  async handleRequest(request: Request): Promise<Response> {
    return this.handler.handle(request);
  }
}

// Usage
const server = new Server();
const response = await server.handleRequest({
  url: '/api/users',
  method: 'GET',
  headers: { 'Authorization': 'Bearer token123' },
  body: null
});

console.log(response);
```

### Notification Decorator

```typescript
// Component interface
interface Notification {
  send(message: string): Promise<boolean>;
  getChannel(): string;
}

// Concrete component
class BasicNotification implements Notification {
  async send(message: string): Promise<boolean> {
    console.log(`Sending notification: ${message}`);
    return true;
  }
  
  getChannel(): string {
    return 'basic';
  }
}

// Base decorator
abstract class NotificationDecorator implements Notification {
  protected wrapped: Notification;
  
  constructor(notification: Notification) {
    this.wrapped = notification;
  }
  
  async send(message: string): Promise<boolean> {
    return this.wrapped.send(message);
  }
  
  getChannel(): string {
    return this.wrapped.getChannel();
  }
}

// Concrete decorators
class FormattedNotification extends NotificationDecorator {
  async send(message: string): Promise<boolean> {
    const formatted = this.formatMessage(message);
    console.log('Formatting message...');
    return super.send(formatted);
  }
  
  private formatMessage(message: string): string {
    return `[${new Date().toISOString()}] ${message.toUpperCase()}`;
  }
}

class RetryNotification extends NotificationDecorator {
  private maxRetries: number;
  private delay: number;
  
  constructor(notification: Notification, maxRetries: number = 3, delay: number = 1000) {
    super(notification);
    this.maxRetries = maxRetries;
    this.delay = delay;
  }
  
  async send(message: string): Promise<boolean> {
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        console.log(`Attempt ${attempt}/${this.maxRetries}...`);
        const result = await super.send(message);
        if (result) return true;
      } catch (error) {
        console.log(`Attempt ${attempt} failed: ${error}`);
      }
      
      if (attempt < this.maxRetries) {
        await this.sleep(this.delay);
      }
    }
    
    return false;
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

class FilteredNotification extends NotificationDecorator {
  private filter: (message: string) => boolean;
  
  constructor(notification: Notification, filter: (message: string) => boolean) {
    super(notification);
    this.filter = filter;
  }
  
  async send(message: string): Promise<boolean> {
    if (!this.filter(message)) {
      console.log('Message filtered out');
      return false;
    }
    
    return super.send(message);
  }
}

class QueuedNotification extends NotificationDecorator {
  private queue: string[] = [];
  private processing: boolean = false;
  
  async send(message: string): Promise<boolean> {
    this.queue.push(message);
    console.log(`Message queued: ${message}`);
    
    if (!this.processing) {
      this.processQueue();
    }
    
    return true;
  }
  
  private async processQueue(): Promise<void> {
    this.processing = true;
    
    while (this.queue.length > 0) {
      const message = this.queue.shift()!;
      await super.send(message);
    }
    
    this.processing = false;
  }
}

// Client code
class NotificationService {
  private notification: Notification;
  
  constructor() {
    // Build decorator chain
    this.notification = new QueuedNotification(
      new RetryNotification(
        new FormattedNotification(
          new BasicNotification()
        )
      )
    );
  }
  
  async notify(message: string): Promise<boolean> {
    return this.notification.send(message);
  }
}

// Usage
const service = new NotificationService();
await service.notify('Hello World!');
```

### TypeScript Decorators (Language Feature)

```typescript
// Method decorator
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;
  
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with args:`, args);
    const result = originalMethod.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };
  
  return descriptor;
}

// Parameter decorator
function Validate(target: any, propertyKey: string, parameterIndex: number) {
  const existingRequiredParameters: number[] = Reflect.getMetadata('required', target, propertyKey) || [];
  existingRequiredParameters.push(parameterIndex);
  Reflect.defineMetadata('required', existingRequiredParameters, target, propertyKey);
}

// Class decorator
function Sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

// Property decorator
function ReadOnly(target: any, propertyKey: string) {
  Object.defineProperty(target, propertyKey, {
    writable: false,
    configurable: false
  });
}

// Usage
@Sealed
class UserService {
  @ReadOnly
  private version: string = '1.0';
  
  @Log
  getUser(@Validate id: string): any {
    return { id, name: 'John' };
  }
  
  @Log
  createUser(data: any): any {
    return { id: '1', ...data };
  }
}
```

## Real-World Use Cases

### 1. Stream Decorators (Node.js Style)

```typescript
// Component interface
interface ReadableStream {
  read(): string;
  getLength(): number;
}

// Concrete component
class StringStream implements ReadableStream {
  private data: string;
  
  constructor(data: string) {
    this.data = data;
  }
  
  read(): string {
    return this.data;
  }
  
  getLength(): number {
    return this.data.length;
  }
}

// Base decorator
abstract class StreamDecorator implements ReadableStream {
  protected wrapped: ReadableStream;
  
  constructor(stream: ReadableStream) {
    this.wrapped = stream;
  }
  
  read(): string {
    return this.wrapped.read();
  }
  
  getLength(): number {
    return this.wrapped.getLength();
  }
}

// Concrete decorators
class UpperCaseStream extends StreamDecorator {
  read(): string {
    return super.read().toUpperCase();
  }
}

class TruncatedStream extends StreamDecorator {
  private maxLength: number;
  
  constructor(stream: ReadableStream, maxLength: number) {
    super(stream);
    this.maxLength = maxLength;
  }
  
  read(): string {
    const data = super.read();
    return data.substring(0, this.maxLength);
  }
  
  getLength(): number {
    return Math.min(super.getLength(), this.maxLength);
  }
}

class ReversedStream extends StreamDecorator {
  read(): string {
    return super.read().split('').reverse().join('');
  }
}

class EncodedStream extends StreamDecorator {
  read(): string {
    return Buffer.from(super.read()).toString('base64');
  }
}

// Client code
const stream = new EncodedStream(
  new ReversedStream(
    new UpperCaseStream(
      new TruncatedStream(
        new StringStream('Hello, World!'),
        10
      )
    )
  )
);

console.log(stream.read()); // SGVsbG8sIFdv
console.log(stream.getLength()); // 10
```

### 2. Data Processing Decorator

```typescript
// Component interface
interface DataProcessor {
  process(data: any): any;
}

// Concrete component
class JSONProcessor implements DataProcessor {
  process(data: any): any {
    return JSON.parse(data);
  }
}

// Base decorator
abstract class ProcessorDecorator implements DataProcessor {
  protected wrapped: DataProcessor;
  
  constructor(processor: DataProcessor) {
    this.wrapped = processor;
  }
  
  process(data: any): any {
    return this.wrapped.process(data);
  }
}

// Concrete decorators
class ValidationProcessor extends ProcessorDecorator {
  private schema: any;
  
  constructor(processor: DataProcessor, schema: any) {
    super(processor);
    this.schema = schema;
  }
  
  process(data: any): any {
    const result = super.process(data);
    
    // Validate against schema
    if (!this.validate(result)) {
      throw new Error('Validation failed');
    }
    
    return result;
  }
  
  private validate(data: any): boolean {
    // Simple validation
    return true;
  }
}

class TransformationProcessor extends ProcessorDecorator {
  private transform: (data: any) => any;
  
  constructor(processor: DataProcessor, transform: (data: any) => any) {
    super(processor);
    this.transform = transform;
  }
  
  process(data: any): any {
    const result = super.process(data);
    return this.transform(result);
  }
}

class CachingProcessor extends ProcessorDecorator {
  private cache: Map<string, any> = new Map();
  
  process(data: any): any {
    const key = JSON.stringify(data);
    
    if (this.cache.has(key)) {
      console.log('Cache hit');
      return this.cache.get(key);
    }
    
    const result = super.process(data);
    this.cache.set(key, result);
    
    return result;
  }
}

// Client code
const processor = new CachingProcessor(
  new TransformationProcessor(
    new ValidationProcessor(
      new JSONProcessor(),
      { type: 'object' }
    ),
    (data) => ({ ...data, processed: true })
  )
);

const result = processor.process('{"name": "John"}');
console.log(result); // { name: 'John', processed: true }
```

### 3. Logging Decorator

```typescript
// Component interface
interface Logger {
  log(message: string): void;
  error(message: string): void;
  warn(message: string): void;
}

// Concrete component
class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(`[LOG] ${message}`);
  }
  
  error(message: string): void {
    console.error(`[ERROR] ${message}`);
  }
  
  warn(message: string): void {
    console.warn(`[WARN] ${message}`);
  }
}

// Base decorator
abstract class LoggerDecorator implements Logger {
  protected wrapped: Logger;
  
  constructor(logger: Logger) {
    this.wrapped = logger;
  }
  
  log(message: string): void {
    this.wrapped.log(message);
  }
  
  error(message: string): void {
    this.wrapped.error(message);
  }
  
  warn(message: string): void {
    this.wrapped.warn(message);
  }
}

// Concrete decorators
class TimestampLogger extends LoggerDecorator {
  log(message: string): void {
    super.log(`${new Date().toISOString()} ${message}`);
  }
  
  error(message: string): void {
    super.error(`${new Date().toISOString()} ${message}`);
  }
  
  warn(message: string): void {
    super.warn(`${new Date().toISOString()} ${message}`);
  }
}

class FileLogger extends LoggerDecorator {
  private logs: string[] = [];
  
  log(message: string): void {
    this.logs.push(`[LOG] ${message}`);
    super.log(message);
  }
  
  error(message: string): void {
    this.logs.push(`[ERROR] ${message}`);
    super.error(message);
  }
  
  warn(message: string): void {
    this.logs.push(`[WARN] ${message}`);
    super.warn(message);
  }
  
  getLogs(): string[] {
    return [...this.logs];
  }
}

class FilteredLogger extends LoggerDecorator {
  private filter: (message: string) => boolean;
  
  constructor(logger: Logger, filter: (message: string) => boolean) {
    super(logger);
    this.filter = filter;
  }
  
  log(message: string): void {
    if (this.filter(message)) {
      super.log(message);
    }
  }
  
  error(message: string): void {
    if (this.filter(message)) {
      super.error(message);
    }
  }
  
  warn(message: string): void {
    if (this.filter(message)) {
      super.warn(message);
    }
  }
}

// Client code
const logger = new TimestampLogger(
  new FileLogger(
    new FilteredLogger(
      new ConsoleLogger(),
      (msg) => !msg.includes('debug')
    )
  )
);

logger.log('Application started');
logger.error('Something went wrong');
logger.warn('This is a warning');
```

## Common Mistakes

### 1. Too Many Decorators

```typescript
// ❌ BAD - Decorator chain too long
const decorated = new DecoratorA(
  new DecoratorB(
    new DecoratorC(
      new DecoratorD(
        new DecoratorE(
          new Component()
        )
      )
    )
  )
);
```

### 2. Decorator with State

```typescript
// ❌ BAD - Decorator with complex state
class BadDecorator extends BaseDecorator {
  private state: any;
  private dependencies: any[];
  
  // Hard to reason about
}
```

### 3. Not Implementing Interface

```typescript
// ❌ BAD - Decorator doesn't implement interface
class BadDecorator {
  private wrapped: Component;
  
  // Missing interface methods
}
```

### 4. Breaking Decorator Chain

```typescript
// ❌ BAD - Decorator doesn't delegate properly
class BadDecorator extends BaseDecorator {
  process(data: any): any {
    // Doesn't call super.process()
    return 'modified';
  }
}
```

## Best Practices

### 1. Implement Component Interface

```typescript
// ✅ GOOD - Implements interface
class GoodDecorator implements Component {
  private wrapped: Component;
  
  process(data: any): any {
    return this.wrapped.process(data);
  }
}
```

### 2. Keep Decorators Focused

```typescript
// ✅ GOOD - Single responsibility
class LoggingDecorator implements Component {
  // Only adds logging
}
```

### 3. Use Dependency Injection

```typescript
// ✅ GOOD - Injectable decorators
class Decorator {
  constructor(private wrapped: Component) {}
}
```

### 4. Limit Decorator Chain

```typescript
// ✅ GOOD - Reasonable chain length
const decorated = new CachingDecorator(
  new LoggingDecorator(
    new Component()
  )
);
```

## Performance Considerations

1. **Chain Overhead**: Each decorator adds a layer of indirection.

2. **Memory Usage**: Decorators are usually lightweight; the wrapped object consumes memory.

3. **Lazy Evaluation**: Consider lazy evaluation in decorators for expensive operations.

4. **Caching**: Use caching decorators to avoid redundant computation.

5. **Batch Operations**: Implement batch operations in decorators for better performance.

## Interview Questions

### Beginner

1. **What is the Decorator pattern?**
   - A structural pattern that adds behavior to objects dynamically by wrapping them.

2. **When would you use Decorator pattern?**
   - When you need to add responsibilities to objects dynamically without subclassing.

3. **What's the difference between Decorator and Adapter?**
   - Decorator adds behavior; Adapter changes interface.

4. **How do you implement Decorator in TypeScript?**
   - Create a base decorator that implements the component interface and wraps the component.

5. **What are the benefits of Decorator pattern?**
   - Flexible behavior extension, Single Responsibility, and组合able behaviors.

### Intermediate

6. **Can Decorator change the return type?**
   - No, decorators should maintain the component interface.

7. **How do you test Decorator pattern?**
   - Test each decorator independently, test decorator chains.

8. **What's the relationship between Decorator and Proxy?**
   - Both wrap objects; Decorator adds behavior, Proxy controls access.

9. **How do you handle decorator ordering?**
   - Order matters; the outermost decorator's behavior is applied first.

10. **Can Decorator be used with inheritance?**
    - Yes, but prefer composition over inheritance.

### Senior

11. **How does Decorator pattern affect scalability?**
    - Decorators are lightweight; chains can be optimized.

12. **What are the SOLID violations with Decorator?**
    - Usually follows SOLID; watch for decorators violating Single Responsibility.

13. **How do you handle Decorator in microservices?**
    - Use decorators for cross-cutting concerns like logging and caching.

14. **What are the memory implications of Decorator?**
    - Decorators are usually stateless; chains consume minimal memory.

15. **How do you refactor Decorator code?**
    - Extract common logic, use generics, and apply SOLID principles.

### FAANG-style

16. **Design a Decorator for a microservices architecture.**
    - Consider cross-cutting concerns, middleware, and observability.

17. **How would you implement Decorator for distributed systems?**
    - Consider network transparency, serialization, and fault tolerance.

18. **What are the implications of Decorator in cloud-native applications?**
    - Consider serverless functions, middleware, and function composition.

19. **How do you handle Decorator in event-driven architectures?**
    - Use decorators for event processing, transformation, and routing.

20. **Design a Decorator that supports A/B testing.**
    - Consider traffic splitting, metrics collection, and gradual rollout.

### Follow-ups

21. **Can Decorator pattern be combined with other patterns?**
    - Yes, commonly with Proxy, Adapter, and Composite patterns.

22. **How do you handle Decorator in testing frameworks?**
    - Use dependency injection, create test decorators, and mock implementations.

23. **What are the memory implications of Decorator pattern?**
    - Decorators are usually lightweight; chains consume minimal memory.

24. **How do you handle Decorator in serverless environments?**
    - Consider stateless decorators, middleware, and function composition.

25. **What's the impact of Decorator on code maintainability?**
    - Improves maintainability by enabling flexible behavior extension.

## Summary

The Decorator pattern is essential for adding behavior to objects dynamically. It promotes the Open/Closed Principle, enables flexible composition, and avoids class explosion. Use it for cross-cutting concerns, middleware, and extending functionality without modifying existing code.

## Cheat Sheet

```
┌─────────────────────────────────────────────┐
│           DECORATOR PATTERN                 │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Add behavior dynamically                  │
│ • Avoid class explosion                     │
│ • Combine multiple behaviors                │
│ • Extend without modifying                  │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple behavior extension                 │
│ • Decorator chain too long                  │
│ • Performance is critical                   │
│ • Decorators with too much state            │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Component interface                       │
│ • Decorator wraps component                 │
│ • Delegation to wrapped component           │
│ • Behavior addition                         │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Too many decorators                       │
│ • Decorators with state                     │
│ • Breaking decorator chain                  │
│ • Not implementing interface                │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • Proxy (controls access)                   │
│ • Adapter (changes interface)               │
│ • Composite (tree structure)                │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Decorator](https://refactoring.guru/design-patterns/decorator)
- [TC39 Decorator Proposal](https://github.com/tc39/proposal-decorators)
