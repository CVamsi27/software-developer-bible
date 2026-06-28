# Design Patterns Interview Questions

## Overview

This comprehensive guide covers 40 of the most commonly asked design patterns interview questions, categorized by difficulty level. Each question includes a detailed answer, code examples where applicable, and follow-up points.

---

## Beginner Questions (5-10)

### 1. What is the Singleton pattern and when would you use it?

**Answer:**
The Singleton pattern ensures a class has only one instance and provides a global point of access to it.

```typescript
class Singleton {
  private static instance: Singleton;

  private constructor() {}

  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }
}
```

**When to use:**
- Database connection pools
- Configuration managers
- Logging services
- Caching mechanisms

**Follow-up:** What are the problems with Singleton?
- Global state, tight coupling, testing difficulties, concurrency issues.

---

### 2. What is the Factory pattern and why is it useful?

**Answer:**
The Factory pattern provides an interface for creating objects without specifying their concrete classes.

```typescript
interface Vehicle {
  getType(): string;
}

class Car implements Vehicle {
  getType(): string { return 'Car'; }
}

class Truck implements Vehicle {
  getType(): string { return 'Truck'; }
}

class VehicleFactory {
  static create(type: 'car' | 'truck'): Vehicle {
    switch (type) {
      case 'car': return new Car();
      case 'truck': return new Truck();
    }
  }
}
```

**Why useful:**
- Loose coupling
- Easier maintenance
- Better testability
- Flexibility in object creation

---

### 3. What is the Observer pattern and where is it used?

**Answer:**
The Observer pattern defines a one-to-many dependency between objects so that when one object changes state, all dependents are notified.

```typescript
interface Observer {
  update(data: any): void;
}

class Subject {
  private observers: Observer[] = [];

  attach(observer: Observer): void {
    this.observers.push(observer);
  }

  detach(observer: Observer): void {
    this.observers = this.observers.filter(o => o !== observer);
  }

  notify(): void {
    this.observers.forEach(o => o.update(this));
  }
}
```

**Where used:**
- React state management
- Node.js EventEmitter
- Event-driven architectures
- UI frameworks

---

### 4. What is the Adapter pattern?

**Answer:**
The Adapter pattern allows objects with incompatible interfaces to collaborate by wrapping one interface to make it compatible with another.

```typescript
interface ModernPrinter {
  print(document: string): void;
}

class OldPrinter {
  printOld(document: string): void {
    console.log(`Printing: ${document}`);
  }
}

class PrinterAdapter implements ModernPrinter {
  constructor(private oldPrinter: OldPrinter) {}

  print(document: string): void {
    this.oldPrinter.printOld(document);
  }
}
```

---

### 5. What is the Builder pattern?

**Answer:**
The Builder pattern separates the construction of a complex object from its representation, allowing step-by-step construction.

```typescript
class QueryBuilder {
  private query: string = '';

  select(fields: string[]): this {
    this.query = `SELECT ${fields.join(', ')}`;
    return this;
  }

  from(table: string): this {
    this.query += ` FROM ${table}`;
    return this;
  }

  where(condition: string): this {
    this.query += ` WHERE ${condition}`;
    return this;
  }

  build(): string {
    return this.query;
  }
}

const query = new QueryBuilder()
  .select(['id', 'name'])
  .from('users')
  .where('age > 18')
  .build();
```

---

### 6. What is the Facade pattern?

**Answer:**
The Facade pattern provides a simplified interface to a complex subsystem, hiding its complexity.

```typescript
class CPU {
  freeze(): void { console.log('CPU freezing'); }
  jump(address: number): void { console.log(`CPU jumping to ${address}`); }
  execute(): void { console.log('CPU executing'); }
}

class Memory {
  load(address: number, data: string): void { console.log('Memory loading'); }
}

class ComputerFacade {
  private cpu = new CPU();
  private memory = new Memory();

  startComputer(): void {
    this.cpu.freeze();
    this.memory.load(0, 'boot');
    this.cpu.jump(0);
    this.cpu.execute();
  }
}
```

---

### 7. What is the difference between Creational, Structural, and Behavioral patterns?

**Answer:**
- **Creational**: Deal with object creation (Singleton, Factory, Builder)
- **Structural**: Deal with object composition (Adapter, Facade, Decorator)
- **Behavioral**: Deal with object communication (Observer, Strategy, Chain of Responsibility)

