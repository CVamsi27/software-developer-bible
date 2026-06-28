# Singleton Pattern

## Definition

The Singleton pattern is a creational design pattern that ensures a class has only one instance and provides a global point of access to that instance. It's one of the most well-known and commonly used design patterns in software development.

The pattern is particularly useful when exactly one object is needed to coordinate actions across the system. It's often used for configuration managers, database connections, logging services, and caching mechanisms.

## Why Do We Need It?

Without the Singleton pattern, multiple instances of a class could be created, leading to:

1. **Resource waste**: Multiple database connections consuming excessive memory

2. **Inconsistent state**: Different instances holding different configuration values

3. **Race conditions**: Multiple threads accessing shared resources simultaneously

4. **Global access problems**: No centralized point to access critical services

## How It Works

The Singleton pattern works by:

1. Making the constructor private to prevent direct instantiation

2. Creating a static method that acts as the global access point

3. Maintaining a single static instance within the class

4. Providing lazy initialization or eager initialization based on requirements

```text
┌─────────────────────────────────────────────┐
│              Singleton Class                 │
├─────────────────────────────────────────────┤
│ - static instance: Singleton                │
│ - private constructor(): Singleton          │
├─────────────────────────────────────────────┤
│ + static getInstance(): Singleton           │
│ +公共方法(): void                            │
└─────────────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────┐
        │   Single Instance  │
        │   (Global Access)  │
        └───────────────────┘
                    │
                    ▼
        ┌───────────────────┐
        │   All Code Accesses│
        │   Same Instance    │
        └───────────────────┘

```

## Code Examples

### Basic Singleton Implementation

```typescript
class Singleton {
  private static instance: Singleton;

  private constructor() {
    // Private constructor prevents direct instantiation
  }

  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }

  public doSomething(): void {
    console.log('Singleton is working');
  }
}

// Usage
const singleton1 = Singleton.getInstance();
const singleton2 = Singleton.getInstance();

console.log(singleton1 === singleton2); // true - same instance

```

### Thread-Safe Singleton with Double-Checked Locking

```typescript
class ThreadSafeSingleton {
  private static instance: ThreadSafeSingleton;
  private static isInitializing = false;

  private constructor() {
    // Simulate expensive initialization
    this.initializeDatabase();
  }

  private initializeDatabase(): void {
    console.log('Initializing database connection...');
  }

  public static getInstance(): ThreadSafeSingleton {
    if (!ThreadSafeSingleton.instance) {
      if (!ThreadSafeSingleton.isInitializing) {
        ThreadSafeSingleton.isInitializing = true;
        ThreadSafeSingleton.instance = new ThreadSafeSingleton();
      }
    }
    return ThreadSafeSingleton.instance;
  }

  public query(sql: string): any {
    console.log(`Executing query: ${sql}`);
    return { results: [] };
  }
}

```

### Module-Level Singleton (TypeScript Best Practice)

```typescript
// database.ts - Simple module-level singleton
class Database {
  private host: string;
  private port: number;
  private isConnected: boolean = false;

  constructor() {
    this.host = 'localhost';
    this.port = 5432;
  }

  async connect(): Promise<void> {
    if (this.isConnected) {
      console.log('Already connected to database');
      return;
    }

    console.log(`Connecting to database at ${this.host}:${this.port}`);
    this.isConnected = true;
  }

  async query<T>(sql: string): Promise<T[]> {
    if (!this.isConnected) {
      throw new Error('Database not connected');
    }
    console.log(`Executing: ${sql}`);
    return [] as T[];
  }

  async disconnect(): Promise<void> {
    this.isConnected = false;
    console.log('Disconnected from database');
  }
}

// Export a single instance
export const database = new Database();

```

### Configuration Manager Singleton

```typescript
interface AppConfig {
  port: number;
  databaseUrl: string;
  redisUrl: string;
  jwtSecret: string;
  environment: 'development' | 'production' | 'test';
}

class ConfigurationManager {
  private static instance: ConfigurationManager;
  private config: AppConfig;

  private constructor() {
    this.config = this.loadConfig();
  }

  private loadConfig(): AppConfig {
    // In real app, this would read from environment variables or config files
    return {
      port: parseInt(process.env.PORT || '3000'),
      databaseUrl: process.env.DATABASE_URL || 'postgresql://localhost:5432/myapp',
      redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
      jwtSecret: process.env.JWT_SECRET || 'dev-secret-key',
      environment: (process.env.NODE_ENV as AppConfig['environment']) || 'development'
    };
  }

  public static getInstance(): ConfigurationManager {
    if (!ConfigurationManager.instance) {
      ConfigurationManager.instance = new ConfigurationManager();
    }
    return ConfigurationManager.instance;
  }

  public get<K extends keyof AppConfig>(key: K): AppConfig[K] {
    return this.config[key];
  }

  public set<K extends keyof AppConfig>(key: K, value: AppConfig[K]): void {
    this.config[key] = value;
  }

  public getAll(): Readonly<AppConfig> {
    return { ...this.config };
  }
}

// Usage
const config = ConfigurationManager.getInstance();
console.log(config.get('port')); // 3000
console.log(config.get('environment')); // 'development'

```

