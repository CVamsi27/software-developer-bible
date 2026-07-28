---
section: Testing
category: Quality
tags: [overview, reference]
---

# Testing Overview

## Definition

Testing is the systematic process of evaluating a software application to identify defects, verify that requirements are met, and ensure the system behaves as expected under various conditions. In modern software development, testing is not merely a phase but an integral practice woven throughout the entire development lifecycle.

**Testing Pyramid** is a strategic model proposed by Mike Cohn that guides teams on how to distribute their testing efforts across different levels. It recommends having a large base of unit tests, a moderate layer of integration tests, and a small top layer of end-to-end (E2E) tests.

**Test-Driven Development (TDD)** is a software development approach where tests are written before the actual code. The developer writes a failing test, writes minimal code to pass the test, and then refactors the code while keeping tests green.

**Behavior-Driven Development (BDD)** extends TDD by writing test cases in natural language that non-technical stakeholders can understand. It focuses on the behavior of the application from the user's perspective using Given-When-Then syntax.

## Why Do We Need It?

- **Catch Bugs Early**: Finding bugs in development is 10-100x cheaper than in production
- **Regression Safety**: Tests ensure new changes don't break existing functionality
- **Documentation**: Tests serve as living documentation of how the system should behave
- **Refactoring Confidence**: With comprehensive tests, you can refactor code fearlessly
- **Team Collaboration**: Tests create a shared understanding of requirements
- **Code Quality**: Writing testable code naturally leads to better architecture
- **CI/CD Enablement**: Automated tests are the foundation of continuous integration and deployment
- **Reduced Debugging Time**: Well-tested code requires less time debugging in production

## How It Works

### The Testing Pyramid

```text
                    /\
                   /  \
                  / E2E \          Few in number, slow, expensive
                 /--------\
                /Integration\      Moderate number, moderate speed
               /--------------\
              /    Unit Tests    \   Many in number, fast, cheap
             /--------------------\
            /    Static Analysis   \  Linting, type checking, always running
           /------------------------\

```

**Base Layer - Unit Tests (70%)**

- Test individual functions, classes, or components in isolation
- Fast execution (milliseconds)
- Low maintenance cost
- High granularity

**Middle Layer - Integration Tests (20%)**

- Test interactions between multiple units
- Verify modules work together correctly
- Moderate execution time
- Medium maintenance cost

**Top Layer - E2E Tests (10%)**

- Test complete user workflows through the entire application
- Slow execution (seconds to minutes)
- High maintenance cost
- Lowest granularity but highest confidence

### Testing Types Comparison

```text
+------------------+------------+----------+---------+----------------+

| Type             | Speed      | Cost     | Scope   | Confidence     |

+------------------+------------+----------+---------+----------------+

| Unit             | Very Fast  | Low      | Single  | Low-Medium     |
| Integration      | Medium     | Medium   | Multiple| Medium-High    |
| E2E              | Slow       | High     | Full    | High           |
| Smoke            | Fast       | Low      | Critical| Quick Check    |
| Regression       | Varies     | High     | Full    | High           |
| Performance      | Slow       | High     | System  | Varies         |
| Security         | Medium     | High     | Varies  | High           |

+------------------+------------+----------+---------+----------------+

```

### TDD Cycle (Red-Green-Refactor)

```text
    ┌─────────────────┐
    │   Write a       │
    │   Failing Test  │◄──────────────────────────────┐
    │   (RED)         │                               │
    └────────┬────────┘                               │
             │                                        │
             ▼                                        │
    ┌─────────────────┐                               │
    │   Write Minimal │                               │
    │   Code to Pass  │                               │
    │   (GREEN)       │                               │
    └────────┬────────┘                               │
             │                                        │
             ▼                                        │
    ┌─────────────────┐                               │
    │   Refactor      │                               │
    │   Code & Tests  │                               │
    │   (REFACTOR)    │                               │
    └────────┬────────┘                               │
             │                                        │
             └────────────────────────────────────────┘

```

