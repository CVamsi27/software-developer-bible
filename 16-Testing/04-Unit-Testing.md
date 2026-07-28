---
section: Testing
category: Quality
tags: [concept]
---

# Unit Testing

## Definition

Unit testing is a software testing technique where individual units or components of software are tested in isolation to verify that each unit functions correctly. A "unit" is the smallest testable part of an application—typically a function, method, class, or module.

**Key Characteristics:**

- Tests a single unit of code in isolation
- Fast execution (milliseconds)
- Low maintenance cost
- High granularity
- Verifies correctness of individual components
- Uses mocks/stubs to isolate dependencies

**Unit Testing Triangle:**

```text
┌─────────────────────────────────────────────────────────────┐
│                     Unit Testing                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input ──────▶ [Unit Under Test] ──────▶ Expected Output   │
│                    │                                        │
│                    ▼                                        │
│              Mocked Dependencies                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

## Why Do We Need It?

- **Early Bug Detection**: Catch bugs during development, not in production
- **Code Quality**: Forces you to think about edge cases and error handling
- **Design Improvement**: Writing testable code leads to better architecture
- **Refactoring Safety**: Change code confidently with tests as safety net
- **Documentation**: Tests serve as living documentation of code behavior
- **Faster Debugging**: Isolated failures are easier to diagnose
- **Reduced Costs**: Fixing bugs in development is 10-100x cheaper than in production
- **CI/CD Enablement**: Fast unit tests enable continuous integration

## How It Works

### Unit Test Structure

```text
┌─────────────────────────────────────────────────────────────┐
│                   Unit Test Components                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    ARRANGE                           │   │
│  │  • Create test data                                  │   │
│  │  • Set up mocks/stubs                               │   │
│  │  • Initialize system under test                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                     ACT                              │   │
│  │  • Execute the unit under test                      │   │
│  │  • Call the method/function                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    ASSERT                            │   │
│  │  • Verify expected outcome                          │   │
│  │  • Check return value                               │   │
│  │  • Verify state changes                             │   │
│  │  • Check mock interactions                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

### Test Doubles Hierarchy

```text
┌─────────────────────────────────────────────────────────────┐
│                     Test Doubles                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Dummy ──── Object passed around but never used            │
│    │       (just to fill parameter lists)                  │
│    │                                                        │
│    ▼                                                        │
│  Stub ──── Returns predefined values                       │
│    │       (doesn't care about calls)                      │
│    │                                                        │
│    ▼                                                        │
│  Spy ───── Records calls for later verification            │
│    │       (wraps real implementation)                     │
│    │                                                        │
│    ▼                                                        │
│  Mock ──── Pre-programmed with expectations                │
│    │       (verifies interactions)                         │
│    │                                                        │
│    ▼                                                        │
│  Fake ──── Working implementation of simplified behavior   │
│            (in-memory database, etc.)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Pure Function Testing

```typescript
// pure-functions.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function isEven(num: number): boolean {
  return num % 2 === 0;
}

export function capitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength - 3) + "...";
}

export function calculateDiscount(price: number, discountPercent: number): number {
  if (price < 0) throw new Error("Price cannot be negative");
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error("Discount must be between 0 and 100");
  }
  return price * (1 - discountPercent / 100);
}

// pure-functions.test.ts
import { add, isEven, capitalize, truncate, calculateDiscount } from "./pure-functions";

