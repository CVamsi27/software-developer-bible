# Test Patterns

## Definition

Test patterns are established, reusable solutions to common problems encountered when writing tests. They provide structure, consistency, and maintainability to test suites. These patterns have evolved through years of practice and help teams write better, more readable, and more maintainable tests.

**Key Patterns:**

- **AAA (Arrange-Act-Assert)**: Standard test structure
- **Given-When-Then (BDD)**: Behavior-focused test structure
- **Factory Pattern**: Creating test data objects
- **Test Data Builder**: Flexible test data construction
- **Fixture Pattern**: Reusable test setup
- **Object Mother**: Centralized test data creation

**Pattern Hierarchy:**

```text
┌─────────────────────────────────────────────────────────────┐
│                    Test Pattern Hierarchy                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Structural Patterns                     │   │
│  │  • AAA (Arrange-Act-Assert)                         │   │
│  │  • Given-When-Then (BDD)                            │   │
│  │  • Four Phase Test                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Data Patterns                           │   │
│  │  • Factory Pattern                                  │   │
│  │  • Test Data Builder                                │   │
│  │  • Object Mother                                    │   │
│  │  • Fixture                                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Interaction Patterns                    │   │
│  │  • Spy Object                                       │   │
│  │  • Mock Object                                      │   │
│  │  • Stub                                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

## Why Do We Need It?

- **Consistency**: Teams follow agreed-upon patterns
- **Readability**: Tests are easier to understand
- **Maintainability**: Patterns reduce duplication and complexity
- **Best Practices**: Patterns embody testing wisdom
- **Onboarding**: New team members learn patterns quickly
- **Code Review**: Patterns provide review criteria
- **Refactoring**: Patterns guide test restructuring
- **Quality**: Patterns prevent common testing mistakes

## How It Works

### AAA (Arrange-Act-Assert) Pattern

```text
┌─────────────────────────────────────────────────────────────┐
│                   AAA Pattern Structure                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    ARRANGE                           │   │
│  │  • Set up test data                                 │   │
│  │  • Initialize objects                               │   │
│  │  • Configure mocks/stubs                           │   │
│  │  • Prepare expected values                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                     ACT                              │   │
│  │  • Execute the code under test                      │   │
│  │  • Call the method/function                         │   │
│  │  • Trigger the behavior                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    ASSERT                            │   │
│  │  • Verify expected outcome                          │   │
│  │  • Check return values                              │   │
│  │  • Verify state changes                             │   │
│  │  • Confirm mock interactions                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

### Given-When-Then (BDD) Pattern

```text
┌─────────────────────────────────────────────────────────────┐
│                  BDD Pattern Structure                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    GIVEN                             │   │
│  │  • Pre-conditions                                   │   │
│  │  • Initial state                                    │   │
│  │  • Context setup                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    WHEN                              │   │
│  │  • Action performed                                 │   │
│  │  • Event triggered                                  │   │
│  │  • Operation executed                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    THEN                              │   │
│  │  • Expected outcome                                 │   │
│  │  • State change                                     │   │
│  │  • Side effects                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### AAA Pattern Implementation

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

  getHistory(): string[] {
    return [...this.history];
  }

  clearHistory(): void {
    this.history = [];
  }
}

// calculator.test.ts - AAA Pattern
import { Calculator } from "./calculator";

describe("Calculator", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      // Arrange
      const calculator = new Calculator();
      const a = 2;
      const b = 3;

      // Act
      const result = calculator.add(a, b);

      // Assert
      expect(result).toBe(5);
    });

    it("should track addition in history", () => {
      // Arrange
      const calculator = new Calculator();

      // Act
      calculator.add(2, 3);

      // Assert
      expect(calculator.getHistory()).toHaveLength(1);
      expect(calculator.getHistory()[0]).toBe("2 + 3 = 5");
    });
  });

  describe("clearHistory", () => {
    it("should clear all history entries", () => {
      // Arrange
      const calculator = new Calculator();
      calculator.add(1, 2);
      calculator.subtract(5, 3);

      // Act
      calculator.clearHistory();

      // Assert
      expect(calculator.getHistory()).toHaveLength(0);
    });
  });
});

```