### BDD Workflow

```text
Feature: User Login
  As a registered user
  I want to log into the application
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid email and password
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see a welcome message

```

### When to Write Tests

```text
+-----------------------------+--------------------------------+

| Situation                   | When to Write Tests            |

+-----------------------------+--------------------------------+

| New Feature                 | Before implementation (TDD)    |
| Bug Fix                     | Before fixing (reproduce first)|
| Refactoring                 | Before refactoring             |
| Complex Logic               | Immediately                    |
| API Endpoint                | During development             |
| UI Component                | During development             |
| Performance Critical Code   | With performance tests         |
| Security Sensitive Code     | With security tests            |

+-----------------------------+--------------------------------+

```

### Testing Philosophy Spectrum

```text
  Pragmatic                                      Dogmatic
    │                                               │
    │  ┌─────────────────────────────────────────┐  │
    │  │  "Test everything that could             │  │
    │  │   possibly break"                        │  │
    │  └─────────────────────────────────────────┘  │
    │                    │                           │
    │  ┌─────────────────┼─────────────────────────┐│
    │  │                 │                         ││
    │  ▼                 ▼                         ▼│
    │  80/20        Kent Beck             Test      ││
    │  Rule         Philosophy            Everything││
    │  (Pragmatic)  (Balanced)            (Dogmatic)││
    └────────────────────────────────────────────────┘

```

## Code Examples

### Basic Unit Test with Jest

```typescript
// math.ts
export function add(a: number, b: number): number {
  return a + b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

export function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error("Division by zero");
  }
  return a / b;
}

// math.test.ts
import { add, multiply, divide } from "./math";

describe("Math functions", () => {
  describe("add", () => {
    it("should add two positive numbers", () => {
      expect(add(2, 3)).toBe(5);
    });

    it("should add negative numbers", () => {
      expect(add(-1, -1)).toBe(-2);
    });

    it("should handle zero", () => {
      expect(add(5, 0)).toBe(5);
    });
  });

  describe("divide", () => {
    it("should divide two numbers", () => {
      expect(divide(10, 2)).toBe(5);
    });

    it("should throw error when dividing by zero", () => {
      expect(() => divide(10, 0)).toThrow("Division by zero");
    });
  });
});

```

### TDD Example - Shopping Cart

```typescript
// Step 1: Write the failing test FIRST
// shopping-cart.test.ts
import { ShoppingCart } from "./shopping-cart";

describe("ShoppingCart", () => {
  let cart: ShoppingCart;

  beforeEach(() => {
    cart = new ShoppingCart();
  });

  it("should start with empty cart", () => {
    expect(cart.getItems()).toHaveLength(0);
    expect(cart.getTotal()).toBe(0);
  });

  it("should add items to cart", () => {
    cart.addItem({ id: "1", name: "Widget", price: 9.99, quantity: 1 });

    expect(cart.getItems()).toHaveLength(1);
    expect(cart.getTotal()).toBe(9.99);
  });

  it("should calculate total with multiple items", () => {
    cart.addItem({ id: "1", name: "Widget", price: 10, quantity: 2 });
    cart.addItem({ id: "2", name: "Gadget", price: 20, quantity: 1 });

    expect(cart.getTotal()).toBe(40);
  });

  it("should remove items from cart", () => {
    cart.addItem({ id: "1", name: "Widget", price: 9.99, quantity: 1 });
    cart.removeItem("1");

    expect(cart.getItems()).toHaveLength(0);
    expect(cart.getTotal()).toBe(0);
  });

  it("should update item quantity", () => {
    cart.addItem({ id: "1", name: "Widget", price: 10, quantity: 1 });
    cart.updateQuantity("1", 3);

    expect(cart.getTotal()).toBe(30);
  });

  it("should apply discount code", () => {
    cart.addItem({ id: "1", name: "Widget", price: 100, quantity: 1 });
    cart.applyDiscount("SAVE10");

    expect(cart.getTotal()).toBe(90);
  });

  it("should throw error for invalid discount", () => {
    expect(() => cart.applyDiscount("INVALID")).toThrow("Invalid discount code");
  });
});

// Step 2: Write minimal code to pass
// shopping-cart.ts
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

const DISCOUNT_CODES: Record<string, number> = {
  SAVE10: 0.1,
  SAVE20: 0.2,
};

export class ShoppingCart {
  private items: CartItem[] = [];
  private discountPercentage: number = 0;

  getItems(): CartItem[] {
    return [...this.items];
  }

  getTotal(): number {
    const subtotal = this.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
    return subtotal * (1 - this.discountPercentage);
  }

  addItem(item: CartItem): void {
    const existing = this.items.find((i) => i.id === item.id);
    if (existing) {
      existing.quantity += item.quantity;
    } else {
      this.items.push({ ...item });
    }
  }

  removeItem(id: string): void {
    this.items = this.items.filter((item) => item.id !== id);
  }

  updateQuantity(id: string, quantity: number): void {
    const item = this.items.find((i) => i.id === id);
    if (item) {
      item.quantity = quantity;
    }
  }

  applyDiscount(code: string): void {
    const discount = DISCOUNT_CODES[code];
    if (discount === undefined) {
      throw new Error("Invalid discount code");
    }
    this.discountPercentage = discount;
  }
}

```