describe("Pure Functions", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("should handle negative numbers", () => {
      expect(add(-1, -1)).toBe(-2);
    });

    it("should handle zero", () => {
      expect(add(5, 0)).toBe(5);
    });

    it("should handle decimal numbers", () => {
      expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });
  });

  describe("isEven", () => {
    it("should return true for even numbers", () => {
      [0, 2, 4, 6, 10, 100].forEach((num) => {
        expect(isEven(num)).toBe(true);
      });
    });

    it("should return false for odd numbers", () => {
      [1, 3, 5, 7, 9, 99].forEach((num) => {
        expect(isEven(num)).toBe(false);
      });
    });
  });

  describe("capitalize", () => {
    it("should capitalize first letter", () => {
      expect(capitalize("hello")).toBe("Hello");
    });

    it("should handle empty string", () => {
      expect(capitalize("")).toBe("");
    });

    it("should handle single character", () => {
      expect(capitalize("a")).toBe("A");
    });

    it("should not change already capitalized string", () => {
      expect(capitalize("Hello")).toBe("Hello");
    });
  });

  describe("truncate", () => {
    it("should truncate long strings", () => {
      expect(truncate("Hello, World!", 10)).toBe("Hello,...");
    });

    it("should not truncate short strings", () => {
      expect(truncate("Hi", 10)).toBe("Hi");
    });

    it("should handle exact length", () => {
      expect(truncate("Hello", 5)).toBe("Hello");
    });
  });

  describe("calculateDiscount", () => {
    it("should calculate discount correctly", () => {
      expect(calculateDiscount(100, 10)).toBe(90);
    });

    it("should handle zero discount", () => {
      expect(calculateDiscount(100, 0)).toBe(100);
    });

    it("should handle 100% discount", () => {
      expect(calculateDiscount(100, 100)).toBe(0);
    });

    it("should throw error for negative price", () => {
      expect(() => calculateDiscount(-100, 10)).toThrow("Price cannot be negative");
    });

    it("should throw error for invalid discount", () => {
      expect(() => calculateDiscount(100, -10)).toThrow("Discount must be between 0 and 100");
      expect(() => calculateDiscount(100, 110)).toThrow("Discount must be between 0 and 100");
    });
  });
});

```

### Class Testing

```typescript
// temperature.ts
export class Temperature {
  private celsius: number;

  constructor(celsius: number) {
    this.celsius = celsius;
  }

  static fromFahrenheit(fahrenheit: number): Temperature {
    const celsius = ((fahrenheit - 32) * 5) / 9;
    return new Temperature(celsius);
  }

  getCelsius(): number {
    return this.celsius;
  }

  getFahrenheit(): number {
    return (this.celsius * 9) / 5 + 32;
  }

  getKelvin(): number {
    return this.celsius + 273.15;
  }

  add(temperature: Temperature): Temperature {
    return new Temperature(this.celsius + temperature.celsius);
  }

  subtract(temperature: Temperature): Temperature {
    return new Temperature(this.celsius - temperature.celsius);
  }

  isFreezing(): boolean {
    return this.celsius <= 0;
  }

  isBoiling(): boolean {
    return this.celsius >= 100;
  }

  toString(): string {
    return `${this.celsius.toFixed(1)}°C`;
  }
}

// temperature.test.ts
import { Temperature } from "./temperature";

describe("Temperature", () => {
  describe("creation", () => {
    it("should create from celsius", () => {
      const temp = new Temperature(25);
      expect(temp.getCelsius()).toBe(25);
    });

    it("should create from fahrenheit", () => {
      const temp = Temperature.fromFahrenheit(77);
      expect(temp.getCelsius()).toBeCloseTo(25);
    });
  });

  describe("conversion", () => {
    it("should convert to fahrenheit", () => {
      const temp = new Temperature(100);
      expect(temp.getFahrenheit()).toBe(212);
    });

    it("should convert to kelvin", () => {
      const temp = new Temperature(0);
      expect(temp.getKelvin()).toBe(273.15);
    });
  });

  describe("operations", () => {
    it("should add temperatures", () => {
      const temp1 = new Temperature(25);
      const temp2 = new Temperature(10);
      const result = temp1.add(temp2);
      expect(result.getCelsius()).toBe(35);
    });

    it("should subtract temperatures", () => {
      const temp1 = new Temperature(25);
      const temp2 = new Temperature(10);
      const result = temp1.subtract(temp2);
      expect(result.getCelsius()).toBe(15);
    });
  });

  describe("comparisons", () => {
    it("should detect freezing temperature", () => {
      expect(new Temperature(0).isFreezing()).toBe(true);
      expect(new Temperature(-10).isFreezing()).toBe(true);
      expect(new Temperature(1).isFreezing()).toBe(false);
    });

    it("should detect boiling temperature", () => {
      expect(new Temperature(100).isBoiling()).toBe(true);
      expect(new Temperature(101).isBoiling()).toBe(true);
      expect(new Temperature(99).isBoiling()).toBe(false);
    });
  });
});