### BDD Pattern Implementation

```typescript
// userService.ts
export interface User {
  id: string;
  name: string;
  email: string;
  isActive: boolean;
}

export class UserService {
  private users: Map<string, User> = new Map();

  createUser(name: string, email: string): User {
    if (this.findByEmail(email)) {
      throw new Error("Email already exists");
    }

    const user: User = {
      id: `user-${Date.now()}`,
      name,
      email,
      isActive: true,
    };

    this.users.set(user.id, user);
    return user;
  }

  deactivateUser(id: string): boolean {
    const user = this.users.get(id);
    if (!user) {
      return false;
    }

    user.isActive = false;
    return true;
  }

  findByEmail(email: string): User | undefined {
    return Array.from(this.users.values()).find((u) => u.email === email);
  }
}

// userService.test.ts - BDD Pattern
import { UserService } from "./userService";

describe("UserService", () => {
  let userService: UserService;

  beforeEach(() => {
    userService = new UserService();
  });

  describe("createUser", () => {
    describe("given a valid name and email", () => {
      it("should create a new user", () => {
        // Given
        const name = "John Doe";
        const email = "john@example.com";

        // When
        const user = userService.createUser(name, email);

        // Then
        expect(user).toBeDefined();
        expect(user.name).toBe(name);
        expect(user.email).toBe(email);
        expect(user.isActive).toBe(true);
      });
    });

    describe("given an email that already exists", () => {
      it("should throw an error", () => {
        // Given
        userService.createUser("John", "john@example.com");

        // When & Then
        expect(() => {
          userService.createUser("Jane", "john@example.com");
        }).toThrow("Email already exists");
      });
    });
  });

  describe("deactivateUser", () => {
    describe("given an existing user", () => {
      it("should deactivate the user", () => {
        // Given
        const user = userService.createUser("John", "john@example.com");

        // When
        const result = userService.deactivateUser(user.id);

        // Then
        expect(result).toBe(true);
        expect(userService.findByEmail("john@example.com")?.isActive).toBe(
          false
        );
      });
    });

    describe("given a non-existing user", () => {
      it("should return false", () => {
        // Given
        const nonExistingId = "non-existing";

        // When
        const result = userService.deactivateUser(nonExistingId);

        // Then
        expect(result).toBe(false);
      });
    });
  });
});

```

### Factory Pattern

```typescript
// factories/userFactory.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user" | "guest";
  isActive: boolean;
  createdAt: Date;
}

interface UserTraits {
  admin?: boolean;
  guest?: boolean;
  inactive?: boolean;
}

let userIdCounter = 1;

export const UserFactory = {
  build: (overrides: Partial<User> = {}, traits: UserTraits = {}): User => {
    const defaults: User = {
      id: `user-${userIdCounter++}`,
      name: `Test User ${userIdCounter}`,
      email: `user${userIdCounter}@example.com`,
      role: "user",
      isActive: true,
      createdAt: new Date(),
    };

    // Apply traits
    if (traits.admin) {
      defaults.role = "admin";
    }
    if (traits.guest) {
      defaults.role = "guest";
    }
    if (traits.inactive) {
      defaults.isActive = false;
    }

    return { ...defaults, ...overrides };
  },

  buildList: (count: number, overrides: Partial<User> = {}): User[] => {
    return Array.from({ length: count }, () => UserFactory.build(overrides));
  },

  reset: () => {
    userIdCounter = 1;
  },
};

// Using factory in tests
describe("User Service", () => {
  beforeEach(() => {
    UserFactory.reset();
  });

  it("should process admin users differently", () => {
    const adminUser = UserFactory.build({}, { admin: true });
    expect(adminUser.role).toBe("admin");
  });

  it("should handle inactive users", () => {
    const inactiveUser = UserFactory.build({}, { inactive: true });
    expect(inactiveUser.isActive).toBe(false);
  });

  it("should create list of users", () => {
    const users = UserFactory.buildList(5);
    expect(users).toHaveLength(5);
    expect(new Set(users.map((u) => u.id)).size).toBe(5); // All unique
  });
});

```