### BDD Example with Cucumber-style

```typescript
// features/login.feature
/*
Feature: User Login
  As a user
  I want to log into the application
  So that I can access my account

  Background:
    Given I am on the login page

  Scenario: Successful login
    When I enter email "user@example.com"
    And I enter password "validPassword123"
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see "Welcome back!"

  Scenario: Failed login with wrong password
    When I enter email "user@example.com"
    And I enter password "wrongPassword"
    And I click the login button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page
*/

// Step definitions would be implemented in TypeScript
// using a framework like Cucumber.js or Serenity/JS

```

### Integration Test Example

```typescript
// userService.integration.test.ts
import { UserService } from "./user-service";
import { Database } from "./database";
import { EmailService } from "./email-service";

describe("UserService Integration", () => {
  let userService: UserService;
  let db: Database;

  beforeAll(async () => {
    db = new Database();
    await db.connect();
    const emailService = new EmailService();
    userService = new UserService(db, emailService);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });

  it("should create and retrieve a user", async () => {
    const userData = {
      email: "test@example.com",
      name: "Test User",
      password: "hashedPassword",
    };

    const createdUser = await userService.create(userData);
    const foundUser = await userService.findById(createdUser.id);

    expect(foundUser).toBeDefined();
    expect(foundUser.email).toBe(userData.email);
    expect(foundUser.name).toBe(userData.name);
  });

  it("should send welcome email on user creation", async () => {
    const userData = {
      email: "new@example.com",
      name: "New User",
      password: "hashedPassword",
    };

    const createdUser = await userService.create(userData);

    // Verify email was sent
    const emailLog = await db.getEmailLog(createdUser.id);
    expect(emailLog).toHaveLength(1);
    expect(emailLog[0].to).toBe(userData.email);
    expect(emailLog[0].subject).toBe("Welcome!");
  });
});

```

## Real-World Use Cases

### 1. E-commerce Checkout Flow

```typescript
// E2E test using Playwright
import { test, expect } from "@playwright/test";

test.describe("Checkout Flow", () => {
  test("complete purchase with credit card", async ({ page }) => {
    // Navigate to product page
    await page.goto("/products/widget");

    // Add to cart
    await page.click('[data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText("1");

    // Proceed to checkout
    await page.click('[data-testid="checkout"]');
    await expect(page).toHaveURL("/checkout");

    // Fill shipping info
    await page.fill('[data-testid="shipping-name"]', "John Doe");
    await page.fill('[data-testid="shipping-address"]', "123 Main St");

    // Fill payment info
    await page.fill('[data-testid="card-number"]', "4242424242424242");
    await page.fill('[data-testid="card-expiry"]', "12/25");
    await page.fill('[data-testid="card-cvc"]', "123");

    // Complete purchase
    await page.click('[data-testid="complete-purchase"]');

    // Verify order confirmation
    await expect(page).toHaveURL("/order-confirmation");
    await expect(page.locator('[data-testid="order-number"]')).toBeVisible();
  });
});

```