---

### 8. What is the Decorator pattern?

**Answer:**
The Decorator pattern allows adding behavior to objects dynamically by wrapping them in decorator objects.

```typescript
interface Coffee {
  getCost(): number;
  getDescription(): string;
}

class SimpleCoffee implements Coffee {
  getCost(): number { return 5; }
  getDescription(): string { return 'Simple coffee'; }
}

class MilkDecorator implements Coffee {
  constructor(private coffee: Coffee) {}

  getCost(): number { return this.coffee.getCost() + 2; }
  getDescription(): string { return `${this.coffee.getDescription()}, milk`; }
}
```

---

### 9. What is the Proxy pattern?

**Answer:**
The Proxy pattern provides a surrogate or placeholder for another object to control access to it.

```typescript
interface Image {
  display(): void;
}

class RealImage implements Image {
  display(): void { console.log('Displaying image'); }
}

class ProxyImage implements Image {
  private realImage: RealImage | null = null;

  display(): void {
    if (!this.realImage) {
      this.realImage = new RealImage();
    }
    this.realImage.display();
  }
}
```

---

### 10. What is the Strategy pattern?

**Answer:**
The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

```typescript
interface SortStrategy {
  sort(data: number[]): number[];
}

class BubbleSort implements SortStrategy {
  sort(data: number[]): number[] { /* implementation */ return data; }
}

class QuickSort implements SortStrategy {
  sort(data: number[]): number[] { /* implementation */ return data; }
}

class Sorter {
  constructor(private strategy: SortStrategy) {}

  sort(data: number[]): number[] {
    return this.strategy.sort(data);
  }
}
```

---

## Intermediate Questions (5-10)

### 11. What are the SOLID principles and how do design patterns relate to them?

**Answer:**
- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes must be substitutable for base types
- **I**nterface Segregation: Many specific interfaces over general ones
- **D**ependency Inversion: Depend on abstractions, not concretions

Design patterns implement SOLID principles:
- Strategy → Open/Closed
- Factory → Dependency Inversion
- Interface Segregation → Many small interfaces

---

### 12. What is the difference between Strategy and State patterns?

**Answer:**
- **Strategy**: Swaps algorithms at runtime, client selects strategy
- **State**: Changes behavior based on internal state, state transitions

```typescript
// Strategy - Client selects
const sorter = new Sorter(new QuickSort());

// State - Object changes internally
class TrafficLight {
  private state: State;

  change(): void {
    this.state = this.state.next();
  }
}
```

---

### 13. What is the difference between Decorator and Proxy patterns?

**Answer:**
- **Decorator**: Adds behavior, focuses on extending functionality
- **Proxy**: Controls access, focuses on managing object lifecycle

Both wrap objects, but their intent differs.

---

### 14. What is the Repository pattern and when should you use it?

**Answer:**
Repository mediates between domain and data mapping layers, acting as an in-memory collection of domain objects.

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<boolean>;
}

class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<User | null> {
    // Database query
  }

  async save(user: User): Promise<User> {
    // Database insert/update
  }

  async delete(id: string): Promise<boolean> {
    // Database delete
  }
}
```

**When to use:**
- Domain-driven design
- Need database abstraction
- Complex queries
- Testing requirements

---

### 15. What is the Chain of Responsibility pattern?

**Answer:**
Chain of Responsibility passes requests along a chain of handlers, each deciding to process or pass along.

```typescript
abstract class Handler {
  private next: Handler | null = null;

  setNext(handler: Handler): Handler {
    this.next = handler;
    return handler;
  }

  handle(request: any): any {
    if (this.next) {
      return this.next.handle(request);
    }
    return null;
  }
}

class AuthHandler extends Handler {
  handle(request: any): any {
    if (!request.token) {
      return { error: 'Unauthorized' };
    }
    return super.handle(request);
  }
}
```

---

### 16. What is the Template Method pattern?

**Answer:**
Template Method defines the skeleton of an algorithm in a base class, letting subclasses override specific steps.

```typescript
abstract class DataProcessor {
  process(): void {
    this.readData();
    this.processData();
    this.writeData();
  }

  protected abstract readData(): void;
  protected abstract processData(): void;
  protected abstract writeData(): void;
}

