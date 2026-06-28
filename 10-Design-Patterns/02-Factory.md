# Factory Pattern

## Definition

The Factory pattern is a creational design pattern that provides an interface for creating objects without specifying their concrete classes. It encapsulates object creation logic, allowing subclasses or methods to decide which class to instantiate.

The pattern is particularly useful when the creation process is complex, involves multiple steps, or when the system needs to be independent from how its objects are created.

## Why Do We Need It?

Without the Factory pattern, object creation logic is scattered throughout the codebase, leading to:

1. **Tight coupling**: Code depends on specific concrete classes
2. **Code duplication**: Object creation logic repeated everywhere
3. **Difficult maintenance**: Changing creation logic requires modifying multiple places
4. **Testing challenges**: Hard to mock or replace object creation

## How It Works

The Factory pattern works by:

1. Defining a common interface or base class for all products
2. Creating a factory class or method responsible for object creation
3. Moving creation logic from client code to the factory
4. Allowing the factory to decide which concrete class to instantiate

```text
┌─────────────────────────────────────────────────┐
│                  Factory Pattern                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Client      │                              │
│  └──────────────┘                               │
│         │                                       │
│         ▼                                       │
│  ┌──────────────┐                               │
│  │    Factory    │◄── Decides which class        │
│  └──────────────┘     to instantiate            │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Product Interface                │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┬────────────┐                    │
│    ▼         ▼            ▼                    │
│ ┌──────┐ ┌──────┐   ┌──────┐                  │
│ │Prod A│ │Prod B│   │Prod C│                  │
│ └──────┘ └──────┘   └──────┘                  │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Simple Factory

```typescript
// Product interface
interface Notification {
  send(message: string): void;
}

// Concrete products
class EmailNotification implements Notification {
  send(message: string): void {
    console.log(`Sending email: ${message}`);
  }
}

class SMSNotification implements Notification {
  send(message: string): void {
    console.log(`Sending SMS: ${message}`);
  }
}

class PushNotification implements Notification {
  send(message: string): void {
    console.log(`Sending push notification: ${message}`);
  }
}

// Simple Factory
class NotificationFactory {
  static create(type: 'email' | 'sms' | 'push'): Notification {
    switch (type) {
      case 'email':
        return new EmailNotification();
      case 'sms':
        return new SMSNotification();
      case 'push':
        return new PushNotification();
      default:
        throw new Error(`Unknown notification type: ${type}`);
    }
  }
}

// Usage
const emailNotifier = NotificationFactory.create('email');
emailNotifier.send('Hello World!');
```

### Factory Method Pattern

```typescript
// Abstract creator
abstract class VehicleFactory {
  abstract createVehicle(): Vehicle;

  // Template method that uses the factory method
  describeVehicle(): void {
    const vehicle = this.createVehicle();
    console.log(`Created ${vehicle.getType()} with ${vehicle.getWheels()} wheels`);
  }
}

// Product interface
interface Vehicle {
  getType(): string;
  getWheels(): number;
  accelerate(): void;
}

// Concrete products
class Car implements Vehicle {
  getType(): string {
    return 'Car';
  }

  getWheels(): number {
    return 4;
  }

  accelerate(): void {
    console.log('Car is accelerating');
  }
}

class Motorcycle implements Vehicle {
  getType(): string {
    return 'Motorcycle';
  }

  getWheels(): number {
    return 2;
  }

  accelerate(): void {
    console.log('Motorcycle is accelerating');
  }
}

class Truck implements Vehicle {
  getType(): string {
    return 'Truck';
  }

  getWheels(): number {
    return 6;
  }

  accelerate(): void {
    console.log('Truck is accelerating');
  }
}

// Concrete factories
class CarFactory extends VehicleFactory {
  createVehicle(): Vehicle {
    return new Car();
  }
}

class MotorcycleFactory extends VehicleFactory {
  createVehicle(): Vehicle {
    return new Motorcycle();
  }
}

class TruckFactory extends VehicleFactory {
  createVehicle(): Vehicle {
    return new Truck();
  }
}

// Usage
const carFactory = new CarFactory();
carFactory.describeVehicle(); // Created Car with 4 wheels