```

### Testing with Dependencies

```typescript
// httpClient.ts
export interface HttpResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

export class HttpClient {
  async get<T>(url: string): Promise<HttpResponse<T>> {
    const response = await fetch(url);
    const data = await response.json();
    return {
      data,
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
    };
  }

  async post<T>(url: string, body: unknown): Promise<HttpResponse<T>> {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    return {
      data,
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
    };
  }
}

// userService.ts
import { HttpClient } from "./httpClient";

export interface User {
  id: string;
  name: string;
  email: string;
}

export class UserService {
  constructor(private httpClient: HttpClient) {}

  async getUser(id: string): Promise<User> {
    const response = await this.httpClient.get<User>(`/api/users/${id}`);
    return response.data;
  }

  async createUser(userData: Omit<User, "id">): Promise<User> {
    const response = await this.httpClient.post<User>("/api/users", userData);
    return response.data;
  }

  async getUsers(): Promise<User[]> {
    const response = await this.httpClient.get<User[]>("/api/users");
    return response.data;
  }
}

// userService.test.ts
import { UserService, User } from "./userService";
import { HttpClient } from "./httpClient";

describe("UserService", () => {
  let userService: UserService;
  let mockHttpClient: jest.Mocked<HttpClient>;

  beforeEach(() => {
    mockHttpClient = {
      get: jest.fn(),
      post: jest.fn(),
    } as any;
    userService = new UserService(mockHttpClient);
  });

  describe("getUser", () => {
    it("should return user by id", async () => {
      const mockUser: User = {
        id: "123",
        name: "John Doe",
        email: "john@example.com",
      };

      mockHttpClient.get.mockResolvedValue({
        data: mockUser,
        status: 200,
        headers: {},
      });

      const user = await userService.getUser("123");

      expect(user).toEqual(mockUser);
      expect(mockHttpClient.get).toHaveBeenCalledWith("/api/users/123");
    });

    it("should propagate errors", async () => {
      mockHttpClient.get.mockRejectedValue(new Error("Network error"));

      await expect(userService.getUser("123")).rejects.toThrow("Network error");
    });
  });

  describe("createUser", () => {
    it("should create user with correct data", async () => {
      const userData = { name: "Jane", email: "jane@example.com" };
      const createdUser: User = { id: "456", ...userData };

      mockHttpClient.post.mockResolvedValue({
        data: createdUser,
        status: 201,
        headers: {},
      });

      const user = await userService.createUser(userData);

      expect(user).toEqual(createdUser);
      expect(mockHttpClient.post).toHaveBeenCalledWith("/api/users", userData);
    });
  });
});

```

### Isolating Dependencies

```typescript
// emailService.ts
export interface EmailOptions {
  to: string;
  subject: string;
  body: string;
}

export class EmailService {
  async sendEmail(options: EmailOptions): Promise<boolean> {
    // In real implementation, this would call an email API
    console.log(`Sending email to ${options.to}`);
    return true;
  }

  async sendBulkEmails(
    recipients: string[],
    subject: string,
    body: string
  ): Promise<{ sent: number; failed: number }> {
    let sent = 0;
    let failed = 0;

    for (const recipient of recipients) {
      try {
        await this.sendEmail({ to: recipient, subject, body });
        sent++;
      } catch {
        failed++;
      }
    }

    return { sent, failed };
  }
}

