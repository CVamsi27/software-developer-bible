# Mocking

## Definition

Mocking is a testing technique where you replace real objects, functions, or modules with simulated versions (test doubles) that mimic the behavior of the real implementations. Mocking allows you to isolate the code under test and control the test environment by providing predictable responses and verifying interactions.

**Key Concepts:**
- **Test Double**: Any replacement for a real object in testing
- **Mock**: A test double that records interactions for later verification
- **Stub**: A test double that returns predefined responses
- **Fake**: A working implementation with simplified behavior
- **Spy**: A wrapper that records calls while preserving original behavior

**Mocking Hierarchy:**

```text
┌─────────────────────────────────────────────────────────────┐
│                    Test Doubles                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Dummy ───── Passed around, never used                     │
│     │       (fills parameter slots)                        │
│     │                                                       │
│     ▼                                                       │
│  Stub ───── Returns fixed values                           │
│     │       (ignores how called)                           │
│     │                                                       │
│     ▼                                                       │
│  Spy ────── Records calls, may wrap real impl              │
│     │       (observability)                                │
│     │                                                       │
│     ▼                                                       │
│  Mock ───── Pre-programmed expectations                    │
│     │       (verifies interactions)                        │
│     │                                                       │
│     ▼                                                       │
│  Fake ───── Simplified real implementation                 │
│             (in-memory DB, etc.)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

- **Isolation**: Test code independently of external dependencies
- **Speed**: Replace slow operations (API calls, database) with fast mocks
- **Control**: Provide deterministic responses for consistent tests
- **Verification**: Verify that functions are called with expected arguments
- **Edge Cases**: Simulate error conditions that are hard to reproduce
- **Cost**: Avoid costs associated with real API calls
- **Reliability**: Remove network/external dependency flakiness
- **Privacy**: Avoid using real user data in tests

## How It Works

### Jest Mocking System

```text
┌─────────────────────────────────────────────────────────────┐
│                  Jest Mocking System                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  jest.fn()                                          │   │
│  │  • Creates mock function                            │   │
│  │  • Tracks calls, arguments, return values           │   │
│  │  • Can be configured with mock implementations      │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  jest.mock()                                        │   │
│  │  • Replaces entire module with mock                 │   │
│  │  • Auto-mocks all exports                          │   │
│  │  • Can provide custom implementation                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  jest.spyOn()                                       │   │
│  │  • Creates spy on existing method                   │   │
│  │  • Preserves original implementation                │   │
│  │  • Can replace implementation if needed             │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  jest.mocked()                                      │   │
│  │  • TypeScript helper for type-safe mocking          │   │
│  │  • Casts module to mocked version                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### jest.fn() - Creating Mock Functions

```typescript
// Basic mock function
const mockFn = jest.fn();

// Call the mock
mockFn("arg1", "arg2");

// Verify calls
expect(mockFn).toHaveBeenCalledTimes(1);
expect(mockFn).toHaveBeenCalledWith("arg1", "arg2");

// Mock with return value
const mockFnWithReturn = jest.fn().mockReturnValue(42);
expect(mockFnWithReturn()).toBe(42);

// Mock with implementation
const mockFnWithImpl = jest.fn((x, y) => x + y);
expect(mockFnWithImpl(2, 3)).toBe(5);

// Mock with resolved promise
const asyncMock = jest.fn().mockResolvedValue("async result");
await expect(asyncMock()).resolves.toBe("async result");

// Mock with rejected promise
const failingMock = jest.fn().mockRejectedValue(new Error("fail"));
await expect(failingMock()).rejects.toThrow("fail");

// Clear mock history
mockFn.mockClear();

// Reset mock (clear + remove implementation)
mockFn.mockReset();

// Restore original implementation (for spies)
mockFn.mockRestore();
```

### jest.mock() - Module Mocking