const truckFactory = new TruckFactory();
truckFactory.describeVehicle(); // Created Truck with 6 wheels
```

### Abstract Factory Pattern

```typescript
// Abstract products
interface Button {
  render(): string;
  onClick(handler: () => void): void;
}

interface Input {
  render(): string;
  getValue(): string;
}

interface Dialog {
  render(): string;
  open(): void;
}

// Concrete products - Light theme
class LightButton implements Button {
  render(): string {
    return '<button class="light-button">Click me</button>';
  }

  onClick(handler: () => void): void {
    console.log('Light button clicked');
    handler();
  }
}

class LightInput implements Input {
  render(): string {
    return '<input class="light-input" />';
  }

  getValue(): string {
    return 'light input value';
  }
}

// Concrete products - Dark theme
class DarkButton implements Button {
  render(): string {
    return '<button class="dark-button">Click me</button>';
  }

  onClick(handler: () => void): void {
    console.log('Dark button clicked');
    handler();
  }
}

class DarkInput implements Input {
  render(): string {
    return '<input class="dark-input" />';
  }

  getValue(): string {
    return 'dark input value';
  }
}

// Abstract factory
interface UIFactory {
  createButton(): Button;
  createInput(): Input;
}

// Concrete factories
class LightThemeFactory implements UIFactory {
  createButton(): Button {
    return new LightButton();
  }

  createInput(): Input {
    return new LightInput();
  }
}

class DarkThemeFactory implements UIFactory {
  createButton(): Button {
    return new DarkButton();
  }

  createInput(): Input {
    return new DarkInput();
  }
}

// Usage
function createUI(factory: UIFactory): void {
  const button = factory.createButton();
  const input = factory.createInput();

  console.log(button.render());
  console.log(input.render());
}

const lightFactory = new LightThemeFactory();
createUI(lightFactory);

const darkFactory = new DarkThemeFactory();
createUI(darkFactory);
```

### Factory with Configuration

```typescript
interface Database {
  connect(): Promise<void>;
  query<T>(sql: string): Promise<T[]>;
  disconnect(): Promise<void>;
}

class PostgreSQLDatabase implements Database {
  async connect(): Promise<void> {
    console.log('Connecting to PostgreSQL...');
  }

  async query<T>(sql: string): Promise<T[]> {
    console.log(`PostgreSQL query: ${sql}`);
    return [];
  }

  async disconnect(): Promise<void> {
    console.log('Disconnecting from PostgreSQL...');
  }
}

class MySQLDatabase implements Database {
  async connect(): Promise<void> {
    console.log('Connecting to MySQL...');
  }

  async query<T>(sql: string): Promise<T[]> {
    console.log(`MySQL query: ${sql}`);
    return [];
  }

  async disconnect(): Promise<void> {
    console.log('Disconnecting from MySQL...');
  }
}

class MongoDatabase implements Database {
  async connect(): Promise<void> {
    console.log('Connecting to MongoDB...');
  }

  async query<T>(sql: string): Promise<T[]> {
    console.log(`MongoDB query: ${sql}`);
    return [];
  }

  async disconnect(): Promise<void> {
    console.log('Disconnecting from MongoDB...');
  }
}

// Factory with configuration
class DatabaseFactory {
  private static databases: Map<string, Database> = new Map();

  static create(type: 'postgresql' | 'mysql' | 'mongodb'): Database {
    if (this.databases.has(type)) {
      return this.databases.get(type)!;
    }

    let database: Database;

    switch (type) {
      case 'postgresql':
        database = new PostgreSQLDatabase();
        break;
      case 'mysql':
        database = new MySQLDatabase();
        break;
      case 'mongodb':
        database = new MongoDatabase();
        break;
      default:
        throw new Error(`Unknown database type: ${type}`);
    }

    this.databases.set(type, database);
    return database;
  }

  static reset(): void {
    this.databases.clear();
  }
}

// Usage
const db = DatabaseFactory.create('postgresql');
await db.connect();
await db.query('SELECT * FROM users');
await db.disconnect();
```

### Factory with Dependency Injection

```typescript
// Service interfaces
interface EmailService {
  sendEmail(to: string, subject: string, body: string): Promise<void>;
}

interface SMSService {
  sendSMS(phone: string, message: string): Promise<void>;
}

interface PushService {
  sendPush(userId: string, title: string, body: string): Promise<void>;
}

