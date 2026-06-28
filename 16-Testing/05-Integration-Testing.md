# Integration Testing

## Definition

Integration testing is a level of software testing where individual units or components are combined and tested as a group. The goal is to verify that different modules work correctly together when integrated, exposing defects in the interactions between components.

**Key Characteristics:**
- Tests interactions between multiple units
- Verifies data flow between components
- Tests interfaces and contracts between modules
- Moderate execution speed (seconds)
- Higher confidence than unit tests
- Uses real or partially mocked dependencies

**Integration Testing Position:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Testing Levels                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Unit Tests          Integration Tests        E2E Tests     │
│  ┌─────────┐         ┌─────────────────┐    ┌────────────┐ │
│  │ Function│         │ Multiple Units  │    │ Full       │ │
│  │ Class   │   ───▶  │ Working Together│ ──▶│ Application│ │
│  │ Module  │         │ API + Database  │    │ User Flow  │ │
│  └─────────┘         └─────────────────┘    └────────────┘ │
│                                                             │
│  • Isolated           • Component          • Complete       │
│  • Fast               • Moderate           • Slow          │
│  • Low confidence     • Medium confidence  • High conf.    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Why Do We Need It?

- **Verify Component Interactions**: Ensure modules work together correctly
- **Catch Interface Defects**: Find issues in data passing between components
- **Test Real Dependencies**: Verify behavior with actual databases, APIs, etc.
- **Higher Confidence**: More confidence than unit tests alone
- **Early Integration Discovery**: Find integration issues before E2E testing
- **API Contract Verification**: Ensure API consumers and providers agree
- **Database Integration**: Verify queries, transactions, and data integrity

## How It Works

### Integration Test Strategy

```
┌─────────────────────────────────────────────────────────────┐
│               Integration Testing Strategy                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Top-Down Approach                   │   │
│  │  Start with high-level modules                      │   │
│  │  Use stubs to simulate lower-level modules          │   │
│  │  Replace stubs with real modules incrementally      │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Bottom-Up Approach                  │   │
│  │  Start with low-level modules (utilities, DB)       │   │
│  │  Use drivers to simulate higher-level modules       │   │
│  │  Replace drivers with real modules incrementally    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Sandwich Approach                   │   │
│  │  Combine top-down and bottom-up                     │   │
│  │  Test from both ends toward middle                  │   │
│  │  Meet in the integration layer                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Common Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                Integration Test Categories                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Service Integration                                │   │
│  │  • API + Database                                   │   │
│  │  • Service A + Service B                           │   │
│  │  • Microservice communication                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  External System Integration                        │   │
│  │  • Payment gateways (Stripe, PayPal)               │   │
│  │  • Email services (SendGrid, SES)                  │   │
│  │  • Third-party APIs                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer Integration                                  │   │
│  │  • Controller → Service → Repository               │   │
│  │  • UI → API → Database                             │   │
│  │  • Frontend → Backend                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### API Integration Testing

```typescript
// userController.ts
import { Request, Response } from "express";
import { UserService } from "./userService";

export class UserController {
  constructor(private userService: UserService) {}

  async getUser(req: Request, res: Response): Promise<void> {
    try {
      const user = await this.userService.getUser(req.params.id);
      if (!user) {
        res.status(404).json({ error: "User not found" });
        return;
      }
      res.json(user);
    } catch (error) {
      res.status(500).json({ error: "Internal server error" });
    }
  }

  async createUser(req: Request, res: Response): Promise<void> {
    try {
      const user = await this.userService.createUser(req.body);
      res.status(201).json(user);
    } catch (error) {
      if (error instanceof ValidationError) {
        res.status(400).json({ error: error.message });
      } else {
        res.status(500).json({ error: "Internal server error" });
      }
    }
  }
}

// userService.ts
import { UserRepository } from "./userRepository";
import { EmailService } from "./emailService";