```typescript
// api.ts
export async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

export async function createUser(data: { name: string; email: string }) {
  const response = await fetch("/api/users", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return response.json();
}

// Mock the entire module
jest.mock("./api");
import { fetchUser, createUser } from "./api";
const mockFetchUser = jest.mocked(fetchUser);
const mockCreateUser = jest.mocked(createUser);

describe("API Mocking", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should mock fetchUser", async () => {
    mockFetchUser.mockResolvedValue({ id: "1", name: "John" });

    const user = await fetchUser("1");

    expect(user).toEqual({ id: "1", name: "John" });
    expect(mockFetchUser).toHaveBeenCalledWith("1");
  });

  it("should mock error response", async () => {
    mockFetchUser.mockRejectedValue(new Error("Network error"));

    await expect(fetchUser("1")).rejects.toThrow("Network error");
  });
});

// Mock with custom implementation
jest.mock("./api", () => ({
  fetchUser: jest.fn(),
  createUser: jest.fn(),
}));

// Partial mock (keep some real implementations)
jest.mock("./api", () => ({
  ...jest.requireActual("./api"),
  fetchUser: jest.fn(),
}));
```

### jest.spyOn() - Spy on Methods

```typescript
// productService.ts
export class ProductService {
  private inventory: Map<string, number> = new Map();

  getStock(productId: string): number {
    return this.inventory.get(productId) || 0;
  }

  updateStock(productId: string, quantity: number): void {
    const current = this.getStock(productId);
    this.inventory.set(productId, current + quantity);
  }
}

// notificationService.ts
export class NotificationService {
  sendLowStockAlert(productId: string, stock: number): void {
    console.log(`Low stock: ${productId} has ${stock} units`);
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

  processOrder(productId: string, quantity: number): boolean {
    if (!this.productService.isAvailable(productId, quantity)) {
      return false;
    }

    this.productService.updateStock(productId, -quantity);

    const newStock = this.productService.getStock(productId);
    if (newStock < 10) {
      this.notificationService.sendLowStockAlert(productId, newStock);
    }

    return true;
  }
}

// inventoryManager.test.ts
import { InventoryManager } from "./inventoryManager";
import { ProductService } from "./productService";
import { NotificationService } from "./notificationService";

describe("InventoryManager", () => {
  let manager: InventoryManager;
  let mockProductService: jest.Mocked<ProductService>;
  let mockNotificationService: jest.Mocked<NotificationService>;
  let sendAlertSpy: jest.SpyInstance;

  beforeEach(() => {
    mockProductService = {
      getStock: jest.fn(),
      updateStock: jest.fn(),
      isAvailable: jest.fn(),
    } as any;

    mockNotificationService = {
      sendLowStockAlert: jest.fn(),
    } as any;

    manager = new InventoryManager(mockProductService, mockNotificationService);
    sendAlertSpy = jest.spyOn(mockNotificationService, "sendLowStockAlert");
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("should process order and send low stock alert", () => {
    mockProductService.isAvailable.mockReturnValue(true);
    mockProductService.getStock.mockReturnValue(8);

    const result = manager.processOrder("widget", 5);

    expect(result).toBe(true);
    expect(mockProductService.updateStock).toHaveBeenCalledWith("widget", -5);
    expect(sendAlertSpy).toHaveBeenCalledWith("widget", 8);
  });

  it("should not send alert when stock is sufficient", () => {
    mockProductService.isAvailable.mockReturnValue(true);
    mockProductService.getStock.mockReturnValue(15);

    manager.processOrder("widget", 5);

    expect(sendAlertSpy).not.toHaveBeenCalled();
  });
});
```

### Manual Mocks