// Implementations
class SendGridEmailService implements EmailService {
  async sendEmail(to: string, subject: string, body: string): Promise<void> {
    console.log(`SendGrid: Sending email to ${to}`);
  }
}

class TwilioSMSService implements SMSService {
  async sendSMS(phone: string, message: string): Promise<void> {
    console.log(`Twilio: Sending SMS to ${phone}`);
  }
}

class FirebasePushService implements PushService {
  async sendPush(userId: string, title: string, body: string): Promise<void> {
    console.log(`Firebase: Sending push to ${userId}`);
  }
}

// Factory
class NotificationServiceFactory {
  static createEmailService(provider: 'sendgrid' | 'ses'): EmailService {
    switch (provider) {
      case 'sendgrid':
        return new SendGridEmailService();
      case 'ses':
        // Would return SESEmailService
        throw new Error('SES not implemented');
      default:
        throw new Error(`Unknown email provider: ${provider}`);
    }
  }

  static createSMSService(provider: 'twilio' | 'nexmo'): SMSService {
    switch (provider) {
      case 'twilio':
        return new TwilioSMSService();
      case 'nexmo':
        // Would return NexmoSMSService
        throw new Error('Nexmo not implemented');
      default:
        throw new Error(`Unknown SMS provider: ${provider}`);
    }
  }

  static createPushService(provider: 'firebase' | 'onesignal'): PushService {
    switch (provider) {
      case 'firebase':
        return new FirebasePushService();
      case 'onesignal':
        // Would return OneSignalPushService
        throw new Error('OneSignal not implemented');
      default:
        throw new Error(`Unknown push provider: ${provider}`);
    }
  }
}

// Usage
const emailService = NotificationServiceFactory.createEmailService('sendgrid');
await emailService.sendEmail('user@example.com', 'Welcome!', 'Hello there!');
```

## Real-World Use Cases

### 1. API Response Factory

```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: Date;
}

class APIResponseFactory {
  static success<T>(data: T): ApiResponse<T> {
    return {
      success: true,
      data,
      timestamp: new Date()
    };
  }

  static error<T>(error: string): ApiResponse<T> {
    return {
      success: false,
      error,
      timestamp: new Date()
    };
  }

  static paginated<T>(data: T[], total: number, page: number, limit: number): ApiResponse<{
    items: T[];
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  }> {
    return {
      success: true,
      data: {
        items: data,
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit)
      },
      timestamp: new Date()
    };
  }
}

// Usage
const response = APIResponseFactory.success({ id: 1, name: 'John' });
const errorResponse = APIResponseFactory.error('Not found');
const paginatedResponse = APIResponseFactory.paginated([1, 2, 3], 100, 1, 10);
```

### 2. Payment Processor Factory

```typescript
interface PaymentProcessor {
  charge(amount: number, currency: string): Promise<{ success: boolean; transactionId: string }>;
  refund(transactionId: string, amount: number): Promise<{ success: boolean }>;
}

class StripeProcessor implements PaymentProcessor {
  async charge(amount: number, currency: string) {
    console.log(`Stripe: Charging ${amount} ${currency}`);
    return { success: true, transactionId: 'stripe_' + Date.now() };
  }

  async refund(transactionId: string, amount: number) {
    console.log(`Stripe: Refunding ${amount} for ${transactionId}`);
    return { success: true };
  }
}

class PayPalProcessor implements PaymentProcessor {
  async charge(amount: number, currency: string) {
    console.log(`PayPal: Charging ${amount} ${currency}`);
    return { success: true, transactionId: 'paypal_' + Date.now() };
  }

  async refund(transactionId: string, amount: number) {
    console.log(`PayPal: Refunding ${amount} for ${transactionId}`);
    return { success: true };
  }
}

class PaymentProcessorFactory {
  static create(provider: 'stripe' | 'paypal'): PaymentProcessor {
    switch (provider) {
      case 'stripe':
        return new StripeProcessor();
      case 'paypal':
        return new PayPalProcessor();
      default:
        throw new Error(`Unknown payment provider: ${provider}`);
    }
  }
}

// Usage
const processor = PaymentProcessorFactory.create('stripe');
const result = await processor.charge(100, 'USD');
```

### 3. Document Generator Factory

```typescript
interface DocumentGenerator {
  generate(data: Record<string, any>): Buffer;
  getExtension(): string;
  getMimeType(): string;
}

