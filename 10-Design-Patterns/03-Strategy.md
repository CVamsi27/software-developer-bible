# Strategy Pattern

## Definition

The Strategy pattern is a behavioral design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from clients that use it.

The pattern is particularly useful when you have multiple algorithms for a specific task and want to switch between them dynamically at runtime.

## Why Do We Need It?

Without the Strategy pattern, algorithms are often implemented with conditional statements, leading to:

1. **Code duplication**: Similar algorithms repeated in different places
2. **Violation of Open/Closed Principle**: Adding new algorithms requires modifying existing code
3. **Complex conditionals**: Large switch/case or if/else chains
4. **Difficult testing**: Hard to test individual algorithms in isolation

## How It Works

The Strategy pattern works by:

1. Defining a common interface for all algorithms
2. Implementing each algorithm as a separate class
3. Keeping a reference to the current strategy in the context
4. Allowing the strategy to be changed at runtime

```
┌─────────────────────────────────────────────────┐
│              Strategy Pattern                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐                               │
│  │   Context     │◄── Uses strategy              │
│  └──────────────┘                               │
│         │                                       │
│         ▼                                       │
│  ┌──────────────────────────────────────────┐   │
│  │         Strategy Interface               │   │
│  │    + execute(data): Result               │   │
│  └──────────────────────────────────────────┘   │
│         │                                       │
│    ┌────┴────┬────────────┐                    │
│    ▼         ▼            ▼                    │
│ ┌──────┐ ┌──────┐   ┌──────┐                  │
│ │StratA│ │StratB│   │StratC│                  │
│ └──────┘ └──────┘   └──────┘                  │
│                                                  │
│  Context can switch between strategies           │
│  at runtime                                      │
└─────────────────────────────────────────────────┘
```

## Code Examples

### Basic Strategy Pattern

```typescript
// Strategy interface
interface SortStrategy<T> {
  sort(data: T[]): T[];
  getName(): string;
}

// Concrete strategies
class BubbleSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    const arr = [...data];
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }
    return arr;
  }

  getName(): string {
    return 'Bubble Sort';
  }
}

class QuickSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    const arr = [...data];
    if (arr.length <= 1) return arr;

    const pivot = arr[0];
    const left = arr.slice(1).filter(x => x <= pivot);
    const right = arr.slice(1).filter(x => x > pivot);

    return [...this.sort(left), pivot, ...this.sort(right)];
  }

  getName(): string {
    return 'Quick Sort';
  }
}

class MergeSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    const arr = [...data];
    if (arr.length <= 1) return arr;

    const mid = Math.floor(arr.length / 2);
    const left = this.sort(arr.slice(0, mid));
    const right = this.sort(arr.slice(mid));

    return this.merge(left, right);
  }

  private merge(left: T[], right: T[]): T[] {
    const result: T[] = [];
    let i = 0, j = 0;

    while (i < left.length && j < right.length) {
      if (left[i] <= right[j]) {
        result.push(left[i++]);
      } else {
        result.push(right[j++]);
      }
    }

    return result.concat(left.slice(i), right.slice(j));
  }

  getName(): string {
    return 'Merge Sort';
  }
}

// Context
class Sorter<T> {
  private strategy: SortStrategy<T>;

  constructor(strategy: SortStrategy<T>) {
    this.strategy = strategy;
  }

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
  }

  sort(data: T[]): T[] {
    console.log(`Sorting with ${this.strategy.getName()}`);
    return this.strategy.sort(data);
  }
}

// Usage
const sorter = new Sorter(new QuickSort<number>());
const sorted = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6]);
console.log(sorted); // [1, 1, 2, 3, 4, 5, 6, 9]

// Switch strategy at runtime
sorter.setStrategy(new BubbleSort<number>());
const sortedAgain = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6]);
console.log(sortedAgain); // [1, 1, 2, 3, 4, 5, 6, 9]
```

### Payment Strategy Pattern

