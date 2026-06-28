# Testing Interview Questions

## Definition

This chapter contains the 40 most commonly asked testing interview questions with detailed answers, covering everything from basic concepts to advanced FAANG-level scenarios. Each question includes a comprehensive answer, code examples where applicable, and follow-up considerations.

## Why Do We Need It?

- **Interview Preparation**: Master the most common testing questions
- **Concept Reinforcement**: Deepen understanding of testing principles
- **Practical Application**: Learn how to apply concepts in real scenarios
- **Career Advancement**: Demonstrate expertise in testing practices
- **Team Leadership**: Understand how to guide testing strategies

## How It Works

### Question Categories

```text
┌─────────────────────────────────────────────────────────────┐
│              Interview Question Categories                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Beginner (5-10)                                    │   │
│  │  • Basic testing concepts                           │   │
│  │  • Testing terminology                              │   │
│  │  • Simple scenarios                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Intermediate (5-10)                                │   │
│  │  • Testing strategies                               │   │
│  │  • Tool-specific questions                          │   │
│  │  • Real-world scenarios                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Senior (10-15)                                     │   │
│  │  • Architecture decisions                           │   │
│  │  • Testing at scale                                 │   │
│  │  • Advanced patterns                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FAANG-style (5-10)                                 │   │
│  │  • System design                                    │   │
│  │  • Complex scenarios                                │   │
│  │  • Leadership questions                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Code Examples

### Beginner Questions (5-10)

#### 1. What is the testing pyramid?

**Answer:** The testing pyramid is a model that recommends how to distribute testing efforts across different levels. It suggests having:

- **Many unit tests** at the base (70%): Fast, isolated tests for individual components
- **Fewer integration tests** in the middle (20%): Tests for component interactions
- **Few E2E tests** at the top (10%): Complete user workflow tests

```text
        /\
       /  \        E2E Tests (10%)
      /    \       • Complete workflows
     /------\      • Slow, expensive
    /        \
   / Integration\  Integration Tests (20%)
  /--------------\ • Component interactions
 /                \ • Moderate speed
/    Unit Tests    \ Unit Tests (70%)
/--------------------\• Fast, isolated
```

The pyramid ensures fast feedback while maintaining confidence in the application.

---

#### 2. What is the difference between unit, integration, and E2E tests?

**Answer:**

| Type | Scope | Speed | Cost | Confidence |
|------|-------|-------|------|------------|
| Unit | Single function/class | Very Fast | Low | Low-Medium |
| Integration | Multiple components | Medium | Medium | Medium-High |
| E2E | Complete user flow | Slow | High | High |

**Unit Test Example:**
```typescript
it("should add two numbers", () => {
  expect(add(2, 3)).toBe(5);
});
```

**Integration Test Example:**
```typescript
it("should create user and send email", async () => {
  const user = await userService.createUser({ name: "John" });
  expect(user.id).toBeDefined();
  expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(user.email);
});
```

**E2E Test Example:**
```typescript
test("complete checkout flow", async ({ page }) => {
  await page.goto("/products");
  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');
  await page.fill('[data-testid="card-number"]', "4242424242424242");
  await page.click('[data-testid="complete-purchase"]');
  await expect(page.locator('[data-testid="confirmation"]')).toBeVisible();
});
```

---

#### 3. What is Test-Driven Development (TDD)?

**Answer:** TDD is a software development approach where tests are written before the actual code. The process follows the Red-Green-Refactor cycle:

1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass the test
3. **REFACTOR**: Improve code while keeping tests green

```typescript
// Step 1: Write failing test (RED)
it("should calculate factorial", () => {
  expect(factorial(5)).toBe(120);
});

