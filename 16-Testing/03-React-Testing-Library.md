# React Testing Library

## Definition

React Testing Library (RTL) is a testing utility library for React that encourages testing components from the user's perspective rather than testing implementation details. Created by Kent C. Dodds, it provides a set of query methods and utilities that simulate how users interact with components.

**Core Philosophy**: "The more your tests resemble the way your software is used, the more confidence they can give you."

**Key Principles:**
- Test what the user sees and does, not how the component is implemented
- Prefer `getByRole` over `getByTestId` for accessibility-driven queries
- Use `userEvent` over `fireEvent` for realistic user interactions
- Focus on behavior, not implementation details
- Test accessibility by default

## Why Do We Need It?

- **User-Centric Testing**: Tests reflect real user interactions
- **Accessibility**: Queries encourage accessible component design
- **Refactoring Safe**: Tests don't break when implementation changes
- **Less Brittle**: No more testing internal state or private methods
- **Better Confidence**: Tests verify actual user-visible behavior
- **Learning Curve**: Simpler API than enzyme or other libraries
- **Maintained**: Actively maintained by Kent C. Dodds and community

## How It Works

### RTL Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Testing Library                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  Queries Layer                           ││
│  │  getByRole  getByLabelText  getByText  queryByRole      ││
│  │  findByRole findByLabelText findByText queryByText      ││
│  │  getAllByRole getAllByText   queryAllByRole              ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  Actions Layer                           ││
│  │  userEvent.click  userEvent.type  userEvent.tab         ││
│  │  userEvent.keyboard  userEvent.hover  userEvent.upload  ││
│  │  fireEvent.click  fireEvent.change  fireEvent.submit    ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  Assertions Layer                        ││
│  │  toBeInTheDocument  toHaveTextContent                  ││
│  │  toHaveAttribute    toHaveClass                        ││
│  │  toBeVisible        toHaveFocus                        ││
│  │  toHaveValue        toBeDisabled                       ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  DOM Wrappers                            ││
│  │  render()  screen  cleanup  act()                      ││
│  │  within()  renderHook()                                ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Query Priority Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                  Query Priority (Best to Worst)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. getByRole      │  Accessible roles (button, heading)   │
│     ↓              │                                        │
│  2. getByLabelText │  Form elements with labels            │
│     ↓              │                                        │
│  3. getByPlaceholderText │  Placeholders (less preferred)  │
│     ↓              │                                        │
│  4. getByText      │  Visible text content                 │
│     ↓              │                                        │
│  5. getByDisplayValue │  Form current values               │
│     ↓              │                                        │
│  6. getByAltText   │  Images and media                     │
│     ↓              │                                        │
│  7. getByTitle     │  Titles (tooltip, dialog)             │
│     ↓              │                                        │
│  8. getByTestId    │  Test IDs (last resort)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Testing User Flow

```
User Interaction Flow:
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Render  │────▶│  Find    │────▶│  Interact│────▶│  Assert  │
│  Component│    │  Elements│     │  (user   │     │  Results │
│          │     │  (queries)│    │   Event) │     │          │
└──────────┘     └──────────┘     └──────────┘     └──────────┘

Example:
render(<LoginForm />)  →  getByRole('button', {name: /login/i})
                        →  userEvent.click(button)
                        →  expect(mockSubmit).toHaveBeenCalled()
```

## Code Examples

### Basic Component Testing