### Test Data Builder Pattern

```typescript
// builders/userBuilder.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user" | "guest";
  profile: {
    avatar?: string;
    bio?: string;
    location?: string;
  };
}

export class UserBuilder {
  private user: Partial<User> = {
    id: `user-${Date.now()}`,
    name: "Test User",
    email: "test@example.com",
    role: "user",
    profile: {},
  };

  static create(): UserBuilder {
    return new UserBuilder();
  }

  withId(id: string): this {
    this.user.id = id;
    return this;
  }

  withName(name: string): this {
    this.user.name = name;
    return this;
  }

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  asAdmin(): this {
    this.user.role = "admin";
    return this;
  }

  asGuest(): this {
    this.user.role = "guest";
    return this;
  }

  withAvatar(avatar: string): this {
    this.user.profile = { ...this.user.profile, avatar };
    return this;
  }

  withBio(bio: string): this {
    this.user.profile = { ...this.user.profile, bio };
    return this;
  }

  withLocation(location: string): this {
    this.user.profile = { ...this.user.profile, location };
    return this;
  }

  build(): User {
    return this.user as User;
  }
}

// Using builder in tests
describe("User Profile", () => {
  it("should display complete user profile", () => {
    const user = UserBuilder.create()
      .withName("John Doe")
      .withEmail("john@example.com")
      .asAdmin()
      .withAvatar("https://example.com/avatar.jpg")
      .withBio("Software Engineer")
      .withLocation("New York")
      .build();

    const profile = renderUserProfile(user);

    expect(profile).toContain("John Doe");
    expect(profile).toContain("Software Engineer");
  });

  it("should handle minimal user data", () => {
    const user = UserBuilder.create()
      .withName("Minimal User")
      .withEmail("minimal@example.com")
      .build();

    expect(user.profile.avatar).toBeUndefined();
    expect(user.profile.bio).toBeUndefined();
  });
});

```

### Object Mother Pattern

```typescript
// mothers/userObjectMother.ts
import { User } from "../models/user";

export class UserObjectMother {
  static createAdmin(): User {
    return {
      id: "admin-1",
      name: "Admin User",
      email: "admin@example.com",
      role: "admin",
      isActive: true,
      permissions: ["read", "write", "delete"],
    };
  }

  static createRegularUser(): User {
    return {
      id: "user-1",
      name: "Regular User",
      email: "user@example.com",
      role: "user",
      isActive: true,
      permissions: ["read"],
    };
  }

  static createGuestUser(): User {
    return {
      id: "guest-1",
      name: "Guest User",
      email: "guest@example.com",
      role: "guest",
      isActive: true,
      permissions: [],
    };
  }

  static createInactiveUser(): User {
    return {
      ...this.createRegularUser(),
      id: "inactive-1",
      name: "Inactive User",
      email: "inactive@example.com",
      isActive: false,
    };
  }

  static createCustomUser(overrides: Partial<User>): User {
    return {
      ...this.createRegularUser(),
      ...overrides,
    };
  }
}

// Using Object Mother
describe("Authorization Service", () => {
  it("should allow admin to access all resources", () => {
    const admin = UserObjectMother.createAdmin();
    expect(authorizationService.canAccess(admin, "resource")).toBe(true);
  });

  it("should restrict guest access", () => {
    const guest = UserObjectMother.createGuestUser();
    expect(authorizationService.canAccess(guest, "resource")).toBe(false);
  });

  it("should deny access for inactive users", () => {
    const inactive = UserObjectMother.createInactiveUser();
    expect(authorizationService.canAccess(inactive, "resource")).toBe(false);
  });
});

```