// orderProcessor.ts
import { EmailService } from "./emailService";

export interface Order {
  id: string;
  customerId: string;
  items: Array<{ productId: string; quantity: number }>;
  total: number;
}

export class OrderProcessor {
  constructor(private emailService: EmailService) {}

  async processOrder(order: Order): Promise<{ success: boolean; message: string }> {
    // Validate order
    if (!order.items || order.items.length === 0) {
      return { success: false, message: "Order has no items" };
    }

    if (order.total <= 0) {
      return { success: false, message: "Invalid order total" };
    }

    // Process payment (mocked)
    const paymentSuccess = await this.processPayment(order.total);
    if (!paymentSuccess) {
      return { success: false, message: "Payment failed" };
    }

    // Send confirmation email
    await this.emailService.sendEmail({
      to: `customer-${order.customerId}@example.com`,
      subject: `Order ${order.id} Confirmed`,
      body: `Your order of $${order.total} has been confirmed.`,
    });

    return { success: true, message: `Order ${order.id} processed successfully` };
  }

  private async processPayment(amount: number): Promise<boolean> {
    // Mock payment processing
    return amount > 0;
  }
}

// orderProcessor.test.ts
import { OrderProcessor, Order } from "./orderProcessor";
import { EmailService } from "./emailService";

describe("OrderProcessor", () => {
  let orderProcessor: OrderProcessor;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    mockEmailService = {
      sendEmail: jest.fn().mockResolvedValue(true),
      sendBulkEmails: jest.fn(),
    } as any;
    orderProcessor = new OrderProcessor(mockEmailService);
  });

  describe("processOrder", () => {
    it("should process valid order", async () => {
      const order: Order = {
        id: "order-123",
        customerId: "cust-456",
        items: [{ productId: "prod-1", quantity: 2 }],
        total: 49.99,
      };

      const result = await orderProcessor.processOrder(order);

      expect(result.success).toBe(true);
      expect(result.message).toContain("processed successfully");
      expect(mockEmailService.sendEmail).toHaveBeenCalledWith(
        expect.objectContaining({
          to: "customer-cust-456@example.com",
          subject: expect.stringContaining("order-123"),
        })
      );
    });

    it("should reject empty order", async () => {
      const order: Order = {
        id: "order-123",
        customerId: "cust-456",
        items: [],
        total: 0,
      };

      const result = await orderProcessor.processOrder(order);

      expect(result.success).toBe(false);
      expect(result.message).toBe("Order has no items");
    });

    it("should reject invalid total", async () => {
      const order: Order = {
        id: "order-123",
        customerId: "cust-456",
        items: [{ productId: "prod-1", quantity: 1 }],
        total: -10,
      };

      const result = await orderProcessor.processOrder(order);

      expect(result.success).toBe(false);
      expect(result.message).toBe("Invalid order total");
    });

    it("should handle email failure gracefully", async () => {
      mockEmailService.sendEmail.mockRejectedValue(new Error("Email failed"));

      const order: Order = {
        id: "order-123",
        customerId: "cust-456",
        items: [{ productId: "prod-1", quantity: 1 }],
        total: 25,
      };

      await expect(orderProcessor.processOrder(order)).rejects.toThrow("Email failed");
    });
  });
});

```

### Testing Edge Cases

```typescript
// string-utils.ts
export function reverseString(str: string): string {
  return str.split("").reverse().join("");
}

export function countWords(str: string): number {
  return str.trim().split(/\s+/).filter(Boolean).length;
}

export function slugify(str: string): string {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "")
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function extractEmails(text: string): string[] {
  const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  return text.match(emailRegex) || [];
}

// string-utils.test.ts
import { reverseString, countWords, slugify, extractEmails } from "./string-utils";

