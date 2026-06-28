# Jest

## Definition

Jest is a JavaScript testing framework developed by Facebook (Meta) that provides a complete testing solution for modern JavaScript applications. It offers a zero-configuration setup, built-in assertion library, mocking capabilities, and comprehensive code coverage reporting.

**Key Features:**
- **Zero Configuration**: Works out of the box for most JavaScript projects
- **Fast Execution**: Parallel test running with intelligent test ordering
- **Built-in Mocking**: Complete mocking system for functions, modules, and timers
- **Snapshot Testing**: Capture and compare rendered outputs
- **Code Coverage**: Built-in coverage reporting with Istanbul
- **Watch Mode**: Interactive test runner that re-runs tests on changes
- **Rich API**: Comprehensive set of matchers and utilities

## Why Do We Need It?

- **Simplicity**: Minimal setup required to start testing
- **Speed**: Fast test execution even for large test suites
- **All-in-One**: Includes assertions, mocking, and coverage in one package
- **Rich Ecosystem**: Extensive plugin system and community support
- **TypeScript Support**: First-class TypeScript support with minimal configuration
- **React Integration**: Excellent support for React component testing
- **Snapshot Testing**: Unique feature for catching unexpected UI changes
- **Code Coverage**: Built-in Istanbul integration for coverage reports

## How It Works

### Jest Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                      Jest Test Runner                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Test Parser │  │  Reporter   │  │  Configuration      │ │
│  │             │  │             │  │                     │ │
│  │ • Collects  │  │ • Console   │  │ • jest.config.js    │ │
│  │   test files│  │ • Coverage  │  │ • package.json      │ │
│  │ • Parses    │  │ • JUnit     │  │ • Environment       │ │
│  │   describe/ │  │ • Custom    │  │                     │ │
│  │   it blocks │  │             │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Test Execution                        ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ││
│  │  │Worker 1 │  │Worker 2 │  │Worker 3 │  │Worker N │  ││
│  │  │         │  │         │  │         │  │         │  ││
│  │  │ • Isolate│  │ • Isolate│  │ • Isolate│  │ • Isolate│  ││
│  │  │ • Run   │  │ • Run   │  │ • Run   │  │ • Run   │  ││
│  │  │ • Report│  │ • Report│  │ • Report│  │ • Report│  ││
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Assertion Library                      ││
│  │  expect().toBe()     expect().toEqual()                ││
│  │  expect().toThrow()  expect().toMatchObject()          ││
│  │  expect().toHaveProperty()  expect().toHaveBeenCalled()││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Mock System                            ││
│  │  jest.fn()  jest.mock()  jest.spyOn()                  ││
│  │  mockImplementation  mockReturnValue                    ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Test Execution Flow

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  npm test    │────▶│ Jest CLI     │────▶│  Config      │
│              │     │              │     │  Loading     │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                    ┌─────────────────────────────┘
                    ▼
           ┌──────────────┐     ┌──────────────┐
           │  Find Test   │────▶│  Transform   │
           │  Files       │     │  (Babel)     │
           └──────────────┘     └──────┬───────┘
                                       │
                    ┌──────────────────┘
                    ▼
           ┌──────────────┐     ┌──────────────┐
           │  Execute     │────▶│  Collect     │
           │  Tests       │     │  Results     │
           └──────────────┘     └──────┬───────┘
                                       │
                    ┌──────────────────┘
                    ▼
           ┌──────────────┐     ┌──────────────┐
           │  Generate    │────▶│  Output      │
           │  Coverage    │     │  Report      │
           └──────────────┘     └──────────────┘
