# E2E Testing

## Definition

End-to-End (E2E) testing is a software testing technique that validates the entire application workflow from start to finish, simulating real user scenarios. E2E tests verify that all components work together correctly in a production-like environment, including the frontend, backend, database, and external services.

**Key Characteristics:**

- Tests complete user workflows
- Runs in real browser environments
- Highest confidence in application behavior
- Slowest execution time
- Most expensive to maintain
- Verifies critical business paths

**E2E Testing Position:**

```text
┌─────────────────────────────────────────────────────────────┐
│                    Testing Pyramid                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                        /\                                   │
│                       /  \        E2E Tests                 │
│                      / E2E \       • Complete workflows     │
│                     /--------\      • Real browser          │
│                    /Integration\     • High confidence       │
│                   /--------------\   • Slow, expensive       │
│                  /    Unit Tests    \                       │
│                 /--------------------\                      │
│                /    Static Analysis   \                     │
│               /------------------------\                    │
│                                                             │
│  E2E Tests: ~10% of test suite                             │
│  Focus on critical user journeys                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

## Why Do We Need It?

- **User Perspective Testing**: Tests exactly what users experience
- **Cross-Browser Compatibility**: Verify behavior across browsers
- **Real Environment Testing**: Tests with real databases, APIs, and services
- **Critical Path Verification**: Ensures essential workflows function
- **Regression Detection**: Catches issues missed by unit/integration tests
- **Stakeholder Confidence**: Provides visible, understandable test results
- **Production-Like Environment**: Tests in conditions similar to production
- **Visual Regression Detection**: Catches UI layout and styling issues

## How It Works

### E2E Testing Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                E2E Testing Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Test Runner                         │   │
│  │  • Cypress / Playwright / Selenium                  │   │
│  │  • Executes tests in parallel                       │   │
│  │  • Manages browser instances                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Browser Control                     │   │
│  │  • Launch browsers (Chrome, Firefox, Safari)        │   │
│  │  • Navigate to URLs                                 │   │
│  │  • Interact with elements                           │   │
│  │  • Take screenshots                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Application Under Test              │   │
│  │  • Frontend (React, Vue, Angular)                   │   │
│  │  • Backend (API servers)                            │   │
│  │  • Database                                         │   │
│  │  • External Services (mocked or real)               │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Assertions                          │   │
│  │  • Element visibility                               │   │
│  │  • Text content                                     │   │
│  │  • URL changes                                      │   │
│  │  • Network requests                                 │   │
│  │  • Visual comparisons                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

### Cypress vs Playwright

```text
┌─────────────────────────────────────────────────────────────┐
│              Cypress vs Playwright Comparison               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Feature              │ Cypress          │ Playwright       │
│  ─────────────────────┼─────────────────┼───────────────── │
│  Browser Support      │ Chrome, Firefox  │ Chrome, Firefox  │
│                       │ Edge (WebKit*)   │ Safari, Edge     │
│  Language Support     │ JS/TS            │ JS/TS, Python,   │
│                       │                  │ Java, C#         │
│  Architecture         │ In-browser       │ Out-of-browser   │
│  Speed                │ Moderate         │ Fast             │
│  Auto-wait            │ Yes              │ Yes              │
│  Parallel Execution   │ Paid (Dashboard)│ Free             │
│  Network Interception │ Yes              │ Yes              │
│  Mobile Testing       │ Limited          │ Yes              │
│  Learning Curve       │ Easy             │ Moderate         │
│  Community            │ Large            │ Growing          │
│  Pricing              │ Free/Paid        │ Free             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

### Page Object Pattern

```text
┌─────────────────────────────────────────────────────────────┐
│                  Page Object Model                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Test File                           │   │
│  │  loginPage.enterEmail("user@test.com")               │   │
│  │  loginPage.enterPassword("password")                 │   │
│  │  loginPage.clickLogin()                              │   │
│  │  dashboardPage.isVisible()                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Page Objects                        │   │
│  │  LoginPage:                                          │   │
│  │    - emailInput                                      │   │
│  │    - passwordInput                                   │   │
│  │    - loginButton                                     │   │
│  │                                                      │   │
│  │  DashboardPage:                                      │   │
│  │    - welcomeMessage                                  │   │
│  │    - navigationMenu                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  Selectors                           │   │
│  │  [data-testid="email-input"]                        │   │
│  │  [data-testid="password-input"]                     │   │
│  │  [data-testid="login-button"]                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

```