### 2. API Endpoint Testing

```typescript
// api/users.test.ts
import request from "supertest";
import { app } from "../src/app";
import { createTestUser, getAuthToken } from "./helpers";

describe("Users API", () => {
  describe("GET /api/users/:id", () => {
    it("should return user profile", async () => {
      const user = await createTestUser();
      const token = getAuthToken(user.id);

      const response = await request(app)
        .get(`/api/users/${user.id}`)
        .set("Authorization", `Bearer ${token}`)
        .expect(200);

      expect(response.body).toMatchObject({
        id: user.id,
        email: user.email,
        name: user.name,
      });
    });

    it("should return 401 without auth token", async () => {
      const user = await createTestUser();

      await request(app)
        .get(`/api/users/${user.id}`)
        .expect(401);
    });

    it("should return 404 for non-existent user", async () => {
      const token = getAuthToken("non-existent-id");

      await request(app)
        .get("/api/users/non-existent-id")
        .set("Authorization", `Bearer ${token}`)
        .expect(404);
    });
  });
});

```

### 3. React Component Testing

```typescript
// UserProfile.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { UserProfile } from "./UserProfile";
import { server } from "../mocks/server";
import { http, HttpResponse } from "msw";

describe("UserProfile", () => {
  it("should display user information", async () => {
    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByText("John Doe")).toBeInTheDocument();
      expect(screen.getByText("john@example.com")).toBeInTheDocument();
    });
  });

  it("should handle error state", async () => {
    server.use(
      http.get("/api/users/123", () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByText("Failed to load user")).toBeInTheDocument();
    });
  });

  it("should call onEdit when edit button clicked", async () => {
    const onEdit = vi.fn();
    const user = userEvent.setup();

    render(<UserProfile userId="123" onEdit={onEdit} />);

    await user.click(screen.getByRole("button", { name: /edit/i }));

    expect(onEdit).toHaveBeenCalledWith("123");
  });
});

```

## Common Mistakes

### 1. Testing Implementation Details

```typescript
// ❌ BAD: Testing implementation details
it("should call setUserState with new name", () => {
  const setStateSpy = vi.spyOn(React, "useState");
  render(<UserForm />);
  // Testing internal state management
});

// ✅ GOOD: Testing behavior
it("should display updated name after save", async () => {
  const user = userEvent.setup();
  render(<UserForm />);

  await user.clear(screen.getByLabelText(/name/i));
  await user.type(screen.getByLabelText(/name/i), "New Name");
  await user.click(screen.getByRole("button", { name: /save/i }));

  expect(screen.getByText("New Name")).toBeInTheDocument();
});

```

### 2. Overly Complex Tests

```typescript
// ❌ BAD: Testing too many things
it("should do everything", async () => {
  // 50+ assertions testing unrelated functionality
});

// ✅ GOOD: Focused tests
describe("when user submits form", () => {
  it("should validate required fields", () => {});
  it("should show loading indicator", () => {});
  it("should submit data to server", () => {});
  it("should show success message", () => {});
  it("should reset form fields", () => {});
});

```

### 3. Flaky Tests

```typescript
// ❌ BAD: Time-dependent test
it("should expire session after 30 minutes", async () => {
  jest.useFakeTimers();
  login();
  jest.advanceTimersByTime(30 * 60 * 1000 + 1); // Flaky!
  expect(isLoggedIn()).toBe(false);
});

// ✅ GOOD: Controlled time
it("should expire session after inactivity", async () => {
  const sessionTimeout = 30 * 60 * 1000;
  jest.useFakeTimers();

  login();
  jest.advanceTimersByTime(sessionTimeout - 1);
  expect(isLoggedIn()).toBe(true);

  jest.advanceTimersByTime(1);
  expect(isLoggedIn()).toBe(false);
});

```