```typescript
// __mocks__/fs.ts
const fs = jest.createMockFromModule("fs");

let mockFiles: Record<string, string> = {};

fs.readFileSync = jest.fn((path: string) => {
  if (mockFiles[path]) {
    return mockFiles[path];
  }
  throw new Error(`File not found: ${path}`);
});

fs.writeFileSync = jest.fn((path: string, content: string) => {
  mockFiles[path] = content;
});

fs.__setMockFiles = (files: Record<string, string>) => {
  mockFiles = files;
};

fs.__clearMockFiles = () => {
  mockFiles = {};
};

module.exports = fs;

// Using manual mock
jest.mock("fs");
import * as fs from "fs";

describe("File Operations", () => {
  beforeEach(() => {
    (fs as any).__clearMockFiles();
  });

  it("should read file", () => {
    (fs as any).__setMockFiles({ "/test.txt": "hello" });

    const content = fs.readFileSync("/test.txt", "utf-8");
    expect(content).toBe("hello");
  });

  it("should throw for missing file", () => {
    expect(() => fs.readFileSync("/missing.txt", "utf-8")).toThrow(
      "File not found"
    );
  });
});
```

### API Mocking with MSW

```typescript
// mocks/handlers.ts
import { rest } from "msw";

export const handlers = [
  rest.get("/api/users", (req, res, ctx) => {
    return res(
      ctx.json([
        { id: "1", name: "John Doe", email: "john@example.com" },
        { id: "2", name: "Jane Smith", email: "jane@example.com" },
      ])
    );
  }),

  rest.get("/api/users/:id", (req, res, ctx) => {
    const { id } = req.params;

    if (id === "non-existent") {
      return res(ctx.status(404), ctx.json({ error: "User not found" }));
    }

    return res(
      ctx.json({
        id,
        name: "John Doe",
        email: "john@example.com",
      })
    );
  }),

  rest.post("/api/users", async (req, res, ctx) => {
    const body = await req.json();

    return res(
      ctx.status(201),
      ctx.json({
        id: "new-user-id",
        ...body,
      })
    );
  }),
];

// mocks/server.ts
import { setupServer } from "msw/node";
import { handlers } from "./handlers";

export const server = setupServer(...handlers);

// Setup and teardown
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Test file
import { render, screen, waitFor } from "@testing-library/react";
import { rest } from "msw";
import { server } from "../mocks/server";
import { UserList } from "./UserList";

describe("UserList with MSW", () => {
  it("should display users", async () => {
    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText("John Doe")).toBeInTheDocument();
      expect(screen.getByText("Jane Smith")).toBeInTheDocument();
    });
  });

  it("should handle API error", async () => {
    server.use(
      rest.get("/api/users", (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText("Failed to load users")).toBeInTheDocument();
    });
  });

  it("should handle empty response", async () => {
    server.use(
      rest.get("/api/users", (req, res, ctx) => {
        return res(ctx.json([]));
      })
    );

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText("No users found")).toBeInTheDocument();
    });
  });
});
```

### Mocking Timer Functions

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

// Mocking Date
describe("Date mocking", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  it("should use mocked date", () => {
    const mockDate = new Date("2024-01-15T10:00:00Z");
    jest.setSystemTime(mockDate);

    expect(new Date()).toEqual(mockDate);
    expect(Date.now()).toBe(mockDate.getTime());
  });

  it("should advance time", () => {
    const startTime = new Date("2024-01-15T10:00:00Z");
    jest.setSystemTime(startTime);

    jest.advanceTimersByTime(60 * 60 * 1000); // 1 hour

    expect(new Date().getHours()).toBe(11);
  });
});
```

### Mocking Fetch/Network Requests

```typescript
// api.ts
export async function fetchWithRetry(
  url: string,
  retries: number = 3
): Promise<any> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    } catch (error) {
      if (i === retries - 1) {
        throw error;
      }
    }
  }
}

// Option 1: Mock global fetch
describe("fetchWithRetry", () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it("should retry failed requests", async () => {
    const mockFetch = jest.fn()
      .mockRejectedValueOnce(new Error("Network error"))
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ data: "success" }),
      });

    global.fetch = mockFetch;

    const result = await fetchWithRetry("/api/data", 2);

    expect(result).toEqual({ data: "success" });
    expect(mockFetch).toHaveBeenCalledTimes(2);
  });

  it("should throw after all retries fail", async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error("Network error"));

    await expect(fetchWithRetry("/api/data", 3)).rejects.toThrow(
      "Network error"
    );
    expect(global.fetch).toHaveBeenCalledTimes(3);
  });
});