```

## Code Examples

### Basic Configuration

```javascript
// jest.config.js
module.exports = {
  // Test environment
  testEnvironment: "node", // or 'jsdom' for browser-like environment

  // File patterns
  testMatch: [
    "**/__tests__/**/*.[jt]s?(x)",
    "**/?(*.)+(spec|test).[jt]s?(x)",
  ],

  // Coverage settings
  collectCoverageFrom: [
    "src/**/*.{js,jsx,ts,tsx}",
    "!src/**/*.d.ts",
    "!src/index.tsx",
  ],

  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  // Setup files
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],

  // Module name mapping
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },

  // Transform configuration
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
  },

  // Test timeout
  testTimeout: 10000,
};
```

### describe/it/expect

```typescript
// calculator.ts
export class Calculator {
  private history: string[] = [];

  add(a: number, b: number): number {
    const result = a + b;
    this.history.push(`${a} + ${b} = ${result}`);
    return result;
  }

  subtract(a: number, b: number): number {
    const result = a - b;
    this.history.push(`${a} - ${b} = ${result}`);
    return result;
  }

  multiply(a: number, b: number): number {
    const result = a * b;
    this.history.push(`${a} * ${b} = ${result}`);
    return result;
  }

  divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    const result = a / b;
    this.history.push(`${a} / ${b} = ${result}`);
    return result;
  }

  getHistory(): string[] {
    return [...this.history];
  }

  clearHistory(): void {
    this.history = [];
  }
}

// calculator.test.ts
import { Calculator } from "./calculator";

describe("Calculator", () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  describe("addition", () => {
    it("should add two positive numbers", () => {
      expect(calculator.add(2, 3)).toBe(5);
    });

    it("should add negative numbers", () => {
      expect(calculator.add(-1, -1)).toBe(-2);
    });

    it("should handle zero", () => {
      expect(calculator.add(5, 0)).toBe(5);
    });

    it("should add decimals", () => {
      expect(calculator.add(0.1, 0.2)).toBeCloseTo(0.3);
    });
  });

  describe("subtraction", () => {
    it("should subtract two numbers", () => {
      expect(calculator.subtract(10, 3)).toBe(7);
    });

    it("should handle negative results", () => {
      expect(calculator.subtract(3, 10)).toBe(-7);
    });
  });

  describe("division", () => {
    it("should divide two numbers", () => {
      expect(calculator.divide(10, 2)).toBe(5);
    });

    it("should throw error when dividing by zero", () => {
      expect(() => calculator.divide(10, 0)).toThrow("Cannot divide by zero");
    });
  });

  describe("history", () => {
    it("should track operation history", () => {
      calculator.add(2, 3);
      calculator.subtract(10, 5);
      expect(calculator.getHistory()).toHaveLength(2);
    });

    it("should clear history", () => {
      calculator.add(1, 2);
      calculator.clearHistory();
      expect(calculator.getHistory()).toHaveLength(0);
    });
  });
});
```

### Mocking with jest.mock and jest.fn

```typescript
// api.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

export async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }
  return response.json();
}

export async function sendEmail(
  to: string,
  subject: string,
  body: string
): Promise<void> {
  // Email service implementation
}

// userService.ts
import { fetchUser, sendEmail } from "./api";

export class UserService {
  async getUserWelcomeEmail(userId: string): Promise<string> {
    const user = await fetchUser(userId);
    return `Welcome, ${user.name}!`;
  }

  async notifyUser(userId: string, message: string): Promise<void> {
    const user = await fetchUser(userId);
    await sendEmail(user.email, "Notification", message);
  }
}

// userService.test.ts
import { UserService } from "./userService";
import { fetchUser, sendEmail } from "./api";

// Mock the entire module
jest.mock("./api");
const mockFetchUser = jest.mocked(fetchUser);
const mockSendEmail = jest.mocked(sendEmail);