```typescript
// Strategy interface
interface PaymentStrategy {
  pay(amount: number): Promise<PaymentResult>;
  getPaymentMethod(): string;
}

interface PaymentResult {
  success: boolean;
  transactionId: string;
  message: string;
}

// Concrete strategies
class CreditCardPayment implements PaymentStrategy {
  private cardNumber: string;
  private cvv: string;

  constructor(cardNumber: string, cvv: string) {
    this.cardNumber = cardNumber;
    this.cvv = cvv;
  }

  async pay(amount: number): Promise<PaymentResult> {
    console.log(`Processing credit card payment of $${amount}`);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    return {
      success: true,
      transactionId: 'cc_' + Date.now(),
      message: 'Credit card payment successful'
    };
  }

  getPaymentMethod(): string {
    return 'Credit Card';
  }
}

class PayPalPayment implements PaymentStrategy {
  private email: string;

  constructor(email: string) {
    this.email = email;
  }

  async pay(amount: number): Promise<PaymentResult> {
    console.log(`Processing PayPal payment of $${amount} for ${this.email}`);
    await new Promise(resolve => setTimeout(resolve, 1000));

    return {
      success: true,
      transactionId: 'pp_' + Date.now(),
      message: 'PayPal payment successful'
    };
  }

  getPaymentMethod(): string {
    return 'PayPal';
  }
}

class BankTransferPayment implements PaymentStrategy {
  private accountNumber: string;
  private routingNumber: string;

  constructor(accountNumber: string, routingNumber: string) {
    this.accountNumber = accountNumber;
    this.routingNumber = routingNumber;
  }

  async pay(amount: number): Promise<PaymentResult> {
    console.log(`Processing bank transfer of $${amount}`);
    await new Promise(resolve => setTimeout(resolve, 2000));

    return {
      success: true,
      transactionId: 'bt_' + Date.now(),
      message: 'Bank transfer initiated'
    };
  }

  getPaymentMethod(): string {
    return 'Bank Transfer';
  }
}

// Context
class ShoppingCart {
  private items: Array<{ name: string; price: number }> = [];
  private paymentStrategy: PaymentStrategy | null = null;

  addItem(name: string, price: number): void {
    this.items.push({ name, price });
  }

  setPaymentStrategy(strategy: PaymentStrategy): void {
    this.paymentStrategy = strategy;
  }

  getTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  async checkout(): Promise<PaymentResult> {
    if (!this.paymentStrategy) {
      throw new Error('No payment method selected');
    }

    const total = this.getTotal();
    console.log(`Checking out ${this.items.length} items for $${total}`);

    return this.paymentStrategy.pay(total);
  }
}

// Usage
const cart = new ShoppingCart();
cart.addItem('Laptop', 999);
cart.addItem('Mouse', 29);

// Use credit card
cart.setPaymentStrategy(new CreditCardPayment('1234-5678-9012-3456', '123'));
await cart.checkout();

// Switch to PayPal
cart.setPaymentStrategy(new PayPalPayment('user@example.com'));
await cart.checkout();
```

### Notification Strategy Pattern

```typescript
// Strategy interface
interface NotificationStrategy {
  send(notification: Notification): Promise<boolean>;
  getName(): string;
}

interface Notification {
  title: string;
  message: string;
  priority: 'low' | 'medium' | 'high';
}

// Concrete strategies
class EmailNotificationStrategy implements NotificationStrategy {
  async send(notification: Notification): Promise<boolean> {
    console.log(`[EMAIL] ${notification.title}: ${notification.message}`);
    // Simulate email sending
    return true;
  }

  getName(): string {
    return 'Email';
  }
}

class SlackNotificationStrategy implements NotificationStrategy {
  async send(notification: Notification): Promise<boolean> {
    console.log(`[SLACK] ${notification.title}: ${notification.message}`);
    // Simulate Slack API call
    return true;
  }

  getName(): string {
    return 'Slack';
  }
}

class SMSNotificationStrategy implements NotificationStrategy {
  async send(notification: Notification): Promise<boolean> {
    console.log(`[SMS] ${notification.title}: ${notification.message}`);
    // Simulate SMS sending
    return true;
  }

  getName(): string {
    return 'SMS';
  }
}

class PushNotificationStrategy implements NotificationStrategy {
  async send(notification: Notification): Promise<boolean> {
    console.log(`[PUSH] ${notification.title}: ${notification.message}`);
    // Simulate push notification
    return true;
  }

  getName(): string {
    return 'Push';
  }
}

// Context
class NotificationService {
  private strategies: Map<string, NotificationStrategy> = new Map();
  private defaultStrategy: NotificationStrategy;

  constructor(defaultStrategy: NotificationStrategy) {
    this.defaultStrategy = defaultStrategy;
  }

  registerStrategy(name: string, strategy: NotificationStrategy): void {
    this.strategies.set(name, strategy);
  }

  setDefaultStrategy(strategy: NotificationStrategy): void {
    this.defaultStrategy = strategy;
  }

  async send(notification: Notification, strategyName?: string): Promise<boolean> {
    const strategy = strategyName
      ? this.strategies.get(strategyName)
      : this.defaultStrategy;

    if (!strategy) {
      throw new Error(`Strategy ${strategyName} not found`);
    }

    console.log(`Sending via ${strategy.getName()}`);
    return strategy.send(notification);
  }

  async sendToAll(notification: Notification): Promise<boolean[]> {
    const results: boolean[] = [];

    for (const strategy of this.strategies.values()) {
      const result = await strategy.send(notification);
      results.push(result);
    }

    return results;
  }
}

// Usage
const notificationService = new NotificationService(new EmailNotificationStrategy());
notificationService.registerStrategy('slack', new SlackNotificationStrategy());
notificationService.registerStrategy('sms', new SMSNotificationStrategy());
notificationService.registerStrategy('push', new PushNotificationStrategy());

const notification: Notification = {
  title: 'Order Shipped',
  message: 'Your order #12345 has been shipped',
  priority: 'high'
};

// Send via default (email)
await notificationService.send(notification);

// Send via specific strategy
await notificationService.send(notification, 'slack');

// Send via all strategies
await notificationService.sendToAll(notification);
```