export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async getUser(id: string) {
    return this.userRepository.findById(id);
  }

  async createUser(data: CreateUserDto) {
    const existingUser = await this.userRepository.findByEmail(data.email);
    if (existingUser) {
      throw new ValidationError("Email already exists");
    }

    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcomeEmail(user.email);
    return user;
  }
}

// userRepository.ts
import { Database } from "./database";

export class UserRepository {
  constructor(private db: Database) {}

  async findById(id: string) {
    return this.db.query("SELECT * FROM users WHERE id = $1", [id]);
  }

  async findByEmail(email: string) {
    return this.db.query("SELECT * FROM users WHERE email = $1", [email]);
  }

  async create(data: CreateUserDto) {
    const result = await this.db.query(
      "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
      [data.name, data.email]
    );
    return result.rows[0];
  }
}

// user.integration.test.ts
import { UserService } from "./userService";
import { UserRepository } from "./userRepository";
import { EmailService } from "./emailService";
import { Database } from "./database";

describe("UserService Integration", () => {
  let userService: UserService;
  let db: Database;

  beforeAll(async () => {
    db = new Database();
    await db.connect();
    
    const userRepository = new UserRepository(db);
    const emailService = new EmailService();
    userService = new UserService(userRepository, emailService);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });

  describe("getUser", () => {
    it("should return user when exists", async () => {
      const created = await db.query(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
        ["John", "john@example.com"]
      );

      const user = await userService.getUser(created.rows[0].id);

      expect(user).toBeDefined();
      expect(user.name).toBe("John");
      expect(user.email).toBe("john@example.com");
    });

    it("should return null when user not exists", async () => {
      const user = await userService.getUser("non-existent-id");
      expect(user).toBeNull();
    });
  });

  describe("createUser", () => {
    it("should create new user", async () => {
      const userData = { name: "Jane", email: "jane@example.com" };

      const user = await userService.createUser(userData);

      expect(user).toBeDefined();
      expect(user.name).toBe("Jane");
      expect(user.email).toBe("jane@example.com");
    });

    it("should throw error for duplicate email", async () => {
      await db.query(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        ["Existing", "existing@example.com"]
      );

      await expect(
        userService.createUser({ name: "Jane", email: "existing@example.com" })
      ).rejects.toThrow("Email already exists");
    });

    it("should send welcome email", async () => {
      const emailService = {
        sendWelcomeEmail: jest.fn(),
      } as any;
      
      const userServiceWithMock = new UserService(
        new UserRepository(db),
        emailService
      );

      await userServiceWithMock.createUser({
        name: "Jane",
        email: "jane@example.com",
      });

      expect(emailService.sendWelcomeEmail).toHaveBeenCalledWith("jane@example.com");
    });
  });
});
```

### Database Integration Testing

```typescript
// productRepository.ts
import { Database } from "./database";

export interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

export class ProductRepository {
  constructor(private db: Database) {}

  async findAll(filters?: { category?: string; inStock?: boolean }) {
    let query = "SELECT * FROM products WHERE 1=1";
    const params: any[] = [];

    if (filters?.category) {
      params.push(filters.category);
      query += ` AND category = $${params.length}`;
    }

    if (filters?.inStock !== undefined) {
      params.push(filters.inStock);
      query += ` AND in_stock = $${params.length}`;
    }

    const result = await this.db.query(query, params);
    return result.rows;
  }

  async findById(id: string) {
    const result = await this.db.query("SELECT * FROM products WHERE id = $1", [id]);
    return result.rows[0] || null;
  }

  async create(product: Omit<Product, "id">) {
    const result = await this.db.query(
      "INSERT INTO products (name, price, category, in_stock) VALUES ($1, $2, $3, $4) RETURNING *",
      [product.name, product.price, product.category, product.inStock]
    );
    return result.rows[0];
  }

  async update(id: string, updates: Partial<Product>) {
    const setClauses = Object.keys(updates)
      .map((key, index) => `${key} = $${index + 1}`)
      .join(", ");
    
    const values = Object.values(updates);
    values.push(id);

    const result = await this.db.query(
      `UPDATE products SET ${setClauses} WHERE id = $${values.length} RETURNING *`,
      values
    );
    return result.rows[0];
  }