describe("UserService", () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
    jest.clearAllMocks();
  });

  describe("getUserWelcomeEmail", () => {
    it("should return welcome message with user name", async () => {
      mockFetchUser.mockResolvedValue({
        id: "1",
        name: "John",
        email: "john@example.com",
      });

      const result = await userService.getUserWelcomeEmail("1");

      expect(result).toBe("Welcome, John!");
      expect(mockFetchUser).toHaveBeenCalledWith("1");
    });

    it("should propagate fetch errors", async () => {
      mockFetchUser.mockRejectedValue(new Error("Network error"));

      await expect(userService.getUserWelcomeEmail("1")).rejects.toThrow(
        "Network error"
      );
    });
  });

  describe("notifyUser", () => {
    it("should send email to user", async () => {
      mockFetchUser.mockResolvedValue({
        id: "1",
        name: "John",
        email: "john@example.com",
      });
      mockSendEmail.mockResolvedValue(undefined);

      await userService.notifyUser("1", "Hello!");

      expect(mockSendEmail).toHaveBeenCalledWith(
        "john@example.com",
        "Notification",
        "Hello!"
      );
    });
  });
});
```

### Spies with jest.spyOn

```typescript
// productService.ts
export class ProductService {
  private inventory: Map<string, number> = new Map();

  constructor() {
    this.inventory.set("widget", 100);
    this.inventory.set("gadget", 50);
  }

  getStock(productId: string): number {
    return this.inventory.get(productId) || 0;
  }

  updateStock(productId: string, quantity: number): void {
    const current = this.getStock(productId);
    this.inventory.set(productId, current + quantity);
  }

  isAvailable(productId: string, quantity: number): boolean {
    return this.getStock(productId) >= quantity;
  }
}

// notificationService.ts
export class NotificationService {
  sendLowStockAlert(productId: string, currentStock: number): void {
    console.log(`Low stock alert: ${productId} has ${currentStock} units`);
  }
}

// inventoryManager.ts
import { ProductService } from "./productService";
import { NotificationService } from "./notificationService";

export class InventoryManager {
  constructor(
    private productService: ProductService,
    private notificationService: NotificationService
  ) {}

  async processOrder(
    productId: string,
    quantity: number
  ): Promise<{ success: boolean; message: string }> {
    if (!this.productService.isAvailable(productId, quantity)) {
      return {
        success: false,
        message: `Insufficient stock for ${productId}`,
      };
    }

    this.productService.updateStock(productId, -quantity);

    const newStock = this.productService.getStock(productId);
    if (newStock < 10) {
      this.notificationService.sendLowStockAlert(productId, newStock);
    }

    return {
      success: true,
      message: `Order processed for ${quantity} ${productId}`,
    };
  }
}

// inventoryManager.test.ts
import { InventoryManager } from "./inventoryManager";
import { ProductService } from "./productService";
import { NotificationService } from "./notificationService";

describe("InventoryManager", () => {
  let inventoryManager: InventoryManager;
  let mockProductService: jest.Mocked<ProductService>;
  let mockNotificationService: jest.Mocked<NotificationService>;
  let sendLowStockAlertSpy: jest.SpyInstance;

  beforeEach(() => {
    mockProductService = {
      getStock: jest.fn(),
      updateStock: jest.fn(),
      isAvailable: jest.fn(),
    } as any;

    mockNotificationService = {
      sendLowStockAlert: jest.fn(),
    } as any;

    inventoryManager = new InventoryManager(
      mockProductService,
      mockNotificationService
    );

    sendLowStockAlertSpy = jest.spyOn(
      mockNotificationService,
      "sendLowStockAlert"
    );
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("should process order when stock is available", async () => {
    mockProductService.isAvailable.mockReturnValue(true);
    mockProductService.updateStock.mockImplementation(() => {});
    mockProductService.getStock.mockReturnValue(15);

    const result = await inventoryManager.processOrder("widget", 5);

    expect(result.success).toBe(true);
    expect(mockProductService.updateStock).toHaveBeenCalledWith("widget", -5);
  });

  it("should send low stock alert when below threshold", async () => {
    mockProductService.isAvailable.mockReturnValue(true);
    mockProductService.updateStock.mockImplementation(() => {});
    mockProductService.getStock.mockReturnValue(8);

    await inventoryManager.processOrder("widget", 5);

    expect(sendLowStockAlertSpy).toHaveBeenCalledWith("widget", 8);
  });

  it("should return failure when stock is insufficient", async () => {
    mockProductService.isAvailable.mockReturnValue(false);

    const result = await inventoryManager.processOrder("widget", 150);

    expect(result.success).toBe(false);
    expect(result.message).toContain("Insufficient stock");
  });
});
```

### Snapshot Testing

```typescript
// UserCard.tsx
import React from "react";

interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
  role: "admin" | "user" | "guest";
}

export const UserCard: React.FC<UserCardProps> = ({
  name,
  email,
  avatar,
  role,
}) => {
  const getRoleBadgeColor = () => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "user":
        return "bg-blue-100 text-blue-800";
      case "guest":
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="user-card">
      <div className="avatar">
        {avatar ? (
          <img src={avatar} alt={name} />
        ) : (
          <div className="avatar-placeholder">{name[0]}</div>
        )}
      </div>
      <div className="info">
        <h3>{name}</h3>
        <p>{email}</p>
        <span className={`badge ${getRoleBadgeColor()}`}>{role}</span>
      </div>
    </div>
  );
};