describe("String Utilities", () => {
  describe("reverseString", () => {
    it("should reverse a normal string", () => {
      expect(reverseString("hello")).toBe("olleh");
    });

    it("should handle empty string", () => {
      expect(reverseString("")).toBe("");
    });

    it("should handle single character", () => {
      expect(reverseString("a")).toBe("a");
    });

    it("should handle spaces", () => {
      expect(reverseString("hello world")).toBe("dlrow olleh");
    });

    it("should handle unicode characters", () => {
      expect(reverseString("héllo")).toBe("olléh");
    });
  });

  describe("countWords", () => {
    it("should count words in normal string", () => {
      expect(countWords("hello world")).toBe(2);
    });

    it("should handle multiple spaces", () => {
      expect(countWords("hello   world")).toBe(2);
    });

    it("should handle leading/trailing spaces", () => {
      expect(countWords("  hello world  ")).toBe(2);
    });

    it("should handle empty string", () => {
      expect(countWords("")).toBe(0);
    });

    it("should handle single word", () => {
      expect(countWords("hello")).toBe(1);
    });
  });

  describe("slugify", () => {
    it("should create slug from normal string", () => {
      expect(slugify("Hello World")).toBe("hello-world");
    });

    it("should handle special characters", () => {
      expect(slugify("Hello, World!")).toBe("hello-world");
    });

    it("should handle multiple spaces", () => {
      expect(slugify("Hello   World")).toBe("hello-world");
    });

    it("should handle leading/trailing spaces", () => {
      expect(slugify("  Hello World  ")).toBe("hello-world");
    });

    it("should handle underscores", () => {
      expect(slugify("Hello_World")).toBe("hello-world");
    });
  });

  describe("extractEmails", () => {
    it("should extract emails from text", () => {
      const text = "Contact us at info@example.com or support@test.org";
      expect(extractEmails(text)).toEqual(["info@example.com", "support@test.org"]);
    });

    it("should return empty array when no emails", () => {
      expect(extractEmails("No emails here")).toEqual([]);
    });

    it("should handle emails with dots and hyphens", () => {
      expect(extractEmails("user.name@domain.co.uk")).toEqual(["user.name@domain.co.uk"]);
    });
  });
});

```

### Testing Async Code

```typescript
// async-utils.ts
export async function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts: number,
  delayMs: number = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxAttempts) {
        await delay(delayMs);
      }
    }
  }

  throw lastError;
}

export async function parallel<T>(
  tasks: Array<() => Promise<T>>,
  concurrency: number
): Promise<T[]> {
  const results: T[] = [];
  const executing: Set<Promise<void>> = new Set();

  for (const task of tasks) {
    const promise = task().then((result) => {
      results.push(result);
    });
    executing.add(promise);

    promise.then(() => executing.delete(promise));

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  await Promise.all(executing);
  return results;
}

// async-utils.test.ts
import { delay, retry, parallel } from "./async-utils";

describe("Async Utilities", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe("delay", () => {
    it("should resolve after specified time", async () => {
      const callback = jest.fn();
      const promise = delay(1000).then(callback);

      jest.advanceTimersByTime(999);
      expect(callback).not.toHaveBeenCalled();

      jest.advanceTimersByTime(1);
      await promise;
      expect(callback).toHaveBeenCalledTimes(1);
    });
  });

  describe("retry", () => {
    it("should return result on first attempt", async () => {
      const fn = jest.fn().mockResolvedValue("success");

      const result = await retry(fn, 3, 0);

      expect(result).toBe("success");
      expect(fn).toHaveBeenCalledTimes(1);
    });

    it("should retry on failure", async () => {
      const fn = jest.fn()
        .mockRejectedValueOnce(new Error("fail"))
        .mockResolvedValue("success");

      const result = await retry(fn, 3, 0);

      expect(result).toBe("success");
      expect(fn).toHaveBeenCalledTimes(2);
    });

    it("should throw after max attempts", async () => {
      const fn = jest.fn().mockRejectedValue(new Error("fail"));

      await expect(retry(fn, 3, 0)).rejects.toThrow("fail");
      expect(fn).toHaveBeenCalledTimes(3);
    });
  });

  describe("parallel", () => {
    it("should execute tasks in parallel", async () => {
      const task1 = jest.fn().mockResolvedValue(1);
      const task2 = jest.fn().mockResolvedValue(2);
      const task3 = jest.fn().mockResolvedValue(3);

      const results = await parallel([task1, task2, task3], 2);

      expect(results).toEqual([1, 2, 3]);
    });

    it("should respect concurrency limit", async () => {
      let concurrent = 0;
      let maxConcurrent = 0;

      const createTask = () => async () => {
        concurrent++;
        maxConcurrent = Math.max(maxConcurrent, concurrent);
        await delay(10);
        concurrent--;
        return maxConcurrent;
      };

      const tasks = Array(5).fill(null).map(createTask);
      await parallel(tasks, 2);

      expect(maxConcurrent).toBeLessThanOrEqual(2);
    });
  });
});