### Fixture Pattern

```typescript
// fixtures/userFixture.ts
import { Database } from "../database";
import { User } from "../models/user";

export class UserFixture {
  private db: Database;

  constructor(db: Database) {
    this.db = db;
  }

  async create(overrides: Partial<User> = {}): Promise<User> {
    const userData: User = {
      id: `fixture-user-${Date.now()}`,
      name: "Fixture User",
      email: `fixture-${Date.now()}@example.com`,
      role: "user",
      isActive: true,
      ...overrides,
    };

    await this.db.query(
      "INSERT INTO users (id, name, email, role, is_active) VALUES ($1, $2, $3, $4, $5)",
      [userData.id, userData.name, userData.email, userData.role, userData.isActive]
    );

    return userData;
  }

  async createAdmin(): Promise<User> {
    return this.create({ role: "admin" });
  }

  async createList(count: number): Promise<User[]> {
    const users: User[] = [];
    for (let i = 0; i < count; i++) {
      users.push(await this.create({ name: `User ${i + 1}` }));
    }
    return users;
  }

  async cleanup(): Promise<void> {
    await this.db.query("DELETE FROM users WHERE id LIKE 'fixture-user-%'");
  }
}

// Using fixtures
describe("User API", () => {
  let userFixture: UserFixture;

  beforeAll(async () => {
    userFixture = new UserFixture(db);
  });

  afterEach(async () => {
    await userFixture.cleanup();
  });

  it("should get user by id", async () => {
    const user = await userFixture.create({ name: "Test User" });

    const response = await request(app).get(`/api/users/${user.id}`);

    expect(response.body.name).toBe("Test User");
  });

  it("should list all users", async () => {
    await userFixture.createList(3);

    const response = await request(app).get("/api/users");

    expect(response.body).toHaveLength(3);
  });
});

```

### Four Phase Test Pattern

```typescript
// Four Phase Test: Setup → Exercise → Verify → Teardown
describe("Shopping Cart", () => {
  let cart: ShoppingCart;
  let product: Product;

  // Phase 1: Setup
  beforeEach(async () => {
    cart = new ShoppingCart();
    product = await productFixture.create({ price: 10 });
  });

  // Phase 2: Exercise (in each test)
  it("should calculate total correctly", () => {
    // Exercise
    cart.addItem(product, 2);
    const total = cart.getTotal();

    // Verify
    expect(total).toBe(20);
  });

  // Phase 4: Teardown (automatic with Jest)
  // Jest automatically cleans up after each test
});

```

### Helper Pattern

```typescript
// helpers/testHelpers.ts
import { render, RenderResult } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider } from "../context/ThemeContext";
import { AuthProvider } from "../context/AuthContext";

export const renderWithProviders = (
  ui: React.ReactElement,
  options: {
    route?: string;
    isAuthenticated?: boolean;
    theme?: "light" | "dark";
  } = {}
): RenderResult => {
  const {
    route = "/",
    isAuthenticated = false,
    theme = "light",
  } = options;

  // Setup
  window.history.pushState({}, "Test page", route);

  const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <BrowserRouter>
      <ThemeProvider initialTheme={theme}>
        <AuthProvider isAuthenticated={isAuthenticated}>
          {children}
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );

  return render(ui, { wrapper: Wrapper });
};

// Using helper
describe("UserProfile", () => {
  it("should display user info when authenticated", () => {
    renderWithProviders(<UserProfile />, { isAuthenticated: true });

    expect(screen.getByText("Welcome!")).toBeInTheDocument();
  });

  it("should redirect to login when not authenticated", () => {
    renderWithProviders(<UserProfile />, {
      isAuthenticated: false,
      route: "/profile",
    });

    expect(screen.getByText("Please log in")).toBeInTheDocument();
  });
});

```