  async delete(id: string) {
    await this.db.query("DELETE FROM products WHERE id = $1", [id]);
  }

  async findByCategory(category: string) {
    const result = await this.db.query(
      "SELECT * FROM products WHERE category = $1 ORDER BY name",
      [category]
    );
    return result.rows;
  }
}

// productRepository.integration.test.ts
import { ProductRepository } from "./productRepository";
import { Database } from "./database";

describe("ProductRepository Integration", () => {
  let repository: ProductRepository;
  let db: Database;

  beforeAll(async () => {
    db = new Database();
    await db.connect();
    repository = new ProductRepository(db);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });

  describe("create", () => {
    it("should create a product", async () => {
      const productData = {
        name: "Widget",
        price: 9.99,
        category: "electronics",
        inStock: true,
      };

      const product = await repository.create(productData);

      expect(product).toBeDefined();
      expect(product.id).toBeDefined();
      expect(product.name).toBe("Widget");
      expect(product.price).toBe(9.99);
    });
  });

  describe("findAll", () => {
    beforeEach(async () => {
      await repository.create({ name: "Widget A", price: 10, category: "electronics", inStock: true });
      await repository.create({ name: "Widget B", price: 20, category: "electronics", inStock: false });
      await repository.create({ name: "Gadget", price: 30, category: "home", inStock: true });
    });

    it("should return all products", async () => {
      const products = await repository.findAll();
      expect(products).toHaveLength(3);
    });

    it("should filter by category", async () => {
      const products = await repository.findAll({ category: "electronics" });
      expect(products).toHaveLength(2);
      products.forEach((p) => expect(p.category).toBe("electronics"));
    });

    it("should filter by stock status", async () => {
      const products = await repository.findAll({ inStock: true });
      expect(products).toHaveLength(2);
      products.forEach((p) => expect(p.inStock).toBe(true));
    });

    it("should combine filters", async () => {
      const products = await repository.findAll({ category: "electronics", inStock: true });
      expect(products).toHaveLength(1);
      expect(products[0].name).toBe("Widget A");
    });
  });

  describe("update", () => {
    it("should update product fields", async () => {
      const product = await repository.create({
        name: "Widget",
        price: 10,
        category: "electronics",
        inStock: true,
      });

      const updated = await repository.update(product.id, { price: 15 });

      expect(updated.price).toBe(15);
      expect(updated.name).toBe("Widget");
    });
  });

  describe("delete", () => {
    it("should delete product", async () => {
      const product = await repository.create({
        name: "Widget",
        price: 10,
        category: "electronics",
        inStock: true,
      });

      await repository.delete(product.id);

      const found = await repository.findById(product.id);
      expect(found).toBeNull();
    });
  });
});
```

### External API Integration Testing

```typescript
// paymentGateway.ts
export interface PaymentResult {
  success: boolean;
  transactionId?: string;
  error?: string;
}

export class PaymentGateway {
  constructor(private apiKey: string) {}

  async processPayment(amount: number, currency: string): Promise<PaymentResult> {
    try {
      const response = await fetch("https://api.stripe.com/v1/charges", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          amount: String(Math.round(amount * 100)),
          currency,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        return { success: false, error: error.message };
      }

      const data = await response.json();
      return { success: true, transactionId: data.id };
    } catch (error) {
      return { success: false, error: "Network error" };
    }
  }

  async refund(transactionId: string): Promise<PaymentResult> {
    // Similar implementation
    return { success: true, transactionId };
  }
}

// payment.integration.test.ts
import { PaymentGateway } from "./paymentGateway";
import { rest } from "msw";
import { setupServer } from "msw/node";