### Discount Strategy Pattern

```typescript
// Strategy interface
interface DiscountStrategy {
  calculateDiscount(amount: number, context?: any): number;
  getName(): string;
  getMinAmount(): number;
}

// Concrete strategies
class NoDiscount implements DiscountStrategy {
  calculateDiscount(amount: number): number {
    return 0;
  }

  getName(): string {
    return 'No Discount';
  }

  getMinAmount(): number {
    return 0;
  }
}

class PercentageDiscount implements DiscountStrategy {
  private percentage: number;

  constructor(percentage: number) {
    this.percentage = percentage;
  }

  calculateDiscount(amount: number): number {
    return amount * (this.percentage / 100);
  }

  getName(): string {
    return `${this.percentage}% Discount`;
  }

  getMinAmount(): number {
    return 0;
  }
}

class FixedAmountDiscount implements DiscountStrategy {
  private discountAmount: number;
  private minAmount: number;

  constructor(discountAmount: number, minAmount: number) {
    this.discountAmount = discountAmount;
    this.minAmount = minAmount;
  }

  calculateDiscount(amount: number): number {
    if (amount >= this.minAmount) {
      return this.discountAmount;
    }
    return 0;
  }

  getName(): string {
    return `$${this.discountAmount} off (min $${this.minAmount})`;
  }

  getMinAmount(): number {
    return this.minAmount;
  }
}

class BuyOneGetOneFree implements DiscountStrategy {
  calculateDiscount(amount: number, context?: any): number {
    // Assuming context contains item count
    const itemCount = context?.itemCount || 1;
    const freeItems = Math.floor(itemCount / 2);
    const averagePrice = amount / itemCount;
    return freeItems * averagePrice;
  }

  getName(): string {
    return 'Buy One Get One Free';
  }

  getMinAmount(): number {
    return 0;
  }
}

// Context
class Order {
  private items: Array<{ name: string; price: number; quantity: number }> = [];
  private discountStrategy: DiscountStrategy;

  constructor(discountStrategy: DiscountStrategy = new NoDiscount()) {
    this.discountStrategy = discountStrategy;
  }

  addItem(name: string, price: number, quantity: number = 1): void {
    this.items.push({ name, price, quantity });
  }

  setDiscountStrategy(strategy: DiscountStrategy): void {
    this.discountStrategy = strategy;
  }

  getSubtotal(): number {
    return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  }

  getItemCount(): number {
    return this.items.reduce((sum, item) => sum + item.quantity, 0);
  }

  getDiscount(): number {
    const subtotal = this.getSubtotal();
    const context = { itemCount: this.getItemCount() };
    return this.discountStrategy.calculateDiscount(subtotal, context);
  }

  getTotal(): number {
    return this.getSubtotal() - this.getDiscount();
  }

  getSummary(): string {
    return `