```typescript
// Counter.tsx
import React, { useState } from "react";

interface CounterProps {
  initialCount?: number;
  step?: number;
  onChange?: (count: number) => void;
}

export const Counter: React.FC<CounterProps> = ({
  initialCount = 0,
  step = 1,
  onChange,
}) => {
  const [count, setCount] = useState(initialCount);

  const increment = () => {
    const newCount = count + step;
    setCount(newCount);
    onChange?.(newCount);
  };

  const decrement = () => {
    const newCount = count - step;
    setCount(newCount);
    onChange?.(newCount);
  };

  const reset = () => {
    setCount(initialCount);
    onChange?.(initialCount);
  };

  return (
    <div role="group" aria-label="Counter">
      <h2>Count: {count}</h2>
      <button onClick={decrement} aria-label="Decrease count">
        -
      </button>
      <button onClick={increment} aria-label="Increase count">
        +
      </button>
      <button onClick={reset} aria-label="Reset count">
        Reset
      </button>
    </div>
  );
};

// Counter.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

describe("Counter", () => {
  it("should render with initial count of 0", () => {
    render(<Counter />);

    expect(screen.getByRole("heading", { name: /count: 0/i })).toBeInTheDocument();
  });

  it("should render with custom initial count", () => {
    render(<Counter initialCount={10} />);

    expect(screen.getByRole("heading", { name: /count: 10/i })).toBeInTheDocument();
  });

  it("should increment count when + button clicked", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    const incrementButton = screen.getByRole("button", { name: /increase count/i });
    await user.click(incrementButton);

    expect(screen.getByRole("heading", { name: /count: 1/i })).toBeInTheDocument();
  });

  it("should decrement count when - button clicked", async () => {
    const user = userEvent.setup();
    render(<Counter initialCount={5} />);

    const decrementButton = screen.getByRole("button", { name: /decrease count/i });
    await user.click(decrementButton);

    expect(screen.getByRole("heading", { name: /count: 4/i })).toBeInTheDocument();
  });

  it("should reset to initial count", async () => {
    const user = userEvent.setup();
    render(<Counter initialCount={10} />);

    const incrementButton = screen.getByRole("button", { name: /increase count/i });
    await user.click(incrementButton); // 11
    await user.click(incrementButton); // 12

    const resetButton = screen.getByRole("button", { name: /reset count/i });
    await user.click(resetButton);

    expect(screen.getByRole("heading", { name: /count: 10/i })).toBeInTheDocument();
  });

  it("should use custom step value", async () => {
    const user = userEvent.setup();
    render(<Counter step={5} />);

    const incrementButton = screen.getByRole("button", { name: /increase count/i });
    await user.click(incrementButton);

    expect(screen.getByRole("heading", { name: /count: 5/i })).toBeInTheDocument();
  });

  it("should call onChange with new count", async () => {
    const onChange = jest.fn();
    const user = userEvent.setup();
    render(<Counter onChange={onChange} />);

    const incrementButton = screen.getByRole("button", { name: /increase count/i });
    await user.click(incrementButton);

    expect(onChange).toHaveBeenCalledWith(1);
  });
});
```

### Form Component Testing

```typescript
// LoginForm.tsx
import React, { useState } from "react";

interface LoginFormProps {
  onSubmit: (data: { email: string; password: string }) => void;
  error?: string;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, error }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

  const validate = () => {
    const newErrors: { email?: string; password?: string } = {};

    if (!email) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Invalid email format";
    }

    if (!password) {
      newErrors.password = "Password is required";
    } else if (password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit({ email, password });
    }
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Login form">
      {error && <div role="alert">{error}</div>}

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert">
            {errors.email}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? "password-error" : undefined}
        />
        {errors.password && (
          <span id="password-error" role="alert">
            {errors.password}
          </span>
        )}
      </div>

      <button type="submit">Login</button>
    </form>
  );
};

// LoginForm.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("should render all form elements", () => {
    render(<LoginForm onSubmit={jest.fn()} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  });

  it("should show validation errors for empty fields", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText("Email is required")).toBeInTheDocument();
      expect(screen.getByText("Password is required")).toBeInTheDocument();
    });
  });

  it("should show error for invalid email format", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.type(screen.getByLabelText(/email/i), "invalidemail");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText("Invalid email format")).toBeInTheDocument();
    });
  });

  it("should show error for short password", async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.type(screen.getByLabelText(/email/i), "user@example.com");
    await user.type(screen.getByLabelText(/password/i), "123");
    await user.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText("Password must be at least 6 characters")).toBeInTheDocument();
    });
  });

  it("should submit form with valid data", async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();
    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), "user@example.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: "user@example.com",
        password: "password123",
      });
    });
  });

  it("should display server error when provided", () => {
    render(<LoginForm onSubmit={jest.fn()} error="Invalid credentials" />);

    expect(screen.getByRole("alert")).toHaveTextContent("Invalid credentials");
  });
});
```