// Option 2: Use jest-fetch-mock
import fetchMock from "jest-fetch-mock";

beforeEach(() => {
  fetchMock.enableMocks();
});

afterEach(() => {
  fetchMock.disableMocks();
});

describe("with jest-fetch-mock", () => {
  it("should mock fetch response", async () => {
    fetchMock.mockResponseOnce(JSON.stringify({ data: "success" }));

    const result = await fetchWithRetry("/api/data");

    expect(result).toEqual({ data: "success" });
  });

  it("should mock fetch error", async () => {
    fetchMock.mockReject(new Error("Network error"));

    await expect(fetchWithRetry("/api/data")).rejects.toThrow("Network error");
  });
});
```

### Mocking Class Instances

```typescript
// emailService.ts
export class EmailService {
  async sendEmail(to: string, subject: string, body: string): Promise<boolean> {
    // Real implementation would call email API
    console.log(`Sending email to ${to}`);
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
        await this.sendEmail(recipient, subject, body);
        sent++;
      } catch {
        failed++;
      }
    }

    return { sent, failed };
  }
}

// Mock entire class
jest.mock("./emailService");
import { EmailService } from "./emailService";
const MockEmailService = jest.mocked(EmailService);

describe("EmailService Mock", () => {
  let emailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    emailService = new MockEmailService() as any;
    emailService.sendEmail.mockResolvedValue(true);
    emailService.sendBulkEmails.mockResolvedValue({ sent: 2, failed: 0 });
  });

  it("should mock sendEmail", async () => {
    const result = await emailService.sendEmail(
      "test@example.com",
      "Subject",
      "Body"
    );

    expect(result).toBe(true);
    expect(emailService.sendEmail).toHaveBeenCalledWith(
      "test@example.com",
      "Subject",
      "Body"
    );
  });

  it("should mock sendBulkEmails", async () => {
    const result = await emailService.sendBulkEmails(
      ["a@test.com", "b@test.com"],
      "Subject",
      "Body"
    );

    expect(result).toEqual({ sent: 2, failed: 0 });
  });
});
```

### Mocking with Factory Functions

```typescript
// factories/userFactory.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user" | "guest";
  createdAt: Date;
}

let userIdCounter = 1;

export const UserFactory = {
  build: (overrides: Partial<User> = {}): User => ({
    id: `user-${userIdCounter++}`,
    name: `Test User ${userIdCounter}`,
    email: `user${userIdCounter}@example.com`,
    role: "user",
    createdAt: new Date(),
    ...overrides,
  }),

  buildAdmin: (overrides: Partial<User> = {}): User =>
    UserFactory.build({ role: "admin", ...overrides }),

  buildGuest: (overrides: Partial<User> = {}): User =>
    UserFactory.build({ role: "guest", ...overrides }),

  buildList: (count: number, overrides: Partial<User> = {}): User[] =>
    Array.from({ length: count }, () => UserFactory.build(overrides)),

  reset: () => {
    userIdCounter = 1;
  },
};

// Using factory in tests
describe("UserService", () => {
  beforeEach(() => {
    UserFactory.reset();
  });

  it("should process admin user", async () => {
    const adminUser = UserFactory.buildAdmin({ name: "Admin" });
    const result = await service.processUser(adminUser);
    expect(result).toBe("admin-processing");
  });

  it("should handle multiple users", async () => {
    const users = UserFactory.buildList(5);
    const result = await service.processUsers(users);
    expect(result).toHaveLength(5);
  });
});
```

### Mocking Database

```typescript
// database.ts
export interface QueryResult<T = any> {
  rows: T[];
  rowCount: number;
}

export class Database {
  private data: Map<string, any[]> = new Map();