### Snapshot Testing Pattern

```typescript
// Component snapshot testing
import { render } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("should render primary button", () => {
    const { container } = render(
      <Button variant="primary">Click me</Button>
    );
    expect(container).toMatchSnapshot();
  });

  it("should render secondary button", () => {
    const { container } = render(
      <Button variant="secondary">Click me</Button>
    );
    expect(container).toMatchSnapshot();
  });

  it("should render disabled button", () => {
    const { container } = render(
      <Button disabled>Click me</Button>
    );
    expect(container).toMatchSnapshot();
  });
});

// Inline snapshots for small outputs
it("should generate correct ID", () => {
  const id = generateId("user", "john@example.com");
  expect(id).toMatchInlineSnapshot();
});

```

### Parameterized Testing Pattern

```typescript
// Parameterized tests
describe("Email validation", () => {
  const testCases = [
    { input: "user@example.com", expected: true },
    { input: "invalid-email", expected: false },
    { input: "@example.com", expected: false },
    { input: "user@", expected: false },
    { input: "user@.com", expected: false },
    { input: "user@example", expected: false },
  ];

  testCases.forEach(({ input, expected }) => {
    it(`should validate "${input}" as ${expected ? "valid" : "invalid"}`, () => {
      expect(isValidEmail(input)).toBe(expected);
    });
  });
});

// Or using test.each (Jest)
describe("Math operations", () => {
  test.each([
    [1, 2, 3],
    [2, 3, 5],
    [0, 0, 0],
    [-1, 1, 0],
  ])("adding %i and %i should give %i", (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
  });
});

```

## Real-World Use Cases

### 1. Testing Complex Business Logic

```typescript
// orderService.ts
export class OrderService {
  calculateDiscount(order: Order, user: User): number {
    let discount = 0;

    // Base discount for large orders
    if (order.total > 100) {
      discount += 10;
    }

    // VIP user discount
    if (user.isVip) {
      discount += 5;
    }

    // First order discount
    if (user.orderCount === 0) {
      discount += 15;
    }

    return Math.min(discount, 50); // Max 50% discount
  }
}

// orderService.test.ts
import { OrderService } from "./orderService";
import { UserBuilder } from "../builders/userBuilder";

describe("OrderService", () => {
  let service: OrderService;

  beforeEach(() => {
    service = new OrderService();
  });

  describe("calculateDiscount", () => {
    it.each([
      {
        description: "small order for regular user",
        order: { total: 50 },
        user: UserBuilder.create().build(),
        expected: 0,
      },
      {
        description: "large order for regular user",
        order: { total: 150 },
        user: UserBuilder.create().build(),
        expected: 10,
      },
      {
        description: "first order for any user",
        order: { total: 50 },
        user: UserBuilder.create().withOrderCount(0).build(),
        expected: 15,
      },
      {
        description: "VIP user",
        order: { total: 50 },
        user: UserBuilder.create().asVip().build(),
        expected: 5,
      },
      {
        description: "maximum discount cap",
        order: { total: 200 },
        user: UserBuilder.create().asVip().withOrderCount(0).build(),
        expected: 50,
      },
    ])(
      "should apply correct discount for $description",
      ({ order, user, expected }) => {
        const discount = service.calculateDiscount(order, user);
        expect(discount).toBe(expected);
      }
    );
  });
});

```

### 2. Testing State Machines