```

## Real-World Use Cases

### 1. Testing a Price Calculator

```typescript
// priceCalculator.ts
interface PricingRule {
  minQuantity: number;
  maxQuantity: number | null;
  pricePerUnit: number;
}

export class PriceCalculator {
  private rules: PricingRule[] = [];

  addRule(rule: PricingRule): void {
    this.rules.push(rule);
    this.rules.sort((a, b) => a.minQuantity - b.minQuantity);
  }

  calculatePrice(quantity: number, discountPercent: number = 0): number {
    if (quantity <= 0) {
      throw new Error("Quantity must be positive");
    }

    if (discountPercent < 0 || discountPercent > 100) {
      throw new Error("Discount must be between 0 and 100");
    }

    const applicableRule = this.rules.find(
      (rule) =>
        quantity >= rule.minQuantity &&
        (rule.maxQuantity === null || quantity <= rule.maxQuantity)
    );

    if (!applicableRule) {
      throw new Error("No pricing rule matches the quantity");
    }

    const basePrice = quantity * applicableRule.pricePerUnit;
    return basePrice * (1 - discountPercent / 100);
  }

  getBestDeal(quantity: number): { rule: PricingRule; total: number } | null {
    if (quantity <= 0) return null;

    let bestDeal: { rule: PricingRule; total: number } | null = null;

    for (const rule of this.rules) {
      if (quantity >= rule.minQuantity) {
        const total = quantity * rule.pricePerUnit;
        if (!bestDeal || total < bestDeal.total) {
          bestDeal = { rule, total };
        }
      }
    }

    return bestDeal;
  }
}

// priceCalculator.test.ts
import { PriceCalculator } from "./priceCalculator";

describe("PriceCalculator", () => {
  let calculator: PriceCalculator;

  beforeEach(() => {
    calculator = new PriceCalculator();
    calculator.addRule({ minQuantity: 1, maxQuantity: 9, pricePerUnit: 10 });
    calculator.addRule({ minQuantity: 10, maxQuantity: 99, pricePerUnit: 8 });
    calculator.addRule({ minQuantity: 100, maxQuantity: null, pricePerUnit: 5 });
  });

  describe("calculatePrice", () => {
    it("should calculate price for small quantity", () => {
      expect(calculator.calculatePrice(5)).toBe(50);
    });

    it("should calculate price for medium quantity", () => {
      expect(calculator.calculatePrice(50)).toBe(400);
    });

    it("should calculate price for large quantity", () => {
      expect(calculator.calculatePrice(200)).toBe(1000);
    });

    it("should apply discount", () => {
      expect(calculator.calculatePrice(10, 10)).toBe(72);
    });

    it("should throw for zero quantity", () => {
      expect(() => calculator.calculatePrice(0)).toThrow("Quantity must be positive");
    });

    it("should throw for invalid discount", () => {
      expect(() => calculator.calculatePrice(10, -10)).toThrow("Discount must be between 0 and 100");
    });
  });

  describe("getBestDeal", () => {
    it("should find best deal for quantity", () => {
      const deal = calculator.getBestDeal(50);
      expect(deal).not.toBeNull();
      expect(deal!.rule.pricePerUnit).toBe(8);
    });

    it("should return null for zero quantity", () => {
      expect(calculator.getBestDeal(0)).toBeNull();
    });
  });
});