## Code Examples

### Cypress Example

```typescript
// cypress/e2e/login.cy.ts
describe("Login Flow", () => {
  beforeEach(() => {
    cy.visit("/login");
  });

  it("should login successfully with valid credentials", () => {
    cy.get('[data-testid="email-input"]').type("user@example.com");
    cy.get('[data-testid="password-input"]').type("password123");
    cy.get('[data-testid="login-button"]').click();

    cy.url().should("include", "/dashboard");
    cy.get('[data-testid="welcome-message"]').should(
      "contain",
      "Welcome, User!"
    );
  });

  it("should show error for invalid credentials", () => {
    cy.get('[data-testid="email-input"]').type("wrong@example.com");
    cy.get('[data-testid="password-input"]').type("wrongpassword");
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="error-message"]').should(
      "contain",
      "Invalid credentials"
    );
    cy.url().should("include", "/login");
  });

  it("should validate required fields", () => {
    cy.get('[data-testid="login-button"]').click();

    cy.get('[data-testid="email-error"]').should("contain", "Email is required");
    cy.get('[data-testid="password-error"]').should(
      "contain",
      "Password is required"
    );
  });

  it("should navigate to register page", () => {
    cy.get('[data-testid="register-link"]').click();
    cy.url().should("include", "/register");
  });
});

// cypress/e2e/checkout.cy.ts
describe("Checkout Flow", () => {
  beforeEach(() => {
    // Seed test data
    cy.task("seedDatabase");
    cy.login("user@example.com", "password123");
  });

  it("should complete checkout with credit card", () => {
    // Add item to cart
    cy.visit("/products");
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart-count"]').should("contain", "1");

    // Proceed to checkout
    cy.get('[data-testid="checkout-button"]').click();
    cy.url().should("include", "/checkout");

    // Fill shipping info
    cy.get('[data-testid="shipping-name"]').type("John Doe");
    cy.get('[data-testid="shipping-address"]').type("123 Main St");
    cy.get('[data-testid="shipping-city"]').type("Springfield");
    cy.get('[data-testid="shipping-zip"]').type("12345");

    // Fill payment info
    cy.get('[data-testid="card-number"]').type("4242424242424242");
    cy.get('[data-testid="card-expiry"]').type("12/25");
    cy.get('[data-testid="card-cvc"]').type("123");

    // Complete purchase
    cy.get('[data-testid="complete-purchase"]').click();

    // Verify order confirmation
    cy.url().should("include", "/order-confirmation");
    cy.get('[data-testid="order-number"]').should("be.visible");
    cy.get('[data-testid="success-message"]').should(
      "contain",
      "Thank you for your order"
    );
  });

  it("should show error for invalid payment", () => {
    cy.visit("/products");
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="checkout-button"]').click();

    // Fill shipping
    cy.get('[data-testid="shipping-name"]').type("John Doe");
    cy.get('[data-testid="shipping-address"]').type("123 Main St");

    // Use declined card
    cy.get('[data-testid="card-number"]').type("4000000000000002");
    cy.get('[data-testid="card-expiry"]').type("12/25");
    cy.get('[data-testid="card-cvc"]').type("123");

    cy.get('[data-testid="complete-purchase"]').click();

    cy.get('[data-testid="payment-error"]').should(
      "contain",
      "Payment declined"
    );
  });
});

```

### Playwright Example