### Async Component Testing

```typescript
// UserProfile.tsx
import React, { useEffect, useState } from "react";

interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
}

interface UserProfileProps {
  userId: string;
  onEdit?: (userId: string) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId, onEdit }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch user");
        }
        const data = await response.json();
        setUser(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  if (loading) {
    return <div role="status">Loading...</div>;
  }

  if (error) {
    return <div role="alert">{error}</div>;
  }

  if (!user) {
    return <div>User not found</div>;
  }

  return (
    <article aria-label="User profile">
      <img src={user.avatar} alt={`${user.name}'s avatar`} />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={() => onEdit(user.id)}>Edit Profile</button>
      )}
    </article>
  );
};

// UserProfile.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { rest } from "msw";
import { setupServer } from "msw/node";
import { UserProfile } from "./UserProfile";

const mockUser = {
  id: "123",
  name: "John Doe",
  email: "john@example.com",
  avatar: "https://example.com/avatar.jpg",
};

const server = setupServer(
  rest.get("/api/users/:userId", (req, res, ctx) => {
    return res(ctx.json(mockUser));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("UserProfile", () => {
  it("should show loading state initially", () => {
    render(<UserProfile userId="123" />);

    expect(screen.getByRole("status")).toHaveTextContent("Loading...");
  });

  it("should display user profile after loading", async () => {
    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: /john doe/i })).toBeInTheDocument();
    });

    expect(screen.getByText("john@example.com")).toBeInTheDocument();
    expect(screen.getByRole("img", { name: /john doe's avatar/i })).toBeInTheDocument();
  });

  it("should display error when fetch fails", async () => {
    server.use(
      rest.get("/api/users/:userId", (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Failed to fetch user");
    });
  });

  it("should call onEdit when edit button clicked", async () => {
    const onEdit = jest.fn();
    const user = userEvent.setup();

    render(<UserProfile userId="123" onEdit={onEdit} />);

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: /john doe/i })).toBeInTheDocument();
    });

    await user.click(screen.getByRole("button", { name: /edit profile/i }));

    expect(onEdit).toHaveBeenCalledWith("123");
  });

  it("should not render edit button when onEdit not provided", async () => {
    render(<UserProfile userId="123" />);

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: /john doe/i })).toBeInTheDocument();
    });

    expect(screen.queryByRole("button", { name: /edit profile/i })).not.toBeInTheDocument();
  });
});
```

### Component with Context

```typescript
// ThemeContext.tsx
import React, { createContext, useContext, useState } from "react";

type Theme = "light" | "dark";

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [theme, setTheme] = useState<Theme>("light");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};

// ThemedCard.tsx
import React from "react";
import { useTheme } from "./ThemeContext";

interface ThemedCardProps {
  title: string;
  children: React.ReactNode;
}

export const ThemedCard: React.FC<ThemedCardProps> = ({ title, children }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div
      className={`card ${theme}`}
      role="article"
      aria-label={`Card with theme ${theme}`}
    >
      <h3>{title}</h3>
      <div className="content">{children}</div>
      <button onClick={toggleTheme}>
        Switch to {theme === "light" ? "dark" : "light"} mode
      </button>
    </div>
  );
};

// ThemedCard.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ThemeProvider } from "./ThemeContext";
import { ThemedCard } from "./ThemedCard";

const renderWithTheme = (ui: React.ReactElement) => {
  return render(<ThemeProvider>{ui}</ThemeProvider>);
};