  async query<T = any>(sql: string, params?: any[]): Promise<QueryResult<T>> {
    // Real implementation would connect to database
    throw new Error("Not implemented");
  }

  async connect(): Promise<void> {
    // Real implementation
  }

  async disconnect(): Promise<void> {
    // Real implementation
  }
}

// Mock database
jest.mock("./database");
import { Database } from "./database";
const MockDatabase = jest.mocked(Database);

describe("Database Mock", () => {
  let db: jest.Mocked<Database>;
  let mockData: Record<string, any[]>;

  beforeEach(() => {
    db = new MockDatabase() as any;
    mockData = {
      users: [
        { id: "1", name: "John", email: "john@example.com" },
        { id: "2", name: "Jane", email: "jane@example.com" },
      ],
      products: [
        { id: "1", name: "Widget", price: 9.99 },
      ],
    };

    db.query.mockImplementation(async (sql: string, params?: any[]) => {
      // Simple mock implementation
      if (sql.includes("FROM users")) {
        return { rows: mockData.users, rowCount: mockData.users.length };
      }
      if (sql.includes("FROM products")) {
        return { rows: mockData.products, rowCount: mockData.products.length };
      }
      return { rows: [], rowCount: 0 };
    });

    db.connect.mockResolvedValue(undefined);
    db.disconnect.mockResolvedValue(undefined);
  });

  it("should query users", async () => {
    const result = await db.query("SELECT * FROM users");
    expect(result.rows).toHaveLength(2);
    expect(result.rows[0].name).toBe("John");
  });

  it("should connect and disconnect", async () => {
    await db.connect();
    expect(db.connect).toHaveBeenCalled();

    await db.disconnect();
    expect(db.disconnect).toHaveBeenCalled();
  });
});
```

## Real-World Use Cases

### 1. Testing Payment Processing

```typescript
// paymentService.ts
import { StripeClient } from "./stripe";
import { EmailService } from "./emailService";
import { Database } from "./database";

export class PaymentService {
  constructor(
    private stripe: StripeClient,
    private emailService: EmailService,
    private db: Database
  ) {}

  async processPayment(
    userId: string,
    amount: number,
    paymentMethodId: string
  ) {
    // 1. Create charge
    const charge = await this.stripe.charges.create({
      amount,
      currency: "usd",
      payment_method: paymentMethodId,
    });

    // 2. Save to database
    await this.db.query(
      "INSERT INTO payments (user_id, amount, stripe_id) VALUES ($1, $2, $3)",
      [userId, amount, charge.id]
    );

    // 3. Send receipt
    const user = await this.db.query("SELECT * FROM users WHERE id = $1", [
      userId,
    ]);
    await this.emailService.sendEmail({
      to: user.rows[0].email,
      subject: "Payment Receipt",
      body: `Your payment of $${amount / 100} was successful.`,
    });

    return charge;
  }
}

// paymentService.test.ts
import { PaymentService } from "./paymentService";
import { StripeClient } from "./stripe";
import { EmailService } from "./emailService";
import { Database } from "./database";