```

### 2. Testing a State Machine

```typescript
// orderStateMachine.ts
type OrderState = "pending" | "confirmed" | "processing" | "shipped" | "delivered" | "cancelled";

interface OrderEvent {
  type: "CONFIRM" | "PROCESS" | "SHIP" | "DELIVER" | "CANCEL";
  payload?: any;
}

const transitions: Record<OrderState, Partial<Record<OrderEvent["type"], OrderState>>> = {
  pending: { CONFIRM: "confirmed", CANCEL: "cancelled" },
  confirmed: { PROCESS: "processing", CANCEL: "cancelled" },
  processing: { SHIP: "shipped" },
  shipped: { DELIVER: "delivered" },
  delivered: {},
  cancelled: {},
};

export class OrderStateMachine {
  private state: OrderState = "pending";
  private history: Array<{ from: OrderState; to: OrderState; event: OrderEvent }> = [];

  getState(): OrderState {
    return this.state;
  }

  getHistory(): Array<{ from: OrderState; to: OrderState; event: OrderEvent }> {
    return [...this.history];
  }

  canTransition(event: OrderEvent["type"]): boolean {
    return event in (transitions[this.state] || {});
  }

  transition(event: OrderEvent): OrderState {
    const nextState = transitions[this.state]?.[event.type];

    if (!nextState) {
      throw new Error(`Cannot transition from ${this.state} with event ${event.type}`);
    }

    this.history.push({ from: this.state, to: nextState, event });
    this.state = nextState;

    return this.state;
  }
}

// orderStateMachine.test.ts
import { OrderStateMachine } from "./orderStateMachine";

describe("OrderStateMachine", () => {
  let machine: OrderStateMachine;

  beforeEach(() => {
    machine = new OrderStateMachine();
  });

  it("should start in pending state", () => {
    expect(machine.getState()).toBe("pending");
  });

  it("should transition through normal flow", () => {
    machine.transition({ type: "CONFIRM" });
    expect(machine.getState()).toBe("confirmed");

    machine.transition({ type: "PROCESS" });
    expect(machine.getState()).toBe("processing");

    machine.transition({ type: "SHIP" });
    expect(machine.getState()).toBe("shipped");

    machine.transition({ type: "DELIVER" });
    expect(machine.getState()).toBe("delivered");
  });

  it("should allow cancellation from pending", () => {
    machine.transition({ type: "CANCEL" });
    expect(machine.getState()).toBe("cancelled");
  });

  it("should allow cancellation from confirmed", () => {
    machine.transition({ type: "CONFIRM" });
    machine.transition({ type: "CANCEL" });
    expect(machine.getState()).toBe("cancelled");
  });

  it("should throw for invalid transition", () => {
    expect(() => machine.transition({ type: "SHIP" })).toThrow(
      "Cannot transition from pending with event SHIP"
    );
  });

  it("should track transition history", () => {
    machine.transition({ type: "CONFIRM" });
    machine.transition({ type: "PROCESS" });

    const history = machine.getHistory();
    expect(history).toHaveLength(2);
    expect(history[0]).toEqual({
      from: "pending",
      to: "confirmed",
      event: { type: "CONFIRM" },
    });
  });

  it("should report valid transitions", () => {
    expect(machine.canTransition("CONFIRM")).toBe(true);
    expect(machine.canTransition("CANCEL")).toBe(true);
    expect(machine.canTransition("PROCESS")).toBe(false);
  });
});