describe("ThemedCard", () => {
  it("should render with default light theme", () => {
    renderWithTheme(
      <ThemedCard title="Test Card">Content</ThemedCard>
    );

    const card = screen.getByRole("article");
    expect(card).toHaveClass("card", "light");
    expect(screen.getByRole("heading", { name: /test card/i })).toBeInTheDocument();
  });

  it("should toggle theme when button clicked", async () => {
    const user = userEvent.setup();
    renderWithTheme(
      <ThemedCard title="Test Card">Content</ThemedCard>
    );

    const toggleButton = screen.getByRole("button", { name: /switch to dark mode/i });
    await user.click(toggleButton);

    const card = screen.getByRole("article");
    expect(card).toHaveClass("card", "dark");
    expect(screen.getByRole("button", { name: /switch to light mode/i })).toBeInTheDocument();
  });
});
```

### Complex Form with React Hook Form

```typescript
// RegistrationForm.tsx
import React from "react";
import { useForm } from "react-hook-form";

interface RegistrationFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  acceptTerms: boolean;
}

interface RegistrationFormProps {
  onSubmit: (data: RegistrationFormData) => void;
}

export const RegistrationForm: React.FC<RegistrationFormProps> = ({
  onSubmit,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegistrationFormData>();

  return (
    <form onSubmit={handleSubmit(onSubmit)} aria-label="Registration form">
      <div>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          {...register("username", {
            required: "Username is required",
            minLength: {
              value: 3,
              message: "Username must be at least 3 characters",
            },
          })}
          aria-invalid={!!errors.username}
          aria-describedby={errors.username ? "username-error" : undefined}
        />
        {errors.username && (
          <span id="username-error" role="alert">
            {errors.username.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register("email", {
            required: "Email is required",
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: "Invalid email format",
            },
          })}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {errors.email && (
          <span id="email-error" role="alert">
            {errors.email.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register("password", {
            required: "Password is required",
            minLength: {
              value: 8,
              message: "Password must be at least 8 characters",
            },
          })}
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? "password-error" : undefined}
        />
        {errors.password && (
          <span id="password-error" role="alert">
            {errors.password.message}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          type="password"
          {...register("confirmPassword", {
            required: "Please confirm your password",
          })}
          aria-invalid={!!errors.confirmPassword}
          aria-describedby={
            errors.confirmPassword ? "confirm-password-error" : undefined
          }
        />
        {errors.confirmPassword && (
          <span id="confirm-password-error" role="alert">
            {errors.confirmPassword.message}
          </span>
        )}
      </div>

      <div>
        <label>
          <input
            type="checkbox"
            {...register("acceptTerms", {
              required: "You must accept the terms",
            })}
          />
          I accept the terms and conditions
        </label>
        {errors.acceptTerms && (
          <span role="alert">{errors.acceptTerms.message}</span>
        )}
      </div>

      <button type="submit">Register</button>
    </form>
  );
};

// RegistrationForm.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { RegistrationForm } from "./RegistrationForm";

describe("RegistrationForm", () => {
  it("should submit with valid data", async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();
    render(<RegistrationForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/username/i), "johndoe");
    await user.type(screen.getByLabelText(/email/i), "john@example.com");
    await user.type(screen.getByLabelText(/^password$/i), "password123");
    await user.type(screen.getByLabelText(/confirm password/i), "password123");
    await user.click(screen.getByLabelText(/accept terms/i));
    await user.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        username: "johndoe",
        email: "john@example.com",
        password: "password123",
        confirmPassword: "password123",
        acceptTerms: true,
      });
    });
  });

  it("should show validation errors", async () => {
    const user = userEvent.setup();
    render(<RegistrationForm onSubmit={jest.fn()} />);

    await user.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(screen.getByText("Username is required")).toBeInTheDocument();
      expect(screen.getByText("Email is required")).toBeInTheDocument();
      expect(screen.getByText("Password is required")).toBeInTheDocument();
      expect(screen.getByText("Please confirm your password")).toBeInTheDocument();
      expect(screen.getByText("You must accept the terms")).toBeInTheDocument();
    });
  });
});
```

### Custom Hook Testing

```typescript
// useCounter.ts
import { useState, useCallback } from "react";

interface UseCounterOptions {
  initialValue?: number;
  step?: number;
  min?: number;
  max?: number;
}