describe("PaymentService", () => {
  let paymentService: PaymentService;
  let mockStripe: jest.Mocked<StripeClient>;
  let mockEmailService: jest.Mocked<EmailService>;
  let mockDb: jest.Mocked<Database>;

  beforeEach(() => {
    mockStripe = {
      charges: {
        create: jest.fn(),
      },
    } as any;

    mockEmailService = {
      sendEmail: jest.fn(),
    } as any;

    mockDb = {
      query: jest.fn(),
    } as any;

    paymentService = new PaymentService(mockStripe, mockEmailService, mockDb);

    mockDb.query.mockResolvedValue({
      rows: [{ id: "user-1", email: "user@example.com" }],
      rowCount: 1,
    });
  });

  it("should process payment successfully", async () => {
    const mockCharge = { id: "ch_123", amount: 1000, status: "succeeded" };
    mockStripe.charges.create.mockResolvedValue(mockCharge);

    const result = await paymentService.processPayment("user-1", 1000, "pm_123");

    expect(result).toEqual(mockCharge);
    expect(mockStripe.charges.create).toHaveBeenCalledWith({
      amount: 1000,
      currency: "usd",
      payment_method: "pm_123",
    });
    expect(mockDb.query).toHaveBeenCalledWith(
      expect.stringContaining("INSERT INTO payments"),
      ["user-1", 1000, "ch_123"]
    );
    expect(mockEmailService.sendEmail).toHaveBeenCalledWith(
      expect.objectContaining({
        to: "user@example.com",
        subject: "Payment Receipt",
      })
    );
  });

  it("should handle payment failure", async () => {
    mockStripe.charges.create.mockRejectedValue(new Error("Card declined"));

    await expect(
      paymentService.processPayment("user-1", 1000, "pm_123")
    ).rejects.toThrow("Card declined");

    expect(mockDb.query).not.toHaveBeenCalledWith(
      expect.stringContaining("INSERT INTO payments"),
      expect.anything()
    );
  });
});
```

### 2. Testing File Operations

```typescript
// fileService.ts
import * as fs from "fs/promises";
import * as path from "path";

export class FileService {
  async readFile(filePath: string): Promise<string> {
    return fs.readFile(filePath, "utf-8");
  }

  async writeFile(filePath: string, content: string): Promise<void> {
    const dir = path.dirname(filePath);
    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(filePath, content, "utf-8");
  }

  async copyFile(src: string, dest: string): Promise<void> {
    await fs.copyFile(src, dest);
  }

  async deleteFile(filePath: string): Promise<void> {
    await fs.unlink(filePath);
  }
}

// fileService.test.ts
import * as fs from "fs/promises";
import { FileService } from "./fileService";

jest.mock("fs/promises");
const mockFs = jest.mocked(fs);

describe("FileService", () => {
  let fileService: FileService;

  beforeEach(() => {
    fileService = new FileService();
    jest.clearAllMocks();
  });

  describe("readFile", () => {
    it("should read file content", async () => {
      mockFs.readFile.mockResolvedValue("file content");

      const content = await fileService.readFile("/test.txt");

      expect(content).toBe("file content");
      expect(mockFs.readFile).toHaveBeenCalledWith("/test.txt", "utf-8");
    });

    it("should handle file not found", async () => {
      mockFs.readFile.mockRejectedValue(new Error("ENOENT"));

      await expect(fileService.readFile("/missing.txt")).rejects.toThrow(
        "ENOENT"
      );
    });
  });

  describe("writeFile", () => {
    it("should write file content", async () => {
      mockFs.mkdir.mockResolvedValue(undefined);
      mockFs.writeFile.mockResolvedValue(undefined);

      await fileService.writeFile("/test.txt", "content");

      expect(mockFs.mkdir).toHaveBeenCalledWith("/", { recursive: true });
      expect(mockFs.writeFile).toHaveBeenCalledWith(
        "/test.txt",
        "content",
        "utf-8"
      );
    });

    it("should create nested directories", async () => {
      mockFs.mkdir.mockResolvedValue(undefined);
      mockFs.writeFile.mockResolvedValue(undefined);

      await fileService.writeFile("/dir1/dir2/file.txt", "content");

      expect(mockFs.mkdir).toHaveBeenCalledWith("/dir1/dir2", {
        recursive: true,
      });
    });
  });
});
```

## Common Mistakes

### 1. Over-Mocking

```typescript
// ❌ BAD: Mocking everything
jest.mock("./user");
jest.mock("./email");
jest.mock("./database");
jest.mock("./utils");

it("should do something simple", async () => {
  // Everything is mocked - what are we actually testing?
});

// ✅ GOOD: Mock only external dependencies
jest.mock("./database");
jest.mock("./email");

it("should create user with valid data", async () => {
  // Test the actual business logic
});
```

### 2. Not Clearing Mocks

```typescript
// ❌ BAD: Mocks accumulate
const mockFn = jest.fn();