// UserCard.test.tsx
import { render } from "@testing-library/react";
import { UserCard } from "./UserCard";

describe("UserCard", () => {
  it("should render user with avatar", () => {
    const { container } = render(
      <UserCard
        name="John Doe"
        email="john@example.com"
        avatar="https://example.com/avatar.jpg"
        role="admin"
      />
    );
    expect(container).toMatchSnapshot();
  });

  it("should render user without avatar", () => {
    const { container } = render(
      <UserCard name="Jane Doe" email="jane@example.com" role="user" />
    );
    expect(container).toMatchSnapshot();
  });

  it("should render guest user", () => {
    const { container } = render(
      <UserCard name="Guest" email="guest@example.com" role="guest" />
    );
    expect(container).toMatchSnapshot();
  });
});

// Updating snapshots
// Run: jest --updateSnapshot
```

### Code Coverage

```typescript
// utils.ts
export function isEven(num: number): boolean {
  return num % 2 === 0;
}

export function fibonacci(n: number): number {
  if (n <= 0) return 0;
  if (n === 1) return 1;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

export function capitalize(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// utils.test.ts
import { isEven, fibonacci, capitalize } from "./utils";

describe("utils", () => {
  describe("isEven", () => {
    it("should return true for even numbers", () => {
      expect(isEven(2)).toBe(true);
      expect(isEven(4)).toBe(true);
    });

    it("should return false for odd numbers", () => {
      expect(isEven(1)).toBe(false);
      expect(isEven(3)).toBe(false);
    });
  });

  describe("fibonacci", () => {
    it("should return 0 for 0", () => {
      expect(fibonacci(0)).toBe(0);
    });

    it("should return 1 for 1", () => {
      expect(fibonacci(1)).toBe(1);
    });

    it("should return fibonacci number for positive input", () => {
      expect(fibonacci(5)).toBe(5);
      expect(fibonacci(10)).toBe(55);
    });
  });

  describe("capitalize", () => {
    it("should capitalize first letter", () => {
      expect(capitalize("hello")).toBe("Hello");
    });

    it("should handle empty string", () => {
      expect(capitalize("")).toBe("");
    });
  });
});

// Coverage report command:
// jest --coverage
//
// Coverage output:
// -------------------|---------|----------|---------|---------|
// File               | % Stmts | % Branch | % Funcs | % Lines |
// -------------------|---------|----------|---------|---------|
// All files          |   85.71 |    83.33 |   83.33 |   85.71 |
// utils.ts           |   85.71 |    83.33 |   83.33 |   85.71 |
// -------------------|---------|----------|---------|---------|
```

### Setup and Teardown

```typescript
// database.test.ts
import { Database } from "./database";

describe("Database Operations", () => {
  let db: Database;

  // Run once before all tests in this describe block
  beforeAll(async () => {
    db = new Database();
    await db.connect();
  });

  // Run once after all tests in this describe block
  afterAll(async () => {
    await db.disconnect();
  });

  // Run before each test
  beforeEach(async () => {
    await db.clear();
    await db.seedTestData();
  });

  // Run after each test
  afterEach(async () => {
    await db.clear();
  });

  it("should insert and retrieve data", async () => {
    await db.insert("users", { name: "John" });
    const users = await db.findAll("users");
    expect(users).toHaveLength(1);
  });

  it("should update data", async () => {
    const id = await db.insert("users", { name: "John" });
    await db.update("users", id, { name: "Updated" });
    const user = await db.findById("users", id);
    expect(user.name).toBe("Updated");
  });

  it("should delete data", async () => {
    const id = await db.insert("users", { name: "John" });
    await db.delete("users", id);
    const users = await db.findAll("users");
    expect(users).toHaveLength(0);
  });
});

// Jest setup file: jest.setup.js
import "@testing-library/jest-dom";

// Global setup
beforeAll(() => {
  console.log("Global test suite starting");
});

afterAll(() => {
  console.log("Global test suite completed");
});

// Custom matchers
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} ${pass ? "not " : ""}to be within range ${floor} - ${ceiling}`,
    };
  },
});

// Async test utilities
export const waitFor = async (
  callback: () => void | Promise<void>,
  timeout = 1000
): Promise<void> => {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    try {
      await callback();
      return;
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
  }
  throw new Error("Timeout waiting for condition");
};
```

### Timer Mocking

```typescript
// debounce.ts
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// debounce.test.ts
import { debounce } from "./debounce";

describe("debounce", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it("should delay function execution", () => {
    const mockFn = jest.fn();
    const debouncedFn = debounce(mockFn, 100);

    debouncedFn();
    expect(mockFn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(100);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it("should reset timer on subsequent calls", () => {
    const mockFn = jest.fn();
    const debouncedFn = debounce(mockFn, 100);

    debouncedFn();
    jest.advanceTimersByTime(50);
    debouncedFn(); // Reset timer
    jest.advanceTimersByTime(50);
    expect(mockFn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(50);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it("should pass arguments to debounced function", () => {
    const mockFn = jest.fn();
    const debouncedFn = debounce(mockFn, 100);

    debouncedFn("arg1", "arg2");
    jest.advanceTimersByTime(100);

    expect(mockFn).toHaveBeenCalledWith("arg1", "arg2");
  });
});
```

## Real-World Use Cases

### 1. Testing a REST API

```typescript
// api.test.ts
import request from "supertest";
import { app } from "../src/app";
import { generateToken } from "../src/auth";

describe("Users API", () => {
  const validToken = generateToken({ userId: "123" });

  describe("GET /api/users", () => {
    it("should return paginated users", async () => {
      const response = await request(app)
        .get("/api/users?page=1&limit=10")
        .set("Authorization", `Bearer ${validToken}`)
        .expect(200);

      expect(response.body).toHaveProperty("data");
      expect(response.body).toHaveProperty("pagination");
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    it("should filter users by role", async () => {
      const response = await request(app)
        .get("/api/users?role=admin")
        .set("Authorization", `Bearer ${validToken}`)
        .expect(200);

      response.body.data.forEach((user: any) => {
        expect(user.role).toBe("admin");
      });
    });
  });

  describe("POST /api/users", () => {
    it("should create a new user", async () => {
      const newUser = {
        name: "John Doe",
        email: "john@example.com",
        password: "securePassword123",
      };

      const response = await request(app)
        .post("/api/users")
        .set("Authorization", `Bearer ${validToken}`)
        .send(newUser)
        .expect(201);

      expect(response.body).toHaveProperty("id");
      expect(response.body.name).toBe(newUser.name);
      expect(response.body.email).toBe(newUser.email);
      expect(response.body).not.toHaveProperty("password");
    });

    it("should return 400 for invalid data", async () => {
      const invalidUser = { name: "", email: "invalid" };

      await request(app)
        .post("/api/users")
        .set("Authorization", `Bearer ${validToken}`)
        .send(invalidUser)
        .expect(400);
    });
  });
});
```

### 2. Testing React Components

```typescript
// LoginForm.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { rest } from "msw";
import { setupServer } from "msw/node";
import { LoginForm } from "./LoginForm";

const server = setupServer(
  rest.post("/api/auth/login", (req, res, ctx) => {
    const { email, password } = req.body;
    if (email === "user@example.com" && password === "password") {
      return res(ctx.json({ token: "fake-token", user: { id: "1" } }));
    }
    return res(ctx.status(401), ctx.json({ error: "Invalid credentials" }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("LoginForm", () => {
  it("should submit form with valid credentials", async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), "user@example.com");
    await user.type(screen.getByLabelText(/password/i), "password");
    await user.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: "user@example.com",
        password: "password",
      });
    });
  });

  it("should display error message on failed login", async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={jest.fn()} />);

    await user.type(screen.getByLabelText(/email/i), "wrong@example.com");
    await user.type(screen.getByLabelText(/password/i), "wrongpassword");
    await user.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText("Invalid credentials")).toBeInTheDocument();
    });
  });

  it("should validate required fields", async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={jest.fn()} />);

    await user.click(screen.getByRole("button", { name: /login/i }));

    expect(screen.getByText("Email is required")).toBeInTheDocument();
    expect(screen.getByText("Password is required")).toBeInTheDocument();
  });
});
```

## Common Mistakes

### 1. Forgetting to Clear Mocks

```typescript
// ❌ BAD: Mocks accumulate between tests
const mockFn = jest.fn();

it("test 1", () => {
  mockFn("a");
  expect(mockFn).toHaveBeenCalledTimes(1);
});

it("test 2", () => {
  // mockFn still has call history from test 1!
  expect(mockFn).toHaveBeenCalledTimes(1); // Might fail!
});

// ✅ GOOD: Clear mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});

it("test 1", () => {
  mockFn("a");
  expect(mockFn).toHaveBeenCalledTimes(1);
});

it("test 2", () => {
  expect(mockFn).toHaveBeenCalledTimes(0); // Correct!
});
```

### 2. Not Using jest.mocked

```typescript
// ❌ BAD: Unsafe type assertion
jest.mock("./api");
const mockFetch = fetch as jest.Mock;

// ✅ GOOD: Type-safe mocking
jest.mock("./api");
const mockFetch = jest.mocked(fetch);
```

### 3. Testing Async Code Improperly

```typescript
// ❌ BAD: Missing await
it("should fetch data", () => {
  fetchData().then((data) => {
    expect(data).toBeDefined();
  });
});

// ✅ GOOD: Proper async handling
it("should fetch data", async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// ✅ GOOD: Or return promise
it("should fetch data", () => {
  return fetchData().then((data) => {
    expect(data).toBeDefined();
  });
});
```

## Best Practices

1. **Use `jest.mocked()`** for type-safe mocking
2. **Clear mocks between tests** with `jest.clearAllMocks()`
3. **Use `beforeEach`/`afterEach`** for setup and teardown
4. **Mock at the module boundary** rather than internal functions
5. **Use snapshot testing sparingly** and review snapshots carefully
6. **Set coverage thresholds** to maintain test quality
7. **Use `jest.useFakeTimers()`** for time-dependent code
8. **Keep test files close** to the code they test
9. **Use descriptive test names** that explain behavior
10. **Avoid testing implementation details** - test behavior instead

## Performance Considerations

### Parallel Execution

```javascript
// jest.config.js
module.exports = {
  // Jest runs tests in parallel by default
  maxWorkers: "50%", // Use 50% of available CPU cores

  // Or set specific number
  // maxWorkers: 4,

  // Run tests sequentially if they have shared state
  // runInBand: true,
};
```

### Test Optimization

```typescript
// ❌ BAD: Slow - each test creates fresh DB connection
describe("Database", () => {
  it("test 1", async () => {
    const db = new Database();
    await db.connect();
    // ...
  });

  it("test 2", async () => {
    const db = new Database();
    await db.connect();
    // ...
  });
});

// ✅ GOOD: Share DB connection
describe("Database", () => {
  let db: Database;

  beforeAll(async () => {
    db = new Database();
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  it("test 1", async () => {
    // Use shared db connection
  });
});
```

## Interview Questions

### Beginner (5-10)

1. **What is Jest and why is it popular?**
   Jest is a JavaScript testing framework with zero configuration, built-in assertions, mocking, and coverage. It's popular due to its simplicity, speed, and comprehensive feature set.

2. **What is the difference between `describe`, `it`, and `test`?**
   `describe` groups related tests. `it` and `test` are aliases for defining individual test cases. `it` is more common in BDD style.

3. **What is `expect` in Jest?**
   `expect` is Jest's assertion function that takes a value and returns an object with matchers to test the value against.

4. **How do you mock a function in Jest?**
   Use `jest.fn()` to create a mock function, or `jest.mock()` to mock an entire module.

5. **What is snapshot testing?**
   Snapshot testing captures the rendered output of a component and compares it to a stored snapshot to detect unexpected changes.

6. **How do you run only specific tests?**
   Use `it.only()` or `describe.only()`, or run tests with a pattern: `jest --testNamePattern="pattern"`.

7. **What is `beforeEach` and `afterEach`?**
   These are lifecycle hooks that run before and after each test in a describe block, used for setup and cleanup.

8. **How do you mock timers in Jest?**
   Use `jest.useFakeTimers()` and `jest.advanceTimersByTime()` to control time in tests.

9. **What is code coverage in Jest?**
   Code coverage measures which parts of your code are executed by tests. Jest uses Istanbul to generate coverage reports.

10. **How do you handle async code in Jest tests?**
    Use `async/await`, return promises, or use `done` callback for asynchronous operations.

### Intermediate (5-10)

11. **What is the difference between `jest.fn()` and `jest.mock()`?**
    `jest.fn()` creates a mock function. `jest.mock()` replaces an entire module with a mock implementation.

12. **How do you test error boundaries in React with Jest?**
    Use `render` with error throwing components and verify fallback UI renders correctly.

13. **What is `jest.spyOn` and when would you use it?**
    `jest.spyOn` creates a mock that tracks calls to an existing method while preserving the original implementation.

14. **How do you mock API calls in Jest?**
    Use `jest.mock` for module-level mocking, or MSW (Mock Service Worker) for network-level mocking.

15. **What is the difference between `mockReturnValue` and `mockImplementation`?**
    `mockReturnValue` returns a fixed value. `mockImplementation` executes a function that can have logic and return different values.

16. **How do you test React hooks?**
    Use `@testing-library/react-hooks` library or wrap hooks in test components with React Testing Library.

17. **What is `jest.requireActual`?**
    `jest.requireActual` imports the real implementation of a module, useful when you want to mock part of a module.

18. **How do you test middleware in Express?**
    Create mock request/response objects and call the middleware function directly.

19. **What is `fakeTimers` in Jest?**
    `fakeTimers` replaces real timer functions with mock implementations to control time in tests.

20. **How do you debug failing Jest tests?**
    Use `--verbose` flag, add `console.log`, use debugger with `node --inspect`, or use VS Code Jest extension.

### Senior (10-15)

21. **How would you set up Jest for a monorepo?**
    Use Jest projects configuration, set up shared configuration, and manage test isolation between packages.

22. **How do you handle flaky tests in Jest?**
    Identify root causes (timing, state, network), fix them, and implement retry mechanisms for environmental issues.

23. **What is Jest's `moduleFileExtensions` configuration?**
    It specifies file extensions Jest should look for when resolving modules. Important for TypeScript and other languages.

24. **How do you optimize Jest for large codebases?**
    Use `--changedSince`, `--onlyChanged`, parallel execution, and test splitting strategies.

25. **How do you test database migrations with Jest?**
    Run migrations in `beforeAll`, test the migration logic, and verify data integrity.

26. **What is `jest-environment-jsdom`?**
    A Jest environment that provides a browser-like DOM API for testing browser code in Node.js.

27. **How do you mock GraphQL queries?**
    Use `jest.mock` for Apollo Client or use MSW for network-level GraphQL mocking.

28. **What is `globalSetup` and `globalTeardown`?**
    These run once before all test suites and after all test suites, useful for starting/stopping servers or databases.

29. **How do you test performance-critical code?**
    Use `jest.retryTimes` for flaky performance tests, and benchmark with `performance.now()`.

30. **How do you integrate Jest with CI/CD?**
    Use `--ci` flag, generate coverage reports, fail on coverage thresholds, and parallelize test execution.

### FAANG-style (5-10)

31. **How would you design a testing strategy for a microservices architecture?**
    Use contract testing, integration tests, and E2E tests. Implement test isolation and independent deployment testing.

32. **How do you handle testing in a CI/CD pipeline with Jest?**
    Implement test parallelization, use test impact analysis, cache dependencies, and fail fast on critical failures.

33. **How would you debug memory leaks in Jest tests?**
    Use `--detectOpenHandles`, profile memory usage, and ensure proper cleanup in `afterAll`.

34. **How do you test serverless functions with Jest?**
    Mock AWS services, test handler functions directly, and verify event processing.

35. **How would you implement test data factories in Jest?**
    Create factory functions with defaults, traits, and sequence generators for test data.

36. **How do you test WebSocket connections in Jest?**
    Mock WebSocket server, test client connection handling, and verify message passing.

37. **How would you handle testing in a micro-frontend architecture?**
    Use contract testing between micro-frontends, integration tests, and shared test utilities.

38. **How do you test edge computing scenarios with Jest?**
    Mock edge runtime APIs, test service worker logic, and verify offline capabilities.

39. **How would you implement visual regression testing with Jest?**
    Use `jest-image-screenshot` or integrate with Percy/Chromatic for visual comparison.

40. **How do you ensure test isolation in a shared test environment?**
    Use database transactions with rollbacks, mock external services, and implement proper cleanup.

### Follow-ups (5-10)

41. **How has your Jest usage evolved over time?**
    Discuss adoption of best practices, migration from other tools, and continuous improvement.

42. **What Jest plugins or extensions have you found valuable?**
    `jest-axe` for accessibility, `jest-fetch-mock` for fetch mocking, `jest-mock-extended` for type-safe mocking.

43. **How do you handle testing legacy code with Jest?**
    Use characterization tests, gradually increase coverage, and refactor while maintaining test coverage.

44. **What's the most challenging Jest testing problem you've solved?**
    Describe complex mocking scenarios, performance issues, or flaky test investigations.

45. **How do you balance test speed with test confidence?**
    Discuss test pyramid, prioritization strategies, and when to use different test types.

## Summary

Jest is a comprehensive JavaScript testing framework that provides everything needed for modern application testing. Key takeaways:

- **Zero Configuration**: Works out of the box with sensible defaults
- **Rich API**: Complete set of matchers, mocking utilities, and assertion functions
- **Snapshot Testing**: Unique feature for catching unexpected UI changes
- **Built-in Coverage**: Istanbul integration for code coverage reporting
- **Watch Mode**: Interactive development experience
- **TypeScript Support**: First-class TypeScript support with ts-jest
- **Extensible**: Rich plugin ecosystem for additional functionality

Master Jest by understanding its core concepts, practicing mock patterns, and implementing test-driven development.

## References & Learn More

- [Jest Official Documentation](https://jestjs.io/docs/getting-started)
- [Jest GitHub Repository](https://github.com/jestjs/jest)
- [Testing JavaScript with Jest - Udemy](https://www.udemy.com/course/testing-javascript-with-jest/)
- [Jest Cheat Sheet](https://github.com/sapegin/jest-cheat-sheet)