```typescript
// tests/login.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Login Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
  });

  test("should login successfully", async ({ page }) => {
    await page.fill('[data-testid="email-input"]', "user@example.com");
    await page.fill('[data-testid="password-input"]', "password123");
    await page.click('[data-testid="login-button"]');

    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('[data-testid="welcome-message"]')).toContainText(
      "Welcome, User!"
    );
  });

  test("should show error for invalid credentials", async ({ page }) => {
    await page.fill('[data-testid="email-input"]', "wrong@example.com");
    await page.fill('[data-testid="password-input"]', "wrongpassword");
    await page.click('[data-testid="login-button"]');

    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      "Invalid credentials"
    );
    await expect(page).toHaveURL(/.*login/);
  });

  test("should validate required fields", async ({ page }) => {
    await page.click('[data-testid="login-button"]');

    await expect(page.locator('[data-testid="email-error"]')).toContainText(
      "Email is required"
    );
    await expect(page.locator('[data-testid="password-error"]')).toContainText(
      "Password is required"
    );
  });
});

// tests/checkout.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Checkout Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto("/login");
    await page.fill('[data-testid="email-input"]', "user@example.com");
    await page.fill('[data-testid="password-input"]', "password123");
    await page.click('[data-testid="login-button"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test("should complete checkout", async ({ page }) => {
    // Add item to cart
    await page.goto("/products");
    await page.locator('[data-testid="product-card"]').first().click();
    await page.click('[data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-count"]')).toContainText("1");

    // Proceed to checkout
    await page.click('[data-testid="checkout-button"]');
    await expect(page).toHaveURL(/.*checkout/);

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
    await expect(page).toHaveURL(/.*order-confirmation/);
    await expect(page.locator('[data-testid="order-number"]')).toBeVisible();
  });

  test("should handle network errors gracefully", async ({ page }) => {
    // Mock API failure
    await page.route("**/api/checkout", (route) =>
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: "Server error" }),
      })
    );

    await page.goto("/checkout");
    await page.click('[data-testid="complete-purchase"]');

    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      "Something went wrong"
    );
  });
});

```

### Page Object Pattern Implementation

```typescript
// pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly registerLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
    this.registerLink = page.locator('[data-testid="register-link"]');
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async getErrorMessage(): Promise<string | null> {
    return this.errorMessage.textContent();
  }
}

// pages/DashboardPage.ts
import { Page, Locator } from "@playwright/test";

export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly navigationMenu: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.locator('[data-testid="welcome-message"]');
    this.navigationMenu = page.locator('[data-testid="nav-menu"]');
    this.logoutButton = page.locator('[data-testid="logout-button"]');
  }

  async getWelcomeMessage(): Promise<string> {
    return (await this.welcomeMessage.textContent()) || "";
  }

  async navigateTo(section: string) {
    await this.navigationMenu.click();
    await this.page.locator(`[data-testid="nav-${section}"]`).click();
  }

  async logout() {
    await this.logoutButton.click();
  }
}

// pages/CheckoutPage.ts
import { Page, Locator } from "@playwright/test";

export class CheckoutPage {
  readonly page: Page;
  readonly shippingName: Locator;
  readonly shippingAddress: Locator;
  readonly cardNumber: Locator;
  readonly cardExpiry: Locator;
  readonly cardCvc: Locator;
  readonly completePurchaseButton: Locator;
  readonly orderNumber: Locator;

  constructor(page: Page) {
    this.page = page;
    this.shippingName = page.locator('[data-testid="shipping-name"]');
    this.shippingAddress = page.locator('[data-testid="shipping-address"]');
    this.cardNumber = page.locator('[data-testid="card-number"]');
    this.cardExpiry = page.locator('[data-testid="card-expiry"]');
    this.cardCvc = page.locator('[data-testid="card-cvc"]');
    this.completePurchaseButton = page.locator(
      '[data-testid="complete-purchase"]'
    );
    this.orderNumber = page.locator('[data-testid="order-number"]');
  }

  async fillShippingInfo(name: string, address: string) {
    await this.shippingName.fill(name);
    await this.shippingAddress.fill(address);
  }

  async fillPaymentInfo(number: string, expiry: string, cvc: string) {
    await this.cardNumber.fill(number);
    await this.cardExpiry.fill(expiry);
    await this.cardCvc.fill(cvc);
  }

  async completePurchase() {
    await this.completePurchaseButton.click();
  }

  async getOrderNumber(): Promise<string> {
    return (await this.orderNumber.textContent()) || "";
  }
}

// Using Page Objects in tests
import { test, expect } from "@playwright/test";
import { LoginPage } from "../pages/LoginPage";
import { DashboardPage } from "../pages/DashboardPage";

test.describe("Login with Page Objects", () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    await loginPage.goto();
  });

  test("should login and see dashboard", async () => {
    await loginPage.login("user@example.com", "password123");

    await expect(dashboardPage.welcomeMessage).toBeVisible();
    const welcomeText = await dashboardPage.getWelcomeMessage();
    expect(welcomeText).toContain("Welcome");
  });
});

```

### Visual Regression Testing