it("test 1", () => {
  mockFn("a");
});

it("test 2", () => {
  // mockFn still has history from test 1!
  expect(mockFn).toHaveBeenCalledTimes(0); // Might fail
});

// ✅ GOOD: Clear mocks
beforeEach(() => {
  jest.clearAllMocks();
});
```

### 3. Mocking Implementation Details

```typescript
// ❌ BAD: Mocking internal functions
class UserService {
  private hashPassword(password: string) {
    return `hashed_${password}`;
  }
}

it("should call hashPassword", () => {
  const spy = jest.spyOn(service as any, "hashPassword");
  service.createUser({ password: "test" });
  expect(spy).toHaveBeenCalled();
});

// ✅ GOOD: Mock external dependencies
jest.mock("./database");

it("should store hashed password", async () => {
  await service.createUser({ password: "test" });
  expect(mockDb.query).toHaveBeenCalledWith(
    expect.stringContaining("INSERT INTO users"),
    expect.arrayContaining([expect.stringContaining("hashed_")])
  );
});
```

## Best Practices

1. **Mock at the boundary**: Mock external services, not internal functions
2. **Clear mocks between tests**: Use `jest.clearAllMocks()` or `mockReset()`
3. **Use `jest.mocked()`**: Type-safe mocking for TypeScript
4. **Verify interactions**: Check that mocks were called correctly
5. **Restore mocks**: Use `jest.restoreAllMocks()` in `afterEach`
6. **Use MSW for API mocking**: Network-level mocking is more realistic
7. **Create mock factories**: Reusable test data builders
8. **Document mock behavior**: Comment complex mock implementations
9. **Keep mocks simple**: Avoid complex logic in mock implementations
10. **Test both success and failure**: Mock both successful and error responses

## Performance Considerations

### Mock Cleanup

```typescript
// Global setup
beforeAll(() => {
  jest.clearAllMocks();
});

afterAll(() => {
  jest.restoreAllMocks();
});

// Per test file
beforeEach(() => {
  jest.clearAllMocks();
});
```

### Efficient Mocking

```typescript
// ❌ BAD: Creating new mocks in each test
it("test 1", () => {
  const mock = jest.fn();
  // ...
});

it("test 2", () => {
  const mock = jest.fn();
  // ...
});

// ✅ GOOD: Shared mocks with reset
let mockService: jest.Mocked<Service>;