class CSVProcessor extends DataProcessor {
  protected readData(): void { console.log('Reading CSV'); }
  protected processData(): void { console.log('Processing CSV'); }
  protected writeData(): void { console.log('Writing CSV'); }
}
```

---

### 17. What is the Command pattern?

**Answer:**
Command encapsulates a request as an object, allowing parameterization and queueing.

```typescript
interface Command {
  execute(): void;
  undo(): void;
}

class CopyCommand implements Command {
  execute(): void { console.log('Copy'); }
  undo(): void { console.log('Undo copy'); }
}

class History {
  private commands: Command[] = [];

  push(command: Command): void {
    this.commands.push(command);
  }

  pop(): Command | undefined {
    return this.commands.pop();
  }
}
```

---

### 18. What is the Mediator pattern?

**Answer:**
Mediator reduces chaotic dependencies between objects by restricting direct communications and forcing them to collaborate via a mediator object.

```typescript
interface Mediator {
  notify(sender: object, event: string): void;
}

class ChatRoom implements Mediator {
  private users: User[] = [];

  addUser(user: User): void {
    this.users.push(user);
  }

  notify(sender: User, message: string): void {
    this.users.forEach(user => {
      if (user !== sender) {
        user.receive(message);
      }
    });
  }
}
```

---

### 19. What is the Composite pattern?

**Answer:**
Composite composes objects into tree structures and lets clients treat individual objects and compositions uniformly.

```typescript
interface Component {
  operation(): number;
}

class Leaf implements Component {
  constructor(private value: number) {}

  operation(): number { return this.value; }
}

class Composite implements Component {
  private children: Component[] = [];

  add(child: Component): void {
    this.children.push(child);
  }

  operation(): number {
    return this.children.reduce((sum, child) => sum + child.operation(), 0);
  }
}
```

---

### 20. What is the Iterator pattern?

**Answer:**
Iterator provides a way to access elements of an aggregate object sequentially without exposing its underlying representation.

```typescript
interface Iterator<T> {
  hasNext(): boolean;
  next(): T;
}

class ArrayIterator<T> implements Iterator<T> {
  private position = 0;

  constructor(private array: T[]) {}

  hasNext(): boolean {
    return this.position < this.array.length;
  }

  next(): T {
    return this.array[this.position++];
  }
}
```

---

## Senior Questions (10-15)

### 21. How do you decide which design pattern to use?

**Answer:**
Consider:
1. **Problem type**: What problem are you solving?
2. **Context**: What's the application context?
3. **Trade-offs**: What are the costs and benefits?
4. **Existing patterns**: What patterns are already in use?
5. **Team familiarity**: What does the team know?

**Decision framework:**
- Creating objects → Factory, Builder, Singleton
- Adding behavior → Decorator, Strategy
- Simplifying interface → Facade, Adapter
- Managing complexity → Composite, Chain of Responsibility

---

### 22. What is the relationship between Design Patterns and Architecture?

**Answer:**
- **Patterns**: Solutions to recurring design problems
- **Architecture**: High-level structure of the system

Patterns support architecture:
- **Microservices**: Factory, Strategy, Observer
- **Clean Architecture**: Repository, Factory, Strategy
- **Event-Driven**: Observer, Mediator, Command

---

### 23. How do you handle cross-cutting concerns with patterns?

**Answer:**
Cross-cutting concerns (logging, security, transactions) can be handled with:

1. **Decorator Pattern**: Add behavior dynamically
2. **Chain of Responsibility**: Middleware pipeline
3. **Proxy Pattern**: Control access
4. **AOP (Aspect-Oriented Programming)**: Separate concerns

```typescript
// Decorator for logging
class LoggingDecorator implements Service {
  constructor(private service: Service) {}

  async execute(): Promise<any> {
    console.log('Before');
    const result = await this.service.execute();
    console.log('After');
    return result;
  }
}
```

---

### 24. What are anti-patterns related to design patterns?

**Answer:**
1. **Pattern Overuse**: Using patterns when simpler solutions exist
2. **Gold Plating**: Adding unnecessary complexity
3. **God Object**: Class doing too much
4. **Spaghetti Code**: No structure or patterns
5. **Resume Driven Development**: Using patterns just to show knowledge

---

### 25. How do you test code that uses design patterns?

**Answer:**
- **Factory**: Mock the factory, test product creation
- **Strategy**: Test each strategy independently
- **Observer**: Mock observers, verify notifications
- **Decorator**: Test each decorator layer
- **Proxy**: Mock real subject, test proxy behavior

```typescript
// Test Strategy pattern
const strategies = [
  new BubbleSort(),
  new QuickSort(),
  new MergeSort()
];