```typescript
// cypress/e2e/visual-regression.cy.ts
describe("Visual Regression", () => {
  it("should match homepage screenshot", () => {
    cy.visit("/");
    cy.get('[data-testid="main-content"]').toMatchImageSnapshot({
      name: "homepage",
      failureThreshold: 0.1,
      failureThresholdType: "percent",
    });
  });

  it("should match login page screenshot", () => {
    cy.visit("/login");
    cy.get('[data-testid="login-form"]').toMatchImageSnapshot({
      name: "login-page",
    });
  });

  it("should match dashboard screenshot for admin user", () => {
    cy.loginAs("admin");
    cy.visit("/dashboard");
    cy.get('[data-testid="dashboard-content"]').toMatchImageSnapshot({
      name: "admin-dashboard",
    });
  });
});

// tests/visual.spec.ts (Playwright)
import { test, expect } from "@playwright/test";

test.describe("Visual Regression", () => {
  test("homepage should match snapshot", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveScreenshot("homepage.png", {
      maxDiffPixelRatio: 0.01,
    });
  });

  test("login page should match snapshot", async ({ page }) => {
    await page.goto("/login");
    await expect(page).toHaveScreenshot("login-page.png");
  });
});

```

### Network Interception

```typescript
// tests/api-mocking.spec.ts
import { test, expect } from "@playwright/test";

test.describe("API Mocking", () => {
  test("should mock API responses", async ({ page }) => {
    // Mock users API
    await page.route("**/api/users", (route) =>
      route.fulfill({
        status: 200,
        body: JSON.stringify([
          { id: "1", name: "John Doe", email: "john@example.com" },
          { id: "2", name: "Jane Smith", email: "jane@example.com" },
        ]),
      })
    );

    await page.goto("/users");

    await expect(page.locator('[data-testid="user-list"]')).toContainText(
      "John Doe"
    );
    await expect(page.locator('[data-testid="user-list"]')).toContainText(
      "Jane Smith"
    );
  });

  test("should handle API errors", async ({ page }) => {
    await page.route("**/api/users", (route) =>
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: "Internal server error" }),
      })
    );

    await page.goto("/users");

    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      "Failed to load users"
    );
  });

  test("should intercept and modify requests", async ({ page }) => {
    await page.route("**/api/users", (route) => {
      const request = route.request();
      // Add auth header
      route.continue({
        headers: {
          ...request.headers(),
          Authorization: "Bearer test-token",
        },
      });
    });

    await page.goto("/users");
    // Verify authenticated request works
  });
});

```

### Testing Authentication Flows

```typescript
// auth.setup.ts
import { test as setup, expect } from "@playwright/test";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page }) => {
  // Perform authentication
  await page.goto("/login");
  await page.fill('[data-testid="email-input"]', "user@example.com");
  await page.fill('[data-testid="password-input"]', "password123");
  await page.click('[data-testid="login-button"]');

  // Wait for redirect
  await expect(page).toHaveURL(/.*dashboard/);

  // Save authentication state
  await page.context().storageState({ path: authFile });
});

// tests/dashboard.spec.ts
import { test, expect } from "@playwright/test";

test.use({ storageState: "playwright/.auth/user.json" });

test.describe("Dashboard", () => {
  test("should display user dashboard", async ({ page }) => {
    await page.goto("/dashboard");

    await expect(
      page.locator('[data-testid="welcome-message"]')
    ).toBeVisible();
  });

  test("should logout successfully", async ({ page }) => {
    await page.goto("/dashboard");
    await page.click('[data-testid="logout-button"]');

    await expect(page).toHaveURL(/.*login/);
  });
});

```

### Testing Forms