Order Summary:
- Items: ${this.getItemCount()}
- Subtotal: $${this.getSubtotal().toFixed(2)}
- Discount (${this.discountStrategy.getName()}): -$${this.getDiscount().toFixed(2)}
- Total: $${this.getTotal().toFixed(2)}
    `.trim();
  }
}

// Usage
const order = new Order();
order.addItem('Laptop', 999);
order.addItem('Mouse', 29);
order.addItem('Keyboard', 79);

console.log(order.getSummary());

// Apply percentage discount
order.setDiscountStrategy(new PercentageDiscount(10));
console.log(order.getSummary());

// Apply fixed amount discount
order.setDiscountStrategy(new FixedAmountDiscount(50, 100));
console.log(order.getSummary());
```

## Real-World Use Cases

### 1. Authentication Strategy

```typescript
interface AuthStrategy {
  authenticate(credentials: any): Promise<User | null>;
  getName(): string;
}

class JWTAuthStrategy implements AuthStrategy {
  async authenticate(credentials: { token: string }): Promise<User | null> {
    console.log('Authenticating with JWT...');
    // Validate JWT token
    return { id: '1', name: 'John' };
  }

  getName(): string {
    return 'JWT';
  }
}

class OAuthStrategy implements AuthStrategy {
  async authenticate(credentials: { provider: string; code: string }): Promise<User | null> {
    console.log(`Authenticating with OAuth ${credentials.provider}...`);
    // Exchange code for token, get user info
    return { id: '2', name: 'Jane' };
  }

  getName(): string {
    return 'OAuth';
  }
}

class APIKeyStrategy implements AuthStrategy {
  async authenticate(credentials: { apiKey: string }): Promise<User | null> {
    console.log('Authenticating with API Key...');
    // Validate API key
    return { id: '3', name: 'API User' };
  }

  getName(): string {
    return 'API Key';
  }
}

interface User {
  id: string;
  name: string;
}

class AuthService {
  private strategies: Map<string, AuthStrategy> = new Map();

  registerStrategy(name: string, strategy: AuthStrategy): void {
    this.strategies.set(name, strategy);
  }

  async login(strategyName: string, credentials: any): Promise<User | null> {
    const strategy = this.strategies.get(strategyName);
    if (!strategy) {
      throw new Error(`Auth strategy ${strategyName} not found`);
    }

    return strategy.authenticate(credentials);
  }
}
```

### 2. Data Validation Strategy

```typescript
interface ValidationStrategy {
  validate(data: any): ValidationResult;
  getName(): string;
}

interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

class RequiredFieldValidation implements ValidationStrategy {
  validate(data: any): ValidationResult {
    const errors: string[] = [];

    if (!data || Object.keys(data).length === 0) {
      errors.push('Data is required');
    }

    return { isValid: errors.length === 0, errors };
  }

  getName(): string {
    return 'Required Field';
  }
}

class EmailValidation implements ValidationStrategy {
  validate(data: { email: string }): ValidationResult {
    const errors: string[] = [];
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!data.email || !emailRegex.test(data.email)) {
      errors.push('Invalid email format');
    }

    return { isValid: errors.length === 0, errors };
  }

  getName(): string {
    return 'Email';
  }
}

class PasswordValidation implements ValidationStrategy {
  private minLength: number;

  constructor(minLength: number = 8) {
    this.minLength = minLength;
  }

  validate(data: { password: string }): ValidationResult {
    const errors: string[] = [];

    if (!data.password || data.password.length < this.minLength) {
      errors.push(`Password must be at least ${this.minLength} characters`);
    }

    if (!/[A-Z]/.test(data.password)) {
      errors.push('Password must contain at least one uppercase letter');
    }

    if (!/[0-9]/.test(data.password)) {
      errors.push('Password must contain at least one number');
    }

    return { isValid: errors.length === 0, errors };
  }

  getName(): string {
    return 'Password';
  }
}

class ValidationService {
  private strategies: ValidationStrategy[] = [];

  addStrategy(strategy: ValidationStrategy): void {
    this.strategies.push(strategy);
  }

  validate(data: any): ValidationResult {
    const allErrors: string[] = [];

    for (const strategy of this.strategies) {
      const result = strategy.validate(data);
      if (!result.isValid) {
        allErrors.push(...result.errors);
      }
    }

    return {
      isValid: allErrors.length === 0,
      errors: allErrors
    };
  }
}
```

### 3. Compression Strategy