// Step 2: Write minimal code (GREEN)
function factorial(n: number): number {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// Step 3: Refactor if needed
function factorial(n: number): number {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
```

**Benefits:**
- Better code design
- Comprehensive test coverage
- Confidence in refactoring
- Living documentation

---

#### 4. What is a mock and when should you use one?

**Answer:** A mock is a test double that simulates the behavior of real objects. Use mocks when:

- Testing code with external dependencies (APIs, databases)
- You need to verify interactions
- You want to simulate error conditions
- You need fast, isolated tests

```typescript
// Mocking an API call
jest.mock("./api");
const mockFetchUser = jest.mocked(fetchUser);

it("should handle API errors", async () => {
  mockFetchUser.mockRejectedValue(new Error("Network error"));

  await expect(userService.getUser("123")).rejects.toThrow("Network error");
});
```

**When NOT to mock:**
- When testing the integration between real components
- When the mock would be more complex than the real implementation
- When you're testing simple, pure functions

---

#### 5. What makes a good unit test?

**Answer:** A good unit test follows the F.I.R.S.T. principles:

- **Fast**: Runs in milliseconds
- **Isolated**: No dependencies on other tests
- **Repeatable**: Produces same results every time
- **Self-validating**: Automatically determines pass/fail
- **Timely**: Written at the right time (ideally before code)

```typescript
// Good unit test
describe("calculateDiscount", () => {
  it("should apply 10% discount for orders over $100", () => {
    // Arrange
    const order = { total: 150 };

    // Act
    const discount = calculateDiscount(order);

    // Assert
    expect(discount).toBe(15);
  });

  it("should not apply discount for orders under $100", () => {
    const order = { total: 50 };
    expect(calculateDiscount(order)).toBe(0);
  });
});
```

---

#### 6. What is the AAA pattern in testing?

**Answer:** AAA (Arrange-Act-Assert) is a test structure pattern:

- **Arrange**: Set up test data and dependencies
- **Act**: Execute the code under test
- **Assert**: Verify the expected outcome

```typescript
it("should calculate total price", () => {
  // Arrange
  const items = [
    { price: 10, quantity: 2 },
    { price: 20, quantity: 1 },
  ];
  const calculator = new PriceCalculator();

  // Act
  const total = calculator.calculateTotal(items);

  // Assert
  expect(total).toBe(40);
});
```

---

#### 7. How do you test error handling?

**Answer:** Test both the error condition and the error handling:

```typescript
describe("error handling", () => {
  it("should throw error for invalid input", () => {
    expect(() => parseAge("abc")).toThrow("Invalid age");
  });

  it("should return error result for failed operation", async () => {
    const result = await service.processInvalidData();
    expect(result.success).toBe(false);
    expect(result.error).toBe("Invalid data");
  });

  it("should handle network errors gracefully", async () => {
    mockFetch.mockRejectedValue(new Error("Network error"));

    const result = await service.fetchData();

    expect(result).toEqual({ error: "Network error", data: null });
  });
});
```

---

#### 8. What is test coverage and what's a good target?

**Answer:** Test coverage measures the percentage of code executed by tests. Types include:

- **Line coverage**: Percentage of lines executed
- **Branch coverage**: Percentage of branches executed
- **Function coverage**: Percentage of functions called

**Good targets:**
- Overall: 70-80%
- Critical business logic: 90%+
- Utility functions: 80%+

```bash
# Generate coverage report
jest --coverage

# Coverage output
-------------------|---------|----------|---------|---------|
File               | % Stmts | % Branch | % Funcs | % Lines |
-------------------|---------|----------|---------|---------|
All files          |   85.71 |    83.33 |   83.33 |   85.71 |
-------------------|---------|----------|---------|---------|
```

**Note:** 100% coverage doesn't mean zero bugs. Focus on testing critical paths and edge cases.

---

#### 9. What is the difference between mocks, stubs, and fakes?

**Answer:**

- **Mocks**: Pre-programmed with expectations, verify interactions
- **Stubs**: Return predefined values, don't track interactions
- **Fakes**: Working implementations with simplified behavior

```typescript
// Stub - returns fixed value
const stub = jest.fn().mockReturnValue(42);

// Mock - verifies interactions
const mock = jest.fn();
service.doSomething();
expect(mock).toHaveBeenCalled();

// Fake - simplified implementation
class FakeDatabase {
  private data = new Map();
  async findById(id: string) { return this.data.get(id); }
  async save(entity: any) { this.data.set(entity.id, entity); }
}
```

---

#### 10. When should you write tests?

**Answer:**

- **Before writing code (TDD)**: When requirements are clear
- **During development**: For complex logic
- **After fixing bugs**: To prevent regression
- **Before refactoring**: To ensure behavior is preserved
- **When requirements change**: To verify new behavior

**Priority for testing:**
1. Critical business logic
2. Complex algorithms
3. Edge cases and error handling
4. Integration points
5. UI components

---

### Intermediate Questions (5-10)

#### 11. How do you test asynchronous code?

**Answer:** Use async/await, return promises, or the `done` callback:

```typescript
// Using async/await
it("should fetch data asynchronously", async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// Using returned promise
it("should handle promise resolution", () => {
  return fetchData().then((data) => {
    expect(data).toBeDefined();
  });
});

// Using done callback (less preferred)
it("should call callback", (done) => {
  fetchData((data) => {
    expect(data).toBeDefined();
    done();
  });
});

// Testing async errors
it("should reject on failure", async () => {
  await expect(failingOperation()).rejects.toThrow("Error message");
});
```

---

#### 12. How do you test React components?

**Answer:** Use React Testing Library to test behavior, not implementation:

```typescript
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { UserProfile } from "./UserProfile";

describe("UserProfile", () => {
  it("should display user information", async () => {
    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByText("John Doe")).toBeInTheDocument();
    });
  });

  it("should handle edit button click", async () => {
    const onEdit = jest.fn();
    const user = userEvent.setup();

    render(<UserProfile userId="123" onEdit={onEdit} />);

    await user.click(screen.getByRole("button", { name: /edit/i }));

    expect(onEdit).toHaveBeenCalledWith("123");
  });
});
```

---

#### 13. How do you mock API calls?

**Answer:** Use MSW (Mock Service Worker) for network-level mocking:

```typescript
import { rest } from "msw";
import { setupServer } from "msw/node";