```typescript
// tests/form.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Registration Form", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/register");
  });

  test("should submit form with valid data", async ({ page }) => {
    await page.fill('[data-testid="username"]', "johndoe");
    await page.fill('[data-testid="email"]', "john@example.com");
    await page.fill('[data-testid="password"]', "password123");
    await page.fill('[data-testid="confirm-password"]', "password123");
    await page.check('[data-testid="accept-terms"]');

    await page.click('[data-testid="register-button"]');

    await expect(page).toHaveURL(/.*success/);
    await expect(
      page.locator('[data-testid="success-message"]')
    ).toContainText("Registration successful");
  });

  test("should validate all required fields", async ({ page }) => {
    await page.click('[data-testid="register-button"]');

    await expect(
      page.locator('[data-testid="username-error"]')
    ).toContainText("Username is required");
    await expect(
      page.locator('[data-testid="email-error"]')
    ).toContainText("Email is required");
    await expect(
      page.locator('[data-testid="password-error"]')
    ).toContainText("Password is required");
  });

  test("should validate email format", async ({ page }) => {
    await page.fill('[data-testid="email"]', "invalidemail");
    await page.click('[data-testid="register-button"]');

    await expect(
      page.locator('[data-testid="email-error"]')
    ).toContainText("Invalid email format");
  });

  test("should validate password match", async ({ page }) => {
    await page.fill('[data-testid="password"]', "password123");
    await page.fill('[data-testid="confirm-password"]', "differentpassword");
    await page.click('[data-testid="register-button"]');

    await expect(
      page.locator('[data-testid="confirm-password-error"]')
    ).toContainText("Passwords do not match");
  });

  test("should show/hide password", async ({ page }) => {
    await page.fill('[data-testid="password"]', "password123");

    // Initially password is hidden
    await expect(
      page.locator('[data-testid="password"]')
    ).toHaveAttribute("type", "password");

    // Click show button
    await page.click('[data-testid="toggle-password"]');

    // Now password is visible
    await expect(
      page.locator('[data-testid="password"]')
    ).toHaveAttribute("type", "text");
  });
});

```

## Real-World Use Cases

### 1. E-commerce Complete Flow

```typescript
// tests/e2e/e-commerce.spec.ts
import { test, expect } from "@playwright/test";

test.describe("E-commerce Complete Flow", () => {
  test("complete purchase journey", async ({ page }) => {
    // 1. Browse products
    await page.goto("/products");
    await expect(page.locator('[data-testid="product-grid"]')).toBeVisible();

    // 2. View product details
    await page.locator('[data-testid="product-card"]').first().click();
    await expect(
      page.locator('[data-testid="product-title"]')
    ).toBeVisible();

    // 3. Add to cart
    await page.click('[data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-count"]')).toContainText("1");

    // 4. View cart
    await page.click('[data-testid="cart-icon"]');
    await expect(page).toHaveURL(/.*cart/);
    await expect(
      page.locator('[data-testid="cart-item"]')
    ).toHaveCount(1);

    // 5. Proceed to checkout
    await page.click('[data-testid="checkout-button"]');
    await expect(page).toHaveURL(/.*checkout/);

    // 6. Fill shipping info
    await page.fill('[data-testid="shipping-name"]', "John Doe");
    await page.fill('[data-testid="shipping-address"]', "123 Main St");
    await page.fill('[data-testid="shipping-city"]', "Springfield");
    await page.fill('[data-testid="shipping-zip"]', "12345");

    // 7. Fill payment info
    await page.fill('[data-testid="card-number"]', "4242424242424242");
    await page.fill('[data-testid="card-expiry"]', "12/25");
    await page.fill('[data-testid="card-cvc"]', "123");

    // 8. Complete purchase
    await page.click('[data-testid="complete-purchase"]');

    // 9. Verify confirmation
    await expect(page).toHaveURL(/.*order-confirmation/);
    const orderNumber = await page
      .locator('[data-testid="order-number"]')
      .textContent();
    expect(orderNumber).toBeTruthy();

    // 10. Check email confirmation (mocked)
    await expect(
      page.locator('[data-testid="confirmation-email"]')
    ).toContainText("Thank you for your order");
  });
});

```

### 2. Admin Dashboard

```typescript
// tests/e2e/admin.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Admin Dashboard", () => {
  test.beforeEach(async ({ page }) => {
    // Login as admin
    await page.goto("/login");
    await page.fill('[data-testid="email-input"]', "admin@example.com");
    await page.fill('[data-testid="password-input"]', "admin123");
    await page.click('[data-testid="login-button"]');
    await expect(page).toHaveURL(/.*admin/);
  });

  test("should manage users", async ({ page }) => {
    // Navigate to users
    await page.click('[data-testid="nav-users"]');
    await expect(page).toHaveURL(/.*admin\/users/);

    // View user list
    await expect(
      page.locator('[data-testid="user-table"]')
    ).toBeVisible();

    // Search for user
    await page.fill('[data-testid="search-input"]', "john");
    await expect(
      page.locator('[data-testid="user-row"]')
    ).toHaveCount(1);

    // Edit user
    await page.click('[data-testid="edit-user-1"]');
    await expect(page.locator('[data-testid="edit-modal"]')).toBeVisible();

    // Update user
    await page.fill('[data-testid="user-name"]', "John Updated");
    await page.click('[data-testid="save-button"]');

    // Verify update
    await expect(
      page.locator('[data-testid="success-toast"]')
    ).toContainText("User updated");
  });

  test("should view analytics", async ({ page }) => {
    await page.click('[data-testid="nav-analytics"]');

    await expect(
      page.locator('[data-testid="revenue-chart"]')
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="user-stats"]')
    ).toBeVisible();

    // Change date range
    await page.click('[data-testid="date-range"]');
    await page.click('[data-testid="last-30-days"]');

    // Verify chart updates
    await expect(
      page.locator('[data-testid="revenue-chart"]')
    ).toBeVisible();
  });
});

```