strategies.forEach(strategy => {
  const sorter = new Sorter(strategy);
  expect(sorter.sort([3, 1, 2])).toEqual([1, 2, 3]);
});
```

---

### 26. How do patterns affect performance?

**Answer:**
- **Singleton**: Minimal overhead, single instance
- **Factory**: Slight overhead for object creation
- **Proxy**: Adds indirection layer
- **Decorator**: Each decorator adds overhead
- **Chain of Responsibility**: Chain length affects performance

**Optimizations:**
- Lazy initialization
- Caching in proxies
- Early termination in chains
- Object pooling

---

### 27. What is the relationship between patterns and SOLID principles?

**Answer:**
| Pattern | SOLID Principle |
|---------|----------------|
| Strategy | Open/Closed |
| Factory | Dependency Inversion |
| Interface Segregation | Many small interfaces |
| Template Method | Open/Closed |
| Decorator | Open/Closed, Single Responsibility |

---

### 28. How do you handle design patterns in distributed systems?

**Answer:**
- **Factory**: Create distributed objects
- **Observer**: Event-driven communication
- **Proxy**: Remote proxies, stubs
- **Facade**: API gateways
- **Mediator**: Message brokers

**Considerations:**
- Network latency
- Fault tolerance
- Consistency
- Scalability

---

### 29. What are modern alternatives to classic design patterns?

**Answer:**
- **Singleton → Module pattern, DI containers**
- **Factory → DI containers, dependency injection**
- **Observer → Reactive programming (RxJS), Event Emitter**
- **Strategy → Functional programming, higher-order functions**
- **Decorator → Middleware, functional composition**

---

### 30. How do you refactor code to use design patterns?

**Answer:**
1. **Identify code smells**: Duplication, complex conditionals
2. **Extract common behavior**: Look for repeated code
3. **Apply appropriate pattern**: Match problem to pattern
4. **Refactor incrementally**: Small changes, test often
5. **Document decisions**: Why this pattern was chosen

---

### 31. What is the impact of design patterns on code maintainability?

**Answer:**
**Positive:**
- Clear structure and intent
- Reusable solutions
- Better testability
- Team communication

**Negative:**
- Over-engineering
- Added complexity
- Learning curve
- Potential misapplication

---

### 32. How do you handle design patterns in legacy code?

**Answer:**
1. **Identify refactoring opportunities**: Look for code smells
2. **Apply Strangler Fig pattern**: Gradually replace
3. **Use Adapter pattern**: Integrate with legacy
4. **Introduce patterns incrementally**: Start with low-risk areas
5. **Write tests first**: Ensure behavior preservation

---

### 33. What is the relationship between patterns and frameworks?

**Answer:**
- **Patterns**: General solutions to problems
- **Framework**: Specific implementation using patterns

Examples:
- **React**: Observer (state changes), Composite (components)
- **Express**: Chain of Responsibility (middleware)
- **NestJS**: Factory, Strategy, Decorator (decorators)

---

### 34. How do you handle design patterns in microservices?

**Answer:**
- **Factory**: Create service instances
- **Strategy**: Different implementations per service
- **Observer**: Event-driven communication
- **Facade**: API gateways
- **CQRS**: Separate read/write models

**Considerations:**
- Service boundaries
- Communication patterns
- Data consistency
- Deployment

---

### 35. What are the trade-offs of using design patterns?

**Answer:**
| Benefit | Trade-off |
|---------|-----------|
| Code reuse | Added complexity |
| Clear structure | Learning curve |
| Testability | More classes |
| Maintainability | Potential over-engineering |

---

### 36. How do you explain design patterns to non-technical stakeholders?

**Answer:**
Use analogies:
- **Factory**: Like a manufacturing assembly line
- **Strategy**: Like different routes to the same destination
- **Facade**: Like a hotel concierge
- **Decorator**: Like adding toppings to a pizza

Focus on benefits:
- Easier to maintain
- Faster development
- Better quality

---

### 37. What is the role of design patterns in code reviews?

**Answer:**
- **Identify pattern usage**: Ensure correct application
- **Check for anti-patterns**: Spot over-engineering
- **Verify SOLID compliance**: Ensure principles are followed
- **Knowledge sharing**: Help team learn patterns
- **Consistency**: Ensure consistent pattern usage

---

### 38. How do design patterns evolve over time?

**Answer:**
- **Classic patterns**: GoF patterns still relevant
- **Modern adaptations**: React patterns, serverless patterns
- **Language-specific**: TypeScript decorators, async/await patterns
- **Architecture patterns**: Microservices, event-driven

---

### 39. What are the most overused design patterns?

**Answer:**
1. **Singleton**: Often when DI is better
2. **Factory**: When simple object creation works
3. **Observer**: When simple callbacks suffice
4. **Decorator**: When inheritance works fine

**Rule of thumb**: Don't use a pattern if a simpler solution exists.

---

### 40. How do you stay updated with design pattern trends?

**Answer:**
- Read blogs and articles
- Study framework source code
- Attend conferences and meetups
- Practice with side projects
- Discuss with team members
- Review open-source projects

---

## FAANG-style Questions (5-10)

### 41. Design a URL shortener using design patterns.

**Answer:**
Patterns to use:
- **Factory**: Create short URLs
- **Strategy**: Different encoding algorithms
- **Proxy**: Caching layer
- **Facade**: Simplified API
- **Singleton**: Configuration manager

```typescript
class URLShortener {
  private factory: URLFactory;
  private cache: CacheProxy;
  private strategy: EncodingStrategy;