```typescript
interface CompressionStrategy {
  compress(data: Buffer): Buffer;
  decompress(data: Buffer): Buffer;
  getName(): string;
}

class GzipCompression implements CompressionStrategy {
  compress(data: Buffer): Buffer {
    console.log('Compressing with Gzip...');
    // Simulate gzip compression
    return data;
  }

  decompress(data: Buffer): Buffer {
    console.log('Decompressing with Gzip...');
    return data;
  }

  getName(): string {
    return 'Gzip';
  }
}

class DeflateCompression implements CompressionStrategy {
  compress(data: Buffer): Buffer {
    console.log('Compressing with Deflate...');
    return data;
  }

  decompress(data: Buffer): Buffer {
    console.log('Decompressing with Deflate...');
    return data;
  }

  getName(): string {
    return 'Deflate';
  }
}

class BrotliCompression implements CompressionStrategy {
  compress(data: Buffer): Buffer {
    console.log('Compressing with Brotli...');
    return data;
  }

  decompress(data: Buffer): Buffer {
    console.log('Decompressing with Brotli...');
    return data;
  }

  getName(): string {
    return 'Brotli';
  }
}

class FileCompressor {
  private strategy: CompressionStrategy;

  constructor(strategy: CompressionStrategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy: CompressionStrategy): void {
    this.strategy = strategy;
  }

  compressFile(data: Buffer): Buffer {
    console.log(`Compressing file with ${this.strategy.getName()}`);
    return this.strategy.compress(data);
  }

  decompressFile(data: Buffer): Buffer {
    console.log(`Decompressing file with ${this.strategy.getName()}`);
    return this.strategy.decompress(data);
  }
}
```

## Common Mistakes

### 1. Creating Too Many Strategies

```typescript
// ❌ BAD - Creating a strategy for every tiny variation
class EmailStrategy1 implements NotificationStrategy { ... }
class EmailStrategy2 implements NotificationStrategy { ... }
class EmailStrategy3 implements NotificationStrategy { ... }

// These could be combined with configuration
```

### 2. Not Using Interface

```typescript
// ❌ BAD - No common interface
class BubbleSort {
  sort(data: number[]): number[] { ... }
}

class QuickSort {
  sort(data: number[]): number[] { ... }
}

// Should implement a common SortStrategy interface
```

### 3. Strategy with Too Much State

```typescript
// ❌ BAD - Strategy with complex state
class ComplexStrategy {
  private state: any;
  private dependencies: any[];

  // This makes the strategy hard to use and test
}
```

### 4. Not Providing Default Strategy

```typescript
// ❌ BAD - No default strategy
class Context {
  private strategy: Strategy | null = null;

  execute() {
    if (!this.strategy) {
      throw new Error('No strategy set');
    }
    // Should have a default strategy
  }
}
```

## Best Practices

### 1. Use Interface for All Strategies

```typescript
// ✅ GOOD - Common interface
interface Strategy {
  execute(data: any): any;
  getName(): string;
}
```

### 2. Keep Strategies Stateless

```typescript
// ✅ GOOD - Stateless strategy
class SimpleStrategy implements Strategy {
  execute(data: any): any {
    // No instance variables, pure function
    return data.map(item => item * 2);
  }

  getName(): string {
    return 'Simple';
  }
}
```

### 3. Provide Default Strategy

```typescript
// ✅ GOOD - Default strategy
class Context {
  private strategy: Strategy;

  constructor(strategy: Strategy = new DefaultStrategy()) {
    this.strategy = strategy;
  }
}
```

### 4. Use Factory for Strategy Creation

```typescript
// ✅ GOOD - Factory for strategies
class StrategyFactory {
  static create(type: string): Strategy {
    switch (type) {
      case 'a': return new StrategyA();
      case 'b': return new StrategyB();
      default: return new DefaultStrategy();
    }
  }
}
```

## Performance Considerations

1. **Strategy Selection**: The overhead of selecting a strategy is minimal compared to the algorithm's execution time.

2. **Memory Usage**: Stateless strategies are lightweight. Avoid strategies with heavy dependencies.

3. **Caching**: If strategies are expensive to create, consider caching them.

4. **Inlining**: TypeScript/JavaScript engines can inline simple strategy methods.

5. **Garbage Collection**: Stateless strategies don't create GC pressure.

## Interview Questions

### Beginner

1. **What is the Strategy pattern?**
   - A behavioral pattern that defines a family of algorithms and makes them interchangeable.

2. **When would you use Strategy pattern?**
   - When you have multiple algorithms for a task and want to switch between them dynamically.

3. **What's the difference between Strategy and State patterns?**
   - Strategy swaps algorithms; State changes behavior based on internal state.