## Common Mistakes

### 1. Testing Too Much in E2E

```typescript
// ❌ BAD: Testing implementation details
test("should call API endpoint", async ({ page }) => {
  const responsePromise = page.waitForResponse("**/api/data");
  await page.click('[data-testid="button"]');
  const response = await responsePromise;
  expect(response.url()).toContain("/api/data");
});

// ✅ GOOD: Testing user-visible behavior
test("should display data after clicking button", async ({ page }) => {
  await page.click('[data-testid="button"]');
  await expect(page.locator('[data-testid="data"]')).toBeVisible();
});

```

### 2. Hardcoded Waits

```typescript
// ❌ BAD: Using fixed timeouts
test("bad example", async ({ page }) => {
  await page.click('[data-testid="button"]');
  await page.waitForTimeout(5000); // Hardcoded wait!
  await expect(page.locator('[data-testid="result"]')).toBeVisible();
});

// ✅ GOOD: Using auto-waiting or explicit waits
test("good example", async ({ page }) => {
  await page.click('[data-testid="button"]');
  await expect(page.locator('[data-testid="result"]')).toBeVisible();
  // Or use:
  await page.waitForSelector('[data-testid="result"]');
});

```

### 3. Flaky Tests

```typescript
// ❌ BAD: Race conditions
test("flaky test", async ({ page }) => {
  await page.click('[data-testid="load-button"]');
  // Might fail if data hasn't loaded yet
  const items = await page.locator('[data-testid="item"]').count();
  expect(items).toBeGreaterThan(0);
});

// ✅ GOOD: Proper waiting
test("reliable test", async ({ page }) => {
  await page.click('[data-testid="load-button"]');
  await expect(page.locator('[data-testid="item"]').first()).toBeVisible();
  const items = await page.locator('[data-testid="item"]').count();
  expect(items).toBeGreaterThan(0);
});

```

## Best Practices

1. **Use Page Object Pattern**: Encapsulate page interactions

2. **Test critical user journeys**: Focus on essential workflows

3. **Use data-testid attributes**: Stable selectors for testing

4. **Avoid hardcoded waits**: Use auto-waiting features

5. **Mock external services**: Use route interception

6. **Clean up test data**: Reset state between tests

7. **Use environment variables**: Different configs for different environments

8. **Run tests in parallel**: Speed up test execution

9. **Take screenshots on failure**: Debug failing tests easily
10. **Monitor flaky tests**: Track and fix flakiness

## Performance Considerations

### Parallel Execution

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { browserName: "chromium" },
    },
    {
      name: "firefox",
      use: { browserName: "firefox" },
    },
    {
      name: "webkit",
      use: { browserName: "webkit" },
    },
  ],
});

```

### Test Splitting

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:

      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install
      - run: npx playwright test --shard=${{ matrix.shard }}/4

```

## Interview Questions

### Beginner (5-10)

1. **What is E2E testing?**
   E2E testing validates complete user workflows from start to finish, simulating real user scenarios in a production-like environment.

2. **How is E2E different from integration testing?**
   Integration tests verify component interactions. E2E tests verify complete user workflows through the entire application stack.

3. **What are the benefits of E2E testing?**
   High confidence, real user perspective, cross-browser testing, and visual regression detection.

4. **What are the drawbacks of E2E testing?**
   Slow execution, expensive maintenance, flaky tests, and limited debugging information.

5. **What tools are commonly used for E2E testing?**
   Cypress, Playwright, Selenium, and Puppeteer are popular choices.

6. **What is the Page Object pattern?**
   A design pattern that encapsulates page interactions in reusable objects, improving test maintainability.

7. **How do you handle authentication in E2E tests?**
   Use authentication setup scripts, save storage state, or mock authentication.