```typescript
// orderStateMachine.ts
type OrderState = "pending" | "confirmed" | "shipped" | "delivered";

interface OrderEvent {
  type: "CONFIRM" | "SHIP" | "DELIVER";
}

const transitions: Record<OrderState, Partial<Record<OrderEvent["type"], OrderState>>> = {
  pending: { CONFIRM: "confirmed" },
  confirmed: { SHIP: "shipped" },
  shipped: { DELIVER: "delivered" },
  delivered: {},
};

export class OrderStateMachine {
  private state: OrderState = "pending";

  getState(): OrderState {
    return this.state;
  }

  transition(event: OrderEvent["type"]): OrderState {
    const nextState = transitions[this.state]?.[event];
    if (!nextState) {
      throw new Error(`Invalid transition: ${this.state} -> ${event}`);
    }
    this.state = nextState;
    return this.state;
  }
}

// State machine tests
describe("OrderStateMachine", () => {
  let machine: OrderStateMachine;

  beforeEach(() => {
    machine = new OrderStateMachine();
  });

  describe("valid transitions", () => {
    it.each([
      ["pending", "CONFIRM", "confirmed"],
      ["confirmed", "SHIP", "shipped"],
      ["shipped", "DELIVER", "delivered"],
    ] as const)(
      "should transition from %s to %s on %s",
      (from, event, expected) => {
        // Arrange
        // Set up state machine to be in 'from' state
        if (from !== "pending") {
          machine.transition("CONFIRM");
        }
        if (from === "shipped") {
          machine.transition("SHIP");
        }

        // Act
        const result = machine.transition(event);

        // Assert
        expect(result).toBe(expected);
      }
    );
  });

  describe("invalid transitions", () => {
    it.each([
      ["pending", "SHIP"],
      ["pending", "DELIVER"],
      ["confirmed", "DELIVER"],
      ["delivered", "CONFIRM"],
    ] as const)("should throw on invalid transition %s -> %s", (from, event) => {
      // Arrange
      if (from === "confirmed") {
        machine.transition("CONFIRM");
      }
      if (from === "delivered") {
        machine.transition("CONFIRM");
        machine.transition("SHIP");
        machine.transition("DELIVER");
      }

      // Act & Assert
      expect(() => machine.transition(event)).toThrow("Invalid transition");
    });
  });
});

```

### 3. Testing Async Operations

```typescript
// asyncService.ts
export class AsyncService {
  async fetchDataWithRetry(
    url: string,
    retries: number = 3
  ): Promise<any> {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      } catch (error) {
        if (i === retries - 1) {
          throw error;
        }
        await this.delay(1000 * (i + 1)); // Exponential backoff
      }
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// asyncService.test.ts
import { AsyncService } from "./asyncService";

describe("AsyncService", () => {
  let service: AsyncService;

  beforeEach(() => {
    service = new AsyncService();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe("fetchDataWithRetry", () => {
    it("should return data on first successful attempt", async () => {
      const mockData = { id: 1, name: "Test" };
      global.fetch = jest.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockData),
      });

      const promise = service.fetchDataWithRetry("/api/data");
      const result = await promise;

      expect(result).toEqual(mockData);
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    it("should retry on failure and succeed", async () => {
      const mockData = { id: 1, name: "Test" };
      global.fetch = jest
        .fn()
        .mockRejectedValueOnce(new Error("Network error"))
        .mockResolvedValue({
          ok: true,
          json: () => Promise.resolve(mockData),
        });

      const promise = service.fetchDataWithRetry("/api/data", 2);

      // Advance past first retry delay
      jest.advanceTimersByTime(1000);

      const result = await promise;

      expect(result).toEqual(mockData);
      expect(global.fetch).toHaveBeenCalledTimes(2);
    });

    it("should throw after all retries fail", async () => {
      global.fetch = jest.fn().mockRejectedValue(new Error("Network error"));

      const promise = service.fetchDataWithRetry("/api/data", 2);

      // Advance past retry delays
      jest.advanceTimersByTime(3000);

      await expect(promise).rejects.toThrow("Network error");
      expect(global.fetch).toHaveBeenCalledTimes(2);
    });
  });
});

```

## Common Mistakes

### 1. Mixing AAA with BDD