  constructor() {
    this.factory = new URLFactory();
    this.cache = new CacheProxy(new DatabaseURLRepository());
    this.strategy = new Base62Encoding();
  }

  async shorten(longUrl: string): Promise<string> {
    const existing = await this.cache.findByLongUrl(longUrl);
    if (existing) return existing.shortUrl;

    const shortUrl = this.strategy.encode(longUrl);
    const url = this.factory.create(longUrl, shortUrl);
    await this.cache.save(url);

    return shortUrl;
  }
}
```

---

### 42. Design a real-time notification system.

**Answer:**
Patterns to use:
- **Observer**: Notify subscribers
- **Strategy**: Different notification channels
- **Chain of Responsibility**: Processing pipeline
- **Factory**: Create notification handlers
- **Facade**: Simplified API

```typescript
class NotificationSystem {
  private channels: Map<string, NotificationChannel>;
  private pipeline: ProcessingPipeline;

  async send(notification: Notification): Promise<void> {
    const processed = await this.pipeline.process(notification);

    for (const channel of processed.channels) {
      await this.channels.get(channel)?.send(processed);
    }
  }
}
```

---

### 43. Design a plugin system for an application.

**Answer:**
Patterns to use:
- **Factory**: Load and create plugins
- **Strategy**: Different plugin behaviors
- **Proxy**: Plugin isolation
- **Chain of Responsibility**: Plugin pipeline
- **Mediator**: Plugin communication

```typescript
class PluginManager {
  private plugins: Map<string, Plugin>;
  private loader: PluginLoader;
  private sandbox: PluginSandbox;

  async loadPlugin(config: PluginConfig): Promise<void> {
    const plugin = await this.loader.load(config);
    const proxied = this.sandbox.wrap(plugin);
    this.plugins.set(config.name, proxied);
  }

  async executePlugin(name: string, command: string): Promise<any> {
    const plugin = this.plugins.get(name);
    if (!plugin) throw new Error('Plugin not found');

    return plugin.execute(command);
  }
}
```

---

### 44. Design a payment processing system.

**Answer:**
Patterns to use:
- **Strategy**: Different payment providers
- **Factory**: Create payment processors
- **Adapter**: Integrate third-party APIs
- **Facade**: Simplified payment API
- **Decorator**: Add features (logging, validation)

```typescript
class PaymentService {
  private processors: Map<string, PaymentProcessor>;
  private adapter: PaymentAdapter;
  private decorator: PaymentDecorator;