### Logger Singleton

```typescript
enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3
}

class Logger {
  private static instance: Logger;
  private logLevel: LogLevel;
  private logs: Array<{ timestamp: Date; level: LogLevel; message: string }> = [];

  private constructor() {
    this.logLevel = LogLevel.INFO;
  }

  public static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  public setLevel(level: LogLevel): void {
    this.logLevel = level;
  }

  public debug(message: string): void {
    if (this.logLevel <= LogLevel.DEBUG) {
      this.log(LogLevel.DEBUG, message);
    }
  }

  public info(message: string): void {
    if (this.logLevel <= LogLevel.INFO) {
      this.log(LogLevel.INFO, message);
    }
  }

  public warn(message: string): void {
    if (this.logLevel <= LogLevel.WARN) {
      this.log(LogLevel.WARN, message);
    }
  }

  public error(message: string): void {
    if (this.logLevel <= LogLevel.ERROR) {
      this.log(LogLevel.ERROR, message);
    }
  }

  private log(level: LogLevel, message: string): void {
    const entry = {
      timestamp: new Date(),
      level,
      message
    };

    this.logs.push(entry);
    console.log(`[${LogLevel[level]}] ${message}`);
  }

  public getLogs(): Array<{ timestamp: Date; level: LogLevel; message: string }> {
    return [...this.logs];
  }
}

```

## Real-World Use Cases

### 1. Database Connection Pool

```typescript
class DatabasePool {
  private static instance: DatabasePool;
  private connections: Array<{ id: number; inUse: boolean }> = [];
  private maxConnections: number;

  private constructor(maxConnections: number = 10) {
    this.maxConnections = maxConnections;
    this.initializePool();
  }

  private initializePool(): void {
    for (let i = 0; i < this.maxConnections; i++) {
      this.connections.push({ id: i, inUse: false });
    }
  }

  public static getInstance(maxConnections?: number): DatabasePool {
    if (!DatabasePool.instance) {
      DatabasePool.instance = new DatabasePool(maxConnections);
    }
    return DatabasePool.instance;
  }

  public acquireConnection(): { id: number } | null {
    const available = this.connections.find(conn => !conn.inUse);
    if (available) {
      available.inUse = true;
      return { id: available.id };
    }
    return null;
  }

  public releaseConnection(id: number): void {
    const conn = this.connections.find(c => c.id === id);
    if (conn) {
      conn.inUse = false;
    }
  }
}

```

### 2. Cache Manager

```typescript
class CacheManager {
  private static instance: CacheManager;
  private cache: Map<string, { value: any; expiry: number }> = new Map();
  private defaultTTL: number = 3600000; // 1 hour

  private constructor() {}

  public static getInstance(): CacheManager {
    if (!CacheManager.instance) {
      CacheManager.instance = new CacheManager();
    }
    return CacheManager.instance;
  }

  public set(key: string, value: any, ttl?: number): void {
    const expiry = Date.now() + (ttl || this.defaultTTL);
    this.cache.set(key, { value, expiry });
  }

  public get<T>(key: string): T | null {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.value as T;
  }

  public delete(key: string): boolean {
    return this.cache.delete(key);
  }

  public clear(): void {
    this.cache.clear();
  }

  public has(key: string): boolean {
    const item = this.cache.get(key);
    if (!item) return false;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }
}

```

### 3. Event Bus

```typescript
type EventHandler = (...args: any[]) => void;

class EventBus {
  private static instance: EventBus;
  private listeners: Map<string, EventHandler[]> = new Map();

  private constructor() {}

  public static getInstance(): EventBus {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus();
    }
    return EventBus.instance;
  }

  public on(event: string, handler: EventHandler): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(handler);
  }

  public emit(event: string, ...args: any[]): void {
    const handlers = this.listeners.get(event);
    if (handlers) {
      handlers.forEach(handler => handler(...args));
    }
  }

  public off(event: string, handler: EventHandler): void {
    const handlers = this.listeners.get(event);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }
}

```