```

## Common Mistakes

### 1. Testing Too Much in One Test

```typescript
// ❌ BAD: Testing multiple behaviors
it("should do everything", () => {
  const result = complexFunction();
  expect(result.a).toBe(1);
  expect(result.b).toBe(2);
  expect(result.c).toBe(3);
  expect(result.d).toBe(4);
});

// ✅ GOOD: Focused tests
it("should calculate part a", () => {
  expect(complexFunction().a).toBe(1);
});

it("should calculate part b", () => {
  expect(complexFunction().b).toBe(2);
});

```

### 2. Testing Implementation Details

```typescript
// ❌ BAD: Testing internal implementation
class UserService {
  private hashPassword(password: string): string {
    return `hashed_${password}`;
  }

  async createUser(data: UserData) {
    const hashedPassword = this.hashPassword(data.password);
    // ...
  }
}

it("should call hashPassword internally", () => {
  const spy = jest.spyOn(userService as any, "hashPassword");
  userService.createUser({ password: "test" });
  expect(spy).toHaveBeenCalled();
});

// ✅ GOOD: Testing behavior
it("should store hashed password", async () => {
  await userService.createUser({ password: "test" });
  const user = await db.getUser(userId);
  expect(user.password).not.toBe("test");
  expect(user.password).toContain("hashed_");
});

```

### 3. Not Cleaning Up

```typescript
// ❌ BAD: Tests affect each other
let counter = 0;

it("should increment", () => {
  counter++;
  expect(counter).toBe(1);
});

it("should still be 1", () => {
  // counter is still 1 from previous test!
  expect(counter).toBe(1);
});

// ✅ GOOD: Reset state
beforeEach(() => {
  counter = 0;
});

it("should increment", () => {
  counter++;
  expect(counter).toBe(1);
});

it("should start fresh", () => {
  expect(counter).toBe(0);
});

```

## Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert

2. **Test one thing per test**: Each test should verify one behavior

3. **Keep tests independent**: No test should depend on another

4. **Use descriptive names**: Test names should explain the behavior

5. **Test edge cases**: Empty inputs, null values, boundaries

6. **Mock external dependencies**: Databases, APIs, file system

7. **Keep tests fast**: Unit tests should run in milliseconds

8. **Test error handling**: Verify exceptions and error messages

9. **Use test data builders**: Create reusable test data factories
10. **Maintain test code**: Refactor tests like production code

## Performance Considerations

### Test Execution Time

```text
Unit Test Performance:
┌─────────────────────────────────────────────────────────────┐
│ Target: < 10ms per test                                    │
├─────────────────────────────────────────────────────────────┤
│ • Keep tests focused on single unit                        │
│ • Mock external dependencies                               │
│ • Use in-memory databases for data tests                   │
│ • Avoid unnecessary setup/teardown                         │
│ • Profile slow tests                                       │
└─────────────────────────────────────────────────────────────┘

```

### Parallel Execution

```typescript
// jest.config.js
module.exports = {
  maxWorkers: "50%", // Use half of CPU cores
  // Or for specific projects
  projects: [
    {
      displayName: "unit",
      testMatch: ["<rootDir>/src/**/*.test.ts"],
      testEnvironment: "node",
    },
  ],
};

```

## Summary

Unit testing is the foundation of a robust test suite. Key principles:

- **Test in isolation** with mocks and stubs
- **Follow AAA pattern** for clear test structure
- **Keep tests fast** and focused
- **Test behavior**, not implementation
- **Cover edge cases** and error scenarios
- **Maintain test code** like production code
- **Use test doubles** appropriately
- **Aim for high confidence**, not 100% coverage

A strong unit test suite enables confident refactoring, faster development, and higher code quality.

---

## See Also
- [React](../03-React/)
- [NestJS](../06-NestJS/)
- [CI/CD](../15-CI-CD/)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- "Test Driven Development: By Example" by Kent Beck
- "The Art of Unit Testing" by Roy Osherove
- "Working Effectively with Legacy Code" by Michael Feathers
- Jest Documentation
- Testing JavaScript by Kent C. Dodds