### 4. Test Interdependence

```typescript
// ❌ BAD: Tests depend on each other
it("should create user", () => {
  userId = createUser(); // Shared state
});

it("should update user", () => {
  updateUser(userId); // Depends on previous test
});

// ✅ GOOD: Independent tests
it("should create user", () => {
  const userId = createUser();
  expect(userId).toBeDefined();
});

it("should update user", () => {
  const userId = createUser();
  const updated = updateUser(userId, { name: "Updated" });
  expect(updated.name).toBe("Updated");
});

```

## Best Practices

1. **Follow the AAA Pattern**: Arrange, Act, Assert

2. **Test Behavior, Not Implementation**: Focus on what the code does, not how

3. **Keep Tests Independent**: Each test should be able to run in isolation

4. **Use Descriptive Test Names**: Names should explain what is being tested and expected outcome

5. **Mock External Dependencies**: Isolate the code under test

6. **Test Edge Cases**: Empty inputs, null values, boundary conditions

7. **Maintain Test Code Like Production Code**: Refactor tests regularly

8. **Write Tests Before Code (TDD)**: When practical, follow the red-green-refactor cycle

9. **Aim for High Confidence, Not 100% Coverage**: Focus on critical paths
10. **Keep Tests Fast**: Slow tests won't be run frequently

## Performance Considerations

### Test Execution Time

```text
+------------------+----------------+------------------+

| Test Type        | Typical Time   | Target Time      |

+------------------+----------------+------------------+

| Unit Test        | < 10ms         | < 5ms            |
| Integration Test | < 100ms        | < 50ms           |
| E2E Test         | < 30s          | < 10s            |
| Snapshot Test    | < 50ms         | < 20ms           |

+------------------+----------------+------------------+

```

### Parallelization Strategy

```text
Test Suite Distribution:
┌─────────────────────────────────────────┐
│ CI Pipeline                            │
├─────────┬─────────┬─────────┬──────────┤
│ Worker 1│ Worker 2│ Worker 3│ Worker 4 │
├─────────┼─────────┼─────────┼──────────┤
│ Auth    │ Users   │ Orders  │ Products │
│ Tests   │ Tests   │ Tests   │ Tests    │
│ (Unit)  │ (Unit)  │ (Unit)  │ (Unit)   │
└─────────┴─────────┴─────────┴──────────┘
         ↓ Merge Results ↓
    ┌─────────────────────────┐
    │ Integration Tests       │
    │ (Run after units pass)  │
    └─────────────────────────┘
         ↓ If passed ↓
    ┌─────────────────────────┐
    │ E2E Tests               │
    │ (Run last, critical)    │
    └─────────────────────────┘

```

## Summary

Testing is a fundamental practice in modern software development that ensures code quality, enables safe refactoring, and provides confidence in deployments. The key principles include:

- Follow the testing pyramid (many unit tests, fewer integration tests, few E2E tests)
- Test behavior, not implementation details
- Keep tests fast, reliable, and isolated
- Use TDD/BDD when appropriate
- Aim for high confidence, not 100% coverage
- Integrate testing into CI/CD pipelines
- Continuously improve testing practices

A well-tested codebase is maintainable, reliable, and enables teams to ship features quickly with confidence.

---

## See Also
- [React](../03-React/)
- [NestJS](../06-NestJS/)
- [CI/CD](../15-CI-CD/)
- [Coding Patterns](../19-Coding-Patterns/)

## References & Learn More

- "Testing JavaScript" by Kent Beck
- "Working Effectively with Legacy Code" by Michael Feathers
- "The Art of Unit Testing" by Roy Osherove
- Martin Fowler's Testing Pyramid
- React Testing Library Documentation
- Jest Documentation
- Cypress Documentation
- Playwright Documentation