class PDFGenerator implements DocumentGenerator {
  generate(data: Record<string, any>): Buffer {
    console.log('Generating PDF...');
    return Buffer.from('PDF content');
  }

  getExtension(): string {
    return 'pdf';
  }

  getMimeType(): string {
    return 'application/pdf';
  }
}

class ExcelGenerator implements DocumentGenerator {
  generate(data: Record<string, any>): Buffer {
    console.log('Generating Excel...');
    return Buffer.from('Excel content');
  }

  getExtension(): string {
    return 'xlsx';
  }

  getMimeType(): string {
    return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  }
}

class DocumentFactory {
  static create(type: 'pdf' | 'excel'): DocumentGenerator {
    switch (type) {
      case 'pdf':
        return new PDFGenerator();
      case 'excel':
        return new ExcelGenerator();
      default:
        throw new Error(`Unknown document type: ${type}`);
    }
  }
}

// Usage
const generator = DocumentFactory.create('pdf');
const buffer = generator.generate({ title: 'Report', data: [1, 2, 3] });
console.log(generator.getMimeType()); // 'application/pdf'
```

## Common Mistakes

### 1. Too Many Factory Classes

```typescript
// ❌ BAD - Creating a factory for every simple class
class UserServiceFactory {
  static create(): UserService {
    return new UserService();
  }
}

class OrderServiceFactory {
  static create(): OrderService {
    return new OrderService();
  }
}

// These factories don't add value - just use the classes directly
```

### 2. Factory Doing Too Much

```typescript
// ❌ BAD - Factory with too many responsibilities
class MegaFactory {
  static create(type: string) {
    // Also handles validation, configuration, logging...
    // Violates Single Responsibility Principle
  }
}
```

### 3. Not Using Interface

```typescript
// ❌ BAD - No common interface
class CarFactory {
  static create(): any {  // Should return Vehicle interface
    return new Car();
  }
}
```

### 4. Hardcoded Factory Logic

```typescript
// ❌ BAD - Hardcoded creation logic
class NotificationFactory {
  static create(type: string): any {
    if (type === 'email') {
      return new EmailNotification();
    }
    // This is okay, but could be more flexible
  }
}
```

## Best Practices

### 1. Use Interface for Products

```typescript
// ✅ GOOD - Common interface
interface Product {
  operation(): string;
}

class ConcreteProductA implements Product {
  operation(): string {
    return 'Product A';
  }
}

class ConcreteProductB implements Product {
  operation(): string {
    return 'Product B';
  }
}
```

### 2. Keep Factory Focused

```typescript
// ✅ GOOD - Single responsibility
class ProductFactory {
  static create(type: 'a' | 'b'): Product {
    switch (type) {
      case 'a':
        return new ConcreteProductA();
      case 'b':
        return new ConcreteProductB();
      default:
        throw new Error(`Unknown product type: ${type}`);
    }
  }
}
```

### 3. Use Dependency Injection

```typescript
// ✅ GOOD - Injectable factory
class ServiceFactory {
  constructor(private config: AppConfig) {}

  create(type: string): Service {
    // Use this.config to configure the service
    switch (type) {
      case 'email':
        return new EmailService(this.config.email);
      default:
        throw new Error(`Unknown service type: ${type}`);
    }
  }
}
```

### 4. Consider Registration Pattern

```typescript
// ✅ GOOD - Flexible registration
class Factory {
  private static creators: Map<string, () => any> = new Map();

  static register(name: string, creator: () => any): void {
    Factory.creators.set(name, creator);
  }

  static create(name: string): any {
    const creator = Factory.creators.get(name);
    if (!creator) {
      throw new Error(`Unknown product: ${name}`);
    }
    return creator();
  }
}