4. **How do you implement Strategy in TypeScript?**
   - Define a common interface, implement concrete strategies, and use a context to switch between them.

5. **What are the benefits of Strategy pattern?**
   - Open/Closed Principle, better testability, and runtime flexibility.

### Intermediate

6. **How do you handle strategy selection?**
   - Use configuration, user input, or factory pattern to select strategies.

7. **Can strategies have state?**
   - Yes, but prefer stateless strategies for simplicity and testability.

8. **How do you test Strategy pattern?**
   - Test each strategy independently, mock strategies in context tests.

9. **What's the relationship between Strategy and Factory?**
   - Factory creates objects; Strategy defines algorithms; they can be combined.

10. **How do you handle strategy errors?**
    - Define error handling in each strategy or use a wrapper/decorator.

### Senior

11. **How does Strategy pattern affect scalability?**
    - New strategies can be added without modifying existing code.

12. **What are the SOLID violations with Strategy?**
    - Usually follows SOLID; watch for context violating Single Responsibility.

13. **How do you handle Strategy in microservices?**
    - Strategies can be in the same service or separate services depending on coupling.

14. **What are the memory implications of Strategy?**
    - Stateless strategies are lightweight; strategies with dependencies consume more memory.

15. **How do you refactor Strategy code?**
    - Extract common logic, use composition, and apply SOLID principles.

### FAANG-style

16. **Design a Strategy for load balancing algorithms.**
    - Consider round-robin, least connections, IP hash, and dynamic switching.

17. **How would you implement Strategy for distributed systems?**
    - Consider remote strategy execution, serialization, and fault tolerance.

18. **What are the implications of Strategy in cloud-native applications?**
    - Consider serverless execution, container scaling, and resource management.

19. **How do you handle Strategy in event-driven architectures?**
    - Use strategies for event processing, routing, and transformation.

20. **Design a Strategy that supports A/B testing.**
    - Consider traffic splitting, metrics collection, and gradual rollout.

### Follow-ups

21. **Can Strategy pattern be combined with other patterns?**
    - Yes, commonly with Factory, Decorator, and State patterns.

22. **How do you handle Strategy in testing frameworks?**
    - Use dependency injection, create test strategies, and mock implementations.

23. **What are the memory implications of Strategy pattern?**
    - Stateless strategies are lightweight; the context holds the reference.

24. **How do you handle Strategy in serverless environments?**
    - Consider cold starts, stateless design, and function composition.

25. **What's the impact of Strategy on code maintainability?**
    - Improves maintainability by separating algorithms and reducing conditionals.

## Summary

The Strategy pattern is powerful for encapsulating algorithms and making them interchangeable. It promotes the Open/Closed Principle, improves testability, and allows runtime flexibility. Use it when you have multiple algorithms for a task and want to switch between them dynamically.

## Cheat Sheet

```
┌─────────────────────────────────────────────┐
│           STRATEGY PATTERN                  │
├─────────────────────────────────────────────┤
│ ✅ USE WHEN:                                │
│ • Multiple algorithms for a task            │
│ • Need runtime algorithm switching          │
│ • Avoid conditional complexity              │
│ • Want to test algorithms separately        │
├─────────────────────────────────────────────┤
│ ❌ AVOID WHEN:                              │
│ • Only one algorithm exists                 │
│ • Algorithms rarely change                  │
│ • Strategy adds unnecessary complexity      │
│ • Performance is critical                   │
├─────────────────────────────────────────────┤
│ 🎯 KEY CONCEPTS:                           │
│ • Strategy interface                        │
│ • Concrete strategies                       │
│ • Context holds strategy                    │
│ • Runtime switching                         │
├─────────────────────────────────────────────┤
│ ⚠️  WATCH OUT FOR:                          │
│ • Too many strategies                       │
│ • Strategies with too much state            │
│ • Not using interface                       │
│ • No default strategy                       │
├─────────────────────────────────────────────┤
│ 🔧 RELATED PATTERNS:                       │
│ • State (similar structure)                 │
│ • Factory (creates strategies)              │
│ • Decorator (adds behavior)                 │
└─────────────────────────────────────────────┘
```

## References & Learn More

- [GoF Design Patterns](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring Guru: Strategy](https://refactoring.guru/design-patterns/strategy)
- [Strategy Pattern in TypeScript](https://www.patterns.dev/posts/strategy-pattern/)