## Common Mistakes

### 1. Not Thread-Safe

```typescript
// ❌ BAD - Not thread-safe
class BadSingleton {
  private static instance: BadSingleton;

  private constructor() {}

  public static getInstance(): BadSingleton {
    // Race condition in multi-threaded environments
    if (!BadSingleton.instance) {
      BadSingleton.instance = new BadSingleton();
    }
    return BadSingleton.instance;
  }
}

```

### 2. Overusing Singleton

```typescript
// ❌ BAD - Using Singleton for everything
class UserService {
  private static instance: UserService;

  private constructor() {}

  public static getInstance(): UserService {
    if (!UserService.instance) {
      UserService.instance = new UserService();
    }
    return UserService.instance;
  }

  // User service doesn't need to be a singleton
  // It could have multiple instances with different configurations
  public async createUser(data: any): Promise<any> {
    // Implementation
  }
}

```

### 3. Global State Pollution

```typescript
// ❌ BAD - Using Singleton as global state
class GlobalState {
  private static instance: GlobalState;
  public currentUser: any = null;
  public theme: string = 'light';

  private constructor() {}

  public static getInstance(): GlobalState {
    if (!GlobalState.instance) {
      GlobalState.instance = new GlobalState();
    }
    return GlobalState.instance;
  }
}

// This creates tight coupling and makes testing difficult

```

### 4. Making Everything Static

```typescript
// ❌ BAD - Using static methods instead of Singleton
class StaticService {
  private static data: any[] = [];

  public static addItem(item: any): void {
    StaticService.data.push(item);
  }

  public static getItems(): any[] {
    return StaticService.data;
  }
}

// This is harder to test and has the same problems as Singleton
// but without the benefits of dependency injection

```

## Best Practices

### 1. Use Module Pattern When Possible

```typescript
// ✅ GOOD - Module-level singleton (simplest approach)
class Database {
  // ... implementation
}

export const database = new Database();

```

### 2. Implement Dependency Injection

```typescript
// ✅ GOOD - Use DI container instead of Singleton
class Database {
  constructor(private config: DatabaseConfig) {}

  async connect(): Promise<void> {
    // Use this.config
  }
}

// DI Container
class Container {
  private static services: Map<string, any> = new Map();

  public static register<T>(name: string, service: T): void {
    Container.services.set(name, service);
  }

  public static resolve<T>(name: string): T {
    return Container.services.get(name) as T;
  }
}

// Register and use
const db = new Database({ host: 'localhost', port: 5432 });
Container.register('database', db);
const database = Container.resolve<Database>('database');

```

### 3. Make Constructor Private and Document

```typescript
// ✅ GOOD - Clear documentation
/**

 - Singleton class for managing application configuration.
 - Use ConfigurationManager.getInstance() to access the instance.
 *

 - @example
 - const config = ConfigurationManager.getInstance();
 - const port = config.get('port');
 */
class ConfigurationManager {
  private static instance: ConfigurationManager;

  private constructor() {
    // Private constructor - use getInstance() instead
  }

  public static getInstance(): ConfigurationManager {
    if (!ConfigurationManager.instance) {
      ConfigurationManager.instance = new ConfigurationManager();
    }
    return ConfigurationManager.instance;
  }
}

```

### 4. Consider Testability

```typescript
// ✅ GOOD - Make Singleton testable
class Database {
  private static instance: Database;

  // Allow resetting for testing
  public static resetInstance(): void {
    Database.instance = undefined as any;
  }

  // Allow setting mock for testing
  public static setInstance(instance: Database): void {
    Database.instance = instance;
  }

  private constructor() {}

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}

```

### 5. Use Lazy Initialization When Appropriate

```typescript
// ✅ GOOD - Lazy initialization with caching
class ExpensiveService {
  private static instance: ExpensiveService;
  private static isInitialized = false;

  private constructor() {
    this.initialize();
  }

  private initialize(): void {
    console.log('Expensive initialization...');
  }

  public static getInstance(): ExpensiveService {
    if (!ExpensiveService.instance) {
      ExpensiveService.instance = new ExpensiveService();
      ExpensiveService.isInitialized = true;
    }
    return ExpensiveService.instance;
  }
}

```

## Performance Considerations

1. **Memory Usage**: Singleton instances persist for the lifetime of the application, so they consume memory throughout.

2. **Initialization Cost**: Lazy initialization delays the cost but can cause delays on first access. Eager initialization pays the cost upfront.

3. **Thread Safety**: Thread-safe implementations have slight overhead but prevent race conditions.