// Usage
Factory.register('email', () => new EmailNotification());
Factory.register('sms', () => new SMSNotification());
```

## Performance Considerations

1. **Object Creation Overhead**: Factories add a layer of indirection, which has minimal performance impact.

2. **Caching**: Consider caching frequently created objects if they're expensive to create.

3. **Lazy Loading**: Use lazy initialization in factories to defer object creation until needed.

4. **Memory Usage**: Factories should be stateless to avoid memory leaks.

5. **Compilation Time**: TypeScript generics and interfaces add compile-time safety with no runtime cost.

## Interview Questions

### Beginner

1. **What is the Factory pattern?**
   - A creational pattern that provides an interface for creating objects without specifying concrete classes.

2. **What's the difference between Simple Factory and Factory Method?**
   - Simple Factory uses a single method; Factory Method uses subclasses to create objects.

3. **When would you use a Factory?**
   - When object creation is complex, involves multiple steps, or needs to be flexible.

4. **What are the benefits of Factory pattern?**
   - Loose coupling, easier maintenance, better testability, and flexibility.

5. **How do you implement a Simple Factory in TypeScript?**
   - Use a static method with a switch statement to create different object types.

### Intermediate

6. **What's the difference between Factory and Abstract Factory?**
   - Factory creates one product type; Abstract Factory creates families of related products.

7. **How do you handle errors in Factory pattern?**
   - Throw descriptive errors for unknown types, validate inputs, and handle creation failures.

8. **Can you use Factory with dependency injection?**
   - Yes, inject the factory or its dependencies to make it testable and configurable.

9. **How do you test Factory pattern?**
   - Mock the factory, test each product independently, verify factory returns correct types.

10. **What are the SOLID violations with Factory?**
    - Open/Closed Principle violations if not designed properly.

### Senior

11. **How does Factory pattern affect scalability?**
    - Factories can be extended easily; consider registration patterns for large systems.

12. **What's the relationship between Factory and Strategy patterns?**
    - Factory creates objects; Strategy defines algorithms; they can be combined.

13. **How do you handle Factory in microservices?**
    - Each service can have its own factories; avoid shared factories across services.

14. **What are the memory implications of Factory?**
    - Factories are usually stateless; the created objects consume memory.

15. **How do you refactor Factory code?**
    - Extract common logic, use registration pattern, and apply SOLID principles.

### FAANG-style

16. **Design a Factory for a plugin system.**
    - Consider dynamic loading, registration, lifecycle management, and isolation.

17. **How would you implement Factory for distributed systems?**
    - Consider remote object creation, serialization, and network transparency.

18. **What are the implications of Factory in cloud-native applications?**
    - Consider serverless cold starts, container scaling, and resource management.

19. **How do you handle Factory in event-driven architectures?**
    - Use factories to create event handlers, producers, and consumers.

20. **Design a Factory that supports multiple configurations.**
    - Consider configuration injection, environment-specific factories, and feature flags.

### Follow-ups

21. **Can Factory pattern be combined with other patterns?**
    - Yes, commonly with Singleton, Abstract Factory, and Prototype patterns.

22. **How do you handle Factory in testing frameworks?**
    - Use dependency injection, create test factories, and mock object creation.

23. **What are the memory implications of Factory pattern?**
    - Factories are usually lightweight; the created objects consume memory.

24. **How do you handle Factory in serverless environments?**
    - Consider cold starts, instance reuse, and stateless factory design.

25. **What's the impact of Factory on code maintainability?**
    - Improves maintainability by centralizing creation logic and reducing coupling.

## Summary

The Factory pattern is essential for creating objects without specifying concrete classes. It promotes loose coupling, improves testability, and makes code more maintainable. Use Simple Factory for basic creation, Factory Method for subclass-based creation, and Abstract Factory for creating families of related objects.

## Cheat Sheet

```text
┌─────────────────────────────────────────────┐
│           FACTORY PATTERN                   │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Complex object creation                   │
│ • Need flexibility in object types          │
│ • Multiple related products                 │
│ • Decouple creation from usage              │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Simple object creation                    │
│ • Only one product type                     │
│ • Factory adds unnecessary complexity       │
│ • Performance is critical                   │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Product interface                         │
│ • Factory method/class                      │
│ • Concrete products                         │
│ • Creation logic encapsulation              │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Too many factory classes                  │
│ • Factory doing too much                    │
│ • Not using interfaces                      │
│ • Hardcoded creation logic                  │
├─────────────────────────────────────────────┤
│ 🔧 VARIANTS:                               │
│ • Simple Factory                            │
│ • Factory Method                            │
│ • Abstract Factory                          │
│ • Registration Factory                      │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Refactoring Guru: Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)