const server = setupServer(
  rest.post("https://api.stripe.com/v1/charges", async (req, res, ctx) => {
    const body = await req.text();
    const params = new URLSearchParams(body);
    const amount = parseInt(params.get("amount") || "0");

    if (amount <= 0) {
      return res(
        ctx.status(400),
        ctx.json({ message: "Invalid amount" })
      );
    }

    return res(
      ctx.json({
        id: `ch_${Date.now()}`,
        amount,
        status: "succeeded",
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("PaymentGateway Integration", () => {
  let gateway: PaymentGateway;

  beforeEach(() => {
    gateway = new PaymentGateway("test-api-key");
  });

  it("should process payment successfully", async () => {
    const result = await gateway.processPayment(50.00, "usd");

    expect(result.success).toBe(true);
    expect(result.transactionId).toBeDefined();
    expect(result.transactionId).toMatch(/^ch_/);
  });

  it("should handle payment failure", async () => {
    server.use(
      rest.post("https://api.stripe.com/v1/charges", (req, res, ctx) => {
        return res(
          ctx.status(402),
          ctx.json({ message: "Card declined" })
        );
      })
    );

    const result = await gateway.processPayment(50.00, "usd");

    expect(result.success).toBe(false);
    expect(result.error).toBe("Card declined");
  });

  it("should handle network errors", async () => {
    server.use(
      rest.post("https://api.stripe.com/v1/charges", (req, res, ctx) => {
        return res.networkError("Connection failed");
      })
    );

    const result = await gateway.processPayment(50.00, "usd");

    expect(result.success).toBe(false);
    expect(result.error).toBe("Network error");
  });

  it("should reject invalid amounts", async () => {
    const result = await gateway.processPayment(-10, "usd");

    expect(result.success).toBe(false);
    expect(result.error).toBe("Invalid amount");
  });
});
```

### Service Layer Integration

```typescript
// orderService.ts
import { ProductRepository } from "./productRepository";
import { PaymentGateway } from "./paymentGateway";
import { EmailService } from "./emailService";

export interface Order {
  id: string;
  userId: string;
  items: Array<{ productId: string; quantity: number }>;
  total: number;
  status: "pending" | "confirmed" | "shipped" | "delivered";
}

export class OrderService {
  constructor(
    private productRepository: ProductRepository,
    private paymentGateway: PaymentGateway,
    private emailService: EmailService
  ) {}

  async createOrder(userId: string, items: Array<{ productId: string; quantity: number }>) {
    // 1. Validate products exist and are in stock
    for (const item of items) {
      const product = await this.productRepository.findById(item.productId);
      if (!product) {
        throw new Error(`Product ${item.productId} not found`);
      }
      if (!product.inStock) {
        throw new Error(`Product ${product.name} is out of stock`);
      }
    }

    // 2. Calculate total
    let total = 0;
    for (const item of items) {
      const product = await this.productRepository.findById(item.productId);
      total += product.price * item.quantity;
    }

    // 3. Process payment
    const paymentResult = await this.paymentGateway.processPayment(total, "usd");
    if (!paymentResult.success) {
      throw new Error(`Payment failed: ${paymentResult.error}`);
    }

    // 4. Create order (simplified - would normally save to database)
    const order: Order = {
      id: `order_${Date.now()}`,
      userId,
      items,
      total,
      status: "confirmed",
    };

    // 5. Send confirmation email
    await this.emailService.sendOrderConfirmation(order);

    return order;
  }
}

// orderService.integration.test.ts
import { OrderService, Order } from "./orderService";
import { ProductRepository } from "./productRepository";
import { PaymentGateway } from "./paymentGateway";
import { EmailService } from "./emailService";
import { Database } from "./database";

describe("OrderService Integration", () => {
  let orderService: OrderService;
  let productRepository: ProductRepository;
  let paymentGateway: PaymentGateway;
  let emailService: EmailService;
  let db: Database;

  beforeAll(async () => {
    db = new Database();
    await db.connect();
    
    productRepository = new ProductRepository(db);
    paymentGateway = new PaymentGateway("test-key");
    emailService = new EmailService();
    
    orderService = new OrderService(
      productRepository,
      paymentGateway,
      emailService
    );
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
    // Seed test products
    await productRepository.create({
      name: "Widget",
      price: 10,
      category: "electronics",
      inStock: true,
    });
    await productRepository.create({
      name: "Gadget",
      price: 20,
      category: "electronics",
      inStock: false,
    });
  });

  describe("createOrder", () => {
    it("should create order with valid items", async () => {
      const product = await productRepository.findById(
        (await productRepository.findAll())[0].id
      );

      const order = await orderService.createOrder("user123", [
        { productId: product.id, quantity: 2 },
      ]);

      expect(order).toBeDefined();
      expect(order.status).toBe("confirmed");
      expect(order.total).toBe(20);
      expect(order.userId).toBe("user123");
    });

    it("should throw error for non-existent product", async () => {
      await expect(
        orderService.createOrder("user123", [
          { productId: "non-existent", quantity: 1 },
        ])
      ).rejects.toThrow("Product non-existent not found");
    });

    it("should throw error for out of stock product", async () => {
      const outOfStockProduct = await productRepository.findById(
        (await productRepository.findAll())[1].id
      );

      await expect(
        orderService.createOrder("user123", [
          { productId: outOfStockProduct.id, quantity: 1 },
        ])
      ).rejects.toThrow("is out of stock");
    });
  });
});
```

### Message Queue Integration

```typescript
// messageQueue.ts
export interface Message<T = any> {
  id: string;
  type: string;
  payload: T;
  timestamp: Date;
}

export class MessageQueue {
  private handlers: Map<string, (message: Message) => Promise<void>> = new Map();
  private messages: Message[] = [];

  async publish(message: Message): Promise<void> {
    this.messages.push(message);
    const handler = this.handlers.get(message.type);
    if (handler) {
      await handler(message);
    }
  }

  subscribe(type: string, handler: (message: Message) => Promise<void>): void {
    this.handlers.set(type, handler);
  }

  getMessages(): Message[] {
    return [...this.messages];
  }
}

// notificationService.ts
import { MessageQueue, Message } from "./messageQueue";

export interface Notification {
  id: string;
  userId: string;
  type: "email" | "sms" | "push";
  content: string;
  sent: boolean;
}

export class NotificationService {
  private notifications: Notification[] = [];

  constructor(private messageQueue: MessageQueue) {
    this.setupSubscriptions();
  }

  private setupSubscriptions() {
    this.messageQueue.subscribe("ORDER_CREATED", async (message) => {
      const { orderId, userId, email } = message.payload;
      await this.sendOrderConfirmation(orderId, userId, email);
    });

    this.messageQueue.subscribe("PAYMENT_RECEIVED", async (message) => {
      const { paymentId, userId, amount } = message.payload;
      await this.sendPaymentReceipt(paymentId, userId, amount);
    });
  }

  async sendOrderConfirmation(orderId: string, userId: string, email: string) {
    const notification: Notification = {
      id: `notif_${Date.now()}`,
      userId,
      type: "email",
      content: `Your order ${orderId} has been confirmed`,
      sent: true,
    };
    this.notifications.push(notification);
    return notification;
  }

  async sendPaymentReceipt(paymentId: string, userId: string, amount: number) {
    const notification: Notification = {
      id: `notif_${Date.now()}`,
      userId,
      type: "email",
      content: `Payment of $${amount} received`,
      sent: true,
    };
    this.notifications.push(notification);
    return notification;
  }

  getNotificationsByUser(userId: string): Notification[] {
    return this.notifications.filter((n) => n.userId === userId);
  }
}

// messageQueue.integration.test.ts
import { MessageQueue } from "./messageQueue";
import { NotificationService } from "./notificationService";

describe("MessageQueue Integration", () => {
  let messageQueue: MessageQueue;
  let notificationService: NotificationService;

  beforeEach(() => {
    messageQueue = new MessageQueue();
    notificationService = new NotificationService(messageQueue);
  });

  it("should deliver ORDER_CREATED message to handler", async () => {
    const message = {
      id: "msg_1",
      type: "ORDER_CREATED",
      payload: {
        orderId: "order_123",
        userId: "user_456",
        email: "user@example.com",
      },
      timestamp: new Date(),
    };

    await messageQueue.publish(message);

    const notifications = notificationService.getNotificationsByUser("user_456");
    expect(notifications).toHaveLength(1);
    expect(notifications[0].content).toContain("order_123");
  });

  it("should deliver PAYMENT_RECEIVED message to handler", async () => {
    const message = {
      id: "msg_2",
      type: "PAYMENT_RECEIVED",
      payload: {
        paymentId: "pay_789",
        userId: "user_456",
        amount: 99.99,
      },
      timestamp: new Date(),
    };

    await messageQueue.publish(message);

    const notifications = notificationService.getNotificationsByUser("user_456");
    expect(notifications).toHaveLength(1);
    expect(notifications[0].content).toContain("99.99");
  });

  it("should not crash when no handler exists", async () => {
    const message = {
      id: "msg_3",
      type: "UNKNOWN_TYPE",
      payload: {},
      timestamp: new Date(),
    };

    await expect(messageQueue.publish(message)).resolves.not.toThrow();
  });
});
```

## Real-World Use Cases

### 1. Testing a Complete Request Flow

```typescript
// app.ts
import express from "express";
import { UserController } from "./userController";
import { UserService } from "./userService";
import { UserRepository } from "./userRepository";
import { Database } from "./database";
import { EmailService } from "./emailService";

export function createApp(db: Database) {
  const app = express();
  
  const emailService = new EmailService();
  const userRepository = new UserRepository(db);
  const userService = new UserService(userRepository, emailService);
  const userController = new UserController(userService);

  app.use(express.json());
  
  app.get("/api/users/:id", (req, res) => userController.getUser(req, res));
  app.post("/api/users", (req, res) => userController.createUser(req, res));

  return app;
}

// app.integration.test.ts
import request from "supertest";
import { createApp } from "./app";
import { Database } from "./database";

describe("API Integration", () => {
  let app: any;
  let db: Database;

  beforeAll(async () => {
    db = new Database();
    await db.connect();
    app = createApp(db);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });

  describe("GET /api/users/:id", () => {
    it("should return user when exists", async () => {
      const result = await db.query(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
        ["John", "john@example.com"]
      );
      const userId = result.rows[0].id;

      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);

      expect(response.body).toMatchObject({
        id: userId,
        name: "John",
        email: "john@example.com",
      });
    });

    it("should return 404 when user not exists", async () => {
      await request(app)
        .get("/api/users/non-existent")
        .expect(404);
    });
  });

  describe("POST /api/users", () => {
    it("should create new user", async () => {
      const response = await request(app)
        .post("/api/users")
        .send({ name: "Jane", email: "jane@example.com" })
        .expect(201);

      expect(response.body).toMatchObject({
        name: "Jane",
        email: "jane@example.com",
      });
      expect(response.body.id).toBeDefined();
    });

    it("should return 400 for invalid data", async () => {
      await request(app)
        .post("/api/users")
        .send({ name: "" })
        .expect(400);
    });

    it("should return 409 for duplicate email", async () => {
      await db.query(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        ["Existing", "existing@example.com"]
      );

      await request(app)
        .post("/api/users")
        .send({ name: "Jane", email: "existing@example.com" })
        .expect(409);
    });
  });
});
```

### 2. Testing with Test Containers

```typescript
// docker-compose.test.yml
/*
version: '3.8'
services:
  test-db:
    image: postgres:14
    environment:
      POSTGRES_DB: testdb
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
    ports:
      - "5433:5432"
*/

// testContainer.ts
import { PostgreSqlContainer, StartedPostgreSqlContainer } from "testcontainers";

let container: StartedPostgreSqlContainer;

export async function startTestDatabase() {
  container = await new PostgreSqlContainer("postgres:14")
    .withDatabase("testdb")
    .withUsername("testuser")
    .withPassword("testpass")
    .start();

  return container.getConnectionUri();
}

export async function stopTestDatabase() {
  if (container) {
    await container.stop();
  }
}

// With test containers
import { startTestDatabase, stopTestDatabase } from "./testContainer";
import { Database } from "./database";

describe("Database Integration with Test Containers", () => {
  let db: Database;
  let connectionString: string;

  beforeAll(async () => {
    connectionString = await startTestDatabase();
    db = new Database(connectionString);
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
    await stopTestDatabase();
  });

  it("should connect to test database", async () => {
    const result = await db.query("SELECT 1 as value");
    expect(result.rows[0].value).toBe(1);
  });
});
```

## Common Mistakes

### 1. Testing Too Much in Integration Tests

```typescript
// ❌ BAD: Testing implementation details
it("should call repository method", async () => {
  const spy = jest.spyOn(userRepository, "create");
  await service.createUser(data);
  expect(spy).toHaveBeenCalled();
});

// ✅ GOOD: Testing behavior
it("should create user in database", async () => {
  const user = await service.createUser(data);
  const found = await db.query("SELECT * FROM users WHERE id = $1", [user.id]);
  expect(found.rows).toHaveLength(1);
});
```

### 2. Not Cleaning Up Test Data

```typescript
// ❌ BAD: Test data persists
beforeAll(async () => {
  await db.connect();
});

// ✅ GOOD: Clean up before each test
beforeEach(async () => {
  await db.clear();
});
```

### 3. Using Production Database

```typescript
// ❌ BAD: Testing against production
const db = new Database(process.env.PRODUCTION_DB_URL);

// ✅ GOOD: Use test database
const db = new Database(process.env.TEST_DB_URL);
```

## Best Practices

1. **Use test databases** that mirror production
2. **Clean up test data** before/after each test
3. **Mock external services** that are slow or unreliable
4. **Test real interactions** between components
5. **Use transactions** that rollback after tests
6. **Test error scenarios** and edge cases
7. **Keep tests independent** - no shared state
8. **Use fixtures** for consistent test data
9. **Test contracts** between services
10. **Monitor test execution time** and optimize

## Performance Considerations

### Test Database Setup

```typescript
// Use transactions for fast cleanup
beforeEach(async () => {
  await db.beginTransaction();
});

afterEach(async () => {
  await db.rollback();
});

// Or use database snapshots
beforeAll(async () => {
  await db.createSnapshot();
});

afterAll(async () => {
  await db.restoreSnapshot();
});
```

### Parallel Test Execution

```typescript
// jest.config.js
module.exports = {
  projects: [
    {
      displayName: "integration-api",
      testMatch: ["<rootDir>/src/**/*.api.test.ts"],
      testEnvironment: "node",
      // Run API tests in parallel
    },
    {
      displayName: "integration-db",
      testMatch: ["<rootDir>/src/**/*.db.test.ts"],
      testEnvironment: "node",
      // Run DB tests sequentially (shared database)
      maxWorkers: 1,
    },
  ],
};
```

## Interview Questions

### Beginner (5-10)

1. **What is integration testing?**
   Integration testing verifies that multiple units or components work correctly together.

2. **How is integration testing different from unit testing?**
   Unit tests verify individual components in isolation. Integration tests verify interactions between components.

3. **What should you test in integration tests?**
   API endpoints, database operations, service interactions, and data flow between components.

4. **How do you test database operations?**
   Use a test database, create test data, verify queries work correctly, and clean up after tests.

5. **What is a test container?**
   A test container is a lightweight, disposable Docker container used for integration testing.

6. **How do you mock external APIs?**
   Use tools like MSW (Mock Service Worker) or nock to intercept network requests.

7. **Why should you clean up test data?**
   To ensure test isolation and prevent tests from affecting each other.

8. **What is contract testing?**
   Contract testing verifies that API consumers and providers agree on the interface.

9. **How do you test error handling in integration tests?**
   Test both success and error scenarios, verify appropriate error responses.

10. **What is the test pyramid?**
    Many unit tests, fewer integration tests, few E2E tests - balancing speed and confidence.

### Intermediate (5-10)

11. **How do you test microservices?**
    Use contract testing, integration tests with real dependencies, and E2E tests for critical flows.

12. **What is an API contract?**
    The interface definition that specifies endpoints, request/response formats, and behavior.

13. **How do you handle flaky integration tests?**
    Fix timing issues, ensure proper cleanup, use deterministic test data, and isolate tests.

14. **How do you test with message queues?**
    Mock the queue or use in-memory implementations, verify message handling.

15. **What is the difference between integration and E2E testing?**
    Integration tests verify component interactions. E2E tests verify complete user workflows.

16. **How do you test authentication/authorization?**
    Test with valid/invalid tokens, verify access control for different user roles.

17. **How do you test file uploads/downloads?**
    Use test files, mock storage services, verify file handling logic.

18. **What is test data management?**
    Creating, maintaining, and cleaning up test data for integration tests.

19. **How do you test with caching?**
    Test cache hits/misses, verify cache invalidation, test cache warming.

20. **How do you handle test environment setup?**
    Use Docker, test containers, or infrastructure as code for consistent environments.

### Senior (10-15)

21. **How do you design testable architecture?**
    Apply SOLID principles, use dependency injection, and design clear boundaries.

22. **How do you test distributed systems?**
    Use chaos engineering, distributed tracing, and resilience testing.

23. **What is chaos engineering?**
    Intentionally introducing failures to test system resilience and recovery.

24. **How do you test event-driven architectures?**
    Verify event publishing, handling, and eventual consistency.

25. **How do you handle test data in CI/CD?**
    Use fixtures, factories, and database migrations for consistent test data.

26. **How do you test API versioning?**
    Test backward compatibility, version negotiation, and deprecation handling.

27. **How do you test multi-tenant applications?**
    Verify data isolation, tenant-specific configurations, and access control.

28. **How do you test real-time features?**
    Test WebSocket connections, pub/sub patterns, and real-time updates.

29. **How do you handle testing in cloud environments?**
    Use cloud-specific test utilities, mock cloud services, and test deployment pipelines.

30. **How do you measure integration test effectiveness?**
    Track defect detection rate, test execution time, and maintenance burden.

### FAANG-style (5-10)

31. **How would you design integration testing for a microservices architecture?**
    Contract testing, integration tests with service virtualization, and E2E tests for critical paths.

32. **How do you handle testing in a CI/CD pipeline?**
    Implement test stages, parallel execution, and fail-fast mechanisms.

33. **How do you ensure test reliability at scale?**
    Implement flakiness detection, quarantine system, and stability metrics.

34. **How do you test with real-time data processing?**
    Use deterministic test data, verify processing pipelines, and test error handling.

35. **How do you balance test coverage with execution time?**
    Prioritize critical paths, use test impact analysis, and optimize test suite.

### Follow-ups (5-10)

36. **How has your integration testing approach evolved?**
    Discuss adoption of contract testing, test containers, and shift-left practices.

37. **What tools have you used for integration testing?**
    Compare Jest, Supertest, Testcontainers, and MSW.

38. **How do you handle testing legacy systems?**
    Characterization tests, strangler fig pattern, and gradual migration.

39. **What's the most challenging integration testing problem you've solved?**
    Describe complex integration scenarios and solutions.

40. **How do you train teams on integration testing?**
    Start with simple examples, establish patterns, and share best practices.

## Summary

Integration testing is essential for verifying that components work together correctly. Key principles:

- **Test real interactions** between components
- **Use test databases** and mock external services
- **Clean up test data** to ensure isolation
- **Test both success and error scenarios**
- **Use contract testing** for API verification
- **Keep tests maintainable** with fixtures and factories
- **Balance coverage with execution time**
- **Integrate into CI/CD** for continuous feedback

A well-designed integration test suite catches issues that unit tests miss while providing higher confidence than E2E tests alone.

## References & Learn More

- "Integration Testing" by Martin Fowler
- Testcontainers Documentation
- MSW (Mock Service Worker) Documentation
- Pact Contract Testing
- Testing Microservices by Sam Newman