export function useCounter({
  initialValue = 0,
  step = 1,
  min = -Infinity,
  max = Infinity,
}: UseCounterOptions = {}) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount((prev) => Math.min(prev + step, max));
  }, [step, max]);

  const decrement = useCallback(() => {
    setCount((prev) => Math.max(prev - step, min));
  }, [step, min]);

  const reset = useCallback(() => {
    setCount(initialValue);
  }, [initialValue]);

  return {
    count,
    increment,
    decrement,
    reset,
    isAtMin: count <= min,
    isAtMax: count >= max,
  };
}

// useCounter.test.ts
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

describe("useCounter", () => {
  it("should initialize with default value", () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it("should initialize with custom value", () => {
    const { result } = renderHook(() => useCounter({ initialValue: 10 }));
    expect(result.current.count).toBe(10);
  });

  it("should increment count", () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it("should decrement count", () => {
    const { result } = renderHook(() => useCounter({ initialValue: 5 }));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it("should reset count", () => {
    const { result } = renderHook(() => useCounter({ initialValue: 10 }));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(12);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });

  it("should respect min and max bounds", () => {
    const { result } = renderHook(() =>
      useCounter({ initialValue: 5, min: 0, max: 10 })
    );

    expect(result.current.isAtMin).toBe(false);
    expect(result.current.isAtMax).toBe(false);

    // Decrement to min
    act(() => {
      result.current.decrement();
      result.current.decrement();
      result.current.decrement();
      result.current.decrement();
      result.current.decrement();
    });

    expect(result.current.count).toBe(0);
    expect(result.current.isAtMin).toBe(true);

    // Try to go below min
    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(0);

    // Increment to max
    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(10);
    expect(result.current.isAtMax).toBe(true);

    // Try to go above max
    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(10);
  });
});
```

### Testing with Mock Service Worker

```typescript
// api.ts
export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}

export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch("/api/products");
  if (!response.ok) {
    throw new Error("Failed to fetch products");
  }
  return response.json();
}

export async function createProduct(
  product: Omit<Product, "id">
): Promise<Product> {
  const response = await fetch("/api/products", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(product),
  });
  if (!response.ok) {
    throw new Error("Failed to create product");
  }
  return response.json();
}

// handlers.ts
import { rest } from "msw";

const mockProducts = [
  { id: "1", name: "Widget", price: 9.99, description: "A useful widget" },
  { id: "2", name: "Gadget", price: 24.99, description: "An amazing gadget" },
];

export const handlers = [
  rest.get("/api/products", (req, res, ctx) => {
    return res(ctx.json(mockProducts));
  }),

  rest.post("/api/products", async (req, res, ctx) => {
    const newProduct = await req.json();
    return res(
      ctx.json({ ...newProduct, id: String(mockProducts.length + 1) })
    );
  }),
];

// ProductList.tsx
import React, { useEffect, useState } from "react";
import { fetchProducts, Product } from "./api";

export const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div role="status">Loading products...</div>;
  if (error) return <div role="alert">{error}</div>;

  return (
    <ul aria-label="Product list">
      {products.map((product) => (
        <li key={product.id}>
          <h3>{product.name}</h3>
          <p>${product.price}</p>
          <p>{product.description}</p>
        </li>
      ))}
    </ul>
  );
};