  async processPayment(payment: Payment): Promise<Result> {
    const processor = this.processors.get(payment.provider);
    if (!processor) throw new Error('Unknown provider');

    const adapted = this.adapter.adapt(payment, processor);
    return this.decorator.process(adapted);
  }
}
```

---

### 45. Design a caching layer for a web application.

**Answer:**
Patterns to use:
- **Proxy**: Cache proxy
- **Strategy**: Different eviction policies
- **Observer**: Cache invalidation
- **Factory**: Create cache instances
- **Facade**: Simplified cache API

```typescript
class CacheLayer {
  private cache: CacheProxy;
  private strategy: EvictionStrategy;
  private invalidator: CacheInvalidator;

  async get<T>(key: string): Promise<T | null> {
    return this.cache.get(key);
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    await this.cache.set(key, value, ttl);
    await this.invalidator.notify(key, 'set');
  }

  async invalidate(pattern: string): Promise<void> {
    await this.cache.invalidate(pattern);
    await this.invalidator.notify(pattern, 'invalidate');
  }
}
```

---

## Follow-up Questions (5-10)

### 46. How would you refactor a codebase that doesn't use design patterns?

**Answer:**
1. **Identify code smells**: Look for duplication, complex conditionals
2. **Start with low-risk areas**: Choose isolated modules
3. **Write tests**: Ensure behavior preservation
4. **Apply patterns incrementally**: One pattern at a time
5. **Document changes**: Explain why patterns were chosen

---

### 47. How do you handle design pattern disagreements in a team?

**Answer:**
1. **Discuss trade-offs**: Benefits vs costs
2. **Consider context**: What works for the project
3. **Look at precedents**: What patterns are already used
4. **Prototype**: Try different approaches
5. **Make a decision**: Avoid analysis paralysis

---

### 48. What questions should you ask before applying a design pattern?

**Answer:**
1. What problem are we solving?
2. Is this the simplest solution?
3. What are the trade-offs?
4. Does this fit our architecture?
5. Will the team understand this?
6. How will this affect testing?
7. What are the performance implications?

---

### 49. How do you document design pattern usage?

**Answer:**
- **Code comments**: Explain why, not what
- **Architecture decision records**: Document decisions
- **README files**: Explain pattern usage
- **Diagrams**: Visual representation
- **Code reviews**: Discuss pattern application

---

### 50. What's the most important thing to remember about design patterns?

**Answer:**
**Patterns are tools, not goals.** Use them when they solve a real problem, not just because they exist. The best pattern is the one that makes your code simpler, more maintainable, and easier to understand.

---

## Cheat Sheet

```
┌─────────────────────────────────────────────────────────────┐
│           DESIGN PATTERNS INTERVIEW CHEAT SHEET             │
├─────────────────────────────────────────────────────────────┤
│ CREATIONAL PATTERNS:                                         │
│ • Singleton: One instance, global access                    │
│ • Factory: Create objects without specifying class           │
│ • Builder: Step-by-step object construction                 │
│ • Prototype: Clone existing objects                         │
│ • Abstract Factory: Create families of related objects       │
├─────────────────────────────────────────────────────────────┤
│ STRUCTURAL PATTERNS:                                         │
│ • Adapter: Interface conversion                             │
│ • Facade: Simplified interface                              │
│ • Decorator: Add behavior dynamically                       │
│ • Proxy: Control access                                     │
│ • Composite: Tree structure                                 │
│ • Chain of Responsibility: Request processing pipeline      │
├─────────────────────────────────────────────────────────────┤
│ BEHAVIORAL PATTERNS:                                         │
│ • Observer: One-to-many notifications                       │
│ • Strategy: Interchangeable algorithms                      │
│ • Command: Encapsulate requests                             │
│ • State: Change behavior based on state                     │
│ • Template Method: Define algorithm skeleton                │
│ • Iterator: Sequential access                               │
├─────────────────────────────────────────────────────────────┤
│ KEY PRINCIPLES:                                              │
│ • SOLID principles                                          │
│ • DRY (Don't Repeat Yourself)                               │
│ • KISS (Keep It Simple, Stupid)                             │
│ • YAGNI (You Aren't Gonna Need It)                          │
└─────────────────────────────────────────────────────────────┘
```

## References & Learn More

- [Refactoring Guru](https://refactoring.guru/design-patterns)
- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Patterns.dev](https://www.patterns.dev/)
- [SourceMaking](https://sourcemaking.com/)