```typescript
// ❌ BAD: Inconsistent structure
describe("Calculator", () => {
  it("should add numbers", () => {
    // Given
    const calc = new Calculator();
    // When
    const result = calc.add(1, 2);
    // Then
    expect(result).toBe(3);
  });

  it("should subtract numbers", () => {
    const calc = new Calculator();
    const result = calc.subtract(5, 3);
    expect(result).toBe(2);
  });
});

// ✅ GOOD: Consistent structure
describe("Calculator", () => {
  describe("add", () => {
    it("should add two numbers", () => {
      // Arrange
      const calc = new Calculator();
      // Act
      const result = calc.add(1, 2);
      // Assert
      expect(result).toBe(3);
    });
  });
});

```

### 2. Too Many Assertions

```typescript
// ❌ BAD: Testing too many things
it("should process order correctly", () => {
  const result = service.processOrder(order);

  expect(result.status).toBe("success");
  expect(result.total).toBe(100);
  expect(result.items).toHaveLength(3);
  expect(result.shipping).toBeDefined();
  expect(result.payment).toBeDefined();
  expect(result.email).toBeDefined();
  // ... too many assertions
});

// ✅ FOCUSED: One behavior per test
it("should set order status to success", () => {
  const result = service.processOrder(order);
  expect(result.status).toBe("success");
});

it("should calculate order total", () => {
  const result = service.processOrder(order);
  expect(result.total).toBe(100);
});

```

### 3. Not Using Setup/Teardown

```typescript
// ❌ BAD: Duplicated setup
it("test 1", () => {
  const db = new Database();
  db.connect();
  // test logic
  db.disconnect();
});

it("test 2", () => {
  const db = new Database();
  db.connect();
  // test logic
  db.disconnect();
});

// ✅ GOOD: Use lifecycle hooks
let db: Database;

beforeEach(() => {
  db = new Database();
  db.connect();
});

afterEach(() => {
  db.disconnect();
});

it("test 1", () => {
  // test logic with shared db
});

it("test 2", () => {
  // test logic with shared db
});

```

## Best Practices

1. **Be consistent**: Choose a pattern and stick with it

2. **Keep tests focused**: One behavior per test

3. **Use descriptive names**: Test names should explain behavior

4. **Follow AAA**: Arrange, Act, Assert for clarity

5. **Use factories**: Create reusable test data builders

6. **Clean up resources**: Use lifecycle hooks properly

7. **Avoid test interdependence**: Tests should run independently

8. **Use helpers**: Extract common test utilities

9. **Document patterns**: Help team members understand conventions
10. **Refactor regularly**: Keep test code maintainable

## Performance Considerations

### Efficient Test Structure

```typescript
// ❌ BAD: Slow - repeated setup
it("test 1", async () => {
  const db = await createDatabase();
  await db.seed();
  // ...
  await db.cleanup();
});

it("test 2", async () => {
  const db = await createDatabase();
  await db.seed();
  // ...
  await db.cleanup();
});

// ✅ GOOD: Shared setup
beforeEach(async () => {
  db = await createDatabase();
  await db.seed();
});

afterEach(async () => {
  await db.cleanup();
});

```

## Interview Questions

### Beginner (5-10)

1. **What is the AAA pattern?**
   Arrange-Act-Assert: set up test data, execute code under test, verify results.

2. **What is BDD?**
   Behavior-Driven Development: tests written in Given-When-Then format focusing on behavior.

3. **What is a test factory?**
   A pattern for creating test data objects with sensible defaults and customization.

4. **What is a test data builder?**
   A fluent API for constructing complex test objects step by step.

5. **What is an Object Mother?**
   A class with static methods that create predefined test objects.

6. **Why use lifecycle hooks?**
   To share setup/teardown code and avoid duplication across tests.

7. **What is parameterized testing?**
   Running the same test logic with different inputs and expected outputs.

8. **What is snapshot testing?**
   Capturing rendered output and comparing it to stored snapshots.

9. **What are test helpers?**
   Reusable functions that simplify common test operations.

10. **Why is consistency important in tests?**
    Makes tests easier to read, understand, and maintain.

### Intermediate (5-10)