8. **What is visual regression testing?**
   Comparing screenshots of UI before and after changes to detect unintended visual changes.

9. **How do you handle flaky E2E tests?**
   Fix timing issues, use proper waiting strategies, and isolate test state.

10. **When should you write E2E tests?**
    For critical user journeys, complex workflows, and scenarios that span multiple components.

### Intermediate (5-10)

11. **How do you mock APIs in E2E tests?**
    Use route interception (Playwright) or cy.intercept (Cypress) to mock network requests.

12. **How do you test file uploads in E2E tests?**
    Use file chooser APIs or set input files directly.

13. **How do you handle multi-tab testing?**
    Use browser context APIs to manage multiple pages/tabs.

14. **How do you test responsive design?**
    Use viewport settings to test different screen sizes.

15. **How do you handle iframe testing?**
    Use frame locators or frame-specific selectors.

16. **How do you test WebSocket connections?**
    Use page events or mock WebSocket servers.

17. **How do you handle shadow DOM?**
    Use shadow-piercing selectors or APIs that pierce shadow boundaries.

18. **How do you test PDF generation?**
    Download the PDF and verify its content or structure.

19. **How do you handle testing with real-time features?**
    Use polling or event-based assertions.

20. **How do you test accessibility in E2E?**
    Integrate axe-core or similar accessibility testing libraries.

### Senior (10-15)

21. **How do you design a scalable E2E test suite?**
    Use page objects, test data factories, parallel execution, and test filtering.

22. **How do you handle testing in CI/CD?**
    Implement test stages, artifact collection, and failure notifications.

23. **How do you reduce E2E test execution time?**
    Parallel execution, test splitting, mocking non-critical services, and test prioritization.

24. **How do you handle flaky tests at scale?**
    Implement quarantine systems, track flakiness metrics, and automated retries.

25. **How do you test micro-frontends?**
    Test each micro-frontend independently and their integration.

26. **How do you test with complex authentication flows?**
    Use OAuth mocking, test token refresh, and session management.

27. **How do you handle testing with real-time data?**
    Use deterministic test data and verify eventual consistency.

28. **How do you test internationalization?**
    Test different language outputs and RTL layouts.

29. **How do you handle testing with complex state?**
    Test state persistence, cross-tab state, and offline capabilities.

30. **How do you measure E2E test effectiveness?**
    Track defect detection rate, test execution time, and maintenance burden.

### FAANG-style (5-10)

31. **How would you design E2E testing for a large-scale application?**
    Risk-based testing, test impact analysis, and selective test execution.

32. **How do you handle testing in a microservices architecture?**
    Contract testing, service virtualization, and integration test environments.

33. **How do you ensure test reliability at scale?**
    Implement flakiness detection, quarantine system, and stability metrics.

34. **How do you handle testing with complex user journeys?**
    Break down into smaller test scenarios, use test data factories.

35. **How do you balance coverage with execution time?**
    Prioritize critical paths, use smoke tests, and implement test filtering.

### Follow-ups (5-10)

36. **How has your E2E testing approach evolved?**
    Discuss adoption of Playwright, shift to component testing, and CI/CD integration.

37. **What tools have you used for E2E testing?**
    Compare Cypress, Playwright, and Selenium, explain selection criteria.

38. **How do you handle testing legacy applications?**
    Strangler fig pattern, gradual migration, and characterization tests.

39. **What's the most challenging E2E testing problem you've solved?**
    Describe complex testing scenarios and solutions.

40. **How do you train teams on E2E testing?**
    Start with simple examples, establish patterns, and share best practices.

## Summary

E2E testing is essential for verifying complete user workflows. Key principles:

- **Test critical user journeys** end-to-end
- **Use Page Object pattern** for maintainability
- **Mock external services** to improve reliability
- **Implement proper waiting strategies** to avoid flakiness
- **Run tests in parallel** for faster execution
- **Monitor and fix flaky tests** proactively
- **Integrate into CI/CD** for continuous feedback
- **Use visual regression testing** for UI stability

A well-designed E2E test suite provides high confidence while remaining maintainable.

## References & Learn More

- [Playwright Documentation](https://playwright.dev/)
- [Cypress Documentation](https://docs.cypress.io/)
- "Testing Node Applications" by Marc Harter
- "Cypress: End-to-End Testing for Web Applications"