beforeEach(() => {
  mockService = createMockService();
  jest.clearAllMocks();
});
```

## Interview Questions

### Beginner (5-10)

1. **What is mocking in testing?**
   Mocking is replacing real objects with simulated versions to isolate code under test and control the test environment.

2. **Why do we need mocking?**
   For isolation, speed, control over responses, verification of interactions, and simulating error conditions.

3. **What is the difference between a mock and a stub?**
   Stubs return predefined values and don't track interactions. Mocks verify interactions and have expectations.

4. **What is `jest.fn()`?**
   Creates a mock function that tracks calls, arguments, and return values.

5. **What is `jest.mock()`?**
   Replaces an entire module with a mock implementation, auto-mocking all exports.

6. **What is `jest.spyOn()`?**
   Creates a spy on an existing method while preserving the original implementation.

7. **What is `jest.mocked()`?**
   A TypeScript helper that casts a module to its mocked version for type safety.

8. **How do you clear mock history?**
   Use `mockClear()`, `mockReset()`, or `jest.clearAllMocks()`.

9. **What is a manual mock?**
   A hand-written mock placed in `__mocks__` directory to replace a module.

10. **What is MSW?**
    Mock Service Worker is a library for mocking network requests at the network level.

### Intermediate (5-10)

11. **How do you mock API calls?**
    Use MSW for network-level mocking, or `jest.mock` for module-level mocking.

12. **How do you mock timers?**
    Use `jest.useFakeTimers()` and `jest.advanceTimersByTime()`.

13. **How do you mock class instances?**
    Mock the class constructor or use `jest.spyOn` on instance methods.

14. **How do you mock database operations?**
    Mock the database module or use in-memory database for testing.

15. **How do you mock file system operations?**
    Mock `fs` module or use `jest-fs-mock` library.

16. **How do you verify mock calls?**
    Use `toHaveBeenCalledWith`, `toHaveBeenCalledTimes`, `toHaveBeenLastCalledWith`.

17. **How do you mock error responses?**
    Use `mockRejectedValue` or `mockImplementation` to throw errors.

18. **How do you create partial mocks?**
    Use `jest.requireActual` and spread with overrides.

19. **How do you mock modules with dependencies?**
    Use factory functions in `jest.mock` or manual mocks.

20. **How do you mock global objects?**
    Assign to global properties or use `jest.spyOn(global, 'property')`.

### Senior (10-15)

21. **How do you design testable code for easy mocking?**
    Use dependency injection, interfaces, and composition over inheritance.

22. **How do you handle complex mocking scenarios?**
    Use mock factories, builders, and layered mocking strategies.

23. **How do you test code with multiple external dependencies?**
    Mock at service boundaries and verify interactions with each.

24. **How do you handle mocking in microservices?**
    Use contract testing and mock service virtualization.

25. **How do you mock GraphQL queries?**
    Use MSW for network-level GraphQL mocking.

26. **How do you mock WebSocket connections?**
    Mock WebSocket constructor or use in-memory WebSocket implementations.

27. **How do you mock real-time features?**
    Use controlled time or mock event emitters.

28. **How do you handle mocking in CI/CD?**
    Ensure mocks are deterministic and don't depend on environment.

29. **How do you test mocking code itself?**
    Verify mock behavior, test mock factories, and validate test setup.

30. **How do you balance mocking with real implementations?**
    Mock external dependencies, use real implementations for internal logic.

### FAANG-style (5-10)

31. **How would you design a mocking strategy for a large codebase?**
    Establish mocking guidelines, create shared utilities, and document patterns.

32. **How do you handle mocking in a microservices architecture?**
    Use contract testing, service virtualization, and mock API gateways.

33. **How do you ensure mock reliability at scale?**
    Implement mock validation, track mock health, and version mock contracts.

34. **How do you handle mocking with complex state machines?**
    Use mock state machines or test state transitions through public interfaces.

35. **How do you balance mock simplicity with test fidelity?**
    Mock at appropriate boundaries and maintain mock documentation.

### Follow-ups (5-10)

36. **How has your mocking approach evolved?**
    Discuss shift from over-mocking to strategic mocking at boundaries.

37. **What mocking tools have you used?**
    Compare Jest mocks, MSW, nock, and explain selection criteria.

38. **How do you handle mocking legacy code?**
    Characterization tests, extract and refactor, and gradual mock introduction.

39. **What's the most complex mocking problem you've solved?**
    Describe complex scenarios and solutions.

40. **How do you teach mocking to junior developers?**
    Start with simple examples, emphasize when to mock, and establish patterns.

## Summary

Mocking is essential for isolating tests and controlling the test environment. Key principles:

- **Mock at boundaries**: External services, not internal functions
- **Clear mocks between tests**: Prevent test pollution
- **Use type-safe mocking**: `jest.mocked()` for TypeScript
- **Verify interactions**: Check mocks were called correctly
- **Use MSW for API mocking**: Network-level mocking is more realistic
- **Create mock factories**: Reusable test data builders
- **Keep mocks simple**: Avoid complex logic in mocks
- **Document mock behavior**: Help future maintainers

A well-designed mocking strategy makes tests reliable, fast, and maintainable.

## References & Learn More

- [Jest Mocking Documentation](https://jestjs.io/docs/mock-functions)
- [MSW Documentation](https://mswjs.io/)
- "Test Driven Development" by Kent Beck
- "The Art of Unit Testing" by Roy Osherove