// ProductList.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import { rest } from "msw";
import { setupServer } from "msw/node";
import { ProductList } from "./ProductList";
import { handlers } from "./handlers";

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("ProductList", () => {
  it("should display products after loading", async () => {
    render(<ProductList />);

    await waitFor(() => {
      expect(screen.getByRole("status")).not.toBeInTheDocument();
    });

    const list = screen.getByRole("list", { name: /product list/i });
    expect(list).toBeInTheDocument();

    expect(screen.getByRole("heading", { name: /widget/i })).toBeInTheDocument();
    expect(screen.getByText("$9.99")).toBeInTheDocument();
  });

  it("should display error message on fetch failure", async () => {
    server.use(
      rest.get("/api/products", (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    render(<ProductList />);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Failed to fetch products");
    });
  });

  it("should display loading state initially", () => {
    render(<ProductList />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading products...");
  });
});
```

## Real-World Use Cases

### 1. Testing a Complete User Flow

```typescript
// CheckoutFlow.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { CheckoutFlow } from "./CheckoutFlow";

const renderWithRouter = (ui: React.ReactElement) => {
  return render(<MemoryRouter>{ui}</MemoryRouter>);
};

describe("Checkout Flow", () => {
  it("should complete full checkout process", async () => {
    const user = userEvent.setup();
    renderWithRouter(<CheckoutFlow />);

    // Step 1: Cart
    expect(screen.getByText(/step 1/i)).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /continue to shipping/i }));

    // Step 2: Shipping
    await waitFor(() => {
      expect(screen.getByText(/step 2/i)).toBeInTheDocument();
    });
    await user.type(screen.getByLabelText(/address/i), "123 Main St");
    await user.type(screen.getByLabelText(/city/i), "Springfield");
    await user.click(screen.getByRole("button", { name: /continue to payment/i }));

    // Step 3: Payment
    await waitFor(() => {
      expect(screen.getByText(/step 3/i)).toBeInTheDocument();
    });
    await user.type(screen.getByLabelText(/card number/i), "4242424242424242");
    await user.click(screen.getByRole("button", { name: /complete order/i }));

    // Confirmation
    await waitFor(() => {
      expect(screen.getByText(/order confirmed/i)).toBeInTheDocument();
    });
  });
});
```

## Common Mistakes

### 1. Using Wrong Queries

```typescript
// ❌ BAD: Using getByTestId
<div data-testid="user-name">John</div>
expect(screen.getByTestId("user-name")).toHaveTextContent("John");

// ✅ GOOD: Using getByRole or getByText
<div role="heading" aria-level={2}>John</div>
expect(screen.getByRole("heading", { name: /john/i })).toBeInTheDocument();
```

### 2. Not Using userEvent

```typescript
// ❌ BAD: Using fireEvent
fireEvent.click(button);

// ✅ GOOD: Using userEvent
const user = userEvent.setup();
await user.click(button);
```

### 3. Testing Implementation Details

```typescript
// ❌ BAD: Testing internal state
expect(component.state.isLoading).toBe(true);

// ✅ GOOD: Testing visible output
expect(screen.getByRole("status")).toHaveTextContent("Loading...");
```

## Best Practices

1. **Query by role, label, or text** before test ID
2. **Use `userEvent`** for realistic interactions
3. **Test accessibility** by default
4. **Avoid testing implementation details**
5. **Use `waitFor`** for async operations
6. **Mock at the network level** with MSW when possible
7. **Use `screen`** instead of destructuring `render`
8. **Test error states** and loading states
9. **Keep tests focused** on one behavior
10. **Use custom render functions** for providers

## Performance Considerations

### Efficient Testing

```typescript
// ❌ BAD: Rendering entire app for simple test
import { App } from "./App";
render(<App />);

// ✅ GOOD: Render only the component under test
import { Button } from "./Button";
render(<Button onClick={jest.fn()}>Click me</Button>);

// ❌ BAD: Using waitFor with short timeout
await waitFor(() => {}, { timeout: 100 });