11. **When should you use AAA vs BDD?**
    AAA for simple tests, BDD for complex business logic and stakeholder communication.

12. **How do you handle test data dependencies?**
    Use fixtures, factories, or builders to create isolated test data.

13. **What is the difference between factories and builders?**
    Factories create objects with defaults. Builders provide step-by-step construction.

14. **How do you test complex state machines?**
    Test each valid and invalid transition, use parameterized tests.

15. **How do you handle test cleanup?**
    Use afterEach/afterAll hooks, transactions, or fixtures with cleanup.

16. **What is the Four Phase Test pattern?**
    Setup → Exercise → Verify → Teardown: explicit test phases.

17. **How do you test async operations?**
    Use async/await, mock timers, and proper waiting strategies.

18. **When should you use snapshot testing?**
    For UI components to catch unexpected visual changes.

19. **How do you test edge cases systematically?**
    Use parameterized tests with comprehensive test cases.

20. **What is the difference between fixtures and factories?**
    Fixtures are pre-defined data. Factories create data dynamically.

### Senior (10-15)

21. **How do you choose test patterns for a codebase?**
    Consider team expertise, codebase complexity, and maintainability needs.

22. **How do you refactor tests to use patterns?**
    Start with AAA, extract helpers, create factories as needed.

23. **How do you handle testing complex business rules?**
    Use parameterized tests, decision tables, or specification pattern.

24. **How do you test distributed systems?**
    Use contract testing, integration tests, and chaos engineering.

25. **How do you handle test data management at scale?**
    Use fixtures, factories, and test data management tools.

26. **How do you ensure test maintainability?**
    Follow SOLID principles, extract helpers, and refactor regularly.

27. **How do you handle testing legacy code?**
    Use characterization tests, strangler fig pattern, and gradual improvement.

28. **How do you test infrastructure as code?**
    Use Terratest, validate configurations, and test deployments.

29. **How do you handle testing in CI/CD?**
    Implement test stages, parallel execution, and failure notifications.

30. **How do you measure test pattern effectiveness?**
    Track maintenance burden, test readability, and defect detection rate.

### FAANG-style (5-10)

31. **How would you design test patterns for a large organization?**
    Establish guidelines, create shared utilities, and document conventions.

32. **How do you handle testing microservices?**
    Use contract testing, service virtualization, and integration tests.

33. **How do you ensure consistency across teams?**
    Create testing standards, shared libraries, and code review processes.

34. **How do you handle testing with complex dependencies?**
    Use dependency injection, mock at boundaries, and test contracts.

35. **How do you balance test patterns with pragmatic testing?**
    Choose patterns that provide value, avoid over-engineering.

### Follow-ups (5-10)

36. **How has your use of test patterns evolved?**
    Discuss adoption of factories, builders, and parameterized tests.

37. **What test patterns have you found most valuable?**
    AAA, factories, and parameterized tests for most situations.

38. **How do you introduce test patterns to a team?**
    Start with simple examples, establish patterns gradually.

39. **What's the most complex testing pattern you've implemented?**
    Describe complex scenarios and solutions.

40. **How do you balance patterns with simplicity?**
    Choose appropriate patterns, avoid over-engineering.

## Summary

Test patterns provide structure and consistency to test suites. Key patterns:

- **AAA**: Standard test structure for clarity
- **BDD**: Behavior-focused for complex business logic
- **Factories**: Reusable test data creation
- **Builders**: Flexible object construction
- **Object Mother**: Predefined test objects
- **Fixtures**: Reusable test setup
- **Parameterized**: Data-driven testing
- **Helpers**: Common test utilities

Choose patterns that fit your team's needs and codebase complexity.

## References & Learn More

- "xUnit Test Patterns" by Gerard Meszaros
- "Growing Object-Oriented Software, Guided by Tests" by Steve Freeman
- "The Art of Unit Testing" by Roy Osherove
- Martin Fowler's blog on testing patterns