4. **Garbage Collection**: Singletons are rarely garbage collected, which can be both good (no GC overhead) and bad (memory can't be reclaimed).

5. **Testing Impact**: Singletons make unit testing harder as they maintain state between tests.

## Interview Questions

### Beginner

1. **What is the Singleton pattern?**

   - Ensures a class has only one instance and provides global access to it.

2. **When would you use a Singleton?**

   - For database connections, configuration managers, logging services, and caching.

3. **What's the difference between lazy and eager initialization?**

   - Lazy creates the instance on first use; eager creates it immediately.

4. **How do you prevent multiple instances in JavaScript/TypeScript?**

   - Using module exports, private constructors, or static instance variables.

5. **What are the problems with Singleton?**

   - Global state, tight coupling, testing difficulties, and concurrency issues.

### Intermediate

6. **How do you make a Singleton thread-safe?**

   - Double-checked locking, mutex, or using language-specific features.

7. **What's the difference between Singleton and static class?**

   - Singleton can implement interfaces, be passed as parameter, and supports inheritance.

8. **How do you test code that uses Singleton?**

   - Use dependency injection, mock the Singleton, or use test doubles.

9. **What are Singleton alternatives?**

   - Dependency injection, service locator, module pattern.

10. **How do you handle Singleton in distributed systems?**

    - Use distributed locks, database constraints, or design without Singleton.

### Senior

11. **How does Singleton affect scalability?**

    - Can become a bottleneck; consider connection pooling or removing Singleton.

12. **What's the relationship between Singleton and Factory patterns?**

    - Factory can create Singletons; Singleton can be used in Factory implementations.

13. **How do you handle Singleton in microservices?**

    - Each service has its own Singleton; avoid shared Singletons across services.

14. **What are the SOLID violations with Singleton?**

    - Single Responsibility, Open/Closed, Dependency Inversion violations.

15. **How do you refactor Singleton code?**

    - Extract dependencies, use DI container, make it testable.

### FAANG-style

16. **Design a Singleton for a distributed caching system.**

    - Consider consistency, partition tolerance, cache invalidation.

17. **How would you implement Singleton in a multi-process environment?**

    - Use file locks, database constraints, or shared memory.

18. **What are the implications of Singleton in cloud-native applications?**

    - Consider serverless, containers, horizontal scaling.

19. **How do you handle Singleton in event-driven architectures?**

    - Use event sourcing, CQRS, or remove Singleton dependency.

20. **Design a Singleton that supports hot reloading.**

    - Consider graceful shutdown, state migration, version compatibility.

### Follow-ups

21. **Can Singleton be inherited?**

    - Yes, but it complicates the pattern; consider composition over inheritance.

22. **How do you handle Singleton in testing frameworks?**

    - Use dependency injection, reset instances between tests, use test doubles.

23. **What are the memory implications of Singleton?**

    - Singletons persist for app lifetime, can cause memory leaks if not managed.

24. **How do you handle Singleton in serverless environments?**

    - Consider cold starts, instance reuse, and state management.

25. **What's the impact of Singleton on code maintainability?**

    - Increases coupling, makes refactoring harder, reduces code flexibility.

## Summary

The Singleton pattern is a powerful tool for ensuring a single instance and global access, but it should be used judiciously. Modern applications often prefer dependency injection and module patterns for better testability and flexibility. Use Singleton when you genuinely need exactly one instance and understand the trade-offs.

## Cheat Sheet

```text
┌─────────────────────────────────────────────┐
│           SINGLETON PATTERN                 │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Exactly one instance needed               │
│ • Global access required                    │
│ • Resource coordination                     │
│ • Configuration management                  │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Multiple instances needed                 │
│ • Tight coupling is bad                     │
│ • Testing is critical                       │
│ • Distributed systems                       │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Private constructor                       │
│ • Static instance variable                  │
│ • Global access point                       │
│ • Lazy or eager initialization              │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Thread safety                             │
│ • Global state pollution                    │
│ • Testing difficulties                      │
│ • Memory leaks                              │
├─────────────────────────────────────────────┤
│ 🔧 ALTERNATIVES:                           │
│ • Module pattern                            │
│ • Dependency injection                      │
│ • Service locator                           │
│ • Static class                              │
└─────────────────────────────────────────────┘

```

## References & Learn More

- [GoF Design Patterns Book](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Singleton](https://refactoring.guru/design-patterns/singleton)
- [Martin Fowler: Singleton](https://martinfowler.com/articles/injection.html#UsingaSingleton)