// ✅ GOOD: Use default or appropriate timeout
await waitFor(() => {});
```

## Interview Questions

### Beginner (5-10)

1. **What is React Testing Library?**
   RTL is a testing utility that provides DOM queries and utilities for testing React components from the user's perspective.

2. **Why is RTL preferred over Enzyme?**
   RTL encourages testing behavior over implementation, is easier to learn, and promotes accessibility by default.

3. **What is `screen` in RTL?**
   `screen` is an object containing queries bound to the entire document, making tests more readable.

4. **What is the difference between `getBy` and `queryBy`?**
   `getBy` throws an error if element not found. `queryBy` returns null if not found, useful for asserting absence.

5. **How do you test async components?**
   Use `waitFor` or `findBy` queries to wait for async operations to complete.

6. **What is `userEvent`?**
   `userEvent` simulates real user interactions with better accuracy than `fireEvent`.

7. **How do you test form submissions?**
   Use `userEvent.type` for inputs and `userEvent.click` for submit buttons, then verify results.

8. **What is `cleanup` in RTL?**
   `cleanup` unmounts React trees rendered in the document, called automatically after each test.

9. **How do you test components with Context?**
   Wrap the component with the provider in a custom render function.

10. **What are `findBy` queries?**
    `findBy` queries return promises that resolve when elements are found, useful for async content.

### Intermediate (5-10)

11. **How do you test loading states?**
    Render the component, check for loading indicator, then use `waitFor` to wait for content.

12. **How do you test error boundaries?**
    Render a component that throws, verify fallback UI renders.

13. **How do you test with React Router?**
    Wrap component with `MemoryRouter` or use custom render with router context.

14. **How do you test custom hooks?**
    Use `renderHook` from `@testing-library/react-hooks`.

15. **How do you mock API calls?**
    Use MSW (Mock Service Worker) for network-level mocking.

16. **How do you test accessibility?**
    Use `jest-axe` to run accessibility audits on rendered components.

17. **How do you test animations?**
    Mock timer functions and verify state changes at specific times.

18. **How do you test portals?**
    RTL automatically handles portals, query within the portal content.

19. **How do you test drag and drop?**
    Use `@testing-library/user-event` v14+ which supports drag and drop.

20. **How do you test file uploads?**
    Create a `File` object and use `userEvent.upload`.

### Senior (10-15)

21. **How do you test a component library?**
    Test each component in isolation, verify accessibility, and test various prop combinations.

22. **How do you handle testing with internationalization?**
    Mock i18n providers, test different language outputs.

23. **How do you test server-side rendering?**
    Use `@testing-library/react` with `renderToString` and verify HTML output.

24. **How do you test performance?**
    Use `React.Profiler` and measure render times.

25. **How do you test complex state management?**
    Test state changes through user interactions, not internal state.

26. **How do you test with GraphQL?**
    Use `msw` to mock GraphQL responses.

27. **How do you test with WebSockets?**
    Mock WebSocket connections and simulate messages.

28. **How do you test with Redux?**
    Wrap component with `Provider` and test through user interactions.

29. **How do you test with Formik?**
    Test form submissions and validation through user interactions.

30. **How do you test complex animations?**
    Use `jest.useFakeTimers()` and verify DOM changes at specific times.

### FAANG-style (5-10)

31. **How would you design a testing strategy for a design system?**
    Test component API, accessibility, visual regression, and integration with consuming apps.

32. **How do you handle testing micro-frontends?**
    Use contract testing between micro-frontends and test shared dependencies.

33. **How do you ensure test reliability at scale?**
    Implement flaky test detection, quarantine system, and test stability metrics.

34. **How do you test with complex forms (multi-step, conditional)?**
    Test each step independently and verify state persistence between steps.

35. **How do you test with real-time features?**
    Mock WebSocket connections, test reconnection logic, and verify UI updates.

### Follow-ups (5-10)

36. **How has RTL changed your testing approach?**
    Discuss shift from testing implementation to testing behavior.

37. **What custom utilities have you created with RTL?**
    Custom render functions, query helpers, and assertion utilities.

38. **How do you handle testing legacy components with RTL?**
    Gradual migration strategy, wrapper components for context.

39. **What are the limitations of RTL?**
    Difficult to test certain animations, complex drag-and-drop, and canvas elements.

40. **How do you contribute to RTL's ecosystem?**
    Creating custom queries, sharing patterns, and helping others.

## Summary

React Testing Library is the standard for testing React applications because it:

- **Encourages accessible code** through role-based queries
- **Tests behavior** not implementation details
- **Provides realistic interactions** with userEvent
- **Is easy to learn** with a simple API
- **Has excellent documentation** and community support

Key takeaways:
- Query by role, label, or text before test ID
- Use `userEvent` for realistic user interactions
- Test what the user sees, not how the component is implemented
- Mock at the network level when possible
- Keep tests focused and maintainable

## References & Learn More

- [React Testing Library Documentation](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Library Query Priority](https://testing-library.com/docs/queries/about#priority)
- [Kent C. Dodds' Blog](https://kentcdodds.com/blog/)
- [Testing JavaScript Course](https://testingjavascript.com/)