const server = setupServer(
  rest.get("/api/users", (req, res, ctx) => {
    return res(ctx.json([{ id: 1, name: "John" }]));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("UserList", () => {
  it("should display users", async () => {
    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText("John")).toBeInTheDocument();
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
});
```

---

#### 14. What is snapshot testing?

**Answer:** Snapshot testing captures rendered output and compares it to stored snapshots to detect unexpected changes.

```typescript
import { render } from "@testing-library/react";
import { Button } from "./Button";

it("should render correctly", () => {
  const { container } = render(<Button>Click me</Button>);
  expect(container).toMatchSnapshot();
});

// Update snapshots when intentional changes occur
// jest --updateSnapshot
```

**Pros:**
- Catches unintended UI changes
- Easy to review changes
- Good for component libraries

**Cons:**
- Can become brittle
- Large snapshot files
- Difficult to review changes

---

#### 15. How do you handle flaky tests?

**Answer:** Flaky tests are tests that sometimes pass and sometimes fail. Fix them by:

1. **Identify root cause**: Timing, state, network issues
2. **Fix timing issues**: Use proper waiting strategies
3. **Isolate tests**: Ensure no shared state
4. **Mock external dependencies**: Remove network flakiness
5. **Use deterministic data**: Avoid random values

```typescript
// ❌ BAD: Flaky test
it("should load data", () => {
  setTimeout(() => {
    expect(screen.getByText("Data")).toBeInTheDocument();
  }, 1000);
});

// ✅ GOOD: Proper waiting
it("should load data", async () => {
  render(<DataComponent />);

  await waitFor(() => {
    expect(screen.getByText("Data")).toBeInTheDocument();
  });
});
```

---

#### 16. What is contract testing?

**Answer:** Contract testing verifies that API consumers and providers agree on the interface (contract).

```typescript
// Consumer tests (define contract)
describe("User API Contract", () => {
  it("should return user with required fields", async () => {
    const response = await fetch("/api/users/1");
    const user = await response.json();

    expect(user).toHaveProperty("id");
    expect(user).toHaveProperty("name");
    expect(user).toHaveProperty("email");
  });
});

// Provider tests (verify contract)
describe("User API Provider", () => {
  it("should implement consumer contract", async () => {
    const pact = new Pact({ consumer: "Frontend", provider: "Backend" });

    await pact.addInteraction({
      state: "user exists",
      uponReceiving: "request for user",
      withRequest: { method: "GET", path: "/api/users/1" },
      willRespondWith: { status: 200, body: { id: 1, name: "John" } },
    });
  });
});
```

---

#### 17. How do you test custom hooks?

**Answer:** Use `renderHook` from `@testing-library/react-hooks`:

```typescript
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("should increment count", () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it("should reset to initial value", () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

---

#### 18. How do you test performance?

**Answer:** Use performance testing tools and metrics:

```typescript
// Measure render performance
import { Profiler, ProfilerOnRenderCallback } from "react";

const onRenderCallback: ProfilerOnRenderCallback = (
  id,
  phase,
  actualDuration
) => {
  console.log(`${id} ${phase}: ${actualDuration}ms`);
};

it("should render within time limit", () => {
  const start = performance.now();

  render(
    <Profiler id="App" onRender={onRenderCallback}>
      <App />
    </Profiler>
  );

  const end = performance.now();
  expect(end - start).toBeLessThan(100); // Under 100ms
});

// Load testing with k6
/*
import http from 'k6/http';

export const options = {
  stages: [
    { duration: '1m', target: 100 }, // ramp up
    { duration: '5m', target: 100 }, // stay at 100 users
    { duration: '1m', target: 0 },   // ramp down
  ],
};

export default function () {
  http.get('http://test-api.com/users');
}
*/
```

---

#### 19. How do you test database operations?

**Answer:** Use test databases with transactions for isolation:

```typescript
describe("User Repository", () => {
  let db: Database;
  let repo: UserRepository;

  beforeAll(async () => {
    db = await Database.connect(process.env.TEST_DB_URL);
    repo = new UserRepository(db);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.beginTransaction();
  });

  afterEach(async () => {
    await db.rollback();
  });

  it("should create and retrieve user", async () => {
    const user = await repo.create({ name: "John", email: "john@test.com" });
    const found = await repo.findById(user.id);

    expect(found.name).toBe("John");
  });
});
```

---

#### 20. What is mutation testing?

**Answer:** Mutation testing introduces code mutations to verify tests catch them. It measures test quality beyond coverage.

```typescript
// Original code
function isEven(num: number): boolean {
  return num % 2 === 0;
}

// Mutation: change > to >=
// function isEven(num: number): boolean {
//   return num >= 2;
// }

// Good test catches mutation
it("should return true for 2", () => {
  expect(isEven(2)).toBe(true); // Would fail with mutation
});

// Mutation score = (killed mutations / total mutations) * 100
// High score = robust tests
```

**Tools:** Stryker, mutmut, pitest

---

### Senior Questions (10-15)

#### 21. How do you design testable code?

**Answer:** Apply SOLID principles and design patterns:

```typescript
// ❌ BAD: Tight coupling
class OrderService {
  processOrder(order: Order) {
    const db = new Database(); // Hard dependency
    const email = new EmailService(); // Hard dependency
    // ...
  }
}

// ✅ GOOD: Dependency injection
class OrderService {
  constructor(
    private db: Database,
    private email: EmailService
  ) {}

  processOrder(order: Order) {
    // Dependencies are injected and can be mocked
  }
}

// ✅ GOOD: Interface-based design
interface IUserRepository {
  findById(id: string): Promise<User>;
  save(user: User): Promise<void>;
}

class UserService {
  constructor(private repo: IUserRepository) {}
}
```

**Key principles:**
- Single Responsibility Principle
- Dependency Injection
- Interface-based design
- Pure functions when possible
- Composition over inheritance

---

#### 22. How do you test microservices?

**Answer:** Use a combination of testing strategies:

```typescript
// 1. Contract Testing (between services)
describe("User Service Contract", () => {
  it("should provide user data as expected", async () => {
    const response = await request(userService).get("/api/users/1");
    expect(response.body).toMatchObject({
      id: expect.any(String),
      name: expect.any(String),
    });
  });
});

// 2. Integration Testing (with real dependencies)
describe("Order Service Integration", () => {
  it("should process order with payment", async () => {
    const order = await orderService.create({
      userId: "123",
      items: [{ productId: "456", quantity: 1 }],
    });

    expect(order.status).toBe("confirmed");
    expect(order.paymentId).toBeDefined();
  });
});

// 3. E2E Testing (critical flows)
test("complete purchase flow", async ({ page }) => {
  // Test entire user journey across services
});
```

**Testing pyramid for microservices:**
- Unit tests: 60%
- Integration tests: 25%
- Contract tests: 10%
- E2E tests: 5%

---

#### 23. How do you handle testing in CI/CD?

**Answer:** Implement a comprehensive testing pipeline:

```yaml
# .github/workflows/test.yml
name: Test Pipeline
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: testdb
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npx playwright install
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

**Best practices:**
- Run fast tests first (unit, then integration, then E2E)
- Fail fast on critical failures
- Parallelize when possible
- Cache dependencies
- Use test impact analysis

---

#### 24. How do you test security?

**Answer:** Implement security testing at multiple levels:

```typescript
// 1. Input validation testing
describe("Input Validation", () => {
  it("should prevent SQL injection", async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    const result = await service.search(maliciousInput);
    expect(result).not.toContain("DROP TABLE");
  });

  it("should prevent XSS attacks", () => {
    const xssInput = '<script>alert("xss")</script>';
    const sanitized = sanitize(xssInput);
    expect(sanitized).not.toContain("<script>");
  });
});

// 2. Authentication testing
describe("Authentication", () => {
  it("should reject expired tokens", async () => {
    const expiredToken = generateExpiredToken();
    await expect(authService.verify(expiredToken)).rejects.toThrow("Token expired");
  });

  it("should enforce rate limiting", async () => {
    const requests = Array(100).fill(null).map(() =>
      request(app).post("/api/login")
    );

    const results = await Promise.all(requests);
    const tooManyRequests = results.filter(r => r.status === 429);
    expect(tooManyRequests.length).toBeGreaterThan(0);
  });
});

// 3. Authorization testing
describe("Authorization", () => {
  it("should prevent privilege escalation", async () => {
    const userToken = generateToken({ role: "user" });
    await request(app)
      .delete("/api/users/admin")
      .set("Authorization", `Bearer ${userToken}`)
      .expect(403);
  });
});
```

---

#### 25. How do you test for performance?

**Answer:** Establish baselines and monitor key metrics:

```typescript
// 1. Load testing with k6
/*
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],   // Less than 1% failures
  },
};

export default function () {
  const res = http.get('http://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
*/

// 2. Database performance testing
describe("Query Performance", () => {
  it("should fetch users under 100ms", async () => {
    const start = performance.now();
    await db.query("SELECT * FROM users WHERE active = true");
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
  });
});
```

---

#### 26. How do you handle test data management?

**Answer:** Use factories, fixtures, and cleanup strategies:

```typescript
// Factory pattern
class UserFactory {
  static build(overrides: Partial<User> = {}): User {
    return {
      id: `user-${uuid()}`,
      name: "Test User",
      email: `test-${uuid()}@example.com`,
      ...overrides,
    };
  }

  static buildList(count: number): User[] {
    return Array.from({ length: count }, () => this.build());
  }
}

// Fixture with cleanup
class UserFixture {
  private users: User[] = [];

  async create(overrides: Partial<User> = {}): Promise<User> {
    const user = await db.users.create(UserFactory.build(overrides));
    this.users.push(user);
    return user;
  }

  async cleanup(): Promise<void> {
    for (const user of this.users) {
      await db.users.delete(user.id);
    }
    this.users = [];
  }
}

// Usage
describe("UserService", () => {
  let fixture: UserFixture;

  beforeEach(() => {
    fixture = new UserFixture();
  });

  afterEach(async () => {
    await fixture.cleanup();
  });

  it("should process user", async () => {
    const user = await fixture.create({ role: "admin" });
    // Test logic
  });
});
```

---

#### 27. How do you test infrastructure as code?

**Answer:** Use Terratest and validate configurations:

```go
// infrastructure_test.go
package test

import (
  "testing"
  "github.com/gruntwork-io/terratest/modules/terraform"
  "github.com/stretchr/testify/assert"
)

func TestTerraformVPC(t *testing.T) {
  terraformOptions := &terraform.Options{
    TerraformDir: "../modules/vpc",
    Vars: map[string]interface{}{
      "vpc_cidr": "10.0.0.0/16",
    },
  }

  defer terraform.Destroy(t, terraformOptions)
  terraform.InitAndApply(t, terraformOptions)

  vpcId := terraform.Output(t, terraformOptions, "vpc_id")
  assert.NotEmpty(t, vpcId)
}
```

**Key aspects:**
- Validate configuration syntax
- Test deployments in staging
- Verify resource creation
- Check connectivity
- Test rollback procedures

---

#### 28. How do you test real-time features?

**Answer:** Mock WebSocket connections and test event handling:

```typescript
describe("WebSocket", () => {
  let mockWebSocket: MockWebSocket;

  beforeEach(() => {
    mockWebSocket = new MockWebSocket();
    jest.spyOn(global, "WebSocket").mockImplementation(() => mockWebSocket);
  });

  it("should receive real-time updates", async () => {
    const onMessage = jest.fn();
    const service = new RealtimeService();

    service.subscribe("updates", onMessage);

    // Simulate incoming message
    mockWebSocket.simulateMessage({ type: "update", data: { id: 1 } });

    expect(onMessage).toHaveBeenCalledWith({ type: "update", data: { id: 1 } });
  });

  it("should reconnect on disconnect", async () => {
    const service = new RealtimeService();
    await service.connect();

    mockWebSocket.simulateClose();

    // Wait for reconnection attempt
    await waitFor(() => {
      expect(mockWebSocket.connect).toHaveBeenCalledTimes(2);
    });
  });
});
```

---

#### 29. How do you handle testing with complex state?

**Answer:** Test state through public interfaces, not internal state:

```typescript
// ❌ BAD: Testing internal state
it("should update internal state", () => {
  const component = render(<Counter />);
  // Don't test component.state.count
});

// ✅ GOOD: Testing behavior
it("should increment count on button click", async () => {
  const user = userEvent.setup();
  render(<Counter />);

  await user.click(screen.getByRole("button", { name: /increment/i }));

  expect(screen.getByText("Count: 1")).toBeInTheDocument();
});

// Testing complex state machines
describe("Order State Machine", () => {
  it("should transition through valid states", () => {
    const machine = new OrderStateMachine();

    expect(machine.getState()).toBe("pending");

    machine.transition("CONFIRM");
    expect(machine.getState()).toBe("confirmed");

    machine.transition("SHIP");
    expect(machine.getState()).toBe("shipped");

    machine.transition("DELIVER");
    expect(machine.getState()).toBe("delivered");
  });
});
```

---

#### 30. How do you measure test effectiveness?

**Answer:** Track multiple metrics:

```typescript
// Metrics to track
const testMetrics = {
  // Coverage metrics
  lineCoverage: 85,
  branchCoverage: 80,
  functionCoverage: 90,

  // Quality metrics
  defectEscapeRate: 2, // Defects found in production per release
  mutationScore: 75,

  // Performance metrics
  testExecutionTime: "45s",
  timeToFirstTest: "2s",

  // Maintenance metrics
  flakyTestRate: 1, // Percentage of flaky tests
  testMaintenanceTime: "2h/week",
};

// Track over time
function analyzeTestEffectiveness() {
  return {
    trend: "improving",
    coverage: "stable",
    flakiness: "decreasing",
    recommendations: [
      "Increase mutation testing score",
      "Reduce E2E test execution time",
      "Fix remaining flaky tests",
    ],
  };
}
```

---

### FAANG-style Questions (5-10)

#### 31. How would you design a testing strategy for a large-scale application?

**Answer:** Consider multiple dimensions:

```text
┌─────────────────────────────────────────────────────────────┐
│              Testing Strategy Framework                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Test Distribution                                       │
│     • Unit: 60%                                             │
│     • Integration: 25%                                      │
│     • E2E: 10%                                              │
│     • Performance: 5%                                       │
│                                                             │
│  2. Test Execution                                          │
│     • Parallel execution                                    │
│     • Test impact analysis                                  │
│     • Selective testing                                     │
│                                                             │
│  3. Test Data Management                                    │
│     • Factories and fixtures                                │
│     • Data isolation                                        │
│     • Cleanup strategies                                    │
│                                                             │
│  4. Monitoring and Metrics                                  │
│     • Coverage tracking                                     │
│     • Flakiness detection                                   │
│     • Performance monitoring                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```typescript
// Test categorization
const testCategories = {
  critical: {
    path: "src/critical/**/*.test.ts",
    coverage: 95,
    executionTime: "30s",
  },
  standard: {
    path: "src/**/*.test.ts",
    coverage: 80,
    executionTime: "2m",
  },
  e2e: {
    path: "e2e/**/*.spec.ts",
    coverage: "critical paths",
    executionTime: "10m",
  },
};

// Test impact analysis
function getTestsForChanges(changedFiles: string[]): string[] {
  // Analyze dependencies and return only affected tests
  return testAnalysis.getAffectedTests(changedFiles);
}
```

---

#### 32. How do you handle testing in a CI/CD pipeline?

**Answer:** Implement a multi-stage pipeline:

```yaml
# Pipeline stages
stages:
  - name: fast-feedback
    jobs:
      - lint
      - type-check
      - unit-tests
    timeout: 5m

  - name: integration
    jobs:
      - integration-tests
      - contract-tests
    timeout: 15m

  - name: e2e
    jobs:
      - e2e-tests
      - visual-regression
    timeout: 30m

  - name: deployment
    jobs:
      - deploy-staging
      - smoke-tests
      - deploy-production
    timeout: 60m
```

**Optimization strategies:**
- Parallel execution
- Caching dependencies
- Test splitting
- Fail fast on critical tests
- Use test impact analysis

---

#### 33. How do you ensure test reliability at scale?

**Answer:** Implement comprehensive reliability measures:

```typescript
// Flaky test detection
class FlakyTestDetector {
  private results: Map<string, boolean[]> = new Map();

  recordResult(testName: string, passed: boolean) {
    const history = this.results.get(testName) || [];
    history.push(passed);
    this.results.set(testName, history.slice(-100)); // Keep last 100 runs
  }

  getFlakyTests(): string[] {
    const flaky: string[] = [];
    for (const [name, history] of this.results) {
      const passRate = history.filter(Boolean).length / history.length;
      if (passRate > 0.1 && passRate < 0.9) {
        flaky.push(name);
      }
    }
    return flaky;
  }
}

// Quarantine system
class TestQuarantine {
  private quarantined = new Set<string>();

  quarantine(testName: string) {
    this.quarantined.add(testName);
  }

  shouldRun(testName: string): boolean {
    return !this.quarantined.has(testName);
  }
}
```

---

#### 34. How do you test complex user journeys?

**Answer:** Break down into smaller scenarios and use test data factories:

```typescript
// Complex journey test
test("complete e-commerce journey", async ({ page }) => {
  // 1. User registration
  await page.goto("/register");
  await page.fill('[data-testid="email"]', "user@test.com");
  await page.fill('[data-testid="password"]', "password123");
  await page.click('[data-testid="register"]');

  // 2. Browse products
  await page.goto("/products");
  await expect(page.locator('[data-testid="product"]')).toHaveCount(10);

  // 3. Add to cart
  await page.click('[data-testid="product-1"]');
  await page.click('[data-testid="add-to-cart"]');
  await expect(page.locator('[data-testid="cart-count"]')).toContainText("1");

  // 4. Checkout
  await page.click('[data-testid="checkout"]');
  await page.fill('[data-testid="shipping"]', "123 Main St");
  await page.fill('[data-testid="card"]', "4242424242424242");
  await page.click('[data-testid="complete-purchase"]');

  // 5. Verify confirmation
  await expect(page.locator('[data-testid="confirmation"]')).toBeVisible();
});

// Use page objects for maintainability
class CheckoutPage {
  async fillShipping(address: string) {
    await this.page.fill('[data-testid="shipping"]', address);
  }

  async completePurchase() {
    await this.page.click('[data-testid="complete-purchase"]');
  }
}
```

---

#### 35. How do you balance coverage with execution time?

**Answer:** Implement test prioritization and optimization:

```typescript
// Test prioritization
const testPriority = {
  critical: {
    businessLogic: true,
    security: true,
    userFlows: true,
  },
  important: {
    errorHandling: true,
    edgeCases: true,
  },
  nice: {
    performance: false,
    visualRegression: false,
  },
};

// Selective testing
function getTestsToRun(changedFiles: string[], timeBudget: number) {
  const allTests = getAllTests();
  const affectedTests = getAffectedTests(changedFiles);

  // Always run affected tests
  const testsToRun = [...affectedTests];

  // Fill remaining time budget with critical tests
  const remainingTime = timeBudget - estimateExecutionTime(testsToRun);
  const criticalTests = allTests
    .filter(t => t.priority === 'critical')
    .filter(t => !testsToRun.includes(t));

  for (const test of criticalTests) {
    if (estimateExecutionTime([...testsToRun, test]) <= timeBudget) {
      testsToRun.push(test);
    }
  }

  return testsToRun;
}
```

---

### Follow-up Questions (5-10)

#### 36. How has your testing approach evolved over your career?

**Answer:** Discuss your journey:

- **Early career**: Focus on coverage numbers, testing everything
- **Mid career**: Shift to behavior testing, understanding trade-offs
- **Senior**: Strategic testing, risk-based approach, mentoring others

**Key lessons learned:**
1. 100% coverage doesn't mean zero bugs
2. Test behavior, not implementation
3. Tests should provide confidence, not just coverage
4. Testing is a team responsibility
5. Pragmatism over dogmatism

---

#### 37. What testing tools have you used and why?

**Answer:** Compare tools and selection criteria:

```typescript
// Jest vs Vitest
const toolComparison = {
  jest: {
    pros: ["Mature ecosystem", "Good documentation", "Wide adoption"],
    cons: ["Slower execution", "Configuration complexity"],
    bestFor: ["Legacy projects", "Teams familiar with Jest"],
  },
  vitest: {
    pros: ["Fast execution", "Native ESM support", "Better DX"],
    cons: ["Newer, less mature", "Smaller ecosystem"],
    bestFor: ["New projects", "Vite-based applications"],
  },
};

// Testing Library vs Enzyme
const reactTestingComparison = {
  testingLibrary: {
    philosophy: "Test behavior",
    pros: ["Accessible", "Maintainable", "User-centric"],
    bestFor: ["Modern React apps"],
  },
  enzyme: {
    philosophy: "Test implementation",
    pros: ["Fine-grained control", "Shallow rendering"],
    bestFor: ["Legacy React apps", "Complex component testing"],
  },
};
```

---

#### 38. How do you handle testing legacy code?

**Answer:** Use Michael Feathers' techniques:

```typescript
// 1. Characterization tests
it("should preserve current behavior", () => {
  // Document what the code actually does
  const result = legacyFunction(input);
  expect(result).toBe(currentOutput);
});

// 2. Sprout method - extract new code
class LegacyClass {
  // Original method
  process() {
    // Legacy code
  }

  // New method for new feature
  processWithFeature() {
    this.process();
    return this.newFeature();
  }

  private newFeature() {
    // Testable new code
  }
}

// 3. Strangler fig pattern
// Gradually replace legacy code with new, tested code
```

**Strategy:**
1. Add characterization tests
2. Identify critical paths
3. Refactor incrementally
4. Add tests for new features
5. Replace legacy code gradually

---

#### 39. What's the most complex testing problem you've solved?

**Answer:** Describe a real scenario:

**Example: Testing a distributed system**

"We had a microservices architecture with event-driven communication. The challenge was testing eventual consistency and message ordering."

**Solution:**
1. Implemented contract testing between services
2. Created deterministic test data factories
3. Used test containers for integration tests
4. Implemented retry mechanisms with timeouts
5. Added distributed tracing for debugging

**Result:**
- Reduced production incidents by 60%
- Improved deployment confidence
- Faster debugging with tracing

---

#### 40. How do you teach testing to junior developers?

**Answer:** Use a progressive learning approach:

```typescript
// Week 1: Basic concepts
// - What is testing
// - AAA pattern
// - Writing simple tests

// Week 2: Tools
// - Jest basics
// - React Testing Library
// - Mocking

// Week 3: Patterns
// - Test factories
// - BDD style
// - Async testing

// Week 4: Best practices
// - Test isolation
// - Refactoring tests
// - Code review
```

**Teaching methods:**
1. Pair programming on tests
2. Code review with feedback
3. Start with simple examples
4. Gradually increase complexity
5. Share testing war stories
6. Establish team conventions

---

## Summary

These 40 questions cover the essential testing knowledge for senior full-stack interviews. Key themes:

1. **Fundamentals**: Testing pyramid, TDD/BDD, test types
2. **Tools**: Jest, React Testing Library, MSW, Cypress/Playwright
3. **Patterns**: AAA, factories, builders, fixtures
4. **Strategy**: Test distribution, CI/CD, metrics
5. **Advanced**: Microservices, security, performance
6. **Leadership**: Mentoring, legacy code, team practices

**Preparation tips:**
- Practice explaining concepts clearly
- Prepare real-world examples from your experience
- Understand trade-offs and when to apply different approaches
- Stay updated on testing trends and tools
- Focus on providing value, not just passing interviews

## References & Learn More

- "Test Driven Development: By Example" by Kent Beck
- "Working Effectively with Legacy Code" by Michael Feathers
- "The Art of Unit Testing" by Roy Osherove
- "Growing Object-Oriented Software, Guided by Tests" by Steve Freeman
- Martin Fowler's blog on testing
- Kent C. Dodds' testing articles
- Testing Library documentation
- Jest documentation
